# WordPerfect 4.2 conversion in the 5.1 DOS utility

At the DOS prompt, launch `CONVERT` and provide the source and
destination filenames. The [main menu](conversion-menu.txt) lists
option 8, WordPerfect 4.2 to WordPerfect 5.1. The [export menu](export-formats.txt)
offers ASCII and other formats. It has no WordPerfect 4.2 output
option, so this path cannot produce the missing original 4.2 fixture.

The capture verifies the utility menus. A 4.2-authored document and
its conversion and retrieval results are still needed for the
Wordling comparison.

Run `PYTHONPATH=scripts/reference python3 docs/research/reference-runs/mission1-convert-42/replay.py OUTPUT`
from the repository root.
