# Mission 1 Linux qualification, November 14, 2026

The working-tree build has SHA-256
`5cff3aec29488df2bd98c1bdfc79c0945e8d5c718a27cf2c2fd109e2c96a394c`.
The rebuild matched byte for byte. The build record identifies all
201 compiled inputs. [Build record](../../research/cache/mission1-initial-work.QviAjJ/working-tree-build-loaded.json)

| Scenario | Evidence |
| --- | --- |
| Initial Codes | F10 matches the whole DOS file with double spacing, with reset to single spacing, when single spacing is selected directly and after an automatic page break. A loaded document resets and resaves byte for byte with both Fast Save settings. Reopened compact and archived files Save As with the original bytes. DOS printed Wordling's double-spacing and reset saves byte for byte with the original streams. [Captures](../../docs/research/reference-runs/mission1-initial-codes/README.md) · [Eight terminal results](../../research/cache/mission1-initial-work.QviAjJ/loaded-pty) · [DOS print replay](../../research/cache/mission1-initial-work.QviAjJ/dos-product-print.log) |
| Macro search | The F2 search compares the actual document. A failure stops the default WPM, ON NOT FOUND handles a missed query, and a real match continues at the DOS cursor. The 19 terminal macro cases passed against the original native bodies. [Captures](../../docs/research/reference-runs/mission1-macro-search/README.md) · [Macro cases](../../research/cache/mission1-initial-work.QviAjJ/macro-r3) |
| List Files Conditions | The terminal exercises the DOS creation and revision date boundaries, all eight Summary fields, Reset, the transient miss and three Undo levels. [Terminal result](../../research/cache/mission1-initial-work.QviAjJ/conditions-final/qualification.json) |
| Print on disk | Standard Printer output for the full on-disk document matches DOS. Typing after print confirms the working document and caret remain in place. [Terminal result](../../research/cache/mission1-initial-work.QviAjJ/disk-print-final/qualification.json) · [DOS run](../../research/cache/mission1-initial-work.QviAjJ/dos-print-preserve.log) |
| Editing | Searching for a real Underline code skips literal `[UND]` text. In a fresh document, Escape, 5, x followed by q saves `xxxxxq`. [Underline search](../../docs/research/reference-runs/mission1-formatting-search/README.md) · [Character repeat](../../docs/research/reference-runs/mission1-character-repeat/README.md) |
| Advance | The DOS captures cover absolute Position, relative Right and Down at the page boundary. They establish when print placement differs from the visible cells and how Down clamps to the page. Wordling still needs the three authoring and layout paths. [DOS captures](../../docs/research/reference-runs/mission1-advance/README.md) |
| Regression | Go tests, go vet, race checks, fixture hashes, and the test that rejects a damaged Initial Codes archive passed. [Go](../../research/cache/mission1-initial-work.QviAjJ/go-loaded.log) · [Vet](../../research/cache/mission1-initial-work.QviAjJ/vet-loaded.log) · [Race](../../research/cache/mission1-initial-work.QviAjJ/race-loaded.log) · [Fixtures](../../research/cache/mission1-initial-work.QviAjJ/fixtures.log) · [Archive refusal](../../research/cache/mission1-initial-work.QviAjJ/archive-refusal.log) |

All 79 cases in the [integrated Linux and DOS preflight](../../research/cache/mission1-initial-work.QviAjJ/suite-loaded/suite.json)
passed on the build with the loaded Initial Codes save formats.
On the latest build, [GNOME Terminal proofreading](../../research/cache/mission1-initial-work.QviAjJ/gnome-proof-loaded/run.log)
matched the original DOS native body and supplementary dictionary.
[Terminal input](../../research/cache/mission1-initial-work.QviAjJ/terminal-loaded/qualification.json)
and [eight recovery journeys](../../research/cache/mission1-initial-work.QviAjJ/recovery-loaded)
also passed.

The [audit](../../docs/research/mission-1-command-audit.md) has 186
verified, 36 partial and 22 unimplemented scenarios. Initial Codes
qualification covers single and double spacing in the captured Standard
Printer profile. Other initial settings, combinations with Summary or
named styles, and further Fast Save generations remain open. Formal
acceptance also requires the remaining parity work, a clean candidate,
independent review, and a rebuilt accepted preview. The
[formal candidate builder](../../research/cache/mission1-initial-work.QviAjJ/formal.log)
reports changes in the shared production tree.
