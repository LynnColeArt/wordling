# Independent prepared-publication ownership investigation

Reviewer codex/reviewer-renata, existing wp51-parity-01M64CVY mission. Resolved
profile and loaded review governance. Scope is sequential public wrapper assignment
between PreparePublication and Publish on approved storage source70e02f7; no broad
API audit, implementation repair, VM, repository or lifecycle change.

**Disposition: three reproduced P2 contract failures, one prepared-request ownership
class. Block41–43 promotion until their bounded structural repair and acceptance
requirements are explicitly included.** This does not revoke or rewrite historical
approval records and makes no product/full M1 claim.

## Actual reproductions

The parent's public overlay source and original raw log are retained unchanged as
parent-reproducer.go.txt and parent-original.log. I ran that overlay independently
on the actual unchanged lane-b; both genuine assertions fail again, retained in
parent-independent-repro.log. Then I wrote a separate public-API overlay with
physical output assertions and ran:

```
go test -race -count=1 -overlay /tmp/wordling-publication-alias-independent/overlay.json ./internal/storage -run '^TestIndependentPrepared' -v
```

It exits1 with three real assertion failures (repro.log); no data race is reported.
The ordinary unmodified storage suite still passes, retained in baseline.log.
New tests expose missing contract protection; baseline success does not invalidate
the failures. No source file or historical evidence log was rewritten.

### R1/P2 — source guard substituted after preparation

PreparePublication stores the caller's `*Document` directly at
internal/storage/publication_linux.go:56. After it returns, change the physical
original source and assign `*source = *otherRead` using another valid snapshot
from the same directory. Publish's checkSource now revalidates the replacement
snapshot, not the prepared original observation. It returns Published/nil and
creates first with the exact prepared payload despite the changed original.
The test fails the expected stale/refusal-before-output assertion.

Root cause: publication source is a mutable public wrapper pointer, not a captured
immutable source observation. checkSource reads doc.origin/doc.name/doc.identity
at execution time (storage_linux.go:338–347). Pre-link source checks are still
called, but their referent has changed. Requirement: capture the original source
identity/name/image and stable opened-directory capability at preparation. If
that original changes, StaleSource must occur before any destination publication,
regardless of later public-wrapper rebinding. Keep all existing freshness checks.

### R2/P2 — prepared target name substituted

Observe absent first and second in the same directory, prepare first, then assign
`*first = *second`. Publish succeeds with Outcome.Name second; first is absent and
second physically contains exact payload bytes. The public Directory wrapper and
ID remain unchanged. The prepared name was retargeted by a later caller assignment.

Root cause: stored `*Destination` is not an owned observation. Requirement: pin the
exact prepared name, absence/identity observation and stable directory capability.
A later wrapper assignment may be ignored through owned capture or cause explicit
refusal; it must never publish at the substituted name. Real late creation of the
original prepared name must still refuse without overwriting either destination.

### R3/P2 — opened-directory capability substituted

Create root/source and a hardlink secondRoot/source BEFORE the fresh original
Directory.Read. The source inode/content, link-dependent ctime and full acquired
snapshot therefore agree when subsequently read through either directory. Open
two genuinely distinct pinned Directory handles, read and prepare original
root/first, then assign `*d = *otherDirectory` before d.Publish.

Publish succeeds with the second directory's ID; original root/first stays absent,
secondRoot/first physically contains exact payload bytes. The assertion fails on
actual redirected output, not just Outcome metadata. The copied original Directory
is closed exactly once through its captured value; the second handle is closed
exactly once through its own wrapper. No lost original descriptor or double-close
is needed to reproduce the defect.

Root cause: Publication.directory, source.origin and target.directory all retain
the same public pointer d. Address comparisons at publication_linux.go:64 still
succeed after d's fields now designate another opened root. checkSource follows
that redirected capability and the hardlink makes it genuinely pass. Directory
pointer identity does not establish immutable opened-capability identity.
Requirement: publication must pin the original stable private capability. Publishing
through a rebound receiver must refuse before effects, or demonstrably use the
captured original capability under an explicit compatible API contract; it must
never touch the substituted root. Do not solve R1/R2 with shallow copies that still
point at a rebindable public Directory wrapper.

## Bounded repair and exact acceptance

WP41's shared transaction work must explicitly close this existing prepared-request
class alongside the new source-less type. Stable private acquired-directory state
and immutable owned source/destination observations are a reasonable structural
solution; this review does not mandate a particular field layout. Preserve the
existing public signatures, typed failures, source/destination checks, pinned-root
rename behavior, descriptor/Close ownership, no-replace candidate verification,
cleanup/uncertainty semantics and approved Save cross-directory behavior. Do not
remove freshness checks, weaken identity to path/hash alone or treat PublicationID
as authorization. No broad speculative storage rewrite is authorized.

Both existing Publication and proposed NewPublication need exact prepared root,
name and observation ownership independent of public source/target/directory
wrapper assignments. NewPublication naturally has no source, but must not inherit
R2/R3 or use source absence to weaken destination ownership. Corresponding caller
routing still requires real sources for loaded/already-bound buffers.

Acceptance must run genuine public-API tests with zero, same-directory other,
cross-directory and rebound wrapper variants after preparation, keeping mutations
sequential. R1 must return stale for the changed original with no output; R2 must
retain prepared first or explicitly refuse with no second output; R3 must retain
original opened-capability authority or refuse, with no redirected second-root
output. Include source/destination changes at actual existing transaction boundaries,
late prepared-target creation, candidate residue/close faults and old exact tests.
New unsourced requests must reject target/root substitution without publishing
elsewhere. Keep exact output bytes, lengths, identities, absence checks, real rooted
filesystem faults and caller byte-copy tests. Run the real storage suite/race checks
and actual downstream editor/TUI consumers after the bounded repair; unchanged
legacy behavior and new-type production routing need independent review.

This is sequential legal Go assignment to exported wrappers, wholly between API
calls. Existing “do not mutate data during preparation” and concurrent-mutation
caveats do not prohibit or account for these cases. Merely documenting caller
wrapper immutability now would weaken the approved prepared-binding contract and
leave the new public type fragile; capture ownership at the boundary instead.

## Bindings and retained limits

Machine findings and seals bind exact70e02f7 production source, helper fixtures,
public overlay, root original evidence and each actual command log. No proprietary
native fixture bytes are copied into this report/evidence; the tests consume the
repository's lawful existing fixture. Actual lane-b and primary remain clean;
no tracked log, code, task or lifecycle artifact changed. All handles and test
scratch data are cleaned by test defers/TempDir. No pending process remains.
Prepared-request integrity repair is a prerequisite disposition for41–43 authoring,
not implementation or product acceptance. Full M1 duties remain unchanged.
