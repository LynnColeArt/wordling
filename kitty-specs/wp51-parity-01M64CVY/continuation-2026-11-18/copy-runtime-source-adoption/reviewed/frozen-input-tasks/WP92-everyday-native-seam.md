---
work_package_id: WP92
title: Conserve native semantics through reflow and occupied retrieval
dependencies:
- WP80
requirement_refs:
- FR-004
- FR-005
- FR-006
- FR-008
- FR-009
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T302
- T303
- T304
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/document/everyday.go
create_intent: []
execution_mode: code_change
owned_files:
- internal/document/document.go
- internal/document/admission.go
- internal/document/everyday.go
- internal/document/history.go
- internal/document/mutation.go
- internal/document/everyday_test.go
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP92 — Conserve native semantics through reflow and occupied retrieval

Read WP78 original evidence, everyday milestone acceptance and issued prompt. The WP84 live integration audit exposed these unmet requirements after upstream review. Preserve original review records and stay within the listed source ownership. WP84 is the production consumer.

## T302

Replace arbitrary-body reflow adoption with a revision-bound plan of space/SRt replacement, DSRt and qualified page transitions. Validate full semantic conservation, immutable opaque spans, caret/history remapping and refusal for stale/foreign/malformed plans. Retain a no-op identity fast path; no mutation from projection or resize. The original default-profile edge probes require Tab followed by DSRt and a typed soft page transition using the witnessed D4 page record plus 0x91. Validate exact complete groups and preserve word, cursor and history semantics across reflow. Reject unqualified opaque, malformed or foreign groups.

## T303

Add atomic checked insertion of a supported source fragment at an owned cursor. Do not import the source prefix; validate receiver context, supported owners, attributes and resulting structure before adoption. Preserve current native source identity, insertion cursor and existing history semantics. Test plain and formatted/wrapped original fixtures, no-partial-failure and original read/edit/resave.

## T304

Verify exact source ancestry, focused public tests and Go formatting/build/test/vet. Freeze the diff, record original evidence, source IDs and remaining gaps, and obtain separate review before WP84 consumes the correction. Preserve the existing document and filesystem safety tests.
