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
    version = "0.1.0"
    def load_script(self, text, initial_segment_index=0): self.text=text; self.segments=segment(text); self.initial_segment_index=max(0,min(initial_segment_index,max(0,len(self.segments)-1))); self.reset()
    def reset(self): self.anchor=getattr(self,"initial_segment_index",0)
    def process_event(self, event): raise NotImplementedError


class GlobalExact(Base):
    name="global-exact"
    def process_event(self,event):
        if event["type"] in ("partial","final"):
            speech=normalize(event["text"])
            if speech:
                for i,s in enumerate(self.segments):
                    n=normalize(s)
                    if n and (n in speech or speech in n): self.anchor=i; break
        return Prediction(self.anchor,confidence=1.0 if event["type"] in ("partial","final") else 0.0,state="locked",candidate_index=self.anchor,score=1.0)


def similarity(a,b):
    a,b=normalize(a),normalize(b)
    if not a or not b:return 0.0
    return SequenceMatcher(None,a,b,autojunk=False).ratio()


class GlobalFuzzy(Base):
    name="global-fuzzy"
    def process_event(self,event):
        if event["type"] in ("partial","final"):
            scores=[similarity(event["text"],s) for s in self.segments]
            if scores:
                idx=max(range(len(scores)),key=scores.__getitem__); score=scores[idx]
                if score>=0.48:self.anchor=idx
            else: idx=0;score=0.0
        else:idx=self.anchor;score=0.0
        return Prediction(self.anchor,confidence=score,state="locked" if score>=.35 else "lost",candidate_index=idx,score=score)


class LocalFuzzy(Base):
    name="local-fuzzy"
    def reset(self): self.anchor=getattr(self,"initial_segment_index",0)
    def process_event(self,event):
        if event["type"]=="manual_anchor":
            self.anchor=min(event["segment_index"],len(self.segments)-1); return Prediction(self.anchor,state="locked",candidate_index=self.anchor)
        if event["type"]=="silence" or len(normalize(event.get("text","")))<2:
            return Prediction(self.anchor,state="locked",candidate_index=self.anchor,score=0.0)
        lo=max(0,self.anchor-2); hi=min(len(self.segments),self.anchor+9)
        scores=[(similarity(event["text"],self.segments[i]),i) for i in range(lo,hi)]
        score,idx=max(scores,default=(0.0,self.anchor))
        # Deliberately simple local reference: no hysteresis or recovery state.
        if score>=0.55:self.anchor=idx
        return Prediction(self.anchor,confidence=score,state="locked" if score>=.55 else "lost",candidate_index=idx,score=score)


BASELINES={x.name:x for x in (GlobalExact,GlobalFuzzy,LocalFuzzy)}
