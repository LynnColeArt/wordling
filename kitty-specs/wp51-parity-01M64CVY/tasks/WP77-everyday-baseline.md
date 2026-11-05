---
work_package_id: WP77
title: Review and qualify the integrated everyday source baseline
dependencies: []
requirement_refs:
- FR-004
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
- T229
- T230
- T231
- T232
- T233
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: tests/baseline_adoption
create_intent:
- tests/baseline_adoption/**
execution_mode: code_change
owned_files:
- tests/baseline_adoption/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP77 — Review and qualify the integrated everyday source baseline

Read the approved everyday milestone spec, plan, acceptance and decisions under `../milestones/everyday-editing/`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-001, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T229 — Bind source custody

Verify the issued workspace contains the feature-source intake of candidate c7f14fd497da62bb577b6bdab7d4be3fb124e546, parent f89a48627916b5cb9e360c35047350031b6f06a9. Record exact ancestry, candidate changed-file hashes, root/H checkpoint identities and unchanged prior lifecycle approvals. Candidate is UNREVIEWED input. Compare the complete computed WP/lane/worktree map against preflight. Missing source or changed earlier mapping requires reviewed correction before edits.

## T230 — Audit inherited preview delta

Independently inspect all 23 candidate source changes, including native newline/history admission, boundary handling, modifier adapters, menus and browser. Separate safe retained foundations from known incomplete product behavior. A preexisting test pass does not approve the delta. Report unsafe candidate findings for source correction and independent re-review before downstream approval.

## T231 — Add baseline public-entry probes

Create tests/baseline_adoption/ public CLI/Model probes for startup, ordinary typing/Enter, keys, menu visibility/focus, Reveal, first save and normal exit. Assert native bytes and terminal restoration. Retain explicit expected product gaps for future packages without claiming them implemented.

## T232 — Verify build and preservation

Run gofmt, build, full tests and vet at the exact source. Check existing native conservation and async ownership tests. Store source identities, commands/results and a focused acceptance mapping in tests/baseline_adoption/REPORT.md and manifest.json.

## T233 — Obtain independent source review

Submit the complete inherited candidate diff and new probe diff to a different reviewer. Approval must expressly cover both. No consumers proceed on approval76 alone or on an unreviewed candidate checkpoint.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
