---
work_package_id: WP81
title: Implement matched original layout and physical cursor mappings
dependencies:
- WP80
requirement_refs:
- FR-008
- FR-009
- NFR-005
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
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T249
- T250
- T251
- T252
- T253
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/layout
create_intent:
- internal/layout/**
execution_mode: code_change
owned_files:
- internal/layout/**
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP81 — Implement matched original layout and physical cursor mappings

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-005, EE-006, EE-008, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T249 — Bind observed layout resources

Read the reviewed WP78 profile: Standard8.5x11, margins1inch, Standard Printer/Courier10cpi, Full justification, Auto height, spacing1, HyphenationNo and original tabs. General metric assumptions require original evidence. Avoid terminal-size inputs to physical layout.

## T250 — Compute lines and pages

Implement paragraph wrapping/reflow, tabs, hard/soft boundaries, ordinary pages and physical positions over native document tokens. Support long words, blank paragraphs, attributes and at least three-page fixtures. Preserve no-edit bytes until an authorized semantic edit requires derived boundary changes.

## T251 — Map cursor and code positions

Produce native-gap to line/page/physical position mappings and reverse navigation targets needed for Up/Down/Home/End/Page movement and Reveal. Distinguish zero-width codes from glyph cells and retain desired horizontal navigation position.

## T252 — Compare original layout

Replay matched-resource fixtures and compare wrap words, page membership, printed Pg/Ln/Pos rounding, ruler/tab locations and layout changes after editing. Full justification default must not silently become Left. Declare any justified tolerance before running comparisons.

## T253 — Review pure layout API

Run Go checks and resource-bound tests. Deliver internal/layout/README.md and evidence/everyday/REPORT.md with an API contract used by the next editor package. Different reviewer checks original fidelity and terminal independence.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
