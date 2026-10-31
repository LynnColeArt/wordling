# WP41 captured publication and source-less transaction

The inherited storage Go tree was byte-identical to approved70e02f7 before edits.
Baseline unit tests passed; the sealed independent public overlay then reproduced
all three real P2 assertions under race instrumentation (exit1, no data race).
Actual baseline/red source bindings, commands and output are retained unchanged.
Promoted e1e4c2c design/ADR/revision3 hashes and independent78bc706 READY analysis
are pinned: historical awaiting-review wording is retained, not silently edited.
READY was planning authority, not a claim that these source failures were fixed.

## Implemented boundary

Directory is a wrapper over one private opened capability: rooted handles, private
filesystem seam, acquired identity and an atomic closed marker. Legitimate value
copies alias that exact resource lifetime. Document/Destination/Macro acquisitions
retain the private capability, not a public reassignable Directory pointer.
Publication captures accepted source name/full identity/immutable image and exact
target observation in private wrapper copies. Publish captures request state once
and compares its receiver capability before filesystem IO. Zero/nil/closed/rebound
receivers, including an independently opened equal physical root, refuse. Copied
same-capability receivers work. Sequential caller wrapper replacement cannot rewrite
accepted referents. Concurrent wrapper mutation during an API call stays excluded.

Close acts on the capability currently designated, releases the actual root and
pinned directory descriptor, and preserves real errors. An original retained copy
can close the original after another wrapper is rebound. Closed aliases cannot
resurrect the acquisition. No request duplicates/reopens a handle, silently transfers
ownership, introduces reference counting or promises idempotent-success Close.
Callers retain the capability ownership needed to Close before discarding wrappers.

PrepareNewPublication/PublishNew and private NewPublication provide distinct
source-less absent-target admission, copied ID/Size/SHA inspection and independently
owned wp51.Parse payload. WPM/invalid framing/bounds/IDs/handles/existing or changed
targets refuse. Existing APIs still require a real source; nil-source overloads and
dummy acquired Documents were not introduced. New and sourced requests enter ONE
private transaction with explicit nonzero guard kind; zero/unknown guards refuse
before candidate creation. Sourced prepare/Publish/pre-link checks remain three
actual source observations; source-less operation never opens a fabricated source.
Save retains its cross-directory source guard and verified same-file no-op.

The existing candidate exclusive create/pin, bounded write/close, inode/hash/full-
byte verification, destination rechecks, no-replace Link, post-link verification,
owned cleanup, final verification and pin-close reporting are shared. Failed or
uncertain outcomes stay non-success and retain conservative DestinationMayExist/
Candidate meaning; no destination is unlinked as rollback, no silent retry, actual
replacement/backup/fsync/durability/global cancellation or new file format is added.

## Exact effects and regressions

Permanent public tests retain the three independent repros plus source-wrapper
zero/same/cross-root substitutions with changed and unchanged original sources;
target zero/other absent/existing/foreign substitutions plus late first creation;
receiver zero/other/equal-root capability replacement with the hardlink created
BEFORE fresh Read. Physical outputs, original/substituted bytes, lengths/identities
and candidate absence/residue are asserted. Private actual filesystem hooks prove
rebound/zero/closed receiver refusal performs zero open/stat/link/remove calls.
Same-capability copies, pinned root rename, Close through copied/rebound aliases,
real closed-root/FD state, repeat Close errors and source observation counts pass.

NewPublication tests start with empty temporary roots and no acquired Document.
Caller buffers can change after preparation without changing payload inspections
or actual publication. A separate real Read matches the final positive receipt;
that is component evidence for a possible future anchor, not editor binding logic.
Concurrent no-replace requests have exactly one complete winner with exact bytes.
Actual late targets, writer/stat/pin/open/read/close faults, candidate substitution,
link errors including effects, cleanup residue and foreign post-link/final states
exercise the same transaction. The declared16MiB framing limit is admitted exactly;
original malformed/WPM/native/storage failures, all sourced guards, old no-edit
cross-directory/no-op tests and34 immutable Macro.Image tests remain passing.

## Actual downstream and measured verification

An isolated /tmp composition exports immutable approved17 b479983 and18 72369db
Go source, their actual raw fixture witnesses and e1e4c2c planning fixtures, then
substitutes only current storage plus approved inherited WPM codec dependency.
Pinned editor/TUI test suites and their race runs pass; all consumer Go bytes and
current production hashes are checked against their declared Git/source bindings.
The existing cmd/wordling builds there with retained binary hash, but was not run
as a new product scenario. No consumer source was merged into lane-b and no reverse
runtime/lane dependency was added. Actual NewPublication product consumers F/G
remain future; no live New route, constructor/genesis or semantic safety is claimed.

The first temporary composition omitted consumer-owned session1 fixtures by taking
only planning data; its missing-fixture failures are retained. The repair exported
those exact immutable72369db fixtures rather than fabricating witnesses. The first
mutation harness similarly omitted the inherited WPM testdata JSON; that baseline
failure is retained and no mutant counted until its exact fixture was copied.

The final frozen checkout passes genuine configured7/7 checks (inventory/scenarios/
adapter/discovery/build/test/vet),0 failures/errors/skips, composed-lane race and238
storage test/subtest events. Twelve finite mutants fail actual assertions: borrowed
source/loaded/new targets, rebound acceptance, lost Close lifetime/closed receiver,
missing source boundaries, zero guard admission, wrong IDs/size category and hidden
pin-close errors. Mutation work is confined to a temporary copied module.

On declared AMD Ryzen5 5600X/Linux/Go1.26.4, actual PrepareNewPublication measured
2964ns/op,2100B/op,19allocs; real-filesystem observe/prepare/publish measured
118920ns/op,9098B/op,84allocs. The timed test/benchmark process peaked at90716KiB
RSS/1.88s wall time, including Go/process work; these are measured cases, not a
universal memory/durability bound. Resource tests admit exact16MiB input and verify
actual descriptor lifetime. New code adds no binary interpreter: native framing
is delegated to unchanged approved wp51; WPM decoding/wrapper behavior is retained.
A declared60s two-worker API-boundary fuzz with max4096-byte payloads and real
pinned scratch roots passed491601 executions (whole driver exit0). It tests owned
payload/target/zero-receiver and typed admission outcomes, not whole-parser or
original-app semantics. All frozen source/test/module/codec hashes remain unchanged.

## Retained work and ownership

Only internal/storage/** changed. Git-blob seals bind current source/evidence;
old WP03/24/34 logs and manifests retain their historical commits. All38 obligations,
91 groups,36 lessons and nested leaves remain M1. Native genesis/constructor,
New/Loaded lineage, first anchor/routing, full F10/overwrite/backup/recovery,
non-US/resources/physical/historical qualifications and full FR/M1 acceptance stay
open. No guest, proprietary program/manual redistribution/decompilation, acceptance,
merge, self-review or M2/PDF action was performed. Independent review and the root's
quiet point govern subsequent canonical lifecycle.

Packaging correction: the first current-file seal enumeration accidentally included
an ignored inherited WP24 Python cache bytecode file. The post-commit actual-Git
audit rejected that path because it was not in the commit. The manifest now uses
Git-tracked files only; source/tests/raw logs remain unchanged. The shared-lane git
guard warned ACTIVE_WP_CONTEXT_AMBIGUOUS against its old local WP03 projection but
allowed the source commit; canonical primary claim/lifecycle authority remains
with the root coordinator, and no metadata bypass/manual repair was performed.
