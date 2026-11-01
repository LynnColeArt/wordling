# WP58 frozen component contract — revision 1

Audience: independent component reviewers and future reference-controller authors.
Frozen before positive fixture runs. This is a Linux-only generic test transport;
no original resource, guest, format, grant or protocol is interpreted.

Public immutable types: Limits, ArtifactSpec, CommandSpec, EndpointSpec, Identity,
Result. Public operations: ArtifactSpec.capture/verify, Attempt.copy/snapshot,
Attempt.run, Attempt.publish, decode_json. Attempt owns a sticky first failure and
an append-only bounded journal. A failed attempt never executes another action.
Callbacks are explicit CommandSpec subprocesses (before_spawn and after_identity),
not arbitrary trusted in-process Python callables. They use the same supervisor,
caps and serial aggregate budget. Callback output is diagnostic, never authority.

All paths are explicit. Inputs are regular files opened O_NOFOLLOW; ancestor
symlinks, hardlinks, field/identity/content swaps refuse. Destination directory is
pinned at Attempt creation; only single basenames and no-clobber publication are
supported. Publication uses private O_EXCL temporary + fsync + no-replace link;
prior output is never replaced. A failure after link is explicitly partial,
never reported durable. No overwrite or hostile shared-directory guarantee.

Default ceilings: ordinary command15s; readiness60s (still bounded by command
lifetime); stdout/stderr each1MiB; aggregate16MiB; address-space256MiB, sampled
session aggregate RSS256MiB; session processes8; serial commands16; polling10ms;
TERM grace200ms then KILL; cleanup1s; source/file8MiB each; total copied16MiB;
files32; journal256events/256KiB; JSON64KiB/depth16/nodes2048; argv/env each16KiB,
argv128items/env64items; TEST request/reply4096B. Lower limits may be supplied,
never greater limits. No compiler exception. Test fixtures use much lower limits.
OS polling is sampled, not a hostile sandbox or zero transient-overrun promise.

The process leader is forked into a new session. Its PID is retained unreaped
until same-session cleanup; waitid WNOWAIT does not release that ownership pin.
Signals target only that anchored session group. Group cleanup does not prove an
escaped daemon absent: daemon state remains UNKNOWN. The public API admits only
foreground leader endpoints, never adopts a supplied pidfile as launch authority.
It returns actual charged/spawned/identity/readiness/cleanup observations, not a
false zero on exceptions. Kernel PID/startticks/exe/argv and tool source are checked
before readiness and SO_PEERCRED before any TEST bytes on every connection.
Readiness and both callbacks have finite execution/output limits. Endpoints are
never unlinked. Missing/malformed/reused daemon identities refuse/remain UNKNOWN.

Closed CLI: `python -B scripts/reference/startup_transport.py fixture CASE` where
CASE is success, nonzero, stdout, stderr, hang, orphan, observer-fail, readiness.
It creates disposable files/processes in its own TemporaryDirectory only, uses
owned authored fixture source and TEST sockets, emits bounded JSON, and accepts
no recipe/path/argv/profile/grant. API callers supply lawful explicit specs.

Frozen falsifiers: source swaps/aliases, prior destination and failed persistence;
stdout/stderr/aggregate/deadline/RSS/process count; leader-exited open-pipe child;
observer/pre-spawn and post-identity failure; foreign socket zero-command; legitimate
TEST exchange; stale/malformed/unknown identity and callback assertions; atomic
prior preservation, malformed/deep JSON, actual CLI roster and semantic mutants.
Legacy macro_session/guest/qmp and all five fresh_start caller files stay byte-exact.
Future E directly composes the new API only after independent approval; it retains
all original resource, protocol, accounting, stop/export and ROOT-grant duties.
Full M1 and all38/91/36/nested obligations remain open; M2 remains gated.

## Final API details frozen before acceptance

`ArtifactSpec(path,size,sha256,identity)` is normally produced with `capture(path,
limit=8388608)`; `verify(limit)` returns owned bytes. CommandSpec(tool,argv,cwd,
env=(),sources=(),input_bytes=b'') captures a private immutable cwd identity at
construction. All tuple/bytes fields are immutable. `EndpointSpec(path,request,
reply)` bounds each message4096B. `Identity.observe(pid)` observes facts only;
no supplied identity or pidfile is accepted as Attempt launch authority.
`Result` is frozen; bytes and nested Identity have no mutable backing aliases.
`Failure.code/result` retain diagnostics, not an authority handle.

`Attempt(directory,Limits())` pins a secure descriptor-walked directory and creates
`attempt.jsonl` O_EXCL. Every journal event is fsynced before its observation can
permit the next effect; the journal inode/path are checked. `copy(source,name)`
returns captured destination ArtifactSpec; `snapshot(tuple)` returns path/hash
pairs; `publish(name,plain_json)` validates before serialization and never replaces.
`run(command,before_spawn=None,readiness=None,after_identity=None)` returns Result
or Failure carrying partial Result after a possible fork. Both hooks are immutable
CommandSpecs, run by the same supervisor; stdin contains bounded copied phase and
invocation/actual identity facts. Hook output cannot mint any authority.

Linux main-thread/single-Python-thread launch only: fork/exec requires this explicit
precondition and refuses a threaded launch before spawning. RLock also rejects
concurrent actions. At most one main command plus one after-identity hook is live;
all active sessions share sampled RSS/process/output aggregate and absolute parent
deadline. Hooks do not recursively install hooks. This is bounded component
concurrency, not independently parallel command execution. Each readiness read
rechecks identity and remaining absolute time. Kernel buffers are finite; stream
caps bound retained diagnostic bytes, and overflow is sticky even if eventual0.
Draining is at most two64KiB reads/stream/10ms iteration; no throughput SLO.

Session ownership is anchored by the unreaped fork child; each member is signalled
through pidfd only after rechecking its same-session membership. Zombies are not
running processes; wait4 reaps the direct leader only. The component does not become
a global subreaper or prove escaped children reaped/gone. `daemon_state=UNKNOWN`
is deliberate even on an otherwise successful foreground TEST command. An escaped
child/pidfile never grants adopt/signal/readiness authority. Filesystem syscalls,
proc sampling and interpreter scheduling are subject to host latency; no hard
real-time or hostile-kernel sandbox guarantee is claimed.
