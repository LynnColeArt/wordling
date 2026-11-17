# Literal printer commands: DOS observations

Shift+F8, Other (4), Printer Functions (6), Printer Command (2),
Command (1) opens literal entry. `<36>TEST` becomes the bytes
`$TEST` inside a native D9/00 command owner. Enter accepts the
command and F7 returns to editing.

The document shows `BeforeAfter` in the main pane and
`Before[Ptr Cmnd:$TEST]After` in Reveal Codes. The Standard
Printer output contains `Before$TESTAfter` in the same position.
Wordling matches the native body and the complete output stream.
[Native document](PRTCMD.WP) · [Printer output](PRTCMD.PRN) ·
[Input](command-input.txt) · [Reveal Codes](reveal.txt)

The fixture covers an embedded literal command sent to a disk
print file. Printer-command files and printer-specific behavior
remain open. Run the replay scripts from the repository root with
`PYTHONPATH=scripts/reference`.
