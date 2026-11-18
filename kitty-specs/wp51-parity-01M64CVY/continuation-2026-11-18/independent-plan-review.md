# Independent continuation plan review

Reviewer Renata resolved through `spec-kitty agent profile show reviewer-renata --json`; action-scoped charter and required compatibility/roadmap documents read. Reviewed proposal against actual source at the roster candidate `f1ca9686febe3868fc5c344ba0f7f9d24ba201b9`. Every `first-slice-source-roster.json` hash still matches the current file. Repository/runtime were not mutated.

**Verdict: request one narrow amendment before approving WP100.** The bounded product seam and WP101–103 sequencing are otherwise sound. This is a plan review, not completed product or M1 acceptance.

## Blocking finding R1 — WP100 cannot satisfy its ownership and full-suite gates together

Location: `continuation-proposal/tasks/WP100-new-buffer-nested-macros.md:37-42`, `:68`, `:72-76`.

The package authorizes changes to only `internal/editor/macro_execution.go` plus new tests/evidence, while requiring general VM-based New nesting, no case/source switches, preservation of the existing regression suites, and a passing full Go suite. Two existing tests explicitly encode the superseded root-only policy:

- `internal/editor/new_macro_test.go:390-419`, `TestNewMacroNestIsHostFailureBeforeChildIOAndPartialEffectsRemain`, stages a real CHILD.WPM, invokes a valid New root with NEST, and requires HostFailure, no pending child, exactly BEFORE, and rejection of child continuation.
- `internal/tui/new_macro_test.go:447-474`, `TestNewMacroNestPartialHostFailureAndStaticUnknown`, stages CHILD.WPM and requires the nest/handler-nest variants to fail before child I/O, excluding AFTER/HANDLED and requiring only one completed root read.

Both tests pass unchanged today: `go test ./internal/editor ./internal/tui -run 'TestNewMacroNest' -count=1` passed. Their successful old refusal assertions necessarily conflict with the proposed general admission at `internal/editor/macro_execution.go:249-250`. Adding new tests cannot change those assertions. Preserving them by source/fixture special-cases would violate the proposed architecture and test real behavior incorrectly.

### Minimal amendment

1. Add **existing** `internal/editor/new_macro_test.go` and `internal/tui/new_macro_test.go` to WP100 `owned_files` only. Do not add them to `create_intent`, renumber old WPs, rewrite historical approvals, or alter archived evidence.
2. Clarify “Source edits are limited to macro_execution.go” as **production source edits** are limited to that file; the two named existing test files may receive narrowly scoped contract updates.
3. Add to T328: replace the obsolete unconditional New-NEST refusal assertions in those two test functions with the newly admitted authentic child-read/resume/result behavior. Preserve the setup and excavated assertions about actual prior effects, dirty/native state, source/name identity, completion/receipt accounting and duplicate rejection. Preserve the UNKNOWN static-preflight subcase and zero-effect refusal unchanged. Retain meaningful host-error/cancel/partial-effect negative coverage by exercising an actual rooted host I/O error or cancellation; do not continue using a valid child call as a fabricated host error. No deletion, skip/xfail, fixture-name special-case, or weakening of unrelated tests.
4. Update the rationale/README and any generated ownership/validation artifact to describe one production owner plus these two bounded existing test updates. Re-run offline ownership/preservation validation; the old 99 prompts/tasks prefix and archived evidence remain immutable.

No additional production-file amendment is proven necessary by this review. Existing `newMacroTarget.current`, serialized owner/transition validation, rooted read proof, accepted acquisition, Resume and normal Runtime child scheduling provide the proposed seam. Any implementation-discovered defect outside that seam still needs the package's precise reviewed amendment process.

## WP100 acceptance correctness

The source diagnosis is accurate: `Resolve` contains a New-only unconditional refusal at lines249–250; root construction/admission and `target.unedited` live separately and must remain intact. Existing `macro_execution.go:96-119,239-309`, `new_macro.go:44-60`, `macro_load.go:30-79`, `macro_session.go:156-188` and `internal/tui/macro_runtime.go:110-207` support one driver and authenticated actual I/O without a second VM or direct writer.

The four outputs are historical authentic-source hypotheses, not fresh New reference evidence. WP100 correctly keeps CMD51-210/212/213/230 partial and limits its approval to product delivery. For the edited-New test variant, the implementation must declare concrete initial bytes/caret and assert the **entire resulting receiver**, preserving initial text around inserted macro output. The bare HANDLED/PCHILDRPARENT/PCPARENT/PCCHILDBADRDONE bodies describe pristine New outcomes; they must not accidentally erase a nonempty receiver. WP102 already requires each claimed edited context to be qualified separately.

## WP101–103 scope and dependency assessment

- **WP101:** Correctly distinguishes an executable reviewed original route from TEST-only controller success or historical smoke grants. It may prepare offline independently of WP100; completion requires real route delivery/review, and absent authority/source support leaves it incomplete pending an exact amendment. No VM launch is implied by plan approval. The current CLI three-digit-ID defect is an independent tooling issue, not a rejection of this plan.
- **WP102:** Correct dependencies on WP100+WP101, fresh two-repetition context-bound original runs, exact candidate comparison, native original reopen/edit/print/save and candidate reopen. Existing `macro_control.py:14,37-47` genuinely retrieves EMPTY.WP for these four cases, so preserving it as loaded coverage and adding a distinct New runner is necessary. Conditional four-row audit promotion cannot close FR012/M1; mismatches and unqualified contexts stay visible.
- **WP103:** Bounded current index/reconciliation, with explicit full source/lesson expansion follow-ons. It does not pretend 244 representative scenarios, 58 open rows, 91 parents or 36 lessons are exhaustive observed leaf coverage. It leaves all obligations and canonical verdicts pending, prohibits unowned executable helpers, and delivers scheduling/traceability rather than acceptance.

The 49-family backlog is an initial research/dependency map, not permission to implement broad multi-feature families. Its instruction to split into precise source-owned child WPs is necessary and retained. Existing resources should be qualified before any new media request; the separate resource discovery report identifies present WPK/language/printer/graphics inputs and a genuine public original4.2 producer lead.

## No fake full acceptance

The proposal explicitly retains all38 FR/NFR/C/FC obligations, SC001–005, meaningful negative invariants, original/native evidence, final-candidate platform checks, independent verification and canonical accept/merge/postmerge gates. Historical 99-WP queue exhaustion, this plan, green Go tests or a TEST controller cannot substitute. No dependency installation is proposed by WP100–103; supply-chain installation controls remain applicable to separately reviewed tooling/dependency changes, not silently passed by this review.

Approval can follow a revised plan that resolves R1 and preserves these boundaries. No implementation, source amendment outside the two tests, fixture acquisition, new VM authority or completed M1 claim is approved here.

## Revised-plan recheck — approved first bounded plan

Root applied R1 to the draft. Independently verified both existing regression files are owned, neither is falsely a create-intent, production edits remain limited to macro_execution.go, obsolete refusal assertions are replaced without deleting/skipping negative coverage, UNKNOWN preflight is retained, and edited-New full receiver preservation is explicit. README, rationale, tasks append and validation record the same amendment. WP100 SHA-256: `5057800a34c94a48ab68d412d968742ff8fc9e96b858825af1a1126e1861fb5d`.

**R1 disposition: changed; resolved. Verdict: APPROVE the revised bounded WP100–103 continuation plan for normal finalization/claims once the canonical tooling path is available.** This is not implementation approval, original-execution permission or Mission1 acceptance; all pending evidence, precise ownership, original safety, independent review and final full-M1 gates remain required. No further blocking source/acceptance finding was verified.
