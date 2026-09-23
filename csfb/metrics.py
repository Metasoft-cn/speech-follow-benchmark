from __future__ import annotations

import math
import statistics


def percentile(values, fraction):
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, math.ceil(fraction * len(ordered)) - 1)
    return ordered[index]


def _expected_set(row):
    return [row["expected"]] + (row.get("acceptable_segments") or [])


def _error(row):
    return min(abs(row["predicted"] - expected) for expected in _expected_set(row))


def _accuracy(rows, tolerance=0):
    if not rows:
        return None
    return sum(_error(row) <= tolerance for row in rows) / len(rows)


def _group_accuracy(rows, field):
    grouped = {}
    labels = sorted({str(row.get(field) or "unknown") for row in rows})
    for label in labels:
        group = [row for row in rows if str(row.get(field) or "unknown") == label]
        judged = [row for row in group if row.get("expected") is not None]
        finals = [row for row in judged if row.get("event_type") == "final"]
        grouped[label] = {
            "event_accuracy": _accuracy(judged),
            "final_accuracy": _accuracy(finals),
            "judged_events": len(judged),
            "final_events": len(finals),
        }
    return grouped


def score(rows):
    """Compute separate tracking metrics and language/region breakdowns."""
    result = _score_core(rows)
    result["by_language"] = _group_accuracy(rows, "language")
    result["by_region"] = _group_accuracy(rows, "region")
    return result


