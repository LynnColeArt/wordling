# Wordling infrastructure recovery and prerelease readiness

Date: November 17, 2026 (America/Chicago).

**Verdict: not ready for native Windows/PowerShell or macOS prerelease testing.**
Both platform builds fail before producing an executable. Linux application
qualification and the broader research-harness results are recorded below;
they do not establish complete WordPerfect 5.1 parity.

## Recovered and synchronized work

- The home-level sanctioned directory is `/home/lynn/work-trees`. It contained
  no Wordling checkout. Git registered 29 Wordling lane worktrees under the
  older project-local `.worktrees` directory.
- The initial main checkout was at `e9caa7e1` with 89 modified tracked files
  and 3,105 untracked files. All 507 paths changed by remote `main` matched
  the corresponding local files byte for byte. Remote `main` had already
  checkpointed those source changes.
- Preserved the additional local qualification captures, synchronized remote
  `main` (`915189c0`), and integrated the November 17 source-sync branch
  (`655c7810`), including Advance and comparison/recovery qualification.
- Seven approved lane tips were outside the checkout's ancestry. Integrating
  lanes i, m, and y also brought in their dependent lanes l, v, w, and x.
  This restored performance measurements, executable editing differentials,
  conformance tooling, merge research, and their retained evidence.
- The three add/add runtime conflicts retained the later page-aware merge
  implementations in `internal/merge/body/{body,compile}.go` and
  `internal/merge/native/semantic.go`. The two Document Compare README
  histories were combined. Mission approval/acceptance state was not advanced.
- Every local branch tip is contained in the recovery branch. Its source is
  pushed as `recovery/wordling-infra-20261117`; this report does not represent
  a release or a merge of that branch into `main`.

The restored contract test still expected a NUL byte to be malformed, although
the newer native reader deliberately preserves it. The active test now checks
NUL preservation and retains the DEL-byte malformed-input assertion. Historical
test bytes remain available in their original Git commits.

## Candidate identity

The normal Linux executable is available at `preview/wordling`.

```text
SHA-256 cfaf15fa112dc3ee69ed02e23eb5704ba7fcec912283fe5e5a0dd8f938285137
Integrated-suite source 82fb52f4b9d1e7ef75fed5a239cbbcc2b9b0ce81
Reproduced source       f6f5211e1bd6256eacfd848c607d4484bef4038f
```

The reproduction has identical hashes for all 206 compiled local inputs and
identical executable bytes. Changes after the suite build concern restored
contract tests and documentation. Normal and `wordling_qa` executables have
separate candidate records; injected save failures use the QA executable only.
The normal preview contains the normal storage seam.

## Fresh validation

[Machine-readable summary](infra-recovery-2026-11-17-evidence/summary.json)
and [exact suite manifest](infra-recovery-2026-11-17-evidence/suite.json) retain
candidate hashes, commands, child results, and original execution paths.

| Check | Outcome |
| --- | --- |
| Git object integrity (`git fsck --full --no-dangling`) | Pass. |
| Inventory/scenario rendering, review adapter, Go package discovery/build/test/vet | All seven configured checks pass. |
| Full Go race run | Pass. |
| Tagged QA storage tests and captured/synthetic Advance tests | Pass. |
| Integrated candidate suite | **85/85 pass**, including the available original DOS round trips; no original/proofreading exclusion flags. |
| Native table sweep | **20/20 pass**: saves, creation, multiline cells, wrapping, pagination, row limits, and overflow variants. |
| Focused Linux PTYs | **5/5 pass**: terminal keys, shell return, recovery decisions, interrupted-save recovery, and indent. |
| Performance Python checks | 4/4 pass. Historical raw performance evidence verifies in its pinned lane context. |
| Historical conformance in its original lane context | **33/33 pass**. |
| Historical conformance against current source | 31 failures in 33 tests; the frozen spec guard refuses current source drift. |
| Historical editing checks against current source | 28/30 pass; two checks meet the frozen Go-inventory guard. |
| Historical editing checks in their lane context | 29/30 pass; one replay requires the missing historical `/tmp/wordling-wp29-build-4rr2vfky/wordling`. |
| Reference startup prerequisite | 57/57 pass. |
| Reference one-leaf envelope | 41/42 pass; checked-endpoint exchange hits `ReadinessDeadline`. A focused rerun also fails (`EnvelopeDeadline`). |
| Reference startup seam | 61/62 pass; copied-identity hook fails `unknown-identity`, reproduced in a focused rerun. |
| Reference stopped-readonly derivation | 94/97 pass; expected-absence control loses control/measurement, and two measurement-completion cases fail in the full run. The two measurement cases pass their focused rerun; the absence case still fails. |

