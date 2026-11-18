---
type: explanation
updated: 2026-11-18
---
# WP103 tooling repair plan — independent architecture review

Audience: Spec Kitty core engineer and the Wordling mission orchestrator.

**Verdict: REQUEST CHANGES — two bounded contracts must be explicit before implementation.** The proposed planning-stage partition and explicit manifest-v2 refusal boundary are appropriate for the diagnosed defect; there is no request for a different scheduler, topology, hosted protocol or broader tooling project. Resolve the mixed-mission planning propagation and the precise finalizer prewrite cut below, then the revised plan is suitable for a narrowly scoped isolated repair. This is a plan review, not code approval or rollout authorization.

Reviewed `/tmp/wordling-mission1-closeout-20261118/wp103-tooling-fix-plan.md`, SHA256 `158d118e1006662223c49f6790e47ae2f94c8c08f8029300a25286393333f440`, against the retained exact cycle diagnosis/reproduction and frozen source `b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3`. No source/index/Git/runtime/lifecycle/grant/remote/VM/Mac mutation occurred. No Op was dispatched in the frozen clone.

## Governance and review boundary

Applied the resolver-loaded Architect Alphonso profile: architectural decisions, component boundaries and testable implementation feasibility; no implementation code. Profile and action-review capsules are `wp103-review-profile.json` and `wp103-review-context.json` beside this report. Read the frozen clone's complete `AGENTS.md`, canonical governing `/home/lynn/projects/spec-kitty/.kittify/charter/charter.md`, relevant execution-lanes documentation and recorded-planning-commit ADR. The ordinary source clone has no materialized governing charter, so resolution used the existing canonical Spec Kitty project rather than creating one or editing activation state. Resolver commands were read-only and source-pinned, with per-invocation local mode; no dispatch/registration/installation was run.

The charter requires single authority, smallest viable seam changes, independent review and separately committed failing acceptance tests before implementation. Existing architecture prose contains stale older lane/dependency claims; source and retained exact reproduction govern this review. Do not treat those stale claims as instructions to restore dependency-based ownership collapse or weaken the real cycle guard.

## Confirmed design fit

The diagnosed graph is valid at WP level. Unconditionally equating early planning with downstream WP103 creates the false quotient cycle. Separate dependency-ordered planning scheduling vertices, sharing one canonical PRIMARY/root placement and explicit target branch, are the smallest honest model correction. Relabeling WP103, deleting its WP86 dependency, filtering approved work, changing old histories or suppressing cycle detection would not be equivalent.

The proposed stage recurrence is sound for the specified class: planning→code preserves stage, code→planning increases it, and planning→planning preserves dependency order. Hence a path that leaves a planning vertex through code and reaches another planning vertex cannot put both in the same stage. Keep the actual final quotient-cycle/depth checks anyway. Existing code-owner contractions that are cyclic even with singleton planning must continue to refuse; splitting code ownership is a separate problem. The minimal three-node and exact retained103 tests, permutation/determinism and nested-stage examples are the correct contract surface.

Typed lane mode is warranted because `ExecutionLane` currently has no kind and `is_planning_lane()` recognizes only one literal ID. The planning summary must remain derived, and actual WP kind/membership must govern mode. Secondary planning IDs must never be treated as code merely because a caller has only a string. Preserve existing code lane IDs/groups and v1 bytes for the single-stage cases; do not broaden this repair into legacy code-ID grammar cleanup.

The proposed v2 encoding is a real compatibility boundary. An in-memory probe of the **actual frozen** public `LanesManifest.from_dict` confirms: version2 without `lanes` raises `KeyError('lanes')`; version2 with a legacy empty `lanes` list silently succeeds. `read_lanes_json` translates that KeyError to CorruptLanesError. Thus merely adding version/mode fields or emitting dual lists is unsafe. Required no-legacy-list v2 plus a strict new version switch is appropriate. Implementation still needs the planned real reader/allocator negative tests and prewrite unsupported-hosted check; this source probe is not future-code validation.

## Required change 1: preserve mixed-mission planning content propagation

**Actual boundary:** `merge/executor.py:448` skips planning consolidation only when the entire mission is planning-artifact-only. In a mixed mission it resolves the explicit planning target (`:470–489`) and calls `lanes/merge.py:234–259` to incorporate that root branch into the mission integration branch. Cleanup separately excludes planning (`executor.py:1660`). Those are different responsibilities.

