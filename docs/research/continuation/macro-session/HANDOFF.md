# WP38 bounded original-consumer handoff

This package observed the pinned March WordPerfect 5.1 DOS original in Linux QEMU/
FreeDOS scratch guests. It did not execute Wordling. Thirty fresh guests comprise
15 retained pairs, with nine pairs selected for the current bounded handoff.
All guests stopped; the oracle lock was released after final extraction and before
offline audit (`oracle-release-02.json`). No further guest is authorized here.

## Current observations

Every row below has two independent fresh repetitions. Full exact per-sample
native body, raw invocation trace, screens, hashes and limitations are in
`audit.json`; its selected rows link run IDs and sample IDs to `runs/`.
The source-derived fixture identities remain distinct from observed behavior.

| Recipe / selected run | Actual bounded observation |
| --- | --- |
| name-cancel / wp38-name-cancel-02 | F1 from the unexecuted Macro-name prompt returned to the document; native dirty Doc1 and Doc2 texts remained `D1SENT DIRTY1` and `D2SENT DIRTY2`. |
| run-doc1 / wp38-run-doc1-01 | Exact original project-authored ABC fixture appended ABC to dirty Doc1; distinct dirty Doc2 remained unchanged. |
| repeat-doc2 / wp38-repeat-doc2-02 | Esc3, Alt-F10 and the same fixture produced `D2SENT DIRTY2ABCABCABC` in Doc2; dirty Doc1 remained unchanged. |
| missing-name / wp38-missing-name-02 | Exact visible submitted name `C:\OUT\M38NONE`; original reports `ERROR: File not found -- C:\OUT\M38NONE.WPM`. Immediate F1 capture can still show the error; settled capture returns to the document. No second F1 was required after the settled main-document capture. Both native dirty buffers remain unchanged. |
| pending-save / wp38-pending-save-01 | With a Save-name prompt already pending, Alt-F10 leaves that prompt visible. F1 returns to the document; both native dirty buffers remain unchanged. This is one prompt context, not universal prompt nesting semantics. |
| internal-cancel / wp38-internal-cancel-02 | Source word 8020 inside the macro yielded **`D1SENT DIRTY1INTERNALMSTAIL`**. The tail executed; no operator F1 was injected. Stored Cancel does not establish operator cancellation semantics. |
| stop-default / wp38-stop-default-02 | Two evolving document-region heartbeats (1 then 3 dots) precede operator F1 in raw QMP. Partial body stabilizes at 3 dots; manual `USERREADY` appears. Native Doc1 equals the exact captured `D1SENT DIRTY1MSLIVE...USERREADY`, Doc2 unchanged; no reachable macro tail executes. |
| stop-on / wp38-stop-on-02 | Separate FC06 CANCEL ON fixture gives the same bounded live-before-F1, stable partial body and native/manual recovery witnesses in both repetitions. |
| stop-off / wp38-stop-off-01 | Separate FC05 CANCEL OFF fixture continues its body heartbeat after operator F1 (1→2 before, 3→6 after). Manual `USERREADY` does not appear. Host containment stops the guest; native AFTER is intentionally unavailable. This is continuation in the observed window, not successful cancellation/native-stop proof. |

`F1` means **operator-injected QEMU keyboard event**, not physical Linux keyboard
qualification. Default/ON evidence is restricted to this exact yielding ASCII
fixture and March executable/profile. OFF does not establish behavior for every
macro/edition/resource. Stored 8020 continued here; do not substitute it for the
operator-command path or claim a broad SDK/edition semantic equivalence.

## Raw failures, corrections and timing

All first-series and calibration reports remain intact. Name-cancel-01 lacks raw
QMP wire custody and is calibration only; name-cancel-02 supplies the selected pair.
Repeat-doc2-01 first D1AFTER export is **zero bytes** despite mcopy exit0; its second
repetition is valid, but that pair is not promoted. The saved original D2 export
contains the expected repeated body. A save/export race is a hypothesis, not a
proven root cause. The corrected save protocol requires a stable named-document
capture before quit/extraction, and repeat-doc2-02 has two complete valid witnesses.

Initial missing-name/internal-Cancel runs retained unresolved modal states and no
native AFTER. Corrected runs use exact visible name echoes, host key quiet time,
immediate and settled first-F1 captures, and a separately captured second-stage
state. A second F1 is sent only if the modal state actually remains. No clipped
field is interpreted as a truncated invoked filename. Stored-Cancel-02 is already
main-document after execution and needs zero operator F1 events.

