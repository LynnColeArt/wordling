# Canonical owned execution investigation

Read-only source/CLI investigation against `/tmp/wordling-spec-kitty-repair-20261118` and installed3.2.7. No repo/runtime/tooling-agent files changed, no new claim, worktree or baseline created. Per-call `SPEC_KITTY_ENABLE_SAAS_SYNC=0` was used for CLI help only; no disable/minimal-import or skip flags.

## Finding

**A supported owned single-branch lifecycle already exists through independent approval; no new allocator/workspace feature is necessary for this bounded continuation if root explicitly performs the existing preimplementation checks and canonical baseline capture and records the prompt's workspace correction.** `next` + `move-task` alone is not fully equivalent to `agent action implement`: automatic baseline capture and correct owned prompt rendering are missing. Do not silently lose those checks.

Evidence:

- Accepted ADR `docs/adr/3.x/2026-09-03-1-explicit-owned-checkout-single-branch-lifecycle.md` explicitly extends the complete single-branch lifecycle to owned checkouts.
- `core/owned_mission.py:52-104`: canonical exact checkout identity, single_branch metadata, mission containment, current branch==target, protection checks, unstaged index.
- `cli/commands/agent/tasks_move_task.py:365-435`: local-only owned lifecycle planned/claimed/in_progress/for_review/in_review/approved; auto-commit required; active sync and force/skip/arbiter/done refused.
- Same source `:443-474` resolves profile/model/Op binding; `:651-718` validates immutable ancestor review base and substitutes the actual owned root as review workspace; `:784-798,897-1003` requires committed owned implementation and normal subtasks/readiness checks; `:1687-1715` retains doctrine-bound transition gates and baseline loading. `--owned-checkout` is a real workflow, not a manually edited state escape.
- Integration tests `tests/specify_cli/cli/commands/agent/test_owned_checkout_move_task.py:228-255,260-321,407-461` exercise claim/start, implementation commits, review submission, independent review/approval and durable review artifact without allocator invocation, leaving sibling/primary checkouts untouched. They also test status-only implementation refusal and invalid review bases.

## Exact recommended sequence (root executes, not performed here)

1. Finish reviewed three-digit-ID tooling correction. Finalize the revised WP100–103 append through the normal supported owned finalizer. Confirm old99 histories/prefix unchanged, authored ownership complete, baseline planning SHA real, current root is the exact unprotected checkout on `feat/wp51-parity`, topology exactly single_branch, no staged/uncommitted unrelated work. Preserve current governance and source/plan approvals.
2. Issue the normal `next` step for the finalized mission with `--owned-checkout /home/lynn/projects/wordling`, actual actor and normal result semantics. Preserve raw decision/prompt/Op identity and hashes. Require the actual WP100 implementation step, not merely a query. Resolve implementer profile/model through the correlated Op and preserve normal source/charter/dependency/feedback checks before starting. Inherited WP65/66/82 planning and implementation objects must actually be ancestors of the owned HEAD; verify with the canonical read-only ancestry predicate or exact git evidence. Do not infer ancestry from lane labels.
3. Record a reviewed execution addendum to the issued prompt: its actual execution workspace is the validated `OwnedMission.root`, target `feat/wp51-parity`; every task lifecycle command carries the same explicit `--owned-checkout`. Preserve issued prompt content unchanged as evidence. The generated lane workspace and flagless completion command are presentation defects on this path, not permission to create projects/.worktrees. Never fabricate `.kittify/workspaces` or change code_change to planning_artifact to force resolution.
4. Claim/start through owned move-task using actual actor/profile/model/Op metadata and process identity, normal auto-commit and no overrides. The supported edge can be `planned -> claimed -> in_progress` (CLI alias `doing`); integration tests prove both explicit claim/start and direct doing that emits the lawful claim chain. Freeze the pre-code target commit.
5. **Before editing code**, invoke the existing canonical Python API shown below, using the same approved tool environment, selected root and ScopeSource as the head-side gate. Require a real non-sentinel result and official artifact matching the frozen commit, WP, declared command/source identity and successful actual baseline run. Inspect the raw JUnit output and report real suite counts; the ScopeSource adapter's stored total/passed can be derived rather than actual counts. Commit the official artifact through the normal safe Spec Kitty commit authority before implementation. Do not fabricate JSON, copy another WP's baseline, accept a missing/ambiguous/sentinel capture, or treat a current-head-only test as a baseline.
6. Implement only the issued bounded WP100 sources and tests; run required focused/full Go/race/build/vet/format gates. Commit authorized code through normal safe commits (or supported owned review auto-commit), record exact candidate and evidence. Mark only T326–328 done through `agent tasks mark-status ... --owned-checkout ROOT --mission MISSION`.
7. `agent tasks move-task WP100 --to for_review --agent ACTOR --owned-checkout ROOT --mission MISSION --json` runs normal transition gates, actual implementation delta, readiness and durable submission. No skip/force flags. Inspect returned gate metadata; UNVERIFIED_BASELINE/NO_COVERAGE is not a passing regression comparison. Preserve warnings/failures and resolve them.
8. Independent reviewer claims `in_review` with explicit owned root, reviews exact immutable base/head plus all required tests/evidence and authored scope, then uses normal `approved` or `planned` rejection with real approval/feedback reference and correlated reviewer identity. Owned mode supports through approved; do not force done. Return to canonical next/accept/merge lifecycle after all real mission obligations are complete. WP100 approval leaves four macro audit rows partial until WP102, and does not accept M1.

