---
work_package_id: WP24
title: Source-bound edited candidate publication without replacement
dependencies:
- WP03
- WP06
requirement_refs:
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
- T070
- T071
- T072
phase: Supported native editing continuation; full M1 remains open
history:
- at: '2026-10-30T23:29:50Z'
  actor: planner-priti
  action: Authored as a next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/storage/
create_intent: []
execution_mode: code_change
owned_files:
- internal/storage/**
role: implementer
tags:
- m1-continuation
- supported-native-editing
task_type: implementation
tracker_refs: []
---

# WP24: Source-bound edited candidate publication without replacement

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

Extend the real common storage transaction to publish independently validated edited candidate bytes under a new name while retaining the original source guard and failure guarantees.

This is one bounded milestone within complete plain WP5.1 DOS parity.
It does not close an entire FR/NFR/FC, canonical scenario or inventory group.
All38 requirements and91 groups, original resource/language/platform duties,
new-document creation and remaining editing/storage/layout families stay visible.
PDF is optional M2 only after genuine M1 acceptance.

## Context and approved prerequisites

**Dependencies:** WP03, WP06.

**Requirement references:** FR-006, NFR-001, NFR-002, NFR-004, C-001, C-002.

**Compatibility references:** FC-002, FC-004, FC-007, FC-009.
Runtime requirement extraction may retain only FR/NFR/C in frontmatter;
these explicit FC references remain binding regardless of that projection.

**Binding contract:** `approved WP03 internal/storage/README.md source identity, no-replace link and uncertain outcomes; contracts/files-platform.md storage foundation and FP02–FP05/FP21`.
Section labels are locators within approved artifacts, not invented filenames.
Verify actual source/fixture hashes before relying on them.
Unresolved contracts are stop/refusal prerequisites, never permission to guess.

**Canonical case leads:** CMD51-067, CMD51-069, CMD51-070, CMD51-149.
Read exact titles, feature IDs and observed scopes before using a case.
Local subcases need their own preconditions/native/output/state witnesses.
A valid but semantically unrelated ID is not acceptable evidence.

## Branch strategy and ownership placement

Planning and merge placement remain `feat/wp51-parity`; eventual GitHub
integration is `main` only through the actual accepted mission workflow.
Claim with `spec-kitty agent action implement WP24 --mission wp51-parity-01M64CVY --agent codex --profile implementer-ivan`.
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

### T070: Separate source guard from candidate identity

1. Read the actual approved storage_linux.go and tests at WP03 commit7deeaf6, including Directory/Document/Destination, checkSource, publish and every candidate verification. Preserve its source-directory descriptor and loaded identity as the source guard.

2. Specify the minimal typed candidate-publication API in the owned storage README. Keep candidate bytes/length/SHA distinct from loaded source identity, destination observation and caller operation/document revision; native framing validation does not certify semantic edit safety.

3. Consume the existing immutable wp51 native image/validated exported bytes. Storage must not import internal/document, internal/editor or Bubble Tea, duplicate a codec, or claim that any outer-framed candidate is semantically safe.

4. Do not manufacture a storage.Document with a changed image/hash to get through Save. That would conflate source freshness and candidate verification. Keep source guard and payload fingerprint distinct through the real common transaction.

5. Retain the existing no-edit Save behavior and explicit same-file no-op. Edited-candidate publication supports an observed absent destination only; an existing destination, including the original inode, remains UnsupportedReplacement.

6. Keep the dependency graph honest: WP24 depends only on WP03/WP06, not WP23/25 or session code. This low-level byte-publication extension is independently testable and cannot authorize semantic edits on its own.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T071: Refactor and reuse the existing publication transaction

1. Refactor the existing publisher so no-edit Save and candidate publication share one candidate-create/write/close/verify/link/cleanup implementation. Do not add a parallel transaction with subtly different safety behavior.

2. Change payload verification to compare actual candidate length/hash/bytes against the immutable candidate fingerprint; retain checkSource against the original loaded snapshot identity/hash before publication. Audit all pre-link, post-link and post-cleanup comparisons.

3. Retain pinned rooted directory descriptors, no-follow leaf reads, candidate inode pin, no-replace hard-link publication, destination observation checks and the declared local-filesystem policy.

4. Retain exact typed failure, cleanup residue and DestinationMayExist outcomes. After an ambiguous side effect, never report complete success or unlink a destination that could belong to another writer.

5. Reject nil/unbound/cross-operation/stale inputs, invalid decisions, unsupported paths and candidate size/framing errors before destination mutation. Copy/ownership rules must prevent caller mutation during an in-flight save.

6. Keep source and existing destination files unopened for writing, untruncated, unrenamed and unlinked. Do not add a caller-asserted exclusivity bypass, hostile-directory/CAS promise, fsync/durability claim, backup or Fast Save policy.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T072: Real failure and candidate/source distinction tests

1. Use existing external API tests and real temporary directories to publish a different lawful candidate from a loaded original. Assert candidate bytes at the new name and byte-identical unchanged original source; same-file no-edit behavior stays unchanged.

2. A test must fail if payload verification uses source SHA instead of candidate SHA, and another must fail if source revalidation uses candidate identity instead of the loaded source. Do not test solely identical source/candidate payloads.

3. Exercise short/write/close failures, stale source replacement/mutation, destination races, candidate substitution, cleanup residue, parent-directory rename and failure after a possible link side effect through the common transaction.

4. Assert uncertainty/no-false-success and preservation at each boundary. Include caller-buffer mutation and concurrent Close/publication races where the API permits concurrency; record unsupported concurrency rather than imply a stronger guarantee.

5. Run Go build/test/vet/gofmt, targeted race and declared project gate from the real lane. Keep evidence under internal/storage/evidence and document live consumer requirements for WP27/28.

6. Publish the actual API and bounded supported-state matrix for downstream implementation. No original F10 or replacement parity follows from this independently approved IO component.

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

No semantic writer, document/editor dependency, actual replacement, backup/Fast Save, new path mapping, generic unbound byte write or duplicate publication transaction. Do not change source identity to make edited candidates appear to be loaded snapshots.

If a prerequisite API/field contract is insufficient, preserve the narrow blocker
and report a scoped follow-up. Do not duplicate a codec/transaction/model,
modify another owner out of map or weaken a prerequisite to force progress.

## Validation and independent review handoff

Run catalogue and genuine configured regression checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp24-validation.xml
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

Commit only owned source/evidence. Mark T070 T071 T072
done through `spec-kitty agent tasks mark-status --mission wp51-parity-01M64CVY`
with the actual subtask IDs and `--status done`, only after their real outputs pass.
Move WP24 to for_review with explicit `--agent codex --profile implementer-ivan`.
Poll that synchronous pre-review gate until it exits; do not bypass, kill or
reissue a running gate. Return actual commit/check commands and remaining limits.
An independent reviewer records exactly one canonical approve/reject verdict.
Rejection returns to this package with concrete feedback; no self-approval,
frontmatter lifecycle edits, forced success, mission acceptance or merge.
