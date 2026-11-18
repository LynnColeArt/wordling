---
work_package_id: WP25
title: Immutable ASCII Bold edits and supported native serialization
dependencies:
- WP15
- WP23
requirement_refs:
- FR-002
- FR-005
- FR-008
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-005
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T073
- T074
- T075
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

# WP25: Immutable ASCII Bold edits and supported native serialization

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

Implement real supported semantic mutations and direct original-format candidate export over the reviewed loaded ASCII/Bold slice, with original-app writer acceptance before approval.

This is one bounded milestone within complete plain WP5.1 DOS parity.
It does not close an entire FR/NFR/FC, canonical scenario or inventory group.
All38 requirements and91 groups, original resource/language/platform duties,
new-document creation and remaining editing/storage/layout families stay visible.
PDF is optional M2 only after genuine M1 acceptance.

## Context and approved prerequisites

**Dependencies:** WP15, WP23.

**Requirement references:** FR-002, FR-005, FR-008, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-005.

**Compatibility references:** FC-001, FC-002, FC-003, FC-004, FC-006, FC-007, FC-009.
Runtime requirement extraction may retain only FR/NFR/C in frontmatter;
these explicit FC references remain binding regardless of that projection.

**Binding contract:** `approved WP23 native-edits/contract.md and ADR0003; WP15 immutable document/token-gap API; contracts/native-framing.md and editing.md EC-046/048`.
Section labels are locators within approved artifacts, not invented filenames.
Verify actual source/fixture hashes before relying on them.
Unresolved contracts are stop/refusal prerequisites, never permission to guess.

**Canonical case leads:** CMD51-046, CMD51-047, CMD51-048, CMD51-149.
Read exact titles, feature IDs and observed scopes before using a case.
Local subcases need their own preconditions/native/output/state witnesses.
A valid but semantically unrelated ID is not acceptable evidence.

## Branch strategy and ownership placement

Planning and merge placement remain `feat/wp51-parity`; eventual GitHub
integration is `main` only through the actual accepted mission workflow.
Claim with `spec-kitty agent action implement WP25 --mission wp51-parity-01M64CVY --agent codex --profile implementer-ivan`.
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

### T073: Validated mutation admission and immutable revisions

1. Read actual WP15 document.go/tests and WP23 accepted contract/evidence. Extend the same document model; do not introduce a second token/cursor model or copy wp51 native framing.

2. Implement an explicit mutation admission check for the exact prefix packets/body/attribute relationships approved by WP23. Parse success, a familiar extension, an identical prefix length or a hard-coded fixture offset is insufficient.

3. Represent each successful edit as a new immutable document revision with complete token gaps/source spans and the original untouched byte image retained for no-edit export. Cursor values from another revision must not silently address the new document.

4. Implement supported ASCII insertion and plain/code-boundary typeover exactly where WP23 establishes them. Mode toggles are session behavior; the document operations receive explicit command preconditions and return typed results.

5. Reject unsupported input identities, opaque/nested/formatter structures, unsafe pair shapes and insufficient field authority before changing document/cursor/history state. Preserve exact source bytes and recognized-versus-opaque distinctions.

6. Keep hard returns, new Bold creation, other attributes/characters and new native document construction out of this first writer unless a separately authored and independently reviewed scoped amendment supplies their complete native and command contract.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T074: Direct native candidate serializer and preservation

1. Emit original WP5.1 data directly from the supported immutable revision, retaining original prefix/header/index/packet ordering and all unrelated accepted bytes. No conversion through another word processor or Wordling wrapper/sidecar is permitted.

2. Apply only WP23-authorized field changes and checked relocation/length relationships. Explain all differences from the source. Locate packet flags by validated indexes, preserve unrelated bits and never normalize prefix padding/timestamps/resources.

3. If the supported fixed-prefix contract proves no relocation is required, assert its full preconditions rather than generalize that result to arbitrary packets. Unknown references or new semantic variants cause an explicit refusal.

4. Export after no successful mutation must remain byte-identical under FC-002. A command whose body is unchanged but whose original semantics require a metadata change is an edit only when that exact behavior has been established; do not guess dirty flags.

5. Validate generated candidates through the actual wp51.Parse API and supported semantic invariants. A parse-after-write test supplements original interoperability; it cannot replace it.

6. Expose the minimal typed candidate/revision API needed by WP26/27, with copied bytes and ownership guarantees. Keep filesystem operations and overwrite decisions outside document code.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T075: Original interoperability and adversarial writer verification

1. Run WP23 candidate-verification mode on real Go-emitted edited fixtures: original Retrieve, declared subsequent edit, text-profile print-to-disk and Save, followed by Wordling reopen. Root schedules exclusive VM access; no simultaneous guest jobs.

2. Compare intended text/code/native relationships and selected-profile raw streams against the exact original command witnesses. Retain full before/after raw files, hashes and executing sources; unexplained differences fail the corresponding supported claim.

3. Test caller/source/export isolation, invalid revision gaps, opaque data, unmatched or crossed pairs, truncated fields, arithmetic overflow, unsupported packets, source/candidate boundaries and no partial mutation on refusal.

4. Set changed binary interpretation input/token/allocation/work limits and fuzz seeds/budget before execution; include original fixtures plus labelled synthetic malformed cases. Reuse existing16MiB/token policies unless a measured reviewed change is required.

5. Run meaningful black-box public-API assertions plus repeatable60s then120s two-worker fuzz runs for the changed binary boundary, relevant race checks, Go tools and genuine regression. Do not broaden budgets repeatedly after passing absent a concern.

6. Publish supported operation/native-field matrix and actual commands/results under internal/document/evidence. Component library approval is bounded; WP27/28 must demonstrate application calls. Any unresolved required original writer result prevents approval rather than becoming a stub success.

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

Loaded, contract-admitted ASCII/Bold documents only; no new-document prefix/template, generic serializer, arbitrary opaque relocation, layout engine, additional character mapping, filesystem transaction or full formatting claim. Existing parser source remains owned by WP02 and is consumed unchanged.

If a prerequisite API/field contract is insufficient, preserve the narrow blocker
and report a scoped follow-up. Do not duplicate a codec/transaction/model,
modify another owner out of map or weaken a prerequisite to force progress.

## Validation and independent review handoff

Run catalogue and genuine configured regression checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp25-validation.xml
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

Commit only owned source/evidence. Mark T073 T074 T075
done through `spec-kitty agent tasks mark-status --mission wp51-parity-01M64CVY`
with the actual subtask IDs and `--status done`, only after their real outputs pass.
Move WP25 to for_review with explicit `--agent codex --profile implementer-ivan`.
Poll that synchronous pre-review gate until it exits; do not bypass, kill or
reissue a running gate. Return actual commit/check commands and remaining limits.
An independent reviewer records exactly one canonical approve/reject verdict.
Rejection returns to this package with concrete feedback; no self-approval,
frontmatter lifecycle edits, forced success, mission acceptance or merge.
