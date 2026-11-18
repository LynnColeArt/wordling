---
work_package_id: WP110
title: Bind ordinary Runtime completions to their actual queued request
dependencies:
- WP94
- WP84
- WP85
- WP89
requirement_refs:
- FR-004
- FR-005
- FR-006
- NFR-002
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity.
  During /spec-kitty.implement this WP may branch from a dependency-specific base,
  but completed changes must merge back into feat/wp51-parity unless the human explicitly
  redirects the landing branch.
subtasks:
- T356
- T357
- T358
phase: Ordinary Runtime completion ownership before public integration closure
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/model.go
create_intent:
- internal/tui/io_completion_ownership_test.go
- internal/tui/evidence/io-completion-ownership/
execution_mode: code_change
owned_files:
- internal/tui/model.go
- internal/tui/runtime.go
- internal/tui/io_completion_ownership_test.go
- internal/tui/original_test.go
- internal/tui/editable_test.go
- internal/tui/model_test.go
- internal/tui/evidence/io-completion-ownership/**
role: implementer
tags:
- m1-continuation
- registered-continuation
- runtime-completion-ownership
task_type: implement
tracker_refs: []
---

# WP110 — authenticate ordinary Runtime completion bookkeeping

## Concrete defect and source boundary

WP107's minimal reproduction opens two real Runtimes, holds the current Runtime's actual callback, executes the foreign Runtime's real callback with coincident Operation/Revision/ReadSelection, and feeds its opaque message to current Model.Update. At f6abda6b, completeIO removes the numeric unsettled key before Session authenticates the result. Native/source/binding and the correct Session.Pending remain safe, but PendingIO wrongly becomes0 with the actual own callback unexecuted. The reproduction and exact model/runtime pins are frozen in the adoption packet; this is not a synthetic successful Result or a storage corruption claim.

Load actual implementer-ivan/action implement governance on normal owned claim. Dependencies WP94/WP84/WP85 supply actual Session/UI/runtime seams, and WP89 is the actual installed runtime/proofreading owner of both production files; there is no dependency on unfinished107. WP107 retains all existing predecessors and adds110, with ROOT/reviewer withholding107approval until110is independently approved. Do not reverse that edge or fake source approval. Use source-pinned ec868755 CLI/owned checkout from AGENTS.md. Source changes are limited to model.go/runtime.go. No new editor API or editor/storage/first-save/macro/proof production owner is authorized.

## T356 — real RED and ordinary-completion ownership census

Capture official clean pre-code baseline plus raw executed results and source/fixture/toolchain pins. Commit a genuine failing test for two actual public Runtimes and opaque callbacks before any production edit. PendingIO must stay1 after the foreign completion, authentic current Pending/document/source/binding/caret/history/native/dirty state must remain intact, foreign and current Completed accounting stay separate, and the correct held callback must still settle exactly once. Repeat with two independent opens of the same root and colliding numeric keys; numeric equality, path or inode does not confer host/request ownership.

Inventory every production ordinary resultMsg constructor, dispatch/queue caller, operation/unsettled removal, detached reconciliation and source/report access. Distinguish existing authenticated first-save, ReadMacro and proofreading envelopes from ordinary results; preserve their actual contracts and tests rather than using them as an invented generic receipt. Review relevant source/history for a recurring or contested ownership class; if DIRECTIVE040's actual trigger is established, stop for its prescribed structural review before applying another point fix. This task already requires a structural ordinary-message ownership contract across all ordinary kinds, not a ReadSelection-only conditional.

Acceptance tests must compile on actual pre-code source and fail for the real accounting/ownership cause, not missing new private types. Include genuine callbacks for success, real stale/read failure, Runtime.Close/capacity refusal before IO, own cancel→late completion, retry/new request, duplicate callback invocation and reordered delivery. Keep actual disk/publication outcomes truthful: UI cancel never cancels already executed filesystem IO, and a genuine own late publication requires reconciliation. A foreign message must neither clear current work nor inject a detached publication warning. Exercise persistent/stale Model copies so stale UI authority cannot steal a valid pending receipt.

## T357 — bind all ordinary queue completions without weakening consumers

Implement one private Runtime/per-issued-request ownership envelope or equivalent sealed private receipt for Model-issued ordinary callbacks, created only by the actual queue/dispatch route. Validate host and exact queued-request identity before removing unsettled work, updating reconciliation or forwarding the completion to Session. Keep ordinary Session result authentication intact. No caller-controlled numeric fields, copied metadata, path/inode equality or a new public grant/query factory substitutes for actual queue custody. The actual dispatch remains called from live Model.reduce, and all real completion paths (including stopped/capacity/error results) carry correct custody; no dead helper or partial producer migration.

Retain existing bounds, one actual execution per admitted operation, receipt accounting, source ownership, immutable copied results and error/reconciliation semantics. Genuine own late completions settle only their own outstanding work and preserve new pending requests; duplicates and foreign/stale messages cannot consume another receipt. Reuse current synchronization/lifetime mechanisms. Do not change storage effects, result proof semantics, receipt ceilings, source admission or generic shell/platform behavior.

Existing private resultMsg's one-field shape may be retained as an explicitly unbound/refused input so unchanged negative tests compile, while real queued callbacks use the new owned path. It must not remain an unauthenticated path to ordinary bookkeeping or Session state. Diagnostic runtime.command observations may retain a raw non-UI-authenticated shape only if the call-site inventory proves no ordinary live Model route bypasses queue ownership; ReadMacro's existing specialized caller remains unchanged. An actual need for an extra production owner is a reviewed source-amendment blocker.

The three existing test owners are narrow compatibility/negative fixes, not permission to rewrite assertions broadly. In original_test.go, the synthetic uncertain result currently asserted as positive SaveUncertain must become an explicit unbound-error refusal preserving real pending work. In editable_test.go, stop mutating a real publication's Err and treating it as an authentic positive uncertainty receipt; verify the genuine publication normally, then an unbound forged-error refusal with correct state. In model_test.go, update only actual callback-envelope/Close/diagnostic result assertions affected by the ownership route, preserving all substantive lifetime/accounting/foreign/stale checks. Never manufacture a fake owned receipt, discard a genuine acceptance failure, or report these forged negatives as real publication-uncertainty proof. Existing storage uncertainty/failure evidence remains independently scoped; genuine owned error handling must still retain uncertainty/reconciliation when it actually occurs. No test-only production hook or qualification-fault activation in normal builds.

## T358 — full verification and independent handoff

Run owned gofmt/diff checks, focused real Runtime/foreign/stale/duplicate/Close/new/macro/proof/save tests, focused editor/TUI/storage race, and full Go test/vet/build. Cross-vet/build the exact Windows production app closure; preserve broad pre-existing research-helper failures and real skips separately. No native-Windows claim from cross checks, no Mac build/test and no reference/TEST/P/CONTROL/original/whole-campaign clock action. Retain PowerShell/default-shell/overwrite guarantees for later exact-candidate Windows CI.

Freeze raw RED/GREEN/failure outputs, all source/test hashes, exact actual callback/receiver/Completed witnesses, ordinary-kind producer/consumer matrix, baseline scope and every current canonical contract disposition with concrete examples. The original15contracts and new103coverage JSON/MD have separate roles; provisional/unapproved planning snapshots are not product acceptance. New private receipt constants/kinds get independent mirrored behavioral tests, with no invented original WP enum or public format change.

Commit only declared owners, leave a clean candidate and request a different independent reviewer. ROOT captures the verdict. Do not selfapprove/push/promote audit, CMD51-065/E3, matrix/M1 or production readiness. The consumer107test bytes must remain opaque to the new private type so they can compile unchanged on the exact pre110/pre109/pre106 sources. Full old9f107replay honestly retains this distinct PendingIO control failure alongside insertion/Copy UnsupportedBody; preserve/classify all failures, additionally run unchanged relevant positive-only selections for each causal source defect. Never overlay later fixes onto an exact-old-tree claim or relabel an unrelated/setup failure as native causal RED.

Use the normal owned single primary checkout, one source/index writer. Keep all authored work committed and remove approved disposable /tmp source archives after preserving evidence; never projects worktrees. All49M1families and original/native interoperability gates remain in scope; Mac testing stays at milestone end.
