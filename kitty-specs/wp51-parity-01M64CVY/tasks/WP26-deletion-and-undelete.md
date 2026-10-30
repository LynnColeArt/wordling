---
work_package_id: WP26
title: Bold code deletion block repair and three-entry Undelete
dependencies:
- WP25
- WP23
- WP04
requirement_refs:
- FR-005
- FR-008
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T076
- T077
- T078
phase: Supported native editing continuation; full M1 remains open
history:
- at: '2026-10-30T23:29:50Z'
  actor: planner-priti
  action: Authored as a next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/document/
create_intent: []
execution_mode: code_change
owned_files:
- internal/document/**
role: implementer
tags:
- m1-continuation
- supported-native-editing
task_type: implementation
tracker_refs: []
---

# WP26: Bold code deletion block repair and three-entry Undelete

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

Implement command-specific native code deletion, blocked-pair repair and original three-entry Undelete over the admitted slice, without turning them into generic modern undo.

This is one bounded milestone within complete plain WP5.1 DOS parity.
It does not close an entire FR/NFR/FC, canonical scenario or inventory group.
All38 requirements and91 groups, original resource/language/platform duties,
new-document creation and remaining editing/storage/layout families stay visible.
PDF is optional M2 only after genuine M1 acceptance.

## Context and approved prerequisites

**Dependencies:** WP25, WP23, WP04.

**Requirement references:** FR-005, FR-008, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002.

**Compatibility references:** FC-002, FC-003, FC-004, FC-006, FC-007, FC-009.
Runtime requirement extraction may retain only FR/NFR/C in frontmatter;
these explicit FC references remain binding regardless of that projection.

**Binding contract:** `contracts/editing.md exact EC-200/201/202/203/204, EC-045, EC-043/211; approved WP23 grouping/history probes; approved WP25 mutation/writer API`.
Section labels are locators within approved artifacts, not invented filenames.
Verify actual source/fixture hashes before relying on them.
Unresolved contracts are stop/refusal prerequisites, never permission to guess.

**Canonical case leads:** CMD51-200, CMD51-201, CMD51-202, CMD51-203, CMD51-204, CMD51-045, CMD51-043, CMD51-211.
Read exact titles, feature IDs and observed scopes before using a case.
Local subcases need their own preconditions/native/output/state witnesses.
A valid but semantically unrelated ID is not acceptable evidence.

## Branch strategy and ownership placement

Planning and merge placement remain `feat/wp51-parity`; eventual GitHub
integration is `main` only through the actual accepted mission workflow.
Claim with `spec-kitty agent action implement WP26 --mission wp51-parity-01M64CVY --agent codex --profile implementer-ivan`.
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

### T076: Whole-code and block deletion semantics

1. Extend the actual immutable document mutation API from WP25. Target complete semantic tokens/gaps, never delimiter bytes, terminal cells or string-rendered code labels.

2. Implement the exact forward Delete and Backspace Bold-boundary outcomes of EC-200/201: remove both researched pair boundaries and preserve their text. Other attribute/code types require their own future evidence.

3. Implement EC-202/203 separately: a confirmed block containing only Bold On or only Bold Off preserves the observed attributed body and clears the block. Do not reuse the non-block remove-pair rule.

4. Implement EC-204 full attributed span deletion with exact gap ranges. Block No/cancel/reversed selection or other variants are enabled only where WP23 supplies complete repeated observations; otherwise return explicit unsupported outcomes.

5. Preserve command provenance, cursor mapping, semantic revision and any required native metadata updates from the reviewed writer contract. A body-equal repair must not be treated as proof that original command metadata/history are unchanged.

6. Reject malformed/unmatched/crossing/opaque spans or unsafe insertion destinations atomically before document/history/cursor mutation; do not silently repair arbitrary code structures.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T077: Command-provenance history and contextual preview

1. Model deletion entries newest-first with the original three-entry retention bound. Keep document state, stored fragments, grouping provenance and preview selection separate; this is not unlimited undo/redo.

2. Keep EC-204 attributed-fragment restoration distinct from EC-045 consecutive character deletion restoring plain BC. Save/Right/interleaving grouping rules must come from exact WP23 observations, not guessed timing or word boundaries.

3. Implement observed numeric F1/1 Restore and2 Previous transitions: previews do not insert, cancel leaves native bytes intact, reopening starts at newest, and restoration is relative to the current cursor.

4. Implement EC-211 eviction/cycling without exposing a fourth entry. No-history/fewer-entry, repeated Restore/consumption/reordering and refused/repaired-command history behavior require the reviewed WP23 branch-specific contract before enabling them.

5. Store lawful native fragments and required pair relationships, preserving original identity; do not store rendered labels or normalize to Unicode. Refuse restoration that would create unvalidated relationships.

6. Keep history transient under the established evidence. No history sidecar, crash-persistence promise, redo stack, arrow selection or cross-document behavior may be invented.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T078: Native and history acceptance without false equivalence

1. Write external-API Given/When/Then tests for every enabled deletion/history branch against approved exact original files, stage/case links and cursor witnesses.

2. Assert attributed versus plain restored native bodies separately; preview/cancel no-edit output must be byte-identical, and edit metadata differences must be those approved by WP23/25.

3. Verify failed/refused commands leave the prior document, history, preview and cursor unchanged. Include empty/adjacent spans, invalid gaps/revisions, opaque code lookalikes and retained fragment isolation.

4. Prove history capacity, eviction, grouping boundaries, preview isolation and repeated-restore behavior using original-derived assertions; a generic undo test is not acceptance for these commands.

5. Use the existing candidate verifier on representative Go outputs for pair removal, blocked-pair repair and attributed/plain restoration; retain original retrieve/edit/print/save and Wordling reopen evidence.

6. Run changed-scope Go/fuzz/negative checks appropriate to newly interpreted structures, declared regression and source immutability checks. Publish a command/branch support table under internal/document/evidence for WP27, retaining all other editing obligations.

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

Only the explicitly researched ASCII/Bold deletion and history branches. Center deletion, arbitrary other attributes, nested/crossing structures, general word/block/search commands, two-document history and modern undo/redo remain pending M1 scope; unsupported branches cannot be silently mapped to the nearest implemented command.

If a prerequisite API/field contract is insufficient, preserve the narrow blocker
and report a scoped follow-up. Do not duplicate a codec/transaction/model,
modify another owner out of map or weaken a prerequisite to force progress.

## Validation and independent review handoff

Run catalogue and genuine configured regression checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp26-validation.xml
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

Commit only owned source/evidence. Mark T076 T077 T078
done through `spec-kitty agent tasks mark-status --mission wp51-parity-01M64CVY`
with the actual subtask IDs and `--status done`, only after their real outputs pass.
Move WP26 to for_review with explicit `--agent codex --profile implementer-ivan`.
Poll that synchronous pre-review gate until it exits; do not bypass, kill or
reissue a running gate. Return actual commit/check commands and remaining limits.
An independent reviewer records exactly one canonical approve/reject verdict.
Rejection returns to this package with concrete feedback; no self-approval,
frontmatter lifecycle edits, forced success, mission acceptance or merge.