Every CLI invocation above uses the documented per-process `SPEC_KITTY_ENABLE_SAAS_SYNC=0`, never `SPEC_KITTY_SYNC_DISABLE`, `SPEC_KITTY_SYNC_MINIMAL_IMPORT`, force or gate-skipping.

## Existing canonical baseline API

This is the shared public function already called by `agent action implement`, not a new test runner or hand-authored artifact. Invocation sketch, with root supplying validated/frozen values:

```python
from pathlib import Path
from specify_cli.core.owned_mission import resolve_owned_mission, require_unstaged_index
from specify_cli.review.baseline import capture_baseline
from specify_cli.review.scope_source import resolve_scope_source

owned = resolve_owned_mission(primary_root, exact_owned_root, mission_handle)
require_unstaged_index(owned)
wp_slug = exact_authored_wp_path.stem
baseline = capture_baseline(
    worktree_path=owned.root,
    base_branch=frozen_pre_code_commit,  # exact target commit, not a later moving tip
    wp_id="WP100",
    mission_slug=owned.slug,
    feature_dir=owned.directory,
    wp_slug=wp_slug,
    scope_source=resolve_scope_source(owned.root),
)
assert baseline is not None and baseline.failed != -1
assert baseline.wp_id == "WP100" and baseline.base_commit == frozen_pre_code_commit
# Validate actual run/artifact/source identity and commit the official artifact.
```

Root must also reject an unexpected cached artifact: `capture_baseline` intentionally returns existing captures without rerunning (`review/baseline.py:317-324`), so validate its identity and timing instead of assuming the call refreshed it. Actual positive baseline test failures require explicit review; do not relabel them clean.

The function locates either `.git` directory or linked `.git` file in the selected root (`:682-692`), places the artifact under the explicit feature_dir, uses a detached baseline worktree under `tempfile.TemporaryDirectory` and removes it in `finally` (`:235-275`). With normal `/tmp` temp placement this satisfies the user's location/cleanup policy. It does not use the prohibited project lane allocator.

## Actual remaining rendering/automatic-capture gaps

- `runtime/next/prompt_builder.py:59-84` exposes only action, feature_dir, mission_slug, wp_id, agent, repo_root and mission_type. There is **no owned root/workspace override parameter**. Its `_build_wp_prompt:160` resolves the ordinary workspace; `decision.py:497` independently does the same for the decision envelope. For code_change, `workspace/context.py:895-914` composes the lane path, and `lanes/branch_naming.py:472-485` joins `repo_root/.worktrees/...`. Passing repo_root=owned does not cause a direct owned execution workspace. `next --owned-checkout` protects mission state placement but does not correct this WP prompt display.
- `agent action implement` has no owned flag and always enters normal workspace materialization (`agent/workflow.py:1284-1305`), then captures baseline (`:1388-1397`). Owned move-task loads the same official baseline but never captures it itself. Wordling has `review.test_command` configured (`.kittify/config.yaml:22-24`), so omitting capture loses a real intended check.
- Keep all preimplementation gates that action implement would perform: sparse/protection/target/charter, dependency status, feedback and actual ancestry. Canonical pure `check_claim_ancestry` can inspect without materializing. Its wrapper `resolve_claim_ancestry_gate` retries failures through allocator self-heal (`lanes/implement_support.py:474-494`); do not call that failure path merely to discover a missing ref under this ownership route. A real missing dependency is a blocker to resolve, not a reason to create a prohibited workspace.

The explicit canonical API capture plus independently reviewed owned-root addendum closes the operational gaps for this bounded run without modifying Spec Kitty CLI source. This is not a claim that raw `next`/`move-task` automatically supply equivalent behavior or that their generated workspace text is correct. If exact validated owned placement or canonical baseline capture fails, stop that claim and report the real blocker; do not patch around it with state writes or synthetic evidence.
