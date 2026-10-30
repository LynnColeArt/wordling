---
work_package_id: WP14
title: Original text layout controls and print streams
dependencies:
- WP07
- WP12
requirement_refs:
- FR-008
- FR-009
- FR-015
- NFR-004
- NFR-005
- C-005
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T040
- T041
- T042
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: researcher-robbie
authoritative_surface: scripts/reference/text_layout.py
create_intent:
- scripts/reference/text_layout.py
- docs/research/continuation/text-layout/
execution_mode: code_change
owned_files:
- scripts/reference/text_layout.py
- docs/research/continuation/text-layout/
role: researcher
tags:
- m1-continuation
task_type: research
tracker_refs: []
---

# WP14: Original text layout controls and print streams

## Identity, governance and prerequisites

Load `researcher-robbie` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP07, WP12.

**Requirement references:** FR-008, FR-009, FR-015, NFR-004, NFR-005, FC-008, C-005.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md L1–L4 and text-only L6, units and predeclared tolerances`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Obtain elementary text/native/print observations on the current declared text profile without waiting for graphics resources.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T040

Implement scripts/reference/text_layout.py using current fingerprinted profile and exact L1–L4 variants: hard/soft returns, hard/automatic pages, margins and absolute/relative tab stops. Select/capture every declared paper/font/line-height/spacing/numbering setting; stop any variant whose inputs cannot actually be expressed.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T041

Execute text L6 for each accepted L1–L4 native fixture to a fresh scratch output. Retain complete streams including initialization/terminators, original native before/after, line/page membership, exact accepted settings and trace. Identify printer-language/unit interpretation from evidence; do not invent 6 lines/inch, glyph advances, soft codes inside opaque payload or missing defaults.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T042

Repeat accepted variants twice and publish per-variant machine manifest, native/code annotations, line/page and print-stream comparison plus unresolved unit/tolerance questions under docs/research/continuation/text-layout/. Freeze any geometry tolerance with derivation before comparing positions. Link local L variants to canonical cases and propose missing subcases locally; canonical expansion is a later scoped change.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-111, CMD51-112, CMD51-197, CMD51-162, CMD51-163, CMD51-101, CMD51-103, CMD51-145, CMD51-165. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Two fresh runs for each accepted local variant, with exact hashes and declared settings.
- A missing print stream, ambiguous control or unmeasured origin is a visible unresolved result.
- Text print observations never certify graphics, preview or full NFR-005.

## Ownership and explicit limits

- No application layout engine, terminal-derived wrapping, graphics L5/L7 acceptance, native writer or canonical registry edits.
- If new canonical cases are required, retain explicit candidate records in the owned report; do not silently call the complete canonical scenario observed.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp14-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
