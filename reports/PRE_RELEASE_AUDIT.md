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
- Quick run: PASS on Python 3.14.
- Full run: PASS twice on Python 3.14.
- Dataset generation: PASS twice; manifest bytes and dataset digest were unchanged.
- CI workflow reviewed: Ubuntu and Windows, Python 3.11 and 3.12; each job installs, runs pytest, validates the dataset, and runs the quick benchmark.
- Hosted CI actually run: NO. No remote is configured.
- Clean-clone test: NOT RUN; the release instructions gate it after a green Hosted CI run.
- Python 3.11 local: unavailable. Python 3.12 and 3.14 were tested.

## Content and licensing audit

- Real secrets or credentials: NO findings. Searched `token`, `secret`, `password`, `api_key`, `access_key`, `authorization`, and private-project path/name patterns; matches were documentation terms only.
- Private filesystem paths: NO findings.
- Private product or engine source: NO findings.
- Copyright: PASS. The corpus consists of original authored/template-derived and deterministic generated text; no third-party source passages or user recordings are included. Dataset and code licenses are separately stated.
- Generated `reports/failures.jsonl`: 24,526,542 bytes. Omitted from the release tree because it exceeds the 20 MB threshold and is reproducible with `csfb run --full`; `reports/results.csv` preserves all event predictions. The failure file is ignored locally.

## Publication gate

- Local release cleanup and validation: PASS.
- Dataset freeze: YES; see [`../docs/CSFB_PREVIEW_FREEZE.md`](../docs/CSFB_PREVIEW_FREEZE.md).
- Remote configured: NO.
- GitHub owner specified: NO. Do not infer the destination from the currently authenticated CLI account.
- GitHub repository created/push completed: NO.
- Hosted CI result: NOT RUN (workflow is configured, but that is not a CI pass).
- Preview tag: NOT CREATED; Hosted CI and clean-clone gates are pending.
- Publication status: PARTIAL; local release candidate is prepared, external publication is blocked until the owner is specified and CI runs.
