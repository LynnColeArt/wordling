# WP03 implementation validation — 2026-10-30

Implementation evidence, pending independent review. Scope is `internal/storage/`;
the dependency base is approved WP02 commit e7de080. No dependencies, original
fixtures, codec source, UI or existing project configuration were changed.
The package contract was written before implementation in `../README.md`.

## Actual checks

```sh
gofmt -w internal/storage/*.go
go test ./internal/storage -count=1 -timeout=30s
GOARCH=386 go build ./internal/storage
go test -race ./internal/storage -count=1 -timeout=60s
python3 scripts/review_checks.py --junitxml internal/storage/evidence/validation.xml
gofmt -l internal/storage/*.go
git diff --check
```

The initial test-first invocation refused to build because no non-test storage
package existed. The completed deterministic suite and race tests pass.
`validation.xml`/`validation.txt` are actual review-adapter output: 7 checks,
7 passing, zero failures/errors/skips. The adapter discovered both real Go
packages and ran build, all tests and vet; it also ran both catalogue checks
and adapter process/reporting tests. Its all-tests run includes unchanged WP02
original-run/fixture hash and provenance checks. No gate was bypassed/disabled.
The runtime for_review gate is a separate check, recorded in runtime history.

`race-tests.txt` is a real `/usr/bin/time -v` run: package test time 2.440s,
process wall time 2.90s, maximum reported RSS 625,544 KiB, exit 0. This includes
race instrumentation, maximum-size 16 MiB snapshots and repeated filesystem
verification/copies; it is not isolated parser/storage memory or a product
performance budget. Host, toolchain, filesystem type and source hash are pinned
in `host.json`. No network filesystem or power-loss/durability result is claimed.
The 386 build checks Linux integer-width portability only, not runtime/platform
qualification. The exercised host is Linux amd64.

Public API tests pin six original fixture hashes/lengths to WP01. Five documents
read and publish with exact original bytes/length/SHA; the macro is refused and
retains its typed wp51 cause. They check same-file no-op plus explicit overwrite
permission, refusal of actual existing-file replacement (even an identical copy),
identity/receipt consistency, buffer isolation, malformed/native refusals, path/
symlink/nonregular nodes, stale source/destination, closed handles, and exactly
16 MiB read AND publication. The reader caps growing acquisition at limit+1;
the resource test verifies the actual bytes read, not only the final error.

Real temporary files and OS operations back the injection boundary. Tests cover
candidate creation, collision retry limit, short/zero/partial/full write errors,
corrupted candidate bytes, writer/read close faults, candidate pin open/stat/close
faults, unknown-identity residue, link errors before and after an actual side
effect, cleanup failure, source modification/inode replacement during candidate
write, late destination file/symlink insertion at the actual link boundary,
candidate substitutions before verification and between check/link, foreign
destination replacement after link and during cleanup, source symlink/FIFO races,
source replacement after open, pinned-directory path replacement and concurrent
Close. They assert exact source/foreign-file preservation and no false success.
The tests explicitly demonstrate snapshot semantics: a later independent source
write after its final validation is not overwritten or treated as an atomic
cross-file transaction. No ordinary rename is used by production; actual link
publication failure is tested. Renames in tests simulate independent writers.

Two adversarial tests drove structural safeguards: Root.OpenFile follows in-root
symlinks despite O_NOFOLLOW, so leaf opens now use Linux openat on a RawConn-
pinned directory descriptor; closing/unlinking a candidate can immediately recycle
its inode, so a read-only candidate descriptor stays open through publication and
cleanup. Source/writer/read/pin close failures are checked. Post-link interference
returns PublicationUncertain (or a conservative failed publication result) and
DestinationMayExist; no destination rollback can remove a foreign writer's entry.
Final verification after candidate removal accounts for the ctime change caused
by removing the extra hard link. Read-only pin close failure also prevents a
complete-success return even if publication occurred.

`mutation-checks.txt` records four selected changed-scope faults killed by actual
assertion failures: missing explicit overwrite permission, ignored short write,
skipped source freshness comparison, and omitted post-link identity checking.
This is a test-quality sample, not a comprehensive mutation score. An initial
source-check probe failed compilation because its removed comparison left an
unused local; `mutation-initial-invalid-probe.txt` preserves that invalid attempt.
The corrected probe retained the unused value without changing behavior, compiled
and was killed by an assertion. All production source was restored byte-exactly
before final race/adapter checks; its SHA matches the mutation report and host.

WP02's native decoder is called directly, not duplicated or changed. Its prior
60s/600s fuzz evidence is retained in the dependency; no new format decoder or
additional native fuzz result is claimed by WP03. Acquisition/publication safety
is validated by the bounded, failure and race tests above. No new native content
or semantic writer was introduced, and no original-app semantic edit/reopen/print
or full user-workflow compatibility result is claimed from a byte-copy pass.

## Remaining boundary

Existing destinations receive no write/rename/unlink at all: only verified
same-file no-op is supported with explicit permission; other replacement is
UnsupportedReplacement. Atomic no-replace publication is one observation point;
source freshness and final published verification are separate observations.
Subsequent external writes/deletes are outside a snapshot guarantee. Candidate
cleanup assumes ownership of the random temporary name, checks the pinned inode
and refuses observed substitution; check/unlink is not an arbitrary same-user
conditional-delete primitive. Such interference/crash may leave reported residue
or a destination; uncertain outcomes require inspection. No ownership/exclusivity
boolean manufactures a replacement guarantee. Original overwrite, backup, locking,
Fast Save, recovery, path mappings, network semantics and durability remain M1
research/implementation obligations under WP06/WP12. Independent review must assess
this bounded contract; this evidence is not acceptance or full file-save parity.
