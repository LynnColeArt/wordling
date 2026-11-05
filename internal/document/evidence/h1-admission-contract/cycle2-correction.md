# WP51 prelaunch cycle 2 — offline correction, not a guest grant

Current authority is this correction, the successor plan/preflight and cycle2-seals.
The old working-and-Git-seals/checks remain unchanged historical cycle1 evidence;
they do not describe the modified entry source. Full cycle1 proposal72, all363
actual pinned Git payloads and39 sealed review artifacts (plus review seal) are
byte-exact mapped inert copies under history/prelaunch-cycle1. Copy receipts bind
original paths, Git/source hashes and renamed .go.txt/.py.txt destinations.

R1: accounting.py atomically claims the declared private ledger O_EXCL/no-follow,
retains the actual descriptor/inode and fsyncs it before source check, public
mkdir, configure or physical lock acquisition. Existing accounting always refuses,
including empty/partial claims; there is no resume. All updates use the same owned
descriptor with identity checks/readback. Foreign/busy/symlink accounting and
foreign output remain untouched. Public reports require separately exclusive
output/file ownership; cleanup never mkdirs or writes merely because output exists.
Authorized owned zero-guest failures halt through the owned descriptor even when
public output is unwritable. Actual unpersistable writes are explicitly reported
non-durable; their retained claim still prevents reuse. Failure to create ANY
accounting object reports AccountingUnavailable before configuration and requires
ROOT intervention, never a claim of persistence or automatic retry permission.

R2: one logical owner/root reservation spans exactly8 ordered leaves. Each leaf
reacquires the actual physical exclusive context, performs fresh-start/runtime
interaction/normalDOS/positive owned stop/socket proof/stopped exports/master check,
then exits that context and immediately prints a safe/unsafe physical release
receipt. Only then does readonly raw frame/stop/72-field/family/repetition audit
run. Prior qualified result/ledger/raw/source/tool checks precede NEXT. A failed
qualification stops at that leaf. Unknown stop, missing exports or bad master
cannot claim a safe oracle release; context-exited is a separate fact and root
reservation is retained for diagnosis. No helper/lock implementation was changed.

cycle2-checks/offline-final.xml:46 actual integrity tests,0 failures/errors/skips.
Real UID1000 chmod0500, actual O_EXCL/flock child contention, foreign/symlink/busy
preservation, inode replacement, RLIMIT_FSIZE write failure with retained empty
claim/restored-retry refusal, unpatched check source drift, and second-descriptor
physical-lock state during guest/audit/reacquire are exercised. Bounded fixture
check/configure/guest/qualify seams isolate these OS tests; they are not originals
or full native observations. Original replay failures are retained in the sealed
review archive. New OS tests directly reject those old outcomes. The initial
RLIMIT test also limited its redirected regular stdout file; that failed log is
retained. The corrected test captures stdout in memory, leaving actual ledger
write failure unmocked and asserting HaltPersistenceFailed/non-durable exactly.

Five focused R1/R2 in-memory source mutations are killed by these actual-OS tests;
all nine retained native/frame/accounting guard mutations still die. Current
Python compiles. Actual Go discovery finds the same10 packages; historical source
archives introduce no Go packages. Go core/probe/binary/module, all4135 protected
files and all source/frame/native hypotheses remain exact. The previous real
configured7/race proof and compiled probe776a173d... remain valid immutable source-
bound evidence; unchanged Go/PTY/fuzz budgets were not repeated for Python entry IO.

Zero original guests, no real private owner/ledger or physical guard, no VM/root
grant, primary/canonical/lifecycle changes or native admission permission. The
successor tooling JSON schema is v2; original native formats remain unchanged.
Exact same8 IDs/cases/initialH1/modes/frames/finite family vectors/failure cap8 and
historical46 count13 persist. Any future launch still needs independent cycle2
prelaunch approval and a separately issued exact ROOT grant. Full38/91/36/nested/
SC001–005 M1 is open, B blocked, M2/PDF not started.
