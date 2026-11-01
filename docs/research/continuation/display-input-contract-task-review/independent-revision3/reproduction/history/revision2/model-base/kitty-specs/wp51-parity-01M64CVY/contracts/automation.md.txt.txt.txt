# WP09 macro and merge execution contract matrix

Research handoff, 2026-10-30. Requirements FR-003 and FR-012; FC-001–009 apply.
Authority: mission spec/plan/research/data-model, compatibility/roadmap and approved
WP01/04–08 contracts. This consolidates **bounded original-only observations**;
it implements no decoder/interpreter and verifies no Wordling behavior. WP12 owns
new executable continuation WPs. Full macro/merge/recording/editor/conversion scope
remains M1; PDF remains M2.

## Identity, source and evidence boundary

Selected original: plain U.S. English DOS WP5.1, Help03/09/92, pinned executable
SHA-256 `0734d0734c78c113ddaf40293c2c21b02e2cacc063bca5aa3d02f696de0bdc6a`.
Runs use fresh copies of QEMU/FreeDOS1.4 and the July1992 text-only Standard
Printer; this is not historical DOS, graphics-font layout or another release.
WP07 profile/measurement requirements apply to printer-sensitive comparisons.
These page-control observations concern the specified native hard-page boundaries,
not a general pagination engine. No raw output/SET/formatter bytes are normalized.

REF51 is 6/92, SDK51 is12/93 with intermediate WP revision marks. Full PDFs,
OCR, registries, contracts, reports and manifests are hash-pinned below. Original
observations may disagree with documentary wording; retain both and the exact
context. Printed/PDF locators use **one-based PDF pages**, REF+17 and SDK WP+13.
No third-party media is redistributed: the native sources/results are existing
project-authored scratch inputs produced in original WP, not bundled resources.

| Topic | Pinned manual printed / PDF | Applicability |
| --- | --- | --- |
| Recording/execution/editor | REF373–393 /390–410 | Original command-entry, prompt and editor obligations, beyond these bounded recipes. |
| Native merge procedure | REF418–433 /435–450 | Primary/secondary files, records/fields and generated output remain native documents. |
| BREAK precedence | REF800–801 /817–818 | Documentary loop/IF/file rules; observed macro versus merge distinction below must remain. |
| FOR, FOR EACH | REF820–822 /837–839 | Inclusive range versus explicit value/expression list; strings/escaping only bounded observations. |
| IF BLANK | REF825 /842 | Empty field differs from absent/space-filled fields; only genuinely empty fixture branch observed. |
| Macro nesting/handlers | REF836–837,843–845 /853–854,860–862 | Default child handling, RETURN ERROR and parent resumption, separately from merge PAGE state. |
| NEST PRIMARY/SECONDARY, NEXT | REF838–840 /855–857 | Current-record primary call, replacement secondary record and current-loop control. |
| PAGE OFF/ON | REF847–848 /864–865 | Global merge setting until opposite command; observed boundary timing below. |
| WHILE | REF876 /893 | Zero-entry and variable-terminating cases only. |
| Merge code framing | SDK WP86–87 /99–100; WP17–18 /30–31 | DE functions/arguments are not two-byte WPM instructions. |
| WPM file/token structure | SDK WP92–99 /105–112 | DOS/VAX/UNIX section; select DOS target by fixture, not shared signature alone. |

## Evidence aliases and exact native results (T025/T026)

Each row gives an exact canonical case/title/feature association, context and
bounded result. All listed cases remain **partially-observed**, implementation
**not-implemented**. The larger scenario is not certified by a smoke recipe.
The ledger gives canonical/repetition run IDs and native result path/size/hash;
for each selected case the audit validates **all native source/companion/result
exports** against each sealed run manifest and compares repetition bytes. The
manifests also seal traces/checks/captures and archived runner sources; audit
checks those evidence hashes and runner archives, not only result filenames.

Output strings below are escaped ASCII: `\n` denotes hard return in this bounded
inspector, `\f` an actual native hard-page control outside validated D4/00
formatter functions. They are diagnostic notation, not replacement stored formats.
Macro body checks are exact bytes from stored document offset to EOF. Merge
checks additionally retain raw body hashes and formatter page metadata; a count
of byte0C anywhere in the file would be invalid. WPM source is not decoded by
this document-body inspector. Guest scratch names had no required host `.WP5`
suffix; host filenames label extracted native documents.

