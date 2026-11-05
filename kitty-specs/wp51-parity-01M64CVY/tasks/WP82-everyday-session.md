---
work_package_id: WP82
title: Complete everyday session lifecycle navigation and save continuations
dependencies:
- WP81
- WP75
requirement_refs:
- FR-004
- FR-005
- FR-006
- FR-008
- FR-009
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
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T254
- T255
- T256
- T257
- T258
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/README.md
create_intent:
- internal/editor/everyday.go
- internal/editor/everyday_test.go
- internal/editor/evidence/everyday/**
execution_mode: code_change
owned_files:
- internal/editor/README.md
- internal/editor/block_backspace_test.go
- internal/editor/bold_authoring.go
- internal/editor/bold_authoring_test.go
- internal/editor/editing.go
- internal/editor/editing_test.go
- internal/editor/macro_boundary_test.go
- internal/editor/macro_budget_assertions_test.go
- internal/editor/macro_execution.go
- internal/editor/macro_fork_test.go
- internal/editor/macro_fuzz_test.go
- internal/editor/macro_load.go
- internal/editor/macro_original_flow_test.go
- internal/editor/macro_resource_test.go
- internal/editor/macro_session.go
- internal/editor/macro_test.go
- internal/editor/new_binding.go
- internal/editor/new_binding_internal_test.go
- internal/editor/new_binding_resource_test.go
- internal/editor/new_binding_test.go
- internal/editor/new_macro.go
- internal/editor/new_macro_internal_test.go
- internal/editor/new_macro_test.go
- internal/editor/original_history_test.go
- internal/editor/resource_test.go
- internal/editor/revision_session_test.go
- internal/editor/save_history_internal_test.go
- internal/editor/save_history_test.go
- internal/editor/session.go
- internal/editor/session_fuzz_test.go
- internal/editor/session_test.go
- internal/editor/everyday.go
- internal/editor/everyday_test.go
- internal/editor/evidence/everyday/**
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP82 — Complete everyday session lifecycle navigation and save continuations

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-004, EE-005, EE-006, EE-007, EE-008, EE-011, EE-012, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T254 — Integrate supported document commands

Route real editor commands through approved document/layout APIs for New/saved/retrieved text. Adopt native reflow changes atomically and preserve cursor/history. Replace narrow pristine-startup guard assumptions with supported-semantic state checks.

## T255 — Complete navigation and correction

Implement original arrows, Home/End sequences, Page movement, desired horizontal position, scrolling targets, Insert/typeover, block correction and Undelete. Handle boundaries through original observable behavior without suppressing real malformed-state failures.

## T256 — Complete save and retrieval lifecycle

First save, edited replacement, Save As, overwrite No/cancel, backups and failures use approved storage outcomes. F7 Save Yes saves then continues the correct exit flow. Retrieval into blank and occupied supported buffers follows original insertion semantics; no implicit destructive clear.

## T257 — Complete two-document and continued-New state

Both screens retain content/name/dirty/cursor/history. Implement original Doc2 closure versus ExitWP, cancel and continuation, and creation of a usable new document after clear/close. Preserve stale/detached I/O guards and existing macro command callers.

## T258 — Review public session journeys

Run public Session tests with genuine storage receipts and original native fixtures, then full Go checks. Deliver internal/editor/evidence/everyday/REPORT.md. Independent review covers repeated edits/saves, failed/canceled operations and downstream live integration contract.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
