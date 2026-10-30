# Block, Undelete, automation and pagination probes — 2026-10-29

This pass expands the original WP 5.1 03/09/92 oracle. It exercises the pinned
FreeDOS and Standard Printer profile, with a fresh image copy for every recipe.
All macros, primary/secondary documents and resulting native files are authored
through the original application. Wordling is not exercised.

## Checked recipes

| Case | Fixture and checked outcome |
| --- | --- |
| CMD51-202 | Select only Bold On in `A[BOLD]BC[bold]D`, then Backspace and confirm Delete Block. WP repairs the pair: all text and the bold BC span survive. |
| CMD51-203 | Select only Bold Off in the same fixture and delete the block. The same text and formatting survive. |
| CMD51-204 | Block both bold codes and BC, delete, then F1 / Restore. The intermediate body is `AD`; restoration recovers BC and both bold codes. |
| CMD51-045 | Delete the opening bold code and BC using consecutive character Delete commands. F1 / Restore recovers plain `ABCD` without the deleted bold pair. |
| CMD51-205 | Author IF 1 / ELSE and IF 0 / ELSE branches, followed by GO / LABEL. Execution produces exactly `TRUEFALSETAIL`, skipping BAD and SKIP. |
| CMD51-178 | A macro types BEFORE, searches for absent ABSENT, then would type SHOULDNOT. It returns to the document with only BEFORE. Direct interactive READY input produces `BEFOREREADY`. |
| CMD51-206 | Install ON NOT FOUND / GO MISS before the same search. The macro produces `BEFOREHANDLED`; SHOULDNOT is skipped. |
| CMD51-210 | Install ON ERROR / GO ERR, then NEST an absent macro file. The error handler produces exactly HANDLED and skips SHOULDNOT. |
| CMD51-207 | Merge Alice and Bob with `Hello {FIELD}1` and a hard return, with no explicit hard page. Final cursor page is 2; the native body contains one hard-page code. |
| CMD51-208 | Add PAGE OFF to that primary. Both records fit on page 1; the native body contains zero hard-page codes. |
| CMD51-209 | Alice has YES in field 2; Bob has a genuinely empty field 2. IF BLANK / ELSE produces `FILLED Alice` and `EMPTY Bob`. Native output has one separating hard page and contains no residual merge commands. |

Source locators, requirements and feature back-links are in the
[scenario registry](../command-scenarios.json). Relevant manual sections are
REF51 pp. 113 (code-pair repair), 697 (Undelete), 381–384 (Macro Editor), 822–825
(control flow and IF BLANK), 843–847 (error actions and PAGE OFF), and 420–427
(native merge procedure). These are locators into the checksum-pinned manuals.

The original Macro Editor receives command tokens through Ctrl+PgUp / Name
Search and keystroke tokens through Ctrl+V. Typing literal braces does not author
a command. ON NOT FOUND and ON ERROR actions containing GO need **two terminating
tildes**: one ends the label argument and one ends the action. Original WPM files
and the editor's visible source are retained with the runs.

## Native evidence and the formatting flag

The blocked-boundary and block-Undelete recipes compare the complete native
**document area**, using its stored offset. Repaired/restored bodies match their
original bodies. The saved files also retain an observed prefix transition from
`00` to `08` at offset 256 in these fixtures. Every prefix difference is listed
in the run manifest; the files are retained without rewriting any bytes.

SDK51, WordPerfect p. 11 (PDF 24), identifies packet 6 as Document-Specific Flags
and Information. Here its first byte is at offset 256; bit 3 means the document
must be formatted. This explains why the original can preserve the entire text
and code stream while changing a saved prefix flag after an editing operation.
It does not relax Wordling's untouched-input byte-preservation requirement.

The narrow read-only inspector in `scripts/reference/document.py` validates
prefix indices and, for these ASCII merge outputs, walks ASCII/control bytes and
D4/00 end-of-page functions. It checks both lengths and the function trailer,
then counts actual hard-page codes outside those functions. Unsupported
document-area functions fail explicitly; it is not a general document codec. SDK51 WP pp. 17–18 (PDF 30–31)
describes control/function structure, and p. 55 (PDF 68) describes the formatter
function. Inspections retain decoded text, formatter page numbers, document
flags and body hashes. Conditional output passes this same narrow inspection,
so unresolved merge-command structures cannot silently count as ordinary text.

## Repetition and limits

Both repetitions passed all 11 recipes: **22 executions and 110 runtime checks**.
All 27 native output pairs are byte-identical. The independent native-body audit
passes 20 exact body/text assertions. These remain bounded original-app results.

Runs: [advanced-03](../reference-runs/2026-10-29-advanced-03/run.json) and
[advanced-04](../reference-runs/2026-10-29-advanced-04/run.json).
[Output comparison](advanced-output-comparison.json) compares all 27 authored
native outputs from each run. An independent [native-body audit](advanced-native-validation.json)
checks exact ASCII bodies after deletion/restoration and macro execution, plus
exact decoded merge text and page controls. Each run includes the exact runner sources,
scenario snapshot, environment profile, input trace, checks, lossless captures
and checksummed native artifacts. Every recipe exits WP normally before QEMU
stops and offline extraction begins.

Calibration corrected a guessed Ctrl+V prompt to the observed `Press Command
Key:`. It also removed an invented requirement for a persistent Not Found
message: under the default DISPLAY OFF macro fixture, failed search returns to
the ordinary document without such a persistent prompt. The checked evidence is
termination before the sentinel and successful direct editing afterward. Failed
calibration attempts remain private and are excluded from passing evidence.
A page-status attempt caught the transient Repositioning screen; the published
runner waits for stable text before capture and leaves the merge cursor at its
original final position. Macro-source head/tail captures wait for the completed
text and restore the editor cursor before saving. The Macro Editor uses the
normal Home-prefix movement rules; the source-head view uses Home, Home, Home, Up
rather than a single Home.

```sh
python3 scripts/reference/smoke.py your-unique-run \
  CMD51-202 CMD51-203 CMD51-204 CMD51-045 CMD51-205 CMD51-178 \
  CMD51-206 CMD51-210 CMD51-207 CMD51-208 CMD51-209
```

Recheck those native outputs without running DOS, choosing a new report path:

```sh
python3 scripts/reference/verify_advanced_bodies.py \
  2026-10-29-advanced-03 2026-10-29-advanced-04 \
  --output /tmp/wordling-native-check-your-unique-id.json
```

Coverage remains bounded: other attribute pairs, three-level Undelete history,
nested error-handler levels, expression/type errors, loops, PAGE ON resumption,
conditional/nested merge combinations, complex printer-dependent pagination and
all Wordling differential behavior remain unverified. These results extend the
existing [explicit-hard-page merge observation](extended-probes.md); they do not
establish a general layout or language-conformance claim.