| Canonical case (title) / features | Context and exact bounded observation | Expected result and native result filename |
| --- | --- | --- |
| CMD51-131 (Record and execute a named macro); WP51-059 | macro-record: Record ABC, stop, execute in same buffer; recording and execution are distinct actions. | `"ABCABC"`; exact body; `MACROOUT.WP5` |
| CMD51-132 (Repeat a macro using Repeat Value); WP51-059 | macro-record: Record ABC, switch to blank Doc2, Repeat Value3 then execute. | `"ABCABCABC"`; exact body; `REPEAT.WP5` |
| CMD51-134 (Merge original primary and secondary files); WP51-062 | merge-primary: Primary contains Hello/FIELD1 and explicit hard page; automatic copy separators also occur. Actual result has blank pages and final cursor page4, not a two-page letter. | `"Hello Alice\f\fHello Bob\f"`; hard pages=3; `MERGED.WP5` |
| CMD51-178 (Macro stops on a default failed search); WP51-060 | macro: Default DISPLAY OFF failed search stops before SHOULDNOT; original saved result includes manually typed READY after termination. BEFORE alone is the pre-interactive screen result. | `"BEFOREREADY"`; exact body; `ERROROUT.WP5` |
| CMD51-205 (Macro IF ELSE and GO LABEL control flow); WP51-059, WP51-060 | macro: IF1 chooses TRUE, IF0 chooses FALSE through ELSE; GO/LABEL skips SKIP and produces TAIL. | `"TRUEFALSETAIL"`; exact body; `FLOWOUT.WP5` |
| CMD51-206 (Handle a macro failed search with ON NOT FOUND); WP51-059, WP51-060 | macro: ON NOT FOUND/GO MISS catches failed search; SHOULDNOT skipped. | `"BEFOREHANDLED"`; exact body; `ERROROUT.WP5` |
| CMD51-207 (Default merge inserts a page break between records); WP51-062 | merge-primary: Default two-record Hello/FIELD1/HR primary, no explicit hard page: automatic separating hard page observed. | `"Hello Alice\n\fHello Bob\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-208 (PAGE OFF suppresses automatic merge page breaks); WP51-062 | merge-primary: Same primary plus PAGE OFF: no automatic separator; both records on page1. | `"Hello Alice\nHello Bob\n"`; hard pages=0; `MERGED.WP5` |
| CMD51-209 (Merge IF BLANK and ELSE select per-record output); WP51-062 | merge-primary: Field2 YES for Alice, genuinely empty for Bob; IF BLANK/ELSE emits FILLED/EMPTY; no residual merge commands in inspected result. | `"FILLED Alice\fEMPTY Bob"`; hard pages=1; `MERGED.WP5` |
| CMD51-210 (ON ERROR handles a missing nested macro); WP51-059, WP51-060 | macro: ON ERROR/GO ERR catches absent nested macro; SHOULDNOT skipped. | `"HANDLED"`; exact body; `ERROROUT.WP5` |
| CMD51-212 (Nested child error handler is local and parent handler resumes); WP51-059, WP51-060 | macro-nested: Child handles its missing-file error locally and RETURNs; parent R resumes, then parent original handler catches another missing-file error. Child does not inherit parent handler. | `"PCHILDRPARENT"`; exact body; `RESULT.WP5` |
| CMD51-213 (Unhandled child macro error returns to parent handler); WP51-059, WP51-060 | macro-nested: Unhandled child missing-file error defaults to RETURN ERROR; parent catches it. CHILDBAD and PARENTBAD continuations do not execute. | `"PCPARENT"`; exact body; `RESULT.WP5` |
| CMD51-214 (FOR loops include endpoints with positive and negative steps); WP51-059, WP51-060 | macro-loop: FOR1..3 step1 followed by FOR3..1 step-1; inclusive endpoints and DONE marker observed. | `"123/321DONE"`; exact body; `RESULT.WP5` |
| CMD51-215 (WHILE skips a false condition and terminates after variable updates); WP51-059, WP51-060 | macro-loop: WHILE0 skips BAD; N initialized0 and incremented until3; second WHILE emits0,1,2. | `"012DONE"`; exact body; `RESULT.WP5` |
| CMD51-216 (PAGE ON restores automatic merge separators after PAGE OFF); WP51-062 | merge-primary: Primary starts PAGE OFF, emits current record line, then PAGE ON; following automatic boundary restored, no explicit hard page in primary. | `"Hello Alice\n\fHello Bob\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-217 (Resume merge pagination after several PAGE OFF records); WP51-062 | merge-primary: Alice/Bob have empty field2→PAGE OFF; Carol/Dave YES→PAGE ON. Carol remains on first page; separator appears before Dave. | `"Hello Alice\nHello Bob\nHello Carol\n\fHello Dave\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-218 (FOR EACH preserves explicit order and repeated values); WP51-059, WP51-060 | macro-loop: FOR EACH numeric list15,10,15,5 retains order and duplicate15. | `"15/10/15/5/DONE"`; exact body; `RESULT.WP5` |
| CMD51-219 (NEXT skips the rest of a FOR iteration); WP51-059, WP51-060 | macro-loop: FOR1..3 NEXT at2 skips remaining body only for that iteration;3 and DONE survive. | `"1X3XDONE"`; exact body; `RESULT.WP5` |
| CMD51-220 (BREAK inside IF exits the enclosing FOR); WP51-059, WP51-060 | macro-loop: FOR1..5 BREAK inside IF at3 exits enclosing FOR before emitting3, rather than merely leaving IF. | `"12DONE"`; exact body; `RESULT.WP5` |
| CMD51-221 (BREAK exits only the current nested FOR level); WP51-059, WP51-060 | macro-loop: Outer I1..2, inner J1..3 BREAK atJ2 exits inner only; both outer R continuations survive. | `"11R21RDONE"`; exact body; `RESULT.WP5` |
| CMD51-222 (Mixed FOR and WHILE loops reset and advance inner state); WP51-059, WP51-060 | macro-loop: Outer FOR resets J0; inner WHILE J<2 emits pair and increments; reset/order/termination observed. | `"10/11/20/21/DONE"`; exact body; `RESULT.WP5` |
| CMD51-223 (Nested primary PAGE ON remains active after return); WP51-062 | merge-nested-primary: Parent PAGE OFF, child PAGE ON; child uses same current record; setting remains ON after return. | `"PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-224 (Nested primary PAGE OFF remains active after return); WP51-062 | merge-nested-primary: Parent PAGE ON, child PAGE OFF; setting remains OFF after return; no automatic separator. | `"PAlice\nCAlice\nR\nPBob\nCBob\nR\n"`; hard pages=0; `MERGED.WP5` |
| CMD51-225 (Parent restores PAGE ON after nested primary PAGE OFF); WP51-062 | merge-nested-primary: Parent PAGE ON, child PAGE OFF; parent explicitly restores ON after return, before following boundary. | `"PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-226 (FOR EACH preserves raw and quoted string values); WP51-059, WP51-060 | macro-values: FOR EACH quoted list red/blue sky/red then unquoted list; quoted section retains literal quotes, spaces and duplicates. No general quote-unescaping rule inferred. | `"\"red\"/\"blue sky\"/\"red\"/RAW:red/blue sky/red/DONE"`; exact body; `RESULT.WP5` |
| CMD51-227 (FOR EACH evaluates arithmetic and variable-containing expressions); WP51-059, WP51-060 | macro-values: ASSIGN B4; FOR EACH1+2, VARIABLE B+4, VARIABLE B+1 evaluates3,8,5; no claim about deferred timing or arbitrary expression coercion. | `"3/8/5/DONE"`; exact body; `RESULT.WP5` |
| CMD51-228 (NEXT advances only the current nested loop); WP51-059, WP51-060 | macro-loop: I1..2 and J1..3; NEXT atJ2 advances inner only; J3 and outer R survive. | `"11/13/R21/23/RDONE"`; exact body; `RESULT.WP5` |
| CMD51-229 (Top-level macro file BREAK is ignored); WP51-059, WP51-060 | macro-file: No enclosing IF/loop: A BREAK BDONE produces ABDONE. BREAK ignored in this top-level macro fixture. | `"ABDONE"`; exact body; `RESULT.WP5` |
| CMD51-230 (File-level BREAK in the nested macro fixture is ignored); WP51-059, WP51-060 | macro-nested: Parent P nests child C BREAK CHILDBAD then emits RDONE. Child remainder runs; file-level BREAK ignored in this nested macro fixture. | `"PCCHILDBADRDONE"`; exact body; `RESULT.WP5` |
| CMD51-231 (File-level BREAK ends one primary merge iteration); WP51-062 | merge-primary: Root primary emits P/FIELD1/HR, BREAK then BAD. BREAK skips BAD, ends current copy; next record still processed. | `"PAlice\n\fPBob\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-232 (File-level BREAK in a secondary terminates the merge); WP51-062 | merge-secondary: Root secondary Alice then BREAK before Bob; primary Hello/FIELD1/HR. Merge terminates before Bob but already-started second copy remains, including space and final hard return. | `"Hello Alice\n\fHello \n"`; hard pages=1; `MERGED.WP5` |
| CMD51-233 (Nested secondary PAGE ON persists on return); WP51-062 | merge-nested-secondary: Root OFF, child ON: Alice,Carol,Dave,Bob,Eve. NEST record replaced; IGNORED suffix absent. Child ON survives return. | `"Hello Alice\nHello Carol\n\fHello Dave\n\fHello Bob\n\fHello Eve\n"`; hard pages=3; `MERGED.WP5` |
| CMD51-234 (Nested secondary PAGE OFF persists on return); WP51-062 | merge-nested-secondary: Root ON, child OFF: same record order, suffix ignored. Separator before Carol remains; child OFF survives return. | `"Hello Alice\n\fHello Carol\nHello Dave\nHello Bob\nHello Eve\n"`; hard pages=1; `MERGED.WP5` |
| CMD51-235 (Parent secondary explicitly restores PAGE ON after child OFF); WP51-062 | merge-nested-secondary: Root ON, child OFF, Bob explicitly restores ON: separators before Carol and Eve; restoration affects following boundary. | `"Hello Alice\n\fHello Carol\nHello Dave\nHello Bob\n\fHello Eve\n"`; hard pages=2; `MERGED.WP5` |
| CMD51-236 (File-level BREAK in a nested primary returns to its parent); WP51-062 | merge-nested-primary: Child emits C/FIELD1/HR then BREAK/CHILDBAD. Child returns early, remainder skipped; parent R continuation appears for each Alice/Bob copy. | `"PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n"`; hard pages=1; `MERGED.WP5` |

## Context boundaries that implementation must preserve

The table is the acceptance oracle for these fixtures; the following are bounded
consequences, not claims about undocumented internals:

- Quoted FOR EACH values retain literal quotes in the observed list. Unquoted
  `blue sky` retains its space; duplicate red is retained. Do not apply ordinary
  programming-language quote stripping. Arithmetic/VARIABLE examples evaluate to
 3/8/5 but do not establish lazy/eager timing across mutations, general numeric
  coercion, string escape rules or evaluation errors. Those remain new probes.
- Loop BREAK inside IF in the observed FOR exits the enclosing loop; inner FOR
  BREAK exits only that loop. NEXT skips the rest of the selected iteration,
  retaining J3 and outer continuations. IF-only BREAK and other loop families
  remain unrun; do not generalize the loop table to merge record controls.
