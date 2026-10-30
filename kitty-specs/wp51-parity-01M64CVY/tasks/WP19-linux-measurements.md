---
work_package_id: WP19
title: Measured Linux session latency resource and binary size investigation
dependencies:
- WP14
- WP18
requirement_refs:
- C-001
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T055
- T056
- T057
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: implementer-ivan
authoritative_surface: tests/performance/
create_intent:
- tests/performance/
- docs/research/continuation/linux-measurements/
execution_mode: code_change
owned_files:
- tests/performance/
- docs/research/continuation/linux-measurements/
role: implementer
tags:
- m1-continuation
task_type: implementation
tracker_refs: []
---

# WP19: Measured Linux session latency resource and binary size investigation

## Identity, governance and prerequisites

Load `implementer-ivan` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP14, WP18.

**Requirement references:** C-001, NFR-003, NFR-004.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/research.md open investigation 4; plan.md resource/latency/size gates; WP02 measured parser evidence; WP18 actual composition`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Replace unmeasured performance assumptions with reproducible Linux distributions, scaling/size evidence and proposed budgets on the real bounded application.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T055

Add tests/performance/ benchmark/measurement harness consuming actual composition APIs, approved original fixtures, text probe fixtures and lawful generated scaling cases up to current 16 MiB policy. Measure read/parse, token traversal, reducer event, View, no-edit export/publication and cold/warm startup separately; declare counts/warmups/repetitions/clock and avoid hiding refusals.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T056

Record hardware/OS/kernel/filesystem/terminal/toolchain/module revisions, build flags, exact fixtures and harness hashes. Publish raw latency samples and p50/p95/p99 with sample counts; allocations and peak process RSS with method/overhead, binary bytes for default and explicitly stripped builds, dependency/build breakdown and scaling curves. Distinguish input-to-model/render latency from actually measured physical-to-paint latency; absent physical measurement stays unknown.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T057

Publish reproducible commands/machine outputs and evidence-based latency/size/resource budget proposals in docs/research/continuation/linux-measurements/. Explain hot spots and candidate bounded follow-ups, limits/refusals, host variance and budget rationale. Retain original timing comparisons as qualified only where actually measurable; do not invent a product SLO or mark a proposed threshold accepted.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Raw samples, binary hashes/size and environment are independently rerunnable, not only prose summaries.
- Any threshold is explicitly proposed pending review; reader policy ceilings and fuzz RSS never become historical application limits.
- No optimizations or dependency changes are bundled into this investigation.

## Ownership and explicit limits

- No full-app performance claim beyond implemented bounded session or graphical layout.
- New benchmark code receives real Go checks; generated max-size inputs retain synthetic labels.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp19-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
