# WP 5.1 command-level scenario catalogue

Generated from `command-scenarios.json` by `scripts/render-scenarios.py`.

**210 documentary scenarios**: 197 manual-derived,
10 project-contract cases, and 3 explicit oracle investigation.
**26 cases have partial original-app observations; 184 remain not run.**
All Wordling implementations/differential tests remain **not implemented**. These are representative cases,
not a claim that every subcommand or branch has been enumerated.

[Reference release decision](../decisions/0001-reference-release.md) selects
plain U.S. English WP 5.1 DOS dated 1992-03-09. The [installation and limits](reference-environment/README.md)
are fingerprinted; bounded original-only smoke probes have begun. [Coverage matrix](scenario-coverage.md) links
the parent groups; [workbook map](workbook-map.md) tracks lesson themes.

## Procedure notation and execution contract

- `KEY Ctrl+F8` is a chord. Commas in `KEY Home, Home, Up` mean sequential presses.
- `TYPE` enters literal fixture text. `SELECT` chooses a named original menu
  item using keyboard navigation; it does not imply a guessed numeric accelerator.
- Begin each case with a fresh copied setup and declared fixture; restore
  clock, keyboard, display, filesystem and printer/resource profiles. Use scratch
  copies for destructive commands. Never operate on the immutable master fixture.
- Starting states are human-readable fixture specifications. No fixture builder
  for the full catalogue exists yet; `scripts/reference/smoke.py` implements a bounded subset of probes. Menu wording and unresolved prompt
  responses require capture before automation; these are documentary drafts.
- Record text/code cursor positions, status/prompt screens and resulting files.
  For print/layout cases include resource hashes and full printer-output bytes.
- Manual-derived expectations are hypotheses to test against the original.
  Contract cases express stronger Wordling requirements (especially byte-identical
  no-edit saves); do not invent matching original behavior. Investigation cases
  intentionally have unresolved behavior and cannot count as acceptance passes.
- `partially-observed` means linked original-only smoke checks were executed;
  it does not mean every expected branch, byte invariant or Wordling behavior was tested.
- Source locators refer to pinned source bytes. OCR has not been visually verified
  for every key/menu label; named navigation avoids uncertain accelerators.

<a id="cmd51-001"></a>

## CMD51-001: Open and close pull-down menus

Parent: WP51-001. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Fresh blank document; original keyboard, menus initially hidden.

**When**

1. KEY Alt+=
2. KEY Alt+=

**Then**

- First invocation shows the menu bar; second hides it.
- Document bytes and cursor position do not change.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 27-28 (printed 10-11)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=27).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-002"></a>

## CMD51-002: Back one menu level versus leave menus

Parent: WP51-001, WP51-007. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Open a pull-down submenu with at least two navigation levels.

**When**

1. KEY F1
2. Reopen the same submenu.
3. KEY F7

**Then**

- F1 backs out one level.
- F7 leaves the pull-down menus entirely; neither navigation action inserts text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 72-73 (printed 55-56)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=72).

<a id="cmd51-003"></a>

## CMD51-003: Help preserves the interrupted feature

Parent: WP51-002. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor in a Format menu with no uncommitted change.

**When**

1. KEY F3
2. KEY Enter

**Then**

- Help concerns the active feature.
- Enter returns to the previous menu without changing document content.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 292-292 (printed 275-275)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=292).

<a id="cmd51-004"></a>

## CMD51-004: Space exits help

Parent: WP51-002. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Help is displayed for an active feature.

**When**

1. KEY Space

**Then**

- The original feature screen returns; no space is inserted into document text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 292-292 (printed 275-275)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=292).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-005"></a>

## CMD51-005: Repeat a character a declared number of times

Parent: WP51-007. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Empty document; no selected block.

**When**

1. KEY Esc
2. TYPE 5
3. TYPE x

**Then**

- Exactly five x characters are inserted.
- The repetition count is consumed according to the one-operation repeat behavior.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 567-568 (printed 550-551)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=567).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-006"></a>

## CMD51-006: Cancel a selected block

Parent: WP51-007. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; alpha selected with Alt+F4 and cursor motion.

**When**

1. KEY F1

**Then**

- Selection is cancelled and text is unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 65-67 (printed 48-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=65).

<a id="cmd51-007"></a>

## CMD51-007: Switch between independent documents

Parent: WP51-006. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document 1 contains FIRST, document 2 is blank.

**When**

1. KEY Shift+F3
2. TYPE SECOND
3. KEY Shift+F3

**Then**

- Document 2 receives SECOND.
- Document 1 still contains FIRST; switching restores its original state.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 645-647 (printed 628-630)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=645).

<a id="cmd51-008"></a>

## CMD51-008: Split document screens into windows

Parent: WP51-006. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Both document screens have distinct text.

**When**

1. KEY Ctrl+F3
2. SELECT Window
3. TYPE 8 then KEY Enter

**Then**

- Two editing windows appear with the requested current-window height subject to documented limits.
- Both documents remain editable; capture active-window focus and status.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 723-724 (printed 706-707)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=723).

<a id="cmd51-009"></a>

## CMD51-009: Display the selected keyboard map

Parent: WP51-003. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- A bundled keyboard definition is available in the declared macro/keyboard directory.

**When**

1. KEY Shift+F1
2. SELECT Keyboard Layout
3. Highlight the declared keyboard.
4. SELECT Map

**Then**

- A map of that keyboard is displayed.
- Displaying the map does not change the keyboard definition or document.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 330-330 (printed 313-313)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=330).

<a id="cmd51-010"></a>

## CMD51-010: Select a keyboard then restore Original

Parent: WP51-003. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Original keyboard active; bundled alternate keyboard available.

**When**

1. KEY Shift+F1
2. SELECT Keyboard Layout
3. Highlight Alternate and SELECT Select.
4. Exit to editing; exercise its documented Help/Cancel mapping.
5. Reopen Keyboard Layout and SELECT Original.

**Then**

- Selected keyboard mappings take effect.
- Restoring Original restores original F1/F3 semantics; capture persisted setup bytes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 321-324 (printed 304-307)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=321).

<a id="cmd51-011"></a>

## CMD51-011: Move one visible character left

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Plain text abc; cursor immediately before c.

**When**

1. KEY Left

**Then**

- Cursor is immediately before b; text stays abc.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-012"></a>

## CMD51-012: Move one visible character right

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Plain text abc; cursor immediately before b.

**When**

1. KEY Right

**Then**

- Cursor is immediately before c; text stays abc.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-013"></a>

## CMD51-013: Move left one word

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Plain text alpha beta gamma; cursor immediately before gamma.

**When**

1. KEY Ctrl+Left

**Then**

- Cursor moves one word left according to original word boundaries; text is unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-014"></a>

## CMD51-014: Move right one word

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Plain text alpha beta gamma; cursor immediately before alpha.

**When**

1. KEY Ctrl+Right

**Then**

- Cursor moves one word right according to original word boundaries; text is unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-015"></a>

## CMD51-015: Move to left screen edge

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Long line extends outside the left edge of the editing viewport.

**When**

1. KEY Home, Left

**Then**

- Cursor reaches the left edge of the screen, which is distinct from the far left of the line.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-016"></a>

## CMD51-016: Move to actual start of line

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Long line extends outside the left edge of the editing viewport.

**When**

1. KEY Home, Home, Left

**Then**

- Cursor reaches the far left of the line, including content off-screen.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-017"></a>

## CMD51-017: Move to right screen edge

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Long line extends outside the right edge of the editing viewport.

**When**

1. KEY Home, Right

**Then**

- Cursor reaches the right screen edge, distinct from the true line end.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-018"></a>

## CMD51-018: Move to actual end of line

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Long line extends outside the right edge of the viewport.

**When**

1. KEY End

**Then**

- Cursor reaches the far right of the line; off-screen content is included.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-019"></a>

## CMD51-019: Go to start after initial codes

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document begins with formatting codes followed by text; cursor at end.

**When**

1. KEY Home, Home, Up

**Then**

- Cursor reaches document beginning after initial formatting codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-020"></a>

## CMD51-020: Go to start before initial codes

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document begins with formatting codes followed by text; cursor at end.

**When**

1. KEY Home, Home, Home, Up

**Then**

- Cursor reaches document beginning before formatting codes, distinguishable in Reveal Codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-021"></a>

## CMD51-021: Go to document end

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document ends in text followed by formatting codes; cursor near beginning.

**When**

1. KEY Home, Home, Down

**Then**

- Cursor reaches document end after terminal formatting codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-022"></a>

## CMD51-022: Page forward

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- At least three pages under fixed resources; cursor on first page.

**When**

1. KEY PgDn

**Then**

- Cursor moves to the first line of the next page.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-023"></a>

## CMD51-023: Page backward

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- At least three pages under fixed resources; cursor on third page.

**When**

1. KEY PgUp

**Then**

- Cursor moves to the first line of the previous page.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120).

<a id="cmd51-024"></a>

## CMD51-024: Go To the next matching character

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; cursor at beginning.

**When**

1. KEY Ctrl+Home
2. TYPE b

**Then**

- Cursor moves immediately to the right of the next b; document unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 241-241 (printed 224-224)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=241).

<a id="cmd51-025"></a>

## CMD51-025: Go To the next paragraph boundary

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Two paragraphs separated by a hard return; cursor in first.

**When**

1. KEY Ctrl+Home
2. KEY Enter

**Then**

- Cursor goes to the next hard-return code, not merely the next visual wrapped line.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 241-241 (printed 224-224)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=241).

<a id="cmd51-026"></a>

## CMD51-026: Go To a numbered page

Parent: WP51-008. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Three pages with ordinary numbering under fixed geometry.

**When**

1. KEY Ctrl+Home
2. TYPE 2 then KEY Enter

**Then**

- Cursor reaches the top of page 2; capture behavior at code boundaries.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 241-241 (printed 224-224)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=241).

<a id="cmd51-027"></a>

## CMD51-027: Select by cursor movement

Parent: WP51-009. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; cursor before a.

**When**

1. KEY Alt+F4
2. KEY Right five times

**Then**

- alpha is selected.
- The text itself has not changed; selection direction and code boundary positions are recorded.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 65-67 (printed 48-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=65).

<a id="cmd51-028"></a>

## CMD51-028: Typing a character while Block is on seeks it

Parent: WP51-009. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Text alpha beta; cursor before a.

**When**

1. KEY Alt+F4
2. TYPE b

**Then**

- The cursor moves to the next b and selection changes.
- b is not inserted and does not replace selected text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 67-67 (printed 50-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=67).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-029"></a>

## CMD51-029: Block Enter extends to a hard return

Parent: WP51-009. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Paragraph wraps across two visual lines then ends with a hard return.

**When**

1. Place cursor at paragraph start.
2. KEY Alt+F4
3. KEY Enter

**Then**

- Selection extends to the paragraph boundary, including wrapped text rather than ending at the first visual line.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 67-67 (printed 50-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=67).

<a id="cmd51-030"></a>

## CMD51-030: Refuse block deletion

Parent: WP51-009, WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; alpha selected.

**When**

1. KEY Delete
2. TYPE n

**Then**

