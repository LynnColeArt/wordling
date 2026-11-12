# WP34 independent review, cycle2

Independent reviewer: codex/reviewer-renata; did not author0793933 or70e02f7.
Source:70e02f7bdfcb155983a60e8c3583b7b497447f86 in canonical lane-b.
Runtime review prompt:bb9ae389fd5744a9b5f62f3d45b94cf5.
Recommendation: APPROVE bounded rooted read-only macro acquisition. Cycle1's P2
is fixed. No new blocking finding. Full38 obligations/91 groups remain open.

## Ownership repair and independent red/green proof

Cycle1 review/evidence b29d6b0 found that Image returned the owned codec pointer.
Legal whole-value zero/cross-image assignment changed Macro.Export while stored
Identity remained original. The fix changes only Macro.Image's returned wrapper:
a separate value copy retains the codec's immutable private backing. Replacing
that returned value cannot replace the acquired snapshot or another view. The
codec has no mutating methods; Export, Description, BodyWords and Inspect findings
copy, while metadata/hash return by value. Its source is unchanged. There is no
reparse/deep-copy parser, second filesystem engine or publication permission.

The exact cycle1 reviewer test bytes are retained, unmodified, and compiled as a
virtual test via Go overlay. Red overlay uses the exact0793933 production
macro_linux.go blob; other relevant source is identical. Both zero-assignment and
cross-image tests fail actual assertions, exit1. The same exact tests pass current
70e02f7 under race, exit0. New production regression tests likewise fail old source
and pass current source; they check pre-existing/repeated views, source name/root/
identity/hash and cross-image/zero replacement. Zero Macro still returns nil
Image/Export; nil receiver remains invalid, with existing panic behavior explicitly
pinned. This does not extend the accepted snapshot contract to zero objects.

Additional independent overlay test runs8 goroutines x100iterations with race:
each replaces its own returned wrappers, mutates copied Export/Words/Description,
and checks another view plus Macro bytes/hash/source identity remain original.
It passes. All overlays/evidence are under /tmp; working source, original corpus
and tracked author logs are unchanged.

## Actual independent validation

- Fresh go build ./..., go test -count=1 ./..., go vet ./..., go test -race
  -count=1 ./... all exit0 in the actual three-package code lane.
- Changed Go formatting and fix-commit whitespace check clean.
- Real configured scripts/review_checks.py JUnit has7 passing cases,0 failures,
  errors or skips. Actual manual checks are distinct from transition gate scope.
- Fresh storage JSON test stream:155 passing nodes, including all46 original WPM
  acquisition subcases;22 distinct original hashes.
- All37 current artifact seals match actual committed Git blobs/size/SHA256.
  All36 inherited codec/acquisition/publication files exactly match0793933 and
  the listed hashes/blobs;4 approved source-proof files match their references.
- All15 old manifest entries independently classified: only macro_linux.go and
  storage README differ;13 other source/raw entries remain exact. Actual46
  originals match pinned SHA/size/Git blobs, and fixed commit's25 paths are all
  storage-owned.0793933..70e02f7 includes supported planning merges; isolated
  diff-tree of the fix commit is the correct change-attribution boundary.
- Existing source/fault tests actually exercise validName/readStable, pinned root,
  no-follow regular file, bounded read/growth, stat/read/close/path failures,
  mutation/replacement/stale detection, closed directory and concurrent reads.
  DOC Read and PreparePublication still refuse WPM; ReadMacro refuses DOC and
  retains typed malformed/unsupported causes. Existing Save/PreparePublication/
  Publish/source-guard tests pass; corresponding source is byte-identical.
- Retained60s basename fuzz and historical mutation records inspected, unchanged.
  No redundant fuzz or VM/original execution is claimed for this pointer-only fix.

## Documentation digest observation

cycle-2/preservation.json contains an intermediate README current_sha256
759433e0d80ffe71c8afb2cbd305dc20409e7e1ef5a5d402bffbcb77c333e68d,
preceding the final appended cycle2 evidence paragraph. Final README's actual
SHA256 is9cd70c98def15d327e6f5cca0a0722ae472b5e25ae5ab3f16f811fb0d8387720,
correctly bound by the authoritative current artifact manifest/Git blob. This
intermediate report is not a current checksum oracle for that one documentation
file. The independently recomputed current37 seals, frozen36 and source/raw tests
all pass; no required current source/provenance binding relies on the stale doc
field. Disclosed as a nonblocking historical packaging limitation. Old evidence
was not rewritten. audit.json records both values and actual preservation checks.

## Anti-pattern checklist and scope

1. Dead code: N/A for staged product integration. ReadMacro is a real production
   method reused by public acquisition/fault tests; its direct product consumer
   is explicitly queued WP36/37. Production call-site grep shows definition only;
   editor/TUI integration NOT RUN. No fabricated caller/full FR012 closure.
2. Synthetic fixtures: PASS.46 actual original source bytes are acquired through
   real storage/codec and checked; errors/faults invoke live methods, not stubs
   mirroring output. Reviewer red tests fail real old production source.
3. Silent empty return: PASS. Refusals return typed storage/codec errors with nil
   Macro; nil image only for zero/unacquired Macro, explicitly not accepted.
4. FR coverage: PASS for scoped component only. FR006 rooted source acquisition,
   FR012 original companion loading, NFR001 byte/hash retention, NFR002 read/error
   preservation and publication boundary, NFR004 actual bound evidence. Full
   requirements and original execution/recording/conversion remain open.
5. Frozen surface: PASS. Codec, DOC reader, acquisition/publication and raw
   originals unchanged;36-file and4-approved-source comparisons independently pass.
6. Locked decisions: PASS. Original formats unchanged; no proprietary code/data,
   arbitrary host paths, WPM save/publication or execution granted.
7. Shared ownership: PASS. WP03/WP24/WP34 share canonical lane-b; narrow existing
   storage ownership is explicit. Prior acquisition/publication source unchanged;
   only wrapper ownership fix, tests and owned docs/evidence change this cycle.
8. Production fragility: PASS. No new panic or filesystem path; nil receiver
   invalidity unchanged. Normal source/stale/path/malformed/unsupported failures
   remain typed and contain no fabricated original-app error text.

Canonical runtime prompt, AGENTS, reviewer profile/governance and charter/native
contracts applied. No implementation fix performed by reviewer. No VM used;
reference oracle held by WP39. Source lane remains unchanged except runtime-created
.spec-kitty coordination. No accept/merge, fullM1 completion or M2/PDF claim.
