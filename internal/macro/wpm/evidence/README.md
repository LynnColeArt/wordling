# WP33 validation evidence

All commands ran in the actual lane-n Go1.26.4 workspace. No VM, native format
writer, opcode execution or original macro-editor/disk roundtrip was run.

`validation-commands.json` records exact final serial commands, exit codes, elapsed
time and output hashes. `validation.xml` is the configured review runner's genuine
JUnit output: inventory/scenarios/review-adapter/Go-discovery/build/test/vet all
pass, no Go skip. `race.txt` covers both wpm and unchanged wp51. Independent
`test-events.jsonl` records actual public-API tests/subtests including all46 native
fixture exports; this extra run supplies per-case evidence rather than a helper
claim. Coverage is95.5% of statements, an observation rather than a quality gate.

Sequential fuzz commands:

```
go test -run '^$' -fuzz '^FuzzImage$' -fuzztime=60s -parallel=2 ./internal/macro/wpm
go test -run '^$' -fuzz '^FuzzImage$' -fuzztime=600s -parallel=2 ./internal/macro/wpm
```

Both exited0/PASS. Smoke:3,647,931 executions in61.028s including shutdown.
Long run:44,600,056 executions in600.073s;25 new interesting inputs beyond the
initial cache. `host.json` records platform/toolchain, two-worker choice and42
cached derived input hashes before the long run. Logs retain the full progress
and completion; fuzz results are bounded searches, not proof of universal safety.
Original project-authored source22 unique hashes supply seeds; additional seed
forms include all header/index truncation lengths and an opaque suffix.

`mutation-checks.json` records eight killed targeted mutants, baseline success and
original source hash. Mutations ran in an isolated temporary module copy, not the
working source: input alias, Export alias, incorrect span, silent unknown opcode,
discarded suffix, absolute alignment rule, input-limit bypass and ignored index
link. Each produced a real failing public test; no source/raw evidence was changed.

`benchmarks.txt`: original80-byte Parse measured209.0ns/op,224B/op,2allocations;
the1,048,576-word copied view measured5.26ms/op,33,554,434B/op,1allocation on this
host. These are illustrative measurements, not a promised CLI or DOS budget.
Parse does not allocate the word array; BodyWords returns it on demand. The
separate resource test (16MiB input/word/depth-independent framing boundaries)
completed in0.17s process wall time with85,444KiB maximum RSS as reported by
`/usr/bin/time -v`. That RSS includes the Go command/test subprocesses and is not
an isolated parser allocation figure or universal process-memory ceiling.

`artifact-manifest.json` pins owned source/test/fixture-reference/evidence bytes and
Git blob identities, excluding itself to avoid a circular digest. Original raw
fixture paths/size/SHA256/Git IDs remain pinned by testdata/original-fixtures.json
and are checked by the actual external tests. The manifest's parent WP32 source
is approved4eb851e; all reported behavior is this reader component only. WP34
storage and WP35 VM are queued production consumers; editor/TUI integration and
all full FR-012/M1 obligations remain open. Independent review is still required.
