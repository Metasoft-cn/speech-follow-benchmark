from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .model import read_jsonl
from .segmenter import canonical_document


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
        block=json.loads((root/"block.schema.json").read_text(encoding="utf-8"))
        case_schema["properties"]["script"]={"oneOf":[{"type":"string","minLength":1},{"type":"object","required":["id","text"],"properties":{"id":{"type":"string"},"text":{"type":"string","minLength":1}},"additionalProperties":False},{"type":"object","required":["id","blocks"],"properties":{"id":{"type":"string"},"blocks":{"type":"array","minItems":1,"items":block}},"additionalProperties":False}]}
        validator=Draft202012Validator(case_schema)
    for path in paths:
        for c in read_jsonl(path):
            if c.id in ids:raise ValueError(f"duplicate id: {c.id}")
            ids.add(c.id); records,_=canonical_document(c.script); n=len(records)
            required_metadata=("category","language","difficulty","source","mutation_severity")
            missing=[key for key in required_metadata if not c.metadata.get(key)]
            if missing:raise ValueError(f"missing metadata {missing}: {c.id}")
            if c.metadata["category"]!=c.category:raise ValueError(f"metadata category mismatch: {c.id}")
            structured=c.script.get("blocks",[]) if isinstance(c.script,dict) else []
            if any(b.get("speech_policy")=="auto" for b in structured):raise ValueError(f"speech_policy must be explicit in dataset case: {c.id}")
            if not n:raise ValueError(f"script has no segments: {c.id}")
            if validator:
                validator.validate(c.to_dict())
            if not c.expectations:raise ValueError(f"case has no expectations: {c.id}")
            for e in c.expectations:
                if not 0<=e.event_index<len(c.events):raise ValueError(f"event index outside case: {c.id}")
                indices=([e.expected_segment] if e.expected_segment is not None else [])+(e.acceptable_segments or [])
                if e.expected_candidate_index is not None:indices.append(e.expected_candidate_index)
                if any(not 0<=x<n for x in indices):raise ValueError(f"segment index outside script: {c.id}")
            for section in c.metadata.get("sections",[]):
                if not 0<=section["start_segment"]<=section["end_segment"]<n:raise ValueError(f"section range outside script: {c.id}")
                nav=section.get("navigation_only_segments",[])+section.get("heading_segments",[])
                if any(not section["start_segment"]<=x<=section["end_segment"] for x in nav):raise ValueError(f"section navigation index outside section: {c.id}")
                blocks=c.script.get("blocks",[]) if isinstance(c.script,dict) else []
                block_by_id={b["id"]:b for b in blocks}
                for block_id in section.get("navigation_only_block_ids",[]):
                    if block_id not in block_by_id or block_by_id[block_id].get("speech_policy")!="skip":raise ValueError(f"navigation block must exist and use speech_policy=skip: {c.id}/{block_id}")
            summary["cases"]+=1;summary["events"]+=len(c.events);summary["script_characters"]+=sum(len(b["text"]) for b in (c.script.get("blocks",[]) if isinstance(c.script,dict) and "blocks" in c.script else [{"text":c.script.get("text","") if isinstance(c.script,dict) else c.script}]))
    return summary


def manifest(paths,seed,generator_version):
    root=Path(__file__).resolve().parents[1]
    files=[]
    for path in paths:
        b=path.read_bytes();cs=read_jsonl(path)
        files.append({"path":path.relative_to(root).as_posix(),"sha256":hashlib.sha256(b).hexdigest(),"case_count":len(cs),"event_count":sum(len(c.events) for c in cs),"bytes":len(b)})
    canonical=json.dumps(files,sort_keys=True,separators=(",",":" )).encode()
    return {"dataset_version":"0.2.0-preview","seed":seed,"generator_version":generator_version,"case_count":sum(x["case_count"] for x in files),"event_count":sum(x["event_count"] for x in files),"files":files,"sha256":hashlib.sha256(canonical).hexdigest()}
