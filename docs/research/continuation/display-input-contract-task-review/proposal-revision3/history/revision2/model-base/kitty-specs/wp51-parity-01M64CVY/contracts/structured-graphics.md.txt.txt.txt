# WP08 structured content and graphics contract map

Research handoff, 2026-10-30. Requirements FR-010 and FR-011; dependencies on
FR-008/009/015/016 and native FC-001–009 remain. This is a documentary map and
bounded probe proposal, not a decoded-format implementation or original-app
observation. Full original scope remains M1; PDF remains M2. WP12 owns executable
continuation packages. Authority is `spec.md`, `plan.md`, `research.md`,
`data-model.md`, `docs/compatibility.md`, `docs/roadmap.md` and approved WP01/04–07
contracts. No queue, canonical registry, raw evidence or production code is changed.

## Source and applicability boundary

The selected target remains plain U.S. English DOS WP5.1, Help03/09/92. The
fingerprinted QEMU/FreeDOS1.4 profile uses the mixed-date July1992 text-only
Standard Printer. It is not historical DOS, graphics preview or font-metric
acceptance evidence. The full WP07 `layout-resources.md` acquisition/profile,
units and **pre-test tolerance** requirements apply to every printed/preview
comparison below. There is no positional/pixel tolerance available to import.
Ready means a proposed original text/menu/native experiment can be scoped now;
it never means run, supported, or layout-verified.

REF51 is the 6/92 reference; WB51 the 11/89 workbook; SDK51 the 12/93 toolkit
with intermediate WP revision marks. Full hashes/editions are in the ledger and
source registry. Printed/PDF locators use inclusive **one-based PDF pages**:
REF printed Arabic+17; SDK WP subsection+13. SDK DR is its own subsection:
DR-1 is PDF204. Toolkit WPWin/VAX/UNIX/Intellitag extensions are version leads,
not automatic March DOS behavior. In particular D4/9 table display information
is labelled WPWin; D7/12 TeamLinks/VAX filename handling is not a plain-DOS
subdocument contract. Unknown valid extensions remain preserved or unsafe edits
refused, not silently translated to a guessed DOS equivalent.

## Native structure and original behavior map (T022/T023)

S identifiers below are local rows, not new feature/scenario IDs. Exact canonical
case titles and feature associations are recorded in each row; all selected cases
are **not-run**, implementation **not-implemented**. Parent groups marked studied
mean selected documentary study, not exhaustive command/field coverage. Native
entries are documentary leads for future field contracts, never claims that the
existing outer-framing reader decodes these structures.

| Row / family | Canonical feature and exact case leads | REF51 printed / PDF | Native structures / SDK locators | Original command and observable obligation |
| --- | --- | --- | --- | --- |
| S01: Styles | WP51-046 (Styles and definitions); CMD51-118 (Create and apply a named style); CMD51-119 (Reject a duplicate style name ignoring case) | 616–625 / 633–642 | Prefix style packets 0x100–0x1FF plus DB/0–3 body definitions/references; paired/global type, name/unique ID, beginning/ending text and Enter behavior. SDK WP-15–16,79–80 / PDF28–29,92–93. | Alt+F8 Create/On: named definitions and applied scope must survive native save/retrieve; case-insensitive duplicate-name refusal is separate from display formatting. |
| S02: Outlines | WP51-047 (Outlines and numbering); CMD51-171 (Create successive outline levels) | 449–468 / 466–485 | D9/4 Outline On, paragraph number definitions (D2/2), D8 paragraph numbers and style definitions; SDK WP-27,29,69–72,79–80 / PDF40,42,82–85,92–93. Outline style names have an internal prefix: not ordinary user text. | Shift+F5 Outline On: hierarchical level, sequence and following text must remain related through edits and regeneration. |
| S03: Table structure | WP51-048 (Tables and structural editing); CMD51-120 (Create a 2 by 2 table); CMD51-121 (Join selected table cells) | 640–664 / 657–681 | D2/11 Table Def; DC/0–2 cell/row/off at end of line; DD/1–3 page transitions; nested cell text, spans and row/border data. SDK WP-44–45,81–87 / PDF57–58,94–100. DA/1 is a graphics table box, not this cell grammar. | Alt+F7 Tables Create/Edit: row/cell navigation and join/split alter structure rather than padding a text grid. |
| S04: Table calculation | WP51-049 (Table formatting and calculations); CMD51-122 (Recalculate table formulas explicitly); CMD51-123 (Copy a formula to another cell) | 665–675 / 682–692 | DC/0 cell formula subgroup with signed relative cell references, formula flags and nested expression; D2/11 table settings and displayed/cached result text. SDK WP-44–45,81–82 / PDF57–58,94–95. Formula source is distinct from last calculated display. | Alt+F7 Table Edit Math Formula/Calculate/Copy Formula: REF671 states input formula calculates immediately, later input edits require recalculation; last result prints. |
| S05: Contents/list/index generation | WP51-050 (Generated contents, lists and index); CMD51-124 (Mark a contents heading at a declared level); CMD51-125 (Generate or decline replacing generated material) | 221–223 / 238–240; 287–291 / 304–308; 355–357 / 372–374; 682–685 / 699–702 | D7/0–2 marked text/definitions; D7/3 index heading/subheading; generated body material and page placeholders. SDK WP-64–65 / PDF77–78. Marks/definitions are not generated result text. | Alt+F5 ToC marking and Generate: replacement refusal preserves previous generated region; approval regenerates entries/order/page references. |
| S06: Authorities | WP51-051 (Table of authorities); CMD51-172 (Mark a full legal authority) | 676–681 / 693–698 | D7/2 definition plus D7/4 authority section and short/full form text. SDK WP-64–65 / PDF77–78. Preserve full/short correspondence and native marks. | Alt+F5 ToA Mark Full/Short and Generate: editor changes and section assignment determine generated authority entries, not merely a styled citation. |
| S07: Cross-references | WP51-089 (Cross-reference targets and generated references); CMD51-129 (Mark reference and target together); CMD51-130 (Mark a target separately with case-insensitive name matching) | 96–103 / 113–120 | D7/7 Auto Reference Definition and D7/8 tag with named target; D8/number styles and generated output depend on reference type. SDK WP-66–67 / PDF79–80. | Alt+F5 Cross-Ref marks reference/target then Generate; named relationship and generated page/paragraph/object identity must survive saves. |
| S08: Master/subdocuments | WP51-052 (Master documents and subdocuments); CMD51-126 (Insert a subdocument link) | 397–400 / 414–417 | D7/9 Include Subdocument plus D7/10 and11 expanded boundaries/filename data; nested content and external file relationship. SDK WP-67–68 / PDF80–81. | Alt+F5 Subdocument and Generate expand/condense: link lifecycle, relative path handling and changes to linked files are observable native behavior. |
| S09: Graphics boxes | WP51-055 (Graphics boxes, wrapping and captions); CMD51-174 (Create a figure graphics box) | 232–250 / 249–267 | DA/0–4 figure/table/text/user/equation boxes, D2/5–9 defaults, D3 box numbering and D4 formatter data. Embedded WPG uses packet8 count/size array; linked images retain filename relationship. SDK WP-12,43,74–76 / PDF25,56,87–89. | Alt+F9 Figure Create/Definition/Edit: anchors, content, size, position, caption and wrap are semantic state, independent of a terminal placeholder. |
| S10: Graphics conversion | WP51-056 (Graphics formats and conversion utility); CMD51-175 (Convert an original graphics file with GRAPHCNV) | 228–231 / 245–248; 251–256 / 268–273 | Standalone input format to WPG prefix/records, then optional packet8 image storage/reference. SDK DR-1–3 / PDF204–206 and WP-12 / PDF25; REF graphics conversion/formats sections distinguish import, temporary conversion and durable WPG output. | DOS GRAPHCNV input/output prompts and report; direct import and graphic-on-disk temporary conversion are separate workflows. |
| S11: Graphics rules/display | WP51-057 (Graphic rules and display options); CMD51-176 (Create a horizontal graphics line) | 257–268 / 274–285 | DA/5 horizontal and DA/6 vertical line structures carry geometry/stroke fields, separate from character-line drawing; graphics display settings affect presentation. SDK WP-77–78 / PDF90–91. | Alt+F9 Line Create Horizontal: measure line length, stroke, alignment and position in original printer/page units. |
| S12: Equations | WP51-058 (Equations and equation editor); CMD51-177 (Create and preview an equation fraction) | 163–193 / 180–210; 729–740 / 746–757 | DA/4 equation box plus DF/0 nested formula text and compact stream, font-size/alignment data; formatter/caption data separate. SDK WP-76–77,88 / PDF89–90,101. This is not generic text in a box. | Alt+F9 Equation Create/Edit, type expression, F9 View: source editing, saved compiled data and graphics/text print choices are distinct obligations. |
| S13: Dates | WP51-054 (Date values and codes); CMD51-127 (Insert literal current date); CMD51-128 (Insert a date code that updates on retrieval) | 109–112 / 126–129 | Literal date is document characters; date code is D8/0 function with format data and generated display. SDK WP-69 / PDF82. Preserve distinction during save/retrieve. | Shift+F5 Date Text/Code under controlled RTC and language settings. |
| S14: Labels/envelopes | WP51-053 (Labels and envelopes); CMD51-173 (Select a label paper definition) | 319–327 / 336–344; 771–772 / 788–789 | Paper/form geometry D0/11 and packet9 forms hashes are leads; logical label pages, offsets and printer definitions govern physical-sheet output. SDK WP-12,33–35 / PDF25,46–48. Envelope control may require distinct fields; no assertion all envelope data is D0/11. | Shift+F8 Page Paper Size/Type chooses available label/envelope definitions; sheet/feed/logical-page placement must be preserved. |
| S15: Notes | WP51-045 (Footnotes and endnotes); CMD51-115 (Create a footnote); CMD51-116 (Create an endnote); CMD51-117 (Configure note continuation constraints) | 209–216 / 226–233 | D6/0 footnote, D6/1 endnote nested text/options/number; D2/3–4 definitions and D7/5–6 endnote generation/page metadata. SDK WP-27,62–66 / PDF40,75–79. | Ctrl+F7 Create/Options and Generate: anchor, nested editing state, numbering, separation and continuation layout remain coupled. |
| S16: Column Math | WP51-064 (Column math and calculations); CMD51-180 (Enter and leave original column Math mode) | 401–414 / 418–431 | D2/0 math-column definitions/formulas plus original function/control codes and ordinary text/results; separate from DC cell formula subgroups despite related formula grammar. SDK WP-21,38 / PDF34,51. | Alt+F7 Math On/Calculate/Off controls original tab-based columns; function markers are not literal printed operators. |
| S17: Other original converters | WP51-061 (Original macro conversion utility); CMD51-179 (Convert a 4.x macro with MACROCNV) | 370–372 / 387–389 | MACROCNV produces original WPM, not graphics/WP document or a Wordling wrapper. Native automation grammar belongs to separate FR-012 research; REF370–372 / PDF387–389. | DOS MACROCNV with original 4.x input and original report; conversion losses/unconverted commands remain visible. |

