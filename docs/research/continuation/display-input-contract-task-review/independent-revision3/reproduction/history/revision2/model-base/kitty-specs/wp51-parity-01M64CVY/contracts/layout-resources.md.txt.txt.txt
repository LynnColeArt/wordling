# WP07 layout and resource comparison contract

Research handoff, 2026-10-30. Requirements FR-009, FR-015, FR-016 and NFR-005;
formatting dependencies FR-008; permanent FC-001–009 apply. This contract specifies
experiments, acquisition gates and comparisons. It implements no layout engine,
preview, printer driver or PDF export. Full original pagination and preview remain
M1. PDF remains M2. WP12 authors executable continuation WPs from these proposals.
`spec.md`, `plan.md`, `data-model.md`, `docs/compatibility.md`, `docs/roadmap.md`, and
the approved WP01/04/05/06 contracts remain authoritative.

## Evidence boundary and pinned documentary locators

The selected target remains plain U.S. English DOS WP 5.1, Help date **03/09/92**.
Executable SHA-256 is `0734d0734c78c113ddaf40293c2c21b02e2cacc063bca5aa3d02f696de0bdc6a`.
The current QEMU 8.2.2/486/16 MiB/VGA profile boots FreeDOS 1.4 (kernel 2043,
FreeCOM 0.86), without a parallel device. It is not historical MS-DOS evidence.
The selected Standard Printer is 10-cpi text only, without graphics; its source
printer disk is **1992-07-17**, while the program disk is March. No untouched
March shipping-set, graphics-font fidelity or historical DOS equivalence is claimed.
The baseline, media, installed-file, environment and resource manifests are
hash-pinned in the ledger below. Setup bytes can vary with printer FAT modification
time; `setup-timestamp.md` records the controlled explanation. Preserve raw SET
files and timestamps; never normalize them to manufacture reproducibility.

Sources: REF51 is the 6/92 reference, WB51 the 11/89 workbook, SDK51 the 12/93
toolkit with intermediate WP revision marks. The source registry and local PDFs
are pinned below. These editions are research evidence, not automatic proof of
March executable behavior. Printed pages below are distinct from **one-based PDF
pages**. Source instructions are paraphrased; no proprietary resources are copied.

| Subject | Source: printed / PDF | Consequence for this contract |
| --- | --- | --- |
| Returns, dormant returns and leading | REF51 557–560 / 574–577 | Capture native boundaries separately from screen lines and print leading. |
| Explicit page break | REF51 471–473 / 488–490 | Test persistence of hard page after preceding edits. |
| Left/right margins | REF51 394–395 / 411–412 | Measure from paper edges; text flow changes with available width. |
| Top/bottom margins | REF51 396 / 413 | Record first-line baseline placement option as well as margin values. |
| Tab and Tab Set | REF51 631–632, 634–639 / 648–649, 651–656 | Distinguish tab codes, stop settings and positions from repeated spaces. |
| Fonts and kerning | REF51 205–208, 303 / 222–225, 320 | Distinguish printer default, document initial font and in-body changes; record available fonts/substitutions. |
| Printer selection | REF51 506–509 / 523–526 | Record actual selected definition and resources, not only a model name. |
| Print to disk | REF51 543 / 560 | Other port writes original printer/text stream; it is not native save or PDF. |
| View Document | REF51 701–704 / 718–721 | Four page-view modes, navigation, colors and printer dependence remain M1. |
| Measurement definitions | SDK51 WP-2 / 15 | WPU and screen pitch are different coordinate systems. |
| Native return/page values | SDK51 WP-19–23 / 32–36 | Preserve hard/soft identity; formatter data is not an arbitrary newline stream. |

REF51 PDF 411 was visually inspected because its margin heading follows macro
prose on the same page; the printed footer is 394. PDF 222 similarly ends the
preceding section before Font. Whole-page headings, not the first OCR line,
establish the locator. WB51 lessons remain not-run as lessons; the WP05 concordance
covers their thematic leads. No workbook exercise is claimed as executed here.

## Resource acquisition and identity gate (T019)

