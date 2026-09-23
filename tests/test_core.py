import json
import random
from argparse import Namespace

from csfb.baselines import GlobalExact, GlobalFuzzy, LocalFuzzy
from csfb.generator import SEED, adversarial_cases, curated_cases, golden_cases, jump_intent_cases, synthetic_cases
from csfb.metrics import score
from csfb.model import Event
from csfb.segmenter import canonical_document, segment


def test_segmenter_is_canonical_and_deterministic():
    text="第一句。第二句！第三句？第四句；第五句\n第六句"
    assert segment(text)==["第一句。","第二句！","第三句？","第四句；","第五句\n","第六句"]
    assert segment("甲"*61)==["甲"*30,"甲"*30,"甲"]
    assert segment("Today is ready. Version 3.5 is stable!")==["Today is ready."," Version 3.5 is stable!"]


def test_structured_document_filters_skip_blocks_and_preserves_mapping():
    records, blocks=canonical_document({"id":"s","blocks":[{"id":"h","type":"heading","text":"Overview","speech_policy":"skip"},{"id":"p","type":"paragraph","text":"第一句。Second sentence.","speech_policy":"spoken"},{"id":"n","type":"note","text":"Do not read.","speech_policy":"skip"}]})
    assert [r["text"] for r in records]==["第一句。","Second sentence."]
    assert [r["document_block_index"] for r in records]==[1,1]
    assert blocks[0]["speech_segment_start"]==0 and blocks[0]["speech_segment_end"]==-1
    assert blocks[2]["speech_segment_start"]==2 and blocks[2]["speech_segment_end"]==1


