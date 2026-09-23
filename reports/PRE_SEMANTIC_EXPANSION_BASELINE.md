# Pre-Semantic Expansion Baseline

**PRE_EXPANSION_BASELINE = FROZEN**

- Git HEAD: `7ab8e1a0dbe4df9dced19820c9e69586fe0fed85`
- Cases: 5390
- Input events: 45813
- Dataset SHA256: `a8eaa5189e8d06f1db67eafaf1c467bcd3d18f1470a2e9d4b793324e4d5f526e`
- Seed: 20260923

## Overall baseline

| Engine | Final accuracy | Within 1 | Catastrophic absolute | Catastrophic backward | Wrong backward | Wrong forward | False movement | Recovery | P95 latency µs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | 0.9216069260412817 | 0.9195331695331695 | 0.0 | 0.006712881712881713 | 0.003071253071253071 | 0.015575640575640575 | 0.017230726985652502 | None | 373 |
| global-fuzzy | 0.9298949480019004 | 0.9425675675675675 | 0.0 | 0.006712881712881713 | 0.003071253071253071 | 0.018668831168831168 | 0.016578567996155695 | 0.0 | 12251 |
| local-fuzzy | 0.9372855408330254 | 0.9678834678834679 | 0.0 | 0.00408037908037908 | 0.0 | 0.0308002808002808 | 0.014072904510194275 | 0.0 | 1489 |

## All category metrics

