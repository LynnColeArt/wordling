# Independent continuation amendments R2–R4

Reviewer Renata; 2026-11-18. Review against Wordling HEAD `d593901289f115aee8055875c67e32dc15c66b96` plus the identified uncommitted authoring amendments. No production source, canonical runtime, approval event or package state changed by reviewer.

**APPROVE R2 dependency serialization, R3 exact portability metadata relocation, and registration of WP100–102 only through the normal finalizer.** No implementation/VM/acceptance approval is implied. WP103 remains unregistered, retained full-M1 work.

## R2 — explicit predecessor order

The original official diagnosis lists the precise historical overlap owners. WP100 now follows WP69/71/73/76 (broad TUI ownership) and WP84/85 (existing New-macro regression ownership), retaining WP65/66/82. WP102 adds WP86 (everyday qualification namespace), retaining WP100/101. Production/test ownership, create-intents, bodies and acceptance criteria of the new packages do not widen.

Independently verified the complete authored graph is acyclic (103 packages before holding WP103, 102 packages after), every referenced ID exists, and every inherited predecessor of WP100–102 is approved/done in the authoritative event log and agrees with the materialized snapshot. The added edges point from new work to already delivered historical work; they serialize genuine overlapping owners rather than bypassing overlap checks. The canonical pure ownership validator passed for all 103 manifests with the amended dependency graph before the registration subset was narrowed.

## R3 — preserve history while locating current ownership

Verified each of the six old→new storage paths against the actual Git rename entries in `27ebe5ee9bcf17b450fe27fca3a2e344fe35694f`; each target exists and each obsolete Linux-only source path is absent. WP79/91/98 diffs alter only `authoritative_surface`, `owned_files` and/or existing `create_intent` path references through those exact relocations. No dummy files or unsupported creation claims were added.

For all three prompts independently verified full before/after SHA-256, archived originals matching the original preservation baseline, exact body equality and recorded body hashes (body bytes after the closing `---\n` marker). The complete after file equals the original with only those metadata substitutions. Canonical event log and materialized approval snapshot remain byte-identical to HEAD.

**Updated preservation guarantee:** all 99 historical prompt bodies and canonical approval/history events are unchanged. 96 prompts remain entirely byte-identical. WP79, WP91 and WP98 have three explicit current-authoring metadata relocations, with exact original files archived and old/new/body hashes in `portable-ownership-amendment.json`. This supersedes the earlier blanket claim that all 99 entire current prompt files remain byte-identical; it does not rewrite what an old approval meant or claim those approvals reviewed future edits.

Reviewed current prompt hashes:

| Prompt | SHA-256 |
| --- | --- |
| WP79 | `6d97e5df6f6949737c2963e7cf8b6349013d4bca379c4b1884f33a69e9e08a1d` |
| WP91 | `c68d911d380df736d9929988f59c42ee2bd23e1e6ee8ae1a9a68b52eb36f06f3` |
| WP98 | `9cd97ee4d40f2f3de40c6c9bba6011f3f3f6f8411e58a9d7ee984a63274bbd81` |

## R4 — truthful three-package registration

Read `registration-scope.md` and the normal finalizer's R3 lane-cycle refusal. Holding only the untracked/unregistered canonical WP103 draft is a sound bounded sequence: the complete proposal and full coverage-index deliverable remain under the continuation record, execution_mode remains planning_artifact, and no official WP103 state/completion is created. Acyclic authored dependencies were not rewritten to pretend lane aggregation succeeded. The remaining full-M1 families and acceptance gate stay in force. WP103 requires an honest later planning-lane/owned-workflow resolution; completing WP100–102 cannot close its work or M1.

Read the R4 dry-run result (not rerun): `finalize-continuation-diagnose-r4.json` reports `validation_passed`, 102 total WPs, 3 newly seeded / 99 already initialized. It proposes branch_strategy normalization only for new WP100–102; the finalizer lists all historical99 unchanged. The three zero-match evidence-glob warnings refer to declared new evidence namespaces, not missing existing production paths. No forced flag, fake kind, old dependency rewrite, approval replay or gate skipping is used. Computed lane metadata is not a worktree allocation; the already reviewed explicit owned-checkout execution protocol remains required.

Independently confirmed the original tasks.md prefix remains byte-identical, canonical new prompts match continuation copies, WP103 has no canonical task file and its continuation proposal/kind is retained. R4 has passed the actual normal validation gate; root may commit the reviewed authoring inputs and invoke the normal finalizer. Inspect its real output and preserve all gates if a later state change causes refusal.

## New prompt content bindings

| Prompt | SHA-256 | Dependencies |
| --- | --- | --- |
| WP100 | `4edb0e710de735e639d332199d3e03ff13fbf1cecac494358ba7f4dc67efadb5` | WP65,WP66,WP82,WP69,WP71,WP73,WP76,WP84,WP85 |
| WP101 | `b8a8f6d99db2ef069d05bcb5f440cba2e0000fcf055c67137bf23d5891a5b4d2` | WP38,WP63,WP64,WP70 |
| WP102 | `fc0fb1138bc5b649ce60a316ca518821a81a97048460ff168f244fc3e52aedf6` | WP100,WP101,WP86 |

Normal finalizer branch_strategy normalization will change those whole-file hashes; retain these input hashes and bind the actual finalized output separately. It does not authorize production scope or acceptance changes. Earlier independent source/acceptance review, R1 test updates, authentic original-route requirements and four partial audit-row restrictions remain binding.
