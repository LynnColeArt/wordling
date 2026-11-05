---
work_package_id: WP84
title: Integrate the original file browser document viewport and Reveal Codes
dependencies:
- WP83
- WP76
requirement_refs:
- FR-004
- FR-005
- FR-006
- FR-008
- FR-009
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
- T264
- T265
- T266
- T267
- T268
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/README.md
create_intent:
- internal/tui/everyday_view.go
- internal/tui/everyday_files.go
- internal/tui/everyday_ui_test.go
- internal/tui/evidence/everyday/**
execution_mode: code_change
owned_files:
- internal/tui/README.md
- internal/tui/ascii_viewport.go
- internal/tui/ascii_viewport_test.go
- internal/tui/bold_authoring.go
- internal/tui/bold_authoring_test.go
- internal/tui/character_repeat.go
- internal/tui/character_repeat_test.go
- internal/tui/chrome.go
- internal/tui/chrome_test.go
- internal/tui/control_keys.go
- internal/tui/dispatch_test.go
- internal/tui/editable_test.go
- internal/tui/fixtures_test.go
- internal/tui/historic.go
- internal/tui/macro_fuzz_test.go
- internal/tui/macro_lifetime_test.go
- internal/tui/macro_model.go
- internal/tui/macro_original_test.go
- internal/tui/macro_pty_artifacts_test.go
- internal/tui/macro_resource_test.go
- internal/tui/macro_runtime.go
- internal/tui/macro_test.go
- internal/tui/menu_bar.go
- internal/tui/menu_bar_test.go
- internal/tui/model.go
- internal/tui/model_test.go
- internal/tui/new_artifacts_test.go
- internal/tui/new_macro_test.go
- internal/tui/new_model.go
- internal/tui/new_runtime.go
- internal/tui/new_test.go
- internal/tui/original_editable_test.go
- internal/tui/original_test.go
- internal/tui/reveal.go
- internal/tui/reveal_anchors_test.go
- internal/tui/reveal_cursor_test.go
- internal/tui/reveal_inspection.go
- internal/tui/reveal_inspection_test.go
- internal/tui/runtime.go
- internal/tui/everyday_view.go
- internal/tui/everyday_files.go
- internal/tui/everyday_ui_test.go
- internal/tui/evidence/everyday/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP84 — Integrate the original file browser document viewport and Reveal Codes

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-004, EE-005, EE-006, EE-008, EE-009, EE-010, EE-011, EE-014. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T264 — Route normal input into authoritative commands

Bind original keys/modifiers, navigation, corrections, search and storage replies through Model.Update and Session.Reduce. Keep modern aliases disabled in the accepted configuration. Resolve prototype shortcuts that bypass semantic/session ownership.

## T265 — Render shared layout and multiline Reveal

Normal and code panes use one native revision/layout result, original physical status, multiline hard/soft codes, ruler/tab/margin information and caret emphasis. Maintain synchronized scroll and original restore behavior.

## T266 — Implement complete browser journey

F5 directory prompt, current/parent/child navigation, short/long listing, scroll, filename location, Look Next/Prev/return and Retrieve operate through approved pinned storage/session APIs. Preserve list context and document bytes. Retain honest outside-milestone gaps.

## T267 — Verify geometry and focus

Test 80x25 cell/attribute grids, actual terminal keys and mouse input, viewport resize without document reflow, modal input caret, code versus text position and filebrowser cancellation. Reuse host terminal restoration and async guards.

## T268 — Review actual executable reachability

Build the normal cmd/wordling executable and prove end-user paths invoke the new logic. Run full Go checks and native conservation cases. Deliver internal/tui/evidence/everyday/REPORT.md and independent review; no helper-only feature completion.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
