# WP17 implementation evidence

T049–T051, FR-004/005/006, NFR-001/002, FC-002/004/009 and C-001's bounded
read-only session component. Source is only internal/editor/. Dependency native
reader e7de080, storage7deeaf6, document44f1a6d and approved original-session
fix18d6afe are present in lane-g; dependency code/evidence and canonical registries
are unchanged. host.json records exact source, module and current primary planning
contract hashes. Dated planning snapshots remain historical; they are not
re-certified against changed canonical counts. No original VM, terminal-key
qualification, semantic writer, layout or full differential parity is claimed.

The supported-state matrix and host API are in ../README.md. Source/case links
are explicit in observations.json:22 semantic associations,78 selected WP13 raw
state witnesses and4 earlier WP11 Reveal witnesses. audit.py verifies canonical
title/features/branch membership, exact selected run hashes, fresh repetitions,
checks, raw artifact hashes, runner-source archives and exact state labels.
Negatives use an unrelated **valid** case with its own correct title/features,
a valid same-feature Home-before state for Home-after, and a pre-wait quit
transition substituted for final DOS evidence. Each is rejected. No valid ID is
used merely because the catalogue accepts its syntax.

Domain comparisons are bounded. Retrieve tests use the literal ORIGIN native
SHA/length and confirm exact exports; cursor tests assert actual body-gap offsets
324/325/328/329/330/333/334, shared normal/Reveal token identities and both leading-
Bold Home endpoints on the hashed original LEAD fixture. Cursor coordinates are
never derived from hardware-cell coincidence. Filename tests compare the exact
B:\ORIGIN to B:\OXIGIN caret edit/cancel and character-first C:\OUT\CHARFST
state. Their DOS prefixes are explicit temporary test bindings, not general
filesystem emulation. Empty-prefix production tests admit only flat names.

Clean named/fresh-empty F7 contexts compare the actual question/default wording,
F1 retention, Esc Save advancement/F1 unwind, F7,n,n and Exit Esc clearing versus
F7,n,y domain exit. CMD51-244 links only approved post-wait DOS states; stale
pre-wait screens are never terminal witnesses. Changed original buffers are not
fabricated; text mutation, Undelete, Repeat, insertion, unsupported filename
editing/commit, successful replacement and save-on-exit continuation refuse.
Original dirty observations are used only for their declared prompt mechanisms,
not as an implemented dirty state.

The storage comparison is a separate compatibility/safety contract. Real
Directory.Read/Observe/Save operations over temporary files verify snapshot load,
explicit same-file no-op, absent-name publication (including separate pinned
directories), source/destination-race refusals and exact original-file bytes.
No-edit original WP save rewrites are not a byte-identity oracle. Typed reducer
completion tests additionally inject all relevant failure/uncertainty/residue
messages at the actual asynchronous result boundary; they are not claims of
new filesystem fault injection (the approved storage suite covers those faults).
An actual publication completed after host cancellation proves detached receipts
cannot falsely report a successful current save while still exposing that a
destination may exist. Wrong operation/revision/kind, duplicate and late results
cannot bind another operation or advance exit. Invalid success identities refuse.
Copied intents/results/native exports and concurrent projections remain isolated.
A synthetic opaque-token variation proves refusal/preservation only, not glyph
semantics. No native reader/framing interpretation changed, so no new parser fuzz
budget is claimed or required by this package.

Reproducible commands from lane-g repository root:

```sh
gofmt -w internal/editor/*.go
go test ./internal/editor -count=1 -v
python3 internal/editor/evidence/audit.py
python3 internal/editor/evidence/mutation-checks.py
go test -race ./... -count=1
python3 -m py_compile internal/editor/evidence/*.py
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp17-validation.xml
gofmt -l internal/editor/*.go
git diff --check
```

Actual tests.txt/race-tests.txt pass. The real checker validation.txt/xml reports
7 checks,0 failures/errors/skips, including actual Go discovery/build/all tests/vet
and both catalogue validators. test-first.txt records the initial expected
compile failure for the first external boundary test before any editor package
existed; it does not pretend the whole later suite preceded implementation.
Four Go overlay mutants compile and fail meaningful assertions: accepting an old
operation, retaining the document on Exit Esc, suppressing uncertainty and
ignoring a storage error. mutation-checks.py never mutates production files;
the failure output and final source hashes remain auditable. Source-audit checks
are offline and exact; no source capture or fixture was regenerated.

This component does not close parent original features or mark any canonical
scenario verified. Full editing, replacement, terminal/UI integration, other
session windows/menus and the remaining M1 ledger require later approved slices.
