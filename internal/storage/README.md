# Bounded no-edit local storage contract (WP03)

This package implements T007–T009, tracing FR-006, NFR-001/002, C-002,
FC-002/004/009 and Story 1 scenarios 1/4 to a bounded filesystem foundation.
It consumes the approved `internal/wp51` image; it does not duplicate a codec.
This is a bounded Linux local-filesystem API, not full F10,
overwrite, backup, locking, Fast Save or file-management compatibility.

## API and identities

`OpenDirectory(path)` pins the directory actually opened using `os.Root` plus a pinned directory descriptor.
`Directory.Read(name)` acquires a regular file without following its final
symlink, reads at most the WP02 limit+1 bytes, and calls `wp51.Parse`.
`Document.Export()` returns fresh exact snapshot bytes. Read captures device/
inode, size, mode, mtime, ctime and SHA-256; checks before/after reading plus a
final rooted lookup refuse observed source replacement or modification.
`Directory.Observe(name)` captures an explicit existing or absent destination.
`Directory.Save(document, destination, decision)` requires that bound destination;
it never interprets a free-form destination at publication time.

Names must be a single nonempty basename of at most 255 bytes (a conservative
Linux policy, not an original DOS filename rule): no slash, NUL, dot, dot-dot, absolute
path or reserved `.wordling-candidate-` prefix. Leaf symlinks and nonregular
files are refused; Linux `openat` with no-follow/nonblocking flags on a
RawConn-pinned directory descriptor avoids symlink/FIFO opens and concurrent
descriptor-close/reuse races. `os.Root.OpenFile` itself follows in-root symlinks
even when passed O_NOFOLLOW, so it is not used for leaf opens.
A pinned directory is the authority, not its original pathname: renaming that
directory or replacing the original path with a symlink does not redirect any
operation. The constructor chooses the actual directory reached at open time;
it does not certify an untrusted path's provenance or ownership. Nested paths,
network filesystem semantics, mount races and hostile filesystem implementations
are outside this validated local scope. The API does not identify network
filesystems automatically; callers must choose a validated local filesystem.

## Supported save cases

- Observed absent destination: create an exclusive random 0600 candidate in the
  pinned directory (permissions may be narrowed by umask), write the complete
  exact exported snapshot, check short writes/errors and close its writer, then verify its
  inode and bytes. Revalidate source freshness and destination absence. Publish
  with `os.Root.Link(candidate, destination)`, which atomically refuses any
  existing destination entry, including a raced symlink. No overwrite-capable
  rename is used. Check the published inode and exact bytes before success;
  remove the temporary candidate entry after successful verification and verify
  again afterward (unlinking the extra hard link changes ctime).
- Observed existing destination: `AllowOverwrite` must be supplied explicitly.
  If it is still the same file as the source snapshot and passes fresh identity/
  hash checks, return `Unchanged` without a candidate, write, unlink or rename.
  Any actual replacement of an existing file is `UnsupportedReplacement`, even
  with permission or identical bytes in a different inode. The API has no
  caller-asserted exclusivity option that pretends to supply atomic replacement.
- A changed observation or changed source is refused. Publication/link failures,
  short writes, write/close failures and cleanup failures are typed and never
  reported as a successful complete save. Original source/existing destination
  files are never opened for writing, truncated, renamed or unlinked.

## Races, linearization and uncertain outcomes

Atomic no-replace link is the new-name publication point. Source freshness is a
separate immediately preceding validation observation; validation and publication
across different files are not an atomic transaction. No-edit Save publishes exactly
the loaded snapshot, not a promise that an independent writer cannot modify the
source after its final check. The same-file no-op's observation point is its
final successful identity/hash check. No guarantee extends to subsequent external
writes, renames or deletions.

Candidate names belong to this operation's temporary namespace; they are not
original document names or required sidecars. A read-only candidate descriptor stays open through publication and cleanup to
prevent inode reuse after the writer closes. Candidate identity/bytes are checked
before and after linking. A same-user actor could still swap a candidate between
check and link, or modify a published file during/after verification. The package
does not claim an atomic compare-and-swap or hostile-directory security guarantee.
If post-link verification fails, return `PublicationUncertain` with
`DestinationMayExist=true`; never announce success and never try to roll back by
unlinking a destination that may now belong to another writer. A link error also
may leave a destination: callers must inspect/refetch after ambiguous outcomes.
Existing destinations cannot be overwritten by this publication primitive.

Cleanup only addresses the operation's random candidate name, checks its inode,
and leaves an observed substituted candidate untouched. Check/unlink is not a
conditional atomic deletion against arbitrary same-user candidate-name attacks;
such interference is outside cleanup's ownership contract. Cleanup errors and
leftover candidate names are exposed. A crash/interruption may leave a candidate
or a published destination; startup recovery/garbage collection is future work.
No fsync, power-loss durability, original DOS backup/locking, metadata/xattr/ACL
preservation, remote filesystem, semantic edit or new native writer claim is made.
Actual overwrite/backup/Fast Save and unsupported paths remain M1 follow-up under
WP06/WP12; these refusals do not remove original parity obligations.

