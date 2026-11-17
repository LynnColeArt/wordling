# Mission 1 qualification run, November 13, 2026

Candidate SHA-256: cf216957c10a81b1188ef05062f1f6f785c7b45f077759509104b07df68c7aa5. The local [run directory](../../research/cache/mission1-qualification.GuAete) contains the executable, working-tree status, source hashes and test results. This is a working-tree preflight candidate. The reviewed release candidate and acceptance verdict remain open.

| Scope | Result and limits |
| --- | --- |
| Original reference | Fresh March 9, 1992 DOS smoke cases cover menus, help, repetition, block selection, typeover, Reveal Codes and save. See [baseline](../../docs/research/reference-runs/mission1-nov13-baseline/run.json) and [editing](../../docs/research/reference-runs/mission1-nov13-editing/run.json). |
| Everyday editor | [22 suite cases passed](../../research/cache/mission1-qualification.GuAete/everyday-final-harness/suite.json). Includes save-policy and continuous Wordling → DOS retrieve/edit/save → Wordling reopen. Independent review reproduced the continuous round trip. |
| Proofreading | The reviewer reproduced the five-session Ctrl+F2 regression with admitted resources. The single continuous EE-A15 journey across Word, Page and Document scopes with a fresh DOS save comparison remains open. |
| Terminal | Isolated VTE 0.76.0 X11 key events produced the expected F1/F3/F5/F7/F10, Shift+F10, Ctrl+F2, Home/End and Alt+= bytes. Alt+keypad Plus lost Alt in numeric mode and emitted ESC O 3 k in application mode. Wordling's application-mode sequence and Linux shell return passed the PTY regressions. Full GNOME Terminal desktop shortcut and mouse delivery remain open. |
| Native integrity | Go suite, save policy, Fast Save, preservation corpus, component fault cases and existing multi-document recovery regression passed. The pre-replacement SIGKILL left the original intact and restored all three documents. The staging file stayed out of F5 List Files and a subsequent native replacement succeeded. EE-A13 still needs broader editor-level save fault coverage. |
| Tables and merges | Focused Wordling tests passed for word overflow, last-row overflow, wrap with pagination, three-page tables, formatted fields with overlapping attributes across pages, and structural Undelete. DOS reopened all four table outputs. See the [reopen manifest](../../research/cache/mission1-qualification.GuAete/dos-table-reopen-retry.json). |
| Menus and remaining coverage | Classic DOS comparisons now explicitly use the classic theme and hidden document tabs, with the Linux File menu label and added document rows recorded in the comparison. File → Summary still reaches an unimplemented route. A fresh DOS capture confirms the [original summary form](../../docs/research/everyday-contract-2026-11-05/qualification/mission1-summary/summary-form/screen.txt) for CMD51-088/089. |

The preview gate stays open while these findings are resolved and each everyday requirement receives an evidence-backed verdict. Keep F10 native and Mission 2 on hold. Next work is the continuous proofreading witness, editor-level fault coverage and remaining live menu routes while continuing command-inventory qualification.

## Everyday journey evidence

Case names refer to the suite manifest above. These are working verdicts for the evidence in this run. Final acceptance also requires the reviewed candidate and full observations specified by each journey.

| Journey | Passing evidence | Remaining evaluation |
| --- | --- | --- |
| EE-A01 | menus | Verify default Linux chrome and GNOME Terminal input together. |
| EE-A02 | menus, help-focus | Resolve reachable unimplemented routes and review Linux menu adaptations. |
| EE-A03 | menus, help-focus, files-reveal | Complete live GNOME Terminal modifier and alias coverage. |
| EE-A04 | flow, continuous | Compare the full resize and multipage edit transcript at matched checkpoints. |
| EE-A05 | navigation-search, files-reveal | Check live terminal Home/End delivery and viewport edges. |
| EE-A06 | corrections | Compare boundary and history cases across saved and retrieved buffers. |
| EE-A07 | attributes, continuous | Check active-format save and all required toggle and pair boundaries. |
| EE-A08 | files-reveal, navigation-search, attributes | Compare both panes through the full resize and editing sequence. |
| EE-A09 | navigation-search, wrapped-search, attributes | Verify menu and function-key route equivalence across the required search branches. |
| EE-A10 | files, files-reveal | Verify mouse selection and all required file-list branches on the integrated candidate. |
| EE-A11 | save-policy, fast-save-yes, original save-policy round trips | Check remaining native save and backup branches against the original. |
| EE-A12 | save-policy, continuous | Compare classic switching separately from multi-tab Linux behavior. |
| EE-A13 | preservation-corpus, refusal, storage-faults, recovery | Exercise more failures through the editor and classify unsupported native cases. |
| EE-A14 | continuous, original, reopen, independent replay | Repeat with the final source-bound candidate. |
| EE-A15 | proof-pages, proofreading, independent replay | Complete the continuous all-scopes journey on the final candidate. |

## Follow-up candidate

Candidate SHA-256 01be64e24bdf63c8db3fcc1d5bba4889283fcf95c38f46b85532746b0f55f38f. [24 everyday regression cases](../../research/cache/summary-qualification.w8ex7S/everyday/suite.json) and the uncached Go suite passed on the working tree.

