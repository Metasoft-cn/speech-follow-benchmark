from __future__ import annotations

import shlex
import subprocess
import time

from .baselines import BASELINES
from .protocol import SubprocessAdapter
from .segmenter import segment


def run_case(case,engine_name,command=None):
    if command:
        adapter=SubprocessAdapter(shlex.split(command));adapter.load_script(case.script["id"],case.script["text"],segment(case.script["text"]),case.metadata.get("initial_segment_index",0))
        engine=None
    else:
        engine=BASELINES[engine_name]();engine.load_script(case.script["text"],case.metadata.get("initial_segment_index",0));adapter=None
    expected={x.event_index:x for x in case.expectations};rows=[];previous=0
    try:
        for i,event in enumerate(case.events):
            obj={k:v for k,v in event.__dict__.items() if v is not None}
            started=time.perf_counter_ns()
            pred=adapter.process_event(obj) if adapter else engine.process_event(obj).__dict__
            latency=(time.perf_counter_ns()-started)//1000
            if "segment_index" not in pred:raise ValueError(f"prediction at event {i} lacks segment_index")
            ex=expected.get(i);idx=int(pred["segment_index"]);confidence=pred.get("confidence")
            state=pred.get("state")
            if state is None:state="locked"
            if state not in ("locked","lost","recovered"):raise ValueError(f"unknown state: {state}")
            acceptable=([ex.expected_segment] if ex and ex.expected_segment is not None else [])+(ex.acceptable_segments or [] if ex else [])
            correct=(ex is None or ex.expected_segment is None or idx in acceptable)
            canonical=segment(case.script["text"])
            rows.append({"case_id":case.id,"category":case.category,"event_index":i,"event_type":event.type,"text":event.text,"expected":ex.expected_segment if ex else None,"expected_segment_text":canonical[ex.expected_segment] if ex and ex.expected_segment is not None and ex.expected_segment<len(canonical) else None,"acceptable_segments":ex.acceptable_segments if ex else None,"should_move":ex.should_move if ex else None,"should_be_lost":ex.should_be_lost if ex else None,"predicted":idx,"moved":idx!=previous,"moved_forward_wrong":idx>previous and not correct,"moved_backward_wrong":idx<previous and not correct,"segment_error":None if ex is None or ex.expected_segment is None else min(abs(idx-x) for x in acceptable),"confidence":float(confidence) if confidence is not None else None,"state":state,"candidate_index":pred.get("candidate_index"),"score":pred.get("score"),"latency_us":int(latency)})
            previous=idx
        return rows
    finally:
        if adapter:adapter.close()
