import json
import sys
import pytest

from csfb.protocol import SubprocessAdapter
from csfb.runner import run_case
from csfb.generator import golden_cases


def test_subprocess_adapter_protocol_roundtrip():
    cmd=f'"{sys.executable}" examples/echo_engine.py'
    adapter=SubprocessAdapter(__import__("shlex").split(cmd))
    try:
        response=adapter.load_script("s1","你好。",["你好。"])
        assert response["segment_index"]==0
        assert adapter.process_event({"type":"final","text":"你好"})["segment_index"]==0
    finally:adapter.close()


def test_single_case_replay_rows():
    c=next(c for c in golden_cases() if c.id=="golden_exact_0001")
    rows=run_case(c,"global-exact")
    assert len(rows)==len(c.events)
    assert rows[0]["expected"]==0


def test_duplicate_case_starts_at_annotated_occurrence():
    c=next(c for c in golden_cases() if c.id=="golden_duplicate_0001")
    assert c.metadata["initial_segment_index"]==2


def test_external_runner_receives_section_navigation_metadata():
    from csfb.generator import jump_intent_cases
    from csfb.runner import run_case
    case=next(c for c in jump_intent_cases() if c.category=="section_jump")
    command=f'"{sys.executable}" examples/echo_engine.py'
    rows=run_case(case,"external",command)
    assert rows[0]["expected_candidate_index"]==4


def test_runner_rejects_out_of_range_prediction():
    c=next(c for c in golden_cases() if c.id=="golden_exact_0001")
    class Bad:
        def load_script(self,*args):pass
        def send(self,*args):return {"segment_index":0}
        def process_event(self,event):return {"segment_index":999}
        def close(self):pass
    import csfb.runner as runner
    old=runner.SubprocessAdapter;runner.SubprocessAdapter=lambda command:Bad()
    try:
        with pytest.raises(ValueError,match="out-of-range"):
            runner.run_case(c,"external","bad-engine")
    finally:runner.SubprocessAdapter=old
