# Independent tool-repair review — 2026-11-18

Audience: Spec Kitty core team and Wordling recovery operator. Reviewer Renata, resolved through the supported profile CLI. Read repository AGENTS.md, complete charter and action-scoped review governance. Reviewer implemented none of these production changes and did not modify the installed CLI, Wordling source, live runtime, tracker or other agents' files.

## Verdict

**APPROVE the bounded local tooling repair at immutable source HEAD `b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3`, against release source base `fb4e8fa9` (tag v3.2.7).** The source checkout `/tmp/wordling-spec-kitty-repair-20261118` is clean, and final `git diff --check fb4e8fa9..HEAD` passes. No unresolved blocking finding remains in this reviewed scope.

This authorizes review acceptance of this local source repair, not an upstream release, a protected-branch merge, hosted WP100 synchronization, completed Wordling implementation or Mission1 acceptance. Live rollout remains the parent operator's task.

## Exact provenance

- Initial RED commits: runtime `b87393f122e7e04aacd2c9fdf96e46dff75f1ad9`; ID/ownership `b1a72eb35828695fd6d8cdd8d0e5069e657a1b12`.
- ID implementation/review correction: `bb5cbd23`, H4 RED `fb9423c4`, fixed ID snapshot `2baa5f9343a03f4897f9e1fbb7b7a5a2b0a11cd8`.
- Combined runtime/ID snapshot: `1e99bc816056a8d24aefe425cfae72eb8a45c6b2`.
- Metadata RED: `ee8a075099d116bc431b2ac1c4c29385b19d73c0`; final validator correction: `b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3`.

The tested GREEN invocation uses explicit `PYTHONPATH=/tmp/wordling-spec-kitty-repair-20261118/src` and `/home/lynn/projects/spec-kitty/.venv/bin/python`. Root independently verified that both CLI package and runtime bridge load from that source clone. This interpreter's installed distribution metadata reports 3.2.6, despite the source checkout's v3.2.7 base/pyproject; spec-kitty-events is 6.1.0. Treat it as the explicit interpreter plus reviewed source SHA, **not a released 3.2.7 repaired binary**. The global installed 3.2.7 CLI remains unmodified.

## Independent execution evidence

1. Reproduced both original RED contracts from an ordinary `git archive b1a72eb3` snapshot, which includes the runtime RED commit: **11 failed, 12 passed**. Failures were actual WP100/101 manifest rejection, Unicode-digit acceptance, filename/path prefix truncation, omitted long-ID dependency forms and CLI missing `--retry`. Record: `tool-review-red-reproduction.txt` in this evidence directory. The test-session fixture automatically provisioned an isolated archive `.pytest_cache` environment and fetched dependencies there; no live CLI installation occurred. Reviewer removed that entire scratch source archive/environment afterwards.
2. Independently ran **515 tests, all passed in 156.94s**, at clean fixed `1e99bc81`: new WP100 acceptance, manifests, dependency parser/graph, frontmatter, finalization, ownership, bookkeeping/architecture ratchets, retry engine, next CLI, runtime bridge and finalized-task selection. Command is recorded in `tool-review-commands.txt`, output in `tool-review-green.txt`; JUnit: `tool-review-green.xml`. The exact command uses the explicit interpreter/source overlay, `SPEC_KITTY_ENABLE_SAAS_SYNC=0`, `-n0 -q --no-cov -p no:cacheprovider` and named affected test files, without gate-skipping environment flags.
3. The only production delta after that run is the single `WPMetadata.validate_wp_id` import/condition/message correction; the other changed path is its new regression file. Independently reviewed that exact two-file diff, then ran its **8 targeted tests, all passed in 1.66s**, at final clean `b45b48fd`. Evidence: `tool-review-metadata-green.txt` and `tool-review-metadata-green.xml`. Did not repeat unchanged broad suites.
4. Independently reproduced initial runtime-corruption acceptance in actual engine-created temporary runs. After fixes, mismatched start mission type, prerequisite success changed to failure, and duplicate run start all refuse while checkpoint and journal remain byte-identical.
5. Read-only purpose check against actual Wordling run `e5253119e41745f281bfaf4e73549111`: pure journal/checkpoint/planner predicates admit retry of the existing failed **implement** step. No bridge/emitter/retry mutation was invoked. This verifies eligibility only; the real failure history is retained, including its November 5 origin.

