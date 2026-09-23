# Built-in baselines

These deliberately small reference implementations are intended for comparison, not optimized entrants.

- **Global Exact:** normalize with Unicode NFKC, lowercase, strip whitespace and Unicode punctuation/symbols; choose the first segment where normalized speech is a substring of normalized segment text or vice versa. No continuity prior.
- **Global Fuzzy:** compare normalized speech against every segment using Python `difflib.SequenceMatcher(..., autojunk=False).ratio()`; select the highest score globally; update only at score >= 0.48. No positional prior.
- **Local Fuzzy:** inspect `[anchor - 2, anchor + 8]` clipped to the document, choose the highest same `SequenceMatcher` ratio, move when score >= 0.55. No recovery widening, hysteresis, or advanced jump gating. Silence and <2 normalized characters hold the anchor.

These simple baselines intentionally expose weaknesses such as repeated-text ambiguity and large skips. Implementation: `csfb/baselines.py` (Apache-2.0).
