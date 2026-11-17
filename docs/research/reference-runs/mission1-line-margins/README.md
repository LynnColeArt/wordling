# Left and right margins

The March 9, 1992 original accepts Left and Right consecutively under
Shift+F8, Line, Margins. The 2-inch left and 1.5-inch right settings apply
after the native margin code at the start of the second paragraph. The
previous paragraph retains its original margins. The second paragraph
wraps using the 50-column printable width.

[Line Format](line-format.txt) · [Reveal Codes](reveal.txt)

Run `replay.py` with `PYTHONPATH=scripts/reference` from the repository root.
The [native save](MARGINS.WP) has a single 16-byte margin owner immediately
after the hard return at body offset 7. Its previous margins are 1200/1200
WordPerfect units and its new margins are 2400/1800. The subsequent soft
return marks the new wrap position. Linux matches the native body and
[Standard Printer output](MARGINS.PRN).

The [mid-line case](inline-reveal.txt) inserts a hard return before the margin
record. The new margins take effect on the new line, and the original preceding
text stays on its own line. The [native save](INLINE.WP) confirms the same
margin owner preceded by a hard return. The [printer output](INLINE.PRN)
retains the leading and trailing spaces and expands interword spacing
on the wrapped line.