## Verification

Tests must pin original fixture bytes/length/SHA, typed malformed/oversize/native
refusals, source/destination identities, explicit overwrite decisions, same-file
no-op behavior and unsupported replacement. Inject candidate create/short-write/
write/close and actual link-publication failures using real temporary files.
Exercise real symlink/FIFO/source/destination/candidate substitutions and parent
path replacement at controlled boundaries, including candidate substitution
between its check and link and foreign destination replacement after link.
Assert no false success, exact successful snapshot bytes, original-file integrity
and explicit uncertain/residue reporting. Ordinary rename is deliberately absent;
publication/link failure is the exercised failure boundary, not a claimed rename
path. Run gofmt, build, all tests, race tests, vet and both catalogue checks;
retain genuine validation/JUnit evidence before independent review.

## Source-bound edited candidates (WP24)

T070–T072 extend the same transaction for an independently supplied native
candidate. This is byte publication, not a semantic writer or an assertion that
an edit is safe. The document layer must establish FC-003/004 edit authority.

```go
id := storage.PublicationID{Operation: 7, Revision: 3}
request, err := directory.PreparePublication(source, absentTarget, candidateBytes, id)
// Handle err before dispatch. Carry id with any asynchronous result.
outcome, err := directory.Publish(request, id)
```

`PublicationID` contains nonzero `Operation` and `Revision` uint64 values.
The caller assigns IDs and maintains current/revised/cancelled session state;
storage does not enforce global uniqueness, monotonicity or cancellation.
`Publish` requires the exact prepared ID. A mismatched operation/revision or
another Directory instance is refused before publication IO. An old ID that
still matches its request cannot prove the UI's current revision was saved:
the session must route results by ID and retain newer dirty state.

`PreparePublication` accepts a loaded `*Document`, an observed absent
`*Destination`, candidate bytes and ID. Both objects must originate from that
same Directory instance. It delegates framing to actual `wp51.Parse`, which
copies the complete image, preserves opaque data and enforces its16MiB policy.
It records independent candidate length/SHA and revalidates the loaded source
and destination observation. Callers must not mutate input during preparation;
after return they may reuse it independently. `ID()`, `Size()` and `SHA256()`
return copied metadata. Nil/zero/unbound objects and IDs, oversized/malformed
data, stale sources and changed observations fail without creating a candidate.
Native parser errors remain wrapped as causes; framing never grants edit safety.

`Publish` revalidates the original source/destination before invoking the same
publisher used by no-edit `Save`. That common publisher keeps two distinct
authorities: the original loaded identity/hash for source freshness, and the
immutable candidate bytes/hash for all candidate/post-link/post-cleanup checks.
It does not synthesize a different source Document or duplicate the transaction.
Source revalidation immediately before the link remains separate from the link's
atomic no-replace point; neither observation promises later source freshness.

Edited candidates always require a new name. Existing destinations, including
the source inode or an identical candidate, are `UnsupportedReplacement` at
preparation. A destination appearing after preparation is a changed observation
or a no-replace link failure. Replaying an already published request therefore
does not overwrite the first result. The existing `Save` decision API and
verified same-file no-edit no-op retain their original behavior.

All descriptor/no-follow/inode-pin, interference, cleanup-residue and uncertain
side-effect limits above apply unchanged. `Outcome.Identity` describes the
published candidate, not the original source; an error is never complete success.
The caller carries its request ID with both success and failure messages.
Actual replacement, backup/Fast Save, recovery, fsync/durability, network
semantics and full F10/native-edit interoperability remain separate M1 work.
No reference VM or semantic writer is used to validate this IO-only component.

WP24 external-API assertions use explicitly synthetic framing-valid payloads
different from their original source. Real-file fault tests cover write/close/
link, late source/destination/candidate changes, substituted destinations after
link/cleanup, pinned parent renames and concurrent Close/publication. Original
WP03 no-edit and fault tests continue to exercise the same common publisher.
Evidence is separate under `evidence/wp24/`; earlier WP03 results are retained.


## WP34 read-only macro snapshots

ReadMacro(name) returns a separate immutable Macro with Image/Export/Identity/Name/
DirectoryID. Image is the approved internal/macro/wpm immutable codec, not a DOC
image or editable buffer. The wrapper uses the same validName/readStable path,
pinned directory, no-follow regular-file open, limit+1 read cap and source stamp/
hash consistency checks as Read. No second filesystem engine or generic transaction
was introduced. Both inherited acquisition and publication code are unchanged.

Storage NativeRefused wraps a typed wpm.Failure for malformed/unsupported input;
read/path/stale/size/close failures retain existing storage kinds and causes. Bounded
opaque WPM content is admitted losslessly with its codec execution-blocking findings
intact. Empty findings are framing evidence, not macro execution permission. Release
evidence remains unknown-from-bytes. All names follow the existing local flat-name
policy; no DOS path search or arbitrary host path mapping is introduced.

