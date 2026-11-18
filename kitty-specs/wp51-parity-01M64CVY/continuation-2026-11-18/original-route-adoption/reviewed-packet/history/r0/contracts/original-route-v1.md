# Proposed original-route source contract

Audience: implementer and independent architecture/source/safety reviewers. PROPOSAL ONLY. No operational permission, source approval or actual original qualification follows from this document.

## 1. Authority and source boundary

Keep the existing TEST `ReferenceController.open_leaf` exact-type `TestGrant`/`TestIssuer` checks and harmless CLI behavior. Add a disjoint original entry in canonical package modules `original.py` and `original_release.py`; never cast, subclass, wrap or relabel TEST authority as original. Original source/deployment policy is a distinct exact validated type and retained registry binding; extending common validation must use an explicit exact-type branch, not duck typing or a caller-supplied validator.

Proposed interfaces (names may change only through recorded task review):

```text
trusted original_release ROOT entry -> opaque RootDecision
RootTicketIssuer.issue(RootDecision, OriginalSourcePolicy, OriginalLeafPlan)
    -> opaque one-use OriginalGrant
original.open_original_leaf(source, immutable_plan, OriginalGrant)
    -> opaque OriginalLeaf
OriginalLeaf.prepare_and_launch() -> diagnostic OWNED_UNREADY facts (WP104)
OriginalLeaf.run_leaf() -> bounded diagnostic OriginalLeafResult (WP105)
OriginalLeaf.close() -> truthful containment/retention facts
```

The trusted ROOT entry is part of the independently reviewed source closure, not a public grant-file loader or `--allow-vm` boolean. It may create a RootDecision only for an actual fresh ROOT decision bound to exact accepted code/deployment/recipe-source hash, immutable plan hash, reference profile, case, start context, repetition, candidate identity, unique grant ID and fixed leaf maxima. RootDecision/OriginalGrant are nonconstructible, noncopyable, nonserializable live objects held in source-owned registries. A path, hash, copied fields, review JSON, environment flag or old dispatch record alone cannot mint one. State explicit trusted-host/ROOT-coordinator assumptions; do not invent a new cryptographic or remote authorization service.

Use an acyclic hash graph: code/recipe/data plan → reviewed source/plan seals → fresh ROOT release binding. Do not require a source file to embed its own final digest or recursively reseal past reviews. Actual constructor/entry provenance must be independently reviewed before implementation is released. No fake root provider in tests; any ROOT control release must actually be issued for a finite harmless control roster.

Original issuance reuses the existing durable TicketStore/LeafAccount/ParentLease machinery with a separate original kind/root/generation. Preserve permanent O_EXCL spent IDs, fsync/readback/current identity order, same-book handoff and no-refund/no-recovery semantics. Changed source/plan/repetition never permits reusing a spent ID. Missing/pre-existing/partial/foreign markers, wrong boot/generation or lost reply cannot yield another grant. Original-store administration is a separately authorized bounded prerequisite, never automatic leaf setup.

Before publishing a grant, durably retain a nonterminal safety reservation under the same original store. An unresolved reservation blocks issuance for other IDs too; kernel release of a dead coordinator's lock must not be interpreted as safety. This is a refusal predicate, never persisted authority from which to recover a grant. WP105 may terminally discharge the reservation only from the same actual retained context's genuine stopped/containment/export proof. Loss/partial persistence/UNKNOWN leaves it quarantined; no automatic recovery, generation switch, deletion or new-ID escape. This uses existing finite store/book/record primitives; if it needs a new generic account/P API, split and review that prerequisite before implementation.

## 2. Offline preparation versus actual private effects

WP104/105 only deliver and qualify source with harmless resources. Invalid/no release refuses before any private original/master/tool/guard stat, read, open or execution. Offline plan validation reads only reviewed public source/declarative manifests and harmless fixtures; module import does not probe private resources. Actual reference fitness is UNKNOWN until a later real release permits its finite checks.

The original ordinary wheel/venv is separately staged by new `tests/original_deployment.py` using `original-pyproject.toml`. Preserve the existing TEST build recipe, package name, fixed TEST source/data roster and its installed public consumer. Original entry uses a pinned copied interpreter with `-I -B`, no user site/customization/cache/foreign module/PYTHONPATH overlays; validate exact complete installed source/import/class identities before project execution. No network installer or proprietary payload in the wheel. New manifests are a closed source-owned schema, never arbitrary extra source modules.

## 3. Physical ownership and ONE foreground

After actual grant consumption, acquire and retain the **existing shared original session guard**, not the TEST `.physical` marker. It must bind a source-selected retained parent/regular file FD, ancestor/name/inode/owner/mode and nonblocking exclusive lock; recheck live association before/after bounded operations. Missing/unproved guard setup blocks; no unlink/replacement or creation on behalf of an expired release. Preserve physical safety holds after unknown stop/control/identity loss; closing a logical lease never asserts safe release.

ONE LeafAccount origin/end funds store, setup, physical guard, protocol, P, helper, chunk, publication, audit and cleanup. Reuse approved `startup_transport` canonical source/class loader and P63/64 public interfaces: capture→prepare/tool→mutate-successor→launch→ProcessLease.verify_current/finish→snapshot-successor→seal_stopped→derive_readonly→read_chunk. Keep one Session/worker and one foreground original. Retain actual ProcessLease privately; no PID-file authority, daemonize, legacy guest/QMP globals, second P Session, daemon adoption or copied usage/exit facts.

QEMU configuration is the reviewed existing offline profile: fixed executable/resources, no network/host shares/serial/parallel or arbitrary media/device/capture options. No external resource acquisition. Firmware and working copies are explicit bounded sources/resources. Every tool, helper, argv/env/cwd/rights and import/source closure is frozen before permitted effects. Source-declared hashes are expectations; actual capture verifies identities after admission.

