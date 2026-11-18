# Mission 1 closeout audit — read only

Audit date: November 18, 2026. Scope is complete WordPerfect 5.1 DOS parity under the existing charter, not only the native Windows milestone. No source/runtime/tracker/VM mutations were performed. Only this report and diagnostic JSON were written outside the repository.

## Immediate conclusions

1. `spec-kitty next --mission wp51-parity-01M64CVY --json` previewing `accept` reflects exhaustion of the authored 99-WP queue (96 approved, 3 done), not full parity. `continuation.md` lines 3–17 explicitly say queue exhaustion cannot authorize acceptance or M2; the initial ledger has `parity_accepted: false`, `all_m1_obligations_closed: false`, and `queue_exhaustion_authorizes_acceptance: false`. Historical `spec.md`/ledger statements that no app exists are stale research snapshots, not present implementation evidence.
2. Current command audit is exactly **186 verified / 38 partial / 20 unimplemented = 244**. All 58 open rows are enumerated below. The 20 unimplemented rows report genuine missing entry points. The 38 partial rows are not merely paperwork: many need substantive product/resource expansion; a few are promising qualification-led closures. The counts are profile-bounded coverage, not effort estimates or whole-M1 acceptance.
3. `acceptance-matrix.json` has **overall_verdict=pending and 17/17 FR criteria pending**, all evidence/verified_by/verified_at unset. Five NFR, six constraints, FC-001–010 and SC-001–005 must be covered via linked evidence before mission acceptance; FC-010 is the M2/PDF gate, not an instruction to implement PDF in M1.
4. `contracts/coverage-concordance.md` and `contracts/coverage-leaves.md` retain 91 parent groups and all 36 workbook lessons as open with unexpanded source/menu/appendix/utility branches. Closing the 58 scenario rows alone is insufficient without the full inventory/leaf reconciliation.
5. The native Windows/PowerShell milestone from PR12 closes useful platform test work. It does not automatically close CMD51-189 (single DOS command vs interactive shell adaptation), all mouse/physical delivery, all resource profiles, or all Mission 1 obligations.

## Actual read-only acceptance diagnostic

Command: `spec-kitty accept --mission wp51-parity-01M64CVY --diagnose --json`.
Complete output: `/tmp/wordling-mission1-closeout-20261118/accept-diagnose.json`.

`ok=false`; `all_done=true` refers to accepted-ready authored WPs. Exact blockers:

- `WP82: missing agent in canonical runtime state`.
- Acceptance must execute on `feat/wp51-parity` or `kitty/mission-wp51-parity-01M64CVY`, not `fix/windows-powershell-overwrite`.
- A successful real GitHub Actions URL/run ID must be bound in mission `workflow-evidence.md`, because the mission changes `.github/workflows/native-prerelease.yml`.
- The Software Dev Kitty template expects `src/` despite the actual Go `cmd/` and `internal/` layout. Resolve the legitimate project-layout configuration or use the documented convention-only handling with explicit rationale; do not create a dummy `src/` or treat substantive gate failures as style exceptions.
- **Acceptance matrix presence/evidence/verdict and negative-invariant checks were skipped on the non-mission branch.** Switching branches is necessary before the diagnostic can expose the actual pending evidence failures. A false positive at this point would hide the entire mission criterion check.

No work package status or matrix was repaired by this audit. Root orchestrator owns canonical metadata repair, adopted baseline, task amendment, and runtime transitions. Preserve existing approved histories and use new reviewed continuation packages for actual unfinished scope; do not mark the 96 approved packages done as a substitute for missing parity.

## Governing final gates

