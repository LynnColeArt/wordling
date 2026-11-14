# Document Initial Codes in WordPerfect 5.1 DOS

With an empty document, Shift+F8 → Document (3) → Initial Codes (2)
opens a separate [editor](initial.txt). Inside it, Shift+F8 → Line (1)
→ Line Spacing (6) → 2 → Enter changes the [setting](spacing.txt).
Three F7 presses return to normal editing. Reentering Initial Codes
shows [`[Ln Spacing:2]`](reopened.txt).
F1 [leaves the editor open](f1.txt) after the spacing change.

| Case | Captured output |
| --- | --- |
| Set double spacing, return to the body and type `alpha` | [ALPHA.WP](ALPHA.WP) |
| Set double spacing and type `alpha`, Enter, `beta` | [DOUBLE.WP](DOUBLE.WP), [DOUBLE.PRN](DOUBLE.PRN) |
| Reenter Initial Codes, set single spacing and type the same two lines | [RESET.WP](RESET.WP), [RESET.PRN](RESET.PRN) |
| Type 30 double-spaced lines and cross the automatic page break | [PAGES.WP](PAGES.WP), [PAGES.PRN](PAGES.PRN), [page two screen](page-two.txt) |
| Reopen DOUBLE.WP, reset to single spacing and type X at the beginning of the second line | [Fast Save Yes](LOADEDY.WP), [Fast Save No](LOADEDN.WP) |

The two-line body in both saves is exactly `alpha 0A beta`. In this
Standard Printer profile, the double-space owner is `D0 02 08 00 00 01
00 02 08 00 02 D0`. It is stored in a type 3 prefix packet, before the
second index block. The reset save still has that packet, with the
new spacing field set to 1. Setting 1 directly in a new document
produces the same packet. The double-spaced printer stream leaves one
blank row between `alpha` and `beta`.

From the repository root, run
`PYTHONPATH=scripts/reference python3 docs/research/reference-runs/mission1-initial-codes/replay.py OUTPUT double`.
The other branches are `alpha`, `reset`, `single`, and `pages`. The print replay takes the
folder containing the captured `INIT.WP` in `WORDLING_INITIAL_SOURCE` and
`INIT` as its positional argument.

The loaded replay takes `yes` or `no` for Fast Save. The Yes file has
a 576-byte prefix with the previous type 3 owner, Document State and
printer data in retired slots. The No file has a reordered 336-byte
prefix with the live type 3 packet first.

Wordling implements the captured single and double spacing in the
Standard Printer profile. Linux F10 matches the complete DOS files,
including the automatic page break and the first reset of a loaded
file under both Fast Save settings. Both compact and archived files
can reopen and Save As with the original bytes. Other Initial Codes
settings, Summary and named style combinations, and further Fast
Save generations remain open.

[Linux terminal qualification](../../../../tests/everyday_qualification/initial_codes.py)
