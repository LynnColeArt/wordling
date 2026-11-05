# Everyday editing reference contract

Research input to the existing WP 5.1 parity mission, recorded 2026-11-05.
These are original-app observations. They do not establish Wordling parity.

## F1 returns focus while keeping the submenu drawn

The earlier UI study waited for the word Full to disappear after pressing F1
inside Layout > Justify. That was an incorrect visual oracle.

Fresh runs r2 and r3 both reproduce this sequence.

1. Alt+= activates the menu bar.
2. L opens Layout and J selects Justify.
3. The Left entry in the child submenu has selected red attribute 0x47.
4. F1 changes precisely eight attribute bytes on that row to normal menu
   attributes 0x71 and mnemonic 0x74. The character grid is unchanged.
5. Up then selects Endnote in the parent Layout menu and displays the Endnote
   child menu. This confirms that focus returned to the parent.
6. Esc then returns to the menu bar in this sequence. Space returns to editing.

The changed cells are zero-based row 14, columns 36 through 43.
Column 37 receives 0x74. The others receive 0x71.
The parent Justify row remains highlighted until Up changes the selection.

Use the character and attribute grid plus the next-key behavior for acceptance.
Do not require all child-menu text to disappear on F1.

Evidence includes r2 and r3 directories 02-justify, 03-after-f1-immediate,
04-after-f1-settled and 04b-after-up-focus. The early screenshot was captured
after the harness's ordinary key-delivery delays and an additional 0.05 seconds.
The settled screenshot waited another two seconds. These are host-timed
observations, not exact emulated-cycle timing measurements.

## Persistent visibility is independent of editing focus

The pinned profile begins with these menu options.

- Alt Key Selects Pull-Down Menu is No.
- Menu Bar Remains Visible is No.
- Menu Bar Separator Line is No.
- Menu Letter Display is BOLD.
- Pull-Down Letter Display and Menu Bar Letter Display are REDLN.
- Pull-Down Text and Menu Bar Text are SHADW.

Shift+F1, 2, 4 opens Menu Options. Choosing 8 then Y sets persistent
visibility to Yes. F7 returns to the editor, where the bar remains visible
and ordinary typing enters the document.

Both r2 and r3 typed the whole paragraph with the visible bar, then invoked F8,
Reveal Codes, F10 Save and F7 Exit directly. The application accepted those
editing commands without a separate keyboard-focus dismissal of the visible bar.

## Layout defaults must be pinned explicitly

The original Format > Line menu in r3 shows the following settings.

| Setting | Observed value |
| --- | --- |
| Hyphenation | No |
| Hyphenation zone | Left 10%, Right 4% |
| Justification | Full |
| Line height | Auto |
| Line spacing | 1 |
| Left and right margins | 1 inch each |
| Tab set | Rel; -1 inch, every 0.5 inch |
| Widow/Orphan Protection | No |

The original Format > Page menu in r4-settings and r5-settings shows
Standard 8.5 × 11 inch paper and top/bottom margins of 1 inch.
The Print menu identifies Standard Printer. The original Base Font list in
r5-settings/02b-base-font identifies Courier 10cpi as selected.

Full justification is the original default in this profile. A ragged-looking
text screen does not justify implementing a Left default. These probes do not
establish full-justified printed spacing or pagination over many pages.

The 122-character paragraph below wraps after Menus, in both r2 and r3.

> A faithful reconstruction needs more than a blue screen. Menus, prompts, wrapping, and cursor movement must work together.

The visible lines are

    A faithful reconstruction needs more than a blue screen. Menus,
    prompts, wrapping, and cursor movement must work together.

The resulting status reads Doc 1 Pg 1 Ln 1.17" Pos 6.8".
After two Enter presses and Plain UNDER after, with only UNDER underlined,
the status reads Doc 1 Pg 1 Ln 1.5" Pos 2.7".

The measurements support one-sixth-inch line advance and one-tenth-inch ordinary
character advance for this sample. General font metrics, justification,
pagination, tabs and other characters still require their own observations.

