# WP35 bounded pure macro evaluator — component implementation

This component admits the20 selected historical macro contexts plus four approved
WP39 normal root/nested-child QUIT replays. WP39 source419edc2 and independent
reviewbd9d29d qualify normal FC20 stop-all in initial DISPLAY OFF mode with
registered, unfired handlers. Active-handler QUIT remains statically refused.
“Top-level” means normal statement context in the current file, including a nested
child; it does not restrict QUIT to call-depth1. No full FR012 or product scenario
is closed. Subtask/lifecycle completion is owned by the canonical runtime.

Cycle1 repair: the reviewed127f211 implementation's eager FOR EACH expansion was
rejected for bypassing actual work/slice bounds. That source's passing checks and
fuzz remain historical, not proof of the repaired path. `evidence/fix-cycle-1/`
binds the repair, exact red/green repro, final frozen source, checks and measured
fuzz. Variable names are interned at Compile, runtime evaluation advances one
precompiled postfix node per charged work unit, and list preparation builds one
fixed node per result before entering its body. Private literal/value backing is
immutable and shared. Variable output is constructed one native word per callback;
no whole expanded value array is constructed in one Step. Run limits, slice limits
and cancellation govern actual evaluation work rather than prepaid scalar debt.

Runtime arithmetic/comparison is fixed signed64; no string concatenation, string
comparison, runtime numeric-text parse, name hash or recursive expression tree
walk is admitted. Numeric output conversion has a fixed maximum20 characters.
The proven single-binary grammar has at most two temporary values and three
postfix nodes; each node is independently charged. Frame variables use private
bounded slots, preserving case-sensitive native names and separate frame state.

The unchanged approved public API separately transfers whole independent native
request/result snapshots: at most4096 Words (128KiB backing on the declared64-bit
host) per name copy. A maximum-width pending NEST Step uses four such copies and
measured524448 bytes including wrappers; a State/waiting-result observation copies
one bounded name. These are intrinsic whole-value API transfers, **not**
quota-proportional interpreter evaluation. Their fixed byte bound and host callback
latency must not be represented as one-word work/slice latency guarantees.

The exact approved WP32 API is implemented: Limits/Policy/Program, Compile/New,
Machine.Step/Resume/Stop/State, native Effect/CommandSink and ProgramRequest/Resolver,
Resolution/Condition/EffectResult, Result and typed Failure. Result has no additive
fields. Its Steps and EmittedWords are charged-work/delivery-attempt counters,
**not applied-output receipts**. The actual sink owns ordered Apply receipts and
document/session effects. The machine records the current MayHaveEffects privately,
stops on a host error, and makes no rollback claim. Arbitrary host error objects
remain host-owned diagnostics; this package does not claim to deep-clone them.

Production imports only the approved wpm codec and standard-library pure helpers.
There is no storage/editor/document/TUI dependency, host IO, terminal, shadow
document or native serializer. Compile consumes original word identities/spans,
not a printed/normalized macro listing. Program code/policy/limits/source are
private snapshots; New copies the caller's replaceable Program wrapper. Compile
also retains an independent Image wrapper sharing only its API-immutable private
backing. Whole-value replacement of caller Image/Program handles cannot retarget
an accepted run. Policy keys, callback words, resolver names, NeedProgram and own
typed failures are independently copied at public/callback boundaries.

Current admission: native ASCII literals, DISPLAY OFF and Forward Search events;
IF/ELSE/END IF, top-level GO/LABEL, numeric ASSIGN/VARIABLE, proven nonempty positive/
negative **unit-step** FOR, bounded WHILE, FOR EACH order/duplicates/literal quote
values, tested FOR NEXT/BREAK and ignored root/child file-level BREAK. Expressions
are native signed decimal/reference/single +/< /= trees; VARIABLE consumes its
inner name~ before the enclosing expression~. No generic split-on-tilde, quote
stripping, Unicode remapping, coercion, precedence or guessed operand width.
Unowned literal tilde/unsupported escape contexts refuse compilation. Scalar
ASSIGN is numeric; unqualified string assignment is refused.

Statically discovered unknown images/instructions/structures, unqualified QUIT, malformed
arguments and ambiguous labels refuse before any effect, including dead branches.
GO/labels/handlers/NEST/RETURN are admitted only at the qualified top-level file
scope. FOR EACH referenced-variable mutation timing, loop-control-variable body
mutation, variable-dependent FOR bounds, untested loop-control families and
cross-file variable scope are conservative refusals. Handler regions admit only
the observed literal/label/child-return bodies; handler-reachable GO/conditions/
loops/nesting/search/redefinition/QUIT refuse before effects. Thus a backward GO
from a handler cannot circumvent an active-handler context guard.

