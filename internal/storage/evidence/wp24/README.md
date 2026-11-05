# WP24 source-bound candidate publication evidence

T070–T072 extend the approved WP03 IO foundation. `PublicationID` is caller
operation/revision correlation. `PreparePublication` binds a validated owned
candidate to the real loaded source and absent destination; `Publish` matches
that ID and uses the same private publisher as `Save`. Three payload checks use
the candidate fingerprint; source checks still use the loaded observation.

The synthetic changed payload is the lawful original NEWTEST.WP5 fixture plus
ASCII X. It is framing-valid and different from the loaded source. This tests
storage identity and preservation only, not semantic write authority. No VM,
original interoperability, terminal qualification, actual overwrite, backup,
Fast Save, recovery or durability claim is made.

Tests were introduced first; `test-first-red.txt` records their expected missing
API compilation failure before implementation. Current acceptance evidence:

- `validation.txt` and `validation.xml`: actual seven-check project gate, zero
  failures/errors/skips; includes catalogue, adapter, discovery, build/test/vet.
- `race-tests.txt`: `go test -race ./internal/storage` passes, including original
  no-edit tests and new candidate/Close/publisher interference assertions.
- `mutation-checks.txt`: three compiling faults fail contract assertions:
  source hash substituted for payload hash, late source check removed, expected
  operation/revision ignored. Each changed source is restored byte-exactly.
- `check_mutations.py`: reproducible bounded mutation probes, run from lane root.
- `host.json`: actual Go/OS/architecture/kernel and implementation base.
- `source-hashes.json`: exact changed source/test/contract hashes.

Eight new top-level tests cover changed payload/input ownership and source
preservation; nil/zero/cross-directory/operation/revision/existing-target
refusals; malformed, oversized and exact16MiB native boundaries; stale source;
eight concurrent distinct candidates publishing one name; thirteen real fault/
interference cases; renamed parent path and sixteen Close/publication races.
The existing tests continue to cover no-follow/symlink/FIFO, inode pin, cleanup
residue, late side effects, source observation points and no-edit same-file no-op.
Storage decodes no new binary field: candidate grammar remains actual WP02
`wp51.Parse`. New parser fuzz claims are therefore absent; its prior contract
and bounds remain unchanged.

The public new methods are a scoped IO library surface. Actual editing callers
belong to WP27/28; the existing production Save calls the same common publisher
immediately. This component is not a disconnected editor demo and claims no
runnable editing capability by itself.

Pre-review commands, all exit0 after implementation:

```sh
gofmt -l internal/storage/publication_linux.go internal/storage/publication_test.go internal/storage/publication_failures_linux_test.go internal/storage/storage_linux.go
go test ./internal/storage
python3 internal/storage/evidence/wp24/check_mutations.py
go test -race ./internal/storage
python3 scripts/review_checks.py --junitxml internal/storage/evidence/wp24/validation.xml
python3 -m py_compile internal/storage/evidence/wp24/check_mutations.py
git diff --check -- internal/storage
```

Action governance was resolved as implementer-ivan. Requested Terminology Canon
and Code Review Checklist sections returned success with explicit not-authored
placeholders; no extra charter policy or permission gate was invented. The base
charter, FC rules, approved storage contract and independent review remain binding.
