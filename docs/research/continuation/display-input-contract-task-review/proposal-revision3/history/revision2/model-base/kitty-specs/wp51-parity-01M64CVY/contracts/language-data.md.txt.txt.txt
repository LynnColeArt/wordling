# WP10 character, language and data contract map

Research handoff, 2026-10-30. Requirements FR-013, FR-014 and FC-006; native
FC-001–009 remain binding. Authority: mission spec/plan/research/data-model,
compatibility/roadmap, approved WP01/05–09 contracts. This is a documentary map
and bounded probe proposal, not a language tool, data parser or verified feature.
WP12 owns executable continuation WPs. Full original scope remains M1; PDF is M2.

## Evidence and resource boundaries

Selected target remains plain U.S. English DOS WP5.1, Help03/09/92, in the pinned
QEMU/FreeDOS1.4 profile with July1992 text-only Standard Printer. Installed files
are fingerprinted, but installation is not feature execution. **Every canonical
case selected here is not-run/not-implemented**. Existing ASCII macro/merge
outputs are not original character/Compose, dictionary, sort or worksheet-import
observations. No new probe, fixture, registry, queue, resource or raw evidence is
changed. Proposed fixture names below are identifiers, not existing paths/hashes.

REF51 is6/92; SDK51 is12/93 with intermediate WP revision marks. Their contents
must be reconciled with March DOS at each version-sensitive field/resource.
One-based PDF locators below use REF Arabic+17, SDK WP+13. Source PDFs/OCR,
canonical records and approved input contracts are hash-pinned in the ledger.
Source statements are paraphrased independently; proprietary wordlists, resource
contents and character/font bitmaps are not reproduced.

US resources already declared in `reference-environment/resource-profile.json`
under `docs/research/` are pinned below by original DOS path, byte size and SHA-256. The table also includes the original
Speller Utility from the installed-file manifest, which corroborates all five. This proves identity,
not a complete resource format or permission to redistribute:

| Original installed path | Bytes | SHA-256 |
| --- | --- | --- |
| `WP51/WP.LRS` | 26064 | `28ebfe81c85eca5a04c671fd4732c21b0f2530479e18624e0397bd7f5ca0cd7b` |
| `WP51/WP{WP}US.LEX` | 363165 | `58fdb7ffb840a3ef64467b693668a535d2d08672bf042392bcdf815d259c68a5` |
| `WP51/WP{WP}US.HYC` | 9676 | `93e185b2441fb7d7b28c2495bd8e204a20fd04ee778265f9fbd701f175ef217e` |
| `WP51/WP{WP}US.THS` | 358472 | `9cfec163904b33893f43356917a1615c47f7112c64b865a4339342ab45541e20` |
| `WP51/SPELL.EXE` | 56336 | `a5a2bca31167114b5afcfd6e77b03caede8fecbff3d4cbad9c656d31009e6370` |

A read-only inventory and resource hash check of the exact pinned private master
was performed for this contract. US `.LEX/.THS/.HYC`, WP.LRS and SPELL.EXE are
**present but these workflows remain unrun/unqualified**. The recursive selected
installation contains only US files with those three dictionary suffixes, and no
`.SUP`, `.PLN`, `.WK1`, `.WK3` or `.XLS`. A supplementary dictionary can be created
through an original scratch-resource probe; no initial SUP is assumed. No qualified
original worksheet fixture is selected. This is a statement about this installation,
not global resource availability. Bundled LEARN `.WKB` files are workbook training
artifacts, not assumed spreadsheet fixtures or redistribution-cleared test inputs.
The audit hashes the master before/after read-only mdir/mtype reads and exposes only
metadata/hashes, never proprietary contents. No source-format conflict blocks the
unrelated ready Compose/count/US-language/sort investigations.

Record actual selected language code, package language, setup/resource paths,
keyboard/display driver, printer/font resources and any dictionary/supplemental
files for each future run. Additional language codes alone do not acquire matching
dictionaries. Require licensed provenance, edition/version, original filename,
size/hash, acquisition source/date and redistribution disposition for each new
resource. Keep proprietary data in ignored private cache; public availability does
not grant redistribution. No substitute modern spellchecker/thesaurus/collator or
Unicode normalization is selected as equivalent original behavior. Replacements
or changed scope require explicit evidence/decision, not silent resource fallback.

REF595–605/PDF612–622 distinguishes main `.LEX`, supplemental/personal `.SUP`,
compressed data and editable document portions. Main dictionaries and compressed
portions need the original Speller Utility; a supplementary document wordlist is
not proof of the compressed binary format. Words added to compressed supplemental
files may remain in their editable portion. Main dictionary hyphenation marks and
additional `.HYC` are separate from supplementary words; supplemental additions
do not by themselves establish original hyphenation. Installed US filename/hash
is authoritative for this profile even where manual examples use another naming
form. No editing the pinned master or republishing derived main dictionaries.

WP.LRS is documented as a WP5.0 secondary merge/Notebook-compatible resource
(REF331/PDF348), not UTF-8 locale configuration. Original-format preservation
and parser applicability need their own contract before writes; WP01's bounded
WP5.1 document reader does not automatically accept this variant. LRS supports
such items as dates and printed note-continuation messages; `.LEX/.THS/.HYC`
search and edition are distinct dependencies. Missing-resource errors remain
original obligations, not permission to change language or lose characters.

## Character identity contract (T028)

Keep original native bytes and semantic WP character identifiers authoritative.
For extended document characters the documentary frame is four bytes:
`C0 character-number character-set C0` (SDK WP23/PDF36), with set0–12 described.
Thus Compose1,36 has candidate token `C0 24 01 C0`; this is a **manual-derived
expectation**, not an observed saved token/body. Ordinary ASCII and document
functions must remain separate:80–BF is not a CP437 or Latin-1 string. The
existing lossless reader's framing/retention is not a Unicode character decoder.