Keep acquisition lawful and private: record rights holder, source URL or owner
media description, retrieval time, edition labels, permission/license terms and
redistribution disposition. A public download location is not redistribution
permission. Store external binaries/manuals/fonts in ignored private cache; publish
only rights-cleared project scratch fixtures, manifests and observations. Missing
permission blocks redistribution, not recording a resource gap.

| Profile | Current readiness | Required acquisition and corroboration |
| --- | --- | --- |
| Existing FreeDOS/text | Available for bounded new experiments, not yet run here | Verify pinned master and resource hashes; copy to a unique run; retain explicit mixed-date/FreeDOS caveat. |
| Historical DOS control | Blocked: no acquired, fingerprinted historical DOS profile declared | Obtain licensed period DOS media, identify exact version/build/locale via original runtime, hash all disks/system files/config and boot image; rerun text controls with the same executable/resources. No DOS version is selected by this contract. |
| Graphics/printer/font | Blocked: no matched graphics-capable print/preview reference profile | Obtain an original plain-5.1-compatible printer definition plus all metric/font/cartridge/soft-font dependencies and documented printer-language reference. Prefer period-matched media; document any date discrepancy instead of replacing the baseline silently. Capture original selection/capability screens and resource availability. |
| Physical printer witness (if used) | Blocked until actual device and calibration are recorded | Model, firmware, resident/downloaded fonts, settings, paper and printable origin; no device equivalence inferred from a driver name. |

Every new profile manifest must include: parent baseline ID; immutable resource
ID; acquisition provenance/rights; full file paths, byte sizes and SHA-256; disk
image/archive hashes and original FAT dates; WP EXE/FIL/DRS and selected PRS;
all selected resident/cartridge/downloadable font names, IDs, style/size/pitch,
metric source and substitution rules; graphics/display drivers; language,
hyphenation and character resources; raw SET file and selected printer options.
Record install/selection transcript, WP Help capture, printer name and capability
capture, font lists, OS COMMAND/kernel versions, CONFIG/AUTOEXEC, code page,
keyboard, emulator binary/version/arguments, firmware hash, CPU/RAM/VGA and RTC.
Printer font names alone are not metric identity. Record point-size scaling,
kerning setting, orientation, paper dimensions/feed/source, copies, quality,
print range, initialization and literal printer commands. Unknown fields mean
incomplete profile and block only comparisons depending on them.

Rebuild from a fresh copy without altering the established master. Preserve raw
images/SET/output before interpreting discrepancies. Recompute hashes before and
after each run, explain expected mutable files, archive runner source and exact
keystroke/settings trace. Require two fresh-copy repetitions before promoting a
bounded observation. A historical-DOS control changes only OS/config dependencies;
a printer control changes only declared printer/font dependencies. If several
resources change, label a combined-profile observation and do not attribute the
difference to one resource. Selection on one profile never certifies another.

## Small reference corpus proposal (T020)

All L rows below are **proposed and unrun**, including the ready text rows.
They are local recipe names, not new canonical CMD51 IDs or verified features.
Each row expands canonical cases in the following association table. Start each
variant from a blank document in a fresh profile copy. Use project-authored ASCII
scratch text; save inputs and outputs through original WP; retain exact trace and
native bytes. Baseline page settings for proposed tests: portrait Letter 8.5 by
11 inches, left/right/top/bottom 1 inch, left justification, single spacing,
hyphenation off, Standard Printer 10 cpi for text rows. Explicitly select and
capture each setting; if unavailable, stop and record the prompt. These are test
inputs, not claims about original defaults. Initial font, line-height, tab stops,
baseline placement and selected paper definition must be recorded rather than
inferred. Do not guess six lines/inch from 10 cpi.