- File → Summary edits a native packet in the supported compact document prefix. The PTY cases cover creating, editing, removing, cancelling a field and discarding a form. March 9 DOS [reopened the edited file](../../research/cache/summary-qualification.w8ex7S/dos-summary-reopened/screen.txt) and displayed the updated subject. The legacy Fast Save rewrite is bypassed for summary-bearing documents to preserve the packet. DOS Fast Save generation, Retrieve to capture and date editing still need qualification.
- The proofreading session now visits Word, Page and Document scopes before saving. The corrected body and supplementary dictionary match the reference bytes. A fresh DOS guest retrieved, edited and resaved the file, and Wordling reopened it and continued editing. See the [round-trip report](../../research/cache/summary-qualification.w8ex7S/proof-final-roundtrip/result.json). The combined journey still needs multi-paragraph attributed input and an independent rerun on the final candidate.
- A real editor overwrite hit an injected EIO on the replacement syscall. Wordling reported PublicationFailed, retained the original and unsaved text, and saved successfully on retry. See the [editor fault run](../../research/cache/summary-qualification.w8ex7S/save-failure-cleanup/qualification.json).
- GNOME Terminal 3.52 ran the actual executable in an isolated X11 session. The editing and native F10 save witness produced the expected body. The GNOME byte probe confirmed Alt+keypad Plus in application mode and found that the terminal intercepted Shift+F10. Mouse and desktop shortcut coverage remain open.

The preview stays at the prior build pending the everyday acceptance gate and independent review.

## Summary, formatted proofreading, and GNOME Terminal

Candidate SHA-256 7da38631e62246e09cdef7a788ac53a9034a65eb437da6436f7f3a16c6239a1f. The [run directory](../../research/cache/everyday-edge.5CptYt) contains the Go test results, native fixtures and terminal evidence.

- [Summary qualification](../../research/cache/everyday-edge.5CptYt/summary-native-comparison/qualification.json) covers capture confirmation and refusal, deletion confirmation, creation date editing, and reuse of Author and Typist from the latest saved Summary. The captured fields and edited date match their DOS packets. An edited loaded Summary document produced the same Fast Save file byte for byte as the March 9, 1992 reference. Revision Date display, rich field editing and additional Fast Save generations remain open.
- The formatted proofreading run visits Word, Page and Document in the same session. It corrects bold and underlined words in a wrapped multi-paragraph document and preserves the second page. DOS reopened and resaved the output. The [independent run](../../research/cache/everyday-edge.5CptYt/independent-proof.json) reopened that resave and continued the edit. Suggestion paging and persistent Add are covered by separate sessions, so the complete EE-A15 sequence on the same formatted input remains open.
- [GNOME Terminal](../../research/cache/everyday-edge.5CptYt/gnome-verified.log) delivered Shift+F10 Retrieve with its menu accelerator disabled in an isolated profile. Clicking Wordling’s File menu and selecting Save published the retrieved native body. The default accelerator intercepts Shift+F10.

The everyday gate still needs the remaining integrated proofreading and save-fault cases, plus release-candidate acceptance. Preview promotion remains conditional on that gate.

All 24 cases passed on this candidate, including the original DOS round trips. [Suite manifest](../../research/cache/everyday-edge.5CptYt/verified-suite/suite.json)

## Integrated proofreading and save failure

Candidate SHA-256 23e43367c6f9f45a9e594ac8ce1a1ec6fe9ef3ef81b23f19fc8d70de5bb9d14a passed the Go suite and all 24 cases in the [everyday regression suite](../../research/cache/everyday-integrated.u0RxE0/suite/suite.json).

- The [independent proofreading run](../../research/cache/everyday-integrated.u0RxE0/independent-proof.json) exercised all three scopes, suggestion paging, both Skip choices, dictionary Add and restart, and Spell Edit and resume on formatted input. The attributed output matches the recorded reference and Wordling continued editing the original DOS resave.
- [Editor save failures](../../research/cache/everyday-integrated.u0RxE0/faults-final) covered denied staging creation, a partial temporary write, a failed sync and failed replacement with backups enabled and disabled. Each case preserved the original and existing backup bytes. DOS reopened, edited and resaved the [successful retry](../../research/cache/everyday-integrated.u0RxE0/dos-retry/reopen/original-roundtrip.json).
- Summary now displays the saved file's revision timestamp, supports cursor movement and deletion within fields, and writes Bold and Underline runs. The rich Subject packet matches the DOS reference, and DOS [reopened the Wordling output](../../research/cache/everyday-integrated.u0RxE0/dos-rich-summary/screen.txt). Inline emphasis rendering and Compose remain open.
- Shift+F10 and File-menu mouse input passed again in [GNOME Terminal](../../research/cache/everyday-integrated.u0RxE0/gnome.log) with the menu accelerator disabled. Direct mouse selection in the file list remains open.

The complete everyday milestone still requires the remaining parity checks and the independent full candidate acceptance recorded in EE-A14.

## Compose and file-list mouse candidate

Candidate SHA-256 0663e051bbd4d097fefaf78f0a6da39af9c049a286a3332c77a7745585eabc55. The [suite manifest](../../research/cache/everyday-acceptance.nUbFZn/suite/suite.json) records the native DOS round trips and executable cases. The [source manifest](../../research/cache/everyday-acceptance.nUbFZn/source-sha256) identifies the working-tree inputs.

