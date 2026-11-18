# Proposed append after existing WP99/T325

DRAFT ONLY. Do not apply/finalize while current CLI assumes two-digit WP IDs. Preserve the existing tasks.md bytes as the prefix and all99 histories; never reuse/renumber completed packages. No canonical status is advanced by this fragment.

## Work Package WP100: Admit authenticated nested macro reads on current New buffers (Priority: P1)

**Prompt**: `tasks/WP100-new-buffer-nested-macros.md`

**Dependencies**: WP65, WP66, WP82, WP69, WP71, WP73, WP76, WP84, WP85

**Requirement Refs**: FR-002, FR-004, FR-005, FR-006, FR-012, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002

### Included Subtasks

- [ ] T326 demonstrate the gap through real New Session/Runtime paths. Add four failing, source-hash-bound tests using the actual original-cases.json WPM exports for CMD51-210/212/213/230. Reach a genuinely initialized NewUnpublished buffer via normal constructors and public Macro prompt/read/Complete/StartMacro. Do not retrieve EMPTY.WP, parse an empty file, inject a loaded source or delete a loaded document to simulate New. Use actual ExecuteMacroRead for every root/child/missing result. Show the existing New-only resolver refusal causes the intended failures. Keep loaded paths as regression controls.
- [ ] T327 reuse authenticated child acquisition and the same serialized owner. Permit nested resolution for a still-current New macro target, preserving the same r.valid/current/expected-transition checks before/after every step and Resume. Root-only target.unedited checks must continue to guard root acquisition; a legitimate root/child edit must not be mistaken for a stale root acquisition. Bind each child request/result to its accepted operation/revision/run/request/parent, rooted directory/name, actual buffer and screen, source identity and current execution owner. Reuse `newMacroReadProof`, `ExecuteMacroRead`, `acceptedMacroResult` and actual VM Resume. Only a genuine rooted missing observation becomes CommandError; fabricated missing wrappers, permission/host I/O errors and wrong-source results must not acquire original ON ERROR semantics by convenience.
- [ ] T328 public integration, adversarial provenance and first-save checks. Use both captured repetitions' source inputs where available and slice quotas 1 and16. For pristine New receivers, assert exact bodies HANDLED, PCHILDRPARENT, PCPARENT and PCCHILDBADRDONE; for edited New declare initial bytes/caret and assert the complete receiver preserving those bytes around macro output; assert real caret, dirty/native revision and unchanged Birth/genesis, New phase/source/name, source WPM bytes, execution completion, parent/child receipt provenance and no duplicate application. Cover child request/source/name/root/parent/run/screen/revision/operation tampering; swapped result from another driver or buffer; stale pre-edit Session/fork replay; duplicate/out-of-order Resume; pending child cancellation/host stop; host error versus real not-found; and unsupported names refusing without mutation. Preserve existing loaded, new root, ownership/fork/ready/first-publication regression suites.

## Work Package WP101: Prepare a reviewed original route for four unsaved-New macro probes (Priority: P1)

**Prompt**: `tasks/WP101-new-buffer-reference-route.md`

**Dependencies**: WP38, WP63, WP64, WP70

**Requirement Refs**: FR-001, FR-012, NFR-002, NFR-003, NFR-004, C-004, C-005, C-006

### Included Subtasks

- [ ] T329 choose and document a genuinely authorized original route. Read current original safety contracts, WP38/63/64/68/70 source/approval evidence, the infra-recovery diagnosis, and the exact candidate closure. Record which original route actually satisfies source binding, actual process ownership, exclusive private run root, one leaf/one use, immutable source/plan/case/repetition, bounded deadlines/accounting, authenticated readiness, retained-process stop and stopped read-only export/publish. Supply source hashes and attributable review references. Existing controller `ReferenceController.open_leaf` admits only TestGrant; WP70 is harmless TEST only. TestIssuer/TestGrant is NOT an original route. Legacy smoke.main/guest globals and a `--allow-vm` flag alone are also not proof of the current protocol.
- [ ] T330 add an offline-by-default four-case recipe. New file only, with explicit offline preparation as the default. Preserve historical sources. Reuse authentic WPM exports and expected bodies through immutable paths/hashes in original-cases.json; record both source repetitions. Candidate recipe only selects CMD51-210/212/213/230; no arbitrary script, input path or regex case expansion. Keep root directory C:\OUT and exact parent/child names/identities. Ensure MISSING is genuinely absent in the private stopped/prepared fixture, not replaced by injected fake I/O. Each run starts a fresh real unsaved Doc1 with no Retrieve/EMPTY.WP surrogate. Before invocation record the blank/current filename/new-document state, original status, actual cursor and native/source start facts available from the original UI; establish the same conditions for the separately declared already-admitted edited-New variant. Capture errors/results/cursor and native save/export. Compare root/child WPMs before/after and retain source hashes.
- [ ] T331 offline negative checks and prelaunch review. Test denial without a genuine original release, foreign/spent/wrong-case/wrong-source/wrong-plan grants, dirty/existing run root, wrong master/resource/tool identities, live export, unexpected MISSING presence, new-vs-loaded receiver mismatch and deadline failure. Tests use harmless fake resources/TEST interfaces explicitly; a green TEST result is never original evidence. Reproduce infrastructure faults without weakening safety conditions. If fixes require source outside owned_files, submit a separately reviewed explicit amendment before launch.

