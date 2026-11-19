# Page number position and suppression in WordPerfect 5.1 DOS

Shift+F8 → Page (2) → Page Numbering (6) → Page Number Position (4)
opens the [position menu](position.txt). Choice 2 is Top Center;
choice 7 is Bottom Right. The fixtures place the number on each
of three explicit pages. Top Center reserves space above the main
body. Bottom Right puts the number at the right margin on row 60.

Page → Suppress (8) → Suppress Page Numbering (4) → Yes at the
start of the first page hides only its number. Pages two and three
still print 2 and 3. The native title page and page-break cache
retain the suppression marker.

| Case | Native DOS document | Standard Printer stream |
| --- | --- | --- |
| Top Center | [TOP.WP](TOP.WP) | [TOP.PRN](TOP.PRN) |
| Bottom Right | [BOTTOM.WP](BOTTOM.WP) | [BOTTOM.PRN](BOTTOM.PRN) |
| First page suppressed | [TITLE.WP](TITLE.WP) | [TITLE.PRN](TITLE.PRN) |

Wordling matches the native codes and printed bytes for these
three explicit-page examples. Other positions, custom numbering
styles, and interactions with automatic pagination and running
headers or footers have not been qualified here.

Run `replay.py OUTPUT 2`, `replay.py OUTPUT 7`, or
`replay.py OUTPUT 7 suppress` from the repo root with
`PYTHONPATH=scripts/reference`; use `replay-print.py` for print
captures.
