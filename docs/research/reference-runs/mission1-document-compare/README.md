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
inserted or removed lines, multiple changed lines, and the
separate command to remove comparison marks remain open.

[Go comparisons](../../../../internal/tui/compare_test.go) ·
[Linux terminal journey](../../../../tests/everyday_qualification/document_compare.py) ·
[DOS replay of a Wordling save](reopen-wordling.py)

Run [replay.py](replay.py) with an output directory from the
repository root with `PYTHONPATH=scripts/reference`.