| Recipe / canonical cases | Deterministic input and variation | Capture and readiness |
| --- | --- | --- |
| L1: CMD51-111, CMD51-197 | Type `alpha`, Enter, `beta`; separately type `word ` 80 times without Enter, then reduce text width using the L3 margins. | Native hard/soft code identities, Reveal Codes and line membership before/after. Ready text experiment; inferred soft breaks must be corroborated after formatting, not searched inside opaque formatter payload. |
| L2: CMD51-112, CMD51-197, CMD51-165 | Type `BEFORE`, Ctrl+Enter, `AFTER`; repeat with `word ` 80 times inserted before BEFORE. Separately type 100 paragraphs `P001` through `P100`, each followed by Enter, without a hard page. Set and capture a declared page-number position. | Hard-page persistence versus automatic page membership and number positions; page-count outcomes unknown until run. Test dormant-return behavior at a soft boundary by moving a blank paragraph across it. Text semantics ready; physical geometry gated on metrics. |
| L3: CMD51-162, CMD51-163 | Use L1 wrapping text, change left/right to 1.25/1.5 inches, then top/bottom to 1/1.25 in a separate fresh variant. | Code scope, line/page membership, first baseline and printable origin. Ready text observation; not a general font/pagination acceptance test. |
| L4: CMD51-101, CMD51-103 | Clear existing stops, explicitly choose absolute left stops 2 and 3 inches from left paper edge; type `A`, Tab, `B`, Tab, `C`, Enter, `AA`, Tab, `BB`, Tab, `CC`. Repeat with relative stops 1 and 2 inches from left margin, then change left margin to 1.25 inches. | Capture exact accepted stop/mode values, codes and glyph origins; stop if menus cannot express inputs. Ready text observation; no claim about proportional alignment. |
| L5: CMD51-160, CMD51-161, CMD51-185 | On the acquired graphics profile, select two actually listed fonts (one proportional) and declared sizes; type `iiii WWWW AV To`, repeat with kerning off/on and a font change at the cursor. | Record exact choices/substitutions, advances, baselines, wrap/page changes; distinguish initial from in-body fonts. Blocked on acquired metrics and font definitions; font names/sizes must be frozen before execution. |
| L6: CMD51-145 | Route Other port to a fresh scratch filename and print each L1–L5 original document separately; record any extension/overwrite prompts and clean completion before exporting bytes. | Complete raw stream including initialization/terminators, size/hash, job options and language. Ready text capture proposal for L1–L4; graphics stream blocked for L5. Never treat text capture as PCL/PostScript evidence. |
| L7: CMD51-146, CMD51-147 | Use L2/L5 in 100%, 200%, Full Page and Facing Pages in separate fresh runs; navigate first/last and adjacent pages, then switch colors and print again. | Lossless VGA raster, viewport/page bounds, navigation state and before/after print streams. Blocked as graphics acceptance on matched resource/preview profile. Existing Standard Printer may supply a diagnostic only. |

The recipes do not replace the complete canonical scenarios. Page numbering,
keep/block protection, paper definitions, columns, headers/footers, foot/endnotes
and continuation, labels, tables, equations, graphics wrapping/anchors, generated
references and printer utilities remain unimplemented M1 obligations. Add bounded
combination cases after elementary resources/geometry are established; Story 3
scenarios 1/2/3 require these combinations and generation behavior. Story 3
scenarios 4/5 specifically require L6/L7 follow-through on accepted resources.

### Canonical semantic associations

The case names, feature links, documentary locators and statuses below are copied
as registry metadata for audit, not copied behavioral evidence. All cases are
not-run except the bounded merge control listed separately.

| Case (canonical title) | Canonical feature(s) | Status |
| --- | --- | --- |
| CMD51-111 (Hard return ends a paragraph) | WP51-016 | not-run |
| CMD51-112 (Insert a hard page break) | WP51-040 | not-run |
| CMD51-197 (Distinguish native hard/soft returns and pages) | FMT51-004 | not-run |
| CMD51-162 (Change left and right margins) | WP51-033 | not-run |
| CMD51-163 (Change top and bottom margins) | WP51-033 | not-run |
| CMD51-101 (Insert a normal tab) | WP51-035 | not-run |
| CMD51-103 (Change tab settings at the cursor) | WP51-035 | not-run |
| CMD51-160 (Set initial base font from selected printer resources) | WP51-031 | not-run |
| CMD51-161 (Toggle printer kerning at cursor) | WP51-031 | not-run |
| CMD51-145 (Direct original printer output to a disk file) | WP51-074 | not-run |
| CMD51-146 (Preview each original page-view mode) | WP51-076 | not-run |
| CMD51-147 (Changing preview colors does not change printed content) | WP51-076 | not-run |
| CMD51-185 (Select an installed original printer definition) | WP51-071 | not-run |
| CMD51-165 (Choose page-number position) | WP51-041 | not-run |
| CMD51-207 (Default merge inserts a page break between records) | WP51-062 | partially-observed |

