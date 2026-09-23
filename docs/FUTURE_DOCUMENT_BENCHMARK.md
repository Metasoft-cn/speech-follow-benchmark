# Future Document Import Benchmark

The current CSFB benchmark measures speech following after a script has already
been converted to its canonical block and spoken-segment representation. It does
not score DOCX, PDF, PPTX, or HTML parsing. Keeping that boundary prevents
document-extraction errors from being confused with speech-alignment errors.

A future, independent benchmark may measure the conversion:

```text
source document → canonical ScriptDocument
```

Candidate metrics:

- **Text preservation:** exact or normalized text retained from the source.
- **Reading order:** blocks and segments appear in the intended sequence.
- **Heading detection:** title and heading blocks receive appropriate types.
- **Note detection:** notes and stage directions are distinguished from spoken text.
- **Non-spoken detection:** speech policy suggestions match reviewed labels.
- **Header and footer detection:** repeated page furniture is identified without
  suppressing actual body content.
- **Table extraction:** cell content, order, and source coordinates are retained.

Such a benchmark should use small, self-authored, redistributable fixtures and
report parser warnings separately from silent extraction errors. PDF reading
order and ambiguous layout classification need explicit uncertainty labels.
Human-reviewed labels should remain the reference for policy suggestions.

This is a future scope proposal only; it does not add a second document-parser
benchmark to CSFB v0.2.