- Deletion is not performed; original text remains.
- Capture whether selection remains active; do not infer it.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 66-67 (printed 49-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=66); [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-031"></a>

## CMD51-031: Confirm block deletion

Parent: WP51-009, WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; alpha selected.

**When**

1. KEY Delete
2. TYPE y

**Then**

- Selected text is removed after confirmation.
- Remaining text and preserved codes match the selected boundaries.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 66-67 (printed 49-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=66); [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-032"></a>

## CMD51-032: Bold a block and finish Block mode

Parent: WP51-009, WP51-030. Requirements: FR-005, FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; alpha selected.

**When**

1. KEY F6

**Then**

- alpha becomes bold; beta does not.
- The block operation ends Block mode; inspect paired codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 66-67 (printed 49-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=66); [REF51 PDF 53-57 (printed 36-40)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=53).

<a id="cmd51-033"></a>

## CMD51-033: Protect a block against page separation

Parent: WP51-009. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Selected block shorter than one page, placed near a page boundary.

**When**

1. KEY Shift+F8
2. TYPE y
3. Add preceding text sufficient to force a page decision.

**Then**

- Protected block moves as a unit instead of splitting across the boundary.
- The text remains editable; block protection is a pagination function.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 68-71 (printed 51-54)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=68).

<a id="cmd51-034"></a>

## CMD51-034: Delete preceding character

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text abc; cursor before c.

**When**

1. KEY Backspace

**Then**

- Text becomes ac.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-035"></a>

## CMD51-035: Delete character at cursor

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text abc; cursor before b.

**When**

1. KEY Delete

**Then**

- Text becomes ac.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-036"></a>

## CMD51-036: Delete current word

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta gamma; cursor at start of beta.

**When**

1. KEY Ctrl+Backspace

**Then**

- Word beta is deleted; capture treatment of the surrounding separator.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-037"></a>

## CMD51-037: Delete current word using alternate key

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta gamma; cursor at start of beta.

**When**

1. KEY Ctrl+Delete

**Then**

- Same word-level deletion semantics as the documented alternate command.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-038"></a>

## CMD51-038: Delete to end of line

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Plain text abcdef on one visual line; cursor before d.

**When**

1. KEY Ctrl+End

**Then**

- Text def to the line end is removed; abc remains.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-039"></a>

## CMD51-039: Delete back to start of word

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; cursor within beta after be.

**When**

1. KEY Home, Backspace

**Then**

- Deletion extends backward to the beginning of the current word.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-040"></a>

## CMD51-040: Delete forward to next word

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta gamma; cursor inside beta.

**When**

1. KEY Home, Delete

**Then**

- Deletion extends forward to the beginning of the next word.
- Capture cursor and saved code stream, including separator handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-041"></a>

## CMD51-041: Confirm delete to end of page

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Multi-page document; cursor in page 1.

**When**

1. KEY Ctrl+PgDn
2. TYPE y

**Then**

- Content from cursor to current page end is deleted.
- Following-page behavior is captured under fixed resources, not inferred from a text-only buffer.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 133-133 (printed 116-116)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=133).

<a id="cmd51-042"></a>

## CMD51-042: Restore latest deletion at the current cursor

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Delete text XYZ, then move the cursor to a different insertion point.

**When**

1. KEY F1
2. SELECT Restore

**Then**

- XYZ is restored at the current cursor rather than automatically at its former location.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 714-714 (printed 697-697)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=714).

<a id="cmd51-043"></a>

## CMD51-043: Select among three remembered deletions

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Create three distinct deletions ONE, TWO and THREE with cursor movement separating operations.

**When**

1. KEY F1
2. SELECT Previous Deletion
3. SELECT Previous Deletion
4. SELECT Restore

**Then**

- The third most recent deletion ONE is restored.
- The three history entries can be browsed without modifying the document until Restore.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 714-714 (printed 697-697)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=714).

<a id="cmd51-044"></a>

## CMD51-044: Consecutive deletion keys belong to one deletion

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text abcdef; cursor at start.

**When**

1. KEY Delete three times without moving cursor.
2. Move to end.
3. KEY F1
4. SELECT Restore

**Then**

- abc is restored as one deletion entry, not three separate entries.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 714-714 (printed 697-697)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=714).

<a id="cmd51-045"></a>

## CMD51-045: Character deletion restoration differs for paired attributes

Parent: WP51-011. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Text has a bold attributed segment; delete through it with character Backspace/Delete.

**When**

1. Move to restoration position.
2. KEY F1
3. SELECT Restore

**Then**

- Restore follows the documented exception: paired bold/underline attribute codes deleted by character commands are not automatically restored.
- Compare against a separate block-deletion fixture; do not reuse one expected code stream for all delete commands.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 714-714 (printed 697-697)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=714).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-046"></a>

## CMD51-046: Toggle typeover and return to insertion

Parent: WP51-012. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Text abc; cursor before b.

**When**

1. KEY Insert
2. TYPE X
3. KEY Insert
4. TYPE Y

**Then**

- Typeover replaces b with X; returning to insert mode inserts Y without overwriting the next character.
- Status shows Typeover only while the mode is active.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 712-713 (printed 695-696)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=712).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-047"></a>

## CMD51-047: Typeover stops short of a code

Parent: WP51-012. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text ab, then an attribute code, then cd; cursor at the code boundary.

**When**

1. KEY Insert
2. TYPE X

**Then**

- X is inserted before the formatting code; the code itself is not overwritten.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 712-712 (printed 695-695)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=712).

<a id="cmd51-048"></a>

## CMD51-048: Toggle Reveal Codes without editing

Parent: WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Document contains plain and bold text; cursor before the bold segment.

**When**

1. KEY Alt+F3
2. KEY Alt+F3

**Then**

- First toggle opens the code pane; second returns to normal editing.
- Native document bytes remain unchanged by view toggling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 577-579 (printed 560-562)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=577).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-049"></a>

## CMD51-049: Traverse a code while visible text cursor appears stationary

Parent: WP51-008, WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor immediately before a formatting code; Reveal Codes enabled.

**When**

1. KEY Right

**Then**

- Code-pane cursor crosses the code even when the normal text cursor has no visible character movement.
- No text or code is deleted.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 120-121 (printed 103-104)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120); [REF51 PDF 577-579 (printed 560-562)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=577).

<a id="cmd51-050"></a>

## CMD51-050: Delete code at cursor

Parent: WP51-011, WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Reveal Codes enabled; cursor directly on an unwanted Center code.

**When**

1. KEY Delete

**Then**

- Center code is removed and both views reflect the changed formatting.
- Capture any confirmation prompt before responding; use only the original prompt behavior.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 129-130 (printed 112-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=129).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-051"></a>

## CMD51-051: Backspace deletes code immediately before cursor

Parent: WP51-011, WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Reveal Codes enabled; cursor immediately after an unwanted alignment code.

**When**

1. KEY Backspace

**Then**

- Code immediately before the cursor is removed; following text is preserved.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 129-130 (printed 112-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=129).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-052"></a>

## CMD51-052: Search forward and repeat

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta alpha; cursor at beginning.

**When**

1. KEY F2
2. TYPE alpha
3. KEY F2
4. KEY F2 twice

**Then**

- First search locates the first alpha.
- Repeating locates the next alpha without changing text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 588-589 (printed 571-572)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=588).

<a id="cmd51-053"></a>

## CMD51-053: Search backward

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta alpha; cursor at end.

**When**

1. KEY Shift+F2
2. TYPE alpha
3. KEY Shift+F2

**Then**

- The previous alpha is located using backward search.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 588-589 (printed 571-572)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=588).

<a id="cmd51-054"></a>

## CMD51-054: Lowercase search includes uppercase

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text ALPHA Alpha alpha; cursor at beginning.

**When**

1. KEY F2
2. TYPE alpha
3. KEY F2
4. Repeat search through matches.

**Then**

- All three spellings match the lowercase search string.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 589-589 (printed 572-572)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=589).

<a id="cmd51-055"></a>

## CMD51-055: Uppercase search restricts matching

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha Alpha; cursor before first word.

**When**

1. KEY F2
2. TYPE Alpha
3. KEY F2

**Then**

- Initial uppercase A excludes the all-lowercase occurrence.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 589-589 (printed 572-572)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=589).

<a id="cmd51-056"></a>

## CMD51-056: Search a real formatting code

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document contains literal characters [UND] and a separately underlined word.

**When**

1. KEY F2
2. KEY F8
3. KEY F2

**Then**

- Search locates the actual Underline code rather than bracketed text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 589-589 (printed 572-572)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=589).

<a id="cmd51-057"></a>

## CMD51-057: Search specifically for Bold Off

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- A bold segment is followed by plain text; cursor at document beginning.

**When**

1. KEY F2
2. KEY F6 twice
3. KEY Left
4. KEY Backspace
5. KEY F2

**Then**

- The search string contains the Bold Off code alone and locates its boundary.
- Deleting a code inside the search editor does not alter document codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 589-589 (printed 572-572)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=589).

<a id="cmd51-058"></a>

## CMD51-058: Extend Block using Search

Parent: WP51-009, WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta gamma; block starts at document beginning.

**When**

1. KEY F2
2. TYPE gamma
3. KEY F2

**Then**

- Selection extends to the search match as specified by original block search semantics.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 590-590 (printed 573-573)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=590).

<a id="cmd51-059"></a>

## CMD51-059: Replace without individual confirmation

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text amber amber; cursor at beginning.

**When**

1. KEY Alt+F2
2. TYPE n
3. TYPE amber
4. KEY F2
5. TYPE blue
6. KEY F2

**Then**

- Both occurrences become blue.
- No individual replacement approval is requested.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 568-569 (printed 551-552)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=568).

<a id="cmd51-060"></a>

## CMD51-060: Replace with per-match decisions

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text amber amber; cursor at beginning.

**When**

1. KEY Alt+F2
2. TYPE y
3. TYPE amber
4. KEY F2
5. TYPE blue
6. KEY F2
7. Approve the first match and skip the second using displayed choices.

**Then**

- Only the approved occurrence changes.
- Capture exact prompt choices from the original instead of guessing response accelerators.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 568-570 (printed 551-553)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=568).

<a id="cmd51-061"></a>

## CMD51-061: Empty replacement deletes matches

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text abXXcdXXef; cursor at beginning.

**When**

1. KEY Alt+F2
2. TYPE n
3. TYPE XX
4. KEY F2
5. KEY F2 without replacement text

**Then**

- Text becomes abcdef.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 569-569 (printed 552-552)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=569).

<a id="cmd51-062"></a>

## CMD51-062: Search accepts F7 as the string terminator

Parent: WP51-014. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; cursor at beginning.

**When**

1. KEY F2
2. TYPE beta
3. KEY F7

**Then**

- Search executes rather than treating F7 as application exit.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [ENH51 PDF 6-7](https://mendelson.org/wpdos/WP51ENHA.pdf#page=6).

<a id="cmd51-063"></a>

## CMD51-063: Convert a block to uppercase

Parent: WP51-015. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; alpha selected.

**When**

1. KEY Shift+F3
2. SELECT Uppercase

**Then**

- Selected word becomes ALPHA; beta remains unchanged.
- This invocation performs case conversion, not document switching.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 73-74 (printed 56-57)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=73).

<a id="cmd51-064"></a>

## CMD51-064: Lowercase conversion preserves sentence/I exceptions

Parent: WP51-015. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- A selected sentence includes its preceding punctuation and the word I followed by an apostrophe.

**When**

1. KEY Shift+F3
2. SELECT Lowercase

**Then**

- Original sentence-initial and I-apostrophe exceptions remain capitalized as documented.
- Do not replace this command with unconditional Unicode lowercasing.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 74-74 (printed 57-57)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=74).

<a id="cmd51-065"></a>

## CMD51-065: Retrieve inserts at the cursor

Parent: WP51-019. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Current document text AB; cursor between A and B; file INSERT contains XY.

**When**

1. KEY Shift+F10
2. TYPE INSERT then KEY Enter

**Then**

- Retrieved text is inserted at the cursor; existing document text is not replaced wholesale.
- Formatting follows original retrieval rules; capture initial-code interactions separately.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 571-573 (printed 554-556)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=571).

<a id="cmd51-066"></a>

## CMD51-066: Name a new document with F10

Parent: WP51-020. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Unnamed document contains WORDLING TEST; scratch directory is writable.

**When**

1. KEY F10
2. TYPE NEWTEST then KEY Enter

**Then**

- NEWTEST is saved in the default directory using native WP format.
- Cursor location is retained and editing can continue.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 582-582 (printed 565-565)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=582).

Observed scope: Bounded original-app smoke probes, repeated from fresh copies. Full scenario branches and all Wordling differential behavior remain unverified.