- File-level BREAK with no enclosing loop/IF is ignored in the tested root and
  child macros. This is an observed discrepancy from blindly applying REF's
  generic nested-file wording; no cause is established. Root-primary BREAK ends
  the current copy and continues the next record; child-primary BREAK returns
  to parent; root-secondary BREAK terminates the merge and retains partial copy.
  It would be wrong to model all these as one RETURN, stop-all, or rollback.
- In the partial-secondary fixture the exact final fragment is `Hello ` plus
  hard return, after a separating hard page. Bob is absent. Trailing space and
  final return are evidence; there is no transactional rollback. The internal
  stage responsible for the final return is not inferred.
- A child primary uses the same secondary record and parent resumes after NEST.
  PAGE changes survive return until explicitly reversed. By contrast the observed
  child macro starts with default error handling; after a handled child returns,
  the parent's original handler resumes. A generic dynamically inherited context
  shared by both languages would contradict at least one observation.
- Nested secondary replaces the nesting record; following IGNORED field text is
  absent and parent resumes at its next record. Root Alice, child Carol/Dave,
  parent Bob/Eve ordering is exact. Child PAGE state survives return. Restoration
  in Bob affects the Eve boundary; PAGE ON does not retroactively insert a break
  before the record where it executes.
- Explicit hard page in the early merge fixture combines with automatic copy
  separators and ends at page4, with blank pages. It is not evidence of two-page
  letter fidelity. Default/PAGE OFF/PAGE ON later fixtures isolate automatic
  separators without an explicit page in primary. Hard/soft layout remains WP07.

Conceptual implementation state should distinguish macro program counter,
call/loop stack, local handlers and editor/session commands from merge primary
stack, secondary record cursor/stack, current field/copy progress, global PAGE
setting and output. This is a proposed boundary, not an original internal design.
Do not decide variable/name scope, error propagation or partial-output policy for
other contexts until their fixtures establish it. Unsupported or malformed input
must not be reported as a successful full-language execution.

## Native and command authoring boundaries

WPM observed header tuple is product/type/major/minor **1/1/1/1**, with a four-entry
index. Documents used for merge have **1/10/0/1**; file extension is not authority.
The recorded ABC macro starts at offset70; its ten body bytes are
`0cfc4100420043000000`. SDK WP92–93 describes two-byte command/character units and
terminal nulls. This one fixture does not decode all opcodes, description layouts,
other producers or character sets; WP01's document parser explicitly refuses WPM.
Do not run the document single-byte text iterator over a WPM stream.

Merge primary/secondary files use document framing with DE enhanced commands
and original field/record representation. WP01 observed empty-payload L4 DE
functions contradict a prose minimum-size assumption; retain L+4 framing and
verify each subfunction payload separately. End Field/End Record, fields, command
arguments and nested filenames need their own original contracts. A plain text
export or conversion to JSON cannot replace the companion/native format.
Unknown command bytes and unused prefix information remain retained in no-edit
exports; unsafe semantic rewrites are refused, not silently skipped.

Original Macro Editor command insertion uses Ctrl+PgUp/Name Search; key tokens
use Ctrl+V and the captured `Press Command Key:` prompt. Literal typed braces do
not create executable command tokens. ON ERROR/ON NOT FOUND with GO action use
two terminating tildes in these source recipes (label and action termination).
Retain exact WPM plus editor-source screen/trace and archived recipe; a pretty
printed pseudocode listing is not proof of token identity. Recording, stopping,
editing, Repeat Value, search DISPLAY behavior and prompt cancellation are
separate user-visible operations, not only an evaluator that emits text.

## Unrun gaps and retained full language scope (T027)

| Canonical case (title) | Feature | Current evidence |
| --- | --- | --- |
| CMD51-133 (Stop a running macro) | WP51-059 | not-run; not-implemented |
| CMD51-179 (Convert a 4.x macro with MACROCNV) | WP51-061 | not-run; not-implemented |
| CMD51-199 (Round-trip an original WPM macro) | FMT51-006 | not-run; not-implemented |

Those pending cases are not covered by a macro that happened to stop on error,
by existing original WPM authorship, or by converted graphics. Retain all
WP51-059 recording/execution/editor prompts/keys, cancellation, editing and macro
assignment/path behavior; all WP51-060 commands, expressions, variables, value
tables and documentary appendix commands; WP51-061 MACROCNV input variants,
reports/errors/partial conversion; WP51-062 merge file/data/command/record options;
and FMT51-006 native serialization across supported producers. WP08's converter
starter requires a provenance-cleared4.x input and format contract first; it
remains unrun. These groups' complete manual locators/statuses remain canonical,
not reclassified by the selected observed cases.

Further original-only probes, to be authored by WP12 with new/expanded canonical
case links and immutable source/native evidence:

| Gap | Exact next experiment and expected information; no claimed result |
| --- | --- |
| Strings/expressions | FOR EACH empty first/middle/last values, literal tildes/quotes/escaped input, extended characters; mutate a referenced variable between iterations to establish evaluation timing. Capture type/error behavior, coercion, precedence and undefined variables separately. |
| Loop scope | IF-only BREAK, BREAK/NEXT in WHILE and FOR EACH, mixed/deeper nesting and handler-triggered loop exits; unmatched END, zero/negative/nonterminating steps and invalid expressions. Record exact last output and post-error state. |
| Handler actions | ON NOT FOUND inside child with/without local override, three-level missing-file chain, explicit RETURN ERROR/QUIT/CHAIN/CALL actions, error within handler, resetting actions and cancelled prompts. No inherited-handler shortcut. |
| File BREAK | Repeat root/child macro fixtures with DISPLAY ON and independent command-entry corroboration; add third nesting level and IF-only/file placement. Compare primary and secondary separately, varying output prefix/suffix and template fields to locate partial-copy boundary without guessing rollback. |
| Merge data | Empty versus absent versus space-only fields; empty/final records and End C/A; field errors and more records; nested secondary at first/last record, nested primary+secondary combinations, paths/missing child/errors, deep/cyclic nesting and page controls together. Capture copy/record resume position and partial output. |
| Interaction/resources | Stop/cancel while running, recording/editing descriptions and controls, repeated command/resource errors, source read/write conflicts and DOS path mappings; historical DOS corroboration and printer-sensitive layout qualification. |

## Bounded implementation proposals for WP12

These are research-to-implementation slices, not created WPs or authorized claims
that the complete language is ready. Reuse the existing Go/native/editing/storage
boundaries; preserve native formats, unknown bytes and source files.

1. **WPM read/no-edit slice:** use the recorded ABC WPM, then the control/handler
   sources from the sealed runs. Publish a field/token contract for DOS header,
   description/index/body/terminator, known opcode widths and argument boundaries.
   Preserve opaque tokens and distinguish unsupported version/command from corrupt
   framing. Add truncated/odd token, bad offsets/lengths/terminators and unknown
   opcode cases, bounded traversal/memory and measured fuzz budgets before reader
   acceptance. Native no-edit export must compare bytes/hashes; original source
   editing/retrieval is an independent compatibility check. No general WPM writer.
2. **Recorded-macro command replay:** decode only the original recorded ABC/key
   subset with exact editor/session preconditions; compare same-buffer and Doc2
   Repeat Value outputs with original fixtures. Recording UI/editor serialization
   and stop-running remain separately gated. Unsupported keystrokes/prompts get
   explicit refusal rather than disappearing from a purported successful replay.
3. **Macro control evaluator:** add IF/ELSE/GO/LABEL then bounded ASSIGN/VARIABLE,
   FOR/WHILE/FOR EACH/NEXT/BREAK subsets from the table, retaining literal string
   observations. Resolve tokens and execution in macro context; reproduce full
   completion/continuation markers and error outcomes. Add local handler/call
   frames only after the error-source token contract, then compare both local and
   propagated child-error fixtures. File BREAK must preserve the two observed
   macro outcomes. Do not import primary/secondary BREAK semantics.
