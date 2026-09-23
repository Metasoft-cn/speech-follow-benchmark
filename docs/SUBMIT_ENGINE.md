# Submit an engine result

1. Implement the JSONL subprocess protocol in any language; begin from `examples/echo_engine.py`.
2. Ensure one prediction object is written to stdout for each input line; send diagnostics to stderr.
3. Record engine name/version/commit, platform, CPU, CSFB version, and dataset hash.
4. Run `csfb run --full --engine external --engine-command "python path/to/adapter.py"`.
5. Inspect JSON, CSV, category metrics, and failure JSONL; share the multi-dimensional result without reducing it to a single score.

The runner executes the command with local user permissions and provides no sandbox. Only run trusted code.
