from __future__ import annotations

import re

VERSION = "canonical-1"
HARD_BREAKS = "。！？；\n\r"
MAX_CHARS = 30
SOFT_BREAKS = "，、,"


def segment(text: str) -> list[str]:
    """Versioned deterministic segmentation shared by every adapter."""
    parts = re.split(f"(?<=[{re.escape(HARD_BREAKS)}])", text)
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
