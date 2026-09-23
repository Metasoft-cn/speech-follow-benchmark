# Dataset design

The manifest separates 210 curated review-status cases, 230 template-derived cases, 5,000 seeded synthetic stream cases, and 1,189 adversarial cases. Curated records have explicit expected labels and review notes, while some constructions remain template-assisted; see [`GOLDEN_REVIEW.md`](GOLDEN_REVIEW.md) for scope and review limits. L3 is reserved for redistributable real-ASR recognized-text replay with timestamps and human anchor labels. No audio is accepted in this repository.

The generator uses `random.Random(20260923)` and records generator version 0.2.1. Every case records category, language, difficulty, source, and mutation severity. It covers original Chinese, English, and mixed-language prose, numbers, duplicate occurrence, non-spoken blocks, intent, pauses, and navigation. It does not scrape external text. `datasets/MANIFEST.json` records per-file hashes, cases, events, and a canonical manifest digest.

Expected labels are segment indices under `canonical-2`. Validation rejects duplicate IDs, missing required scenario metadata, empty scripts/events, unresolved `auto` policies, out-of-range event and segment indices, missing expectations, and schema violations when the optional JSON Schema validator is installed.

The adversarial layer also contains paired intentional-skip and accidental-future-phrase streams, forgotten-word pauses, pause-then-skip sequences, false jump candidates, confirmation and cancellation sequences, and section jumps. Expected labels distinguish committed anchor from candidate location and annotate state, jump status, candidate index, and evidence count. Section metadata makes heading blocks available for navigation even when excluded from speech matching.
