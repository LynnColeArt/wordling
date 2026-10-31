# WP50 native merge reader — independent implementer handoff

Audience: the independent WP50 reviewer and a later, separately approved pure
merge consumer. This component is a reader/semantic inspection, not a merge
interpreter, native serializer, editor document, filesystem resolver or UI command.
Production imports only standard packages and the actual approved internal/wp51
reader (e7de080452c2906e99c8ace0048c415d842f2f89, native.go SHAe13c9368…);
New46/editor47/layout49/WPM are not dependencies or semantic authority.

## Native authority and public API

`Parse(raw, limits)` borrows input during that call; the caller must not mutate it
concurrently. Identity/prefix/index/body outer validation and native typed errors
come from actual wp51.Parse, unchanged. After acceptance only privately owned
immutable wp51 backing is retained. The subsequent bounded pass indexes already
checked outer spans; it is not a competing validator or recursive payload parser.
Export is always a fresh exact full native image, including prefix/gaps/opaque
payloads/tails. No JSON, normalized listing or replacement format is input to the
production package. JSON under evidence is provenance/inspection tooling only.

`Image.View(Primary|Secondary|Result)` requests an explicit semantic context over
that roleless framing image. Role is not inferred from extension/path/hash/native
length. Views privately capture source and role. Result views NEVER admit a Program,
even if their ordinary text could also be inspected under a separate Primary
request. There is no Result-to-program promotion API or inspection-field authority.
A separately requested context is not evidence that a merged result is a program;
actual acquisition/resolver context belongs to the future consumer contract.

`View.Admit()` returns a private, by-value `Program` handle only after this bounded
role/syntax predicate succeeds. It confers no writer, host action or implemented
execution. Result, unknown and unresolved views remain exportable and reject it.
Image/View wrappers are replaceable Go values; captured copies and Program handles
retain their own private source/role independently of later wrapper substitution.
Program must be passed by value to future consumers. A caller's assignment to its
own wrapper is not a cross-source rebind of previously captured authority.

Span has private source/bounds, and exposes only a copied absolute offset/length.
Bytes rejects zero/wrong-source spans; callers cannot fabricate ranges through
public numeric fields. Tokens/commands/operands/records/fields/findings/framing
inspections and nested slices are independent copies; their mutation cannot change
admission. Exact native character byte identities are retained; no Unicode/CP437
substitution occurs. Concurrent read-only calls are supported after Parse; concurrent
caller mutation during Parse or wrapper assignment while that wrapper is read is
not promised safe. No mutable wp51.Image wrapper escapes.

## Supported predicate and source table

These are separately reported levels: outer framing; classified payload; explicit
requested role; bounded program syntax admission. The production public witness
covers104 unchanged original scratch exports/35hashes/15contexts×2, with exact
immutable Git source/capture/runner/profile proof. It is not actual cmd/wordling
merge, executor compatibility or FR012/full-parent acceptance.28 Primary views are
currently syntax-admitted. All Secondary views remain blocked; all Result views
remain non-programs. No file/path/hash whitelist exists in production.

