# Closed CONTROL-V1 profile and finite roster

Normative R2 selection for WP104/105; source work only. This is not an issued release or executed result. Parent selected the R1 direct same-interpreter ROOT entry; CONTROL is a disjoint domain of that same canonical implementation, not the existing TEST route and not original software.

## Fixed source, data and setup

New explicitly owned source: `tests/original_control_fixture.c`, `tests/original_control_master.txt`, `tests/original_control_roster.json`, `tests/original_control_admin.py` under `internal/document/evidence/reference_controller/`. The raw master has exactly the ASCII bytes `WORDLING ROOT CONTROL V1\n`. It is never named or parsed as a WP/DOS image. Compile the C source offline with the reviewed compiler/argv; freeze actual source and ELF hashes in C/K/D before ROOT control authorization. Do not substitute a Python fake provider or modify the old harmless_fixture.c.

One reviewed `CONTROL-ADMIN-104` or `CONTROL-ADMIN-105` ROOT row preprovisions only its enumerated disposable groups. Root is `/tmp/wordling-reference-CONTROL-v1/<wp104-or-wp105>/<fixed-group>`; the literal wp104/wp105 component and finite group names are frozen source-owned values recorded in the roster, not leaf arguments or a hash-derived self-reference. Each group has `issuer/`, `ledgers/`, `shared/session1.lock`, `sources/control-master.bin`, `tools/control-fixture`, `observations/` and a fresh per-row P-workspace basename. Directories are owned 0700, the pre-existing guard is owned single-link 0600, and source/tool copies have fixed source-declared modes/hashes. Administration performs no launch and has no ORIGINAL path or tool option. It is a separate deliberate ROOT action; an invalid/expired leaf does not provision anything.

Fault groups are finite and disjoint before the campaign. A group left unresolved cannot be used again with a new grant ID. Independent groups test independent cases; they are not an automatic retry or a mechanism available to ORIGINAL. ORIGINAL always uses its actual fixed shared `session1.lock` and persistent original issuer store across actual leaves.

## Exact process and helper roles

All roles use the same captured real ExecutableLease for the fixed compiled CONTROL ELF:

```text
mutate <ResourceArgument(working)>                  # append PREPARED to same inode
serve <ResourceArgument(working)> qmp.sock <scenario-from-closed-roster>
derive <ResourceArgument(sealed)> <OutputArgument(0)> <OutputArgument(1)>
       <OutputArgument(2)> <scenario-from-closed-roster>
```

No shell, arbitrary argv/cwd/env/tool/path, daemonization or extra foreground is accepted. The fixture is an actual source-owned C process. `serve` creates a real Unix QMP peer; it supports only capabilities, query-status, the fixed4000 `pmemsave` observation, source-fixed input transitions and quit. It writes exactly4000 authored bytes into the already-created E observation slot, with the same truncate/write/ack ordering required by the original route. It never uses a private image or QEMU. Initial text is CONTROL READY. The fixed finite input transition (the reviewed CONTROL stop chord) produces CONTROL STOP READY. Quit returns a genuine empty success reply, appends STOPPED to the actual working bytes and exits zero. It does not claim WordPerfect readiness or normal DOS.

`derive` runs after genuine finish/snapshot/seal through the SAME P Session/worker. It copies the actual sealed raw CONTROL payload into `export.bin`, creates `empty.bin` and leaves `absent.bin` genuinely absent. Use real OutputSpec/OutputArgument/ResourceArgument values and JobBudget; no fabricated output observation or DerivedArtifactLease. Publication reads genuine sequential chunks, including exact EOF/empty/absence semantics and full byte/hash/readback/fsync checks. CONTROL expected bytes are independently known master+PREPARED+STOPPED; no native producer qualification is implied.

Shared lifecycle is exact:

