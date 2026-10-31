# WP15 implementation evidence — 2026-10-30

T043–T045, pending independent review. Scope is only `internal/document/`.
Actual dependency is approved WP02 commit e7de080, with unchanged native reader.
The exact production SHA256, host/toolchain and policy limits are in host.json.
No dependency, source fixture, native codec, canonical registry or other WP was
changed. This is a read-only component, not a semantic writer or session parity.

The public API and safety budgets were recorded in ../README.md before source
implementation/fuzzing. `test-first.txt` is the genuine initial expected failure:
external tests could not build because no non-test document package existed.
`tests.txt` is the completed passing deterministic/seed suite. It verifies exact
ORIGIN gap offsets and both projections; all six pinned original fixture hashes
(five accepted documents and typed WPM refusal); complete opaque span retention;
source/export/token/presentation isolation; all16 fixed widths and maximum
variable-length frames; every truncation of ORIGIN; malformed delimiters/lengths;
zero/invalid document/cursor and arithmetic/end boundaries; exact/over token
policy and4096-token windows; and a valid exactly16MiB native image.

These tests use existing original-produced files and their independent literal
SHA256/lengths. Synthetic prefix/body substitutions test refusal and preservation
only; they never establish original behavior. Existing native framing tests
independently recheck their WP01 run/manifest/provenance identities in the real
regression suite. There is no new original application run or screen/layout test.

Actual commands, executed sequentially from lane-e:

```sh
gofmt -w internal/document/*.go
go test ./internal/document -count=1 -v
/usr/bin/time -v env GOMAXPROCS=2 go test ./internal/document -run='^$' -fuzz=FuzzReadOnlyDocument -fuzztime=60s -parallel=2
/usr/bin/time -v env GOMAXPROCS=2 go test ./internal/document -run='^$' -fuzz=FuzzReadOnlyDocument -fuzztime=120s -parallel=2
python3 internal/document/evidence/mutation-checks.py
/usr/bin/time -v go test ./internal/document -run='^$' -bench=Benchmark -benchtime=5x -benchmem
python3 scripts/review_checks.py --junitxml internal/document/evidence/validation.xml
go test -race ./internal/document -count=1
gofmt -l internal/document/*.go
git diff --check
```

validation.txt/xml are genuine project-runner results:7 checks,7 passing,
zero failures/errors/skips. Go discovery found actual wp51/document packages;
Go build, all tests and vet really ran, plus both catalogue checks and regression
adapter tests. race-tests.txt passes (package1.307s). The later runtime pre-review
gate remains a separate event; no evidence here claims that gate has run yet.

fuzz-60s.txt:6,185,417 executions, PASS, package60.842s, process wall61.48s,
maximum reported RSS110,668KiB, exit0. fuzz-120s.txt:11,951,069 executions,
PASS, package121.020s, process wall121.16s, RSS110,904KiB, exit0. Both used
GOMAXPROCS2/two workers; the expanded run reused Go's interesting-input cache.
Counts/corpus discovery are nondeterministic and not exhaustive coverage proof.
RSS includes Go coordinator/workers/runtime/harness copies; it is not isolated
live document memory or aggregate simultaneous process RSS. Production source
and fuzz target did not change between/after these runs.

benchmarks.txt records five-iteration host observations: token-limit parse
~3.977ms,6,310,334 B/op,18 allocs/op;4096-ASCII-token presentation ~50.418us,
200,704 B/op,2 allocs/op. B/op is allocated bytes, not peak live memory. The gap
index has exactly1,048,577 uint32 entries at the token ceiling (4,194,308 bytes).
The constructor also owns the dependency image and temporarily copies its body;
WP02 has its own bounded metadata. Presentation copies only its requested window,
not the whole document; opaque windows return typed refusal before element
allocation. These measurements are not product SLOs, DOS limits or WP19 session
latency/size results.

mutation-checks.py/.txt record four selected compiling faults killed by actual
assertion failures: wrong gap step, allowed opaque crossing, wrong Reveal label
and rejecting the exact token ceiling. Production source was restored byte-exactly
on every path and its final SHA256 matches host.json before final regression/race
checks. This is a selected test-quality sample, not a comprehensive mutation score.
Trailing whitespace in tool logs is trimmed without altering numeric results.

Remaining boundaries: printable ASCII and exact Bold identities only. C0 Compose,
all other functions/attributes and nested content remain opaque; movement across
and presentation of them refuse explicitly while inspection/export preserve raw
bytes. No pair-relation/edit validity, terminal geometry, original Home/GoTo,
new native writer, filesystem session, display mapping or full FR/FC/M1 acceptance
is implied. Later consumers must honor typed unsupported results and obtain their
own reviewed command/writer/resource evidence.