4. **Merge file/field evaluator:** separately decode native secondary field/record
   boundaries and primary command payloads. First reproduce the default/PAGE OFF/
   conditional pair fixtures, then PAGE ON timing. Add nested primary call/return,
   then nested-secondary replacement/resume with exact ordering. Global PAGE state
   and output/copy progress must reproduce the recorded boundaries and partial
   secondary termination; source bytes remain untouched. Do not substitute an
   all-or-nothing output transaction for the original partial result.
5. **Writers/editor/conversion and full-language closure:** native WPM/merge authoring
   needs its own field invariants, unrelated-byte preservation and original
   retrieve/edit/execute/save checks. MACROCNV source formats/reports and every
   remaining command/value-table/record option stay explicit work. Do not infer
   writer or editor parity from an interpreter passing existing output fixtures.

Each future slice declares supported opcodes **and contexts**, input/token/call/
loop/output budgets and user-visible resource-limit failure before tests. Budgets
are implementation safeguards to be measured, not asserted DOS language limits.
Preflight unsupported statically discoverable instructions before execution where
possible. Unknown dynamic nested input/error remains explicit and preserves source;
retain partial diagnostics and distinguish unsupported execution from the normal
observed partial merge result. Never silently ignore unsupported commands or
invent an original error message. Add safe cancellation/instruction-budget tests
for cycles/nontermination without modifying raw evidence. Tests must compare
native/token preservation, session effects and original output separately;
self-generated output alone cannot establish differential conformance.

## Reproducible input and native-output audit

All paths are repository-relative. The ledger pins sealed manifests plus source
reports, native result metadata and expected body/text. All selected source/output
files, capture evidence, runner archives and repeated native bytes are validated
through the pinned run manifests. Proprietary runtime/media remain private cache.

