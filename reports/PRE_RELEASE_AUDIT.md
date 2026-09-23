# CSFB Pre-release Audit

Audit snapshot for the locally verified CSFB preview. No push, publication, or final tag was performed.

## Frozen inputs

- Repository: `chinese-speech-follow-benchmark (public benchmark checkout)`
- Git HEAD: `faddba4b81a7635675a555fde8a85d7d511398c0`
- Pre-expansion baseline: frozen in [`PRE_SEMANTIC_EXPANSION_BASELINE.md`](PRE_SEMANTIC_EXPANSION_BASELINE.md)
- Benchmark: 0.2.0 preview; dataset: 0.2.0-preview; generator: 0.2.1; seed: 20260923
- Corpus layers: 210 curated review-status, 230 template-derived, 5,000 synthetic, 1,189 adversarial
- Total: 6,629 cases and 48,851 input events
- Dataset SHA256: `242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf`
- Language strata: 6,003 zh, 40 en, 586 mixed
- Structured cases containing at least one skipped block: 195
- Intentional skip: 144; accidental future phrase: 140; forgotten-word pause: 140; forgotten-then-skip: 120

## Reference baseline results

Rates use the definitions in [`../docs/METRICS.md`](../docs/METRICS.md). Duplicate accuracy is `1 - duplicate_reanchor_error_rate`. Catastrophic absolute error is at least 5 segments; catastrophic backward error is more than 2 segments behind the expected index.

| Engine | Final accuracy | Within 1 | Duplicate accuracy | Non-spoken accuracy | Intentional-skip recovery | False jump commit | Catastrophic absolute | Catastrophic backward | Wrong backward | False movement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.906806 | 0.921764 | 0.012970 | 0.657143 | 0.026738 | 0.107901 | 0.015178 | 0.007610 | 0.012628 | 0.053811 |
| global-fuzzy | 0.889557 | 0.947143 | 0.012970 | 0.314286 | 0.026738 | 0.107901 | 0.015178 | 0.007610 | 0.011106 | 0.045592 |
| local-fuzzy | 0.903307 | 0.968882 | 0.110246 | 0.657143 | 0.331551 | 0.135514 | 0.009481 | 0.005224 | 0.000514 | 0.047868 |

These baselines expose the intended tradeoffs; they are not a production-engine comparison. The pre-expansion catastrophic-absolute rate was zero for all three baselines. The expanded long-distance, duplicate, and navigation cases now produce nonzero rates, showing that the previous zero came from limited scenario coverage under the same 5-segment threshold.

## Largest event-error categories

Counts below come from `failures.jsonl` and exclude predictions listed as acceptable alternatives.

- **global-exact:** duplicate 1,512; near-duplicate 1,362; skip 360; jump-confirmation 360; false-jump-candidate 360; missing-words 330; intentional-skip 258; numbers 246; repeated-final 238; traditional/simplified 234.
- **global-fuzzy:** duplicate 1,512; near-duplicate 1,362; skip 450; jump-confirmation 360; mixed-error 330; stale-partial 304; repeated-final 301; traditional/simplified 300; filler-words 294; exact 288.
- **local-fuzzy:** duplicate 1,362; near-duplicate 1,362; skip 450; mixed-error 330; stale-partial 304; repeated-final 301; traditional/simplified 300; filler-words 294; jump-confirmation 294; exact 288.

## Verification and release gates

- Schema and dataset validation: PASS (6,629 cases, 48,851 events)
- Unit tests: PASS, 25 tests on Python 3.12.10 and Python 3.14.6
- Quick run: PASS on Python 3.12 and 3.14
- Full run: PASS for all three reference baselines
- Determinism: PASS. Two full runs on this manifest matched after excluding latency and host metadata. CSV prediction digest: `6d702632d943b3d8faa942b334c14859aae87bf3942478837d4b0ed4b31b2567`; logical metrics digest: `0a544b6e9a2e15d19c8763239c779f211151f747f8b57d90a1b521343beb14a5`.
- Python 3.11 local: unavailable; Python 3.12 and 3.14 were exercised.
- GitHub Actions workflow: configured for Python 3.11/3.12 on Linux and Windows; actual hosted run: NOT RUN. This checkout has no Git remote.
- Private app repository modified: NO. Private FollowEngine source included: NO.
- Private paths found: NO. Secret-like assignments found: NO. Third-party text/copyright concern found: NO; the corpus is authored/template-assisted or generated and contains no imported source passages.
- Ready for public GitHub pre-release: YES, after committing this audit snapshot; publishing still requires a configured remote and owner action.
- Ready for final v0.1.0 tag: NO. Hosted Actions has not run, and this work is a 0.2.0 preview.

Detailed artifacts: [`CSFB_V0_2_BASELINES.md`](CSFB_V0_2_BASELINES.md), [`results.json`](results.json), [`results.csv`](results.csv), [`failures.jsonl`](failures.jsonl), and [`../docs/GOLDEN_REVIEW.md`](../docs/GOLDEN_REVIEW.md).
