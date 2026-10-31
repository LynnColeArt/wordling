---
work_package_id: WP29
title: Executable native edit original-app differential acceptance
dependencies:
- WP28
- WP23
- WP14
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- FR-008
- FR-015
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- NFR-005
- C-001
- C-002
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-10-31T08:45:01.815525+00:00'
subtasks:
- T085
- T086
- T087
phase: Supported native editing continuation; full M1 remains open
history:
- at: '2026-10-30T23:29:50Z'
  actor: planner-priti
  action: Authored as a next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: scripts/reference/wordling_edits.py
create_intent:
- scripts/reference/wordling_edits.py
- tests/compatibility/editing/
- docs/research/continuation/editing-differential/
execution_mode: code_change
owned_files:
- scripts/reference/wordling_edits.py
- tests/compatibility/editing/**
- docs/research/continuation/editing-differential/**
role: implementer
tags:
- m1-continuation
- supported-native-editing
task_type: implementation
tracker_refs: []
---

# WP29: Executable native edit original-app differential acceptance

## Do this first: resolve profile and governance

Use the resolver-backed profile-load skill before implementing this package.
Resolve `implementer-ivan` with `spec-kitty agent profile show implementer-ivan`;
apply its initialization/boundaries and action-scoped charter context.
The assigned role is `implementer` and the configured tool is `codex`.
Read spec.md, plan.md, data-model.md, docs/compatibility.md, docs/roadmap.md
and both historical and appended checkpoints in continuation.md.
Read every actual prerequisite output and its independent review findings.
Use canonical runtime commands with `--mission wp51-parity-01M64CVY`.
Do not self-approve, advance another WP, accept/merge M1 or start M2.

## Objective

Independently exercise the real executable and its native edit outputs against the original application, retaining bounded case-level results and the complete remaining parity gap.

This is one bounded milestone within complete plain WP5.1 DOS parity.
It does not close an entire FR/NFR/FC, canonical scenario or inventory group.
All38 requirements and91 groups, original resource/language/platform duties,
new-document creation and remaining editing/storage/layout families stay visible.
PDF is optional M2 only after genuine M1 acceptance.

## Context and approved prerequisites

**Dependencies:** WP28, WP23, WP14.

**Requirement references:** FR-002, FR-004, FR-005, FR-006, FR-008, FR-015, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, C-001, C-002, C-004, C-005, C-006.

**Compatibility references:** FC-001, FC-002, FC-003, FC-004, FC-006, FC-007, FC-008, FC-009.
Runtime requirement extraction may retain only FR/NFR/C in frontmatter;
these explicit FC references remain binding regardless of that projection.

**Binding contract:** `actual approved WP28 executable and WP23 candidate verifier/field ledger; original WP04/WP13/23 command witnesses; reviewed WP14 matching text print procedure`.
Section labels are locators within approved artifacts, not invented filenames.
Verify actual source/fixture hashes before relying on them.
Unresolved contracts are stop/refusal prerequisites, never permission to guess.

**Canonical case leads:** CMD51-046, CMD51-047, CMD51-048, CMD51-149, CMD51-200, CMD51-201, CMD51-202, CMD51-203, CMD51-204, CMD51-045, CMD51-043, CMD51-211.
Read exact titles, feature IDs and observed scopes before using a case.
Local subcases need their own preconditions/native/output/state witnesses.
A valid but semantically unrelated ID is not acceptable evidence.

## Branch strategy and ownership placement

Planning and merge placement remain `feat/wp51-parity`; eventual GitHub
integration is `main` only through the actual accepted mission workflow.
Claim with `spec-kitty agent action implement WP29 --mission wp51-parity-01M64CVY --agent codex --profile implementer-ivan`.
Use the exact workspace returned by runtime; never choose a lane/base manually.
All code/evidence edits and commits happen in that workspace.
This package is honestly `code_change`, not a planning-artifact workaround.

Owned surfaces are exactly frontmatter owned_files; real sequential overlaps
with prerequisite WPs remain narrow and share the computed code lane.
No codebase-wide exemption or fake disjoint/new-file claim is selected.
Primary has no approved Go packages: source exists in dependency code lanes.
Verify actual approved commits/APIs in the assigned workspace before editing.
Zero-primary-match glob warnings describe that placement, not absent code.
Existing implementation source is not new create_intent; only truly new paths are.
Do not modify old prompts, requirements, lifecycle metadata, canonical registries,
another package's surface or the historical continuation ledger.

## Scope, outputs and subtasks

### T085: Repeatable executable/original differential driver

1. Implement the owned wordling_edits.py and compatibility/editing harness to launch the actual built cmd/wordling, not a serializer helper substituted for the product.

2. Select a small exact matrix covering insertion/typeover, code-boundary retention, paired deletion, block repair, attributed/plain restoration, three-entry preview/cancel/eviction, no-edit export and changed Save As.

3. Bind each local subcase to its canonical title/features, starting native fixture and reviewed original branch. Missing canonical breadth remains an explicit local proposal; no canonical registry edits belong to this package.

4. Record executable/build/module/host/input profile, exact fixture/runner hashes, raw event/state/native captures and command sequence. Distinguish model-level protocol tests from unavailable physical keyboard delivery.

5. Invoke WP23 candidate verification for original Retrieve, subsequent edit, selected-profile print and Save. Serialize guest access through the common lock under root scheduling; fresh copies and stopped-disk extraction remain mandatory.

6. Retain diagnostics and reproducible negative-path runs as such. No screenshot resemblance, helper self-comparison, successful process exit or parser round trip alone establishes interoperability.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T086: Native and observable comparisons with real failures

1. Compare original and Wordling command states/cursors/mode/history/prompt results independently. Verify exact intended body semantics and explained structural updates; retain unrelated prefix/code bytes.

2. No-edit supported outputs require exact bytes/length/SHA. Edited outputs need only the approved differences, and all changed relationships must be valid when the original reopens/edits/prints/saves them.

3. Keep complete raw selected-profile printer streams and predeclared exact/geometry criteria. These observations exercise original printing of candidates, not a newly implemented Wordling print engine or graphics/preview fidelity.

4. Reopen the original-resaved outputs in Wordling and record recognized/read-only/unsupported distinctions honestly. Unknown formatter/resource variants cannot be silently normalized or called safely editable.

5. Exercise refused unsafe inputs, failed/short writes, source/destination interference, stale messages and uncertainty through actual external boundaries available to the executable. Verify source integrity and absence of false clean/save/exit claims.

6. If a valid product defect is found, publish exact reproducer and structured finding for a scoped dependent repair package. Do not edit dependency-owned code out of map or weaken the comparison to make the package pass.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T087: Checkable bounded verdict and remaining M1 obligations

1. Publish machine-readable per-subcase verdicts, captured starting/ending states, source/candidate/output/stream hashes and rerunnable commands under editing-differential/. Verify Git blob bytes against manifests.

2. Separate original-observed, implemented component, executable integration, differential pass/fail and physically qualified status. A passed local slice does not close its canonical scenario or parent feature.

3. Include negative checks for wrong same-feature case association, missing final capture, missing print/native output, tampered blob and a simulated false-success save so evidence failures cannot become passes.

4. Run genuine catalogue/regression and changed Go/Python checks. Retain current policy/resource refusals as implementation limitations with pending work, not historical DOS capacity or owner-approved exclusions.

5. Retain all38 requirement and91 group obligations by reference to continuation.md and give concrete next editing/storage/formatting work still absent: new native documents, actual replacement/backups, other characters/attributes/commands and layout/printing beyond this slice.

6. Do not accept/merge M1 or start M2 even if all29 packages are approved. Remaining full-scope obligations and external qualification gaps require further reviewed execution; root owns queue continuation and mission-level gates.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

## Source and evidence boundary

Use selected plain U.S. English DOS WP5.1 Help03/09/92 with pinned
executable/resources/settings and declared QEMU/FreeDOS1.4 mixed-date
Standard Printer limitations. Never silently select another baseline/resource.
Source publication dates do not prove March executable applicability.
Historical DOS, graphics metrics/preview, foreign-language resources and
physical terminal delivery remain independent unresolved qualification duties.
Reference binaries/manuals/dictionaries/images remain external and ignored.
Only lawful project-authored fixtures and permitted evidence may be committed.

Every original probe uses a fresh private copy and an archived executing runner,
actual shared lock, root-coordinated exclusive VM slot and normal guest exit
before stopped-image extraction. No speculative lock-free parallel guest jobs.
Retain native/source/stream/capture length+SHA and raw bytes without normalization.
Put necessary -text/blank-row attributes inside the owned evidence subtree;
verify committed Git blob bytes, not just working-tree hashes.
Keep documentary expectation, original observation, implemented component,
executable differential result and physical qualification distinct.

## Acceptance criteria

- Every enabled behavior and changed native field has the exact approved
  precondition/contract and durable evidence, with explicit unsupported outcomes.
- Original and unrelated bytes survive failed/refused edits/saves; no false
  saved/clean/exit success follows uncertainty or a stale result.
- Actual production APIs/entry points within this package's authorized boundary
  are used; a detached helper or duplicate model is not a completed integration.
- No whole-parent verification, resource qualification, full M1 acceptance or
  M2 feature is inferred from this package's local passing cases.
- Required original/native/print results cannot be replaced by parser
  self-comparison, screenshot resemblance or sealed process success alone.

## Ownership and explicit limits

Only local differential harness/reports/tests; no dependency source edits, canonical registry promotion, parity-percentage claim, new baseline, normalized native evidence, graphic profile, full print engine or physical-delivery substitution. Dependency defects require a separately owned repair package, not an audit-scope write.

If a prerequisite API/field contract is insufficient, preserve the narrow blocker
and report a scoped follow-up. Do not duplicate a codec/transaction/model,
modify another owner out of map or weaken a prerequisite to force progress.

## Validation and independent review handoff

Run catalogue and genuine configured regression checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp29-validation.xml
```

Changed Go passes gofmt, `go build ./...`, `go test ./...`, `go vet ./...`.
Use meaningful external-API contract assertions and changed-boundary negative
cases; filesystem/pending-state changes require real failures/races as relevant.
Changed Python compiles and executes appropriate harness/unit tests.
Changed binary decoding/writing declares measured input/allocation/traversal
limits, original+malformed seeds and repeatable fuzz budget before acceptance.
Compare no-edit length/SHA/bytes and caller ownership; preserve false-success,
unexplained native diffs and missing original observations as failures.
Run changed-scope lint/diff checks; fix actual findings without repeated broad
testing after all required checks pass unless a new concern justifies it.

Commit only owned source/evidence. Mark T085 T086 T087
done through `spec-kitty agent tasks mark-status --mission wp51-parity-01M64CVY`
with the actual subtask IDs and `--status done`, only after their real outputs pass.
Move WP29 to for_review with explicit `--agent codex --profile implementer-ivan`.
Poll that synchronous pre-review gate until it exits; do not bypass, kill or
reissue a running gate. Return actual commit/check commands and remaining limits.
An independent reviewer records exactly one canonical approve/reject verdict.
Rejection returns to this package with concrete feedback; no self-approval,
frontmatter lifecycle edits, forced success, mission acceptance or merge.
