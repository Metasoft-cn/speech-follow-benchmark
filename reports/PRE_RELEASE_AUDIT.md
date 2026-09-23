# CSFB v0.2.0-preview publication audit

This audit records local release readiness. No repository was published, no Hosted GitHub Actions run occurred, and no tag was created.

## Frozen benchmark

- Benchmark code commit used for runs: `1d9b13b2d8a7d1af9f7fbcd8905813a3753ef8a8`
- Dataset: `0.2.0-preview`; generator `0.2.1`; seed `20260923`
- Corpus: 210 curated review-status, 230 template-derived, 5,000 synthetic, 1,189 adversarial cases
- Total: 6,629 cases and 48,851 events
- Dataset SHA256: `242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf`
- Full baseline runs: 146,553 predictions each
- Logical prediction SHA256: `6d702632d943b3d8faa942b334c14859aae87bf3942478837d4b0ed4b31b2567` on both runs
- Logical metrics SHA256: `ebb46141d778fbc0d204d42b4baf8bb55644f91192fd4d94941edc42f0975a13` on both runs
- Combined logical output SHA256: `9a8aedbea4a3063851831fae132a3a9ea94c2998ea3aa37c85fc7fde404f00ee` across both stored runs and the final full replay, excluding latency, host/runtime, and source identity.
- Language strata: 6,003 zh, 40 en, 586 mixed; 195 cases contain at least one skipped block.
- Navigation strata: 144 intentional skips, 120 forgotten-then-skip cases, 140 accidental future phrases, 140 forgotten-word pauses.

## Reference baselines

| Engine | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward | False jump commit |
|---|---:|---:|---:|---:|---:|
| Global Exact | 90.68% | 92.18% | 1.52% | 1.26% | 10.79% |
| Global Fuzzy | 88.96% | 94.71% | 1.52% | 1.11% | 10.79% |
| Local Fuzzy | 90.33% | 96.89% | 0.95% | 0.05% | 13.55% |

These are reference algorithms, not production-engine claims. Full metrics are in [`CSFB_V0_2_BASELINES.md`](CSFB_V0_2_BASELINES.md).

## Local validation

- Pytest: 26 passed on Python 3.12 and 3.14.
- Dataset schema validation: PASS (6,629 cases; 48,851 events).
- Quick run: PASS on Python 3.12 and 3.14.
- Full run: PASS twice on Python 3.14.
- Dataset generation: PASS twice; manifest bytes and dataset digest were unchanged.
- CI workflow reviewed: Ubuntu and Windows, Python 3.11 and 3.12; each job installs, runs pytest, validates the dataset, and runs the quick benchmark.
- Hosted CI actually run: NO. No remote is configured.
- Clean-clone test: NOT RUN; the release instructions gate it after a green Hosted CI run.
- Python 3.11 local: unavailable. Python 3.12 and 3.14 were tested.

## Content and licensing audit

- Real secrets or credentials: NO findings. Searched `token`, `secret`, `password`, `api_key`, `access_key`, `authorization`, and private-project path/name patterns; matches were documentation terms only.
- Current release tree and sanitized `main` history: NO private filesystem paths or private-project path/name findings. The sole historical absolute path identified by the earlier audit referred to this public benchmark checkout; it was replaced by a repository-neutral label before publication. No private product or engine source was found.
- Private product or engine source: NO findings.
- Copyright: PASS. The corpus consists of original authored/template-derived and deterministic generated text; no third-party source passages or user recordings are included. Dataset and code licenses are separately stated.
- Curated golden review: 210 records received row-by-row label review by one contributor; no external adjudication is claimed. See [`../docs/GOLDEN_REVIEW.md`](../docs/GOLDEN_REVIEW.md).
- Generated `reports/failures.jsonl`: 24,526,542 bytes. Omitted from the release tree because it exceeds the 20 MB threshold and is reproducible with `csfb run --full`; `reports/results.csv` preserves all event predictions. The failure file is ignored locally.

## Pre-publication history rewrite

The absolute checkout path in the historical audit snapshot was replaced with `chinese-speech-follow-benchmark (public benchmark checkout)`. Only the `main` ref was rewritten. The current tree is byte-identical to the pre-rewrite tree, including all dataset files, and the frozen dataset SHA256 remains unchanged.

| Original commit | Sanitized commit |
|---|---|
| `109bea980e9f900b6729a327fcbd944b2bc6b1ee` | `2090cc7d61e5b64238522d0428817153e1c63e8a` |
| `1d9b13b2d8a7d1af9f7fbcd8905813a3753ef8a8` | `57c5d58999ce8d47ce01dc2c29c5c40e2e6c6bcc` |
| `a2d1b38853d794fc6b3435687834f7b29bd2643f` | `6fb033aaf83cc4a3e5159ecba77772c6016d506a` |
| `6004dffa2b12bbe4b0701636c8b31d9dea5a4656` | `b00391e53afa7c6826b172fe221ff209cde99d59` |
| `8349c1b232402a53704acbe4e8edb7da55eb120d` | `29f20a469568b9ec440ee20daa505d80ea1189eb` |
| `a645fcbcc2c81781c07bfb126a0d7675e336afef` | `cbb59126682637115a2b8a5ae35c793cabd1498c` |

The original history is retained in a local backup ref and bundle only; neither is included in the public push. The complete commit map is preserved with the local release audit records.

## Publication gate

- Local release cleanup, history scan, pytest, schema validation, and quick run: PASS after history sanitization.
- Dataset freeze: YES; see [`../docs/CSFB_PREVIEW_FREEZE.md`](../docs/CSFB_PREVIEW_FREEZE.md).
- GitHub destination: `wlyl123/speech-follow-benchmark`, confirmed public and empty; owner supplied by the user.
- Remote configured: NO at this audit snapshot; the initial push is pending.
- Hosted CI result: NOT RUN (workflow is configured, but that is not a CI pass).
- Clean-clone test: NOT RUN; gated on a green Hosted CI run.
- Preview tag: NOT CREATED; Hosted CI and clean-clone gates are pending.
- Publication status: READY FOR INITIAL PUSH; release completion still requires Hosted CI, a GitHub clean clone, and the preview tag.
