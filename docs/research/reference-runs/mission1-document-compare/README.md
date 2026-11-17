# Document Compare: DOS observations

Save `Alpha old tail` as BEFORE.WP. Replace `old` with `new` on
screen, keeping the old file unchanged. Press Alt+F5, Generate
(6), then Compare (2). The Other Document field defaults to the
open document's filename. DOS marks the full current line as
redline and appends the full old line as strikeout. The original
Standard Printer overprints the two spans with periods and
hyphens respectively.

[Native input](BEFORE.WP) · [Compare prompt](compare.txt) ·
[Reveal Codes](reveal.txt) · [Native result](COMPARE.WP) ·
[Printer stream](COMPARE.PRN)

Wordling reproduces a single replacement between two ASCII
documents with corresponding hard-return lines. In the
[multiline capture](multiline.txt), WordPerfect keeps the common
first and last paragraphs and includes each changed line's hard
return inside its mark. See the [before](MULBEFR.WP) and
[after](MULTI.WP) native documents. Formatted documents,
inserted or removed lines and multiple changed lines remain open.
Removal of comparison marks is covered by the bounded operation below.

[Go comparisons](../../../../internal/tui/compare_test.go) ·
[Linux terminal journey](../../../../tests/everyday_qualification/document_compare.py) ·
[DOS replay of a Wordling save](reopen-wordling.py)

Run [replay.py](replay.py) with an output directory from the
repository root with `PYTHONPATH=scripts/reference`.

## Bounded removal of marks

The retained `BEFORE.WP`/`COMPARE.WP` and `MULBEFR.WP`/`MULTI.WP`
fixtures capture the existing one-changed-ASCII-line comparison, including
unchanged surrounding paragraphs. This change does not expand comparison
creation to several changed lines or phrase-level diffs.

### Removal reference and implementation

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