```text
ROOT direct coordinate_one -> SAME RootTicketIssuer -> durable unresolved hold
-> registered one-use grant -> SAME retained pre-existing guard routine/account
-> ONE P open_session -> capture/prepare/tool -> mutate.successor
-> launch(resources=(working,)) -> retained ProcessLease.verify_current
-> SAME authenticated bounded peer/QMP/retained-slot protocol
-> domain-specific ordered stage+quit facts -> retained ProcessLease.finish
-> snapshot.successor -> seal_stopped -> SAME-worker derive_readonly
-> real read_chunk -> SAME retained publisher -> discharge/guard/audit order
```

WP104's ownership-only positive stops at verified OWNED_UNREADY, then deliberately contains/closes. Its successful assertion is creation/ownership and honest unresolved quarantine, not normal stop/export/discharge. WP105's complete positives traverse the entire chain. Existing P supports both; no P live WorkingLease read is used. The E observation slot is outside the P workspace with its own retained safe parent/FD and accounting.

## Closed control roster

`original_control_roster.json` must enumerate only these named control families and the exact listed variants, each with a unique immutable row/grant ID, profile=CONTROL-V1, domain=CONTROL, fixed group, case, repetition, plan/candidate digest and smaller budgets. A parameterized variant is a real counted case. No regex/subset/unknown scenario, additional repetition, custom path or `--domain/--root/--test` worker promotion exists. Exact executable/data digests are measured at implementation freeze, not invented in this proposal; an unpinned row is unreleasable.

| WP104 family | Closed variants |
|---|---|
| C104-OWNED | verified creation then deliberate containment; second ID blocked by its unresolved hold |
| C104-NOAUTH | missing grant; raw data; foreign object; genuine TestGrant |
| C104-BINDING | wrong domain; profile; source; plan; candidate; case; context; repetition |
| C104-SPENT | replay; durable-marker reply loss; handoff loss |
| C104-GUARD | pre-existing contention; retained inode/link replacement; missing guard |
| C104-ROOT | dirty/existing workspace; expired decision; attempted daemonized/arbitrary command |
| C104-LOSS | coordinator death then different ID; actual source/identity loss; postblocking expiry |

| WP105 family | Closed variants |
|---|---|
| C105-FULL | full clean CONTROL chain, repetitions1 and2 under distinct fresh rows |
| C105-PEER | foreign peer; inherited peer; wrong generation |
| C105-GREETING | false TEST token; partial/oversize input; late completion |
| C105-SLOT | wrong size; retarget; forbidden path/address |
| C105-STOP | before control witness; failed quit reply; nonzero/signal; copied stop facts |
| C105-EXPORT | live attempt; stale successor; wrong helper; helper failure/master change |
| C105-OUTPUT | required missing; empty versus absent; changed/truncated/reordered bytes; write/fsync/readback failure |
| C105-LOSS | source/identity/deadline loss after blocking call; coordinator loss at stop/export/release; exhausted budget |

Source/task review freezes the exact expansion and real cost schedule before effects. Keep <=28 public OS controls and <=64 total cases per WP, counting all variants; schema-only cases do not replace OS evidence. Every row also intersects the remaining <=300s campaign deadline and earlier leaf clocks. If the finite schedule cannot fit, propose a reviewed finite extension or split before running; never silently remove a variant, auto-retry or call an unrun case passed.

CONTROL reports permanently retain `domain=CONTROL`, `profile=CONTROL-V1`, original_qualification=false and actual control stage names. ORIGINAL rejects CONTROL source/profile/grants/stage witnesses/guard/store/helper resources, and CONTROL rejects ORIGINAL ones before the mismatched effect. Changing a public data field cannot change the source-owned profile or registered grant binding. TEST remains its existing separate type/namespace path.

## Authorization order

Review/freeze CONTROL source, compiled candidate, deployment and this finite roster first. ROOT then actually invokes `coordinate_one` for one accepted CONTROL administration or leaf row, recording a fresh deliberate decision; ordinary leaf tests do not mint it. After controls, independent review covers source and real receipts. Only later WP101's exact ORIGINAL closure/roster is reviewed, followed by separate ROOT ORIGINAL invocations for WP102. No release is present in this document.
