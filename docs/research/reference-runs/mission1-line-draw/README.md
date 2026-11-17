# Line Draw: DOS observations

Ctrl+F3, Line Draw (2), then 1 selects a single line and 2
selects a double line. From the start of a blank document,
four Right presses create a five-character run with two end
caps. F7 leaves Line Draw and the caret sits on the last cap.

The files contain native extended characters in WordPerfect set 3.
For a single line the numbers are 50, 8, 8, 8, and 48.
For a double line they are 54, 19, 19, 19, and 52.
[Single file](SINGLE.WP) · [Double file](DOUBLE.WP) ·
[Single Reveal](reveal-1.txt) · [Double Reveal](reveal-2.txt)

Wordling matches the visible horizontal stroke and both native bodies.
Other directions, corners, erasing and changing existing strokes,
and printing with a line-draw printer profile remain open.
Run `replay.py` with `PYTHONPATH=scripts/reference` from the
repository root.