| Native owner / width | Implemented interpretation | Authority and status | Unsupported outcome |
|---|---|---|---|
| DE frame+1 /u8 | 22 BREAK;30 ELSE;31 END FIELD;33 END IF;34 END RECORD;36 FIELD;3B IF BLANK;45 NEST PRIMARY;46 NEST SECONDARY;4D PAGE OFF;4E PAGE ON | SDK51 WP86–87/PDF99–100; all11 exact original frames in sealed recon, observed | UnknownMergeCommand; whole frame retained |
| DE frame+2 /u16LE L | L4 gives8 total bytes; END RECORD L6 gives10, with payload2 | Same SDK plus original207/209; implemented/observed, no nine-byte minimum | CommandPayloadUnsupported; malformed outer trailer/length remains wp51 failure |
| END RECORD frame+4 /u16LE | Raw stored count retained, source-bound Payload | Original207 SECOND count2/one explicit value;209 count3/two values, including genuine empty field2. SDK calls this field count, but relationship to saved editing representation remains unresolved | RecordCountUnresolved ALWAYS for Secondary; UnobservedRecordCount outside2/3. No decrement/count-as-END-FIELD or implicit value rule |
| Immediately AFTER FIELD/IF BLANK frame, before external tilde /ASCII byte spans | FIELD1, IF BLANK2 only; raw digit identity and numeric value, separate tilde owner; following literal/command never consumed on failed syntax | SDK WP86/PDF99 and original207/209; documentary+observed bounded contexts | OperandSyntax, UnobservedOperand, OperandDelimiterMissing, OperandLimit |
| Immediately AFTER NEST frame through external tilde | Exact unquoted native DOS-name lexical bytes; observed C:\OUT\CHILD. Lexical alphabet retained, no host/filename/expression coercion or complete DOS filesystem validator | SDK WP87/PDF100, original223–225/233–236; documentary+observed operand location, resolution NOT implemented | ALL NEST requests block NestedResolutionRequired, including observed name; quotes/non-ASCII/escape contexts refuse, no nested execution permission |
| IF BLANK/ELSE/END IF frame owners | Checked bounded nesting, matched command indices; at most one ELSE | Original209/217 and documentary control structure | UnmatchedIf/Else/EndIf; DepthLimit; unsupported code blocks even in dead branch |
| Secondary data start through explicit END FIELD frame start | Exact field Content, END FIELD owner and per-record1-based ordinal; genuinely empty, ASCII-spaces-only and complex native content remain distinct | Original207/209 captures/native/archived advanced.py secondary recipe; FIELD2 Bob is a zero-byte content span, not missing/whitespace | No field is dropped; no absent↔empty↔space equivalence |
| Exactly one0A immediately after END FIELD /u8 | Separately owned Field.Separator, documented editing convention only | REF51 printed421–422/PDF438–439; advanced04 secondary recipe uses F9; bytes prove singleHR | FieldSeparatorUnobserved if absent; no global stripping, embedded field HR remains native data |
| Secondary raw record start→END RECORD end; Tail→END RECORD start | Exact source extents, raw count and explicit fields. Empty Tail retained as zero-width span, never invented as another field | Same original sources; count interpretation remains unresolved | UnterminatedField/RecordTerminatorMissing; incomplete raw source remains exactly exportable |
| Post-END RECORD D4 whole function, then0C /separate outer spans | Record.Interstitial owns every raw span. REF describes record hardpage convention; D4 geometry/metadata semantics remain unresolved | Original207/209 and all104 machine witness; documentary context separated from observation | FormatterUnresolved; no D4 stripping/rendering, arbitrary0C never generalized to record delimiter |
| Other functions/controls/native characters | Whole token/payload retained atomically, no recursion into payload-contained DE/tilde/0A/0C | Approved native reader outer validity only | UnknownNativeFunction, FormatterUnresolved, NativeCharacterContextUnresolved, LiteralTildeUnsupported |

Plain ASCII literals and the observed Primary0A/0C identities may accompany the
qualified commands; they are not Unicode text or a layout/rendering promise.
Secondary END FIELD/END RECORD in Primary is WrongCommandRole. Unobserved secondary
conditional/FIELD/NEST PRIMARY contexts block separately. Dynamic nested resolution,
all remaining merge functions, expression/string coercion and native output are
future duties. A recognized command frame alone never grants program support.

Counterexamples are public in evidence/public-inspections.json with exact image
path/hash, record/field ordinal, source spans/raw content and blockers. In particular,
advanced04/CMD51-207 SECOND rawcount2 is not one marker counted as2;209 Bob's field2
is genuinely empty while rawcount3 remains unexplained. These do not authorize an
implicit-field/decrement algorithm. Original assets and manual/private program/
SET/PRS/font bytes are untouched; only lawful project-authored scratch references,
public captures and hashes are used. Private manual hashes/printed+PDF locators
are recorded, not copied proprietary prose or resources.

## Positive Linux safeguards and measurements

