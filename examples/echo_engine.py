#!/usr/bin/env python3
"""Minimal JSONL adapter example; intentionally not a useful alignment engine."""
import json
import sys

anchor=0
for line in sys.stdin:
    msg=json.loads(line)
    if msg["type"]=="load_script":anchor=msg.get("initial_segment_index",0)
    elif msg["type"]=="manual_anchor":anchor=msg["segment_index"]
    print(json.dumps({"segment_index":anchor,"confidence":0.0,"state":"locked"}),flush=True)
