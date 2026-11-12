# WP58 independent cycle1 — changes requested

## I1 — P2: enforce active-session and readiness limits during readiness progress

Source: scripts/reference/startup_transport.py:357–366 and:682–688, particularly synchronous `_exchange(readiness, identity, deadline)` at:687.

The readiness reply loop bypasses `_monitor` and gets only the command deadline. A valid same-owned TEST peer can keep delivering reply bytes while its same-session workload exceeds selected process/RSS limits, reap the excess before final reply, and receive a successful Result. Lower `readiness_seconds` is also checked only before entry rather than throughout the exchange.

Independent actual PUBLIC repros (no patches/mocks/originals):
1. `readiness-adversary-v2.py`: Limits(seconds=2,processes=2), foreground peer forks2same-session children for~0.55s, streams20byte valid reply every0.04s, reaps children before finalreply. Both fresh readiness runs return success/ready:true/peak_processes:1 despite3processes. Identical no-readiness control refuses process-limit. Initial unreaped-zombie calibration is retained separately and correctly refused later; it is not the finding.
2. `readiness-deadline-adversary.py`: Limits(seconds=2,readiness_seconds=0.1), slow valid peer reply; both fresh runs return success/ready:true after~1.0s instead of enforcing selected0.1s readiness budget.

Keep readiness processing inside actual bounded supervision/cooperative monitoring, with the minimum applicable absolute readiness and enclosing command/hook deadlines checked throughout progress. Preserve positive kernel/peer/source checks, sticky first fault, partialResult and bounded owned cleanup. Add actual public OS regressions that fail current source for these exact conditions, with precise limit/deadline refusal and no next action; don't relax limits or change evidence expectations. Source/API/OS fixtures only, no original/VM needed.

Fresh47tests and8closedCLI cases pass; configured7=4PASS/3legitimate no-packageSKIP. This does not cover I1. All157owned/178sourceGit/SHA bindings remain exact. No code was changed by reviewer; allM1 remains open. Independent dossier report/raw probes/JUnit source bindings provide complete repro context.
