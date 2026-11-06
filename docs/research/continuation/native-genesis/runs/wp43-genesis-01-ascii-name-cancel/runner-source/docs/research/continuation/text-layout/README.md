# WP14 original text layout and printer streams

2026-10-30. T040–T042 completed as bounded original-reference research, pending
independent review. Nine local variants have two independently fresh successful
runs each, covering16 state pairs,64 native before/after snapshots and32 complete
printer streams. Every paired native snapshot, raw stream, native code count and
derived line/page membership matches exactly. Inputs/settings/profile hashes
match across each pair. No raw byte masking or normalization was used.

`analysis.json` is the machine ledger and comparison; each run's run.json pins
complete traces, archived runner/profile, VGA/text/raster captures, native files,
printer bytes and diagnostic annotations. Four preliminary menu calibrations,
one successful pilot and two incomplete attempts are retained separately. The
accepted pairs are the wp14-r01/wp14-r01b and wp14-r02 records selected in analysis;
the actual automatic-page first run is named wp14-r01b-L2-AUTO.

## Repeated corpus and original observations

| Local variant | Canonical leads (not promoted) | Complete raw streams per repetition |
| --- | --- | --- |
| L1-HR | CMD51-111, CMD51-197 | BASE:206B |
| L1-WRAP-L3-LR | CMD51-111, CMD51-197, CMD51-162 | BASE:641B, CHANGE:673B |
| L2-DORMANT | CMD51-111, CMD51-197 | BASE:1931B, DORMANT:1931B, CHANGE:1931B |
| L2-HP | CMD51-112, CMD51-197, CMD51-165 | BASE:385B |
| L2-HP-LONG | CMD51-112, CMD51-197, CMD51-165 | BASE:385B, CHANGE:839B |
| L3-TB | CMD51-163 | BASE:641B, CHANGE:641B |
| L4-ABS | CMD51-101, CMD51-103 | BASE:240B, CHANGE:241B |
| L4-REL | CMD51-101, CMD51-103 | BASE:240B, CHANGE:247B |
| L2-AUTO | CMD51-197, CMD51-165 | BASE:1931B |

L1-HR retains alpha/Enter/beta with one native0A hard return. L1 wrapping retains
all80 words: six native0D soft returns with1in/1in margins, then seven with
1.25in/1.5in. Hard-page fixtures retain one0C and BEFORE on native page1, AFTER
on page2 even after the actual80-word prepend edit; BEFORE moves to line7.

P001–P100 are preserved in order, with98 hard returns plus two8C combined
HRt/SPg codes. Page starts are P001/P044/P087, corroborated by saved native
breaks and original page state. A blank paragraph inserted at the observed
page2 start becomes99 Dormant HRt; its BASE and DORMANT printer streams are
byte-identical1931B in each repetition. Changing top margin1→1.2in converts it
back to a normal hard return:99 disappears, ordinary HRt increases by1, and
page starts become P001/P043/P084. No hard page is invented for these soft
boundaries. Independent vertical-margin variation retains the wrapping text
while the original T/B code records1200/1500 WPU.

Absolute2/3in tabs retain2400/3600 WPU and an FFFF absolute sentinel after the
left margin becomes1.25in. Relative1/2in stops are recorded with creation margin
1200 WPU and positions2400/3600, while the resulting tab positions become
2700/3900 WPU after that same margin change. C1 tab records and original rulers
corroborate this distinction. Original printer LF-segment bytes place B/C at
indices20/30 for absolute tabs; relative tabs shift with A. These are explicitly
stream-byte positions, not calibrated physical paper origins or terminal cells.

The observer annotates complete native outer tokens only; control-looking bytes
inside opaque functions are not counted as pages/returns. Selected documented
D0/C1/D9 field readings retain raw frames and source locators (SDK51 WP23,
31–34 and72; PDF36,44–47 and85). Heights/margins/tabs/leading use their stated
WPU fields; line spacing uses1/256 line. Unknown payloads remain opaque.

## Exact profile, settings and native changes

The Help capture in every run confirms plain DOS WP5.1 03/09/92. The established
QEMU8.2.2/FreeDOS1.4 profile and immutable master/boot/firmware hashes are used.
All raw master hashes remain unchanged. EXE/FIL/DRS/STANPRIN.PRS extracted from
all stopped successful images match the installed manifest. Mutated original
SET snapshots are retained privately with public lengths/SHA-256 and access
paths; no proprietary application, dictionary, manual or printer resource is
published. The printer is the declared mixed-date July1992 Standard Printer,
not an untouched March shipping set or historical DOS corroboration.

Every declared input is selected and captured: the original Standard8.5x11in
portrait continuous-feed definition (Letter dimensions), Courier10cpi initial
font,1in margins, left justification, hyphenationNo, single spacing1, fixed
line-height0.2in, baseline-placementNo, primary/secondary leading0in, Arabic
number1 at Bottom Center. Changed margins/tab modes and accepted ruler values
are captured separately. No six-lines/inch or font advance is guessed from10cpi.
The Print menu captures copies1, WordPerfect-generated copies, binding0in,
graphics Medium and text High; printer definition filename/font/port are visible.

