# CSFB v0.1 Baseline Results

- Cases: 5390
- Input events: 45813
- Predictions: 137439
- Dataset SHA256: `a8eaa5189e8d06f1db67eafaf1c467bcd3d18f1470a2e9d4b793324e4d5f526e`
- Seed: 20260923
- Generator: 0.1.0
- Runner: 0.1.0
- Git commit: `d3e2cca04cc058bbe1c890c8784a1ca136cca051`
- Timestamp (UTC): 2026-09-23T03:16:47.482076+00:00

These are transparent reference baselines, not production-engine claims.

| Engine | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward | Recovery | P95 latency (µs) |
|---|---:|---:|---:|---:|---:|---:|
| global-exact | 0.9216069260412817 | 0.9195331695331695 | 0.0 | 0.003071253071253071 | None | 373 |
| global-fuzzy | 0.9298949480019004 | 0.9425675675675675 | 0.0 | 0.003071253071253071 | 0.0 | 12251 |
| local-fuzzy | 0.9372855408330254 | 0.9678834678834679 | 0.0 | 0.0 | 0.0 | 1489 |

## Failure categories

Highest event error counts per engine:

- **global-exact:** duplicate (1492), near_duplicate (1362), short_segment (1050), missing_words (882), substitution (384), skip (360), mixed_error (306), prefix_collision (267)
- **global-fuzzy:** duplicate (1492), near_duplicate (1362), short_segment (1050), skip (360), substitution (270), prefix_collision (267), stale_partial (256), mixed_error (234)
- **local-fuzzy:** duplicate (1362), near_duplicate (1362), short_segment (1050), skip (360), partial_growth (272), substitution (270), prefix_collision (267), stale_partial (256)
