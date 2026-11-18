---
work_package_id: WP106
subtasks: [T344, T345, T346]
title: Insert balanced native Italics through occupied Retrieve safely
task_type: implement
phase: Bounded Retrieve source delivery; genuine original qualification remains pending
execution_mode: code_change
owned_files:
- internal/document/everyday.go
- internal/document/retrieve_italics_test.go
- internal/editor/retrieve_italics_test.go
- internal/tui/retrieve_italics_test.go
- internal/document/evidence/retrieve-italics/**
authoritative_surface: internal/document/everyday.go
create_intent:
- internal/document/retrieve_italics_test.go
- internal/editor/retrieve_italics_test.go
- internal/tui/retrieve_italics_test.go
- internal/document/evidence/retrieve-italics/
agent_profile: implementer-ivan
role: implementer
dependencies: [WP99, WP94, WP84, WP85]
requirement_refs: [FR-002, FR-004, FR-005, FR-006, FR-008, NFR-002, NFR-003, NFR-004]
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Reuse canonical owned mission checkout after normal finalization and claim; no unowned source or project-local worktree.
history: []
tags: [m1-continuation, proposed-unregistered, retrieve-italics]
tracker_refs: []
---

# Work Package Prompt: WP106 — safe occupied Retrieve of balanced native Italics

## Do This First: Load Agent Profile

PROPOSAL ONLY. WP106/T344–346 are unreserved, not registered or claimed. No implementation follows from this file. Root/reviewer must approve this package and receiver-contract.md before canonical finalization/issued implementation. Resolve implementer-ivan and actual action-implement governance then; authored profile/role are not the executing model identity.

## Review Feedback

Read independent task/design feedback and the real event-log review reference before implementation. Resolve all returned findings; never fabricate history, approval or completion entries in frontmatter. Root controls lifecycle transitions.

## Objectives & Success Criteria

- Add balanced self-contained Italics sources to the existing checked native InsertDocument/InsertBlockCopy seam, preserving bounds, unrelated bytes/birth, caret/history and the exact frozen receiver contract.
- Reach it through actual rooted public occupied Retrieve and Yes, including real runtime save/reopen; source bytes and receiver's disk binding remain their own. No synthetic Result/receipt replaces I/O.
- Commit failing acceptance tests before production changes, prove the failure is the current UnsupportedBody source refusal, then make only the smallest authorized production fix.
- Deliver reviewed source and Linux/Windows regression evidence. Original occupied-Retrieve/native reopen/edit/print/save qualification remains explicitly pending; CMD51-065, E3 and mission matrix are not promoted by this WP.

## Context & Constraints

Read `.kittify/charter/charter.md`, `docs/compatibility.md`, mission spec/plan/tasks, continuation full-family and acceptance-closure artifacts, receiver-contract.md and source-pins.json accompanying this draft. Existing original fixture records attribute encoding, not original occupied-Retrieve semantics.

Current `internal/document/everyday.go:637–687` accepts balanced Bold/Underline but refuses Italics owners. Existing native ordinary admission, Italics authoring, layout and rendering already support those owners. `internal/editor/everyday_live.go:592–610` uses native InsertDocument; no editor/TUI/storage production change is planned. Normal dependencies carry the actual delivered native chain WP80→WP92→WP97→WP99, current session WP94 and UI WP84/WP85. Preserve all prior approvals/histories and independently verify ownership/lifecycle at finalization. Source presence does not manufacture approval.

Only self-contained native Italics plus previously admitted source owners are added. No style/font/prefix/resource transfer, admission expansion, native-format conversion, macro changes, alternate public APIs or ordinary source/archive changes. Shared InsertBlockCopy must inherit the same checked behavior and be tested. Any genuinely required source outside the sole production owner returns for a precise amendment.

## Branch Strategy

Planning base/target: `feat/wp51-parity`. Use actual issued owned root, preserving current ancestors. Any needed isolated worktree must use the approved tool under `~/work-trees` or `/tmp`, be removed when done, and leave all work committed. WP104/105 reference source is disjoint and can proceed independently; no original execution or Mac testing in this package.

## Subtasks & Detailed Guidance

### T344 — freeze contract and commit genuine RED acceptance

- Review receiver-contract.md before coding. Balanced Italics insertion outside receiver Italics succeeds; the same source inserted inside an active receiver Italics span refuses atomically; plain-source insertion inside Italics preserves existing behavior. At the four ON/OFF boundary gaps assert exact native outcomes, not ANSI guesses.
- Capture baseline source/fixture hashes and actual candidate ancestry; obtain the ordinary project baseline. Add only the three declared new test files. First commit tests while production everyday.go remains byte-identical to the approved baseline.
- Native tests parse cached original `mission1-appearance/ITALICS.WP`, insert at beginning/interior/end of plain receivers, and exercise source balance, both Copy/Insert APIs, foreign/stale cursors, bounds and candidate validation. Expect the new positive cases to fail at the existing UnsupportedBody path; negative controls should already pass. No xfail/skip/mock implementation.
- Public tests use genuine disposable rooted workspaces, actual storage selection/read and `editor.ExecuteEveryday`/Runtime completion. Occupied Retrieve requires the actual Yes confirmation; decline/cancel must not acquire/publish source. Test loaded and edited real New receivers and retain original buffer/source identity.
- Files: new document/editor/TUI test files only; baseline/RED proof under the new evidence namespace. No parallel writer.

### T345 — minimal checked native admission and receiver preservation

- Amend only `internal/document/everyday.go`: carry a separate Italics source balance flag in the same bounded source scan as Bold/Underline, include exact ItalicsOn/Off owners, reject duplicate/unmatched/unclosed sources before publishing. Preserve existing allowlist for every other kind and existing byte/token limits.
- Retain the existing native publication→CheckMutation gate and all immutable provenance/receipt/history behavior. If it already enforces active receiver refusal, use that authoritative path; do not duplicate it or bypass it to make a positive pass.
- Require exact surrounding receiver bytes and source bytes unchanged, intended native body/owners and caret, correct dirty/history state, independent Bold/Underline composition, and refusal at active Italics gaps including source plain prefix/suffix. No font/style packet imports or normalization.
- Re-run actual RED tests and existing insertion/history/admission regressions. If expected safety cannot hold under the existing APIs, stop production expansion for reviewed design/ownership amendment.
- Production owner: everyday.go only. No parallel writer.

### T346 — real runtime save/reopen, verification and honest handoff

- Through normal Runtime in a disposable root: load named receiver; move caret; retrieve cached source via actual selected entry/confirmation/I/O; verify source identity unchanged; save receiver to its own binding; reopen and inspect native source owners and unaffected receiver text. Exercise edited New first-save to a fresh name with real publication/binding and retained genesis identity. Cancel and stale/foreign completions cannot publish a different document.
- Preserve source file bytes and independently compare intended body plus only documented existing publication prefix changes. Native no-edit reopen/save stays byte-identical. Test actual native candidate/print projection without claiming it is an original occupied-Retrieve differential.
- Run required formatting/diff/full Go tests/vet/build, meaningful focused tests and focused race; derive Windows own-module production package closure from the actual application and record exact targets for cross-vet/build. Preserve PowerShell/overwrite regression behavior. No Mac commands; no new native Windows execution is claimed by cross-checks.
- Commit source/tests/evidence with baseline/RED/GREEN/candidate hashes, exact commands, failure/skip truth and a pending genuine-original qualification checklist. Return frozen candidate to root for independent review; do not move lifecycle yourself or edit audit/matrix status.

## Test Strategy

Tests must use independent expected cached native owners and actual source/receiver bytes, not repeat the implementation's flag logic. Required cases: one/multiple balanced source runs; plain leading/trailing source; independent Bold/Underline overlap; all receiver ON/OFF boundary gaps; active Italics refusal; unchanged plain-source behavior; Copy/Insert caret differences; empty source/no-op; malformed/unbalanced/opaque and size/foreign/stale refusals; existing history; loaded/edited-New identity; runtime Yes/No/cancel, save and reopen.

Focused names should share `TestRetrieveItalics` for new tests. Suggested verification: `go test ./internal/document ./internal/editor ./internal/tui -run 'TestRetrieveItalics|TestEveryday.*Insert|TestLiveWorkspaceNestedSelection|TestFontAppearance'`; corresponding focused `-race`; `gofmt -l` owned Go files; `git diff --check`; `go test ./...`; `go vet ./...`; `go build ./...`. Use project toolchain and final candidate exact closure. Existing environment/native-only skips and pre-existing Windows research-helper failures must be reported precisely, never renamed all-green. No Mac.

## Risks & Mitigations

- Blind allowlisting can duplicate a receiver's active Italics ON and break surrounding formatting. Frozen contract requires refusal and authoritative candidate validation, tested before coding.
- Original attribute fixture is not an original Retrieve oracle. Preserve explicit later reference gate and full E3 backlog; do not promote scenario status or bundle a private installation.
- Post-edit native prefix flags may legitimately change through the existing writer. Explain exact required differences; retain unrelated packets and no-edit byte identity, never broadly normalize.
- IO completion notices/accounting may advance on a real refusal; distinguish immutable document/disk safety from pretending no authenticated read occurred.

## Review Guidance

Review RED commit before code, exact one-production-file diff, active receiver safety table, genuine rooted Runtime path, source/cursor/history/first-publication provenance and truthful verification. Reject invented original proof, replay of expired grants, new macro/API source, broad attribute/prefix admission or hidden pending matrix promotion. Source completion is separate from the later genuine original occupied-Retrieve/native reopen/edit/print/save qualification; that writer-interoperability obligation is mandatory before corresponding compatibility/mission claims.

## Activity Log

No lifecycle events exist for this proposed package. Registration, claim, implementation/review and status events must be issued through canonical commands by root after independent proposal review; history remains empty here.