A semantic token must retain its source span and WP set/number or exact control
identity. A display mapping to one/many Unicode code points is optional,
versioned and reversible only within its proven domain; many-to-one mappings and
unsupported glyphs must keep distinct original tokens. Never reconstruct a saved
document by reverse-mapping terminal glyphs, normalize precomposed/combining
forms, substitute question marks or collapse hard/soft spaces/returns/pages.
An opaque/reserved/undefined valid identity remains preserved; malformed framing
and unsupported semantic edits are explicit refusals, not empty text.

REF913/PDF930 was visually checked with the PDF skill because character tables
and OCR can make glyph identity ambiguous. The original normal screen can show
a placeholder where resources cannot display a character; that does not authorize
replacement of its native identity. Compose Ctrl+V versus Ctrl+2 depends on
input context. WP07 matched printer/fonts, display resources and predeclared
measurement rules gate print/preview comparison; display-cell equality cannot
certify the stored character or its metrics. Appendix character-set coverage,
keyboard mappings and language modules remain required, including not-yet-qualified
fonts/Greek/Russian/Hebrew editions. No unsupported-language exclusion is made.

## Language and data operation map (T028/T029)

Each row is local research identity, not a new canonical case. Exact existing
case title/group links and locators are in the row and ledger. A family with no
dedicated case says so; a valid unrelated scenario is not substituted. Native
structures are **documentation leads**, not implemented codecs or safe writers.

| Row / family | Canonical feature and exact case leads | REF51 printed / PDF | Native/resource obligation | Original commands and observable results |
| --- | --- | --- | --- | --- |
| L01: Character identity / Compose | WP51-066 (WP characters and compose); CMD51-138 (Compose a character by WP set and character number) | 84–87 / 101–104; 913–920 / 930–937 | ASCII20–7E is character data;80–BF includes functions, not a DOS code-page string. Extended document character C0/number/set/C0 (SDK WP23/PDF36) retains original pair. Controls/breaks remain distinct. | Ctrl+V Compose1,36 inserts the selected WP pair; Ctrl+2 is needed in contexts such as Macro/Equation Editor, searches and filenames (REF84–87/PDF101–104; appendix913–920/PDF930–937). Normal/preview/print glyph availability is a resource issue, not character identity. |
| L02: Language code / language resource | WP51-067 (Language selection and resources); CMD51-181 (Set a language code at cursor) | 328–336 / 345–353 | D3/17 old/new two-letter language IDs (SDK WP53/PDF66); WP.LRS is documented WP5.0 secondary merge/Notebook-compatible resource (REF331–336/PDF348–353), not a Unicode locale or assumed WP5.1-only document. | Shift+F8 Other Language writes a reference-language control. It changes Sort/date and installed language tools, not menu language. Nested continued-message behavior needs Initial Codes and note options; resource search path is separate. |
| L03: Speller / dictionaries / lookup / count | WP51-068 (Spelling, dictionaries, lookup and counts); CMD51-139 (Count words through the Speller menu); CMD51-140 (Count option is unavailable for an active block); CMD51-141 (Cancel spell-checking) | 587–605 / 604–622 | Main US .LEX plus supplementary/personal .SUP and .HYC resources; resource storage and native replacement words are distinct. REF595–605/PDF612–622 describes compressed/header versus document portions, utility operations and paths, not a complete binary codec. | Ctrl+F2 opens Speller. Count one two three is documentary3; Count availability differs with Block; cancel spell-check preserves unapproved text. Original correction/lookup order and resource mutations must be observed. |
| L04: Thesaurus | WP51-069 (Thesaurus); CMD51-182 (Open and cancel the Thesaurus) | 692–694 / 709–711 | Pinned US .THS is an external resource; selected original WP word identity and replacement codes must remain native. REF692–694/PDF709–711 gives workflow, not a full THS format. | Alt+F1 uses word at cursor; exact entry/menu/exit and replacement behavior must be captured from matching original resource. |
| D01: Sorting | WP51-063 (Sorting and record selection); CMD51-135 (Sort original records by a declared key) | 577–586 / 594–603 | Native record units depend on line/paragraph/secondary-merge/table sort; keys identify type/field/word/line, sorting must move full associated codes. Sort settings/resource collation are not Unicode code-point order. REF577–586/PDF594–603. | Ctrl+F9 Sort selects screen/disk input/output, Type/Keys/Order then Perform Action. Language placement differs whole-document Initial Codes versus a code before Block. Numeric key handling differs alphanumeric keys. |
| D02: Record selection | WP51-063 (Sorting and record selection); no dedicated canonical case | 577–586 / 594–603 | Same original records and keys as sorting; select predicate and output scope are separate from ordering. REF585–586/PDF602–603; no dedicated canonical select-records case exists in this group. | Ctrl+F9 Sort input/output, Select and original comparison/AND/OR criteria, then Perform Action. Output contains only selected records, requiring source preservation. |
| D03: Column Math | WP51-064 (Column math and calculations); CMD51-180 (Enter and leave original column Math mode) | 401–414 / 418–431 | D2/0 math-column definitions/formulas, A1–A8/B1 controls and result text; SDK WP21–22,38/PDF34–35,51. This is not the DC cell-formula/table-calculation structure. | Alt+F7 Math On/Calculate/Off applies to tab-defined column roles. Original functions/operator markers and displayed last result must remain distinct. |
| D04: Spreadsheet import | WP51-065 (Spreadsheet import and links); CMD51-136 (Import a declared spreadsheet range) | 606–615 / 623–632 | External worksheet records/values/formats become native text/tab/row/table data. Historical source format/version is part of identity. SDK WP102/PDF115 gives necessary Lotus version/dimension records, not a complete worksheet codec. | Ctrl+F5 Spreadsheet Import filename/range/type Perform Import; source unchanged. Table type creates original cell/row structures and depends on WP08; Text type is separate. Base font affects widths; PlanPerfect attributes have format-specific behavior. |
| D05: Spreadsheet links / refresh | WP51-065 (Spreadsheet import and links); CMD51-137 (Create a spreadsheet link) | 606–615 / 623–632 | D2/13–14 Define Link Start/End carries original type/timestamp/range/path plus imported result region; SDK WP45–46/PDF58–59. D2/15–16 is WPWin DDE, not the DOS link contract. | Ctrl+F5 Spreadsheet Create Link/Edit Link, Perform Link; Link Options Update All Links, retrieval-update and display settings are distinct. F7 without Perform can insert empty link codes; F1 cancels without inserting. Refresh replaces content between link markers. |

