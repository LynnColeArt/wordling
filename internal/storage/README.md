# Native local storage contracts

The final WP79 section defines the current everyday editing APIs. Earlier
sections preserve the legacy entrypoint contracts and their qualification limits.

## Legacy bounded no-edit storage (WP03)

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

## Everyday editing storage foundation (WP79)

T239–T243 add opt-in workspace and save APIs for EE-010/011/013. The earlier
sections describe the still-supported legacy `Save`, `PreparePublication`, and
`PrepareNewPublication` APIs: their absent-target restrictions remain deliberate
compatibility contracts for existing callers. They are no longer a claim that
this package cannot replace a file. New editor lifecycle code in WP82 must use
`PrepareSave`/`PublishSave` and `PrepareNewSave`/`PublishNewSave`; WP84 consumes
workspace listing/navigation/selection for F5 and Look. Those consumers and WP86
must prove normal executable reachability. Layer approval alone is not an
implemented user workflow or complete M1 parity.

### Linux workspace mapping

`OpenWorkspace(path)` pins the caller-selected local Linux directory as drive
`C:\`. `Root`, `Navigate`, `List`, `Listing.Select`, `EntrySelection.Read` and
`EntrySelection.Enter` separate observations from acquired authority. `Read`
returns the unchanged native snapshot for Look or Retrieve; it does not mutate
an editor buffer. A later Retrieve must revalidate/acquire again. `Directory()`
returns an alias of the selected pinned capability for read/observe/save, and
`Observe` resolves a single DOS filename to an existing host spelling or an
uppercase new name. Direct legacy Directory observations may retain lowercase
for new host names while sharing the same case-ambiguity checks. The workspace owns all navigation handles and their Close.

The deliberately explicit compatibility profile is:

- Direct ASCII 8.3 names, case-insensitive lookup and uppercase DOS display. No
  generated `~1` aliases, Unicode normalization or truncation. Braces in the
  original `WP{WP}US.SUP` and extensionless `SPELLADD` are supported. DOS device
  basenames, spaces and illegal DOS punctuation are refused.
- Two host names projecting to the same DOS name are ambiguous. Both remain
  visible as unsupported observations; acquisition/publication refuses them.
  Long/non-ASCII names and symlinks are likewise explicit unsupported rows in
  an unfiltered list, not fake original context-disabled commands or aliases.
- Only drive C is mapped. Backslash separates directories. Absolute C paths
  start at the pinned root; relative paths start at the current acquisition.
  Parent navigation follows acquired ancestry, never filesystem `..`, and
  refuses traversal above root. Forward slashes are not DOS path separators.
  A renamed directory remains the originally acquired location; its displayed
  DOS path is logical navigation ancestry, not a claim of current host pathname.
- Child acquisition checks no symlink, before/after inode/metadata and opened
  identity. Selected files are checked again for case ambiguity and full stamp;
  read adds content hashing/native validation. A stale row is not authority to
  silently read its replacement. Refresh the listing after a stale refusal.
- Wildcards apply independently to padded 8-character stem and 3-character
  extension: `?` consumes one character or padding, `*` consumes the remainder.
  `*` and `*.*` include extensionless files; a literal extensionless pattern
  matches extensionless names only. Directories remain available under filters.
  This is the declared Linux DOS-name projection, not an unobserved claim about
  every original DOS wildcard edge case. A listing sorts directories first,
  then canonical name and host spelling. The UI owns original column traversal,
  short/long presentation, selection position and name-search keyboard behavior.
- Metadata exposes host file byte size, mode and modification instant. Consumers
  render timestamps in their explicitly selected host timezone. `Entries` counts
  displayed rows including directories; `Unsupported` counts refused rows.
  `TotalBytes`, `FreeBytes` and `AvailableBytes` come from `fstatfs` on the pinned
  directory. These are labeled Linux filesystem figures, not DOS “Document
  size,” DOS drive allocation or the original fixed reference clock. WP78 proves
  document size and native disk bytes differ; no conversion is fabricated.
- Complete enumeration is limited to 16,384 entries, paths to 1,024 bytes,
  navigation depth to 64 and retained directory acquisitions to 256 per
  workspace. Exceeding a bound fails explicitly instead of returning a partial
  count or discarding an unvisited alias. Repeated visits reuse an unchanged
  pinned child. Close releases all retained capabilities; copies share lifetime.

The initial workspace path is an explicit host choice, with the same acquisition
trust boundary as OpenDirectory. This is not a general host filesystem browser,
a network filesystem compatibility claim or permission to follow arbitrary
mount/symlink escapes. Public wrappers cannot rebind previously prepared requests.

### Prepared edited saves and original document backups

```go
id := storage.PublicationID{Operation: 7, Revision: 3}
target, err := currentDirectory.Observe("LETTER.WP")
// Handle err; if target.Exists(), obtain the original explicit Replace Yes.
request, err := currentDirectory.Directory().PrepareSave(
    source, target, nativeBytes, storage.AllowOverwrite,
    storage.OriginalBackupOn, id)
