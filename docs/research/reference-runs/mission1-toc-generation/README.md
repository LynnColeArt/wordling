# Generating a table of contents: DOS observations

Alt+F5, Define (5), Table of Contents (1) opens the definition.
F7 inserts the default single-level definition. Alt+F5, Generate (6),
Generate Tables, Indexes, Cross-References, etc. (5) asks whether
existing generated material may be replaced. No leaves the document
alone. Yes generates the heading and its page number with a leader.

[DEFIN.WP](DEFIN.WP) and [GEN.WP](GEN.WP) show the contents
definition before and after generation for one heading.
[TWODEF.WP](TWODEF.WP) and [TWOGEN.WP](TWOGEN.WP) add a second
marked heading on page two. DOS creates a blank line between the
entries and refreshes the existing hard-page record. Wordling
matches those native bodies and the single-heading
[Standard Printer stream](GEN.PRN). Generating again leaves the
contents unchanged if the headings and page labels are unchanged.

The original [nested definition capture](NESTED.WP) puts the
definition just inside the opening heading mark.
[Definition](definition.txt) · [Confirmation](confirm.txt) ·
[Declined](declined.txt) · [Generated](generated.txt) ·
[Reveal Codes](reveal-first.txt)

[LVLDEF.WP](LVLDEF.WP) and [LVLGEN.WP](LVLGEN.WP) cover the
two-level definition: level two is indented half an inch and starts
without an extra blank line. Wordling matches both native bodies.

Generation covers one and two levels in the default leader format
with single-line ASCII headings. More levels, wrapped entries,
indexes, lists, and authorities remain open. Run the replay scripts with
`PYTHONPATH=scripts/reference` from the repository root.
