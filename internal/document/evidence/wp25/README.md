# WP25 immutable native writer evidence

Audience: WP25 independent reviewer and WP26/27 implementers. This is a bounded
library implementation, not product/session parity, new document creation or
closure of any parent FR/NFR/FC/scenario/group. M1 remains complete WP5.1 parity;
PDF is M2 only. Ownership is exclusively internal/document/**.

## Final immutable revision correction

Before lifecycle handoff, root reproduced a concrete legal Go wrapper-assignment
defect in the initial implementation: same-length *d=*other accepted an old cursor
against different content; a shorter replacement made Offset panic, and zeroing
rebound snapshots. The public failing repro is retained in revision-fix-repro.txt.
This was caught before independent review/status transition; it is not an
original-app mismatch or verdict event.

The final model puts image/gaps/original into one private immutable revisionState.
Document is a replaceable public handle; Revision/Cursor capture actual state,
never the handle address. Old cursor offsets/movement/views remain stable after
same-length, shorter, zero and repeated handle replacement. Edits reject stale
state before indexing; copied handles to the same actual state deliberately share
identity, separately parsed equal bytes do not. Independent returned-result
snapshots remain stable when another result handle is replaced. No second model,
native decoder, grammar, metadata rule or support limit was introduced.

Final source and producer hashes are in revision-fix-candidate-seal.json. The
producer emitted all5 candidates into a fresh revision-fixed-candidates directory;
all bytes/SHA match the actual ten previously tested guest inputs. Original runs,
input metadata and old test/fuzz logs remain unchanged. The final source itself
was not run in a guest: the exact native-byte equality bridge binds its outputs
to those original observations. No identical-byte guest rerun was authorized or
needed. New direct-run-unrun expectation metadata does not replace the actual
earlier control-qualified Q+Z reference/expectations.

Use audit.py --revision-fix for current verification. It checks historical changed
Go source against immutable14d8f21 Git blobs, final source against the new seal,
all original custody/protocol outputs, all5 candidate equalities and actual final
document API reopens of52 native paths. The prior audit/default invocation belongs
to the initial source checkpoint; previous final-source-identities.json and logs
are historical, not evidence that source never changed afterward.

The same prescribed60s then120s two-worker budgets were explicitly re-declared
before execution for this real boundary change. Final fuzz adds legal shorter
wrapper replacement, stable Revision/Offset/Present and stale-edit atomic refusal.
Final logs/results use revision-fix-* names. Final21 top-level tests, race and7
configured checks pass(0 skips). Final60s fuzz:4317541 executions,60.69s wall,
RSS89280KiB;120s:8546210 executions,120.22s,RSS96964KiB. No budget expansion.
Final measurement retains19128 B/op admission,187144 B/op changed typeover and
786485 B/op inherited max-metadata refusal; no hard peak-live cap is claimed.
Six compiling overlay faults include
accepting stale state and mutating already published private state, both killed by
public assertions. Raw/native policies and the admitted/refused resource-cost
distinction remain unchanged; final-source measurements are separate.

## Authority and API

WP15 immutable model44f1a6d is extended, not duplicated. Actual unchanged native
reader SHA e13c93687e6119bff44f8405616455849cb728f3b4a1b3949d987dbe2c30b1d6
owns native framing. WP23 a3f3ae3/eb86058 field contract/ADR0003 was independently
approved by event01M67WQ9AQMX49C480NN3A267C (review evidence9bc71db, recorder2d7c97e,
transition42021fe). Its original source says conditional/proposed; this approval
provides the required authority. No approved contract/source/raw witness changed.

Public API: CheckMutation() error; InsertASCII(Cursor, []byte) and
TypeoverASCII(Cursor, []byte) return EditResult{Document, Cursor, Changed} plus an
error. Every refusal returns the exact receiver and incoming cursor unchanged,
with no partial revision. Successful body changes create a distinct opaque
comparable Revision; old/cross-document cursors fail RevisionMismatch. Repeated
character typeover replaces next ASCII, inserts before a code, and appends at EOF;
characters after encountering a code remain before it. Normal/Reveal share gaps.

Export copies the current native revision; OriginalExport retains/copies the
initially loaded image across revisions. Empty input preserves identity. Same-byte
typeover advances its cursor without a new native revision or guessed metadata
change. Changed describes actual native body change, not an original session
clean/dirty/save outcome. Original prompt/mode/history/IO semantics stay outside
this package. Failure remains typed document.Failure; malformed native errors
retain wp51.Failure. InvalidASCII TokenIndex identifies the offending input byte;
unsupported field spans identify exact absolute source ranges.

## Admission, serialization and safety

Admission consumes actual reader block/packet spans and checks both full index
blocks, terminal/unused zeros, five indexed packets, complete nonoverlapping
prefix ownership and all approved72 header/resource/metadata fields. Resource
caches e724/1172 remain literal; counter1 is required. Pool/AFC and zero-graphics
relationships are explicit. No digest/fixture whitelist, prefix template, fixed
body start or packet6 offset grants admission. Synthetic physical relocation
resolves flags at166. Qualified body is printable WP ASCII and at most2 sequential
matched nonnested Bold pairs including literal empty pairs. This is an initial
qualification policy, never an original format limit; higher counts remain M1.
Hard returns, C0, other attributes/characters, opaque/nested/formatter functions,
unknown/deleted/aliased/unowned prefix variants refuse before mutation.

Parse/no-edit Export keep prior16MiB/1M-token policies. Mutation additionally caps
input/output at65536 bytes/16384 tokens. In this closed schema, combined max-token
+2-pair input derives16716 bytes and65540 bytes of gap index; these are support
bounds, not universal original offsets/capacities. The writer copies its owned
INPUT prefix, changes only indexed packet6 must-format bit3 on body change,
serializes directly in original format and revalidates through actual Parse and
admission. All other bytes/pointers remain identical; no relocation is needed
because the admitted field contract has no body-target references/length field.

Original after-Off typeover saves flag0 in the sampled witnesses; the independently
approved writer policy sets8. Tests expose that exact allowed difference. Both
fresh Go candidates pass original reformat/edit/print/Save; no normalization or
whole-native byte-equality claim hides the difference.

budget-plan.json is the unchanged pre-execution policy checkpoint. Its allocation
phrase was too broad for refused broad-reader inputs: inherited Inspect clones
metadata before rejection. allocation-interpretation.md and measurements.json
separate that cost (786488 B/op at4096 blocks/16384 entries) from admitted max-token
inspection19128 B/op and changed typeover187136 B/op. Neither B/op nor process RSS
is a hard peak-live cap, DOS limit or product SLO. No source/policy/fuzz expansion
was made to optimize/conceal it.

## Actual original interoperability

Source checkpoint14d8f21 pins the actual Go API, producer and five edited files in
candidates/sealed-plan.json. All source/file hashes remain unchanged through the
batch. The owned pure serial batch.py and invoke.py archive executing Python,
transitive helpers and scheduler before each fresh guest; additional unused helper
snapshots are labelled snapshots, not proof they executed. Producer/API sources
are committed prelaunch and pinned by provenance. Only output/temp-reader-probe
routing changes; the approved WP23 engine/helper sources execute unchanged.

All12 fresh guests completed and stopped/extracted, batch exit0. Ten actual Go
candidate runs (five kinds×2) passed the approved candidate protocol. Four kinds:
ASCII abc→aXc→aXYc; Bold insertX g1; typeoverX g2; typeoverX g5. The fifth changes
the actual repair-Restore empty-first-pair source X→Q atgap4. It is not a net-zero
or surrogate output. Two fresh ORIGINAL controls separately captured Typeover,
Reveal native labels and actual gap4→5; retained literal On-Off-On. Their complete
Q+Z streams were exactly equal165B/SHA479a7f6fca1e5a7eef7f3add9e9ecea1d8ddd9ec2ba7850e80391a699c30a117.
Only then were the Go Q expectations sealed and its two guests launched.

Controls are original observations, not candidate verdicts. Their retained X+Z
anchor comparison deliberately fails the prior-print equality check; every other
protocol check plus native/code-pane/literal-ink audits and independent paired
Q+Z streams qualifies the new baseline. This expected exception remains explicit
in raw-derived diagnostics; it is never turned into official candidate acceptance.
Go Q candidate comparisons against the sealed actual Q streams pass all checks.

Every candidate had readonly B seed, fresh master, shared primary session1.lock
and short QMP, actual settings/resource/source/archive identities; original
Retrieve, declared subsequent Home3 Up End insertZ, complete selected Other-port
print and empty-job capture, fresh Saves, exact approved postwait DOS state, stop
and extraction. Master/input/seed remain unchanged. Oracle released immediately
after final extraction at02:59:58UTC, before offline audit/checks. No failed,
skipped, tuned or extra guest. Earlier approved evidence remains immutable.

Actual document.Parse/Export reopens all52 new native artifact paths byte-exact:
40 original post-save outputs plus12 candidate/control inputs (including repeats).
All52 share normal/Reveal token spans. Twelve clean inputs admit mutation; the40
original FastSave/deleted/residue outputs remain lossless read-only and refuse
mutation. No full original-save→arbitrary-edit roundtrip is claimed. Existing666
artifact paths separately retain303 mutation admissions/363 refusals. Artifact
paths include duplicate contents, not independent documents.

The selected baseline is March9 1992 U.S. English, QEMU8.2.2/FreeDOS1.4 and mixed-date
July1992 text-only Standard Printer. Raw settings/EXE/FIL/DRS/PRS/SET identities are
in every run; no proprietary resource/manual/disk is committed. No historical DOS,
graphics/preview, physical metrics,6lpi, terminal delivery or tolerance claim.

## Reproducible verification

Executed from runtime lane-e, all exit0:

```
go test ./internal/document -count=1 -v
env GOMAXPROCS=2 go test ./internal/document -run='^$' -fuzz=FuzzNativeMutation -fuzztime=60s -parallel=2
env GOMAXPROCS=2 go test ./internal/document -run='^$' -fuzz=FuzzNativeMutation -fuzztime=120s -parallel=2
python3 internal/document/evidence/wp25/mutants.py --revision-fix
python3 internal/document/evidence/wp25/audit.py --revision-fix
go run ./internal/document/evidence/wp25/measure
go test -race ./internal/document -count=1
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml internal/document/evidence/wp25/validation.xml
```

60s fuzz:2814547 executions,61.46s process wall,RSS94888KiB.120s:3832818 executions,
121.30s,RSS92772KiB. Both two workers, no crash/source mutation; counts are
nondeterministic/exhaustiveness is not claimed. These retained initial logs bind the pre-correction source. The final correction
and final-source fuzz sequence are identified separately above. Explicit declared budgets/seeds preceded execution.

External API tests include actual source/native outputs, all32 original boundary
outcomes across views, invalid/stale/cross-revision gaps, every prefix-byte fault,
relocated indexed flag, literal cache variants, caller/export/original isolation,
opaque/nested/unmatched/third-pair/truncation/overflow/source/output boundaries and
no partial return on refusal. Five compiling Go-overlay faults were killed by
actual assertions; production was never modified. Seven exact canonical title/
feature/inventory associations and a wrong-feature negative pass, with bounded
scopes and unchanged registry statuses. Native/body/raw/source/final-state audits
reproduce all12 results,2848 raw manifest paths/332914329 bytes. The seven real
configured checks pass (0 skips), including actual go build ./..., go test ./...
and go vet ./..., with relevant race check. Formatting/diff and Git-object checks
are separate final handoff receipts.

WP26/27 must use this same model and the exact contextual deletion/history
contracts. Product/session/application consumers and filesystem publication remain
later gates; this library approval cannot substitute for them or full M1 scope.
