from __future__ import annotations

import re

VERSION = "canonical-2"
HARD_BREAKS = "。！？；\n\r"
MAX_CHARS = 30
SOFT_BREAKS = "，、,"
BLOCK_TYPES={"title","heading","paragraph","note","stage_direction","list_item","quote","table_cell","caption","header","footer","speaker_note","unknown"}


def segment(text: str) -> list[str]:
    """Versioned deterministic segmentation shared by every adapter."""
    # English sentence punctuation is a boundary only before whitespace/end,
    # so decimal/version dots (for example 3.5 and 2026.1) stay intact.
    parts = re.split(f"(?<=[{re.escape(HARD_BREAKS)}])|(?<=[.!?])(?=\\s|$)", text)
    out: list[str] = []
    for part in parts:
        if not part.strip():
            continue
        while len(part) > MAX_CHARS:
            end = MAX_CHARS
            for i in range(end, max(8, end - 12), -1):
                if part[i - 1] in SOFT_BREAKS:
                    end = i
                    break
            out.append(part[:end])
            part = part[end:]
        if part.strip():
            out.append(part)
    return out


def canonical_document(script):
    """Return spoken segments, preserving block-to-speech position mapping.

    Legacy `{id, text}` and plain strings are treated as one spoken paragraph.
    Structured documents expose only `speech_policy=spoken` content as candidates.
    """
    if isinstance(script,str):
        script={"id":"legacy","text":script}
    if "blocks" not in script:
        blocks=[{"id":"b0","type":"paragraph","text":script["text"],"speech_policy":"spoken"}]
    else:
        blocks=script["blocks"]
    records=[];block_ranges=[]
    for bi,block in enumerate(blocks):
        policy=block.get("speech_policy","spoken")
        if policy not in ("spoken","skip","auto"):
            raise ValueError(f"unsupported speech_policy {policy!r} in block {bi}")
        btype=block.get("type","unknown")
        if btype not in BLOCK_TYPES:
            raise ValueError(f"unsupported block type {btype!r} in block {bi}")
        start=len(records)
        if policy=="spoken":
            for text in segment(block["text"]):
                records.append({"index":len(records),"document_block_index":bi,"block_id":block.get("id",f"b{bi}"),"block_type":btype,"speech_policy":"spoken","language_hint":block.get("language_hint","auto"),"text":text})
        end = len(records) - 1 if len(records) > start else start - 1
        block_ranges.append({"index":bi,"id":block.get("id",f"b{bi}"),"type":btype,"speech_policy":policy,"text":block["text"],"speech_segment_start":start,"speech_segment_end":end})
    return records,block_ranges