def _score_core(rows):
    judged = [row for row in rows if row.get("expected") is not None]
    finals = [row for row in judged if row.get("event_type") == "final"]
    errors = [_error(row) for row in judged]
    confidence_rows = [row for row in judged if row.get("confidence") is not None]
    high_confidence = [row for row in confidence_rows if row["confidence"] >= 0.8]

    confirmed = [row for row in rows if row.get("expected_jump_status") == "confirmed"]
    cancelled = [row for row in rows if row.get("expected_jump_status") == "cancelled"]
    should_candidate = [row for row in rows if row.get("expected_jump_status") in ("suspected", "confirmed")]
    should_not_candidate = [row for row in rows if row.get("expected_jump_status") in ("none", "cancelled")]
    state_labeled = [row for row in rows if row.get("expected_state") is not None]
    candidate_labeled = [row for row in rows if row.get("expected_candidate_index") is not None]
    # Evidence-count labels describe the evidence available when a candidate is
    # first suspected. Confirmation events may include the confirmation signal
    # itself, so their accumulated count is not comparable to this label.
    evidence_labeled = [
        row for row in candidate_labeled
        if row.get("expected_jump_evidence") is not None
        and row.get("expected_jump_status") == "suspected"
    ]
    duplicate_labeled = [row for row in rows if row.get("expected_occurrence") is not None]

    # A suspected candidate is still a no-commit event when the expected anchor
    # must hold. Count a large wrong movement here as a false jump commit.
    false_jump_labeled = [
        row for row in rows
        if row.get("expected_jump_status") in ("none", "suspected", "cancelled")
        and row.get("expected") is not None
        and (row.get("should_move") is False or row.get("expected_jump_status") != "suspected")
    ]

    wrong_forward = [row for row in judged if row.get("moved_forward_wrong")]
    wrong_backward = [row for row in judged if row.get("moved_backward_wrong")]
    catastrophic_absolute = [row for row in judged if _error(row) >= 5]
    catastrophic_backward = [row for row in judged if row["predicted"] < min(_expected_set(row)) - 2]

    lost = [row for row in rows if row.get("state") == "lost"]
    lost_labeled = [row for row in rows if row.get("should_be_lost") is not None]
    false_lost = [row for row in lost_labeled if row.get("state") == "lost" and row["should_be_lost"] is False]
    false_lost_denominator = sum(row["should_be_lost"] is False for row in lost_labeled)
    should_hold = [row for row in rows if row.get("should_move") is False]
    wrong_movement = [row for row in should_hold if row.get("moved")]

    false_jump_commits = [
        row for row in false_jump_labeled
        if row.get("movement_type") == "forward"
        and row.get("jump_distance", 0) >= 3
        and _error(row) > 0
    ]

    by_case = {}
    for row in rows:
        by_case.setdefault(row["case_id"], []).append(row)

    recovery_events = []
    lost_cases = 0
    recovered_cases = 0
    for sequence in by_case.values():
        sequence.sort(key=lambda row: row["event_index"])
        lost_at = next((i for i, row in enumerate(sequence) if row.get("state") == "lost"), None)
        if lost_at is None:
            continue
        lost_cases += 1
        recovered_at = next(
            (i for i, row in enumerate(sequence[lost_at + 1 :], lost_at + 1) if row.get("state") == "recovered"),
            None,
        )
        if recovered_at is not None:
            recovered_cases += 1
            recovery_events.append(recovered_at - lost_at)

    reversals = 0
    for sequence in by_case.values():
        sequence.sort(key=lambda row: row["event_index"])
        anchors = [row["predicted"] for row in sequence if row.get("event_type") == "partial"]
        reversals += sum((b - a) * (c - b) < 0 for a, b, c in zip(anchors, anchors[1:], anchors[2:]))

    duplicate_error = (
        sum(row["predicted_occurrence"] != row["expected_occurrence"] for row in duplicate_labeled) / len(duplicate_labeled)
        if duplicate_labeled else None
    )

    skip_cases = {}
    for row in rows:
        if row.get("intent") == "skip" or row.get("category") in ("intentional_skip", "section_jump", "forgotten_then_skip"):
            skip_cases.setdefault(row["case_id"], []).append(row)

    skip_success = []
    skip_recovery_events = []
    confirmation_latencies = []
    wrong_intermediate = 0
    intermediate_count = 0
    for sequence in skip_cases.values():
        sequence.sort(key=lambda row: row["event_index"])
        candidates = [
            row for row in sequence
            if row.get("expected_jump_status") == "suspected" and row.get("expected_candidate_index") is not None
        ]
        targets = [row for row in sequence if row.get("expected_jump_status") == "confirmed" and row.get("expected") is not None]
        if not candidates or not targets:
            continue

        first_candidate = candidates[0]
        target = targets[0]["expected"]
        intermediate = [row for row in candidates if row["event_index"] < targets[0]["event_index"]]
        intermediate_count += len(intermediate)
        wrong_intermediate += sum(row["predicted"] != row["expected"] for row in intermediate)

        recovered = next(
            (row for row in sequence if row["event_index"] >= first_candidate["event_index"] and row["predicted"] == target),
            None,
        )
        skip_success.append(recovered is not None)
        if recovered is not None:
            skip_recovery_events.append(recovered["event_index"] - first_candidate["event_index"] + 1)

        predicted_confirm = next(
            (row for row in sequence if row["event_index"] >= first_candidate["event_index"] and row.get("jump_status") == "confirmed"),
            None,
        )
        if predicted_confirm:
            confirmation_latencies.append(predicted_confirm["event_index"] - first_candidate["event_index"] + 1)

    latencies = [row["latency_us"] for row in rows]
    denominator = max(1, len(judged))
    return {
        "event_accuracy": _accuracy(judged),
        "final_accuracy": _accuracy(finals),
        "within_1_accuracy": _accuracy(judged, 1),
        "within_2_accuracy": _accuracy(judged, 2),
        "mae_segments": statistics.mean(errors) if errors else None,
        "median_ae_segments": statistics.median(errors) if errors else None,
        "p95_segment_error": percentile(errors, 0.95),
        "wrong_forward_jump_rate": len(wrong_forward) / denominator,
        "wrong_backward_jump_rate": len(wrong_backward) / denominator,
        "wrong_movement_rate": len(wrong_movement) / len(should_hold) if should_hold else None,
        "false_movement_rate": len(wrong_movement) / len(should_hold) if should_hold else None,
        "false_jump_commit_rate": len(false_jump_commits) / len(false_jump_labeled) if false_jump_labeled else None,
        "false_jump_commit_events": len(false_jump_commits),
        "false_jump_commit_denominator": len(false_jump_labeled),
        "duplicate_reanchor_error_rate": duplicate_error,
        "duplicate_reanchor_cases": len(duplicate_labeled),
        "catastrophic_absolute_rate": len(catastrophic_absolute) / denominator,
        "catastrophic_backward_rate": len(catastrophic_backward) / denominator,
        "lost_rate": len(lost) / max(1, len(rows)),
        "false_lost_rate": len(false_lost) / false_lost_denominator if false_lost_denominator else None,
        "recovery_success_rate": recovered_cases / lost_cases if lost_cases else None,
        "median_recovery_events": statistics.median(recovery_events) if recovery_events else None,
        "p95_recovery_events": percentile(recovery_events, 0.95) if recovery_events else None,
        "jump_candidate_detection_rate": sum(row["jump_status"] in ("suspected", "confirmed") for row in should_candidate) / len(should_candidate) if should_candidate else None,
        "jump_candidate_position_accuracy": sum(row.get("candidate_index") == row["expected_candidate_index"] for row in candidate_labeled) / len(candidate_labeled) if candidate_labeled else None,
        "jump_candidate_labeled_events": len(candidate_labeled),
        "jump_evidence_count_accuracy": sum(row.get("jump_evidence") == row["expected_jump_evidence"] for row in evidence_labeled) / len(evidence_labeled) if evidence_labeled else None,
        "mean_jump_evidence_count_error": statistics.mean(abs((row.get("jump_evidence") or 0) - row["expected_jump_evidence"]) for row in evidence_labeled) if evidence_labeled else None,
        "jump_evidence_labeled_events": len(evidence_labeled),
        "false_jump_candidate_rate": sum(row["jump_status"] in ("suspected", "confirmed") for row in should_not_candidate) / len(should_not_candidate) if should_not_candidate else None,
        "jump_confirmation_accuracy": sum(row["jump_status"] == "confirmed" and row["predicted"] == row["expected"] for row in confirmed if row.get("expected") is not None) / len([row for row in confirmed if row.get("expected") is not None]) if any(row.get("expected") is not None for row in confirmed) else None,
        "jump_cancellation_accuracy": sum(row["jump_status"] == "cancelled" and row["predicted"] == row["expected"] for row in cancelled if row.get("expected") is not None) / len([row for row in cancelled if row.get("expected") is not None]) if any(row.get("expected") is not None for row in cancelled) else None,
        "intentional_skip_recovery_rate": sum(skip_success) / len(skip_success) if skip_success else None,
        "intentional_skip_events_to_recover_median": statistics.median(skip_recovery_events) if skip_recovery_events else None,
        "intentional_skip_events_to_recover_p95": percentile(skip_recovery_events, 0.95) if skip_recovery_events else None,
        "intentional_skip_wrong_intermediate_jump_rate": wrong_intermediate / intermediate_count if intermediate_count else None,
        "median_jump_confirmation_events": statistics.median(confirmation_latencies) if confirmation_latencies else None,
        "p95_jump_confirmation_events": percentile(confirmation_latencies, 0.95) if confirmation_latencies else None,
        "expected_state_accuracy": sum(row["state"] == row["expected_state"] for row in state_labeled) / len(state_labeled) if state_labeled else None,
        "anchor_reversal_count": reversals,
        "high_confidence_accuracy": sum(_error(row) == 0 for row in high_confidence) / len(high_confidence) if high_confidence else None,
        "high_confidence_wrong_rate": sum(_error(row) > 0 for row in high_confidence) / len(high_confidence) if high_confidence else None,
        "latency_mean_us": statistics.mean(latencies) if latencies else 0,
        "latency_median_us": statistics.median(latencies) if latencies else 0,
        "latency_p95_us": percentile(latencies, 0.95),
        "latency_p99_us": percentile(latencies, 0.99),
        "judged_events": len(judged),
        "final_events": len(finals),
        "total_events": len(rows),
    }
