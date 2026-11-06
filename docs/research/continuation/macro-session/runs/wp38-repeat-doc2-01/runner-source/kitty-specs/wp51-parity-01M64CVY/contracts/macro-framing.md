# WP32 original WPM framing, token and consumer contract

Research handoff for T094–T096, FR-002/003/012, NFR-001/003/004 and C-002/004.
This is a planning artifact. It introduces no codec, interpreter, original run,
storage permission or product compatibility claim. The companion
`macro-fixtures.json` is a hash-bound evidence ledger, not a replacement macro
format or a resource required by saved files. Full38 obligations,91 inventory
groups, discovered nested leaves and complete plain WP5.1 DOS parity remain M1.
PDF begins in M2 only after accepted M1. FC-001–010 remain binding.

## Evidence identity and applicability

Selected original: plain U.S. English DOS WP5.1, Help03/09/92, executable SHA256
`0734d0734c78c113ddaf40293c2c21b02e2cacc063bca5aa3d02f696de0bdc6a`.
The original observations use QEMU/FreeDOS1.4 and July1992 text-only Standard
Printer; they do not establish historical DOS, graphics/fonts, non-US resources
or physical-key delivery. Existing project-authored scratch macro sources and
native results are redistributable project evidence; proprietary programs,
manuals, dictionaries and other bundled resources are not copied or relicensed.
No application code was decompiled.

SDK51 is the12/93 toolkit, with intermediate WP section revision marks; REF51 is
the6/92 reference. Neither publication alone proves a feature existed in March.
One-based PDF pages are SDK printed WP page+13, REF Arabic page+17. Every word
admitted for the initial evaluator below is also present in the selected plain
original sources. Other documented keys/opcodes remain documentary only until
separately qualified; no general 5.1+/Windows/UNIX applicability is inferred.

| Fact | Exact primary locator | Local OCR location |
| --- | --- | --- |
| WPM prefix, tuple, terminal bytes | SDK WP92/PDF105 | toolkit.txt4909–4951 |
| Four indexes, description extent, word representation | SDK WP93/PDF106 | toolkit.txt4952–5002 |
| Legacy control-word identities | SDK WP94/PDF107 | toolkit.txt5003–5050 |
| Forward Search key word | SDK WP95/PDF108 | toolkit.txt5051–5103 |
| Other key identities | SDK WP96/PDF109 | toolkit.txt5104–5135 |
| Macro instruction identities and operand shapes | SDK WP97–98/PDF110–111 | toolkit.txt5136–5233 |
| Worked byte example and nonprinting low controls | SDK WP99/PDF112 | toolkit.txt5234–5255 |
| Record/run/editor obligations | REF373–393/PDF390–410 | reference.txt Macros sections |
| Repeat and original Cancel(F1) | REF379/PDF396 | reference.txt28256–28279 |
| Loop/control/error semantics | REF800–801,820–822,836–845,876 / PDF817–818,837–839,853–862,893 | WP09 exact case locators retained in ledger |

PDF hashes: SDK `5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754`;
REF `ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531`.
OCR hashes: toolkit `8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f`;
reference `f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c`.
The ledger pins these, WP01/09/10 inputs, all10 sealed run manifests and1014 raw
evidence/archived-runner/environment files. Its Git blob IDs bind tracked bytes;
null Git IDs identify ignored private manuals/OCR, whose content hashes remain
checked. Existing raw files and historical catalogues are immutable inputs.

WP09 has35 observations: **20 macro and15 merge**. The macro subset supplies40
canonical/repetition results and46 native WPM exports,22 distinct hashes. These
are original-only observations; Wordling was not tested. Every macro export has
tuple1/1/1/1, a four-entry40-byte index, description starting56, even relative
body length, and terminal0000 at EOF. Four body offsets are70;42 are75.
FLOW.WPM is169 bytes with body offset75: absolute even alignment is invalid.
The ledger records exact word arrays/command byte offsets, source recipes,
capture hashes, canonical IDs/contexts and expected native results. These prove
the bounded facts below, not the whole language or a general producer family.

## Prefix and image boundary

All multi-byte fields below are unsigned little-endian: short16,long32. Read the
complete field before interpreting it. Use checked subtraction (`length <= end -
offset` after checking `offset <= end`) rather than unchecked pointer addition.
The immutable owned image remains authoritative; Export copies it, never rebuilds
indexes/descriptions, normalizes text or changes version/offset bytes.

