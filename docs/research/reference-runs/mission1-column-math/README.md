# Column Math: DOS observations

Alt+F7, Math (3), On (1) starts a calculation area. Tab inserts
a decimal tab with the default ruler. Math, Off (2) ends the area
and ordinary typing resumes. [Scope and tab record](MATH.WP) ·
[Math menu](math-menu.txt) · [Reveal Math Off](math-off.txt)

With rows labelled N and S, enter 3 and 5 in the same math column,
then add a row labelled T with the subtotal operator (+) in that
column. Math, Calculate (4) inserts `8.00` before the subtotal
owner, displays `8.00+`, and prints `8.00` without the operator.
[Before Calculate](before-calculate.txt) · [Calculated](calculated.txt) ·
[Native output](TOTAL.WP) · [Standard Printer output](TOTAL.PRN)

Wordling matches both native bodies and the subtotal printer stream
for this single default column of whole numbers. Other functions,
multiple columns, and the Math column definitions remain open.

Run the replay scripts from the repository root with
`PYTHONPATH=scripts/reference`.
