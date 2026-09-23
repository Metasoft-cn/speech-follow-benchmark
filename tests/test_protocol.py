import json
import sys

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
