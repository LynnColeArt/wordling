# Permanent compatibility contract

These are project requirements, not claims about an implemented application.
They apply to both missions.

| ID | Obligation | Acceptance evidence |
| --- | --- | --- |
| FC-001 | Save native documents as original WP 5.1 files. No replacement container, private version, or required sidecar. | Original WP 5.1 opens, edits, prints, and saves Wordling-created files; Wordling reopens the results. |
| FC-002 | An untouched valid supported input saves byte-identically. | SHA-256 and direct byte comparison, including prefix packets and embedded data. Opening must not silently normalize the source. |
| FC-003 | Editing preserves unrelated codes, packet content, embedded resources, and semantic relationships. | Targeted edit fixtures; binary differences explained; original-app retrieval and behavior checked. Offset/length changes are permitted when required, arbitrary normalization is not. |
| FC-004 | Unknown or not-yet-supported structures are preserved. Unsafe edits/saves fail explicitly before replacing the original. | Opaque-code and packet fixtures, reference checks, rejected-edit and failed-save scenarios with original bytes unchanged. |
| FC-005 | Original companion artifacts retain their original formats wherever the app reads/writes them. | Per-format fixtures and original-app checks for macros, styles, merge data, keyboard definitions, and user resources; scope expanded from manual research. |
| FC-006 | Characters preserve their WP character-set identities and round-trip. | Character-set corpus; unsupported input receives an explicit error or choice before modification, never silent replacement. |
| FC-007 | Native saves are independent of conversion through another word processor. | The Go format writer emits original-format data directly; external tools may be independent test witnesses only. |
| FC-008 | Original export/conversion and print-to-disk modes retain their documented formats and semantics. | Per-mode comparison against original output with encoding, resources, and conversion losses declared. These modes do not replace the native save format. |
| FC-009 | A failed save must not corrupt the existing file. | Tests for permissions, interrupted/short writes, full storage, and failed replacement; original backup conventions researched and preserved. |
| FC-010 | PDF is a new, optional M2 export. It never becomes the editable native document format. | M2 PDF acceptance tests against the shared layout output and native-file preservation checks. |

## Fidelity levels

Byte identity is required for no-edit native round-trips. After an edit, the whole
file need not have identical bytes: lengths, pointers, and related state may need
to change. Differences must be confined to the intended edit and required
structural updates, with unrelated data preserved.

Behavioral fidelity includes command sequences, prompts, code/cursor semantics,
selection, error handling, pagination, and rendered/printed results. A matching
screen alone does not establish format or behavioral compatibility.

Exact pagination needs a declared printer, font metrics, resources, settings, and
reference output. Linux printer delivery may differ operationally; document
layout or original print-to-disk bytes must not change without an explicit,
tested adaptation decision.

## Reference baseline and remaining installation work

- Primary documentary target: plain WP 5.1 DOS, U.S. English, 1992-03-09.
  See [ADR 0001](decisions/0001-reference-release.md). Selection does not narrow
  the original language/character compatibility obligations.
- The executable and 158 installed files are fingerprinted in
  [the baseline registry](research/reference-baseline.json). Fifty-three bounded original
  reference recipes have been repeated; Wordling and full scenarios remain unverified.
- The [current reference environment](research/reference-environment/README.md)
  uses FreeDOS 1.4 and a July 1992 text-only printer resource alongside the
  confirmed March program. Historical DOS and graphics/pagination profiles remain
  to be established; this is not an untouched March shipping-set claim.
- OS/emulator, keyboard, display settings, and filesystem behavior.
- Installed printer definitions, fonts, dictionaries, hyphenation resources.
- Repeatable input fixtures and keystroke captures with provenance.
- Differences between the 6/92 reference manual, the 11/89 workbook, and later
  toolkit documentation; record applicability rather than assuming equivalence.

Encrypted documents, graphics preview, legacy printer resources, DOS integration,
and resource licensing remain explicit research obligations. Uncertainty does not
remove them from M1 scope or establish support.