Spreadsheet version and field traps remain explicit. REF607/PDF624 lists
PlanPerfect3.0–5.1, Lotus1-2-3 1x/2x/3x, Excel2x–3.0, Quattro, Quattro Pro
and Symphony at publication time; capture original Help for later support.
These are not `.xlsx`, arbitrary `.xls`, CSV or converted modern worksheets.
SDK WP102/PDF115 lists Lotus version field values0404/0406/1000 and required
dimension record fields; those are necessary header/dimension facts, not a full
Lotus codec or proof every Lotus3 variant works on this executable. Pin the
original producer, source format/version, cached formula results, date/number
formats, encoding, dimensions/range and recalculation/save state before a probe.

SDK WP45–46/PDF58–59 carries DOS link definitions; subsequent DDE fields are
labelled WPWin. Link End's printed ending-row short at offset13 overlaps the
filename start14, so an original fixture must establish the actual boundary
before writer implementation. Preserve raw bytes and discrepancy; do not invent
an adjusted offset. Refresh updates the existing linked result region, distinct
from initial source import. REF609/PDF626 says F7 without Perform can retain link
codes without imported data, while F1 cancels without them. REF613–615/PDF630–632
specifies original Edit/Update behavior and option scope; do not treat all exit
keys as cancellation. Last imported data prints until original update occurs.

## First independently verifiable slices and retained scope (T030)

All probes below are **proposed and unrun**. Documentary expected values/order
are acceptance hypotheses to corroborate, not original observations. Use fresh
profile copies and original commands to author native sources and outputs.

| Row | Exact starter input/probe | Readiness and implementation prerequisites | Retained M1 scope |
| --- | --- | --- | --- |
| L01 | CHR1: blank native document, type A, Compose1,36, then Z; save/retrieve and capture Compose prompt, Reveal Codes, native bytes and both original views where resources allow. Documentary candidate token is C0 24 01 C0, not an observed complete body. Freeze accepted native token after two original runs; make a separate variant using Ctrl+2 in a supported alternate context. | Ready bounded normal-editor/native probe using installed resources; full glyph/print acceptance blocked on WP07 matched graphics/fonts. No original extended-character fixture exists in this selected corpus. | WP51-066: All13 documented character sets, undefined/reserved positions, digraph/diacritic sequences, control input, context-specific Compose, keyboard maps, search/edit boundaries, bidirectional/language editions and all unsupported-glyph behavior. |
| L02 | LANG1: capture US language code at cursor between `before` and `after`, save/retrieve, compare native ID/scope and no menu-language change. In separate scratch variants move language into document Initial Codes and inspect date/continued-message behavior; foreign language variant only after matching resources identified. | US native/menu probe ready; WP.LRS interpretation and old-format preservation need separate framing contract. Non-US spelling/hyphenation/thesaurus requires actual licensed matched dictionaries, not merely a selectable code. | WP51-067: All language codes, package/reference language distinctions, Initial Codes/nested scope, resource paths, custom LRS edits/restart behavior, locale date/sort/hyphenation, Greek/Russian/Hebrew modules and edition-specific direction controls. |
| L03 | SPELL1: save `one two three`, Count with Block off; repeat selecting `one two` and inspect Count availability. Separate fixture `wordlingtestzz`: first verify it is flagged under pinned US dictionary, then cancel with F1/F7 and compare source bytes. No candidate correction assumed. For supplementary words use copied scratch resource, add own token through original UI, capture .SUP before/after and repeat lookup. | Count/cancel probes ready with pinned US resources; .SUP mutation probe requires exact original Add choices and resource provenance review. Full .LEX/compressed .SUP/.HYC decoding remains unresolved; no bundled resource output is republished. | WP51-068: All suggestion/replace/skip/add/delete prompts, spell selection/document scopes, punctuation/possessive/extended-character rules, lookups/phonetics/wildcards/counts, main/supplemental/personal dictionaries, compression/optimization and standalone SPELL.EXE/error paths. |
| L04 | THES1: own text `good`; cursor on word; Alt+F1 capture entries then exit/cancel without replacement, save and compare native text. If no entry exists record that outcome rather than substituting another dictionary. Replacement variant requires captured exact selected original entry and next native save. | Ready US resource workflow probe after exact exit choices captured; other editions/resources and complete THS decoder are blocked pending acquisition/research. | WP51-069: All lookup categories/synonyms/antonyms/meaning navigation, replacement/case/attribute handling, no-entry/cancel/errors, language switching and resource formats. |
| D01 | SORT1: original secondary records field1 Zebra/field2 IDZ then field1 Amber/field2 IDA, authored with original End Field/End Record. Save source; select merge record type, alphanumeric first-field first-word ascending, separate absent output filename; Perform Action. Documentary expected order Amber/IDA then Zebra/IDZ; preserve entire records/codes and source file. No tie order assumed. | Ready original text/native probe; decoder/writer blocked on exact record/key grammar and original saved output. Alphabetic extended-character collation requires language/code/resource evidence. | WP51-063: Line/paragraph/merge/table/block sorts, multiple/numeric/negative-index keys, ascending/descending, equal/missing values, language/case/punctuation, output/overwrite/cancel/errors and record selection. |
| D02 | SELECT1: use SORT1 source; choose key1 alphanumeric field1 word1 equal Amber, separate output filename, capture exact predicate editor spelling/keystrokes and selected result. Documentary intention is only Amber/IDA. Add a dedicated canonical case through WP12 before acceptance; no command-string grammar is invented here. | Ready prompt/predicate investigation; executable acceptance needs new canonical case plus observed exact selection expression/output and cancel/error branches. | WP51-063: All comparison operators, AND/OR precedence, range/pattern/numeric conditions, empty/missing fields, selection-only/sort combination, screen/block replacement and failure/cancel behavior. |
| D03 | Reuse WP08 MATH1: declared tab stop1inch from left margin, rows2,3 then original subtotal function+, Calculate, save; Math Off then ordinary+ outside scope, save/retrieve. Documentary arithmetic subtotal5; exact codes/result/print visibility remain unrun. Capture scope and commands before implementation. | Text probe ready after columns/tab settings captured; follow approved WP08 dependencies. No structured table/calculation support is claimed. Numeric precision/locale/errors and output geometry remain separate prerequisites. | WP51-064: Every role/function/formula, subtotal/total/grand total, precision/rounding/negative formats, range/update/error behaviors. WP51-049 table Math remains independently gated in WP08. |
| D04 | SHEET1: acquire/create own original Lotus2.0 worksheet with A1 label NAME, B1 value2, A2 label ROW2, B2 formula B1+3 with saved cached result5, plus sentinel C1 EXCLUDED. Hash/source-producer/version and native worksheet record audit first. Import exactly A1:B2 as Table, capture values/formats/codes and source equality; separate Text variant later. Formula versus cached-value semantics are a question, not guessed output. | Blocked fixture/resource: no provenance-cleared original worksheet and complete Lotus2.0 record specification selected here. Need producer/calculation state and exact original recognized format; Table output additionally needs WP08 structure. | WP51-065: All supported formats/versions and range/named-range/format/empty/error/date/formula cases, fonts/widths, text/table/box output, malformed/unsupported worksheets and legacy export behavior. |
| D05 | LINK1: qualified SHEET1 source and exact range A1:B2; Create Link Perform Link, save; change B1 to7 in original producer, recalculate/save workbook; Update All Links, save/retrieve native output. Compare imported region/path/range/source bytes and stale-versus-refreshed values. Separate fresh F7/no-Perform and F1/cancel variants; deletion/missing-source cases captured before writer. | Blocked on qualified worksheet, path/refresh native fixtures and field-offset resolution. SDK Link End gives ending-row short at13 and filename at14 (overlap); do not implement guessed offsets. WP06 DOS path mappings and WP08 output structures apply. | WP51-065: All update-on-retrieve/options, edit/rebind path/ranges, show-link nonprinting state, source errors/conflicts, nested links, source timestamp behavior, cancellation and preservation of outside content. |

