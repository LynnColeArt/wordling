---
work_package_id: WP09
title: Macro and merge execution contract matrix
dependencies:
- WP05
requirement_refs:
- FR-003
- FR-012
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T025
- T026
- T027
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/automation.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/automation.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/automation.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP09: Macro and merge execution contract matrix

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Every rule has its context and evidence level. File-level BREAK and PAGE state are not generalized across macro/primary/secondary contexts without original evidence.

Requirement refs: FR-003, FR-012

## Scope and subtasks

### T025

Consolidate observed strings/expressions/FOR EACH/NEXT/BREAK/loops/handlers into distinct macro and merge execution-context tables, preserving exact unexpected results.

### T026

Record nested primary/secondary record/copy/page transitions and partial-output behavior using existing original run hashes and fixtures; identify unanswered branches without normalizing bytes.

### T027

Define bounded decoder/interpreter implementation packages and additional original-only probes for missing branches, including explicit unsupported commands and error paths.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
