from __future__ import annotations

import shlex
import time

from .baselines import BASELINES
from .protocol import SubprocessAdapter
from .segmenter import canonical_document


def run_case(case, engine_name, command=None):
    canonical, blocks = canonical_document(case.script)
    original_text = case.script if isinstance(case.script, str) else case.script.get("text", "\n".join(b["text"] for b in blocks))
    initial = case.metadata.get("initial_segment_index", 0)
    if command:
        adapter = SubprocessAdapter(shlex.split(command))
        engine = None
    else:
        engine = BASELINES[engine_name]()
        engine.load_script(original_text, initial, segments=[s["text"] for s in canonical], segment_indices=[s["index"] for s in canonical])
        adapter = None

    expected = {e.event_index: e for e in case.expectations}
    rows = []
    previous = initial
    expected_anchor = initial
    segment_count = len(canonical)
    structured_blocks = case.script.get("blocks", []) if isinstance(case.script, dict) else []
    region = case.metadata.get(
        "region_kind",
        "non_spoken_region" if any(b.get("speech_policy") == "skip" for b in structured_blocks) else "spoken_only",
    )
    try:
        for i, event in enumerate(case.events):
            if adapter and i == 0:
                sections = case.metadata.get("sections", [])
                segment_records = []
                for record in canonical:
                    section = next((s for s in sections if s.get("start_segment", 0) <= record["index"] <= s.get("end_segment", -1)), {})
                    heading_indices = section.get("heading_segments", [])
                    segment_records.append({**record, "section_id": section.get("id"), "role": "heading" if record["index"] in heading_indices else "content", "navigation_only": record["index"] in section.get("navigation_only_segments", [])})
                adapter.send({"type": "load_script", "script_id": case.script.get("id", case.id) if isinstance(case.script, dict) else case.id, "text": original_text, "blocks": blocks, "segments": segment_records, "sections": sections, "initial_segment_index": initial})

            event_data = {k: v for k, v in event.__dict__.items() if v is not None}
            started = time.perf_counter_ns()
            pred = adapter.process_event(event_data) if adapter else engine.process_event(event_data).__dict__
            latency_us = (time.perf_counter_ns() - started) // 1000
            if "segment_index" not in pred:
                raise ValueError(f"prediction at event {i} lacks segment_index")
            idx = int(pred["segment_index"])
            if not 0 <= idx < segment_count:
                raise ValueError(f"prediction at event {i} has out-of-range segment_index {idx} for {segment_count} segments")
            confidence = pred.get("confidence")
            if confidence is not None and not 0.0 <= float(confidence) <= 1.0:
                raise ValueError(f"prediction at event {i} has confidence outside [0, 1]")
            candidate_index = pred.get("candidate_index")
            if candidate_index is not None and not 0 <= int(candidate_index) < segment_count:
                raise ValueError(f"prediction at event {i} has out-of-range candidate_index {candidate_index}")
            jump_evidence = pred.get("jump_evidence")
            if jump_evidence is not None and int(jump_evidence) < 0:
                raise ValueError(f"prediction at event {i} has negative jump_evidence")
            state = pred.get("state") or "locked"
            if state not in ("locked", "suspect_jump", "confirmed_jump", "uncertain", "lost", "recovered"):
                raise ValueError(f"unknown state: {state}")
            jump_status = pred.get("jump_status", "none")
            if jump_status not in ("none", "suspected", "confirmed", "cancelled"):
                raise ValueError(f"unknown jump_status: {jump_status}")

            ex = expected.get(i)
            acceptable = ([ex.expected_segment] if ex and ex.expected_segment is not None else []) + (ex.acceptable_segments or [] if ex else [])
            correct = ex is None or ex.expected_segment is None or idx in acceptable
            expected_text = canonical[ex.expected_segment]["text"] if ex and ex.expected_segment is not None and ex.expected_segment < segment_count else None
            occurrence = (case.metadata.get("expected_occurrence") or {}).get(str(i))
            if occurrence is None and case.category == "duplicate" and ex and ex.expected_segment is not None:
                occurrence = ex.expected_segment
            block_language = canonical[ex.expected_segment].get("language_hint") if ex and ex.expected_segment is not None else None
            raw_language = (block_language if block_language and block_language != "auto" else None) or case.metadata.get("language_hint") or case.metadata.get("language", "auto")
            lowered_language = raw_language.lower()
            language = "mixed" if lowered_language == "mixed" else "en" if lowered_language.startswith("en") else "zh" if lowered_language.startswith("zh") else lowered_language
            rows.append({
                "case_id": case.id,
                "category": case.category,
                "intent": case.metadata.get("intent") or ("skip" if case.category in ("intentional_skip", "section_jump", "forgotten_then_skip") else "pause" if case.category == "forgotten_word_pause" else "mistake" if case.category in ("accidental_future_phrase", "false_jump_candidate", "jump_cancellation") else None),
                "skip_distance": case.metadata.get("skip_distance"),
                "language": language,
                "region": region,
                "event_index": i,
                "event_type": event.type,
                "text": event.text,
                "expected": ex.expected_segment if ex else None,
                "expected_segment_text": expected_text,
                "acceptable_segments": ex.acceptable_segments if ex else None,
                "expected_occurrence": occurrence,
                "predicted_occurrence": idx if occurrence is not None else None,
                "speech_policy_context": case.metadata.get("speech_policy_context"),
                "should_move": ex.should_move if ex else None,
                "should_be_lost": ex.should_be_lost if ex else None,
                "expected_state": ex.expected_state if ex else None,
                "expected_jump_status": ex.expected_jump_status if ex else None,
                "expected_candidate_index": ex.expected_candidate_index if ex else None,
                "expected_jump_evidence": ex.expected_jump_evidence if ex else None,
                "expected_candidate_distance": (ex.expected_candidate_index - expected_anchor) if ex and ex.expected_candidate_index is not None else None,
                "predicted_candidate_distance": (int(candidate_index) - previous) if candidate_index is not None else None,
                "predicted": idx,
                "moved": idx != previous,
                "moved_forward_wrong": idx > previous and not correct,
                "moved_backward_wrong": idx < previous and not correct,
                "segment_error": None if ex is None or ex.expected_segment is None else min(abs(idx - x) for x in acceptable),
                "jump_distance": idx - previous,
                "movement_type": "forward" if idx > previous else "backward" if idx < previous else "hold",
                "confidence": float(confidence) if confidence is not None else None,
                "state": state,
                "jump_status": jump_status,
                "candidate_index": candidate_index,
                "jump_evidence": jump_evidence,
                "score": pred.get("score"),
                "latency_us": int(latency_us),
            })
            previous = idx
            if ex and ex.expected_segment is not None and ex.expected_jump_status not in ("suspected", "cancelled"):
                expected_anchor = ex.expected_segment
        return rows
    finally:
        if adapter:
            adapter.close()