- Summary numeric Compose retains native extended character owners. Wordling and DOS produced the same Summary field bytes for set 1, character 36, and DOS [displayed Æ after retrieving the Wordling save](../../research/cache/everyday-acceptance.nUbFZn/dos-compose-summary/screen.txt). The Summary regression checks distinct display attributes for Bold and Underline. Other character glyphs and digraph shortcuts remain open.
- [GNOME Terminal](../../research/cache/everyday-acceptance.nUbFZn/gnome.log) delivered a click on the second file entry. Retrieve and Save produced the second fixture's exact body. [Shift+F10](../../research/cache/everyday-acceptance.nUbFZn/gnome-shift.log) also passed on the same binary with the terminal menu accelerator disabled.
- The [independent proofreading replay](../../research/cache/everyday-acceptance.nUbFZn/independent-proof.json) passed all seven processes, including continued editing after opening the DOS resave.

The release verdict remains open. The suite records a working-tree candidate, and the independent review identified incomplete Compose display coverage.

## Summary digraphs and VGA character display

Candidate SHA-256 3aa75f7a371798430204754483a7b4da965f9cc88174c633e7c311cdd8831e83. [Compiled source inputs](../../research/cache/everyday-compose.IDU6Ld/source-sha256)

- The Summary test compares eight composed characters against the March 9, 1992 DOS screen and native field. DOS [reopened the Wordling save](../../research/cache/everyday-compose.IDU6Ld/dos-compose-summary/screen.txt) and showed the same ligatures, letters and solid squares for symbols absent from its screen font. Additional glyph mappings use the [VGA capture](../../docs/research/everyday-contract-2026-11-05/qualification/summary-glyph-dos/glyphs/screen.txt).
- Independent review passed the [formatted proofreading replay](../../research/cache/everyday-compose.IDU6Ld/independent-proof.json) and the continuous [DOS retrieve, edit and save round trip](../../research/cache/everyday-compose.IDU6Ld/independent-roundtrip.json) on this binary.
- [GNOME Terminal](../../research/cache/everyday-compose.IDU6Ld/gnome.log) selected the second file by mouse and saved its native body on this binary.

The [suite manifest](../../research/cache/everyday-compose.IDU6Ld/final-suite/suite.json) records the executable runs. The full acceptance verdict remains open. The Compose table covers sampled screen characters and documented symbol pairs. The other character sets and general diacritic composition still need coverage.

## Everyday editing acceptance

Candidate SHA-256 41da2dd5c1cdc30ca70d68f27a2fae482307b9bdb964693e33384296adc74def. The build from the recorded working-tree sources reproduced this executable byte for byte. The suite's preflight flag denotes its working-tree origin. [Source hashes](../../research/cache/everyday-diacritics.HEaOlX/source-sha256) · [Build metadata](../../research/cache/everyday-diacritics.HEaOlX/build-info)

- EE-A01–A03 use the menus, help-focus and files-reveal cases, with DOS menus and focus-r1/r2 as reference.
- EE-A04–A09 use flow, corrections, attributes, files-reveal, navigation-search and wrapped-search, with DOS flow-reliable, history-repeat, scroll-search and proof-boundaries as reference.
- EE-A10–A13 use files, save-policy, fast-save-yes, preservation-corpus, refusal and save-failure, with the original files and backup witnesses and the fresh DOS round trips. GNOME Terminal also selected and retrieved the second file by mouse on this candidate.
- EE-A14 passed an independent continuous editing run, fresh March 9, 1992 DOS retrieve/edit/save, and Wordling reopen and continuation. EE-A15 passed seven independent proofreading processes with the admitted resources. [DOS round trip](../../research/cache/everyday-diacritics.HEaOlX/independent-roundtrip.json) · [Proofreading](../../research/cache/everyday-diacritics.HEaOlX/independent-proof.json)

The Summary regression compared 26 diacritic pairs, alternating key order, against the original field bytes and screen text. The DOS guest reopened the Wordling save and displayed the same Subject. The broader Compose repertoire and remaining extended character glyphs belong to full Mission 1, as stated in the everyday editing specification. [Original capture](../../docs/research/everyday-contract-2026-11-05/qualification/summary-accent-dos/glyphs/screen.txt) · [DOS reopen](../../research/cache/everyday-diacritics.HEaOlX/dos-compose-summary/screen.txt)

The everyday editing milestone passed on the recorded candidate. All 24 executable cases passed, and the independently replayed editing and proofreading journeys passed. The rebuilt preview is byte-identical to the tested executable. [Suite results](../../research/cache/everyday-diacritics.HEaOlX/suite/suite.json) · [Preview](../../preview/wordling)

## Broader DOS character coverage

The pinned March 9, 1992 DOS guest displayed 1,578 numeric identities from sets 1–12 in Summary. Wordling matched every captured cell across twelve packed Summary fixtures. The table reflects the stock US VGA screen, including DOS substitutions and solid squares. The additional Compose replay covered caron, crossbar, dot above, macron, ogonek and more vowel combinations, with matching native Subject bytes. [DOS VGA captures and Linux comparison](../../research/cache/compose-coverage) · [DOS Compose fixture](../../docs/research/everyday-contract-2026-11-05/qualification/compose-marks-dos)

The Linux parity sweep also passed four nested merge scenarios, four table layout cases, and the four Standard Printer fixtures. The fresh ordinary-document DOS Compose capture shows the extended character in both editing and Reveal Codes and preserves its native owner. Extending Compose beyond Summary, covering the remaining key pairs and qualifying alternate display profiles remain open under FR-014. [Ordinary document reference](../../docs/research/everyday-contract-2026-11-05/qualification/compose-body-dos)