- `spec.md` SC-001: no unclassified original documented features/utilities after full reconciliation.
- SC-002: every M1 obligation has passing original-app comparison evidence, and accepted native fixtures meet FC-001–009 as applicable.
- SC-003: declared editing/generated/print workflows match under the recorded baseline/resources.
- SC-004: no unresolved destructive mismatch, false-success save or undisclosed format substitution.
- SC-005: platform/version discrepancies have tested dispositions; any actual exclusion requires explicit owner approval recorded in git.
- `docs/compatibility.md`: byte-identical untouched saves; unrelated and unknown content preserved; original companion formats/character identities retained; direct native writer; original conversions/print formats; failure-safe saves. Native Go/race tests alone do not prove these original-interoperability obligations.
- `remaining-qualification.md` batches 0–5: establish exact candidate and reconcile inventory → everyday original/physical/proofreading journeys → original save/recovery cases → layout/automation and native reopening → remaining inventory/resources/utilities → independent final parity review and accepted preview.

## Practical continuation order

These are proposed slices, not reserved WP IDs or runtime claims. Root should first get the canonical mission onto the reviewed merged native baseline, repair metadata/evidence/layout diagnostics, then author/review/finalize a dependency-aware continuation rather than accepting the exhausted old queue.

1. **Coverage/evidence reconciliation and reference-harness repair.** Create a current machine-readable mapping from all 244 scenarios, 91 groups, 36 lessons and 38 FR/NFR/C/FC obligations to exact source/tests/reference evidence and explicit remaining branches. Preserve historical evidence. Reproduce current infrastructure-recovery reference failures (`ReadinessDeadline` / `EnvelopeDeadline`, startup `unknown-identity`, stopped-readonly expected-absence failure) without weakening guards. Distinguish intentionally frozen historical source guards from current product defects. Capture current original safety/preflight/tool ownership before any new oracle execution.
2. **Fast qualification-led editing closures**, with product fixes when actual comparisons disagree: CMD51-041/045/051, then exact display/mouse variants and the CMD51-189 adaptation. Existing CLI/native tests and original recipes supply starting points. Do not promote merely because an adjacent scenario is verified.
3. **New-buffer nested macro behavior** (CMD51-210/212/213/230) as a focused product/native-session continuation: `internal/editor/macro_execution.go:250` explicitly refuses nested resolution for New targets (`New macro target admits root source only`). Reuse original loaded-buffer fixtures, establish original unsaved-buffer equivalents, then broaden admission with independent failure/history/save/Doc2 checks. Keep richer Repeat/CANCEL/nested-function grammar separate (132/133/196).
4. **Classic window/keyboard/display and timed-backup behavior** (008/010/072–074/153/154/188/190), with actual native resource/physical-key evidence. Modern tabs/recovery are not an implicit exclusion of original two-screen/window/backup semantics.
5. **Layout foundations before dependents**: tab/Advance/hyphenation/base font/kerning/spacing/paper definitions (101/107–109/160/161/164/166/173), then newspaper/parallel columns (168/169), general note continuations (115–117), then expanded styles/table formula/join/generated documents (118/121–123/125). Declare matched font/printer metrics before new pagination claims.
6. **Resource and missing-format acquisition can run alongside implementation**: actual 4.2 document and 4.x macro producers (157/179); THS decoding/language resources (181/182); admitted graphics/font/printer profile. Do not invent legacy fixtures by changing a version byte or bootstrap a matching oracle from the candidate implementation.
7. **Graphics/equations/preview/printing and utilities**, after resource/native layout foundations: 146–148/174–177/185/187; separate original-format codecs, product commands, layout, printer stream and Linux presentation boundaries. The terminal-only current profile cannot justify declaring these features unsupported by scope.
8. **Passwords, file comparison, and shared access**: 082/159/192 need dedicated native-format and failure-safe contracts and (for shared workflows) a reference profile beyond the current no-NIC/single-user oracle. Broader Retrieve and column Math follow their model dependencies (065/180).
9. **Final exact-candidate gate**: integrated DOS and native output reopen/edit/print/save cycles, byte-for-byte no-edit cases, preserved opaque/packet data, physical GNOME/native host follow-ups, independent Mission 1 review, truthful full matrix verdict, canonical accept → merge → post-merge review/retrospective. Full modern format/PDF work remains Mission 2.

## Resources and actual blockers

