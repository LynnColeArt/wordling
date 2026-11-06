# WP04 observed editing command contracts

Research handoff for document/editor implementers and reviewers, 2026-10-30.
Requirements: FR-004 (session and prompts), FR-005 (editing/Reveal Codes),
FR-008 (attributes), NFR-004 (evidence). Authority remains `spec.md`, `plan.md`,
`data-model.md`, `docs/compatibility.md` and `docs/roadmap.md`. The WP01
`contracts/native-framing.md`/`native-fixtures.json` govern native framing.
This research does not implement editing or establish M1 parity. M1 retains
complete original scope; PDF remains M2. WP12 owns executable continuation WPs.

## Evidence boundary and manual locators

Observed means the exact bounded original-app recipe, not the whole catalogue
scenario or a Wordling comparison. The selected original is plain U.S. English
WP 5.1 DOS dated 1992-03-09. `docs/research/reference-baseline.json` and
`docs/research/reference-environment/{environment,resource-profile}.json` pin
its executable, FreeDOS/QEMU environment and July 1992 text-only Standard Printer.
This is not historical MS-DOS or a graphics/font-independent cursor oracle.

Canonical CMD51 status/source/requirement links are in
`docs/research/command-scenarios.json`; status remains partially-observed or
not-run and implementation remains not-implemented. Sources are pinned in
`docs/research/sources.json` and mission `research/source-register.csv`.
Locators below are printed pages and **one-based PDF pages**:

| Source | Subject | Printed / PDF |
| --- | --- | --- |
| REF51, 6/92 reference | Cursor movement across codes | 103–104 / 120–121 |
| REF51 | Delete Codes; code-pair repair | 112–113 / 129–130 |
| REF51 | Reveal Codes | 560–562 / 577–579 |
| REF51 | Typeover | 695–696 / 712–713 |
| REF51 | Undelete, three entries and eviction | 697–698 / 714–715 |
| SDK51, 12/93 toolkit | Packet 6 formatting flag | WP-11 / 24 |
| SDK51 | Body framing and attribute C3/C4 | WP-17–18,24–25 / 30–31,37–38 |

The later toolkit does not automatically establish release applicability. Its
attribute widths and flag identify observed bytes; original captures establish
these command outcomes. All contents are project-authored scratch inputs; no
bundled sample/resource/manual is copied. Existing raw evidence is immutable.

Four recipe families have two published repetitions each. Aliases below expand
under `docs/research/reference-runs/` and are used only for readability:

| Alias | Canonical run / repetition | Primary archived recipe source |
| --- | --- | --- |
| S | 2026-10-29-smoke-03 / smoke-02 | S/runner-source/smoke.py |
| E | 2026-10-29-extended-04 / extended-03 | E/runner-source/extended.py |
| A | 2026-10-29-advanced-04 / advanced-03 | A/runner-source/advanced.py |
| H | 2026-10-29-history-02 / history-01 | H/runner-source/history_loops.py |

Each run's `run.json` pins its trace, checks and export/capture hashes. The ledger
below pins all eight manifests, the four selected archived recipe sources,
20 canonical native outputs and 39 canonical screen captures. Whole output-pair
comparisons are retained in `docs/research/reference-environment/extended-output-comparison.json`,
`advanced-output-comparison.json` and `history-output-comparison.json`.
The advanced/history native-validation JSON files in that directory supply an
independent bounded body audit; they are not a production codec.

## State and position notation

One authoritative document state must serve normal and Reveal Codes views.
Use token gaps to express semantic cursor positions; a token can be an original
character identity or a complete native code. Never put the cursor inside a
C3/C4 byte sequence, or equate terminal cells, displayed inches and byte offsets.
`|` below is a gap, not a stored character. Selection `[start,end)` is a range
between gaps, including complete codes. The following notation is an
implementation contract derived from fixture framing, not an original internal
WP data structure:

- D: owned native image plus interpreted tokens and opaque spans; unrelated bytes
  and relationships remain preserved under FC-003/004.
- P: active token gap; R: Reveal Codes visible/hidden; M: insertion/typeover.
- B: no block or a block anchor/current gap; Q: normal/Delete Block/Undelete
  interaction context. F1 is context-dependent.
- H: remembered **deletion entries with command provenance**, newest first;
  h: optional preview choice. Preview is not an inserted document fragment.