// Handle err, then dispatch this exact request and id.
saved, err := currentDirectory.Directory().PublishSave(request, id)
// Only complete success admits saved.Document as the next acquired source.
```

`PrepareNewSave` is distinct and is permitted only for a genuinely never-sourced
New buffer. It may overwrite an explicitly approved destination, but must never
be used to bypass a retrieved document's source guard. `PrepareSave` accepts a
real acquired source from this or another pinned directory (Save As), an observed
target, native candidate, overwrite decision, backup setting and nonzero ID.
Candidate framing uses the existing lossless `wp51.Parse`; storage does not grant
semantic edit authority. Bytes and wrappers are captured. Original complete
native headers and opaque regions are never recreated or normalized here.

An observed existing target requires `AllowOverwrite`; original default No and
cancellation therefore prepare/publish nothing. Requests share a single-use
state even when their wrapper is copied. `Cancel()` succeeds only before publish
begins. A mismatched ID or receiver cannot consume a valid request. Once dispatch
starts, cancel returns false: the controller must account for the actual outcome
and must not attach a late save to a newer/different document merely because its
ID matched this request. Success returns the actual new `Document`, directory
identity and operation/revision for subsequent edits/saves. A failed request is
also consumed; retry requires fresh source and target observations. A successful
rollback conserves bytes but rename changes ctime, so retaining an old source
stamp is not a valid retry shortcut.

Original outcome rules are backed by WP78 `backup/` and `qualification/files/` observations:

| Destination and setting | Successful native document / original backup outcome |
| --- | --- |
| Absent, either setting | Exact candidate created; no original backup created or removed |
| Existing, enabled | Exact candidate replaces target; same-directory basename `.BK!` becomes the complete previous **destination**, including on Save As |
| Repeated enabled | Single `.BK!` rotates to immediately previous destination, not numbered history |
| Existing, disabled | Exact candidate replaces target; existing same-basename `.BK!` is removed |
| Refused or canceled before dispatch | Target and backup retain complete prior bytes |

A.TXT and A.WP intentionally share A.BK!. An unrelated regular backup is replaced
by prior destination bytes on enabled replacement. Existing backup/destination
observations are hashed and revalidated before mutation. Symlinks, ambiguity and
backup inode aliases to target or acquired source are refused. Replacing a
native document whose name already ends `.BK!` is a safe explicit refusal: its
self-backup behavior is unqualified by original evidence. First save does not
delete a preexisting same-basename backup; no original observation authorizes
that extrapolation. Timed backup/recovery, backup self-collision parity, metadata/
ACL preservation, Fast Save and multiuser DOS locking remain later M1 work.

### Replacement transaction and failure contract

Existing candidate creation, short-write handling, byte verification, pinning
and guarded cleanup are shared with legacy publication. Everyday saves add file
`fsync`, `renameat2(RENAME_EXCHANGE)` for an existing entry, no-replace hard link
for a new entry, and directory `fsync`. A displaced original remains under the
operation's private candidate name with a read-only inode pin. Backup rotation
uses another verified staged file containing the complete old destination;
disabled backup removal moves the old backup to a private recovery name with
`RENAME_NOREPLACE`. No original file is opened for writing or truncated.

The document namespace changes first, followed by the backup. Both changes are
verified; the directory is synced, recovery entries are removed with ownership
checks, the directory is synced again, and final document/backup bytes and
identities are verified before success. New files use private 0600 permissions
subject to umask. Filesystems lacking exchange/no-replace or required sync
support fail rather than falling back to overwrite-prone emulation.

This is **not an atomic two-file transaction**. Other processes can observe the
intermediate document/backup pair. An OS crash can leave either namespace state
and recovery files. Fsync calls are the promised local-filesystem durability
boundary, not a claim to emulate original disk errors, repair host storage or
provide a journal/recovery manager. The two-file window remains explicit.

| Failure boundary | Report and conservation |
| --- | --- |
| Preparation, cancellation, stale source/target/backup, staging/write/file-sync failure | No admitted publication; original target/backup preserved. Candidate cleanup failures expose their residue. |
| Main/backup namespace operation or first directory-sync failure | Attempt reverse-order rollback while entries still match this transaction. Fully verified rollback plus directory sync reports failure with original target/backup bytes restored. |
| Concurrent modification prevents rollback | `PublicationUncertain`, `DestinationMayExist=true`; do not overwrite the concurrent file. Retain recovery entries and report their names. |
| Cleanup after verified durable namespace update | `CleanupFailed`, destination may contain committed candidate; recovery entry is retained. Do not report a declined/unchanged save. |
| Final directory sync or final file/backup verification | `PublicationUncertain`, destination may be committed; inspect/reacquire before any retry. |
| Descriptor close failure | Failure, never successful receipt; publication may already have completed. |

Directory wrapper aliases serialize everyday transactions and Close on their
shared capability. Independent acquisitions/processes are external writers; no
unimplemented interprocess lock is implied. Freshness checks and namespace
mutation are separate observations, not atomic compare-and-swap. Rollback checks
current bytes/inode before exchange/unlink and refuses observed interference;
a malicious same-user writer in the remaining check/syscall window is outside
the trusted-directory contract, as it is for legacy candidate cleanup. There is
no guarantee after the final observation. Failed/uncertain operations never
return a newly admitted source and must not clear editor dirty state.

See `evidence/everyday/REPORT.md` for checks, source custody and consumer gates.