The reference-harness groups are **not all green**. Their failures were retained;
no deadline, identity, measurement, or source guard was weakened. The two passing
measurement reruns do not turn the initial 97-test group into a passing run.

The first table invocation lacked its required `--fast-save` argument; it was an
invocation error. The corrected complete 20-case sweep passes. The initially
restored NUL contract failure was repaired and followed by fresh passing standard
and full race runs.

These are the fresh suites executed for this recovery. Long historical fuzz
campaigns, every research replay, exhaustive performance acceptance, and physical
desktop/native-host testing were not repeated.

## Platform blockers

All four cross-build attempts returned exit status 1:

| Target | Result |
| --- | --- |
| Windows amd64 | Storage package has no eligible Go files. |
| Windows arm64 | Storage package has no eligible Go files. |
| macOS amd64 | Storage package has no eligible Go files. |
| macOS arm64 | Storage package has no eligible Go files. |

The storage implementation is selected through `_linux.go` filenames. Its
directory capabilities, path checks, native replacement/backup operations, and
fault controls need platform implementations before either host can run the
application. Recovery also directly uses Unix file flags and `Flock`; Windows
needs a corresponding implementation. Successful compilation must be followed
by native-host save/backup/recovery and terminal keyboard/mouse testing.

## Acceptance limits

The current command audit records 186 verified, 38 partial, and 20 unimplemented
scenarios. Those audit labels are not fresh acceptance of every scenario.
Complete Mission 1 qualification, independent acceptance, physical desktop
input checks, and native Windows/macOS behavior remain open. PTY input tests
establish the exercised terminal sequences only.

The restored WP31 conformance registry is pinned to historical specification
and implementation bytes. On the current source it correctly refuses
`working source drift: kitty-specs/wp51-parity-01M64CVY/spec.md`.
The WP29 editing driver similarly refuses the expanded current Go inventory;
its frozen replay also references a temporary executable that is no longer
present. These guards were not relaxed or relabeled as current acceptance.

## Recovery artifacts and cleanup

The recovery Git bundle, archived local-only worktree files, retired workspace
contexts, and prior preview are preserved under the ignored directory
`research/cache/infra-recovery-20261117`. No proprietary reference installation
or research cache was added to the source-sync commits.

All **29 lane worktrees are retired** after clean-tree, local-ancestry, and
pushed-ancestry checks. Their branches remain recoverable in the synchronized
history and recovery bundle. Local `main` was safely fast-forwarded to remote
`main`; the active recovery branch retains the complete combined work.

Compact result records and diagnostic logs are tracked in
[`infra-recovery-2026-11-17-evidence/`](infra-recovery-2026-11-17-evidence/).
The complete raw validation directory, including terminal captures and original
round-trip artifacts, is preserved under the ignored
`research/cache/infra-recovery-20261117/validation/`. Manifests retain their
original `/tmp/wordling-recovery-20261117` execution paths as provenance.

Before native Windows/macOS testing, implement the platform storage/recovery
backends, obtain successful native builds, resolve the reproducible reference
harness failures, and establish a current evidence baseline. Then run the native
filesystem, recovery, terminal-key, mouse, and document round-trip journeys on
both hosts. Full Mission 1 acceptance remains a separate open obligation.
