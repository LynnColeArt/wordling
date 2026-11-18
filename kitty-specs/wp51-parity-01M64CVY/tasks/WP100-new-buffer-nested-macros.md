---
work_package_id: WP100
title: Admit authenticated nested macro reads on current New buffers
dependencies:
- WP65
- WP66
- WP82
- WP69
- WP71
- WP73
- WP76
- WP84
- WP85
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- FR-012
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T326
- T327
- T328
phase: New-buffer nested source composition; original New-buffer qualification remains WP102
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/macro_execution.go
create_intent:
- internal/editor/new_macro_nested_test.go
- internal/editor/new_macro_nested_internal_test.go
- internal/tui/new_macro_nested_test.go
- internal/editor/evidence/new-macro-nesting/
execution_mode: code_change
owned_files:
- internal/editor/macro_execution.go
- internal/editor/new_macro_test.go
- internal/tui/new_macro_test.go
- internal/editor/new_macro_nested_test.go
- internal/editor/new_macro_nested_internal_test.go
- internal/tui/new_macro_nested_test.go
- internal/editor/evidence/new-macro-nesting/**
role: implementer
tags:
- m1-continuation
- draft-unreserved
- new-buffer-nesting
task_type: implementation
tracker_refs: []
---

# WP100 — authenticated nested source composition on a New buffer

PROPOSAL ONLY. Tentative IDs checked against f1ca9686febe3868fc5c344ba0f7f9d24ba201b9: existing WP01–99 and T001–325 stay unchanged. Root must independently review/finalize this append and issue the normal implement prompt before code work. No old approval is overwritten or interpreted as general New macro parity. Resolve implementer-ivan and current implementation governance. Read the mission spec, compatibility contract, continuation, this proposal's rationale and exact issued claim.

The actual product gap is the `r.target != nil` refusal in `macroExecutionState.Resolve`. Loaded execution already uses the native VM, rooted ReadMacro, private acquisition proofs, serialized Resume and authentic missing-file CommandError handling. New admission already captures private Birth/genesis/buffer/screen/transition authority. Compose those existing seams for current New targets; do not create a second VM, filesystem reader, mutable Session surrogate or direct native writer. This deliberately supersedes only the old root-source-only New limitation. Other scope protections remain unless separately reviewed and amended.

## T326 — demonstrate the gap through real New Session/Runtime paths

Add four failing, source-hash-bound tests using the actual original-cases.json WPM exports for CMD51-210/212/213/230. Reach a genuinely initialized NewUnpublished buffer via normal constructors and public Macro prompt/read/Complete/StartMacro. Do not retrieve EMPTY.WP, parse an empty file, inject a loaded source or delete a loaded document to simulate New. Use actual ExecuteMacroRead for every root/child/missing result. Show the existing New-only resolver refusal causes the intended failures. Keep loaded paths as regression controls.

Initial positive scope is pristine New Doc1, Repeat1, plus the ordinary edited New workspace path already admitted by CanRunWorkspaceMacro (a nonempty unsaved ASCII receiver at its real caret, Repeat1, no selection/Reveal/typeover). Existing source restrictions on otherwise unsupported New contexts, Repeat3, arbitrary nested grammar and workspace UI commands are not silently broadened. Those remain explicit M1 follow-ups.

## T327 — reuse authenticated child acquisition and the same serialized owner

Permit nested resolution for a still-current New macro target, preserving the same r.valid/current/expected-transition checks before/after every step and Resume. Root-only target.unedited checks must continue to guard root acquisition; a legitimate root/child edit must not be mistaken for a stale root acquisition. Bind each child request/result to its accepted operation/revision/run/request/parent, rooted directory/name, actual buffer and screen, source identity and current execution owner. Reuse `newMacroReadProof`, `ExecuteMacroRead`, `acceptedMacroResult` and actual VM Resume. Only a genuine rooted missing observation becomes CommandError; fabricated missing wrappers, permission/host I/O errors and wrong-source results must not acquire original ON ERROR semantics by convenience.

Preserve all already-applied native text/dirty/history on terminal errors or host stop, release one owner once, and preserve NewUnpublished/no-source/no-name/no-false-save state until actual first publication. Child-local handler, unhandled child propagation, parent handler resumption and nested file-level BREAK use the existing VM, not case-number/source-name switches. Production source edits are limited to macro_execution.go. The two named existing test files may receive only the contract updates described in T328. If an actual defect demands changing new_macro.go, macro_load.go, macro_session.go, Runtime or native/storage APIs, report the exact failing case and obtain a reviewed source amendment from the orchestrator; do not weaken a guard or expand ownership implicitly.

## T328 — public integration, adversarial provenance and first-save checks

Use both captured repetitions' source inputs where available and slice quotas 1 and16. For pristine New receivers, assert exact bodies HANDLED, PCHILDRPARENT, PCPARENT and PCCHILDBADRDONE. For edited New receivers, declare initial bytes and caret and assert the entire resulting receiver, preserving the initial text around inserted output; assert real caret, dirty/native revision and unchanged Birth/genesis, New phase/source/name, source WPM bytes, execution completion, parent/child receipt provenance and no duplicate application. Cover child request/source/name/root/parent/run/screen/revision/operation tampering; swapped result from another driver or buffer; stale pre-edit Session/fork replay; duplicate/out-of-order Resume; pending child cancellation/host stop; host error versus real not-found; and unsupported names refusing without mutation. Preserve existing loaded, new root, ownership/fork/ready/first-publication regression suites.

Replace the obsolete unconditional New-NEST refusal assertions in TestNewMacroNestIsHostFailureBeforeChildIOAndPartialEffectsRemain (internal/editor/new_macro_test.go) and TestNewMacroNestPartialHostFailureAndStaticUnknown (internal/tui/new_macro_test.go) with authenticated child-read/resume/result behavior. Preserve their setup, actual prior effects, dirty/native state, source/name identity, completion/receipt accounting and duplicate rejection. Preserve the UNKNOWN static-preflight zero-effect refusal unchanged. Retain actual host-error/cancel/partial-effect negative coverage through a real rooted host I/O error or cancellation; a valid child call must not be used as a fabricated host error. No deletion, skip/xfail, fixture-name special case or weakening of unrelated tests.

Reach the four workflows through public Runtime Open/Model.Update/Cmd using the actual rooted temporary files. Save through normal F10/ExecuteSave, reopen through normal storage/editor and prove exact native body, unchanged source WPMs and truthful save receipt. Include an existing-other-screen sentinel on the already admitted workspace path where constructible; otherwise retain the existing other-screen refusal and report that positive variant as uncovered. Do not fake Doc2 coverage. Original WP reopen/edit/print belongs WP102.

Run focused editor/TUI tests, focused race tests covering asynchronous ownership, full `go test ./...`, `go vet ./...`, `go build ./cmd/wordling`, gofmt and git diff --check. Freeze candidate/source hashes and independent review evidence. No mutation-surrogate test is required where the existing real negative cases already prove the seam; any selective mutation probe must demonstrate a meaningful provenance guard.

## Independent acceptance

- All four New product workflows pass through authentic I/O and the real reducer/Runtime, and loaded equivalents retain exact prior outcomes.
- The first source-only refusal is resolved without relaxing root freshness, constructor identity, pending result authentication, history or first-save guards.
- Negative results preserve actual state and never synthesize success or ON ERROR for unauthenticated I/O.
- Tests/build/vet/race/format results and exact commit are recorded; independent reviewer can reproduce without a VM.
- CMD51-210/212/213/230 remain **partial** in the canonical command audit until WP102 has actual fresh unsaved-New original comparisons. This WP may be approved as bounded product delivery while full M1 and original New-context qualification remain open.

No VM/original image access, archived source edits, canonical audit/matrix promotion or changes outside owned_files are permitted by this WP. Evidence namespace is new. Existing source fixtures are read-only provenance, not new permission to distribute private media.