| Absolute byte offset | Width | Meaning; initial reader policy |
| --- | --- | --- |
| 0 | 4 | Signature FF575043; otherwise UnsupportedFormat. |
| 4 | 4 | Absolute macro body offset B, not an index-relative pointer. Require56 <= B <= N for this index-bearing slice. |
| 8 | 1 | Product1; other products UnsupportedProduct. This alone does not identify release/platform. |
| 9 | 1 | Macro file type1; document type10 is UnsupportedFileType here. Filename extension is not authority. |
| 10,11 | 1 each | Stored major1/minor1. Other versions UnsupportedVersion; WP5.0 0/0 remains M1 work. |
| 12 | 2 | Key0 in selected WPM; nonzero UnsupportedEncryption, without guessing decryptability. |
| 14 | 2 | Reserved0; other values UnsupportedVariant, not necessarily corrupt. |
| 16 | 2 | Special index type FFFB; incomplete width TruncatedInput, wrong type MalformedPrefix. |
| 18 | 2 | Index count4, including header. Zero/inconsistent structure malformed; other internally consistent counts UnsupportedVariant. |
| 20 | 2 | Index block length40. For any read count, require checked count*10 agreement and complete block before deciding variant support. |
| 22 | 4 | Next block0 for documented WPM single-block layout. Nonzero is UnsupportedVariant after pointer bounds checks; never follow a speculative chain. |
| 26 | 2 | First ordinary index type1, the macro description. Other types UnsupportedVariant. |
| 28 | 4 | Description byte length L. |
| 32 | 4 | Absolute description byte position P. |
| 36–55 | 20 | Two remaining ten-byte index slots; observed allzero. Preserve them exactly. |

The three ordinary slots each have a16-bit type,32-bit length and32-bit absolute
position. For an unexpected nonzero slot, validate any declared nonempty extent
against `[56,B)` without following new structures; retain a disjoint bounded extent
as an opaque prefix finding and deny execution. Any overlap/alias with description,
index or another declared nonempty extent returns UnsupportedStructure, never a
fabricated original format prohibition. Allzero unused slots have no pointed
extent; do not require their zero position to be a valid packet pointer.

For the admitted description require `56 <= P <= B`, `L <= B-P`, L within the
description budget, and L>=1 with its last byte zero. A missing/out-of-bounds
extent is MalformedPrefix; malformed termination is reported with the exact
field/span. A description that does not end at B, contains an earlier zero, or
uses a different bounded placement may be retained with an execution-blocking
UnsupportedVariant finding. Never require P=56 or B=70/75 for all future files:
those are observed fixture values, not universal format constants.

SDK describes a one-byte empty description for an original WP-created macro
and zero length for certain editor-created files. This corpus has lengths14/19,
not those empty variants. Zero-length/editor-created description is explicitly
UnsupportedVariant for this first slice, not declared globally malformed. Preserve
any admitted gap bytes and opaque content; do not claim a description Unicode
encoding from the two ASCII descriptions. Description text is a byte span, **not
the two-byte macro stream**. No editable description writer is specified here.

Keep image admission distinct from execution admission. Bounded opaque prefix,
command and suffix findings can coexist with an accepted lossless Image; runtime
Compile must refuse the unqualified structure before effects. Cases refused at
Parse return a typed error and no usable Image; caller retains its untouched
input/source. Neither case grants mutation or discarding permission.

Release provenance is a third independent axis: tuple1/1/1/1 does not distinguish
all producers, platforms or dates. Inspection reports `unknown-from-bytes` for
release evidence; an external source/hash/run binding can identify the22 observed
fixtures as selected-original evidence. An otherwise admitted user's WPM remains
release-unqualified, not malformed and not certified March1992 by its tuple. A
known unsupported tuple returns UnsupportedVersion; a known tuple with opaque
words is an admitted image with blocked execution; malformed bounds are a parsing
failure. Preserve these outcomes separately in downstream evidence and UI.

## Macro word stream and typed identity

Read two-byte units relative to B, at B+2*i; B itself may be odd. `Word.Value` is
the16-bit original identity; byte storage is low byte then high byte. Each Word
retains its absolute two-byte span. Classification adds meaning without replacing
the raw value:

| Identity | Interpretation/support |
| --- | --- |
| 0041/0042/0043, bytes4100/4200/4300 | Observed literal ABC characters. ASCII20–7E with high byte0 is an admitted literal class; Unicode display is not stored identity. |
| High byte0–12, other set/number pairs | SDK character identities; preserve set/number. Non-ASCII execution/rendering needs separate original character/resource proof. |
| 0000, bytes0000 | One terminal word, consisting of two null bytes; not two terminal words. |
| 007E | Literal stored tilde functioning as an argument/list terminator in the grammatical context below. It is not always document output. |
| FC3A | SDK hard-tilde instruction, documentary only here; preserve, refuse execution until qualified. Do not replace it with007E. |
| 8021, bytes2180 | Observed Forward Search original key; external command sink owns its actual modal command behavior. |
| FCxx | Macro instruction namespace. Known identity is separate from supported operands/context; unknown low byte stays opaque. |
| 80xx/FExx/FFxx key classes | SDK control/Alt/function representations; preserve identity, execute only specifically admitted original keys. No terminal key-code substitution. |
| Low nonprinting words0002/0009/000A/000D etc. | Documentary editor/control possibilities, not ordinary ASCII text in this slice. Preserve and refuse unqualified execution. |

Stop word decoding at the first0000 on a relative word boundary. The observed
profile ends there. Remaining bytes, even an odd number, are an opaque suffix
retained verbatim with execution denied; their meaning is unproved. Without a
terminal word, an unpaired final byte is MalformedBody/OddWord, otherwise
MalformedBody/MissingTerminator. An opaque suffix is not a second program.
Never reject valid FLOW169/body75 by testing `N%2` or `B%2`. Never use DOC body
iterators, C0 document character framing or merge DE payload grammar on WPM.