def test_public_schema_accepts_legacy_text_and_block_types():
    from pathlib import Path
    from jsonschema import Draft202012Validator
    root=Path(__file__).resolve().parents[1]/"schema"
    case=json.loads((root/"case.schema.json").read_text(encoding="utf-8"))
    script_schema=case["properties"]["script"]
    Draft202012Validator(script_schema).validate("Legacy plain script.")
    block=json.loads((root/"block.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(block).validate({"id":"cell","type":"table_cell","text":"cell contents","speech_policy":"skip"})


def test_baselines_exact_text_position():
    for cls in (GlobalExact,GlobalFuzzy,LocalFuzzy):
        e=cls();e.load_script("第一段内容。第二段内容。")
        p=e.process_event({"type":"final","text":"第二段内容"})
        assert p.segment_index==1


def test_silence_does_not_move_local_baseline():
    e=LocalFuzzy();e.load_script("第一段内容。第二段内容。")
    e.process_event({"type":"final","text":"第二段内容"});before=e.anchor
    assert e.process_event({"type":"silence","duration_ms":5000}).segment_index==before


def test_local_baseline_duplicate_anchor_is_stable():
    e=LocalFuzzy();e.load_script("感谢大家。补充内容。感谢大家。",2)
    assert e.process_event({"type":"final","text":"感谢大家"}).segment_index==2


def test_metrics_catastrophic_are_separate():
    rows=[{"expected":0,"predicted":5,"event_type":"final","event_index":0,"confidence":.9,"state":"locked","latency_us":1,"case_id":"x","moved_forward_wrong":True,"moved_backward_wrong":False}]
    m=score(rows)
    assert m["catastrophic_absolute_rate"]==1
    assert m["catastrophic_backward_rate"]==0
    assert m["high_confidence_wrong_rate"]==1


def test_multi_hypothesis_jump_metrics():
    common={"event_type":"final","confidence":.9,"candidate_index":5,"jump_evidence":1,"latency_us":1,"case_id":"skip","moved":False,"movement_type":"hold","jump_distance":0,"predicted_occurrence":None,"expected_occurrence":None,"moved_forward_wrong":False,"moved_backward_wrong":False,"should_move":False,"should_be_lost":False,"acceptable_segments":None,"expected_candidate_index":5,"expected_jump_evidence":1,"intent":"skip"}
    rows=[{**common,"category":"intentional_skip","event_index":0,"expected":2,"expected_state":"suspect_jump","state":"suspect_jump","expected_jump_status":"suspected","jump_status":"suspected","predicted":2},{**common,"category":"intentional_skip","event_index":1,"expected":5,"expected_state":"confirmed_jump","state":"confirmed_jump","expected_jump_status":"confirmed","jump_status":"confirmed","predicted":5,"moved":True,"should_move":True,"jump_evidence":2,"expected_jump_evidence":2}]
    m=score(rows)
    assert m["jump_candidate_detection_rate"]==1
    assert m["jump_evidence_count_accuracy"]==1
    assert m["jump_confirmation_accuracy"]==1
    cancel={**common,"category":"jump_cancellation","event_index":0,"expected":2,"expected_state":"locked","state":"locked","expected_jump_status":"cancelled","jump_status":"cancelled","expected_candidate_index":None,"predicted":2}
    assert score([cancel])["jump_cancellation_accuracy"]==1


def test_suspected_but_unconfirmed_wrong_jump_counts_as_false_commit():
    row={"case_id":"false-future","category":"accidental_future_phrase","intent":"mistake","event_index":0,"event_type":"partial","expected":3,"predicted":10,"acceptable_segments":None,"expected_jump_status":"suspected","expected_candidate_index":10,"should_move":False,"jump_status":"suspected","candidate_index":10,"moved":True,"jump_distance":7,"movement_type":"forward","moved_forward_wrong":True,"moved_backward_wrong":False,"confidence":None,"state":"suspect_jump","latency_us":1}
    metrics=score([row])
    assert metrics["false_jump_commit_rate"]==1
    assert metrics["false_jump_commit_events"]==1


def test_intentional_skip_recovery_and_intermediate_hold_are_separate():
    common={"case_id":"skip","category":"intentional_skip","intent":"skip","event_type":"final","acceptable_segments":None,"confidence":None,"state":"locked","latency_us":1,"moved_forward_wrong":False,"moved_backward_wrong":False,"should_move":False,"should_be_lost":False}
    rows=[
        {**common,"event_index":0,"expected":2,"predicted":2,"expected_jump_status":"suspected","expected_candidate_index":7,"jump_status":"suspected","moved":False,"jump_distance":0,"movement_type":"hold"},
        {**common,"event_index":1,"expected":7,"predicted":7,"expected_jump_status":"confirmed","expected_candidate_index":7,"jump_status":"confirmed","moved":True,"jump_distance":5,"movement_type":"forward","should_move":True},
    ]
    metrics=score(rows)
    assert metrics["intentional_skip_recovery_rate"]==1
    assert metrics["intentional_skip_events_to_recover_median"]==2
    assert metrics["intentional_skip_wrong_intermediate_jump_rate"]==0


def test_score_exposes_language_and_region_strata():
    common={"acceptable_segments":None,"confidence":None,"state":"locked","latency_us":1,"moved":False,"movement_type":"hold","jump_distance":0,"expected_jump_status":"none","jump_status":"none","moved_forward_wrong":False,"moved_backward_wrong":False}
    rows=[
        {**common,"case_id":"zh","event_index":0,"expected":0,"predicted":0,"event_type":"final","language":"zh","region":"spoken_only"},
        {**common,"case_id":"en","event_index":0,"expected":0,"predicted":1,"event_type":"final","language":"en","region":"non_spoken_region"},
    ]
    metrics=score(rows)
    assert metrics["by_language"]["zh"]["final_accuracy"]==1
    assert metrics["by_language"]["en"]["final_accuracy"]==0
    assert metrics["by_region"]["spoken_only"]["judged_events"]==1


def test_generators_are_deterministic():
    assert [c.to_dict() for c in synthetic_cases(30)]==[c.to_dict() for c in synthetic_cases(30)]
    assert [c.to_dict() for c in golden_cases()]==[c.to_dict() for c in golden_cases()]
    assert SEED==20260923


def test_preview_report_does_not_overwrite_v01_baseline(tmp_path, monkeypatch):
    from csfb import cli

    monkeypatch.setattr(cli, "REPORT_PATH", tmp_path / "CSFB_V0_2_BASELINES.md")
    cli.run(Namespace(
        category=None,
        case="curated_exact_001",
        quick=False,
        engine="global-exact",
        engine_command=None,
        output_dir=str(tmp_path),
    ))

    assert (tmp_path / "CSFB_V0_2_BASELINES.md").exists()
    assert not (tmp_path / "CSFB_V0_1_BASELINES.md").exists()


def test_golden_and_adversarial_counts_and_duplicate_examples():
    assert len(golden_cases())>=200
    curated=curated_cases()
    assert len(curated)>=200
    assert all(c.metadata.get("review_status")=="reviewed" and c.metadata.get("review_notes") for c in curated)
    adv=adversarial_cases()
    assert len(adv)>=100
    assert sum(c.category=="duplicate" for c in adv)>=100
    assert all(len(c.expectations)>0 for c in adv)
    duplicate=next(c for c in golden_cases() if c.id=="golden_duplicate_0001")
    assert duplicate.expectations[0].should_move is False
    assert duplicate.expectations[0].should_be_lost is False


def test_case_ids_unique_across_layers():
    all_cases=golden_cases()+synthetic_cases(60)+adversarial_cases()
    ids=[c.id for c in all_cases]
    assert len(ids)==len(set(ids))


def test_jump_intent_categories_are_explicit_and_large_enough():
    cases=jump_intent_cases()
    counts={category:sum(c.category==category for c in cases) for category in {c.category for c in cases}}
    assert set(counts)=={"intentional_skip","accidental_future_phrase","forgotten_word_pause","false_jump_candidate","jump_confirmation","jump_cancellation","section_jump","forgotten_then_skip"}
    assert all(n>=100 for n in counts.values())
    skip=next(c for c in cases if c.category=="intentional_skip")
    assert skip.expectations[0].expected_segment==skip.metadata["initial_segment_index"]
    assert skip.expectations[0].expected_candidate_index>skip.expectations[0].expected_segment
    assert skip.expectations[1].expected_jump_status=="confirmed"
    section=next(c for c in cases if c.category=="section_jump")
    assert section.metadata["sections"][2]["navigation_only_block_ids"]==["heading_3"]
    assert section.script["blocks"][6]["speech_policy"]=="skip"


def test_expected_candidate_distance_is_anchor_relative():
    from csfb.runner import run_case

    case=next(c for c in jump_intent_cases() if c.id=="intentional_skip_distance_50")
    rows=run_case(case,"local-fuzzy")
    assert [row["expected_candidate_distance"] for row in rows]==[50,50]
    assert [row["expected_jump_evidence"] for row in rows]==[1,2]


def test_curated_golden_review_status_and_language_coverage():
    cases=curated_cases()
    assert len(cases)>=100
    assert all(c.metadata.get("review_status")=="reviewed" and c.metadata.get("review_notes") for c in cases)
    assert {"zh-Hans","en","mixed"} <= {c.metadata["language"] for c in cases}
    assert all(c.metadata.get("mutation_severity") and c.metadata.get("category")==c.category for c in cases)


def test_curated_english_duplicates_and_confirmed_jump_targets_are_exact():
    cases=curated_cases()
    for case in cases:
        segments,_=canonical_document(case.script)
        if case.id.startswith("curated_english_duplicate_"):
            assert len(segments)==3
            assert segments[0]["text"].strip().lower()==segments[2]["text"].strip().lower()
            assert case.expectations[0].expected_segment==2
        for expectation in case.expectations:
            if expectation.expected_jump_status=="confirmed":
                assert expectation.expected_candidate_index is not None
                assert expectation.expected_segment==expectation.expected_candidate_index+1
    for case in jump_intent_cases():
        for expectation in case.expectations:
            if expectation.expected_jump_status=="confirmed":
                assert expectation.expected_candidate_index is not None
                assert expectation.expected_segment==expectation.expected_candidate_index+1


def test_safety_and_occurrence_metrics():
    base={"expected":3,"predicted":7,"event_type":"final","event_index":0,"confidence":.5,"state":"locked","latency_us":1,"case_id":"x","moved":True,"movement_type":"forward","jump_distance":5,"expected_jump_status":"cancelled","jump_status":"confirmed","candidate_index":7,"expected_candidate_index":3,"predicted_occurrence":0,"expected_occurrence":2,"moved_forward_wrong":True,"moved_backward_wrong":False,"should_move":False,"should_be_lost":False,"acceptable_segments":None,"intent":"skip"}
    metrics=score([base])
    assert metrics["false_jump_commit_rate"]==1
    assert metrics["false_movement_rate"]==1
    assert metrics["duplicate_reanchor_error_rate"]==1