## Work Package WP102: Qualify unsaved-New nested macros against fresh original runs (Priority: P1)

**Prompt**: `tasks/WP102-new-buffer-original-qualification.md`

**Dependencies**: WP100, WP101, WP86

**Requirement Refs**: FR-001, FR-002, FR-004, FR-006, FR-012, NFR-001, NFR-002, NFR-004, C-004, C-005

### Included Subtasks

- [ ] T332 execute source-reviewed finite original leaves. After WP101 is independently approved and the root issues fresh exact-case source/plan-bound grants, execute the declared New cases through the reviewed original route under exclusive ownership. Start fresh private copies and verify March03/09/92 environment/resources, unsaved Doc1 and exact receiver context immediately before invocation. Use two independent repetitions per context. Preserve all failed attempts and logs without replacing archived results. Retain source/grant/plan/tool/environment/resource hashes, controller ownership/accounting/readiness/stop/export evidence, UI/cursor traces and native/WPM outputs. Export only after actual retained process closure, using the selected stopped read-only route. No direct live-image reads or arbitrary private-media redistribution.
- [ ] T333 candidate comparison and original interoperability. Build the exact WP100-containing candidate and bind its source/binary hashes. Run the new terminal qualification via Run/ALT_F10/F10 and actual rooted child files, without any empty-file retrieval. Compare reference vs candidate native bodies and cursor/dirty/source/name/error outcomes for CMD51-210/212/213/230. Assert exact outputs HANDLED, PCHILDRPARENT, PCPARENT, PCCHILDBADRDONE where the original actually observes them; preserve mismatches rather than normalizing bytes. Both original WPM repetitions remain byte-identical and unchanged. Run loaded controls through macro_control.py. Qualify pristine New and each edited-New context claimed by WP100 separately; do not imply Repeat3/Doc2/selection/Reveal/recording completeness.
- [ ] T334 truthful audit disposition and independent evidence review. Create new manifest/report linking exact case→start state→source→reference repetitions→candidate run→original reopen/edit/print/save→tests. Run focused/full build/test/vet and relevant race/format checks after new code. Independently review original safety and actual differential evidence. Only then change the four specific audit rows/counts if their complete listed remaining New obligation is satisfied. Existing body/handler claims remain bounded by the observed contexts; new broader feature branches stay visible in the full coverage ledger. All four rows remain partial for any unexplained mismatch or missing New context comparison. This WP cannot close FR012 or Mission1 by itself.

## Work Package WP103: Reconcile full Mission1 obligations without rewriting historical evidence (Priority: P1)

**Prompt**: `tasks/WP103-full-mission-coverage-index.md`

**Dependencies**: WP05, WP21, WP86

**Requirement Refs**: FR-001, NFR-004, C-003, C-004, C-005, C-006

### Included Subtasks

- [ ] T335 census every source scope and current evidence. Bind spec/charter/compatibility/inventory/workbook/coverage contracts, current command audit and exact candidate to hashes. Index all244 scenarios, all91 feature groups, all36 workbook lessons, G01–09 uncovered starts, appendix/version/menu/utility obligations and all38 FR/NFR/C/FC plus SC001–005. Preserve original documentary/implementation/oracle roles independently; historical "not implemented" text is a dated snapshot, not a reason to erase delivered code or mark current code missing. Conversely186 verified representative scenarios are not proof of entire parent groups/lessons. Record exact immutable source/tests/reference/resource links and remaining branches for each row.
- [ ] T336 make missing leaf expansion and delivery independently schedulable. Use the accompanying full-family plan as an initial assignment map. For each parent/lesson assign exact source spans, known expanded leaves, gaps, reviewer, next research slice and downstream implementation/evidence dependencies. Partition complete source study into bounded family/chapter and lesson batches rather than a single rest-of-M1 WP. G01 font-marking, G02 file deletion, G03 display settings, G04 mouse setup, G05 Overstrike, G06 paragraph numbering, G07 menus, G08 Screen and G09 diagnostics/PIF each retain their distinct contracts. Every missing step/leaf gets a stable local ID with source/version/resource/negative/cancel/failure variants; no invented official CMD ID or verified label. Propagate all newly discovered work back into explicit continuation proposals; the current58 rows are a floor, not a cap.
- [ ] T337 acceptance evidence schema and mechanical audit. Define per-claim source/version/resources/receiver/context/commands/reference outputs/candidate outputs/native/print comparisons/test IDs and candidate hash; independent verifier/date/disposition are required before closure. For acceptance-matrix FR rows provide coverage links only, leaving pending verdicts unchanged. Add companion rows for 5NFR/6C/10FC/5SC and meaningful negative invariants (wrong password/malformed input, stale/foreign requests, overwrite refusal/disk failure, unknown payload preservation, resource absence, failure-safe concurrency). Track zero-unclassified requirement separately from zero unexplained mismatch.


Review amendment R1 (2026-11-18): WP100 owns internal/editor/new_macro_test.go and internal/tui/new_macro_test.go for narrowly replacing the superseded unconditional nested-call refusal while preserving real host-error, cancellation, partial-effect, provenance and UNKNOWN negatives. Production ownership remains only macro_execution.go. Edited-New results preserve declared initial receiver bytes/caret.
