# WP35 cycle1 work-budget repair

Independent review correctly rejected127f211's eager FOR EACH value expansion.
The exact unchanged public-API overlay test is retained as reviewer-red stdout,
stderr and command metadata: the8204-word source expanded1024 references to4096
words and allocated16,845,392 bytes in one charged step. The exact test is now
part of the owned permanent suite. Earlier final/development/fuzz evidence stays
unchanged and bound to its historical source, not relabeled as repair acceptance.

## Repair and scope

Compile interns case-sensitive native variable names to bounded private IDs and
compiles each proven expression to postfix nodes. Runtime uses frame-local value
slots, avoiding name hashing and recursive tree traversal. One actual postfix
node consumes one charged unit. Numeric evaluation is fixed signed64; no runtime
numeric-text parsing, string comparison or concatenation exists. Numeric word
formatting has a fixed20-character maximum. The single-binary grammar has at most
two temporary values/three nodes, with a fixed stack and no variable-size setup.

FOR EACH prepares one argument node at a time and stores each completed value in
a fixed-size linked node. There is no all-item allocation/geometric slice-copy.
All arguments still evaluate before any loop body effects, including late failure.
Private value/literal backing is immutable and shared; later variable assignment
rebinds a private slot rather than mutating that backing. Variable output constructs
one native word per charged delivery, without materializing a full value array.
Source spans, native identities, conditions/handlers, exact-once receipts, public
copies and independent machines retain the approved API and semantics.

The intermediate scalar-precharge design was discarded before final acceptance:
prepaying debt would still defer long name/tree work into a final one-unit burst.
The final source contains actual evaluation continuations and compile-time IDs.
No production caps were raised, supported original context removed or native/API
expanded. The focused fuzz harness now exercises the existing4096-word value cap
and permits16384 charged test work units so the8204-word regression seed reaches
execution; its former64-word/512-step harness could only refuse that seed.

## Actual bounded evidence

The exact repaired repro now allocates48 bytes in the sampled one-unit Step.
The next call reaches the run limit without body effects. Total allocations for
extra run budgets2/200/1088 were512/10240/50128 bytes; all stopped at the exact
run limit. The full4096x1024 non-emitting traversal completes at10258 charged steps
with49888 allocated bytes, retaining no sink effects. Per-Step counter deltas stay
at most1. Max measured allocation in the long-variable delivery test is240 bytes
per one-unit Step; OutputWords1 permits exactly one actual callback, then limits.
These are measured cases, not a universal memory ceiling.

Tests cover cancellation and explicit Stop during partial preparation, terminal
idempotence, long-name interned control, late undefined-list failure before effects,
expression-node work before output, source retention and copy isolation. All20
historical macro trace contexts and four approved39 root/nested QUIT replays still
pass. The15 merge cases remain excluded; no product/native output is claimed.

The frozen repaired source passes genuine7-check configured JUnit with0 failures/
errors/skips, full composed-lane race, final event/resource tests and16 killed
mutants. New faults restore long-value copying, omit node charging, materialize
whole variable arrays and enter list bodies before all arguments evaluate. Two
mutation-harness targeting mistakes are documented with retained initial harness
code and the next attempt stdout/stderr: the first aliased
literal backing even on the separate variable path (panic), and the next source
pattern matched two locations. Final mutants target the intended paths and fail
actual assertions; neither harness mistake counted as a killed semantic mutant.

Final measured benchmarks on declared AMD Ryzen5 5600X/Linux/Go1.26.4 are421.9ns,
960B/10allocs per Compile(originalABC) and1043ns,1952B/19allocs per New+drive.
The resource/benchmark process peaked at87276KiB RSS and2.84s wall time, including
Go/process work. Commands and real stdout/stderr are retained. Final focused fuzz passed2,569,320 executions/60s and20,099,742/600s,
with the whole driver exit0 and180 passing runtime test/subtest events. It uses native original+negative+long-value list seeds, up to16384 work units,
128 output words/4096 value words, source/counter/terminal/pending invariants and
a4MiB runtime-allocation test bound for that bounded harness. Actual60s then600s
results are in fuzz-summary.json after complete CLI exit; previous660s results
remain historical. No macro producer, VM or new host dependency was introduced.

## Fixed public snapshot and host boundaries

The approved WP32 API requires independent whole ProgramRequest.Name snapshots in
resolver arguments and Result.NeedProgram/State observations. Each name is bounded
at4096 native Words. Word is32 bytes on the declared64-bit host: one name backing
is128KiB. The maximum-width pending-NEST Step makes four such transfers and
actually allocated524448 bytes including wrappers; a later State/waiting result
copies one bounded name. This is a fixed intrinsic public API transfer, not a
quota-proportional evaluator operation or a small-step latency guarantee. Host
resolver/sink latency also remains outside VM instruction-derived timing claims.
The permanent test records the measured bound and mutation isolation. Independent
review must assess this retained boundary against approved32; it is not silently
called one word of real copy work or a solved generic callback-latency problem.

## Review handoff

Only internal/macro/runtime/** changed. All final frozen Go/test/corpus/module/
codec hashes and the current Git-blob manifest bind actual source/evidence;
old manifests reference their historical commits when old paths have new bytes.
Actual consumers remain editor36/TUI37 using rooted34 acquisition and ordinary
editor commands. No storage/editor/document/TUI import, shadow document, native
writer, direct host IO or original reference VM run exists here.

All38 requirements/91 groups/nested leaves remain retained. Recording/editor/
conversion/CMD51-199/full merge/non-ASCII/resources/physical/historical gaps and
full FR012/M1 remain open; no acceptance/merge/PDF work is claimed. Independent
review and canonical lifecycle follow the root's explicit quiet point.