The saved A fixture `A[BOLD]BC[bold]D` has B=324 and body
`41 C3 0C C3 42 43 C4 0C C4 44`. Its gaps g0..g6 correspond to absolute byte
offsets `324,325,328,329,330,333,334`. g1 is before Bold On, g2 after it,
g4 before Bold Off and g5 after it. The 3-byte codes are each one token here.
For the unsaved E fixture `A[BOLD]B[bold]C`, use the analogous token gaps without
claiming its missing pre-edit native file was captured. Printed code labels are
views; `[BOLD]` is not literal document text.

Movement setup in E/A is `Home,Home,Home,Up` followed by the exact Right sequence
in the archived recipe. g1 in A has displayed Pos 1.1 inches; g4 has Pos 1.3.
These are resource-specific observations, not a universal position conversion.
Center's after-code position is 4.1 inches in CMD51-051; removing it returns to
1 inch. A code can affect geometry without adding an ordinary character.

## Bounded transition table

Rows below define only observed branches. File names are relative to
`<alias>/<CMD51-ID>/`; captures use `<stage>/screen.txt`. Exact hashes and full
paths are in the ledger. Native effect means observed body bytes unless explicitly
labelled a future writer requirement. Post-command cursor status is a screen
observation; unrecorded cursor/model state must not be inferred.

| CMD51 | Preconditions and input | Observed state/output | Native evidence / position |
| --- | --- | --- | --- |
| 046 | S: `a|bc`, insertion; Insert, X, Insert, Y | Typeover status appears then disappears; `aXc` then `aXYc` | `typeover-active`, `insert-restored`; final Pos 1.3. **No WP5 export**. ASCII body `61 58 59 63` is a future writer expectation, not observed native evidence. |
| 048 | S: F6, alpha, F6, beta; Alt+F3 twice | `[BOLD]alpha[bold]beta` exposed, then normal `alphabeta`; final R hidden | `normal`, `codes-on`, `codes-off`; all Pos 1.9. **No native before/after export**; byte-identical view toggling remains a required writer invariant. Recipe cursor is at end, despite broader catalogue precondition. |
| 050 | E: Center ABC; R visible; cursor before Center; Delete | Center disappears, ABC survives | `before-delete`, `after-delete`; `CENTER.WP5` body `414243`, Pos 1 before/after. No saved pre-delete Center image. |
| 051 | E: same; one Right places cursor after Center; Backspace | Same final plain ABC | `before-backspace`, `after-backspace`; `BACKSP.WP5` body `414243`; Pos 4.1 -> 1. |
| 200 | E: `A|[BOLD]B[bold]C`; Delete | Both bold codes removed, ABC survives | `before-boundary-delete`, `after-boundary-delete`; `PAIRED.WP5` body `414243`; Pos 1.1 -> 1.1. This file is post-delete, not an attributed seed. |
| 201 | E: `A[BOLD]B[bold]|C`; Backspace | Both bold codes removed, ABC survives | Same capture stages/name; body `414243`; Pos 1.2 -> 1.2. |
| 202 | A: select only `[g1,g2)` Bold On; Alt+F4, Right, Backspace, Y at prompt | Text ABCD and bold BC retained; B clears and normal context resumes | `ORIGIN.WP5` and `REPAIRED.WP5` identical ten-byte bodies; `selected-block`, `delete-confirmation`, `pair-repaired`; final Pos 1.1. |
| 203 | A: select only `[g4,g5)` Bold Off; same commands | Same body/code-pair repair | Same file/stage names; final Pos 1.3. |
| 204 | A: select `[g1,g5)` including both codes and BC; Backspace, Y | D becomes `A|D`; F1, 1 Restore brings back both codes and BC | ORIGIN -> DELETED body `4144` -> RESTORED original ten-byte body; `deleted`, `restore-preview`, `restored`; Pos 1.1 -> 1.3 on restore. |
| 045 | A: at g1, Delete opening code then Delete twice for B,C; F1, 1 | Intermediate AD; restores plain BC, not removed bold codes | ORIGIN attributed; DELETED `4144`; RESTORED `41424344`; `restore-preview`, `restored-without-attributes`; Pos 1.1 -> 1.3. Only forward character Delete exercised. |
| 043 | H: delete ONE/TWO/THREE with cursor Right between word groups; F1,2,2 | Preview THREE,TWO,ONE; F1 cancels; reopen starts at THREE; 2,2,1 restores ONE at current cursor | BASE=BROWSED body `2020`; HISTORY `20204f4e45` (two spaces + ONE); `latest`, `previous`, `oldest-retained`, `reopened-latest`, `restore-choice`, `restored`; final Pos 1.5. |
| 211 | H: add a separate fourth deletion FOUR | Only FOUR,THREE,TWO retained; further Previous shows FOUR in this capture; cancel/reopen then restore TWO | BASE=BROWSED `202020`; HISTORY `20202054574f` (three spaces + TWO); same history stages plus `beyond-third`; final Pos 1.6. No recovery of ONE. |

