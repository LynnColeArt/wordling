---
work_package_id: WP13
title: Original SESSION1 prompt and cursor probes
dependencies:
- WP03
- WP04
- WP06
- WP11
- WP12
requirement_refs:
- FR-004
- FR-005
- FR-006
- NFR-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-10-30T22:39:47.533864+00:00'
subtasks:
- T037
- T038
- T039
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: researcher-robbie
authoritative_surface: scripts/reference/session1.py
create_intent:
- scripts/reference/session1.py
- docs/research/continuation/session1/
execution_mode: code_change
owned_files:
- scripts/reference/session1.py
- docs/research/continuation/session1/
- docs/research/command-scenarios.json
- docs/research/command-scenarios.md
- docs/research/scenario-coverage.md
- docs/research/workbook-map.md
- docs/research/feature-inventory.json
- docs/research/feature-inventory.md
role: researcher
tags:
- m1-continuation
task_type: research
tracker_refs: []
---

# WP13: Original SESSION1 prompt and cursor probes

## Identity, governance and prerequisites

Load `researcher-robbie` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP03, WP04, WP06, WP11, WP12.

**Requirement references:** FR-004, FR-005, FR-006, NFR-004, C-005, C-006.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/session.md §§ First bounded composed session proposal, G1–G4/G6–G9; files-platform.md FP01–FP05/FP21; editing.md token-gap notation`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

A repeated original SESSION1 transcript closes exact Retrieve, filename, cursor and contextual Cancel/Exit questions before session code relies on them.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T037

Implement scripts/reference/session1.py using the existing fresh-copy/reference guest harness and archived-source pattern. Fingerprint selected baseline/settings; load the exact advanced04 CMD51-204 ORIGIN.WP5 fixture by manifest hash. Exercise blank Retrieve, missing path retry and F1 versus Esc; record the actual prompt/default/cursor/initial-code effects. Never replace original files or infer in-buffer insertion behavior from blank retrieval.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T038

Run dedicated Home/Home/Up versus Home/Home/Home/Up and Right around each Bold On/Off token gap in both normal and Reveal panes. Probe prefilled filename editing versus character-first replacement, refusal/cancel, named/unnamed saved/changed exit contexts, F7,n,n separately from n,y and F1/Esc at each relevant prompt. Capture every intermediate state and native source/output; split the composed run if a branch changes the starting state.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T039

Repeat each accepted branch twice from fresh copies; publish raw traces, screen/native hashes, runner/profile manifest and a branch table in docs/research/continuation/session1/. Expand canonical session scenarios with explicit subcase preconditions and source links, including missing exit/retrieve Cancel cases. Update exact feature-inventory.json command_scenario_ids back-links for new CMD51 IDs, preserving catalogue order; regenerate feature-inventory.md with scripts/render-inventory.py and all three scenario/workbook summaries with scripts/render-scenarios.py, without promoting Wordling implementation/verification. Record divergences as unresolved, not normalized expectations.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-065, CMD51-019, CMD51-020, CMD51-049, CMD51-066, CMD51-067, CMD51-069, CMD51-070, CMD51-087. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Every accepted state has a stable CMD51/subcase link, exact prompt/cursor/name/buffer state and two independently fresh run identities.
- Same reference source bytes survive cancelled/failed retrieval/save. Native source/fixture hashes match their pinned manifests.
- SESSION1 remains partially observed if any branch fails; downstream WP17 must refuse that branch explicitly and cannot claim it accepted.

## Ownership and explicit limits

- No Linux terminal qualification, new semantic writer, actual replacement implementation, insertion into existing document, full menus or two-screen parity.
- No new terminal alias/shortcut or baseline change. Only owned session entries may change in canonical registries; unrelated entries/status remain exact.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp13-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.

### Canonical registry validation boundary

The existing render validator requires IDs matching CMD51-###, exact case-to-feature back-links in feature-inventory.json, valid requirement/source/baseline fields and current run.json schema. Newly partially-observed cases require run.scope original-reference-only, wordling_tested false, matching results/case_id, observed-matches-smoke-expectations plus passed checks and immutable artifact hashes. Add only session cases needed here and preserve every unrelated row. Regenerate feature-inventory.md, command-scenarios.md, scenario-coverage.md and workbook-map.md with the two existing renderers; all are owned. Do not edit historical research checkpoint counts or approved contract snapshots to disguise their dated state. Publish a new dated count snapshot in this package’s owned report; old input hashes are historical and cannot certify newly changed registries.
