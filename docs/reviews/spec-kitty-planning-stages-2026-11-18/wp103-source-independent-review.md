---
type: explanation
updated: 2026-11-18
---

# Planning-stage source review — REQUEST CHANGES

Audience: Spec Kitty core engineer and Wordling mission orchestrator.

Reviewed immutable candidate `43869ef858a58ae879345c19cd1cc1e4e1581514`, executable source `0b306189eb13daad297dec1994fa67a0474ee433`, against base `b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3` and approved plan SHA256 `f64ea3de5e8e4b9de41172a856d6098a0a75c620ebe3c91c31a274d1ae85eb31`. Reviewer differs from implementer. The actual `reviewer-renata` profile and review-action charter context were loaded; dispatch normalized its action to `audit`, Op `01M7QQVHH9TT318R5R4P47AH74`. No model/mission/WP claim was fabricated.

The implementation correctly separates dependency-derived scheduling stages from their shared root placement. Its compute/model/finalizer/integration changes are well supported by the existing tests. However, two live consumers still use the now-invalid string-only branch resolver for a real later planning stage. This is an incomplete consumer migration and blocks approval/rollout.

## Findings

### R1 — P1: Bound MissionContext creation fails for a later planning WP

`src/specify_cli/context/resolver.py:270–274` retrieves the actual typed lane from the manifest but calls `lane_branch_name(...)` without `lane=lane`. The new resolver deliberately refuses a secondary planning ID without that context. On a normally computed/persisted three-WP early-plan → code → late-plan mission, actual public `resolve_context('WP01', ...)` succeeds with authoritative ref `release/test`, while `resolve_context('WP03', ...)` raises `ValueError: Planning stage requires typed lane context` at this call. No resolver, ownership, branch result or lane kind was mocked.

This is used by the public `spec-kitty context mission-resolve` command (`cli/commands/context.py:273`) and `resolve_or_load`, so a valid newly supported late planning WP cannot obtain the bound context expected by context-based workflows. Preserve the typed refusal. Pass the already resolved authoritative lane through the existing branch-target seam, and pin the actual public early/late context behavior in a committed RED-first regression. Do not infer planning privilege from an identifier prefix or add a second resolver.

### R2 — P2: Topology output fails for every mission containing a later planning stage

`src/specify_cli/core/worktree_topology.py:225–229` has the same omitted typed lane argument while iterating the real finalized manifest. Actual public `materialize_worktree_topology(...)` raises the same `ValueError` on the same disposable mission, even though direct workspace resolution is correct. The implement/review prompt builders call this path (`agent/workflow_executor.py:1364,1959`) and catch the failure as `[Topology unavailable: ...]`, dropping the full topology rather than showing correct stage membership and branch targets.

This violates the approved complete-consumer contract. Carry the actual lane context through this call and exercise the public topology output, including early/late stage membership, shared target, all WPs and correct code-lane treatment. Keep cleanup/allocation refusals intact. The remaining string-only calls were inspected: code-only cleanup callers have an explicit semantic planning skip; the migration best-effort diff caller catches failure and is not used for already-authored complete planning records. A bounded call-site regression should distinguish such intentionally code-only callers from calls that consume arbitrary actual lanes.

## Independent observations and validation

The review-only reproducer `/tmp/wordling-mission1-closeout-20261118/wp103-independent-public-consumers.py` creates an ordinary disposable Git repository under `/tmp`, uses real public compute/persistence/context/topology entry points, then removes that repository. Its JSON evidence records the successful early-context control and both causal late-stage failures with real source stack traces. It changes no candidate source or live Wordling metadata and performs no reference-controller, private-resource, original, VM, native-platform or Mac action.

Independently repeated on the fixed candidate (all Linux, explicit local mode and source-pinned `PYTHONPATH`):

- New stage/finalizer contract files: **50 passed** in33.57s.
- The entire declared affected surface from the source handoff: **622 passed, 2 existing skips** in66.66s. This includes lane compute/model/persistence, workspace/allocator/ancestry, finalizer/lifecycle and integration regressions. The skips do not cover the new cases.
- Declared architecture gates plus actual enabled cycle benchmark: **73 passed** in20.69s; the100-lane/500-edge governed benchmark executed, with mean75.31µs.
- Ruff on all12 changed source files and both changed test files: exit0.
- Strict mypy with the declared import mode on all12 changed source files: exit0.
- Aggregate `git diff --check`: exit0.
- Independent original-source RED replay through the unchanged frozen b45 import root reproduced both the minimal false cycle (`lane-a→lane-planning→lane-a`) and exact retained103 false cycle (`lane-a→lane-planning→lane-e→lane-c→lane-b→lane-a`). Those source-derived historical cases are GREEN in the candidate's independently repeated tests.

The passing affected suite does not erase R1/R2: neither public consumer is exercised with a later planning lane by those tests. The missing consumer coverage is the reason the regressions escaped the current green surface.

## Accepted parts and limits

Aggregate source inspection and repeated tests support the selected stage partition, deterministic IDs/order, all-WP edge conservation, unchanged code ownership contraction and genuine-cycle refusals. V2 omits legacy `lanes`; the test executes actual frozen b45 model/persistence source and observes its corruption refusal. Typed schema shape/identity/membership/dependency guards and v1 cases pass. Planning allocation, root resolution from root/code/coord checkouts, stale/rebase/lifecycle skips, actual Git late-content integration/idempotence/conflict/root preservation and pre-writer finalizer refusal snapshots pass.

The prepared immutable manifest is shared by preview and persistence; commit-time planning-SHA guards remain separate. The exact103 fixture verifies normalized prompt preservation, old event prefix and old status equality with its explicitly documented external bootstrap/commit collaborators isolated. It is not a hosted delivery or a live Wordling registration receipt. Author-reported changed-source coverage is94.779% statements/92.105% branches, whole measured package coverage75%; this review did not relabel whole-package coverage as90% or rerun an arbitrary full repository test campaign.

No dependency manifest, architecture allowlist, source guard or tests for genuine ownership cycles were weakened. No rollout, global/shared installation, remote operation or live Wordling write is approved by this review. The source candidate remains unchanged. Address R1/R2 with source-first regressions and return a new frozen aggregate for independent re-review; root retains the rollout decision.
