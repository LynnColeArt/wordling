# Audited local runtime retry repair

Source checkout: `/tmp/wordling-spec-kitty-repair-20261118`, branch `fix/wordling-m1-workflow-recovery`, based on `v3.2.7`.

Combined review head: `1e99bc816056a8d24aefe425cfae72eb8a45c6b2`. The checkout is clean. No push, PR, global package installation, live Wordling mutation, tracker change or credential change was performed by this agent.

## Red-first proof

Commit `b87393f1` added the CLI acceptance test before implementation. It drove a real custom runtime through prepare → successful completion → execute → failed result, then requested `next --retry --reason ...`. The test failed specifically with exit 2 and `No such option: --retry`. It had already verified that the original checkpoint retained only prepare as completed and had a real failed execute result.

Implementation commit `1e99bc81` adds the retry module, public bridge API, CLI flags and advancing charter preflight, refusal tests, and operator documentation. Distinct WP-ID repair commits through `2baa5f93` precede it on this combined branch; this agent staged and committed only its own seven source/test/doc paths.

## Contract

Public API:

```python
runtime.next.runtime_bridge.retry_failed_step_via_runtime(
    agent: str, mission_slug: str, reason: str, repo_root: Path,
    *, effective_root: Path | None = None,
) -> Decision
```

CLI, from the existing project checkout after the repaired tool has been selected:

```bash
SPEC_KITTY_ENABLE_SAAS_SYNC=0 spec-kitty next \
  --mission wp51-parity-01M64CVY --agent codex --retry \
  --reason "Describe the actual remediation before retrying implementation" --json
```

The retry is explicitly local-only. Active hosted synchronization is refused. The public bridge locates the existing run without a create-on-missing fallback. The engine requires an explicit actor/reason and a real, last failed result paired with its issuance. It reconciles the start identity and exact successful completion history with the checkpoint, validates prior retry audit references, checks frozen/live template integrity and planner admission, and reissues the same step. It preserves run/mission identity, completed steps, inputs, decisions, policy and the complete original journal prefix. It appends only `NextStepRetryRequested` and `NextStepIssued`; it never invents successful completion or changes WP lanes.

Unsupported event/audit-only completion histories, arbitrary blocks, bad references, inconsistent checkpoints, malformed or missing history, changed templates and already reissued steps fail closed. An interrupted atomic checkpoint replacement leaves the old blocked checkpoint and durable audit evidence, then refuses another automatic retry rather than fabricating a successful recovery. CLI retry passes the normal advancing charter preflight. The returned prompt and admission checks use the existing bridge path.

The initial surface intentionally does not infer audit approval semantics or add hosted event contracts. Operator documentation: `docs/guides/how-to/recovery/retry-failed-runtime-step.md`.

## Validation

All commands below ran in the source checkout using `/home/lynn/projects/spec-kitty/.venv/bin/python` with the repository's source/test isolation. No live Wordling runtime was used as the test subject.

- New engine surface: `python -m pytest tests/next/test_failed_step_retry.py -q -n0 --cov=runtime.next._internal_runtime.retry --cov-report=term-missing` → **40 passed**, **100% coverage**, 126 statements, 89.68 seconds on the committed source.
- Existing next/bridge/preflight/terminology surface: `python -m pytest tests/next/test_next_command_integration.py tests/runtime/test_bridge_engine.py tests/runtime/test_bridge_decide_next.py tests/agent/cli/commands/test_next_preflight.py tests/architectural/test_no_legacy_terminology.py -q -n2 --dist loadfile` → **116 passed**, 166.41 seconds.
- Additional CLI/no-implicit-success/package/parity checks: `python -m pytest tests/next/test_failed_step_retry.py tests/next/test_next_command_integration.py::TestNextFailedStepRetry tests/contract/test_next_no_implicit_success.py tests/runtime/test_bridge_parity.py tests/next/test_next_package_unit.py -q -n2 --dist loadfile` → **62 passed**, 440.16 seconds. This command began before the final additional audit corruption cases; the final engine run above covers all 40 committed engine cases.
- `python -m mypy --strict src/runtime/next/_internal_runtime/retry.py src/runtime/next/runtime_bridge.py src/specify_cli/cli/commands/next_cmd.py` → **no issues in 3 source files**.
- `python -m ruff check` on those three source files and both touched test files → **all checks passed**.
- `git diff --check` passed; final source checkout is clean.

Independent reviewer `/root/pr12_review` has the immutable combined head and is running its own bounded validation. This agent does not issue its own approval verdict.

## Historical correction

The original failure was durably recorded for implement on **2026-11-05 at 06:30:21.044150+00:00**. The parent verified that the November 18 `--result failed` invocation did not create a new failed runtime event; the retained runtime had already been blocked. Recovery must preserve and reference that real historical failure, not claim a new same-day failure. The new retry derives its failed step and event reference from the existing journal, so it does not depend on that earlier mistaken causal inference.
