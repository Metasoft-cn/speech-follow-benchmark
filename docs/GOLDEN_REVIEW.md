# Curated corpus review

The preview manifest identifies 210 curated review-status records in `datasets/golden/curated.jsonl`, separately from 230 template-derived cases. Curated records have explicit expected segment labels and review notes covering the intended normalization, occurrence, movement, pause, or block-policy behavior. The original 130 records use small authored templates; the 80-case extension adds authored language variants, shared-prefix cases, and explicitly labeled skip, cancellation, and pause evidence streams. Text or numbering in some scenario variants is generated from those templates, so the set is not described as 210 independently handwritten scripts.

Review checks performed by the generator and dataset validator:

- Stable, unique case IDs and explicit event-to-segment expectations.
- English, Chinese, and mixed-language strata are marked in metadata.
- Structured cases map only `spoken` blocks into canonical speech segments; skipped blocks remain document metadata.
- Duplicate cases annotate the intended occurrence, and intentional skips annotate their initial position and distance.
- Paired jump cases keep the current anchor on first distant evidence, confirm only after continuation, and cancel on return to the current segment.
- Forgotten-word cases include long silence followed by a continuation that resumes the held anchor.
- Review-status records carry a short note describing the label criterion.

This review is a corpus-label review, not an independent external adjudication. Before a final frozen release, contributors should review the curated records independently and record any adjudication changes here.

## Pre-release row review (2026-09-23)

All 210 curated records were read in three consecutive batches and checked against their scripts, event streams, expected positions, difficulty, category, and intended behavior. The review found and corrected these label/content issues before regenerating the preview corpus:

- Shortened overlong English curated sentences where canonical segmentation split a word.
- Rebuilt Chinese and English duplicate scenarios so the repeated occurrence is textually identical and the expected occurrence is explicit.
- Adjusted curated skip examples so the target varies and has a spoken continuation.
- Corrected jump-confirmation and section-jump expectations to point at the actually spoken continuation after the candidate.
- Replaced semantic substitutions mislabeled as homophones with phonetic near-homophones.
- Corrected forgotten-word-then-skip intent/target labels.

The review also checked the resulting corpus invariants: confirmed jump labels point to the labeled candidate continuation; English curated single-sentence records stay within the canonical chunk limit; duplicate labels resolve to the intended occurrence; and review-status cases carry a concise label rationale. This is one contributor's row-by-row dataset review, not external or inter-annotator validation. Template-derived records remain separately counted and are not described as independent handwritten cases.
