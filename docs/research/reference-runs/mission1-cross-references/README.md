# Cross-referencing pages: DOS observations

Alt+F5, Cross-Ref (1), Mark Reference (1), Page Number (1)
inserts an unresolved named reference. Mark Target (2) at the target
inserts a named marker. Both names are displayed in uppercase. Generate
(Alt+F5, 6, 5, Yes) replaces the question mark with the target page
number, even when the names were entered in different cases.
[Before](BEFORE.WP) · [After](AFTER.WP) · [Standard Printer](AFTER.PRN)

Mark Both (3) records the reference location before the cursor moves to
the target. Enter selects the target location; the name commits both
codes and displays the page number immediately. Repeating Generate
preserves the codes. [Native save](BOTH.WP) · [Position prompt](position.txt)

Wordling matches these document bodies and the Standard Printer stream.
The two-page renumbering captures verify that the generated number is the
label DOS prints, including uppercase Roman numerals.
[Arabic before](NUMDEF.WP) · [Arabic after](NUMGEN.WP) ·
[Roman before](ROMDEF.WP) · [Roman after](ROMGEN.WP)

Other reference types and targets inside expanded subdocuments remain
open. Run the replay scripts with `PYTHONPATH=scripts/reference` from the
repository root.