The toolkit cell-formula page was visually checked (SDK WP-82/PDF95): row
reference offsets are signed with positive=up, negative=down; column offsets
positive=right, negative=left. This unusual convention must be tested with
nonzero offsets in each direction, not guessed from spreadsheet notation. Table
row data also distinguishes older versus newer border encodings. These findings
identify research risk; they are not a complete formula/border implementation.
Style packet names, style body names and outline internal names likewise need
original relationship fixtures before rewriting. Displayed table text or style
attributes cannot replace those identities.

WP01's initial packet8 rule accepts only zero graphics count. SDK WP-12/PDF25
indexes only a two-byte count, followed by the size array and image data; a
nonzero image extent cannot be inferred from index length2. Future decoding must
validate the whole array/images with checked arithmetic and ownership boundaries.
DA table boxes and DC/DD table row/cell functions must stay distinct; DF equation
source/compact stream is nested content, not arbitrary ASCII following a box.
SDK DR-1–3/PDF204–206 documents WPG applicability and prefix/record framing;
it does not establish support for every later WPG variant by the selected DOS app.
Its byte-order prose conflicts with the low/high-byte diagram; an actual fixture
and independent inspector must resolve fields before writing, rather than copying
that prose as an endian rule.

## Independently verifiable starters and retained scope (T024)

Every named fixture below is a **proposal identifier**, not an existing file/path
or hash claim. No new original probe is run by WP08, and no original structured
fixture is promoted from a plain/bold/merge fixture. All outputs must be produced
from project-authored inputs under the common protocol below before implementation.

