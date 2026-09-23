from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Event:
    type: str
    text: str = ""
    duration_ms: int | None = None
    segment_index: int | None = None
    sequence: int | None = None
    timestamp_ms: int | None = None


@dataclass
class Expectation:
    event_index: int
    expected_segment: int | None
    acceptable_segments: list[int] | None = None
    should_move: bool | None = None
    should_be_lost: bool | None = None


@dataclass
class Case:
    id: str
    category: str
    script: dict[str, str]
    events: list[Event]
    expectations: list[Expectation]
    metadata: dict[str, Any] = field(default_factory=dict)
    version: int = 1

    def to_dict(self):
        data=asdict(self)
        data["events"]=[{k:v for k,v in event.items() if v is not None} for event in data["events"]]
        data["expectations"]=[{k:v for k,v in exp.items() if v is not None or k=="expected_segment"} for exp in data["expectations"]]
        return data

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["category"], d["script"], [Event(**e) for e in d["events"]], [Expectation(**e) for e in d["expectations"]], d.get("metadata", {}), d.get("version", 1))


def read_jsonl(path):
    import json
    with open(path, encoding="utf-8") as f:
        return [Case.from_dict(json.loads(line)) for line in f if line.strip()]


def write_jsonl(path, cases):
    import json
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for c in cases:
            f.write(json.dumps(c.to_dict(), ensure_ascii=False, separators=(",", ":")) + "\n")