Identity is the observation at acquisition, not a lock, future freshness guarantee
or editor operation/revision. Export and all codec views are independent copies;
Image returns a separate codec value wrapper over immutable private backing; whole-
value assignment through that pointer affects only the caller's wrapper. Repeated
Image calls return independent wrappers. Construct Macro only through ReadMacro;
its zero value is not an acquired snapshot. Macro has no Save/Publish operation and
cannot replace a Document in existing APIs. Read still refuses WPM; ReadMacro refuses
DOC; PreparePublication remains DOC-specific and refuses WPM candidate bytes.

The queued actual production consumers are WP36 editor loading/nested resolution and
WP37 executable integration, which must supply real run/target/revision/late-result
identity and ordinary command behavior. Reading a macro is not executing it. Full
macro recording/editing/conversion/WPM writing, merge language, non-ASCII/resources,
physical qualification and all38 obligations/91 groups/nested leaves remain open.
PDF remains M2 after accepted M1. No VM or CMD51-199 disk/editor roundtrip was run.

Local external tests cover all46 pinned original WPM exports/22 distinct hashes,
source identity/copy isolation, codec-versus-storage failures, DOC/publication
refusals, pinned-root rename, actual symlink/FIFO/nonregular/size cases, and concurrent
reads. Internal fault tests exercise the real shared acquisition seams for read/stat/
close/lookup failures, actual post-open modification/replacement/symlink swaps and
a growing reader capped at limit+1. Fuzzing targets only the changed basename/read
boundary; WP33's unchanged binary parser is not reimplemented or requalified here.
Evidence and committed Git-blob seals are in evidence/macro-read/. Component review
remains independent; no whole FR-012 or M1 acceptance is claimed.

WP34 cycle2 tests additionally replace returned image wrappers with zero and with
a different approved original image, including earlier and repeated accessor views.
Only the caller's wrapper changes; acquired bytes/hash/source identity stay bound.
The exact independent reviewer reproducer and fresh seven-check/race evidence are
retained separately in evidence/macro-read/cycle-2/; earlier raw results are intact.

## WP41 prepared capture and source-less publication

WP41 replaces public-wrapper authority with a stable private opened capability.
Document/Destination/Macro acquisitions retain that capability; prepared sourced
requests independently capture the original source name/full identity/image and
exact destination observation. Between calls, assigning zero/other values to the
original source or destination wrapper cannot rewrite the accepted request.
Source freshness is still checked at prepare, Publish and pre-link. A source
change matters even after a public wrapper is replaced with another valid read.

Directory values alias the same actual opened resource lifetime. A legitimate
copy can publish a request prepared on that capability. A rebound receiver,
including a separate OpenDirectory of the same physical root/FileID, is refused
before filesystem IO; path/FileID/public wrapper address is not authorization.
Nil/zero/closed receivers refuse safely. Close acts on the capability currently
designated by that wrapper; a retained original copy can close the original after
another wrapper is rebound. Close releases the real root and pinned descriptor,
retains real errors, and does not promise repeated idempotent success. There are
no per-request duplicated/reopened handles or reference-count subsystem. Callers
must retain ownership needed to Close a capability before discarding/rebinding
its last Directory wrapper. Concurrent wrapper mutation during a synchronous call
remains outside the contract; concurrent Close uses the existing safe OS handles.

PrepareNewPublication(target,data,id) returns a distinct private NewPublication
with copied ID/Size/SHA256 inspection. It requires a bound observed-absent target,
nonzero operation/revision, bounded input and actual wp51.Parse DOC framing; WPM,
malformed input and existing targets refuse. Parse owns caller data after return.
NewPublication captures the same stable capability/destination observation.
PublishNew checks that exact receiver/correlation before IO and uses the ONE common
no-replace transaction with an explicit source-less guard kind. Unknown/zero guards
refuse. Existing PreparePublication/Publish still require a real acquired source;
nil is never an overload. Save retains cross-directory no-edit publication and
same-source no-op. All candidate/pin/verification/destination/cleanup/uncertainty
behavior above remains; no existing-file replacement or durability is introduced.

This type proves framing/transaction admission, not native genesis, semantic edit
permission or caller birth lineage. Future F/G editor/executable consumers must
route only genuinely never-sourced New buffers through it, acquire/verify the
first real anchor after publication, and retain original guards thereafter.
Actual existing WP17 editor/WP18 TUI tests and races pass in an isolated immutable
pinned-source /tmp composition against this storage; no reverse dependency or
consumer merge exists in lane-b. NewPublication has no live product route yet.
All38 obligations/91 groups/36 lessons/nested leaves remain M1; no full command/FR,
acceptance/merge, constructor, original VM result or PDF/M2 work is claimed.

Evidence under evidence/wp41/ preserves unchanged70e02f7 baseline and three actual
red independent alias assertions, permanent green source/target/root/Close tests,
real fault seams and exact bytes/identities, configured checks/race/resources,
12 finite mutants and bounded60s API fuzz. Earlier WP03/24/34 evidence remains
historical and unchanged. Prior paragraphs' unchanged-code statements describe
those original packages; WP41's scoped capability/capture changes are explicit.
