---
work_package_id: WP93
title: Repair physical lines, pages, tab stops and caret mapping
dependencies:
- WP81
- WP92
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
- T305
- T306
- T307
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/layout/layout.go
create_intent: []
execution_mode: code_change
owned_files:
- internal/layout/layout.go
- internal/layout/layout_test.go
- internal/layout/README.md
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP93 — Repair physical lines, pages, tab stops and caret mapping

Read WP78 original evidence, everyday milestone acceptance and issued prompt. The WP84 live integration audit exposed these unmet requirements after upstream review. Preserve original review records and stay within the listed source ownership. WP84 is the production consumer.

## T305

Keep FromDocument as the pure production entry point. Group each native token exactly once in Lines.Tokens in order, including zero-width owners. Add TokenPosition.Index and Layout.PositionAt(gap int) (line, column int, ok bool) using zero-based physical-line and nominal cell positions. Preserve blank/final rows and distinct native gaps sharing a cell.

## T306

Use WP78 matched geometry and evidence for tabs, soft and hard returns, DSRt, page-owner groups, derived wrapping, physical Page Up/Down and desired x. Provide a layout producer for the native derived-boundary plan, never serialize display text. Compare FLOW.WP positions and independent wrap/tab/page-edge probes. No terminal width input or view-time mutation.

## T307

Verify exact source ancestry, focused public tests and Go formatting/build/test/vet. Freeze the diff, record original evidence, source IDs and remaining gaps, and obtain separate review before WP84 consumes the correction. Preserve the existing document and filesystem safety tests.