### Opcode and operand admission matrix

These21 command/key identities occur in selected original WPM bytes. The ledger
contains every file offset and little-endian encoding; SDK locators and fixture
cases below independently bind identity and context. “Admitted” means a proposed
bounded downstream implementation contract, not implemented/verified Wordling.

| Word | Name / operand structure | Observed canonical cases; bounded consequence |
| --- | --- | --- |
| FC0C | DISPLAY OFF; no operand | All20 macro observations. Emit typed display-control effect; actual rendering/UI semantics remain integration work. |
| FC01 | ASSIGN name~expr~ | 215,222,227. Numeric initialization/update only. |
| FC03 | BREAK; no operand | 220,221,229,230. Exit the tested enclosing loop; root/child file-level BREAK ignored in those macro contexts. |
| FC0E/FC10 | ELSE / END IF; no operands | 205,219–221,228. Structured IF boundaries. |
| FC0F | END FOR; no operand | 214,218–222,226–228. Closes FOR or FOR EACH. |
| FC11 | END WHILE; no operand | 215,222. |
| FC12 | FOR name~start~stop~step~ | 214,219–222,228. Inclusive endpoints; tested positive/negative steps. |
| FC13 | FOR EACH name~item~...~~ | 218,226,227. Order/duplicates/literal quotes and bounded numeric expressions preserved. |
| FC14/FC16 | GO label~ / LABEL label~ | 205,206,210,212,213. Jump and handler action targets. |
| FC15 | IF expr~ | 205,219–221,228. Tested zero/nonzero/comparison branches. |
| FC18 | NEST filename~ | 210,212,213,230. Native name words passed to resolver; source path is not arbitrary host IO authority. |
| FC19 | NEXT; no operand | 219,228. Current loop iteration only in tested FOR/nested FOR. |
| FC1C/FC1D | ON ERROR / ON NOT FOUND action~ | 210,212,213 /206. Observed action is nested GO label~ followed by another~. |
| FC20 | QUIT; no operand | 206,210,212,213 sources. Taken/unreached paths must stay distinguished; no broad QUIT interaction claim. |
| FC22 | RETURN; no operand | 212 child. Local child return resumes parent. |
| FC2B | WHILE expr~ | 215,222. Zero-entry and variable update/termination only. |
| FC34 | VARIABLE name~ | 214,215,218–222,226–228. Embedded expression reference or emitted value according to context. |
| 8021 | Forward Search key | 178,206. Default termination versus ON NOT FOUND output; production search support is not currently present. |

Source occurrence alone does not prove every instruction path executed. Examples:
QUIT in a skipped sentinel path proves stored identity, not its stop-all interaction;
RETURN ERROR default behavior is inferred from the observed unhandled child
outcome213, whereas an explicit FC24 instruction is absent from this corpus.
FC24/other handlers/CHAIN/CALL/CANCEL ON/OFF and the remaining SDK table entries
are documentary-only here. Do not activate them from a table name or Plus feature.

### Exact operand boundary rules

The raw reader exposes all Words; a separate runtime compiler consumes supported
operand structures. Preserve delimiter/source spans even when they are not emitted.
No expression/identifier is rewritten back into a WPM source file.

1. A `name~`, `label~` or `filename~` is a nonempty sequence of admitted literal
   words ending at007E. The observed variable names are N/I/J/V/B, labels uppercase
   ASCII and filenames original `C:\OUT\...`. Names retain exact words/case;
   case folding and general DOS path lookup are unproved. The host resolver maps
   only a separately declared rooted profile; it never opens that literal DOS path
   directly. Empty/embedded-command/unsupported character forms refuse execution.
2. `expr~` scans at the current grammar depth. FC34 recursively consumes its own
   `name~` and contributes a variable-reference node, **not** an expression end.
   A007E encountered back at outer depth closes the expression. The admitted
   expression subset is signed decimal integer, VARIABLE reference, or one binary
   `+`, `<` or `=` combination of those atoms. No parentheses, chained precedence,
   arbitrary coercion, division or undefined-variable default is inferred.
3. FC12 consumes four terminated operands, with expressions for start/stop/step.
   FC13 consumes name, then one or more item expressions/literal values; an empty
   next item terminates the list. This empty delimiter is not a proven empty-valued
   first/middle/last item. Nested VARIABLE terminators do not end the outer list.
4. The observed list strings are raw `red`, `blue sky` and quoted equivalents;
   the quote words remain literal value content. Do not apply quote stripping,
   string escaping or general expression-to-string coercion. Ambiguous/unobserved
   forms get UnsupportedExpression, not a guessed string/number conversion.
5. ON ERROR/ON NOT FOUND in this admitted subset consumes FC14, its label~, then
   the handler-action~. The two closing tildes have different grammar ownership.
   Other documented actions are retained opaque/refused, not silently ignored.
6. Structured IF/FOR/FOR EACH/WHILE boundaries are matched before execution; labels
   must resolve unambiguously within the compiled file. Unmatched structures,
   duplicate/unresolved labels or unsupported operand forms produce typed compiler
   refusals, not invented original error text. Unknown instruction width/arity is
   never guessed to continue execution; the complete source remains exportable.
