# Chinese Speech Follow Benchmark (CSFB)

**A reproducible benchmark for evaluating real-time speech-to-script alignment in Chinese teleprompters, reading-follow systems, and voice-follow applications.**

> A teleprompter that pauses is inconvenient. A teleprompter that confidently jumps to the wrong paragraph is broken.

CSFB measures the path from an **ASR recognized-text stream** to a **canonical script segment position**. It focuses on wrong jumps, repeated text, recovery, partial stability, and latency alongside ordinary accuracy. CSFB v0.1 is a pre-release open benchmark, not an industry standard.

## Quick start

Python 3.11+; core code uses only the standard library.

```powershell
git clone https://github.com/REPLACE_ME/chinese-speech-follow-benchmark.git
cd chinese-speech-follow-benchmark
python -m venv .venv
.venv\Scripts\activate
pip install -e .
csfb validate
csfb run --quick
```

From a source checkout without installation, use `python -m csfb.cli validate` and `python -m csfb.cli run --quick`. Generate a deterministic corpus with `csfb generate`; run everything with `csfb run --full`; inspect a case with `csfb replay --case adversarial_duplicate_0001 --trace`.

## Scope and privacy

CSFB v0.1 evaluates recognized **text events**, not audio. It is not an ASR word-error-rate, acoustic quality, speaker recognition, TTS, or language-model benchmark. No audio, user recordings, private user text, network, GPU, paid API, or LLM is used or required. Real ASR replay may be added from text, timestamps, event kinds, and human position annotations only.

## Results

See [`reports/CSFB_V0_1_BASELINES.md`](reports/CSFB_V0_1_BASELINES.md) for actual reference runs and category breakdown. Generated values are not hard-coded into this README. The three built-in baselines are simple educational reference points, not contenders or a leaderboard ranking.

Their exact algorithms and thresholds are described in [`docs/BASELINES.md`](docs/BASELINES.md).

Accuracy alone is insufficient. An engine with 98% accuracy and frequent catastrophic jumps may behave worse for a reader than one with 96% accuracy and rare wrong movement. CSFB reports multiple dimensions and does not create a single composite score.

## What is tested

Exact text; punctuation and spacing; fillers; missing and extra words; substitutions and homophone-like forms; numbers; mixed English; simplified/traditional variants; partial growth and correction; repeated finals; stale partials; silence; duplicate and near-duplicate phrases; prefix collisions; short ambiguous segments; backtracking; forward skips; LOST and recovery; long scripts; mixed errors.

The dataset combines human-written original examples and deterministic synthetic cases across daily speech, company/product introductions, teaching, technology, finance, news-like original prose, speeches, self-introductions, short video, livestream, number-heavy, English-mixed, and technical text. It does not reproduce news articles, books, blogs, commercial copy, film dialogue, or user recordings.

## Canonical positions

All engines receive the same versioned segments, defined in [`SPEC.md`](SPEC.md): hard breaks are `。！？；` and line breaks; overlong chunks are deterministically soft-split at at most 30 Unicode code points. The evaluated output is segment-level. Character timing is out of scope for v0.1.

## Third-party engines

Any language can participate through the JSONL subprocess protocol. The runner sends `load_script` with canonical segments, then one event per line on stdin; it reads one prediction JSON object per line from stdout. See [`docs/ENGINE_PROTOCOL.md`](docs/ENGINE_PROTOCOL.md) and the runnable [example adapter](examples/echo_engine.py). A subprocess command runs arbitrary local code; run only trusted programs.

## Dataset integrity

`datasets/MANIFEST.json` records version, seed, generator, file hashes, case counts, and event counts. `csfb generate` recreates the same bytes for the same version and seed. Dataset and metric changes are recorded in `CHANGELOG.md`; once v1.0 freezes, silent changes are prohibited.

## License

- Code: [Apache-2.0](LICENSE)
- Dataset: [CC0 1.0 Universal](DATASET_LICENSE.md) for original and synthetic examples only; no third-party restricted data is included.

## Roadmap

- v0.1: segment-level deterministic synthetic benchmark and public adapter protocol.
- v0.2: annotated real-ASR text replay.
- v0.3: expanded Traditional Chinese coverage.
- v0.4: character-level tracking metrics.
- v1.0: frozen specification, schemas, metrics, and datasets.

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/BENCHMARK_DESIGN.md`](docs/BENCHMARK_DESIGN.md), [`docs/METRICS.md`](docs/METRICS.md), and [`docs/GITHUB_RELEASE_CHECKLIST.md`](docs/GITHUB_RELEASE_CHECKLIST.md).
