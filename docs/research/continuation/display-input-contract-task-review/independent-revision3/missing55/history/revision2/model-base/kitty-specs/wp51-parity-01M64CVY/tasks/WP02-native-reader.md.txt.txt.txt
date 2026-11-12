---
work_package_id: WP02
title: Lossless native reader and no-edit export
dependencies:
- WP01
requirement_refs:
- FR-002
- NFR-001
- NFR-003
- C-001
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-10-30T07:35:41.482509+00:00'
subtasks:
- T004
- T005
- T006
phase: Initial M1 delivery and contract research
history:
- at: '2026-10-30T06:14:49Z'
  actor: codex
  action: Prompt generated from M1 plan; not executed
agent_profile: implementer-ivan
authoritative_surface: internal/wp51/
create_intent:
- internal/wp51/
execution_mode: code_change
owned_files:
- internal/wp51/
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# WP02: Lossless native reader and no-edit export

## Profile and prerequisites

Load `implementer-ivan` through the profile-loading skill/API before executing. Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, `docs/compatibility.md`, and `docs/roadmap.md`. Read dependency outputs and all review feedback. Use the existing mission and canonical runtime.

## Objectives and acceptance

Every accepted WP01 fixture exports byte-identically; malformed cases fail without panic or uncontrolled work; opaque bytes and caller buffer isolation survive. Reader acceptance does not establish edit interoperability.

Requirement refs: FR-002, NFR-001, NFR-003, C-001, C-002

## Scope and subtasks

### T004

Implement immutable owned native images, checked framing and typed failures in internal/wp51 using only the approved WP01 contract. Preserve opaque spans and trailing bytes; reject unsupported structural variants explicitly.

### T005

Expose no-edit byte export and span inspection without caller mutation of owned storage. Keep semantic mutation, UI, filesystem replacement and dependency changes outside this package.

### T006

Add original-fixture byte/length/SHA comparisons, buffer-isolation tests and malformed/cyclic/oversized/truncated cases plus fuzzing under the WP01 budget; run formatting, build, test and vet.

## Validation and review

Confirm all referenced source/fixture paths and hashes, preserve evidence levels and run both catalogue validation scripts. Changed Go additionally requires formatting, build, test and vet; binary readers require malformed/fuzz checks and writers original-app comparisons appropriate to their supported contract. Commit no proprietary media. Review rejects unsupported compatibility claims, unknown-byte loss, invented behavior or implicit scope cuts. Record validation and remaining limitations in the package activity/evidence.

## Delivery and continuation

Produce the owned surfaces above and trace them to stable requirement/scenario IDs. Research output includes explicit next implementation slices; its completion never marks those features implemented. Follow existing single-branch mission placement, with later GitHub integration to main only after real acceptance. Do not bypass guards, self-approve or mark the mission complete from this initial queue.

## Activity Log

- 2026-10-30T06:17:12Z – codex – Planned prompt validated; no execution or acceptance claimed.
- 2026-10-30T07:54:30Z – codex – shell_pid=811205 – T004-T006 implemented in internal/wp51. Exact original bytes/length/SHA verified; macro explicitly refused. All malformed/isolation/resource tests pass. 60s fuzz:7000569exec;600s fuzz:57160290exec, no crash/hang. Final JUnit adapter 7 passing checks, zero skips/failures, real Go build/test/vet. Evidence includes logs/host/RSS/limits/mutation probes; payloads remain unvalidated, no semantic editing or filesystem writer. Independent review required.