CMD51-207 is a control for native **merge separators**, not soft-page layout.
Its two advanced runs saved `MERGED.WP5` with a counted hard-page separator and
ended at the expected page 2. Exact trace/checks/exports are in the pinned run
manifests and their archived runner. The output pairs are pinned below and match;
this does not observe L1/L2, printer bytes, glyph positions or Wordling behavior.
No existing partial merge observation promotes CMD51-197 or any layout scenario.

## Units, measurement procedure and predeclared tolerances

Use exact rational WPU for documentary geometry: 1 WPU = 1/1200 inch (SDK51
WP-2). Inch-to-WPU multiplication is exact; keep entered decimal strings and
original displayed values. Points use 1/72 inch for proposed test bookkeeping;
confirm original conversion/rounding through original prompts before asserting
point-input equivalence. Record raw native field units per code contract before
converting; do not infer every integer uses WPU. A screen pitch unit is a column,
not a physical length. At a declared 10-cpi pitch the nominal advance is 120 WPU,
but actual font/driver advances and vertical metrics still require measurement.
Raster pixels, emulated VGA cells, printer dots and physical paper coordinates
remain explicitly tagged units. No rounding to terminal columns defines layout.

1. Freeze recipe revision, resource/profile/input hashes and expected invariants
   before tests. Capture native input and actual settings. Run original twice on
   fresh copies; force the documented formatting/print path and record completion.
2. Extract code identities with a type-aware audited inspector and corroborate
   Reveal Codes. Retain formatter packets and computed breaks; never count raw
   0B/0C bytes inside arbitrary payloads as document pages. Record page assignment
   by content marker, line membership, page labels, first/last baseline, x origins,
   glyph advances and paper/printable origins with units and evidence source.
3. Decode the captured original printer stream only after its language and metric
   semantics are pinned. Keep bytes authoritative; separate initialization, font
   selection/downloads, text/position commands and end-of-job. A diagnostic decoder
   must retain unknown bytes and flag unsupported commands. Independent rendering
   is a witness whose version/fonts/resolution must be pinned, not an oracle
   replacing original WP. Physical witnesses require measured registration/scale.
4. For each future Wordling comparison, use the same native input/settings and
   declared metric profile. Compare native invariants, semantic line/page/number
   assignments, ordered glyph identity/position records and original output bytes
   separately. FC-002 requires exact bytes for no-edit native saves. FC-003/004
   preserve unrelated bytes on edits; intended formatting changes need explanation.
5. Compare original preview state/functions and displayed page membership with
   original print geometry. Map page rectangle to raster coordinates using recorded
   viewport/scale; use lossless captures with cursor/menus identified separately.
   A bitmap similarity score alone cannot certify printed placement or navigation.

**No empirical positional or pixel tolerance is set by WP07.** Page membership,
page numbering, hard/soft identities and invariant comparisons require exact
agreement. Raw print streams are compared byte-for-byte first; any differences
require a documented command-level explanation, never broad byte masking. Repeat
variance is reported from raw outputs, including setup changes; raw evidence is
never normalized. No arbitrary one-pixel/one-WPU or percentage pass threshold.

Before a positional acceptance run, a follow-up must publish a tolerance record:
profile and corpus revision; coordinate/metric units; exact comparison layer;
quantization/rounding derivation from original driver/language; repeated original
measurements; screenshot/device calibration uncertainty if applicable; separate
x/y bounds and origin transform; rationale and reviewer approval recorded before
the differential run. Exact rational comparisons need no empirical allowance.
Absent that record, measurement may proceed as exploration but cannot pass NFR-005.
A post-result tolerance expansion is a new test revision requiring new runs and
preservation of the failed result. Zero unexplained differences remains the gate.

## Bounded continuation proposals (T021)

