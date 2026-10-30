---
work_package_id: WP03
title: Failure-safe no-edit filesystem save
dependencies:
- WP02
requirement_refs:
- FR-006
- NFR-001
- NFR-002
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: implementer-ivan
authoritative_surface: internal/storage/
create_intent:
- internal/storage/
execution_mode: code_change
owned_files:
- internal/storage/
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# WP03: Failure-safe no-edit filesystem save

## Profile and prerequisites

Load `implementer-ivan` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

The documented local-filesystem cases preserve originals under injected failures and refuse overwrite without an explicit decision. No original backup, locking or Fast Save behavior is falsely advertised.

Requirement refs: FR-006, NFR-001, NFR-002, C-002

## Scope and subtasks

### T007

Specify the bounded new-file and existing-file no-edit transaction API with explicit destination/source identity and overwrite decision; leave original prompt UI and unobserved backup/Fast Save behavior unsupported.

### T008

Implement candidate creation/write/close and safe replacement only under that contract. Refuse stale source identity, unsafe paths and unsupported replacement cases before changing the destination; avoid claiming network/durability semantics not tested.

### T009

Inject write/close/rename failures and concurrent-source changes. Assert original bytes remain intact on refusal/failure and exported bytes are exact on success; run formatting, build, test and vet.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
