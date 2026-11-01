# Cycle 2 — I3 response-publication correction

Independent review found a real monitoring gap in cycle 1. The pristine exact
2c0dec source reproduces it: with legal 12,000-byte argv padding and only the
causally owned anonymous pipes resized to 4096B, 21 observed excess-process samples
are missed, a lease/finish is accepted, first_fault is None and peak is 3 despite
five live processes under selected four. The zero-padding and 64KiB controls
already refused correctly; these are retained as controls, not reproductions.

Only lifetime.py production code changes. Its private provisional/atomic-commit
response protocol keeps full supervision and minimum selected absolute clocks
running while a client stops draining. Partial or full provisional payloads are
not authority. Failure after any queued prefix contains and invalidates the
generation instead of concatenating an error frame. Client ControlLost/UNKNOWN
does not fabricate a typed server cause or safe cleanup. Actual durable first
fault and owned kernel observations are retained.

The exact independent source probe is copied unchanged into a disposable output
directory for old RED and new GREEN. On final current code both 4KiB cases refuse
without a ProcessLease or finish; durable server ProcessLimit remains. Both
64KiB controls still observe the earlier valid launch and later ProcessLimit.
Three same-PID exec full/partial refusals and the passive-exit/stopped-snapshot
positive control also pass. Raw scripts are archived inert, with exact source
hashes and outputs; they were not edited to manufacture the result.

Final public verification: 57 new tests pass (44 original/clock cases plus 13
publication cases), 62 unchanged old cases pass, all 23 CLI cases match expected
exits, and 31 actual-source compile/import-valid mutants are killed. Configured
checks report four passes/three legitimate Go skips/zero failures. The lawful
9,135,040B executable and 64MiB streamed fixtures still pass. No source/API/type/
import/successor or old-default waiver is used.

The 13 real-OS cases inspect only the two positively owned coordinator pipes,
use kernel resize/FIONREAD and nondestructive tee header observation, and exercise
partial and fully queued provisional responses, process/stream/96MiB RSS pressure,
lower lifetime/startup/readiness clocks, live identity/source change, parent loss,
small/default-pipe controls and fault-free legal backpressure. Actual per-case
JSON includes queue/frame sizes, journal first faults, stopped direct children
and no accepted later action after failure.

One existing .1-second OWNED readiness test now accepts its exact typed
ReadinessDeadline at endpoint publication or exchange, since the same absolute
clock correctly covers both. No phase is extended or reset. A separate .1-second
progressing exchange under an ample overall phase pins the IO deadline. Raw
earlier-boundary failures and the root's explicit review steering are not hidden.

Development first tests exposed lost typed diagnostics after an already committed
future fault, and a mislabeled minimum lifetime/startup crossing. Those were
corrected, with raw reds preserved. Two clock mutants survived because the new
publication deadline correctly supplied another defense; corrected composite
mutants remove both actual defenses. A duplicate needle was corrected to the
precise monitor guard. The premature-authority mutant preserves HELLO/setup and
bypasses commit only for launch, so the final queued-response falsifier reaches
the actual bad authority boundary.

The prior 645-path owned tree, including its root seal, remain in immutable source2c0dec.
Exact archived originals of amended files, root manifest and report are included
once under history. Old baseline/custody hashes remain checked; no private or
original resource, VM, QEMU or new grant was used. Full M1 remains open.
