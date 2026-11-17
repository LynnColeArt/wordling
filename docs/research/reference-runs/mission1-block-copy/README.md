# Block Copy and Append

The March 9, 1992 WordPerfect 5.1 reference opens Move with Ctrl+F4.
Choosing `1 Block`, then `2 Copy`, clears the selection and displays
“Move cursor; press Enter to retrieve.” The caret can move before Enter
and stays at the insertion point afterwards. The original word stays
in place and the copy carries the Bold pair even when the normal-screen
selection contains only the displayed letters. [Prompt](copy-choice.txt) ·
[Reveal Codes](reveal.txt) · [DOS document](BLOCK.WP)

Choosing `4 Append` instead prompts for an existing filename. With
`APPEND` in Bold on the editing screen and `BEGIN` in the target, the DOS
target's body is `BEGIN` immediately followed by the attributed text.
If the target is absent, DOS creates it with the same attributed fragment.
The Linux terminal replay compares both native bodies and saves the source
to verify that its native bytes stayed intact. [Prompt](append-prompt.txt) ·
[Existing target](APPEND.WP) · [New target](NEWAPP.WP) ·
[Linux replay](../../../../tests/everyday_qualification/navigation_deletion.py)

Run `replay.py`, `replay-append.py` and `replay-append-new.py` from the repository root with
`PYTHONPATH=scripts/reference`. Each run uses a disposable guest disk.