| Slice for WP12 to author | Entry and output | Exit evidence / remaining scope |
| --- | --- | --- |
| Text control/probe harness | Existing pinned profile; add only L1–L4 and text L6 recipes with unique runs and immutable exports. | Two original repetitions, complete traces/native/print hashes, clarified units and code effects; no general pagination/preview claim. |
| Historical DOS corroboration | Licensed media and full fingerprint acquisition gate above. | Fresh historical profile, same text controls and discrepancy report with OS differences isolated. Missing media remains explicit, not a blocker to text probes. |
| Graphics resource/metric contract | Acquire definition/font dependencies and identify exact original printer language; freeze L5 choices. | Capability/selection captures, resource hashes, field/metric interpretation, two original L5–L7 runs and pre-test tolerance derivation. No unexplained substitution. |
| Elementary semantic/layout implementation | Reviewed code/unit contract and original L1–L5 evidence; preserve WP01 byte-image and WP04 command boundaries. | Bounded Go decoder/layout tests plus original retrieve/edit/print/save and differential geometry; keep unsafe/unknown structures preserved or refused. No terminal-driven layout. |
| Original printing and preview implementation | Accepted stream/resource and page geometry contracts, L6/L7 oracle. | Exact original print-to-disk behavior, page-view modes/navigation/colors on Linux with tested resource handling; failures/missing fonts explicit. No PDF implementation. |
| Pagination combinations | Elementary comparisons accepted; acquire needed structural fixture/resource evidence. | Headers, notes/continuations, numbering, keeps, columns, paper definitions and advanced structures checked separately then together under Story 3. No full-scope acceptance from the small corpus. |

Each proposal needs stable canonical case expansion where no dedicated case exists,
provenance-cleared fixtures, acceptance invariants and review before executable WP
creation. This document changes no canonical status, lifecycle authority, tasks
queue, raw evidence or resource baseline. Missing external resources stay visible
beside ready experiments; completion of T019–T021 is contract research completion.

## Reproducible ledger and validation

All paths are repository-relative. Local cached sources remain ignored and must
be reacquired by their pinned registry URL/hash when absent. The ledger pins full
input files, not proprietary contents. Run the embedded audit from repository root.

