---
type: explanation
updated: 2026-11-18
---
# WP104 TEST baseline — authorized recovery inspection

Audience: ROOT orchestrator and WP104 implementer.

**No exact baseline payload was located in the authorized filename/member indexes.** No payload was restored or decoded, and no operational qualification was performed. The existing188-campaign resource prerequisite remains unresolved by this finite search. ROOT’s separate review of a scoped canonical noncampaign TEST positive is not decided or selected here.

## Exact inspected container and indexes

Authorized container only: `/home/lynn/projects/wordling/research/cache/infra-recovery-20261117`.

| Inspection | Result |
|---|---|
| Container filename inventory (`rg --files -uuu`) |1,985 names; no expected-inputs.json.gz or recordedV19/R19 carrier/freeze name |
| `retired-local-manifest.json` |449 relative custody rows; no matching name, target SHA256 or1,027,525-byte row |
| `retired-worktree-local.tar.gz` member index (`tar -tzf`) |449 members; no matching baseline/carrier/freeze name; nothing extracted |
| `before-lane-reconciliation.bundle` reference header (`git bundle list-heads`) |102 reference names; no matching name; no fetch/clone/import/index/ref mutation |

No README exists among these scoped filenames. The retired manifest lists only relative paths and no immediate external archive/custody link, so no external recovery container was followed. Searches used the exact expected-inputs.json.gz name and recorded Wordling-WP70 V19/R19 source-freeze/carrier spellings. Filenames of other recovered artifacts were treated only as index data; no private ORIGINAL image/tool/guard payload was opened or statted.

The bundle’s reference header is **not a historical file-path index**. Its pack objects were not imported, decoded or searched for historical blobs; this report does not claim that no matching blob can exist anywhere in its history. Going beyond this finite index inspection would need a separately bounded, approved bundle-metadata/file-path investigation; no ad hoc object restoration was attempted.

Required candidate verification remains1,027,525 compressed bytes and SHA256 `c5861dd98775ea3be3b36c7d6e88219cdca96f0d41e230a818c2a5eba089c012`. No exact candidate emerged, so there was no compressed payload to hash and no decode/use. None of the unrelated binary artifacts was used as an inferred replacement.

## Authorized public Python metadata probe

Actually executed the explicitly authorized public base with `-I -B -c` from `/tmp`, importing only `sys,os,json,site` and checking attributes/metadata. Full exact argv, status and observed JSON are retained in `wp104-test-baseline-recovery-inspection.json`; raw stdout is `test-baseline-base-probe.stdout.json`, stderr `test-baseline-base-probe.stderr.txt`.

Actual exit status: **0**, stderr empty. Observations:

- CPython **3.12.14**, version string `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`.
- Executable `/home/lynn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`; prefix/base_prefix are that dependency’s Python root.
- Isolated/no-user-site/ignore-environment/no-bytecode flags all1; safe_path true; user site disabled; default exception hook retained.
- All required OS attributes checked exist: pidfd_open/P_PIDFD, fork, pipe2, waitid/waitpid, P_PID/WEXITED/WNOHANG/WNOWAIT/CLD_EXITED and O_NOFOLLOW/O_CLOEXEC/O_DIRECTORY. **No process/resource primitive was invoked** by the probe beyond the authorized interpreter process itself.
- No reference_controller/startup_family/startup_transport/peer/boundaries/qmp operational module loaded.
- `sitecustomize` and `usercustomize` absent; **`_distutils_hack` present**. sys.path includes the base’s python312.zip, standard library, lib-dynload and base site-packages.

This establishes the actual base version and advertised primitives only. It is **not** the clean copied TEST venv or an188-path qualification. The base’s site-packages/customization observation must stay explicit; ordinary copied-venv isolation, exact runtime origins/files and genuine TEST source/type/deployment guards still need their own real evidence. No runtime was built or modified and no qualification guard was relaxed.

## Handoff and preservation

The earlier `wp104-existing-test-deployment.md/.json` remain intact. The full missing V19/current custody-source problem is unchanged by these index results; no expected mapping, old path or authority was reconstructed. Root retains review authority over whether the canonical noncampaign route can satisfy a separately scoped unchanged CLI positive without claiming the old188 campaign. Neither that route nor the new ORIGINAL756D deployment was selected here.

Only new `/tmp/wordling-mission1-closeout-20261118/` report/index/probe-output artifacts were written. No repository source/index/runtime, lifecycle, grant, TEST/P/CONTROL/ORIGINAL campaign, private resource, VM or Mac action occurred. Read-only bundle-header listing changed no Git state. Prior105-ready/106-blocked and103-plan-approved reports were preserved.
