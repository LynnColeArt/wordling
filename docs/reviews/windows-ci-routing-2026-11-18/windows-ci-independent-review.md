# Independent Windows-only CI routing review

**APPROVE** source commit `be7da39b81195b0e1a5d39d401737c531209bf52`, reviewed against source base `39569f1d6811b8cc54c4a750eb4ae7cb77a828ab`. Approval also binds the source-identical governance/evidence checkpoint `238fd996b59feacd9c6c8293108234a4d535a43d`. No blocking findings.

Reviewer is the distinct mission_gap_audit agent, resolved `reviewer-renata` with review-scoped charter context for this parent-owned full-M1 subtask. This is not the author's Op/self-approval; no new standalone Op or lifecycle mutation was needed. No source/Git/CI/original/Mac mutation or real product test/build execution. Read-only validation invoked only actionlint, Bash routing checks with inert argv-recording stubs, exact Git source comparisons and diff hygiene.

## Source and behavior reviewed

Only `.github/workflows/native-prerelease.yml` and `docs/testing/native-prerelease.md` differ in source. Workflow SHA256 is `b883ab766960123d03ce4b69a552df9c8070f4be42ba9f56646a7b29ac78608b`; documentation SHA256 `198d61692cb3049ed62dec924b93a5e0aedbff613dc771786fc16ced3013ad9e`. Both working bytes equal be7da39b and238fd996. Go code, go.mod/go.sum and actual build-prerelease/verify-native scripts are unchanged.

The trigger is an exact push branch `validation/windows-native`, not a glob/wildcard default-branch trigger. The shared predicate selects Windows-only for that exact push, or for workflow_dispatch with platform windows. The shell env evaluates to true/false text and controls array arguments; strategy repeats the same predicate using fromJSON because that graph cannot rely on a step's shell state. Native job requires successful build as before. Linux regression always runs unchanged; contents token remains read-only and action SHA pins/artifact/needs/concurrency semantics are preserved.

| Event/input | Build target set | Native runner set |
|---|---|---|
| Exact validation/windows-native push | linux/amd64, windows/amd64, windows/arm64 | windows-latest |
| workflow_dispatch platform windows | same three | windows-latest |
| workflow_dispatch all/default | old three plus darwin/amd64, darwin/arm64 | windows-latest, macos-latest |
| pull_request | same old five | windows-latest, macos-latest |
| Unrelated push | workflow not triggered | none |

Manual all on the validation branch remains all because the first predicate also requires event_name push; likewise a PR originating on that branch remains all. Documentation explicitly says publish the exact reviewed commit to the dedicated branch **without opening a PR**, so the selected root route honors deferred Mac execution. It accurately distinguishes compiled ARM64 from native amd64 execution, fixture-free smoke filters from fixture-dependent NewNested tests and prior Mac results from current candidate evidence.

Inspected actual build script: repeated --target choices are explicit and it builds only those targets. Inspected actual verify-native script: selects only current host/architecture ZIP, so the Windows-only artifact set does not require a Darwin package. Upload/download still carries Linux/Windows ZIPs and the same verifier; Windows smoke includes console input, storage, recovery/PowerShell/app workflows. No accidental Mac process or artifact invocation exists on the selected branch route.

## Independent checks completed

- `/tmp/wordling-actions-tools-20261118/actionlint -shellcheck= .github/workflows/native-prerelease.yml` passes. Pinned actionlint1.7.7; shellcheck absent and explicitly disabled, not claimed executed.
- Read author checker source, then reran `/home/lynn/projects/spec-kitty/.venv/bin/python /tmp/wordling-mission1-closeout-20261118/check-windows-ci.py`: six trigger/input cases pass; exact build argv and native matrix agree; actual build-step Bash parses and executes against inert argv-recording Python/cp stubs. This executes no real product build/test, Windows or Mac job. Source review also confirms event/ref predicates agree for PR and dispatch on the validation branch.
- `git diff --check 39569f1d 238fd996` passes; exact frozen source and unchanged build/verifier/module bytes independently compared with git show.
- Read committed canonical validation at `.kittify/evidence/01M7QC6W71N0D6KJZZFP7BRTYA/{evidence.md,record.json}`. No `docs/reviews/windows-ci-routing-2026-11-18/` directory exists in this candidate; actual committed evidence is that alternate canonical location. Its green truth table is durable; full RED/checker/actionlint raw files remain in `/tmp/wordling-mission1-closeout-20261118/` with the author's handoff. This naming/custody distinction is recorded, not a source blocker.

Approval is for bounded workflow source correctness, not a passing remote Windows run, new native candidate qualification, full nested-macro Windows coverage, original behavior or mission acceptance. Root retains publication and bounded monitoring of the exact dedicated-branch run, preserving run URL/source/artifact/input hashes. No Mac work should be launched until the user’s milestone-end gate.
