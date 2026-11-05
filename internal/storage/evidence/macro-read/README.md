# WP34 rooted macro acquisition evidence

Owned change: Macro/ReadMacro in macro_linux.go, public/fault tests, this evidence
and the appended README section. Inherited storage_linux.go/publication_linux.go
and approved codec/image/corpus metadata remain byte-identical to their approved
Git objects; inherited-source-proof.json records hashes and blob IDs. No other
checkout supplied implementation code, no filesystem engine was duplicated and no
module dependency changed. WP32's contract is read from immutable4eb851e because
that planning artifact is not in the canonical code lane's ancestry.

All46 original WPM exports/22 distinct hashes were acquired through the actual
rooted Directory API using temporary copies of pinned project-authored inputs.
Each test checks source device/inode/size/mode/time/hash, directory/name binding,
immutable exported/image views, source bytes/inode preservation and no new files.
The original corpus and Git blob hashes are verified through approved WP33's
existing fixture manifest; no proprietary binary/resource or new WPM writer was
introduced. test-events.jsonl records every actual per-fixture and failure result.

External API/fault evidence includes DOC→ReadMacro and WPM→Read refusals;
PreparePublication refuses WPM bytes; codec errors survive NativeRefused wrapping;
opaque words retain blocking findings; renamed roots stay pinned; actual symlinks,
directories/FIFOs/oversized files are refused. Existing rooted FS hooks inject
read/close/stat/lookup failures at real boundaries and verify nil macro results,
original causes and unchanged files. Tests perform real post-open source writes,
inode replacement and leaf-symlink swaps and require StaleSource. A synthetic
growing reader stops at exactly16MiB+1 through existing readStable; unsafe names
must not reach OpenFile. Concurrent observations are covered by race tests.

The changed boundary fuzz command was:

```
go test -run '^$' -fuzz '^FuzzReadMacroNames$' -fuzztime=60s -parallel=2 ./internal/storage
```

It exited0/PASS after2,316,888 executions in60.429s, with17 new interesting names.
It checks basename refusal, typed/no-partial failures, exact admitted macro bytes
and no filesystem entry creation/removal. The immutable binary codec is unchanged;
its separate approved600s parser fuzz is not rerun or claimed as WP34 work.
host.json records toolchain/platform/base and the declared scope/budget.

Six targeted wrapper mutants failed real tests in an isolated temporary module:
ignored name refusal, leaked partial failed acquisition, dropped codec cause,
wrong source identity, wrong name and appended native byte. mutations.json records
the baseline, source hash and killed-test/output identities. No working-source or
raw-evidence mutation was used. Selected mutation clients deliberately exclude
unneeded external-name fuzz seeds while testing the actual wrapper path.

Final serial validation: formatting, race across the composed code packages and
the configured seven-check runner all pass. validation.xml is genuine JUnit for
inventory/scenarios/review-adapter/Go-discovery/build/test/vet, with no skip/failure.
The final per-test event run supplies46 macro fixture results plus inherited
publication/source-guard and new fault results. Exact commands/exit times/output
hashes are in validation-commands.json. No wider tests or VM were run afterward.

artifact-manifest.json binds owned changed source/tests/docs/evidence bytes and
Git blob IDs, excluding its own digest to avoid a cycle. Existing publication
tests/source guard remain unchanged and pass; no WPM Save/Publish capability was
added. Macro identity is an acquisition observation, not a future freshness/lock or
editor revision. Actual product consumers remain queued WP36/37; component proof
does not close macro execution/recording/editor/conversion/merge/non-ASCII/resource,
physical, CMD51-199 or full FR-012/M1 scope. All38 obligations/91 groups/nested leaves
remain open; PDF remains M2. Independent review is required.
