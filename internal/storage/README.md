# Bounded no-edit local storage contract (WP03)

This package implements T007–T009, tracing FR-006, NFR-001/002, C-002,
FC-002/004/009 and Story 1 scenarios 1/4 to a bounded filesystem foundation.
It consumes the approved `internal/wp51` image; it does not duplicate a codec.
This is a Linux local-filesystem API, pending independent review, not full F10,
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
across different files are not an atomic transaction. Success publishes exactly
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