The Linux preview was rebuilt from candidate `f10eb418a9b7aee8ed546dd70ef79939c324c13b070bf567ecf61cbef0e8c1b4` after all 24 everyday regressions passed. The installed preview matches the tested binary. [Suite results](../../research/cache/compose-coverage/final-suite/suite.json)

## Main editor Compose

Ctrl+V, silent Ctrl+2 and Font → Characters now share the same Compose input
with Summary. The DOS pair matrix tested 825 two-key inputs; 219 inserted an
owner. A separate capture verified uppercase `*O`, bringing the qualified map
to 220 pairs. The stock release produced no character for `Pl`, and its
`--` and `**` identities differ from some printed examples.
[Inputs and DOS exports](../../docs/research/everyday-contract-2026-11-05/qualification/compose-final-0/README.md).

Extended owners consume one cell in the editor. Reveal Codes expands only the
owner at the caret (for example, `[Æ:1,36]`). The Linux test covers ordinary
typing, typeover, whole-owner delete and Undelete, native save, DOS-produced
file retrieval, and a right-margin wrap. The [DOS round trip](../../research/cache/compose-editor/dos-fifth/result.json)
reopened a Wordling save in the pinned March 9, 1992 release, verified its Reveal
Codes display, and preserved the extended owner while editing and resaving.

The scope is the ordinary editing canvas and Summary on the pinned US display
profile. Compose within table cells and merge source editing, other display
profiles and printer/language-resource parity remain open under Mission 1.

Linux preview: `preview/wordling`, SHA-256
`3439a52e051ed8565d8340936a5284e8ce017b8a9c4303237fd2185bf5018ea3`.
[Exact candidate suite and DOS round trip](../../research/cache/compose-editor/final-suite/suite.json).

## List Files, DOS text and everyday commands

The working-tree build `78f63ca51a44562236a1a8ae133cf2886e5c5e779e4d319f7dc6eb932deae7c2`
passed [all 40 Linux preflight cases](../../research/cache/mission1-linux-checkpoint.OgJaBt/suite/suite.json),
including original DOS reopen, edit and resave. It also passed
[the uncached Go suite](../../research/cache/mission1-linux-checkpoint.OgJaBt/go-test.log),
the [List Files and DOS text terminal replay](../../research/cache/mission1-linux-checkpoint.OgJaBt/files/qualification.json),
and the [navigation and editing terminal replay](../../research/cache/mission1-linux-checkpoint.OgJaBt/navigation/qualification.json).
The checkout contained concurrent work. The [compiled source hashes](../../research/cache/mission1-linux-checkpoint.OgJaBt/source-sha256)
record the exact sources used by the 40-case preflight executable, and a rebuild
matched that executable byte for byte.

- List Files covers Find patterns, Summary fields, creation and revision date bounds, three Undo levels, and printing a selected page. The DOS text fixtures cover CP437 extended bytes, control bytes, line and page breaks, and replacement prompts. DOS reopened Wordling's native save and reproduced the reference text export. [DOS captures](../../docs/research/everyday-contract-2026-11-05/qualification/mission1-list-dos-text/README.md)
- Everyday editing covers word movement, Go To, line and word deletion and Undelete, Block case conversion, Copy and Append, and a nonbreaking Hard Space. The terminal replay compares the saved Copy, Append and Hard Space bodies with DOS. The original reopened all four Wordling saves and showed the expected Reveal Codes. [Movement and deletion](../../docs/research/reference-runs/mission1-word-nav/README.md) · [Copy and Append](../../docs/research/reference-runs/mission1-block-copy/README.md) · [Hard Space](../../docs/research/reference-runs/mission1-line-format/README.md) · [DOS reopen](../../research/cache/mission1-linux-checkpoint.OgJaBt/dos-reopen)
- Recovery passed after an interrupted overwrite and after staging a replacement. The same run covers six open documents, selective restoration and a subsequent successful retry. [Recovery captures](../../research/cache/mission1-linux-checkpoint.OgJaBt/recovery) · [Terminal keys](../../research/cache/mission1-linux-checkpoint.OgJaBt/terminal-keys/qualification.json)
- The follow-up build `59314927beec99a0027c85e9eda8cb38764791e82b88651720f04ae9ffdc3424` passed the uncached Go suite and both focused terminal replays. Ctrl+Page Down retained the explicit page break and the next page's text, matching the DOS native body. [Go results](../../research/cache/mission1-page-final.wAlBaU/go-test.log) · [Editing replay](../../research/cache/mission1-page-final.wAlBaU/navigation/qualification.json) · [Files replay](../../research/cache/mission1-page-final.wAlBaU/files/qualification.json) · [DOS evidence](../../docs/research/reference-runs/mission1-page-delete/README.md)

Full Linux acceptance remains open. The audit classifies 120 of 244 commands
as verified, 52 as partial and 72 as unimplemented. Line margin and alignment
behaviors have additional DOS captures, and Linux implementation is still due.
The clean source-bound candidate and independent acceptance review remain due.
[Command audit](../../docs/research/mission-1-command-audit.md) ·
[Margin captures](../../docs/research/reference-runs/mission1-line-margins/README.md)


## Layout, running text and notes

The working-tree layout candidate
`711924e3f1faaee56b5e3c19e49656241c6e66cce1aa6f803d655cc4e04726b8`
passed all 41 Linux preflight cases, including the new terminal layout replay.
[Suite](../../research/cache/mission1-layout-current.ZC5O3t/suite/suite.json) ·
[Compiled source hashes](../../research/cache/mission1-layout-current.ZC5O3t/source-sha256) ·
[Focused terminal replay](../../research/cache/mission1-layout-current.ZC5O3t/line-format/qualification.json)

