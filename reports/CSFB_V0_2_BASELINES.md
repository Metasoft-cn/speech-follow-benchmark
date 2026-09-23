# CSFB v0.2.0 Preview Baseline Results

- Cases: 500
- Input events: 1180
- Predictions: 3540
- Dataset SHA256: `242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf`
- Seed: 20260923
- Generator: 0.2.1
- Runner: 0.2.0
- Base Git commit: `1d9b13b2d8a7d1af9f7fbcd8905813a3753ef8a8`
- Working tree dirty: True
- Code SHA256: `9fa1002ff914def7ba225a7777ad85a5899ef65b44380ec741d72a6ca24f85fc`
- Timestamp (UTC): 2026-09-23T05:44:32.727863+00:00

These are transparent reference baselines, not production-engine claims.

Corpus layers: curated review-status cases, template-derived cases, seeded synthetic cases, and adversarial cases.

| Engine | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward | Candidate detection | False candidate | Candidate position | Evidence count | Confirm accuracy | Cancel accuracy | P95 latency (µs) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.909217877094972 | 0.9097872340425532 | 0.00851063829787234 | 0.03914893617021276 | 0.0 | 0.0 | 0.6666666666666666 | 0.0 | 0.0 | 0.0 | 653 |
| global-fuzzy | 0.8924581005586593 | 0.9336170212765957 | 0.00851063829787234 | 0.03659574468085106 | 0.0 | 0.0 | 0.6666666666666666 | 0.0 | 0.0 | 0.0 | 5921 |
| local-fuzzy | 0.9343575418994413 | 0.9676595744680851 | 0.013617021276595745 | 0.000851063829787234 | 0.0 | 0.0 | 0.4666666666666667 | 0.0 | 0.0 | 0.0 | 637 |

## Tracking safety

| Engine | Wrong backward | False movement | False jump commit | Duplicate reanchor error | Catastrophic absolute | Catastrophic backward | Wrong intermediate skip jump |
|---|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.0391 | 0.1147 | 0.1429 | 0.7436 | 0.0085 | 0.0085 | 1.0000 |
| global-fuzzy | 0.0366 | 0.1055 | 0.1429 | 0.7436 | 0.0085 | 0.0085 | 1.0000 |
| local-fuzzy | 0.0009 | 0.0700 | 0.0857 | 0.3590 | 0.0136 | 0.0102 | 0.8000 |

## Event position accuracy by intent and navigation category

| Engine | Intentional skip | Accidental future phrase | Forgotten-word pause | False candidate | Confirmation | Cancellation | Section jump | Skipped blocks | Skip similarity trap | Spoken skip text | Duplicate | Backtrack |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.750 | 0.600 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | n/a | n/a | 0.000 | 1.000 |
| global-fuzzy | 0.750 | 0.800 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | n/a | n/a | 0.000 | 1.000 |
| local-fuzzy | 0.500 | 0.800 | 1.000 | n/a | n/a | n/a | n/a | 1.000 | n/a | n/a | 0.625 | 1.000 |

## Candidate evidence by expected jump distance

| Engine | Distance (segments) | Candidate events | Detection | Candidate position | Evidence count | Confirmation |
|---|---:|---:|---:|---:|---:|---:|
| global-exact | 2 | 10 | 0.000 | 1.000 | 0.000 | n/a |
| global-exact | 5 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 6 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 7 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 8 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 9 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 10 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 11 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 12 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 13 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-exact | 14 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 2 | 10 | 0.000 | 1.000 | 0.000 | n/a |
| global-fuzzy | 5 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 6 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 7 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 8 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 9 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 10 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 11 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 12 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 13 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| global-fuzzy | 14 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 2 | 10 | 0.000 | 1.000 | 0.000 | n/a |
| local-fuzzy | 5 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 6 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 7 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 8 | 2 | 0.000 | 0.500 | 0.000 | 0.000 |
| local-fuzzy | 9 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 10 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 11 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 12 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 13 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |
| local-fuzzy | 14 | 2 | 0.000 | 0.000 | 0.000 | 0.000 |

## Intentional skip recovery by distance

