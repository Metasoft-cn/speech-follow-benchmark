# Release process

1. Review the specification, schemas, expected labels, dataset provenance, and all diffs.
2. Regenerate the corpus twice and compare manifests and canonical predictions/metrics, excluding timestamps, host metadata, and latency.
3. Run unit tests, schema validation, quick benchmark, and full benchmark on supported Python versions.
4. Review category metrics and representative failures. Preserve the pre-expansion baseline and explain changed metrics.
5. Audit repository contents for private paths, credentials, and third-party text.
6. Verify the configured CI workflow on the hosted repository and record the actual run URL/result.
7. Update the changelog and release checklist. A preview is not a final v0.2.0 release.
8. Create a final tag only after dataset, golden review, local checks, determinism, and hosted CI gates pass.

This checkout has no configured Git remote, so GitHub Actions cannot be run or verified from this workspace. No final release tag is created.
