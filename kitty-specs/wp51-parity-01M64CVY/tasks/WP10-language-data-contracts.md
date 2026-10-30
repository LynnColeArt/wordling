---
work_package_id: WP10
title: Character language and data contract map
dependencies:
- WP05
requirement_refs:
- FR-013
- FR-014
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T028
- T029
- T030
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP10: Character language and data contract map

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Each family has explicit native identity, resource and comparison requirements; no proprietary dictionary redistribution or unapproved substitute behavior.

Requirement refs: FR-013, FR-014, FC-006

## Scope and subtasks

### T028

Map original character identity/composition/display and spelling/dictionary/thesaurus resources to native obligations and redistribution constraints; do not substitute Unicode identity for native codes.

### T029

Map sort/record selection/column math/spreadsheet import/links to observable commands, source formats and fixtures.

### T030

Specify a first character-preservation and data-operation slice with source locators, original-app probes and follow-up packages; expose missing resources and variants.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
