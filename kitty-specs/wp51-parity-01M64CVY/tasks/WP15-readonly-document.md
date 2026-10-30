---
work_package_id: WP15
title: Read-only native token gaps and shared Reveal view
dependencies:
- WP02
- WP04
- WP10
- WP12
requirement_refs:
- FR-002
- FR-004
- FR-005
- NFR-001
- NFR-003
- C-001
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T043
- T044
- T045
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: implementer-ivan
authoritative_surface: internal/document/
create_intent:
- internal/document/
execution_mode: code_change
owned_files:
- internal/document/
role: implementer
tags:
- m1-continuation
task_type: implementation
tracker_refs: []
---

# WP15: Read-only native token gaps and shared Reveal view

## Identity, governance and prerequisites

Load `implementer-ivan` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP02, WP04, WP10, WP12.

**Requirement references:** FR-002, FR-004, FR-005, NFR-001, NFR-003, FC-002, FC-004, C-001.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/editing.md token/gap notation and EC-048; native-framing.md; language-data.md native identity boundary`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Provide one immutable document and semantic token-gap cursor for the accepted ASCII/C3/C4 Bold fixture, usable by both session views.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T043

Implement internal/document/document.go and README.md against approved wp51.Parse/Image/Inspect/Bytes/Export APIs. Recognize printable ASCII and the exact C3/C4 Bold token identities established by the ORIGIN fixture; retain complete source spans/opaque codes and exact image. Publish supported-token/read-only/refusal distinctions. Never treat parse success as edit permission or an opaque sequence as empty text.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T044

Implement bounded gap traversal and derived normal/Reveal presentations over the same token sequence. Test the ORIGIN ten-byte body and exact gaps g0..g6; toggling views changes no document or cursor. Unknown tokens retain raw identity and an explicit unsupported rendering/movement boundary; no cursor can enter a multi-byte token. No terminal-cell or inch-based indexing.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T045

Add external-API document tests, malformed/boundary/unknown-token cases and buffer isolation; record measured traversal/allocation limits and reproducible fuzz invocation in internal/document/evidence/. Compare original fixture hash/length/bytes before and after every read-only operation. Keep all parsing bounded by WP02 limits.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-048, CMD51-049, CMD51-204. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- The consumer imports approved internal/wp51 rather than copying the decoder.
- Original ORIGIN source and Export remain exact; normal and Reveal share the same semantic gap.
- Separate assertions cover malformed framing, unsupported semantics and valid opaque preservation.

## Ownership and explicit limits

- No insertion/typeover/deletion/Undelete/selection semantics or native mutation/serialization.
- C0 Compose identity and arbitrary attributes/nested functions remain distinct later contracts; never map arbitrary bytes to Unicode.
- Endpoint movement required by unobserved session branches remains gated on WP13.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp15-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
