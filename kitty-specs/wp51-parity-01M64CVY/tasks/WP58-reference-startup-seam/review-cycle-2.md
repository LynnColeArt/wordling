---
affected_files: []
cycle_number: 2
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-01T03:41:24Z'
reviewer_agent: codex
wp_id: WP58
---

# WP58 independent cycle2 — changes requested

## I1 resolved

Original cycle1 public process3vs2 and readiness0.1vs2 repros independently OLDRED/NEWGREEN, twice each; new refusals retain peak3/readiness-deadline.57fresh tests/10fresh mutants/8closedCLI/configured4PASS3legitSKIP pass. Preserve that fix and all old raw evidence.

## I2 — P2: revalidate kernel identity after readiness wait before accepting reply

At startup_transport.py:399–412, owner.verify is before wait_for(EVENT_READ), not after wait/recv or before success. The internal checkpoint monitors resources/deadlines but not the bound kernel argv/executable. If peer execs during that wait and exits immediately after its valid reply, the next outer iteration sees an exited leader and skips Identity.observe, accepting stale captured identity.

Actual PUBLIC API counterexample readiness-exec-adversary.py: foreground owned TEST peer receives TEST ping, sleeps0.15s, execv's second immutable declared script with DIFFERENT kernel argv/samePID, then sends exact20byte reply and exits0. Both fast-exit runs returnSUCCESS/ready:true with old main.py Identity.argv while raw after-exec.json has after.py cmdline. Identical0.3s post-reply delay control correctly refusesidentity-changed. No mocks/patches/forged results/originals, no source bytes changed.

Keep source-bound identity valid at readiness receipt boundaries after wait/progress and before ready/success. Changed/unprovable peer must fail closed with precise identity refusal/UNKNOWN and retained partialResult/cleanup, never rely solely on a later live outer check or source-file rehash. Add actual public fast-exec-exit and delayed controls, preserve legitimate readiness/foreign0commands/allI1 limits/sticky/cleanup and all source/native/oldhelper invariants. No contract waiver, original/VM, E/controller/private helper or reviewer fix is authorized.

Independent dossier captures all319/318sealed source bindings, old157history/canonicalreview48/old18+5Go unchanged, rawprobes, source and command hashes. One open P2 only; fullM1 remains open.
