# Engine protocol

The protocol is newline-delimited JSON over a subprocess's stdin/stdout; it is language- and platform-neutral. The runner starts a trusted command and sends one `load_script` object before case events.

```json
{"type":"load_script","script_id":"script_001","text":"大家好。今天开始。","initial_segment_index":0,"segments":[{"index":0,"text":"大家好。"},{"index":1,"text":"今天开始。"}]}
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

Optional fields: `char_position` (non-negative integer), `confidence` (number 0..1), `state` (`locked`, `lost`, `recovered`), `candidate_index`, and `score`. Diagnostics belong on stderr, never stdout. The runner initializes/reset state for every case by sending `load_script` to the adapter process. `initial_segment_index` is optional and defaults to 0; cases use it only when the scenario explicitly starts mid-script. Canonical segment indices are the only scored position coordinate.

The example `examples/echo_engine.py` is a tiny working adapter. External engine commands run arbitrary local programs; the benchmark does not sandbox them.