WP08 MATH1 and table-calculation probes remain separate: reuse the agreed column
fixture rather than creating an incompatible duplicate. Table cell formulas
WP51-049 use different structure/relative addressing; neither successful column
Math nor a worksheet containing a formula establishes table calculation support.
SHEET1 formula source and cached value are distinct. The experiment must reveal
which original import semantics apply; it must not evaluate a formula with a
modern spreadsheet library and call that an original result.

Other dependent original obligations remain tracked: WP51-003 keyboard mapping,
WP51-005 display configuration, WP51-031/073 printer/font resources, WP51-039
hyphenation, WP51-025/026 text and old-format conversion, WP51-048/049 tables and
WP51-062 native merge records. FMT51-004 covers original code classes; its current
boundary-class scenario is not a Compose oracle. WP09's macro-expression numeric
results are not evidence for column Math, worksheet import or locale collation.

## Probe and implementation handoff for WP12

First author two independent packages: CHR1 native identity and SORT1 whole-record
movement. Both can investigate original text/native behavior under the current
US profile without pretending graphics or other locales are qualified. Count,
US-language and original dictionary/thesaurus cancel workflows can proceed as
separate prompt/resource probes. Acquire worksheet specifications/producers and
licensed foreign resources independently so those blockers do not stall the
ready text investigations.

For CHR1, capture exact Compose prompt/termination and original native before/after
files twice. Freeze an original-produced fixture with token offsets, expected
WP identities and raw SHA-256; verify original retrieve/edit/save and source
preservation. Then propose a read-only character tokenizer limited to ASCII and
proven C0 identities, preserving unknown framed content, coupled to exact no-edit
export. Add truncated/mismatched C0 delimiters, invalid lengths/unsupported sets,
context controls and buffer-isolation tests, with measured bounded fuzz/resource
budgets. Do not call undefined pairs universally malformed without evidence.
A later semantic writer needs targeted edits, original retrieve/edit/print/save,
unrelated-byte preservation and safe refusal for unsupported structures. Any
Unicode/display mapping is a separate derived table with explicit uncertainty
and independent reverse-round-trip tests; native storage never depends on it.

For SORT1, capture native source/output, original key/record/type/settings and
output prompts twice. Independently inspect whole field/record spans and ensure
reordering preserves each complete record and source bytes. Before code, define
native record boundary grammar, key extraction, output/overwrite transaction,
collation/numeric policy and unsupported variants. Initially support only the
accepted ASCII merge-record key subset; no silent locale/tie/missing-key defaults.
Add malformed End Field/Record, truncated keys, code-containing field, unsupported
records and failure/cancel/source-integrity cases. SELECT1 requires a new case
and exact predicate grammar first; do not mark the general sort case observed
merely by inspecting its selection menu.

Resource readers/writers need independent per-format contracts (LRS, LEX, SUP,
HYC, THS, SET paths); a dictionary replacement algorithm is not a native resource
codec. Qualify original scratch supplementary additions and redistribution rights
before committing any derived fixture. SHEET1/LINK1 need full source worksheet
record/encoding contracts, original accepted fixture and output types, link
boundaries, refresh/cancel/errors and source preservation before implementation.
Missing/malformed source, stale cache, missing resource, wrong locale/edition,
read-only/conflicting destination and malformed native structures must produce
explicit outcomes, preserving source and unrelated data. Do not assert unknown
original error text or rollback behavior; research the exact branch first.

