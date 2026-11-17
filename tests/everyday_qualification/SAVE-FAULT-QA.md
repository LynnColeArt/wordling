# Portable terminal save-fault qualification

The `wordling_qa` Go build tag enables a one-shot, process-local storage phase
fault for terminal QA only. Normal builds compile a no-op and ignore both
`WORDLING_QA_SAVE_FAULT` and `WORDLING_QA_FAULT_RECORD`; a normal-build negative
test covers all three modes. Never distribute the QA executable as the product.

Modes: `sync-error` returns EIO before syncing the first written candidate;
`exchange-error` returns EIO before the first candidate RENAME_EXCHANGE;
`exchange-crash` records that boundary and SIGKILLs the QA process before exchange
or rollback. Only candidate-prefixed files and exact exchange flags match.
Each fault requires a newly created JSON evidence file. Evidence failure exits
125 rather than claiming the fault ran. Once consumed, later saves run normally.

These are application-level behavioral tests, not syscall tracing or evidence
that the kernel returned EIO. They test the real editor PTY, staging, cleanup,
original/backup conservation, retained edits, successful retry, and crash recovery.
The interruption leaves a complete staged candidate and original intact; recovery
must restore all three autosaved documents. No ptrace/strace is used or bypassed.
Existing modern tabs and recovery choices are unchanged; this is not new DOS
semantics or a complete Mission 1 acceptance claim.

Build both variants with `build_candidate.py REPO OUT` and the same command with
`--qa-save-faults` into another OUT. The records bind exact compiled inputs and
binary hashes. Run `run_suite.py REPO NORMAL_BINARY OUT --candidate-record NORMAL_RECORD
--fault-binary QA_BINARY --fault-candidate-record QA_RECORD` (one shell line).
The normal executable runs all ordinary cases; only save-failure uses the QA
executable. `--without-original --without-proof` is explicitly Linux preflight,
not original/proofreading qualification. Run `recovery.py QA_BINARY NEW_OUTPUT`
from the repository separately for the longer recovery sequence.

Private reference fixtures are local inputs, never new tracked payload. Their
presence and hashes must be checked before the suite. Do not reinterpret missing
fixtures or archive failures as successful tests.
