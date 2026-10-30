---
work_package_id: WP01
title: Native framing contract and fixture corpus
dependencies: []
requirement_refs:
- FR-002
- FR-003
- NFR-001
- NFR-003
- C-002
- C-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md
- kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md
- kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP01: Native framing contract and fixture corpus

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

A reviewer can derive every checked native offset and boundary from the contract, validate every fixture hash, and identify which variants must be refused. No reader code or general companion-file support is claimed.

Requirement refs: FR-002, FR-003, NFR-001, NFR-003, C-002, C-004

## Scope and subtasks

### T001

Specify SDK51 prefix, linked index/packet and body framing fields with widths, endian rules, validation and release applicability; include exact source/page locators.

### T002

Select a small provenance-approved original-produced corpus spanning plain text, paired attributes, prefix packets, macros/merges as distinct file types, and opaque/trailing data; record paths, hashes and supported/refused variants without copying proprietary resources.

### T003

Declare parser input/allocation/traversal limits, typed failure categories, malformed cases, fuzz seed corpus and reproducible budget. Measure the selected corpus against those limits and record unresolved variants.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
