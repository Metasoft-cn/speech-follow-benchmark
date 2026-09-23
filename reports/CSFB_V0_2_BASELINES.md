# CSFB v0.2.0 Preview Baseline Results

- Cases: 6629
- Input events: 48851
- Predictions: 146553
- Dataset SHA256: `242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf`
- Seed: 20260923
- Generator: 0.2.1
- Runner: 0.2.0
- Base Git commit: `faddba4b81a7635675a555fde8a85d7d511398c0`
- Working tree dirty: True
- Code SHA256: `c6134a1d0c941651137524d51693a91b1680828919e3757d1e757c72d8b6e7c2`
- Timestamp (UTC): 2026-09-23T05:12:08.704520+00:00

These are transparent reference baselines, not production-engine claims.

Corpus layers: curated review-status cases, template-derived cases, seeded synthetic cases, and adversarial cases.

| Engine | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward | Candidate detection | False candidate | Candidate position | Evidence count | Confirm accuracy | Cancel accuracy | P95 latency (µs) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.9068059730915184 | 0.9217638106207067 | 0.015178314343301386 | 0.012628028464481099 | 0.0 | 0.0 | 0.2571041948579161 | 0.0 | 0.0 | 0.0 | 1183 |
| global-fuzzy | 0.8895569464294515 | 0.9471432684792892 | 0.015178314343301386 | 0.011106083665830283 | 0.0 | 0.0 | 0.3382949932341001 | 0.0 | 0.0 | 0.0 | 15828 |
| local-fuzzy | 0.9033068848257848 | 0.9688823989140718 | 0.009481304759162519 | 0.0005141705400847353 | 0.0 | 0.0 | 0.5087956698240866 | 0.0 | 0.0 | 0.0 | 1083 |

## Tracking safety

| Engine | Wrong backward | False movement | False jump commit | Duplicate reanchor error | Catastrophic absolute | Catastrophic backward | Wrong intermediate skip jump |
|---|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.0126 | 0.0538 | 0.1079 | 0.9870 | 0.0152 | 0.0076 | 0.3583 |
| global-fuzzy | 0.0111 | 0.0456 | 0.1079 | 0.9870 | 0.0152 | 0.0076 | 0.6791 |
| local-fuzzy | 0.0005 | 0.0479 | 0.1355 | 0.8898 | 0.0095 | 0.0052 | 0.6738 |

## Event position accuracy by intent and navigation category

| Engine | Intentional skip | Accidental future phrase | Forgotten-word pause | False candidate | Confirmation | Cancellation | Section jump | Skipped blocks | Skip similarity trap | Spoken skip text | Duplicate | Backtrack |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.104 | 0.517 | 1.000 | 0.000 | 0.000 | 0.500 | 0.500 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| global-fuzzy | 0.104 | 0.966 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.935 |
| local-fuzzy | 0.069 | 0.966 | 1.000 | 1.000 | 0.183 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 | 0.099 | 0.935 |

## Candidate evidence by expected jump distance

| Engine | Distance (segments) | Candidate events | Detection | Candidate position | Evidence count | Confirmation |
|---|---:|---:|---:|---:|---:|---:|
| global-exact | 1 | 360 | 0.000 | 1.000 | 0.000 | n/a |
| global-exact | 2 | 12 | 0.000 | 0.833 | 0.000 | 0.000 |
| global-exact | 3 | 242 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-exact | 4 | 120 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-exact | 5 | 122 | 0.000 | 0.008 | 0.000 | 0.000 |
| global-exact | 6 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 7 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 8 | 362 | 0.000 | 0.003 | 0.000 | 0.000 |
| global-exact | 9 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 10 | 4 | 0.000 | 0.250 | 0.000 | 0.000 |
| global-exact | 11 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 12 | 122 | 0.000 | 0.008 | 0.000 | 0.000 |
| global-exact | 13 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 14 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 20 | 120 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-exact | 50 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-fuzzy | 1 | 360 | 0.000 | 1.000 | 0.000 | n/a |
| global-fuzzy | 2 | 12 | 0.000 | 0.833 | 0.000 | 0.000 |
| global-fuzzy | 3 | 242 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-fuzzy | 4 | 120 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-fuzzy | 5 | 122 | 0.000 | 0.008 | 0.000 | 0.000 |
| global-fuzzy | 6 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 7 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 8 | 362 | 0.000 | 0.334 | 0.000 | 0.000 |
| global-fuzzy | 9 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 10 | 4 | 0.000 | 0.250 | 0.000 | 0.000 |
| global-fuzzy | 11 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 12 | 122 | 0.000 | 0.008 | 0.000 | 0.000 |
| global-fuzzy | 13 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 14 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 20 | 120 | 0.000 | 0.000 | 0.000 | 0.000 |
| global-fuzzy | 50 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 1 | 360 | 0.000 | 1.000 | 0.000 | n/a |
| local-fuzzy | 2 | 12 | 0.000 | 0.833 | 0.000 | 0.000 |
| local-fuzzy | 3 | 242 | 0.000 | 0.496 | 0.000 | 0.000 |
| local-fuzzy | 4 | 120 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 5 | 122 | 0.000 | 0.008 | 0.000 | 0.000 |
| local-fuzzy | 6 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 7 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 8 | 362 | 0.000 | 0.707 | 0.000 | 0.000 |
| local-fuzzy | 9 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 10 | 4 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 11 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 12 | 122 | 0.000 | 0.025 | 0.000 | 0.000 |
| local-fuzzy | 13 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 14 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 20 | 120 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 50 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |

## Intentional skip recovery by distance

| Engine | Intentional skip distance | Cases | Recovery | Events to recover median | P95 |
|---|---:|---:|---:|---:|---:|
| global-exact | +2 | 2 | 0.000 | n/a | n/a |
| global-exact | +3 | 2 | 0.000 | n/a | n/a |
| global-exact | +4 | 25 | 0.000 | n/a | n/a |
| global-exact | +5 | 26 | 0.040 | 2 | 2 |
| global-exact | +6 | 2 | 1.000 | 2 | 2 |
| global-exact | +7 | 2 | 1.000 | 2 | 2 |
| global-exact | +8 | 146 | 0.007 | 2 | 2 |
| global-exact | +9 | 2 | 1.000 | 2 | 2 |
| global-exact | +10 | 3 | 0.500 | 2 | 2 |
| global-exact | +11 | 2 | 1.000 | 2 | 2 |
| global-exact | +12 | 25 | 0.040 | 2 | 2 |
| global-exact | +13 | 1 | 1.000 | 2 | 2 |
| global-exact | +14 | 1 | 1.000 | 2 | 2 |
| global-exact | +20 | 24 | 0.000 | n/a | n/a |
| global-exact | +50 | 1 | 0.000 | n/a | n/a |
| global-fuzzy | +2 | 2 | 0.000 | n/a | n/a |
| global-fuzzy | +3 | 2 | 0.000 | n/a | n/a |
| global-fuzzy | +4 | 25 | 0.000 | n/a | n/a |
| global-fuzzy | +5 | 26 | 0.040 | 2 | 2 |
| global-fuzzy | +6 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +7 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +8 | 146 | 0.007 | 2 | 2 |
| global-fuzzy | +9 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +10 | 3 | 0.500 | 2 | 2 |
| global-fuzzy | +11 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +12 | 25 | 0.040 | 2 | 2 |
| global-fuzzy | +13 | 1 | 1.000 | 2 | 2 |
| global-fuzzy | +14 | 1 | 1.000 | 2 | 2 |
| global-fuzzy | +20 | 24 | 0.000 | n/a | n/a |
| global-fuzzy | +50 | 1 | 0.000 | n/a | n/a |
| local-fuzzy | +2 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +3 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +4 | 25 | 0.000 | n/a | n/a |
| local-fuzzy | +5 | 26 | 0.040 | 2 | 2 |
| local-fuzzy | +6 | 2 | 1.000 | 2 | 2 |
| local-fuzzy | +7 | 2 | 1.000 | 2 | 2 |
| local-fuzzy | +8 | 146 | 0.007 | 2 | 2 |
| local-fuzzy | +9 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +10 | 3 | 0.000 | n/a | n/a |
| local-fuzzy | +11 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +12 | 25 | 0.000 | n/a | n/a |
| local-fuzzy | +13 | 1 | 0.000 | n/a | n/a |
| local-fuzzy | +14 | 1 | 0.000 | n/a | n/a |
| local-fuzzy | +20 | 24 | 0.000 | n/a | n/a |
| local-fuzzy | +50 | 1 | 0.000 | n/a | n/a |

## Language breakdown

| Engine | Language | Judged events | Final accuracy | Within 1 |
|---|---|---:|---:|---:|
| global-exact | zh | 45033 | 0.914 | n/a |
| global-exact | en | 40 | 0.750 | n/a |
| global-exact | mixed | 3549 | 0.685 | n/a |
| global-fuzzy | zh | 45033 | 0.908 | n/a |
| global-fuzzy | en | 40 | 0.750 | n/a |
| global-fuzzy | mixed | 3549 | 0.265 | n/a |
| local-fuzzy | zh | 45033 | 0.922 | n/a |
| local-fuzzy | en | 40 | 1.000 | n/a |
| local-fuzzy | mixed | 3549 | 0.265 | n/a |

## Spoken and non-spoken document scenarios

| Engine | Region | Judged events | Final accuracy | Within 1 |
|---|---|---:|---:|---:|
| global-exact | spoken_only | 48272 | 0.911 | n/a |
| global-exact | non_spoken_region | 350 | 0.657 | n/a |
| global-fuzzy | spoken_only | 48272 | 0.900 | n/a |
| global-fuzzy | non_spoken_region | 350 | 0.314 | n/a |
| local-fuzzy | spoken_only | 48272 | 0.908 | n/a |
| local-fuzzy | non_spoken_region | 350 | 0.657 | n/a |

## Failure categories

Highest event error counts per engine:

- **global-exact:** duplicate (1512), near_duplicate (1362), skip (360), jump_confirmation (360), false_jump_candidate (360), missing_words (330), intentional_skip (258), numbers (246)
- **global-fuzzy:** duplicate (1512), near_duplicate (1362), skip (450), jump_confirmation (360), mixed_error (330), stale_partial (304), repeated_final (301), traditional_simplified (300)
- **local-fuzzy:** duplicate (1362), near_duplicate (1362), skip (450), mixed_error (330), stale_partial (304), repeated_final (301), traditional_simplified (300), filler_words (294)

`CSFB_V0_1_BASELINES.md` is retained as a compatibility artifact path; its contents report this v0.2.0-preview dataset and must not be read as v0.1 results.
