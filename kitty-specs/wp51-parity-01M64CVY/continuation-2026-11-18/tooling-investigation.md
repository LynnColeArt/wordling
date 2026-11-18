# Wordling M1 runtime recovery investigation

Read-only investigation of installed Spec Kitty 3.2.7 on 2026-11-18. Mission: `wp51-parity-01M64CVY` / `01M64CVYYRTDKBCYZ56H6XNTEQ`. No repository, runtime, credentials, tracker, workflow, or VM state was changed by this investigation.

## Findings

1. The source-layout acceptance blocker has a legitimate project configuration fix: `project.path_conventions.workspace: internal` in `.kittify/config.yaml`.
2. WP82's missing `agent` can be repaired through the explicitly public, append-only `emit_inner_state_changed` API. Historical implementation identity is `kat`; do not copy the authored profile or invent model/provider attribution.
3. The failed runtime run has no supported reset/retry/unblock/replan surface in the installed CLI or public runtime API. Adding new planned WPs can alter read-only query output but does not clear the retained run's failure. Do not report a false success, edit snapshots, delete the run mapping, or start a second product mission to conceal this.
4. Logged-out TeamSpace guidance does not prevent local mission operations. Hosted publication and durable hosted outbox delivery are not established; preserve and verify local authoritative writes separately.

## Honest source-layout correction

Merge this subsection into the existing `project` mapping, preserving project identity fields:

```yaml
project:
  path_conventions:
    workspace: internal
```

The project has its Go implementation under `internal/` and executable entry point under `cmd/`. The override remaps the generic `workspace: src` convention to the actual implementation directory. It does not weaken blocking policy, create a dummy directory, or alter a mission artifact requirement.

Installed source (all paths below are relative to `/home/lynn/.local/share/uv/tools/spec-kitty-cli/lib/python3.13/site-packages/`):

- `specify_cli/config/path_conventions.py:1` explicitly documents Go `internal/` as a supported use.
- `.../path_conventions.py:42` exports `load_project_path_conventions`; it reads only `.kittify/config.yaml` → `project.path_conventions`.
- `specify_cli/validators/paths.py` applies the mapping before mission defaults. Values must be nonempty repository-relative paths without `..`. `deliverables` is artifact-routed and cannot be overridden.

After applying and committing the real configuration change, rerun the same acceptance diagnosis used by the parent. The remaining metadata and evidence blockers still need resolution.

## WP82 metadata repair, with provenance

Canonical `status.events.jsonl` records real implementation by `kat`, followed by independent `reviewer-renata` approval:

- `01M72KRKTE9Z9HEZZ4188WB2CV`: `planned → claimed`, actor `kat`, 2026-11-10. Reason references source commits `5640032b`, `bc60a480`, `16fbeb64` and rejection findings `610b6952`.
- `01M72KSBFY7TJZ41QRFZ6SDY1T`: `claimed → in_progress`, actor `kat`.
- `01M72N08PM0HZ8B3HWF2HQ4CPE`: `in_progress → for_review`, actor `kat`, with actual pre-review gate evidence.
- `01M72N3RH0NX787NRJ9TF59EEV`: independent reviewer enters review; references merged implementation `6e50092c`, placement restoration and retirement `3b169e13`.
- `01M72N4RBQR18QR785328SBTQK`: approved by `reviewer-renata`; review reference `review-cycle://wp51-parity-01M64CVY/WP82-everyday-session/review-cycle-3.md`.
- `01M72N56V0BN01SK34M8V9B30K`: `approved → done`, actor `reviewer-renata`.

Current snapshot has lane `done`, review approved, actor reviewer-renata, but no `agent`. Restoring `agent=kat` from the canonical claim/progress history is an attribution repair, not a new implementation claim.

The sanctioned public API is exported from `specify_cli.status` (`__init__.py:131,365`), implemented in `status/emit.py:981`. It explicitly supports off-axis runtime annotations without traversing the FSM, canonicalizes the authority path, acquires the feature lock, appends durably with readback verification, and materializes. Example for the parent to execute once:

```python
from pathlib import Path
from specify_cli.status import WPInnerStateDelta, emit_inner_state_changed

repo = Path('/home/lynn/projects/wordling')
slug = 'wp51-parity-01M64CVY'
event = emit_inner_state_changed(
    repo / 'kitty-specs' / slug,
    'WP82',
    WPInnerStateDelta(
        agent='kat',
        note=(
            'Restore missing agent attribution from canonical WP82 implementation '
            'events 01M72KRKTE9Z9HEZZ4188WB2CV and 01M72KSBFY7TJZ41QRFZ6SDY1T '
            '(actor kat); preserve done lane and independent reviewer-renata '
            'approval 01M72N4RBQR18QR785328SBTQK.'
        ),
    ),
    actor='codex',
    mission_slug=slug,
    repo_root=repo,
)
print(event.to_dict())
```

