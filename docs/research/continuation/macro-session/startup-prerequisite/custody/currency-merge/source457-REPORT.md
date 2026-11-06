# WP61 implementation verification

The shared startup family implements the new generic TEST resource/lifetime
contract and preserves the old small synchronous API. Implementation is ready
for source-currency resolution and independent review, not approval. No lifecycle
mark/move, original session, private resource access, acceptance or merge was run
by this implementation agent.

## Actual final checks

| Check | Actual result |
| --- | --- |
| New public OS/API tests | 43 passed, whole exit 0, 14.671s |
| Unchanged old public OS/API tests | 62 passed, whole exit 0, 20.463s |
| Original closed fixture CLI | 8 cases: 2 success/6 expected refusal, stderr empty |
| New closed managed fixture CLI | 15 cases: 3 success/12 expected refusal, stderr empty |
| Actual-source semantic mutants | 28 compile/import-valid candidates killed |
| Large public TEST executable | 9,135,040B: direct control 0, old default refused, new lease launch/passive exit 0 |
| Large executable changed after capture | SourceChanged before any foreground launch |
| Authored opaque data | Full 67,108,864B capture/copy/snapshot and streaming equality |
| Configured review adapter | 7 entries, 4 passed, 3 legitimate skips, zero failures/errors |
| Source AST/compile/whitespace | Exit 0; broad exact owned cached diff also 0, zero raw notices |
| Public-component JUnit | 157 projections of actual 43+62+23+28+1 executions, zero failures |

Configured Go discovery finds no root Go packages in this P checkout. The three
Go build/test/vet entries are legitimate skips, not seven passing checks. Its
historical nested WP33 module is excluded by root Go discovery; all five actual
Go/module inputs are unchanged. No new Go code, overlay or unrelated long fuzz
run was used.

The measured large-tool sample has coordinator/supervisor/foreground descriptor
counts 7/14/4.
Its combined sampled peak RSS is 55,984,128B.
The 64MiB path charged 402,653,184B source IO,
prepared exactly 67,108,864B and observed a maximum 65,536B artifact chunk.
These are this host's bounded TEST observations, not emulator/DOS fit or SLOs.
No generated executable or large file payload is committed.

## Fidelity and adversarial evidence

The live old Attempt composition and new private supervisor call shared engine
fork/exec-witness, identity, stream, aggregate-sampling, journal and cleanup
primitives. The facade, package exports and public CLI actually call every new
module. Source-bound aliases share exact classes without sys.path changes.
Different roots, changed caches, partial loads and concurrent initialization have
actual public tests.

The ratified successor contract is implemented without changing method return
types: successful mutations issue fresh epoch handles, READY snapshots preserve
their exact input handle, and eligible stopped snapshots issue the next epoch.
Old handles/ResourceArguments, fake facts, forked clients and stale results do not
reissue authority. Real nonzero, FSIZE short writes, inode and journal replacement
retain partial owned bytes, sticky faults and UNUSABLE diagnostic results with
successor None. No rollback or failed-resource recovery is provided.

The worker continues supervising during control handoff and IO. Actual tests
exercise process/output pressure, absolute clocks, same-PID exec/full-reply/exit,
passive direct reap, TERM-ignoring child containment after coordinator death,
worker death with UNKNOWN cleanup and foreign endpoints receiving zero bytes.
UNKNOWN launch/cleanup is never normalized to zero or native-safe stop.

Development receipts preserve two real weak-probe mutant survivors, an invalid
mutant needle, initial syntax/JSON/probe mistakes, conservative exit-race and
parent-loss classification failures. They are historical negatives, not final
passes. Strengthened public probes kill the same two surviving faults. The final
28 candidates include all 11 old source falsifiers against their real extracted
locations, composite parent-deadman and cached-READY authority faults, and new
source/stream/atomic/epoch/successor/quota/clock/monitor/foreign-peer guards.

## Source custody and current blocker

Claim baseline is c889de4882377f3bb410b7edca6708b0fd2143c5.
Of 2,402 baseline reference/evidence/Go/module paths, 2,401 remain exact. The only
amendment is the explicitly owned startup_transport.py facade. Of the approved
P58 511-member source/evidence set, 510 unamended members remain exact; the
original facade remains available in immutable approved Git history. Old tests,
reports, contracts, results, seals and all legacy callers are unchanged.

The final eight production/test/probe files match their frozen SHA-256 closure.
The root recursive evidence seal includes all nested seals and excludes only its
own exact path, with actual Git blob identities and finite metadata budgets.

Installed source currency at exact primary
79839335b9bf4d6a1607d717ef5d5ef4bdff4525 is BLOCKED: 20 behind, 60 paths outside
the installed planning/status prefixes. Full exact callback/path/commit receipts
are retained. No merge/rebase/force/host repair was performed. ROOT must resolve
this real normal workflow gate against a clean exact target before lifecycle
advancement; this report does not claim a None result.

Full M1 remains open: all 38 obligations, 91 groups, 36 lessons and nested leaves.
The component grants no original controller, prelaunch readiness, ROOT grant,
normal DOS/quit/export authority or native editing capability. M2/PDF is gated.