The H/043 word-deletion document sequence is `ONE TWO THREE` -> ` TWO THREE`
-> `  THREE` -> two spaces; cursor Right over each surviving separator separates
the deletion groups. H/211 starts `ONE TWO THREE FOUR` and finishes three spaces.
The retained newest-first choices are `[THREE,TWO,ONE]` and `[FOUR,THREE,TWO]`
respectively. Preview F1 returns to normal context without inserting that displayed
word; normal-context F1 reopens at newest. Restore's effect on subsequent H
ordering/consumption is deliberately unspecified, because no later history
inspection was captured. Cursor status after restoring is recorded in the table.

`Delete Block? No (Yes)` is captured before Y in 202/203/204. The tested input
explicitly answers Y; cancellation/No is **not observed** here. Ordinary code
Delete/Backspace recipes issue no confirmation response. Their successful outcome
establishes no mandatory user confirmation in those exact recipes, not the absence
of every possible transient prompt or confirmations for other code types.

For A/202,203,204,045 the entire prefix is otherwise identical: the **only**
prefix byte difference ORIGIN -> REPAIRED/DELETED/RESTORED is absolute offset 256,
`00 -> 08`. This is packet 6 bit 3, must-be-formatted, for these files, not a
universal fixed flag offset. Locate it via the packet index in real code.
Restored/repaired **body** identity is not whole-file identity. H BASE and BROWSED
are whole-file byte-identical in these fixtures. Never normalize reference bytes.

## Given/When/Then contracts for later implementation

These are executable acceptance intentions, not claims that tests or code exist.
Evidence labels distinguish original assertions from still-required native checks.

**EC-046 — modes (observed screen; native writer pending).** Given S/046's abc
and cursor gap after a, When Insert enables typeover and X is entered, Then b
is replaced, c survives and the resulting cursor permits Y to be inserted between
X/c after Insert disables typeover. Assert `aXYc`, status Typeover only while
active, and after a writer exists exact ASCII native characters without silently
changing unrelated codes/resources. There is no saved original output to serve
as a byte-for-byte writer oracle yet.

**EC-048 — shared views (observed screen; native preservation obligation).**
Given the actual S/048 end-of-document position, When Alt+F3 toggles twice,
Then the same bold alpha/plain beta document is shown in both views and Pos 1.9
is retained. A Wordling no-edit export must remain byte-identical by FC-002.
The original probe has no native save comparison and does not establish the
catalogue's before-bold cursor branch or all view-specific cursor behavior.

**EC-050/051/200/201 — code-targeted deletion (observed output).** Given the
exact gaps in the transition table, When the indicated Delete or Backspace is
used without an active block, Then remove the indicated Center code or both bold
boundaries, preserve all ABC text, and match the post-edit native body. Deleting
a code must target its full token, not one delimiter byte. These outcomes do not
imply all paired codes share bold's deletion rules.

**EC-202/203 — one blocked boundary (observed native body).** Given A/ORIGIN and
only g1..g2 or g4..g5 selected, When Backspace opens Delete Block and Y confirms,
Then text and the bold BC span remain as the original ten-byte body; the block
indicator clears. Compare each endpoint separately. Preserve the observed packet
6 transition as reference evidence while requiring a future writer to explain
its own required metadata changes. Do not substitute the non-block rule that
removes the pair, and do not infer an original internal repair algorithm.

**EC-204 — blocked span restoration (observed native body).** Given A/ORIGIN,
When both boundaries and BC are blocked, deleted and confirmed, Then body is AD.
When F1 then 1 Restore is used at that cursor after the recipe's intermediate
save, Then native body returns to `41c30cc34243c40cc444`. The restored fragment
includes both attribute codes; this is a command-specific deletion entry.
Its subsequent history lifetime, persistence across exit, and later save effects
are not established by this observation.

**EC-045 — character deletion restoration (observed native body).** Given the
same original, When character Delete removes Bold On and both pair boundaries
vanish, followed by two more Deletes for BC, Then body is AD. When F1/1 is used,
Then body is plain ABCD. Restoration must not reuse EC-204's attributed fragment.
The consecutive Delete commands restore BC together in this recipe; this does
not specify grouping under every interleaved key, mode or reverse deletion.

