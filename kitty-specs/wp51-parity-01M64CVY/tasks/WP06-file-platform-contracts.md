---
work_package_id: WP06
title: File and Linux platform investigation
dependencies:
- WP05
requirement_refs:
- FR-006
- FR-007
- FR-017
- C-006
- NFR-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T016
- T017
- T018
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP06: File and Linux platform investigation

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Each platform-sensitive behavior has an explicit mapping proposal, evidence status and next test; no hidden exclusions or fabricated historical-DOS result.

Requirement refs: FR-006, FR-007, FR-017, C-006, NFR-002

## Scope and subtasks

### T016

Produce a matrix of original retrieval/save/list/backup/recovery/Fast Save/locking/conversion commands and required fixtures or reference prerequisites; include overwrite refusal and cancellation evidence already captured.

### T017

Classify Linux path/key/shell/network mappings and owner decisions needed for actual scope changes. Prioritize one minimal no-edit retrieve/save workflow for UI integration; preserve unsupported functions visibly.

### T018

Specify independent probe/implementation slices for each unresolved family with failure safety and original artifact-format acceptance.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.