Implementer evidence was also inspected: ID 329-test affected/architecture run; metadata 156-test model/resolved-agent/ownership run; runtime 40 tests with 100% new-module statement coverage, 116 existing next/bridge/preflight/terminology tests and 62 additional package/no-implicit-success/parity checks. Strict mypy and ruff evidence is green for the touched source surfaces. Those longer unchanged checks were not duplicated by the reviewer. Runtime commands and limits are documented in `runtime-repair-result.md`; ID/metadata logs are under `/tmp/wordling-spec-kitty-repair-evidence-20261118/`.

## Findings and final dispositions

| Finding | Verified consequence | Final disposition |
| --- | --- | --- |
| Dependency punctuation narrowed | Base accepted `Depends on WP01: prerequisite` and dependency bullet `WP01:`; initial patch silently lost their edges, including WP100 equivalents. | **Changed/resolved**: explicit delimiter grammar retains colon/Markdown/dash punctuation; old and long-ID regressions pass. |
| H4 sections dropped during parser unification | Mission parser previously accepted `#### WP02`; delegation to H2/H3-only shared parser returned no dependency section. | **Changed/resolved**: canonical shared parser handles H2–H4, with separately committed RED and old/WP100 tests. |
| Unicode suffix became ASCII prefix | Combining acute and zero-width suffixes after WP100 were accepted as shorter WP100 dependencies by a broad non-word boundary. | **Changed/resolved**: explicit separator boundary refuses these malformed tokens and traversal/alphanumeric/Unicode-digit suffixes. |
| Retry history inconsistent with checkpoint | Changed start mission type or earlier successful prerequisite result could still admit retry. | **Changed/resolved**: start identity, successful issuance/result history and exact checkpoint completions reconcile; duplicate start and corrupt retry references are also refused. Independent no-write re-probes pass. |
| Hosted retry was unqualified | Local-only audit had no new hosted recovery contract. | **Changed/resolved**: public bridge explicitly refuses active synchronization; help/docs select per-invocation local mode and state the limitation. Existing hosted event schema/emitter remains unchanged. |
| Authored metadata retained permissive regex | Real `WPMetadata` and ownership flow accepted fullwidth digits or a trailing newline even after manifest/filename fixes. | **Changed/resolved** under explicit root scope amendment: typed metadata uses the same canonical fullmatch helper. RED model/disk-acquisition tests precede the one-validator fix; final targeted 8 and implementer 156 checks pass. |

## Contract assessment

`core/wp_ids.py` is the owning ASCII complete-ID/filename grammar. Manifest/model/schema/finalization/dependency/requirement/ownership consumers now preserve full WP100/101 values, reject the tested invalid/Unicode/path/prefix forms and retain ownership and dependency edges. User-facing touched errors explicitly describe at least two ASCII digits and WP100. Existing histories, source ownership, status authority and finalization gates are not rewritten. No source templates or generated agent copies changed; the enrolled bookkeeping regex remains explicit and architecture ratchets pass.

Runtime retry is explicit and audited, not an implicit success or a generic block clearer. It requires the actual existing run, actor/reason, last matching failed result and issuance, consistent checkpoint/history and unchanged planner/template admission. It preserves mission/run identity, completed steps, inputs, decisions, policy and original journal bytes; appends retry audit and issuance; atomically replaces only the issued/block checkpoint fields; refuses incomplete interrupted recovery. Normal advancing charter preflight, prompt admission and invocation recording remain. No work-package lane is reset or approved by retry.

Known conservative boundary is honest: unsupported/audit-only completion histories fail closed instead of being inferred. Hosted WP100 event support is not supplied; local finalization uses the existing per-call local configuration. No `SPEC_KITTY_SYNC_DISABLE`, `SPEC_KITTY_SYNC_MINIMAL_IMPORT`, false success, forced state edit, gate skip, recreated run or live-history repair was used.

No dependency manifests/lockfiles, package source registries or lifecycle scripts change. This review approves no dependency upgrade/installation; Node/lifecycle-script checks are not applicable to this Python source-only repair. Installed/runtime package provenance above remains explicit. Full upstream release validation and native application/complete M1 acceptance remain separate obligations.