Each frame has independent default handlers. Explicit original CommandError from
the resolver models only the captured missing-macro condition; NotFound is admitted
only from an injected Forward Search event. Host errors/unsupported commands never
become original handler conditions. Child command-error propagation, local handling
and parent-handler resumption have component plumbing tests on explicitly derived
inputs (QUIT overlaid with DISPLAY OFF in test memory). Those are **not** original
source conformance passes. The unchanged originals are separately replayed in
TestOriginalMacroContexts after approved39 qualification. Known source width alone
does not qualify behavior. QUIT in a structure, without initial DISPLAY OFF or a
registered handler, or with broader preceding control/variable contexts is refused.

Waiting resolution preserves a copied request and invokes the resolver once.
Wrong/duplicate/late IDs fail without consuming the live pending request. Ready
children receive full compile preflight before child effects; parent effects
already applied remain in sink receipts. Resume reports terminal run failures as
typed errors and State. Host Stop/context cancellation are separate safety
operations, not original Cancel(F1)/ON CANCEL integration. Machine mutation has a
single serialized owner; callback reentry is refused as Busy. Independent machines
may run concurrently. User code must not mutate arguments during Compile/New.

Budgets are the approved Linux safeguards:1,000,000 work steps,1,048,576 delivered
words,16 call frames,32 loops,256 variable names,4096 words/value/name,16 expression
levels and at most256 charged work units/slice. Every limit is positive/capped;
New may narrow but cannot enlarge its Program's copied compile limits. All calls
share one run's counters. Host Repeat clients subtract previous charged counters
from their remaining run budget rather than resetting them invisibly.

Input-word compilation work is accounted as a bounded debt before a program's
first effect; slices charge that debt before continuing. Literal delivery is
charged per word and every control iteration is charged even if it emits nothing.
Compilation itself and injected callback latency have separately bounded inputs,
not an instruction-derived wall-time promise. A maximum codec-word stream exceeds
the narrower compile-step budget; an exactly1,000,000-word admitted scan consumes
the entire work budget and delivers no effects. Native source bytes remain exact.

Evidence is separated carefully:20 original contexts/40 original result exports
are hash/body inspected,46 WPM source exports retain22 source hashes, and all20
match component trace projections. Four new approved39 replays additionally consume
actual Q39R/Q39P/Q39C inputs and compare native QBEFORE/QAFTER/QOTHER bodies,
retaining two incomplete39 samples outside success accounting. Those native files
are original evidence, not Wordling-generated outputs. Recording131 has
an external recorded ABC prefix;132 uses an explicit host repeat client;178 has
an external manual READY suffix and a source-span query exclusion. Every literal/
key/query event remains in sink receipts. The trace inspector is not a general
search or document model and produces no native file.15 merge cases are excluded
from macro success accounting. Existing raw files are not changed.

The10s fuzz log in evidence/development is an early development probe. Its16/4
case-status and checkpoint manifests intentionally retain the historical state;
they are not final acceptance. evidence/final binds the final Go and corpus hashes,
actual commands/results, genuine seven-check JUnit, race, ordered sink receipt test
events, resources and finite mutants. The acceptance sequence is60s then600s with
two workers; commands.json and raw logs report actual completion separately.
The frozen-inputs manifest includes codec/module/source/native-ledger bindings.
These safeguards are measured Linux bounds, not original DOS resource limits.

A real client obtains an immutable image through approved storage34, compiles with
its ordinary command sink's capabilities, constructs one machine, and feeds bounded
slices to its event loop:

```go
limits := runtime.DefaultLimits()
program, err := runtime.Compile(image, sink.Capabilities(), limits)
// Handle err before creating or running the machine.
machine, err := runtime.New(program, sink, resolver, limits)
// Handle err, then schedule slices until terminal or waiting:
result := machine.Step(ctx, limits.SliceSteps)
// A pending resolver's later reply uses the exact request ID:
// err = machine.Resume(result.NeedProgram.ID, resolution)
// The same client retains each sink.Apply receipt and its document/session result.
```

The public boundary is tested externally. Actual editor36/TUI37 acquisition,
ordinary command delivery, selection/source/revision guards and integration of
original Run/Repeat/Cancel behavior remain queued consumer work. Machine.Stop is
a host safety API, not a claim of original F1 integration. This component never
opens files or publishes native documents.

Queued consumers are actual editor36 and executable37 through ordinary document
commands and rooted34 acquisition after its independent review. All38 requirements,
91 groups and nested leaves remain retained; macro recording/editor/conversion,
full merge/data, non-ASCII/resources/physical/historical qualification and full
FR-012/M1 acceptance remain open. PDF is M2 after accepted M1. No reference VM,
new native WPM writer or CMD51-199 editor/disk roundtrip was run here.
