# WP25 independent review, cycle1

Reviewer codex/reviewer-renata, independent of implementation author; previously
reviewed the WP23 prerequisite. Fixed source83ef17d40a97cf236e49816e2873a6cea0de9680,
private-state correction536e3b3f29dfb0deb9ad2c8366ab6e9b4aedd9ad and historical
producer14d8f21d38b42a38bdc61bd1e2af7dd263b20bf2. Actual runtime lane-e, prompt
49bb873a48f04e798dde0ec0c80a9211. Recommendation: approve the bounded component
writer. No actionable finding. No filesystem/editor/UI or complete M1 acceptance.

## Source and native contract review

Applied reviewer profile/governance and unchanged charter/compatibility/roadmap.
Read the full runtime WP, actual approved WP23 contract/ADR/field ledger and review,
WP15 model/API, source, tests and both historical/final evidence. Approved23
contract, ledger, two-pair qualification and ADR match eb86058 Git bytes exactly.
The complete native reader remains byte-identical to approved e7de080.

Actual admission consumes the approved reader's packet/index spans, checks exact
header/native framing through that reader, two index blocks, all checked index
slots/order/next links, complete nonoverlapping prefix ownership, required resource
field values and source-local font/AFC references. Independently parsed Go resource
constants: all64 packet fields match their rows in the72-field approved ledger;
the remaining8 header fields are delegated to the unchanged reader. Only literal
flag0/8 and descriptor-match hash e724/1172 variants are admitted; their unrelated
bytes/counters are preserved, not recomputed. Packet6 is addressed through its
checked indexed span, including physically reordered-packet safety tests.

The writer copies its owned input prefix/body around complete token-gap edits.
Only indexed packet6 must-format bit3 may be set on a real body change. It does
not rebuild a prefix template, normalize caches, introduce a container/sidecar,
relocate opaque references or convert through another word processor. It reparses
and readmits each new candidate before publication as a revision. Broad immutable
Parse/Export remains available independently of narrower mutation permission.

Safety limits65536 bytes/16384 tokens/two sequential nonnested matched Bold pairs
are initial qualification policies, not DOS format limits. Empty On-Off-On remains
literal. Unsupported resource/prefix/body/character/nested/formatter/third-pair
and excessive inputs fail without partial result mutation. No new Bold creation,
Delete/Undelete, hard returns, new-document construction or filesystem IO is added.
Typeover repeatedly replaces ASCII, inserts before a code and appends at EOF;
full text is validated and resource/result budgets checked before any candidate.
Same-byte typeover moves its cursor without inventing native metadata dirtiness;
Changed is documented native-byte change, not a blanket session-dirty rule.

## Immutable revision ownership

The previous wrapper-rebinding defect is corrected structurally. Document is a
mutable public handle around private immutable revisionState; Cursor and Revision
capture that state, not the replaceable handle. Images/gaps/original image pointers
are not exposed. Equal byte reparses get distinct identity; copied handles of the
same state retain identity. The new state is completed before it is returned,
retains the initially loaded OriginalExport and does not mutate any prior state.

Fresh existing regressions cover qualified same-length/shorter/zero/repeated/
independent/result-wrapper replacements, original old Offset/Present, true revision
mismatch, invalid inputs and copied/exported buffers. Added independent race-enabled
public-API overlay test repeatedly zeroes/replaces a returned result handle,
reparses equal bytes, rejects the old cursor on that different revision, restores
an actual copied state and edits it, then verifies the old cursor/view/offset and
initial original remain bound. It passes against unchanged actual source; no unsafe
or reflection access, source edit or panic tolerance masks the result.

## Original interoperability and final-source equality join

Independently re-executed the actual final audit and all12 original comparisons,
redirecting only its two known derived output writes to /tmp. Actual input paths,
approved helper semantics and Go temporary reader location remain unchanged.
All10 Go candidate verdicts reproduce accepted; the two original Q controls
reproduce their explicitly expected old-X-print mismatch and every other required
protocol check. Those controls are observations, never relabelled candidate passes.
All52 new native artifact paths reopen/export byte-exact through actual Document
APIs. Twelve clean inputs admit mutation;40 original post-save variants stay
read-only and refuse mutation. Paths include duplicate contents, not52 independent
documents. Existing666-file303/363 mutation admission split also passes real tests.

The actual five candidate kinds are ASCII modes, Bold insertion g1, typeover g2,
typeover g5 and real two-pair X→Q typeover g4. Historical native inputs were produced
by committed public Go APIs, not an original-authored surrogate. Original runs use
fresh private masters, readonly seed, shared primary lock, immutable input/source,
selected resources, actual Retrieve/subsequent Z edit/complete raw print/Save,
exact final postwait DOS/cursor, stopped extraction and actual reader reopen.
No unexplained bytes are normalized; saved prefix/FastSave/cache changes remain
literal and separately mutation-refused.

