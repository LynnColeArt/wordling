# WorkingLease successor delivery v1

Normative WP61 clarification, ratified after independent review with zero findings. Applies solely to NEW startup_family managed-resource API; old approved58 ArtifactSpec/Attempt/Result/defaults/CLI are unchanged.

1. Add one public field to existing immutable NEW result contracts, preserving current method signatures and all other fields:

   MutationResult.successor: WorkingLease | None
   Snapshot.successor: WorkingLease

   COMMITTED MutationResult has exactly one non-None successor; UNUSABLE MutationResult, available only inside raised failure diagnostics/history, has successor=None. Snapshot is returned only on success. Any failure raises StartupFailure and exposes no usable successor through its PartialOutcome/history/serialization.

2. Mutation success: the supervisor validates the exact current issuer/session/channel-generation/resource/epoch/op binding, performs bounded same-inode mutation, verifies all existing postconditions and durably records the committed transition. It advances READY(epochN) to READY(epochN+1), invalidates every epochN lease, then issues a fresh opaque WorkingLease for that SAME owned resource and exact epochN+1 in the success result. before_epoch=N and after_epoch=N+1 agree with the server state and successor. No input wrapper is mutated to refresh authority. A stored ResourceArgument using an old lease remains stale; callers rebuild it using the successor for subsequent operations.

3. Snapshot success has two explicit cases:

   - Target is READY(epochN): perform all existing bounded identity/source/hash/journal checks, return Snapshot(epoch=N,successor=target) with the identical opaque input lease and no epoch/state change. Repeated valid read-only snapshots do not invalidate an otherwise current lease. Counters/deadlines still charge normally.
   - Target is DIRTY_STOPPED(epochN): only the already-authorized generic zero-exit/no-signal/no-fault path is eligible. Use its attached prelaunch lease as a one-use requalification input for this state, perform all existing bounded stopped-resource/source/postcondition/persistence checks, then durably advance to READY(epochN+1) and return Snapshot(epoch=N+1,successor=fresh lease for that exact resource/epoch). Every epochN reference becomes stale. This path never requalifies UNUSABLE/UNKNOWN/contained resources.

4. A result's successor conveys only the existing WorkingLease operations permitted by current Session phase/state and unchanged budgets. It cannot reset clocks/quotas/first fault, reopen/replace a session, authorize a second child beyond the existing policy, certify native content/normalDOS/normal original quit, or grant original access. All subsequent use rechecks server-side root/channel generation/resource/epoch/source/ownership/state; a timestamped success result is not future validity.

5. Result containers and observation facts remain immutable/defensively copied. This successor field is an explicit exception to generic “observations are facts only” wording for these TWO types only. It contains a reference to an actual Session-issued nonconstructible opaque handle; no raw FD, secret control pipe or mutable server table is exposed. JSON projections include at most diagnostic nonauthoritative lease facts (or omit the field), never a transferable/rebindable capability. Constructing/copying/wrapping a result or its fact fields cannot issue a lease.

6. Any mutation/requalification/postcondition/journal/control failure preserves sticky fault and actual partial effects. A transition may already have committed when reporting fails: do not pretend rollback or unchanged epoch, recover authority from epoch/hash, retry, or expose a successor on an exception. Preserve actual committed/unknown facts, invalidate further operations according to existing fault rules, and contain/close. Lost, delayed or replayed responses cannot refresh authority; server epoch/state remains authoritative. No public lookup/resume/reissue endpoint is added.

No method signature, old API, chosen file/process/time/RSS/IO/FD/output/journal/wire limit, ownership namespace, import DAG, opaque process lease, E boundary or grant rule changes. Existing minimum absolute clocks/I1/I2 protections stay binding. This addendum corrects successor composition; it is not a policy expansion or prototype.


# Proposed additive conformance cases

Harmless authored TEST files/tools/processes only. Run after ratification against a separately frozen implementation through public APIs; nothing is executed by this review.

1. Prepare epoch0→successful mutate. Result is COMMITTED, before0/after1 and usable opaque successor for same resource. Use successor for bounded READY snapshot and a second public mutate (within existing prelaunch phase/command budgets), obtaining epoch2; subsequently use that successor in launch resources and ResourceArgument. Observe actual intended bytes, same inode and immutable source unchanged. Do not expose private epoch tokens/FDs or patch internal registries to arrange success.
2. READY snapshot returns same opaque input object, same epoch and exact bounded digest; repeat snapshot within limits then use the still-current lease. No artificial version churn, quota reset or mutation.
3. Prepare/launch→actual generic zero-exit/no-signal/fault finish→DIRTY_STOPPED snapshot. It returns exact epoch+1 and a current successor; another permitted READY snapshot with that successor succeeds without further epoch increment. The attached old lease is allowed only for the first eligible stopped requalification, never as a general stale bypass. Do not add a second child or reopen the terminal session merely to prove handle usefulness.
4. In separate fault-isolated sessions, attempt each old lease/ResourceArgument after a successful version change: refuse before tool launch/file/endpoint effect; retain sticky fault. Old scalar epoch/hash facts, public result wrappers, forged dictionaries and cross-session/fork/wrong-generation handles cannot reacquire authority. A stale-probe refusal is not followed by a claimed successful action in the same sticky-failed session.
5. Actual nonzero/short-write/interruption/source drift/rename/postcondition/journal failure: UNUSABLE diagnostic result has successor=None; no successful Snapshot/lease on exception. A possibly committed transition followed by reporting/control failure retains actual/unknown facts and no usable recovered handle. Existing diagnostic getters/containment/close only. Prior/foreign/immutable bytes remain protected under original requirements; partial owned target effects are not rolled back.
6. Replaying an older success result after a later epoch change or session fault/close does not revive its successor. Altering/reconstructing the immutable result cannot refresh issuer authority. Wrong-root result/cache cannot bridge source families. Genuine current successor remains class/issuer-compatible across same-root supported alias entrypoints.
7. All original old58 compatibility and current new streaming/supervisor/I1/I2/ownership/UNKNOWN/failure acceptance cases remain required; this change cannot weaken them. Report these additive cases and source-bound result/journal projections without serializing actual authority.


This active clarification takes precedence only over the frozen R2 result-field lists, facts-only wording for these two result types, and ambiguous snapshot epoch wording. Historical R2 artifacts remain unchanged. Proposal and independent review are preserved under docs/research/continuation/startup-family-task-review/successor-correction/.
