---
work_package_id: WP96
title: Drive the contextual editor session with admitted proofreading resources
dependencies:
- WP88
- WP94
- WP95
- WP97
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
- T315
- T316
- T317
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/session.go
create_intent:
- internal/editor/proofreading_live_test.go
execution_mode: code_change
owned_files:
- internal/editor/session.go
- internal/editor/proofreading.go
- internal/editor/proofreading_session.go
- internal/editor/proofreading_test.go
- internal/editor/proofreading_live_test.go
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP96 — Drive the contextual editor session with admitted proofreading resources

Use the issued prompt, WP78 original evidence and milestone EE-013/EE-015 acceptance. The current provider/session source audit found demonstration behavior in production. Preserve prior verdicts and source boundaries. Proofreading must work generally through admitted resources and observed contextual behavior. Exact original lexical ranking remains outside the approved Linux adaptation.

## T315

Route Ctrl+F2 and the Check menu through the admitted provider and the editor’s native token ranges. Remove the fixture cohort and literal suggestion-letter branches from the production editor. Bind the actual current suggestions to displayed letters and Enter pagination; use the declared lookup adaptation and do not assert original lexical order. Implement Word/Page/Document/Block scopes from caret, physical layout and selection, actual Count, and observed native word boundaries (punctuation, apostrophes, tabs, SRt, DSRt and zero-width attributes). Expose read-only prompt state for WP89 with exact native suspect range, suggestions, action/ack state and word counts. Explicitly report missing resource failures.

## T316

Implement observed session transitions for Skip Once and case-aware per-pass Skip, remembered replacements applied to later occurrences, Ignore Numbers, New Sup. Dictionary, Add, Look Up, Edit and F7 resumption, F1 interruption and partial acknowledgement, including observed Double Word and Irregular Case. Use WP97 atomic correction and approved layout reflow; preserve unrelated native bytes/history, viewport return, separate screen state and no-op cancellation. Qualify the observed 64-character DSRt residue case from WP78. Use authenticated editor intent/results for dictionary I/O, bound to operation, screen, revision and current suspect. Only a checked successful publication updates active vocabulary or advances Add. Failed/stale/cancelled results preserve document, dirty/history state and report failure or uncertainty accurately.

## T317

Exercise complete editor journeys with general admitted vocabulary, original formatted/wrapped/page fixtures, cursor and exact correction bytes, remembered/skip/Add separation, fresh process dictionary reopening, failure/refusal and other-screen/stale results. Run focused/full build/test/vet and diff/format checks, freeze scoped source and request independent review. WP89 must wire these APIs in normal executable and WP86 must qualify complete journeys.
