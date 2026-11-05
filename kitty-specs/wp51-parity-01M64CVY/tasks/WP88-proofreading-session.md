---
work_package_id: WP88
title: Implement continuous contextual proofreading in the editor
dependencies:
- WP83
- WP87
requirement_refs:
- FR-014
- FR-005
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
- T279
- T280
- T281
- T282
- T283
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/session.go
create_intent:
- internal/editor/proofreading.go
- internal/editor/proofreading_test.go
- internal/editor/evidence/proofreading/**
execution_mode: code_change
owned_files:
- internal/editor/session.go
- internal/editor/proofreading.go
- internal/editor/proofreading_test.go
- internal/editor/evidence/proofreading/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP88 — Implement continuous contextual proofreading in the editor

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-015, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T279 — Model the original proofreading journey

Implement CtrlF2 scopes and contextual questionable-word state from WP78. Track native positions, current suggestion, dictionary/ignore decisions and continuation independently for the correct document screen.

## T280 — Apply corrections through real native editing

Suggestion replacement and typed correction use approved document/history/session operations, preserve attributes and unrelated bytes, and update layout/search/proofreading positions consistently. No rendering-side string replacement or alternate document model.

## T281 — Implement skip add and continuity

Implement only observed original skip/ignore-all/add choices, next-word advance, cancellation, interruption/resume and restart semantics. Preserve reading place and document focus at each transition, including after save/retrieve and in repeated sessions.

## T282 — Verify public proofreading scenarios

Exercise misspellings across paragraphs/wraps/codes, repeated suspect words, replacements of different lengths, add/ignore behavior, cancellation and resource failures. Assert original native effects and unchanged bytes for skip/cancel paths.

## T283 — Review session correctness

Run full Go checks and original workflow comparisons. Deliver internal/editor/evidence/proofreading/REPORT.md with exact continuation/state evidence. Independent review must examine a continuous journey, not just isolated provider calls.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