Use `/home/lynn/.local/share/uv/tools/spec-kitty-cli/bin/python`, the CLI's Python, for these imports. Inspect the returned event, canonical log, materialized snapshot and repository diff; commit through the governing safe commit workflow. The API canonicalizes placement: inspect its resolved write location instead of assuming the supplied path was the final authority.

`spec-kitty agent tasks add-history WP82 --agent kat ...` is insufficient: `tasks.py:1007` only changes the task activity prose and emits HistoryAdded. It never sets the runtime `agent` slot. Do not force a fake done→planned→done cycle. Model/provider/profile remain unresolved; authored frontmatter recommendations are not historical execution evidence.

## Runtime failure is a tooling dead end in this installation

Parent-observed command:

```text
spec-kitty next --agent codex --mission wp51-parity-01M64CVY --result failed --json
```

Durable run `e5253119e41745f281bfaf4e73549111` now reports: `Previous step 'implement' failed; manual intervention required.`

The earlier read-only preview of `accept` did not establish that `accept` was the issued runtime step. `runtime/next/runtime_bridge.py:653` has a finalized-task-board query override (approved/done WPs → accept). The retained runtime step was still implement.

`runtime/next/_internal_runtime/engine.py:244` consumes an issued step. On failed result it stores `blocked_reason` and clears `issued_step_id`. On success it merely appends the existing issued step to completed_steps and carries blocked_reason forward; a subsequent success cannot clear this block. `planner.py:362` returns blocked whenever blocked_reason is present. The only assignment clearing blocked_reason is new run construction at engine.py:185–223.

The CLI exposes no retry/unblock/reset/replan option:

- `next --help`: agent, result, mission, JSON, answer, decision-id, owned-checkout.
- `mission reopen`: only mission lifecycle reopening and merge marker removal (`mission_type.py:1233`), no runtime run/index repair.
- `mission run`: custom mission definition start-or-attach; existing run is reused.
- `doctor mission-state --fix`: mission artifact-shape migration; it explicitly skips runtime side logs in `migration/mission_state.py:1433` and has no blocked run recovery.
- Public `runtime.next` exports only Decision, DecisionKind, decide_next. CLI-internal lifecycle exports start_mission_run, next_step, provide_decision_answer; no retry/unblock.

`runtime_bridge_io.py:604` `get_or_start_run` always reuses the existing mapping when `state.json` exists. `save_feature_runs` is a narrow persistence port, not a documented operator recovery contract. Combining it manually with CLI-internal start_mission_run would re-index a new run and discard the active workflow checkpoint; it is not a supported recovery command and is not recommended here. Deleting the mapping/state, copying snapshots, or relabeling a failure as success would bypass the missing recovery behavior.

Appending legitimate new WPs and validating them via `spec-kitty agent tasks finalize-tasks --mission wp51-parity-01M64CVY --validate-only --json` can prepare the product continuation. However, a query preview of implement afterwards is not proof the blocked mutation engine recovered. Installed runtime needs an actual supported recovery fix before the canonical next loop can truthfully resume. Preserve the failing run/events and report this as a tooling defect; do not claim completion from the query override. No upstream recovery command was verified by this local investigation.

## Auth/publication scope

`specify_cli/readiness/coordinator.py:224–301` performs a no-network, no-queue-mutation readiness probe and renders guidance. It does not gate or throw for the logged-out verdict. `readiness/render.py` is explicitly never-raises. Sync-specific commands separately use `handle_unauthenticated_with_teamspace`, which can exit 4 when hosted credentials are absent.

Local status API persistence precedes hosted fan-out (`status/emit.py:1018–1052`); hosted fan-out is explicitly best effort. Runtime engine appends its local event before emitting hosted events. Therefore auth guidance alone does not invalidate local mission control.

The observed `Event did not durably queue; dropping from publication` warning is stronger than merely being logged out: `sync/emitter.py:2332–2360` says the publication outbox refused or could not persist that event; it returns None and suppresses live publication. It does not roll back independently committed local status/runtime records. Verify local records and report hosted sync as unavailable/unverified. Do not infer eventual delivery, initiate OAuth, change credentials, or enable global/env overrides as a workaround.

## Follow-up: fresh run boundary and WP100+/owned-checkout support

The installed lifecycle constructor has this exact signature (`runtime/next/_internal_runtime/engine.py:185`, re-exported by `_internal_runtime/lifecycle.py`):

