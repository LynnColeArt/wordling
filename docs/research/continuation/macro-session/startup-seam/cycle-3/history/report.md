# WP58 cycle2 handoff — I1 readiness supervision correction

The first version violated its declared readiness supervision and selected clock.
Independent cycle1 requested changes (I1P2). This source fixes that finding only;
its older47-test/8-CLI/8-mutant evidence remains historical and is not relabeled.

Readiness connect/write/read now use nonblocking10ms selector waits with the SAME
internal active-session supervisor before/after progress. The selected readiness
absolute clock is bounded by the enclosing command/hook clock, checked throughout,
and never reset by incoming bytes. The winning clock has a precise refusal code.
Kernel identity, peer credentials before any TEST byte, source guards, sticky first
fault, partialResult and owned bounded cleanup remain. Actual violating RSS/process
samples are retained in Result before failure. No public API or execution cap changed.

Current source SHA256:
ea4095a3419ea94ea8943a4f50ce785982847df00496ce9efcbfdb184965150b.

## Actual red and green

Unchanged independent review probes were run from disposable copies, never overwriting
the review's sealed evidence. Old source reproduced2 false readiness successes at
actual3processes under limit2, and2 false successes near1.03s under a0.1s readiness
budget. The exact new persistent public tests also failed twice against old source.
All raw outputs/source hashes remain in cycle-2/red and historical reviewer records.

Final frozen-source probes: control plus2 readiness runs refuse process-limit with
actual peak3 retained, ready:false, before peer reaping. Both0.1s readiness runs
refuse readiness-deadline at0.149/0.147s including cleanup. Final57 public tests pass
in16.626s: old47 plus10 actual readiness process/RSS/stream/aggregate/deadline,
parent-clock/cancel/short-reply/positive-progress cases. A development check exposed
a deadline-label race, corrected before freezing; its failed raw log is preserved.

Ten final semantic mutants are killed, including removing readiness monitoring and
restoring parent-deadline-only behavior. Existing8 mutants are replayed against this
source. Configured7 has4 executed passes/3 legitimate no-root-Go-package skips and
exit0. No new Go module/helper, race or unchanged parser fuzz claim. Source AST/
compile and source-only whitespace checks pass; full raw staged checks are separate.

All8 fresh closed CLI cases have expected exits: success/readiness0, six negatives1.
Raw stdout/stderr/argv/env/cwd/RSS receipts are current under cycle-2/cli. Max CLI
RSS37,808KiB; max component elapsed1.586s includes cleanup after its1.5s fixture
command deadline; max JSON output17,976bytes. Raw times/PIDs/temporary paths are
nondeterministic. Canonical publication/semantic roles do not imply byte-identical
execution logs or hard real-time enforcement.

## Custody and preserved boundaries

The prior178-path Git/source baseline is inventoried in cycle-2/baseline178.json.
All18 inherited reference/module entries and all5 tracked Go/module paths remain
exact. Only owned component/test/current-pointer source changes. All old157
owned files remain in immutable22e27ab671fbac19aecac32c39cd8d288685151d; superseded
source/pointers/seal have selective exact inert copies, and all unchanged old raw
history stays in place. The complete48-file canonical cycle1 review is copied
byte-exact with source/Git mapping, executable-source suffixes inert. Nested old
seals are INCLUDED in the new manifest; only the exact current root manifest path
is excluded. No basename filtering. New package metadata bound512files/8MiB covers
mandatory cumulative history; prior256-file bound remains historical. This is not
an enlargement of any runtime/file/process/output/command/guest budget.

Legacy macro_session/guest/qmp and callers are unchanged/unexecuted; absent callers
remain immutable Git inventory only. New code imports stdlib only, no E/private
helpers. No original/QEMU/VM/guard/ledger/master/program/manual/SET/PRS/fonts/failed
HD or original software was read/run. No original stop/export/grant/native/app
qualification or fullM1 closure follows. Full38/91/36/nested scope stays open.

Limits remain explicit: sampled RSS/process counts are not a hostile sandbox;
filesystem/kernel scheduling latency is not hard real-time. Only the anchored
session is signalled; escaped daemon state stays UNKNOWN, never adopted from a
pidfile. Main-thread/single-Python-thread launch is still enforced. Independent
cycle2 review is required; root owns lifecycle quietpoint/primary publication.