- Line margins, centering, flush right, end alignment, and paragraph justification match the sampled DOS screen and native bodies. The page margin, line spacing and line height cases also match the observed automatic and explicit page breaks.
  [Horizontal margins](../../docs/research/reference-runs/mission1-line-margins/README.md) ·
  [Alignment](../../docs/research/reference-runs/mission1-line-format/README.md) ·
  [Justification](../../docs/research/reference-runs/mission1-justification/README.md) ·
  [Page margins](../../docs/research/reference-runs/mission1-page-margins/README.md) ·
  [Spacing](../../docs/research/reference-runs/mission1-line-spacing/README.md)
- Double and hanging indents match the sampled native saves and screen. The Standard Printer distributes extra justification spaces differently across the first lines in the indent fixture.
  [Indent evidence](../../docs/research/reference-runs/mission1-indents/README.md)
- The sampled headers and footers support A/B slots, every/odd/even pages and discontinuation. Short footnotes and endnotes support creation and editing by number. Richer note text, overflow and editing existing running text remain open.
  [Headers and footers](../../docs/research/reference-runs/mission1-headers/README.md) ·
  [Notes](../../docs/research/reference-runs/mission1-notes/README.md)
- The line numbering fixture matches the native toggle and printer stream. The binding offset fixture matches the changed document state, the reset, and printing both pages.
  [Line numbering](../../docs/research/reference-runs/mission1-line-numbering/README.md) ·
  [Binding offset](../../docs/research/reference-runs/mission1-binding/README.md)

The pinned March 9, 1992 DOS guest also reopened eight Wordling saves and
displayed the expected codes.
[DOS reopen captures and replay](../../research/cache/mission1-layout-current.ZC5O3t/dos-reopen)

A follow-up build reproduced byte for byte at
`08ec0b65170904e893263283e69f3e62be3893f5be72337acef934dbf9daeabd`.
It passed the extended terminal layout replay, including both indent shortcuts,
as well as an uncached Go run with 17 byte-for-byte DOS print stream
comparisons.
[Source hashes](../../research/cache/mission1-layout-final.kecNsw/source-sha256) ·
[Terminal replay](../../research/cache/mission1-layout-final.kecNsw/line-format/qualification.json) ·
[Go results](../../research/cache/mission1-layout-final.kecNsw/go-test.log)

Conditional End of Page now matches the DOS saves with enough room, an
early break, and the ordinary page boundary. The candidate
`4f7c2e32bb8084e41e2a5019492c4855a13c8f72102ffb8047559c56b760f629`
passed all 41 Linux preflight cases.
[Conditional break captures](../../docs/research/reference-runs/mission1-conditional-page/README.md) ·
[Suite](../../research/cache/mission1-conditional-linux.vaoS8D/suite/suite.json)

The follow-up matches four Widow/Orphan Protection saves, including the
pending widow at the end of the file and its resolution on hard return.
The [pagination build](../../research/cache/mission1-pagination-linux.nHHbvI/suite/suite.json)
passed all 41 Linux preflight cases.
Date Text matches the default US literal date and preserves it when the
file is retrieved after the clock changes. Dynamic dates and custom
formats remain open.
[Protection captures](../../docs/research/reference-runs/mission1-widow-protection/README.md) ·
[Date captures](../../docs/research/reference-runs/mission1-dates/README.md)

The working-tree build
`7cdd5fa099040786d0d068909b5f03714995bf05df903fd2f846ba9f1dc90179`
reproduced byte for byte and passed uncached Go tests, vet, and the
294-step layout terminal replay.
[Source hashes](../../research/cache/mission1-dates-linux.eCPasN/source-sha256) ·
[Go results](../../research/cache/mission1-dates-linux.eCPasN/go-test-final.log) ·
[Layout terminal replay](../../research/cache/mission1-dates-linux.eCPasN/line-format/qualification.json) ·
[Date Text terminal replay](../../research/cache/mission1-dates-linux.eCPasN/date-key/qualification.json)

The pinned DOS guest reopened the follow-up's Conditional End of Page
and Widow/Orphan saves and displayed the expected native codes.
[Conditional break](../../research/cache/mission1-dates-linux.eCPasN/dos-reopen/SHORT.WP/screen.txt) ·
[Widow protection](../../research/cache/mission1-dates-linux.eCPasN/dos-reopen/WIDOW.WP/screen.txt)

GNOME Terminal 3.52 also selected the second List Files entry by mouse
and retrieved it. F10 published the selected file's exact native body.
Shift+F6 and Enter produced the original centered heading and following line.
[GNOME mouse replay](../../research/cache/mission1-dates-linux.eCPasN/gnome-final.TnFh/gnome.log) ·
[GNOME alignment replay](../../research/cache/mission1-dates-linux.eCPasN/gnome-layout.Twuu/gnome.log)

The same build passed the terminal-key replay and the interrupted-save
recovery journeys, including six open documents and selective recovery.
[Terminal keys](../../research/cache/mission1-dates-linux.eCPasN/terminal-keys/qualification.json) ·
[Recovery](../../research/cache/mission1-dates-linux.eCPasN/recovery)

The Conditional End of Page fixture is the eighteenth byte-for-byte
printer comparison. The widow and orphan print captures match the page
placement and expose a remaining difference in extra justification spaces.