Each state saves to a fresh native name before configuring Other port, prints
to its own fresh C:\OUT\*.PRN, waits for Control Printer No print jobs and zero
additional jobs, and saves the after-print native snapshot to a second fresh
name. The app exits normally before QEMU termination and offline extraction.
Source or prior output files are not overwritten. Before/after native changes
are listed literally: a common one-byte change at Packet6+8 is the SDK51
WP11/PDF24 printer-select count flag for equation hashing. It is observed across
port configuration, printing and the following save; causation is not attributed
to printing alone. Document flags/body equality and all changed byte offsets
remain in the report. The native files and printer bytes are never normalized.

Raw streams contain original CR/LF/space/text initialization, page-number and
termination sequences. The Standard Printer emits line-feed padding rather
than a form feed in this corpus; the100-paragraph stream has198 LF and204 CR.
Nonuniform LF increments between marker lines are recorded as bytes, not
converted into an invented physical line-height rule. Raw stream segmentation
is a diagnostic witness, not a substitute printer-language renderer.

## Failed attempts and timing provenance

Four calibration runs are labelled diagnostic-only with deliberately unclean
shutdown and no accepted exports. wp14-attempt-01 sent4 after Full Document had
already returned to editing, creating beta4 and then an exit prompt. It remains
incomplete. wp14-attempt-02 is a successful pilot, excluded from accepted pairs.
The initial wp14-r01-L2-AUTO attempt timed out while scrolling remained unstable
at visible P089; it remains incomplete with no accepted stream. Its fresh retry
waits for each unique marker before the next Enter. Capture settling retains
0.4s unchanged text, with an explicit60s maximum instead of20s. Host-timed input
is not claimed instruction-identical. Archived source hashes distinguish every
revision; the changed scrolling branch/timeout does not alter the earlier four
variants' inputs, and their exact native/stream repeat matches are checked.

No failed capture is rewritten or quietly reused. All25 raw run/calibration
manifests and every listed artifact are verifiable. Local .gitattributes keeps
native/PRN/VGA/PPM blobs binary and screen.txt raw, including all25 blank rows.
The committed Git-blob check compares SHA-256/length with actual raw files.

## Validation and reproduction

Focused self-tests cover malformed/truncated framing, complete opaque payload
isolation, exact/over diagnostic token limits, and unchanged print control/spaces.
Six analysis tests use real original outputs for native units, hard/dormant page
membership, absolute/relative tabs, wrong-width refusal and raw comparison.
All pass. Python compilation passes. The declared seven-check regression suite
reports four passes and three explicit no-Go skips in this code lane; no Go
package exists here. This does not claim tests of other implementation lanes.

The native diagnostic limit is16MiB/65,536 outer tokens, stated as a research
safety policy. A10s final seeded mutation workload in fuzz-final.json passes
135,573 cases (32,437 accepted framed diagnostics,103,136 refusals), preserving
body reconstruction/hash and bounded indexing. It is a small synthetic workload,
not a general codec or original behavior proof. The earlier10s workload and
single65,536-token allocation observation retain their exact archived source:
0.608s and18,165,192B peak Python-traced allocations at65,860 native bytes.
These are host/harness observations, not DOS capacity or product SLOs.

```sh
python3 scripts/reference/text_layout.py self-test
python3 -m unittest discover -s docs/research/continuation/text-layout -p test_analysis.py -v
python3 docs/research/continuation/text-layout/verify.py --git-ref HEAD
python3 docs/research/continuation/text-layout/analyze.py --private-resources --require-complete-pairs --output /tmp/wp14-new-analysis.json
python3 scripts/reference/text_layout.py fuzz --seconds 10 --output /tmp/wp14-new-fuzz.json
python3 scripts/review_checks.py --junitxml /tmp/wp14-validation.xml
```

Set WORDLING_REFERENCE_PRIMARY to a primary checkout/private-cache location on
another host; reacquire proprietary inputs by the established lawful manifest,
not by committing them. To rerun an original variant, use a new run ID with
`python3 scripts/reference/text_layout.py run NEW_ID VARIANT`. The short primary
runtime and shared session1.lock prevent concurrent original guests. Source
archives/recipe-plan/environment/resource hashes identify the exact experiment.
Historical and final diagnostics remain separate from raw original observations.

## Remaining obligations and proposed canonical expansion

All canonical registries/statuses are unchanged. Propose separately scoped
subcases under CMD51-111/197 for hard/soft/dormant control distinctions;
CMD51-112 for hard-page persistence after prepend; CMD51-162/163 for margin
scope/vertical effects; CMD51-101/103 for absolute versus relative tab anchoring;
CMD51-145 for Other-port filename/job completion/raw output; CMD51-165 for the
captured Bottom Center numbering. These local recipes do not certify the entire
canonical command, workbook lesson or broader manual coverage.

Physical first baseline/printable origin, graphics/proportional metrics,
historical DOS corroboration, L5/L7/preview, printer/device calibration and
quantization interpretation remain unresolved. No positional/pixel tolerance
is selected; no NFR-005 positional comparison or full acceptance is claimed.
Exact byte/code/page invariants are checked independently of those gaps.
No layout engine, native writer, terminal-based wrapping or Wordling feature
comparison was implemented. All complete M1 obligations remain open; PDF is M2.