<!-- WP07_AUDIT_BEGIN -->
```json
{
  "inputs": [
    {
      "path": "docs/research/sources.json",
      "size": 3434,
      "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"
    },
    {
      "path": "docs/research/feature-inventory.json",
      "size": 60797,
      "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"
    },
    {
      "path": "docs/research/command-scenarios.json",
      "size": 346162,
      "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"
    },
    {
      "path": "docs/research/reference-baseline.json",
      "size": 2026,
      "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"
    },
    {
      "path": "docs/research/reference-environment/environment.json",
      "size": 2482,
      "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"
    },
    {
      "path": "docs/research/reference-environment/resource-profile.json",
      "size": 2161,
      "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"
    },
    {
      "path": "docs/research/reference-environment/media-manifest.json",
      "size": 3548,
      "sha256": "6735740085436dcfdfc1c4e9c6e95efd335612a70ff642046840474333cb2397"
    },
    {
      "path": "docs/research/reference-environment/installed-files.json",
      "size": 24040,
      "sha256": "a8532ce5be7caa5759799841c8c0e3128810f7631f49101978102244139a1238"
    },
    {
      "path": "docs/research/reference-environment/setup-timestamp.md",
      "size": 3956,
      "sha256": "a7ba6d0b6088e8856129cc30340648071c65dd40a4fc06734c17856007a8f815"
    },
    {
      "path": "research/cache/WPDOS51Reference.pdf",
      "size": 61124991,
      "sha256": "ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531"
    },
    {
      "path": "research/cache/WPDOS51Workbook.pdf",
      "size": 28520554,
      "sha256": "868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d"
    },
    {
      "path": "research/cache/WP51DevelopersToolkit.pdf",
      "size": 1907150,
      "sha256": "5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754"
    },
    {
      "path": "research/cache/reference.txt",
      "size": 5758334,
      "sha256": "f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c"
    },
    {
      "path": "research/cache/workbook.txt",
      "size": 1351703,
      "sha256": "4a99b406886f1e128ab673c9cefddc83ca9f53ddbc8dcfd621e38b7afe79ecce"
    },
    {
      "path": "research/cache/toolkit.txt",
      "size": 1430467,
      "sha256": "8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md",
      "size": 23043,
      "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json",
      "size": 21525,
      "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/editing.md",
      "size": 43728,
      "sha256": "7f542edd647b8735575036b0be570a88b048c5ea97755f25dbddadf92ce3a4bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md",
      "size": 69065,
      "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md",
      "size": 132707,
      "sha256": "e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"
    },
    {
      "path": "docs/research/reference-runs/2026-10-29-advanced-03/run.json",
      "size": 127860,
      "sha256": "6abdb82bb54d9cd1a3d0a6089977cdfa1086c5cc484f27cc067e176626b16610"
    },
    {
      "path": "docs/research/reference-runs/2026-10-29-advanced-03/CMD51-207/MERGED.WP5",
      "size": 619,
      "sha256": "032ffe0a99168179a11a3d7bd2d2da743871a466aab1c60848259f0bb5701905"
    },
    {
      "path": "docs/research/reference-runs/2026-10-29-advanced-04/run.json",
      "size": 127860,
      "sha256": "ae9bc9fda6091903b04c07b2894c487074a4c01edec656667b8a75da8dbbceb8"
    },
    {
      "path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-207/MERGED.WP5",
      "size": 619,
      "sha256": "032ffe0a99168179a11a3d7bd2d2da743871a466aab1c60848259f0bb5701905"
    }
  ],
  "case_links": [
    {
      "case_id": "CMD51-111",
      "title": "Hard return ends a paragraph",
      "feature_ids": [
        "WP51-016"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 557,
          "printed_end": 560,
          "pdf_start": 574,
          "pdf_end": 577
        }
      ]
    },
    {
      "case_id": "CMD51-112",
      "title": "Insert a hard page break",
      "feature_ids": [
        "WP51-040"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 471,
          "printed_end": 473,
          "pdf_start": 488,
          "pdf_end": 490
        }
      ]
    },
    {
      "case_id": "CMD51-197",
      "title": "Distinguish native hard/soft returns and pages",
      "feature_ids": [
        "FMT51-004"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "SDK51",
          "printed_start": 19,
          "printed_end": 23,
          "pdf_start": 32,
          "pdf_end": 36
        }
      ]
    },
    {
      "case_id": "CMD51-162",
      "title": "Change left and right margins",
      "feature_ids": [
        "WP51-033"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 394,
          "printed_end": 395,
          "pdf_start": 411,
          "pdf_end": 412
        }
      ]
    },
    {
      "case_id": "CMD51-163",
      "title": "Change top and bottom margins",
      "feature_ids": [
        "WP51-033"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 396,
          "printed_end": 396,
          "pdf_start": 413,
          "pdf_end": 413
        }
      ]
    },
    {
      "case_id": "CMD51-101",
      "title": "Insert a normal tab",
      "feature_ids": [
        "WP51-035"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 631,
          "printed_end": 632,
          "pdf_start": 648,
          "pdf_end": 649
        }
      ]
    },
    {
      "case_id": "CMD51-103",
      "title": "Change tab settings at the cursor",
      "feature_ids": [
        "WP51-035"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 634,
          "printed_end": 639,
          "pdf_start": 651,
          "pdf_end": 656
        }
      ]
    },
    {
      "case_id": "CMD51-160",
      "title": "Set initial base font from selected printer resources",
      "feature_ids": [
        "WP51-031"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 205,
          "printed_end": 208,
          "pdf_start": 222,
          "pdf_end": 225
        }
      ]
    },
    {
      "case_id": "CMD51-161",
      "title": "Toggle printer kerning at cursor",
      "feature_ids": [
        "WP51-031"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 303,
          "printed_end": 303,
          "pdf_start": 320,
          "pdf_end": 320
        }
      ]
    },
    {
      "case_id": "CMD51-145",
      "title": "Direct original printer output to a disk file",
      "feature_ids": [
        "WP51-074"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 543,
          "printed_end": 543,
          "pdf_start": 560,
          "pdf_end": 560
        }
      ]
    },
    {
      "case_id": "CMD51-146",
      "title": "Preview each original page-view mode",
      "feature_ids": [
        "WP51-076"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 701,
          "printed_end": 704,
          "pdf_start": 718,
          "pdf_end": 721
        }
      ]
    },
    {
      "case_id": "CMD51-147",
      "title": "Changing preview colors does not change printed content",
      "feature_ids": [
        "WP51-076"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 702,
          "printed_end": 702,
          "pdf_start": 719,
          "pdf_end": 719
        }
      ]
    },
    {
      "case_id": "CMD51-185",
      "title": "Select an installed original printer definition",
      "feature_ids": [
        "WP51-071"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 506,
          "printed_end": 509,
          "pdf_start": 523,
          "pdf_end": 526
        }
      ]
    },
    {
      "case_id": "CMD51-165",
      "title": "Choose page-number position",
      "feature_ids": [
        "WP51-041"
      ],
      "oracle_status": "not-run",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 474,
          "printed_end": 478,
          "pdf_start": 491,
          "pdf_end": 495
        }
      ]
    },
    {
      "case_id": "CMD51-207",
      "title": "Default merge inserts a page break between records",
      "feature_ids": [
        "WP51-062"
      ],
      "oracle_status": "partially-observed",
      "source_locators": [
        {
          "source_id": "REF51",
          "printed_start": 420,
          "printed_end": 420,
          "pdf_start": 437,
          "pdf_end": 437
        },
        {
          "source_id": "REF51",
          "printed_start": 423,
          "printed_end": 423,
          "pdf_start": 440,
          "pdf_end": 440
        },
        {
          "source_id": "REF51",
          "printed_start": 847,
          "printed_end": 847,
          "pdf_start": 864,
          "pdf_end": 864
        },
        {
          "source_id": "SDK51",
          "printed_start": 17,
          "printed_end": 18,
          "pdf_start": 30,
          "pdf_end": 31
        },
        {
          "source_id": "SDK51",
          "printed_start": 55,
          "printed_end": 55,
          "pdf_start": 68,
          "pdf_end": 68
        }
      ]
    }
  ],
  "original_evidence": [
    {
      "case_id": "CMD51-207",
      "run_manifest": "docs/research/reference-runs/2026-10-29-advanced-03/run.json",
      "path": "docs/research/reference-runs/2026-10-29-advanced-03/CMD51-207/MERGED.WP5",
      "sha256": "032ffe0a99168179a11a3d7bd2d2da743871a466aab1c60848259f0bb5701905",
      "size": 619
    },
    {
      "case_id": "CMD51-207",
      "run_manifest": "docs/research/reference-runs/2026-10-29-advanced-04/run.json",
      "path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-207/MERGED.WP5",
      "sha256": "032ffe0a99168179a11a3d7bd2d2da743871a466aab1c60848259f0bb5701905",
      "size": 619
    }
  ],
  "recipe_cases": {
    "L1": [
      "CMD51-111",
      "CMD51-197"
    ],
    "L2": [
      "CMD51-112",
      "CMD51-197",
      "CMD51-165"
    ],
    "L3": [
      "CMD51-162",
      "CMD51-163"
    ],
    "L4": [
      "CMD51-101",
      "CMD51-103"
    ],
    "L5": [
      "CMD51-160",
      "CMD51-161",
      "CMD51-185"
    ],
    "L6": [
      "CMD51-145"
    ],
    "L7": [
      "CMD51-146",
      "CMD51-147"
    ]
  }
}
```
<!-- WP07_AUDIT_END -->

