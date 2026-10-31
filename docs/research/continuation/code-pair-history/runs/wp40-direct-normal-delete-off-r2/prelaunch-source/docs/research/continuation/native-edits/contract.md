# Conditional bounded native edit field contract

WP23 proposal; independent contract approval is required before any production
serializer. The accepted-pair and field audits are complete and reviewable in
verification.json. It grants no production writer authority before independent
WP23 contract approval. M1 remains complete plain WP5.1 parity; this is a bounded first slice.

## Native identity and complete ownership prerequisite

Use the actual approved native reader before mutation. A read-only accepted file
is not necessarily mutation-admitted. Admission additionally requires the exact
unencrypted native tuple, two checked five-entry index blocks, only live packets
7/15/12/6/8, zero graphics, complete nonoverlapping prefix coverage and no deleted,
reserved, unknown, initial-code, nested or formatter structures. Packet order is
an admitted observation, not a universal schema. The header's body pointer is
checked against actual file bounds; index lengths/pointers are decoded, not
replaced by template offsets. All unused slots/terminators must be zero and the
last index next pointer0. Every nonempty prefix byte must belong to the header,
a checked index block or one admitted packet; unexplained gaps/aliases refuse.

field-ledger.json inventories every header, index and packet field with width,
signedness, units, references, ownership and preservation policy. Its72 field
rows exactly cover the16-byte header and packet payloads; index schemas separately
cover every10-byte slot. The observed source prefix totals324 bytes because of
its checked constituent sizes;324 is not a universal body start. Packet6 location
is resolved from its index. A synthetic reordered-packet safety test resolves it
at166 rather than256; this is not original behavior evidence or permission to
rebuild packet order.

Preserve the owned INPUT prefix bytes. Never substitute a bundled fixture,
abbreviated prefix, resource template or reconstructed header. Supported body
mutation changes EOF length only: there is no header body-length field or explicit
EOF code in the admitted schema. The header/index pointers remain prefix-local
and unchanged. No edited body byte is the target of any admitted prefix field:
font-pool references are packet7-relative; AFC references are font-record indexes;
font/printer IDs, descriptor hashes, metrics and strings belong to resources;
packet6 fields are document/display/printing metadata; zero-count packet8 has no
graphics table or data extent beyond its two bytes. Reject any other relationship
rather than assuming EOF framing alone proves edit safety.

## Font and resource relationships

Only the selected Standard Printer/Courier10cpi resource payload shape is proposed.
Packet7 contains the bounded NUL string. Packet15 contains one86-byte font row;
its+18 offset points to a string start in packet7, not to body text. Packet15's
27-byte descriptor is completely inventoried, including signed italic adjustment,
traits, hashes, completeness bit planes, point size and flags. Packet12's initial
printer-font descriptor and current font fields are distinct resource information;
they are not falsely required to equal the document's font descriptor.

SDK51 WP103–105/PDF116–118 defines AFC bytes as indexes into86-byte font rows,
FF for no change and FE for an unavailable chain target. The pinned row has Bold
slot12=FF; FE occurs only in slot15 (Small Caps), which this grammar never enables.
Character-set and orientation arrays are pinned FF. No C0, font change, orientation
function, other attribute, nonzero font flags or unqualified resource row is
admitted. Font match hash and printer-selection counter are source-owned scalar
metadata: their original changes will be retained and classified, never guessed
from file offsets, recomputed from body length or treated as body references.
The two exact descriptor-match hash bytes e724/1172 are qualified by literal
original pre/post-print witnesses with all other font payload bytes unchanged.
Admission preserves whichever input variant is present. The fresh-document
printer-select counter must equal1; other observed counters remain read-only
accepted original variants and refuse this first mutation admission.

The paper/font/initial settings and actual EXE/FIL/DRS/PRS/SET identities accompany
each original run. Physical font advance/height, printer origins and graphics
remain outside this field proof. The later toolkit's publication/version labels
are not executable provenance. manual-locators.json pins exact PDF/source hashes;
font/descriptor/AFC tables were visually checked with the PDF skill, including
unsigned sentinel interpretation and the signed italic field.

