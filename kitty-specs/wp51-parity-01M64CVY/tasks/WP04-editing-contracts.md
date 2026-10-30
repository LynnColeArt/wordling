---
work_package_id: WP04
title: Observed editing command contracts
dependencies:
- WP01
requirement_refs:
- FR-004
- FR-005
- FR-008
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T010
- T011
- T012
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/editing.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/editing.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/editing.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP04: Observed editing command contracts

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Each proposed implemented transition has a linked original observation and native expected effect; unknown combinations are explicit and do not become guessed editor behavior.

Requirement refs: FR-004, FR-005, FR-008, NFR-004

## Scope and subtasks

### T010

Extract the existing cursor/code-boundary/typeover/blocked-pair deletion and three-level Undelete observations into a state-transition table with exact CMD51 IDs and fixture links.

### T011

Write Given/When/Then contracts for document positions, paired-code repair and command-specific restoration; separate original observations from untested combinations.

### T012

Define the smallest subsequent document/editor implementation packages and their native-write prerequisites; add original probes only for genuinely unanswered contract branches.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.
