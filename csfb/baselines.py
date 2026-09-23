from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher

from .normalize import normalize
from .segmenter import segment


@dataclass
class Prediction:
    segment_index: int
    char_position: int = 0
    confidence: float | None = None
    state: str | None = None
    candidate_index: int | None = None
    score: float | None = None


class Base:
    name = "base"
    version = "0.2.0"

    def load_script(self, text, initial_segment_index=0, segments=None, segment_indices=None):
        self.text = text
        self.segments = list(segments) if segments is not None else segment(text)
        self.segment_indices = list(segment_indices) if segment_indices is not None else list(range(len(self.segments)))
        if len(self.segment_indices) != len(self.segments):
            raise ValueError("segment_indices length must match segments")
        self.initial_segment_index = self._nearest_index(initial_segment_index)
        self.reset()

    def _nearest_index(self, document_index):
        if not self.segment_indices:
            return 0
        return next((i for i in self.segment_indices if i >= document_index), self.segment_indices[-1])

    def _anchor_position(self):
        if not self.segment_indices:
            return 0
        return min(range(len(self.segment_indices)), key=lambda i: abs(self.segment_indices[i] - self.anchor))

    def reset(self):
        self.anchor = getattr(self, "initial_segment_index", 0)

    def process_event(self, event):
        raise NotImplementedError


class GlobalExact(Base):
    name = "global-exact"

    def process_event(self, event):
        if event["type"] in ("partial", "final"):
            speech = normalize(event["text"])
            if speech:
                for i, text in enumerate(self.segments):
                    n = normalize(text)
                    if n and (n in speech or speech in n):
                        self.anchor = self.segment_indices[i]
                        break
        return Prediction(self.anchor, confidence=1.0 if event["type"] in ("partial", "final") else 0.0,
                          state="locked", candidate_index=self.anchor, score=1.0)


def similarity(a, b):
    a, b = normalize(a), normalize(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


class GlobalFuzzy(Base):
    name = "global-fuzzy"

    def process_event(self, event):
        if event["type"] in ("partial", "final"):
            scores = [similarity(event["text"], text) for text in self.segments]
            if scores:
                pos = max(range(len(scores)), key=scores.__getitem__)
                idx, score = self.segment_indices[pos], scores[pos]
                if score >= 0.48:
                    self.anchor = idx
            else:
                idx, score = self.anchor, 0.0
        else:
            idx, score = self.anchor, 0.0
        return Prediction(self.anchor, confidence=score, state="locked" if score >= .35 else "lost",
                          candidate_index=idx, score=score)


class LocalFuzzy(Base):
    name = "local-fuzzy"

    def reset(self):
        self.anchor = getattr(self, "initial_segment_index", 0)

    def process_event(self, event):
        if event["type"] == "manual_anchor":
            self.anchor = self._nearest_index(event["segment_index"])
            return Prediction(self.anchor, state="locked", candidate_index=self.anchor)
        if event["type"] == "silence" or len(normalize(event.get("text", ""))) < 2:
            return Prediction(self.anchor, state="locked", candidate_index=self.anchor, score=0.0)
        anchor_pos = self._anchor_position()
        lo = max(0, anchor_pos - 2)
        hi = min(len(self.segments), anchor_pos + 9)
        scores = [(similarity(event["text"], self.segments[i]), i) for i in range(lo, hi)]
        score, pos = max(scores, default=(0.0, anchor_pos))
        idx = self.segment_indices[pos] if self.segment_indices else 0
        # Deliberately simple local reference: no hysteresis or recovery state.
        if score >= 0.55:
            self.anchor = idx
        return Prediction(self.anchor, confidence=score, state="locked" if score >= .55 else "lost",
                          candidate_index=idx, score=score)


BASELINES = {engine.name: engine for engine in (GlobalExact, GlobalFuzzy, LocalFuzzy)}
