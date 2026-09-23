# CSFB v0.2.0-preview freeze record

The public preview dataset and its evaluation contract were frozen on 2026-09-23 before running any private product engine.

## Frozen inputs

- Dataset version: `0.2.0-preview`
- Generator: `0.2.1`; seed: `20260923`
- Cases: 6,629; events: 48,851
- Layers: 210 curated review-status, 230 template-derived, 5,000 synthetic, 1,189 adversarial
- Dataset SHA256: `242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf`
- Canonical segmentation: `canonical-2`
- Code commit used for the baseline run: `1d9b13b2d8a7d1af9f7fbcd8905813a3753ef8a8`
- Benchmark source SHA256: `9fa1002ff914def7ba225a7777ad85a5899ef65b44380ec741d72a6ca24f85fc`

This freeze covers the dataset, expected labels, canonical segmentation, metric definitions, and the three reference baseline implementations. Any objective benchmark defect requires a documented versioned correction and a complete rerun; private engine results must not be used to alter the frozen inputs.

## Verification

- Tests: 26 passed on Python 3.12 and 3.14.
- Schema validation: passed, 6,629 cases and 48,851 events.
- Quick benchmark: passed on Python 3.14.
- Full benchmark: passed twice on Python 3.14; each run produced 146,553 predictions.
- Dataset generation: two successive generations produced the same manifest bytes and dataset SHA256.
- Logical prediction SHA256 (latency excluded): `6d702632d943b3d8faa942b334c14859aae87bf3942478837d4b0ed4b31b2567` on both runs.
- Logical metrics SHA256 (latency, timestamp, Python/platform metadata, and working-tree status excluded): `ebb46141d778fbc0d204d42b4baf8bb55644f91192fd4d94941edc42f0975a13` on both runs.

| Reference baseline | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward |
|---|---:|---:|---:|---:|
| Global Exact | 90.68% | 92.18% | 1.52% | 1.26% |
| Global Fuzzy | 88.96% | 94.71% | 1.52% | 1.11% |
| Local Fuzzy | 90.33% | 96.89% | 0.95% | 0.05% |

The JSON/CSV outputs and the full category breakdown are in [`../reports/CSFB_V0_2_BASELINES.md`](../reports/CSFB_V0_2_BASELINES.md), [`../reports/results.json`](../reports/results.json), and [`../reports/results.csv`](../reports/results.csv). Hosted CI has not run, and no GitHub remote or preview tag is configured; those are publication gates, not dataset-freeze inputs.
