# Independent WP67 code review — cycle 1

**CHANGES REQUESTED. READY_FOR_CANONICAL_REJECTION ONLY.** One blocking acceptance finding, F1. No canonical verdict has been executed; ROOT's exclusive quietpoint grant is required. Audience: ROOT and the WP67 implementer.

## Finding

**F1 [P2]: local compiled-source membership is incompletely bound.** `Session.build` in `scripts/reference/explicit_secondary_data.py:217–237` checks only local GoFiles against the approved manifest. Other enumerated compiled kinds are recorded without that approval check. A valid empty assembly addition to the frozen native package passes the public audit and replaces a prior successful report. This contradicts T200's all-compiled-native/wp51 source check and source-substitution refusal contract. Exact reproduction, expected correction and regression criteria are in [feedback.md](feedback.md).

The counterexample is real: all260 existing disposable-copy files matched the frozen sources; only the68-byte `internal/merge/native/unreviewed.s` was added. The actual compiler metadata records its SFile/source SHA, yet the launcher exits0 and reports24records/36fields/6empties/sixcohorts. The added member is absent from the approved manifest. No malicious payload, native-document overwrite or product-worktree modification occurred. The disposable Git HEAD is diagnostic only, consistently with the source-authority contract.

## Identity, scope and custody

Loaded Reviewer Renata through the normal resolver and review governance. All2142 generated review-prompt lines were read. The prompt's display header retains the implementer recommendation; the actual normal review-claim event and annotation name reviewer-renata/reviewer/codex/model-null. That diagnostic mismatch was retained, not repaired.

Reviewed frozen lane-x HEAD `be000145719ca2aaea328017d2da176356d2fb64`; product/source commit `5feffa6be17247b6b046fd5963367d8264a30302`. The actual claim-base `6c62c62f44c35a6fa3c12ff8d4586c5ffe9e6001` diff contains exactly94 additions in the three new owned scopes. The generated mission-wide diff includes inherited approved history and is not falsely counted as WP67 work. All93 sealed members plus root seal match actual Git/working bytes. Seal `e99fac71a7a6a7e469701966c71e2dcf49166bc3e6905238c776c6bdde39860d` verified. All59 immutable Git/blob pins and221 inherited working/Git byte identities verified; all221 Git executable-mode semantics agree. Three historical context/metadata roster paths have different working bytes, separately recorded rather than relabeled current provider inputs.

Canonical currency returned None: no merge/rebase/overlay. Product source stayed unchanged throughout. The only untracked lane file is the normal `.spec-kitty/review-lock.json` from ROOT's claim; it was retained untouched and excluded only from product-source cleanliness. No ignore/config/host repair occurred.

## Independent verification

| Check | Actual result |
|---|---|
| Configured review checks | WHOLE0; JUnit7 tests,0failures,0errors,0skips. Actual Go package discovery/build/test/vet included. |
| Affected Go race tests | WHOLE0 for explicit, real qualifier, native and wp51; count1/timeout90s. |
| Public Python workflow/OS suite | WHOLE0;9tests, including real ownership loss, exited leader/TERM-ignoring descendant, caps/timeouts, report guards and prior-report behavior. Raw ResourceWarnings remain visible; no clean-stderr claim. |
| Fresh actual public audit | WHOLE0; real30-image API qualification24/36/6/sixcohorts.102packages,4local,751compiled source members. All751 actual source hashes, compiler archives and pinned host tools independently rechecked. |
| New public API consumer probe | Seven finite control groups pass against exact copied production bytes: original/generic blocker, empty≠missing, equal-byte foreign Source refusal, wrapper/copy/span isolation, fresh Clara structural admission, framed opaque-owner refusal, role/zero refusal. Actual cwd/GOMOD/binary/source hashes retained. |
| Independent semantic mutants | Three compile-valid faults killed at intended public assertions: dropped source identity, missing→last empty, dropped opaque predicate. Executed only in a disposable exact-source module; source restored exactly. |
| Formatting/source checks | gofmt output empty; Python AST parses; changed-source whitespace0. Original raw evidence whitespace2 remains an author-declared raw-evidence limit. |
| Added-source authority falsifier | **FAIL**: build-valid unapproved SFile accepted; prior report replaced. This is F1, not a semantic-mutant kill. |