Read-only availability checks found `/usr/bin/qemu-system-i386`, `/usr/bin/mcopy`, `/usr/bin/mdir`, `/usr/sbin/mkfs.fat`, Go and Python, and the expected private `research/cache/reference/master/{boot,harddisk}.img` paths. This audit did not read disk-image contents or execute a VM; current hashes/tool fit/ownership/readiness still need the reviewed prelaunch checks. Do not label them unavailable merely because the current task has not launched them.

The declared original is WP 5.1 US 03/09/92, FreeDOS 1.4, QEMU 8.2.2, Standard Printer from **July 17, 1992**, 10-cpi text only, no graphics, no NIC and no shared host directory. This is not historical MS-DOS, graphics/font pagination or network acceptance. `resource-profile.json` fingerprints original HYC/LEX/THS and printer resources; licensing prevents redistribution, not all private interoperability investigation. THS lookup/cancel already has original evidence under `docs/research/reference-runs/mission1-thesaurus/`.

Missing exact reference inputs are real: `mission1-convert-42/README.md` says a 4.2-authored document and conversion/native retrieval result are absent; the 5.1 utility can import 4.2 but cannot export a fixture. `mission1-macro-converter/README.md` has only MACROCNV launch, not a 4.x source macro or resulting WPM. These require lawful producers/fixtures, not fabricated bytes. The graphics/proportional-font/historical-DOS/language/network profiles need acquisition or explicit adjudicated adaptations; do not narrow the mission silently.

Reference controllers have explicit source/plan/case/repetition/authorization-note and exclusive-root-grant controls (`native_genesis.py`, `macro_session.py`, `wordling_edits.py`, `macro_quit.py`). Root must inspect the applicable current protocol and user authorization; old scoped grants are not reusable blanket permission. Their presence is not proof that the present full-mission user request is inadequate—routine authorized work should continue wherever current safety contracts can be satisfied. Physical-keyboard/mouse qualification cannot be claimed from PTY/ConPTY alone and may eventually require a bundled physical-machine handoff. `remaining-qualification.md` explicitly says no routine check-ins, only actual access/physical-input/product decisions.

## All 58 current open scenarios

Evidence-led means start with actual comparison, **not** “already fixed.” Partial means bounded functionality exists but remaining branches still require proof, implementation or resources. Source: `docs/research/mission-1-command-audit.md`.

### Editing, input and display

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-008 — Split document screens into windows | unimplemented | Implementation: independent split-window geometry/focus, preserving original two-document semantics. |
| CMD51-010 — Select a keyboard then restore Original | unimplemented | Implementation + native WPK/resource and Original-reset qualification. |
| CMD51-041 — Confirm delete to end of page | partial | Evidence-led: sampled hard-return automatic boundary passes; other automatic boundary kinds need DOS comparison and any resulting repair. |
| CMD51-045 — Character deletion restoration differs for paired attributes | partial | Evidence-led: compare command-specific paired-attribute restoration; related editing alone does not close this branch. |
| CMD51-051 — Backspace deletes code immediately before cursor | partial | Evidence-led: exact Backspace/code-owner boundary comparison, then repair if required. |
| CMD51-064 — Lowercase conversion preserves sentence/I exceptions | partial | Implementation/evidence: extended character identities and punctuation exceptions beyond sampled ASCII. |
| CMD51-065 — Retrieve inserts at the cursor | partial | Implementation/evidence: broaden safe insert-at-cursor native document contexts; keep unsupported relationships explicit. |
| CMD51-153 — Select and cancel text using the mouse | partial | Qualification-led/mixed: original mouse selection/cancel and actual physical delivery; current bounded menus/mouse support is insufficient proof. |
| CMD51-154 — Change the text display independently of print layout | partial | Qualification-led/mixed: exact editing-display variants, proving native/print independence. |
| CMD51-188 — Set an editing display option | partial | Qualification-led/mixed: exact original display options beyond bounded settings. |
| CMD51-190 — Choose an original cursor appearance | partial | Qualification-led/mixed: original cursor choices and native terminal delivery. |

