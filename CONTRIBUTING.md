# Contributing

Contributions are welcome: original cases, Chinese ASR error patterns, baselines, adapters, Traditional Chinese coverage, technical vocabulary, metric clarifications, and documentation.

Before adding text, confirm it is original, redistributable, and not private. Do not submit copied news, books, blogs, commercial copy, scripts, recordings, or user text. New expectations must be reviewed against the canonical segmenter. Keep generators seeded and deterministic; update the dataset version/changelog and manifest whenever data or expected labels change.

For code changes, install the `dev` extra, run `pytest`, `csfb validate`, and `csfb run --quick`. Add focused tests for changed behavior. Engine submissions must include engine version/commit and benchmark hash; no ranking or single composite score is implied.

By intentionally submitting a contribution, you agree it is offered under the project’s Apache-2.0 code license; dataset contributions are released under CC0 1.0 as described in `DATASET_LICENSE.md`.
