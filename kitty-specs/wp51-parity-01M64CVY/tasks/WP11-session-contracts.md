---
work_package_id: WP11
title: Classic session and terminal interaction contracts
dependencies:
- WP04
- WP06
requirement_refs:
- FR-004
- FR-005
- C-001
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T031
- T032
- T033
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/session.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/session.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/session.md
role: researcher
tags: []
task_type: research
tracker_refs: []
---

# WP11: Classic session and terminal interaction contracts

## Profile and prerequisites

Load `researcher-robbie` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

A subsequent implementer can build the bounded session without guessing original prompts, while the rest of classic interaction remains visible in M1.

Requirement refs: FR-004, FR-005, C-001

## Scope and subtasks

### T031

Specify the first retrieve/Reveal Codes/cursor/save/cancel/exit session as original command/prompt states linked to original transcripts; include both display and input adaptation boundaries.

### T032

Declare Linux terminal key ambiguities and supported terminal profile, with explicit fallback decisions that preserve original commands; do not invent menus from generic text editor conventions.

### T033

Author bounded Bubble Tea/session implementation packages independent of document/layout semantics, with observable state tests and the necessary original command probes.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Propose follow-up implementation/probe slices inside this package’s owned contract artifact only. WP12 owns authoring the executable continuation queue and new WP prompts; this research package does not edit `tasks.md` or create other WP prompts.

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