The unchanged600-second reader fuzz was not repeated. The author's separate60-second DATA fuzz/14mutants and evidence were inspected; independent results above are separately identified. No private original/resources, VM, old PID/grant or historical six-variant P61 campaign was accessed or retried.

## Contracts and public reachability

All15 contract artifacts were enumerated and classified in `contract-walk.json`. Native framing/preservation and automation's explicit-data context were checked against actual parser/consumer behavior; unrelated editor/TUI/layout/resource/macro/startup examples are not claimed implemented. Existing contracts and source remained unchanged.

The real caller is launcher→compiled qualifier→native.Parse/View→explicit.Admit→Data/Value getters. Every public DATA method is reached in that consumer; no observer clone or result writer substitutes for the API. Source-owned spans, whole View capture, defensive provenance and value copies, exact EF/HR/EOR/count/tail coverage and six opaque owner literals are present. The six literal octets independently equal both the documentary cohort set and actual API outputs. Actual Scope/missing-category literals are asserted through the consumer tests. Generic native Secondary admission remains blocked. Missing fields never acquire explicit-empty authority; raw StoredCount/opaque bytes remain uninterpreted. The source-closure gate defect is distinct from those otherwise passing DATA properties.

## Eight anti-pattern decisions

1. **Dead code — PASS.** Actual non-test qualifier/launcher reaches the new package and public getters.
2. **Synthetic-fixture test — PASS.** Runtime assertions use actual native Parse/View/DATA and compiled public consumers. Synthetic Clara/malformed variants are labeled structural tests.
3. **Silent empty return — PASS.** Invalid zero handles are explicit/non-authoritative; valid empty fields retain presence. Refusals exit nonzero; failed-attempt receipts are separate from qualification. Trusted admitted-span helper assumptions do not accept injected provenance.
4. **FR coverage — FAIL.** Narrow DATA assertions cover the intended FR-002/003/012 contribution, but T200/NFR-004 approved-source coverage is incomplete for non-Go compiled members (F1). Full parent requirements remain open.
5. **Frozen surface — PASS.**94additions only; all221 inherited bytes/Git mode semantics unchanged.
6. **Locked decision — FAIL.** F1 violates the explicit approved native/wp51 compiled-source boundary; no format/evaluator permission was otherwise broadened.
7. **Shared-file ownership — PASS.** Three new scopes only, no shared production edits; normal runtime metadata is separately coordinated.
8. **Production fragility — PASS.** New failures are explicit bounded refusals with prior-report protection where correctly identified; actual public cleanup/loss tests pass. F1 is the missing identification/gate, not a swallowed exception.

## Evidence limitations and review-harness reds

The author candidly retains early missing child stdout/transient incomplete-mutant outputs, raw lint2 and absolute shared build-cache size without claiming a delta. This review does not reconstruct those missing bytes or count invalid constructions as kills.

Reviewer metadata-only custody initially assumed the entire worktree clean; the normal review-lock disproved that assumption before positives. A reviewer mutant-runner syntax typo executed zero commands, and the first opaque mutant was compile-invalid because its variable became unused; both are disclosed and excluded from kills. The corrected opaque case alone was rerun and reached the intended runtime assertion. Source-closure setup first had a syntax error and then unnecessarily requested a historical cross-lane working path; no product invocation occurred in either attempt. The final bounded control copied only actual manifest/inherited/corpus inputs and reproduced F1. Standalone full raw command logs for those initial tool-level setup errors were not available; their tool tracebacks and explicit notes are retained, without a full-raw-history claim.

All38 obligations/91groups/36lessons/nested M1 and SC001–005 remain OPEN. No merge evaluator/PAGE/materialized-native writer/application Merge/PDF/original-execution authority is approved. Await ROOT publication/feedback/normal sole rejection; no self-fix, manual recorder, force or lifecycle mutation has occurred.