```python
start_mission_run(
    template_key: str,
    inputs: dict[str, Any] | None,
    policy_snapshot: MissionPolicySnapshot,
    context: DiscoveryContext | None = None,
    run_store: Path | None = None,
    emitter: RuntimeEventEmitter | None = None,
    template_override: MissionTemplate | None = None,
    template_path_override: str | None = None,
    mission_slug: str | None = None,
    mission_id: str | None = None,
) -> MissionRunRef
```

It can technically preserve a mission identity while creating another run directory, but the module explicitly labels its API **CLI-internal**. It starts from empty completed_steps/decisions and no issued step. It provides no supported retry/checkpoint semantics and does not bind the new run to the mission index. The index writer is `runtime.next.runtime_bridge_io.save_feature_runs(path: Path, index: dict[str, _FeatureRunEntry]) -> None` (line177), documented as a narrow persistence port. The CLI's binding logic is embedded in get_or_start_run; no public replace/restart binding callable was found. `runtime_bridge.__all__` at3033 enumerates exactly eight public names and includes get_or_start_run, not start_mission_run/save_feature_runs. `orchestrator-api --help` likewise has no start/restart runtime run command (start-implementation is a WP lane composite, not a runtime restart).

Therefore no lawful **public fresh-run-and-bind recovery contract** was verified. Recombining those internal parts can be engineered, but labeling it an existing supported operator API would be inaccurate. This finding is a tooling gap, not a product decision requiring the user to invent a new mission.

### WP100+ is not supported end-to-end in 3.2.7

Although canonical status and some task readers accept `WP\d+`, critical implementation/finalization/ownership readers still hard-code two digits:

- `specify_cli/cli/commands/implement.py:91,279`: `^WP\d{2}$`; WP100 is rejected with “Expected format WP##”.
- `specify_cli/cli/commands/agent/tasks_finalize_validation.py:121`: `^WP\d{2}$`.
- `specify_cli/core/wps_manifest.py:37,45`: both IDs and dependencies must be two digits.
- `specify_cli/ownership/frontmatter_source.py:39,85`: `^(WP\d{2})(?:[-_.]|$)` skips `WP100-*.md` entirely, omitting ownership validation.
- `specify_cli/core/dependency_parser.py`, dependency_graph.py, mission_finalize.py, mission_parsing.py and requirement_mapping.py also contain two-digit/truncating readers.

Pure read-only model probe confirmed WorkPackageEntry(id='WP99', title='probe') succeeds and WP100 raises `Value error, WP id must be WPnn (e.g. WP01), got: 'WP100'`. Do not publish WP100+ as if installed finalization/ownership guarantees apply. A tool fix is required for that numbering, or existing real WPs can be reopened for genuinely matching remediation scope using canonical lifecycle rules (never recycle a completed ID to disguise a new package).

### Explicit owned checkout is real but currently has a sync-mode blocker

M1 meta.json declares `topology: single_branch`, `target_branch: feat/wp51-parity` and no coordination_branch. A read-only call to the exported `resolve_owned_mission` validates `/home/lynn/projects/wordling` as both primary and owned root and resolves M1 successfully. It checks explicit mission identity, same Git repository, branch equals target, unprotected destination and artifact containment (`core/owned_mission.py:51–100`). This command selects the existing checkout without creating a worktree:

```text
spec-kitty next --mission wp51-parity-01M64CVY --owned-checkout /home/lynn/projects/wordling --json
```

For WP lifecycle mutation, `agent tasks move-task` has `--owned-checkout` and `_mt_owned_workspace` (`tasks_move_task.py:701`) maps workspace to the selected root directly instead of an allocator. Its preflight (`tasks_move_task.py:366–400`) requires no staged changes, auto-commit, no review overrides, and **inactive synchronization**. It supports the local review lifecycle through approved; done is excluded from this owned path. No unsupported option should be forced.

Read-only `specify_cli.core.saas_sync_config.sync_active()` returned **True** in the current shell. Therefore owned move-task would presently fail with `OWNED_SYNC_UNSUPPORTED: Owned move-task does not yet support active synchronization.` Being logged out does not make sync_active false: this is the explicit machine-level rollout gate. No env/config flags were changed in this investigation. The parent must resolve the supported local/hosted execution mode or tool limitation before choosing this mutation path. Simply adding --owned-checkout does not make all implementation commands use it (`implement` itself has no such option).

## Direct journal correction (root, 2026-11-18)

The retained runtime journal contains 11 records and ends with the actual failed implement result at 2026-11-05T06:30:21.044150+00:00. It was already blocked before this recovery pass. The Nov18 failed-result invocation appended only the mission-level invocation record, without a new runtime failure or consumed issuance. Therefore the initial hypothesis that the Nov18 readiness check newly blocked the retained runtime is rejected. Preserve the complete old journal and retry the actual Nov5 failed step through the reviewed recovery command.