The latest integrated run passed 40 of 41 cases. It logged a timeout during
FreeDOS startup in the structural Compose case. The same three candidate files passed the individual
rerun with their native bodies unchanged after DOS saved them. That replay
now uses the same 60-second boot allowance as the reference guest bootstrap.
[Integrated results](../../research/cache/mission1-dates-linux.eCPasN/suite/suite.json) ·
[Recorded timeout](../../research/cache/mission1-dates-linux.eCPasN/suite/original-compose-structural.log) ·
[Rerun saves](../../research/cache/mission1-dates-linux.eCPasN/original-compose-structural-boot60)

This brings the audited coverage to 144 verified, 45 partial and 55
unimplemented scenarios out of 244. The preflight builds do not satisfy
the clean candidate or independent review requirements in issue #7.
[Command audit](../../docs/research/mission-1-command-audit.md)

## Custom tabs, note continuation, dates and comments

The tab ruler now supports sampled relative and absolute left stops and
decimal stops. The hard Ctrl+F6 decimal command uses a different code from
a ruler decimal. Both align unequal integer widths to the same period
column and match the original native bodies and printer streams.
[Custom tab captures](../../docs/research/reference-runs/mission1-custom-tabs/README.md)

A half-inch note minimum splits the six-line footnote across two pages in
the short-page fixture. A 1.25-inch minimum moves the reference and the
whole footnote to the next page. The option, reference and break records
match DOS, apart from two unresolved bytes in the multiline note owner.
Both Standard Printer streams match. Multiple long notes, wrapping and
rich note content remain open.
[Note continuation captures](../../docs/research/reference-runs/mission1-note-continuation/README.md)

Default US Date Code updates on retrieval under a different clock and
matches the native and printer captures. Screen → Rewrite refreshes the
projection without changing the native document or caret in the sampled
automatic formatting profile. A short Document Comment appears in a box
and in Reveal Codes, with no effect on the printer stream.
[Dates](../../docs/research/reference-runs/mission1-dates/README.md) ·
[Rewrite](../../docs/research/reference-runs/mission1-rewrite/README.md) ·
[Comments](../../docs/research/reference-runs/mission1-comment/README.md)

The tab, note and Date Code build
`e9f2df5026e7147e1f4055d13ac5015ec974435e4e4ea0beb65a232e0863ac5f`
passed all 43 integrated Linux preflight cases.
[Suite](../../research/cache/mission1-tabs-notes-date.rqi6Fo/suite/suite.json)

The latest working-tree executable
`5db0352afccc9846f41809140d9c73af2b3ebfb11a2af35e5ca2d814efe32043`
reproduced byte for byte and passed the uncached Go suite, vet, the
focused terminal comment replay, and GNOME Terminal mouse retrieve and
save. DOS reopened the new decimal ruler, split footnote, and comment
saves and displayed their content. The paced rerun of three-page typing
also passed after milestone assertions were added to the test input.
[Source hashes](../../research/cache/mission1-comments-linux.jMVwcs/source-sha256) ·
[Go](../../research/cache/mission1-comments-linux.jMVwcs/go-test.log) ·
[Comment replay](../../research/cache/mission1-comments-linux.jMVwcs/document-comment/qualification.json) ·
[GNOME Terminal](../../research/cache/mission1-comments-linux.jMVwcs/gnome.CGBv/gnome.log) ·
[DOS reopen](../../research/cache/mission1-comments-linux.jMVwcs/dos-reopen) ·
[Three-page typing](../../research/cache/mission1-comments-linux.jMVwcs/flow-confirm/qualification.json)

That build passed all 45 cases in its integrated working-tree preflight.
[Integrated suite](../../research/cache/mission1-comments-linux.jMVwcs/suite/suite.json) ·
[Recovery](../../research/cache/mission1-comments-linux.jMVwcs/recovery)

The follow-up matches the DOS native records for successive decimal
fields, a four-and-two note split, and marking a contents heading at
levels 1 and 5. The original DOS release reopened the new level 1
Wordling save and displayed both marks. The follow-up binary
`c8f38572fd4625e032d89dcbd6fa43e8e5c8623d2ebbff41e1665c43c54890d6`
reproduced byte for byte and passed the uncached Go suite, vet, and all
47 integrated Linux preflight cases.
[Contents captures](../../docs/research/reference-runs/mission1-toc-mark/README.md) ·
[Source hashes](../../research/cache/mission1-toc-linux.U1dGk2/source-sha256) ·
[Go](../../research/cache/mission1-toc-linux.U1dGk2/go-test.log) ·
[47-case suite](../../research/cache/mission1-toc-linux.U1dGk2/suite/suite.json) ·
[Terminal mark replay](../../research/cache/mission1-toc-linux.U1dGk2/toc-terminal/qualification.json) ·
[DOS reopen](../../research/cache/mission1-toc-linux.U1dGk2/dos-reopen/LEVEL1.WP/screen.txt)

The same binary passed terminal key delivery, GNOME Terminal mouse
retrieval and save, physical Ctrl+F6 decimal entry, and
interrupted-save recovery.
[Terminal keys](../../research/cache/mission1-toc-linux.U1dGk2/terminal-keys/qualification.json) ·
[GNOME Terminal](../../research/cache/mission1-toc-linux.U1dGk2/gnome.IAFE/gnome.log) ·
[GNOME decimal tabs](../../research/cache/mission1-toc-linux.U1dGk2/gnome-tabs.irx2/gnome.log) ·
[Recovery](../../research/cache/mission1-toc-linux.U1dGk2/recovery)

