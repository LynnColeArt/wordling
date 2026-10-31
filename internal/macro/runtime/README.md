# WP35 bounded pure macro evaluator — source checkpoint

**In progress, not ready for review.** This checkpoint admits16 of the20 selected
original macro contexts. Original206/210/212/213 are statically blocked by the
unqualified FC20 QUIT instruction, even on paths captured handlers skip. WP39's
normal root/nested-child QUIT handoff must be independently approved and brought
into this lane through the supported dependency refresh before admission changes.
Active-handler QUIT remains unqualified. T103–T105 are not marked complete here.

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

Statically discovered unknown images/instructions/structures, QUIT, malformed
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
source conformance passes. Known source width does not qualify QUIT behavior.

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
are hash/body inspected,46 WPM source exports retain22 source hashes,16 contexts
currently match component trace projections, and4 are blocked. Recording131 has
an external recorded ABC prefix;132 uses an explicit host repeat client;178 has
an external manual READY suffix and a source-span query exclusion. Every literal/
key/query event remains in sink receipts. The trace inspector is not a general
search or document model and produces no native file.15 merge cases are excluded
from macro success accounting. Existing raw files are not changed.

The10s fuzz log in evidence/development is an early development probe, not the
required final60s/600s acceptance sequence. Finite mutation/resource/race results
there are bounded development evidence. Final source validation, the full configured
runner and the prescribed acceptance fuzz sequence remain pending until approved39
and any resulting compiler change. No source/probe/review/approval handoff is
claimed by this checkpoint.

Queued consumers are actual editor36 and executable37 through ordinary document
commands and rooted34 acquisition after its independent review. All38 requirements,
91 groups and nested leaves remain retained; macro recording/editor/conversion,
full merge/data, non-ASCII/resources/physical/historical qualification and full
FR-012/M1 acceptance remain open. PDF is M2 after accepted M1. No reference VM,
new native WPM writer or CMD51-199 editor/disk roundtrip was run here.