7. A key Word such as8021 is a key event, not an operand-taking macro instruction.
   Subsequent literal events are delivered in order; a real editor search command
   would own its modal input. A component test sink may simulate NotFound, but
   cannot thereby prove an integrated search or inject that result as host failure.

For WHILELP.WPM, the second WHILE operand is the literal word sequence
`FC34 004E 007E 003C 0033 007E`: VARIABLE N~ consumes the first tilde, then `<3~`
closes the WHILE expression. For EXPRLIST, `FC34 0042 007E 002B 0034 007E` is one
list item (B+4), not separate B and +4 entries. ONERROR has `FC1C FC14 ERR 007E
007E`. Ledger word arrays and spans make these independently checkable without
trusting a pretty-printed recipe. Actual parser acceptance/rejection/fuzz behavior
is a WP33/35 deliverable, not a result of this research artifact.

## Execution contexts and externally visible effects

The only permitted macro semantics are the bounded WP09 macro case observations,
whose exact native expected outputs and final continuation markers are in the
ledger. Respect positive/negative inclusive FOR; false-entry WHILE; FOR EACH order,
duplicates and retained quote words; NEXT/BREAK on the current tested loop; ignored
top-level/child file BREAK229/230. Do not import merge primary/secondary BREAK,
record iteration, global PAGE or partial-copy policy. The15 merge rows are listed
separately and cannot count as macro passes.

Macro child handlers start with default handling in observed212/213; the parent's
handler resumes after child return, and unhandled child error reaches that parent.
Do not use a shared dynamically inherited handler context. This does not resolve
general variable scope, arbitrary call actions, recursion, three-level handlers or
errors inside handlers. A host filename/refusal/resource-limit failure is not
automatically an original ON ERROR condition. The original command adapter must
justify each original condition; unsupported host features fail explicitly.

Compile preflights all statically discoverable unsupported instructions/structures
in the primary file before any command effect. Initially reject unsupported words
even in statically unreachable branches; that conservative admission rule is a Linux
support boundary, not a statement that original WP inspects dead branches. Nested
programs are independently compiled before child effects; parent effects already
applied remain recorded. Do not promise all-or-nothing rollback. Step exhaustion,
host cancellation, unsafe target/source, unsupported command and unqualified
expression are separately reported. Partial native document effects are owned by
the ordinary editor reducer and its normal writer, never a macro byte serializer.

## Proposed downstream API contract (not installed APIs)

These Go declarations are the concrete WP33–37 handoff, **not existing functions**.
Implementations may amend signatures through an independently reviewed contract
change when actual WP27/38 source requires it; never hide drift behind a helper.
Package alias `mac` below means internal/macro/runtime. The machine uses only wpm
and standard-library dependencies. Neither codec nor VM imports storage, document,
editor or TUI. Storage imports only the codec; editor/TUI compose both later.

### WP33: internal/macro/wpm

```go
type Span struct { Offset, Length uint32 } // absolute half-open byte extent
type Kind string // "literal", "character", "key", "macro", "control", "terminal", "opaque"
type Word struct { Value uint16; Span Span; Kind Kind }
type Limits struct { InputBytes, DescriptionBytes, Words uint32 }
type Finding struct { Code string; Span Span; ExecutionBlocked bool }
type Header struct { BodyOffset uint32; Product, FileType, Major, Minor byte }
type Inspection struct {
    Header Header
    Description, Body, Terminal, Suffix Span
    Findings []Finding
    ReleaseEvidence string // "unknown-from-bytes"; external provenance is separate
}
type Failure struct { Code string; Offset uint32; Field, Detail string }
func (e *Failure) Error() string
type Image struct { /* private owned bytes and checked spans */ }
func DefaultLimits() Limits
func Parse(input []byte, limits Limits) (*Image, error)
func (i *Image) Export() []byte
func (i *Image) Inspect() Inspection
func (i *Image) Description() []byte // copied raw extent, including terminal byte
func (i *Image) BodyWords() []Word   // copies, includes terminal; excludes opaque suffix
func (i *Image) SHA256() [32]byte    // exact complete image
```

Export, Description, BodyWords and Inspect slices are fresh independent copies.
Kind never destroys Value; a known namespace with unknown instruction remains
execution-blocked. Body span includes its terminal word; Suffix starts immediately
after it. Parse rejects nil/short/oversized/inconsistent fields with typed Failure.
Limits must be positive and no larger than the declared maxima; invalid settings
get InvalidLimit, never zero-as-unbounded. Error codes distinguish unsupported
format/product/type/version/encryption/variant/structure, truncated/malformed
prefix/body and input/traversal limits. Errors are Wordling diagnostics, not
purported original messages. No Marshal/Write/Edit function is authorized.

### WP34: additions to existing internal/storage

```go
type Macro struct { /* private *wpm.Image, *Directory, name, Identity */ }
func (d *Directory) ReadMacro(name string) (*Macro, error)
func (m *Macro) Image() *wpm.Image // immutable codec object
func (m *Macro) Export() []byte
func (m *Macro) Identity() Identity
func (m *Macro) Name() string
func (m *Macro) DirectoryID() FileID
```

