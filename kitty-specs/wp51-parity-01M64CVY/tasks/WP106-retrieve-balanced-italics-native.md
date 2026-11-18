---
work_package_id: WP106
title: Admit balanced native Italics at the checked document insertion seam
dependencies:
- WP99
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- FR-008
- NFR-002
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T344
- T345
- T346
phase: Native insertion safety; public integration and original qualification remain separate
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/document/everyday.go
create_intent:
- internal/document/retrieve_italics_test.go
- internal/document/evidence/retrieve-italics/
execution_mode: code_change
owned_files:
- internal/document/everyday.go
- internal/document/retrieve_italics_test.go
- internal/document/evidence/retrieve-italics/**
role: implementer
tags:
- m1-continuation
- registered-continuation
- retrieve-italics-native
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP106 — balanced native Italics insertion safety

## Do This First: Load Agent Profile

This canonical task adopts the independently reviewed scope in `kitty-specs/wp51-parity-01M64CVY/continuation-2026-11-18/delivery-task-adoption/reviewed-packets/retrieve-italics-resliced-proposal`. Resolve implementer-ivan/action implement through the actual CLI and governance at the normal claim. Runtime status and approval live in canonical status/events; this authored scope does not create a claim, grant, model identity or completed subtask. Read the immutable reviewed packet, source pins and applicable contracts before work.

## Review Feedback

Read the event-log review_ref, independent task/design feedback, coverage-conservation.md and the unchanged receiver-contract.md before coding. Address real feedback and record progress chronologically through normal workflow. ROOT controls status/review capture; do not fabricate approvals/history or self-approve.

## Objectives & Success Criteria

- Add self-contained balanced native Italics source owners to the existing checked InsertDocument/InsertBlockCopy seam; preserve exact receiver/source owners, bytes/birth, bounds, caret and history under the frozen receiver contract.
- Commit native acceptance tests and actual UnsupportedBody RED evidence before touching production everyday.go. Existing atomic-refusal controls must pass in that RED checkpoint.
- Make only the minimal authorized source-owner/balance change in everyday.go, retaining the existing final publisher→CheckMutation receiver gate.
- Freeze native GREEN/source/provenance and Linux/Windows source-check evidence for independent review. Public rooted Retrieve/Runtime/save/reopen acceptance belongs to subsequent WP107; this core alone cannot claim it.
- Keep original occupied-Retrieve and native original reopen/edit/print/save qualification explicitly pending. Do not promote CMD51-065, E3, audit or mission matrix.

## Context & Constraints

Read .kittify/charter/charter.md, docs/compatibility.md, docs/roadmap.md, active M1 spec/plan/tasks, continuation full-family/acceptance-closure artifacts, receiver-contract.md, coverage-conservation.md and this proposal's source-pins.json. The original single-package proposal and reslice review are retained immutable provenance, not an instruction to edit editor/TUI production.

Current everyday.go admits balanced Bold/Underline but rejects Italics in insertDocument. Native admission/authoring/layout/rendering already support the Italics owners; the cached original ITALICS.WP records their encoding, not original occupied-Retrieve semantics. Only body owners already supported by ordinary admission are in scope: no style/font/prefix/resource transfer, parser/prefix/admission expansion, format conversion/intermediary, new API/writer, macro change, fixture/archive edits or external-source acquisition.

WP99 carries the actual native chain WP80→WP92→WP97→WP99 and broad document routing predecessors. Source presence is not approval: ROOT checks actual authoritative dependency state and ownership at normal finalization/claim. The consumer/session/UI predecessors remain in WP107 and are not removed from the complete delivery.

## Branch Strategy

Planning base/merge target: feat/wp51-parity. Use the actually issued canonical owned checkout. If supported isolation is necessary, use the required worktree tool under ~/work-trees or /tmp, clean it up and leave authorized work committed. Never create a worktree under projects. Preserve other agents' index/source; request a ROOT quiet point for commits. WP104/105 reference source is disjoint; this package grants no original/VM/reference process or Mac testing.

## Subtasks & Detailed Guidance

### T344 — freeze native contract and commit genuine test-first RED

- Freeze exact pre-core Git/source/fixture/template inputs and normal project baseline before any production change. The pre-core checkpoint must remain addressable for WP107's later causal replay.
- Create only internal/document/retrieve_italics_test.go plus native evidence. Commit tests while everyday.go remains byte-identical to the approved baseline; preserve exact commands, exits, case names and raw JUnit/Go evidence. New native positives must fail at the actual existing UnsupportedBody source refusal, not compilation, setup, missing fixture or another gate. No skip/xfail/mock implementation or fabricated result.
- Parse the existing pinned docs/research/reference-runs/mission1-appearance/ITALICS.WP through actual public native admission. Use independent expected native owner bytes/identities and actual source/receiver images; do not copy the new flag algorithm as the oracle or use ANSI style guesses.
- Test InsertDocument and InsertBlockCopy at beginning/interior/end and all four gaps immediately before/after receiver ON/OFF. Outside Italics succeeds; inside an active receiver span, any source Italics pair (including plain leading/trailing text) refuses atomically; plain source inside Italics retains existing behavior. Independent Bold/Underline composition succeeds only without duplicate same-attribute conflicts.
- Cover one/multiple balanced source runs, duplicate ON/unmatched OFF/unclosed source, opaque/unsafe input, empty/no-op, limits, foreign/stale cursors and native candidate validation. Verify unchanged source/receiver bytes, revision, cursor, dirty/history on refusal. Existing negatives should already pass.
- No parallel writer; no production change in this subtask.

### T345 — minimally admit independently balanced source Italics

- Edit everyday.go only. Add a separate Italics balance flag in the existing bounded source scan as Bold/Underline use today; admit exact ItalicsOn/Off owner bytes, reject duplicate/unmatched/unclosed source owners before publication, preserve the existing allowlist and byte/token limits for every other kind.
- Preserve semantic demotion of existing derived boundaries, receiver prefix/birth, immutable provenance/receipts/token mapping and InsertDocument versus InsertBlockCopy caret behavior. Source contributes no prefix packets, cache/resource or binding.
- Retain native publication→CheckMutation as the authoritative receiver validator. Prove it enforces active-receiver refusal under actual tests; do not duplicate its state machine, weaken it or broadly normalize formatting/prefixes to force GREEN.
- Require exact intended inserted body and surrounding owner relationships, independent source bytes unchanged, correct dirty/history and no-op behavior. Any needed production source outside everyday.go or unsupported safety result stops for an independently reviewed scope amendment.
- Re-run real committed RED tests plus existing insertion/history/admission regressions. No parallel writer, public path rewrite or alternate writer.

### T346 — complete native verification and independent source handoff

- Complete every native row of coverage-conservation.md and receiver-contract.md, including all source/receiver balance/boundary/independent-attribute/Copy-versus-Insert/empty/opaque/bounds/foreign/stale/history cases. Keep independent byte/caret/provenance expectations.
- Explain only existing justified publication flag/offset differences; preserve unrelated packets. Native no-edit reopen/save must remain byte-identical. Exercise actual native candidate/print projection only as source behavior, not an original Retrieve or printer oracle. Do not edit original fixture/replay/resource bytes or claim a real original process ran.
- Run gofmt on owned Go files, git diff --check, full go test ./..., go vet ./..., go build ./..., meaningful focused insertion/appearance/history tests and focused race. Derive the actual Windows application's production package closure and perform source-bound cross-vet/build using the selected toolchain. Preserve PowerShell/default-shell/overwrite behavior; distinguish unchanged pre-existing research-helper cross failures and environment/native-only skips from scoped failures. No Mac commands. Cross checks do not mean native Windows execution.
- Commit authorized source/tests/native evidence with baseline/RED/GREEN/source hashes, test ordering, exact command/exit/skip truth and pending original-qualification checklist. ROOT obtains a different independent native reviewer; do not self-transition/approve/push.
- Native approval is a prerequisite for WP107, not proof that its real rooted public Retrieve/save/reopen obligations are complete. Preserve the exact pre-core source and RED commit for later same-test integration replay.

## Test Strategy

New tests share TestRetrieveItalics. Focused example: go test ./internal/document -run 'TestRetrieveItalics|TestEveryday.*Insert|TestFontAppearance', plus corresponding focused -race and relevant history/admission tests. Use actual selected cases and current project toolchain; full Go checks remain required. Tests verify behavior/data integrity, not implementation flags or snapshots of fabricated receipts. The complete receiver and coverage contracts are binding; no new binary parser or broad fuzz campaign is introduced.

## Risks & Mitigations

- Blind allowlisting inside receiver Italics can duplicate active ON state. Frozen atomic refusal plus final native validation must prevent it before any result/publication.
- A cached original attribute example is not an occupied-Retrieve/native interoperability oracle. Genuine original differential and reopen/edit/print/save gates remain mandatory later, not permanent exclusions.
- Required writer flags/offsets can change after edits; explain exact justified changes and preserve unrelated bytes. No-edit saves remain identical.
- This native slice has no rooted public user-path evidence yet. WP107 explicitly retains all that work; do not declare the overall Retrieve delivery complete from this package.

## Review Guidance

Verify genuine native RED commit before production edit, exact one-production-file diff, all frozen receiver/native negative cases, source/receiver identity and provenance, immutable original fixture pins, full verification truth and scope. Reject API/parser/prefix/resource/macro expansion, fabricated original proof, hidden audit/matrix promotion or unowned source. Original qualification and public integration remain independent required gates.

## Activity Log

The immutable proposal and review history are retained in the adoption packet. Normal finalization/claim/review commands record actual lifecycle events; no runtime state or completion is authored here.
