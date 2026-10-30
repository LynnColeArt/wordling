---
work_package_id: WP17
title: Pure read-only Retrieve Save Cancel session reducer
dependencies:
- WP03
- WP11
- WP12
- WP13
- WP15
requirement_refs:
- FR-004
- FR-005
- FR-006
- NFR-001
- NFR-002
- C-001
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T049
- T050
- T051
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: implementer-ivan
authoritative_surface: internal/editor/
create_intent:
- internal/editor/
execution_mode: code_change
owned_files:
- internal/editor/
role: implementer
tags:
- m1-continuation
task_type: implementation
tracker_refs: []
---

# WP17: Pure read-only Retrieve Save Cancel session reducer

## Identity, governance and prerequisites

Load `implementer-ivan` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP03, WP11, WP12, WP13, WP15.

**Requirement references:** FR-004, FR-005, FR-006, NFR-001, NFR-002, FC-002, FC-004, FC-009, C-001.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/session.md O1–O10/G1–G10 and reviewed WP13 branch evidence; files-platform.md first no-edit workflow; approved storage README`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

A deterministic session reducer composes an immutable retrieved document, original contextual commands/prompts and typed storage outcomes for the observed bounded session.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T049

Implement internal/editor/ state and reducer independent of Bubble Tea. Store one document/token-gap cursor, Reveal visibility, prefix/context, filename draft/caret/original name and pending operation identity. Adopt only observed WP11/WP13 exact prompt/name/cancel/exit branches. Read-only sessions cannot fabricate dirty edits, typeover or new-document writer support.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T050

Define explicit storage intents/results consuming actual WP03 Directory/Document/Destination concepts without filesystem operations in the reducer. Support loaded snapshot, same-file no-op with explicit decision and absent-destination publication; preserve UnsupportedReplacement, stale source, failure, cleanup residue and PublicationUncertain with DestinationMayExist. Tie results to operation/document revision; late or cancelled results cannot become another operation success.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T051

Test Given/When/Then session branches from WP13 and approved fragments, context-specific F1/Escape/F7, filename first-character/edit behavior, cursor/view preservation and unsupported transitions. Assert source/document immutability and no false save/exit success on failure/uncertainty. Publish supported-state matrix and original-to-domain comparison in internal/editor/evidence/.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-065, CMD51-066, CMD51-067, CMD51-069, CMD51-070, CMD51-087, CMD51-048, CMD51-049, CMD51-149. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Every enabled branch cites exact repeated original evidence; unresolved branches have explicit unsupported results.
- Normal F1 Undelete remains unsupported, prompt F1 follows its observed branch; Escape is contextual.
- Session state distinguishes no-op, new-name publication, unsupported replacement, failure and uncertain destination.

## Ownership and explicit limits

- No generic full editor, semantic writes, full menu/help/mouse/two-document support or new replacement transaction.
- Do not mutate internal/storage or internal/document owned sources; missing dependency APIs require a separately authorized scoped amendment, not duplicate models.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp17-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
