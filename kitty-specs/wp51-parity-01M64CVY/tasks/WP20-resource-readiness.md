---
work_package_id: WP20
title: Historical graphics and language resource readiness register
dependencies:
- WP07
- WP08
- WP10
- WP12
requirement_refs:
- FR-011
- FR-014
- FR-015
- FR-016
- FR-017
- NFR-005
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T058
- T059
- T060
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: researcher-robbie
authoritative_surface: kitty-specs/wp51-parity-01M64CVY/contracts/resource-readiness.md
create_intent:
- kitty-specs/wp51-parity-01M64CVY/contracts/resource-readiness.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/wp51-parity-01M64CVY/contracts/resource-readiness.md
role: researcher
tags:
- m1-continuation
task_type: research
tracker_refs: []
---

# WP20: Historical graphics and language resource readiness register

## Identity, governance and prerequisites

Load `researcher-robbie` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP07, WP08, WP10, WP12.

**Requirement references:** FR-011, FR-014, FR-015, FR-016, FR-017, NFR-005, C-004, C-005, C-006.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md acquisition gate; structured-graphics.md S09–S14; language-data.md resource formats and locales`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

A concrete acquisition/readiness register identifies exact lawful resources and conflicts blocking historical DOS, graphics metrics and non-US/resource-format work.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T058

Create contracts/resource-readiness.md with identity/provenance/license/access fields for historical DOS, graphics-capable printer definition/font dependencies and original US language resources. Correlate installed hashes with baseline and mixed dates. Acquire/fingerprint only resources actually lawfully available; absent access remains a named blocker with next acquisition action, not a fabricated installed profile.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T059

Record independent per-format readiness for WPG, printer definitions/fonts, LRS/LEX/SUP/HYC/THS/SET, original worksheet producers/versions and relevant legacy .CRS/macro/graphics converter inputs. Preserve Greek/Russian/Hebrew/other original locale obligations and source edition applicability. Each entry gets fixture/format/oracle/resource/rights gaps and an explicit next bounded probe; no replacement dictionaries or modern worksheet substitution.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T060

Define reproducible profile qualification procedures for historical-DOS corroboration, L5–L7 fonts/graphics/preview and language tool comparisons. Include WPG byte-order prose-versus-diagram conflict, Link End offset13/filename14 overlap, nonzero packet8 size-array bounds, signed table formula directions and old/new borders as unresolved field-contract prerequisites. Distinguish acquisition/configuration decisions from actual scope changes requiring owner decision.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-175, CMD51-185, CMD51-146, CMD51-147, CMD51-181, CMD51-136, CMD51-137. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Every resource readiness assertion points to existing hash/access evidence; absent inputs remain unresolved.
- No historical DOS, graphics printer, foreign locale or binary resource codec is certified by the US text baseline.
- The register retains all format/conflict/locale obligations without licensing assumptions.

## Ownership and explicit limits

- No proprietary media/resource commits, executable harness or code, canonical registry change or new baseline selection.
- This is a planning artifact in the shared planning lane; it depends on planning outputs only and never waits for a code lane before unblocking another code lane.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `planning_artifact`: documentary register only, with no runnable source changes. It shares lane-planning with all planning packages. Do not add a code-lane dependency or execute a code→planning→code cycle. Research acceptance cannot establish implementation.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp20-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
