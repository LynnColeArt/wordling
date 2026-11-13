# Original 2 by 2 table

In WordPerfect 5.1 US DOS, press Alt+F7, 2 for Tables, and 1 for Create at the start of a blank document. Enter 2 columns and 2 rows. Press F7 to leave Table Edit, then type ALPHA, BETA, GAMMA, and DELTA in successive cells using Tab to advance. Save with F10. This is the source for CMD51-120.

The 577-byte file has a 324-byte prefix. Its table begins with a D2 subtype 0B owner, followed by DC subtype 01 row owners and DC subtype 00 cell owners. The final DC subtype 02 owner follows the last cell. The row and cell owners include layout values, so changing cell text requires an editing and layout contract beyond identifying the framing.

The Wordling terminal test retrieved the original file and reproduced all bytes on both an unchanged F10 save and Save As.

The DOS editing replay retrieves the table, presses Down to enter A1, End,
and types X. It then presses Tab to reach B1, deletes B, and types Z. The
reference saves with Fast Save Yes and No are `EDITYES.WP` and `EDITNO.WP`.
Wordling reproduced both files byte for byte. A fresh DOS guest retrieved
each Wordling output and displayed ALPHAX, ZETA, GAMMA, and DELTA in the
original grid.

The initial editor supported this default standalone 2×2 table layout
with single-line ASCII cells. The original table controls and layout bytes
are preserved. The larger-table increment below extends this scope.

Alt+F7, Tables (2), and Create (1) now creates the default table in a new
document. Enter 2 columns and 2 rows and press F7 to enter the first cell.
The empty Wordling save matches the DOS-created `EMPTY.WP` byte for byte.
DOS reopened that Wordling file, accepted text in A1, and moved to B1 with Tab.

```sh
run_dir=$(mktemp -d /tmp/wordling-table.XXXXXX)
go build -o "$run_dir/wordling" ./cmd/wordling
for mode in yes no create; do
  python3 tests/everyday_qualification/table_edit.py "$PWD" "$run_dir/wordling" "$run_dir/$mode" --fast-save "$mode"
done
```

The larger-table editor supports default standalone Letter tables with two to
four columns and up to 20 rows that fit on one page. Enter inserts a hard
return in a cell. The row grows to fit the tallest cell, and the document
writer updates the row heights and the following cell positions. Cell text
uses printable ASCII and explicit line breaks. Each line must fit its column.

The March 9, 1992 DOS fixtures for this increment include a blank 4×4
(`FOUR.WP`) and 4×5 (`FIVE.WP`), a 3×3 with two lines in A1 and text in B1
(`MULTI.WP`), a 3×3 with three lines in B2 (`MIDDLE.WP`), and the result of
retrieving MULTI and appending X to the second line in A1 with Fast Save No
(`MULTINO.WP`). The terminal replay compares the complete Wordling files
with these originals. DOS Retrieve checks the grid and edited cell text.

```sh
run_dir=$(mktemp -d /tmp/wordling-larger-table.XXXXXX)
go build -o "$run_dir/wordling" ./cmd/wordling
for mode in yes no create four five multi middle edit-multi; do
  python3 tests/everyday_qualification/table_edit.py "$PWD" "$run_dir/wordling" "$run_dir/$mode" --fast-save "$mode"
done
```
