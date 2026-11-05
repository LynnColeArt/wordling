---
work_package_id: WP90
title: Preserve modal input ownership across terminal resize
dependencies:
- WP76
requirement_refs:
- FR-004
- FR-005
- NFR-003
- NFR-004
- C-001
- C-002
- C-003
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T294
- T295
- T296
- T297
- T298
phase: Correct confirmed source safety defect before WP77 baseline re-review
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/model.go
create_intent:
- internal/tui/historic_resize_test.go
- internal/tui/evidence/resize-modal/**
execution_mode: code_change
owned_files:
- internal/tui/model.go
- internal/tui/historic_resize_test.go
- internal/tui/evidence/resize-modal/**
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP90 — Preserve modal input ownership across terminal resize

Read the issued prompt, project charter, permanent compatibility contract, everyday milestone plan, and preserved WP77 rejection at `kitty-specs/wp51-parity-01M64CVY/tasks/WP77-everyday-baseline/review-feedback-1.md`. The independent finding R77-001 is an unwanted document mutation, not an accepted limitation. This narrow repair runs before WP77 re-review. It does not approve the rest of the inherited candidate or complete everyday parity.

Source input is the existing integrated H candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`, or a canonically supplied descendant whose complete additional source delta is identified. WP76 is the declared approved prerequisite. WP90 may inspect and fix this known-unreviewed candidate; it must not assert inherited source approval. Missing candidate source, unexpected mutations or ownership changes require reviewed source propagation before editing. Do not add a dependency on WP77 or force a lane identifier. Pure planning computation predicts the existing H owner, but only canonical finalization/claim issues the workspace.

## T294 — Preserve and reproduce R77-001

Record issued source commit, candidate ancestry, exact owned-file hashes and the independent rejection event `01M6NV9Z0CPE615HWJBBJK38Q8`. Add a regression in `internal/tui/historic_resize_test.go` using exported `tui.Open`, `Model.Update`, `Model.View`, `State` and immutable native export, with no private field edits or fabricated completions. Independently reproduce F5 List Files and Alt+= menu: type a, open modal at 80x25, establish that x at normal size does not change the document, resize to 80x11 and render, type x, restore 80x25. The safety assertion must fail on the inherited source. Preserve the red-run output and before/after native bytes, revision, dirty state, history and visible modal evidence.

## T295 — Repair input ownership independently of rendering height

Make the smallest coherent correction in `internal/tui/model.go` so an active menu/browser cannot silently hand document input to the reducer when presentation falls below the historic-chrome threshold. Either retain modal ownership with truthful small-window presentation, or explicitly resolve/cancel the modal before subsequent editing; resize itself must never apply text. Do not globally disable editing, bypass session/native ownership, turn off historical chrome, or fake a passing fixture-specific branch. Preserve pending I/O, macro/repeat, stale-transition and existing context guards. If a safe fix genuinely requires another production file, request reviewed ownership amendment before editing it.

## T296 — Exercise both modes and resize boundaries

Assert native bytes, revision, dirty flag and edit-history state remain unchanged by modal-only inputs across 25→11→25, 12→11, 11→12 and repeated crossings. Include safe render calls, text and navigation/action keys, cancellation and resuming ordinary typing only after focus returns. Check small-window entry behavior without inventing a physical DOS geometry claim. Exercise normal public command routes and a real compiled CLI/PTTY resize sequence. Verify no duplicate or stale UI dispatch can bypass modal ownership and no pending I/O is accidentally consumed by the fix.

## T297 — Verify focused correction and resource-safe evidence

Run gofmt on changed Go files, `go build ./...`, `go test ./...`, `go vet ./...`, focused modal regression and equivalent public CLI/PTTY checks against the actual issued source and its existing admitted suites. Do not import unapproved WP77 tests or use a source overlay; author any needed focused CLI probe within this package’s declared evidence scope. WP77’s own full baseline probes run only after approved repair intake. Preserve pre-fix failure and post-fix results in `internal/tui/evidence/resize-modal/REPORT.md` and a manifest with source/dependency commits, changed-file hashes, exact commands and relevant raw output. Evidence must explain why each changed production line is needed; no copied repository snapshots or edits to baseline tests to conceal the defect. Confirm normal terminal cleanup and existing native conservation tests still pass.

## T298 — Obtain independent repair review and handoff

A different reviewer verifies the complete narrow fix, reproduces both original failing cases, checks public entrypoint regression and original native conservation, and records the actual Spec Kitty verdict. WP90 cannot pass while R77-001 remains reproducible. Approval qualifies this repair only. Hand the approved fix commit and review evidence to the orchestrator for a separately reviewed ordinary source intake into `feat/wp51-parity`, preservation checks and canonical planning/source refresh. WP77 then retries against that explicit repaired source epoch and independently reviews both the original 23-file candidate delta and this repair; its prior rejection remains durable. Do not merge/accept M1, update the user preview, alter WP77 lifecycle, or broaden this repair into unrelated TUI work.

## Review requirements

Ownership remains the three declared paths. The reviewer checks production reachability, no data mutation behind either modal, preservation of normal input/I/O boundaries, focused diff scope, failed-test provenance and source custody. Source integration is the orchestrator's responsibility. WP84 must depend on this approved repair for shared-file ordering and retain its regressions; WP86 reruns the repaired behavior in the final integrated executable.
