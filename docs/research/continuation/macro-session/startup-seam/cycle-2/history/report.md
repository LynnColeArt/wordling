# WP58 implementation handoff

Audience: independent code reviewer and future E startup consumer authors.

## Result and boundary

A new generic Linux component provides immutable artifact/command/endpoint/result
specs; descriptor-walked source validation; no-clobber atomic publication; a bounded,
fsynced sticky attempt journal; and a default streaming fork/exec supervisor. The
actual closed CLI is a production consumer of this component's TEST API. It runs
project-authored disposable processes/files/Unix TEST sockets, not an original
recipe or a demonstration of an original controller. Future E integration is
separate, and no future task/ID is authored or reserved here.

The main-thread-only supervisor retains its direct fork child unreaped while
observing its session. Same-session members are checked and signalled using pidfds;
wait4 reaps the direct leader. Command-based observers/readiness hooks use the same
caps and absolute parent deadline; all active sessions are monitored, not hidden
behind an unbounded callback. Kernel executable/argv/startticks identity and
SO_PEERCRED gate every connection before any TEST bytes. A supplied pidfile,
callback JSON or observation cannot adopt a daemon. Daemon absence is always
UNKNOWN, independent of foreground success and session cleanup. Readiness means
only the declared TEST exchange, never normalDOS, safe original stop or permission.

## Actual validation

Final47 tests passed in13.723s (final-acceptance.xml/log), including the narrow
public verify-limit regression. Tests use actual public APIs/CLI and harmless OS
processes/files/socket boundaries. They cover both-stream/aggregate output caps,
deadline/TERM-ignore cancellation, process/RSS enforcement, live descendants with
open or closed pipes after leader exit, a new process group, exec identity change,
foreign endpoint zero-command behavior, legitimate readiness, callback failure
before/after spawn, callback-output authority refusal, source/cwd/journal swaps,
immutable observations, short writes and failed journal persistence after launch.
Actual KeyboardInterrupt cleanup and threaded-launch refusal are included.

Eight intended semantic mutants were killed against the final source. The initial
kernel-lifetime mutant survived because its fixture could hit the other immediate
post-hook identity check; a handshake-separated exec transition now isolates the
loop guard. The initial journal mutant removed only one half of a redundant guard;
the corrected full-guard mutant is killed. Preserve their initial raw survivors;
they are not counted as killed runs. All8 final raw mutants are retained inert.

Configured-final.xml records7 checks, zero failures/errors: inventory, scenarios,
review-adapter and actual Go package discovery passed; build/test/vet were honestly
skipped because go list ./... returned no root packages. The configured command
completed exit0. No root Go overlay, new Go source, race or unchanged-parser fuzz
claim. AST/compile and source-only whitespace checks passed. New-file no-index
Git check returns1 with no diagnostics (differences), not0; the initial audit's
wrong exit0 assertion is explicitly retained. Staged whitespace checking is
separately recorded. Raw diagnostic whitespace is not normalized.

The final8-case public CLI capture has2 success exits0 and6 intended exits1;
unknown CLI case is argparse exit2. Raw stdout/stderr, full argv/env/cwd, GNU time
receipts, kernel PID/executable facts and result limits are retained. Final maximum
CLI RSS is37,608KiB; maximum reported component elapsed1.654s includes bounded
cleanup after the fixture's1.5s command deadline; maximum JSON stdout17,972bytes.
Exact raw timestamps/PIDs/temporary paths are intentionally nondeterministic.
The semantic projection and canonical JSON publication are deterministic in shape
and content roles, not a claim of byte-identical wall-clock execution logs.

## Source and evidence custody

Source SHA256:3efb24e62008c4b2b8855c8fe40ca02b85598fc08e746edef9785314f8a40d70.
Final frozen input manifest SHA256:
4efa3c42b027f091c02b7ba46892b32315444fb1a0e16ccdb52110473c6aa411.
All18 inherited source entries are byte/Git-blob exact against the actual approved
P claim baseline558c8b715289f2c7d603b8b40bc04a56ecb69ae4. All5 tracked Go/module
paths (including isolated historical WP33 files) are exact. Seven legacy source
inventories are pinned: the first3 exist in P; four later callers are absent and
are inventoried from immutable44aab36accdf14a370a67fd73945907871ab7193 only.
They were neither copied/imported/executed nor given new bounds claims.
Runtime closure records actual direct stdlib bindings and postrun tool identity;
each actual command internally captures and verifies its explicit tool separately.

All implementation/test/evidence paths are within the3 owned namespaces. An owned
SET/size/SHA256/Git-blob manifest binds all deliverables except itself. Package
custody budget is256 files/8MiB (distinct from per-attempt file/process/output caps);
this does not enlarge command or fixture budgets. Prior raw failures remain intact.

## Limits and future handoff

This is a scoped Linux component, not a hostile-process sandbox or hard real-time
system. RSS/process sampling can observe an overrun after it happens. Address-space
limits are intrinsic per exec process; escaped sessions remain UNKNOWN and are not
claimed killed/reaped. Filesystem syscall latency is host-dependent. Actual IO
faults tested include RLIMIT_FSIZE short writes, no-replace collisions and journal
retarget/persistence failures; no physical power-loss, full-device or exotic kernel
close-fault simulation is claimed. Main-thread/single-Python-thread launch is an
explicit enforced prerequisite. New-source/rules require an independent review.

Future E must directly compose the approved generic API with its own approved
source/grant/account/peer/normal-stop/controller authority. Old fresh_start remains
unchanged and limited. This handoff supplies no native interpretation, original
readiness, acquisition, grant, safe-stop/export authority, app qualification or
full M1 closure. No subtasks/status/verdict/primary push is performed by this source
commit; root must grant a lifecycle quietpoint and another agent must review.
