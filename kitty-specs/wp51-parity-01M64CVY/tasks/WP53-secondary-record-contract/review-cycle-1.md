---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-10-31T18:27:45Z'
reviewer_agent: codex
wp_id: WP53
---

# WP53 independent review cycle 1 — changes requested

## R1 — P2: terminate owned descendants when the immediate helper has already exited

In `scripts/reference/secondary_record_contract.py:114–119`, exception cleanup is conditional on `process.poll() is None`. This only proves the immediate process is still running; its already-created process group may retain live descendants after that process exits. `bounded` is the actual production wrapper for Git/Go build/test/inspection commands and promises capped sequential subprocess lifetime/cancellation with no orphan.

The sealed independent `probe_orphan.py` invokes the real `bounded` entry with an isolated parent that spawns a child inheriting stdout/stderr, then exits0. At timeout0.3s the wrapper raises `HelperTimeout` but skips group cleanup because the parent has exited. The actual child is still sleeping (`/proc` state S), in the owned group whose PGID equals the captured start_new_session parent PID. `orphan-result.json` captures exact argv, parent exit0, descendant PID/group/start-state and timeout. The review harness then terminates ONLY this isolated test-owned group. No reference VM/guest or other host process is involved.

Repair owned-group cleanup so a leader's exit does not make a live descendant group escape timeout/output/exception cancellation. Keep cleanup bounded and scoped to the private process group started by this call; handle already-gone groups and retain safe parent reap semantics. Do not broaden process killing or change native/source authority. Add a real process regression with the parent exiting before timeout while its child retains a pipe; assert the descendant cannot remain running after refusal. Also cover a descendant that ignores graceful termination so parent exit/wait success cannot skip bounded escalation. Existing immediate-parent timeout, output cap, failure and prior-report preservation controls must remain effective.

Preserve this frozen source/review/raw failure evidence as history, fix only owned checker/tests/evidence, rerun impacted meaningful tests/CLI/helper/configured checks and reseal exact successor authority. No native admission/interpreter/output or new original permission is requested. No full parser fuzz or VM is necessary for this bounded subprocess correction.
