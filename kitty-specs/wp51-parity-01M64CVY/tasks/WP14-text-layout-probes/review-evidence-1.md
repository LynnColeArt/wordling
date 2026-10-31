# WP14 independent review evidence

Reviewer-renata; reviewed lane-d commit d491d9584d7e5aa60ff12736b18c884a3c28075f
against9585c4d. Recommendation: approve bounded T040–T042 original research;
no blocking findings. This reviewer did not implement WP14. Full review prompt
3a98a0f765054f55a40b89ba68a42a37 and exact acceptance/ownership were read;
reviewer profile and review governance resolved. WP07 current primary L1–L4,
text L6, units and tolerance constraints remain binding. Root granted the quiet
point for durable evidence and one verdict. No implementation/raw evidence edit,
VM launch/stop, other WP state or mission acceptance.

## Scope and source assessment

Nine variants have18 accepted fresh runs,16 paired states,64 native before/after
files and32 complete streams. All25 run/calibration manifests remain immutable:
four unclean calibrations, one excluded successful pilot and two incomplete
attempts are preserved alongside the accepted pairs. The scrolling timeout and
retry source differences remain explicit; archived sources identify the actual
input/capture logic. Recipe-plan is a historical proposed/precalibration record;
actual Standard paper and Courier10cpi selection are captured, not retroactively
asserted as untested defaults. Current and archived recipes retain exact text,
variants, cases and tab choices. Canonical registries/statuses remain unchanged.

The selected target is actual plain DOS WP5.1 Help03/09/92, QEMU8.2.2/FreeDOS1.4
and mixed-date July1992 Standard Printer. This does not establish historical DOS,
graphics metrics or another edition. Reviewed pinned SDK text locators for D0
line height/margins/spacing/tab fields (WP31–34/PDF44–47), C1 tab positions and
Packet6+8 (WP11/PDF24); the documentation's edition labels remain distinct from
original observed behavior. Original menu/ruler values and native fields provide
independent corroboration for the selected observations, not general decoding
or a resolution of unrelated version conflicts.

## Independent executions and raw semantic checks

1. verify.py --git-ref HEAD passes25 manifests,9 fresh pairs,16 exact native/
   print states and SHA256/length equality for7328 owned committed Git blobs.
   This count includes source/summary files as well as raw captures. All artifact,
   runner/profile archives and current source-manifest hashes match. Historical
   master/boot/QEMU/firmware/environment/resource identities independently match.
2. analyze.py --private-resources --require-complete-pairs rebuilds21 run records
   and9 pairs; full JSON equals committed analysis.json exactly. No normalization
   or promoted Wordling/NFR005 claim. The independent raw checker additionally
   re-reads90 resource/settings fingerprints directly from18 stopped per-run
   disks, rather than trusting the analyzer's private cached archives. No shared
   runtime/live disk is accessed and no proprietary bytes are published.
3. review-independent-1.py independently walks raw native frames (skipping opaque
   payloads), compares every frame with annotations, reconstructs line/page
   ordinals, and checks64 native files and32 streams. It independently decodes
   all1206 accepted VGA buffers as CP437 and compares exact25-row screen text.
   Every accepted run has captured release, paper8.5x11 Standard, Courier10cpi,
   fixed0.2in line height, single spacing, Left justification/hyphenationNo,
   baselineNo/leading0 and Bottom Center number1. Every state has an empty actual
   print-job queue and each run a final captured DOS prompt. No elapsed wait or
   missing prompt alone substitutes for completed output.
4. Raw body controls confirm alpha/HR/beta;6→7 wrapping soft returns; hard page
   BEFORE(page1)/AFTER(page2), with BEFORE moving to line7 after80-word prepend;
   100 ordered P markers, two8C combined HR/SPg controls and starts P001/P044/P087.
   Dormant99 appears only at the boundary insertion; its stream equals BASE.
   After top-margin change it disappears and starts become P001/P043/P084.
   Native single controls are counted only at complete outer-token boundaries,
   never by scanning opaque payload bytes. Native ordinal and formatter page
   fields remain separate observations, with no double page increment.
