# WP02 implementation validation — 2026-10-30

This is implementation evidence, pending independent review. It does not claim
mission acceptance, semantic editing, original-app edit interoperability or parity.
Source is confined to `internal/wp51/`; no dependencies or original fixtures changed.

Commands run from the lane checkout:

```sh
gofmt -w internal/wp51/*.go
go build ./...
go test ./internal/wp51 -count=1 -v
go vet ./...
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
GOMAXPROCS=2 go test ./internal/wp51 -run='^$' -fuzz=FuzzNativeFraming -fuzztime=60s -parallel=2
GOMAXPROCS=2 go test ./internal/wp51 -run='^$' -fuzz=FuzzNativeFraming -fuzztime=600s -parallel=2
python3 scripts/review_checks.py --junitxml internal/wp51/evidence/validation.xml
go test ./internal/wp51 -run='^$' -bench=BenchmarkMax -benchtime=3x -benchmem
gofmt -l internal/wp51/*.go
git diff --check
```

The first test-first invocation failed because no non-test Go package existed.
The completed external-API deterministic suite passes. Every original seed and
both synthetic recipe seeds are truncated at every byte boundary. Malformed body
and prefix tests require typed refusal, no accepted image and unchanged inputs.
Selected whole-token truncations legitimately pass with exact export because the
native outer framing has no body-length/end marker. Input and metadata buffers
are isolated; original bytes, lengths and SHA-256 hashes match.

`validation.xml` and `validation.txt` preserve the real review adapter results:
7 checks, 7 passing, 0 failures/errors/skips. Go discovery found the actual package;
Go build, test and vet all executed. The adapter also ran the inventory and scenario
catalogue checks and its own real successful/failing-process reporting tests.
No gate was skipped or disabled. Historical WP01 pytest/JUnit baseline failures
and later baseline capture remain in runtime history; these results do not erase
them or rewrite cached baseline data. The runtime for_review gate is separate.

`fuzz-60s.txt`: 7,000,569 executions, PASS, test time 60.132s,
process-tree time 60.90s, maximum reported RSS 110,496 KiB.
`fuzz-600s.txt`: 57,160,290 executions, PASS, test time 601.033s,
process-tree time 601.30s, maximum reported RSS 214,072 KiB.
Both ran with two workers / GOMAXPROCS=2 and `/usr/bin/time -v`.
No crashes or hangs were reported. Go retained interesting inputs in its standard
fuzz cache. The target loads all six original fixtures, both recipe seeds and
malformed boundary/cycle seeds; Go deduplicates duplicate empty seeds. The longer
run also used interesting inputs cached by the smoke run. Counts and corpus
discovery are nondeterministic, and these observations are not exhaustive proof.
RSS includes the Go command, fuzz coordinator, worker/harness copies and runtime;
it is not isolated parser-owned memory or aggregate simultaneous process RSS.

`benchmarks.txt` has stdout trailing whitespace trimmed (numeric output unchanged).
It is a three-iteration observation on the host pinned in `host.json`:
maximum 16 MiB single-byte body ~20.9ms, 16,777,498 B/op, 5 allocations/op;
maximum prefix (4,096 blocks / 16,384 zero-length packet entries) ~1.84ms,
4,667,458 B/op, 89 allocations/op. B/op is allocated bytes, not peak live heap.
The parser allocates one owned byte image plus bounded metadata and no per-body-
token list. Tests accept the exact input/block/entry ceilings, reject 16 MiB+1 as
InputLimit and 4,097 blocks as TraversalLimit. Four general entries per accepted
block mathematically cap packet entries at 16,384. These policies do not establish
original application limits, product latency targets or support for larger variants.

`mutation-checks.txt` records four deliberate changed-scope faults that the
export/isolation, exact-limit, fixed-delimiter and overlap tests detected. Each
fault produced an assertion failure, and production source was restored exactly
before the final validation adapter and benchmark. This is a selected test-quality
probe, not a comprehensive mutation score. The production source hash in host.json
matches the final source and the source used by both fuzz runs. Later additions
only strengthened deterministic tests and documentation; the fuzz target and
production source did not change after the long run began.

`corpus-verification.txt` records read-only SDK51 PDF/extracted-text checksum
verification from the primary ignored research cache, and all six tracked original
fixtures checked against WP01 and their original-run evidence (including packet
hashes, index fields, body hashes, runner archives and registry paths). No manual,
proprietary executable or new native fixture is redistributed by this package.

Limitations and next boundaries: function/packet payloads and nested text remain
unvalidated, all data stays opaque, and semantic mutations are absent. WPM and
other companion formats, alternate versions/index counts, encryption, nonzero
graphics and overlaps remain explicit unsupported variants requiring M1 follow-up.
WP03 owns bounded acquisition, filesystem transactions and the first production
consumer. No UI/CLI or general writer was introduced to manufacture a caller.
