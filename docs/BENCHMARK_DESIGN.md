# Benchmark design

CSFB evaluates text-stream speech-to-script position tracking. Its input begins after speech recognition: script plus ordered partial/final/silence/manual-anchor events. Its output is a canonical segment index. This isolates alignment behavior from microphone, operating-system ASR, and acoustic conditions.

The main failure modes are wrong movement, catastrophic jumps, duplicate-text ambiguity, partial instability, and inability to recover after an off-script interval. Scores are reported by category and as a metric vector; no composite rank is published.

The benchmark includes authored golden examples and seeded synthetic/adversarial streams. Each case stores explicit event-index expectations. All engines see the same versioned canonical segmentation. Dataset provenance is limited to original and generated text; L3 real-ASR replay is an interface placeholder and accepts text annotations only.

Non-goals: ASR WER/acoustics, speaker identification, audio quality, TTS, semantic QA, and LLM evaluation. The v0.1 evaluated unit is a segment, not character timing.
