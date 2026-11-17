# Conditional End of Page

The March 9, 1992 DOS release opens this command with Shift+F8, Other
(4), Conditional End of Page (2). With the caret on the line above
the heading, entering 3 records the keep count at the caret.

- [ROOM](ROOM.WP) leaves the heading and two lines on page 1.
- [SHORT](SHORT.WP) moves them to page 2 and adds a derived soft page
  to the hard return after the condition.
- [EDGE](EDGE.WP) reaches the ordinary page boundary, where DOS still
  records that the condition prompted the page break.

Wordling matches the three native bodies and the page shown in the status
line. The [SHORT print stream](SHORT.PRN) also matches byte for byte.
These captures cover a single condition preceding a hard return in
single spaced text. Wrapped lines, stacked conditions and mixed spacing
need additional DOS comparisons.

[Prompt](prompt.txt) · [Short page Reveal Codes](short-reveal.txt)

Run the replay from the repository root with
`PYTHONPATH=scripts/reference python3 docs/research/reference-runs/mission1-conditional-page/replay.py SHORT`.