| Row | Exact proposed starter / fixture | Prerequisites and readiness | Explicit deferred M1 obligations under the same feature |
| --- | --- | --- | --- |
| S01 | STYLE1: create paired WPTEST with Bold On beginning and Bold Off ending, apply to `Styled text`, turn style off and type ` plain`; save, retrieve, edit definition and inspect both spans. Separately attempt wptest duplicate. Capture actual type/Enter choices before scripting. | Text probe ready; semantic writer blocked on original before/after corpus and packet/body identity-link contract. | WP51-046: Global styles, Enter Off/Off-On, nested/adjacent application, library save/retrieve, replacement/deletion/collisions and library format interoperability. |
| S02 | OUTLN1: follow canonical First/Child level recipe; add a second top-level `Next`, save, retrieve, insert a peer before Child and record renumbering. Record selected outline scheme, start value and level keys; do not assume arbitrary Tab means nesting in every state. | Text probe ready after scheme/options capture; implementation needs number/style decoding and original update behavior. | WP51-047: All numbering definitions/restarts, skipped levels, multi-paragraph items, style editing, prefixes/suffixes, Enter/Tab behavior and cross-reference integration. |
| S03 | TABLE1: create 2x2 table, put A1/B1/A2/B2 marker text in matching cells, save before, join the top row through original Join prompts, save after, retrieve and inspect structure/content. Record precise selected span and retained-content result rather than assuming join concatenation. | Text structural probe ready; placement/borders await WP07 metrics. Decoder/writer needs lengths, row/page states, spans, nested text and unrelated-byte audit. | WP51-048: Insert/delete/move/copy/join/split, row height, header rows, cell locks, spanning pages, selection and failure/cancel branches. |
| S04 | TCALC1: use 2x2 table, A1=2, A2=3, B1 formula A1+A2; save initial, change A1 to 7 without Calculate and save, then explicitly Calculate and save. Copy B1 formula to B2 separately, inspect actual adjusted references/result. Expected arithmetic after Calculate is 10; original pre-calculate/cache behavior remains to be observed. | Text probe ready; implementation needs formula token grammar, signed relative addressing, numeric/locale/error and cache invalidation contract. | WP51-049: All functions/operators/rounding/errors, relative copy directions/ranges, formatting/shading/borders, decimal alignment and calculation scope; copy formula must not copy unrelated cell formatting. |
| S05 | GEN1: two headings `Alpha` and `Beta` separated by one explicit hard page; mark each ToC level1, define destination/options and generate. Change Alpha to Aardvark; decline replacement then approve in separate saves; inspect marks and output. Capture exact definition/destination prompts before automation. | Text generator probe ready with fixed text profile; number/position acceptance awaits WP07. Index/list have no dedicated mark-case in this selected lead pair; WP12 must author them. | WP51-050: Every contents/list/index definition, levels, leaders, sort/collation, concordance input, page ranges, multiple occurrences, regenerated regions and combined generation. |
| S06 | TOA1: project text `Example v Sample`, mark full in section1, assign short name EXAMPLE through original prompts; mark same short name on a second hard page, define destination and generate. Save marks/output; alter full form, regenerate. Record actual editor exit/short-form prompts before scripting. | Text probe ready after exact prompt capture; page references await accepted resource layout. Need definition/entry grammar and name-resolution error contract. | WP51-051: All sections, unmatched/duplicate short forms, edited full form, generation errors/asterisks, ordering/page ranges and interactions with index/contents. |
| S07 | XREF1: place reference before `See target`; hard page then `Target text`; Mark Both with Page type and name TARGET1. Save and generate; in separate fixture Mark Target target1 for existing TARGET1 reference; compare resolution. Move target behind one additional hard page and regenerate. | Text probe ready; implementation needs name rules/types/unknown-target errors and generated-region behavior; layout page result gated by WP07. | WP51-089: Separate/together marking, target-name conflicts/missing targets, every reference type and cross-document/generated/reference updates. |
| S08 | MASTER1: make own SUB1 native file containing `child text`; blank master `before`/link SUB1/`after`; save linked, expanded and condensed states using original commands. Reopen each with child present, then a copied run with child renamed; record error/cancel and source bytes. Expected no automatic hard page on initial link comes from manual only. | Text probe ready; original path/error behavior and multi-file save ownership must be captured before writes. WP06 DOS/Linux mapping applies. | WP51-052: Nested/recursive/missing/moved/changed subdocuments, cross-file generation and numbering, condensation edits and conflict/failure handling; no implicit flattening. |
| S09 | BOX1: project-owned WPG containing one rectangle (source prerequisite below); type `before` and `after` paragraphs, insert figure between at explicitly selected paragraph anchor, width 1 inch and captured wrap option, caption `Figure test`; save/retrieve, change width to 1.5 inch and save. Repeat linked/on-disk versus embedded as distinct variants only after exact options captured. | Blocked graphics acceptance: WP07 matched printer/fonts/graphics profile and bounded packet8/WPG decoder contract required; text UI observations alone are insufficient. | WP51-055: All box types/anchors/positions, aspect/scale/crop/rotation where documented, wrap/overlap, captions/numbering, defaults, embedded/linked ownership and nested structures. |
| S10 | CONVG1: create project-owned 8x8 monochrome PCX showing a border, after acquiring/pinning PCX header/RLE spec and independent validation; run GRAPHCNV to a new WPG filename, retain source/output/report. Separately test nonexistent input and unsupported ASCII bytes; inspect errors and source/output preservation, do not assume exit code semantics. | Blocked fixture prerequisite: no pinned PCX source-format contract or produced fixture selected here. Conversion metadata probe need not wait for printer; visual geometry comparison does. | WP51-056: Every documented supported format/variant, DXF standalone requirement, converter switches/batch/reporting/overwrite/color/scaling, import/on-disk differences, unsupported/malformed/resource-failure outputs. |
| S11 | RULE1: at top of blank page create horizontal rule length 1 inch with first explicitly named available plain style, capture actual thickness/alignment/baseline options; save/retrieve and change length to 2 inches. Capture native code and original preview/print stream. | Structural/UI probe possible; graphics fidelity blocked on WP07 profile and predeclared measurement/tolerance record. Decoder needs line fields and units, not screenshot tracing. | WP51-057: Vertical/column-relative rules, all line styles/weights/shading/position flags, graphics screen/display options and printer differences; text drawing remains separate WP51-037. |
| S12 | EQ1: type `{a times b} over c`, F9 view, return and save; reopen editor, replace c with d, save new native document and compare expression/compact stream. Capture original graphics and text print choices in separate fresh variants. | Text expression/menu probe possible if installed resources work; full preview/print blocked on matched resources. Compact-stream grammar and nesting/size limits remain research before semantic write. | WP51-058: Complete grammar/operators/symbols, nesting, errors, alignment/fonts, captions/numbering, editing controls, graphics/text modes and conversion of existing equations; appendix equations retained. |
| S13 | DATE1: fresh copies at 1992-03-09 insert Date Text and Date Code separately using captured same date format; save, reopen copies with RTC 1992-03-10; compare literal versus updating form and native bytes. Original formatting/retrieval rules remain unobserved. | Text probe ready, isolate RTC and locale; implementation needs date-format/source versus rendered-value contract. | WP51-054: All date formats/languages/custom layouts, stale/updated display timing, arithmetic/other clock cases and native no-edit preservation. |
| S14 | LABEL1: select captured original label definition, type `LABEL ONE` then original next-label boundary then `LABEL TWO`; save/retrieve/print. Record actual label width/height/count/gutters/feed. Envelopes remain separate probe: define exact paper/feed with original documented choices before creating fixture. | Blocked geometry/profile: no label/envelope printer definitions selected here. Native structure and input commands can be researched independently; require original geometry capture before implementation. | WP51-053: Every label/paper definition, repeated labels, sheet boundaries, envelope addresses/orientation/feed and failures. REF771–772/PDF788–789 describes the MACROS keyboard Ctrl-e envelope helper; its alternate-keyboard behavior needs separate applicability study, not assignment to the Original keyboard. |
| S15 | NOTE1: type `Body`, create footnote `Note text`, return to body and save/retrieve; separate fixture endnote `End note text` with captured placement/Generate steps. One long note variant later crosses a declared page under matched metrics. | Text nesting probe ready; continuation and placement acceptance blocked on WP07. Need nested token boundaries and independent note/options relationship decoder. | WP51-045: All note numbering/characters, separators/options, continuation constraints, endnote placement/regeneration, cross-page nested content and failures. |
| S16 | MATH1: explicit tab stop 1 inch from left margin, turn Math on, enter column rows 2 then 3 then original subtotal function +, Calculate, save; leave Math and type ordinary + outside scope, save/retrieve. Capture exact number/operator insertion and result; expected arithmetic subtotal 5, print/operator visibility still unobserved. | Text probe ready after tab/column roles and menu capture; numeric grammar/format/error/rounding and scope decoder needed before implementation. | WP51-064: All column roles, formula/functions, subtotal/total/grand-total, range scope, precision/negative formats, editing/recalculation and all math errors. |
| S17 | CONVM1: acquire a provenance-cleared project-authored original 4.x macro that inserts X; pin original-format spec and source bytes before execution. Run conversion beside absent same-stem WPM, inspect report and replay converted output in WP; source remains intact. | Blocked input-format fixture prerequisite; no 4.x fixture or complete format contract is selected here. WP06 owns general conversion/path behavior; automation researcher owns token execution. | WP51-061: All supported legacy macro variants/commands/options, partial conversion reports, conflicts/overwrite/error behavior; CONVERT text/native modes remain WP51-079 and WP51-026 under WP06. |

For BOX1, author a minimal original-format WPG rectangle only after freezing the
SDK DR prefix/record/version subset and independently checking dimensions,
record lengths, end markers and encoding; feed it to original WP and keep the
original accepted file as evidence. This is a synthetic source fixture until
original retrieval is observed. CONVG1's PCX must have its own pinned external
format specification and independently checked header/plane/RLE bytes; WPG
output inspection is not validation of the PCX input. Neither source exists here.
Bundled graphics are not substitutes for redistributable project-owned fixtures.

REF51 228–231/PDF245–248 and251–256/PDF268–273 distinguish durable GRAPHCNV
conversion from temporary graphic-on-disk conversion, which leaves source intact.
The documented format list includes CGM, DHP, DXF, EPS, GEM, HPGL, IMG, MSP, PIC,
PNTG, PPIC, TIFF and WPG as well as PCX; each variant/conversion limit stays under
WP51-056. DXF requires standalone conversion. A tiny PCX success would establish
only its declared variant. Font/display resource selection remains under
WP51-031/005/071/073, original printer utilities and original print-to-disk under
WP51-073/074/070, not silently replaced by a modern renderer. MACROCNV is the
WP51-061 adjacent converter lead; text/native CONVERT modes under WP51-026/079
remain in WP06. The toolkit's DUMPWPG is an optional external inspector needing
lawful acquisition/fingerprinting, not a new required product dependency.

