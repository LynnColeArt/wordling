# Center, Flush Right and Hard Space

In the March 9, 1992 reference, Shift+F6 centers `Heading` and Alt+F6
flushes `RIGHT` to the right margin. Each is followed by Enter and a line
at the ordinary left margin. The [native save](LINEFMT.WP) includes each
alignment's C1 owner and 83 before the hard return. Linux matches the
saved codes and the [Standard Printer output](LINEFMT.PRN). The captured
screen places fractional columns on the whole cell to their left.
[Centered heading](centered.txt) ·
[Reveal Codes](reveal.txt)

Format → Other → 9 ends centering without a hard return. The original
places the following text immediately after the centered span, and the
native body contains 8F for `[End C/A]`. [Other menu](format-other.txt) ·
[Reveal Codes](end-centering-reveal.txt) · [Native save](CENTEND.WP) ·
[Printer output](CENTEND.PRN)

Home, Space writes A0. On the last two lines of the same fixture, the
right margin wraps before `alpha[ ]beta`, keeping both words on the next
line. The Linux terminal replay compares the hard-space paragraph's native
body, including its soft return and hard space, with the DOS capture.
DOS Text Save writes an ordinary space and the final DOS EOF byte.
[Wrapped text](hard-space-wrap.txt) ·
[Text export](HSPACE.TXT) ·
[Linux replay](../../../../tests/everyday_qualification/navigation_deletion.py)

Run `replay.py`, `replay-end-centering.py` or `replay-hard-space-export.py`
from the repository root with `PYTHONPATH=scripts/reference`.
