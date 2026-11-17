# Footnote continuation

Ctrl+F7, Footnote (1), Options (4), Amount of Note to Keep Together (2)
sets a distance in inches from the caret forward. On the captured
two-inch body page, setting 0.5 inches splits the six-line footnote
three and three. Setting 1.25 inches moves the note reference and
the whole footnote to the following page. A separate [four-and-two split](ASYM.WP)
checks the unequal continuation fields. A page with room keeps the
footnote in one piece at the original reference.

The DOS native saves record the option, reference and split in both
the nested note body and the surrounding page layout. Wordling
matches those records except for two bytes immediately before the
inline note number in the multiline owner. Those bytes are preserved
on read; their original meaning is unresolved. Both Standard Printer
streams match byte for byte.

This fixture covers one footnote whose text uses hard returns under
the default printer, with at most one continuation. Multiple long
footnotes, automatic wrapping inside notes, continued-message
options, and styled text need broader qualification.

[Option prompt](option-prompt.txt) · [Room](ROOM.WP) ·
[Split save](SPLIT.WP) · [Split Reveal Codes](split-reveal.txt) ·
[Split print](SPLIT.PRN) · [Keep save](KEEP.WP) ·
[Keep Reveal Codes](keep-reveal.txt) · [Keep print](KEEP.PRN)

Replay the split or keep case from the repository root using
`PYTHONPATH=scripts/reference python3 docs/research/reference-runs/mission1-note-continuation/replay.py 0 dot 5`
or pass `1 dot 2 5`. Run `replay-room.py` for the case with room.
