---
work_package_id: WP18
title: Runnable Bubble Tea no-edit session composition
dependencies:
- WP03
- WP15
- WP16
- WP17
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- C-001
- C-002
- NFR-001
- NFR-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-10-31T00:00:01.238151+00:00'
subtasks:
- T052
- T053
- T054
phase: Bounded M1 continuation; full parity remains open
history:
- at: '2026-10-30'
  actor: planner-priti
  action: Authored from approved contracts; not executed or accepted
agent_profile: implementer-ivan
authoritative_surface: internal/tui/
create_intent:
- internal/tui/
- cmd/wordling/
- docs/research/continuation/composed-session/
execution_mode: code_change
owned_files:
- internal/tui/
- cmd/wordling/
- docs/research/continuation/composed-session/
role: implementer
tags:
- m1-continuation
task_type: implementation
tracker_refs: []
---

# WP18: Runnable Bubble Tea no-edit session composition

## Identity, governance and prerequisites

Load `implementer-ivan` through resolver-backed profile loading and load action-scoped charter context. Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md and continuation.md. Read all dependency outputs and their independent review findings. Use canonical runtime; do not self-approve, accept/merge the mission or advance another package.

**Dependencies:** WP03, WP15, WP16, WP17.

**Requirement references:** FR-002, FR-004, FR-005, FR-006, C-001, C-002, NFR-001, NFR-002, FC-002, FC-004, FC-009.

**Binding approved contract:** `kitty-specs/wp51-parity-01M64CVY/contracts/session.md bounded Bubble Tea view/storage composition; WP13 state matrix; WP16 qualified event profiles; WP17 reducer`. Section labels after the filename are locators. These are bounded evidence contracts; read exact tables/ledgers and verify fixture/source hashes before using them.

## Objective and observable outcome

Run the real Linux Go application through a bounded retrieve/Reveal/cursor/no-edit-save/cancel/exit workflow, composing approved libraries rather than stopping at helper packages.

This package is one milestone within complete WP 5.1 DOS parity. Completion does not close the entire referenced FR/FC/NFR or a parent inventory group. The continuation ledger retains remaining branches, resources, implementation and differential-verification work. PDF stays optional M2.

## Scope, outputs and subtasks

### T052

Implement cmd/wordling/main.go and internal/tui/ Bubble Tea model using pinned v2, input adapter, editor reducer and shared document. Render normal/Reveal panes and exact supported prompt/status states; View cannot decide native serialization, semantic positions or printed layout. Handle resize without changing native data; expose unsupported/unqualified input states truthfully.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T053

Wire actual WP03 rooted Directory.Read/Observe/Save operations through tea.Cmd/messages and reducer identities. Require declared validated local directory/profile; preserve flat-basename and path limitations visibly, with no invented DOS-to-Linux aliasing. Publish only supported no-op/new-name results; refuse actual replacement and unsupported editing; failure/uncertain outcomes retain document and never present complete success.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

### T054

Execute composed application scenarios against WP13 original traces and WP16 actual qualified delivery where available. Test real temp-directory native preservation, source races, stale messages, cancel during pending IO, resize and unknown input. Export bytes/length/SHA before/after; publish state/capture/raw-input comparisons and unqualified branches in docs/research/continuation/composed-session/.

**Required evidence:** commit the concrete output and validation described above on this package’s owned surfaces; preserve rejected or incomplete branches explicitly. A plan to do the work is not completion.

## Source and evidence contract

Use the selected plain U.S. English DOS WP5.1 Help03/09/92 baseline and declared QEMU/FreeDOS1.4/mixed-date Standard Printer limitations. Never claim historical DOS, graphics metrics or another locale from that baseline. Source identity includes executable, resources/settings, runner and fixtures; source publication dates do not prove executable behavior.

Canonical case leads: CMD51-065, CMD51-066, CMD51-067, CMD51-087, CMD51-048, CMD51-049, CMD51-149. These links are scope leads, not completed Wordling comparisons. Read exact titles/features and recorded oracle_status before selecting a fixture. Local subcases must have explicit starting state and output; no unrelated valid ID can substitute for semantic association.

Evidence levels stay distinct: documentary expectation, repeated original observation, implemented component, and differential Wordling/original verification. Do not edit raw evidence, normalize bytes, silently replace resources or promote canonical verified statuses based on self-comparison. Project-authored lawful scratch fixtures must retain provenance and raw SHA-256/length. Proprietary executables/manuals/resources stay external and ignored.

## Acceptance criteria

- go run ./cmd/wordling launches the actual bounded session on Linux; integration consumes storage/document/editor/input APIs.
- Original command prompts/states and byte-exact no-edit outputs are compared independently.
- Any unavailable physical terminal qualification remains a declared blocker to physical workflow acceptance; synthetic integration alone does not claim supported terminal parity.

## Ownership and explicit limits

- No new semantic native writer, typeover/delete/history, actual overwrite, backup, Fast Save, layout engine, PDF or full-editor completion claim.
- No generic q/Ctrl+Q/Ctrl+S shortcuts. Keep incomplete M1 functions explicit rather than adding speculative remapping or placeholder success.

Owned source paths are exactly the frontmatter `owned_files`; `create_intent` authorizes absent paths only. Do not modify dependency-owned sources, existing WP01–WP12 prompts, other lifecycle state, central plan or continuation ledger. If an API/contract is insufficient, record the narrow blocker and request a scoped follow-up rather than implementing a duplicate codec/model or expanding ownership silently.

This is honestly `code_change`: executable Go/Python harness or application code is part of the deliverable. Run in the canonical dependency-aware code lane. WP02 code exists at approved e7de080 and WP03 at approved 7deeaf6; the planning checkout has neither Go implementation. Resolve actual dependency commits in the assigned lane before making code claims. Do not reclassify as planning to bypass lane guards.

## Validation and independent review handoff

Run both catalogue checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp18-validation.xml
```

For changed Go, run gofmt, `go build ./...`, `go test ./...` and `go vet ./...`; include real failure/race tests where pending IO/filesystem state is involved. New or changed binary token interpretation needs negative/malformed cases, measured bounds and reproducible fuzz budget. Semantic writers require separately authorized native field contracts and original retrieve/edit/print/save evidence; this package cannot infer such authority from no-edit exports.

For Python harness changes, compile changed files and run existing harness/unit checks appropriate to the changed boundary. Original probes require two fresh-copy repetitions with exact profile/source/native/capture hashes and archived runner. Report an unavailable prerequisite honestly; do not fabricate a passing oracle or physical terminal result. Review must be able to rerun the evidence checks from committed manifests.

Commit only owned implementation/evidence surfaces using the applicable mission placement. Keep lifecycle events under runtime authority. Record actual commands, outputs, refusals and remaining limits in the owned evidence/report; mark this package’s subtasks and move it for independent review only after required checks pass. A blocked acceptance prerequisite must remain visible. No full-parity, success-criteria, acceptance or merge claim follows from this package.
