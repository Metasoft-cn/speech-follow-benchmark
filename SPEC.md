# CSFB Specification v0.1

Status: pre-release. Normative terms describe version 0.1 behavior and may change with a changelog entry before v1.0.

## Problem

Given a script and a time-ordered stream of ASR text events, predict the zero-based position of the script segment currently being read. The benchmark evaluates position tracking, not acoustic recognition quality.

## Canonical segmentation `canonical-1`

Hard breaks are Chinese full stop, exclamation, question, semicolon (`。！？；`) and LF/CR line breaks. The break character remains attached to the preceding segment. Empty/whitespace chunks are discarded. Chunks longer than 30 Unicode code points are split deterministically: select the rightmost soft punctuation (`，、,`) in the last 12 code points of the 30-code-point window when available; otherwise split at 30. The last remainder is retained. Indices are zero-based and stable for a fixed input and version. All adapters receive the canonical segments with `load_script`.

## Event stream

Events are `partial`, `final`, `silence`, or `manual_anchor`. Optional `sequence` supports stale-event cases; optional `timestamp_ms` supports future wall-clock metrics. The v0.1 core score uses event order, not elapsed time. An expectation labels an event index with a canonical expected segment, optional acceptable segment indices, and optional movement/LOST expectations.

## Data layers

L0 golden cases are explicit authored examples. L1 synthetic cases use a fixed seeded generator. L2 adversarial cases emphasize duplicate text, short ambiguity, and prefix collisions. L3 real-ASR cases are reserved for redistributable recognized text and human position labels; no audio is included.

## Principles and non-goals

Stability before aggressiveness is an evaluation lens, not a required design imposed on engines. Holding position under uncertainty may be preferable to a wrong jump, so wrong forward/backward movement and catastrophic errors are reported separately. CSFB is not an ASR WER, acoustic, speaker, TTS, semantic QA, or LLM benchmark. No single composite score is defined.

## Version policy

Current release line: CSFB v0.1 Preview. Before v1.0, schema, expected answers, datasets, and metrics may evolve only with a `CHANGELOG.md` entry and updated manifest. After v1.0, every normative, data, or metric change requires a versioned release; no silent edits.
