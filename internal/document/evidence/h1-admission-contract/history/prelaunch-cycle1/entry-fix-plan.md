# WP51 entry ownership/accounting repair plan — READ-ONLY proposal

Status: proposed only, no lane/source/canonical/private-owner changes, no VM or
original permission. Frozen source remains d5c7874a5c65d86c8a7167831b9054ff4c46de2c.
Await the complete sealed independent prelaunch review and root authorization
before implementation. No reviewer files were changed or reproductions rerun.

## Confirmed cause and evidence

The independent actual run-entry reproductions show:

* A valid-shaped isolated grant with preexisting public run.json returns
  PriorEvidence, but run.json is overwritten and an unowned halt ledger created.
* With the public runs parent actually chmod0500 under UID1000, the failed mkdir
  is repeated in the exception handler before the ledger write. PermissionError
  escapes with no durable halt. Restoring permissions lets the same authorization
  reach configuration. No real guest or shared guard was used by the reproduction.

Frozen oracle.py:153–154 validates authorization and checks ledger existence but
establishes no exclusive write ownership. Line157 checks existence and makes the
public output before any accounting claim. Line184 repeats mkdir before the halt
write. Line191 writes reports whenever output exists, even if it was foreign.
Lines168/177/185 write the private ledger through pathname-based dump, with no
exclusive creation or held identity. The current zero-guest SourceDrift unit test
missed the actual chmod and existing-output branches; its passing result is not
proof of general entry durability. These are real bounded entry blockers, not
original behavior or a changed native hypothesis.

Exact reproduction input hashes are in evidence.json in this directory. The
current frozen plan remains d52d4da3ced7fb3cf3d1372c7989066bf72bf1b3a6615b281a8022ed85e1f19b,
preflight317eae54a860188e446cb274b4e133749040cc0eedaaa1a73f6072043d16d8c3,
71 seals/72 files/363 source pins. Those historical claims and their failures must
remain byte exact in an inert mapped archive; they are not a passed prelaunch.

## Minimal chosen repair: the ledger is the exclusive accounting claim

Reuse the one declared private ledger as the ownership/accounting object rather
than adding a second mission/lease system or borrowing48 code. After complete
structural/root-grant validation, but BEFORE check(), public mkdir, configure or
physical lease acquisition:

1. Open its already-existing parent directory safely (directory descriptor,
   no-follow final component). Atomically create the ledger via parent dir_fd and
   O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, mode0600. Capture actual fstat dev/inode and
   hold the descriptor for the entire invocation. A nonblocking flock on the same
   descriptor may supplement exclusive creation; it does not replace O_EXCL.
   Existing files, directories, symlinks or busy accounting are refused without
   reading them as permission, truncating, rewriting, deleting or "repairing" them.
2. Initialize and fsync the owned descriptor and parent directory before continuing.
   Bind canonical frozen plan, exact grant ID/root-grant file SHA, all8 ordered IDs,
   unchanged historical46 count13, new failure-inclusive cap8, actual invocation
   owner metadata, phase claimed/unfinalized and attempts[]. Creation is a
   permanent no-resume claim even if a later write fails or a process exits.
   Owner labels are provenance, not cryptographic proof; the actual descriptor
   and inode are the write authority. No API path may reopen an existing empty
   ledger and continue. A new invocation always refuses an existing accounting
   object, including a valid empty/incomplete/partial one.
3. All live ledger updates and the sticky failure record write only through that
   original owned descriptor. Use bounded JSON bytes, complete writes, seek/truncate,
   fsync and descriptor readback. Verify the parent/path dev+inode still identify
   the held objects before/after updates. Refuse lost/replaced ownership and never
   write through a replacement pathname. Keep the existing object/partial bytes;
   never unlink the claim to permit retry. Bind immutable owner/header fields in
   ledger_check and prior-control/replay checks as appropriate.

The parent must already exist; inability to claim it gives AccountingUnavailable
before any source setup/output/configuration/guard/guest action. No new parent or
fallback path is invented to evade a permission failure. If initial persistence
or halt persistence is genuinely impossible, report that exact failure and
halt_durable=false. Do not promise durability, a completed observation or oracle
release. No software can truthfully promise a persistent halt if it cannot retain
any writable owned state. The root must withdraw/review an unpersistable grant;
there is no automatic retry authorization. A claim created but left partial still
blocks future invocations by exclusive existence.

A preexisting foreign output with an otherwise absent ledger is different: the
valid authorization may first create its own accounting claim, then record an
owned zero-guest PriorEvidence halt. It must preserve every foreign output byte
and inode. This repairs the authority gap; it does not forbid a new **owned**
accounting record. If the ledger is already foreign/busy, no new private write
is permitted at all.

## Independent public-output ownership

