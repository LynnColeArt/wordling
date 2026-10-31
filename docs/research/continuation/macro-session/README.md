# WP38 original macro session reference observations

Current evidence authority: [HANDOFF.md](HANDOFF.md), [audit.json](audit.json) and
[audit.xml](audit.xml). Thirty fresh guests were stopped and their raw outputs
retained. Nine selected two-repetition recipes provide bounded original-only
observations; they do not test Wordling, close a parent case or accept M1.
The oracle has been released; no new guest is authorized by these files.

The offline `plan` command intentionally emits an **unexecuted recipe template**.
It is not the current run ledger. `check` validates source inputs without starting a
guest; its zero executed-runs field describes that invocation only. Consult the
sealed per-run reports and current audit for actual executions.

The following preparation text is retained as a historical account of commit
4003ce9 and its then-unexecuted plan. Its present-tense VM hold and not-run labels
apply to preparation, not the subsequent authorized experiments below.

---

# WP38 macro session experiments — OFFLINE PREPARATION ONLY

Audience: root's original-VM scheduler, independent researcher/reviewer and future
WP36/37 consumers. No original guest has been launched for this package. T113/T114
are not completed, no Wordling behavior was tested, and no macro/FR/M1 parent closes.

The preparation was authored under researcher-robbie. Approved inputs are WP09's
original-only automation contract, WP11's session contract, and WP32 source
4eb851eac3096d27d4743616ce3ae74f7a9edc05 with independent review754bdcc. Exact source
hashes and the actual pre-mission helper APIs are retained in preparation.json.
No WP23-owned implementation or post-mission session helper is imported. The
existing qmp/guest/smoke/extended/advanced/history modules are hash-pinned, read
without executing them during offline check, and imported only after authorization.

## Explicit VM hold

**WP23 owns the original VM. Do not launch this harness until root explicitly
releases it.** Merely creating this preparation does not grant VM authority.

Public offline commands:

```sh
python3 scripts/reference/macro_session.py check
python3 scripts/reference/macro_session.py plan
python3 -m unittest discover -s docs/research/continuation/macro-session -p test_offline.py -v
python3 scripts/reference/macro_session.py result /path/to/run.json
```

The guarded future execution form (not executed during preparation) is:

```sh
python3 scripts/reference/macro_session.py run UNIQUE_ID --case name-cancel \
  --allow-vm --authorization-note 'Exact root release/ownership instruction'
```

Both the flag and nonempty release note are required *before* helper import,
lock acquisition, output creation or guest launch. The program cannot authenticate
human permission: the operating agent must actually have root's explicit release.
Never supply the flag/note just to evade this hold. No VM start/stop, QMP connection,
master write, lock open or fixture injection is performed by check/plan/result.

Execution uses the actual shared primary lock
`/home/lynn/projects/wordling/research/cache/reference/session1.lock`, also used by
WP13/WP23. The chosen QMP runtime is the short primary path `runtime/wp38/qmp.sock`
under that same private reference tree; Unix socket length is checked. An occupied
lock or unknown existing own-runtime socket is a refusal, not permission to stop
another guest. Each repetition has a new private boot/disk copy and public directory;
prior evidence is not overwritten. The pinned master, selected profile, QEMU and
firmware are hashed before launch. Fixture injection/extraction happens only on
stopped scratch images. Settings bytes remain private with exact public hashes;
program/manual/dictionary/resource contents are never republished.

On each started guest the runner captures selected Help date, two distinct buffer
sentinels, saved baselines and subsequent dirty inputs before the actual experiment.
The probe budget starts after bounded setup. QMP stop is attempted in finally;
fallback signals require a PID whose command line contains this exact owned QMP
socket. Host containment is never called original Cancel. The lock is released after
the last stop/extraction and before native-body auditing, reporting or review work.

## Planned original recipes

Every recipe has **two fresh repetitions**. All are currently **not-run**. See
plan.json for machine-readable parent associations and source locators.

