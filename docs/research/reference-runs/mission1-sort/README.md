# Sorting secondary merge records: DOS observations

The [input](BEFORE.WP) contains two native records. Zebra and Amber
are the first fields; the second fields, Keep Z and Keep A, make it
possible to check that entire records move together.

Ctrl+F9, Sort (2), and Enter twice choose screen input and output.
Select Type (7), Merge (1), and Perform Action (1). The default
ascending key is alphabetical, field 1, line 1, word 1. The [sorted
native body](SORTED.WP) puts Amber and Keep A first, keeps both
End Field and End Record owners, and renumbers both page records.

Wordling matches the native body for this on-screen workflow.
Sorting disk files directly, other key definitions, and richer
record formats remain open.
[Sort prompt](sort.txt) · [Type](record-type.txt) ·
[Criteria](merge-criteria.txt) · [Sorted screen](sorted.txt)

Run `replay.py` from the repository root with
`PYTHONPATH=scripts/reference`.
