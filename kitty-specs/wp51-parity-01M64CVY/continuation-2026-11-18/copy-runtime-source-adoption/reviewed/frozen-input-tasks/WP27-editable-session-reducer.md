---
work_package_id: WP27
title: Revision-bound editing session and candidate Save As
dependencies:
- WP17
- WP24
- WP25
- WP26
- WP41
requirement_refs:
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
- T079
- T080
- T081
phase: Supported native editing continuation; full M1 remains open
history:
- at: '2026-10-30T23:29:50Z'
  actor: planner-priti
  action: Authored as a next-tranche draft; unexecuted, not accepted
agent_profile: implementer-ivan
authoritative_surface: internal/editor/
create_intent: []
execution_mode: code_change
owned_files:
- internal/editor/**
role: implementer
tags:
- m1-continuation
- supported-native-editing
task_type: implementation
tracker_refs: []
---

# WP27: Revision-bound editing session and candidate Save As

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

Make real document mutations, original contextual commands, dirty revisions and source-bound candidate Save As part of the existing pure session reducer.

This is one bounded milestone within complete plain WP5.1 DOS parity.
It does not close an entire FR/NFR/FC, canonical scenario or inventory group.
All38 requirements and91 groups, original resource/language/platform duties,
new-document creation and remaining editing/storage/layout families stay visible.
PDF is optional M2 only after genuine M1 acceptance.

## Context and approved prerequisites

**Dependencies:** WP17, WP24, WP25, WP26, WP41.

**Requirement references:** FR-004, FR-005, FR-006, NFR-001, NFR-002, NFR-004, C-001, C-002.

**Compatibility references:** FC-002, FC-003, FC-004, FC-009.
Runtime requirement extraction may retain only FR/NFR/C in frontmatter;
these explicit FC references remain binding regardless of that projection.

**Binding contract:** `approved WP17 actual reducer; corrected approved WP13 prompt/cancel/exit states; WP24 candidate publication API and WP25/26 exact mutation/history result contracts`.
Section labels are locators within approved artifacts, not invented filenames.
Verify actual source/fixture hashes before relying on them.
Unresolved contracts are stop/refusal prerequisites, never permission to guess.

WP41 is an explicit prerequisite for WP24's strengthened, API-compatible loaded-source candidate publication: approved source `5ad84e4` plus packaging receipt `0df934c`, independent review `0e383d5`, approval event `01M689XXRTW64NPDR38M7Z73K6`. Consume its captured source/destination observations and stable opened-directory capability rather than relying on an inherited lane tip. Capture private owned loaded-source, queued intent and result observations; acceptance must prove that whole public-wrapper reassignment or mutations through returned getter values cannot retarget accepted revisions or IO guards. Preserve the actual Close lifetime, rebound-receiver refusal, loaded-source guards, no-replace, failure/uncertainty and synchronous cross-directory Save contracts. Original loaded source guard, displayed name and last-published revision/receipt remain distinct: a successful later Save As may update the displayed name but does not rebase the original source guard. This package uses loaded-source candidate publication only; WP41's new-publication API and native constructor routing remain outside WP27.

**Canonical case leads:** CMD51-046, CMD51-047, CMD51-043, CMD51-204, CMD51-067, CMD51-069, CMD51-070, CMD51-087.
Read exact titles, feature IDs and observed scopes before using a case.
Local subcases need their own preconditions/native/output/state witnesses.
A valid but semantically unrelated ID is not acceptable evidence.

## Branch strategy and ownership placement

Planning and merge placement remain `feat/wp51-parity`; eventual GitHub
integration is `main` only through the actual accepted mission workflow.
Claim with `spec-kitty agent action implement WP27 --mission wp51-parity-01M64CVY --agent codex --profile implementer-ivan`.
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

### T079: Route actual supported editing commands and dirty revisions

1. Read and extend the real approved WP17 reducer; do not build a parallel session. Consume WP25/26 document operations and retain one document/token-gap authority for normal and Reveal views.

2. Route admitted ASCII input, original Insert mode toggle, exact supported Delete/Backspace/block operations and contextual F1 history commands. No global Escape=Cancel or F1=Cancel rule is permitted.

3. Bind cursor/selection/history to document revision and record original command provenance. Refused input or mutation keeps every affected session field intact and produces explicit unsupported/error state.

4. Track loaded source snapshot identity separately from current edited revision and last successfully published revision/name. A body-equal semantic command or supported metadata update follows its reviewed dirty-state contract.

5. Keep paste, mouse, unknown/release/capability events outside contextual command guesses. This package receives typed intents; input transport remains WP16 and physical delivery remains separately qualified.

6. No new blank-document writer, generic full menu engine, F6 attribute creation, layout/word-wrap, or unobserved editing command is introduced.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T080: Bound candidate Save As and contextual exit

1. Add typed intents/results for the actual WP24 candidate operation, carrying loaded source guard, immutable candidate bytes/hash, explicit observed destination and operation/document revision identity.

2. Keep IO outside the reducer. Preserve WP17 no-edit snapshot/no-op behavior and distinguish edited new-name publication from unsupported existing-file replacement; F10 naming follows corrected original prompt branches.

3. Only successful publication of the matching revision can mark that revision saved. A late result for an older candidate must not clear newer edits, change the current name incorrectly, or authorize exit.

4. Retain source-stale, failed, cleanup-residue and uncertain DestinationMayExist states. Cancellation after a possible side effect does not prove the destination absent; keep actual outcomes visible without rolling back another file.

5. Use exact WP13 named/unnamed and changed/unchanged save/exit branches. F1 and Escape have different observed outcomes at save and exit questions; unsupported Save-to-existing cannot become a false successful quit.

6. Test interrupted/pending Save As and requests during later edits with explicit operation/revision rules; do not infer a stronger atomic cancellation or filesystem transaction than storage guarantees.

**Required evidence:** deliver the concrete owned source/report/test outputs above; a plan, stub or passing unrelated test is not completion. Record actual commands, failures, refusals and remaining limits.

### T081: Pure reducer acceptance and immutable failure paths

1. Build Given/When/Then sequences combining original-derived mode/edit/code deletion/history/prompt states with typed successful, failed, stale and uncertain storage responses.

2. Check current token gap, selection, pane visibility, mode/history preview, filename draft/caret, dirty revision and exit decision independently; matching screen text alone is insufficient.

3. Prove no false saved/clean/exit state after replacement refusal, failed publication or uncertainty. Test late duplicated/cancelled results from another revision/operation and a publication that completes after newer typing.

4. Assert document/source/history immutability on every refused command and cancelled preview. Reuse approved document/storage APIs rather than stubbing alternate models that hide integration mismatches.

5. Run real Go checks, declared regression and targeted races if shared state is introduced; document why pure value-level state needs no filesystem fake. Publish exact supported transition and original evidence links under internal/editor/evidence.

6. Library-level session approval is not executable UI acceptance: WP28 must call the actual reducer and IO intents. Keep unobserved original branches explicitly unsupported with full M1 follow-ups.

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

No filesystem side effects in the reducer, duplicate document/history model, actual overwrite/backup/Fast Save, new-document construction, unqualified terminal support or full editor parity. Preserve older no-edit session acceptance and all original command obligations.

If a prerequisite API/field contract is insufficient, preserve the narrow blocker
and report a scoped follow-up. Do not duplicate a codec/transaction/model,
modify another owner out of map or weaken a prerequisite to force progress.

## Validation and independent review handoff

Run catalogue and genuine configured regression checks from the actual checkout:

```sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp27-validation.xml
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

Commit only owned source/evidence. Mark T079 T080 T081
done through `spec-kitty agent tasks mark-status --mission wp51-parity-01M64CVY`
with the actual subtask IDs and `--status done`, only after their real outputs pass.
Move WP27 to for_review with explicit `--agent codex --profile implementer-ivan`.
Poll that synchronous pre-review gate until it exits; do not bypass, kill or
reissue a running gate. Return actual commit/check commands and remaining limits.
An independent reviewer records exactly one canonical approve/reject verdict.
Rejection returns to this package with concrete feedback; no self-approval,
frontmatter lifecycle edits, forced success, mission acceptance or merge.

## Activity Log

- 2026-10-31T07:59:45Z – codex – Acknowledged independent cycle1 I1 at13105b90/event01M68F2YZGHR0105E6WW3NKFBH. Public selected-block Backspace mismatch reproduced red on8b0a8ed; fixed selected guard and actual DeleteBlock dispatch at5d5c767. Selected forward Delete remains unqualified/refused; original23/40 replays now use Backspace. Source/evidence only internal/editor;122 current seals verified; historical98 unchanged; no VM/UI/newbirth.