The plan's statement that only code branches retain consolidation, with planning stages already at root, is underspecified and can accidentally delete the existing mixed-mission propagation path. Sharing placement does not by itself prove that the mission integration branch contains a late planning amendment. This also affects resumable integration bookkeeping (`any_lane_had_unintegrated_code`) and what is actually frozen in a mission-branch candidate.

**Add an explicit minimal contract:** planning stages never allocate, rebase, delete or invent stage branches. For mixed missions, preserve the existing incorporation of canonical planning-root content into the integration branch, idempotently once for that shared target/source rather than redundantly once per scheduling stage. A target already equal to the destination/current root must be a no-op with no self-merge. Planning-only behavior stays unchanged. Do not introduce live moving-tip semantics into the recorded `planning_commit_sha` allocation contract; distinguish integration-time planning propagation from lane-allocation ancestry.

**Acceptance:** a real temporary Git fixture with distinct target and mission integration refs, early and late planning commits and code lanes. Assert the integration candidate retains required late planning content, normal final target integration preserves it, no synthetic stage branch/worktree or root deletion occurs, and retry/resume is idempotent. Include target==destination and planning-only counterexamples. Preserve review/lifecycle/acceptance gates. If the intended design deliberately changes existing propagation instead, it needs a separate explicit rationale and equally concrete content/ancestry proof; silent removal is not a minimal fix.

## Required change 2: locate the pure preflight before every existing writer

**Actual boundary:** finalization currently validates the WP DAG before writers, but lane/schema computation is much later. `mission_finalize.py:3505+` persists the branch contract, then issue-matrix scaffolding runs; `:3556` flushes WP frontmatter, `:3561` can regenerate tasks.md, and `_run_commit_pipeline:2969–2980` emits local events and bootstraps canonical status **before** `_compute_and_write_lanes` computes the lane graph. Putting new-stage/sync/schema refusal only inside that compute/write helper is too late for the promised unchanged-state failure contract.

The proposal correctly requires zero writes on graph/schema/unsupported-hosted error, but must identify this phase cut rather than leave an implementer to infer a generic transaction rewrite.

**Add an explicit minimal contract:** prepare eligible metadata/ownership/body/dependency inputs using the existing read-only/in-memory projection, compute and validate the final typed manifest and supported local/hosted mode before `_persist_branch_contract_for_finalize`, issue-matrix scaffolding, frontmatter/tasks writes or local/canonical event emission. Both validate-only reporting and application consume that same prepared validated result. Commit-phase SHA capture/refresh retains its existing authority and guards; revalidate volatile identity/ancestry as required without inventing a second scheduling authority. No generic repository transaction subsystem or rollback of unrelated state is needed for this repair.

**Acceptance:** exercise the real finalizer with a true lane-cycle fixture, malformed/unsupported v2 input and hosted-active multistage refusal. Snapshot prompt bytes, tasks/index/manifest/meta/matrix files, status/event bytes and Git refs/index before invocation, asserting exact identity after each refusal. Run a valid local multistage finalization through the same entry point, and compare its prepared manifest with validate-only output apart from declared volatile timestamps/commit provenance. Existing old99 histories/prompts remain unchanged in the isolated exact103 fixture. Negative tests should observe actual effect seams, not monkeypatch graph success or merely assert that lanes.json was absent.

## Consumer scope and remaining review gates

The plan's identified consumer set is justified by source, not an excuse to edit every listed file:

- `lanes/models.py`, `persistence.py`, `compute.py`: mode/stage invariants, strict version adapter, acyclic complete assignment and atomic persistence.
- `branch_naming.py`, `workspace/context.py:788–895`, `ownership/workspace_strategy.py`: actual stage ID/members must survive resolution, while PRIMARY root is resolved canonically from root/code/coord CWDs. Current planning return arms overwrite IDs with PLANNING_LANE_ID and one helper simply returns its supplied root.
- `worktree_allocator.py:221–242,443+,712–728,819` and `lanes/implement_support.py:374–420`: prediction/allocation and approved dependency ref lookup must consume typed context/explicit target, not guess a stage branch or silently fall back to `main`. Retain real approved/done readiness, recorded planning SHA, base/refusal, dirty worktree, identity and merge-conflict guards.
- `stale_check.py`, `lifecycle_sync.py`, actual auto-rebase/for-review callers: semantic planning skip, without suppressing status or dependency gates. No need to modify unrelated file-conflict resolution internals just because the module name appears in this checklist.
- `merge/executor.py`, `lanes/merge.py`, `merge/forecast.py`: all stages included in scheduling/status/review diagnostics; shared-root propagation preserved as above; no stage allocation or cleanup of target/root.
- `mission_finalize.py`: prepare/validate before effects, one validated computation shared with application, unchanged normal lifecycle and planning-SHA decisions.

