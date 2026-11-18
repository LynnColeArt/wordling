---
work_package_id: WP104
title: Source-bound original admission and retained foreground ownership
dependencies:
- WP63
- WP64
- WP68
- WP70
- WP74
requirement_refs:
- FR-001
- NFR-002
- NFR-003
- NFR-004
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T338
- T339
- T340
phase: Original-route source component and harmless controls only
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/document/evidence/reference_controller/
create_intent:
- internal/document/evidence/reference_controller/original.py
- internal/document/evidence/reference_controller/original_release.py
- internal/document/evidence/reference_controller/original-pyproject.toml
- internal/document/evidence/reference_controller/tests/original_deployment.py
- internal/document/evidence/reference_controller/tests/test_original_admission.py
- internal/document/evidence/reference_controller/tests/test_original_foreground.py
- docs/research/continuation/original-route/admission/
- internal/document/evidence/reference_controller/tests/original_control_fixture.c
- internal/document/evidence/reference_controller/tests/original_control_master.txt
- internal/document/evidence/reference_controller/tests/original_control_roster.json
- internal/document/evidence/reference_controller/tests/original_control_admin.py
- internal/document/evidence/reference_controller/tests/test_original_root_callgraph.py
execution_mode: code_change
owned_files:
- internal/document/evidence/reference_controller/issuance.py
- internal/document/evidence/reference_controller/bootstrap.py
- internal/document/evidence/reference_controller/original.py
- internal/document/evidence/reference_controller/original_release.py
- internal/document/evidence/reference_controller/original-pyproject.toml
- internal/document/evidence/reference_controller/tests/original_deployment.py
- internal/document/evidence/reference_controller/tests/test_original_admission.py
- internal/document/evidence/reference_controller/tests/test_original_foreground.py
- docs/research/continuation/original-route/admission/**
- internal/document/evidence/reference_controller/tests/original_control_fixture.c
- internal/document/evidence/reference_controller/tests/original_control_master.txt
- internal/document/evidence/reference_controller/tests/original_control_roster.json
- internal/document/evidence/reference_controller/tests/original_control_admin.py
- internal/document/evidence/reference_controller/tests/test_original_root_callgraph.py
role: implementer
tags:
- m1-continuation
- draft-unreserved
- original-route-source
task_type: implementation
tracker_refs: []
---

# Work Package Prompt: WP104 — original admission and foreground ownership

## Load Agent Profile

Resolve implementer-ivan/action implement at the actual claim. This is an unregistered proposal: no implementation, grant, private resource probe or VM action follows from this file. Read all independent task/design feedback first. Record later execution through normal event-log commands; do not fabricate activity or approval entries.

## Objectives & Success Criteria

Deliver the bounded source component from contract §§1–3: a genuine disjoint original issuer/entry, ordinary sealed deployment, one immutable leaf and retained physical/foreground ownership over the existing P supervisor. Public harmless OS controls exercise the actual implementation, and existing TEST public behavior remains working. RootTicketIssuer with missing/foreign/raw authorization still refuses before path effects.

Success is independently reviewed source/test delivery, not original behavior, readiness, normal-DOS stop, native export, New-buffer qualification or M1 acceptance. WP105 supplies those route operations. Actual original release remains closed until WP105 and the exact later recipe/candidate are reviewed and ROOT issues a fresh finite decision.

## Context & Constraints

Read `.kittify/charter/charter.md`, `docs/compatibility.md`, actual M1 spec/plan, approved WP63/64/68/70 review/source bindings, COMMON-E-CONTRACT and the adopted `original-route-v1.md`. Consume actual approved source/class roots, not archived copies. The selected trust entry is DIRECT same-interpreter ROOT invocation of original_release.coordinate_one, under the explicit trusted-host/no-sandbox model in contract §1. Source review checks this concrete call graph and acyclic C/K/P/R/D/B then dynamic J binding; it does not leave role selection to worker data or flags. Read the normative control-profile-v1.md and revision-r1-r2.md together with the route contract.

Preserve TEST `ReferenceController.open_leaf` exact-type protection and existing harmless CLI/TEST deployment. Do not amend controller.py, cli.py, account.py, ownership.py, records.py, P's five source files, guest.py, qmp.py or historical runners/evidence. Existing issuance/bootstrap changes are narrow additive original-kind branches; do not make common validators accept arbitrary providers/objects. The original wheel has a separate exact source/metadata staging map; no editable/PYTHONPATH/global patch or proprietary package data.

Only harmless authored files/processes may be used for implementation controls. A positive ROOT-control test requires an actual ROOT-issued source/plan/control-case/repetition release for its harmless candidate. No test may synthesize RootDecision/OriginalGrant or convert TestGrant into one. Ordinary negative tests can prove no-release refusal; actual original-positive admission stays unrun until later authorization.

## Branch Strategy

Planning base and merge target: `feat/wp51-parity`. Reuse a suitable checkout; if isolation is required use the approved worktree tool under `~/work-trees` or `/tmp`, clean it up and leave all work committed. No changes to active WP100 files. WP105 follows sequentially because it extends original.py/bootstrap/original deployment sources; no parallel overlap.

## Subtasks & Detailed Guidance

### T338 — freeze contract/deployment/release and commit RED admission tests

- Pin the exact baseline and all owned/unchanged E/P/peer/QMP input sources. Record the distinct TEST versus original source/class/namespace sets and the trusted-host assumptions; do not claim a sandbox.
- Implement the selected coordinate_one call graph and sole private mint caller from contract §1. Test the actual source call graph: ordinary leaf/TEST/child entry points cannot invoke that mint or select ROOT role; import has no effects. Freeze immutable C/K/P/R/D/B before a later deliberate ROOT action creates dynamic J outside every seal. Define exact immutable OriginalLeafPlan/OriginalSourcePolicy and registered live RootDecision/OriginalGrant/OriginalLeaf, with the specified rejection order. Bind source/plan/profile/case/context/repetition/candidate/grant ID/limits; no strings or reconstructed results mint objects.
- Commit a failing acceptance test through the actual installed entry before source implementation. It must assert no private path/guard/store/launch effect for absent or foreign authority and unchanged TEST admission behavior. Do not use a fake root issuer to arrange a positive.
- Prepare a closed ordinary original wheel map using original-pyproject.toml and original_deployment.py. Validate interpreter/stdlib/package/import/class origins and no extra/customization/cache source before operational imports; import itself cannot inspect private assets.
- Files: issuance.py, bootstrap.py, new metadata/release module and new admission/deployment tests. No parallel work.

### T339 — consume one real release and retain physical/foreground ownership

- Implement original issuance with the existing durable store/book/parent machinery and disjoint source-selected ORIGINAL versus CONTROL kind/root/generation, stable spent-ID key and exact persistence order. New original_control_fixture.c/master.txt/roster.json/admin.py supply the fixed authored C mutate/serve/derive tool, literal raw data, closed finite rows and separately reviewed direct ROOT administration of pre-existing disposable CONTROL guard/store/resources; no fake provider, old TEST fixture modification or selector patch. Keep no-argument `RootTicketIssuer.issue()` refusing. No leaf auto-provisions a store or upgrades a historical grant.
- Publish a grant only after a durable nonterminal safety reservation. Any unresolved reservation blocks other grant IDs; process/lock disappearance cannot clear it. No new-ID, generation, delete/reparse or replay recovery. Persist truthful partials and spent credit.
- New original.py provides an exact-type retained context and one permitted prepare/launch path. The SAME guard acquisition routine retains the source-selected pre-existing FD/parent/lock: actual shared session1.lock for ORIGINAL; the fixed preprovisioned disposable CONTROL session1.lock for CONTROL. TEST .physical is neither. Domain/profile/grant/resources remain bound; missing/unproved administration blocks. No invalid leaf auto-provisions anything.
- Use only P capture/prepare/tool/mutate successors/launch and retained ProcessLease; store handles privately. One Session/worker/foreground: ORIGINAL has fixed reviewed offline QEMU arguments without daemonization/host shares/network/serial/parallel/arbitrary media; CONTROL has only the captured authored C tool and raw master from the closed profile. Both use the same P machinery and no PID-file authority. Recheck source, identity, all earlier clocks and counters after waits/IO. No VM in this WP's controls.
- Freeze finite declared tool/resource/import/argv/env/cwd requirements. All phases and cleanup fit immutable limits before effects; no enlargement of intrinsic caps or free work. Real image/tool fitness remains UNKNOWN until a later original release.
- Expose only OWNED_UNREADY diagnostics and truthful close/containment; no READY/StoppedRun/export claims. Original readiness is WP105. No parallel work.

### T340 — public controls, source custody and independent component review

- Freeze <=28 public OS controls and <=64 total logical cases including schema negatives, with actual per-case/total budgets before running; count each parameterized negative as a real case. If this cannot fit <=30s+2s/case and <=300s, obtain a finite source-reviewed extension before effects.
- After independent CONTROL source/roster/deployment review, actual ROOT CONTROL invocations authorize positive OS rows through the same canonical issuer/hold/guard/account/P chain; ordinary CI/leaf tests cannot mint or deserialize decisions. Freeze the exact closed variants in control-profile-v1.md, including cross-domain/profile rejection. WP104 positive ownership deliberately ends in truthful unresolved quarantine; it does not claim stop/export/discharge.
- Controls cover: unchanged installed TEST positive; genuine ROOT-authorized harmless admission/creation-bound foreground; missing/forged/foreign/TestGrant/wrong class; wrong source/plan/case/context/repetition/candidate; expired release; spent/replayed/lost marker/handoff; same-ID and different-ID/physical contention; dirty/existing run root; wrong master/tool declarations; shared guard/ancestor/inode retarget; post-wait deadline/source/identity loss; unexpected child/daemonized command; no-refund exhaustion; coordinator death with durable unresolved safety reservation; wrong cleanup FD and preservation of foreign bytes. Isolate sticky-failed cases; never test refusal then claim success in that same context.
- Use source-valid semantic mutants for type boundary, durable-before-grant order, stable spent key, no-create-on-invalid, retained lock/identity, no-daemonize/one-child, source recheck and sticky reservation. Construction/import failure is not a kill; a real survivor blocks approval.
- Run targeted new tests plus relevant existing installed TEST issuer/ownership/controller and approved P regressions/configured Python compile/discovery/lint. Freeze commands, environment, source sets, receipts, raw failures and evidence <=1024 files/16MiB. No broad original/Go/fuzz campaign or history overwrite.
- Commit only owned files. Request ROOT quiet point and normal for_review; a different reviewer verifies actual source/tests/closure. Do not self-approve, merge/push, issue original grants or touch another WP.

## Test Strategy

RED then GREEN through the new installed closed entry using the normative control-profile-v1.md; real harmless OS controls for issuance/ownership/process claims, typed negatives for schema only. TEST route remains TEST. No image/tool inventory, network acquisition or original launch is part of validation. Review the sealed ordinary deployment and actual source/class origins, not just pytest import success. Independent reviewer supplies exact commands for the final frozen test roster; no guessed broad runner overwrites prior evidence.

## Risks & Mitigations

The original trust entry and physical safety hold are new authority, not boilerplate. If this needs generic account/ownership/P changes, another supervisor, a remote authorization service, or larger source/evidence/clock caps, stop and split a prerequisite package before code. No such expansion is authorized here. The parent-selected direct ROOT and closed CONTROL architecture is concrete; an unexpected source/API expansion requires an explicit revised package and independent review, never an ad-hoc bypass.

## Review Guidance

Verify every grant was genuine and exact, every private side effect followed consumption, durable loss cannot grant/regrant, TEST exact types/CLI stay protected, and only existing P public handles create/retain the foreground. Positive harmless receipts do not establish original/reference qualification. All 49 M1 families and later reference obligations remain open.

## Activity Log

Proposal only; no claim or implementation history exists. Append real chronological activity through canonical workflow only after adoption.


## Approved registration serialization amendment

Normal owned finalization found the historical WP74 internal/document/** routing overlap. Independent registration-amendment review approves adding WP74 as an already approved source/ownership predecessor, retaining WP63/64/68/70. WP105 follows it transitively through WP104. This changes scheduling only; reviewed scope, exact owned files and all authority/safety controls are unchanged. See continuation-2026-11-18/original-route-adoption/review-evidence/original-route-registration-amendment-review.md.
