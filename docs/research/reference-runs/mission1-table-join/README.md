# Joining table cells: DOS observations

In a default 2 by 2 table containing ALPHA, BETA, GAMMA, and DELTA,
Alt+F7 opens Table Edit while inside a cell. With A1 active, Alt+F4
starts cell selection. Right selects A1:B1, and Down selects A1:A2.
Join (7) prompts `Join cells? No (Yes)`.

[Horizontal join](ROWJOIN.WP) keeps A1 and B1 content in one cell
with a native tab between the old columns. The second cell's owner
is removed, but the other row and its two cells remain. [Vertical
join](VERT.WP) keeps both rows: A1 contains a hard return between its
original text and the text from A2, while the A2 owner stays as a
continuation of the combined cell.

[Block](block.txt) · [Confirmation](join.txt) · [Result](joined.txt)

Wordling matches the top-row horizontal join, preserves the other
row, and reproduces the [printer stream](ROWJOIN.PRN). Declining
leaves the table unchanged. Editing within the combined cell,
vertical joins and other table sizes remain open. Run the replay scripts with
`PYTHONPATH=scripts/reference` from the repository root.
