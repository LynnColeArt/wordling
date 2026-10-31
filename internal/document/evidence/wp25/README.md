# WP25 implementation checkpoint (original interoperability unrun)

Audience: WP25 reviewer and WP26/27 implementers. This checkpoint implements the
approved WP23 field contract in the existing WP15 immutable model. It does not
claim completed T073–75, original writer interoperability or M1 acceptance yet.

Public API: `CheckMutation() error`; `InsertASCII(Cursor, []byte)` and
`TypeoverASCII(Cursor, []byte)` return `EditResult{Document, Cursor, Changed}` plus
an error. Every failure returns the exact receiver and incoming cursor unchanged.
Successful body changes create a distinct opaque comparable `Revision`; cursors
from another revision refuse. Multi-character typeover behaves as repeated
character commands at the resulting gaps: replace ASCII; insert before a code;
append at EOF. Normal/Reveal use the same gaps and explicit view value. Empty
input and same-byte typeover do not invent metadata changes; the latter advances
its cursor. `Export` copies the current native revision. `OriginalExport` retains
and copies the initially loaded image through all revisions. No filesystem IO,
new document construction, mode toggle or deletion/history command is added here.

Admission consumes the actual unchanged wp51 reader's block/packet spans, checks
both complete index blocks (including unused zeros/terminal next pointer), all
five indexed packets and complete nonoverlapping prefix ownership. Every admitted
resource/metadata field is checked against the approved72-field closed schema.
Literal e724/1172 caches and counter1 are retained; no algorithm is inferred. The
font pool/AFC and zero-graphics relationships are checked explicitly. No source
fixture digest, template prefix, fixed body start or fixed packet6 offset grants
admission. The relocated-packet synthetic test checks flags at166, not256.

Body grammar admits printable WP ASCII and at most2 sequential nonnested matched
Bold pairs including literal empty pairs. This is a qualification policy, never an
original format limit. Parse/no-edit Export retain the prior16MiB/1M-token policies
and preserve additional reader-accepted native variants; mutation additionally
requires <=65536 bytes, <=16384 tokens and this narrow field/grammar contract.
Prospective output limits/refusals occur before a new revision/cursor is returned;
no history state exists in this WP. Full NFR/FR/FC and M1 remain open.

The serializer copies the admitted input prefix and changes only indexed packet6
bit3 on actual body change; it appends the changed ASCII/body bytes directly in
original format, then validates through actual Parse and admission. All unrelated
bytes remain identical. Original after-Off typeover sometimes saves flag0; the
approved writer policy sets8. Tests explicitly allow only that one raw difference,
without rewriting the original witnesses or calling their native files identical.
Required actual original retrieval/reformat/edit/print must still qualify it.

`candidates/sealed-plan.json` contains five real Go-emitted changed candidates and
executing source hashes. `reference/plan.json` freezes12 planned fresh guests:
8 for the four exact existing original-reference kinds;2 original typeover-Q
controls on the actual empty-first-pair source, then2 Go Q candidates against
those observed identical Q+Z print streams. The fifth expectation deliberately
has no reference until the two actual controls qualify; no guessed printer bytes.
`reference/invoke.py` executes the approved unchanged WP23 engine, routing output
only to owned evidence while retaining exact executing helpers and sources.
Baseline observations and official Go candidate acceptance remain distinct.
Root must grant exclusive VM access before any invocation.

Completed offline: initial expected test-first build failure; deterministic public
API tests, all32 original boundary output/body/flag comparisons, all666 archived
reader paths with303 admitted/363 refused, every prefix-byte mutation, relocated
indexed flag ownership, literal hash/flag variants, malformed/opaque/pair and
budget/refusal/revision/isolation tests. The declared60s two-worker mutation fuzz
completed exit0. The120s run, resource measurements, meaningful selected mutants,
race/build/vet/configured checks and actual interoperability remain pending at
this checkpoint. No subtask or lifecycle transition is authorized by this text.
