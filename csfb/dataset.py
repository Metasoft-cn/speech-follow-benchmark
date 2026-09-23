from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .model import read_jsonl
from .segmenter import segment


def validate(paths, schema=True):
    ids=set();summary={"cases":0,"events":0,"script_characters":0}
    try:
        from jsonschema import Draft202012Validator
    except ImportError:Draft202012Validator=None
    validator=None
    if schema and Draft202012Validator:
        root=Path(__file__).resolve().parents[1]/"schema"
        case_schema=json.loads((root/"case.schema.json").read_text(encoding="utf-8"))
        event=json.loads((root/"event.schema.json").read_text(encoding="utf-8"))
        expectation=json.loads((root/"expectation.schema.json").read_text(encoding="utf-8"))
        case_schema["properties"]["events"]["items"]=event
        case_schema["properties"]["expectations"]["items"]=expectation
        validator=Draft202012Validator(case_schema)
    for path in paths:
        for c in read_jsonl(path):
            if c.id in ids:raise ValueError(f"duplicate id: {c.id}")
            ids.add(c.id); n=len(segment(c.script["text"]))
            if not n:raise ValueError(f"script has no segments: {c.id}")
            if validator:
                validator.validate(c.to_dict())
            if not c.expectations:raise ValueError(f"case has no expectations: {c.id}")
            for e in c.expectations:
                if not 0<=e.event_index<len(c.events):raise ValueError(f"event index outside case: {c.id}")
                indices=([e.expected_segment] if e.expected_segment is not None else [])+(e.acceptable_segments or [])
                if any(not 0<=x<n for x in indices):raise ValueError(f"segment index outside script: {c.id}")
            summary["cases"]+=1;summary["events"]+=len(c.events);summary["script_characters"]+=len(c.script["text"])
    return summary


def manifest(paths,seed,generator_version):
    root=Path(__file__).resolve().parents[1]
    files=[]
    for path in paths:
        b=path.read_bytes();cs=read_jsonl(path)
        files.append({"path":path.relative_to(root).as_posix(),"sha256":hashlib.sha256(b).hexdigest(),"case_count":len(cs),"event_count":sum(len(c.events) for c in cs),"bytes":len(b)})
    canonical=json.dumps(files,sort_keys=True,separators=(",",":" )).encode()
    return {"dataset_version":"0.1.0","seed":seed,"generator_version":generator_version,"case_count":sum(x["case_count"] for x in files),"event_count":sum(x["event_count"] for x in files),"files":files,"sha256":hashlib.sha256(canonical).hexdigest()}
