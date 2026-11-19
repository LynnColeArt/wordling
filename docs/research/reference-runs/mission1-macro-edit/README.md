# Editing an existing WordPerfect 5.1 DOS macro

Copy the project-recorded [TYPED.WPM](../mission1-macro-recording/TYPED.WPM)
into the guest and use Ctrl+F10 to name it. The existing-file menu
offers Edit (2) and Description (3).

- Edit opens Macro: Action with the caret before Display Off. Move
  right, type Z, and delete A to reproduce [ACTION.WPM](ACTION.WPM).
- Description opens with [the existing text](prefill.txt) and the
  caret at the start. Replace it with Revised, press Enter to return
  to Action, then F7. [DESCR.WPM](DESCR.WPM) has a new description
  extent and body offset, with every action byte intact.
- Ctrl+V then Left inserts an executable Left owner. Ordinary Enter
  inserts a bare 000A word, which breaks a line in the Action window
  but has no effect on DOS playback. A recorded Enter uses two words
  and executes once. [MIDDLE.WPM](MIDDLE.WPM) exercises both forms.
- F7 saves the changed WPM. F1 opens [Cancel changes?](cancel.txt)
  with No as the default. Yes discards the buffer and keeps the
  original file byte for byte.

Wordling reproduces these edit and description paths. It limits
action editing to the captured Display Off/text/Left/Enter profile.
Description edits preserve opaque body bytes when the prefix permits
relocation. Stale files cannot be overwritten by an open editor.

[Linux terminal journeys](../../../../tests/everyday_qualification/macro_edit.py) ·
[DOS replay of Wordling's WPMs](replay-wordling.py)

Run `replay.py OUTPUT action|description|left|commands|middle|cancel` from
the repo root with `PYTHONPATH=scripts/reference`.