## Body grammar and native flag policy

Proposed body tokens are printable ASCII20–7E and up to two sequential matched,
nonnested Bold On C3 0C C3 / Bold Off C4 0C C4 pair. Every token boundary is
complete; unknown/opaque/nested/formatter functions, controls, C0 and unmatched,
crossing or above-bound attribute structures refuse semantic writes. Original WP
character identity is never replaced by a Unicode/display-glyph identity.
Input65536 bytes,16384 body tokens and8 inspector index blocks are predeclared
research safety bounds, not DOS limits; mutation admission requires2 blocks.
Truncation, overflow, malformed references, token/prefix limits and unsupported
variants fail before any candidate output is declared accepted.

No-edit export is always the exact original owned image. Navigation, projection,
preview/cancel and a source-preserving refusal cannot justify rewriting unrelated
metadata. The proposed body-changing serializer may only preserve the prefix
except the documented packet6 bit3 (must-format), and must address that field by
indexed packet ownership. It may not recalculate hashes/counters, clear other
flags or relocate packet data. The original also sets bit3 on some body-preserving
operations (calibrated Block No followed by F1 cleanup); those raw differences
remain observations, not a global flag algorithm or an exemption from FC002.
The final evidence table must distinguish original cache behavior, compatibility
no-edit preservation and any independently approved edit flag policy.

## Read-only acceptance and original reformatting boundary

Approved WP22 and WP13 observations show source prefix324 becoming564 after
Retrieve/SaveAs. The new prefix contains deleted FFFF records and relocated live
packets. Post-print original reuse can leave index-unowned/slack regions as well.
These are not silently called corruption: actual wp51.Parse classification is
recorded separately and accepted images must export exactly. Even a read-only
accepted original output is refused by the first mutation gate when deleted,
aliased or unexplained prefix ownership remains. Original reformatting is never
normalized to force a whole-file match, and324 is never hard-coded as universal.
If the actual reader refuses a required original result, the handoff must name
that precise separate reader prerequisite; WP23 cannot edit its implementation.

## Original commands and interoperability prerequisite

The accepted run/subcase ledger will bind exact canonical titles/features,
source snapshot, incoming token gap, view/mode, prompt/result, native intermediates,
full raw print bytes and two fresh recipe identities. Position inches/cells alone
do not identify a code gap. Code-path setup, raw native code boundaries, actual
Reveal selection and subsequent edit witnesses must corroborate it.

History recipes each start on their OWN fresh master. Clearing a document or
retrieving a file is never assumed to reset deletion history. No-history/fewer
entries, navigation/save grouping, restoration consumption/order, repaired and
refused deletion effects are distinct observations. The older three-entry and
eviction witnesses remain their actual character-Delete/Right sequence, never
an invented word-delete command. Block No retains Block on; its subsequent F1
cleanup is a separate observed command before whole-document saving. No erased
selection or history reset may be inserted to make expected results pass.

candidate-protocol.json freezes the consumer CLI/JSON boundary. Every candidate
must be lawful, bounded, hashed and copied before original launch. Verification
requires original Retrieve, a declared subsequent edit, full selected-profile
print-to-disk with job completion, fresh Save, captured final DOS exit, stopped-
image extraction and actual Go-reader reopen classification. Merely reopening,
passing a parser or matching a screen is insufficient. Every native byte change
is classified by indexed field/relationship or stays explicitly unresolved.
There is no proprietary redistribution or new-document creation/product writer.

## Qualification2: required repaired-deletion Restore

The current policy admits **at most two sequential, nonnested matched Bold pairs**,
including the literal empty first pair. This is an initial implementation and
qualification bound, **not an original file-format limit**. Higher counts remain
an explicit full M1 obligation. A prospective operation exceeding this bound must
refuse before changing document bytes, cursor/history state or publication state;
never collapse the empty pair to make the output fit.

