---
work_package_id: WP80
title: Extend lossless native editing and history for everyday documents
dependencies:
- WP79
- WP74
requirement_refs:
- FR-002
- FR-003
- FR-005
- FR-008
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
- T244
- T245
- T246
- T247
- T248
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/document/README.md
create_intent:
- internal/document/everyday.go
- internal/document/everyday_test.go
- internal/document/evidence/everyday/**
execution_mode: code_change
owned_files:
- internal/document/README.md
- internal/document/admission.go
- internal/document/admission_test.go
- internal/document/bold_authoring.go
- internal/document/bold_authoring_test.go
- internal/document/deletion.go
- internal/document/deletion_negative_test.go
- internal/document/deletion_test.go
- internal/document/document.go
- internal/document/document_test.go
- internal/document/history.go
- internal/document/history_fuzz_test.go
- internal/document/history_observation.go
- internal/document/history_original_test.go
- internal/document/history_ownership_test.go
- internal/document/history_test.go
- internal/document/history_wp40_test.go
- internal/document/mutation.go
- internal/document/mutation_categories_test.go
- internal/document/mutation_fuzz_test.go
- internal/document/mutation_test.go
- internal/document/new.go
- internal/document/new_encoding_test.go
- internal/document/new_test.go
- internal/document/reordered_test.go
- internal/document/reveal_catalogue.go
- internal/document/reveal_catalogue_test.go
- internal/document/revision_snapshot_test.go
- internal/document/everyday.go
- internal/document/everyday_test.go
- internal/document/evidence/everyday/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP80 — Extend lossless native editing and history for everyday documents

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-004, EE-007, EE-008, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T244 — Admit actual everyday native structures

Extend semantic decoding/admission for observed Underline, soft/hard returns, tabs and ordinary page boundaries while retaining wp51 framing authority. Use original native samples and exact supported structure checks. Preserve unknown spans and existing enum/public caller contracts.

## T245 — Generalize safe edit lifecycle

Implement supported text insertion/deletion/typeover and return/tab operations on New, saved and Loaded revisions. Remove birthplace/first-save/two-pair restrictions only where semantic safety is established. Maintain immutable revision/cursor/history ownership and atomic failure.

## T246 — Implement paired attributes and block/history

Support repeated Bold/Underline, original permitted overlap, active toggles, pair boundary deletion and block selection/deletion. Preserve original three-level Undelete behavior across supported edits and save/retrieve transitions. Test stale/foreign history refusal.

## T247 — Provide native reflow adoption contract

Expose a narrow atomic native operation for the validated layout boundary changes, preserving hard versus soft return meaning and required structural updates. A renderer must never serialize display text. Test untouched byte identity and conservation around unrelated opaque data.

## T248 — Verify native interoperability

Original app retrieves, edits and saves generated mutation fixtures; Wordling reopens them. Run malformed/fuzz and conservation checks, full Go checks, and independent review. Deliver internal/document/evidence/everyday/REPORT.md with byte-range explanations and fixture provenance.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
