# Local Spec Kitty lane naming repair

Installed Spec Kitty 3.2.7 generated punctuation after lane-z, which its identity parsers could not recognize. This independently reviewed four-file patch adds bijective lowercase suffixes and updates the branch identity, legacy merge, and ownership guard consumers. It preserves existing a–z identities. No Wordling source or lifecycle state was changed by applying the patch.

The exact installed before/after hashes are in manifest.json. Independent approval is in ../review-tasks-1.md. Originals are retained at /tmp/wordling-kitty-lane-repair/before on this host. Fresh-process installed verification passed using the installed tool interpreter and check.py --installed: 10,000 unique suffixes; 1/26/27/29/52-lane allocations; legacy and modern branch round-trip; commit guard recognition; malformed and reserved-suffix exclusion. The check without --installed uses the prepared after tree in that temporary directory.

The complete 89-package graph was independently evaluated with the prepared modules, preserving all old 76 memberships. Actual canonical validation and issued claims remain required. This is a local tooling repair, not an upstream release claim. A subsequent Spec Kitty installation can replace it; verify hashes before relying on the extended suffix support.

## Optional synchronization queue recovery

Initial canonical78 finalization seeded WP77/WP78 durably but became CPU-bound publishing dossier artifacts into an existing full 100,000-event queue. Independent read-only diagnosis identified repeated SQLite COUNT scans per rejected event. The owned CLI process was gracefully interrupted; both genesis events and old approvals were retained. The same canonical command completed successfully with the supported per-command `SPEC_KITTY_SYNC_DISABLE=1`, which disables optional synchronization fanout and dossier capture while preserving local lifecycle authority. No pending events were deleted, and consent/authentication were not changed. Use this environment setting for this local implementation/review run.
