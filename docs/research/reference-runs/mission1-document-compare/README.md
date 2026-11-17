# Document Compare: bounded removal of marks

The retained `BEFORE.WP`/`COMPARE.WP` and `MULBEFR.WP`/`MULTI.WP`
fixtures capture the existing one-changed-ASCII-line comparison, including
unchanged surrounding paragraphs. This change does not expand comparison
creation to several changed lines or phrase-level diffs.

## Removal reference and implementation

WordPerfect 5.1 Reference manual (REF51), printed pages 130 and 549,
describes Alt+F5 → Generate (6) → Remove (1), followed by Y confirmation.
Removal keeps redlined text, removes struck-out text, removes both sets of
attribute codes, and places the cursor at the document end. It also applies
to manually applied marks. The locally read reference PDF SHA-256 is
`ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531`.
No reference binaries or private reference documents were modified or added.

Wordling now implements that bounded operation for ASCII/hard-return text
with balanced Redline and Strikeout attributes. Other formatting and moved
phrase annotations are refused without partial changes. Enter, N, Escape,
F1 and F7 cancel; explicit Y performs the edit. The confirmation wording is
Wordling's wording, not an independently captured original prompt.

`internal/document/compare_cleanup_test.go` checks exact cleaned native bodies
from both retained original comparison outputs, multiple manually marked
regions, overlapping attributes, end-cursor/reveal state, no-op/idempotence,
and atomic refusals. `internal/tui/compare_test.go` checks confirmation,
cancellation, end-position typing, and that editing does not alter the disk
source. Existing comparison modes remain covered by their original tests.

This is manual-backed removal semantics exercised against existing DOS
comparison artifacts, **not a new live DOS cleanup differential capture**.
Open work includes multi-change/phrase/moved-text comparison generation,
formatted and subdocument cleanup, moved-phrase notation removal, and an
original-system differential of removal prompt and visual cursor behavior.
