# WP109 / WP110 / WP107 combined scope R1 review

**APPROVE_TASK_SOURCE_SCOPE. No blocking findings.** This approves the exact proposed tasks/amendments only. It does not approve source implementation, normal registration/status, execution qualification, original interoperability, a final Windows candidate or M1.

Reviewer: reviewer-renata, using previously resolved read-only governance/profile context. I authored none of these R1 tasks and no production implementation. R0 WP109 approval is preserved byte-for-byte under `copy-italics-source-amendment/history/r0-native109-approved/`; this review adds the separate Runtime ownership scope, not retrospective source approval.

Packet directory `/tmp/wordling-mission1-closeout-20261118/copy-italics-source-amendment/`:

| Artifact | SHA256 |
| --- | --- |
| WP110-runtime-completion-ownership.md | `1c28f05cf24f05040b7889f6dda0b6200029b9807bd61893406cdda8ea2a3f8a` |
| WP109-copy-italics-native-producer.md | `aada735ca64e72eacfe753e5557880814b1e44d2335428249b255aaad5fbb59b` |
| WP107-retrieve-italics-public-integration.md | `90ab169fbeb9f88b57ecbb5fc8940babb90e77296d9803359919bacb7ddcb659` |
| source-pins.json | `d984a591b9e8e6bd2a6a400972cc6fe1aa87abfa21885f20199b967f140430b5` |
| projection.json | `1affd3dcff264f543b428b7f567065ae3760cbe9e0825433fc24eb9c826115b3` |

## Actual defect and source feasibility

The raw f6abda6b reproduction and its test/source hashes are consistent. It opens two independent actual public Runtimes on one root, acquires the real selected files, holds the current Runtime callback, and delivers the other Runtime's genuine callback with colliding numeric Operation/Revision/ReadSelection. Raw output reports PendingIO0 while ownCompleted1, foreignCompleted2 and ownSessionPending=true. Source/native/binding remain protected by Session; the defect is earlier host bookkeeping, not demonstrated disk corruption or a fabricated Result. The exact test hash `01bb0bb238b8deb833fb31488f41fd0d477f3233a1975e52754260acb25e09d4` and all four exact f6 source pins match. All10 current source/legacy-test/task pins match their declared30943680 Git objects.

Actual `Model.reduce` appends a numeric operation then calls `runtime.dispatch`; ordinary `resultMsg` is a bare editor.Result. `Model.Update` forwards it to completeIO, which removes unsettled by numeric triple and updates Reconciliation/detached-publication state before forwarding to Session authentication. Thus the proposed real host/per-issued-request queue custody must be checked before **all three** of bookkeeping, reconciliation and Session delivery. Merely rejecting foreign Session payloads later or checking ReadSelection would leave the cause intact.

The two production owners are sufficient. model.go can carry the queued opaque request identity in its immutable pending chain, validate it after the existing actual UI-authority gate and before completeIO, while runtime.go can create/return a private sealed envelope only for actual Model queue dispatch. It can reuse Runtime mutex, executed map, workers, stopping/capacity and copied-result mechanisms. No new editor API or generic grant/query factory is necessary. Same root/path/inode, Runtime numeric keys and copied metadata are not the actual issued request identity. Persistent stale Model copies must be refused by the existing transition authority before consuming the live receipt; delivered messages cannot become an alternate authority. Actual implementation must preserve those facts and bounded receipt lifetime, not merely add a private type name.

The inventory requirement reaches every ordinary producer, not only the repro branch. The ordinary return paths in runtime.go include successful/end-of-command completion and stopping/capacity refusals, both generic and everyday authenticated refusals. Model.reduce is the live ordinary dispatch route. Runtime.command remains a diagnostic/specialized entry; the only other live Model command caller found is macro_model.go's ReadMacro path, which already returns its own macro receipt. Existing first-save, macro and proofreading shapes are separate protected contracts; keep their guards/one-shot ownership and substantive existing tests. In particular proofReply's owner/kind check and completeIO path must remain valid while bare ordinary resultMsg loses all bookkeeping authority.

Keeping the historical single-field resultMsg shape as a refused input allows existing bare-negative tests in new_test.go and proofreading_runtime_test.go to compile unchanged. Raw diagnostic runtime.command observations can remain raw only when they cannot be fed back as an owned ordinary UI completion. The task explicitly requires proving that no live ordinary path bypasses queue custody; no partial constructor migration/dead helper is allowed. No extra production owner is currently needed.

## Test ownership, RED chronology and real error semantics

The proposal correctly requires acceptance tests to compile on actual pre-code source and fail at the real PendingIO/foreign-callback defect. New tests must use opaque genuine callback messages rather than refer to a newly introduced private envelope type and then mistake a pre-code compile failure for RED. The existing repro is supporting exploratory evidence; future WP110 native/public RED is committed before any production change.

The test matrix retains actual callbacks for success and real stale/read errors; stopping/Close/capacity before IO; cancel→own late completion; retry/new request and reordered delivery; duplicate invocation and receipt delivery; independent same-root Runtime collision; persistent/stale Model copies and immutable Completed diagnostics. Ownership settlement must affect only the exact queued operation, preserve a newer pending request and execute admitted IO once. Duplicate/error paths must retain the actual1024 receipt bound and avoid an unbounded retained ticket registry. Cancel does not undo filesystem IO already performed: genuine own late publication still requires truthful reconciliation, whereas a foreign/bare message cannot inject a warning or settle current work. Those are contract requirements already stated in T356/T357, not a request for new files or guards.

