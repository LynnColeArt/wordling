# Top and bottom margins

Shift+F8, Page, Margins sets the top and bottom values at a page boundary.
The original inserts a D0 subfunction 5 owner after the hard page. At
2 inches top and 1.25 inches bottom, the next page's baseline starts at
2 inches. [Reveal Codes](reveal.txt) · [Native save](PAGEMAR.WP) ·
[Printer output](PAGEMAR.PRN)

With the same values applied at the beginning of a document, the 46th
line ends the first page. The end-of-page owner carries the 9,300-unit
printable height and 2,400-unit top margin. Linux reproduces the
automatic page break and matches the native body and printer bytes.
[Screen](automatic-page.txt) · [Native save](AUTO.WP) ·
[Printer output](AUTO.PRN)

Run the replay scripts with `PYTHONPATH=scripts/reference` from the repository root.
