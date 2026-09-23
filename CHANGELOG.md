# Changelog

## 0.2.0-preview - 2026-09-23

- Added structured spoken/non-spoken blocks while retaining legacy plain-text scripts.
- Added curated, template-derived, synthetic, and adversarial corpus layers; intent, navigation, and English/mixed-language scenarios.
- Added multi-hypothesis jump labels for intentional skips, accidental future phrases, long pauses, candidate cancellation, and section navigation; expanded the curated review set to 210 cases.
- Added candidate-distance and evidence-count metrics; expanded the adversarial corpus to 1,189 cases (generator 0.2.1).
- Added jump, false movement, duplicate occurrence, recovery, and language-stratified reporting.
- Generator 0.2.1 makes language, category, source, difficulty, and mutation severity explicit on every case; added forgotten-word-then-skip streams and corrected false-jump accounting for unconfirmed candidates.
- This is a preview. GitHub Actions has not yet been run against a hosted repository; no final release tag is implied.

## 0.1.0 - 2026-09-23

- Initial pre-release specification, JSON schemas, canonical segmenter, JSONL protocol, seeded datasets, transparent reference baselines, metrics, CLI, and reports.
- Seed: 20260923; generator version: 0.1.0.
