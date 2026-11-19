# Macro recording: DOS observations

Ctrl+F10 prompts for a macro name and a description. Typed text
and editing keys also affect the current document while recording.
A second Ctrl+F10 closes the recording. See [name](name.txt),
[description](description.txt) and [editing result](typed.txt).

The original [TYPED.WPM](TYPED.WPM) records `A B`, Enter, `C`,
and Left. It starts the recording with word 0xFC0C, stores the
printable bytes as 16-bit words, records Enter in this context
as 0x800A then 0x000A, stores Left as 0x8019, and ends with 0.
This extends the existing DOS [ABC recording
fixture](../2026-10-29-extended-04/CMD51-131/TESTMAC.WPM).
Wordling now records these inputs with Ctrl+F10 and plays
them with Alt+F10. Its WPMs match the DOS captures byte for byte,
and the original application replays both with the expected
text and cursor position. Playback leaves the WPM unchanged. The existing-file Edit
choice opens the [Macro: Action view](action.txt) for inspection;
closing with F7 leaves the file exactly as acquired. DOS does
the same for an unchanged macro.

DOS shows an [existing file menu](exists.txt) and a [default
No confirmation](replace.txt) before re-recording. Confirmed
replacement starts with an empty description; the existing
file is retained until recording ends. See the [replacement
file](REPLACED.WPM) and the separate [empty description
file](EMPTY.WPM). Wordling also checks that the destination
still matches the one confirmed before replacing it.

The qualified recorder admits printable ASCII other than tilde,
Enter and Left. The [follow-up](../mission1-macro-edit/README.md) adds edits to the
captured Action profile and description changes. Converting 4.x macros
remains open. F1
stops supported playback with the already applied edits intact;
the original CANCEL override modes remain open.

[Linux terminal journeys](../../../../tests/everyday_qualification/macro_recording.py) ·
[DOS replay of Wordling WPMs](replay-wordling.py)

From the repository root, use `PYTHONPATH=scripts/reference
python3 docs/research/reference-runs/mission1-macro-recording/replay.py OUTPUT`.
