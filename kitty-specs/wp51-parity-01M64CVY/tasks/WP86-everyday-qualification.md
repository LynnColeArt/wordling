---
work_package_id: WP86
title: Independently qualify and deliver the complete everyday editing milestone
dependencies:
- WP85
- WP89
requirement_refs:
- FR-004
- FR-005
- FR-006
- FR-008
- FR-009
- FR-014
- NFR-005
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
- T289
- T290
- T291
- T292
- T293
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: tests/everyday_qualification
create_intent:
- tests/everyday_qualification/**
execution_mode: code_change
owned_files:
- tests/everyday_qualification/**
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP86 — Independently qualify and deliver the complete everyday editing milestone

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-001, EE-002, EE-003, EE-004, EE-005, EE-006, EE-007, EE-008, EE-009, EE-010, EE-011, EE-012, EE-013, EE-014, EE-015. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T289 — Bind final integrated candidate

Record all independently approved dependency commits and current canonical source, resource profile and actual build identity. Verify no source/lane drift and no unreviewed inherited delta. Build through normal cmd/wordling.

## T290 — Run full original and product journeys

Execute EE-A01–A15 with real files and terminal input, including golden continuous editing and proofreading. Compare original character/attribute grids, focus/cursor, physical layout and native outcomes. Preserve failed runs and report exact unmet criteria.

## T291 — Prove original interoperability and conservation

Original retrieves/edits/saves Wordling outputs, then Wordling reopens/continues. Check no-edit byte identity, unrelated preservation, repeat saves/backups and refusal/failure outcomes. Resource and terminal adaptations are declared.

## T292 — Close integration findings independently

Different reviewer audits the complete product journey and all requirement mappings. Return product-code findings to the owning package, repair there under review, then rerun affected integration scenarios. This package does not gain broad product source ownership.

## T293 — Deliver exact reviewed preview and milestone report

Run final formatting/build/test/vet checks and record the tested binary hash. Publish the exact candidate to preview atomically using authorized host delivery, without committing binaries. Deliver tests/everyday_qualification/REPORT.md with EE coverage, launch command and explicit remaining M1 gaps. Do not accept the entire mission or start M2.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
