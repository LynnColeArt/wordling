# Word navigation

March 9, 1992 US WordPerfect 5.1. [Checkpoints](checkpoints.json) record
zero-based BIOS caret coordinates and the active Reveal Codes cells. The base
multiline replay is `replay.py`, run from the repository root with
`PYTHONPATH=scripts/reference`.

Ctrl+Left and Ctrl+Right treat punctuation within a run of text as part of
the word. They cross repeated spaces, tabs and hard returns. With Reveal Codes
visible they stop on the first character of the target word, past any opening
format code. At either end of the document, pressing the same direction again
keeps the caret there.

[Editing checkpoints](editing-checkpoints.json) cover Block character selection,
Block Enter, Ctrl+Backspace and Ctrl+Delete, Ctrl+End, and Home followed by
Backspace or Delete. A word deletion leaves an empty Bold pair in place and
Undelete inserts the removed text after the pair.

[Go To checkpoints](goto-checkpoints.json) cover the prompt, character seek,
hard-return seek, no match and ordinary page 2.
