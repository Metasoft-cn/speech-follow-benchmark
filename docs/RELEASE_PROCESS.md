# Release process

1. Review spec, schemas, golden labels, license provenance, and all changes.
2. Regenerate corpus; run twice and compare `datasets/MANIFEST.json` and logical predictions/metrics (ignore latency and host metadata).
3. Run `pytest`, `csfb validate`, `csfb run --quick`, and `csfb run --full` on supported Python versions.
4. Review category metrics and failure examples; ensure reports contain benchmark/runner versions and dataset hash.
5. Update changelog and release checklist. Before v1.0, identify the result as a preview.
6. Tag locally only after all gates pass. Publishing requires an explicitly configured remote and an explicit release request.
