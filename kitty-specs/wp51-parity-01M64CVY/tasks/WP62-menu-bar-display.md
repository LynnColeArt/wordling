---
work_package_id: WP62
title: Alt+= top menu-bar display in the evidenced idle blank context
dependencies:
- WP60
- WP16
requirement_refs:
- FR-004
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
- T184
- T185
- T186
phase: HOST top-row display subset only; no menu action/caret/native permission
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/
create_intent:
- internal/tui/evidence/menu-bar/
execution_mode: code_change
owned_files:
- internal/tui/**
role: implementer
tags:
- m1-continuation
- menu-bar-display-subset
- temporary-unreserved-proposal
task_type: implementation
tracker_refs: []
---

# TEMP WP62 — evidenced Alt+= menu-bar display subset (T184–T186 NOT reserved)

TEMP task-design proposal ONLY, based on actual clean52be43d3d59983aa051b1eac9bf8714db6f8e51b/planningb31cbfd16a8a0ee247a89372e88caa663ce15c93. NEW independent TASK review, current-baseline verification, canonical normalize/fullsnapshot/refresh, separate CURRENT62 analysis and normal issued claim remain required. No code from this proposal. Preserve actual corrected WP61 narrow appended successor clarification and active contracts/startup-family-successors.md (15th contract) exactly; it supplies no menu semantics or P dependency. Actual H60 is APPROVED source0a8fdec27916c4379b8372b52becd9ff895952b3; P61 is in_progress metadata only, NO P61 code/semantics/dependency is used. Full38/91/36/nestedSC001–005/M1 OPEN; queue exhaustion/NEXT preview accept is not acceptance; M2/PDF gated.

Read AGENTS/actual charter/spec/plan/session and input contracts, adjacent exact recon+integration supplement, source-proof and immutable approved H60 source. This is a useful original-evidenced DISPLAY subset of WP51-001/CMD51-001/FR-004, NOT full menu subsystem/command/focus/caret/full-screen or completeFR acceptance. Two public original smoke02/smoke03 sequences qualify only idle blank-document80×25 bar cells/show/hide. Smoke02 archive limitation remains explicit; smoke03 runner provenance is retained. No original run/native before-after/cursor/CRTC proof is newly claimed.

Harddeps ONLY60 (actual H implementation and ordering) and16 (actual delivered-input contract). H60 inherits52/47/37/E59 source as existing source closure, not a new E dependency. No P→H or E→H backedge, no unreviewed/moving P61 input. Own ONLY internal/tui/**, genuinely new internal/tui/evidence/menu-bar/** as create_intent. Existing model.go/runtime.go/reveal.go are existing approved H files absent on planning primary, NEVER falsely create_intent. Dedicated new menu_bar.go/_test.go may be authored under the real H package. Do not change cmd/wordling, input decoder, Go module/dependency, editor/document/storage/native/format APIs, old fixtures, oldH60 raw evidence or canonical conformance/registries. All former H functionality remains. No product facade/mock/overlay implementation to pass tests.

## T184 — current idle-context admission and exact delivered-key routing

Use actual Runtime.Open→editor.New initialized startup buffer; zero/nil Model/Session/Document never represents the oracle. Proposed admitted context is exact80×25, current non-stopping runtime/authentic UI token, actual Doc1 Editing/NewUnpublished, source nil, nonzero native GenesisRevision equal NativeRevision, token count0/gap0, Session.Revision1, no name/draft/original/prompt/session/H notice/reconciliation/publication/receipt/first-save state beyond untouched constructor. Require Insert mode/no Reveal/selection/history preview, MacroRepeat1/no Repeat-entry. Require actual pending/detached/unsettled/first-ticket/deferred/worker/ticket/CPU/active-or-other-model macro and DISPLAY-suppressed/frozen state all idle, not just Pending==nil. Use the approved public snapshots/document observations and existing H private orchestration, not new G/E accessors or native serialization/byte guessing. Preserve actual constructor dirty/history defaults by before/after equality; NEVER assume Dirty=false or history qualification from absence. Source proof identifies constructor fields and actual UI/IO ownership.

A private shown/closed display overlay is sufficient; bind it to the same current runtime/UI/session/native genesis. State/View are pure observations, never claim/advance UI authority, reduce editor state, dispatch IO or manufacture genesis. Preserve Model.Update's original claimUI boundary. Stale copied Models cannot acquire/show a new menu or influence the authentic token. State diagnostic data must be copied values, not exported mutable authority. Read-only menu diagnostics may be added to H State if needed, with Visible/Available/Reason clearly HOST-only; no native or physical qualification.

Admission identity is EXACT input.Translate Press, primary Code='=', Mod==Alt only, IsRepeat=false, Text either empty or exactly '='. ShiftedCode/BaseCode remain passive delivered metadata: neither can substitute for a different primary Code nor be rewritten. A primary'=' with shifted'+' or nonzero base is admitted only because PRIMARY/mod/text qualify, not by inferring a physical key; primaryother with alternate'=' is refused. CapsLock/Shift/Control/Super extra modifiers, mismatched/multirune associated Text, release/repeat/paste/unknown/capability/mouse/focus events never toggle. Do not concatenate Escape+equals, strip Alt into reducer text or modify input/terminal decoder. Bare'=' retains approved ordinary typing only while bar CLOSED. Physical delivery remains UNQUALIFIED.

While shown, intercept ALL other press inputs BEFORE macroKey/resolve/reduce: arrows/letters/Enter/F1/F3/F7/Escape/Save/Retrieve/Reveal/Repeat/etc cannot edit native text, dispatch IO, change mode/repeat or invent submenu/help/cancel. Exact qualifying Alt+= is the only hide action in the witnessed recipe. Preserve normal nonpress/lifecycle behavior. Host shutdown/actual replies/deferred/stop/close always retain their existing routing authority BEFORE overlay handling; changed external state invalidates/hides overlay and clears only its own data, never swallows a receipt or touches another macro's authority. Current H60 chosen-visible frozen frame precedence wins before any live bar/diagnostics. No live bar over DISPLAY OFF.

Resolve refusal separation explicitly: store own bounded HOST menu diagnostic separately from session.Prompt/session.Notice/m.notice/reconcile. After an unsupported press, say 'Menu bar display only; Alt+= hides; action unsupported' ONLY in the already-present EMPTY Editing prompt row2, never insert a row or overwrite a nonempty application prompt/notice. The exact two-toggle baseline adds no diagnostic. Closing clears only own diagnostic and restores the original HOST frame; do not clear authentic application state to regain eligibility. In excluded Alt+= contexts, preserve native/session/IO and required frame; expose a copied HOST unavailable reason, and render it in existing empty prompt slot ONLY if safe—otherwise authentic current prompt/notice wins unchanged. Other key behavior when closed stays approved. No string matching of notice contents as eligibility/authority, no second editor/session state machine.

## T185 — exact logical row0 overlay, restoration, dimensions and styles

At admitted80×25, show EXACT80 ASCII cells:

`File Edit Search Layout Mark Tools Font Graphics Help        (Press F3 for Help)`

Logical VGA47 columns0–3;74 columns5,10,17,24,29,36,40,49;71 every other cell. These are ZERO-based columns, including all spaces/trailing cells. Actual Font accelerator is 'o' at36, not guessed 'F'. Logical Linux ANSI map is fixed:71→ESC[22;34;47m,74→ESC[22;31;47m,47→ESC[22;37;41m, ending full reset. Do not reuse native Reveal-active styling as authority, translate attributes into RGB, or claim font/raster/palette identity. Decode styles into80 logical cell roles in tests; substring/heading tests alone are insufficient.

Current row0 branding is replaced, NEVER insert a row. Row1 document/error and every later approved row/cursor retain their positions/content/styles on the unmodified two-toggle path; preserve chosen visible frame/copy semantics. H off-state restores its exact prior heading/frame, not original's blank row0. This explicit HOST presentation difference means no all-screen original match claim. Hardware caret visibility/position was NOT captured; preserve current HOST Cursor by nonmutation and test it only as HOST behavior. Do not alter native movement/presentation/admission or compute Pg/Ln/Pos/units/geometry.

Only80×25 admits entry. At any other dimensions, decline display rather than stretch/wrap/clip it as qualified. A resize while shown hides overlay/own diagnostic BEFORE usual baseline View recomputation, with zero reducer/IO effects; do not add rows/style bleed. Return to80×25 permits entry only if pristine eligibility still holds. Existing1..4096 dimension normalization stays unchanged; zero/one/tiny/79/81 widths and24/26 heights are explicit safety tests. This resize policy is HOST-only, NOT an original observation.

## T186 — real public Model plus unmodified production PTY, adversaries and custody

Freeze original public inputs/source/argv/env/cwd/expectations and finite resources before positive runs. Read-only comparator must verify original run-manifest SHA/size for BOTH iterations' before/on/off screen/VGA/status objects, derive all80 text+attribute cells from actual4000-byte buffers, prove before==off whole4000 and rows1–24on unchanged. guest-status pause metadata is not cursor/CRTC/native gap. Preserve smoke02 provenance limitation. These public observations contain no native save before/after. Do not redistribute proprietary program/manual/SET/PRS/font/master bytes or inspect private resource/failedHD paths.

Public Model acceptance MUST start through actual Runtime.Open on owned disposable directories and exercise real delivered tea/input events and actual View/State/Session/Runtime.Completed, not directly call a private renderer or set a bool. Before/on/off compare editor/native revisions/genesis/gap/source/dirty/history/name/mode/save/publication/first-save fields, receipt counts and returned Cmd absence; no native export or filesystem side effect. Actual document/session source snapshots remain immutable; returned diagnostic mutation cannot change authentic behavior. Full frame row1+ and HOST Cursor unchanged on two-toggle sequence. Real current/stale/zero/closed runtime, loaded/nonblank/edited-then-empty, first-save questions/tickets/retry/detached/reconciliation, Doc2/selection/typeover/Reveal/history/Repeat/macro/worker/DISPLAYOFF states must be reached via actual public actions where reachable. Existing async source/ownership regressions remain. Unsupported shown presses cannot fall through to any editor/macro command. Aliases and resize/attribute/cell-boundaries/refusal diagnostics must exercise actual routing.

A SEPARATE fresh build of unchanged cmd/wordling production entrypoint and actual PTY proves actual terminal decode→Model→render at80×25, exact row0 role cells/on/off/host heading restore/no shifted body, terminal restore/clean exit and disposable-directory no-created-file effects it can observe. No modified product, test-only flags/observer, module overlay, injected fake state or posthoc frame. Public Model proves private snapshots; PTY does NOT claim those internals/IO tickets. In-process tests do NOT prove production decoder/caller wiring. Record actual cwd/GOMOD/go-list packageDir/GoFiles/module+source hashes, binarySHA and executed argv; do not treat an automatic Go VCS stamp as compiled-source authority. Compare logical styles with a bounded ANSI cell parser, retain exact raw PTY and failure outputs; no normalization of raw/original bytes.

Meaningful actual-source mutants must kill wrongrow/style/accelerator/cell, inserted-row or hidden required notice, key alias/Altstrip/release-repeat/CapsLock, shown-input fallthrough, missing pristine/currentUI/pending/macro/frozen predicate, incorrect frame restore/style reset and resize gating. Preserve initial survivors and strengthen probes; do not count import/build failures as semantic kills. No trivial implementation-mirroring tests. At least one actual public Model test and production PTY must fail if bar integration is deleted, not merely assert literal golden data.

Run actual configured7/discovered Go build/test/vet/race, gofmt/source compile/scoped lint, targeted bounded package/resource checks and relevant oldH60/52/37/47 regressions. No unrelated long parser fuzz/native reader budgets. Freeze bounded roster: each PTY<=30s+2s TERM/KILL/reap cleanup, no new originals; each Go/configured command<=300s with actual target/exit/elapsed; evidence metadata<=512files/8MiB with raw diagnostics under it, otherwise STOP/report, no truncation or unreviewed cap expansion. Limit test-only Model loops/events≤4096 per case and PTY retained stdout+stderr≤2MiB per case with explicit overflow refusal/cleanup, no capture-then-slice. Document actual RSS/process/FD observations and no hostile-sandbox/hardRT claim. Only owned disposable HOST processes cleaned; no original oracle/guard/private ledger/VM/QEMU ever in this task.

Commit only actual H source/tests/evidence. Recursive current source/evidence seals include ALL nested historical seals, exclude only exact root manifest. Pin actual immutable H60/input/G/E closure and changed files; preserve old H/input/G/E/Go module/contracts/old evidence except genuinely owned H implementation changes. Old source hashes/history stay historical; no current conformance status/parentFR/fullM1 promotion. Request ROOT primary quietpoint BEFORE T184–186 status/history/ONE normal for_review explicit codex/implementer-ivan/mission. Poll whole synchronous gate/CLI; no force/skip/bypass/kill/retry/manual status repair/selfreview. Independent code review required; no accept/merge/push/original grant. Insufficient facts/API/scope must be reported, never solved by hidden G/E/native widening. FullM1 all38/91/36/nested OPEN.
