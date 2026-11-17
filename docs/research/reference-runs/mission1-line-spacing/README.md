# Line spacing

Format → Line → Line Spacing writes a D0 subfunction 2 owner with the
previous and new spacing values. In the March 9, 1992 DOS capture, double
spacing begins with the second paragraph. The first line remains at 1 inch,
and the second and third are at 1.17 and 1.5 inches. A subsequent code
restores single spacing. Linux matches the displayed position and native
save. [Screen](doubled.txt) · [Reveal Codes](reveal.txt) ·
[Native save](SPACING.WP)

The automatic page fixture shows a page break after 27 double-spaced rows.
Its native record stores the physical row at the break. The Linux body
matches the DOS save. [Screen](automatic-page.txt) · [Native save](SPACEAUT.WP)

Format → Line → Line Height → Fixed sets the baseline advance directly.
At 0.2 inches, the following line in the fixture starts at 1.37 inches.
The D0 subfunction 0 owner stores 240 units. The separate pagination
fixture retains the exact 10,560-unit distance to the last baseline on
page 1. Both native bodies match the Linux saves. [Reveal Codes](height-reveal.txt) ·
[Native save](HEIGHT.WP) · [Pagination save](HEIGHTPG.WP)

Run the replays from the repository root with `PYTHONPATH=scripts/reference`.
