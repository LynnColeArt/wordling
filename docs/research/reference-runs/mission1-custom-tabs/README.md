# Custom tab rulers and hard decimal alignment

On WordPerfect 5.1 for DOS, Shift+F8, Line (1), Tab Set (8) opens the
ruler. Type 2.2 and press Enter to add a left stop measured from the
margin; F7 twice writes the new setting. The preceding paragraph keeps
its original tab. Type → Absolute interprets the same measurement
from the page edge.

Ctrl+F6 uses the next tab stop as a fixed anchor. Input before the
first period occupies cells to its left. Typing the period adds the
alignment terminator before it, and Enter ends alignment on the
integer-only line. In the native save the decimal tab's start
position changes with the integer width.

Press D at a ruler stop to make it a decimal stop. Tab then selects
the ruler's decimal anchor. DOS uses a different native code from
Ctrl+F6, and both routes place the decimal points at the same column
within each fixture. A subsequent plain Tab or Ctrl+F6 can close the
current decimal field and start another. [Chained fields](CHAIN.WP)

Wordling matches the native bodies and Standard Printer streams.
Center and right ruler stops, repeating interval entry, dot leaders,
and alignment on another character still need work.

[Relative save](RELATIVE.WP) · [Relative screen](relative-screen.txt) ·
[Relative print](RELATIVE.PRN) · [Absolute save](ABSOLUTE.WP) ·
[Absolute screen](absolute-screen.txt) · [Absolute print](ABSOLUTE.PRN) ·
[Decimal stop](DECIMAL.WP) · [Decimal stop print](DECIMAL.PRN)

DOS Text export also matches the aligned spaces in the
[relative](RELATIVE.TXT) and [decimal ruler](DECIMAL.TXT) captures.

Run the replay scripts from the repository root with
`PYTHONPATH=scripts/reference`.
