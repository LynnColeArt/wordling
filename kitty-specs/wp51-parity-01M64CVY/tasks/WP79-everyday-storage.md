---
work_package_id: WP79
title: Support original file lifecycle and backups in navigable directories
dependencies:
- WP77
- WP78
- WP41
requirement_refs:
- FR-006
- FR-017
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-003
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Existing parity feature target. Canonical finalized mapping and issued claim determine workspace; preserve
  pre-existing lane identities.
subtasks:
- T239
- T240
- T241
- T242
- T243
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/storage/README.md
create_intent:
- internal/storage/everyday_paths_linux.go
- internal/storage/everyday_backup_linux.go
- internal/storage/everyday_test.go
- internal/storage/evidence/everyday/**
execution_mode: code_change
owned_files:
- internal/storage/README.md
- internal/storage/failures_linux_test.go
- internal/storage/independent_alias_test.go
- internal/storage/list_linux.go
- internal/storage/macro_failures_linux_test.go
- internal/storage/macro_image_test.go
- internal/storage/macro_linux.go
- internal/storage/macro_test.go
- internal/storage/new_publication_failures_linux_test.go
- internal/storage/new_publication_resource_test.go
- internal/storage/new_publication_test.go
- internal/storage/prepared_capture_test.go
- internal/storage/publication_failures_linux_test.go
- internal/storage/publication_linux.go
- internal/storage/publication_test.go
- internal/storage/storage_linux.go
- internal/storage/storage_test.go
- internal/storage/everyday_paths_linux.go
- internal/storage/everyday_backup_linux.go
- internal/storage/everyday_test.go
- internal/storage/evidence/everyday/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP79 — Support original file lifecycle and backups in navigable directories

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-010, EE-011, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T239 — Define reviewed workspace path mapping

Implement the WP78 DOS-directory/workspace-root contract with pinned child directories, parent boundary, filename/case/wildcard and symlink policy. Preserve local-flat existing callers. Separate display observations from capabilities used for read/save.

## T240 — Provide stable browser and Look acquisitions

Support directory enumeration and metadata needed by the original short/long list and Look. Revalidate selected files at retrieval. Bound resources and retain directory/cursor context without treating stale enumeration as authority.

## T241 — Implement replacement and original backups

Reuse existing candidate/publication transactions for edited replacement and Save As. Implement Original Document Backup enabled/disabled rotation, naming and byte preservation exactly from WP78. Preserve original document and backup outcomes across cancellation, overwrite refusal and failures.

## T242 — Test races and failure outcomes

Exercise first/repeated writes, existing backup, path replacement, changed source/destination, symlink/permission failure, interrupted or short write, retry and close concurrency. No success report before actual durable outcome. Preserve existing native read and macro callers.

## T243 — Review storage contract

Run full declared Go checks and relevant original file outcome comparisons. Deliver internal/storage/evidence/everyday/REPORT.md with API/acceptance mapping. Different reviewer approves storage behavior and conservation before document/session consumers.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