| Local recipe | Planned observation; no result claimed |
| --- | --- |
| name-cancel | Dirty Doc1/Doc2; Alt-F10 Macro:; type an unexecuted name; user F1; capture actual return and native target state. |
| run-doc1 | Exact pre-existing original project-authored ABC WPM on dirty Doc1; distinguish untouched Doc2 with another sentinel. |
| repeat-doc2 | Switch to Doc2, Esc3, Alt-F10 and same original ABC macro; capture exact target/repeat state and both native exports. |
| missing-name | Invoke a name with no fixture; retain exact original prompt/error and recovery. No invented wording or assumption it equals a nested-macro error. |
| pending-save | Alt-F10 while an actual Save-name prompt is visible; capture whether it remains pending, nests another prompt or refuses. |
| internal-cancel | Stored SDK8020 Cancel key inside a project-authored reference WPM; no user F1 during that observation. It is not user cancellation proof. |
| stop-default | Visible unconditional heartbeat loop; require two evolving heartbeats before user F1, then stable partial output/manual recovery. |
| stop-on | Separate documentary CANCEL ON fixture with the same live-running proof; not enabled as product behavior from SDK source presence. |
| stop-off | Separate documentary CANCEL OFF fixture; retain ignored/unknown/contained outcomes. No Ctrl-Break alias is introduced. |

Published-source fixtures use exact SDK native words: DISPLAY ON FC0D,
CANCEL OFF FC05, CANCEL ON FC06 (SDK97/PDF110), WAIT FC2A and WHILE FC2B /
END WHILE FC11 (SDK97–98/PDF110–111), and Cancel key8020 (SDK95/PDF108).
The SDK is12/93; those documentary identities do **not** establish March support.
The existing original WHILE observations cover only their actual cases. DISPLAY/
WAIT/CANCEL variants remain separate original-consumer experiments, with failures
or unavailable branches retained. They are never admitted into a production macro
VM merely because a table names them.

`SDKNativeWords` is a tightly bounded research-fixture emitter/inspector, using
little-endian native words over the exact original project-authored TESTMAC prefix
(SHA e0e71258e6dc4c678b27773831105f0e7fca0b0803d451fb58b80ac02bc20b4e).
Existing pinned helpers have no such emitter symbol; their actual APIs are reused
for QMP, guest argv, captures and native save interaction. This local emitter is
not a new application codec, general producer, recorder/editor/converter or Go WPM
writer permission. CMD51-199 roundtrip and native WPM writing remain open.

REF379/PDF396 documents Repeat Esc, Macro Alt-F10 and Cancel F1 while running.
The stop fixture has an unconditional visible loop and no reachable tail under its
intended grammar. Two growing heartbeat captures must precede the actual host F1
trace. A finished/failed/unobservable program cannot pass this guard. A key injected
through QMP is the original user-command path, not physical Linux terminal-key
qualification. The internally executed Cancel word is isolated from that path.

## Custody and acceptance limits

Archive the executing runner/helper sources before any guest launch, plus exact
input WPM, trace, raw VRAM/screens/status, native exports, private settings hashes,
profile/master/firmware identities and per-repetition outcomes/JUnit. Unexpected
prompts, failures, skipped exports and host timeouts remain separate raw outcomes.
Partial-loop timing can change raw dot counts/native bytes; do not normalize those
files or manufacture cross-run equality. Compare only declared deterministic target,
mode/progress/preservation invariants, retaining every raw hash and variant.

The bounded native audit uses the pinned pre-mission ASCII/formatter inspector,
not displayed Pos as a semantic document offset. Prompt/selection/dirty state comes
from actual captures and input/native witnesses; no new semantic gap model is
inferred. Dirty-source inputs are explicit typed mutations after saved baselines.
If original handling prevents a native after-export, record it unavailable rather
than inventing a partial file or inferring byte preservation from a screen alone.

A checksum-valid result means sealed artifact integrity, not complete scenario or
product acceptance. An unavailable branch stays unsupported in WP36/37. Parent IDs
are leads only: missing-name, pending-save and stored-Cancel experiments require
future canonical case expansion rather than substituting an unrelated valid ID.
Full38 obligations/91 groups, discovered leaves, all remaining macro/merge commands,
record/edit/conversion, non-ASCII/resources/period-DOS and physical qualifications
remain M1. PDF is M2 after genuine acceptance. No current conformance registry,
acceptance matrix, other WP, native format or mission state is edited here.

Offline preparation checks: six public-CLI tests and Python compilation passed.
These are not original observations, guest protocol execution or completion of
T112–T114. Await root's explicit VM release before proceeding.
