# CSFB Specification v0.2.0 Preview

Status: pre-release. Normative terms describe the 0.2.0 preview and may change with a changelog entry before v1.0.

## Problem

Given a script and a time-ordered stream of ASR text events, predict the zero-based position of the script segment currently being read. The benchmark evaluates position tracking, not acoustic recognition quality.

## Canonical segmentation `canonical-2`

Hard breaks are Chinese full stop, exclamation, question, semicolon (`。！？；`), LF/CR line breaks, and English `.`, `!`, `?` when followed by whitespace or end of input. The break character remains attached to the preceding segment. Decimal/version dots before a digit are not sentence boundaries. Empty/whitespace chunks are discarded. Chunks longer than 30 Unicode code points are split deterministically: select the rightmost soft punctuation (`，、,`) in the last 12 code points of the 30-code-point window when available; otherwise split at 30. The last remainder is retained. For structured scripts, each `speech_policy: spoken` block is segmented independently; `skip` blocks remain available as document/navigation metadata and do not consume a speech segment index. Indices are zero-based and stable for a fixed input and version. All adapters receive canonical spoken segments plus the block/section map with `load_script`.

Legacy `script: string` and `{id, text}` scripts are interpreted as one all-spoken document. Structured `{id, blocks}` scripts require each block's type and `speech_policy`; `spoken` blocks contribute canonical segments, while `skip` blocks remain in the document map only. `auto` is reserved in the schema but is invalid in frozen cases until preprocessing resolves it to `spoken` or `skip`. Each spoken segment carries both its compact speech index and originating document block index.

## Event stream

Events are `partial`, `final`, `silence`, or `manual_anchor`. Optional `sequence` supports stale-event cases; optional `timestamp_ms` supports future wall-clock metrics. The v0.1 core score uses event order, not elapsed time. An expectation labels an event index with a canonical expected segment, optional acceptable segment indices, and optional movement/LOST expectations.

## Multi-hypothesis jump evaluation

Cases can annotate a current anchor separately from a forward jump candidate. A predicted `suspect_jump` must keep the committed `segment_index` at the current anchor and may expose `candidate_index`, `jump_status: suspected`, and an evidence count. A later matching event can be expected to emit `confirmed_jump` and commit the candidate. If speech returns to the current passage, the expected status is `cancelled` and the anchor stays. A short isolated future phrase is insufficient evidence by itself. `uncertain` is available for a pause or incomplete current phrase; silence must not invent a new position.

Expected candidate distance and evidence count are labeled per event. Reports stratify candidate detection, candidate position, evidence-count accuracy, and confirmation by distance so behavior on a nearby transition can be compared with a distant intentional skip. These strata measure engine behavior; they do not prescribe fixed distance thresholds or a specific state machine.

CSFB measures these behaviors but does not require every engine to implement a particular state machine. It reports candidate detection, false-candidate, candidate-position, confirmation, cancellation, and expected-state metrics independently.

## Data layers

The manifest separates curated review-status examples, template-derived examples, seeded synthetic cases, and adversarial cases. Language is reported as an independent stratum (`zh`, `en`, or `mixed`; finer tags may appear in case metadata). L1 synthetic cases use a fixed seeded generator. L2 adversarial cases cover duplicate text, non-spoken blocks, intentional skips, accidental future phrases, pauses, section jumps, short ambiguity, and prefix collisions. L3 real-ASR cases are reserved for redistributable recognized text and human position labels; no audio is included.

## Principles and non-goals

Stability before aggressiveness is an evaluation lens, not a required design imposed on engines. Holding position under uncertainty may be preferable to a wrong jump, so wrong forward/backward movement and catastrophic errors are reported separately. CSFB is not an ASR WER, acoustic, speaker, TTS, semantic QA, or LLM benchmark. No single composite score is defined.

## Version policy

Current release line: CSFB v0.2.0 Preview. Before v1.0, schema, expected answers, datasets, and metrics may evolve only with a `CHANGELOG.md` entry and updated manifest. After v1.0, every normative, data, or metric change requires a versioned release; no silent edits.
