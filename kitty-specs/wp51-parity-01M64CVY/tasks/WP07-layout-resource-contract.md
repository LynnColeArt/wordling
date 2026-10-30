---
work_package_id: WP07
title: Layout and resource comparison profile
dependencies:
- WP05
requirement_refs:
- FR-009
- FR-015
- FR-016
- NFR-005
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T019
- T020
- T021
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP07: Layout and resource comparison profile

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Another researcher can reproduce the declared comparison or identify the exact missing resource. No layout fidelity is claimed from terminal wrapping or unmatched printer metrics.

Requirement refs: FR-009, FR-015, FR-016, NFR-005

## Scope and subtasks

### T019

Define acquisition/provenance and fingerprint requirements for historical DOS plus graphics-capable printer/font profiles; document current FreeDOS and Standard Printer limitations.

### T020

Specify a small reference layout corpus covering returns/pages/margins/tabs/font metrics and original print-to-disk/preview, with units and comparison procedure. Set tolerances only with evidence before comparison.

### T021

Separate blocked external resources from ready text-profile experiments and author follow-up layout/resource/print packages; retain remaining pagination and preview scope.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