### File handling, backups, safety and legacy documents

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-072 — Configure timed backup | partial | Implementation/evidence: original timed-backup configuration, directory/interval and startup behavior. Setup currently displays timed backup but only original backup choice has a handler. |
| CMD51-073 — Empty editing screen does not create a zero-byte timed backup | partial | Original timed-backup empty-screen semantics; modern autosave alone is not equivalent. |
| CMD51-074 — Startup checks backups for both document screens | partial | Original both-screen startup backup discovery and decisions; compare to modern six-buffer recovery adaptation. |
| CMD51-082 — Set a document password | unimplemented | Implementation: password/encryption support with original fixtures and failure safety. |
| CMD51-157 — Retrieve an original 4.2 document into 5.1 | unimplemented | Missing reference input + implementation: actual 4.2-authored document and CONVERT result; 5.1 CONVERT cannot export a 4.2 fixture. |
| CMD51-159 — Compare screen and disk document versions | partial | Implementation/evidence: multiple/ formatted changes and live removal differential beyond bounded ASCII. |
| CMD51-192 — Investigate shared-file access with separate user setups | unimplemented | Implementation + new reference profile: shared-file/multiuser locking; existing oracle has no NIC and single user setup. |

### Layout, pagination and resource-dependent formatting

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-101 — Insert a normal tab | partial | Implementation/evidence: arbitrary tab/layout settings, beyond current default tab profile. |
| CMD51-107 — Advance relative and absolute positions | partial | Implementation/evidence: remaining Advance directions and wrap configurations. |
| CMD51-108 — Do not advance beyond the current page | partial | Implementation/evidence: remaining native layouts and page-boundary cases, retaining raw Fast Save relationships. |
| CMD51-109 — Enable hyphenation at the cursor | unimplemented | Implementation + admitted hyphenation resource and cursor/native behavior. |
| CMD51-115 — Create a footnote | partial | Implementation/evidence: larger footnotes, automatic continuation and nested native relationships. |
| CMD51-116 — Create an endnote | partial | Implementation/evidence: other endnote placements and explicit generation. |
| CMD51-117 — Configure note continuation constraints | partial | Mixed: two unresolved native bytes plus more continuation combinations. Matching printed streams does not dispose of native uncertainty. |
| CMD51-160 — Set initial base font from selected printer resources | unimplemented | Resource + implementation: selected-printer base font and metrics, not text-only Standard Printer inference. |
| CMD51-161 — Toggle printer kerning at cursor | partial | Resource + implementation/evidence: proportional kerning metrics beyond fixed-pitch capture. |
| CMD51-164 — Set word and letter spacing independently | unimplemented | Implementation + resource-matched independent word/letter spacing. |
| CMD51-166 — Choose an existing paper definition | unimplemented | Implementation + original paper-definition/resource semantics. |
| CMD51-168 — Define and enable newspaper columns | unimplemented | Implementation: newspaper columns with native/page/print semantics. |
| CMD51-169 — Move through parallel columns with a hard boundary | unimplemented | Implementation: parallel-column boundaries and movement. |
| CMD51-173 — Select a label paper definition | unimplemented | Implementation + label paper definitions and original layout/print evidence. |

### Structured documents

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-118 — Create and apply a named style | partial | Implementation: remaining style types, arbitrary codes and library operations. |
| CMD51-121 — Join selected table cells | partial | Implementation: vertical joins and editing combined contents, beyond one horizontal 2x2 join. |
| CMD51-122 — Recalculate table formulas explicitly | partial | Implementation: formula/function/reference families beyond sampled two-cell addition. |
| CMD51-123 — Copy a formula to another cell | partial | Implementation: remaining copied formula/reference types. |
| CMD51-125 — Generate or decline replacing generated material | partial | Implementation: generated lists/indexes/authorities beyond default one/two-level contents. |

