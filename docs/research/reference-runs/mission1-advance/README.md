# Advance in WordPerfect 5.1 DOS

Shift+F8 → Other (4) → Advance (1) opens the [Advance menu](menu.txt).

- Choose Position (6), enter 3 and type `A`. Then choose Right (5),
  enter 1 and type `B`. The normal text screen shows adjacent
  letters, while Reveal Codes shows `[AdvToPos:3"]A[AdvRgt:1"]B`
  and the status line reports Pos 4.2". The printed letters start
  at 3" and 4.1". [Screen](horizontal.txt) · [Native file](HORIZ.WP) ·
  [Standard Printer stream](HORIZ.PRN)
- After 51 returns, the line containing `bottom` is at 9.5".
  Choose Down (2) and enter 3. DOS leaves the cursor on page 1 at
  10". The code retains the requested distance and the next
  printable character is `Z`. [Before](near-bottom.txt) ·
  [After and Reveal Codes](page-boundary.txt) · [Native file](BOUNDARY.WP)

The native examples use three types within group D3, subfunction 6.
The horizontal examples separate screen cells from printed geometry.
The vertical example separates the requested distance from the clamped
position. Wordling still needs these layout rules and editor commands.

Run `PYTHONPATH=scripts/reference python3 docs/research/reference-runs/mission1-advance/replay.py OUTPUT horizontal`
or substitute `boundary`.