Both isolated repair-Restore repetitions retain the exact body
`41c30cc3c40cc4c30cc3584243c40cc444` after the no-navigation X witness:
A / On / Off / On / XBC / Off / D. Restore inserted Off+On, retained the
empty first pair, and left gap4 before X; the marker then leaves gap5. The
unsaved pre-marker body is a corroborated inference from the exported unique-X
native and exact raw pre-X code-pane highlight, not a separately exported file.
`two-pair-qualification.json` pins both source/final images and their literal
prefix comparison: the body start and all index/resource fields stay identical;
only the indexed packet6 flag changes0→8.

Source-backed format facts are the documented fixed C3/C4 token widths/selector,
complete prefix-field inventory, prefix-local pool/AFC relationships, absent
body-length/pair-count fields, and zero graphics. The bounded inference is that
this exact resource/prefix schema gains no new body reference merely because a
second identical attribute pair appears. This field argument is separate from
semantic permission: it does not qualify general higher-pair command behavior,
additional attributes, nesting, graphics, resources or native variants.

## Completed local evidence and refusal boundary

`verification.json` binds19 fresh pairs/38 accepted original runs and140 local
case instances. Its666-file actual-reader classification includes648 selected
native artifact paths,16 pilot native files and2 separately extracted diagnostic
sources; duplicate content and candidate input copies count as artifact paths,
not independent documents. Accepted runs contain118 complete raw print streams.
Five calibrations and two incomplete normal-delete attempts remain excluded.
Original process `result: observed` is distinct from accepted semantic evidence.

Normal code-question No/F1/Escape closes that question and preserves the Bold
body in all four tested contexts. The actual post-answer Reveal highlight is
after the target code for forward Delete (g1→g2, g4→g5), and before the code for
Backspace (g2→g1, g5→g4). Block No/F1/Escape instead retains the active block;
its separate F1 cleanup remains part of that accepted trace. No context-wide
cancel/no-op rule follows. Normal X operation gaps are bound to independent
exact-source X/Y continuations without an intervening save, pane change or
navigation, not to Pos inches. Plain post-delete gaps use the complete exact
ASCII native/VGA row plus hardware cursor; code-bearing gaps use native labels
and the raw code-pane highlight.

Consecutive character Deletes a,b group as ab. Saving between them produces
separate b,a entries; Right between deletions produces separate c,a in the tested
abc fixture. Restore retains entries in the tested immediate and save-interleaved
repetition paths. Repaired blocked deletion remembers the actual Off+On fragment;
refused blocked deletion leaves no history entry in its fresh recipe after the
separately observed block cleanup. These statements are limited to the exact
recipes, not reverse deletion, arbitrary interleavings or persistent undo.
The approved old043/211 recipes remain repeated character Deletes separated by
Right, never a word-delete command. Their exact preview/eviction behavior and
045 versus204 restored fragments remain pinned in `reused-evidence.json`.

Research admission exceptions carry explicit categories in
`refusal-contract.json`; they are distinct from actual Go `wp51.Failure`.
Read-only diagnostics may retain an opaque/unqualified body without decoding
inner lookalikes. Actual Go acceptance/exact Export, diagnostic prefix inspection
and strict mutation admission are separate results. Deleted/FastSave extents,
aliases and index-unowned residue are refused for mutation even when actual Go
accepts them losslessly. Output residue in these original interoperability runs
is byte-identical at the same source offset; changed unowned bytes fail the
relationship verifier. Literal deleted extents are not decoded as controls.

The final grammar qualification and offline audit were applied after VM release.
The actual C CLI smoke versions remain archived with their original one-pair
preflight policy; their plain-ASCII input qualifies identically under policy2.
The two-pair original Retrieve/edit/print/Save chain is independently captured
in the B repair-Restore repetitions. No final-source VM rerun, Go-emitted
candidate or complete Wordling comparison is claimed. Future Go outputs must
execute the documented candidate CLI against their own lawful scratch files.
