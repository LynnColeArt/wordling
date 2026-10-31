# Bounded immutable WPM image (WP33)

Implements T097–T099 against approved WP32 source
`4eb851eac3096d27d4743616ce3ae74f7a9edc05`, reviewed/approved independently.
This is a native companion reader component, not macro execution, editing,
recording, conversion, WPM writing or product FR-012 completion. All38 M1
obligations/91 groups and discovered nested leaves remain retained. PDF is M2.

`Parse(input, DefaultLimits())` admits the bounded DOS macro tuple1/1/1/1,
four-entry index, description byte extent and body words. It owns its complete
input; Export is an independent exact copy. Inspect, Description and BodyWords
also return independent copies. SHA256 covers every original byte. Caller input
must not change during Parse. Accepted images are safe for concurrent read access;
the zero/nil image is not an accepted native file.

Words retain original uint16 identity, kind and absolute two-byte span. Alignment
is relative to the stored body offset: original FLOW has length169/body75.
Descriptions remain raw bytes including their terminal byte. There is no Unicode,
CP437, DOC token decoder or document serializer. Tests verify all46 original WPM
exports/22 unique hashes and their Git blob identities without copying/editing raw
evidence. The small testdata manifest is extracted from WP32's approved ledger,
SHA256 `fca8446e98ad95ab118fc672e48e821afc65e9e3b2b5a43c27f7759824c2ce5d`.
It references existing project-authored sources under docs/research/reference-runs;
proprietary binaries/manuals/resources are not included. Lane-n's canonical base
does not include WP32 planning files, so tests pin this owned manifest rather than
depending on another checkout or unmerged contract paths at runtime.

Parse success is framing/retention, **not execution admission**. Known macro/key
identities remain typed, but their operands, matched structures, expressions,
commands and context require WP35 Compile. A known opcode without valid operands
can be a framed Image with no findings; that never licenses execution. Inner
VARIABLE and outer argument tilde identities remain distinct raw Words for that
compiler. Only original ASCII literals, the20 observed macro identities, Forward
Search and terminal have no classification finding. Even those have no execution
implementation here. No original error message is fabricated.

Unqualified macro/key/character/control/unknown words, nonzero unused indexes,
description variants/gaps and suffix bytes are retained with blocking findings.
Diagnostics retain the **first occurrence per finding code**; BodyWords retains
every word before/including the first terminal. An odd opaque suffix is allowed,
while an unpaired body byte before the first terminal is malformed. Finding count
is therefore bounded independently of hostile word repetition. Reserved/other
producer/version/index-chain variants are distinguished from malformed fields.
Unsafe overlap is UnsupportedStructure. No linked block is followed, including
cycles. ReleaseEvidence is always unknown-from-bytes; tuple recognition never
certifies the producing release/platform. External original fixture provenance is
a separate evidence binding.

Limits are explicit positive settings, capped at16MiB input,4096 description bytes
and1,048,576 body words including terminal. They are Linux support budgets, not
historical DOS limits. Size/traversal rejection occurs before input copying; Parse
allocates no word array. BodyWords allocates its bounded independent view on demand.
Failure uses Code/Offset/Field/Detail, distinguishing invalid limits, unsupported
format/product/type/version/encryption/variant/structure, truncation, malformed
prefix/body and input/traversal limits. Returned diagnostics describe this reader.

Public surface is the exact WP32 contract: Span,Kind,Word,Limits,Finding,Header,
Inspection,Failure,Image; DefaultLimits/Parse and Image.Export/Inspect/Description/
BodyWords/SHA256. WP34 is the queued production storage consumer: ReadMacro will
reuse readStable and delegate validation here. WP35 consumes BodyWords for the
injected-sink evaluator; it must not import storage/editor/document/TUI. Actual
editor/TUI integration is WP36/37 after reviewed original WP38 evidence. No
filesystem transaction, Macro Save/Publish or implicit original execution is added.

Validation/evidence records live in evidence/. Original hashes, copy isolation,
DOC↔WPM refusal, unknown-word retention, relative offsets, prefix/description/index
refusals, odd body/missing terminators and exact limit boundaries have external
public-API tests. Fuzzing checks typed failure/no mutation or exact accepted bytes,
terminal/spans/suffix and independent exports. Benchmark figures are measurements
on the recorded host, not product/physical-terminal performance qualification.

`go test ./...`, `go build ./...`, `go vet ./...`, race, catalogue/configured review
checks and sequential60s/600s fuzz runs are the validation commands. No VM or
CMD51-199 original macro-editor/disk roundtrip is claimed. Component validation
cannot close recording/editor/conversion/merge/non-ASCII/resource/physical or
remaining M1 obligations. Independent review remains required.
