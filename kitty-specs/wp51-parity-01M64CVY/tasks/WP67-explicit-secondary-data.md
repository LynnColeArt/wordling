---
work_package_id: WP67
title: Source-bound explicit Secondary DATA and maintainer qualification
dependencies:
- WP50
- WP53
requirement_refs:
- FR-002
- FR-003
- FR-012
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-wp51-parity-01M64CVY
base_commit: 9585c4d0279627b91ef6e266def92181f68fef3a
created_at: '2026-11-01T12:52:34.892296+00:00'
subtasks:
- T199
- T200
- T201
phase: Closed explicit-field DATA proof; generic execution and full M1 remain open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/merge/explicit/
create_intent:
- internal/merge/explicit/
- scripts/reference/explicit_secondary_data.py
- docs/research/continuation/explicit-secondary-data/
execution_mode: code_change
owned_files:
- internal/merge/explicit/**
- scripts/reference/explicit_secondary_data.py
- docs/research/continuation/explicit-secondary-data/**
role: implementer
tags:
- m1-continuation
- explicit-secondary-data
- source-bound-values
task_type: implementation
tracker_refs: []
---

## ⚡ Do This First: Load Agent Profile

Resolve implementer-ivan through the actual profile resolver and load implement action governance.
Read current AGENTS, spec/plan/continuation, docs/compatibility.md and docs/roadmap.md.
Use the canonical generated implementation prompt and assigned lane after normal root promotion/claim.
This TMP proposal has no claim, ID reservation, source approval or implementation authority.

## Objective and approved decision

Deliver ONE cohesive production DATA component and its genuinely new maintainer qualification workflow.
The product guarantee is immutable source-bound access to already-explicit field values under a closed whole-Secondary predicate.
The maintainer workflow is the real non-test consumer of that guarantee, not an end-user Merge command.
It must call the actual new API before reporting qualified values; an unused package or observer clone fails this WP.

Design authority is the complete inert packet under provenance/history/draft47/history/design with root seal28d089588575427386d7512c3f61f8cb39aa9bd3e144255d3b75609e2b9629ff.
Its decision SHA is32a6c2ca0355877f9df6b82ac9859ad597ca071a3f0c425211aac2cd2f7bf5e1.
Independent design review is the complete provenance/history/draft47/history/review packet, root4327e81d4925b017debd1bd5a7ce7bbfbec36aafa6b8585c1bf368ea9456d2c1/report0c85cd109de57af4c7009b52c56508b80a11cb8dae77619331ba76038f6705b1.
That verdict is READY_FOR_TASK_AUTHORING only, not source/code/runtime acceptance.
The seven-file merge assessment is retained exactly once under provenance/history/draft47/history/assessment, seal6e301ddc0ec0de3fa7da2c21c36845e88916961af46d6f3467aa18590026b5f0.
The source map supplies canonical destinations and exact byte/Git identities; historical seals retain original names and paths as inert history.
Never execute a provenance .txt/script or import it as product authority.

Direct semantic prerequisites are WP50 and WP53, not P64, E, G or H.
Approved50 source376a37a6afd0d9f11594cadfefe0d557b874a56c/implementationd396bbe1f9823c139797d4f94687375b259212c5 remains byte-exact.
Approved53 frozenf70310abb1127a645bf14e984cfcb6da64082713/fixeae7f09f214e5b719d3144aa12adef6b7fec9664 remains byte-exact.
Inherited WP09/02/13/14/21 authority stays context-specific; it supplies no merge evaluator/writer permission.
Use the pinned existing module; no new dependency/module/toolchain upgrade is included.

## Branch strategy and source boundary

Planning base and mission placement remain feat/wp51-parity; final mission GitHub integration is a separate root operation.
Execution is allocated by the actual finalized lanes.json, not a branch guessed from this title.
Pure draft topology adds an honest25th lane, lane-x, preserving every old24 lane ID and assignment.
This is expected topology, not authorization to create a worktree, alter a lane or force a24-lane result.
The old unreserved E-controller draft's WP67 label remains history; its possible logical successor is WP68/T202–204 after approved P64 binding.
No WP68 prompt, dependency or scope is added here.

Own only the THREE genuinely new scopes declared above; do not amend old53/native50 sources or assertions.
New production files are internal/merge/explicit/data.go and data_test.go, with supporting files confined to that sibling scope.
The actual Go qualification consumer is internal/merge/explicit/evidence/qualify/main.go with public-boundary tests there.
The actual launcher is scripts/reference/explicit_secondary_data.py.
New workflow documentation/authority/qualification reports/test tools/raw receipts live under docs/research/continuation/explicit-secondary-data/.
Default Go discovery, including the actual consumer, must be reported truthfully.
Do not use a hidden overlay, alternate decoder, old observer fallback or false existing-source create_intent.
No source under document/editor/tui/cmd/storage/layout/resources/macro/native or old53 is owned.

## T199 — Production immutable explicit-field DATA proof

Implement the reviewed sibling internal/merge/explicit using only standard library and approved native.
The approved package graph is explicit→native→wp51; no reverse dependency or E/G/H/P import.
Use actual native public Parse/View/Inspect/Bytes/source/span ownership; do not duplicate framing, operands or native IR.
Capture the WHOLE caller View value once, then use only that private captured value for Inspect/Bytes.
Authenticate its actual Secondary role and expected opaque Source.Equal before issuing a proof.
Independently Parsed equal bytes are a different Source; digest/path equality is not authority.
Caller unsynchronized wrapper mutation during capture remains outside the Go contract; accepted immutable reads must be race-safe.

Implement the approved boundary, with private immutable proof state and by-value Data/Value handles:
- Admit(view *native.View, expected native.Source) (Data,error).
- Data.Source(), Data.RecordCount(), Data.Field(recordOrdinal,fieldOrdinal) (Value,error), using one-based explicit ordinals.
- Value.Valid(), Value.Bytes() ([]byte,error), Value.ExplicitlyEmpty() (bool,error).
- Defensive copied provenance using existing native.Source/Span/Record/Field values; retain counts/tail/EF/HR/EOR/opaque owners/findings and DATA-only scope.
No mutable Inspection/Record/Field/JSON/table input or public authority setter may instantiate Data/Value.
Missing/out-of-range lookup returns typed ExplicitFieldMissing AND invalid Value, never valid empty.
Nil byte slices alone cannot indicate presence; an explicit empty has zero Content with its OWN EF.
Data.RecordCount counts delimited records, not the meaning of StoredCount.
Zero/nil/invalid/foreign/role mismatches refuse atomically and never return partial accepted data.
Do not create Program/effect/IO/target/write/export-generation capabilities.

Apply the entire reviewed predicate, not an allowed-finding-code shortcut:
1. Valid captured Secondary/source, positive inherited Parse limits, uncapped findings; no unsupported site/context.
2. Contiguous complete native-body coverage through actual EOF, with one or two explicitly delimited fields per record.
3. Exact printable ASCII bytes, either genuinely empty or not entirely spaces; no trim/coercion/Unicode substitution.
4. Each source Content ends at actual8-byte DE31/L4 EF followed by exactly one separately owned0A.
5. Empty unaddressed tail stays zero-length and never becomes a field; nonempty tail refuses.
6. Exact10-byte DE34/L6 EOR; only literal observed pairs(raw2,oneEF)/(raw3,twoEF), never count arithmetic.
7. Exactly one contiguous32-byte D4/00 owner from the SIX normative octet cohorts, then actual0C per record.
8. No byte/token gap, unowned trailing data, unsupported command/native character/attachment/extra separator.
Prove byte coverage and finding-site correspondence through real public spans; numerical Bounds alone is not a span capability.
Use actual reader body/token extents, never fixture offset324 or hardcoded original path/hash.
The two broader53 C8/page3–4 cohorts are REFUSED; preserve their distinct negative identity.
All opaque attachments, raw counts, old findings and whole bytes remain retained without declaring formatter data dead.
The SAME native Secondary must still have Supported=false and generic Admit refusal after DATA admission.
Result stays nonprogram and rejects DATA; Primary syntax admission does not qualify Secondary DATA.

Use all ten Secondary originals from five paired contexts207/208/209/216/217, with both run identities.
They witness24 records/36 fields/6 explicit empties;24 is a fixture-roster observation, not a runtime maximum/universal count.
209 Bob field2 is explicitly empty;217 field2 is empty/empty/YES/YES.
Change actual printable value bytes to Clara under a fresh real native Parse/source: DATA admission must still work.
Label that synthetic structural proof, not original merge behavior or a generated output.

## T200 — Actual new maintainer qualification workflow

Implement the NEW launcher and Go consumer; this must be a documented operational research workflow, not only tests.
Its public path is actual native.Parse→Image.View(Secondary)→explicit.Admit(expected actual Source)→Data.Field→Value getters→diagnostics.
Do not clone53.secondary_shape, scan record delimiters in Python or reconstruct trusted fields from expected JSON.
Frozen53 field byte/span observations are independent expected facts after the actual production API returns handles.
Neither original result strings nor fixture hash/path/name selects computed DATA.
Retain all30 full original input/result byte identities and associations without reproducing selected result projections as output.
The workflow reports qualified DATA, explicit-empty/missing typed results, copied provenance and unchanged generic blockers.
It performs no Primary run, PAGE effect, nesting, native result construction, app adoption, original guest call or file conversion.

Define a NEW source authority containing actual compiled Go/module/consumer/explicit/native/wp51 closure.
Record actual GoFiles/imports/local/standard packages, GOMOD/GOWORK/Go env/toolchain, argv/cwd/stdin/stdout/stderr/status, compiler/binary SHA and source Git/SHA/size.
Do not repeat old16-file/three-local-package composition claims after introducing new sources.
Check all actual compiled native/wp51 bytes against approved source; no P64/E/G/H source in closure.
Every old53 script/helper/authority/report/raw file and native50 production source remains byte-exact.
If reusing53's approved public bounded(argv,cwd,data,timeout,cap), import its exact pinned module via a declared immutable staged path.
Its SHA is216d59f01cb596b1e3fca2c0005d86dbad89854231ac8e9923276039e28d67b8 in both approved frozen/fix commits.
Do not invoke old Session/authority loader, alter globals/private functions, fork private supervisor code, or claim that old literal exists in primary.
Declare staged script as an inherited pinned input, not new owned source or materialized canonical old53 script.
If that public function cannot meet the contract, report the exact host prerequisite before inventing another supervisor.

Freeze a finite Linux execution/evidence policy before positives:
- Native input<=1MiB; inherited tokens<=65536/records<=4096/fields<=16384; closed<=2 explicit fields/record.
- Preappend traversal/proof bounds and one bounded full-source admission capture at most, never Export-per-field.
- Value and cumulative returned bytes bounded by admitted actual body; copied observations/fields bounded by inherited limits.
- Original workflow exactly30 declared images,<=30MiB cumulative native input, source roster59 immutable pins.
- Helper/report stdout<=64MiB and stderr<=1MiB while reading; each native call<=120s, synthetic case<=30s, complete qualification<=600s.
- Public launcher failure exits nonzero, bounded diagnostic; each report atomically replaced only after complete source/API checks.
- At most3 reports per invocation; evidence run<=120 files/64MiB, source archive hashes streamed<=32MiB each; ordinary build cache measured separately.
- Declare positive per-admission memory/work/append/copy bounds and a finite changed-boundary fuzz budget before running; measure them, retain raw limits/results, no DOS/SLO claim.
Preserve prior successful reports on source/role/helper/input/cap failures; never publish incomplete qualification as success.
Actual owned process-group cleanup must retain unreaped leader/PGID/SID ownership through TERM/KILL/drain/reap.
Lost ownership reports failure and must not signal a reused/unproved numeric PID; no timeout/pipe orphan leakage.

## T201 — Independent falsifiers, affected regression and honest handoff

Write public tests before implementation, distinguishing real reader failure from reader-valid DATA refusal.
Prove nil/zero/wrong role/source; foreign equal-byte Parse; public Image/View wrapper assignments before/after capture.
Prove private capture survives later caller wrapper replacement, returned copies/Inspection/Record/Field/JSON mutation and copied Data/Value aliases.
Prove missing versus valid explicit-empty versus all-space versus nonempty tail; invalid handles cannot masquerade as empty.
Prove concurrent immutable reads and exact original exports including every opaque attachment/count/finding.
Reject framed-valid raw1/4, raw2/twoEF, raw3/oneEF, third explicit field/count4, missing/extra EF/HR/space/control.
Reject format/control/multiline/all-space/tilde content, nonempty tail, EOR semantic extent mismatch and extra trailing byte/token ownership.
Reject unknown/nested/context commands, capped findings, and misplaced/absent/extra/altered D4/subfunction/group/page owners.
Exercise all SIX selected opaque cohorts; reject the two broader unobserved cohorts without a whole-image hash shortcut.
Add actual malformed/truncated native controls that fail unchanged native.Parse before explicit admission.
Workflow tests must falsify source substitution, old mutable-observer fallback, partial/invalid/truncated diagnostic output, helper exit, deadline, stdout/stderr cap and prior-report overwrite.
Use real bounded process/OS controls including leader-exits-descendant-keeps-pipe, TERM-ignoring descendant and ownership-loss safety.

Run actual affected Go gofmt/build/test/vet/race in the genuine finalized lane; include explicit consumer and unchanged approved native/wp51 packages.
Run configured scripts/review_checks.py checks with actual discovery/JUnit/exits; no skips called passes, no gate bypass/config weakening.
Run new launcher/workflow public tests, exact full original export regressions and all old53/native-source custody checks.
Do not repeat unchanged native reader600s fuzz merely to borrow evidence; exercise the new DATA/adversarial boundary with its own finite declared budget.
Compiled/restored semantic mutants must reach meaningful assertions: missing=empty, count-minus-one, source identity dropped, foreign-span-by-offset, returned alias, dropped coverage/metadata/findings, generic blocked flag cleared, fixture digest shortcut and workflow oldJSON replay.
Count only compile-valid faults reaching the relevant runtime test; type errors/early source-hash refusal are not semantic kills.
Retain raw red/green commands/exits, JUnit, source/binary/input/report seals, resource/OS measurements and restored exact source identities.
No fake comparable baseline or normalized raw failures; disclose inherited/current source composition differences.
Independent code review rejects a dead library, cloned observer, injected semantics, fake workflow or broadened permission.

## Definition of done and root handoff

### Public acceptance discriminators

Given209's real Secondary, qualification yields Alice/YES and Bob/present-empty from private handles.
Given207's one-field Secondary, Field(1,2) returns typed ExplicitFieldMissing and invalid Value.
Given an equal-byte independently Parsed Secondary, the old expected Source refuses it.
Given accepted Data then caller View replacement, already captured Data and Value still read their original source.
Given a defensive-copy mutation, later getters and admission/findings remain unchanged.
Given printable Clara input with fresh expected Source, structural DATA admission succeeds without original-output claims.
Given any missing/changed opaque attachment elsewhere in the body, the whole Data admission refuses.
Given a qualified Secondary, its same native generic Program admission still refuses and its old findings remain visible.
Given a launcher helper/source/cap failure, the prior report survives and the command exits nonzero.
Given successful qualification, no merge effects, native result or application target can be obtained from Data.

All T199–201 deliverables pass the actual public API/workflow contract with exact owned diff and provenance.
Whole native no-edit bytes, old53/native50 source, generic Secondary refusals and all current unrelated source contracts remain intact.
No formatter/evaluator/pagination/count-tail interpretation, native writer,0A/0C result construction, Merge UI, original resources/VM/grant or M2/PDF permission.
Full38 requirements/91groups/36lessons/nested M1/SC001–005 remain OPEN; no FR or parent acceptance follows from DATA qualification.
Before code: independent task review, ROOT review-bound canonical promotion/finalization, fresh CURRENT67 analysis and normal claim are mandatory.
Use normal root-coordinated marking/for_review after actual code checks; one independent reviewer decides the source verdict.
Never self-approve, advance global-next, alter lifecycle by hand, force/skip a gate or merge the mission here.