Limits must all be positive and no greater than explicit maxima: input1MiB;
outer tokens65536; records4096; fields16384; operand lookahead256 bytes INCLUDING
the terminator; findings1024 (default128); IF nesting64. These are implementation
safety policies, not original DOS format limits or a scope cut. Input limit precedes
native ownership copy; every token/record/field/stack append checks its actual bound.
Operand lookahead stops before consuming a failed operand. Findings cap replaces
one slot with FindingsCapped, preserves blocking status and all raw bytes, and never
hides unknowns as success. Semantic limit failure returns no partial View while the
accepted framing Image remains exportable. No per-declared-length allocation or
opaque recursive payload traversal occurs.

At the exact1MiB accepted boundary,15 maximal opaque frames plus ASCII produce
65440 indexed tokens. The measured source-span coverage accounting is2,097,020bytes,
not an instruction count or CPU guarantee; it conservatively accounts revisited
owned extents. Public resource check measured16,373,216allocatedbytes and about
8.95ms on this host; log/tool/host identities are retained, no throughput SLO.
The test enforces32MiB allocation ceiling for that measured path and coverage<=3×
input; caller exports/inspection copies are separate bounded allocations per call.
Native outer reader has its own unchanged bounds and prefix traversal algorithm.

## Verification and evidence phases

- evidence/originals.json pins104 raw images,35 hashes, expected original token
  spans, explicit role/context and immutable snapshot57758765. Provenance is NOT
  production input format. audit_sources.py verifies992 immutable Git/working
  source/capture/runner/profile files plus the five approved dependency blobs.
- `go run ./internal/merge/native/evidence/inspect . internal/merge/native/evidence/originals.json`
  exercises the REAL public API and emits tokens/commands/operands/records/fields/
  interstitials/blockers for all104. It uses no duplicate native decoder.
- Public Go tests cover all104, exact export/spans, ownership/caller/inspection/
  whole-wrapper/cross-source/nil/zero/role behavior, malformed framing, unknown
  semantic payloads, missing/ambiguous/external operands, genuine empty/space fields,
  IF structure, each limit boundary, cap safety, concurrent reads and memory/work.
- Compiled Go overlays mutate PRODUCTION source (not expectations). Eight required
  mutants are killed: lossy unknown export, source span retarget, operand terminator
  retarget, count-as-visible-END-FIELD, dropped empty field, swallowed following
  native command, Result admission and skipped real token limit. A surviving first
  swallow mutant exposed a weak assertion; its log remains. Separate public contract
  tests now check the following frame AND exact operand Data/tilde/literal ownership.
- Actual discovery/build/full uncached tests/vet/race/configured7 checks pass,
 0 skipped. Discovery includes the real new contract/witness packages and existing
 storage/wp51; no falsely skipped Go module or active consumer code is involved.
- The original60s fuzz attempt was externally interrupted after45s/4,132,425exec;
 it is NOT reported as complete and600s had not started. Distinct resumed logs
 run sequential60s then600s with2workers; actual completion/count/RSS are in receipts.
 Timed source4 closure (three production files+native_test target) remains byte-exact.
 The separate contracts/witness packages added later are NOT claimed as compiled
 into that fuzz binary; they do not change its production dependencies or target.
 Go property fuzz checks actual Parse/View/Export/spans/admission with4096B/2048token
 per-input caps; exact1MiB and other maxima are deterministic resource tests.

Initial failed logs preserve a Go composite-literal harness typo, a missing JSON
Git-blob tag and an incorrectly constructed synthetic D4 frame; they were corrected
without changing raw sources or relaxing the production predicate. No VM or original
execution occurred. Native reader permission does not establish writer permission.

Root must independently review this implementation; the owner cannot self-approve.
Future pure executor, source acquisition/nested resolution, merged-native serializer,
editor/storage/TUI integration and actual executable/original comparisons remain
separately reviewed work. All38/91/36/nested leaves/SC001–005 and WB23/24/25/28 stay
required/open. No cmd/wordling merge/FR012/parent/M1 acceptance, scope cut or M2/PDF.
