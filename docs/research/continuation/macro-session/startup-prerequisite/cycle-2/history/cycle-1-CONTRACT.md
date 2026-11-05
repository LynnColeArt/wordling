# Generic startup family v1

This Linux reference-harness component operates on authored TEST files and
processes. It supplies no WordPerfect, QEMU, DOS, native-file, original-stop or
export authority. Actual private resource fit remains unknown. Original sessions
require their separate reviewed controller, source/prelaunch checks and a fresh
exact ROOT grant.

The compatibility entry is scripts/reference/startup_transport.py. Its old
ArtifactSpec, CommandSpec, Attempt, Limits, Failure, Identity and Result come from
one source-bound package. Existing 8MiB file, 16MiB preparation and 15-second
synchronous defaults remain unchanged. The old eight fixture commands and 62
public tests exercise the extracted implementation.

The new entry is open_session(NewWorkspace, StreamPolicy, ManagedPolicy). A fresh
pinned directory and private inherited pipes bind one coordinator to its actual
forked supervisor. The supervisor remains the foreground child's parent, retains
a positive pidfd and an unreaped anchor, drains streams and checks aggregate
resources, absolute clocks, immutable sources and coordinator pidfd while the
caller is idle or performs protocol IO. It has no public control socket, pidfile
adoption, callback executor, original recipe or resume path.

## Sources and callers

| Module | Responsibility and actual callers |
| --- | --- |
| engine.py | Shared identity, causal fork/exec witness, stream draining, aggregate sampling, pinned journal append and positively anchored cleanup. Both LegacyKernel and managed Worker call these primitives. |
| artifacts.py | Single old small-artifact/type authority and new streaming resource store, requests, policies and opaque handles. The compatibility adapter and managed lifetime use it. |
| lifetime.py | Retained supervisor, bounded control protocol, opaque sessions/process/channels and immutable observations. Called by public exports and managed fixture CLI. |
| __init__.py | Public exports and real old Attempt composition adapter. The facade loads this package. |
| startup_transport.py | Checked loader and old/new closed TEST fixture entrypoints. |

The loader uses its own checked source parent and standard importlib package
initialization under wordling_reference_startup_v1. It does not modify sys.path or
replace foreign modules. Same-root aliases share exact classes. Directory
identity, package version, every module origin and full source digests must agree
on cache reuse. Changed or different roots refuse. Failed first loads remove only
package entries that initialization created.

## New policy and state

StreamPolicy.test_v1 permits 64MiB per opaque source, 256MiB declared sources and
128MiB prepared data. It uses at most 64KiB chunks and two artifact payload chunks,
32 retained resource descriptors, four mutable resources, 32 declarations, 64
workspace files, 256MiB allocated workspace, 4GiB charged source IO, 30 seconds per
preparation/mutation operation and 60 seconds prelaunch preparation. It returns
digests and observations, never a large-file bytes object. Old verify caps remain.

ManagedPolicy.test_v1 selects 120 seconds total child lifetime, explicitly bounded
to 900 seconds; tests select 2–3 seconds. Startup is at most 15 seconds, readiness
at most 60 seconds from ownership and the remaining lifetime. Session lifetime is
at most 960 seconds. Fixed limits include 16 OS commands, 1MiB per stream/16MiB
aggregate output, eight processes and 256MiB sampled RSS including coordinator,
supervisor, child and observed owned descendants. Worker/child address space is
256MiB, core size zero and descriptors 64. Coordinator-global rlimits are unchanged.

Other caps are control frames 64KiB, raw chunks 16KiB, JSON depth 16/nodes 2048,
argv/env 16KiB each, 4096 control messages/64MiB wire, 512 journal events/1MiB,
endpoint requests/replies 4096 bytes each, and client buffers below 2MiB. Monitor
polls request 10ms intervals with 100,000 polls per session. Cleanup uses positively
anchored TERM, then KILL and direct reap within bounded waits. These are engineering
ceilings and sampled observations. Kernel, filesystem and scheduling latency is
host-dependent: this is no hostile sandbox, hard real-time guarantee or DOS SLO.

Sources require known size/hash, absolute non-symlink paths, regular files and
nlink 1. Tools additionally require executable mode and no setuid/setgid bits.
Prepared resources publish without replacement and retain owned descriptors.
In-place mutation has truthful partial effects: failure makes the resource
UNUSABLE and raises a sticky failure, without rollback or requalification.

The ratified successor clarification preserves method signatures. A committed
mutation returns MutationResult.successor for the exact next epoch. A READY
snapshot returns the identical input handle/epoch; an eligible DIRTY_STOPPED
snapshot durably returns a fresh next-epoch successor. Old references and
ResourceArguments remain stale. Results, JSON, PIDs or hashes cannot construct a
handle. Reporting failure can follow an actual committed transition: no recovered
authority is issued and no clocks, quotas or first fault reset.

Current kernel identity and connected credentials are checked before bytes and
after waits, progress and final readiness acceptance. An exited or unverifiable
peer cannot become READY from a full reply. Passive finish sends no protocol or
signals and observes direct exit/reap. Daemon state stays UNKNOWN: owned-session
facts do not prove absence of unseen escapes. The later original controller must
separately join approved peer/opaque normal-quit contracts at each IO boundary.

## Verification

The final directory holds actual outputs, refusal codes, measurements and JUnit.
Development retains raw failures, initial probe/syntax errors, weak-probe survivors
and invalid mutant construction; they are not passing results. Custody binds old
inventory, actual frozen inputs and unchanged Go/modules. The root seal includes
every owned source/evidence member and nested seals, excluding only itself.

Public tests use real 64MiB data, a valid padded public Python ELF larger than
8MiB, full copy equality, old-default refusal, source changes, quotas, no-clobber,
stale/forked/forged handles, successor composition, actual nonzero/FSIZE short
writes, inode/journal replacement, process/stream pressure, absolute clocks,
same-PID exec/reply/exit, zero-byte foreign-peer refusal, coordinator/worker death
and import collisions/partial initialization. Generated payloads are disposable.

Full M1 remains open. WP61 accessed no original guest/private resource, changed no
document format, and grants no original-controller readiness. M2/PDF remains gated.
