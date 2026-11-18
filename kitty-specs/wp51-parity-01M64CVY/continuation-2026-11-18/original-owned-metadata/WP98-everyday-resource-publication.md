---
work_package_id: WP98
title: Publish native resources without touching document backups
dependencies:
- WP91
requirement_refs:
- FR-004
- FR-005
- FR-014
- NFR-001
- NFR-002
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T320
- T321
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/storage/everyday_backup_linux.go
create_intent: []
execution_mode: code_change
owned_files:
- internal/storage/everyday_backup_linux.go
- internal/storage/everyday_test.go
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP98 — Publish native resources without touching document backups

Use the issued prompt, WP78 original evidence and milestone EE-013/EE-015 acceptance. The current provider/session source audit found demonstration behavior in production. Preserve prior verdicts and source boundaries. Proofreading must work generally through admitted resources and observed contextual behavior. Exact original lexical ranking remains outside the approved Linux adaptation.

## T320

Add an explicit checked native resource replacement policy to the existing prepared save API. In this policy skip the original-document BK! lookup, staging, rotation and deletion entirely, because OriginalBackupOff removes an existing same-stem BK! by design. Preserve the existing Off/On behavior and no-overwrite checks. Reuse the same source/target validation, prepared transaction and failure semantics.

## T321

Prove a replaced native SUP leaves an unrelated same-stem BK! byte-identical even if that file is opaque or otherwise inadmissible as a document; cover first save, replacement, conflict/refusal and existing backup suites. Run full and focused race tests and independent review. WP95 is the production consumer.
