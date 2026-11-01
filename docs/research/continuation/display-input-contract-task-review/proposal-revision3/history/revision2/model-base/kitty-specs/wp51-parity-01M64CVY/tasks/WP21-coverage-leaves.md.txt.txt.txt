---
work_package_id: WP21
title: Command workbook and utility leaf coverage expansion
dependencies:
- WP05
- WP12
requirement_refs:
- FR-001
- NFR-004
- C-003
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T061
- T062
- T063
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/coverage-leaves.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/coverage-leaves.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/coverage-leaves.md
role: researcher
tags:
- m1-continuation
task_type: research
tracker_refs: []
---

# WP21: Command workbook and utility leaf coverage expansion

## Identity, governance and prerequisites

Load `researcher-robbie` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP05, WP12.

**Requirement references:** FR-001, NFR-004, C-003, C-005, C-006.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md 431 dispositions, G01–G09, V01–V08 and 36 workbook lessons`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Expand a bounded first leaf tranche (G01–G03 and workbook lessons WB01–WB03) into exact source/version obligations, retaining all remaining leaves and lessons visibly uncovered.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T061

Create contracts/coverage-leaves.md with stable local leaf IDs and exact REF/WB/SDK page/section locators for priority gaps G01–G03: printer/font branches, List Files confirmation/failures, and display/editing-option setup. Reconcile relevant version lead V02 against March executable evidence. Do not treat existing thematic links as complete behavior. Retain G04–G09 and remaining version leads in an explicit pending table.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T062

For workbook lessons WB01–WB03 enumerate actual numbered exercise/step obligations against source text and correction pages, mark indexed/studied/observed/uncovered separately and map to parent inventory/canonical case candidates. Include a complete WB01–WB36 status table with WB04–WB36 visibly pending step expansion. If source access is absent, retain a specific blocker rather than calling a lesson complete.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T063

Publish a machine-checkable local leaf register, bounded first-tranche coverage counts and source hashes with missing canonical case proposals and bounded later queue-authoring recommendations. Preserve all remaining reference/menu/appendix/utility and workbook obligations, including all 91 parent groups. Do not edit accepted prior contracts or canonical registries; no implemented/verified labels follow from documentary reading.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- G01–G03 and WB01–WB03 have exact leaf/step dispositions; every other gap/lesson remains explicitly pending, and all 91 groups remain accounted for.
- No command leaf is marked implemented/verified from source reading; evidence level/status stay separate.
- Remaining authoring work is enumerated for a future ownership-scoped queue revision; no empty-queue acceptance.

## Ownership and explicit limits

- No executable implementation or rewritten WP05 contract; no new scope exclusions or oracle promotions.
- The entire package is documentary work in the single planning lane.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `planning_artifact`: documentary register only, with no runnable source changes. It shares lane-planning with all planning packages. Do not add a code-lane dependency or execute a code→planning→code cycle. Research acceptance cannot establish implementation.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp21-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