| Engine | Category | Cases/events judged | Final accuracy | Within 1 | Catastrophic absolute | Catastrophic backward | Wrong backward | False movement | LOST | Recovery | P95 µs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global-exact | backtrack | 1372 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 17 |
| global-exact | duplicate | 1492 | 0.0 | 0.0 | 0.0 | 0.08042895442359249 | 0.0871313672922252 | 0.10276679841897234 | 0.0 | None | 16 |
| global-exact | english_mixed | 1372 | 0.8776371308016878 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 20 |
| global-exact | exact | 1398 | 0.872093023255814 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 20 |
| global-exact | extra_words | 1378 | 0.8739495798319328 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 22 |
| global-exact | filler_words | 1378 | 0.8823529411764706 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 21 |
| global-exact | homophone_like | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 6 |
| global-exact | long_script | 14915 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 486 |
| global-exact | long_sentence | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 11 |
| global-exact | lost_recovery | 1372 | 0.8734177215189873 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 20 |
| global-exact | manual_reanchor | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | None | 0.0 | None | 8 |
| global-exact | missing_words | 1378 | 0.38235294117647056 | 0.969521044992743 | 0.0 | 0.0 | 0.0 | 0.022239872915011914 | 0.0 | None | 22 |
| global-exact | mixed_error | 1368 | 0.7763157894736842 | 1.0 | 0.0 | 0.0 | 0.0 | 0.006304176516942475 | 0.0 | None | 21 |
| global-exact | near_duplicate | 1362 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 16 |
| global-exact | numbers | 1372 | 0.8270042194092827 | 1.0 | 0.0 | 0.0 | 0.0 | 0.005573248407643312 | 0.0 | None | 21 |
| global-exact | partial_correction | 15 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 6 |
| global-exact | partial_growth | 1831 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 20 |
| global-exact | prefix_collision | 1669 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.19044222539229672 | 0.0 | None | 11 |
| global-exact | punctuation | 1372 | 0.8818565400843882 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 26 |
| global-exact | repeated_final | 1589 | 0.8546255506607929 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 22 |
| global-exact | repetition | 10 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | None | 5 |
| global-exact | short_segment | 1372 | 0.2616033755274262 | 0.4446064139941691 | 0.0 | 0.13556851311953352 | 0.0 | 0.03127641589180051 | 0.0 | None | 7 |
| global-exact | silence | 1601 | 0.8607594936708861 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 19 |
| global-exact | skip | 1362 | 0.73568281938326 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 21 |
| global-exact | skip_forward | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | None | 0.0 | None | 34 |
| global-exact | spacing | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 9 |
| global-exact | stale_partial | 1816 | 0.8590308370044053 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 23 |
| global-exact | substitution | 1378 | 0.7310924369747899 | 1.0 | 0.0 | 0.0 | 0.0 | 0.004827031375703942 | 0.0 | None | 21 |
| global-exact | traditional_simplified | 1362 | 0.8061674008810573 | 1.0 | 0.0 | 0.0 | 0.0 | 0.007177033492822967 | 0.0 | None | 21 |
| global-fuzzy | backtrack | 1372 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.827259475218659 | 0.0 | 189 |
| global-fuzzy | duplicate | 1492 | 0.0 | 0.0 | 0.0 | 0.08042895442359249 | 0.0871313672922252 | 0.10276679841897234 | 0.7607238605898123 | 0.0 | 279 |
| global-fuzzy | english_mixed | 1372 | 0.8776371308016878 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.827259475218659 | 0.0 | 209 |
| global-fuzzy | exact | 1398 | 0.872093023255814 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8154506437768241 | 0.0 | 196 |
| global-fuzzy | extra_words | 1378 | 0.8739495798319328 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8272859216255443 | 0.0 | 229 |
| global-fuzzy | filler_words | 1378 | 0.8823529411764706 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8272859216255443 | 0.0 | 200 |
| global-fuzzy | homophone_like | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 30 |
| global-fuzzy | long_script | 14915 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.07609788803218237 | 0.0 | 13089 |
| global-fuzzy | long_sentence | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 78 |
| global-fuzzy | lost_recovery | 1372 | 0.8734177215189873 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8519675202998126 | 0.0 | 194 |
| global-fuzzy | manual_reanchor | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | None | 0.0 | None | 53 |
| global-fuzzy | missing_words | 1378 | 0.865546218487395 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8272859216255443 | 0.0 | 193 |
| global-fuzzy | mixed_error | 1368 | 0.8289473684210527 | 1.0 | 0.0 | 0.0 | 0.0 | 0.006304176516942475 | 0.8333333333333334 | 0.0 | 212 |
| global-fuzzy | near_duplicate | 1362 | 0.0 | 0.7400881057268722 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8333333333333334 | 0.0 | 259 |
| global-fuzzy | numbers | 1372 | 0.8565400843881856 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8345481049562682 | 0.0 | 207 |
| global-fuzzy | partial_correction | 15 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.06666666666666667 | 0.0 | 19 |
| global-fuzzy | partial_growth | 1831 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.008746355685131196 | 0.6204259967231022 | 0.0 | 218 |
| global-fuzzy | prefix_collision | 1669 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.19044222539229672 | 0.6800479328939485 | 0.0 | 158 |
| global-fuzzy | punctuation | 1372 | 0.8396624472573839 | 1.0 | 0.0 | 0.0 | 0.0 | 0.007980845969672785 | 0.827259475218659 | 0.0 | 235 |
| global-fuzzy | repeated_final | 1589 | 0.8546255506607929 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.7142857142857143 | 0.0 | 240 |
| global-fuzzy | repetition | 10 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | None | 69 |
| global-fuzzy | short_segment | 1372 | 0.2616033755274262 | 0.4446064139941691 | 0.0 | 0.13556851311953352 | 0.0 | 0.03127641589180051 | 0.827259475218659 | 0.0 | 155 |
| global-fuzzy | silence | 1601 | 0.8607594936708861 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8519675202998126 | 0.0 | 176 |
| global-fuzzy | skip | 1362 | 0.73568281938326 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8333333333333334 | 0.0 | 181 |
| global-fuzzy | skip_forward | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | None | 0.0 | None | 50 |
| global-fuzzy | spacing | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 139 |
| global-fuzzy | stale_partial | 1816 | 0.8590308370044053 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.7406387665198237 | 0.0 | 237 |
| global-fuzzy | substitution | 1378 | 0.8109243697478992 | 1.0 | 0.0 | 0.0 | 0.0 | 0.004827031375703942 | 0.8272859216255443 | 0.0 | 195 |
| global-fuzzy | traditional_simplified | 1362 | 0.8678414096916299 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8333333333333334 | 0.0 | 202 |
| local-fuzzy | backtrack | 1372 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 272 |
| local-fuzzy | duplicate | 1492 | 0.3641456582633053 | 0.7667560321715817 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 357 |
| local-fuzzy | english_mixed | 1372 | 0.8776371308016878 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 267 |
| local-fuzzy | exact | 1398 | 0.872093023255814 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 254 |
| local-fuzzy | extra_words | 1378 | 0.8739495798319328 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 299 |
| local-fuzzy | filler_words | 1378 | 0.8823529411764706 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 282 |
| local-fuzzy | homophone_like | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 33 |
| local-fuzzy | long_script | 14915 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 1634 |
| local-fuzzy | long_sentence | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 122 |
| local-fuzzy | lost_recovery | 1372 | 0.8734177215189873 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.14303560274828234 | 0.0 | 261 |
| local-fuzzy | manual_reanchor | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | None | 0.0 | None | 352 |
| local-fuzzy | missing_words | 1378 | 0.865546218487395 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 271 |
| local-fuzzy | mixed_error | 1368 | 0.8289473684210527 | 1.0 | 0.0 | 0.0 | 0.0 | 0.006304176516942475 | 0.0 | None | 297 |
| local-fuzzy | near_duplicate | 1362 | 0.0 | 0.7400881057268722 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 352 |
| local-fuzzy | numbers | 1372 | 0.8565400843881856 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.01239067055393586 | 0.0 | 259 |
| local-fuzzy | partial_correction | 15 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.2 | 0.0 | 34 |
| local-fuzzy | partial_growth | 1831 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0478134110787172 | 0.08738394320043692 | 0.0 | 281 |
| local-fuzzy | prefix_collision | 1669 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.19044222539229672 | 0.0 | None | 182 |
| local-fuzzy | punctuation | 1372 | 0.8396624472573839 | 1.0 | 0.0 | 0.0 | 0.0 | 0.007980845969672785 | 0.0 | None | 298 |
| local-fuzzy | repeated_final | 1589 | 0.8546255506607929 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 332 |
| local-fuzzy | repetition | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 125 |
| local-fuzzy | short_segment | 1372 | 0.2616033755274262 | 0.4446064139941691 | 0.0 | 0.13556851311953352 | 0.0 | 0.03127641589180051 | 0.0 | None | 164 |
| local-fuzzy | silence | 1601 | 0.8607594936708861 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 250 |
| local-fuzzy | skip | 1362 | 0.73568281938326 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 252 |
| local-fuzzy | skip_forward | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | None | 0.0 | None | 198 |
| local-fuzzy | spacing | 10 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 81 |
| local-fuzzy | stale_partial | 1816 | 0.8590308370044053 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.125 | 0.0 | 317 |
| local-fuzzy | substitution | 1378 | 0.8109243697478992 | 1.0 | 0.0 | 0.0 | 0.0 | 0.004827031375703942 | 0.0 | None | 264 |
| local-fuzzy | traditional_simplified | 1362 | 0.8678414096916299 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | None | 262 |

## Failure counts

| Engine | Incorrect judged events | Cases with >=1 incorrect judged event |
|---|---:|---:|
| global-exact | 8609 | 1744 |
| global-fuzzy | 7632 | 1602 |
| local-fuzzy | 7549 | 1519 |

## Catastrophic metric audit (pre-expansion definition)

- Catastrophic absolute: segment error >= 5, measured to the nearest expected/acceptable segment.
- Catastrophic backward: prediction is at least 3 segments behind the nearest acceptable expected position.
- The three pre-expansion rates were zero. This is recorded as the observed result; the expansion adds occurrence, false-jump, and intent-specific metrics to test whether the zero reflected missing semantics.
- The pre-expansion runner and metric implementation did not record jump candidate, evidence-count, confirmation, cancellation, or intentional-skip recovery fields. Those historical jump metrics are unavailable; they are not inferred or backfilled from predictions.

This report freezes the pre-expansion result only. It does not claim the old dataset covers non-spoken regions, user intent, or language-balanced cases.