Initial Default/ON host containment came from the harness counting all screen dots:
status `Pos 3.1` changing to `Pos 4` changed that count even with a stable document.
These reports remain host-contained, never retroactive passes. Corrected counting
uses the named first document row only; two evolving pre-F1 body captures, stable
partial output, manual input and exact full native text establish the selected
02 pairs. `diagnosis-initial-series.json` preserves diagnosis and run separation.

Raw timing variants are not normalized. The offline audit rejects missing/changed
heartbeat regions, extra/wrapped document rows, ≥64 first-row characters, or >16
dots; absence/saturation/wrap cannot become a false stop. These conservative limits
bound the actual observation, not general document/layout semantics. Native body
inspection uses pinned `document.plain_merge`, not displayed Pos as semantic offset.

## Provenance and replay

`preparation.json` pins17 source/manual/helper artifacts. WP32 source is
4eb851eac3096d27d4743616ce3ae74f7a9edc05, independent review754bdcc.
Every run archives its **actually executing** runner and helper sources, baseline
executable/profile/firmware identities, input WPM, raw QMP tx/rx bytes, captures,
native exports and private settings hashes. Each original-only run.json seals
artifacts; extraction reports independently bind stopped-disk WPM bytes to inputs.
Private programs/media/settings/resources remain private; only hashes are public.
Per-run master-before equals master-after. No master was changed.

The corrected rerun source SHA256 was
`6f607650d3c082775840211a55499109a6f3693ceab3761625a4c46f35470c1b`, sealed by
`rerun-prelaunch.json` and every rerun's source archive. Final source adds only
post-run reference-helper exposure: `configure(primary, runtime_tag='wp38')` accepts
a short safe isolated runtime tag, and `SDKNativeWords.emit` admits exact immutable
WP32-catalogued words as well as WP38's documentary probe words. These pure API
changes were **not guest-rerun**. Offline tests prove every retained emitted input fixture
remain byte-identical. Importing these helpers does not call configure/start QEMU;
future callers need their own ownership, authorization, source seals and evidence.
No executed probe function was refactored for the future WP39 use.

The emitter is reference-fixture-only, over the exact project-authored TESTMAC prefix
SHA256 `e0e71258e6dc4c678b27773831105f0e7fca0b0803d451fb58b80ac02bc20b4e`.
Published SDK words are source-located by WP32 and preparation pins. Admission to
this research emitter grants neither original semantic qualification nor Wordling
WPM writing/recording/editor/conversion permission. Future QUIT/handler experiments
belong to WP39 and are not results of this package.

Offline reproducible commands (no guest launched):

```sh
python3 scripts/reference/macro_session.py check
python3 scripts/reference/macro_session.py plan
python3 scripts/reference/macro_session.py result docs/research/continuation/macro-session/runs/wp38-stop-on-02/run.json
python3 docs/research/continuation/macro-session/audit_results.py
python3 -m unittest discover -s docs/research/continuation/macro-session -p test_offline.py -v
python3 scripts/review_checks.py --junitxml docs/research/continuation/macro-session/verification/project.xml
```

The audit checks30 stopped guests,1,756 sealed raw artifacts and18 selected
observations. Its XML has18 checks, with OFF2 skipped for absent native-stop proof.
An audit pass means custody and the stated bounded original observations, not
product parity. Final offline commands/source seals are in verification/. Ten offline tests include
2,000 seeded malformed binary inputs (seed380114), bad offsets/termination and
positive reference fixture parsing; this is bounded research-reader checking. The
project adapter passes4 checks and explicitly skips3 Go checks because this lane
contains no Go packages. It supplies no product validation.

## WP36/37 implementation boundary

Keep Macro-name entry, command dispatch, Doc1/Doc2 target, numeric Repeat, missing-name
error, pending prompt, macro-internal key and operator stop as distinct transitions.
Use the exact run/sample/native witnesses rather than a helper's passed Boolean.
Cancellation must preserve bounded partial effect and return to a usable command
context; OFF's host containment must never be reported as an original Cancel.
These are implementation leads, not approval of any unexecuted Wordling code.

Parent CMD51-131 and WP51-059/060 are traceability leads, not closed cases. Missing
name, pending Save and stored-Cancel need explicit future leaf-case extensions.
All38 obligations/91 groups and discovered leaves remain in M1. Full macro/merge,
recording/editing/conversion/CMD51-199, selection contexts not actually exercised,
non-ASCII/resources/period DOS and physical qualifications stay open. No current
conformance ledger, acceptance matrix, native format or other WP state changed.
No M1 acceptance; PDF/M2 begins only after genuine full M1 acceptance.
