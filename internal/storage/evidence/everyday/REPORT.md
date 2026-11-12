# WP79 everyday storage implementation — independent review pending

Source base: `cf9b2af5d0cdb4cb85a22c74c8e9ca9ef54bbb46`, issued lane B.
The approved WP77 `d55067a6`, WP78 `d6b24d3f`, and WP90 `78a05497` are actual
ancestors, verified with `git merge-base --is-ancestor`; no source overlay,
cherry-picked test dependency or replacement checkout was used. Full IDs,
approval events, changed-source hashes and reference hashes are in manifest.json.
The final source commit is the commit containing this report, not a self-approval.
Only WP79-owned storage files and this focused evidence directory changed.

## Delivered APIs and requirement mapping

| Task / criterion | Implementation and observable check |
| --- | --- |
| T239; EE-A10 browse/acquire | OpenWorkspace pins C root; Navigate/EntrySelection.Enter acquire child/parent locations; ASCII 8.3, case ambiguity, wildcard, symlink, confinement, bounded resources and Linux metadata mapping are explicit in README. Pinned-parent replacement test saves only into the originally acquired directory. |
| T240; EE-A10 Look/Retrieve | List returns copied metadata; selection captures original name/stamp and revalidates case ambiguity, inode/metadata and native read. Look acquisition leaves editor state to its owner; stale content cannot silently replace a selected snapshot. |
| T241; EE-A11/A13 save/reopen/exit | Prepared sourced/New saves admit edited existing destinations and Save As with explicit overwrite. SaveResult includes the actual acquired new Document and operation/revision. Repeated-save tests use this receipt directly. Cancel/default No do not stage or mutate. F7 continuation is the WP82 consumer, not a new storage special case. |
| T241; FC009 | Original backup first-save/rotation/disabled deletion/shared basename/Save As outcomes operate on complete old destination bytes. Tests compare actual original STAGE1/2/3 and BACK2/3 images, not body text. |
| T242; NFR conservation | Stale source/target/backup, changed case alias, symlinks, denied creation, short writes, file sync/close, backup staging, main/backup rename, directory sync, cleanup, pin close, concurrent writer rollback, single-use replay and concurrent Close have real filesystem probes. |
| T243 | Full Go checks, storage race checks, focused original outcomes and mutation test recorded; independent review must approve the complete contract. |

README is the authoritative API and failure contract. Old no-replace publication
callers and macro/native suites remain supported without weakened assertions.
The shared candidate writer is extracted, not replaced by a duplicate codec or
new byte format. Everyday replacement explicitly supersedes the old *product*
limitation through new APIs; tests asserting old APIs' bounded behavior remain
correct and passing.

## Original reference and byte evidence

The reference remains US WordPerfect 5.1 for DOS dated 03/09/92, approved WP78
profile in `docs/research/everyday-contract-2026-11-05/profile.json`.
Backup evidence is `backup/REPORT.md`, `backup/checks.json` and the stopped-guest
complete exports. Shared-basename/refusal evidence is in WP78-REPORT.md and
`qualification/files/`. No new virtual-machine run or unobserved failure behavior
is claimed by this storage implementation.

`TestEverydayMatchesOriginalCompleteBackupSnapshots` publishes the original
STAGE1, STAGE2 and STAGE3 bytes, compares BASE.BK! with original BACK2 and BACK3,
then uses the fourth original BASE image with backups disabled and checks removal.
`TestEverydaySaveAsBacksUpDestinationAndCollision` adds independent arbitrary
candidate bodies and a distinct old destination so a source/destination mix-up
cannot pass. The mutation probe intentionally backs up the new candidate instead
of the old destination; that test fails, and source is restored in `finally`.
Mutation evidence is in mutation.json. This is a test-quality witness, not a
runtime fallback or an alternate source tree.

The original 471-byte EVERY.WP and original-authored supplementary files
WP{WP}US.SUP / SPELLADD also survive exact publication/replacement. Opaque native
prefixes and bytes are conserved; storage does not authorize semantic edits.
No proprietary dictionary or program resource is added.

## Failure outcomes exercised

- Before mutation: overwritten-source/destination/backup observations, case
  ambiguity and symlinks refuse; canceled/refused requests preserve all bytes.
  Short write, denied candidate, file sync, writer close and backup-stage faults
  leave prior document and backup unchanged and clean owned staging.
- After document replacement: backup rename/remove or first directory-sync
  failure rolls back exact old bytes when transaction entries still match. Both
  backup settings and both prior-backup/absent states are covered. Retrying uses
  a freshly acquired source/target, not a stale prepared request.
- Concurrent external writer during backup failure: rollback refuses to overwrite
  its new destination, reports PublicationUncertain, and keeps the displaced old
  document in an identified recovery candidate.
- After durable namespace update: cleanup failure retains recovery material;
  final directory-sync or candidate-pin close failure does not return success.
  The newly published document/backup can already be present; the controller
  must inspect/reacquire instead of reporting overwrite refusal or clearing dirty
  state. A case alias appearing during publication is likewise uncertain.
- Same-capability concurrent prepared saves serialize: exactly one old-observation
  request succeeds; the other is stale. Close waits for an already-started
  transaction, cancellation reports false after start, and a closed capability
  cannot publish again.

There is no atomic multi-file or adversarial-directory claim. The document and
backup namespace updates are separate; crash recovery of retained candidates is
not implemented here. Safe rollback checks are observations before syscalls,
not Linux compare-and-swap against malicious same-user races. File and directory
fsync establish the stated local filesystem boundary. These limits are explicit
and tested failure outcomes are not presented as original DOS failure parity.

## Checks and remaining consumer gates

validation.json records exact commands, return codes and output. Build, full
repository tests, vet, formatting and diff checks pass. Storage tests run with the
race detector; the final focused run includes all added everyday cases. Existing
native reader, document, controller, TUI, baseline and macro tests continue to pass.
The charter Code Review Checklist query reported the section is not authored;
no out-of-scope charter edit was made. Sync was disabled only for optional Spec
Kitty transport via the supported environment variable, not consent/lifecycle.

This package is a foundation, not a standalone finished user feature:

- WP82 must route first/repeated save, Save As, F7 Save Yes, Doc2 and stale async
  completions through these receipts, preserving dirty edits on every failure.
- WP84 must map real F5 short/long navigation, selection, Look Next/Prev and
  retrieval to these acquisitions. A display row is never write authority.
- WP87 may use native supplementary storage, but dictionary/provider behavior
  is not implemented or qualified by WP79.
- WP86 must exercise the whole journey through the real executable and qualify
  it against the original. No preview is replaced and no mission is accepted here.

Unqualified backup-as-target self-collision is explicitly refused for replacement.
First save preserves a preexisting same-basename backup; original evidence does
not authorize deleting it. Timed recovery, full DOS filesystem/device support,
network filesystems, metadata/ACL equivalence, Fast Save and locking remain open
M1 obligations. These are not hidden stub behavior on the committed everyday
save paths or claims that the complete historical application is already done.