After the durable claim and source check, create the exact public out directory
once using exclusive mkdir. Record out_owned only on actual success and capture
its directory descriptor/dev/inode. No exception/finally block repeats mkdir or
uses out.exists as authority. If creation fails, retain the private owned halt
and emit a bounded stdout/stderr receipt; leave public paths untouched.

Create public run.json and aggregate-ledger.json exclusively within the owned
directory and retain their descriptors for updates; do not turn later file
existence into ownership. One-shot prelaunch/result files use exclusive creation.
Child evidence/source directories are created only below the owned output.
Verify held directory/file identity when writing; a foreign replacement or lost
output permission must not redirect writes or mask the original failure. Failure
to publish a public report cannot prevent the earlier private halt persistence.
Close only this invocation's descriptors in finally. Never unlink foreign or
busy ledger/output/owner state. Do not alter the approved oracle lock/helper.

## Required actual-entry test matrix (future implementation only)

Use isolated temp private/public trees, real OS open/mkdir/chmod/flock/descriptors,
actual run() entry, exact shaped frozen grants, and observable configure/attempt
counters. Do not mock the failing ownership/mkdir/ledger-write primitive. A bounded
fixture source-check/configure sentinel may isolate these OS paths; label that
scope explicitly. Retain the separate unpatched check()-entry SourceDrift test.
No test may acquire the real oracle or touch a real private owner/ledger.

1. Existing public run.json sentinel: exact bytes/inode preserved, configure0,
   attempt0; new owned ledger halted0; removing output cannot make retry proceed.
2. Real chmod0500 public parent: PermissionError after owned claim, durable halt0,
   configure0/attempt0; restore0700 then same grant still refused before configure.
3. Preexisting ledger variants (foreign valid/invalid bytes, symlink, directory)
   and separately held busy descriptor: no writes/truncation/deletion or public
   output creation; all sentinels unchanged, configure0/attempt0.
4. Two concurrent isolated runners: one exclusive claim at most; loser does not
   rewrite winner's claim or outputs. Winner can be blocked at a controlled
   preconfiguration boundary; no guest is used.
5. Actual claimed path replacement/rename to a foreign sentinel: inode loss is
   detected, replacement preserved, no next configuration/guest/report redirection.
6. Real unpersistable account parent: explicit unavailable/non-durable refusal,
   no output/configuration/guest. Real resource-limited write in a child (for
   example RLIMIT_FSIZE) can test initial/partial persistence failure without
   faking an OSError. Partial claimed object is retained and blocks restart.
   Do not call chmod on an already-open writable fd a write-failure proof.
7. After-owned-output archive/report/physical-lease failure: private sticky halt
   persists even if public report creation/update fails. Restore conditions;
   same grant still cannot reach configure/attempt. Preserve foreign lease state.
8. Malformed/unauthorized/subset requests: no exclusive claim or private/public
   writes. Exact integer cap/history/header identities remain enforced.
9. Actual unpatched check entry with authorized source drift: owned zero-guest
   sticky halt, restored source then retry refusal. Failed halt write explicitly
   cannot claim durability. Preserve existing first-incomplete/no-NEXT, control
   tamper-before-next, master/export/stop and strict-frame controls.

Assert exact refusal categories/owned counts, not any exception. Independent
review must replay the real chmod and foreign-output cases and inspect raw OS
receipts/counters. No mocked mkdir/dump-only test substitutes for them.

## Preservation and re-sealing sequence once authorized

Archive all72 frozen proposal files, original71 seals,363 source pins, full old
checks/failures and the complete eventual sealed review with explicit path-only
copy receipts before editing current proposal. Archived Go/Python source must be
inert .go.txt/.py.txt so Go discovery/import does not execute historical copies.
Verify each original SHA/size/Git blob against d5c7874 and mapped destination;
original manifests retain original contents/paths, explained by the copy map.
No original was run and no old private accounting object exists; do not invent
spent guests or a budget reset. If accounting schema/path versioning is needed,
freeze it explicitly in the successor proposal with old0/new<=8 and historical46
13 unchanged, rather than silently resuming the old unexecuted source identity.

Change only owned51 entry/accounting/report helpers/tests/evidence. The exact H1
source, eight native/frame/operation hypotheses, binary/producer, actual decoder,
all72 facts, Go source, approved helpers and original resources remain unchanged.
Run the focused entry OS matrix, impacted Python/public CLI/strict routing tests,
compile and meaningful accounting mutants, then regenerate current plan/source/
preflight/pins/seals and commit owned files. Existing Go/race/configured results
remain source-bound; no unchanged Go/PTY/fuzz budget or guest is repeated merely
for this bookkeeping repair. Source-pin changes may require current Python plan
checks; independently review the successor before ANY root grant.

No implementation/lifecycle/primary/private-owner/VM changes are authorized by
this plan. Root authorization after the sealed review is the next boundary.