DOS Text exports now match the captured relative and decimal rulers and
the default Date Code rendered at export time. The working-tree executable
`c2c42f2bc093b6b3cbbf500aa0eef4ce8fad2989f6a38cd1d8f24e3cb55968f8`
reproduced byte for byte and passed the uncached Go suite, vet, and a
terminal export of a native document with ruler decimal stops.
[Source hashes](../../research/cache/mission1-tab-export-linux.LdmtaM/source-sha256) ·
[Go](../../research/cache/mission1-tab-export-linux.LdmtaM/go-test.log) ·
[Terminal export](../../research/cache/mission1-tab-export-linux.LdmtaM/dos-text/qualification.json)

## Styles, generated documents, tables, and record sort

The pinned DOS release and Wordling agree on compact paired Bold style
creation and application, duplicate-name refusal, and the default
one- and two-level contents layouts. The contents confirmation preserves
the earlier body when declined. On approval, DOS and Wordling match the
generated bodies, including page numbers and level-two indentation.
[Styles](../../docs/research/reference-runs/mission1-style-authoring/README.md) ·
[Contents](../../docs/research/reference-runs/mission1-toc-generation/README.md)

Condensed subdocument links preserve the surrounding text and do not
add a page break. Page cross-references match the paired and separate
marking workflows, including case-insensitive matching and Arabic and
Roman page resets. The full-authority case preserves the visible
citation and stores its full and short forms. The default outline
uses separate native owners for the first two automatic levels.
[Subdocuments](../../docs/research/reference-runs/mission1-subdocuments/README.md) ·
[Cross-references](../../docs/research/reference-runs/mission1-cross-references/README.md) ·
[Authorities](../../docs/research/reference-runs/mission1-authorities/README.md) ·
[Outline](../../docs/research/reference-runs/mission1-outline/README.md)

Default 2 by 2 tables match DOS on explicit recalculation, copying a
relative two-operand sum, and the horizontal join of both top cells.
DOS printer bytes match the recalculated and joined tables. The
vertical join capture is retained as a separate open case. On-screen
sort matches the DOS bodies for the ascending secondary merge key,
moving each record intact and regenerating its page record.
[Table Math](../../docs/research/reference-runs/mission1-table-math/README.md) ·
[Joined cells](../../docs/research/reference-runs/mission1-table-join/README.md) ·
[Sort](../../docs/research/reference-runs/mission1-sort/README.md)

The join build `00a01b7ab804d0de0a60cb90c447fce0d91d3dae1aa7ab53944a1cd9eb2ee91e`
passed all 54 integrated Linux and DOS cases, including both proofreading
journeys. It also passed physical key delivery, GNOME Terminal mouse
retrieval and save, and interrupted-save recovery. DOS reopened all
seven new terminal saves.
[54-case suite](../../research/cache/mission1-join-linux.yXWtz0/suite/suite.json) ·
[Terminal keys](../../research/cache/mission1-join-linux.yXWtz0/terminal-keys/qualification.json) ·
[GNOME Terminal](../../research/cache/mission1-join-linux.yXWtz0/gnome.L6RE/gnome.log) ·
[Recovery](../../research/cache/mission1-join-linux.yXWtz0/recovery) ·
[DOS reopen](../../research/cache/mission1-join-linux.yXWtz0/dos-reopen.log)

The later sort build `1a2abcfeff91158f238e83cb327313842a8501a6ce3b8ceff73d04054b07e5d1`
reproduced byte for byte, passed the uncached Go suite and vet, and
passed all 57 integrated cases, plus the separate terminal sort replay
with the original input left intact. DOS reopened its sorted file.
[Source hashes](../../research/cache/mission1-sort-linux.J2daZ5/source-sha256) ·
[Go](../../research/cache/mission1-sort-linux.J2daZ5/go-test.log) ·
[Sort replay](../../research/cache/mission1-sort-linux.J2daZ5/merge-sort/qualification.json) ·
[57-case suite](../../research/cache/mission1-sort-linux.J2daZ5/suite/suite.json) ·
[DOS reopen](../../research/cache/mission1-sort-linux.J2daZ5/dos-reopen.log)

Column Math matches the captured On and Off owners, decimal tabs, and
a single whole-number subtotal. The terminal shows the active operator;
the native printer stream shows the calculated value without it.
The Column Math build `737028cf20a904d20eb9b0bff65e5775e295e5744ed19ef489bfc46502c9da21`
passed all 58 integrated cases, the uncached Go suite, vet, terminal keys,
GNOME Terminal mouse retrieval and save, and interrupted-save recovery.
DOS reopened the saved subtotal and found Math Off before the ordinary text.
[Column Math evidence](../../docs/research/reference-runs/mission1-column-math/README.md) ·
[58-case suite](../../research/cache/mission1-column-linux.n5b2e0/suite/suite.json) ·
[Reopen](../../research/cache/mission1-column-linux.n5b2e0/dos-reopen.log)

The original startup switch `/m-TESTMAC` runs the recorded macro in
a blank first document. Linux accepts it and the equivalent
`-macro TESTMAC` through its existing macro resolver. F10 saves the
same native body; the startup run leaves the macro file intact.
[Startup evidence](../../docs/research/reference-runs/mission1-startup-macro/README.md) ·
[Terminal replay](../../research/cache/mission1-startup-linux.cUxp15/startup-macro/qualification.json) ·
[59-case suite](../../research/cache/mission1-startup-linux.cUxp15/suite/suite.json) ·
[DOS reopen](../../research/cache/mission1-startup-linux.cUxp15/dos-reopen.log)