All existing intrinsic maxima remain ceilings: 64MiB/file, 256MiB captured sources, 128MiB prepared, 4 working resources, 32 sources, <=16KiB chunks, 4GiB brokered source/transfer IO, 16 commands, 8 processes, 256MiB sampled combined RSS, 64 aggregate FDs, 4096 control messages/64MiB wire, 512 journal events/1MiB journal, and existing per-operation/session/child/readiness deadlines. Select a finite earlier leaf end and smaller immutable phase budgets; total fit including every read/check/response reservation and cleanup must be demonstrated before effects. Declared 64MiB disk size is at the file ceiling, not proof of current resource/aggregate fitness. Missing measurements are UNKNOWN, not zero; no cap increase, restart or refund on failure.

## 4. Authentic readiness and finite text observation (WP105)

Readiness requires authenticated actual QMP peer/current retained child and a real original UI observation; a greeting, TEST token, elapsed delay or caller `ready=true` is insufficient. Preserve approved peer/QMP JSON codec and bounded stream. Use a closed, source-owned QMP command/argument grammar, with reserved complete line/event/transaction/poll costs and pre/postblocking deadline/source/identity checks. Do not inherit legacy `QMP.__enter__/text/capture/wait` methods that reopen globals, write arbitrary paths or reset clocks.

The minimal proposed UI observation is exactly the existing 4000-byte 80×25 text VRAM region via fixed `pmemsave 0xb8000 4000` into a fresh retained **observation slot**. Slot name/path is source-selected, no-clobber, funded before issuing the command, held by the same E context and checked by FD/path/inode/length after real command completion and identity/deadline checks. Read exactly 4000 bytes, retain raw bytes/attribute facts and the declared CP437 text projection; hashes/decoded status are observations only. No image decoding, arbitrary memory ranges, disk read, packet capture, screenshot filenames or new media command is admitted. If this retained-slot method cannot meet actual ownership/accounting/response semantics, stop for an explicit design amendment; no unmanaged `qmp.text` fallback. Cursor/status observations must state their limits; do not invent hardware-cursor proof from footer text.

First greeting and readiness use earlier creation-bound clocks; no per-poll reset. Observe genuine blank/current filename/Doc1/status/start facts before invoking the reviewed recipe. Failed/foreign/late/partial readiness permanently refuses subsequent keys and successful export; a timeout cannot become readiness success.

## 5. Normal stop and stopped export (WP105)

The same context records actual original recovery/normal WP exit and DOS-ready witness before one audited QMP quit and its real successful reply. Original cancel/F1, program error, normal WP exit, QMP quit, generic process exit and containment are distinct facts. Parameterless internal finish calls retained P finish once. Only ordered, source/plan/grant/leaf/session/epoch/process-bound normal-DOS/quit evidence plus eligible direct passive exit can issue a private stopped object. No caller-supplied witness/ExitObservation/dict/lookup/retry can mint it. Retain P's `identity_at_exit_unproved`/daemon UNKNOWN observational limitations; no sandbox/unseen-exec claim.

Parameterless export consumes that internal stopped object and current snapshot successor, then P's readonly seal, same-worker readonly helper derivation and sequential authentic chunks. Use a fixed source-reviewed mtools/helper plan for exact declared output names and positive absence; no live image reads, writable master arguments, shell, glob expansion or arbitrary paths. Native files are copied as original bytes; no WPM/format manufacturing or normalization. Publish through retained O_EXCL destinations with full byte/hash/readback/fsync evidence; empty, missing-required and expected-absent are distinct outcomes. New `original_export.py` is a closed readonly helper/validator only; it cannot launch QEMU or acquire grants.

Only after proven stopped export, required checks and containment can the actual physical guard be safely released, with immediate notification preceding finite audit. Unknown stop, helper/IO/source/control/journal/publication failure retains actual partial effects, spent credit and safety-hold diagnostics; do not signal safe release or publish success. No normal-stop retry, second original, resumed session or cleanup FD reuse.

## 6. Source/test acceptance versus original qualification

Commit RED tests through actual installed public entry before implementation. Use harmless authored fixtures and real OS processes/peers/FDs/helpers for machinery; label all such results CONTROL/TEST, never original behavior. No fabricated RootDecision/OriginalGrant, private registry patch, fake source/identity/READY sampler or substituted P provider. A genuine ROOT-authorized harmless control release may exercise the real original admission machinery only for its exact source/plan/control leaf; it authorizes no proprietary target. Otherwise report original-positive admission unrun, not passed by substituting TestGrant.

Per package freeze <=28 public OS controls and <=64 total logical cases including separately enumerated schema/parameterized negatives, <=30s/case plus <=2s cleanup and <=300s total; source review must approve a finite extension before any overrun, not retry-to-green. Evidence <=1024 files/16MiB/package, preserve raw failures/UNKNOWN/mutant survivors. Schema negatives cannot replace meaningful OS controls. Semantic mutants must compile and fail the intended public safety target. Existing relevant TEST/P contracts and configured Python compile/discovery/lint checks remain required; no unrelated Go/full fuzz campaign or made-up skips.

Independent task/architecture review precedes claims; independent source/safety review against immutable closure and actual command/cost plan precedes ROOT's original release. Reviewer differs from implementer. WP104/105 acceptance closes bounded source/test delivery only. Actual eight pristine leaves (four cases × two copies), any edited-New leaves and native reopen/edit/print leaves belong to later reviewed WP101/WP102 releases. No all-M1, parent family, new context or original compatibility verdict follows from component success.
