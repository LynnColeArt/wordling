---
work_package_id: WP94
title: Complete the live editor commands and filesystem session seam
dependencies:
- WP82
- WP83
- WP88
- WP91
- WP92
- WP93
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
- T308
- T309
- T310
- T311
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/session.go
create_intent:
- internal/editor/everyday_live.go
- internal/editor/everyday_live_test.go
execution_mode: code_change
owned_files:
- internal/editor/session.go
- internal/editor/editing.go
- internal/editor/everyday.go
- internal/editor/search_state.go
- internal/editor/search.go
- internal/editor/bold_authoring.go
- internal/editor/everyday_journey_test.go
- internal/editor/everyday_live.go
- internal/editor/everyday_live_test.go
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP94 — Complete the live editor commands and filesystem session seam

Read WP78 original evidence, everyday milestone acceptance and issued prompt. The WP84 live integration audit exposed these unmet requirements after upstream review. Preserve original review records and stay within the listed source ownership. WP84 is the production consumer.

## T308

Append Tab, Underline, PageUp, PageDown and RetrieveSelection editor commands without changing existing command values. Route Underline to F8 search term input in search prompt modes. Route normal Up/Down/Home/End/page motion through shared physical layout and desired x. Use typed Tab/Underline mutations and adopt qualified reflow only after semantic edits, with native history conservation.

## T309

Add Config.Workspace, Event.Selection and Intent.Selection with pinned workspace ownership. Add observable RetrieveInsertQuestion for occupied acquisition; No/cancel preserves document/list context; Yes inserts supported native fragment using document API. Blank retrieval binds the acquired source. Expose an editor executor helper for real selected-file Read and prepared publication, with operation/revision/screen and source/target authenticity validated on completion.

## T310

Route first/repeated edited saves and SaveAs through approved PrepareSave/PrepareNewSave and PublishSave/PublishNewSave. Observe the selected workspace directory and exact destination, retain refusal/default No and cancel, preserve dirty state on uncertainty, refresh source only on authentic success and resume F7 only after actual successful publication. Preserve local-flat callers and independent Doc1/Doc2. Test actual nested selection, stale/foreign completions, original backup rotation, saved/reopened editing, new and edited F7 saves, Tab/Underline, navigation, F8 search and reflow.

## T311

Verify exact source ancestry, focused public tests and Go formatting/build/test/vet. Freeze the diff, record original evidence, source IDs and remaining gaps, and obtain separate review before WP84 consumes the correction. Preserve the existing document and filesystem safety tests.