**EC-043 — preview isolation and cursor-relative restore (observed files).**
Given three separately remembered word deletions leaving two spaces and cursor
at their end, When F1 opens the preview then 2 twice selects ONE, Then the preview
shows THREE/TWO/ONE in order while D remains two spaces. When F1 cancels, Then
BASE and BROWSED remain byte-identical. When history reopens, Then newest THREE
is selected again; 2,2,1 inserts ONE at the current cursor (body two spaces+ONE),
not at its original location. The menu displays `1 Restore; 2 Previous Deletion`;
this contract uses numeric keys, not untested arrow selection.

**EC-211 — eviction (observed files and capture).** Given FOUR is deleted after
ONE/TWO/THREE as distinct groups, When history is opened, Then retained entries
are FOUR/THREE/TWO, ONE is unavailable; the next Previous after TWO displays FOUR
in `beyond-third`. Cancel/reopen starts at FOUR again. Restoring TWO yields
three spaces+TWO. Do not invent a fourth accessible entry, unlimited undo, redo,
or a persistent version history. Whether restoring consumes/reorders an entry
or how repeated Restore behaves still needs a probe.

## Explicit untested combinations and next probes

No new original run was necessary to extract the above existing observations;
this owned surface does not alter the harness or evidence. The following remain
M1 obligations and must not acquire observed/implemented labels from this contract:

- **CMD51-047 is not-run.** Its manual-derived requirement (REF51 695/PDF712) is
  that typeover at a formatting-code boundary inserts before the code, retaining
  it. EC-046 tests only plain ASCII. Probe exact code gaps/modes, save before/after,
  expose Reveal Codes and record cursor/attribute outcomes before enabling that
  write branch. Do not substitute an inferred overwrite or skip-across rule.
- **CMD51-049 is not-run.** The code-boundary setup in E/A shows usable Right
  navigation, but the dedicated stationary-visible-cursor crossing assertion is
  not separately checked or natively saved. Probe before/after each boundary in
  both views with stable cursor captures and native preservation checks.
- The general CMD51-027 selection, CMD51-035 ordinary Delete and CMD51-042
  cursor-restoration scenarios remain not-run as catalogue scenarios. Incidental
  use in these recipes does not upgrade full scenario coverage.
- Test other attribute pairs (underline is documentary, not observed here),
  nested/crossing formatting, adjacent/empty pairs, extended characters, opaque
  functions, notes/boxes/subdocuments, paragraph/page boundaries and large spans.
- Test block No/cancel, reversed selection and Left/Backspace grouping, Delete
  versus Backspace in block mode, normal-view versus code-pane targeting,
  restored cursor gaps at each boundary and codes with confirmation prompts.
- Test Undelete arrow selection, no history, fewer than three entries, deletion
  grouping with interleaved navigation/mode/view/save commands, deletion of only
  codes, repeated Restore, history after a failed command, across two documents,
  exit/retrieve, memory limits/spill and restoration into differently formatted
  or structurally unsafe locations. Do not infer disk persistence from H files;
  they contain document data, not a serialized history sidecar.

Each probe needs its own approved owned surfaces/queue entry, original baseline,
exact keystrokes, stable captures, native files/hashes and clear failure outcomes.
Unknown or unsupported edit combinations must fail explicitly before mutation
under FC-004 until their semantics and safe native writes are validated; they
remain in M1. Full editor parity is not defined as only these recipes.

## Bounded implementation proposals for WP12

These are research handoffs **inside this artifact**, not new executable WPs.
Dependency order is intentional; do not implement a semantic writer merely
because WP02 passes a no-edit copy test.

1. **Token/gap model and view toggle:** build on WP02's immutable owned image and
   framed span support. Recognize original ASCII and C3/C4 identities without
   losing opaque spans. Model normal/Reveal views over one document; assert gap
   mapping independently of terminal geometry. Implement EC-048's observed end
   position first and retain unobserved branches as probes. No semantic writes.
2. **Plain insertion/typeover:** EC-046 with explicit M/Q state, cursor gaps and
   mode status. Obtain original saved files for native writer comparison and
   CMD51-047 before code-boundary writes. No terminal-cell-based document indexing.
3. **Bounded Center/bold deletion and block repair:** implement EC-050/051,
   EC-200/201 and EC-202/203 for exactly researched structures only. Preserve
   command provenance and explain required paired-code/packet6/length updates.
   Unknown packet references or unsafe relationships prevent mutation/save.
4. **Command-specific Undelete:** EC-204 versus EC-045 fragment semantics, then
   EC-043/211 three-entry preview/cancel/restore/eviction. Preserve separate D/H/Q
   states and current-cursor insertion; establish grouping/consumption behavior
   with probes before generalizing. Keep history transient until evidence says
   otherwise; no new required native sidecar or modern undo model.

