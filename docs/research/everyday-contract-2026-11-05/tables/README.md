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

The editor currently supports this default standalone 2×2 table layout
with single-line ASCII cells. The original table controls and layout bytes
are preserved. Other layouts remain outside the cell editor's scope.

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
