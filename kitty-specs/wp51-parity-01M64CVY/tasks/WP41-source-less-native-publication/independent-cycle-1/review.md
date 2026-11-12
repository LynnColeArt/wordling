# WP41 independent review — cycle one

Reviewer codex/reviewer-renata. Recommendation: approve bounded WP41 storage
component source5ad84e4000f4d9e2475acc1eb88e0a26448e1761 plus evidence packaging
0df934ce3185d73ec53be6d887fba513b44ab803. Zero unresolved findings. Read actual
runtime prompt68472eb3048545108d7ff7cb1d26df5d, approved02/24/34 storage/native
contracts and promoted native-lifecycle design/READY analysis. Resolved reviewer
profile and review governance; charter has no authored Code Review Checklist.
No implementation fix, original VM, out-of-owner source or lifecycle change.

## Three independently reproduced failures closed

I rebuilt exact old70e02f7 source/module/native fixture into an isolated temporary
module and ran the original independent public-API reproducer under race. All three
real assertions fail (exit1), with no data race. The current permanent reproducer
is byte-identical after gofmt to that original source; its same assertions now pass:
changed original source gives StaleSource and no output; substituted target writes
prepared first and leaves second absent; rebound Directory refuses InvalidRequest
and leaves both roots untouched. Hardlink is created before fresh source acquisition,
so source ctime coincidence cannot hide directory authority drift. Red/green logs
and immutable old source seals are independent review evidence.

PreparePublication now captures private copies of accepted source name/full Identity/
immutable native image and target name/existence/Identity. Their origins are stable
private openedDirectory capabilities, not mutable public Directory wrappers.
Publish snapshots its prepared request once, validates the exact live receiver
capability before IO, and uses captured referents thereafter. Sequential source/
target wrapper assignment cannot change those observations. There is no shallow
public root pointer still controlling acquired authority.

A legitimate Directory value copy holds the same private acquisition and works.
Another OpenDirectory of the same path/FileID has a distinct capability and refuses.
Nil/zero/rebound/closed receivers are rejected before actual filesystem hooks;
no candidates are created in either root. Root renames retain pinned authority.
Directory copies share actual Close lifetime: closing the currently designated
capability closes its root/descriptor, an earlier saved original can still close
its own resource, and aliases cannot resurrect a closed capability. Atomic closed
state and safe OS handles preserve concurrent Close behavior; no hidden reopen,
duplicate request handles, reference counting or idempotent-success claim exists.
Caller retains ownership needed to close before discarding/rebinding its last wrapper.

## New publication and unchanged guarded transaction

PrepareNewPublication/PublishNew are distinct typed APIs, not nil-source overloads.
NewPublication captures private absent target/capability and owned wp51.Parse image,
ID/hash/length; caller buffers may change after preparation. DOC framing/type and
16MiB bound delegate to approved native reader; WPM/malformed/oversize/zero/wrong
ID/capability/existing/late target cases refuse with typed errors. Storage grants
framing/absent-target publication only, not semantic edit or genesis permission.

Both paths enter the same private no-replace transaction. Its explicit guard kind
refuses zero/unknown and requires a real acquired source for loaded requests.
Actual loaded observation counts remain prepare/Publish/pre-link. Source-less
requests never open a dummy source. Source mutation at old fault boundaries still
matters; request origin may never be dropped to bypass stale checks.

Exclusive random candidate creation/pinning, bounded write/close, exact inode/hash/
bytes, destination rechecks, no-replace link, post-link verification, owned cleanup,
final verification and pin-close reporting remain the same engine. Tests exercise
real late targets, shorts/read/stat/open/close failures, candidate substitution,
side-effecting link failures, residue and foreign post-link/final states. Conservative
DestinationMayExist/Candidate remain non-success; no destination rollback or silent
retry. Existing Save retains its distinct cross-directory source snapshot/no-op
policy; sourced PreparePublication remains same-capability. Actual overwrite,
backup/recovery, durability/fsync, cancellation and stat-CAS are not added.

