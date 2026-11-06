# Prelaunch stop/extraction correction; no WP43 guest run

Root's review of1da9fd94 found two orchestration flaws: missing PID could satisfy
an OR termination condition and extract, and failed mcopy entries could retain
complete-observation and permit repetition2. That source and final-preflight.json
remain immutable historical preparation at1da9fd94; their passing earlier controls
did not cover these actual run failure paths. preflight-stop-fix.json supplies the
new readiness snapshot. The five first-save/F1 recipes are unchanged and unrun.

The owned run now durably counts a pending incomplete attempt before launch and
never declares completion in the original-app try block. Live process capture
requires a positive PID, matching private boot/disk and unique QMP argv, and its
start ticks. Only verified captured-process gone/zombie plus absent owned socket
can set guest_stopped. Missing/unowned process proof never authorizes stop or
extraction; it does not create termination facts. A source-proven failure before
returning the launch argv is separately no-start, with no guest_stopped claim.
An unresolved guest keeps oracle-safe-release false even though the process-local
shared guard is released; no subsequent case/guest is allowed automatically.

Stop, extraction and metadata failures are retained as separate errors without
overwriting the original failure. Raw failed-copy stdout/stderr or invocation/
exception records remain, including partial successful outputs. Failed stop
skips extraction; every extraction requires the captured stop proof and stays
inside the actual shared guard. Required outputs come from the exact declared
case, not a passed boolean or a shortened exports list. Each must have exit0,
nonempty actual file, exact size and SHA; required canceled-name absence (or
whole unchanged directory for empty cancel) is checked. Per-attempt immutable
master hashes are recorded and compared after guarded extraction before either
completion or the next fresh_start. Normal captured DOS exit alone cannot mark
a guest complete. The final pair can complete only if both entire attempts do.

The actual run/attempt code is exercised offline through a simulated helper
boundary, explicitly not original evidence. Controls cover missing and unowned
PID, real missing/unrelated-PID capture refusal, stop exception, nonzero copy,
missing declaration, successful exit without output, zero output, post-copy
size/hash substitution, canceled-name presence, copy exception, master mismatch,
prelaunch/no-start and the hard10 cap. Every injected incomplete path retains a
manifest/master/error, launches exactly one simulated fresh_start, performs only
proved guarded extraction or explicitly skips it, and rejects a later case.
The positive simulation reaches exactly two complete attempts. Actual PID capture
of an unrelated live process refuses without signaling it. No original helper,
42 code, source contract, global runtime, VM, primary or lifecycle is modified.
