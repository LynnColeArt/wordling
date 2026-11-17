# Font Appearance: Italics in WordPerfect 5.1 DOS

Press Ctrl+F8, Appearance (2), then Italics (4). Type `alpha`,
repeat the menu action to turn Italics off, and type `beta`.
DOS changes the color for the first five characters in the
editor and shows `[ITALC]alpha[italc]beta` in Reveal Codes.
The native owners are `C3 08 C3` and `C4 08 C4`. Standard
Printer overprints underscores under the italic characters.

[Font prompt](font.txt) · [Appearance prompt](appearance.txt) ·
[Reveal Codes](reveal.txt) · [Native save](ITALICS.WP) ·
[Printer output](ITALICS.PRN)

The same workflow is qualified in Wordling. Other Appearance
attributes and printer profiles have separate coverage.
Run `replay.py OUTPUT` and `replay-print.py` from the repo root
with `PYTHONPATH=scripts/reference`.