Branch parsers accepting code-lane names do not need to recognize synthetic planning-stage branch names: such branches must never exist. Prove refusal for contextless secondary-stage string calls instead of expanding branch grammar. Raw-manifest search found canonical `models.py` as the direct `data['lanes']` reader in the inspected CLI/runtime sources; retain/strengthen that single authority rather than adding consumer-specific JSON adapters.

Keep the proposed separately committed RED acceptance sequence and fixed aggregate GREEN independent review, scoped pytest/lint/strict typing/new-branch coverage and affected non-vacuous architecture gates. Do not install or replace frozen b45 during WP104. The amended plan may authorize only an isolated source repair after root review; live held103 remains unregistered until a reviewed candidate passes real dry-run preservation checks and ordinary finalization.

## Source identity

Frozen inspected source hashes match the plan: compute `84927ad5ce621140c86f40ba0ea3b5a6049dd92783749f86e565bd17c5df4bb5`; models `11b939957990c677afbaf7fe5a4c9a9ef1c5395d8e58a25e3bd7bef15ef39b3f`; persistence `25a30363d4aa945581e67072dfb2e267d244e4ee5d9447615b4439370c780a2b`; branch naming `45a24e3004ba46f082a3037d046bbe9da39f243dfbb1f2429e0b70c190d2c874`; workspace context `5a15f5456718ab9260b3d8f6c53cd57f94ec9e5e26c24ec57bd99cfb26ebf0c4`; finalizer `357dc338029fbddd06f7caef716a32c930d62e0a2b980611758bac222c77aafb`. No implementation, test-suite run, live registration or other effect accompanied this review; only the documented read-only resolver calls and pure in-memory old-model probe were executed.

## Revision recheck — current verdict APPROVE PLAN

2026-11-18. Rechecked the exact amended plan SHA256 `f64ea3de5e8e4b9de41172a856d6098a0a75c620ebe3c91c31a274d1ae85eb31`. **Both initial findings are resolved.** This current verdict supersedes the earlier request-changes verdict for that revised plan only; the initial review above remains preserved.

R1 now explicitly preserves canonical shared-target content propagation into a distinct mixed-mission integration branch once/idempotently, distinguishes it from the frozen allocation SHA, and names actual temporary-Git late-content, same-source/destination, already-contained, resume, conflict, planning-only and cleanup counterexamples. No stage branch or root self-merge/deletion is introduced.

R2 now names the exact cut after eligibility and WP-DAG validation and before branch-contract persistence or any matrix/prompt/tasks/event/bootstrap writer. It uses the existing genuinely writer-free `_run_bootstrap_loop` projection (source1566–1700 defers disk changes to pending writes), normalized ownership/frontmatter/body inputs and one immutable prepared validated result shared by validate-only/application. Input identity changes refuse before effects; volatile checkout/ancestry and existing planning-SHA capture/refresh guards remain. Actual public finalizer failure snapshots include refs/index, metadata, prompts, regenerated tasks, matrices and event/status bytes, including would-change inputs so the no-effects proof is meaningful.

The amended proposal is bounded and actionable at the stated source/model/workspace/allocator/merge/finalizer seams. No remaining plan blocker was found in this finite recheck. This approves **an isolated implementation plan**, not implementation, tests, installation, active-CLI replacement, hosted support, WP103 registration or mission acceptance. Those retain the plan’s separate RED-first, aggregate GREEN, independent review and normal guarded rollout requirements. Active frozen b45, Wordling source/index/runtime and existing histories remain untouched. No Op, new test suite, original/VM/Mac or remote operation accompanied this recheck.
