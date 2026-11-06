# WP39: normal-flow QUIT original evidence for WP35

Four corrected fresh guests provide two complete observations for each of two
precisely named contexts. In this selected March original, FC20 executed normally
with registered but unfired ON ERROR handlers stops execution, preserves the
already inserted characters, and returns to usable document input. In the nested
child context it stops both child and parent: parent post-NEST text does not run.
These are original-only facts awaiting independent WP39 review. They test no
Wordling interpreter and authorize no product behavior without WP35 implementation
and separate review.

## Qualified inputs and actual outcomes

All inputs begin **FC0C DISPLAY OFF**, matching the relevant WP32 original sources.
Root/parent handler tails end at ordinary terminal0000; only child CH ends with
its separately source-qualified FC22 RETURN. No handler executes and no QUIT
occurs inside a handler. The source programs have no loop, WAIT, input prompt or
intentional error. Capture visibility was observed in this actual mode; mode
independence is not assumed.

| Local case / corrected run | Source and normal executed site | Exact observed Doc1 / manual continuation |
| --- | --- | --- |
| WP39-NQ-ROOT-v1, revision1 / wp39-root-02 | Q39R.WPM134 bytes; registered RH; literal R39; FC20 at90 before ROOTAFTER and RH label/ROOTERR. | `D1SENT DIRTY1R39` then `D1SENT DIRTY1R39READY`, in both guests. ROOTAFTER/ROOTERR absent. |
| WP39-NQ-CHILD-v1, revision1 / wp39-nested-02 | Q39P.WPM186 bytes registers PH, inserts P39 and NESTs exact C:\OUT\Q39C; Q39C.WPM138 bytes registers CH, inserts C39, FC20 at90 before CHILDTAIL/CHILDERR. | `D1SENT DIRTY1P39C39` then `D1SENT DIRTY1P39C39READY`, in both guests. PARENTBACK/PARENTTAIL/PARENTERR/CHILDTAIL/CHILDERR absent. |

The nested parent's own FC20 at136 is **unreached** because child QUIT stops the
parent too. This package directly executes root@90 and child@90; it does not claim
execution at every original/parent QUIT site. The separately predeclared
child-return alternative would include PARENTBACK. Actual complete native/state
observations instead support stop-all in this exact context; no expectations were
repaired to obtain that result. Current facts are separate from the original
prelaunch stop-all hypothesis and all other unreached branches.

Source identity:

| Authored reference input | SHA256 |
| --- | --- |
| Q39R.WPM | 185d917a4623c0a1bf77af2526a75c19611fed9b08d38bfabc7c32ee853d6ac7 |
| Q39P.WPM | 4f0005af89ed61ca007e0ab31324db5f4d4e22add1c6859071b6abed59d3de86 |
| Q39C.WPM | 68a16bd1d110b232ffc8ca748b86aab5d82216d4ba06e24c3b097e9a0d597f3b |

Every independent fresh guest began with saved D1SENT /D2SENT baselines and
subsequent explicit DIRTY1/DIRTY2 inputs. In all four complete samples, QOTHER
retains exactly `D2SENT DIRTY2`; Doc1's pre-QUIT insertion remains in QBEFORE and
QAFTER. This establishes these literal partial effects, not generic rollback,
variable lifetime, code/cursor semantics or an inferred editor revision protocol.
The actual raster/status/prompt/dirty/selection context and typed trace are retained;
no hardware cursor-register or physical Linux keyboard qualification is invented.

## Native, manual and normal shutdown evidence

Each completed sample has original saved D1BASE/D2BASE, QBEFORE (before manual
READY), QAFTER (after READY) and QOTHER. The named-document save-completion guard
was satisfied before moving on. All five native files and unchanged injected WPMs
were extracted only after that guest stopped. Corresponding native files are
byte-identical between the two fresh repetitions; no bytes or text were normalized.

| Context | QBEFORE size / SHA256 | QAFTER size / SHA256 |
| --- | --- | --- |
| root | 340 / e74151f03c600554acbee8208effcb0e5b4cad4ad6fa2f9db716bbdd8fb9be73 | 345 / 94a921e9a7c0cc8a7617d943e96114c08cc004862907182ef5107f6979d15449 |
| nested | 343 / 11eadde62b5f8a4edf333720b051362dd21dc2e35040564f79f37255b642d516 | 348 / e9934365919ba31a3c492b3f12622ecfa20cb0c7d2d892d5dfbe85ef28f2909f |

QOTHER is337 bytes, SHA256
314467bc6ae152d9eb33e4198c1e81d391fb06bb91aab9b10663110a4972fa2b,
in all four samples. Full-file/source/body spans and Git blobs are retained in
observations.json and run reports. WPM input bytes are identical before injection
and after stopped extraction; this grants no Wordling WPM producer permission.

