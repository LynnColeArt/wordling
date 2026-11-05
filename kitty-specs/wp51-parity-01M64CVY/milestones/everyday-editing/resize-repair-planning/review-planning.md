# Independent WP90 corrective planning review — APPROVE

Reviewer: `/root/everyday_baseline_audit`, independent of proposal author and WP90 implementer.

Approved exact patch SHA-256: `adadd1328f8be4a3a71dc0d2eacf18a72858c7cfd7e91a21af08a88d29d19858`.

The proposal preserves the rejected WP77 verdict and its original safety gate. It adds a narrowly scoped corrective WP90, not audit-only acceptance of an unsafe product. WP90 may consume the explicitly identified unreviewed candidate only to reproduce and fix R77-001; its independent approval covers its repair delta, never the rest of the candidate. Ordinary downstream work remains gated by WP77/WP78.

## Verified scope and delivery

- WP90 owns only `internal/tui/model.go`, `internal/tui/historic_resize_test.go`, and `internal/tui/evidence/resize-modal/**`. The code defect is in Model dispatch; a coherent fix is feasible within this scope. Any necessary wider production change requires reviewed amendment.
- Red/green public Model tests must cover both F5 and Alt+=, 12/11 boundaries, restoration, native bytes/revision/history, actual rendering and focus return. A compiled CLI/PTTY resize path and ordinary terminal cleanup are required. Existing I/O/session guards must remain operative.
- Corrected T297 explicitly excludes consumption or import of rejected WP77 probes into H. It uses actual issued source suites and its own owned CLI probe. Full WP77 probes run after reviewed repair intake.
- WP77 retry preserves all original 23 candidate path hashes and verifies the complete inherited delta. Only exact paths changed by the independently approved repair may differ from c7, and those must equal the approved repair source. New repair tests/evidence are separately inventoried. An explicit reviewed intake receipt binds repair review, source commits, integration parents and actual retry ancestry. General path exceptions and source overlays are forbidden.
- The former no-bypass report must be corrected, original rejection remains durable, and WP77 independent review verifies the repaired complete source and closure before ordinary consumers proceed. Neither WP90 nor source intake constitutes M1 acceptance or preview authorization.
- The malformed WP85 table row found during review is corrected: WP85 depends on WP84, which depends on WP83, WP76 and WP90.

## Independent validation

Using a fresh installed Spec Kitty interpreter, independently read all canonical prompts with exact proposed file overrides, resolved typed frontmatter ownership, ran `validate_all`, `validate_glob_matches`, and full `compute_lanes` including exact proposed task bodies. Result: 90 WPs, 30 acyclic lanes, zero ownership/glob errors, no changes to any of the 89 current or 76 historical memberships. WP90 computes to existing lane-h; prerequisites are WP76 only; WP84 adds WP90; WP77 has no reverse H edge. `git apply --check planning.patch` passed. This is read-only planning proof, not a runtime claim or lifecycle mutation. Canonical finalization/claim and identity checks remain required.

Independent result and file hashes: `independent-validation.json`.

## Exact proposed file hashes

- `kitty-specs/wp51-parity-01M64CVY/milestones/everyday-editing/decisions.md`: `d6e55e539ad44dbd6d04496869727c9c14bca8ef6f0f52440c46e70c98257cdf`
- `kitty-specs/wp51-parity-01M64CVY/milestones/everyday-editing/plan.md`: `2d5eeba075f6df73d41ebf2af335fe58df0b3e5056ea21fe5b30d60fc8327f4e`
- `kitty-specs/wp51-parity-01M64CVY/tasks.md`: `21fcfd6abcd1f06aba37ad5504d8d1f5407d493bdb65630918d6cef5d870ab7e`
- `kitty-specs/wp51-parity-01M64CVY/tasks/WP77-everyday-baseline.md`: `284b96dddc70569a0c67027eb432f7a01af01992cb563dd4944a5be02309d2e2`
- `kitty-specs/wp51-parity-01M64CVY/tasks/WP84-everyday-editor-ui.md`: `4f934b69611bb28fbc6d0509003c1cd268e5d74094b4a2961e375adcf332c408`
- `kitty-specs/wp51-parity-01M64CVY/tasks/WP90-resize-modal-safety.md`: `919b0f0f885b5a42210f7c8fdff35552b8d169d8eac52979cb43798e3ddd840b`

No repository, source, status, lane, approval or git mutation was performed by this review.
