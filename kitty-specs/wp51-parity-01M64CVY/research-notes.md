# Parity research pass 2 — 2026-10-29

User request: identify the best WP 5.1 DOS reference release and expand the manual
inventory into command-level acceptance scenarios. This work stays within M1;
it does not create a third product mission or advance implementation state.

## Decisions and artifacts

- [ADR 0001](../../docs/decisions/0001-reference-release.md) selects plain U.S.
  English WP 5.1 DOS dated 1992-03-09 as the primary documentary target.
- The publisher maintenance list ENH51, reference corrections DOC51 and workbook
  corrections WBC51 are added to the checksum-pinned source register.
- [199 scenario drafts](../../docs/research/command-scenarios.md) link to 91 parent
  groups. Their basis is explicit: manual-derived, stronger project contract, or
  oracle investigation. None has been executed or implemented.
- [Coverage](../../docs/research/scenario-coverage.md) identifies representative
  parent coverage and the remaining deeper command/branch decomposition.
- [36 workbook lessons](../../docs/research/workbook-map.md) have thematic parent
  mappings and candidate scenario links, not step-level replay claims.

## Inventory corrections

Added WP51-089 cross-references, WP51-090 document summaries and WP51-091 binding
offsets. Existing IDs remain stable. WP51-010's erroneous 96-102 copy locator
actually belongs to cross-references (beginning after conversion text on p. 96).
Its copy/move/append coverage is corrected. Capitalization extends onto p. 57.
The old envelope citation at pp. 157-158 was editing-screen options; label and
bundled envelope-helper sources are now used instead.

The workbook's copyright leaf is PDF 3, contents PDF 4-5, and Arabic lesson pages
are PDF +9. Corrected the first pass's off-by-one front-matter references. Its
1989 lesson sequence is not assumed to match later manual lesson references.

## Limits and next work

No executable, emulator or resource profile has been acquired or run. The baseline
registry intentionally has null fingerprint fields. The release recommendation
rests on dated publisher change entries and the secondary chronology's edition
sequence, not on an independently inspected program binary.

Scenarios remain human-readable drafts. Some use named menu navigation where OCR
does not establish a reliable accelerator. Exact prompts/cursor/code positions
must be captured before automation. The network case deliberately leaves original
locking behavior unresolved rather than inventing it. Contract no-edit byte
identity is a Wordling requirement; it is not assumed to be original WP's save
normalization behavior.

Next priorities: acquire/fingerprint the reference and resources; visually confirm
ambiguous source details; build original fixtures/capture procedures; enumerate
macro/merge language commands, equation palette/syntax, graphics/table variants,
printer/resource editing and conversion/error branches. The specification quality
checklist remains open on these points.