5. Raw line-height240WPU, spacing256(1line), margins1200→1500/1800WPU and T/B
   variation1200/1500WPU agree with captured settings and pinned field definitions.
   Raw tab set carries absolute FFFF versus relative creation margin1200; C1
   targets remain2400/3600 absolute but become2700/3900 relative after margin
   shift. Independently read printer LF segments place B/C at byte indices20/30
   for absolute BASE/CHANGE; relative CHANGE shifts to23/33. These are byte
   positions, not physical glyph origins or inferred 6-lines/inch metrics.
6. Native before/after changes are preserved, not masked. The common changed
   offset316 is actual Packet6+8, documented printer-select count flag. In both
   L2-DORMANT/CHANGE repetitions there are also79 changed body bytes, body_equal
   false and equal file length, retained literally in analysis. Final print/
   formatting/save observations are not no-edit byte identity and causation is
   not attributed to printing alone. Repetition comparisons remain exact.
   Complete streams retain CR/LF initialization/padding, text, footer numbers
   and terminators; there is no ESC/FF in this accepted corpus. LF segmentation
   is diagnostic, not a calibrated printer-language renderer or physical origin.
7. Four diagnostic self-tests and six analysis tests pass. Independently compile
   changed Python with compile(text,path,'exec'); no source/bytecode edits needed.
   Frozen recipe checks and correct semantic case/title/feature associations pass;
   changed text and an unrelated valid case with correct replacement metadata
   are rejected. Two compiling in-memory mutations (Dormant99 misclassified as
   normal HR; margin offsets shifted) each fail meaningful assertions. Production
   bytes never change. The recorded10s diagnostic fuzz budget/source is bounded
   and qualified; no new broad fuzz run or original probe was needed.
8. Actual catalogue checks and scripts/review_checks.py pass: four real passes
   (inventory/scenarios/review-adapter/Go discovery) and three explicit no-Go
   build/test/vet skips in this Python-only lane. Exact XML is review-checks-1.xml.
   git diff --check passes; changed paths are confined to the two owned surfaces.

Retained reproducible helper scripts are review-only and must be run from the
reviewed lane root. Facts/verification/XML are durable alongside this review.
Source master/private resource payloads stay external. No implementation changed.

## Acceptance and anti-pattern checklist

T040 PASS exact captured settings and L variants, with diagnostic failures visible.
T041 PASS native before/after, fresh complete streams, job completion and raw unit
boundaries. T042 PASS two fresh repeats, exact comparisons, source provenance and
local canonical proposals without registry promotion. Unmeasured origin, printer
quantization, graphics/font/preview profiles, historical DOS and positional/pixel
tolerances remain unresolved; no full NFR005 or FR/FC acceptance follows.

1. Dead code: PASS executable CLI harness and actual25 archived runs; analyzer
   and verifier have actual CLI callers. Historical precalibration script is
   retained diagnostic provenance, not claimed application code.
2. Synthetic-fixture coverage: PASS actual original raw outputs/settings, native
   controls and streams checked; synthetic malformed/mutation tests are bounded
   diagnostic safety supplements, not original behavior proof.
3. Silent empty return: PASS unknown payloads are retained opaque; capture/run
   errors are recorded incomplete, never promoted to accepted output.
4. FR coverage: PASS bounded FR008/009/015 control/page/printing observations,
   NFR004/C005 provenance and explicit NFR005/tolerance readiness boundary.
5. Frozen surface: PASS only scripts/reference/text_layout.py and owned
   docs/research/continuation/text-layout/ additions; prior evidence/registries
   and dependency sources remain unchanged.
6. Locked decisions: PASS no native writer/layout engine/terminal wrapping,
   graphics/preview acceptance, normalization, physical origin or invented6lpi.
7. Shared-file ownership: PASS local evidence only; new canonical subcases remain
   proposals, no competing canonical owner or other lifecycle edit.
8. Production fragility: PASS bounded fail-loud diagnostics and explicit original
   run incompleteness; no transient failure silently yields a passing oracle.

Approve the bounded original evidence package only. Full M1 and its geometry,
resource, application, terminal and differential comparisons remain open.