Actual exit actions in every corrected guest were captured separately:
main Doc1→F7; Save document? (Text was not modified)→No; Exit doc1?→Yes;
main Doc2→F7; Save document?→No; Exit WP?→Yes; clear `C:\WP51>` DOS shell.
Exit doc2? is handled by the narrow protocol/offline controls but **did not appear
in these four original sequences**. No is never sent merely because a document is
clean or an exit question is visible. Unknown states refuse. The audit binds each
captured prompt to the next actual raw QMP key and final DOS capture. Host process
termination or a DOS-looking line within a document cannot qualify completion.
There was no operator F1 in any of these normal QUIT observations.

## Provenance and retained failures

Corrected executing runner SHA256:
2e2f60d522b7b49c508856efb31e352c565584de3001a70d193dd1dd2b7e0915.
Its full source, approved38 helper source SHA6119e4c4d8b4db14eb156001100798a10ec799fa08d6ac64c1d57d361412f616
and transitive helper/contract/provenance files were archived before each pair's
first guest. Both fresh scratch argv sets differ; all masters and selected profile
identities remain pinned. Raw commit d7f1d3b572ed98d325d8a160d1a287fb83e3a124
contains740 immutable files across all three run directories. audit.py independently
reads those actual Git blobs and checks source/output lengths, SHA256 and blob IDs,
source/case/revision identity, native bodies, agreement and actual release/exit proof.
No checkout, Git rewrite, VM or raw mutation is performed by check/result/audit.

Initial wp39-root-01's two guests remain **incomplete diagnostics**, not positive
witnesses. Their normal macro/native/manual observations agree with the later root
pair, but the inherited pre-mission clean_exit wait accepted only Exit doc2/Exit WP,
while the actual original reached Exit doc1. The raw exact modal, timeout/error,
partial trace, native files and executing source492cc3d6... are retained unchanged.
They were safely stopped/extracted and the oracle released. diagnosis-initial-root.json
verifies197 sealed artifacts and actual native observations without promoting them.
The correction changed only the owned captured exit protocol; pre-mission/approved38
helpers, three macro inputs and native/Doc2/macro comparators remained unchanged.
The DISPLAY ON and root/parent-RETURN prelaunch versions remain separately retained
and were never guest-executed. No alternate original result was discarded.

Approved WP32 contract/fixture ledger4eb851e and approved WP38 source58eaf84,
independent reviewcde944d, are pinned. SDK98/PDF111 and REF852/PDF869 are privately
read/hash-bound. Historical WP32 FC20 locations206 HANDLER139,210 ONERROR141,
212 CHILD141/PARENT175 and213 PARENT141 remain unchanged and were skipped by their
old observed error-handler branches. New normal root/child observations supplement
that gap; they do not retroactively execute those historical sites. The reference
emitter uses the exact project-authored TESTMAC prefix and original little-endian
words; no program decompilation, Macro Editor/recording, product format writer,
conversion or proprietary redistribution is involved.

The selected program is plain U.S. English Help03/09/92 on FreeDOS1.4/QEMU with
mixed-date July Standard Printer resources. Complete profile/firmware/master/input/
SET hashes and raw captures remain sealed; private program/media/manual/resource/
configuration bytes remain private. The oracle was released immediately after the
last stopped extraction, before offline review. No further guests are needed.

## Verification and WP35 boundary

Public commands are documented in README; verification/ retains actual stdout,
stderr, exit codes and genuine XML. Twenty-two offline tests include positive
original/Git auditing and ten rehashed adversarial replay controls in temporary
copies. Mutants change screen sentinel, native body, source plus source-envelope
hashes, case, native QUIT opcode, DOS completion, exit response, host containment,
operator F1 and an internally consistent child-return branch. They all reject.
The child-return replay passes the general run classifier as an alternative branch,
then fails the independent recorded-original ledger check; it cannot rewrite the
observed stop-all fact by recomputing hashes. Original files remain untouched.

The first negative-harness attempt expected SemanticChanged for a changed pre-manual
screen; the comparator correctly rejected it earlier as ManualContinuation. That
assertion mismatch and outputs remain retained as semantic-negatives-initial-assertion.*;
the final test expects the actual earlier safety guard. No product comparator was
relaxed or original result changed. The configured reference adapter reports4 passes
and3 explicit no-Go skips. Direct go-test/go-vet no-package failures captured in the
canonical claim are retained separately; they were not hidden or called product
build/test coverage. This lane has a go.mod but no Go source packages.

After independent WP39 approval, WP35 may use these exact normal root/unfired-handler
and nested-child/unfired-handler contexts as bounded original evidence for FC20
stop-all admission. The document sink still owns real partial document/session
effects; VM counters represent charged work, not rollback permission. Active-handler
QUIT, handler reentry, recursion, arbitrary cancellation/error/return, variable scope,
mode independence and other contexts remain unqualified and must retain explicit
refusal or receive separate evidence. Existing Result API/native formats are unchanged.

Full macro/merge/record/editor/conversion/CMD51-199, language/resources/historical DOS,
graphics and physical qualifications remain M1 obligations. All38 requirements,
91 groups and discovered leaves stay retained. No frozen catalogue/current
conformance/acceptance matrix/other WP changed. No full FR/group/M1 acceptance or
M2/PDF work is claimed; the independent reviewer decides this package's verdict.
