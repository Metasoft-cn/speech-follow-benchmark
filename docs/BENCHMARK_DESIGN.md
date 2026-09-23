# Benchmark design

CSFB evaluates temporal text-stream speech-to-script position tracking. Its input begins after speech recognition: script plus ordered partial/final/silence/manual-anchor events. Its output is a canonical spoken-segment index. This isolates alignment behavior from microphone, operating-system ASR, and acoustic conditions. Scripts can be plain text or structured documents with spoken and skipped blocks.

The main failure modes are wrong movement, catastrophic jumps, duplicate-text ambiguity, partial instability, false future-phrase jumps, poor intentional-skip recovery, and inability to recover after an off-script interval. Holding position under uncertainty is measured separately from committing a wrong jump. Scores are reported by category, intent, and language as a metric vector; no composite rank is published.

The preview contains 210 curated review-status cases, 230 template-derived cases, 5,000 seeded synthetic cases, and 1,189 adversarial cases. Each case stores explicit event-index expectations. All engines see the same versioned canonical segmentation. Dataset provenance is limited to original and generated text; L3 real-ASR replay is an interface placeholder and accepts text annotations only.

Non-goals: ASR WER/acoustics, speaker identification, audio quality, TTS, semantic QA, and LLM evaluation. The evaluated unit is a segment, not character timing.