<!-- WP09_AUDIT_BEGIN -->
```json
{
"source_inputs": [
{"path": "docs/research/command-scenarios.json", "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"},
{"path": "docs/research/feature-inventory.json", "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"},
{"path": "docs/research/reference-baseline.json", "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"},
{"path": "docs/research/reference-environment/advanced-native-validation.json", "sha256": "11771442ff44f95c7680f3be6a7c2230586913a428d8005ded8a1761c8e1cac2"},
{"path": "docs/research/reference-environment/advanced-output-comparison.json", "sha256": "04748ab734008513ed02e851aeae812d16a5daeb6cdc34f3ade324c2e7d325ac"},
{"path": "docs/research/reference-environment/advanced-probes.md", "sha256": "2526a581bea3b57ad40acfd4269d9bb8809e7617b41575887f855f92abd97b69"},
{"path": "docs/research/reference-environment/environment.json", "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"},
{"path": "docs/research/reference-environment/extended-output-comparison.json", "sha256": "38c35b93a48ab09152219e75b69d3ad8acef031a763906bc3ea4fa34e40db20c"},
{"path": "docs/research/reference-environment/extended-probes.md", "sha256": "6bbec3c3a66dddff1466e10a6d62fa6ce0a7da7deb2dfa64e119d299b12e1963"},
{"path": "docs/research/reference-environment/history-loops-probes.md", "sha256": "1b586a58b3c069bf723efdf641e2199e6aa94be528dc712711510e875ab7f14a"},
{"path": "docs/research/reference-environment/history-native-validation.json", "sha256": "6dd77b00bcc9d05073d34fc478316db86e6a2778b37b3bf3fc5b7b396a4baba9"},
{"path": "docs/research/reference-environment/history-output-comparison.json", "sha256": "15199f4ec0765ba73b8cf8a6423f909132961a2176aeb08ea256b675a2ef61a5"},
{"path": "docs/research/reference-environment/iteration-native-validation.json", "sha256": "18fa5c80b91ba90898337c787e9e8a831ce42a09b9401956b4af8044dbca0554"},
{"path": "docs/research/reference-environment/iteration-nesting-probes.md", "sha256": "554ea350562ecb15f091ae8122c1aedcf9d465a9f5d68af0d6f1f3c45bcf708a"},
{"path": "docs/research/reference-environment/iteration-output-comparison.json", "sha256": "b252fbf085a26a37b7e5416a9d343f8fb83a949ec027d0b6bb7c93c3708a4281"},
{"path": "docs/research/reference-environment/resource-profile.json", "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"},
{"path": "docs/research/reference-environment/values-native-validation.json", "sha256": "adead32f67f2577272eaeb98924cb857f943976726af6fd442ae0baea6bd6413"},
{"path": "docs/research/reference-environment/values-output-comparison.json", "sha256": "8ca14fbedf0ec9f781b5d47a9a8d980b7ef11352356a072cc37ee327d4556124"},
{"path": "docs/research/reference-environment/values-secondary-probes.md", "sha256": "ad8fdf83bc061f4cb87513d7c9675fbc5cb38ef24b912d423fe39e0760a42ac5"},
{"path": "docs/research/reference-runs/2026-10-29-advanced-03/run.json", "sha256": "6abdb82bb54d9cd1a3d0a6089977cdfa1086c5cc484f27cc067e176626b16610"},
{"path": "docs/research/reference-runs/2026-10-29-advanced-04/run.json", "sha256": "ae9bc9fda6091903b04c07b2894c487074a4c01edec656667b8a75da8dbbceb8"},
{"path": "docs/research/reference-runs/2026-10-29-extended-03/run.json", "sha256": "68450fd8efa5deea93e83021b043ad0a9ab1ada4867e5d5616c49fcf7c1d7809"},
{"path": "docs/research/reference-runs/2026-10-29-extended-04/run.json", "sha256": "c7d98c6225892261dff38b88b3c9c044856ad43ad4e5776d4197089d885ac0fc"},
{"path": "docs/research/reference-runs/2026-10-29-history-01/run.json", "sha256": "4075080561b4b2215aac7f7b8df64f9b2ddfe6dcc2dd010a092515e3f59fc0da"},
{"path": "docs/research/reference-runs/2026-10-29-history-02/run.json", "sha256": "08e77a5ae04175697da06884a3ce01c1eddcd8e77780c163ae0eb36fe361057d"},
{"path": "docs/research/reference-runs/2026-10-29-iteration-01/run.json", "sha256": "d405f25a3e3e94cd7ecc1d9cda95ef9a0d7b0ff7faf06bd8d4af6220af4d5d7e"},
{"path": "docs/research/reference-runs/2026-10-29-iteration-02/run.json", "sha256": "1941c3245bed0e6c5e79ba55ba86420bfb766cc3a1dd9fd311bde1430c74a1f2"},
{"path": "docs/research/reference-runs/2026-10-30-values-01/run.json", "sha256": "827744274753d2043c91b1d543c62b47d6b9dfc4422f3e24cc2bceb0462f4bde"},
{"path": "docs/research/reference-runs/2026-10-30-values-02/run.json", "sha256": "b802beb2fb1209064dd6d576804e1c9d7b42cf98b3c8174c908fbb61d22ed2e2"},
{"path": "docs/research/sources.json", "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md", "sha256": "e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/editing.md", "sha256": "7f542edd647b8735575036b0be570a88b048c5ea97755f25dbddadf92ce3a4bd"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md", "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md", "sha256": "aa6384662a74c1c0451a506bd9fdd169420614c558677a40715fbe0bab906631"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json", "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md", "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/structured-graphics.md", "sha256": "32a9fa1352c2a07fb754a7d6211cc43f8b356542ce816d7b42c3a9d5a0f425a6"},
{"path": "research/cache/WP51DevelopersToolkit.pdf", "sha256": "5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754"},
{"path": "research/cache/WPDOS51Reference.pdf", "sha256": "ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531"},
{"path": "research/cache/reference.txt", "sha256": "f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c"},
{"path": "research/cache/toolkit.txt", "sha256": "8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f"},
{"path": "scripts/reference/document.py", "sha256": "dfb646f08ec21c8549b3e0d99e0efe285185ffa178e2b65b2df02a6b7e22296d"},
{"path": "scripts/reference/verify_advanced_bodies.py", "sha256": "1290d210aa65c0dff88cbb0f06904945e8b1d8e6ca185193b82a9fc0d6491ecc"}
],
"rows": [
{"case_id": "CMD51-131", "title": "Record and execute a named macro", "feature_ids": ["WP51-059"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 373, "printed_end": 379, "pdf_start": 390, "pdf_end": 396}], "context": "macro-record", "observation": "Record ABC, stop, execute in same buffer; recording and execution are distinct actions.", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "runner": "extended.py", "expected": {"filename": "MACROOUT.WP5", "kind": "body", "expected_hex": "414243414243", "expected_text": "ABCABC"}, "result": {"path": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/MACROOUT.WP5", "size": 330, "sha256": "21c4619a3d219a676db3678ed96dd1fe488e4956af50a47c7c2d9e052dc9af1c", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-132", "title": "Repeat a macro using Repeat Value", "feature_ids": ["WP51-059"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 379, "printed_end": 379, "pdf_start": 396, "pdf_end": 396}], "context": "macro-record", "observation": "Record ABC, switch to blank Doc2, Repeat Value3 then execute.", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "runner": "extended.py", "expected": {"filename": "REPEAT.WP5", "kind": "body", "expected_hex": "414243414243414243", "expected_text": "ABCABCABC"}, "result": {"path": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-132/REPEAT.WP5", "size": 333, "sha256": "216dd8e04abb7678a4cb7444b4c4fbace5cab15c38eab0fffe43c96a1c8e9ced", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-134", "title": "Merge original primary and secondary files", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 420, "printed_end": 433, "pdf_start": 437, "pdf_end": 450}], "context": "merge-primary", "observation": "Primary contains Hello/FIELD1 and explicit hard page; automatic copy separators also occur. Actual result has blank pages and final cursor page4, not a two-page letter.", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "runner": "extended.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\f\fHello Bob\f", "hard_pages": 3}, "result": {"path": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-134/MERGED.WP5", "size": 683, "sha256": "8a2782895e3605538f56f656499df83c0e460fb25458b6cccbaee9aeb6b96bd3", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-178", "title": "Macro stops on a default failed search", "feature_ids": ["WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 379, "printed_end": 379, "pdf_start": 396, "pdf_end": 396}], "context": "macro", "observation": "Default DISPLAY OFF failed search stops before SHOULDNOT; original saved result includes manually typed READY after termination. BEFORE alone is the pre-interactive screen result.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "ERROROUT.WP5", "kind": "body", "expected_hex": "4245464f52455245414459", "expected_text": "BEFOREREADY"}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-178/ERROROUT.WP5", "size": 335, "sha256": "d89e5807d8ec6467c47052959880d4d964a3668520e6dd94981228d6d755b8ea", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-205", "title": "Macro IF ELSE and GO LABEL control flow", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 381, "printed_end": 381, "pdf_start": 398, "pdf_end": 398}, {"source_id": "REF51", "printed_start": 383, "printed_end": 383, "pdf_start": 400, "pdf_end": 400}, {"source_id": "REF51", "printed_start": 384, "printed_end": 384, "pdf_start": 401, "pdf_end": 401}, {"source_id": "REF51", "printed_start": 822, "printed_end": 822, "pdf_start": 839, "pdf_end": 839}, {"source_id": "REF51", "printed_start": 823, "printed_end": 823, "pdf_start": 840, "pdf_end": 840}, {"source_id": "REF51", "printed_start": 824, "printed_end": 824, "pdf_start": 841, "pdf_end": 841}], "context": "macro", "observation": "IF1 chooses TRUE, IF0 chooses FALSE through ELSE; GO/LABEL skips SKIP and produces TAIL.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "FLOWOUT.WP5", "kind": "body", "expected_hex": "5452554546414c53455441494c", "expected_text": "TRUEFALSETAIL"}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-205/FLOWOUT.WP5", "size": 337, "sha256": "4737b9e891dda361a6b146e5dc3d571e73cef2e328a18f943032d73cb05a3c01", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-206", "title": "Handle a macro failed search with ON NOT FOUND", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 843, "printed_end": 843, "pdf_start": 860, "pdf_end": 860}, {"source_id": "REF51", "printed_start": 846, "printed_end": 846, "pdf_start": 863, "pdf_end": 863}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}], "context": "macro", "observation": "ON NOT FOUND/GO MISS catches failed search; SHOULDNOT skipped.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "ERROROUT.WP5", "kind": "body", "expected_hex": "4245464f524548414e444c4544", "expected_text": "BEFOREHANDLED"}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-206/ERROROUT.WP5", "size": 337, "sha256": "2c2123b2cbd4a581e0558edd8e30bfe909bbd4ea86f575397e716da9e4f6bb78", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-207", "title": "Default merge inserts a page break between records", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 420, "printed_end": 420, "pdf_start": 437, "pdf_end": 437}, {"source_id": "REF51", "printed_start": 423, "printed_end": 423, "pdf_start": 440, "pdf_end": 440}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "SDK51", "printed_start": 17, "printed_end": 18, "pdf_start": 30, "pdf_end": 31}, {"source_id": "SDK51", "printed_start": 55, "printed_end": 55, "pdf_start": 68, "pdf_end": 68}], "context": "merge-primary", "observation": "Default two-record Hello/FIELD1/HR primary, no explicit hard page: automatic separating hard page observed.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\n\fHello Bob\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-207/MERGED.WP5", "size": 619, "sha256": "032ffe0a99168179a11a3d7bd2d2da743871a466aab1c60848259f0bb5701905", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-208", "title": "PAGE OFF suppresses automatic merge page breaks", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}, {"source_id": "SDK51", "printed_start": 17, "printed_end": 18, "pdf_start": 30, "pdf_end": 31}, {"source_id": "SDK51", "printed_start": 55, "printed_end": 55, "pdf_start": 68, "pdf_end": 68}], "context": "merge-primary", "observation": "Same primary plus PAGE OFF: no automatic separator; both records on page1.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\nHello Bob\n", "hard_pages": 0}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-208/MERGED.WP5", "size": 586, "sha256": "fa3de155c57c6967d88623bca1bb52cc3045b98dd3e9993df437e34e11fe0824", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-209", "title": "Merge IF BLANK and ELSE select per-record output", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 824, "printed_end": 824, "pdf_start": 841, "pdf_end": 841}, {"source_id": "REF51", "printed_start": 825, "printed_end": 825, "pdf_start": 842, "pdf_end": 842}], "context": "merge-primary", "observation": "Field2 YES for Alice, genuinely empty for Bob; IF BLANK/ELSE emits FILLED/EMPTY; no residual merge commands in inspected result.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "FILLED Alice\fEMPTY Bob", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-209/MERGED.WP5", "size": 618, "sha256": "ac9c388920bd3d2909571713589b7bb475aad6fc21af2798e5c6b0df991e1afc", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-210", "title": "ON ERROR handles a missing nested macro", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 843, "printed_end": 843, "pdf_start": 860, "pdf_end": 860}, {"source_id": "REF51", "printed_start": 844, "printed_end": 844, "pdf_start": 861, "pdf_end": 861}, {"source_id": "REF51", "printed_start": 845, "printed_end": 845, "pdf_start": 862, "pdf_end": 862}], "context": "macro", "observation": "ON ERROR/GO ERR catches absent nested macro; SHOULDNOT skipped.", "run": "2026-10-29-advanced-04", "repeat": "2026-10-29-advanced-03", "runner": "advanced.py", "expected": {"filename": "ERROROUT.WP5", "kind": "body", "expected_hex": "48414e444c4544", "expected_text": "HANDLED"}, "result": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-210/ERROROUT.WP5", "size": 331, "sha256": "fa749310a5c2a6c9fd8a4ba83f7264fcbf8de0f4cee9bbb1fe1816c4e552273a", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-212", "title": "Nested child error handler is local and parent handler resumes", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 836, "printed_end": 836, "pdf_start": 853, "pdf_end": 853}, {"source_id": "REF51", "printed_start": 837, "printed_end": 837, "pdf_start": 854, "pdf_end": 854}, {"source_id": "REF51", "printed_start": 843, "printed_end": 843, "pdf_start": 860, "pdf_end": 860}, {"source_id": "REF51", "printed_start": 844, "printed_end": 844, "pdf_start": 861, "pdf_end": 861}, {"source_id": "REF51", "printed_start": 845, "printed_end": 845, "pdf_start": 862, "pdf_end": 862}], "context": "macro-nested", "observation": "Child handles its missing-file error locally and RETURNs; parent R resumes, then parent original handler catches another missing-file error. Child does not inherit parent handler.", "run": "2026-10-29-history-02", "repeat": "2026-10-29-history-01", "runner": "history_loops.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "504348494c4452504152454e54", "expected_text": "PCHILDRPARENT"}, "result": {"path": "docs/research/reference-runs/2026-10-29-history-02/CMD51-212/RESULT.WP5", "size": 337, "sha256": "bd1965f29b3f0178b6579f4cc134ea24df9eef8005481ed3c32083c66cd7e7c9", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-213", "title": "Unhandled child macro error returns to parent handler", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 836, "printed_end": 836, "pdf_start": 853, "pdf_end": 853}, {"source_id": "REF51", "printed_start": 837, "printed_end": 837, "pdf_start": 854, "pdf_end": 854}, {"source_id": "REF51", "printed_start": 843, "printed_end": 843, "pdf_start": 860, "pdf_end": 860}, {"source_id": "REF51", "printed_start": 844, "printed_end": 844, "pdf_start": 861, "pdf_end": 861}, {"source_id": "REF51", "printed_start": 845, "printed_end": 845, "pdf_start": 862, "pdf_end": 862}], "context": "macro-nested", "observation": "Unhandled child missing-file error defaults to RETURN ERROR; parent catches it. CHILDBAD and PARENTBAD continuations do not execute.", "run": "2026-10-29-history-02", "repeat": "2026-10-29-history-01", "runner": "history_loops.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "5043504152454e54", "expected_text": "PCPARENT"}, "result": {"path": "docs/research/reference-runs/2026-10-29-history-02/CMD51-213/RESULT.WP5", "size": 332, "sha256": "6bff5d74053441bdd5641b38e8dc0a7a9620bf95d73c6b098a84d2c35b4ca469", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-214", "title": "FOR loops include endpoints with positive and negative steps", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 820, "printed_end": 820, "pdf_start": 837, "pdf_end": 837}, {"source_id": "REF51", "printed_start": 821, "printed_end": 821, "pdf_start": 838, "pdf_end": 838}], "context": "macro-loop", "observation": "FOR1..3 step1 followed by FOR3..1 step-1; inclusive endpoints and DONE marker observed.", "run": "2026-10-29-history-02", "repeat": "2026-10-29-history-01", "runner": "history_loops.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "3132332f333231444f4e45", "expected_text": "123/321DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-history-02/CMD51-214/RESULT.WP5", "size": 335, "sha256": "e1990ce3986ed929e1b4bdf7d9745500e1168558ca385d995c883a8123c74756", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-215", "title": "WHILE skips a false condition and terminates after variable updates", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 876, "printed_end": 876, "pdf_start": 893, "pdf_end": 893}], "context": "macro-loop", "observation": "WHILE0 skips BAD; N initialized0 and incremented until3; second WHILE emits0,1,2.", "run": "2026-10-29-history-02", "repeat": "2026-10-29-history-01", "runner": "history_loops.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "303132444f4e45", "expected_text": "012DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-history-02/CMD51-215/RESULT.WP5", "size": 331, "sha256": "c6182c0553b5a85fa46628fd9c1263baae29e355d1b553a09d2c92de86653ae8", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-216", "title": "PAGE ON restores automatic merge separators after PAGE OFF", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-primary", "observation": "Primary starts PAGE OFF, emits current record line, then PAGE ON; following automatic boundary restored, no explicit hard page in primary.", "run": "2026-10-29-history-02", "repeat": "2026-10-29-history-01", "runner": "history_loops.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\n\fHello Bob\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-29-history-02/CMD51-216/MERGED.WP5", "size": 619, "sha256": "032ffe0a99168179a11a3d7bd2d2da743871a466aab1c60848259f0bb5701905", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-217", "title": "Resume merge pagination after several PAGE OFF records", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 825, "printed_end": 825, "pdf_start": 842, "pdf_end": 842}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-primary", "observation": "Alice/Bob have empty field2\u2192PAGE OFF; Carol/Dave YES\u2192PAGE ON. Carol remains on first page; separator appears before Dave.", "run": "2026-10-29-history-02", "repeat": "2026-10-29-history-01", "runner": "history_loops.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\nHello Bob\nHello Carol\n\fHello Dave\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-29-history-02/CMD51-217/MERGED.WP5", "size": 642, "sha256": "503c365788e413c2f515347dfc97e911d181fa27d6b8d1bc53c098b8773565fc", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-218", "title": "FOR EACH preserves explicit order and repeated values", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 822, "printed_end": 822, "pdf_start": 839, "pdf_end": 839}], "context": "macro-loop", "observation": "FOR EACH numeric list15,10,15,5 retains order and duplicate15.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "31352f31302f31352f352f444f4e45", "expected_text": "15/10/15/5/DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-218/RESULT.WP5", "size": 339, "sha256": "863dc4dbd2203715911d580fe26c55893038fae6d420ae4cc6ffbf33e805fafc", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-219", "title": "NEXT skips the rest of a FOR iteration", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 840, "printed_end": 840, "pdf_start": 857, "pdf_end": 857}], "context": "macro-loop", "observation": "FOR1..3 NEXT at2 skips remaining body only for that iteration;3 and DONE survive.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "31583358444f4e45", "expected_text": "1X3XDONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-219/RESULT.WP5", "size": 332, "sha256": "066a40da637c14c5396ba6a48c86710fa4906821fff3750fdb61ae07bf5c8eb0", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-220", "title": "BREAK inside IF exits the enclosing FOR", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}], "context": "macro-loop", "observation": "FOR1..5 BREAK inside IF at3 exits enclosing FOR before emitting3, rather than merely leaving IF.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "3132444f4e45", "expected_text": "12DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-220/RESULT.WP5", "size": 330, "sha256": "8dbe9a5bbb6677861d55e58955495cdfc38126bde961900772724a7935be8c0f", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-221", "title": "BREAK exits only the current nested FOR level", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}], "context": "macro-loop", "observation": "Outer I1..2, inner J1..3 BREAK atJ2 exits inner only; both outer R continuations survive.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "313152323152444f4e45", "expected_text": "11R21RDONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-221/RESULT.WP5", "size": 334, "sha256": "ba8ce3f1e6790dd1c34acfeedf2233b4f8fce56d5d1c3dc0b2c34bba4b61e83b", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-222", "title": "Mixed FOR and WHILE loops reset and advance inner state", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 820, "printed_end": 820, "pdf_start": 837, "pdf_end": 837}, {"source_id": "REF51", "printed_start": 821, "printed_end": 821, "pdf_start": 838, "pdf_end": 838}, {"source_id": "REF51", "printed_start": 876, "printed_end": 876, "pdf_start": 893, "pdf_end": 893}], "context": "macro-loop", "observation": "Outer FOR resets J0; inner WHILE J<2 emits pair and increments; reset/order/termination observed.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "31302f31312f32302f32312f444f4e45", "expected_text": "10/11/20/21/DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-222/RESULT.WP5", "size": 340, "sha256": "5de5e7c036ef9a401814f0ec4bed4df62a73de8b41920fd78e08db5e93727948", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-223", "title": "Nested primary PAGE ON remains active after return", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 838, "printed_end": 838, "pdf_start": 855, "pdf_end": 855}, {"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-nested-primary", "observation": "Parent PAGE OFF, child PAGE ON; child uses same current record; setting remains ON after return.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-223/MERGED.WP5", "size": 625, "sha256": "0d35b4f5959c37592ded95ea8077c3bf335df4ed3a599eb044d82e838e002791", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-224", "title": "Nested primary PAGE OFF remains active after return", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 838, "printed_end": 838, "pdf_start": 855, "pdf_end": 855}, {"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-nested-primary", "observation": "Parent PAGE ON, child PAGE OFF; setting remains OFF after return; no automatic separator.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "PAlice\nCAlice\nR\nPBob\nCBob\nR\n", "hard_pages": 0}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-224/MERGED.WP5", "size": 592, "sha256": "dc95b5da0a3501d53940d163daa60252eb4d41a74c5a14a6735015123b84ae3d", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-225", "title": "Parent restores PAGE ON after nested primary PAGE OFF", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 838, "printed_end": 838, "pdf_start": 855, "pdf_end": 855}, {"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-nested-primary", "observation": "Parent PAGE ON, child PAGE OFF; parent explicitly restores ON after return, before following boundary.", "run": "2026-10-29-iteration-02", "repeat": "2026-10-29-iteration-01", "runner": "iteration_nesting.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-29-iteration-02/CMD51-225/MERGED.WP5", "size": 625, "sha256": "0d35b4f5959c37592ded95ea8077c3bf335df4ed3a599eb044d82e838e002791", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-226", "title": "FOR EACH preserves raw and quoted string values", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 822, "printed_end": 822, "pdf_start": 839, "pdf_end": 839}], "context": "macro-values", "observation": "FOR EACH quoted list red/blue sky/red then unquoted list; quoted section retains literal quotes, spaces and duplicates. No general quote-unescaping rule inferred.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "22726564222f22626c756520736b79222f22726564222f5241573a7265642f626c756520736b792f7265642f444f4e45", "expected_text": "\"red\"/\"blue sky\"/\"red\"/RAW:red/blue sky/red/DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-226/RESULT.WP5", "size": 372, "sha256": "cdd4f3c9b3d0cf63b2faecef0605967e3f98c16a91fd8394914b105cf5cafca9", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-227", "title": "FOR EACH evaluates arithmetic and variable-containing expressions", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 822, "printed_end": 822, "pdf_start": 839, "pdf_end": 839}], "context": "macro-values", "observation": "ASSIGN B4; FOR EACH1+2, VARIABLE B+4, VARIABLE B+1 evaluates3,8,5; no claim about deferred timing or arbitrary expression coercion.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "332f382f352f444f4e45", "expected_text": "3/8/5/DONE"}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-227/RESULT.WP5", "size": 334, "sha256": "86f66a73a637e1d11d24901978652cf129b59dbe1466b59affeb7ba2b7734d3f", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-228", "title": "NEXT advances only the current nested loop", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 840, "printed_end": 840, "pdf_start": 857, "pdf_end": 857}], "context": "macro-loop", "observation": "I1..2 and J1..3; NEXT atJ2 advances inner only; J3 and outer R survive.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "31312f31332f5232312f32332f52444f4e45", "expected_text": "11/13/R21/23/RDONE"}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-228/RESULT.WP5", "size": 342, "sha256": "9177444baf48a3a23442a1f73fea7c3f685db7258b628f1dc543bed46aef9645", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-229", "title": "Top-level macro file BREAK is ignored", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}], "context": "macro-file", "observation": "No enclosing IF/loop: A BREAK BDONE produces ABDONE. BREAK ignored in this top-level macro fixture.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "4142444f4e45", "expected_text": "ABDONE"}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-229/RESULT.WP5", "size": 330, "sha256": "acd3f8ae1a864020beadfc4cc46cc5ecac2dc213166b908fba7e4f8bef6ee053", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-230", "title": "File-level BREAK in the nested macro fixture is ignored", "feature_ids": ["WP51-059", "WP51-060"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}, {"source_id": "REF51", "printed_start": 836, "printed_end": 836, "pdf_start": 853, "pdf_end": 853}, {"source_id": "REF51", "printed_start": 837, "printed_end": 837, "pdf_start": 854, "pdf_end": 854}], "context": "macro-nested", "observation": "Parent P nests child C BREAK CHILDBAD then emits RDONE. Child remainder runs; file-level BREAK ignored in this nested macro fixture.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "RESULT.WP5", "kind": "body", "expected_hex": "50434348494c4442414452444f4e45", "expected_text": "PCCHILDBADRDONE"}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-230/RESULT.WP5", "size": 339, "sha256": "23ac561baeb4380a6706bbbda64c62c40866a0ca9b861806914a2952bf3f7114", "prefix_hex": "ff57504344010000010a000100000000"}},
{"case_id": "CMD51-231", "title": "File-level BREAK ends one primary merge iteration", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}], "context": "merge-primary", "observation": "Root primary emits P/FIELD1/HR, BREAK then BAD. BREAK skips BAD, ends current copy; next record still processed.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "PAlice\n\fPBob\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-231/MERGED.WP5", "size": 609, "sha256": "496f25b90442a327b82d4eb86458cfa0fa4af332108d509effbdcfc19a3476e3", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-232", "title": "File-level BREAK in a secondary terminates the merge", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}], "context": "merge-secondary", "observation": "Root secondary Alice then BREAK before Bob; primary Hello/FIELD1/HR. Merge terminates before Bob but already-started second copy remains, including space and final hard return.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\n\fHello \n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-232/MERGED.WP5", "size": 616, "sha256": "da616ce0d5dc670d66ae5f421371f9cae1ded1e3bce94ec7afdf6bfe400150a7", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-233", "title": "Nested secondary PAGE ON persists on return", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-nested-secondary", "observation": "Root OFF, child ON: Alice,Carol,Dave,Bob,Eve. NEST record replaced; IGNORED suffix absent. Child ON survives return.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\nHello Carol\n\fHello Dave\n\fHello Bob\n\fHello Eve\n", "hard_pages": 3}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-233/MERGED.WP5", "size": 718, "sha256": "3fb96928e3ca18087627d628c92cc8b04f253589335164dcca5dbdfa91565615", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-234", "title": "Nested secondary PAGE OFF persists on return", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-nested-secondary", "observation": "Root ON, child OFF: same record order, suffix ignored. Separator before Carol remains; child OFF survives return.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\n\fHello Carol\nHello Dave\nHello Bob\nHello Eve\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-234/MERGED.WP5", "size": 652, "sha256": "4c20e17063c341ea58d94e46ded5d14e293b5e4bbb0511e4230152f80a9cc25f", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-235", "title": "Parent secondary explicitly restores PAGE ON after child OFF", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 839, "printed_end": 839, "pdf_start": 856, "pdf_end": 856}, {"source_id": "REF51", "printed_start": 847, "printed_end": 847, "pdf_start": 864, "pdf_end": 864}, {"source_id": "REF51", "printed_start": 848, "printed_end": 848, "pdf_start": 865, "pdf_end": 865}], "context": "merge-nested-secondary", "observation": "Root ON, child OFF, Bob explicitly restores ON: separators before Carol and Eve; restoration affects following boundary.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "Hello Alice\n\fHello Carol\nHello Dave\nHello Bob\n\fHello Eve\n", "hard_pages": 2}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-235/MERGED.WP5", "size": 685, "sha256": "50035d643359b5243ad4dfc11385e55d66f49b921f81d10799afd3c407ad1fce", "prefix_hex": "ff57504334020000010a000100000000"}},
{"case_id": "CMD51-236", "title": "File-level BREAK in a nested primary returns to its parent", "feature_ids": ["WP51-062"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 800, "printed_end": 800, "pdf_start": 817, "pdf_end": 817}, {"source_id": "REF51", "printed_start": 801, "printed_end": 801, "pdf_start": 818, "pdf_end": 818}, {"source_id": "REF51", "printed_start": 838, "printed_end": 839, "pdf_start": 855, "pdf_end": 856}], "context": "merge-nested-primary", "observation": "Child emits C/FIELD1/HR then BREAK/CHILDBAD. Child returns early, remainder skipped; parent R continuation appears for each Alice/Bob copy.", "run": "2026-10-30-values-02", "repeat": "2026-10-30-values-01", "runner": "value_secondary.py", "expected": {"filename": "MERGED.WP5", "kind": "merge", "expected_text": "PAlice\nCAlice\nR\n\fPBob\nCBob\nR\n", "hard_pages": 1}, "result": {"path": "docs/research/reference-runs/2026-10-30-values-02/CMD51-236/MERGED.WP5", "size": 625, "sha256": "0d35b4f5959c37592ded95ea8077c3bf335df4ed3a599eb044d82e838e002791", "prefix_hex": "ff57504334020000010a000100000000"}}
],
"pending": [
{"id": "CMD51-133", "title": "Stop a running macro", "feature_ids": ["WP51-059"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 379, "printed_end": 379, "pdf_start": 396, "pdf_end": 396}]},
{"id": "CMD51-179", "title": "Convert a 4.x macro with MACROCNV", "feature_ids": ["WP51-061"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 370, "printed_end": 372, "pdf_start": 387, "pdf_end": 389}]},
{"id": "CMD51-199", "title": "Round-trip an original WPM macro", "feature_ids": ["FMT51-006"], "oracle_status": "not-run", "source_locators": [{"source_id": "SDK51", "printed_start": 92, "printed_end": 99, "pdf_start": 105, "pdf_end": 112}]}
]
}
```
<!-- WP09_AUDIT_END -->