[Fixture checksums](../../docs/research/reference-runs/mission1-structured-fixtures.sha256)

The DOS worksheet replays now supply original A1:B2 import, link,
and explicit refresh fixtures. The refreshed table changes 7 to 19
and preserves its source path and selected range.
[Worksheet evidence](../../docs/research/reference-runs/mission1-spreadsheet/README.md)

The first printer follow-up matches the embedded literal command
owner, Reveal Codes, and the complete saved Standard Printer stream.
The printer build `a78dbae89118ee40c8ffa9304a3f31ad358f4cddf08048c9d2afb0232c0bd264`
reproduced byte for byte and passed the terminal print-to-disk replay
and all 60 integrated cases.
[Printer command evidence](../../docs/research/reference-runs/mission1-printer-command/README.md) ·
[Terminal save and print replay](../../research/cache/mission1-printer-linux.PeTUFt/literal-save/qualification.json) ·
[DOS reopen](../../research/cache/mission1-printer-linux.PeTUFt/dos-reopen.log) ·
[60-case suite](../../research/cache/mission1-printer-linux.PeTUFt/suite/suite.json)

The single and double Line Draw cases preserve the original set 3
character identities, including the two different end caps. Four
Right presses and F7 match the DOS visual and native observations.
The Line Draw build `0a0230d1bbcab96e30894c447b85f199f53ce9c1cf8009fbe44bbdefeae85ee4`
reproduced byte for byte and passed the uncached Go suite, vet, and both
focused terminal replays. The original reopened both output files.
[Line Draw evidence](../../docs/research/reference-runs/mission1-line-draw/README.md) ·
[Source hashes](../../research/cache/mission1-draw-linux.5715pk/source-sha256) ·
[Single stroke](../../research/cache/mission1-draw-linux.5715pk/single/qualification.json) ·
[Double stroke](../../research/cache/mission1-draw-linux.5715pk/double/qualification.json) ·
[DOS reopen](../../research/cache/mission1-draw-linux.5715pk/dos-reopen.log) ·
[62-case suite](../../research/cache/mission1-draw-linux.5715pk/suite/suite.json)

The language cue switches US to UK at the cursor and survives a DOS
reopen with the original native owner. The product still has only the
US proofreading dictionary. The DOS Thesaurus capture establishes the
lookup and cancel flow for a known word; product lookup remains open.
[Language evidence](../../docs/research/reference-runs/mission1-language/README.md) ·
[Thesaurus evidence](../../docs/research/reference-runs/mission1-thesaurus/README.md)

The language build `3001598c3d1f9814727fa3bdb800c705177b24539efc132366c7245410194505`
reproduced byte for byte, passed the uncached Go suite and vet, and
matched the DOS body in the focused terminal replay.
[Source hashes](../../research/cache/mission1-language-linux.OnGFk8/source-sha256) ·
[Go](../../research/cache/mission1-language-linux.OnGFk8/go-test.log) ·
[Terminal replay](../../research/cache/mission1-language-linux.OnGFk8/language/qualification.json) ·
[DOS reopen](../../research/cache/mission1-language-linux.OnGFk8/dos-reopen.log) ·
[Terminal keys](../../research/cache/mission1-language-linux.OnGFk8/terminal-keys/qualification.json) ·
[GNOME Terminal](../../research/cache/mission1-language-linux.OnGFk8/gnome.ZsBq/gnome.log) ·
[Recovery](../../research/cache/mission1-language-linux.OnGFk8/recovery) ·
[Integrated run](../../research/cache/mission1-language-linux.OnGFk8/suite/suite.json)
The integrated manifest records the completed case count and final verdict
when the run finishes.

The fixed-pitch printer captures also qualify native Kerning On at the
cursor. Its Reveal Codes and Standard Printer stream match. Proportional
kerning with the selected font metrics remains open.
The working-tree build
`e7bb6487674dd0252878b4a9d96a44d94c06fda0971981b1d0b6e7d02b5bee0f`
reproduced byte for byte and passed the uncached Go suite, vet, the
focused terminal replay, terminal keys, and GNOME Terminal mouse
retrieval and save. DOS reopened the native document with Kerning On.
[Kerning evidence](../../docs/research/reference-runs/mission1-kerning/README.md) ·
[Source hashes](../../research/cache/mission1-kerning-linux.DkamUG/source-sha256) ·
[Go](../../research/cache/mission1-kerning-linux.DkamUG/go-test.log) ·
[Terminal replay](../../research/cache/mission1-kerning-linux.DkamUG/kerning/qualification.json) ·
[GNOME Terminal](../../research/cache/mission1-kerning-linux.DkamUG/gnome.Z90X/gnome.log) ·
[DOS reopen](../../research/cache/mission1-kerning-linux.DkamUG/dos-reopen.log) ·
[Integrated run](../../research/cache/mission1-kerning-linux.DkamUG/suite/suite.json)

The current audit has 161 verified, 54 partial, and 29 unimplemented
scenarios. Linux acceptance remains open: the tested executables came
from the working tree. The remaining command gaps, a clean source build
and rerun, independent review, and promotion of the accepted preview
are still required.
[Command audit](../../docs/research/mission-1-command-audit.md)