These methods are absent today. The real approved lane-b source exposes
`OpenDirectory`, `Directory.Read`, private `readStable`, `Document.Identity/Export`,
`Observe/Save` and WP24 `PreparePublication/Publish`. Read calls wp51.Parse, which
intentionally rejects WPM. PreparePublication is bound to *Document/*wp51.Image,
and also calls wp51.Parse. Leave both DOC contracts intact. ReadMacro reuses
validName/readStable: pinned rooted directory, flat names, no-follow regular-file
open, bounded read and before/after/path metadata+hash observation. It delegates
only WPM validation to the new codec and captures the same identity semantics.
Do not duplicate Linux open/read transactions, expose readStable, accept arbitrary
paths, invent a generic native-file wrapper or add Macro Save/Publish here.
An Image/source hash is not a lock/future freshness guarantee or UI revision.

### WP35: internal/macro/runtime

```go
// Imports: context; internal/macro/wpm. All document/session/IO policy is injected.
type Limits struct {
    Steps, OutputWords uint64
    CallDepth, LoopDepth, Variables, VariableWords, ExpressionDepth, SliceSteps uint32
}
type Policy struct { Keys []uint16; ASCII, DisplayControl bool }
type Program struct { /* private immutable compiled statements and source */ }
type Effect struct {
    Kind string // "literal", "key", "display-off"
    Words []wpm.Word
    Source [32]byte
    At wpm.Span
}
type Condition string // "none", "not-found", "command-error", "user-cancelled"
type EffectResult struct { Condition Condition; MayHaveEffects bool }
type CommandSink interface {
    Capabilities() Policy
    Apply(context.Context, Effect) (EffectResult, error)
}
type ProgramRequest struct { ID uint64; Parent [32]byte; Name []wpm.Word; At wpm.Span }
type Resolution struct {
    State string // "ready", "pending", "condition", "host-error"
    Image *wpm.Image
    Condition Condition
    Err error
}
type Resolver interface { Resolve(context.Context, ProgramRequest) Resolution }
type Failure struct { Code string; Source [32]byte; At wpm.Span; Detail string }
func (e *Failure) Error() string
type Result struct {
    State string // "ready", "running", "waiting", "complete", "stopped", "refused", "failed", "limited"
    Steps, EmittedWords uint64
    NeedProgram *ProgramRequest
    Err error
}
type Machine struct { /* private per-run state; not a document */ }
func DefaultLimits() Limits
func Compile(image *wpm.Image, policy Policy, limits Limits) (*Program, error)
func New(program *Program, sink CommandSink, resolver Resolver, limits Limits) (*Machine, error)
func (m *Machine) Step(ctx context.Context, quota uint32) Result
func (m *Machine) Resume(requestID uint64, resolution Resolution) error
func (m *Machine) Stop(reason string) Result // explicit host safety operation
func (m *Machine) State() Result
```

Compile owns/copies policy and limits; Program retains immutable source identities
and spans. New checks sink capabilities cover compiled effects. It cannot broaden
policy automatically. Variables, frames and byte/word values are runtime state;
there is no parallel editable document. The slice/word fields in returned results,
requests and effects must not expose mutable source/machine state. Reusing the same
Program in two Machines does not share variables/handlers. Initial supported
variable lookup is current-frame behavior only where original fixtures establish
it; cross-file variable-scope forms remain unsupported.

Each accepted Step delivers each effect exactly once to Apply, charges actual
statement/word work to limits, then advances the PC. Effects contain native Word
identities; dynamically expanded ASCII numbers/strings use original word values
with zero source length where no literal source word exists, while At names the
VARIABLE expression. Apply's nonnil error is a host/unsupported failure and ends
the run without synthesizing an original condition. A Condition with nil error
is an explicitly supplied command condition; only the tested handlers/context may
consume it. Record MayHaveEffects and already-applied session changes; never infer
rollback. UnsupportedCommand is a host refusal, not an original command-error.

Resolver may return ready from an immutable cache or pending. For pending, Step
returns waiting with a copied request; further Step calls produce no effects or
new resolver invocation until Resume of the exact request ID. The host performs
WP34 acquisition outside the VM and passes ready/condition/host-error on Resume.
Wrong/duplicate/late IDs get StaleResume; stopped runs cannot be resumed. Nested
names are exact native words, not strings giving the VM filesystem authority.
Resume ready input undergoes the same compile/limit preflight before child entry.
The editor adapter binds source/target/revision/run identities outside this API.

Step quota is1..SliceSteps; invalid quota is a typed refusal. A slice ending with
more work returns running, not complete. Total steps/output/depth limits are shared
across nested files/repetitions under the host's run budget. Context cancellation
and Stop are host safety outcomes, **not** proven original Cancel(F1)/ON CANCEL
semantics. Current callback latency/IO cannot be bounded by instruction count;
TUI workers and later pending identities must handle it explicitly.

### WP36/37: actual session/TUI consumer, proposed additions only

Approved lane-h currently has persistent `editor.Session`, `Reduce(Event)
(Session,*Intent,error)`, `Intent`/`Result` operation+revision identities, a single
source/document/cursor, and read-only command paths. `tui.Runtime.command` executes
Read/Observe/WriteSnapshot using actual storage; Model.Update returns
(tea.Model,tea.Cmd). These inspected APIs are pinned by Git blob/hash in the
ledger. WP27/28 editable/dirty/candidate APIs are pending, not present source at
this checkpoint. There is no installed macro API or safe text-insertion/Doc2
adapter to claim merely by defining a sink.

Minimum proposed editor additions, expressed as complete signatures:

```go
// Existing Session/Intent/Result gain typed macro load/run fields, not a second reducer.
type ScreenID uint8 // original Doc1/Doc2 identities only after reviewed WP38 evidence
type MacroEffect struct {
    Run, ExpectedRevision, Sequence uint64
    Target ScreenID
    Effect mac.Effect
}
type MacroReceipt struct {
    Run, Revision, Sequence uint64
    Result mac.EffectResult
    Err error
}
func (s Session) BeginMacro(name string, repeat uint32, target ScreenID) (Session, *Intent, error)
func (s Session) ApplyMacroEffect(effect MacroEffect) (Session, MacroReceipt, error)
func (s Session) EndMacro(run uint64, result mac.Result) (Session, error)
```

BeginMacro creates an actual typed ReadMacro intent and immutable pending identity;
normal completion through Reduce validates operation/revision/run/target and binds
the loaded storage.Macro. A host-owned Machine is distinct from persistent Session:
never hide a mutable *Machine inside a copied Session value. The sink serializes
typed effects through ApplyMacroEffect and replaces the authoritative Session with
the returned persistent value. Subsequent effects carry its actual new revision.
Ordinary WP27 commands/document mutations own text, typeover/cursor/history/dirty
and native output; the adapter must never edit bytes or maintain another buffer.
Original source and target/run identity, pending/late messages, repeat limits and
stop/error effects must be reviewed against actual WP38 results before enabling.
Search, second screen or any missing ordinary command is refused explicitly until
implemented; synthetic sink NotFound is not production search proof.

WP37 extends the existing runtime command switch with ReadMacro and typed macro
resume/step messages; it continues the actual `Model.Update(tea.Msg)
(tea.Model,tea.Cmd)` and cmd/wordling executable. Proposed private adapter seams:

```go
func (r *Runtime) readMacro(request editor.Intent) tea.Cmd
func (m Model) advanceMacro(run uint64, quota uint32) (tea.Model, tea.Cmd)
```

Signatures do not authorize another runtime/session or unreviewed command aliases.
Original Alt-F10→Macro prompt, Repeat(Esc) and Doc2 selection have only the exact
WP09 recipes; REF379 names Cancel(F1), not a guessed Ctrl-Break macro alias. WP38
must capture stop/prompt/error/dirty/buffer boundaries before WP36/37 admit them.
Workers must reconcile completed rooted reads/late effects and host shutdown even
if UI cancellation detaches a request; no claim that disk IO rolled back. Native
output comparisons come from actual ordinary document writer/Save As, not traces.

### Concrete downstream acceptance calls

These sequences are **future acceptance clients**, not runnable against current
primary source. They deliberately make absent API dependencies visible.

```go
// WP33: raw bytes from a pinned original fixture; no alternate source format.
img, err := wpm.Parse(raw, wpm.DefaultLimits())
if err != nil { t.Fatal(err) }
if !bytes.Equal(raw, img.Export()) { t.Fatal("lossless image changed") }
words := img.BodyWords()
if words[0].Value != 0xFC0C || words[1].Value != 0x0041 { t.Fatal("wrong identity") }
words[1].Value = 0x005A
if img.BodyWords()[1].Value != 0x0041 { t.Fatal("caller alias") }