For every new original probe record exact executable/environment/resource/profile
hashes, source/native hashes, source producer/version, original keystroke trace,
setup/language/keyboard state, stable captures and archived runner; two fresh-copy
repetitions must agree or discrepancies remain explicit. Published evidence must
separate manual expectation, original observation, implementation and differential
verification. Accept typed identity/order/results first, then print/preview under
WP07 qualified profiles and pre-test tolerances. Never normalize source bytes,
dictionary entries, Unicode sequences or unknown fields to make a comparison pass.
No proposed package or test here closes full FR-013/014 or FC-006 coverage.

## Reproducible source and semantic association audit

Paths are repository-relative. Ignored sources are reacquired only by the pinned
source registry URL/hash. Resource fingerprints are metadata only; proprietary
resource files remain private. The audit checks both canonical links and fixed
family-feature bindings, so a valid unrelated case/title cannot satisfy a row.

<!-- WP10_AUDIT_BEGIN -->
```json
{
"source_inputs": [
{"path": "docs/research/sources.json", "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"},
{"path": "docs/research/feature-inventory.json", "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"},
{"path": "docs/research/command-scenarios.json", "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"},
{"path": "docs/research/reference-baseline.json", "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"},
{"path": "docs/research/reference-environment/resource-profile.json", "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"},
{"path": "docs/research/reference-environment/installed-files.json", "sha256": "a8532ce5be7caa5759799841c8c0e3128810f7631f49101978102244139a1238"},
{"path": "docs/research/reference-environment/environment.json", "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"},
{"path": "research/cache/WPDOS51Reference.pdf", "sha256": "ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531"},
{"path": "research/cache/WP51DevelopersToolkit.pdf", "sha256": "5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754"},
{"path": "research/cache/reference.txt", "sha256": "f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c"},
{"path": "research/cache/toolkit.txt", "sha256": "8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md", "sha256": "e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md", "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json", "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md", "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md", "sha256": "aa6384662a74c1c0451a506bd9fdd169420614c558677a40715fbe0bab906631"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md", "sha256": "32a9fa1352c2a07fb754a7d6211cc43f8b356542ce816d7b42c3a9d5a0f425a6"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/automation.md", "sha256": "2529b6218b36fccba2c143c8158017ae853d10e8fe3d7afc1958d6407d50e6f6"}
],
"resource_fingerprints": [
{"path": "WP51/WP.LRS", "size": 26064, "sha256": "28ebfe81c85eca5a04c671fd4732c21b0f2530479e18624e0397bd7f5ca0cd7b"},
{"path": "WP51/WP{WP}US.LEX", "size": 363165, "sha256": "58fdb7ffb840a3ef64467b693668a535d2d08672bf042392bcdf815d259c68a5"},
{"path": "WP51/WP{WP}US.HYC", "size": 9676, "sha256": "93e185b2441fb7d7b28c2495bd8e204a20fd04ee778265f9fbd701f175ef217e"},
{"path": "WP51/WP{WP}US.THS", "size": 358472, "sha256": "9cfec163904b33893f43356917a1615c47f7112c64b865a4339342ab45541e20"},
{"path": "WP51/SPELL.EXE", "size": 56336, "sha256": "a5a2bca31167114b5afcfd6e77b03caede8fecbff3d4cbad9c656d31009e6370"}
],
"cache_inventory": {"image": "research/cache/reference/master/harddisk.img", "partition_offset": 1048576, "only_us_suffixes": [".LEX", ".THS", ".HYC"], "absent_suffixes": [".SUP", ".PLN", ".WK1", ".WK3", ".XLS"]},
"rows": [
{"id": "L01", "title": "Character identity / Compose", "feature_id": "WP51-066", "feature_title": "WP characters and compose", "locators": [{"printed_start": 84, "printed_end": 87, "pdf_start": 101, "pdf_end": 104}, {"printed_start": 913, "printed_end": 920, "pdf_start": 930, "pdf_end": 937}], "cases": [{"id": "CMD51-138", "title": "Compose a character by WP set and character number", "feature_ids": ["WP51-066"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 84, "printed_end": 85, "pdf_start": 101, "pdf_end": 102}]}], "native": "ASCII20\u20137E is character data;80\u2013BF includes functions, not a DOS code-page string. Extended document character C0/number/set/C0 (SDK WP23/PDF36) retains original pair. Controls/breaks remain distinct.", "command": "Ctrl+V Compose1,36 inserts the selected WP pair; Ctrl+2 is needed in contexts such as Macro/Equation Editor, searches and filenames (REF84\u201387/PDF101\u2013104; appendix913\u2013920/PDF930\u2013937). Normal/preview/print glyph availability is a resource issue, not character identity.", "probe": "CHR1: blank native document, type A, Compose1,36, then Z; save/retrieve and capture Compose prompt, Reveal Codes, native bytes and both original views where resources allow. Documentary candidate token is C0 24 01 C0, not an observed complete body. Freeze accepted native token after two original runs; make a separate variant using Ctrl+2 in a supported alternate context.", "readiness": "Ready bounded normal-editor/native probe using installed resources; full glyph/print acceptance blocked on WP07 matched graphics/fonts. No original extended-character fixture exists in this selected corpus.", "deferred": "All13 documented character sets, undefined/reserved positions, digraph/diacritic sequences, control input, context-specific Compose, keyboard maps, search/edit boundaries, bidirectional/language editions and all unsupported-glyph behavior."},
{"id": "L02", "title": "Language code / language resource", "feature_id": "WP51-067", "feature_title": "Language selection and resources", "locators": [{"printed_start": 328, "printed_end": 336, "pdf_start": 345, "pdf_end": 353}], "cases": [{"id": "CMD51-181", "title": "Set a language code at cursor", "feature_ids": ["WP51-067"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 328, "printed_end": 330, "pdf_start": 345, "pdf_end": 347}]}], "native": "D3/17 old/new two-letter language IDs (SDK WP53/PDF66); WP.LRS is documented WP5.0 secondary merge/Notebook-compatible resource (REF331\u2013336/PDF348\u2013353), not a Unicode locale or assumed WP5.1-only document.", "command": "Shift+F8 Other Language writes a reference-language control. It changes Sort/date and installed language tools, not menu language. Nested continued-message behavior needs Initial Codes and note options; resource search path is separate.", "probe": "LANG1: capture US language code at cursor between `before` and `after`, save/retrieve, compare native ID/scope and no menu-language change. In separate scratch variants move language into document Initial Codes and inspect date/continued-message behavior; foreign language variant only after matching resources identified.", "readiness": "US native/menu probe ready; WP.LRS interpretation and old-format preservation need separate framing contract. Non-US spelling/hyphenation/thesaurus requires actual licensed matched dictionaries, not merely a selectable code.", "deferred": "All language codes, package/reference language distinctions, Initial Codes/nested scope, resource paths, custom LRS edits/restart behavior, locale date/sort/hyphenation, Greek/Russian/Hebrew modules and edition-specific direction controls."},
{"id": "L03", "title": "Speller / dictionaries / lookup / count", "feature_id": "WP51-068", "feature_title": "Spelling, dictionaries, lookup and counts", "locators": [{"printed_start": 587, "printed_end": 605, "pdf_start": 604, "pdf_end": 622}], "cases": [{"id": "CMD51-139", "title": "Count words through the Speller menu", "feature_ids": ["WP51-068"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 599, "printed_end": 599, "pdf_start": 616, "pdf_end": 616}]}, {"id": "CMD51-140", "title": "Count option is unavailable for an active block", "feature_ids": ["WP51-068"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 599, "printed_end": 599, "pdf_start": 616, "pdf_end": 616}]}, {"id": "CMD51-141", "title": "Cancel spell-checking", "feature_ids": ["WP51-068"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 588, "printed_end": 589, "pdf_start": 605, "pdf_end": 606}]}], "native": "Main US .LEX plus supplementary/personal .SUP and .HYC resources; resource storage and native replacement words are distinct. REF595\u2013605/PDF612\u2013622 describes compressed/header versus document portions, utility operations and paths, not a complete binary codec.", "command": "Ctrl+F2 opens Speller. Count one two three is documentary3; Count availability differs with Block; cancel spell-check preserves unapproved text. Original correction/lookup order and resource mutations must be observed.", "probe": "SPELL1: save `one two three`, Count with Block off; repeat selecting `one two` and inspect Count availability. Separate fixture `wordlingtestzz`: first verify it is flagged under pinned US dictionary, then cancel with F1/F7 and compare source bytes. No candidate correction assumed. For supplementary words use copied scratch resource, add own token through original UI, capture .SUP before/after and repeat lookup.", "readiness": "Count/cancel probes ready with pinned US resources; .SUP mutation probe requires exact original Add choices and resource provenance review. Full .LEX/compressed .SUP/.HYC decoding remains unresolved; no bundled resource output is republished.", "deferred": "All suggestion/replace/skip/add/delete prompts, spell selection/document scopes, punctuation/possessive/extended-character rules, lookups/phonetics/wildcards/counts, main/supplemental/personal dictionaries, compression/optimization and standalone SPELL.EXE/error paths."},
{"id": "L04", "title": "Thesaurus", "feature_id": "WP51-069", "feature_title": "Thesaurus", "locators": [{"printed_start": 692, "printed_end": 694, "pdf_start": 709, "pdf_end": 711}], "cases": [{"id": "CMD51-182", "title": "Open and cancel the Thesaurus", "feature_ids": ["WP51-069"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 692, "printed_end": 694, "pdf_start": 709, "pdf_end": 711}]}], "native": "Pinned US .THS is an external resource; selected original WP word identity and replacement codes must remain native. REF692\u2013694/PDF709\u2013711 gives workflow, not a full THS format.", "command": "Alt+F1 uses word at cursor; exact entry/menu/exit and replacement behavior must be captured from matching original resource.", "probe": "THES1: own text `good`; cursor on word; Alt+F1 capture entries then exit/cancel without replacement, save and compare native text. If no entry exists record that outcome rather than substituting another dictionary. Replacement variant requires captured exact selected original entry and next native save.", "readiness": "Ready US resource workflow probe after exact exit choices captured; other editions/resources and complete THS decoder are blocked pending acquisition/research.", "deferred": "All lookup categories/synonyms/antonyms/meaning navigation, replacement/case/attribute handling, no-entry/cancel/errors, language switching and resource formats."},
{"id": "D01", "title": "Sorting", "feature_id": "WP51-063", "feature_title": "Sorting and record selection", "locators": [{"printed_start": 577, "printed_end": 586, "pdf_start": 594, "pdf_end": 603}], "cases": [{"id": "CMD51-135", "title": "Sort original records by a declared key", "feature_ids": ["WP51-063"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 577, "printed_end": 584, "pdf_start": 594, "pdf_end": 601}]}], "native": "Native record units depend on line/paragraph/secondary-merge/table sort; keys identify type/field/word/line, sorting must move full associated codes. Sort settings/resource collation are not Unicode code-point order. REF577\u2013586/PDF594\u2013603.", "command": "Ctrl+F9 Sort selects screen/disk input/output, Type/Keys/Order then Perform Action. Language placement differs whole-document Initial Codes versus a code before Block. Numeric key handling differs alphanumeric keys.", "probe": "SORT1: original secondary records field1 Zebra/field2 IDZ then field1 Amber/field2 IDA, authored with original End Field/End Record. Save source; select merge record type, alphanumeric first-field first-word ascending, separate absent output filename; Perform Action. Documentary expected order Amber/IDA then Zebra/IDZ; preserve entire records/codes and source file. No tie order assumed.", "readiness": "Ready original text/native probe; decoder/writer blocked on exact record/key grammar and original saved output. Alphabetic extended-character collation requires language/code/resource evidence.", "deferred": "Line/paragraph/merge/table/block sorts, multiple/numeric/negative-index keys, ascending/descending, equal/missing values, language/case/punctuation, output/overwrite/cancel/errors and record selection."},
{"id": "D02", "title": "Record selection", "feature_id": "WP51-063", "feature_title": "Sorting and record selection", "locators": [{"printed_start": 577, "printed_end": 586, "pdf_start": 594, "pdf_end": 603}], "cases": [], "native": "Same original records and keys as sorting; select predicate and output scope are separate from ordering. REF585\u2013586/PDF602\u2013603; no dedicated canonical select-records case exists in this group.", "command": "Ctrl+F9 Sort input/output, Select and original comparison/AND/OR criteria, then Perform Action. Output contains only selected records, requiring source preservation.", "probe": "SELECT1: use SORT1 source; choose key1 alphanumeric field1 word1 equal Amber, separate output filename, capture exact predicate editor spelling/keystrokes and selected result. Documentary intention is only Amber/IDA. Add a dedicated canonical case through WP12 before acceptance; no command-string grammar is invented here.", "readiness": "Ready prompt/predicate investigation; executable acceptance needs new canonical case plus observed exact selection expression/output and cancel/error branches.", "deferred": "All comparison operators, AND/OR precedence, range/pattern/numeric conditions, empty/missing fields, selection-only/sort combination, screen/block replacement and failure/cancel behavior."},
{"id": "D03", "title": "Column Math", "feature_id": "WP51-064", "feature_title": "Column math and calculations", "locators": [{"printed_start": 401, "printed_end": 414, "pdf_start": 418, "pdf_end": 431}], "cases": [{"id": "CMD51-180", "title": "Enter and leave original column Math mode", "feature_ids": ["WP51-064"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 401, "printed_end": 405, "pdf_start": 418, "pdf_end": 422}]}], "native": "D2/0 math-column definitions/formulas, A1\u2013A8/B1 controls and result text; SDK WP21\u201322,38/PDF34\u201335,51. This is not the DC cell-formula/table-calculation structure.", "command": "Alt+F7 Math On/Calculate/Off applies to tab-defined column roles. Original functions/operator markers and displayed last result must remain distinct.", "probe": "Reuse WP08 MATH1: declared tab stop1inch from left margin, rows2,3 then original subtotal function+, Calculate, save; Math Off then ordinary+ outside scope, save/retrieve. Documentary arithmetic subtotal5; exact codes/result/print visibility remain unrun. Capture scope and commands before implementation.", "readiness": "Text probe ready after columns/tab settings captured; follow approved WP08 dependencies. No structured table/calculation support is claimed. Numeric precision/locale/errors and output geometry remain separate prerequisites.", "deferred": "Every role/function/formula, subtotal/total/grand total, precision/rounding/negative formats, range/update/error behaviors. WP51-049 table Math remains independently gated in WP08."},
{"id": "D04", "title": "Spreadsheet import", "feature_id": "WP51-065", "feature_title": "Spreadsheet import and links", "locators": [{"printed_start": 606, "printed_end": 615, "pdf_start": 623, "pdf_end": 632}], "cases": [{"id": "CMD51-136", "title": "Import a declared spreadsheet range", "feature_ids": ["WP51-065"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 607, "printed_end": 611, "pdf_start": 624, "pdf_end": 628}]}], "native": "External worksheet records/values/formats become native text/tab/row/table data. Historical source format/version is part of identity. SDK WP102/PDF115 gives necessary Lotus version/dimension records, not a complete worksheet codec.", "command": "Ctrl+F5 Spreadsheet Import filename/range/type Perform Import; source unchanged. Table type creates original cell/row structures and depends on WP08; Text type is separate. Base font affects widths; PlanPerfect attributes have format-specific behavior.", "probe": "SHEET1: acquire/create own original Lotus2.0 worksheet with A1 label NAME, B1 value2, A2 label ROW2, B2 formula B1+3 with saved cached result5, plus sentinel C1 EXCLUDED. Hash/source-producer/version and native worksheet record audit first. Import exactly A1:B2 as Table, capture values/formats/codes and source equality; separate Text variant later. Formula versus cached-value semantics are a question, not guessed output.", "readiness": "Blocked fixture/resource: no provenance-cleared original worksheet and complete Lotus2.0 record specification selected here. Need producer/calculation state and exact original recognized format; Table output additionally needs WP08 structure.", "deferred": "All supported formats/versions and range/named-range/format/empty/error/date/formula cases, fonts/widths, text/table/box output, malformed/unsupported worksheets and legacy export behavior."},
{"id": "D05", "title": "Spreadsheet links / refresh", "feature_id": "WP51-065", "feature_title": "Spreadsheet import and links", "locators": [{"printed_start": 606, "printed_end": 615, "pdf_start": 623, "pdf_end": 632}], "cases": [{"id": "CMD51-137", "title": "Create a spreadsheet link", "feature_ids": ["WP51-065"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 607, "printed_end": 615, "pdf_start": 624, "pdf_end": 632}]}], "native": "D2/13\u201314 Define Link Start/End carries original type/timestamp/range/path plus imported result region; SDK WP45\u201346/PDF58\u201359. D2/15\u201316 is WPWin DDE, not the DOS link contract.", "command": "Ctrl+F5 Spreadsheet Create Link/Edit Link, Perform Link; Link Options Update All Links, retrieval-update and display settings are distinct. F7 without Perform can insert empty link codes; F1 cancels without inserting. Refresh replaces content between link markers.", "probe": "LINK1: qualified SHEET1 source and exact range A1:B2; Create Link Perform Link, save; change B1 to7 in original producer, recalculate/save workbook; Update All Links, save/retrieve native output. Compare imported region/path/range/source bytes and stale-versus-refreshed values. Separate fresh F7/no-Perform and F1/cancel variants; deletion/missing-source cases captured before writer.", "readiness": "Blocked on qualified worksheet, path/refresh native fixtures and field-offset resolution. SDK Link End gives ending-row short at13 and filename at14 (overlap); do not implement guessed offsets. WP06 DOS path mappings and WP08 output structures apply.", "deferred": "All update-on-retrieve/options, edit/rebind path/ranges, show-link nonprinting state, source errors/conflicts, nested links, source timestamp behavior, cancellation and preservation of outside content."}
]
}
```
<!-- WP10_AUDIT_END -->