```sh
python3 - <<'PY_AUDIT'
from pathlib import Path
import hashlib, json, re, subprocess
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md')
t = p.read_text()
a = json.loads(t.split('<!-- WP07_AUDIT_BEGIN -->',1)[1].split('```json\n',1)[1].split('\n```',1)[0])
sha = lambda b: hashlib.sha256(b).hexdigest()
for x in a['inputs']:
    b = Path(x['path']).read_bytes()
    assert (len(b),sha(b)) == (x['size'],x['sha256']), x['path']
cases = {x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
features = {x['id']:x for x in json.loads(Path('docs/research/feature-inventory.json').read_text())}
sources = {x['id']:x for x in json.loads(Path('docs/research/sources.json').read_text())}
assert set(re.findall(r'CMD51-\d{3}',t)) == {x['case_id'] for x in a['case_links']}
assert set(a['recipe_cases']) == {'L'+str(i) for i in range(1,8)}
for rid, ids in a['recipe_cases'].items():
    row = next(line for line in t.splitlines() if line.startswith('| '+rid+':'))
    assert re.findall(r'CMD51-\d{3}',row) == ids, rid
# Feature-specific expectations prevent a valid but unrelated case/title substitution.
required = {'L1':{'WP51-016','FMT51-004'},'L2':{'WP51-040','FMT51-004','WP51-041'},
            'L3':{'WP51-033'},'L4':{'WP51-035'},'L5':{'WP51-031','WP51-071'},
            'L6':{'WP51-074'},'L7':{'WP51-076'}}
for rid, ids in a['recipe_cases'].items():
    assert {g for cid in ids for g in cases[cid]['feature_ids']} == required[rid], rid
for x in a['case_links']:
    c = cases[x['case_id']]
    assert (x['title'],x['feature_ids'],x['oracle_status'],x['source_locators']) == (c['title'],c['feature_ids'],c['oracle_status'],c['source_locators'])
    assert '| '+x['case_id']+' ('+c['title']+') | '+', '.join(c['feature_ids'])+' | '+c['oracle_status']+' |' in t
    for f in x['feature_ids']:
        assert x['case_id'] in features[f]['command_scenario_ids']
    for loc in x['source_locators']:
        assert 1 <= loc['pdf_start'] <= loc['pdf_end'] <= sources[loc['source_id']]['pdf_pages']
        assert loc['pdf_start'] == loc['printed_start']+(17 if loc['source_id']=='REF51' else 13)
for sid in ('REF51','WB51','SDK51'):
    s = sources[sid]
    assert sha(Path('research/cache',s['filename']).read_bytes()) == s['sha256']
# Exact page extraction checks reject a wrong page even when numeric offsets agree.
for pdf,page,needle in [('WPDOS51Reference.pdf',411,'Margins, Left and Right'),('WPDOS51Reference.pdf',413,'Margins, Top and Bottom'),('WPDOS51Reference.pdf',560,'Printing to Disk'),('WPDOS51Reference.pdf',719,'View Document and the Printer'),('WP51DevelopersToolkit.pdf',15,'1/1200th of an inch')]:
    out = subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout','research/cache/'+pdf,'-'],text=True)
    assert needle in out, (pdf,page)
for e in a['original_evidence']:
    b = Path(e['path']).read_bytes()
    assert (len(b),sha(b)) == (e['size'],e['sha256'])
    r = json.loads(Path(e['run_manifest']).read_text())
    assert r['scope']=='original-reference-only' and not r['wordling_tested']
    c = next(x for x in r['results'] if x['case_id']==e['case_id'])
    assert any(x['path']==e['path'] and x['sha256']==sha(b) and x['size']==len(b) for x in c['evidence'])
    assert e['run_manifest'] in cases[e['case_id']]['evidence_paths']
assert Path(a['original_evidence'][0]['path']).read_bytes()==Path(a['original_evidence'][1]['path']).read_bytes()
print('WP07 pinned inputs, semantic links, source locators and bounded merge evidence valid')
PY_AUDIT
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp07-review.xml
```

Author validation: the embedded hash/semantic-link/page-locator/run-evidence audit
passes, as do both catalogue checks and the genuine regression runner (JUnit at
`/tmp/wp07-review.xml`). Go package discovery succeeds; build/test/vet are explicitly
skipped because this planning checkout has no Go packages. These skips do not test
separate approved code lanes. A negative audit replacing the L4 normal-tab lead
with a valid margin case is rejected by the recipe feature-association assertion.
No new original probe or Wordling differential test was run; all L recipes remain
unrun proposals, with blocked graphics/historical resources recorded above.