Every writer slice requires supported-structure/offset ownership, checked
relocation and relationship updates beyond WP01 outer framing; unrelated-byte
preservation and failed-edit immutability; original retrieve/**edit/print/save**
comparison under declared resources; reopening in Wordling; Go build/test/vet and
native malformed/fuzz checks for affected decoding. WP03 safe filesystem
transactions must precede replacing real files. A body-only match or the
packet6 reference observation never authorizes blanket normalization, arbitrary
prefix rewrite or claiming complete interoperability/layout acceptance.

## Validation and evidence ledger

The JSON ledger pins source evidence, not Wordling results. Verify each native
body from its stored header pointer and compare all selected capture/file hashes
against their case's run manifest. Confirm case IDs against the canonical
catalogue, and repeat both catalogue `--check` commands. These checks need no DOS
run and alter no raw file. The declared project regression runner is
`python3 scripts/review_checks.py --junitxml=<temporary-output>`; review transition
runs the genuine configured command. The installed runtime's baseline count
stores failure identities rather than full JUnit suite counts; a total of zero
in baseline-tests.json does not prove no project checks executed. WP04's baseline
and head must use DeclaredCommandScopeSource/junit_xml; report any mismatch
explicitly rather than treating differing sources as a comparable clean baseline.

Author validation: the embedded ledger verifier passes every selected hash,
run/case link, native body and native repetition. Both catalogue checks pass.
The genuine regression command exits zero in the planning checkout; inventory,
scenarios, review-adapter tests and Go package discovery pass. Go build/test/vet
are explicitly skipped because this checkout has no Go packages yet. WP02's
separate coding lane is not inspected or claimed by these planning-lane results.
No new probes, raw-evidence edits or code changes were performed for WP04.

<!-- WP04_EVIDENCE_BEGIN -->
```json
[
  {"path":"docs/research/reference-runs/2026-10-29-smoke-02/run.json","sha256":"d361f81768a5ee9ea85d4590b013c53c2e68770af76ceaf91302b308281091d6","size":31814,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/run.json","sha256":"c4cae074cc75e651eff994e62cb0917d5645477c906a1f975738ea4ab62de4fe","size":32746,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-03/run.json","sha256":"68450fd8efa5deea93e83021b043ad0a9ab1ada4867e5d5616c49fcf7c1d7809","size":63907,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/run.json","sha256":"c7d98c6225892261dff38b88b3c9c044856ad43ad4e5776d4197089d885ac0fc","size":63907,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-03/run.json","sha256":"6abdb82bb54d9cd1a3d0a6089977cdfa1086c5cc484f27cc067e176626b16610","size":127860,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","sha256":"ae9bc9fda6091903b04c07b2894c487074a4c01edec656667b8a75da8dbbceb8","size":127860,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-history-01/run.json","sha256":"4075080561b4b2215aac7f7b8df64f9b2ddfe6dcc2dd010a092515e3f59fc0da","size":115830,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/run.json","sha256":"08e77a5ae04175697da06884a3ce01c1eddcd8e77780c163ae0eb36fe361057d","size":115830,"kind":"run"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-046/typeover-active/screen.txt","sha256":"9c8c4fee6148b4a7751d4c833e9ba69c841a0b4f53e267a41b17a7a9211bb793","size":105,"kind":"screen","case_id":"CMD51-046","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-046/insert-restored/screen.txt","sha256":"358cd5b4b122aac26b78ca712a6875585ce2d3c7eae4a36d70a8cb957a977524","size":106,"kind":"screen","case_id":"CMD51-046","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-048/normal/screen.txt","sha256":"4cf29298079b3019e62ece9413fcc742844c295d82e94170e3dfe05eb0418648","size":111,"kind":"screen","case_id":"CMD51-048","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-048/codes-on/screen.txt","sha256":"a2c28aedf3b46b6ac3839113a0b3cd103a9d75d4a882d2e9b0b94e5a585f5802","size":234,"kind":"screen","case_id":"CMD51-048","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-048/codes-off/screen.txt","sha256":"4cf29298079b3019e62ece9413fcc742844c295d82e94170e3dfe05eb0418648","size":111,"kind":"screen","case_id":"CMD51-048","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-050/CENTER.WP5","sha256":"80977af454407a88e5250423a653bd30143c947658bf279798dcb3cc97bfcd38","size":327,"kind":"native","case_id":"CMD51-050","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json","body_offset":324,"body_hex":"414243"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-050/before-delete/screen.txt","sha256":"3c11e45c541c4ece3cc78b543e6a6304dd0d8c3c2f7f247aee6ab8a2160283ec","size":247,"kind":"screen","case_id":"CMD51-050","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-050/after-delete/screen.txt","sha256":"c3ac5aad9f1d3a75a7a2ff2aa9f88ce1a871e537e1939d8ba8624f12c383672b","size":208,"kind":"screen","case_id":"CMD51-050","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-051/BACKSP.WP5","sha256":"80977af454407a88e5250423a653bd30143c947658bf279798dcb3cc97bfcd38","size":327,"kind":"native","case_id":"CMD51-051","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json","body_offset":324,"body_hex":"414243"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-051/before-backspace/screen.txt","sha256":"3c4d59721205ababf66c9e2f6ed1af32b436b7a49d3debeb156c7792fb154dc0","size":249,"kind":"screen","case_id":"CMD51-051","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-051/after-backspace/screen.txt","sha256":"c3ac5aad9f1d3a75a7a2ff2aa9f88ce1a871e537e1939d8ba8624f12c383672b","size":208,"kind":"screen","case_id":"CMD51-051","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-200/PAIRED.WP5","sha256":"80977af454407a88e5250423a653bd30143c947658bf279798dcb3cc97bfcd38","size":327,"kind":"native","case_id":"CMD51-200","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json","body_offset":324,"body_hex":"414243"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-200/before-boundary-delete/screen.txt","sha256":"fa5167d034c39613feaae4906d09fbe17ae12f1bb6ef206ed48d9a1d077b1728","size":222,"kind":"screen","case_id":"CMD51-200","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-200/after-boundary-delete/screen.txt","sha256":"514291db6e77f4ee92595d24fd1f0b95a335a6a4d91a0848c726c13eaea447fa","size":210,"kind":"screen","case_id":"CMD51-200","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-201/PAIRED.WP5","sha256":"80977af454407a88e5250423a653bd30143c947658bf279798dcb3cc97bfcd38","size":327,"kind":"native","case_id":"CMD51-201","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json","body_offset":324,"body_hex":"414243"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-201/before-boundary-delete/screen.txt","sha256":"7646d5fb846f56a301b4fbd78ca8e0d30cc993bb01f41aa0495f1965d6b5abfe","size":222,"kind":"screen","case_id":"CMD51-201","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-201/after-boundary-delete/screen.txt","sha256":"cd955203619c18a3de31e1b05facc2ad058d6522cf450bb17834a061f4e763c8","size":210,"kind":"screen","case_id":"CMD51-201","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-202/ORIGIN.WP5","sha256":"c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d","size":334,"kind":"native","case_id":"CMD51-202","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-202/REPAIRED.WP5","sha256":"e04b59b3efc3a3e5c03de7e4be768af9bc2e76d0e2b7a706051a1ab090869685","size":334,"kind":"native","case_id":"CMD51-202","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-202/selected-block/screen.txt","sha256":"f096daab514de9d8448ea1119e5f72fb85fed4d579441050a1521f7e8eefda01","size":231,"kind":"screen","case_id":"CMD51-202","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-202/delete-confirmation/screen.txt","sha256":"659a9c66c844b1ff2db43a84a956759d8971d5e1ef37c1ee581a82f5acef772d","size":176,"kind":"screen","case_id":"CMD51-202","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-202/pair-repaired/screen.txt","sha256":"ee999fa91f16f2e59927fae6500e22538d4472882c2f5a9858d9f46b91c3d5b3","size":224,"kind":"screen","case_id":"CMD51-202","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-203/ORIGIN.WP5","sha256":"c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d","size":334,"kind":"native","case_id":"CMD51-203","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-203/REPAIRED.WP5","sha256":"e04b59b3efc3a3e5c03de7e4be768af9bc2e76d0e2b7a706051a1ab090869685","size":334,"kind":"native","case_id":"CMD51-203","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-203/selected-block/screen.txt","sha256":"7288a58ee8ba7e1998ab616125e16790291025e020de3e0d4e61697e5f0fd44d","size":231,"kind":"screen","case_id":"CMD51-203","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-203/delete-confirmation/screen.txt","sha256":"27df5103faa9afb5e817a70242b3cb09e39db772d49a3d396bdeacb436086171","size":176,"kind":"screen","case_id":"CMD51-203","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-203/pair-repaired/screen.txt","sha256":"4072122f6d4786d99f4b9e2b7caee1f492c2db5fc3a759b337900db3f15cb977","size":224,"kind":"screen","case_id":"CMD51-203","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/DELETED.WP5","sha256":"273e4fbc663ee58fba04c5653b87d8bfdea1bfc4de355ffa612dafdc659ddaaa","size":326,"kind":"native","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"4144"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5","sha256":"c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d","size":334,"kind":"native","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/RESTORED.WP5","sha256":"e04b59b3efc3a3e5c03de7e4be768af9bc2e76d0e2b7a706051a1ab090869685","size":334,"kind":"native","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/selected-block/screen.txt","sha256":"186617660b9847634c574c5e1bb7cab2c1803ba262a74e036e6761724d21a163","size":231,"kind":"screen","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/deleted/screen.txt","sha256":"b1a6ebdb73e80179e852895b0430f56124bb5902b499f66cd7bef0eefae257fe","size":208,"kind":"screen","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/restore-preview/screen.txt","sha256":"d355c7672c4b60cd1783cabb6dd704cbf76f453e82a42e5fc987b7ec1d4199dc","size":197,"kind":"screen","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/restored/screen.txt","sha256":"965dbe7c169524384b4267e029fb7f11b91b3de782adb7b3261e8d60d0a5505c","size":224,"kind":"screen","case_id":"CMD51-204","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-045/DELETED.WP5","sha256":"273e4fbc663ee58fba04c5653b87d8bfdea1bfc4de355ffa612dafdc659ddaaa","size":326,"kind":"native","case_id":"CMD51-045","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"4144"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-045/ORIGIN.WP5","sha256":"c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d","size":334,"kind":"native","case_id":"CMD51-045","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41c30cc34243c40cc444"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-045/RESTORED.WP5","sha256":"910acdb00f37e89356a2b1245b7273ae82f17a88832c088967ca2fb0be15cc52","size":328,"kind":"native","case_id":"CMD51-045","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json","body_offset":324,"body_hex":"41424344"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-045/deleted/screen.txt","sha256":"b1a6ebdb73e80179e852895b0430f56124bb5902b499f66cd7bef0eefae257fe","size":208,"kind":"screen","case_id":"CMD51-045","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-045/restore-preview/screen.txt","sha256":"3e2752bfb13526bd82ddbe9e21fe638d6ea2c4c2144820175edc381daf298386","size":185,"kind":"screen","case_id":"CMD51-045","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/CMD51-045/restored-without-attributes/screen.txt","sha256":"e640ce0389f77624fd8c91b2398f5d07db10e6f154279fc666b64a7509b8618c","size":212,"kind":"screen","case_id":"CMD51-045","run_manifest":"docs/research/reference-runs/2026-10-29-advanced-04/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/BASE.WP5","sha256":"96c8286999117af13946eef81b67240d1e79a10a489003cf340db30579c95439","size":326,"kind":"native","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json","body_offset":324,"body_hex":"2020"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/BROWSED.WP5","sha256":"96c8286999117af13946eef81b67240d1e79a10a489003cf340db30579c95439","size":326,"kind":"native","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json","body_offset":324,"body_hex":"2020"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/HISTORY.WP5","sha256":"209059e5cf644baa51dcaa3952383cee456b7b1fb103f94d94489e73f3f92f3b","size":329,"kind":"native","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json","body_offset":324,"body_hex":"20204f4e45"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/latest/screen.txt","sha256":"76ee2b8c87417c7d45eed304f9b4312094c905dbd554989b722e15d4e639a498","size":75,"kind":"screen","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/previous/screen.txt","sha256":"668389bfff5f9719d45c1b53b50124641d12c95e6fdeb4643423b0efd025765a","size":73,"kind":"screen","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/oldest-retained/screen.txt","sha256":"881a2e30f736ccd44410bd511356fa7494a24a55e3530acdbf462bff9c7e99c5","size":73,"kind":"screen","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/reopened-latest/screen.txt","sha256":"76ee2b8c87417c7d45eed304f9b4312094c905dbd554989b722e15d4e639a498","size":75,"kind":"screen","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/restore-choice/screen.txt","sha256":"881a2e30f736ccd44410bd511356fa7494a24a55e3530acdbf462bff9c7e99c5","size":73,"kind":"screen","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-043/restored/screen.txt","sha256":"e8f87247341d5963528e4359b76d0ed35e726a8f5bd4d324d639dc3eb8da5cdc","size":107,"kind":"screen","case_id":"CMD51-043","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/BASE.WP5","sha256":"fbba76fcc4e3b6316994474e114e2a2499776d746b81930c689aa5ada6641b40","size":327,"kind":"native","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json","body_offset":324,"body_hex":"202020"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/BROWSED.WP5","sha256":"fbba76fcc4e3b6316994474e114e2a2499776d746b81930c689aa5ada6641b40","size":327,"kind":"native","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json","body_offset":324,"body_hex":"202020"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/HISTORY.WP5","sha256":"96f9c70050ae75d28877e92fee24e76e9141e3b2e512279935051e8d18772dd1","size":330,"kind":"native","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json","body_offset":324,"body_hex":"20202054574f"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/latest/screen.txt","sha256":"e193201bde1a4ce704080bd0fdb3a0da7896507274f337e6d7765c90f33f12e6","size":75,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/previous/screen.txt","sha256":"ecfb3c92513c70e3001bf8411dce95d94145d2c43f594471bfecc6515dd684ef","size":76,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/oldest-retained/screen.txt","sha256":"655634ba6ef91cf2a2cdb57d177c5568bb86b2930879a915d7dba5a43f693a42","size":74,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/beyond-third/screen.txt","sha256":"e193201bde1a4ce704080bd0fdb3a0da7896507274f337e6d7765c90f33f12e6","size":75,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/reopened-latest/screen.txt","sha256":"e193201bde1a4ce704080bd0fdb3a0da7896507274f337e6d7765c90f33f12e6","size":75,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/restore-choice/screen.txt","sha256":"655634ba6ef91cf2a2cdb57d177c5568bb86b2930879a915d7dba5a43f693a42","size":74,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/CMD51-211/restored/screen.txt","sha256":"d8669352eb65adac038986044fe5f96aaed25957fd732d5ae41e595678109cbe","size":108,"kind":"screen","case_id":"CMD51-211","run_manifest":"docs/research/reference-runs/2026-10-29-history-02/run.json"},
  {"path":"docs/research/reference-runs/2026-10-29-smoke-03/runner-source/smoke.py","sha256":"e70bd625b572bd2018d0f4fb5e2868a0850142ab1755dedda175ffeaf0be9a8a","size":7655,"kind":"runner"},
  {"path":"docs/research/reference-runs/2026-10-29-extended-04/runner-source/extended.py","sha256":"ac58afcef32b0fa2d6bf7eff6129a7108b7e65ec8bc8d5119faaf3678c64e2a8","size":6195,"kind":"runner"},
  {"path":"docs/research/reference-runs/2026-10-29-advanced-04/runner-source/advanced.py","sha256":"837cdcb8aa85531c7dff873f3705f52b81e4ae6a9c1c419f5891d1336eb9203f","size":8795,"kind":"runner"},
  {"path":"docs/research/reference-runs/2026-10-29-history-02/runner-source/history_loops.py","sha256":"d788b84952f971a2e3d1b1512a5ad75b480943931a3266251db548c92f60a87b","size":5746,"kind":"runner"}
]
```
<!-- WP04_EVIDENCE_END -->

Reproduce ledger verification from the repository root:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json, struct
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/editing.md')
s = p.read_text().split('<!-- WP04_EVIDENCE_BEGIN -->',1)[1]
rows = json.loads(s.split('```json\n',1)[1].split('\n```',1)[0])
catalogue = {c['id']: c for c in json.loads(Path('docs/research/command-scenarios.json').read_text())}
repeats = {'smoke-03':'smoke-02', 'extended-04':'extended-03',
           'advanced-04':'advanced-03', 'history-02':'history-01'}
sha = lambda b: hashlib.sha256(b).hexdigest()
for r in rows:
    path = Path(r['path'])
    data = path.read_bytes()
    assert (len(data), sha(data)) == (r['size'], r['sha256'])
    if 'case_id' in r:
        assert r['case_id'] in catalogue
        run = json.loads(Path(r['run_manifest']).read_text())
        case = next(c for c in run['results'] if c['case_id'] == r['case_id'])
        assert any(e['path'] == r['path'] and e['sha256'] == r['sha256'] and
                   e['size'] == len(data) for e in case['evidence'])
        assert r['run_manifest'] in catalogue[r['case_id']]['evidence_paths']
    if r['kind'] == 'runner':
        run = json.loads((path.parent.parent/'run.json').read_text())
        assert any(Path(e.get('archive_path',e['path'])).name == path.name and
                   e['sha256'] == r['sha256'] for e in run['runner_sources'])
    if r['kind'] == 'native':
        body = struct.unpack_from('<I',data,4)[0]
        assert body == r['body_offset'] and data[body:].hex() == r['body_hex']
        repeat = r['path']
        for after,before in repeats.items():
            repeat = repeat.replace(after,before)
        assert Path(repeat).read_bytes() == data
assert catalogue['CMD51-047']['oracle_status'] == 'not-run'
assert catalogue['CMD51-049']['oracle_status'] == 'not-run'
print('WP04 evidence hashes, original run links, native bodies and repetitions valid')
PY
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
```