FR-010 also retains paper/numbering WP51-041, keeps WP51-042, columns WP51-043,
headers/footers WP51-044, notes WP51-045 and all their combinations with the rows
above; WP07 covers layout-resource prerequisites rather than implementing them.
Date and label/envelope rows are explicit, despite being smaller than the main
structured families. WP51-037 line-drawing characters stay distinct from graphics
rules. Cross-references WP51-089 are not reduced to generated contents WP51-050.
Workbook lessons remain not-run as lessons; WP05 retains complete contents-level
coverage and step-decomposition work. No selected starter closes its parent group.

## Common probe protocol and implementation prerequisites

1. Freeze one row revision, canonical case expansion and inputs/settings before
   execution. For undocumented branches, first capture exact menus/prompts with
   bounded scratch sessions; do not silently invent command sequences. When no
   dedicated case exists (index/list marks, some envelope and box variants), WP12
   must author a canonical linked case before using it as acceptance evidence.
   A shared Generate case is not an observed index, authority or reference case.
2. Fingerprint resources/EXE/FIL/DRS, setup, converters and equation/display tools
   actually used. `installed-files.json` is an availability/identity register,
   not proof utility/font/graphics functionality was exercised. Acquire licensed
   missing resources privately under WP07. Record no-resource failures separately.
3. Run two fresh-copy original repetitions with exact original keyboard/menu
   state, RTC, locale, printer/font profile and declared native input. Capture
   before/after nested editor state, Reveal Codes, command prompts/cancel/errors,
   source/companion/native outputs, raw original print stream and preview state as
   applicable. Exit/save completion must be captured before exporting bytes.
   Record output sizes/SHA-256 in immutable run manifests with archived runner,
   resource identity and original-only scope. No normalization of raw data.
4. Independently inspect prefix/index ownership, typed payload lengths and nested
   boundaries, paired relationships, formula/mark/definition identities and
   linked-file paths. Explain formatter/hash/offset updates separately from
   authored content. Preserve unknown packet/code bytes and cross-references;
   outer framing alone establishes no editable nested grammar. Refuse unsupported
   edits before mutation until all affected relationships are understood.
5. Before each implementation slice, publish a bounded field/token contract with
   version applicability, signedness/units, enum meaning, nested ownership,
   invalidation rules, preservation/refusal behavior and original fixture hashes.
   Add malformed/truncated/length-overflow/invalid-reference/cycle/unsupported-
   version tests appropriate to that structure and a measured bounded fuzz budget.
   Do not reuse WP01's depth0 validation as proof of nested payload safety.
6. Separate test layers: native no-edit exact bytes (FC-002); targeted semantic edit
   with unrelated data preserved (FC-003/004); command/state correctness; generated
   entry/calculation/source correctness; layout/print/preview with WP07 resources
   and any evidence-derived tolerance frozen before differential runs. Formula
   evaluation is not printing a cached number; regenerated references need actual
   marks/definitions and page computation. Writers must pass original retrieve,
   edit, print, save and Wordling reopen checks for the supported slice. No shapes
   drawn in the TUI count as graphics/equation/native interoperability acceptance.

## Decision-ready continuation for WP12

First obtain original text/native control fixtures for S01–S08 and S13/S15/S16;
prioritize S03's four-cell structure and S04's explicit-recalculation sequence as
independent boundaries after style/number nesting research. Their menu/native
questions need not await historical DOS or graphics printer acquisition. Keep
resource qualification and original graphical evidence as separate acquisition
work for S09–S12/S14. Converters S10/S17 need licensed/owned input-format fixtures
and complete source specifications first; their byte/report behavior can be
studied without claiming printer fidelity.

Then author separate bounded decoder/state-command, semantic writer,
generation/calculation and layout/output implementation packages from accepted
contracts. Each package gets exact source/fixture/profile links, malformed/unsafe
refusal cases and independent original comparisons. Avoid a single omnibus
structured-content writer before those contracts exist. Implementer/reviewer
roles remain separate; no research completion promotes a feature to implemented
or verified. Every deferred cell above and the adjacent IDs remain in M1 until
reviewed follow-up evidence closes it or an explicit owner decision changes scope.

## Reproducible audit ledger

Paths are repository-relative. Ignored PDFs/text must be acquired at their pinned
source URL/hash when absent; proprietary contents are not embedded here.

