---
work_package_id: WP61
title: Shared generic startup family streaming resources and managed foreground lifetime
dependencies:
- WP58
- WP38
requirement_refs:
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T181
- T182
- T183
phase: Offline generic component only; no original resources or guest permission
history: []
agent_profile: implementer-ivan
authoritative_surface: scripts/reference/startup_family/
create_intent:
- scripts/reference/startup_family/
- scripts/reference/startup_family/__init__.py
- scripts/reference/startup_family/engine.py
- scripts/reference/startup_family/artifacts.py
- scripts/reference/startup_family/lifetime.py
- tests/reference/startup-prerequisite/
- docs/research/continuation/macro-session/startup-prerequisite/
execution_mode: code_change
owned_files:
- scripts/reference/startup_*
- scripts/reference/startup_family/**
- tests/reference/startup-prerequisite/**
- docs/research/continuation/macro-session/startup-prerequisite/**
role: implementer
tags:
- m1-continuation
- generic-startup-family
- offline-test-only
- temporary-unreserved-proposal
task_type: implementation
tracker_refs: []
---

# TEMP WP61 — shared generic startup family (T181–T183 NOT reserved)

This is a TEMP task proposal ONLY. It is not canonical, code, a ROOT grant, source/prelaunch readiness, actual original tool fit or M1 acceptance. Root external HOLD: independent NEW TASK review, fresh protected-baseline verification, canonical finalize/fullsnapshot/refresh, separate CURRENT61 analysis and normal runtime claim remain mandatory. Do not start code from this proposal. Actual60 is IN_PROGRESS in H: its UNAPPROVED implementation/semantics are NOT inputs or prerequisites. Existing full38 requirements/91 groups/36 lessons/nested SC001–005 remain OPEN; M2/PDF gated.

## Exact approved authority and owned family

ApprovedP58 source676de09bce7672a8fd965f35c23acc5d5746a6e2/provider603cc95307fe681d51637c08351efbbc101b98e8b3f2bc9325f8fe635ee590c9/event01M6AMH3BFS1G8Z41M4MZBV9TS provides only its bounded generic TEST contract. Exact designR2 seal8e494203130aee36399f7ebc6db8c0c435b3c1019be99548c6a1745562a5ac0f plus NEW independent DESIGN-only review sealeba2bd85cc1a93cdb593220f7842e94a3a203bda7dc9eab3f80744b433a3beda are immutable inputs, archived ONCE under this task's provenance/ with complete path/size/SHA mapping. Read ALL API.md, STATE-MACHINE.md, LIMITS.md, LOADING-SCOPE.md and ACCEPTANCE.md in provenance/design-r2 (inert .txt suffixes), report and independent review before implementation. These exact contracts are mandatory, not options to redesign. Old R1 stale JSON/actual exit1 and BLOCKED review are preserved INSIDE R2 history, not recopied/laundered. New module/API claims below are proposed, NOT already present in approved58.

Hard prerequisites ONLY58 and38.58 provides actual code/API;38 provides legacy-source nonmutation authority inherited through58. No E55/57, H60, QMP/original resource/recipe/profile/native semantics or moving unreviewed source dependency. At claim inspect actual approved dependency ancestors, full old511 source metadata and actual Git/working bytes. Read approved public source from immutable Git where not on planning ancestry; normal runtime claim supplies P source. Do not manually merge/copy/overlay code into primary to fix path resolution. Actual installed Git workflow says primary is planning-only; accepted lane→mission→target routing is CLI-owned.

Own ONLY scripts/reference/startup_* (actual existing startup_transport.py plus genuine NEW startup_family package), explicit scripts/reference/startup_family/**, tests/reference/startup-prerequisite/** and docs/research/continuation/macro-session/startup-prerequisite/**. Authoritative public surface is the genuine new package directory scripts/reference/startup_family/. Existing facade is AMENDED, never create_intent. Only new package/four module files/new test/evidence directories are create_intent. Pattern and package entry serve actual shared responsibilities/import authority, not an exotic spelling/single-file wildcard/dummy marker/owner reslice. No guest.py/qmp.py/macro_session.py/old caller changes. No old58 raw/test/result rewriting; keep source comparisons and baseline source metadata. If actual scope/import/source contract cannot be achieved, report precise prerequisite; do not weaken contracts or patch host tools/private globals.

P61 must NEVER stat/read/execute actual original/QEMU/private tool/program/master/boot/firmware/font/SET/PRS/manual/failed-HD/reference guard/private ledger or acquire a guest. TEST processes/files/Unix sockets are authored disposable fixtures ONLY. Published actual QEMU/boot/firmware/mtools sizes/host resource envelopes remain UNKNOWN. Public profile's64MiB declaration and exact tool hashes are metadata, not actual access or permission. A generic lease/streamed digest cannot grant native validity, normalDOS/normal QMP quit, source-prelaunch READY or actual E controller capability. Later E remains separately source/prelaunch reviewed and needs an exact NEW ROOT grant; no later task/ID is authored here.

## T181 — actual shared engine, streaming/mutable artifacts and exact import compatibility

Implement the reviewed conventional package with FOUR genuinely used modules:

- engine.py: ONE shared identity/pidfd/stream/selector/journal/process kernel and Failure/Identity/Result/Limits class authority. Stdlib only, imports NO artifacts/lifetime/facade/E. Old synchronous Attempt AND new supervisor call this actual engine; no copied second supervisor/controller.
- artifacts.py: SINGLE exact old ArtifactSpec/CommandSpec plus new SourceRequest/StreamPolicy/SourceLease/WorkingLease/ExecutableLease/MutationSpec/LaunchSpec resource custody. Uses engine only. Both old facade and new lifetime are real callers.
- lifetime.py: managed Session/ProcessLease/CheckedChannel and immutable new observations; imports engine+artifacts only.
- __init__.py: real exports and old Attempt composition adapter, not marker. Amended startup_transport facade reexports the single authorities, old public CLI and new managed-fixture CLI reach them.

Preserve ALL old public fields/signatures/defaults/small semantics and existing Result API. Old ArtifactSpec.capture/verify still hard-refuses >8MiB; old copied aggregate16MiB,15s synchronous commands/readiness bounded by its command, output/process/JSON/journal/runtime limits and8-case CLI remain unchanged. Preserve old daemonUNKNOWN and I1 continuous aggregate limits/absolute clocks + I2 current kernel checks after wait/IO/final acceptance. No class-name-only alias conversion or source-hash-only substitute for kernel identity.

Implement exact LOADING-SCOPE contract: facade derives checked sibling package from its own __file__, not cwd/PYTHONPATH/sys.path. Standard importlib package initialization under ONE new canonical package name wordling_reference_startup_v1, correct synchronization, explicit origins/restricted relative source paths. Validate saved source-directory dev/inode, every loaded module origin/version/full source digest before cache reuse; cached wrong root/changed package refuses before effects. Register ONLY own new package using standard import machinery; no foreign replacement, sys.path/meta_path/old helper/private-global patch or silent reload. Same-root standalone and arbitrary spec_from_file_location aliases reexport identical authoritative classes/exceptions; wrong-worktree/same-byte different-root cannot retarget leases. Initial partial-load cleanup removes only entries this import created. Actual tests must prove it; file-spec loading alone is insufficient.

Implement exact API/STATE contracts: source requests have known expected size/hash, absolute no-symlink regular nlink1 files; tools executable/no setuid/setgid. Streaming seal returns digest/identity, NEVER large payload bytes. SourceLease and freshly owned WorkingLease remain distinct; copy is no-clobber atomic with source/FD/root/version guards. Actual partial writes/publication/source/persistence faults preserve foreign/prior bytes and truthful may-exist facts, no rollback. Working epochs READY→MUTATING→READY(next) only on bounded successful same-inode/source-safe outcome; ANY failure UNUSABLE. BUSY attached resources cannot copy/digest/mutate during active child; stopped generic zero-exit can become DIRTY_STOPPED then checked opaque snapshot, never native qualification. Public dict/PID/hash/zero/closed/stale/forked/wrong-session wrappers cannot construct/retarget new opaque leases. Any failed operation raises sticky StartupFailure; diagnostics/containment/close only afterward, no NEXT/reset/requalify.

Freeze and enforce NEW StreamPolicy.test_v1 separately from old defaults:64MiB/file,256MiB declared source aggregate,128MiB copied/prepared aggregate,4mutable resources/32sources,64KiB chunks/<=2payload chunks,64workspace files/256MiB allocated bytes,4GiB total counted source IO,30s single capture/prep/mutation and60s total prelaunch preparation,32resource FDs/64total,64path components/4096B, nlink1/no symlinks. No fake small chunks/cp outside preparation/omitted source binding/full64MiB allocation/E wrapper raising old caps. Source/byte/time counters do not reset at handoff. Actual TOOL-size fit remains unknown.

## T182 — real managed lifetime, causal ownership and reachable new TEST CLI

Implement exact frozen public API signatures/results/errors from API.md. open_session(NewWorkspace,StreamPolicy,ManagedPolicy)→opaque Session with capture/prepare/tool/mutate/launch/snapshot/close; ProcessLease identity/verify_current/open_endpoint/finish/cancel; CheckedChannel exchange/send/receive/close. New copied observations/results remain separate from old Result, include actual creation/identity/epoch/time/IO/cleanup/durability facts. No mutable exported aliases, raw control/resource FDs, receipt constructors or JSON-issued ownership. Mutation failures are raised with retained UNUSABLE facts, not returned as normal success.

Chosen mechanism is mandatory: ONE isolated private supervisor process is actual foreground parent/reaper; retained positive pidfd/unreaped anchor; worker owns source/resource/channel FDs, journal and streams. Coordinator holds opaque client handles. Two private inherited CLOEXEC bounded framed pipes, normal source-bound creation proof/HELLO; worker retains coordinator pidfd and observes control EOF independently. No public path control socket/pidfile provider, no daemon adoption/subreaper in this capability. Worker uses same engine as old Attempt, not duplicate code. No foreground launch before durable separate SPAWN_INTENT. Actual fork/exec-witness facts distinguish not-attempted/possible-unknown/spawned-unbound/currently-owned; loss after possible spawn stays UNKNOWN, never0. Caller-observed JSON cannot upgrade it.

Supervisor continues draining/limits/kernel/source checks while E-like TEST consumer IO runs, not behind synchronous callback/whole-file work. Capture/prep jobs process <=64KiB chunk then service monitor, not suspend it. Handoff resets NO counter/deadline/first fault. Same private root/channel/resource epochs and actual kernel PID/startticks/exe/argv/source/connected peer bind every operation. Verify before any TEST bytes AND AFTER waits, reads/writes/progress/final acceptance and before Ready issuance (I1/I2). Fast-exited/unverifiable owner refuses ready:false even full expected reply. Timestamped observations are not future liveness or universal unseen exec/fork audit. Every later action revalidates live opaque lease; stale responses cannot authorize it. No arbitrary unbounded Python callback/API/factory can mint ownership. Existing bounded CommandSpec observer semantics remain backward compatible.

Freeze NEW ManagedPolicy.test_v1 independently:1coordinator session/1foreground child/serial operations; startup<=15s; initial readiness phase<=60s from OWNED and remaining total (no per-byte/repeated READY reset); total child default120s/explicit selected<=900s from durable SPAWN_INTENT; complete session<=960s; observer/mutation command<=15s and16 OS commands/session; stream1MiB each/16MiB total;8processes and256MiB sampled RSS INCLUDING coordinator/supervisor/child+owned descendants; worker/child AS256MiB each/core0; client buffers<=2MiB; monitor requested<=10ms/100000polls; parent loss observed<=10ms/begin containment<=250ms observed; TERM200ms/KILL+reap1000ms; passive finish<=10s and remaining clocks;64KiB control frames/16KiB raw chunks; JSONdepth16/nodes2048; argv/env16KiB each;4096messages/64MiB wire;512journal events/1MiB; endpoint request/reply4096B each/exchange<=60s+remaining clocks. These are finite TEST ceilings, not measured QEMU/DOS/runtime SLO claims. Parent global rlimits are not lowered; aggregate observation can refuse overshoot. Kernel/filesystem/scheduling latency remains host-dependent, no hostile sandbox/hard real-time claim.

Session lifecycle NEW→OPENING→PREPARING→IDLE→SPAWN_INTENT→SPAWNED_UNBOUND→OWNED→READY→EXIT_OBSERVED→STOPPED; any fault→FAULTED→CONTAINING→STOPPED_UNUSABLE or CLEANUP_UNKNOWN→CLOSED. Parent/channel loss, source/identity/persistence/stream/resource/clock fault is sticky, positive own containment only, unknown ownership never signalled/unlinked. finish sends NO protocol/signal and returns actual generic ExitObservation only after bounded direct reap/session observation; daemon_state remains UNKNOWN, not all escaped-process absence. Containment invalidates attached resources, no failed-HD extraction. E normalDOS/opaque quit/stopped exports/master/release/accounting are NOT provided by this API; no P→E import or implicit original grant.

New CLOSED actual public `managed-fixture CASE` route on amended facade must use PUBLIC operations for streaming64m, mutable-success/failure, handoff, parent-loss, cancel, foreign-endpoint, unknown-launch, process-progress, readiness-deadline-progress, exec-reply-exit, prior-no-clobber, worker-death, stale-handle and wrong-root-load. Old fixture CASE8 unchanged. No arbitrary recipe/path/profile/argv/grant CLI. Every new module has real reachable caller/source graph evidence, not helper-only demonstration/dead API.

## T183 — real public OS adversaries, preserved defaults, mutants and closed custody

Read/follow ALL ACCEPTANCE.md and exact reviewed limits. Freeze authored fixture rights/full source/tool/import/argv/env/cwd/FD/policy roster BEFORE runs. Actual disposable64MiB source gets known hash and FULL streaming byte-equality after prep; measure chunk/buffer/RSS/IO/time work, prove >64MiB/aggregate/deadline/source/alias/target/persistence refuses. Generated large files remain disposable TEST workspaces (never proprietary), not huge committed raw payloads; retain reproducible generator/source plus actual SHA/size/full comparison/process/resource receipts.

Prove NEW larger immutable source policy applies to EXECUTABLES, not only data. Freeze a harmless valid public test executable >8MiB and <=64MiB with known full size/hash/rights (for example a TEMP copy of the declared public test Python ELF plus bounded authored trailing padding, ONLY if actual Linux direct-exec control proves it valid; do not assume that result now). A live harmless invocation keeps identity observable for real Session.tool→launch→finish; old ArtifactSpec/CommandSpec default must refuse the SAME large file before launch. Test mutated/retargeted/hash-changed large executable sources through the actual public new lease path, with stream/FD/source/hash refusal and bounded memory. No copied executable payload is committed/published, no actual QEMU/private tool is read or measured, and no real-reference size fit is inferred. If a valid fixture or the reviewed new executable-source path is insufficient, report the precise prerequisite rather than claiming data-only success solves tool capture. This is acceptance of the reviewed distinct policy, never widening old caps.

Real OS mutable success/new epoch and nonzero/FSIZE-shortwrite/interrupt/close/rename/persistence/atomic faults: prior/foreign bytes unchanged, partial target/unusable source-bound facts true, old handles stale/no reset. Real handoff while resource/stream pressure and client IO occurs; actual parent kill/control close with TERM-ignore child, worker death/unknown cleanup; own cleanup/reap bounded, no unrelated PID/group/socket signals/unlink. Actual spawn-then-report/journal/ownership failure/delayed or reused identity and daemon escape: UNKNOWN never zero or adopted from JSON/pidfile. No mocks/private-global patches/successful dummy executor.

Replay old62 public cases/old8 CLI against actual new shared-family code without changing old58 test/source/result bytes. New owned runners emit evidence only under new namespace (old58 mutation/capture runners write old paths and MUST NOT be invoked unmodified to overwrite history). Preserve their actual public falsifier semantics; new source-based mutants may need different source locations after extraction. I1 actual3vs2 progressing reply, transient RSS/streams,0.1readiness vs2parent/absolute clocks; I2 samePIDexec/differentargv/fullreply+fast exit twice, partial reply/delayed control/exited-owner socket, current-identity positives. All require true refusal/ready:false/sticky/noNEXT and real source/identity/cleanup facts. Freeze source-dir/class identity/importlib/standalone foreign-cache tests per LOADING-SCOPE. Wrong source/hash/epoch/wrapper/late/duplicate/cross-session attempts refuse before IO. Public TEST/direct CLI flows, not testing only internals.

Meaningful finite actual-source mutants must challenge every critical source/stream/atomic/monitor/absolute-clock/ownership/parent-loss/lease-expiry/ready-acceptance guard through public APIs/CLI; retain raw red errors/survivors and strengthen non-discriminating probes rather than suppressing them. New-class authority must be proven under same-root alias loads and foreign/worktree/source-cache collision, no registry/sys.path/helper patch. Original-reference sources are never loaded to make a fixture convenient.

Run genuine configured7, honest actual Go discovery/legitimate skips, AST/compile/source whitespace, component/JUnit/resource/alias/fault checks; no Go overlay/new native helper or unchanged parser long fuzz. Source-only lint0 is distinct from raw retained log whitespace2; record actual exits. At each source freeze bind actual full old source inventory/Git/working blob hashes (old511 metadata provided, not3.7MiB duplicated raw), all unchanged legacy/callers and Go/modules; all altered source paths ONLY owned family/test/evidence. Old58 test/contract/raw/approval snapshots remain exact history, not rewritten to pass.

Publish deterministic semantic contract/CLI projections where meaningful (not fake byte-equal PID/time logs), actual command/env/cwd/binary/source/current ownership, measured RSS/process/FD/bytes/time, no pending own workers, source/handoff limitations and future directE interface. Complete recursive source/evidence SET/SHA/size/Git-blob seal MUST include nested historical seals and exclude only its own exact root manifest. Metadata/handoff cap2048files/32MiB is DISTINCT from runtime/file/prep/output limits and grants no waiver; retain all failures under fixed bounds, stop if insufficient rather than truncate evidence silently.

Commit ONLY owned source/test/evidence. Request ROOT primary quietpoint BEFORE T181–183 status/history/ONE normal for_review with explicit codex/implementer-ivan/mission identity; poll entire synchronous gate/CLI to actual exit, no force/skip/bypass/kill/retry/manual metadata repair. Separate independent code review mandatory; no selfapproval/merge/acceptance/push. If source/ownership/API/limits are insufficient, report concrete BLOCKED prerequisite without broadening scope or substituting old fresh_start. FullM1 stays open.


## Normative successor clarification

The active contract contracts/startup-family-successors.md and its seven conformance groups are mandatory for T181–T183. It repairs successor lease delivery after mutation and stopped-resource requalification while preserving method signatures, limits, old WP58 APIs, IDs, dependencies, and ownership. It takes precedence narrowly over the historical R2 result-field/facts-only and snapshot-epoch clauses; all other frozen requirements remain binding. Independent review found no blocking findings. Historical proposals remain exact in the correction evidence dossier.
