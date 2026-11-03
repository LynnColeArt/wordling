# Exactly ONE cumulative LEAF envelope

DESIGN ONLY, absent public addendum. One Controller, one owned leaf/ticket, one P Session/worker, at most one original foreground child. A helper is a separate bounded phase in that same worker AFTER that original is terminal. No second original, second Session, NEXT, subset/resume or implicit four-leaf coordinator is in this delivery. Total durations, launches, bytes, wire, metadata and work budgets below apply from ONE leaf's pre-effect origin through its final semantic audit/publication, NOT to four leaves and NOT independently to each phase.

The earlier origin precedes charged setup. Absolute time and all spent/reserved counters persist through source capture/preparation, E peer IO, passive finish, stopped snapshot, readonly derivation/publication and post-release audit. One close is terminal; failure/report loss never issues a new session. A wrapper cannot reset policy to rerun a leaf. This is a smaller reviewed contract, not a silent split of the prior promised four-leaf budget. Future batch authority/allocation/repetition proof is explicitly deferred in DECISION.md.

## Frozen candidate ceilings and precise units

The proposed optional SharedEnvelopePolicy at open_session binds the per-leaf absolute end/stricter ceilings BEFORE effects; it is ABSENT from the current public signature. Relative P durations or a current identity timestamp cannot silently redefine the E origin. All existing P61 intrinsic limits remain unchanged; future opt-in envelope must be <=them, except dimensions explicitly defined as distinct accounting totals below. Values below are proposed ceilings, NOT QEMU fit and NOT original capacities. Actual private inventory/host fit can BLOCK them, never change during an attempt.

- Wall time: one monotonic origin before charged setup; total acquisition+required extraction<=960s, original child selected<=900s (default120), startup<=15s, initial E greeting/capabilities<=60s from OWNED, helper<=15s/each, passive finish<=10s, all bounded by absolute remaining. Source/UI audit after physical release still has a finite declared deadline and remaining budget; insufficient remaining blocks, never newSession.
- Process/RSS:<=8 actual owned coordinator+supervisor+original/helper+descendants,<=256MiB combined sampled RSS, worker/child intrinsicAS256MiB/core0 unchanged. No E-launched subprocess while worker owns a phase; actual readonly helpers run in that worker. E parser memory is coordinator memory, included. Peak samples/overshoot retained; no hostile sandbox/hardRT/unseen-fork claim.
- FDs: existing32 resource FDs and intrinsic64 per worker/child remain. Proposed E per-leaf aggregate openFD ceiling64 across coordinator+worker+active child requires new actual actor-bound usage/enforcement; it is stricter optional accounting, NOT a false claim current P already enforces global64. Baseline/host extra descriptors must fit or block. No raw secret FD transfer.
- Data:64MiB/file/tool/working resource;256MiB declared immutable source total;128MiB prepared;4mutable resources/32sources;64KiB streaming/<=2 chunks;64workspace files/256MiB allocated. Tools/resources are opaque data; actual original sizes/links/rights/canonical names UNKNOWN. Native verifier still retains approved64KiB input gate; larger P extent is not native admission.
- Controlled source/transfer IO:<=4GiB cumulative hashes/copies/snapshots/derived streams/E publication IO counted exactly where brokered; no reset at successor/phase. Internal device IO of opaque executables is a DIFFERENT dimension, not silently counted as source_io. Readonly helper rchar/wchar/child-IO samples need explicit bounded measurement/unknown handling; cannot infer all actual disk/mmap IO from resulting file size or /proc read_bytes. If a hard all-syscall/all-mmap byte cap is demanded, this design is BLOCKED pending an additional broker/sandbox capability; not claimed by current non-sandbox P. Actual internal QEMU device IO remains unqualified by this source report.
- Commands:<=16 total external tool/original/helper launches, charged before invocation. Actual E protocol commands are separately bounded<=512 request transactions/<=4096 events, no unlimited native/key loops. All count before fallible send; original roster may need fewer. No counting just successful exit or resetting at post-stop phase.
- Bytes:<=1MiB stdout/stderr per job;<=16MiB cumulative managed output. Proposed ONE combined control+E-protocol wire<=64MiB,<=4096 control messages with framing/depth16/nodes2048/argv+env16KiB and <=4096B QMP line. E per-command<=64events/64KiB. Own stream reads are real bounded reads, not capture-then-slice. Control wire actual/reserved fields currently absent publicly; OptionB must expose them before this is enforceable.
- Journal<=512events/1MiB for P server; E account/wire/custody journal uses a separately named finite metadata allowance, INCLUDED in a per-leaf<=32MiB/2048file audit envelope, not falsely folded into512 P events. No raw16MiB payload hidden in journal. Failed durable publication grants no release/NEXT. This distinction avoids pretending P's old journal can contain a full E reference run.

## Retained authority and reservations

Envelope retains actual Session, source-bound bounded E stream, owned one-shot account/root directory capabilities and selected absolute deadline. All credits are scoped to this ONE leaf. Before effects reserve maximum response/IO/FD/job/wire amounts from actual remaining allowance. Session.usage is called internally on its retained actual session; external observations cannot supply/refund credits. Server enforces P limits while E stalls. E accounts actual bounded protocol bytes/commands. Lost/late/unknown reply spends its full reservation and permanently HALTs this leaf, with no refund/reissue/new controller under the same plan. Successful audit cannot replenish counters.

P close currently supplies only partial final totals; public live usage/control wire/messages/aggregate FDs and same-supervisor export capabilities are absent. Option B must provide them before this envelope is implementable. Source_io is brokered transfer IO; opaque device/mmap/tool IO still has the precise unknown/non-sandbox limits above. No duplicated E supervisor or two-session reservation arithmetic is claimed as an existing solution.

## Resource and release custody

Actual retained parent nofollow directory/account capability owns the run namespace; P workspace and actual server leases bind root/source/epoch. A pathname/hash/result is not authority. Only actual stopped successor + internally retained E StoppedRun and P server history allow readonly sealing. Server outputs are fresh no-clobber opaque handles; bounded streaming into E-owned output proves exact bytes. Missing required export and explicitly expected absence are distinct.

Physical reservation is held through actual normal stop, accepted stopped extraction and required master/export checks, then released and immediately notified BEFORE readonly semantic audit. The logical ONE-leaf reservation remains held until actual leaf completion or explicit root safety disposition. Unsafe stop/fault cannot claim qualified release or read the failed image. Final audit failure leaves permanent incomplete; no NEXT. Lost output or stop capability cannot be reconstructed from diagnostic JSON/hash/path.

## Cardinality and scope table

| Dimension | Scope | Maximum/reset rule |
|---|---|---|
| Root original grant | one exact leaf | not a subset of an old multi-leaf grant |
| Controller/Envelope/P worker+Session | one per leaf | no successor Session/reopen |
| Original foreground launch | one | never restarted after terminal |
| Readonly helper launches | same worker after stop | together with original/prep <=16 total |
| Time/IO/wire/output/metadata | whole leaf including audit | ceilings above, never per-phase reset |
| Process/RSS/FD/file live limits | actual simultaneous bound actors/resources | maxima/peaks retained, not replenishable credits |
| Four-leaf family/repetitions | DEFERRED | no batch API, budget or count claimed |