<!-- WP08_AUDIT_BEGIN -->
```json
{
  "source_inputs": [
    {
      "path": "docs/research/sources.json",
      "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"
    },
    {
      "path": "docs/research/feature-inventory.json",
      "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"
    },
    {
      "path": "docs/research/command-scenarios.json",
      "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"
    },
    {
      "path": "docs/research/reference-baseline.json",
      "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"
    },
    {
      "path": "docs/research/reference-environment/installed-files.json",
      "sha256": "a8532ce5be7caa5759799841c8c0e3128810f7631f49101978102244139a1238"
    },
    {
      "path": "docs/research/reference-environment/environment.json",
      "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"
    },
    {
      "path": "docs/research/reference-environment/resource-profile.json",
      "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"
    },
    {
      "path": "research/cache/WPDOS51Reference.pdf",
      "sha256": "ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531"
    },
    {
      "path": "research/cache/WPDOS51Workbook.pdf",
      "sha256": "868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d"
    },
    {
      "path": "research/cache/WP51DevelopersToolkit.pdf",
      "sha256": "5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754"
    },
    {
      "path": "research/cache/reference.txt",
      "sha256": "f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c"
    },
    {
      "path": "research/cache/workbook.txt",
      "sha256": "4a99b406886f1e128ab673c9cefddc83ca9f53ddbc8dcfd621e38b7afe79ecce"
    },
    {
      "path": "research/cache/toolkit.txt",
      "sha256": "8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md",
      "sha256": "e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md",
      "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json",
      "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/editing.md",
      "sha256": "7f542edd647b8735575036b0be570a88b048c5ea97755f25dbddadf92ce3a4bd"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md",
      "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"
    },
    {
      "path": "kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md",
      "sha256": "aa6384662a74c1c0451a506bd9fdd169420614c558677a40715fbe0bab906631"
    }
  ],
  "rows": [
    {
      "id": "S01",
      "title": "Styles",
      "feature_id": "WP51-046",
      "feature_title": "Styles and definitions",
      "locators": [
        {
          "printed_start": 616,
          "printed_end": 625,
          "pdf_start": 633,
          "pdf_end": 642
        }
      ],
      "case_links": [
        {
          "id": "CMD51-118",
          "title": "Create and apply a named style",
          "feature_ids": [
            "WP51-046"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 621,
              "printed_end": 625,
              "pdf_start": 638,
              "pdf_end": 642
            }
          ]
        },
        {
          "id": "CMD51-119",
          "title": "Reject a duplicate style name ignoring case",
          "feature_ids": [
            "WP51-046"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 621,
              "printed_end": 621,
              "pdf_start": 638,
              "pdf_end": 638
            }
          ]
        }
      ],
      "native": "Prefix style packets 0x100\u20130x1FF plus DB/0\u20133 body definitions/references; paired/global type, name/unique ID, beginning/ending text and Enter behavior. SDK WP-15\u201316,79\u201380 / PDF28\u201329,92\u201393.",
      "command": "Alt+F8 Create/On: named definitions and applied scope must survive native save/retrieve; case-insensitive duplicate-name refusal is separate from display formatting.",
      "probe": "STYLE1: create paired WPTEST with Bold On beginning and Bold Off ending, apply to `Styled text`, turn style off and type ` plain`; save, retrieve, edit definition and inspect both spans. Separately attempt wptest duplicate. Capture actual type/Enter choices before scripting.",
      "readiness": "Text probe ready; semantic writer blocked on original before/after corpus and packet/body identity-link contract.",
      "deferred": "Global styles, Enter Off/Off-On, nested/adjacent application, library save/retrieve, replacement/deletion/collisions and library format interoperability."
    },
    {
      "id": "S02",
      "title": "Outlines",
      "feature_id": "WP51-047",
      "feature_title": "Outlines and numbering",
      "locators": [
        {
          "printed_start": 449,
          "printed_end": 468,
          "pdf_start": 466,
          "pdf_end": 485
        }
      ],
      "case_links": [
        {
          "id": "CMD51-171",
          "title": "Create successive outline levels",
          "feature_ids": [
            "WP51-047"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 451,
              "printed_end": 455,
              "pdf_start": 468,
              "pdf_end": 472
            }
          ]
        }
      ],
      "native": "D9/4 Outline On, paragraph number definitions (D2/2), D8 paragraph numbers and style definitions; SDK WP-27,29,69\u201372,79\u201380 / PDF40,42,82\u201385,92\u201393. Outline style names have an internal prefix: not ordinary user text.",
      "command": "Shift+F5 Outline On: hierarchical level, sequence and following text must remain related through edits and regeneration.",
      "probe": "OUTLN1: follow canonical First/Child level recipe; add a second top-level `Next`, save, retrieve, insert a peer before Child and record renumbering. Record selected outline scheme, start value and level keys; do not assume arbitrary Tab means nesting in every state.",
      "readiness": "Text probe ready after scheme/options capture; implementation needs number/style decoding and original update behavior.",
      "deferred": "All numbering definitions/restarts, skipped levels, multi-paragraph items, style editing, prefixes/suffixes, Enter/Tab behavior and cross-reference integration."
    },
    {
      "id": "S03",
      "title": "Table structure",
      "feature_id": "WP51-048",
      "feature_title": "Tables and structural editing",
      "locators": [
        {
          "printed_start": 640,
          "printed_end": 664,
          "pdf_start": 657,
          "pdf_end": 681
        }
      ],
      "case_links": [
        {
          "id": "CMD51-120",
          "title": "Create a 2 by 2 table",
          "feature_ids": [
            "WP51-048"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 640,
              "printed_end": 643,
              "pdf_start": 657,
              "pdf_end": 660
            }
          ]
        },
        {
          "id": "CMD51-121",
          "title": "Join selected table cells",
          "feature_ids": [
            "WP51-048"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 651,
              "printed_end": 664,
              "pdf_start": 668,
              "pdf_end": 681
            }
          ]
        }
      ],
      "native": "D2/11 Table Def; DC/0\u20132 cell/row/off at end of line; DD/1\u20133 page transitions; nested cell text, spans and row/border data. SDK WP-44\u201345,81\u201387 / PDF57\u201358,94\u2013100. DA/1 is a graphics table box, not this cell grammar.",
      "command": "Alt+F7 Tables Create/Edit: row/cell navigation and join/split alter structure rather than padding a text grid.",
      "probe": "TABLE1: create 2x2 table, put A1/B1/A2/B2 marker text in matching cells, save before, join the top row through original Join prompts, save after, retrieve and inspect structure/content. Record precise selected span and retained-content result rather than assuming join concatenation.",
      "readiness": "Text structural probe ready; placement/borders await WP07 metrics. Decoder/writer needs lengths, row/page states, spans, nested text and unrelated-byte audit.",
      "deferred": "Insert/delete/move/copy/join/split, row height, header rows, cell locks, spanning pages, selection and failure/cancel branches."
    },
    {
      "id": "S04",
      "title": "Table calculation",
      "feature_id": "WP51-049",
      "feature_title": "Table formatting and calculations",
      "locators": [
        {
          "printed_start": 665,
          "printed_end": 675,
          "pdf_start": 682,
          "pdf_end": 692
        }
      ],
      "case_links": [
        {
          "id": "CMD51-122",
          "title": "Recalculate table formulas explicitly",
          "feature_ids": [
            "WP51-049"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 671,
              "printed_end": 671,
              "pdf_start": 688,
              "pdf_end": 688
            }
          ]
        },
        {
          "id": "CMD51-123",
          "title": "Copy a formula to another cell",
          "feature_ids": [
            "WP51-049"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 671,
              "printed_end": 672,
              "pdf_start": 688,
              "pdf_end": 689
            }
          ]
        }
      ],
      "native": "DC/0 cell formula subgroup with signed relative cell references, formula flags and nested expression; D2/11 table settings and displayed/cached result text. SDK WP-44\u201345,81\u201382 / PDF57\u201358,94\u201395. Formula source is distinct from last calculated display.",
      "command": "Alt+F7 Table Edit Math Formula/Calculate/Copy Formula: REF671 states input formula calculates immediately, later input edits require recalculation; last result prints.",
      "probe": "TCALC1: use 2x2 table, A1=2, A2=3, B1 formula A1+A2; save initial, change A1 to 7 without Calculate and save, then explicitly Calculate and save. Copy B1 formula to B2 separately, inspect actual adjusted references/result. Expected arithmetic after Calculate is 10; original pre-calculate/cache behavior remains to be observed.",
      "readiness": "Text probe ready; implementation needs formula token grammar, signed relative addressing, numeric/locale/error and cache invalidation contract.",
      "deferred": "All functions/operators/rounding/errors, relative copy directions/ranges, formatting/shading/borders, decimal alignment and calculation scope; copy formula must not copy unrelated cell formatting."
    },
    {
      "id": "S05",
      "title": "Contents/list/index generation",
      "feature_id": "WP51-050",
      "feature_title": "Generated contents, lists and index",
      "locators": [
        {
          "printed_start": 221,
          "printed_end": 223,
          "pdf_start": 238,
          "pdf_end": 240
        },
        {
          "printed_start": 287,
          "printed_end": 291,
          "pdf_start": 304,
          "pdf_end": 308
        },
        {
          "printed_start": 355,
          "printed_end": 357,
          "pdf_start": 372,
          "pdf_end": 374
        },
        {
          "printed_start": 682,
          "printed_end": 685,
          "pdf_start": 699,
          "pdf_end": 702
        }
      ],
      "case_links": [
        {
          "id": "CMD51-124",
          "title": "Mark a contents heading at a declared level",
          "feature_ids": [
            "WP51-050"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 685,
              "printed_end": 685,
              "pdf_start": 702,
              "pdf_end": 702
            }
          ]
        },
        {
          "id": "CMD51-125",
          "title": "Generate or decline replacing generated material",
          "feature_ids": [
            "WP51-050"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 221,
              "printed_end": 221,
              "pdf_start": 238,
              "pdf_end": 238
            }
          ]
        }
      ],
      "native": "D7/0\u20132 marked text/definitions; D7/3 index heading/subheading; generated body material and page placeholders. SDK WP-64\u201365 / PDF77\u201378. Marks/definitions are not generated result text.",
      "command": "Alt+F5 ToC marking and Generate: replacement refusal preserves previous generated region; approval regenerates entries/order/page references.",
      "probe": "GEN1: two headings `Alpha` and `Beta` separated by one explicit hard page; mark each ToC level1, define destination/options and generate. Change Alpha to Aardvark; decline replacement then approve in separate saves; inspect marks and output. Capture exact definition/destination prompts before automation.",
      "readiness": "Text generator probe ready with fixed text profile; number/position acceptance awaits WP07. Index/list have no dedicated mark-case in this selected lead pair; WP12 must author them.",
      "deferred": "Every contents/list/index definition, levels, leaders, sort/collation, concordance input, page ranges, multiple occurrences, regenerated regions and combined generation."
    },
    {
      "id": "S06",
      "title": "Authorities",
      "feature_id": "WP51-051",
      "feature_title": "Table of authorities",
      "locators": [
        {
          "printed_start": 676,
          "printed_end": 681,
          "pdf_start": 693,
          "pdf_end": 698
        }
      ],
      "case_links": [
        {
          "id": "CMD51-172",
          "title": "Mark a full legal authority",
          "feature_ids": [
            "WP51-051"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 679,
              "printed_end": 681,
              "pdf_start": 696,
              "pdf_end": 698
            }
          ]
        }
      ],
      "native": "D7/2 definition plus D7/4 authority section and short/full form text. SDK WP-64\u201365 / PDF77\u201378. Preserve full/short correspondence and native marks.",
      "command": "Alt+F5 ToA Mark Full/Short and Generate: editor changes and section assignment determine generated authority entries, not merely a styled citation.",
      "probe": "TOA1: project text `Example v Sample`, mark full in section1, assign short name EXAMPLE through original prompts; mark same short name on a second hard page, define destination and generate. Save marks/output; alter full form, regenerate. Record actual editor exit/short-form prompts before scripting.",
      "readiness": "Text probe ready after exact prompt capture; page references await accepted resource layout. Need definition/entry grammar and name-resolution error contract.",
      "deferred": "All sections, unmatched/duplicate short forms, edited full form, generation errors/asterisks, ordering/page ranges and interactions with index/contents."
    },
    {
      "id": "S07",
      "title": "Cross-references",
      "feature_id": "WP51-089",
      "feature_title": "Cross-reference targets and generated references",
      "locators": [
        {
          "printed_start": 96,
          "printed_end": 103,
          "pdf_start": 113,
          "pdf_end": 120
        }
      ],
      "case_links": [
        {
          "id": "CMD51-129",
          "title": "Mark reference and target together",
          "feature_ids": [
            "WP51-089"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 98,
              "printed_end": 99,
              "pdf_start": 115,
              "pdf_end": 116
            }
          ]
        },
        {
          "id": "CMD51-130",
          "title": "Mark a target separately with case-insensitive name matching",
          "feature_ids": [
            "WP51-089"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 99,
              "printed_end": 103,
              "pdf_start": 116,
              "pdf_end": 120
            }
          ]
        }
      ],
      "native": "D7/7 Auto Reference Definition and D7/8 tag with named target; D8/number styles and generated output depend on reference type. SDK WP-66\u201367 / PDF79\u201380.",
      "command": "Alt+F5 Cross-Ref marks reference/target then Generate; named relationship and generated page/paragraph/object identity must survive saves.",
      "probe": "XREF1: place reference before `See target`; hard page then `Target text`; Mark Both with Page type and name TARGET1. Save and generate; in separate fixture Mark Target target1 for existing TARGET1 reference; compare resolution. Move target behind one additional hard page and regenerate.",
      "readiness": "Text probe ready; implementation needs name rules/types/unknown-target errors and generated-region behavior; layout page result gated by WP07.",
      "deferred": "Separate/together marking, target-name conflicts/missing targets, every reference type and cross-document/generated/reference updates."
    },
    {
      "id": "S08",
      "title": "Master/subdocuments",
      "feature_id": "WP51-052",
      "feature_title": "Master documents and subdocuments",
      "locators": [
        {
          "printed_start": 397,
          "printed_end": 400,
          "pdf_start": 414,
          "pdf_end": 417
        }
      ],
      "case_links": [
        {
          "id": "CMD51-126",
          "title": "Insert a subdocument link",
          "feature_ids": [
            "WP51-052"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 397,
              "printed_end": 400,
              "pdf_start": 414,
              "pdf_end": 417
            }
          ]
        }
      ],
      "native": "D7/9 Include Subdocument plus D7/10 and11 expanded boundaries/filename data; nested content and external file relationship. SDK WP-67\u201368 / PDF80\u201381.",
      "command": "Alt+F5 Subdocument and Generate expand/condense: link lifecycle, relative path handling and changes to linked files are observable native behavior.",
      "probe": "MASTER1: make own SUB1 native file containing `child text`; blank master `before`/link SUB1/`after`; save linked, expanded and condensed states using original commands. Reopen each with child present, then a copied run with child renamed; record error/cancel and source bytes. Expected no automatic hard page on initial link comes from manual only.",
      "readiness": "Text probe ready; original path/error behavior and multi-file save ownership must be captured before writes. WP06 DOS/Linux mapping applies.",
      "deferred": "Nested/recursive/missing/moved/changed subdocuments, cross-file generation and numbering, condensation edits and conflict/failure handling; no implicit flattening."
    },
    {
      "id": "S09",
      "title": "Graphics boxes",
      "feature_id": "WP51-055",
      "feature_title": "Graphics boxes, wrapping and captions",
      "locators": [
        {
          "printed_start": 232,
          "printed_end": 250,
          "pdf_start": 249,
          "pdf_end": 267
        }
      ],
      "case_links": [
        {
          "id": "CMD51-174",
          "title": "Create a figure graphics box",
          "feature_ids": [
            "WP51-055"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 232,
              "printed_end": 245,
              "pdf_start": 249,
              "pdf_end": 262
            }
          ]
        }
      ],
      "native": "DA/0\u20134 figure/table/text/user/equation boxes, D2/5\u20139 defaults, D3 box numbering and D4 formatter data. Embedded WPG uses packet8 count/size array; linked images retain filename relationship. SDK WP-12,43,74\u201376 / PDF25,56,87\u201389.",
      "command": "Alt+F9 Figure Create/Definition/Edit: anchors, content, size, position, caption and wrap are semantic state, independent of a terminal placeholder.",
      "probe": "BOX1: project-owned WPG containing one rectangle (source prerequisite below); type `before` and `after` paragraphs, insert figure between at explicitly selected paragraph anchor, width 1 inch and captured wrap option, caption `Figure test`; save/retrieve, change width to 1.5 inch and save. Repeat linked/on-disk versus embedded as distinct variants only after exact options captured.",
      "readiness": "Blocked graphics acceptance: WP07 matched printer/fonts/graphics profile and bounded packet8/WPG decoder contract required; text UI observations alone are insufficient.",
      "deferred": "All box types/anchors/positions, aspect/scale/crop/rotation where documented, wrap/overlap, captions/numbering, defaults, embedded/linked ownership and nested structures."
    },
    {
      "id": "S10",
      "title": "Graphics conversion",
      "feature_id": "WP51-056",
      "feature_title": "Graphics formats and conversion utility",
      "locators": [
        {
          "printed_start": 228,
          "printed_end": 231,
          "pdf_start": 245,
          "pdf_end": 248
        },
        {
          "printed_start": 251,
          "printed_end": 256,
          "pdf_start": 268,
          "pdf_end": 273
        }
      ],
      "case_links": [
        {
          "id": "CMD51-175",
          "title": "Convert an original graphics file with GRAPHCNV",
          "feature_ids": [
            "WP51-056"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 228,
              "printed_end": 231,
              "pdf_start": 245,
              "pdf_end": 248
            }
          ]
        }
      ],
      "native": "Standalone input format to WPG prefix/records, then optional packet8 image storage/reference. SDK DR-1\u20133 / PDF204\u2013206 and WP-12 / PDF25; REF graphics conversion/formats sections distinguish import, temporary conversion and durable WPG output.",
      "command": "DOS GRAPHCNV input/output prompts and report; direct import and graphic-on-disk temporary conversion are separate workflows.",
      "probe": "CONVG1: create project-owned 8x8 monochrome PCX showing a border, after acquiring/pinning PCX header/RLE spec and independent validation; run GRAPHCNV to a new WPG filename, retain source/output/report. Separately test nonexistent input and unsupported ASCII bytes; inspect errors and source/output preservation, do not assume exit code semantics.",
      "readiness": "Blocked fixture prerequisite: no pinned PCX source-format contract or produced fixture selected here. Conversion metadata probe need not wait for printer; visual geometry comparison does.",
      "deferred": "Every documented supported format/variant, DXF standalone requirement, converter switches/batch/reporting/overwrite/color/scaling, import/on-disk differences, unsupported/malformed/resource-failure outputs."
    },
    {
      "id": "S11",
      "title": "Graphics rules/display",
      "feature_id": "WP51-057",
      "feature_title": "Graphic rules and display options",
      "locators": [
        {
          "printed_start": 257,
          "printed_end": 268,
          "pdf_start": 274,
          "pdf_end": 285
        }
      ],
      "case_links": [
        {
          "id": "CMD51-176",
          "title": "Create a horizontal graphics line",
          "feature_ids": [
            "WP51-057"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 257,
              "printed_end": 260,
              "pdf_start": 274,
              "pdf_end": 277
            }
          ]
        }
      ],
      "native": "DA/5 horizontal and DA/6 vertical line structures carry geometry/stroke fields, separate from character-line drawing; graphics display settings affect presentation. SDK WP-77\u201378 / PDF90\u201391.",
      "command": "Alt+F9 Line Create Horizontal: measure line length, stroke, alignment and position in original printer/page units.",
      "probe": "RULE1: at top of blank page create horizontal rule length 1 inch with first explicitly named available plain style, capture actual thickness/alignment/baseline options; save/retrieve and change length to 2 inches. Capture native code and original preview/print stream.",
      "readiness": "Structural/UI probe possible; graphics fidelity blocked on WP07 profile and predeclared measurement/tolerance record. Decoder needs line fields and units, not screenshot tracing.",
      "deferred": "Vertical/column-relative rules, all line styles/weights/shading/position flags, graphics screen/display options and printer differences; text drawing remains separate WP51-037."
    },
    {
      "id": "S12",
      "title": "Equations",
      "feature_id": "WP51-058",
      "feature_title": "Equations and equation editor",
      "locators": [
        {
          "printed_start": 163,
          "printed_end": 193,
          "pdf_start": 180,
          "pdf_end": 210
        },
        {
          "printed_start": 729,
          "printed_end": 740,
          "pdf_start": 746,
          "pdf_end": 757
        }
      ],
      "case_links": [
        {
          "id": "CMD51-177",
          "title": "Create and preview an equation fraction",
          "feature_ids": [
            "WP51-058"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 163,
              "printed_end": 166,
              "pdf_start": 180,
              "pdf_end": 183
            }
          ]
        }
      ],
      "native": "DA/4 equation box plus DF/0 nested formula text and compact stream, font-size/alignment data; formatter/caption data separate. SDK WP-76\u201377,88 / PDF89\u201390,101. This is not generic text in a box.",
      "command": "Alt+F9 Equation Create/Edit, type expression, F9 View: source editing, saved compiled data and graphics/text print choices are distinct obligations.",
      "probe": "EQ1: type `{a times b} over c`, F9 view, return and save; reopen editor, replace c with d, save new native document and compare expression/compact stream. Capture original graphics and text print choices in separate fresh variants.",
      "readiness": "Text expression/menu probe possible if installed resources work; full preview/print blocked on matched resources. Compact-stream grammar and nesting/size limits remain research before semantic write.",
      "deferred": "Complete grammar/operators/symbols, nesting, errors, alignment/fonts, captions/numbering, editing controls, graphics/text modes and conversion of existing equations; appendix equations retained."
    },
    {
      "id": "S13",
      "title": "Dates",
      "feature_id": "WP51-054",
      "feature_title": "Date values and codes",
      "locators": [
        {
          "printed_start": 109,
          "printed_end": 112,
          "pdf_start": 126,
          "pdf_end": 129
        }
      ],
      "case_links": [
        {
          "id": "CMD51-127",
          "title": "Insert literal current date",
          "feature_ids": [
            "WP51-054"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 109,
              "printed_end": 112,
              "pdf_start": 126,
              "pdf_end": 129
            }
          ]
        },
        {
          "id": "CMD51-128",
          "title": "Insert a date code that updates on retrieval",
          "feature_ids": [
            "WP51-054"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 110,
              "printed_end": 110,
              "pdf_start": 127,
              "pdf_end": 127
            }
          ]
        }
      ],
      "native": "Literal date is document characters; date code is D8/0 function with format data and generated display. SDK WP-69 / PDF82. Preserve distinction during save/retrieve.",
      "command": "Shift+F5 Date Text/Code under controlled RTC and language settings.",
      "probe": "DATE1: fresh copies at 1992-03-09 insert Date Text and Date Code separately using captured same date format; save, reopen copies with RTC 1992-03-10; compare literal versus updating form and native bytes. Original formatting/retrieval rules remain unobserved.",
      "readiness": "Text probe ready, isolate RTC and locale; implementation needs date-format/source versus rendered-value contract.",
      "deferred": "All date formats/languages/custom layouts, stale/updated display timing, arithmetic/other clock cases and native no-edit preservation."
    },
    {
      "id": "S14",
      "title": "Labels/envelopes",
      "feature_id": "WP51-053",
      "feature_title": "Labels and envelopes",
      "locators": [
        {
          "printed_start": 319,
          "printed_end": 327,
          "pdf_start": 336,
          "pdf_end": 344
        },
        {
          "printed_start": 771,
          "printed_end": 772,
          "pdf_start": 788,
          "pdf_end": 789
        }
      ],
      "case_links": [
        {
          "id": "CMD51-173",
          "title": "Select a label paper definition",
          "feature_ids": [
            "WP51-053"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 319,
              "printed_end": 327,
              "pdf_start": 336,
              "pdf_end": 344
            }
          ]
        }
      ],
      "native": "Paper/form geometry D0/11 and packet9 forms hashes are leads; logical label pages, offsets and printer definitions govern physical-sheet output. SDK WP-12,33\u201335 / PDF25,46\u201348. Envelope control may require distinct fields; no assertion all envelope data is D0/11.",
      "command": "Shift+F8 Page Paper Size/Type chooses available label/envelope definitions; sheet/feed/logical-page placement must be preserved.",
      "probe": "LABEL1: select captured original label definition, type `LABEL ONE` then original next-label boundary then `LABEL TWO`; save/retrieve/print. Record actual label width/height/count/gutters/feed. Envelopes remain separate probe: define exact paper/feed with original documented choices before creating fixture.",
      "readiness": "Blocked geometry/profile: no label/envelope printer definitions selected here. Native structure and input commands can be researched independently; require original geometry capture before implementation.",
      "deferred": "Every label/paper definition, repeated labels, sheet boundaries, envelope addresses/orientation/feed and failures. REF771–772/PDF788–789 describes the MACROS keyboard Ctrl-e envelope helper; its alternate-keyboard behavior needs separate applicability study, not assignment to the Original keyboard."
    },
    {
      "id": "S15",
      "title": "Notes",
      "feature_id": "WP51-045",
      "feature_title": "Footnotes and endnotes",
      "locators": [
        {
          "printed_start": 209,
          "printed_end": 216,
          "pdf_start": 226,
          "pdf_end": 233
        }
      ],
      "case_links": [
        {
          "id": "CMD51-115",
          "title": "Create a footnote",
          "feature_ids": [
            "WP51-045"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 209,
              "printed_end": 211,
              "pdf_start": 226,
              "pdf_end": 228
            }
          ]
        },
        {
          "id": "CMD51-116",
          "title": "Create an endnote",
          "feature_ids": [
            "WP51-045"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 209,
              "printed_end": 214,
              "pdf_start": 226,
              "pdf_end": 231
            }
          ]
        },
        {
          "id": "CMD51-117",
          "title": "Configure note continuation constraints",
          "feature_ids": [
            "WP51-045"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 215,
              "printed_end": 216,
              "pdf_start": 232,
              "pdf_end": 233
            }
          ]
        }
      ],
      "native": "D6/0 footnote, D6/1 endnote nested text/options/number; D2/3\u20134 definitions and D7/5\u20136 endnote generation/page metadata. SDK WP-27,62\u201366 / PDF40,75\u201379.",
      "command": "Ctrl+F7 Create/Options and Generate: anchor, nested editing state, numbering, separation and continuation layout remain coupled.",
      "probe": "NOTE1: type `Body`, create footnote `Note text`, return to body and save/retrieve; separate fixture endnote `End note text` with captured placement/Generate steps. One long note variant later crosses a declared page under matched metrics.",
      "readiness": "Text nesting probe ready; continuation and placement acceptance blocked on WP07. Need nested token boundaries and independent note/options relationship decoder.",
      "deferred": "All note numbering/characters, separators/options, continuation constraints, endnote placement/regeneration, cross-page nested content and failures."
    },
    {
      "id": "S16",
      "title": "Column Math",
      "feature_id": "WP51-064",
      "feature_title": "Column math and calculations",
      "locators": [
        {
          "printed_start": 401,
          "printed_end": 414,
          "pdf_start": 418,
          "pdf_end": 431
        }
      ],
      "case_links": [
        {
          "id": "CMD51-180",
          "title": "Enter and leave original column Math mode",
          "feature_ids": [
            "WP51-064"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 401,
              "printed_end": 405,
              "pdf_start": 418,
              "pdf_end": 422
            }
          ]
        }
      ],
      "native": "D2/0 math-column definitions/formulas plus original function/control codes and ordinary text/results; separate from DC cell formula subgroups despite related formula grammar. SDK WP-21,38 / PDF34,51.",
      "command": "Alt+F7 Math On/Calculate/Off controls original tab-based columns; function markers are not literal printed operators.",
      "probe": "MATH1: explicit tab stop 1 inch from left margin, turn Math on, enter column rows 2 then 3 then original subtotal function +, Calculate, save; leave Math and type ordinary + outside scope, save/retrieve. Capture exact number/operator insertion and result; expected arithmetic subtotal 5, print/operator visibility still unobserved.",
      "readiness": "Text probe ready after tab/column roles and menu capture; numeric grammar/format/error/rounding and scope decoder needed before implementation.",
      "deferred": "All column roles, formula/functions, subtotal/total/grand-total, range scope, precision/negative formats, editing/recalculation and all math errors."
    },
    {
      "id": "S17",
      "title": "Other original converters",
      "feature_id": "WP51-061",
      "feature_title": "Original macro conversion utility",
      "locators": [
        {
          "printed_start": 370,
          "printed_end": 372,
          "pdf_start": 387,
          "pdf_end": 389
        }
      ],
      "case_links": [
        {
          "id": "CMD51-179",
          "title": "Convert a 4.x macro with MACROCNV",
          "feature_ids": [
            "WP51-061"
          ],
          "oracle_status": "not-run",
          "source_locators": [
            {
              "source_id": "REF51",
              "printed_start": 370,
              "printed_end": 372,
              "pdf_start": 387,
              "pdf_end": 389
            }
          ]
        }
      ],
      "native": "MACROCNV produces original WPM, not graphics/WP document or a Wordling wrapper. Native automation grammar belongs to separate FR-012 research; REF370\u2013372 / PDF387\u2013389.",
      "command": "DOS MACROCNV with original 4.x input and original report; conversion losses/unconverted commands remain visible.",
      "probe": "CONVM1: acquire a provenance-cleared project-authored original 4.x macro that inserts X; pin original-format spec and source bytes before execution. Run conversion beside absent same-stem WPM, inspect report and replay converted output in WP; source remains intact.",
      "readiness": "Blocked input-format fixture prerequisite; no 4.x fixture or complete format contract is selected here. WP06 owns general conversion/path behavior; automation researcher owns token execution.",
      "deferred": "All supported legacy macro variants/commands/options, partial conversion reports, conflicts/overwrite/error behavior; CONVERT text/native modes remain WP51-079 and WP51-026 under WP06."
    }
  ]
}
```
<!-- WP08_AUDIT_END -->

