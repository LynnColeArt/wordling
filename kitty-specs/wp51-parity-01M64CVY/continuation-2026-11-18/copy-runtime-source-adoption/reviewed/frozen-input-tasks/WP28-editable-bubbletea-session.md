---
work_package_id: WP28
title: Runnable Bubble Tea native editing and Save As composition
dependencies:
- WP18
- WP27
- WP16
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- NFR-001
- NFR-002
- NFR-004
- C-001
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T082
- T083
- T084
phase: Supported native editing continuation; full M1 remains open
history:
- at: '2026-10-30T23:29:50Z'
  actor: planner-priti
  action: Authored as a next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/tui/
create_intent:
- docs/research/continuation/editable-session/
execution_mode: code_change
owned_files:
- internal/tui/**
- cmd/wordling/*.go
- docs/research/continuation/editable-session/**
role: implementer
tags:
- m1-continuation
- supported-native-editing
task_type: implementation
tracker_refs: []
---

# WP28: Runnable Bubble Tea native editing and Save As composition

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

Run the actual Linux executable through supported native editing, code/history interactions and changed-document Save As using the approved production components.

This is one bounded milestone within complete plain WP5.1 DOS parity.
It does not close an entire FR/NFR/FC, canonical scenario or inventory group.
All38 requirements and91 groups, original resource/language/platform duties,
new-document creation and remaining editing/storage/layout families stay visible.
PDF is optional M2 only after genuine M1 acceptance.

## Context and approved prerequisites

**Dependencies:** WP18, WP27, WP16.

**Requirement references:** FR-002, FR-004, FR-005, FR-006, NFR-001, NFR-002, NFR-004, C-001, C-002.

**Compatibility references:** FC-001, FC-002, FC-003, FC-004, FC-007, FC-009.
Runtime requirement extraction may retain only FR/NFR/C in frontmatter;
these explicit FC references remain binding regardless of that projection.

**Binding contract:** `approved WP18 actual application/model/IO composition; WP27 edit/dirty/save reducer; WP16 event/profile qualification boundary; WP24 candidate storage and WP25/26 document contracts`.
Section labels are locators within approved artifacts, not invented filenames.
Verify actual source/fixture hashes before relying on them.
Unresolved contracts are stop/refusal prerequisites, never permission to guess.

**Canonical case leads:** CMD51-046, CMD51-047, CMD51-043, CMD51-204, CMD51-069, CMD51-070, CMD51-087.
Read exact titles, feature IDs and observed scopes before using a case.
Local subcases need their own preconditions/native/output/state witnesses.
A valid but semantically unrelated ID is not acceptable evidence.

## Branch strategy and ownership placement

Planning and merge placement remain `feat/wp51-parity`; eventual GitHub
integration is `main` only through the actual accepted mission workflow.
Claim with `spec-kitty agent action implement WP28 --mission wp51-parity-01M64CVY --agent codex --profile implementer-ivan`.
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

### T082: Live original-key editing and shared view composition

1. Extend the actual cmd/wordling and Bubble Tea model from WP18; do not create an alternate demo. Retain the pinned Bubble Tea v2.1.1/module versions.

2. Translate supported input through WP16 and dispatch contextual commands through WP27. Preserve key identity and original keys; no q/Ctrl+Q/Ctrl+S convenience aliases or global Escape cancellation.

3. Render supported insertion/typeover, selection/block prompt, Undelete preview, dirty/name status and failure/unsupported states from the reducer. View does not own serialization, history semantics, token positions or printed layout.

4. Normal/Reveal panes consume the same document revision and semantic gap. Resize cannot mutate native data or silently hide unsupported codes; do not claim terminal wrapping equals WP layout.

5. Only loaded contract-admitted documents are editable in this tranche. Blank/new native document saving, F6 new attributes, unsupported identities and other original commands retain explicit incomplete status.

6. Verify actual production imports/callers of new document/editor/storage methods. Passing tests for unused helpers or an independent toy command do not satisfy this package.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T083: Real candidate storage commands and pending-result handling

1. Wire actual WP24 candidate publication through tea.Cmd/messages and WP27 identities, alongside existing no-edit operations. Require the declared validated rooted local directory/profile; do not invent DOS-to-Linux path aliases.

2. Exercise real source/destination observations and immutable candidates. Use the original filename first-character/edit/cancel behavior that WP13 establishes, with explicit bounded host path limitations.

3. Refuse actual existing-file replacement; show real failure, stale and uncertain/residue outcomes. A possible destination side effect cannot be presented as absent, a clean document, or a successful exit.

4. Handle typing/resize/cancel while IO is pending according to revision-bound reducer rules. Late responses may acknowledge an older publication without falsely saving the newer current document.

5. Keep original source files unchanged and new-name publication byte-exact to the supported writer candidate. Preserve terminal restoration/abnormal host termination distinctions inherited from the pinned library.

6. No new semantic byte manipulation in TUI, parallel storage transaction, host file-dialog replacement, recovery sidecar, actual-overwrite shortcut or unverified locking/durability guarantee is permitted.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T084: Executable editing session and failure evidence

1. Launch the actual command on Linux, retrieve the admitted original fixture, type/edit supported ASCII, toggle typeover/Reveal, perform reviewed code deletion/history actions and Save As a fresh basename.

2. Capture actual raw/event/model/view outputs, before/after native lengths/SHA/bytes and source integrity. Distinguish synthetic PTY transport, typed integration and genuinely qualified physical delivery.

3. Use real temporary directories for success and failure/race cases: destination appears, source changes, stale responses, cancel during pending IO, uncertain publication, resize and unknown events.

4. Compare enabled prompt/cursor/native transitions independently against approved WP13/WP23/26 evidence; do not label the whole canonical scenario verified from one happy path.

5. Run declared Go/test/vet/build/gofmt/regression checks and meaningful executable integration tests. Publish reproducible commands, supported profile/command matrix and incomplete branches under editable-session/.

6. Approval requires the actual runnable composition; WP29 performs independent original interoperability acceptance on its outputs. No complete M1, layout, printer implementation or physical workflow acceptance follows here.

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

No new semantic writer, document-model fork, actual overwrite, backup/Fast Save, layout engine, PDF, modern keyboard aliases or full editor claim. Physical keys remain qualified only by actual captured delivery evidence, never synthetic PTY decoding alone.

If a prerequisite API/field contract is insufficient, preserve the narrow blocker
and report a scoped follow-up. Do not duplicate a codec/transaction/model,
modify another owner out of map or weaken a prerequisite to force progress.

## Validation and independent review handoff

Run catalogue and genuine configured regression checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp28-validation.xml
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

Commit only owned source/evidence. Mark T082 T083 T084
done through `spec-kitty agent tasks mark-status --mission wp51-parity-01M64CVY`
with the actual subtask IDs and `--status done`, only after their real outputs pass.
Move WP28 to for_review with explicit `--agent codex --profile implementer-ivan`.
Poll that synchronous pre-review gate until it exits; do not bypass, kill or
reissue a running gate. Return actual commit/check commands and remaining limits.
An independent reviewer records exactly one canonical approve/reject verdict.
Rejection returns to this package with concrete feedback; no self-approval,
frontmatter lifecycle edits, forced success, mission acceptance or merge.
