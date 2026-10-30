---
work_package_id: WP08
title: Structured content and graphics contract map
dependencies:
- WP05
requirement_refs:
- FR-010
- FR-011
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T022
- T023
- T024
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP08: Structured content and graphics contract map

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

The map identifies native structures, observable results and resource blockers without collapsing structured content into display-only approximations.

Requirement refs: FR-010, FR-011

## Scope and subtasks

### T022

Decompose styles/outlines/tables/calculation/generated references/master documents into native structure, original command and output obligations.

### T023

Do the same for boxes/graphics/rules/equations and original conversion utilities; identify resource-dependent cases and native format documentation boundaries.

### T024

Choose one independently verifiable starter slice for each family and specify fixture/probe and implementation prerequisites; retain every deferred obligation with inventory IDs.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