## Native soft return and underline are now observed

The script saves the authored sample as C:\OUT\EVERY.WP, exits WordPerfect,
stops the guest, then exports the file from the stopped disk with mcopy.

The r2 and r3 exports are byte-identical.

- Native file size is 471 bytes.
- Document body starts at offset 324.
- SHA-256 is 47a1dd33fe87a69a0303f82a2cdf4f10964a77f4ab1144998a2325a12f0bf6a3.
- The body is 147 bytes.

The original stored the wrapping boundary as byte 0D in place of the space
between Menus, and prompts. Enter produced byte 0A.
Underline ON is c3 0e c3. Underline OFF is c4 0e c4.

    A faithful reconstruction needs more than a blue screen. Menus,<0D>
    prompts, wrapping, and cursor movement must work together.<0A><0A>
    Plain <C3 0E C3>UNDER<C4 0E C4> after

The line breaks shown above are explanatory. See native.json for exact
hexadecimal bytes and prefix packet descriptions.

Reveal Codes shows [SRt], [HRt], [UND] and [und] in the correct paragraph
structure. The underline word uses the original contrasting text attribute.
The lower pane remains multiline and the physical ruler separates the views.

These findings agree with the local Developer's Toolkit transcription,
function 195 Attribute ON, function 196 Attribute OFF, attribute type14
Underline, and control byte13 Soft return. The original files provide the
release-specific witness.

## Acceptance implications

1. A menu model needs distinct visibility, selected parent, selected child and
   keyboard-focus states. F1 can change focus without changing text content.
2. Default settings are part of the reference configuration. Record the
   visibility preference and Full justification before comparing screens.
3. Model soft returns as native format objects whose semantic role differs
   from hard returns. Reflow and save must preserve native interoperability.
4. Underline authoring must emit the observed native three-byte codes and
   cooperate with editing, saving, reopening and Reveal Codes.
5. Compare raw character/attribute grids, relevant status and next-key behavior.
   PNG appearance or text-only screenshot matching alone misses real changes.
6. Repeat broader edit-after-retrieve and edit-after-save journeys before
   claiming their native-format and state-machine semantics. This probe only
   creates, formats and saves a fresh document.

## Reproduction and provenance

The capture scripts reuse scripts/reference/guest.py and qmp.py. Each run
uses its own scratch disk copied from the same master, its own short /tmp
QMP socket, offline TCG execution and the existing hash-checked reference profile.
Every run records the launch command, profile and input/capture trace.
Runs r2 and r3 exit WordPerfect cleanly and stop QEMU before native export.
Settings-only runs stop their independent guest without modifying the master.

Run r1 successfully captured menu focus evidence but failed later because the
script pressed F7 after Space had already returned to the document, entering
the exit/save workflow instead of Setup. Its failure and raw evidence remain.
The r2 script added a screen-state guard before F7. Run r3 additionally inspects
the line settings before creating the same document. r2 and r3 have saved copies
of their actual probe source. The exploratory r1 trace is retained, but its
original script version was not separately frozen.

The reference uses FreeDOS 1.4 and the established mixed-date printer resources.
The app release is the pinned US 03/09/92 binary. No OS equivalence or
untouched-shipping-installation claim follows from this work.

The DOS filename input in the probes contains doubled separators, accepted by
the original. The exported directory entry is EVERY.WP. This does not establish
general path normalization semantics.

Files EVERY.WP are authored test documents. Original executables, driver files,
manuals and disk images stay in the local private research cache.

## Documentary source anchors

The local Reference transcription supports menu cancellation and visibility on
printed pages 545–546, Menu Options on 418–419, and left/right margins on 394.
The local Developer's Toolkit transcription describes soft return on its
WordPerfect file-format page 19 and Attribute ON/OFF on pages 24–25.
Source checksums are recorded in evidence-manifest.json. The screenshots and
native sample are the primary release-specific witnesses for this report.
