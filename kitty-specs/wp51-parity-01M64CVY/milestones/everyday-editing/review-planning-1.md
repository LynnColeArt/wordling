# Independent everyday-editing planning review

Verdict: **APPROVE** after focused amendment review. The initial verdict was REQUEST_CHANGES; its findings are retained below for traceability.

Reviewer: `everyday_baseline_audit` (independent of the planner). Date: 2026-11-05.

Reviewed `spec.md`, `plan.md`, `acceptance.md`, and `decisions.md` against the project charter, permanent compatibility contract, integrated H source baseline and installed Spec Kitty 3.2.7 implementation. This is a planning verdict; it is not an implementation approval, lifecycle transition, or full-M1 acceptance.

## Resolved findings from the initial review

### EE-PLAN-R1 — Separate baseline integration from code-claim placement

`decisions.md` D-EE-02 describes bringing H source into the feature target and establishing its canonical owned checkout, while `plan.md` leaves the source/branch workflow unspecified. The installed runtime supports owned-root planning finalization but does not make that root the execution workspace for code packages. `specify_cli/lanes/implement_support.py:create_lane_workspace` runs `planning_artifact` packages at the repository root and allocates/reuses a lane for every `code_change` package. Metadata `single_branch` does not bypass that code allocation path. `resolve_owned_mission` also refuses H as an owned finalization checkout because its branch differs from `meta.target_branch`.

The amendment must explicitly keep code claims on their canonical issued workspaces. If ordinary git integration of a pinned H snapshot into the feature target is selected, describe it as a separately authorized source-baseline operation, with named root and H checkpoints, captured status/approval identities, preflight of the actual merge inputs, and post-operation preservation checks. It must not be presented as Spec Kitty full-mission `accept`/`merge`, and must not imply that source presence at root changes code execution placement.

Task finalization must also preserve the identity of existing execution lanes. The installed finalizer recomputes all lane groups from ownership. A new package owning document, editor, and TUI paths can union their existing groups and renumber later lanes; sequential execution alone does not prevent this. Require canonical validation and inspection of the computed map before execution, split production ownership along stable existing boundaries as necessary, and stop if a proposed mapping silently changes existing worktree identities. Exact new lane names may be discovered during supported finalization; this review does not prescribe guessed metadata or handwritten lane assignments. No existing approval or topology field should be changed to bypass this gate.

The initial read-only comparison found no overlapping changed paths between committed feature HEAD and H HEAD since `b7f58493d37110e2218b7f3c6fb6c7471206891e`. This is useful evidence, not an approval of a later merge after new checkpoints. H contributes approximately 98,231 changed paths, predominantly historical evidence. Record and check that footprint rather than treating it as only the 23 preview source files. Preview approval must explicitly cover the candidate delta after `f89a48627916b5cb9e360c35047350031b6f06a9`; WP76 approval does not cover it.

### EE-PLAN-R2 — Include original backup behavior in repeated-save acceptance

EE-A11 and EE-A13 thoroughly cover replacement, cancellation and failed publication but omit backup behavior. FC-009 explicitly includes original backup conventions, and the charter identifies original backup/recovery behavior as M1 functionality. A milestone claiming faithful repeated publication under EE-011/EE-013 needs an explicit reference outcome for backups rather than silently replacing the current file only.

Add WP78 observations for the selected original backup setting and relevant enabled/disabled variants, and add save acceptance for backup naming/content after first and subsequent replacements, canceled overwrite, and publication failure. Test the configured reference default and disclose the selected Linux mapping. Where backup/recovery modes remain outside this milestone, enumerate those exact open modes and do not claim their FC-009 coverage; the selected everyday replacement behavior still needs complete evidence.

## Positive findings

- The milestone stays inside M1 and leaves full parity acceptance and M2/PDF closed. It does not turn a useful subset into a parity claim.
- The new/saved/retrieved and two-screen matrix directly addresses the application’s actual lineage guards, save continuations, uneditable clear state and bounded attribute authoring.
- The native revision, document layout and viewport separation is appropriate. Full justification, real physical positions, soft-return semantics, original-format preservation and original interoperability are explicit gates.
- The acceptance journeys exercise menu focus, original key families, Help, Reveal Codes, search, browsing/Look, repeated saves, Doc 2, failure handling and one uninterrupted real-executable journey. They avoid helper-only completion evidence.
- Menu visibility is an original preference rather than a new shortcut scheme. Historical context-disabled commands are distinguished from implementation gaps.
- Original observations are repeated before adoption. Cell attributes and next-key focus probes are correctly required where screenshot text alone is ambiguous.
- Independent review is required per package and again for the actual delivered binary. The package table can be split during task authoring without changing the product scope.

## Approval route

Focused rereview completed on 2026-11-05. D-EE-02 now separates optional ordinary feature-branch integration from canonical code-workspace allocation, requires capture and preservation of existing WP-to-lane/worktree and lifecycle identities, and requires splitting new ownership rather than silently coalescing old lanes. This resolves EE-PLAN-R1 at the planning level; the exact canonical task mapping and source checkpoint still require execution-time verification.

EE-011, EE-A11, EE-A13, the lifecycle package description and D-EE-11 now require enabled/disabled original backup observations and preservation through replacement, cancellation and failure. This resolves EE-PLAN-R2.

The product plan is approved for task authoring and canonical finalization. Package splitting/reordering to respect existing ownership is permitted by the plan and does not change the approved product scope. Source/package implementation may begin only after normal task finalization and the issued claim, with the actual allocator outcome checked. This approval does not approve the unreviewed preview source, a particular ordinary git merge, existing package changes, or all of M1.

Reviewed artifact SHA-256 values:

| Artifact | SHA-256 |
| --- | --- |
| spec.md | ef69cc3510c3210db9fe2f28dcb9044884a7dc0b3d2fcd6ae8fe19d7ab20de5a |
| plan.md | 3a87305e8a1089f5f30aaf06ac299d86ecf61779d5383adb8d338afff834ff24 |
| acceptance.md | cdbe2f7c9d66df1693324feb0cc4273c65e3648d2d988fd6a8393b233deec52a |
| decisions.md | d14f3d4d7067501e26304c0b1d066698d08fc23159f7b76cbb3868920c97cdb4 |