Macro.Image's approved34 independent wrapper is unchanged in meaning; only its
acquired origin now retains private capability. WPM parser/codec and native parser
are unchanged. No public native format/constructor/history/document semantics changed.
Production diffs are exactly storage_linux.go, publication_linux.go and macro_linux.go;
all source/evidence ownership remains internal/storage/**.

## Fresh independent checks and real consumers

Fresh actual configured runner passes seven checks, zero skips: inventory, scenarios,
adapter, Go discovery/build/test/vet. Fresh composed-lane race passes storage/wp51/
WPM, with original34 image alias tests and actual old/new fault cases retained.
The three permanent independent source/target/root tests pass. A further public
review overlay races prepared New publication against shared-copy Close24 times;
all outcomes remain typed/nonoptimistic, any visible output is exact complete bytes,
and every closed alias refuses later reuse. The overlay is archived inert .go.txt.

The isolated consumer composition contains actual approved17 b479983 and18 72369db
production APIs/tests, required native/document/input/module sources and candidate
storage/approved WPM codec. It is NOT inherited lane-b testing or a reverse dependency.
I independently verified all20 consumer/module records, all16 copied storage/codec
records, all actual Go paths and3439 exported data paths against exact Git/source
precedence. Actual production storage matches final5ad source. The historical copied
storage dependency-test snapshot precedes only two added final guard-count tests;
dependency _test.go is not compiled by go test editor/tui. Final lane race runs those
two added assertions. This distinction is retained rather than falsely requiring
unused copied test bytes to equal final production or claiming final source changed.

Independently reran actual editor/TUI race suites in that verified composition:
both pass. Rebuilt actual cmd/wordling there to an independent output path: exact
5770316bytes/SHA2565e8be87477cf0775a6f234f93f230d2b9c3a475e96c9c611fc798f9d9f53f949,
matching the recorded binary. It was not executed as a new product scenario.
This proves existing consumer compatibility; there is no live NewPublication product
route. Future constructor/session/executable F/G must provide that routing and first
anchor behavior; no current product/native genesis compatibility is inferred.

Retained bounded60s/two-worker API fuzz passed491601 executions with4096-byte input
bound and frozen source. It targets ownership/admission, not whole-parser semantics.
Twelve temporary mutants compile and fail real assertions, including source/targets,
rebound/Close lifetime, source observation boundaries, guards/IDs/size and pin-close
uncertainty. Scripts/first-failure records match actual production hashes. No repeated
fuzz/mutation budget was needed absent a new concern. Recorded resource measurements
are bounded measured cases (2100B/op prepare,9098B/op real-filesystem path; process
RSS90716KiB), not universal memory/durability promises. Exact maximum frame test passes.

## Evidence integrity and history

All109 manifest entries match current length/SHA AND actual0df934c Git bytes/blob IDs:
827725 total manifest bytes. Authority design/ADR/current-analysis Git bindings match.
The packaging-only commit changes just report and artifact manifest: drops one ignored
inherited WP24 .pyc never in Git and updates honest explanation; every remaining
non-report entry is unchanged. No production/test/raw log regeneration occurred.
Older03/24/34 evidence retains historical bindings and bytes.

Original temporary consumer composition omitted old consumer-owned fixtures, and
initial mutation composition omitted inherited WPM testdata; those honest failed
attempts remain. Exact immutable fixtures were then composed; they are not counted
as killed mutants or passed consumers. All current fixture paths were independently
Git-checked. No private manual/program/settings/media material is included here.

Reviewer audit first over-required equality of unused copied storage _test.go with
later final guard tests, then corrected the check to production equality plus exact
historical test-snapshot hash; an additional set-parenthesis correction excluded
module files from the Go-path set. These were review-tool assumptions, not source
fixes. Logs are retained. Raw CPU benchmark trailing spaces and one diagnostic final
blank line intentionally remain; source Go formatting passes and original logs are
not normalized to satisfy whitespace checks.

## Required anti-pattern checklist

1. Dead code: PASS for component API/internal paths; new exports are explicitly
   staged library capabilities whose product F/G consumer is required later by the
   approved WP41 scope. Existing production consumers exercise unchanged APIs and
   all new methods execute real rooted transaction tests. No live product route is
   claimed or invented merely to satisfy a generic application call-site check.
2. Synthetic-fixture coverage: PASS — real rooted files, pinned capabilities, actual
   aliases/faults, independent old-red/new-green and real consumer suites protect
   the claimed component behavior; no literal receipt stands in for real IO.
3. Silent empty return: PASS — invalid/closed/mismatched/fault/uncertain outcomes
   are typed; source-less guard's no-source check is explicit kind, not nil fallback.
4. FR coverage: PASS — bounded FR002/006 storage publication and NFR preservation/
   failure/bounds/evidence assertions; full command/FR/genesis remains open.
5. Frozen surface: PASS — only owned storage changes; native/WPM/helper/contract/
   older raw evidence unchanged, packaging correction is explicit manifest custody.
6. Locked decisions: PASS — no loaded-guard bypass, format mutation, constructor,
   overwrite, silent source rebasing, product routing or full parity claim.
7. Shared ownership: PASS — storage03/24/34/41 share the computed lane sequentially;
   scoped41 changes/authority documented, review evidence/verdict root quietpoint.
8. Production fragility: PASS — real failure/race paths preserve typed outcomes,
   payload/source/destination integrity and conservative residue/uncertainty; no new
   hidden IO engine or unbounded request loop.

Approval is storage-component only. New-document research/constructor, lineage,
first anchor, actual F/G routing/executable/original differential and all broader
38 obligations/91 groups/36 lessons/nested leaves remain M1. No full requirement,
product, mission acceptance/merge, oracle permission or M2/PDF is authorized.
