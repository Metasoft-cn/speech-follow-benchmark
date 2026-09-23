# Engine protocol

The protocol is newline-delimited JSON over a subprocess's stdin/stdout; it is language- and platform-neutral. The runner starts a trusted command and sends one `load_script` object before case events. Segment records may include `section_id`, `role` (`heading` or `content`), and `navigation_only`; `sections` carries section ranges and heading/navigation indices. Headings can remain navigation anchors when excluded from spoken-text matching.

```json
{"type":"load_script","script_id":"script_001","text":"大家好。今天开始。","initial_segment_index":0,"blocks":[{"id":"heading_1","type":"heading","text":"第一部分","speech_policy":"skip","speech_segment_start":0,"speech_segment_end":-1},{"id":"paragraph_1","type":"paragraph","text":"大家好。","speech_policy":"spoken","speech_segment_start":0,"speech_segment_end":0}],"segments":[{"index":0,"text":"大家好。","section_id":"section_1","role":"content","navigation_only":false}],"sections":[{"id":"section_1","start_segment":0,"end_segment":0,"navigation_only_block_ids":["heading_1"]}]}
```

Then it sends exactly one case event per line:

```json
{"type":"partial","text":"大家好","sequence":1}
{"type":"final","text":"大家好。","sequence":2}
{"type":"silence","duration_ms":5000}
{"type":"manual_anchor","segment_index":20}
```

For each input line, write exactly one JSON prediction line to stdout and flush it. The minimum response is:

```json
{"segment_index":0}
```

Optional fields: `char_position` (non-negative integer), `confidence` (number 0..1), `state` (`locked`, `suspect_jump`, `confirmed_jump`, `uncertain`, `lost`, `recovered`), `jump_status` (`none`, `suspected`, `confirmed`, `cancelled`), `candidate_index`, `candidate_score`, `jump_evidence`, and `score`. A suspected jump must preserve `segment_index`; a confirmed jump may commit it. A cancelled candidate returns to ordinary tracking at the current anchor. Diagnostics belong on stderr, never stdout. The runner initializes/reset state for every case by sending `load_script` to the adapter process. `initial_segment_index` is optional and defaults to 0. Canonical segment indices are the only scored position coordinate.

The example `examples/echo_engine.py` is a tiny working adapter. External engine commands run arbitrary local programs; the benchmark does not sandbox them.
