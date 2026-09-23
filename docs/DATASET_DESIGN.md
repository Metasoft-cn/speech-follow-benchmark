# Dataset design

Layers: L0 golden cases expanded from human-authored templates; L1 seeded synthetic stream cases; L2 adversarial cases emphasizing duplicates, near duplicates, prefixes, short segments, and recovery; L3 reserved real-ASR recognized-text replay with timestamps and human anchor labels. The golden case count includes deterministic template variants, not that many independently handwritten scripts. No audio is accepted in this repository.

The generator uses `random.Random(20260923)` and records generator version 0.1.0. It covers original prose across daily speech, company/product, teaching, technology, finance, news-like writing, speeches, introductions, video/live scripts, numbers, English-mixed and technical content. It does not scrape external text. `datasets/MANIFEST.json` records per-file hashes, cases, events, and a canonical manifest digest.

Expected labels are segment indices under `canonical-1`. Validation rejects duplicate IDs, empty scripts/events, out-of-range event and segment indices, missing expectations, and schema violations when the optional JSON Schema validator is installed.
