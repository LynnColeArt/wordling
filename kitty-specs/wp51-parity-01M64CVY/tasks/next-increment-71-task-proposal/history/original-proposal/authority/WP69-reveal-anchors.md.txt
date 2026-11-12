---
work_package_id: WP69
title: Bounded 80x25 editing and Reveal Codes display anchors
dependencies:
- WP66
requirement_refs:
- FR-004
- FR-005
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T205
- T206
- T207
phase: Small H-only M1 Reveal anchor increment; full geometry and M1 remain open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/
create_intent:
- internal/tui/reveal_anchors_test.go
- internal/tui/evidence/reveal-anchors/
execution_mode: code_change
owned_files:
- internal/tui/**
role: implementer
tags:
- m1-continuation
- reveal-codes
- bounded-display-anchors
task_type: implementation
tracker_refs: []
---

# WP69 — bounded editing and Reveal display anchors

WP69/T205–207 deliver the bounded H display increment. E68/T202–204 and E70/T208–210 are separate packages, not H dependencies. The only direct dependency is genuinely CODE-approved WP66; this transitively retains H62/60/52/48/37, G65/47 and their approved source contracts. No P64, E68/E70 or unfinished source is consumed. Implementation follows normal independent TASK review, canonical validation/finalization/full snapshot/refresh/fresh CURRENT analysis and the actual issued claim.

## Evidence, current source and exact scope

Resolve implementer-ivan and action implement governance at actual claim; read applicable AGENTS, actual mission spec/plan/continuation, docs/compatibility.md and docs/roadmap.md. Read actual approved H66 commit66a65d4b311d81ab2699c9725a24d77cea3e7271 and G65f110c5a7e113b063081879ea491c1dde5bf79aed, H52 active ranges and H60 partial inspection contracts and independent reports. Verify actual claim source, public interfaces and compiler input closure; a planning HEAD or VCS stamp is not proof source installation. Missing source/API is a precise blocker, never permission to copy source, replace modules or add a core API.

Independent planning input is the literal seven-file product-priority packet, root SHA16c6a7eb4cfdee3ad6078ff70cd220a0c0f6de0727b5a7af9ffac8ac46ed92e4, REPORT SHA56e60c3d0d6e9ede79c714be7220d0a5daaf12074499f30041c4330a9dfaf85b. Its complete source-proof.json binds85 immutable Git entries, including28 original public4000-byte VRAM captures and28 cursor observations from WP13 commit18d6afe95ffcd676fc3f9e964dcad884c9a8c289. Two fresh original runs each cover seven native gaps in normal and Reveal modes. Preserve the literal packet and metadata-check-failure: footer originally guessed35/45, actual checked bytes are36/44. This task consumes accepted public capture outputs only, not a new reference run or permission to read original/private assets.

The current real entry is UNMODIFIED cmd/wordling→tui.Open→Model.Update/View. H66 View currently puts branding row0, actual normal/caret row1, Reveal banner row2 and lower stream row3. Source-backed originals put normal/caret row0, lower stream row13 and Reveal footer row24. This WP changes those anchors in a narrowly admitted healthy80x25 editing view. It does not introduce layout/formatter/status engines, general wrapping or scrolling, a viewport framework, ruler, native formats, parsers, writers or a second document model. Existing partial readonly [HRt]/[HPg]/unknown-owner inspection already exists in59/60; do not implement or qualify it again.

Own only the five EXISTING H production/docs files and the two EXISTING affected tests reveal_cursor_test.go and editable_test.go enumerated in the execution allowlist below (honest amendments), genuinely NEW reveal_anchors_test.go, and genuinely NEW evidence/reveal-anchors/**. There is no create intent for existing H source/tests. The two existing tests may change ONLY superseded healthy row/caret/branding expectations and supplemental test-local coherent frozen-layout capture setup required by this view change. Retain every native-byte/source-span/token/active-role/clipping/EOF/reducer/history/save/IO assertion; preserve row3/Y1 where fallback still applies, including partial/virtual/error/non80x25 contexts. No global3-to13 replacement, fixture/hash/path/test-name recognition, skipped assertion, or golden-file normalization. In editable_test.go replace only the obsolete healthy branding assertion with an actual healthy anchor/no-branding check; its active/inactive Typeover assertions remain intact. All other H tests, including menu_bar_test.go and its complete body/caret/menu/refusal/restore assertions, remain byte-exact. Keep all other H code/old raw evidence, cmd/main, input/decoder, G/editor, E/document, storage/native/macro, Python startup/controller/resource code, Go modules/dependencies, public original fixtures, canonical contracts/status/registry/spec/plan unchanged. A necessary extra file/API is a scope question to report before widening. No original/private program/manual/SET/PRS/font/boot/master/failed-HD/resource inspection/stat/exec, VM/QEMU, PID/grant/ledger action or physical qualification is authorized.

## Ownership representation and mandatory execution allowlist

The frontmatter uses the SAME legitimate existing H namespace granularity as approved66: `internal/tui/**`. This is routing ownership, NOT expanded write authorization. The normal finalizer resolves MAIN planning-only repo_root even from lane H; seven approved existing source/test literal paths are genuinely absent there and hard-error, whereas the established namespace may yield a zero-match SOFT WARNING. Retain that exact warning and the old literal-failure raw evidence truthfully. A mechanically accepted namespace does not establish source installation. No historical existing file becomes create_intent; no placeholders, source overlays, per-filename wildcard disguises, alternate validation root, host repair or topology change is permitted.

The following JSON is the closed semantic execution allowlist; copy it EXACTLY into the proposal manifest's H69 execution_allowlist and check actual changed/new path sets against it. Only these seven existing amendments plus one NEW test and NEW evidence namespace may change. Before/after verify every other inherited H pathSET/Git blob/working SHA unchanged; no unrelated test/evidence edits or deletion/rename. Existing-test narrow geometry/branding/frozen-setup restrictions above continue to apply. Assert actual approved66 H source presence/hash and genuine new-path absence against actual dependency source separately from planning-root routing glob checks. Missing actual source is a blocker, never creation permission.

```json
{
  "schema": "wordling.H69-execution-allowlist/v1",
  "routing_ownership": [
    "internal/tui/**"
  ],
  "amend_existing": [
    "internal/tui/model.go",
    "internal/tui/reveal.go",
    "internal/tui/reveal_inspection.go",
    "internal/tui/macro_model.go",
    "internal/tui/README.md",
    "internal/tui/reveal_cursor_test.go",
    "internal/tui/editable_test.go"
  ],
  "create_files": [
    "internal/tui/reveal_anchors_test.go"
  ],
  "create_namespaces": [
    "internal/tui/evidence/reveal-anchors/"
  ],
  "protected": "Every other inherited H file/source/test/evidence remains exact pathSET/Git blob/working SHA; no deletion/rename or write outside this execution allowlist.",
  "historical_source": "66a65d4b311d81ab2699c9725a24d77cea3e7271",
  "new_path_absence": "Prove actual approved H source presence and genuinely NEW path absence independently of planning-root glob matches."
}
```

## T205 — source-consistent anchors in the actual production view

1. Retain the first authentic Update/claimUI/input/reducer/async handling; this is rendering, not new command dispatch or authority. Select the SAME visible frame/source before choosing geometry. State/View observations remain read-only and cannot claim/advance UI transitions, perform filesystem IO or derive permission from displayed text. Retain Present token identities/spans, current opaque native Revision versus integer reducer Revision, clipping and all existing errors.
2. The new layout applies only at exact80 columns ×25 rows, ordinary Editing, successful supported native ASCII/Bold presentation, with a current initialized non-stopping UI/runtime, no selection/history/modal/repeat-entry/Typeover, no active/pending/deferred macro or IO/first-save ownership, no suppression or genuine prompt/notice/reconciliation. The menu-capable pristine startup context is an explicit legacy-base exception BOTH before showing and while showing the menu: choose its SAME existing baseline geometry independent of the shown flag/own menu diagnostic, then overlay only the existing row0 menu. It never enters anchors merely because the menu is hidden; this preserves the qualified body/caret invariant without a layout jump. Use the existing source-authenticated menuReason/menu availability observation on the actual current Model: its pristine genesis/source/revision/screen/IO/macro/runtime/size guards, not fixture/test/name matching; shown flag and own menu diagnostic do not select a different base. This is read-only and must not claim UI or perform IO. Menu availability/admission and key dispatch are unchanged. Document this pristine-startup legacy exception explicitly in README. Existing completed macro facts alone are not active work; they remain available in State. Do not infer source freshness by new IO. Partial inspection/error/source-stale/unknown-size/other modes keep the existing truthful bounded fallback; never suppress their actual prompts/refusals/uncertainty to enter the new layout. Preserve existing fallback content/caret and disclose in README that anchor parity is only this admitted slice.
3. In the admitted normal view, place the actual authoritative normal stream and its ordinary text-width caret at zero-based row0. In admitted Reveal, retain that SAME row0 upper stream/caret and place the actual authoritative lower styled stream at row13. Do not use label width as normal caret width. Native Bold labels, ASCII and real EOF retain H52 roles and source-span identity; literal ASCII `[BOLD]`/`[bold]` remains characters. Do not recognize fixture name/hash/text, paste measured frames or static native outputs, or construct a shadow stream from raw native bytes.
4. In admitted Reveal, row24 is exactly80 cells: `Press Reveal Codes to restore screen` (36 ASCII bytes), then44 spaces. Use existing logical role map: half-open columns[0,6)=0x17, [6,18)=0x1F, [18,80)=0x17, with explicit SGR/reset containment. These are logical Linux roles, not RGB/raster/palette/physical keyboard parity. The footer is UI wording, never native content. Toggle-off removes it and the lower stream without leaving stale cells; retain actual row0 normal stream/caret.
5. Remove implementation-only branding/gap/revision/history/profile lines from the admitted clone-content area, leaving their actual existing State/Session diagnostics intact. Keep physical delivery UNQUALIFIED in State and documented. Do not remove real errors/prompts/uncertainty from any mode, reset state to hide them, or replace them with cosmetic success. Rows11/12 have no qualified ruler/status algorithm: leave unused cells as neutral host blank space in this slice, explicitly unqualified as original blank rows. Do not paste captured Pg/Ln/Pos, path, braces or triangles; no new inferred metrics or normal-mode fake footer. Reserved blank padding is view-only.
6. Preserve4096-token/native presentation bounds, existing horizontal clip semantics and64KiB partial-inspection expansion bound. At exact80x25 compose at most25 rows of at most80 visible cells plus bounded ANSI, preflight before allocating/filling. Outside this size preserve resize normalization1..4096 and existing bounded fallback. This is no scroll/window-height/wrap/pagination algorithm and no whole-screen oracle.

## T206 — preserve frozen, virtual, menu, source and IO contracts

Use the already selected frozen display as a whole before live geometry/inspection/style decisions. DISPLAY OFF must retain the SAME captured normal/reveal/error/inspection/caret and any relevant layout choice; never restyle frozen strings using a live gap or live eligibility. Resume/terminal/error transitions reveal actual current state according to existing macro rules. Where necessary extend existing owned macroPane capture coherently, without new live source reads, callbacks or authority. Actual Update/worker/deferred IO/HostStop/Close settlement stays reachable.

Menu H62 remains its exact80-cell row0 display, authentic Alt+= shown refusal/hide and ordinary row restoration. It never becomes an action menu or auto-dismiss-and-run. For the menu-capable pristine startup exception select the unchanged legacy base with ordinary document caret row1, whether hidden or shown; replace ONLY row0 on show. All rows1–24 and the caret must remain identical across the initial toggle, and hide restores the whole actual pre-show frame. Its own unsupported-action diagnostic retains the existing prompt slot/precedence without changing base geometry; genuine external notices/errors remain visible. No document/history/IO reset or weakened menu test is allowed. When actual typing/retrieve legitimately leaves pristine menu eligibility, the ordinary healthy Insert context may use anchors; menu availability cannot be regained by clearing state. Typeover always uses the truthful legacy fallback with its actual visible Typeover indicator, not anchors or a new inferred status/ruler. Insert return may restore anchors only if all other admission predicates genuinely hold. Modal/name/question/history/selection/typeover/pending/late/detached/first-save/unbound/reconciliation and partial HR/HP contexts retain existing semantics and truthful visible notice precedence. No new eligibility gate may silently swallow the async replies or change command admission. Test current/stale/foreign Model/source wrappers as observations without pretending old value renders acquire current authority.

Through repeated View/State, AltF3/right/left/toggle/resize compare full native bytes, Source identity, native/reducer revisions, gap, dirty/saved/name/publication/Birth, selection and history knowledge against actual legitimate reducer transitions. Navigation may legitimately change reducer grouping/history knowledge; rendering must not fabricate resets. No view-only padding/SGR/EOF enters native bytes/history/IO. The same source/revision anchors all compared rows. Successful native no-edit Save As through the real app remains byte-identical under approved storage rules; retain genuine New→first-publication→Read-binding and post-macro first-save regressions, without changing writers or qualifying new originals.

## T207 — public Model and real unmodified executable acceptance

Freeze the public fixture/source/expected-row/role/caret map and finite commands before positives. Revalidate immutable source-proof entries and both runs'28 VRAM/cursor pairs directly; no new original execution. The334-byte ORIGIN witness has actual spans A324+1, BoldOn325+3, B328+1, C329+1, BoldOff330+3, D333+1. Seven gaps0..6 map upper columns0/1/1/2/3/3/4 and lower active ranges A[0,1), BoldOn[1,7), B[7,8), C[8,9), BoldOff[9,15), D[15,16), EOF[16,17). These are source associations, not hardware-cursor-alone token inference.

Required verification layers:

- Real public Open/rooted Retrieve/Cmd/reply/Update/View/State test traverses all seven gaps forward AND backward with ordinary AltF3/right/left/toggles. Compare decoded actual rows0/13/24, complete80-cell footer/padding/logical role spans, actual upper caret and lower active ranges against BOTH independent original runs. Check normal toggles and no stale row/footer cells. State/source/native/IO assertions use genuine public observations, not private injection. Only sourced anchors/cells are original comparisons; do not label the unsourced blank/status rows or full2000cell frame as original equality.
- Freshly build UNMODIFIED cmd/wordling from the actual final source/Go module closure and run at least two independent80x25 real PTYs, each through real decode→Retrieve→AltF3→seven gaps→reverse→toggle→ordinary safe exit. Decode raw ANSI into bounded terminal cell/style/cursor facts; substring-only assertions or renderer-only/synthetic terminal positives cannot pass. Compare linked source/binary/toolchain/argv/GOMOD/go-list packageDirs/GoFiles/compiled inputs and output hashes. PTY witnesses visible cells/caret/terminal/files only; it cannot claim inaccessible Model/receipt/history telemetry. No debug flag/input alias/observer hook is added.
- Independent non-ORIGIN printable/literal bracket and distinct Bold-bearing accepted public fixtures kill fixed-output/hash/path recognition. Zero/empty EOF, adjacent/repeated accepted codes, clipped label and4096 boundary cases retain source identity and approved fallback; no unsafe synthetic native editing is needed. Selected/history virtual overlays, native-source-stale and genuine partial HR/HP/unknown inspections remain their current behaviors, never newly active. Width/height1,79x25,80x24,81x25,80x26,80x25→other→80x25 test fallback and restoration with bounds, no fake metric claims.
- Preserve real menu show/refuse/hide with unchanged full body/caret and whole-frame hide restoration in its explicit pristine legacy-base exception; prove actual pristine startup→first ordinary ASCII edit legitimately enters anchors (with real revision/genesis/menu-unavailability changes, no synthetic state reset), and actual Insert→Typeover visible fallback→Insert anchor restoration without state/IO reset. Preserve real macro DISPLAY OFF frozen frames/inspection/caret including resize, loaded and New root macro execution, prompts/name caret/IO/first-save/deferred/uncertainty paths using existing public tests and meaningful added cases. Structural-only arrangements are labeled supplemental, not user reachability. Run full native no-edit app save/readback plus existing New first-save regression; complete source bytes are compared, not a prefix. No native writer/original qualification claim arises.
- Finite actual-owned-source mutants must compile and execute the intended public/PTY consumers: restore row1/row3, move footer to23 or use35+45, omit footer keyword role/reset, use lower width for caret, replace actual stream with fixture text, choose live gap/style/geometry during suppression, suppress a genuine error to gain eligibility, or leak view padding into output. Test the reachable semantic effects; failed compilation/construction is not a kill. Use selected relevant falsifiers rather than a broad campaign; preserve every actual survivor/failure and source hashes.

Run real gofmt/scoped source lint, actual discovered build/go test ./.../go vet ./..., focused H/editor tests, race and all configured7 with true package discovery. An inapplicable check is reported exactly, never guessed success/blanket skip. No unchanged parser fuzz or source-controller/original campaigns. Each PTY<=30s plus2s owned TERM/KILL/reap; live retained wire/output<=2MiB checked before append; Model case<=4096 explicit events; individual Go/configured command<=300s; new H evidence<=512files/8MiB including raw history/nested seals. Record actual elapsed/owned-process cleanup and bounded render/allocation measurements, not original DOS capacities or hard-real-time/sandbox assurances. Exceeding a bound or missing API is a stop/report, no truncation or silent scope/cap expansion.

## Completion and independent review

Before edits capture clean claim HEAD, complete inherited H/source/protected tests/Go module SET with actual Git blobs and working SHA, approved66/G65/source context and current installed currency callback. None means NOmerge. Non-None requires exact classification/ROOT resolution before any merge; no force/reset/rebase/overlay/source copy/dependency reentry. At freeze bind actual changed source/test/compiler/binary/fixture bytes, complete old protected SET and every evidence file. Current recursive root seals include ALL nested historical seals and exclude ONLY the exact root manifest. Keep raw failure/typed refusal/mutant outcomes and original-vs-host comparisons honest.

Commit only explicitly owned H paths, then STOP for ROOT's canonical quietpoint before marking T205–207 or normal for_review with actual mission/codex/implementer-ivan. No self-review, manual state/Op/host repair, push or accept/merge. Independent CODE reviewer receives exact source, source-consistent publicModel/actualPTY comparisons and transparent remaining limits. Full38 obligations/91groups/36lessons/nested SC001–005 stay open; approved WP does not imply full Reveal/layout/physical/M1 completion. M2/PDF remains gated.
