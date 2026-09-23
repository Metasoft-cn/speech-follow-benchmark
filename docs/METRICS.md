# Metrics

All rates are reported as numerator/denominator-derived fractions, without a combined score. Accuracy treats an event as correct if its predicted index equals the expected index or appears in `acceptable_segments`.

- Event and final accuracy; within-1 and within-2 segment accuracy.
- Mean, median, and P95 absolute segment error.
- Wrong forward/backward movement rate: the engine moved in that direction from its preceding predicted anchor and the current position is outside the annotated expected/acceptable positions.
- Wrong movement rate on explicitly annotated `should_move: false` events; false LOST rate only uses events explicitly annotated `should_be_lost: false`.
- False jump commit rate counts a wrong forward movement of at least 3 segments on an explicitly labelled no-commit event: `none`, `cancelled`, or `suspected` with `should_move: false`. False movement rate is separately reported for all no-move annotations.
- Duplicate reanchor error rate compares predicted index with the explicitly annotated repeated occurrence. Intentional-skip recovery is case-level and succeeds when the predicted anchor reaches the confirmed target at or after the first suspected candidate event; events-to-recover counts from that first candidate event.
- Wrong intermediate skip jump rate checks whether the anchor moves away from the expected current position before the target confirmation event.
- Jump candidate detection and candidate-position accuracy; false candidate rate on events where no candidate should remain; confirmation accuracy requires both a confirmed status and the expected committed position; cancellation accuracy requires a cancelled status and the original expected position.
- Candidate distance is measured from the expected current anchor and reported in distance strata. Each stratum reports detection, candidate-position accuracy, evidence-count accuracy, and confirmation; these are measurements, not mandated threshold values.
- State accuracy on explicitly annotated events (`locked`, `suspect_jump`, `confirmed_jump`, `uncertain`, `lost`, `recovered`).
- Catastrophic absolute error: absolute error >= 5 segments. Catastrophic backward error: prediction is more than 2 segments behind expected. Report separately.
- LOST rate and false LOST rate on annotated events; recovery success and recovery event latency when an engine emits a `recovered` state after LOST.
- Anchor reversals: partial-event anchor direction changes in a three-anchor oscillation pattern. Partial stability is exposed as the reversal count.
- If confidence is emitted, high-confidence means confidence >= 0.8; report accuracy and wrong rate among those predictions.
- Mean, median, P95, and P99 process latency in microseconds. This is observational and varies by host; deterministic comparisons exclude latency.

Movement expectations allow wrong-movement analysis on events where `should_move` is false. `should_be_lost` supports false-LOST analysis. Accuracy is not a substitute for safety-oriented movement metrics: a hold can be inconvenient, while a confident jump to the wrong passage can lose the reader's place.
