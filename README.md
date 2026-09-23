# Chinese Speech Follow Benchmark (CSFB)

**A reproducible benchmark for evaluating real-time speech-to-script alignment in teleprompters and voice-follow applications.**

CSFB measures the path from an **ASR recognized-text stream** to a **canonical spoken-script segment position**. It evaluates temporal tracking: text similarity alone cannot distinguish identical occurrences, and a wrong jump has a different cost from holding position. CSFB v0.2.0-preview is a pre-release benchmark, not an industry standard.

## Quick start

Python 3.11+; core code uses only the standard library.

```powershell
cd chinese-speech-follow-benchmark
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
csfb validate
csfb run --quick
```

From a source checkout without installation, use `python -m csfb.cli validate` and `python -m csfb.cli run --quick`. Generate a deterministic corpus with `csfb generate`; run everything with `csfb run --full`; inspect a case with `csfb replay --case adversarial_duplicate_0001 --trace`.

## Scope and privacy

CSFB v0.2.0-preview evaluates recognized **text events**, not audio. It is not an ASR word-error-rate, acoustic quality, speaker recognition, TTS, or language-model benchmark. Benchmark execution requires no audio, user recordings, private user text, network access, GPU, paid API, or LLM. It includes Chinese, English, and mixed-language text cases.

## Results

See [`reports/CSFB_V0_2_BASELINES.md`](reports/CSFB_V0_2_BASELINES.md) for actual reference runs and category breakdown. Generated values are not hard-coded into this README. The three built-in baselines are simple reference algorithms, not production trackers or a leaderboard ranking.

Their exact algorithms and thresholds are described in [`docs/BASELINES.md`](docs/BASELINES.md).

Accuracy alone is insufficient. An engine with 98% accuracy and frequent catastrophic jumps may behave worse for a reader than one with 96% accuracy and rare wrong movement. CSFB reports multiple dimensions and does not create a single composite score.

## What is tested

Exact text; punctuation and spacing; fillers; missing and extra words; substitutions and homophone-like forms; numbers; mixed English; simplified/traditional variants; partial growth and correction; repeated finals; stale partials; silence; duplicate and near-duplicate phrases; prefix collisions; short ambiguous segments; backtracking; forward skips; forgotten-word pauses followed by a deliberate skip; LOST and recovery; long scripts; mixed errors.

The preview corpus contains 210 curated review-status cases, 230 template-derived cases, 5,000 seeded synthetic cases, and 1,189 adversarial cases. Curated labels have explicit review notes; some scenario variants use authored templates. The dataset combines original text across daily speech, products, teaching, technology, numbers, and scripts, and does not reproduce news articles, books, blogs, commercial copy, film dialogue, or user recordings.

The adversarial suite distinguishes **intentional skips** from **accidental future phrases**. A candidate can be reported while the committed anchor stays put; the next event can confirm it or cancel it. Forgotten-word pauses test whether an engine holds position, including the case where the reader resumes by intentionally skipping ahead. Candidate detection, candidate position, evidence count, and confirmation are reported by jump distance. Section jumps carry heading/navigation metadata, including headings excluded from spoken matching.

Structured cases can mark headings, notes, stage directions, headers, and other blocks as `speech_policy: "skip"`: they do not count as spoken segments, while document block and spoken-segment indices remain mapped in the adapter's `load_script` navigation data. Legacy plain-text scripts remain supported as all-spoken documents.

## Canonical positions

All engines receive the same versioned spoken segments, defined in [`SPEC.md`](SPEC.md): hard breaks include Chinese sentence marks, English `.!?` before whitespace/end, and line breaks; overlong chunks are deterministically soft-split at at most 30 Unicode code points. The evaluated output is segment-level. Character timing is out of scope for this preview.

## Third-party engines

Any language can participate through the JSONL subprocess protocol. The runner sends `load_script` with canonical segments, then one event per line on stdin; it reads one prediction JSON object per line from stdout. See [`docs/ENGINE_PROTOCOL.md`](docs/ENGINE_PROTOCOL.md) and the runnable [example adapter](examples/echo_engine.py). A subprocess command runs arbitrary local code; run only trusted programs.

## Dataset integrity

`datasets/MANIFEST.json` records version, seed, generator, file hashes, case counts, and event counts. `csfb generate` recreates the same bytes for the same version and seed. Dataset and metric changes are recorded in `CHANGELOG.md`; once v1.0 freezes, silent changes are prohibited.

## License

- Code: [Apache-2.0](LICENSE)
- Dataset: [CC0 1.0 Universal](DATASET_LICENSE.md) for original and synthetic examples only; no third-party restricted data is included.

## Roadmap

- v0.1: initial segment-level benchmark and public adapter protocol.
- v0.2: semantic preview with non-spoken blocks, intent/jump labels, and language strata.
- Future: annotated real-ASR text replay, broader Traditional Chinese coverage, and character-level tracking.
- v1.0: future frozen specification, schemas, metrics, and datasets.

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/BENCHMARK_DESIGN.md`](docs/BENCHMARK_DESIGN.md), [`docs/METRICS.md`](docs/METRICS.md), and [`docs/GITHUB_RELEASE_CHECKLIST.md`](docs/GITHUB_RELEASE_CHECKLIST.md).