```sh
python3 - <<'PY_AUDIT'
from pathlib import Path
import hashlib,json,re,struct,subprocess,sys
p=Path('kitty-specs/wp51-parity-01M64CVY/contracts/automation.md');text=p.read_text()
a=json.loads(text.split('<!-- WP09_AUDIT_BEGIN -->',1)[1].split('```json\n',1)[1].split('\n```',1)[0])
sha=lambda b:hashlib.sha256(b).hexdigest()
for x in a['source_inputs']:assert sha(Path(x['path']).read_bytes())==x['sha256'],x['path']
features={x['id']:x for x in json.loads(Path('docs/research/feature-inventory.json').read_text())}
cases={x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
sources={x['id']:x for x in json.loads(Path('docs/research/sources.json').read_text())}
sys.path.insert(0,'scripts/reference');from document import plain_merge,prefix
used=set();runs={};counts=0
for row in a['rows']:
    cid=row['case_id'];used.add(cid);c=cases[cid]
    assert (row['title'],row['feature_ids'],row['oracle_status'],row['source_locators'])==(c['title'],c['feature_ids'],c['oracle_status'],c['source_locators'])
    assert c['oracle_status']=='partially-observed' and c['implementation_status']=='not-implemented'
    # Semantic binding, not merely existence of a valid ID/title.
    required='WP51-062' if row['context'].startswith('merge') else ('WP51-059' if row['context']=='macro-record' else 'WP51-060')
    assert required in c['feature_ids'],(cid,row['context'])
    assert all(cid in features[f]['command_scenario_ids'] for f in row['feature_ids'])
    line=next(x for x in text.splitlines() if x.startswith('| '+cid+' ('))
    cols=[x.strip() for x in line.split('|')]
    assert cols[1]==cid+' ('+c['title']+'); '+', '.join(c['feature_ids'])
    assert cols[2]==row['context']+': '+row['observation']
    e=row['expected'];tail='; hard pages='+str(e['hard_pages']) if e['kind']=='merge' else '; exact body'
    assert cols[3]=='`'+json.dumps(e['expected_text'],ensure_ascii=True)+'`'+tail+'; `'+e['filename']+'`'
    for rid in (row['run'],row['repeat']):
        path=Path('docs/research/reference-runs')/rid/'run.json'
        assert str(path) in c['evidence_paths']
        if rid not in runs:
            r=json.loads(path.read_text());runs[rid]=r
            assert r['scope']=='original-reference-only' and not r['wordling_tested']
            assert r['baseline_id']=='wp51-dos-us-1992-03-09'
            base=path.parent
            for src in r['runner_sources']:
                archived=base/'runner-source'/Path(src['path']).name
                assert sha(archived.read_bytes())==src['sha256'],str(archived)
            env=Path(r['environment_profile_archive'])
            assert sha(env.read_bytes())==r['environment_manifest_sha256']
        r=runs[rid];result=next(x for x in r['results'] if x['case_id']==cid)
        assert result['result']=='observed-matches-smoke-expectations'
        assert result['checks'] and all(x['passed'] for x in result['checks'])
        for item in result['evidence']:
            b=Path(item['path']).read_bytes();assert (len(b),sha(b))==(item['size'],item['sha256'])
        for item in result['native_outputs']:
            b=Path(item['path']).read_bytes();assert (len(b),sha(b))==(item['size'],item['sha256'])
            assert any(x['path']==item['path'] and x['sha256']==item['sha256'] for x in result['evidence'])
            other=Path(item['path'].replace(rid,row['repeat'] if rid==row['run'] else row['run']))
            assert other.read_bytes()==b
        output=next(x for x in result['native_outputs'] if Path(x['path']).name==e['filename'])
        b=Path(output['path']).read_bytes();body=struct.unpack_from('<I',b,4)[0]
        if rid==row['run']:assert output==row['result']
        if e['kind']=='body':assert b[body:].hex()==e['expected_hex'] and b[body:]==e['expected_text'].encode('ascii')
        else:
            decoded=plain_merge(b)
            assert (decoded['ascii_text'],decoded['hard_page_count'])==(e['expected_text'],e['hard_pages'])
        assert (path.parent/'runner-source'/row['runner']).exists();counts+=1
for c in a['pending']:
    used.add(c['id']);canonical=cases[c['id']]
    assert all(c[k]==canonical[k] for k in c)
    assert c['oracle_status']=='not-run' and canonical['implementation_status']=='not-implemented'
    assert '| '+c['id']+' ('+c['title']+') | '+', '.join(c['feature_ids'])+' | not-run; not-implemented |' in text
assert set(re.findall(r'CMD51-\d{3}',text))==used
assert len(a['rows'])==35 and counts==70 and len(runs)==10
for sid in ('REF51','SDK51'):
    s=sources[sid];assert sha(Path('research/cache',s['filename']).read_bytes())==s['sha256']
for c in [*a['rows'],*a['pending']]:
    for loc in c['source_locators']:
        assert 1<=loc['pdf_start']<=loc['pdf_end']<=sources[loc['source_id']]['pdf_pages']
        assert loc['pdf_start']==loc['printed_start']+(17 if loc['source_id']=='REF51' else 13)
for pdf,pg,needle in [('WPDOS51Reference.pdf',817,'BREAK'),('WPDOS51Reference.pdf',839,'FOR EACH'),('WPDOS51Reference.pdf',864,'PAGE OFF'),('WP51DevelopersToolkit.pdf',99,'Enhanced Merge Command'),('WP51DevelopersToolkit.pdf',105,'WPM Macro File')]:
    out=subprocess.check_output(['pdftotext','-f',str(pg),'-l',str(pg),'-layout','research/cache/'+pdf,'-'],text=True)
    assert needle in out,(pdf,pg)
macro=Path('docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM').read_bytes()
assert macro[8:12]==bytes([1,1,1,1]) and struct.unpack_from('<I',macro,4)[0]==70
assert macro[70:].hex()=='0cfc4100420043000000'
print('WP09 source/semantic/run/capture/native audits and',counts,'exact result repetitions valid')
PY_AUDIT
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp09-review.xml
```

Author validation: embedded source/hash/canonical-title/feature/context/locator and
sealed-run/capture/native evidence audit passes all 70 exact result repetitions.
Both catalogue checks and the genuine configured regression runner pass (JUnit
`/tmp/wp09-review.xml`). Go discovery passes; build/test/vet explicitly skip the
planning checkout with no Go packages, which does not test approved code lanes.
A negative full-audit substitution of a valid merge case/title into a macro row
is rejected by the context-to-feature assertion. No new original probe,
interpreter, writer, queue/registry change or Wordling conformance is claimed.
