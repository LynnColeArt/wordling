# Widow/Orphan Protection

Shift+F8, Line (1), Widow/Orphan Protection (9), Y enables the rule on
the pinned March 9, 1992 DOS release. N disables it. The two commands
save the single byte owners 8A and 8B, shown as [W/O On] and [W/O Off]
in Reveal Codes.

- [Widow](WIDOW.WP): WordPerfect moves one line across the page break to
  join the isolated last line. The prior wrap becomes a protected soft page.
- [Orphan](ORPHAN.WP): WordPerfect moves the entire paragraph to page 2.
  The hard return before it becomes a protected soft page.
- [End of file](WIDEOF.WP): the last line remains isolated. The page break
  carries a different marker until a hard return closes the paragraph.
- [Toggle](TOGGLE.WP): both explicit codes survive a native save.

Wordling matches all four native bodies. The compared paragraphs wrap
at ordinary spaces. Deletable wraps inside words and other layout
interactions need more work.

[Widow print](WIDOW.PRN) and [orphan print](ORPHAN.PRN) match page
placement; DOS distributes the extra justification space differently
within those lines.

[Prompt](prompt.txt) · [Toggle Reveal Codes](toggle-reveal.txt)

Run the replay from the repository root with
`PYTHONPATH=scripts/reference python3 docs/research/reference-runs/mission1-widow-protection/replay.py WIDOW`.
