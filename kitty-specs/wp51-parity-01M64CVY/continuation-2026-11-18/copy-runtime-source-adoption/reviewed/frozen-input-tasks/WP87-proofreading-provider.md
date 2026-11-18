---
work_package_id: WP87
title: Implement the resource-backed original proofreading engine contract
dependencies:
- WP78
- WP80
requirement_refs:
- FR-014
- FR-005
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
- T274
- T275
- T276
- T277
- T278
phase: Everyday editing milestone within M1; full parity remains open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/proofreading
create_intent:
- internal/proofreading/**
execution_mode: code_change
owned_files:
- internal/proofreading/**
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP87 — Implement the resource-backed original proofreading engine contract

Read the approved everyday milestone spec, plan, acceptance and decisions under `../`, the project charter, compatibility contract, and the issued implementation prompt. Original reference evidence is in `docs/research/everyday-contract-2026-11-05/`, including its backup and proofreading extensions. Original US WP 5.1 dated 03/09/92 governs behavior. Preserve full M1 obligations and keep PDF/new conveniences in M2.

Canonical finalization and the issued claim determine the workspace and actual source. Compare all existing WP-to-lane memberships, branch/worktree identities and prior lifecycle/approval identities before and after computation. Stop source edits on an unexplained change, missing approved dependency, ownership union or lane cycle. Resolve it through reviewed planning/source propagation. Do not guess lane names, force topology, mark old work approved again, copy a whole source tree, or use a test overlay to manufacture dependencies.

The feature-source intake includes UNREVIEWED candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546`, parent `f89a48627916b5cb9e360c35047350031b6f06a9`. Its source presence does not imply approval. WP77 explicitly reviews that delta. WP78 is independent original research; all later implementation consumption requires the relevant WP77/WP78 approvals. Existing historical evidence remains intact. Approved changes to old product limitations require a precise requirement-to-test mapping.

## Package contract

Milestone requirements EE-015, EE-013. See the acceptance matrix for exact journeys. Ownership metadata limits source edits to this component. Cross-component API changes return to the owning package through a reviewed amendment. No source-model or native-format shortcut satisfies a UI criterion.

## T274 — Bind original proofreading resources

Adopt the reviewed CtrlF2 workflow/resource contract. Record original dictionary/supplemental resource identities and allowed host resource sources, formats and redistribution rights. Resource absence is explicit; no bundled proprietary data or silent pass-through success.

## T275 — Implement lexical and suggestion services

Provide deterministic token/word boundary, suspect-word and suggestion operations needed by the original workflow using actual admitted resources. Preserve original character identities and dictionary distinctions. Any resource/lexical difference remains a qualified limitation, not a hidden generic modern replacement.

## T276 — Implement supplementary dictionary operations

Implement the observed add/persistent dictionary behavior and per-run ignore vocabulary with the original semantic distinction. Use original-compatible formats or a reviewed explicit platform adaptation with conservation tests.

## T277 — Test original corpus and resource failures

Test suspect words, correct words, suggestions/order where required, repeated occurrences, added words, encoding/resource failures and bounded work. Record differences from original under matched resources and resolve cases claimed by the milestone.

## T278 — Review provider contract

Run Go checks and focused resource/native tests. Deliver internal/proofreading/README.md and evidence/REPORT.md. Different reviewer approves real resource behavior and the API consumed by session proofreading.

## Verification and independent review

Use the normal public entrypoints and actual approved dependency APIs. Foundational packages may prove their public APIs with dependency integration tests before the scheduled production consumer exists; their approval qualifies the layer, not the complete user feature. Identify the consuming WP explicitly and require it to remove any superseded route. Consumer packages must prove normal application reachability, and WP86 must exercise every delivered behavior through the real executable. Unused implementations cannot satisfy milestone completion. Run the project-required formatting, `go build ./...`, `go test ./...` and `go vet ./...` for changed Go source. Research/tooling changes receive syntax checks and actual scenario execution. Native parser changes require relevant malformed-input/fuzz tests; native writer changes require original-app interoperability and preservation. Test retry/concurrent/partial-failure paths where operations cross I/O or asynchronous boundaries.

Record source and dependency commits, focused changed-file hashes, commands/results, exact original profile and fixtures, relevant raw observations, acceptance mapping and remaining gaps in the stated package report. Preserve useful failure evidence without copying repository-wide historical artifact trees. No arbitrary file-by-file hash whitelist, special fixture name or hard-coded demonstration transcript may replace general behavior for the supported fixture family.

A different reviewer checks the complete requirement contract, original evidence, native conservation, normal executable reachability and source custody. Reject incomplete paths. Use Spec Kitty's implementation/review lifecycle and record its actual verdict. Package approval unblocks dependents but does not establish complete M1 acceptance. The orchestrator owns integration and final preview delivery sequencing.