```sh
python3 - <<'PY_AUDIT'
from pathlib import Path
import hashlib,json,re,subprocess
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md')
t = p.read_text()
a = json.loads(t.split('<!-- WP08_AUDIT_BEGIN -->',1)[1].split('```json\n',1)[1].split('\n```',1)[0])
sha = lambda b: hashlib.sha256(b).hexdigest()
for x in a['source_inputs']:
    assert sha(Path(x['path']).read_bytes()) == x['sha256'], x['path']
features = {x['id']:x for x in json.loads(Path('docs/research/feature-inventory.json').read_text())}
cases = {x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
sources = {x['id']:x for x in json.loads(Path('docs/research/sources.json').read_text())}
# Independent family-to-feature binding rejects a valid case/title from another family.
expected = ['WP51-046','WP51-047','WP51-048','WP51-049','WP51-050','WP51-051','WP51-089','WP51-052','WP51-055','WP51-056','WP51-057','WP51-058','WP51-054','WP51-053','WP51-045','WP51-064','WP51-061']
assert len(a['rows']) == 17
used = set()
for n,r in enumerate(a['rows'],1):
    assert r['id'] == 'S'+str(n).zfill(2) and r['feature_id'] == expected[n-1]
    f = features[r['feature_id']]
    assert r['feature_title']==f['title'] and r['locators']==f['locators']
    line = next(x for x in t.splitlines() if x.startswith('| '+r['id']+':'))
    cells = [x.strip() for x in line.split('|')]
    leads = r['feature_id']+' ('+f['title']+'); '+'; '.join(c['id']+' ('+c['title']+')' for c in r['case_links'])
    loc = '; '.join(f"{x['printed_start']}–{x['printed_end']} / {x['pdf_start']}–{x['pdf_end']}" for x in r['locators'])
    assert cells[2:6] == [leads,loc,r['native'],r['command']],r['id']
    starter = next(x for x in t.splitlines() if x.startswith('| '+r['id']+' |'))
    assert [x.strip() for x in starter.split('|')][2:5] == [r['probe'],r['readiness'],r['feature_id']+': '+r['deferred']]
    for c in r['case_links']:
        cid=c['id'];used.add(cid);canonical=cases[cid]
        assert all(c[k]==canonical[k] for k in ('title','feature_ids','oracle_status','source_locators'))
        assert c['oracle_status']=='not-run' and canonical['implementation_status']=='not-implemented'
        assert r['feature_id'] in c['feature_ids'] and cid in f['command_scenario_ids'],(r['id'],cid)
    for x in r['locators']:
        assert x['pdf_start']==x['printed_start']+17 and x['pdf_end']==x['printed_end']+17
        assert 1<=x['pdf_start']<=x['pdf_end']<=sources['REF51']['pdf_pages']
assert set(re.findall(r'CMD51-\d{3}',t)) == used
assert set(re.findall(r'(?:WP51|FMT51)-\d{3}',t)) <= features.keys()
for sid in ('REF51','WB51','SDK51'):
    s=sources[sid];assert sha(Path('research/cache',s['filename']).read_bytes())==s['sha256']
# Physical page checks supplement numeric offsets; inspect entire page, not OCR first line.
for name,pg,needle in [('WP51DevelopersToolkit.pdf',25,'Packet Type 8'),('WP51DevelopersToolkit.pdf',28,'Styles 256'),('WP51DevelopersToolkit.pdf',95,'cell formula'),('WP51DevelopersToolkit.pdf',101,'Equation Nested Function'),('WP51DevelopersToolkit.pdf',204,'DrawPerfect (DOS)'),('WPDOS51Reference.pdf',638,'Style, Create'),('WPDOS51Reference.pdf',688,'Calculate'),('WPDOS51Reference.pdf',245,'Graphics, Conversion Program')]:
    out=subprocess.check_output(['pdftotext','-f',str(pg),'-l',str(pg),'-layout','research/cache/'+name,'-'],text=True)
    assert needle in out,(name,pg)
print('WP08 inputs, 17 family associations, canonical statuses and source locators valid')
PY_AUDIT
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp08-review.xml
```

Author validation: the embedded source/hash/17-family semantic/title/status/locator
audit passes, as do both catalogue checks and the genuine configured regression
runner (JUnit `/tmp/wp08-review.xml`). Go discovery passes; build/test/vet are
explicitly skipped because this planning checkout has no Go packages. Separate
approved code lanes are not tested by those skips. A negative audit replacing the
table-structure lead with a valid graphics-table case/title is rejected by the
family feature-association assertion. No original structured probe, original
fixture production or Wordling behavior is claimed by this documentary research.