// WP34: same rooted operation and immutable identity as the real storage API.
dir, err := storage.OpenDirectory(tempRoot)
if err != nil { t.Fatal(err) }
defer dir.Close()
source, err := dir.ReadMacro("TESTMAC.WPM")
if err != nil { t.Fatal(err) }
if source.Identity().SHA256 != source.Image().SHA256() { t.Fatal("source binding") }
if _, err := dir.Read("TESTMAC.WPM"); err == nil { t.Fatal("DOC accepts macro") }

// WP35: traceSink is an observable test CommandSink; it owns no document/writer.
policy := traceSink.Capabilities() // ASCII + DISPLAY OFF; no unsupported keys
program, err := mac.Compile(source.Image(), policy, mac.DefaultLimits())
if err != nil { t.Fatal(err) }
machine, err := mac.New(program, traceSink, resolver, mac.DefaultLimits())
if err != nil { t.Fatal(err) }
for {
    result := machine.Step(ctx, 64)
    if result.State == "running" { continue }
    if result.State == "waiting" {
        req := result.NeedProgram
        // Host decodes only an admitted original-name/rooted-profile mapping.
        // Actual acquisition uses dir.ReadMacro; host failures are not invented WP errors.
        resolution := resolveThroughStorage(req)
        if err := machine.Resume(req.ID, resolution); err != nil { t.Fatal(err) }
        continue
    }
    if result.State != "complete" { t.Fatalf("%+v", result) }
    break
}
// Assert actual delivered original words ABC and DISPLAY OFF separately.
// A trace assertion proves component effects only, never native document output.