Evidence: [2026-10-29-smoke-02](reference-runs/2026-10-29-smoke-02/run.json), [2026-10-29-smoke-03](reference-runs/2026-10-29-smoke-03/run.json).

<a id="cmd51-067"></a>

## CMD51-067: Decline overwriting an existing file

Parent: WP51-020. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Existing file SAME contains ORIGINAL; current document differs and uses filename SAME.

**When**

1. KEY F10
2. KEY Enter to accept displayed filename.
3. TYPE n at replacement confirmation.

**Then**

- Existing file bytes remain ORIGINAL.
- The application requests a different filename rather than reporting a successful save.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 583-583 (printed 566-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=583).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-068"></a>

## CMD51-068: Approve overwriting an existing file

Parent: WP51-020. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Existing scratch file SAME; edited document bears that name.

**When**

1. KEY F10
2. KEY Enter
3. TYPE y at replacement confirmation.

**Then**

- The edited document replaces SAME after approval.
- Capture native bytes and effects of declared backup/Fast Save settings.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 583-583 (printed 566-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=583).

<a id="cmd51-069"></a>

## CMD51-069: Edit the displayed save filename

Parent: WP51-020. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- An existing document has a displayed filename in the F10 prompt.

**When**

1. KEY F10
2. Use Left/Right and Backspace to edit the displayed filename.
3. KEY Enter

**Then**

- Cursor/edit keys edit the existing name rather than clearing it immediately.
- Contrast with entering a character first, which replaces the displayed name.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 583-583 (printed 566-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=583).

<a id="cmd51-070"></a>

## CMD51-070: Typing a save filename starts a new name

Parent: WP51-020. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- An existing document has filename OLD displayed at its save prompt.

**When**

1. KEY F10
2. TYPE NEW then KEY Enter

**Then**

- The typed name is NEW rather than OLDNEW.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 583-583 (printed 566-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=583).

<a id="cmd51-071"></a>

## CMD51-071: Enable original-document backup

Parent: WP51-021. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch file ORIGINAL exists; backup disabled in copied setup.

**When**

1. KEY Shift+F1
2. SELECT Environment > Backup Options > Original Document Backup
3. TYPE y
4. KEY F7 to leave setup.
5. Retrieve ORIGINAL, edit it and save with overwrite confirmation.

**Then**

- Prior version survives in the original backup artifact.
- Capture the exact backup filename, overwrite-cycle semantics and file bytes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 58-60 (printed 41-43)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=58).

<a id="cmd51-072"></a>

## CMD51-072: Configure timed backup

Parent: WP51-021. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Nonempty modified document; copied setup and controlled clock.

**When**

1. KEY Shift+F1
2. SELECT Environment > Backup Options > Timed Document Backup
3. TYPE y
4. TYPE 1 then KEY Enter
5. KEY F7 to leave setup.
6. Allow the declared timer interval to pass.

**Then**

- A timed backup is produced according to original naming/location rules.
- This is original M1 backup behavior, not modern recovery.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 60-62 (printed 43-45)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=60).

<a id="cmd51-073"></a>

## CMD51-073: Empty editing screen does not create a zero-byte timed backup

Parent: WP51-021. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank editing screen; timed backup enabled with a declared short interval.

**When**

1. Wait through a backup interval with the document still blank.

**Then**

