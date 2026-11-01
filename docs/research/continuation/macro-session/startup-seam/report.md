# WP58 cycle3 handoff — I2 readiness identity acceptance

Cycle2 resolved I1 monitoring/deadline limits, but independent review found I2P2:
a same-PID peer could exec into different kernel argv during the read wait, send a
valid reply and exit before the outer loop observed the changed identity. The old
57-test/10-mutant results remain OLD evidence, not proof of this boundary.

The narrow fix revalidates captured kernel executable/argv/startticks identity
AFTER readiness wait, AFTER receive/monitor, at final reply acceptance and before
publishing ready. The ready flag is assigned only after these checks. Changed or
unverifiable identity refuses; a full reply/source-file rehash/cache/JSON assertion
cannot replace live identity proof. I1 continuous aggregate monitoring and absolute
selected/enclosing clocks remain unchanged. No API or runtime cap changed.

Source SHA256:
603cc95307fe681d51637c08351efbbc101b98e8b3f2bc9325f8fe635ee590c9.

## Actual evidence

Exact unchanged reviewer probe against old935: delayed control identity-changed,
but TWO fast exec/full-reply/exit runs falsely succeeded. Frozen new-source probe:
delayed control refuses identity-changed, BOTH fast runs refuse unknown-identity,
all ready:false. Same PID and different kernel argv are captured before/after.
New persistent public fast tests also fail twice against old935, with raw logs.

Final62 tests PASS in18.987s: previous57/I1 cases plus five new real OS controls:
two fast exec exits, delayed exec, exec between partial/final reply, and exited
owner/inherited socket. Refusals preserve partialResult, bounded own cleanup,
no ready journal event and no next action. Eleven semantic mutants are killed;
the new collective acceptance-check mutant reproduces the actual before-wait-only
bug. No mocked ownership/receipt or private monkeypatch is used.

A development replay correctly exposed conservative identity-unverifiable refusals
in old immediate-exit positive TEST fixtures. Their raw failure is retained. Positive
fixtures now keep the SAME kernel identity for a bounded200ms after reply so the
actual final acceptance can be observed. An immediate/unverifiable exit is NOT
reclassified as success. The absent-endpoint callback-negative accepts not-ready OR
unknown-identity, while still requiring ready:false/no callback-minted authority.

Fresh8 public CLI cases retain expected2 exits0/6 intended exits1. Full argv/env/cwd,
stdout/stderr and GNU time receipts are under cycle-3/cli. Max CLI RSS37,740KiB,
max component elapsed1.558s including cleanup after the1.5s fixture command budget,
max JSON output17,976B. Logs contain varying times/PIDs/temp paths, not byte-identical
execution claims. Configured7 completed0 with4 actual passes/3 legitimate no-root-Go
package skips. Source AST/compile/whitespace checks pass. No Go/race/fuzz claim for
absent root packages or unchanged native readers; actual5 Go/module paths unchanged.

## Custody and retained limits

Current evidence is cycle-3; cycles1/2 remain history. Entire319 prior owned paths
remain immutable in935135aefdc6e067b0522daa80bf9a637c20a126; superseded source,
contract/report/pointers/seal have selective exact inert copies, and unchanged raw
artifacts remain in place. The full canonical94-file cycle2 review/feedback is
copied exactly with Git/SHA mapping. Baseline340 additionally proves18 inherited
reference/module entries and5 Go/module paths unchanged. The new root manifest
closes the ENTIRE recursive owned SET, including all nested historical seals;
only its exact own path is excluded, never a basename filter.

Cumulative metadata cap1024files/8MiB now accommodates mandatory319-history plus
94-review records and current proofs. This changes NO process/stream/artifact/
command/guest/source verification cap. Runtime limits, main-thread-only launch,
no-clobber/source guards, foreground-only lifecycle and UNKNOWN escaped-daemon
semantics stay intact. Only sampled resource guarantees apply; no hostile sandbox,
hard-real-time or universal kernel exec-audit guarantee. Identity is proved at
actual receipt boundaries; Result's immutable identity is an observation, not a
transferable live authority after process exit.

Legacy helpers/callers are unchanged/unexecuted. No E/core/Go/native/UI/storage
imports/edits, original VM/QEMU/master/program/manual/font/SET/PRS/failed-HD,
reference guard/private ledger or original protocol was accessed/run. The separate
64MiB artifact/daemon-lifetime future-consumer design gaps were NOT expanded here.
No original readiness, grant/native/app/M1 closure follows. Full38/91/36/nested M1
remains open; root owns lifecycle quietpoint and independent cycle3 review.

Full staged raw-whitespace check exits2 solely for the preserved development.log
unittest subtest line's trailing space. Source-only whitespace/AST checks exit0.
The raw failure log is retained byte-exact; no claim that all raw logs are lint-clean.