```sh
python3 - <<'PY_AUDIT'
from pathlib import Path
import hashlib,json,re,subprocess
p=Path('kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md');text=p.read_text()
a=json.loads(text.split('<!-- WP10_AUDIT_BEGIN -->',1)[1].split('```json\n',1)[1].split('\n```',1)[0])
sha=lambda b:hashlib.sha256(b).hexdigest()
for x in a['source_inputs']:assert sha(Path(x['path']).read_bytes())==x['sha256'],x['path']
features={x['id']:x for x in json.loads(Path('docs/research/feature-inventory.json').read_text())}
cases={x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
sources={x['id']:x for x in json.loads(Path('docs/research/sources.json').read_text())}
profile=json.loads(Path('docs/research/reference-environment/resource-profile.json').read_text())['resources']
installed={x['path']:x for x in json.loads(Path('docs/research/reference-environment/installed-files.json').read_text())['files']}
for x in a['resource_fingerprints']:
    if x['path'] in profile:assert x==profile[x['path']]
    assert all(installed[x['path']][k]==x[k] for k in ('path','size','sha256'))
    assert '| `'+x['path']+'` | '+str(x['size'])+' | `'+x['sha256']+'` |' in text
# Private cache is required for this resource check; reacquire/fingerprint if absent.
env=json.loads(Path('docs/research/reference-environment/environment.json').read_text())
private=a['cache_inventory'];image=Path(private['image'])
assert sha(image.read_bytes())==env['master_disk_sha256']
image_arg=str(image)+'@@'+str(private['partition_offset'])
listing=subprocess.check_output(['mdir','-b','-s','-i',image_arg,'::/WP51'],text=True).splitlines()
for suffix in private['absent_suffixes']:assert not any(x.upper().endswith(suffix) for x in listing)
for suffix in private['only_us_suffixes']:
    matches=[x for x in listing if x.upper().endswith(suffix)]
    assert len(matches)==1 and matches[0].upper().endswith('US'+suffix)
for x in a['resource_fingerprints']:
    b=subprocess.check_output(['mtype','-i',image_arg,'::/'+x['path']])
    assert (len(b),sha(b))==(x['size'],x['sha256'])
assert sha(image.read_bytes())==env['master_disk_sha256']
expected={'L01':'WP51-066','L02':'WP51-067','L03':'WP51-068','L04':'WP51-069','D01':'WP51-063','D02':'WP51-063','D03':'WP51-064','D04':'WP51-065','D05':'WP51-065'}
assert {r['id']:r['feature_id'] for r in a['rows']}==expected
used=set()
for r in a['rows']:
    f=features[r['feature_id']];assert (r['feature_title'],r['locators'])==(f['title'],f['locators'])
    line=next(x for x in text.splitlines() if x.startswith('| '+r['id']+':'))
    lead=r['feature_id']+' ('+f['title']+'); '+('; '.join(c['id']+' ('+c['title']+')' for c in r['cases']) or 'no dedicated canonical case')
    loc='; '.join(f"{x['printed_start']}–{x['printed_end']} / {x['pdf_start']}–{x['pdf_end']}" for x in r['locators'])
    assert [x.strip() for x in line.split('|')][2:6]==[lead,loc,r['native'],r['command']]
    starter=next(x for x in text.splitlines() if x.startswith('| '+r['id']+' |'))
    assert [x.strip() for x in starter.split('|')][2:5]==[r['probe'],r['readiness'],r['feature_id']+': '+r['deferred']]
    for c in r['cases']:
        cid=c['id'];used.add(cid);canonical=cases[cid]
        assert all(c[k]==canonical[k] for k in c)
        assert r['feature_id'] in c['feature_ids'] and cid in f['command_scenario_ids'],(r['id'],cid)
        assert c['oracle_status']=='not-run' and canonical['implementation_status']=='not-implemented'
        for x in c['source_locators']:
            assert 1<=x['pdf_start']<=x['pdf_end']<=sources[x['source_id']]['pdf_pages']
            assert x['pdf_start']==x['printed_start']+17
    for x in r['locators']:
        assert x['pdf_start']==x['printed_start']+17 and x['pdf_end']==x['printed_end']+17
assert set(re.findall(r'CMD51-\d{3}',text))==used
assert set(re.findall(r'(?:WP51|FMT51)-\d{3}',text))<=features.keys()
for sid in ('REF51','SDK51'):
    s=sources[sid];assert sha(Path('research/cache',s['filename']).read_bytes())==s['sha256']
for pdf,pg,needle in [('WP51DevelopersToolkit.pdf',36,'Extended Character'),('WP51DevelopersToolkit.pdf',66,'Set Language'),('WP51DevelopersToolkit.pdf',58,'Define Link Start'),('WP51DevelopersToolkit.pdf',115,'Importing Lotus'),('WPDOS51Reference.pdf',348,'5.0 secondary'),('WPDOS51Reference.pdf',612,'Speller, Dictionaries'),('WPDOS51Reference.pdf',624,'PlanPerfect'),('WPDOS51Reference.pdf',630,'Updating'),('WPDOS51Reference.pdf',930,'Character Entry')]:
    out=subprocess.check_output(['pdftotext','-f',str(pg),'-l',str(pg),'-layout','research/cache/'+pdf,'-'],text=True)
    assert needle in out,(pdf,pg)
assert bytes([0xc0,36,1,0xc0]).hex()=='c02401c0' # documentary token, no fixture claim
print('WP10 pinned inputs/resources, 9 semantic families, canonical statuses and locators valid')
PY_AUDIT
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp10-review.xml
```

Author validation: the embedded source/resource/private-cache/9-family semantic
association/status/locator audit passes; both catalogue checks and the genuine
configured regression runner pass (JUnit `/tmp/wp10-review.xml`). Go discovery
passes; build/test/vet explicitly skip the planning checkout with no Go packages,
not separate approved code lanes. A negative full-audit substitution of a valid
Compose case/title into a sort row is rejected by the feature-association check.
No original language/data probe, resource mutation or Wordling implementation is
claimed. The read-only installation check is inventory qualification only.
