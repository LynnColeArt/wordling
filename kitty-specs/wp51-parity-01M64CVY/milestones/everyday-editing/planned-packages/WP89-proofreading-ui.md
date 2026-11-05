---
work_package_id: WP89
title: Recreate the original contextual proofreading screen and controls
dependencies:
- WP85
- WP88
requirement_refs:
- FR-004
- FR-005
- FR-014
- NFR-001
- NFR-002
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
branch_strategy: Existing parity feature target. Canonical finalized mapping and issued claim determine workspace; preserve
  pre-existing lane identities.
subtasks:
- T284
- T285
- T286
- T287
- T288
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/model.go
create_intent:
- internal/tui/everyday_view.go
- internal/tui/everyday_menus.go
- internal/tui/proofreading.go
- internal/tui/proofreading_test.go
- internal/tui/evidence/proofreading/**
execution_mode: code_change
owned_files:
- internal/tui/model.go
- internal/tui/historic.go
- internal/tui/everyday_view.go
- internal/tui/everyday_menus.go
- internal/tui/proofreading.go
- internal/tui/proofreading_test.go
- internal/tui/evidence/proofreading/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP89 — Recreate the original contextual proofreading screen and controls

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-015, EE-014. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T284 — Render original proofreading context

Display questionable words in their document context, original suggestion list and original scope/action prompts, preserving layout and emphasis. Exact controls and labels come from WP78; do not introduce a generic modern spell modal.

## T285 — Wire original proofreading interactions

Bind CtrlF2 and original menu routes, suggestion navigation/selection, correction, observed skip/ignore/add choices and cancellation through the approved editor state. Keep input focus and document cursor distinct where original requires it.

## T286 — Preserve continuous reading and correction

Advance to the next questionable word with the same contextual continuity as original. Verify interruption/resume, restart, long/wrapped paragraphs and return to ordinary editing without losing place or leaking prompt input.

## T287 — Exercise the golden proofreading journey

Run a real executable sequence with multiple suspect words, one accepted suggestion, one typed correction where observed, skip, persistent dictionary add, interruption, resume and final save/reopen. Compare original grids, cursor/focus and native effects.

## T288 — Review proofreading product experience

Independent reviewer runs the actual terminal workflow and checks resource provenance, truthful limitations and exact screen behavior. Deliver internal/tui/evidence/proofreading/REPORT.md, full Go checks and native-output comparison.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
