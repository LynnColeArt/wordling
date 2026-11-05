# WP68 cycle1 narrow correction — pending independent re-review

F1 is corrected in account.consume: genuine update permits must match the SAME
account's current operation and issued sequence and exceed its durable committed
sequence BEFORE consumption, encoding or filesystem effects. Issuing a later
operation supersedes an older outstanding update. Stale refusal sets InvalidPermit
and prevents later noncleanup operations; all reservation maxima stay spent.
ownership.write_json advances the account watermark only after validated exact
readback and journal charging. Ordinary sequential transactions remain useful.
F2 removes only unused PhaseReservation.observation; no consuming API was added.

The unfixed public RED is fix-cycle1-red: both stale orderings fail, ordinary
sequential succeeds. It uses the actual offline wheel, copied isolated interpreter,
public issuer/ParentLease/OwnedLedger and real descriptors; no synthetic book or
source import loader. Final source-level public unittest checks both orderings,
complete prior bytes/ctime, complete reservation retention, postfault refusal,
actual reserved closes and sequential exact independently encoded JSON bytes.
The existing repeat-use/copy/wrongissuer and all other functional categories remain.

The complete first corrected-source full campaign is history-archives/
fix-cycle1-final.tar.gz: WHOLE1/47PASS1FAIL; the contradiction was in the new
assertion after an expected refusal, not a changed product outcome. Exact original
610 files584606bytes plus79 directories are preserved with modes/paths/SHA,
prearchive manifest, bounded full roundtrip receipt and inert operator. Raw mutant
labels from that red baseline do NOT qualify a meaningful kill. Corrected-test-
static-review and failed original test literal record the one assertion removal.

Only fix-cycle1-final-r2 qualifies the current source/test roster: WHOLE0,
48PASS0FAIL categories (51 logical functional controls), nine current semantic
mutants KILLED against a green baseline,7 configured checks PASS0SKIP. It completed
in48.897347951s under unchanged300s. Four permit subcontrols share the original
ONE30s/2MiB case; the three added ordering unittests do not reset either limit.
Their full combined output and actual elapsed time are in acceptance-summary.json.
The new sequencing mutant is compile-valid and reaches STALE_UPDATE_BOUNDARY;
old forge-permitguard mutation remains historical, not silently relabeled.

Sourcecatalog65118/65536bytes. Frozen-source-readback verifies every production
and harness input unchanged after the fresh campaign. Source-lint-and-F2 retains
successful compile-without-import/cache checks. All baseline protected paths and
historical namespace members are checked separately. The original root seal is
literal; its original1381 members verify against exact immutable rejected commit
df651f7b94a708e9b0ec7687499544af97b0e089, never a recomputed transformed old seal.

archive-and-index-census.json distinguishes physical evidence, ten complete runtime
archives (4242 logical files3796308 expanded bytes) and two separate finite metadata
indexes. Metadata-index expansions are not hidden as runtime archives. All prior
failure/UNKNOWN/loss history remains; missing02 child streams stay unavailable.
No failed grant is repaired, reused or reconstructed. Same finite source/runtime/
evidence caps remain. No old51/55/57/Go/provider/canonical/private/original/VM/source
changes; production original entry remains blocked. Foundation is not run_leaf,
M1 remains OPEN, M2/PDF remains GATED. No selfapproval or lifecycle transition here.
