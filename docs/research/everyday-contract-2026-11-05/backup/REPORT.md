# Original backup and exit-save observations

Focused WP78 research input for the everyday editing milestone, recorded
2026-11-05. This extends the reference contract without changing the previous
research report or its evidence.

## Observed setting and default

In the pinned original 03/09/92 application, follow Shift+F1, Environment (3),
Backup Options (1), Original Document Backup (2).

The default Original Document Backup value is No. The same screen shows Timed
Document Backup enabled with a 30-minute interval. Timed backup was not exercised.

Selecting option 2 and Y enables original backup. Selecting option 2 and N
disables it. F7 leaves the settings screen.

## File effects

The authored document is C:\OUT\BASE.WP. Stage snapshots were created by DOS COPY
inside the guest. The disk was read with mtools only after WordPerfect exited
and the guest stopped.

| Setting and operation | Current document | Original backup |
| --- | --- | --- |
| Disabled, first save | BASE.WP contains ONE | No BASE.BK! |
| Disabled, second save with explicit overwrite | BASE.WP contains ONE TWO | No BASE.BK! |
| Enabled, first save | BASE.WP contains ONE | No BASE.BK! |
| Enabled, second save with explicit overwrite | BASE.WP contains ONE TWO | BASE.BK! contains the complete preceding ONE file |
| Enabled, third save through F7 Save Yes | BASE.WP contains ONE TWO THREE | BASE.BK! is replaced with the complete preceding ONE TWO file |
| Disable backup, then save a fourth version | BASE.WP contains ONE TWO THREE FOUR | BASE.BK! is deleted |

The backup uses the document's basename and extension .BK!, in the same directory.
It replaces the prior backup rather than accumulating numbered versions.

The checks.json file records byte-for-byte comparisons between the original
saved stages and the corresponding guest-made backup snapshots. files.json and
directory.txt in each run record the stopped-disk exports and directory listings.

## Overwrite default and refusal

A repeated F10 save prompts for Document to be saved, prefilled with the current
name. Enter at that filename prompt opens

    Replace C:\OUT\BASE.WP? No (Yes)

Enter at the replacement question declines replacement and returns to the
filename prompt. Y explicitly accepts replacement.

The first exploratory command sequences incorrectly expected Enter to accept.
Their downstream waits failed, and those failures remain in trace.jsonl.
The original remained in its actual filename/replacement prompt. Subsequent
explicit Y completed the saves. The disabled run's
04-second-save-complete screenshot therefore documents the returned filename
prompt despite its premature capture label.

These observations establish the prompt transition on refusal. This probe did
not export a separate post-refusal disk snapshot before subsequently accepting
replacement. A formal refusal-byte-preservation test should capture that
checkpoint independently.

## F7 Save Yes to an existing name

The successful enabled-run sequence is

1. Append THREE to the already-saved ONE TWO document.
2. F7 opens Save document? Yes (No).
3. Y opens Document to be saved with C:\OUT\BASE.WP prefilled.
4. Enter opens Replace C:\OUT\BASE.WP? No (Yes).
5. Y writes the replacement and rotates the original backup.
6. The original then asks Exit WP? No (Yes), with Cancel to return to document.
7. F1 returns to the same editing document.
8. Guest DOS COPY preserves the current file and backup for later comparison.

Thus saving during Exit uses the original file and backup lifecycle and then
continues to the exit question. It must not terminate immediately after the save
or skip the overwrite decision.

## Documentary corroboration and remaining questions

The original Reference manual, printed pages 41–43, describes the .BK! name,
same-directory location, replacement of the preceding backup and deletion at the
next save after original backup is disabled. These points were observed above.

The manual additionally says files with the same basename but different
extensions share one original backup name. This collision behavior was not
exercised here and remains documentary evidence.

This probe does not establish recovery behavior for disk-full, permission,
rename, interrupted-write or backup-rotation failures. FC-009 still requires
safe failure tests in the Linux implementation and original observations where
needed to preserve backup conventions. Timed backup remains separate original
functionality.

## Provenance and scope

Two independent fresh guests used the existing hash-checked master/profile,
offline QEMU and private sockets. The disabled and enabled scenarios have their
own environment metadata, frozen control source, chronological trace and raw
screen/raster captures. Native exports are authored test documents. Original
executables and disk images remain in the local private cache.

This is focused qualitative research, with one completed sequence for each
setting. It is not formal acceptance or an independent repeat campaign.
The current Wordling implementation and all Spec Kitty planning/status files
were untouched.
