---
work_package_id: WP05
title: Manual and workbook coverage concordance
dependencies: []
requirement_refs:
- FR-001
- NFR-004
- C-003
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T013
- T014
- T015
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP05: Manual and workbook coverage concordance

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Every contents-level manual/workbook entry has a disposition and owner-visible remaining step/subcommand gaps. This is an audited concordance, not a claim of exhaustive behavior verification.

Requirement refs: FR-001, NFR-004, C-003, C-005, C-006

## Scope and subtasks

### T013

Build a chapter/appendix/utility and 36-lesson concordance against existing inventory and scenario IDs, retaining exact edition and locator; mark indexed, studied, observed and uncovered separately.

### T014

Identify version-sensitive entries between REF51 6/92, WB51 11/89, SDK51 12/93 and the selected executable. Assign each discrepancy a bounded probe or external-resource prerequisite.

### T015

List unrepresented subcommands and lesson steps as actionable follow-up packages with coverage impact. Do not mark a lesson or chapter complete from a thematic mapping alone.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Propose follow-up implementation/probe slices inside this package’s owned contract artifact only. WP12 owns authoring the executable continuation queue and new WP prompts; this research package does not edit `tasks.md` or create other WP prompts.

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
