# WP68 TEST foundation

This package supplies the account, durable TEST ticket issuer, retained directory
lease, owned ledger, finite LedgerRecordV1 encoder, and a real installed public
administration/transaction command. It does **not** implement `run_leaf`, start a
reference process, import P/peer providers, access private assets, or qualify any
original-app action. `RootTicketIssuer.issue` always refuses before caller paths
are inspected. Mission 1 remains open; PDF belongs to Mission 2.

The ordinary supported deployment is an offline wheel in a pinned, copied
CPython 3.13.13 venv. `tests/deployment.py` is the trusted test coordinator: it
records the exact build source and wheel, pins the executable, actual imported
stdlib/extension closure, pyvenv configuration and every installed file, refuses
caches/customizations/extra files before interpreter startup, and writes the
bounded deployment-data manifest. The package repeats flags, source-root and
source-byte checks before importing its transaction implementation. Post-import
checks do not claim to neutralize an already-executed hostile .pth file. The
premise is exclusive custody of this fixed local deployment, not a Python sandbox
against a malicious deployment owner or reflective caller.

The CLI is deliberately small:

```
<pinned-copied-venv>/bin/python -I -B -m reference_controller test-admin \
  --root /tmp/wordling-reference-TEST-<fresh-id> --generation <fresh-generation>
<pinned-copied-venv>/bin/python -I -B -m reference_controller test-transaction \
  --root /tmp/wordling-reference-TEST-<fresh-id> --generation <fresh-generation> \
  --grant-id <fresh-test-id>
```

Administration preprovisions one trusted local TEST store and a separate ledger
sibling. A transaction reserves its single earlier account, obtains an actual
issuer-held permit, creates the permanent stable spent marker, writes/syncs the
marker and its held parent, reads it back, then hands off one opaque TEST grant.
Only its one-use activation enables parent/ledger operation permits. The public
consumer writes and reads back actual AUTHORIZED/COMPLETE records, uses the
same-book audit reservation seam, and closes held resources. A spent marker is
never parsed as authority, deleted, migrated, reissued, or repaired. Store lock
and ticket descriptors remain held through the transaction. Boot/source/kind/
generation mismatch quarantines the store. Original and TEST types/stores remain
disjoint.

The generic `book.reserve_phase(phase, owner, maxima)` seam reserves full maxima
in this same cumulative book; it never refunds unused work. Its actual returned
reservation checks owner identity and source-owned counters. Future WP70 must
consume this approved API and the same earlier origin, not edit or reset these
foundation modules. Ledger permits remain four exact kinds. Public facts,
serialized observations, copied objects, paths, stats and SourcePolicyData cannot
replace a registered live capability. Bootstrap validates policy-data provenance;
it cannot issue a grant.

Bounds: 64 frozen acceptance cases, 30 seconds plus two cleanup seconds per case,
300 seconds per suite, 2 MiB stdout/stderr per case, 2,048 evidence files and
32 MiB total evidence. Runtime ledger serialization is exact-builtin-only,
two-pass, alias-free and finite. Its conservative byte bound can refuse a record
whose eventual compact content would fit. Actual writes/readbacks are bounded
4096-byte pieces. The leaf has one 30-second end; issuer stage has at most two
seconds within it. A local fsync may block: an observed post-call expiry refuses
grant delivery; no hard real-time or hardware power-loss guarantee is claimed.
Trusted fixed local filesystem semantics remain an explicit premise.

`tests/run_acceptance.py <NEW-ATTEMPT-LABEL> --full --all-checks` freezes exact
source/roster/tool/argv/cwd/environment inputs, builds and installs an ordinary
wheel, runs the 48 public CLI/API/OS cases, builds nine independent semantic-mutant
wheels, then runs the actual seven project checks. Each attempt uses fresh IDs
and stores. Mutation/import/build failures count UNKNOWN rather than a kill.
The configured Go checks use the already installed Go 1.26.4 and its normal
existing caches with network/toolchain download disabled. No product loader,
sys.path, legacy class, global IO function, private resource or peer module is
patched to make a deployment fit.

History remains material evidence. The initial tests-first missing-package RED
is retained. Attempt02 preserved 38 PASS / 10 FAIL: nine log-directory collisions
in the coordinator and an injected short read that hit metadata before any
marker. Those nine early loss/race failures occurred after the OS action but
before the coordinator wrote its child streams; the missing streams are UNKNOWN,
not reconstructed. Attempt03 corrected those coordinator errors and passed all
48 functional cases. Attempt04 passed those cases and all nine mutants, but the
configured minimal PATH omitted installed Go (one discovery failure/three actual
skips). Attempt05 pinned the existing Go environment and passed 48+9+7. Explicit
`py_compile` created caches despite -B; those unused generated bytes were moved
into initial evidence, never admitted to a runtime source root. No failed ID was
reused or any failed outcome rewritten.

The consolidated source separates eleven cumulative dimensions from four live
ceilings: processes, RSS, FDs and workspace files. Live ceilings are not credits.
The actual coordinator-only Linux sampler returns a registered, one-use opaque
observation; filesystem-free account recording retains baseline/current/peaks or
HALTs. Copied, field-identical, malformed, foreign, replayed or expired observations
cannot replace it. A kernel sample is neither a worst-case reservation nor
continuous monitoring. Future WP70 must bind and measure the actual complete
provider/session actor set; this package proves no P/child totals.

Cleanup has 64 close attempts with separately funded syscall/work costs.
Source factories reserve their aggregate cleanup hold before opening resources.
`close_requirements()` returns data derived from that held reservation; only an
actual one-use operation permit allows close. The maximum parent path retains33
FDs and has an actual66-syscall close requirement. The max-depth public control
creates that path, writes/readbacks a real ledger and closes every held resource.
There is no fresh cleanup budget after HALT or refund after a shorter close.

Attempts07/08 were genuine green historical revisions;09 tested terminal finish;
10 added buffer/file/journal accounting and retained one semantic-mutant UNKNOWN
rather than relabeling its changed failure. The systematic charge matrix then
consolidated live-vs-cumulative accounting, typed observations, aggregate cleanup,
pre-entry report allocation, metadata primitive types/decode work and namespace
bounds. Targeted11 passed six installed public controls plus the meaningful
consumed-permit mutant. The same production revision passed full12:48 functional
cases, nine semantic mutant kills and all seven configured checks, WHOLE0 in
48.457s under the shared300s end. Maximum observed cumulative child high-water
RSS was81,920KiB, including packaging/Go tools; actual coordinator measurements
are separately retained in transaction records and do not become RSS credits.

Complete actual attempts01–04/07–10 are losslessly archived under ROOT's explicit
representation ratifications, each with exhaustive original path/type/mode/size/
SHA maps and bounded full round-trip receipts. Original names and any old seals
keep their original meaning. Missing02 streams remain UNKNOWN in GAPS.json.
Attempt05, failed predeployment06, targeted11 and consolidated12 remain literal.
The inherited-baseline gzip is a separate metadata index, not a runtime archive;
its36,105,177-byte original JSON expansion is explicitly reported separately.

The first configured Go runs used HOME=CWD and generated exactly seven local
telemetry cache files. Their complete bytes/metadata and provenance were verified
and archived before removing only those own redundant files. Future coordinator
runs keep HOME in their declared isolated TMP target; no user HOME, inherited
cache or project source is removed or staged for this correction.
