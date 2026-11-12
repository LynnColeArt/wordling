---
work_package_id: WP41
title: Prepared-request ownership repair and source-less native publication
dependencies:
- WP02
- WP24
- WP34
requirement_refs:
- FR-002
- FR-006
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
- T121
- T122
- T123
phase: Native lifecycle prerequisite tranche; full M1 remains open
history:
- at: '2026-10-31T05:07:17.694252+00:00'
  actor: planner-priti
  action: Temporary task draft after independent architecture cycle2; not finalized/executed/approved
agent_profile: implementer-ivan
authoritative_surface: internal/storage/
create_intent: []
execution_mode: code_change
owned_files:
- internal/storage/**
role: implementer
tags:
- m1-continuation
- native-lifecycle-prerequisite
task_type: implementation
tracker_refs: []
---

# WP41: Prepared-request ownership repair and source-less native publication

## Governance, scope and evidence boundary

Resolve the frontmatter profile with `spec-kitty agent profile show`, load action-scoped charter context and apply its initialization/boundaries. Read AGENTS, mission spec/plan/data-model/continuation, docs/compatibility.md, docs/roadmap.md, actual approved dependencies and independent review findings. Production remains Linux, Go1.26.4, Bubble Tea v2.1.1 and original native/companion formats; Apache-2.0 covers project contributions. Complete plain DOS WP5.1 U.S. Help03/09/92 M1 remains: all38 obligations/91 groups/36 workbook lessons and discovered nested leaves. These are bounded component/original-research milestones, not full command/group/FR acceptance. M2/PDF waits for genuine M1 acceptance. No proprietary program/manual/resource redistribution or decompilation, modern persistent format/sidecar or silent character conversion.

Read design-ready ADR proposal `docs/decisions/0003-native-document-lifecycle.md` and its `docs/research/continuation/native-lifecycle-design/` review/source seals after root promotes those exact materials. Promotion is a planning prerequisite; no package may fabricate the missing ADR, edit it or treat the stale first architecture review as current approval. Cycle2 design readiness is not implementation/original-behavior approval. Verify exact frozen versions and report mismatch before coding.

Use only the canonical runtime-returned workspace and declared owned surfaces. Source is in approved dependency lanes; primary's absent Go files do not prove product source absence. These are honest code_change packages, including Python research. No codebasewide exemption, renamed fake ownership, lifecycle frontmatter edits, out-of-owner repair, unrelated source normalization or approved-contract rewriting. Requirement refs are partial contributions; explicit FC duties remain binding even if runtime extraction projects only FR/NFR/C. No final accept/merge/M2, self-approval or another WP's lifecycle change.

## Objective and binding authority

Implement clarified proposal A only: repair immutable ownership of accepted prepared source/destination/opened-directory observations, and add distinct source-less framing-validated absent-target publication through the same existing storage engine. Dependencies approved02/24/34; storage70e02f7 is the inspected baseline, including34 private immutable Macro.Image wrapper. Inspect actual approved final source before changing it. No constructor/document/editor/TUI dependency or ownership is added. E/F/G are future consuming constructor/session/executable packages; the storage capability is not a second CLI or semantic-genesis proof.

Canonical leads from approved13: CMD51-066 Name a new document with F10 (WP51-020, REF565/PDF582),149 Preserve an untouched native file byte for byte,150 Reject an unsafe opaque-structure edit before replacement,151 Preserve unrelated native data after a supported edit,152 Retain original after a failed save (WP51-020, REF565–566/PDF582–583). These are full-scenario leads; this component does not implement the command or qualify constructor bytes. FC001–004/007/009 and files-platform FP02–FP09 remain binding; overwrite/backup/recovery remain separate M1 work.

## Confirmed prerequisite and bounded repair scope

Independent sealed public-API investigation on unchanged70e02f7 reproduced three P2 failures in one ownership class: source-wrapper replacement bypasses the accepted original source guard; destination-wrapper replacement changes the prepared output name; Directory-wrapper replacement redirects physical output into another pinned root with a pre-acquisition hardlink control. The ordinary suite passes and the independent race overlay fails all three assertions without a data race. Read the exact report/findings/seals/overlays/raw logs promoted under native-lifecycle-design/alias-investigation/; they are baseline failure evidence, not a source fix. This explicit scoped repair replaces the earlier pending-investigation note. Do not reinterpret sequential between-call legal whole-wrapper assignment as concurrent mutation during a synchronous call.

The appended architecture capture clarification is pending independent design/task analysis before promotion. Preserve both old architecture review cycles as historical; they did not assess this later issue. Root's temporary promotion receipt binds exact prior drafts and the independent alias evidence. No approved history is revoked or rewritten.

## T121: Capture prepared source destination and opened capability

First reproduce all three sealed independent public-API failures against exact unmodified70e02f7 using an overlay or equivalent external tests; record actual red assertions, command/build/source hashes and race result without editing baseline source/logs. Implement the bounded capture repair in existing Publication/acquisition wrappers: accepted source name/full identity/native image plus stable acquired directory capability; exact destination name/existence/identity plus stable capability; and exact receiver opened capability. Store immutable private accepted observation state, never caller-reassignable *Document/*Destination/*Directory authority. Shallow wrapper copies that still follow a public *Directory are insufficient. Preserve public signatures. Source/target wrapper reassignment after Prepare cannot retarget accepted request; revalidate the captured original at every old guard boundary.

Use stable private opened-resource state (or equivalently proven capture). A legitimate Directory copy aliases that actual resource lifetime. Publish/PublishNew explicitly refuse nil/zero/closed or a rebound receiver capability before filesystem IO/candidate creation; matching public pointer or path/FileID is insufficient authority. A copied same-capability open receiver remains valid. Close on an original/copy/rebound wrapper closes the capability it actually designates; once closed no prepared request or alias may resurrect it, use another root, reopen/duplicate handles secretly or lose descriptor ownership. Preserve real Close errors/semantics without adding a promised idempotent-success API or reference-count subsystem. Capture private request state once per synchronous operation; concurrent caller mutation during that call remains outside guarantee.

Add `Directory.PrepareNewPublication(target *Destination,data []byte,id PublicationID) (*NewPublication,error)` and `Directory.PublishNew(p *NewPublication,expectedID PublicationID) (Outcome,error)` per ADR0003. NewPublication fields stay private: exact Directory/Destination observation, owned wp51.Image, operation/revision, payload size/hash. Copied ID/Size/SHA inspections parallel sourced Publication. Validate nonnil/zero/cross-directory handles, absent target, nonzero IDs, current destination, bounded data and actual wp51.Parse native-document framing/type (WPM refuses). Caller input mutation during call is forbidden; after return every candidate and captured destination observation are independently owned. NewPublication must capture immutable private observation state rather than retain a caller-reassignable *Destination wrapper as its authority. Subsequent whole-value assignment of the original observed wrapper must not retarget the prepared request. No exported mutable payload or arbitrary caller-built valid handle.

Do not overload old PreparePublication/Publish with nil-source semantics. The new storage type proves framing/transaction admission, not constructor provenance or semantic edit safety; future editor must select it only for a genuinely never-sourced New buffer. No dummy storage.Document, wrapper hack, relaxed parser or native template. OriginalExport/Origin/NewConfig belong to later document packages and are not implemented here.

## T122: Add source-less requests through the repaired shared transaction

Factor current publish internals into a single private transaction requiring an explicit nonzero guard kind: real loaded source or explicit source-less. Unknown/zero guards refuse. Loaded branches preserve source revalidation of the captured accepted original at all old prepare/publish/pre-link points; source-less guard is constructible only through the new typed request. Never change checks into a generic `if source != nil`. Keep old Save cross-directory publication and same-source no-op behavior exactly; PreparePublication retains its narrower same-Directory constraint. Preserve34's Macro.Image immutability and all sourced request guards.

Reuse existing candidate exclusive create/pin, rooted flat-path/no-follow protection, bounded write/close, full candidate inode/hash/bytes verification, destination rechecks, no-replace Link, post-link checks, owned cleanup, final verification and pin-close failure handling. Outcome/Failure categories and conservative DestinationMayExist/Candidate meaning stay intact. Failed/uncertain/cleanup outcomes never report complete success, unlink a destination as rollback or silently retry. No actual existing-file replacement, backup/recovery, durability/fsync promise, global cancellation or stat-then-rename CAS. No public nullable guard or second FS engine.

## T123: Red-to-green alias faults and real consumer regressions

Use real temporary pinned directories and existing private filesystem fault seam, asserting public API effects. Promote equivalent independent red cases into permanent meaningful public-API tests and demonstrate green on repaired source. For R1 alter retained original then assign source wrapper zero/other same-root/cross-root; require stale/refusal before any output and prove changing the original still matters. For R2 replace target with zero/other absent/existing/cross-root observation; retain prepared first or refuse safely, never publish substituted second. For R3 build the hardlink before fresh Read, prepare on original root, reassign receiver to other/zero root, and assert explicit refusal before IO with neither redirected output nor candidates. Verify actual paths/bytes/length/identities, not only Outcome metadata. Cover NewPublication target/root substitution equally. Test legitimate same-capability Directory copies, root rename, Close via copied/original/rebound wrappers, already-closed capabilities, wrong capabilities and absence of leaked/stale descriptors. Keep original-source mutation independent from wrapper substitution. Consumer regression must exercise actual inherited editor/TUI external APIs against this repaired storage (test-only composition/overlay is permissible without new runtime code dependencies or out-of-owner source changes); report exact compatible source/build, old name/source guards and IO faults. No new product NewPublication routing is claimed until F/G. If a downstream consumer is unavailable or incompatible, report the precise blocker for root rather than add a reverse lane dependency or fake consumer.  Test caller-buffer independence and post-Prepare whole-value assignment of original destination wrappers (including same-directory different absent names and foreign observations) without retargeting the new prepared request. Bind the sealed R1/R2/R3 ownership repair and exact original/green results without broadening into a general API audit. Test malformed/oversize/WPM/zero/cross-directory/ID mismatches, target-existing/refused and late destination creation, short write, writer/pin close failures, failed candidate read/verification, candidate substitution, Link/post-link/final verification and cleanup residue. Assert exact payload/identity and original/destination preservation, explicit uncertainty and untouched substituted leaves. Exercise source mutation at every existing sourced validation boundary and retain old Save cross-directory/no-op and Macro wrapper regressions. No negative expected pass merely because parser accepts self-produced bytes. Record actual resource/allocation bounds and race/failure coverage in internal/storage/evidence; no guest is required for this component contract. Keep loaded source guard separate from any future displayed SaveAs name/publication receipt; later sourced SaveAs must not rebind it.


## Validation and independent review

Run actual configured regression from the composed checkout: `python3 scripts/render-inventory.py --check`, `python3 scripts/render-scenarios.py --check`, and `python3 scripts/review_checks.py --junitxml /tmp/wp41-validation.xml` (use this actual WP number). Discover inherited Go packages: gofmt changed Go and run `go build ./...`, `go test ./...`, `go vet ./...` where present; only report no-Go skips when the actual assigned checkout has none. Changed Python compiles and its real public CLI, meaningful malformed/semantic negatives and applicable offline tests pass with JUnit. Any new binary interpretation declares byte/allocation/traversal bounds, malformed/boundary seeds and reproducible measured fuzz budget before acceptance. Keep raw input/native/print/terminal bytes, lengths and SHA; check committed Git blobs and raw attributes under owned evidence, not just working-tree hashes. Passing framing/process exit/checksum alone is not semantic or original compatibility proof.

Commit only owned source/evidence after checks. Request root quietpoint before T121 T122 T123 done/for_review mutations with actual `--mission wp51-parity-01M64CVY --agent codex --profile` matching frontmatter. Poll the entire synchronous pre-review gate to exit, never bypass/kill/reissue a running gate. Independent reviewer records one canonical approve/reject verdict on exact source; failures return with concrete findings. Report unsupported/unobserved/failed/component-only separately. No package acceptance closes its parent or full M1.
