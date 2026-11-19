# List Files and DOS text conversion

Reference is the March 9, 1992 US WordPerfect 5.1 release with Standard Printer
and the pinned [offline DOS guest](../../../reference-environment/README.md).
Run the `replay-*.py` scripts from the repository root with
`PYTHONPATH=scripts/reference`. They allocate private disk copies and retain
capture directories under `research/cache`.

- [Creation From](creation-from-same-day.txt) excludes the Summary date itself.
  [An earlier From](creation-from-prior-day.txt) includes it, and
  [To](creation-to-same-day.txt) includes the same day.
- Revision uses the directory date. A [lower bound alone](revision-lower-epoch.txt)
  yielded zero results. The [upper bound alone](revision-upper-prior.txt) can
  exclude later revisions. [Both bounds on the same day](revision-same-day-range.txt)
  include that date, and the [two-date range](revision-range.txt) confirms the
  upper cutoff. A miss briefly displays in Conditions and then yields
  [an empty listing](dos-conditions-no-match.txt).
- [The Summary form](dos-summary-search-fixture.txt) supplies eight unique
  field values. The `summary-*.txt` captures each show only `FIELDS.WP` after
  the corresponding field search. [Undo](undo-1.txt) rolls back one search at
  a time, [including a no-match search](undo-2.txt), for [three levels](undo-3.txt).
- [List Files Print](dos-list-print-prompt.txt) asks for pages. Enter with an
  empty field prints all of the original `Z.WP`; entering `2` prints only
  page two. Wordling's worked examples match `LIST.PRN` and `PAGE2.PRN`
  byte for byte. The [Print Document on Disk](print-disk-filename.txt) route
  produces the same printer bytes without retrieving the source into the editor.
- [Declining DOS text replacement](dos-decline-overwrite.txt) preserves the
  target and returns to the DOS text filename prompt. The next accepted
  replacement writes the converted bytes.
- `CTRL.TXT` covers raw controls except tab, line/page breaks and EOF.
  DOS produced `CTRL.WP` and exported `BACK.TXT`. NUL persists in the native
  body and renders as `^@` on the first DOS text import. DOS removes it when
  reopening a native document and from its text export. The other tested
  controls retain their identities. [DOS reopened Wordling's native save](dos-reopened-wordling.txt)
  and produced `BACK.TXT` exactly.
- `CP437.TXT` exercises every byte from 7F through FF in isolation. The
  Linux native body and export match `CP437.WP` and `CP437OUT.TXT`. The
  original preserves 7F through FE on export and omits FF.
- `LINES.TXT` covers tabs, bare line feeds, repeated CR, soft and hard pages,
  FF and DOS EOF. `LINES.WP` and `LINESOUT.TXT` are the original outputs.
  [Reveal Codes](dos-line-controls-reveal.txt) identifies the standalone
  soft page, which DOS exports as a space.

The [Find patterns](pattern-results.json) cover literal names, wildcards, quoted
phrases, and left-to-right AND, OR and exclusion terms. The Linux regressions
are in `internal/tui/everyday_ui_test.go`. The [marked-file witness](../issue7-marked-files/filtered/screen.txt) confirms
that Find filters the marked subset, and [Undo](../issue7-marked-files/undo/screen.txt)
restores the marks. The full printer page-selection grammar and a broader
conversion and overwrite matrix remain open.
