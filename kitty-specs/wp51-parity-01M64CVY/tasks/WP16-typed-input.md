---
work_package_id: WP16
title: Pinned Bubble Tea input adapter and delivery qualification
dependencies:
- WP11
- WP12
requirement_refs:
- FR-004
- FR-017
- C-001
- C-006
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T046
- T047
- T048
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: implementer-ivan
authoritative_surface: internal/input/
create_intent:
- internal/input/
- cmd/wordling-input-probe/
- docs/research/continuation/terminal-input/
execution_mode: code_change
owned_files:
- internal/input/
- cmd/wordling-input-probe/
- docs/research/continuation/terminal-input/
role: implementer
tags:
- m1-continuation
task_type: implementation
tracker_refs: []
---

# WP16: Pinned Bubble Tea input adapter and delivery qualification

## Identity, governance and prerequisites

Load `implementer-ivan` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP11, WP12.

**Requirement references:** FR-004, FR-017, C-001, C-006, NFR-004.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/session.md pinned v2 capability check, proposed qualification target and ambiguity table`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Translate typed pinned-v2 events without guessing original command context and provide an executable physical-delivery qualification harness.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T046

Implement internal/input/ adapter using charm.land/bubbletea/v2 v2.1.1 and actual KeyPressMsg Code/Mod/Text and capability Supports APIs. Keep physical event identity separate from contextual session command resolution. Include paste/mouse/resize/capability/release/repeat/unknown events without interpreting paste as command chords; no dependency update.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T047

Implement cmd/wordling-input-probe/ to record raw/event/profile evidence for direct Linux PTY US/UTF-8 candidate profile. Capture terminal binary/version/config/TERM/terminfo and negotiation response, exact physical original F1/F3/F7/F10, Alt+F3, Shift+F10, Alt+=, Home/Right, Escape5x and ambiguous Ctrl/Tab/Enter/Backspace pairs. Archive split/delayed ESC and enhanced/legacy transport observations separately.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T048

Test typed/synthetic fragmented/unknown/capability/paste/resize paths and publish actual delivery qualification or a precise blocked matrix under docs/research/continuation/terminal-input/. Synthetic decoding cannot qualify unavailable physical delivery. Retain terminal/desktop-conflicting chords as unresolved resources or owner decisions only when a scope change is proposed.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-001, CMD51-005, CMD51-048, CMD51-065, CMD51-066, CMD51-087. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- Code compiles against pinned v2 APIs and preserves original event distinctions where delivered.
- Actual supported profile label requires physical capture and exact decoded Code/Mod outcomes; unavailable hardware/profile yields an explicit blocked qualification.
- No q/Ctrl+Q/Ctrl+S/global Escape fallback is invented.

## Ownership and explicit limits

- No document, session reducer, menu engine or storage mutation.
- Do not change original shortcuts to evade desktop interception. Profile configuration can be qualified; a parity baseline change requires explicit owner decision.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp16-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