- No zero-byte document backup is created for the blank screen.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [ENH51 PDF 2-2](https://mendelson.org/wpdos/WP51ENHA.pdf#page=2).

<a id="cmd51-074"></a>

## CMD51-074: Startup checks backups for both document screens

Parent: WP51-021. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Both document-screen backup artifacts exist from a controlled interrupted session.

**When**

1. Start the reference with the copied setup.
2. Observe both backup prompts before switching screens.
3. Choose Rename for one and Delete for the other using displayed choices.

**Then**

- Both backup artifacts are considered at startup, including document 2.
- Choices affect the designated backup only.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [ENH51 PDF 2-2](https://mendelson.org/wpdos/WP51ENHA.pdf#page=2).

<a id="cmd51-075"></a>

## CMD51-075: Disable Fast Save before saving

Parent: WP51-022. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document with previous font/style/printer state; default Fast Save enabled.

**When**

1. KEY Shift+F1
2. SELECT Environment > Fast Save (unformatted)
3. TYPE n
4. KEY F7 to return.
5. Save through F10.

**Then**

- Document is fully formatted before save.
- Capture differences in purged obsolete settings; do not conflate this with Wordling no-edit preservation policy.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 214-214 (printed 197-197)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=214).

<a id="cmd51-076"></a>

## CMD51-076: List files with a filename pattern

Parent: WP51-023. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch directory contains A.WP, B.TXT and C.WP.

**When**

1. KEY F5
2. TYPE scratch-path/*.WP using the declared DOS path mapping; KEY Enter.

**Then**

- Only matching files appear.
- Capture exact prompts/default-directory behavior; host paths are not inferred to be DOS paths.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 364-367 (printed 347-350)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=364).

<a id="cmd51-077"></a>

## CMD51-077: Copy a listed file

Parent: WP51-023. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch file COPYME exists and its source bytes are hashed.

**When**

1. KEY F5 and display scratch directory.
2. Highlight COPYME.
3. SELECT Copy
4. Enter a distinct scratch destination.

**Then**

- Destination has identical source file bytes.
- Source remains intact.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 367-368 (printed 350-351)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=367).

<a id="cmd51-078"></a>

## CMD51-078: Rename a listed file

Parent: WP51-023. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch file OLDNAME exists; NEWNAME does not.

**When**

1. KEY F5 and highlight OLDNAME.
2. SELECT Move/Rename
3. Enter NEWNAME using displayed prompts.

**Then**

- NEWNAME identifies the same file content; OLDNAME is no longer the source name.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 367-369 (printed 350-352)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=367).

<a id="cmd51-079"></a>

## CMD51-079: Decline deleting a file from List Files

Parent: WP51-023. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch file KEEP exists with a recorded hash.

**When**

1. KEY F5 and highlight KEEP.
2. SELECT Delete
3. TYPE n

**Then**

- KEEP and its bytes remain present.
- File deletion is not editor Undelete.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 131-132 (printed 114-115)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=131).

<a id="cmd51-080"></a>

## CMD51-080: Toggle long/short file display

Parent: WP51-023. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Directory contains files with document summaries and descriptive names.

**When**

1. KEY F5
2. SELECT Short/Long Display
3. SELECT Short/Long Display

**Then**

- Display alternates original long/short modes without changing document data.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 365-369 (printed 348-352)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=365).

<a id="cmd51-081"></a>

## CMD51-081: Disable file-list sorting in March 1992

Parent: WP51-023. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Copied setup; scratch directory has a controlled entry order distinct from alphabetical order.

**When**

1. KEY Shift+F1
2. SELECT Environment > Document Management/Summary > Sort List Files
3. TYPE n
4. Return to editing and use F5 to display the directory.
5. Invoke Name Search.

**Then**

- List follows directory-entry order under the declared filesystem environment.
- Name Search is refused in unsorted mode; F2 remains the documented search alternative.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [ENH51 PDF 18-18](https://mendelson.org/wpdos/WP51ENHA.pdf#page=18).

<a id="cmd51-082"></a>

## CMD51-082: Set a document password

Parent: WP51-024. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch document; password has not been set.

**When**

1. KEY Ctrl+F5
2. SELECT Password > Add/Change
3. Enter the same test password twice.
4. Save document.

**Then**

- Password entry is not echoed.
- Saved locked document follows the original encrypted format; exact cryptographic bytes require reference fixtures.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 379-380 (printed 362-363)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=379).

<a id="cmd51-083"></a>

## CMD51-083: Import DOS CR/LF as hard returns

Parent: WP51-025. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch DOS text file contains alpha CR LF beta CR LF; blank document.

**When**

1. KEY Ctrl+F5
2. SELECT DOS Text > Retrieve (CR/LF to HRt)
3. Enter text-file name.

**Then**

- CR/LF boundaries become Hard Return codes.
- Input file is preserved.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 702-704 (printed 685-687)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=702).

<a id="cmd51-084"></a>

## CMD51-084: Import DOS text using hyphenation-zone soft-return mode

Parent: WP51-025. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- DOS text fixture has lines ending both inside and outside the declared hyphenation zone.

**When**

1. KEY Ctrl+F5
2. SELECT DOS Text > Retrieve (CR/LF to SRt in H-Zone)
3. Enter fixture filename.

**Then**

- Return conversion follows the selected zone-sensitive mode instead of mapping all lines identically.
- Record exact converted boundaries from the reference.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 703-704 (printed 686-687)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=703).

<a id="cmd51-085"></a>

## CMD51-085: Find files by content

Parent: WP51-028. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch directory has one file containing amber and one without it.

**When**

1. KEY F5
2. SELECT Find
3. Select document-text search and enter amber.

**Then**

- Result list contains only files satisfying the content condition.
- Files are not modified by the search.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 214-218 (printed 197-201)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=214).

<a id="cmd51-086"></a>

## CMD51-086: Display file contents through Look

Parent: WP51-028. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- File with known text/summary is highlighted in List Files.

**When**

1. SELECT Look

**Then**

- File content/summary is inspectable without inserting it into the current editing document.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 381-385 (printed 364-368)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=381).

<a id="cmd51-087"></a>

## CMD51-087: Exit without saving and cancel application exit

Parent: WP51-029. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Modified scratch document; original disk file hash recorded.

**When**

1. KEY F7
2. TYPE n to decline save.
3. TYPE n to decline exiting WordPerfect.

**Then**

- Reference returns to the documented editing/session state.
- Disk file remains unchanged; capture whether the document buffer has been cleared.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 211-211 (printed 194-194)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=211).

<a id="cmd51-088"></a>

## CMD51-088: Commit a document summary

Parent: WP51-090. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document text unchanged; cursor in middle of a paragraph.

**When**

1. KEY Shift+F8
2. SELECT Document > Summary
3. Set Author to Wordling and Abstract to Scratch summary.
4. KEY F7 to accept.
5. Save and retrieve the document; inspect summary.

**Then**

- Summary fields persist.
- Returning from the summary restores the editing cursor position.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 162-164 (printed 145-147)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=162).

<a id="cmd51-089"></a>

## CMD51-089: Cancel summary changes

Parent: WP51-090. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document already has a saved Author value.

**When**

1. KEY Shift+F8
2. SELECT Document > Summary
3. Change Author to DISCARD.
4. KEY F1

**Then**

- Unaccepted summary changes are discarded.
- Original Author value remains.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 163-163 (printed 146-146)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=163).

<a id="cmd51-090"></a>

## CMD51-090: Toggle bold while typing

Parent: WP51-030. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document; original font resources.

**When**

1. KEY F6
2. TYPE alpha
3. KEY F6
4. TYPE beta

**Then**

- alpha has the selected attribute and beta does not.
- Reveal Codes contains corresponding on/off boundaries.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 53-57 (printed 36-40)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=53).

<a id="cmd51-091"></a>

## CMD51-091: Toggle underline while typing

Parent: WP51-030. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document; original font resources.

**When**

1. KEY F8
2. TYPE alpha
3. KEY F8
4. TYPE beta

**Then**

- alpha has the selected attribute and beta does not.
- Reveal Codes contains corresponding on/off boundaries.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 53-57 (printed 36-40)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=53).

<a id="cmd51-092"></a>

## CMD51-092: Apply an appearance attribute through Font

Parent: WP51-030. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document.

**When**

1. KEY Ctrl+F8
2. SELECT Appearance > Italics
3. TYPE alpha
4. Disable Italics through the same menu.
5. TYPE beta

**Then**

- Only alpha is italic; emitted code boundaries persist on save.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 54-57 (printed 37-40)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=54).

<a id="cmd51-093"></a>

## CMD51-093: Set document initial codes

Parent: WP51-032. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- New document with no text yet; copied application setup.

**When**

1. KEY Shift+F8
2. SELECT Document > Initial Codes
3. Set an allowed formatting feature through its original command.
4. KEY F7 until normal editing.
5. TYPE alpha and save.

**Then**

- Formatting lives in document initial codes without cluttering main text.
- Saved file retains the selected initial settings.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 309-311 (printed 292-294)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=309).

<a id="cmd51-094"></a>

## CMD51-094: Center a line and terminate with Enter

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at left margin on an empty line.

**When**

1. KEY Shift+F6
2. TYPE Heading
3. KEY Enter
4. TYPE Body

**Then**

- Heading is centered between margins.
- Enter ends the center alignment; Body uses normal alignment.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 82-84 (printed 65-67)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=82).

<a id="cmd51-095"></a>

## CMD51-095: End centering without ending the line

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Centered text Heading on current line.

**When**

1. KEY Shift+F8
2. SELECT Other > End Centering/Alignment
3. TYPE tail

**Then**

- An End C/A code terminates centering without inserting a hard return.
- tail is not governed by the preceding center code.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 82-84 (printed 65-67)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=82).

<a id="cmd51-096"></a>

## CMD51-096: Flush right until Enter

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at empty line left margin.

**When**

1. KEY Alt+F6
2. TYPE RIGHT
3. KEY Enter
4. TYPE Body

**Then**

- RIGHT ends at the right margin.
- Following line resumes normal alignment.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 220-222 (printed 203-205)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=220).

<a id="cmd51-097"></a>

## CMD51-097: Use paragraph left indent

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank paragraph; declared tab settings; enough text to wrap.

**When**

1. KEY F4
2. TYPE a wrapping paragraph.
3. KEY Enter
4. TYPE Normal

**Then**

- Wrapped lines remain indented to the next tab stop.
- Hard return terminates the indent for Normal.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 302-303 (printed 285-286)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=302).

<a id="cmd51-098"></a>

## CMD51-098: Use equal double indent

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank paragraph with declared tab stops.

**When**

1. KEY Shift+F4
2. TYPE a wrapping paragraph.
3. KEY Enter

**Then**

- Paragraph is indented from both margins by the documented equal distance.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 303-303 (printed 286-286)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=303).

<a id="cmd51-099"></a>

## CMD51-099: Create hanging indent

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at paragraph beginning with declared tab stops.

**When**

1. KEY F4
2. KEY Shift+Tab
3. TYPE a wrapping paragraph.
4. KEY Enter

**Then**

- First line remains at the margin; subsequent lines follow the indent stop.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 303-303 (printed 286-286)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=303).

<a id="cmd51-100"></a>

## CMD51-100: Choose full paragraph justification

Parent: WP51-034. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at beginning of a line with wrapping text after it.

**When**

1. KEY Shift+F8
2. SELECT Line > Justification > Full
3. KEY F7 until editing.

**Then**

- Text after the justification code aligns at both margins.
- Earlier text retains its prior setting.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 316-319 (printed 299-302)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=316).

<a id="cmd51-101"></a>

## CMD51-101: Insert a normal tab

Parent: WP51-035. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank line with known left tab settings.

**When**

1. KEY Tab
2. TYPE item

**Then**

- Left Tab code is inserted and item begins at the next tab stop.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 648-649 (printed 631-632)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=648).

<a id="cmd51-102"></a>

## CMD51-102: Align decimal values

Parent: WP51-035. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Two lines with identical tab stops and decimal alignment character period.

**When**

1. On first line KEY Ctrl+F6; TYPE 12.34; KEY Enter.
2. On next line KEY Ctrl+F6; TYPE 5.67.

**Then**

- Decimal points align at the selected stop despite different integer widths.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 650-651 (printed 633-634)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=650).

<a id="cmd51-103"></a>

## CMD51-103: Change tab settings at the cursor

Parent: WP51-035. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Paragraph before cursor uses existing tabs; paragraph after will use new settings.

**When**

1. KEY Shift+F8
2. SELECT Line > Tab Set
3. Set one explicit left stop at a declared measurement.
4. KEY F7 until editing; KEY Tab; TYPE item.

**Then**

- Tab Set code changes subsequent tab behavior only.
- Capture absolute/relative tab mode and actual stop value.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 651-656 (printed 634-639)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=651).

<a id="cmd51-104"></a>

## CMD51-104: Set fixed line height

Parent: WP51-036. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Paragraph using declared font and geometry.

**When**

1. KEY Shift+F8
2. SELECT Line > Line Height > Fixed
3. TYPE 0.2 inches then KEY Enter
4. KEY F7 to return.

**Then**

- Subsequent line baselines use fixed line height rather than font-derived auto height.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 358-360 (printed 341-343)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=358).

<a id="cmd51-105"></a>

## CMD51-105: Set double line spacing

Parent: WP51-036. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Two consecutive paragraphs with a cursor between them.

**When**

1. KEY Shift+F8
2. SELECT Line > Line Spacing
3. TYPE 2 then KEY Enter
4. KEY F7 to return.

**Then**

- A line-spacing code affects subsequent text; preceding paragraph remains unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 363-363 (printed 346-346)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=363).

<a id="cmd51-106"></a>

## CMD51-106: Enable line numbering

Parent: WP51-036. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor where numbering should begin.

**When**

1. KEY Shift+F8
2. SELECT Line > Line Numbering
3. TYPE y and accept the declared numbering options.
4. KEY F7 until editing; print/view document.

**Then**

- Numbering begins at the declared position and follows configured numbering rules.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 361-362 (printed 344-345)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=361).

<a id="cmd51-107"></a>

## CMD51-107: Advance relative and absolute positions

Parent: WP51-038. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor on a page with declared geometry; no graphics wrapping constraint.

**When**

1. KEY Shift+F8
2. SELECT Other > Advance > Position
3. Enter a declared absolute horizontal location.
4. Return and TYPE A.
5. Repeat Advance with a declared relative Right distance; TYPE B.

**Then**

- A uses an absolute page position; B uses the relative displacement.
- Advance is represented in document geometry rather than terminal-cell count.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 48-51 (printed 31-34)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=48).

<a id="cmd51-108"></a>

## CMD51-108: Do not advance beyond the current page

Parent: WP51-038. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor near the bottom of a page.

**When**

1. KEY Shift+F8
2. SELECT Other > Advance > Down
3. Enter a distance that would pass the current page break.

**Then**

- Advance cannot move the cursor past a page break; capture the original boundary response.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 49-49 (printed 32-32)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=49).

<a id="cmd51-109"></a>

## CMD51-109: Enable hyphenation at the cursor

Parent: WP51-039. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Known long-word fixture and declared language/hyphenation resource.

**When**

1. KEY Shift+F8
2. SELECT Line > Hyphenation
3. TYPE y
4. KEY F7 until editing.
5. Type/reflow the long-word fixture.

**Then**

- Hyphenation begins after the inserted control; language-dependent suggestions use declared resources.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 294-297 (printed 277-280)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=294).

<a id="cmd51-110"></a>

## CMD51-110: Insert a nonbreaking hard space

Parent: WP51-016. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha; cursor immediately after a.

**When**

1. KEY Home, Space
2. TYPE beta
3. Reflow near a right margin.

**Then**

- A Hard Space code joins alpha and beta so normal wrapping does not separate them.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 286-286 (printed 269-269)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=286).

<a id="cmd51-111"></a>

## CMD51-111: Hard return ends a paragraph

Parent: WP51-016. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text wraps across multiple visual lines.

**When**

1. KEY Enter at a declared insertion point.
2. Inspect Reveal Codes.

**Then**

- Enter inserts a Hard Return distinct from computed soft line wraps.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 574-577 (printed 557-560)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=574).

<a id="cmd51-112"></a>

## CMD51-112: Insert a hard page break

Parent: WP51-040. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor between two text segments on the first page.

**When**

1. KEY Ctrl+Enter

**Then**

- A Hard Page code forces following content onto the next page.
- Changing preceding text does not remove the explicit page boundary.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 488-490 (printed 471-473)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=488).

<a id="cmd51-113"></a>

## CMD51-113: Keep a declared number of lines together

Parent: WP51-040. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor just before a heading and two following lines near the page bottom.

**When**

1. KEY Shift+F8
2. SELECT Page > Conditional End of Page
3. TYPE 3 then KEY Enter
4. KEY F7 to return; reflow.

**Then**

- A Conditional EOP code protects the declared line count and inserts a soft page break before it if needed.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 105-106 (printed 88-89)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=105).

<a id="cmd51-114"></a>

## CMD51-114: Apply and reset binding offset

Parent: WP51-091. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Multi-page document with controlled logical page numbering and declared printer.

**When**

1. KEY Shift+F7
2. SELECT Binding Offset
3. Enter 0.25 inches.
4. KEY F7; print/view output.
5. Reopen Binding Offset and enter zero.

**Then**

- Nonzero offset follows logical odd/even pages, including labels.
- Setting zero restores the unshifted document geometry; setting is saved with document without a normal body binding code.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 63-65 (printed 46-48)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=63).

<a id="cmd51-115"></a>

## CMD51-115: Create a footnote

Parent: WP51-045. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at a reference point in main text outside columns or notes.

**When**

1. KEY Ctrl+F7
2. SELECT Footnote > Create
3. TYPE Note text
4. KEY F7

**Then**

- A numbered note and its text are created; editor returns to the main document.
- Note content/code structure survives save/retrieve.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 226-228 (printed 209-211)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=226).

<a id="cmd51-116"></a>

## CMD51-116: Create an endnote

Parent: WP51-045. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at a main-text reference point; declared generation settings.

**When**

1. KEY Ctrl+F7
2. SELECT Endnote > Create
3. TYPE End note text
4. KEY F7
5. Run Generate when required by the selected placement.

**Then**

- Endnote reference and text are retained and positioned according to original generation rules.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 226-231 (printed 209-214)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=226).

<a id="cmd51-117"></a>

## CMD51-117: Configure note continuation constraints

Parent: WP51-045. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document has a note longer than available page space.

**When**

1. KEY Ctrl+F7
2. SELECT Footnote > Options
3. Set the declared amount of note text to keep together.
4. KEY F7 to return; print/view output.

**Then**

- Continuation and kept-together note text follow the selected option under fixed resources.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 232-233 (printed 215-216)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=232).

<a id="cmd51-118"></a>

## CMD51-118: Create and apply a named style

Parent: WP51-046. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document; style name WPTEST is unused.

**When**

1. KEY Alt+F8
2. SELECT Create
3. Set Name to WPTEST and configure its type and formatting codes.
4. KEY F7 to return to Styles.
5. SELECT On
6. TYPE Styled text and save.

**Then**

- WPTEST applies its declared codes and is saved with the document.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 638-642 (printed 621-625)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=638).

<a id="cmd51-119"></a>

## CMD51-119: Reject a duplicate style name ignoring case

Parent: WP51-046. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Style WPTEST already exists.

**When**

1. KEY Alt+F8
2. SELECT Create
3. Set Name to wptest.

**Then**

- Duplicate name is rejected; user is allowed to enter another name.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 638-638 (printed 621-621)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=638).

<a id="cmd51-120"></a>

## CMD51-120: Create a 2 by 2 table

Parent: WP51-048. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at left margin on an empty line.

**When**

1. KEY Alt+F7
2. SELECT Tables > Create
3. Enter 2 columns and 2 rows.

**Then**

- A 2-column, 2-row table is created and Table Edit mode becomes active.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 657-660 (printed 640-643)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=657).

<a id="cmd51-121"></a>

## CMD51-121: Join selected table cells

Parent: WP51-048. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Table Edit active in a 2 by 2 table with controlled cell text.

**When**

1. SELECT Join
2. Select the documented target span and confirm with the shown choices.

**Then**

- Selected cells join according to the original structural rules.
- Native spans and content placement are captured; unrelated cells survive.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 668-681 (printed 651-664)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=668).

<a id="cmd51-122"></a>

## CMD51-122: Recalculate table formulas explicitly

Parent: WP51-049. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Table cells A1=2, B1=3, and a formula cell references their sum; result initially 5.

**When**

1. Change A1 to 7.
2. KEY Alt+F7 from inside the table.
3. SELECT Math > Calculate

**Then**

- Formula recalculates to 10.
- The last calculated result governs displayed and printed output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 688-688 (printed 671-671)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=688).

<a id="cmd51-123"></a>

## CMD51-123: Copy a formula to another cell

Parent: WP51-049. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Table has a declared valid formula and an empty destination cell.

**When**

1. Open Table Edit with source formula cell active.
2. SELECT Math > Copy Formula > Cell
3. Move to destination and KEY Enter.

**Then**

- Destination receives the original copy operation semantics; capture relative/absolute reference adjustments.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 688-689 (printed 671-672)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=688).

<a id="cmd51-124"></a>

## CMD51-124: Mark a contents heading at a declared level

Parent: WP51-050. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Heading text Overview is selected.

**When**

1. KEY Alt+F5
2. SELECT ToC
3. Enter level 1.

**Then**

- Selected text is marked for contents level 1.
- Capture exact original accelerator for ToC; the OCR glyph is ambiguous and is not encoded as a guessed numeric key.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 702-702 (printed 685-685)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=702).

<a id="cmd51-125"></a>

## CMD51-125: Generate or decline replacing generated material

Parent: WP51-050. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document has marked headings and an existing generated contents/index location.

**When**

1. KEY Alt+F5
2. SELECT Generate > Generate Tables, Indexes, Cross-References, etc.
3. TYPE n
4. Repeat command and TYPE y.

**Then**

- Decline leaves existing generated material unchanged.
- Approval regenerates defined material and updates cross-references/endnote placement.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 238-238 (printed 221-221)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=238).

<a id="cmd51-126"></a>

## CMD51-126: Insert a subdocument link

Parent: WP51-052. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Master document cursor at declared insertion point; scratch subdocument exists.

**When**

1. KEY Alt+F5
2. SELECT Subdocument
3. Enter scratch subdocument filename.

**Then**

- A link is inserted; a hard page break is not automatically added for the subdocument.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 414-417 (printed 397-400)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=414).

<a id="cmd51-127"></a>

## CMD51-127: Insert literal current date

Parent: WP51-054. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Controlled system date; blank document.

**When**

1. KEY Shift+F5
2. SELECT Date Text

**Then**

- Current date is inserted as literal text in the selected format.
- Retrieval on a different day does not change that literal date.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 126-129 (printed 109-112)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=126).

<a id="cmd51-128"></a>

## CMD51-128: Insert a date code that updates on retrieval

Parent: WP51-054. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Controlled system date D1; blank document.

**When**

1. KEY Shift+F5
2. SELECT Date Code
3. Save; change controlled clock to D2; retrieve file.

**Then**

- Date code displays D2 after retrieval rather than retaining D1 as literal text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 127-127 (printed 110-110)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=127).

<a id="cmd51-129"></a>

## CMD51-129: Mark reference and target together

Parent: WP51-089. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document has a reference insertion point and a later target paragraph.

**When**

1. KEY Alt+F5
2. SELECT Cross-Ref > Mark Both Reference and Target
3. Choose Page reference type.
4. Move to just after the target; KEY Enter.
5. Enter unique target name TARGET1.
6. Run Generate and approve replacement.

**Then**

- Reference uses target page number.
- Named reference/target codes survive save and regeneration.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 115-116 (printed 98-99)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=115).

<a id="cmd51-130"></a>

## CMD51-130: Mark a target separately with case-insensitive name matching

Parent: WP51-089. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Page reference already names TARGET1; target lies on a later page.

**When**

1. Move just after the target.
2. KEY Alt+F5
3. SELECT Cross-Ref > Mark Target
4. Enter target1.
5. Run Generate and approve.

**Then**

- Different case still resolves the target name.
- Reference uses the generated location of that target.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 116-120 (printed 99-103)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=116).

<a id="cmd51-131"></a>

## CMD51-131: Record and execute a named macro

Parent: WP51-059. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Scratch macro directory; TESTMAC does not exist; blank document.

**When**

1. KEY Ctrl+F10
2. Enter TESTMAC and a description.
3. TYPE ABC
4. KEY Ctrl+F10
5. KEY Alt+F10
6. Enter TESTMAC.

**Then**

- Recording stops on the second Ctrl+F10.
- Execution inserts ABC again; native TESTMAC.WPM exists in the configured directory.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 390-396 (printed 373-379)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=390).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-132"></a>

## CMD51-132: Repeat a macro using Repeat Value

Parent: WP51-059. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- TESTMAC inserts ABC; fresh blank document.

**When**

1. KEY Esc
2. TYPE 3
3. KEY Alt+F10
4. Enter TESTMAC.

**Then**

- Macro executes three times, inserting ABCABCABC.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 396-396 (printed 379-379)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=396).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-133"></a>

## CMD51-133: Stop a running macro

Parent: WP51-059. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Controlled macro with a long or waiting operation.

**When**

1. KEY Alt+F10
2. Enter macro filename.
3. KEY F1 while macro runs.

**Then**

- Original default cancellation stops the macro.
- Capture behavior separately for macros that explicitly override cancellation handling.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 396-396 (printed 379-379)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=396).

<a id="cmd51-134"></a>

## CMD51-134: Merge original primary and secondary files

Parent: WP51-062. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Authored scratch primary and secondary fixtures with two records and declared native fields.

**When**

1. KEY Ctrl+F9
2. SELECT Merge
3. Enter primary filename.
4. Enter secondary filename.

**Then**

- Output substitutes the two records using original merge semantics and preserves original file formats.
- Do not assume modern CSV field or line-ending rules.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 437-450 (printed 420-433)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=437).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-135"></a>

## CMD51-135: Sort original records by a declared key

Parent: WP51-063. Requirements: FR-013.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Two original records with first-field values Zebra and Amber; simple ascending key.

**When**

1. KEY Ctrl+F9
2. SELECT Sort
3. Set input, record type and key to the first field/word as declared.
4. SELECT Perform Action

**Then**

- Amber record precedes Zebra; original record field boundaries remain intact.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 594-601 (printed 577-584)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=594).

<a id="cmd51-136"></a>

## CMD51-136: Import a declared spreadsheet range

Parent: WP51-065. Requirements: FR-013.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Supported original-format worksheet fixture with a 2 by 2 range.

**When**

1. KEY Ctrl+F5
2. SELECT Spreadsheet > Import
3. Set filename, exact range and output type Table.
4. SELECT Perform Import

**Then**

- Only the declared range is imported with original value/format semantics; source worksheet is unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 624-628 (printed 607-611)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=624).

<a id="cmd51-137"></a>

## CMD51-137: Create a spreadsheet link

Parent: WP51-065. Requirements: FR-013.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Supported worksheet fixture and recorded range; writable scratch document.

**When**

1. KEY Ctrl+F5
2. SELECT Spreadsheet > Create Link
3. Set filename, range and output type.
4. Perform the original link-creation action.

**Then**

- A link rather than a disconnected plain-text import is retained in native document data.
- Capture the original refresh workflow and stored path/range references.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 624-632 (printed 607-615)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=624).

<a id="cmd51-138"></a>

## CMD51-138: Compose a character by WP set and character number

Parent: WP51-066. Requirements: FR-014.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document; original character resources.

**When**

1. KEY Ctrl+V
2. TYPE 1,36 then KEY Enter if requested by the active input editor.

**Then**

- The WP character identified by set 1, number 36 is inserted.
- Native character identity survives save/retrieve; terminal Unicode rendering is not the stored format.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 101-102 (printed 84-85)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=101).

<a id="cmd51-139"></a>

## CMD51-139: Count words through the Speller menu

Parent: WP51-068. Requirements: FR-014.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document text one two three; Block off and declared language resources.

**When**

1. KEY Ctrl+F2
2. SELECT Count
3. Press a key to dismiss the count; KEY F7.

**Then**

- Word count is 3 for this plain-text fixture.
- The original document text remains unchanged.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 616-616 (printed 599-599)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=616).

<a id="cmd51-140"></a>

## CMD51-140: Count option is unavailable for an active block

Parent: WP51-068. Requirements: FR-014.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text one two three; block selects one two.

**When**

1. KEY Ctrl+F2
2. Inspect Count availability.

**Then**

- Normal Word Count option is unavailable with Block on.
- Block word counting instead belongs to spell-checking the selection.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 616-616 (printed 599-599)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=616).

<a id="cmd51-141"></a>

## CMD51-141: Cancel spell-checking

Parent: WP51-068. Requirements: FR-014.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document contains a declared misspelled word; matching original dictionary loaded.

**When**

1. KEY Ctrl+F2
2. Start the original document spell-check action.
3. KEY F1
4. KEY F7

**Then**

- Spell-check stops and returns to document without applying an unapproved correction.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 605-606 (printed 588-589)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=605).

<a id="cmd51-142"></a>

## CMD51-142: Draw a single line

Parent: WP51-017. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank fixed-pitch document; cursor at a declared start cell.

**When**

1. KEY Ctrl+F3
2. SELECT Line Draw
3. TYPE 1
4. KEY Right four times
5. KEY F7

**Then**

- A single-line drawing is inserted along the traversed cells.
- Ending drawing returns to normal editing with original character identities retained.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 354-355 (printed 337-338)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=354).

<a id="cmd51-143"></a>

## CMD51-143: Draw a double line

Parent: WP51-017. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank fixed-pitch document; cursor at a declared start cell.

**When**

1. KEY Ctrl+F3
2. SELECT Line Draw
3. TYPE 2
4. KEY Right four times
5. KEY F7

**Then**

- Double-line characters are produced rather than single-line or ASCII substitutions.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 354-355 (printed 337-338)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=354).

<a id="cmd51-144"></a>

## CMD51-144: Rewrite the editing display

Parent: WP51-018. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document with known content/layout; automatic-formatting setting recorded.

**When**

1. KEY Ctrl+F3
2. SELECT Rewrite

**Then**

- Screen is rewritten according to original automatic-format settings.
- This display command does not itself insert text.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 580-580 (printed 563-563)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=580).

<a id="cmd51-145"></a>

## CMD51-145: Direct original printer output to a disk file

Parent: WP51-074. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared original printer selected; scratch capture file does not exist.

**When**

1. KEY Shift+F7
2. SELECT Select Printer
3. Highlight printer and SELECT Edit > Port > Other
4. Enter scratch print filename.
5. KEY F7 twice
6. Print through the ordinary document command.

**Then**

- Captured file contains original printer-language data, not a PDF or converted document container.
- Printer profile and complete captured bytes are saved as reference evidence.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 560-560 (printed 543-543)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=560).

<a id="cmd51-146"></a>

## CMD51-146: Preview each original page-view mode

Parent: WP51-076. Requirements: FR-016.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Three-page document under declared printer resources.

**When**

1. KEY Shift+F7
2. SELECT View Document
3. Select 100%, 200%, Full Page and Facing Pages in separate clean runs.

**Then**

- Modes expose the same document pages at the selected views.
- Facing Pages uses even pages on the left and odd on the right; page 1 has no preceding mate unless page 0 exists.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 718-721 (printed 701-704)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=718).

<a id="cmd51-147"></a>

## CMD51-147: Changing preview colors does not change printed content

Parent: WP51-076. Requirements: FR-016.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Preview open with declared printer and page fixture.

**When**

1. KEY Shift+F3
2. Exit preview and print to the original disk-capture destination.

**Then**

- Foreground/background change affects preview presentation only.
- Printed content/layout is unaffected.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 719-719 (printed 702-702)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=719).

<a id="cmd51-148"></a>

## CMD51-148: Choose a declared sheet feeder

Parent: WP51-075. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Original printer resource includes named feeder definitions.

**When**

1. KEY Shift+F7
2. SELECT Select Printer
3. Highlight printer and SELECT Edit > Sheet Feeder
4. Highlight declared feeder and SELECT Select.

**Then**

- The selected original feeder becomes active.
- Missing resource behavior is captured explicitly rather than silently choosing a host tray.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 593-593 (printed 576-576)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=593).

<a id="cmd51-149"></a>

## CMD51-149: Preserve an untouched native file byte for byte

Parent: WP51-020. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid provenance-recorded WP 5.1 input and its raw hash.

**When**

1. Open and save in Wordling without edits.
2. Compare exact bytes and SHA-256 with input.
3. Retrieve result in the reference WP app.

**Then**

- Wordling no-edit output is byte-identical.
- Reference retrieval succeeds; original WP no-edit-save byte identity is not assumed.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 582-583 (printed 565-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=582).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-009.

<a id="cmd51-150"></a>

## CMD51-150: Reject an unsafe opaque-structure edit before replacement

Parent: WP51-020. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid native file with unknown code/packet structure that cannot safely survive the proposed edit.

**When**

1. Open in Wordling and attempt the declared unsafe edit/save.
2. Compare original path bytes after refusal.

**Then**

- An explicit refusal occurs and the original file remains byte-identical.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 582-583 (printed 565-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=582).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-009.

<a id="cmd51-151"></a>

## CMD51-151: Preserve unrelated native data after a supported edit

Parent: WP51-020. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid native file contains a known text span plus unrelated prefix packets and embedded structures.

**When**

1. Edit only the selected supported text span in Wordling.
2. Save to a new file.
3. Open, inspect and print in original WP.

**Then**

- Only intended semantic changes and required pointer/length updates occur.
- Unrelated data and original-app behavior remain intact.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 582-583 (printed 565-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=582).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-009.

<a id="cmd51-152"></a>

## CMD51-152: Retain original after a failed save

Parent: WP51-020. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Original native file has recorded bytes; test injects short-write, permission or replacement failure.

**When**

1. Attempt save in Wordling with one declared failure injected.
2. Inspect original bytes and reported error.

**Then**

- Failure is explicit; original path is not corrupted or falsely reported saved.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 582-583 (printed 565-566)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=582).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-009.

<a id="cmd51-153"></a>

## CMD51-153: Select and cancel text using the mouse

Parent: WP51-004. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Original supported mouse profile; text alpha beta.

**When**

1. Drag from immediately before a to immediately before the following space.
2. Cancel the block with the documented middle-button action or two-button chord for that profile.

**Then**

- alpha is selected by dragging, then the selection is cancelled.
- Text remains unchanged; terminal mouse adaptation must reproduce the same command effect.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 451-454 (printed 434-437)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=451); [REF51 PDF 67-67 (printed 50-50)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=67).

<a id="cmd51-154"></a>

## CMD51-154: Change the text display independently of print layout

Parent: WP51-005. Requirements: FR-004.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Document has bold and ordinary text; printer profile fixed.

**When**

1. KEY Shift+F1
2. SELECT Display > Colors/Fonts/Attributes
3. Change one ordinary-text display color through available choices.
4. KEY F7 until editing; print to scratch capture.

**Then**

- Editing display changes; document/print formatting does not acquire an unintended color or font change.
- Display configuration is retained in the original setup artifact.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 85-90 (printed 68-73)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=85); [REF51 PDF 139-140 (printed 122-123)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=139).

<a id="cmd51-155"></a>

## CMD51-155: Copy a selected block to another insertion point

Parent: WP51-010. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Text alpha beta; alpha selected; target is document end.

**When**

1. KEY Ctrl+F4
2. SELECT Block > Copy
3. Move to document end and KEY Enter to retrieve the copied text.

**Then**

- Source alpha remains in place and a copy appears at target.
- Capture prompt state and attribute boundaries at both locations.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 455-460 (printed 438-443)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=455).

<a id="cmd51-156"></a>

## CMD51-156: Append selected text to an existing file

Parent: WP51-010. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Selected text APPEND; scratch target contains BEGIN.

**When**

1. KEY Ctrl+F4
2. SELECT Block > Append
3. Enter target filename.

**Then**

- Selected content is appended to target end, not inserted at its beginning.
- On-screen source and original code semantics are preserved.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 51-53 (printed 34-36)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=51).

<a id="cmd51-157"></a>

## CMD51-157: Retrieve an original 4.2 document into 5.1

Parent: WP51-026. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Provenance-recorded WP 4.2 fixture contains supported formatting and extended characters.

**When**

1. KEY Shift+F10
2. Enter 4.2 fixture name.
3. Save as a distinct native 5.1 file.

**Then**

- Original conversion maps supported content according to declared character/resources.
- The original 4.2 input remains unchanged; losses/warnings require explicit captured expectations.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 147-155 (printed 130-138)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=147).

<a id="cmd51-158"></a>

## CMD51-158: Create a nonprinting document comment

Parent: WP51-027. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Main-document cursor at a known position.

**When**

1. KEY Ctrl+F5
2. SELECT Comment > Create
3. TYPE Internal note
4. KEY F7
5. Print document to declared capture.

**Then**

- Comment is retained in native document data and can be inspected.
- Comment text is absent from ordinary printed output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 141-144 (printed 124-127)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=141).

<a id="cmd51-159"></a>

## CMD51-159: Compare screen and disk document versions

Parent: WP51-027. Requirements: FR-006.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Original scratch document on disk; on-screen copy contains one insertion and one deletion.

**When**

1. KEY Alt+F5
2. SELECT Generate > Compare Screen and Disk Documents and Add Redline and Strikeout
3. Enter original disk filename.

**Then**

- Comparison adds original redline/strikeout markings for the differences.
- Disk source is not rewritten by comparison.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 144-147 (printed 127-130)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=144).

<a id="cmd51-160"></a>

## CMD51-160: Set initial base font from selected printer resources

Parent: WP51-031. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared printer has two usable portrait fonts.

**When**

1. KEY Shift+F8
2. SELECT Document > Initial Base Font
3. Highlight the declared font and SELECT Select.

**Then**

- Initial base font changes using available original resources.
- Substructure/default-font behavior is captured separately from an in-body Base Font code.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 222-225 (printed 205-208)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=222).

<a id="cmd51-161"></a>

## CMD51-161: Toggle printer kerning at cursor

Parent: WP51-031. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared printer/font supports known kerning pairs; text fixture AV AV.

**When**

1. KEY Shift+F8
2. SELECT Other > Printer Functions > Kerning
3. TYPE y
4. KEY F7 until editing; print/view.

**Then**

- Subsequent text uses selected printer kerning metrics.
- Text before the control retains its previous setting.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 320-320 (printed 303-303)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=320).

<a id="cmd51-162"></a>

## CMD51-162: Change left and right margins

Parent: WP51-033. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor before a paragraph; geometry/units fixed.

**When**

1. KEY Shift+F8
2. SELECT Line > Margins
3. Enter 1.25 inches left and 1.5 inches right.
4. KEY F7

**Then**

- A left/right margin code affects following text.
- Measurements are from page edges and do not vary with font size.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 411-412 (printed 394-395)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=411).

<a id="cmd51-163"></a>

## CMD51-163: Change top and bottom margins

Parent: WP51-033. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at a declared page boundary; geometry fixed.

**When**

1. KEY Shift+F8
2. SELECT Page > Margins
3. Enter 1 inch top and 1.25 inches bottom.
4. KEY F7

**Then**

- Original page-margin semantics and first-line baseline placement apply.
- Capture resulting page geometry and code scope.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 413-413 (printed 396-396)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=413).

<a id="cmd51-164"></a>

## CMD51-164: Set word and letter spacing independently

Parent: WP51-037. Requirements: FR-008.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared printer/font profile; same sample text printed for control and changed runs.

**When**

1. KEY Shift+F8
2. SELECT Other > Printer Functions > Word Spacing/Letter Spacing
3. Set word spacing to 120% of Optimal and letter spacing to Optimal.
4. KEY F7 until editing; print/view.

**Then**

- Word spacing increases relative to the declared optimal width while letter spacing retains its selected mode.
- Capture actual printer-dependent positions; do not calculate from terminal cells.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 725-728 (printed 708-711)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=725).

<a id="cmd51-165"></a>

## CMD51-165: Choose page-number position

Parent: WP51-041. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at top of first page; three-page document.

**When**

1. KEY Shift+F8
2. SELECT Page > Page Numbering > Page Number Position
3. Choose a declared position from the original menu.
4. KEY F7 until editing; print/view.

**Then**

- Page numbers appear at the selected original page position.
- Formatting changes do not silently replace logical page numbers with physical sheet indices.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 491-495 (printed 474-478)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=491).

<a id="cmd51-166"></a>

## CMD51-166: Choose an existing paper definition

Parent: WP51-041. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Selected original printer has a declared paper definition.

**When**

1. KEY Shift+F8
2. SELECT Page > Paper Size/Type
3. Highlight declared definition and SELECT Select.

**Then**

- Original paper dimensions, orientation and resource-specific settings govern subsequent layout.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 495-504 (printed 478-487)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=495).

<a id="cmd51-167"></a>

## CMD51-167: Enable widow/orphan protection

Parent: WP51-042. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Paragraph would otherwise leave a single isolated line at a page boundary.

**When**

1. KEY Shift+F8
2. SELECT Line > Widow/Orphan Protection
3. TYPE y
4. KEY F7; reflow.

**Then**

- Protection control applies from the cursor forward.
- The isolated-line page split is prevented according to original pagination rules.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 722-722 (printed 705-705)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=722).

<a id="cmd51-168"></a>

## CMD51-168: Define and enable newspaper columns

Parent: WP51-043. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document; known paper/margins.

**When**

1. KEY Alt+F7
2. SELECT Columns > Define
3. Set type Newspaper, two columns and declared column margins.
4. Return to Columns and SELECT On.
5. TYPE enough text to flow to second column.

**Then**

- Column definition and On controls are distinct.
- Text flows according to newspaper column semantics; enabling without a definition is not silently accepted.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 92-96 (printed 75-79)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=92).

<a id="cmd51-169"></a>

## CMD51-169: Move through parallel columns with a hard boundary

Parent: WP51-043. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared two-column parallel definition.

**When**

1. KEY Alt+F7
2. SELECT Columns > On
3. TYPE Left text
4. KEY Ctrl+Enter
5. TYPE Right text

**Then**

- Hard Page advances to the next parallel column under original column semantics.
- Column text remains in original native structure.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 96-100 (printed 79-83)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=96).

<a id="cmd51-170"></a>

## CMD51-170: Suppress title-page numbering without renumbering following pages

Parent: WP51-044. Requirements: FR-009.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Three-page document numbered from 1; cursor at top of title page.

**When**

1. KEY Shift+F8
2. SELECT Page > Suppress
3. Choose Page Number through displayed original choices.
4. KEY F7; print/view.

**Then**

- Title-page number is hidden; following pages still display 2 and 3.
- Suppression does not restart logical numbering.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 643-644 (printed 626-627)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=643).

<a id="cmd51-171"></a>

## CMD51-171: Create successive outline levels

Parent: WP51-047. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document with original outline definition.

**When**

1. KEY Shift+F5
2. SELECT Outline > On
3. KEY Enter
4. TYPE First
5. KEY Enter
6. KEY Tab
7. TYPE Child

**Then**

- First item uses first-level numbering; Tab after next item starts a second-level number.
- Outline numbering and text remain distinct native functions.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 468-472 (printed 451-455)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=468).

<a id="cmd51-172"></a>

## CMD51-172: Mark a full legal authority

Parent: WP51-051. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- A citation phrase is selected in a legal document.

**When**

1. KEY Alt+F5
2. SELECT ToA (Table of Authorities) / Mark Full
3. Enter section number 1.
4. Review/edit the captured authority text through original prompts.

**Then**

- Citation is marked in the selected authorities section.
- Exact citation-editor exit/short-form follow-up choices must be captured before automating the procedure.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 696-698 (printed 679-681)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=696).

<a id="cmd51-173"></a>

## CMD51-173: Select a label paper definition

Parent: WP51-053. Requirements: FR-010.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared printer has a label definition; cursor at top of page.

**When**

1. KEY Shift+F8
2. SELECT Page > Paper Size/Type
3. Highlight declared label definition and SELECT Select.
4. TYPE two labels using original label boundaries.

**Then**

- Labels use the definition’s logical-page geometry and count; physical-sheet behavior is retained.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 336-344 (printed 319-327)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=336).

<a id="cmd51-174"></a>

## CMD51-174: Create a figure graphics box

Parent: WP51-055. Requirements: FR-011.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch supported graphics file and declared printer/graphics resources.

**When**

1. KEY Alt+F9
2. SELECT Figure > Create
3. Set content filename and explicit width/position using Definition options.
4. KEY F7

**Then**

- A figure box references/contains original graphics content according to selected options.
- Declared placement and wrapping survive save/retrieve; a terminal placeholder alone cannot establish parity.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 249-262 (printed 232-245)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=249).

<a id="cmd51-175"></a>

## CMD51-175: Convert an original graphics file with GRAPHCNV

Parent: WP51-056. Requirements: FR-011.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch supported graphics fixture; output does not exist; original utility installed.

**When**

1. At the reference DOS prompt RUN GRAPHCNV.
2. Enter full input pathname.
3. Enter full output pathname.

**Then**

- Utility produces its documented conversion report and original output format.
- Input remains intact; capture bytes and unsupported-format error behavior separately.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 245-248 (printed 228-231)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=245).

<a id="cmd51-176"></a>

## CMD51-176: Create a horizontal graphics line

Parent: WP51-057. Requirements: FR-011.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor at a declared page position; printer fixed.

**When**

1. KEY Alt+F9
2. SELECT Line > Create Horizontal Line
3. Set length and line style from the original choices.
4. KEY F7

**Then**

- A page-geometry graphics line is created, distinct from line-drawing characters.
- Output position, length and stroke settings match the selected values.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 274-277 (printed 257-260)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=274).

<a id="cmd51-177"></a>

## CMD51-177: Create and preview an equation fraction

Parent: WP51-058. Requirements: FR-011.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Blank document; original equation resources available.

**When**

1. KEY Alt+F9
2. SELECT Equation > Create > Edit
3. TYPE {a times b} over c
4. KEY F9 to view the equation.

**Then**

- Equation displays a fraction with a times b above c.
- Stored equation expression and graphics/text print modes require separate captured output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 180-183 (printed 163-166)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=180).

<a id="cmd51-178"></a>

## CMD51-178: Macro stops on a default failed search

Parent: WP51-060. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Original-editor-authored native macro searches for ABSENT then types SHOULDNOT; input document contains no ABSENT.

**When**

1. KEY Alt+F10
2. Enter macro filename.

**Then**

- Failed search stops the macro under original default conditions; SHOULDNOT is not inserted.
- Macros with explicit search-error handling require separate command cases.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.
- The bounded probe uses the original Macro Editor and default DISPLAY OFF behavior; failed search returns directly to the document without a persistent error prompt. Interactive READY input confirms recovery.

Sources: [REF51 PDF 396-396 (printed 379-379)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=396).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-179"></a>

## CMD51-179: Convert a 4.x macro with MACROCNV

Parent: WP51-061. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch original 4.x .MAC fixture; no matching output .WPM exists.

**When**

1. At reference DOS prompt RUN MACROCNV.
2. Enter full source macro pathname at the prompt.

**Then**

- A .WPM output is produced beside the source with the same stem.
- Source remains intact; conversion report identifies unconverted parts rather than silently claiming full compatibility.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 387-389 (printed 370-372)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=387).

<a id="cmd51-180"></a>

## CMD51-180: Enter and leave original column Math mode

Parent: WP51-064. Requirements: FR-013.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared tab stops and math columns; scratch document.

**When**

1. KEY Alt+F7
2. SELECT Math > On
3. Enter original numeric/operator fixture according to declared column roles.
4. Calculate using the documented Math action.
5. KEY Alt+F7
6. SELECT Math > Off

**Then**

- Math controls delimit calculation scope; ordinary editing resumes after Math Off.
- Function/operator codes are not printed as ordinary characters; exact calculation commands remain to be decomposed.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 418-422 (printed 401-405)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=418).

<a id="cmd51-181"></a>

## CMD51-181: Set a language code at cursor

Parent: WP51-067. Requirements: FR-014.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared original resources support the selected language code.

**When**

1. KEY Shift+F8
2. SELECT Other > Language
3. Enter the declared original two-letter language code.
4. KEY F7

**Then**

- Original language-dependent formatting/spelling behavior applies after the code.
- Global application to nested text requires placing the language control in document Initial Codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 345-347 (printed 328-330)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=345).

<a id="cmd51-182"></a>

## CMD51-182: Open and cancel the Thesaurus

Parent: WP51-069. Requirements: FR-014.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Cursor on a known dictionary word with matching original thesaurus installed.

**When**

1. KEY Alt+F1
2. Inspect displayed entries.
3. Return with the original exit/cancel action without choosing a replacement.

**Then**

- Thesaurus relates to the word at the cursor.
- Without a chosen replacement, document text remains unchanged; capture exact menu action before automation.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 709-711 (printed 692-694)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=709).

<a id="cmd51-183"></a>

## CMD51-183: Print the current page

Parent: WP51-070. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Three-page document; cursor on page 2; declared print-to-disk capture.

**When**

1. KEY Shift+F7
2. SELECT Page

**Then**

- Only the current page is printed through the selected original printer driver.
- Captured bytes and selected logical page identify the output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 510-511 (printed 493-494)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=510).

<a id="cmd51-184"></a>

## CMD51-184: Print an on-disk document without retrieving it

Parent: WP51-070. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Current editor contains UNSAVED; scratch native PRINTME exists on disk.

**When**

1. KEY Shift+F7
2. SELECT Document on Disk
3. Enter PRINTME.
4. KEY Enter to print whole document.

**Then**

- PRINTME is printed without replacing current editor content.
- UNSAVED remains intact.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 507-510 (printed 490-493)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=507).

<a id="cmd51-185"></a>

## CMD51-185: Select an installed original printer definition

Parent: WP51-071. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Two original printer definitions installed and fingerprinted.

**When**

1. KEY Shift+F7
2. SELECT Select Printer
3. Highlight declared printer and SELECT Select.

**Then**

- Chosen original definition governs font availability and formatting; capture retained document resource association.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 523-526 (printed 506-509)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=523).

<a id="cmd51-186"></a>

## CMD51-186: Insert a literal printer command

Parent: WP51-072. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Declared printer-language byte sequence is harmless in a scratch capture profile.

**When**

1. KEY Shift+F8
2. SELECT Other > Printer Functions > Printer Command > Command
3. Enter the declared bytes using original input syntax.
4. Return and print to disk.

**Then**

- Original output includes the inserted command at its documented stream position.
- Document text does not gain a visible substitute for the command.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 527-528 (printed 510-511)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=527).

<a id="cmd51-187"></a>

## CMD51-187: Open and quit original Printer Program

Parent: WP51-073. Requirements: FR-015.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Copies of declared .ALL/.PRS files; immutable resources are not edited.

**When**

1. At reference DOS prompt RUN PTR.
2. Retrieve a copied resource using the utility’s original retrieval command.
3. KEY Alt+F7
4. Decline saving if prompted.

**Then**

- PTR reads its original resource format and exits through its original quit flow.
- Scratch resource bytes remain unchanged after declining save.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 535-536 (printed 518-519)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=535).

<a id="cmd51-188"></a>

## CMD51-188: Set an editing display option

Parent: WP51-077. Requirements: FR-017.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Copied setup; original Show Hard Returns option initially disabled.

**When**

1. KEY Shift+F1
2. SELECT Display > Edit-Screen Options
3. Choose Show Hard Returns and configure a declared display character.
4. KEY F7 until editing.

**Then**

- Hard-return markers appear in editing according to the option.
- Printed output does not acquire marker characters; setup persistence is tested separately.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 174-176 (printed 157-159)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=174).

<a id="cmd51-189"></a>

## CMD51-189: Run a DOS command and return to the same cursor

Parent: WP51-078. Requirements: FR-017.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Scratch document with cursor in its middle; reference DOS environment declared.

**When**

1. KEY Ctrl+F1
2. SELECT DOS Command
3. Enter a read-only command that displays the current directory.
4. Press a key to return as prompted.

**Then**

- DOS command executes without retrieving a new document or launching another WP instance.
- Editor returns to the previous cursor and content; Linux mapping is still an explicit adaptation decision.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 242-242 (printed 225-225)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=242).

<a id="cmd51-190"></a>

## CMD51-190: Choose an original cursor appearance

Parent: WP51-079. Requirements: FR-017.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Reference DOS environment with CURSOR.COM installed.

**When**

1. Exit to DOS and RUN CURSOR.
2. Choose a declared cursor shape and KEY Enter.
3. Start WP and inspect cursor.

**Then**

- Chosen cursor appearance affects DOS and WP.
- Blinking is not disabled by this utility; Linux mapping must preserve meaningful user control without pretending to execute DOS hardware calls.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 122-123 (printed 105-106)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=122).

<a id="cmd51-191"></a>

## CMD51-191: Start WP with a declared macro

Parent: WP51-080. Requirements: FR-017.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- TESTMAC.WPM exists and inserts STARTED; reference executable/overlays available.

**When**

1. RUN WP /m-TESTMAC in the reference DOS environment.

**Then**

- WP executes the selected startup macro.
- Capture original startup switch spelling and resource resolution; filename bytes are not guessed from a Linux path.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 916-916 (printed 899-899)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=916).

<a id="cmd51-192"></a>

## CMD51-192: Investigate shared-file access with separate user setups

Parent: WP51-081. Requirements: FR-017.
Basis: **oracle-investigation**. Readiness: investigation. Oracle: **not-run**.

**Given**

- Two reference users with separate personal setups share a scratch document directory; rights and file hashes declared.

**When**

1. User A retrieves a scratch file.
2. User B attempts to retrieve and then save that same path.
3. Capture displayed access/lock decisions and source bytes at each step; do not overwrite the immutable master fixture.

**Then**

- Original network-directory and personal-setup separation must be maintained.
- The exact lock/conflict policy is unresolved until section-specific study and oracle capture; this is an investigation, not an executable acceptance assertion.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.
- Resolve exact sharing/locking behavior and Linux mapping before this can become an acceptance-ready case.

Sources: [REF51 PDF 948-953 (printed 931-936)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=948).

<a id="cmd51-193"></a>

## CMD51-193: Check the original keyboard rather than the alternate profile

Parent: WP51-082. Requirements: FR-017.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Copied setup selects Original; no custom keyboard definitions active.

**When**

1. Use F3 at normal editing and return from Help.
2. Delete scratch text and invoke F1.

**Then**

- Original F3 opens Help and F1 opens the deletion-restoration workflow.
- Alternate/custom keyboard behavior must not be treated as the default.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [REF51 PDF 782-793 (printed 765-776)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=782).

<a id="cmd51-194"></a>

## CMD51-194: Read native prefix fields before original-app retrieval

Parent: FMT51-001. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Original unencrypted 5.1 native fixture with known document offset.

**When**

1. Inspect the first 16 bytes using an independent binary inspector.
2. Parse using Wordling’s future reader and compare fields.
3. Retrieve fixture in reference WP.

**Then**

- Identifier is FF 57 50 43; product 1, document type 0A, stored major/minor 00/01.
- Document offset and byte-reversed integer interpretation agree; native product name 5.2 is never substituted.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [SDK51 PDF 16-19 (printed 3-6)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=16).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-007.

<a id="cmd51-195"></a>

## CMD51-195: Traverse and preserve prefix packet chains

Parent: FMT51-002. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid fixture has multiple prefix index blocks and data packets.

**When**

1. Inspect all index pointers/lengths independently.
2. Open/save untouched in Wordling and compare bytes.
3. Retrieve result in original WP.

**Then**

- Packet relationships and bytes survive unchanged; FC-002 is a Wordling guarantee rather than an assertion about original WP normalization.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [SDK51 PDF 20-29 (printed 7-16)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=20).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-007.

<a id="cmd51-196"></a>

## CMD51-196: Parse nested function text without flattening it

Parent: FMT51-003. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid native fixture has formatting functions inside footnote/text-box text.

**When**

1. Parse framed functions recursively using Wordling’s future reader.
2. Edit an unrelated supported span; save to a new file.
3. Retrieve and inspect nested content in original WP.

**Then**

- Nested text retains function structure, not just literal bytes treated as text.
- Unknown frames remain preserved or the unsafe edit is refused before replacement.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [SDK51 PDF 30-31 (printed 17-18)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=30).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-007.

<a id="cmd51-197"></a>

## CMD51-197: Distinguish native hard/soft returns and pages

Parent: FMT51-004. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid fixture contains all four native boundary classes.

**When**

1. Inspect original bytes and compare reader classification.
2. Use Reveal Codes in original WP to confirm represented boundaries.

**Then**

- Native control values 0A/0D distinguish hard/soft returns and 0B/0C distinguish soft/hard pages.
- They must not be converted to a single newline class.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [SDK51 PDF 32-36 (printed 19-23)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=32).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-007.

<a id="cmd51-198"></a>

## CMD51-198: Keep table and graphics function groups distinct

Parent: FMT51-005. Requirements: FR-002.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Valid original document contains table structures and a graphics box.

**When**

1. Inspect framed group identities using SDK and an independent binary inspector.
2. Retrieve file and inspect both structures in original WP.
3. Round-trip through future Wordling codec.

**Then**

- Original table and box representations remain semantically distinct and survive save; exact subfunction coverage requires further decomposition.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [SDK51 PDF 87-101 (printed 74-88)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=87).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-007.

<a id="cmd51-199"></a>

## CMD51-199: Round-trip an original WPM macro

Parent: FMT51-006. Requirements: FR-003, FR-012.
Basis: **project-contract**. Readiness: documentary-draft. Oracle: **not-run**.

**Given**

- Macro TESTMAC.WPM was recorded by the reference application.

**When**

1. Inspect macro-specific prefix and commands under SDK rules.
2. Read/save untouched through future Wordling macro support.
3. Execute output in reference WP using Alt+F10 and TESTMAC.

**Then**

- Original macro format, command boundaries and behavior survive; a document-format wrapper is not substituted.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Capture exact wording, cursor/code positions and output bytes from the fingerprinted original; do not treat manual expectations as executed evidence.

Sources: [SDK51 PDF 105-112 (printed 92-99)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=105).

Project policy: [compatibility contract](../compatibility.md), docs/compatibility.md:FC-001..FC-007.

<a id="cmd51-200"></a>

## CMD51-200: Delete at a paired bold-code boundary

Parent: WP51-011, WP51-013. Requirements: FR-005.
Basis: **oracle-investigation**. Readiness: investigation. Oracle: **partially-observed**.

**Given**

- Fresh document A, bold B, plain C; Reveal Codes on.

**When**

1. Place cursor immediately on the opening BOLD code.
2. KEY Delete

**Then**

- Observe whether paired attribute codes are removed together while A, B and C survive.
- Capture confirmation behavior, Reveal Codes, and original native output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- This bounded paired-bold experiment does not establish behavior for every paired code or Undelete.

Sources: [REF51 PDF 129-130 (printed 112-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=129).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-201"></a>

## CMD51-201: Backspace at a paired bold-code boundary

Parent: WP51-011, WP51-013. Requirements: FR-005.
Basis: **oracle-investigation**. Readiness: investigation. Oracle: **partially-observed**.

**Given**

- Fresh document A, bold B, plain C; Reveal Codes on.

**When**

1. Place cursor immediately after the closing bold code.
2. KEY Backspace

**Then**

- Observe whether paired attribute codes are removed together while A, B and C survive.
- Capture confirmation behavior, Reveal Codes, and original native output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- This bounded paired-bold experiment does not establish behavior for every paired code or Undelete.

Sources: [REF51 PDF 129-130 (printed 112-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=129).

Observed scope: Bounded original-app recipe repeated from fresh copies, with clean WP exits and native-file evidence. Only the selected code, overwrite, macro or two-record merge branch is observed; full scenario and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-extended-03](reference-runs/2026-10-29-extended-03/run.json), [2026-10-29-extended-04](reference-runs/2026-10-29-extended-04/run.json).

<a id="cmd51-202"></a>

## CMD51-202: Delete a block containing only Bold On

Parent: WP51-009, WP51-011, WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- A[BOLD]BC[bold]D with Reveal Codes; select only the opening bold code.

**When**

1. KEY Alt+F4 then Right to select only Bold On.
2. KEY Backspace; confirm Delete Block.

**Then**

- The original repairs the formatting pair; ABCD and the bold BC span remain.
- Compare native document bodies and record every prefix difference.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.
- Packet 6 bit 3 means the document must be formatted. Preserve and record this original prefix-state transition while checking restored/repaired document-body bytes.

Sources: [REF51 PDF 130-130 (printed 113-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=130); [SDK51 PDF 24-24 (printed 11-11)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=24).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-203"></a>

## CMD51-203: Delete a block containing only Bold Off

Parent: WP51-009, WP51-011, WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- A[BOLD]BC[bold]D with Reveal Codes; select only the closing bold code.

**When**

1. KEY Alt+F4 then Right to select only Bold Off.
2. KEY Backspace; confirm Delete Block.

**Then**

- The original repairs the formatting pair; ABCD and the bold BC span remain.
- Compare native document bodies and record every prefix difference.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.
- Packet 6 bit 3 means the document must be formatted. Preserve and record this original prefix-state transition while checking restored/repaired document-body bytes.

Sources: [REF51 PDF 130-130 (printed 113-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=130); [SDK51 PDF 24-24 (printed 11-11)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=24).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-204"></a>

## CMD51-204: Undelete an entire blocked bold span

Parent: WP51-009, WP51-011, WP51-013. Requirements: FR-005.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- A[BOLD]BC[bold]D; select both codes and BC.

**When**

1. Delete selected block and confirm.
2. Capture AD and native output.
3. KEY F1; SELECT Restore.

**Then**

- Both BC and its paired bold codes return.
- Compare against character deletion separately; native prefix differences remain recorded.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.
- Packet 6 bit 3 means the document must be formatted. Preserve and record this original prefix-state transition while checking restored/repaired document-body bytes.

Sources: [REF51 PDF 130-130 (printed 113-113)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=130); [REF51 PDF 714-714 (printed 697-697)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=714); [SDK51 PDF 24-24 (printed 11-11)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=24).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-205"></a>

## CMD51-205: Macro IF ELSE and GO LABEL control flow

Parent: WP51-059, WP51-060. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Author a new native WPM in the original Macro Editor.

**When**

1. Insert IF 1, TRUE, ELSE BAD, END IF.
2. Insert IF 0, BAD, ELSE FALSE, END IF.
3. Insert GO DONE, SKIP, LABEL DONE, TAIL.
4. Save with F7 and execute using Alt+F10.

**Then**

- Exactly TRUEFALSETAIL is inserted.
- BAD and SKIP are absent; retain authored native macro and output.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.

Sources: [REF51 PDF 398-398 (printed 381-381)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=398); [REF51 PDF 400-400 (printed 383-383)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=400); [REF51 PDF 401-401 (printed 384-384)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=401); [REF51 PDF 839-839 (printed 822-822)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=839); [REF51 PDF 840-840 (printed 823-823)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=840); [REF51 PDF 841-841 (printed 824-824)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=841).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-206"></a>

## CMD51-206: Handle a macro failed search with ON NOT FOUND

Parent: WP51-059, WP51-060. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Empty document; macro explicitly installs ON NOT FOUND GO MISS before searching ABSENT.

**When**

1. Execute macro: BEFORE, Search ABSENT, SHOULDNOT, QUIT, LABEL MISS, HANDLED.
2. Terminate nested GO and handler actions with the documented two tildes.

**Then**

- Result is BEFOREHANDLED; the failed search reaches its handler and skips SHOULDNOT.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.

Sources: [REF51 PDF 860-860 (printed 843-843)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=860); [REF51 PDF 863-863 (printed 846-846)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=863); [REF51 PDF 864-864 (printed 847-847)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=864).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-207"></a>

## CMD51-207: Default merge inserts a page break between records

Parent: WP51-062. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Two native secondary records Alice and Bob. Primary Hello FIELD 1 plus hard return, with no explicit hard page.

**When**

1. Merge primary and secondary.
2. Capture final page status and native Reveal Codes.

**Then**

- Alice and Bob are on separate pages, with final page 2.
- Retain all native inputs and output; count document-body hard-page codes.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.

Sources: [REF51 PDF 437-437 (printed 420-420)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=437); [REF51 PDF 440-440 (printed 423-423)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=440); [REF51 PDF 864-864 (printed 847-847)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=864); [SDK51 PDF 30-31 (printed 17-18)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=30); [SDK51 PDF 68-68 (printed 55-55)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=68).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-208"></a>

## CMD51-208: PAGE OFF suppresses automatic merge page breaks

Parent: WP51-062. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Same two native records; primary starts with PAGE OFF and has a hard return after Hello FIELD 1.

**When**

1. Merge primary and secondary.
2. Capture final page status and native Reveal Codes.

**Then**

- Both records fit on page 1; automatic separating hard-page codes are suppressed.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.

Sources: [REF51 PDF 864-864 (printed 847-847)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=864); [REF51 PDF 865-865 (printed 848-848)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=865); [SDK51 PDF 30-31 (printed 17-18)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=30); [SDK51 PDF 68-68 (printed 55-55)](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=68).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-209"></a>

## CMD51-209: Merge IF BLANK and ELSE select per-record output

Parent: WP51-062. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Native secondary records: Alice with YES in field 2; Bob with empty field 2.

**When**

1. Create primary IF BLANK field 2, EMPTY, ELSE FILLED, END IF, space, FIELD 1.
2. Merge and retain primary, secondary and output.

**Then**

- Output selects FILLED Alice and EMPTY Bob, in order.
- Opposite branches and unresolved conditional commands are absent.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.

Sources: [REF51 PDF 841-841 (printed 824-824)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=841); [REF51 PDF 842-842 (printed 825-825)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=842).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).

<a id="cmd51-210"></a>

## CMD51-210: ON ERROR handles a missing nested macro

Parent: WP51-059, WP51-060. Requirements: FR-012.
Basis: **manual-derived**. Readiness: documentary-draft. Oracle: **partially-observed**.

**Given**

- Macro installs ON ERROR GO ERR; C:\OUT\MISSING.WPM is absent.

**When**

1. Execute NEST C:\OUT\MISSING followed by SHOULDNOT and QUIT.
2. Handler LABEL ERR inserts HANDLED.

**Then**

- Missing nested-file error reaches handler, producing HANDLED.
- SHOULDNOT is not inserted; preserve native macro source and result.

**Capture / unresolved details**

- Screen and status/prompt states after each step
- Reveal Codes and native document before/after when document content changes
- Bounded fixture only; compare against the fingerprinted original and retain all prompt, native-body and prefix differences. Full command-language and Wordling differential acceptance remain pending.

Sources: [REF51 PDF 860-860 (printed 843-843)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=860); [REF51 PDF 861-861 (printed 844-844)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=861); [REF51 PDF 862-862 (printed 845-845)](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=862).

Observed scope: Original-app authored fixture repeated from fresh copies. Stable screen captures, clean WP exits, native body/prefix comparisons and bounded merge inspections are retained. Other code pairs, handler levels, language branches and Wordling differential acceptance remain unverified.

Evidence: [2026-10-29-advanced-03](reference-runs/2026-10-29-advanced-03/run.json), [2026-10-29-advanced-04](reference-runs/2026-10-29-advanced-04/run.json).