### Automation and data

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-132 — Repeat a macro using Repeat Value | partial | Implementation/evidence: broader Repeat Value and original macro runtime/recording contexts. |
| CMD51-133 — Stop a running macro | partial | Implementation/evidence: original CANCEL ON/OFF overriding stop behavior. |
| CMD51-179 — Convert a 4.x macro with MACROCNV | unimplemented | Missing reference input + implementation: original 4.x macro and MACROCNV 1.6 output. Utility launch is already observed. |
| CMD51-180 — Enter and leave original column Math mode | partial | Implementation/evidence: remaining original column Math functions/column definitions. |
| CMD51-196 — Parse nested function text without flattening it | partial | Implementation/evidence: nested function text editing/round-trip beyond bounded native framing. |
| CMD51-210 — ON ERROR handles a missing nested macro | partial | Implementation: missing-child error handling in new unsaved buffers; current loaded context passes. |
| CMD51-212 — Nested child error handler is local and parent handler resumes | partial | Implementation: nested child-local handler and parent resumption in new unsaved buffers. |
| CMD51-213 — Unhandled child macro error returns to parent handler | partial | Implementation: propagated child error reaches parent handler in new unsaved buffers. |
| CMD51-230 — File-level BREAK in the nested macro fixture is ignored | partial | Implementation: nested file-level BREAK ignored with parent resumption in new unsaved buffers. |

### Language tools

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-181 — Set a language code at cursor | partial | Resource + implementation: language-specific proof/format resources and Initial Codes, beyond US→UK native code. |
| CMD51-182 — Open and cancel the Thesaurus | unimplemented | Implementation/resource decoder: original THS lookup exists as DOS evidence and private resource fingerprint, not a product decoder. |

### Graphics, preview, printing and utilities

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-146 — Preview each original page-view mode | partial | Resource + implementation: graphics-capable page-view modes, color controls and printer definitions. |
| CMD51-147 — Changing preview colors does not change printed content | partial | Resource + evidence: view/palette changes must preserve print content across original modes. |
| CMD51-148 — Choose a declared sheet feeder | unimplemented | Implementation + compatible printer/sheet-feeder resource. |
| CMD51-174 — Create a figure graphics box | unimplemented | Implementation + WPG/graphics-resource and anchored-box semantics. |
| CMD51-175 — Convert an original graphics file with GRAPHCNV | unimplemented | Implementation + original graphics input/output fixtures and GRAPHCNV behavior. |
| CMD51-176 — Create a horizontal graphics line | unimplemented | Implementation + graphics printer/native rule representation. |
| CMD51-177 — Create and preview an equation fraction | unimplemented | Implementation + equation native structure and graphics preview/print baseline. |
| CMD51-185 — Select an installed original printer definition | partial | Resource + implementation: installed-printer selection/resources beyond Standard Printer. |
| CMD51-187 — Open and quit original Printer Program | unimplemented | Implementation/resource semantics: original Printer Program utility mapping. |

### Platform adaptation

| Scenario | Recorded status | Exact next obligation |
| --- | --- | --- |
| CMD51-189 — Run a DOS command and return to the same cursor | partial | Adaptation + evidence: interactive Linux/PowerShell shell is tested; original single-DOS-command semantics remain an explicit different behavior to disposition. |

## Main sources inspected

- `.kittify/charter/charter.md` and `charter.yaml` (WL-001–007), `docs/compatibility.md`, `docs/roadmap.md`.
- `kitty-specs/wp51-parity-01M64CVY/{spec.md,meta.json,status.json,analysis-report.md,acceptance-matrix.json,continuation.md,remaining-qualification.md,reference-execution.md}`.
- `contracts/{coverage-concordance.md,coverage-leaves.md}` and current `docs/research/mission-1-command-audit.md`.
- `docs/research/reference-environment/{README.md,environment.json,resource-profile.json}` and relevant original-run READMEs.
- Current native milestone report and infrastructure recovery report; `scripts/review_checks.py` and reference controller authorization checks.

No runtime advance, acceptance mutation, VM execution, original-image read, worktree creation, tracker write, or source edit was performed. The orchestrator may retain this report as planning evidence after review.