// WP36 sink.Apply uses the real ordinary-command adapter and current revision:
next, receipt, err := session.ApplyMacroEffect(editor.MacroEffect{
    Run: runID, ExpectedRevision: session.Snapshot().Revision,
    Sequence: nextSequence, Target: selectedScreen, Effect: effect,
})
if err != nil { /* return host refusal; do not fake original condition */ }
session = next
// WP37 then exercises this path through actual executable input/tea messages,
// retrieves/writes actual native output, and compares with WP09/WP38 artifacts.
```

`traceSink`, `resolver`, `resolveThroughStorage`, run/sequence/selectedScreen and
test context are supplied by the appropriate future client, not invented current
globals. Acceptance clients must implement the exact interfaces above and assert
their public error/effect behavior. In particular, resolver host path adaptation
and a trace collector cannot stand in for production filesystem/session integration.

## Safeguard budgets and finite negative corpus

These are proposed Linux support limits, not original DOS format/language limits
or measured performance claims. WP33/35 must measure actual fuzz/allocations/latency
before their acceptance; if a limit changes, update contract/evidence together.

| Boundary | Initial explicit budget |
| --- | --- |
| Whole WPM input |16MiB, matching actual WP02/storage acquisition maximum. |
| Prefix indexes | One complete40-byte/four-entry macro index; no linked traversal. |
| Description |4096 bytes; all observed14/19 fit. |
| Body word count |1,048,576 including terminal; bound allocation/traversal independently of input bytes. |
| Compiler expression nesting |16 maximum, but only proven VARIABLE/name nesting grammar admitted. |
| Call/loop depth |16/32 respectively; declared safety cap, observed cases much shallower. |
| Variables / value length |256 names;4096 original words/value; aggregate values charged to output/memory checks. |
| Execution |1,000,000 charged steps/run;1,048,576 emitted words/run; maximum256 steps/slice. |
| Numeric safeguard | Checked signed64 arithmetic only for the proven single-operation subset; overflow/unsupported coercion refuses without claiming original numeric range. |
| Fuzz acceptance proposal | Original+negative seeds;60s smoke then600s parser fuzz on declared host, commands, Go version, corpus hashes and real results. |

Charge literal emission per word, compilation scans per word and all control
iterations even when they emit nothing. Resource counters cannot reset at a child
file boundary or Repeat invocation to evade the host's total run budget. Budget
exhaustion/cancel leaves source bytes unchanged and exposes already-applied effects.
No unmeasured allocation ceiling or physical-key-to-paint claim is made.

The finite downstream negative plan includes:

| Mutation/condition | Required behavior |
| --- | --- |
| Header truncation at every width; short index | TruncatedInput, no panic/OOB/no usable image. |
| B before56 or beyond EOF; overflowing P/L; description overlapping header | MalformedPrefix with exact field/span; no wraparound allocation. |
| Index count/size disagree or zero; wrong FFFB | MalformedPrefix. Consistent other count/chain/version/product remains distinctly unsupported. |
| Missing terminal; unpaired final body byte before terminal | MalformedBody/MissingTerminator or OddWord; relative alignment only. |
| Valid terminal plus uninterpreted suffix; nonzero unused slot | Preserve exact admitted image, execution-blocking finding, no guessed extra program. |
| Unknown FC opcode/unknown key/extended glyph/hard tilde | Preserve original words; Compile refuses before primary effects even in a dead branch. |
| Missing outer expression/action/list tilde; nested VARIABLE boundary | Exact typed compiler refusal; never swallow following instruction or strip quotes. |
| Unmatched END, duplicate/missing labels; invalid step/unknown expression | Refuse compilation/execution conservatively, no invented original diagnostic. |
| GO cycle, zero/invalid step, nested/input/output exhaustion | Finite host refusal/limit, source unchanged, actual partial effect receipt retained. |
| Sink host error versus explicit original NotFound | Distinct outcomes; host error cannot masquerade as ON ERROR/ON NOT FOUND input. |
| Nested missing input/unknown program; stale/duplicate Resume | Explicit resolution/unsupported/StaleResume, no duplicate/late effects. |
| Source/target changed, unsupported screen/search, pending stop | WP36/37 real identity gate; no wrong-buffer edit, false rollback or fabricated support. |

Current evidence proves loop endpoints/output branches, not zero-step historical
errors, general precedence, empty list values, arbitrary escaping, IF-only BREAK,
all loop families' NEXT/BREAK, deeper handlers, error-inside-handler, cross-file
variable scope, prompt timing or Stop semantics. Those stay research/integration
gaps. Stop/record/edit/macro conversion/native WPM writing+disk saving, CMD51-199
original macro-editor roundtrip, all merge/data commands, non-ASCII/non-US resources,
historical DOS/physical terminal qualification and the rest of every M1 obligation
remain explicit. WP33 Export equality and WP35 traces never close those parents.

## Reproducible read-only contract audit

The following inline audit checks existing evidence, not production codec behavior.
It writes no project file, invokes no VM and is not a new executable validator
deliverable. Run from repository root. All tracked source/raw Git blobs must match;
all proprietary cache files remain private. Temporary tests of tampered copies
must fail these checks rather than rewriting evidence to make it fit.

```sh
python3 - <<'PY_AUDIT'
from pathlib import Path
import hashlib,json,struct,collections
p=Path('kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json')
a=json.loads(p.read_text()); sha=lambda b:hashlib.sha256(b).hexdigest()
for item in a['sources']+a['runs']+a['sealed_raw_files']:
    b=Path(item['path']).read_bytes()
    assert len(b)==item['size'] and sha(b)==item['sha256'],item['path']
    if item['git_blob']:
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['git_blob']
assert a['counts']['macro_observations']==20 and len(a['macro_cases'])==20
assert len(a['excluded_from_macro_semantics'])==15 and len(a['runs'])==10
assert a['counts']['retained_requirements']==38 and a['counts']['retained_groups']==91
original=Path('kitty-specs/wp51-parity-01M64CVY/contracts/automation.md').read_text()
wp09=json.loads(original.split('<!-- WP09_AUDIT_BEGIN -->')[1].split('```json\n')[1].split('\n```')[0])
selected=[x for x in wp09['rows'] if x['context'].startswith('macro')]
fields=['case_id','title','feature_ids','context','observation','source_locators','run','repeat','runner','expected']
assert [{k:x[k] for k in fields} for x in a['macro_cases']]==[{k:x[k] for k in fields} for x in selected]
assert a['excluded_from_macro_semantics']==[{'case_id':x['case_id'],'context':x['context']} for x in wp09['rows'] if not x['context'].startswith('macro')]
byrun={x['run_id']:json.loads(Path(x['path']).read_text()) for x in a['runs']}
for item in a['wpm_exports']:
    b=Path(item['path']).read_bytes(); B=struct.unpack_from('<I',b,4)[0]
    assert len(b)==item['size'] and sha(b)==item['sha256'] and b[8:12]==bytes([1]*4)
    assert struct.unpack_from('<HHHI',b,16)==(0xFFFB,4,40,0)
    L,P=struct.unpack_from('<II',b,28)
    assert b[26:28]==b'\1\0' and b[36:56]==bytes(20)
    assert P==56 and P+L==B and b[B-1]==0 and (len(b)-B)%2==0
    W=struct.unpack('<'+'H'*((len(b)-B)//2),b[B:])
    assert [f'{x:04X}' for x in W]==item['body_words'] and W[-1]==0
    result=next(x for x in byrun[item['run']]['results'] if x['case_id']==item['case_id'])
    assert any(x['path']==item['path'] and x['sha256']==item['sha256'] for x in result['native_outputs'])
    for span in item['command_spans']:
        off=span['file_offset']; assert off==B+2*span['body_word_index']
        assert b[off:off+2].hex()==span['little_endian_hex']
        assert struct.unpack_from('<H',b,off)[0]==int(span['value'],16)
assert len(a['wpm_exports'])==46 and len({x['sha256'] for x in a['wpm_exports']})==22
assert collections.Counter(x['body_offset'] for x in a['wpm_exports'])=={70:4,75:42}
assert len(a['opcodes'])==21
for op in a['opcodes']:
    assert op['sdk_pdf_page']==op['sdk_printed_page']+13
    for occ in op['occurrences']:
        b=Path(occ['path']).read_bytes()
        assert struct.unpack_from('<H',b,occ['file_offset'])[0]==int(op['word'],16)
for row in a['macro_cases']:
    for rid in [row['run'],row['repeat']]:
        result=next(x for x in byrun[rid]['results'] if x['case_id']==row['case_id'])
        assert byrun[rid]['scope']=='original-reference-only' and not byrun[rid]['wordling_tested']
        output=next(x for x in result['native_outputs'] if Path(x['path']).name==row['expected']['filename'])
        b=Path(output['path']).read_bytes(); B=struct.unpack_from('<I',b,4)[0]
        assert row['expected']['kind']=='body'
        assert b[B:].hex()==row['expected']['expected_hex'] and b[B:]==row['expected']['expected_text'].encode('ascii')
print('WP32 read-only source/blob/manifest/header/word audit passed:',len(a['sealed_raw_files']),'raw files;46 WPM exports/22 hashes/20 macro cases')
PY_AUDIT
```

Author validation passed source/hash/Git-blob/manifest/word audits for1014 raw
files,46 WPM exports/22 hashes and40 exact native result repetitions. Eight
in-memory tamper negatives were rejected: raw hash, Git blob, merge context,
valid merge ID substitution, native word, command offset, expected output and
parent-coverage corruption. These check evidence integrity, not parser semantics. No Go packages changed; no Go, parser-fuzz, original-run,
macro disk-roundtrip or executable integration result is claimed here. Independent
review must validate the proposed interfaces/support boundaries against the same
raw sources and actual future consumers before downstream implementation approval.
