# Metrics

All rates are reported as numerator/denominator-derived fractions, without a combined score. Accuracy treats an event as correct if its predicted index equals the expected index or appears in `acceptable_segments`.

- Event and final accuracy; within-1 and within-2 segment accuracy.
- Mean, median, and P95 absolute segment error.
- Wrong forward/backward movement rate: the engine moved in that direction from its preceding predicted anchor and the current position is outside the annotated expected/acceptable positions.
- Wrong movement rate on explicitly annotated `should_move: false` events; false LOST rate only uses events explicitly annotated `should_be_lost: false`.
- Catastrophic absolute error: absolute error >= 5 segments. Catastrophic backward error: prediction is >= 3 segments behind expected. Report separately.
- LOST rate and false LOST rate on annotated events; recovery success and recovery event latency when an engine emits a `recovered` state after LOST.
- Anchor reversals: partial-event anchor direction changes in a three-anchor oscillation pattern. Partial stability is exposed as the reversal count.
- If confidence is emitted, high-confidence means confidence >= 0.8; report accuracy and wrong rate among those predictions.
- Mean, median, P95, and P99 process latency in microseconds. This is observational and varies by host; deterministic comparisons exclude latency.

Movement expectations allow wrong-movement analysis on events where `should_move` is false. `should_be_lost` supports false-LOST analysis. Accuracy is not a substitute for safety-oriented movement metrics: a hold can be inconvenient, while a confident jump to the wrong passage can lose the reader's place.