The three existing test owners are justified by actual code:

- original_test.go's TestFailedUncertainResultKeepsNativeAndNeverExits manufactures a bare matching-key Result with an injected storage.Failure and currently treats it as a positive SaveUncertain transition. It must instead prove an unbound forged error is refused while actual pending work/native state stays intact. This correction must not erase the independently scoped true storage uncertainty guarantee.
- editable_test.go's TestActualPublishedGenericErrorRetainsUncertainty executes a real callback, mutates its Err afterward, then expects authentic SaveUncertain. The real publication should be verified normally; a separate bare forged-error input should be refused. A tampered host message is not evidence of a real disk fault or valid publication uncertainty. Other direct Runtime.command diagnostic type assertions may stay if their result shape remains diagnostic-only; actual Model callback-envelope assertions can change narrowly.
- model_test.go contains callback type assertions for queued Close plus diagnostic command/concurrent shutdown/capacity/duplicate/result-copy controls. Shape assertions affected by the new route may change, while actual no-IO/retained-receipt/one-execution/immutable-state/pending-work assertions remain. Its bare wrong-envelope negatives remain meaningful with the preserved resultMsg shape.

The task explicitly preserves genuine owned error handling, storage uncertainty/reconciliation semantics and existing storage evidence, and forbids a fake owned receipt, hidden test omission, test-only production hook or normal-build fault mode. The source review must check actual error copies/causes and all affected assertions against that DoD. Removing forged positives is not permission to discard a genuine acceptance failure or label a forged negative as real uncertainty proof.

The source-wide ordinary-message custody contract and constructor/caller census are the appropriate structural scope here. Prior specialized receipt types alone do not establish the directive's historical recurrence/contested-ownership threshold; the task requires inspection of actual source/history and prescribed structural review if that trigger is established. Nothing in this approval waives doctrine or licenses another ReadSelection-only point fix.

## WP109 conservation and exact-old replay

WP109 production ownership remains only block_copy.go plus its new native test/evidence. R1 adds no source owner; it clarifies the beginBlockAppend shared caller, all implementation-time contracts (original15 plus two provisional103 coverage artifacts) and separate noncausal host failures in exact-old replays. The previously approved producer tests/partial edges/independent style balance/detached prefix/08 literal mirror/six-wrapper versus old conservative-four bound requirements all remain.

WP107 retains its original test/evidence-only owners and every public rooted Retrieve/Copy, Runtime/loaded/New/save/reopen/foreign/stale/cancel/no-op/negative obligation. It adds110 to its four original dependencies and109. Its final GREEN therefore honestly requires approved106+109+110. Full exact pre106/9f replay may retain the distinct foreign PendingIO failure alongside producer/insertion UnsupportedBody. Classify all raw failures, and use unchanged positive-only selected commands on exact pre109/pre110/pre106 sources to isolate each cause. No later production overlay, false all-failures-one-cause label, dropped control or fabricated early integration chronology is permitted.

The amended appendix is a clear specific update to earlier106-only/106+109 GREEN prose; it preserves those earlier exploratory observations without pretending the later discovered source defect never happened. Native106 and future109/110 retain their real RED-before-production obligations; later integration causal replay is explicitly later.

## Dependencies and projection

WP110 predecessors94/84/85 plus89 reflect the actual Session/UI/runtime/proofreading owners. The initial failed pure projection explicitly reports89 ownership overlap and is preserved; adding89 resolves the real serialization constraint without changing a guard, relabeling a kind or falsely approving an owner. WP109 depends106;107 retains106/94/84/85 and adds109/110, never reverse edges to unfinished107. ROOT withholds107 approval despite the host's already-in-progress dependency re-gating limitation.

The corrected canonical pure projection reports108→110 WPs,313→320 edges,31 lanes,29 existing code groups and zero errors. Independent static inspection confirms every old WP membership retained,109 added only to lane-f and110 only to lane-c, unchanged lane IDs/execution modes/code-group count and an acyclic lane dependency graph. The82→84 warnings are the retained Go/internal-versus-src conventions and new matching declarations, not reported errors or a bypass. These checks are proposal evidence; normal registration/finalization and actual approved predecessor state remain ROOT's responsibility.

## Shared gates and review limits

All tasks preserve native/source/binding invariants, original occupied-Retrieve/Copy and reopen/edit/print/save qualification, independent review, full Go/race/source checks and future exact-candidate Windows PowerShell/default-shell/overwrite validation. Mac stays deferred until milestone end. The two103 coverage artifacts are planning/index evidence, not product acceptance. No CMD51-065/E3, audit/matrix/M1 promotion or original/TEST/P/CONTROL action follows from scope approval.

This review read actual source, legacy assertions, ordinary constructor/callers, frozen repro bytes/raw output, packet diffs and pure projection. It performed only static file/Git-object hash and manifest comparisons and scratch report writes. No test/build/probe, primary/source/index/Op/status mutation, normal finalizer, reference/private/VM/grant/TEST/P/CONTROL/Original/Mac or clock action occurred. ROOT retains normal adoption and durable verdict control.
