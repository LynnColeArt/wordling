# Planning-stage repair: independent review cycle 2

Audience: Spec Kitty core engineer and independent reviewer. This is an implementation
handoff for re-review, not approval, rollout or live Wordling registration.

The independent REQUEST CHANGES report SHA-256 is
`e985ed051271e4c9258509495e819c54c3139b69615bfe7fa6fd30e03bf04e4c`.
The previously reviewed candidate is `43869ef858a58ae879345c19cd1cc1e4e1581514`;
review-only records are retained through `8b69124d299ce7db6f1a5b1d367e4fe8e18baa3a`.
The original approved plan and cycle-one source handoff remain authoritative.

R1/R2 are addressed by exactly two product-source insertions in `ab8cf95d`:
`context/resolver.py:resolve_context` passes `lane=lane`, and
`core/worktree_topology.py:materialize_worktree_topology` passes `lane=lane_entry`.
Both use the already resolved actual record. No resolver/type guard, scheduler,
kind, identity, ownership, lifecycle, allocation or cleanup rule changed.

RED `fdb8046a` preceded the fix: the real public late context and full topology
failed with `Planning stage requires typed lane context`; the new live call-site
gate named both omissions. The clean RED run reported **3 failed, 6 passed**.
Early planning and code controls passed. The first test attempt also wrongly
expected no context cache; the fixture was corrected to verify the API's actual
persisted token roundtrip, unchanged tracked files/Git refs and no worktree.
Both raw logs are retained, not rewritten. Public tests use normal compute and
persistence, actual context/topology APIs and real temporary Git; no branch,
kind, ownership, workspace or resolver result is mocked.

All 17 live canonical branch-name calls were inspected. Nine generic consumers
now carry typed context. Five string-only code paths require an earlier semantic
planning exit on the same lane; three contextless naming/prediction/historical
migration seams retain their existing refusal/best-effort behavior. Each retained
site has a rationale in `tests/architectural/test_planning_branch_context.py`.
The gate has concrete live-call floors, import-alias detection, actual-source
keyword-removal mutations, semantic-exit removal mutations and canonical ratchet
growth mutations. `d1122ebd` registers only this new gate's initial 5/3 counts in
`_baselines.yaml` and both canonical comparison arms. No pre-existing baseline
count grows; no guard exception was added to a generic context consumer.

Linux/source-pinned validation, all with per-call
`SPEC_KITTY_ENABLE_SAAS_SYNC=0 PYTHONPATH=$PWD/src`:

- New public contracts plus complete context/topology surface: **189 passed**.
- Original affected packages plus the expanded context/topology packages:
  **806 passed, 2 existing skips**, 119.14 seconds. This includes the retained103
  public preview/apply and unchanged original99/history/recorded-SHA contracts.
- Selected architectural gates, canonical ratchet suite, new gate and enabled
  governed cycle benchmark: **94 passed**, 73.39 seconds. With the final two
  canonical-growth mutations added, final new-gate/ratchet subset: **23 passed**.
- Prior strict ASCII/complete-ID, large-WP, eligibility, runtime retry and retry
  CLI pins: **117 passed, 1 existing skip**, 69.56 seconds.
- Ruff: all 14 changed product-source files and every changed Python test pass.
  Strict mypy (`--strict --follow-imports=silent`) on all 14 product-source files
  passes. The two newly touched files were also green before the two-line fix.
- `git diff --check` passes. No new dependency installation or manifest change.

Exact command argument vectors are recorded in the adjacent evidence JSON;
raw stdout/stderr is retained in the corresponding
`/tmp/wordling-mission1-closeout-20261118/wp103-cycle2-*.log` files.
Reproduction command surfaces:

```sh
T=.pytest_cache/spec-kitty-test-venv/bin/python
$T -m pytest tests/lanes/test_planning_public_consumers.py tests/architectural/test_planning_branch_context.py -q -n0
$T -m pytest tests/architectural/test_planning_branch_context.py tests/architectural/test_ratchet_baselines.py -q -n0
```

The expanded regression command adds `tests/context`, `tests/specify_cli/context`,
`tests/specify_cli/core/test_worktree_topology.py`,
`tests/specify_cli/coordination/test_worktree_topology.py`,
`tests/specify_cli/coordination/test_worktree_topology_decision_table.py` and
`tests/init/test_worktree_topology.py` to the exact cycle-one affected command.
It instruments the original packages plus `specify_cli.context.resolver` and
`specify_cli.core.worktree_topology` with branch coverage. The architecture command
adds the new gate and canonical ratchet suite to the cycle-one architecture
command and explicitly sets `SPEC_KITTY_RUN_PERFORMANCE=1`.

Aggregate new-source coverage versus b45 remains **236/249 statements (94.779%),
105/114 branches (92.105%), combined 93.939%**. The two added keyword argument
lines add no separately instrumented executable statements; their behavior is
proved by the real public contracts. Whole measured-package coverage is **76%**,
not represented as 90%. Exact per-file counts, source/test hashes and raw evidence
hashes are in `wp103-cycle2-source-evidence.json`.

The original frozen b45 CLI, global/shared installation, Wordling checkout/index,
reference controller/resources, external services and Mac/VM state were untouched.
The isolated ordinary `/tmp` clone remains for distinct review; no new worktree,
repository, mission, push or remote publication was created. Repair Op
`01M7QR6RFBKZD61CBRPX1AZT5Y` uses actual implementer governance and closes with the
real implementation outcome. Independent re-review and the parent's explicit
rollout decision remain outstanding.
