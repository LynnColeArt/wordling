---
work_package_id: WP91
title: Bind selected files and save targets to the pinned workspace
dependencies:
- WP79
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
- T299
- T300
- T301
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/storage/everyday_paths_linux.go
create_intent: []
execution_mode: code_change
owned_files:
- internal/storage/everyday_paths_linux.go
- internal/storage/everyday_test.go
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP91 — Bind selected files and save targets to the pinned workspace

Read WP78 original evidence, everyday milestone acceptance and issued prompt. The WP84 live integration audit exposed these unmet requirements after upstream review. Preserve original review records and stay within the listed source ownership. WP84 is the production consumer.

## T299

Expose Workspace.OwnsSelection(*EntrySelection) and Workspace.OwnsDirectory(*WorkspaceDirectory), including nil, closed and foreign capabilities; identify the selected directory and actual filename through read-only selection methods. Preserve pinning and full identity freshness in Read, not just DOS name or inode number.

## T300

Test child and root acquisitions, foreign/closed/stale selections, case ambiguity and capability copy. Preserve the entire existing backup/publication contract.

## T301

Verify exact source ancestry, focused public tests and Go formatting/build/test/vet. Freeze the diff, record original evidence, source IDs and remaining gaps, and obtain separate review before WP84 consumes the correction. Preserve the existing document and filesystem safety tests.