Independent temporal/control audit confirms both original Q controls finish
before first Go Q candidate start; scheduler seals their exact165-byte equal Q+Z
streams before invoking that pair. Both actual candidate inputs/archive expectations
bind SHA479a7f6fca1e5a7eef7f3add9e9ecea1d8ddd9ec2ba7850e80391a699c30a117.
Their captured code highlights establish original gap4→5 and literal empty pair.

Final correction does not fabricate a final-source guest rerun. Verified bridge
SHA0fdb9309ad006b1ed50fa24aad554ef6a611675ddd1d9c3d3584c74525c0b2f1 joins
historical source hashes to14d8f21 Git bytes, final hashes to current source, and
five final candidate bytes to actual original-tested inputs. Independently copied
byte-identical final production/producer source into a temporary module, invoked
the real producer there, and obtained all five candidates byte/SHA-identical to
historical tested inputs and final fixed copies. This is a real final serializer
call/equality proof; it claims no guest execution of the corrected Go source.
Temporary-copy source hashes and exact invocation/results are retained in review.

Initial audit-output routing attempts used temporary input paths and therefore
hit Go internal-import/path-equality guards. Corrected reviewer routing changes
only known output destinations. Those were reviewer harness corrections, not
source defects or altered original verdicts. No tracked derived log was rewritten.

## Independently executed verification and evidence integrity

- Fresh real go build ./..., go test -count=1 ./..., go vet ./... and composed
  go test -race -count=1 ./... pass. Evidence producer/measure/reopen are genuine
  clients; no-filesystem library approval is not substituted for future app calls.
- Configured runner emits genuine7 passing JUnit cases,0 failures/errors/skips;
  formatting and owned-diff whitespace checks pass.
- Exact actual Git object audit:2848 raw paths+10 historical/final candidate paths,
 459 unique objects,332917673 manifest bytes, all size/SHA256 equal. Actual source/
  private engine/scheduler/candidate/input/stream/final-state provenance joins pass.
- Final source's21 top-level tests cover actual originals/32 boundary outcomes,
  admission bits/slots/relationships, indexed relocation, immutable exports,
  same-byte/cross-revision/unsafe rejection and the private-state regression.
- Retained final60s/120s two-worker fuzz passes report4,317,541 and8,546,210 executions.
  The correction's repeated budgets were predeclared for the real wrapper defect,
  not arbitrary broadening; original passing logs remain separately historical.
  Six compiling overlay faults are killed by assertions. Inspected source/seed/
  budget/log bindings; no redundant180-second fuzz run or guest by reviewer.
- Measurement evidence separates admitted max-shape cost from broad readonly
  metadata refusal. Final source records19128 B/op admission,187144 B/op changed
  typeover and786485 B/op broad metadata refusal, with bounded inherited Inspect
  clones. These are host cumulative allocation observations, not peak-live/RSS
  caps, product SLOs or original DOS capacity. Older measurements/logs stay intact.

## Contract/anti-pattern checklist and retained scope

Native-framing/editing/approved23 contracts are directly in scope; complete header,
field, token, copy, revision, literal candidate and original verification examples
are exercised. Session/storage/language/layout resource boundaries remain consumed
unchanged; automation/structured/coverage contracts gain no support here. Historical
EC047 missing native proof is now supplied by exact bounded originals, not by an
invented generic code rule. No current canonical registry or conformance closure.

Real public Document APIs are called by tests, final producer and original-output
reopen clients. This is explicitly staged component delivery; future27/28 actual
editor/app integration remains NOT RUN. Tests assert actual source/native behavior,
not a detached duplicate model. No silent success or partial native candidate on
refusal, frozen reader/previous raw evidence preserved, locked native/rights rules
retained, narrow document ownership only, no overlapping owner edits. Exactly one
independent verdict follows; reviewer made no implementation repair.

All38 obligations/91 groups/discovered leaves remain full M1 scope. General native
variants, new documents, deletion/history/selection, original replacement/storage,
full layout/print/resources, nonASCII/locales, historical DOS/graphics/physical Linux
qualification and product integration remain open. Original after-Off cache flag0
versus independently authorized must-format8 is explained and actually original-
tested, not normalized. Approval of these exact library operations cannot close a
whole FR/NFR/FC/case/group or accept/merge M1; PDF remains M2 after true acceptance.
