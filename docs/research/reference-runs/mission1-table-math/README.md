# Table Math: DOS observations

In a default 2 by 2 table, Alt+F7, Math (5), Formula (2) opens
the formula entry. Entering `A1+B1` in A2 stores a relative
formula in a DC/00 cell owner and writes the last result as text.
WordPerfect displays `5.00` for inputs 2 and 3. After changing 2
to 7, the old result remains until Math, Calculate (1) replaces
it with `10.00`. Standard Printer prints the cached value.
[Initial native save](INIT.WP) · [Stale result](stale-result.txt) ·
[Recalculated native save](RECALC.WP) · [Printer bytes](RECALC.PRN)

Math, Copy Formula (3), Cell (1) selects a destination by cursor
movement and Enter. Copying `B1+B1` from A1 to A2 preserves its
relative operands, so it becomes `B2+B2` and displays `10.00`.
[Copied formula](copied.txt) · [Native save](COPY.WP)

Wordling matches these three bodies and the captured Standard
Printer stream. Formula entry currently covers addition of two
relative cell operands, and the print comparison covers a default
standalone 2 by 2 table with single-line ASCII cells. Other operators,
functions, absolute references, range copies, and table formats
remain open.

Run the replay scripts with `PYTHONPATH=scripts/reference` from
the repository root.
