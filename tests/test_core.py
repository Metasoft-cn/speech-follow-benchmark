import json
import random

from csfb.baselines import GlobalExact, GlobalFuzzy, LocalFuzzy
from csfb.generator import SEED, adversarial_cases, golden_cases, synthetic_cases
from csfb.metrics import score
from csfb.model import Event
from csfb.segmenter import segment


def test_segmenter_is_canonical_and_deterministic():
    text="第一句。第二句！第三句？第四句；第五句\n第六句"
    assert segment(text)==["第一句。","第二句！","第三句？","第四句；","第五句\n","第六句"]
    assert segment("甲"*61)==["甲"*30,"甲"*30,"甲"]


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
    rows=[{"expected":0,"predicted":5,"event_type":"final","confidence":.9,"state":"locked","latency_us":1,"case_id":"x","moved_forward_wrong":True,"moved_backward_wrong":False}]
    m=score(rows)
    assert m["catastrophic_absolute_rate"]==1
    assert m["catastrophic_backward_rate"]==0
    assert m["high_confidence_wrong_rate"]==1


def test_generators_are_deterministic():
    assert [c.to_dict() for c in synthetic_cases(30)]==[c.to_dict() for c in synthetic_cases(30)]
    assert [c.to_dict() for c in golden_cases()]==[c.to_dict() for c in golden_cases()]
    assert SEED==20260923


def test_golden_and_adversarial_counts_and_duplicate_examples():
    assert len(golden_cases())>=200
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
