# WP68 independent CODE review cycle1 — changes requested

Reviewed frozen source `df651f7b94a708e9b0ec7687499544af97b0e089` against actual parent `fc032d61ac54fefbc6c526d6c761fe3553ee6451`. No reviewer product/source changes. This feedback is TMP-only pending ROOT's canonical-publication/rejection quietpoint.

## F1 [P1] Refuse stale update permits before encoding or filesystem effects

`account.py:100–123` consumes any registered, unused, correct-kind/owner permit without checking its captured `_operation`/record sequence against the account's current update/commit order. Public `reserve_ledger_operation` can issue two genuine update permits consecutively; neither is rejected or superseded. `records.encode` checks the record sequence only against its own permit, and `ownership.py:211–214` counts commits without recording/enforcing monotonic committed sequence.

A fresh ordinary offline-wheel/copied-venv installed public TEST consumer reproduced:

1. Activate one actual issuer grant/book; acquire actual ParentLease and OwnedLedger.
2. Reserve older update permit (operation3, sequence1), create its AUTHORIZED record.
3. Reserve newer update permit (operation4, sequence2), create its COMPLETE record.
4. Write/read back newer record: durable sequence2, ledger_commits1.
5. Attempt older record with its still-unused genuine permit: **accepted**, rewrites full ledger to sequence1, changes ctime and ledger_commits becomes2, with no refusal/fault.

This uses public factories/methods only; no copied/forged/private-field mutation, global patch or hostile-reflection assumption. The exact stale test fails at `STALE_UPDATE_ACCEPTED_OR_EFFECT` (child exit1, normal owned cleanup), after successful actual write/fsync/readback. `out-of-order/1.stdout` retains complete before/after hex bytes and account snapshots; `1.stderr`, `freeze.json`, `results.json` and `out_of_order_probe.py` preserve the bounded repro.

Ratified R2 CONTRACT §1 binds each update to the actual next operation and says stale/consumed substitutes refuse before encoding/effect; §2 requires monotonic operation sequence checked by the account. T202 repeats genuine one-use operation binding and stale refusal. The current consumed-permit test covers using the SAME permit twice, which does not cover this unconsumed older-permit case.

Enforce the actual account-owned ordering/terminal state before consuming/encoding/writing. For example, reject a second outstanding update or invalidate/refuse an older permit before any newer commit can make it stale; choose a contract-consistent implementation rather than treating payload sequence text as authority. Reservations remain fully spent on refusal, no rollback/refund/reissue. Add real installed public and source-level regression coverage for both orderings, stale before/after newer commit, unchanged full prior bytes/ctime and proper reserved cleanup. Existing ordinary sequential transaction must remain useful. Do not weaken the stale or monotonic contract or label the old successful rewrite merely diagnostic.

## F2 [P3; mandatory anti-pattern #1] Use or remove the unused public phase diagnostic

`account.py:75 PhaseReservation.observation()` has zero production callers across all nine frozen production Python modules. AST caller evidence is retained in `F2-callsite-evidence.json`: the only two `.observation()` calls are `cli.py:44,58`, both on `book`, not PhaseReservation. Its result is not used by the ordinary installed consumer.

This is a read-only diagnostic, not an authority bypass; the severity is distinct from F1. The mandatory work-package dead-code rule nevertheless requires a real production consumer. Integrate it into genuinely useful maintainer diagnostics within existing work/output/custody bounds, or remove it if the ratified interface does not require it. Do not add a discarded/no-op call to satisfy grep. Keep the useful full-phase reservation API and actual cumulative semantics. The static LedgerRecordV1 TypedDict and explicitly mandated disabled RootTicketIssuer guard are separate categories, not these unused phase diagnostics.

No other actionable finding. The first eight independent installed controls pass; diagnostic-only hypotheses are disposed of in REPORT.md. Preserve all original history/UNKNOWNs, current source/evidence provenance and bounds. Full M1/Reveal/controller/original acceptance remains open and PDF/M2 gated. Independent re-review of a newly frozen implementation is required after fixes.