| Engine | Intentional skip distance | Cases | Recovery | Events to recover median | P95 |
|---|---:|---:|---:|---:|---:|
| global-exact | +2 | 1 | n/a | n/a | n/a |
| global-exact | +3 | 1 | n/a | n/a | n/a |
| global-exact | +4 | 1 | n/a | n/a | n/a |
| global-exact | +5 | 2 | 1.000 | 2 | 2 |
| global-exact | +6 | 2 | 1.000 | 2 | 2 |
| global-exact | +7 | 2 | 1.000 | 2 | 2 |
| global-exact | +8 | 2 | 1.000 | 2 | 2 |
| global-exact | +9 | 2 | 1.000 | 2 | 2 |
| global-exact | +10 | 2 | 1.000 | 2 | 2 |
| global-exact | +11 | 2 | 1.000 | 2 | 2 |
| global-exact | +12 | 1 | 1.000 | 2 | 2 |
| global-exact | +13 | 1 | 1.000 | 2 | 2 |
| global-exact | +14 | 1 | 1.000 | 2 | 2 |
| global-fuzzy | +2 | 1 | n/a | n/a | n/a |
| global-fuzzy | +3 | 1 | n/a | n/a | n/a |
| global-fuzzy | +4 | 1 | n/a | n/a | n/a |
| global-fuzzy | +5 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +6 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +7 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +8 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +9 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +10 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +11 | 2 | 1.000 | 2 | 2 |
| global-fuzzy | +12 | 1 | 1.000 | 2 | 2 |
| global-fuzzy | +13 | 1 | 1.000 | 2 | 2 |
| global-fuzzy | +14 | 1 | 1.000 | 2 | 2 |
| local-fuzzy | +2 | 1 | n/a | n/a | n/a |
| local-fuzzy | +3 | 1 | n/a | n/a | n/a |
| local-fuzzy | +4 | 1 | n/a | n/a | n/a |
| local-fuzzy | +5 | 2 | 1.000 | 2 | 2 |
| local-fuzzy | +6 | 2 | 1.000 | 2 | 2 |
| local-fuzzy | +7 | 2 | 1.000 | 2 | 2 |
| local-fuzzy | +8 | 2 | 1.000 | 2 | 2 |
| local-fuzzy | +9 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +10 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +11 | 2 | 0.000 | n/a | n/a |
| local-fuzzy | +12 | 1 | 0.000 | n/a | n/a |
| local-fuzzy | +13 | 1 | 0.000 | n/a | n/a |
| local-fuzzy | +14 | 1 | 0.000 | n/a | n/a |

## Language breakdown

| Engine | Language | Judged events | Final accuracy | Within 1 |
|---|---|---:|---:|---:|
| global-exact | zh | 1060 | 0.917 | n/a |
| global-exact | en | 40 | 0.750 | n/a |
| global-exact | mixed | 75 | 0.944 | n/a |
| global-fuzzy | zh | 1060 | 0.903 | n/a |
| global-fuzzy | en | 40 | 0.750 | n/a |
| global-fuzzy | mixed | 75 | 0.861 | n/a |
| local-fuzzy | zh | 1060 | 0.934 | n/a |
| local-fuzzy | en | 40 | 1.000 | n/a |
| local-fuzzy | mixed | 75 | 0.861 | n/a |

## Spoken and non-spoken document scenarios

| Engine | Region | Judged events | Final accuracy | Within 1 |
|---|---|---:|---:|---:|
| global-exact | spoken_only | 1155 | 0.907 | n/a |
| global-exact | non_spoken_region | 20 | 1.000 | n/a |
| global-fuzzy | spoken_only | 1155 | 0.889 | n/a |
| global-fuzzy | non_spoken_region | 20 | 1.000 | n/a |
| local-fuzzy | spoken_only | 1155 | 0.932 | n/a |
| local-fuzzy | non_spoken_region | 20 | 1.000 | n/a |

## Failure categories

Highest event error counts per engine:

- **global-exact:** duplicate (48), accidental_future_phrase (20), near_duplicate (18), repeated_final (14), substitution (12), intentional_skip (10), repetition (10), missing_words (6)
- **global-fuzzy:** duplicate (48), near_duplicate (18), punctuation (16), repeated_final (14), substitution (12), accidental_future_phrase (10), intentional_skip (10), repetition (10)
- **local-fuzzy:** intentional_skip (20), duplicate (18), near_duplicate (18), punctuation (16), repeated_final (14), substitution (12), prefix_collision (11), accidental_future_phrase (10)
