---
proposal_key: per-record-field-body
status: NUMBER_NEUTRAL_PROPOSAL_FOR_DIFFERENT_INDEPENDENT_TASK_REVIEW
proposed_title: Bounded compiled FIELD1 and IFBLANK2 per-record body evaluation
dependencies: [WP50, WP53, WP67]
requirement_refs: [FR-003, FR-012, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-004, C-005, C-006]
proposed_execution_mode: code_change
proposed_authoritative_surface: internal/merge/body/
proposed_routing_ownership: [internal/merge/body/**]
proposed_create_intent: [internal/merge/body/]
---

Audience: the eventual implementer and independent TASK/CODE reviewers. This is TMP-only, number-neutral proposed work, not a reserved WP/subtask, architecture approval, canonical task or implementation permission. ROOT requested this boundary from independently reviewed research; another reviewer must assess this proposal before any promotion. Do not run specify/finalize/claim/implement/status commands for it now.

## Purpose and source authority

Deliver a real compiled per-record body evaluator for the two smallest original-backed forms below, plus a genuine non-test compiled maintainer consumer. Compute body bytes from actual immutable native.Program and explicit.Data. This advances a narrow part of merge semantics without copy-boundary pagination or native output materialization. No ordinary end-user Merge command, editor/reducer/storage/TUI integration, replacement file format, writer, complete merge, layout or pagination is delivered.

Read source-pins.json, the complete assessment.md and its DIFFERENT independent research review, project governance, compatibility/roadmap, mission spec/plan and applicable contracts. Actual sources are approved50 376a37a6afd0d9f11594cadfefe0d557b874a56c, approved53 f70310abb1127a645bf14e984cfcb6da64082713, approved67 5f3035c3efce23c96449458d2c2c783517528cf4. This proposal independently verified all39 declared Git pins:9 source/provenance artifacts and30 native input/result files, retaining both run associations. Manual evidence remains the already sealed later June1992 edition with exact printed/PDF locators; no new original/reference/manual/private execution or acquisition is authorized.

At eventual claim verify actual approved dependency installation, complete compiler/package/GoFiles closure, public signatures, exact protected pathSET/Git/working hashes and genuinely new namespace absence. A source stamp/task routing glob is not installed-source proof. Missing source/API is a precise blocker; never copy/replace a dependency, use a fake Go module/overlay, relax an old test/closure check or borrow moving WP68/70 source. Preserve the old native and DATA consumers' discovered closures exactly. The new package depends outward on native/explicit; neither approved package may gain a backedge/import.

## A — compile a closed WHOLE-primary semantic proof

Implement the proposed new body API in api-contract.md. The existing APIs are ONLY the actual pinned Program.Valid/Source/Inspect/Bytes, Source.Equal, Span.Bounds, and explicit.Data.Valid/Source/RecordCount/Field with Value.Valid/Bytes/ExplicitlyEmpty/Provenance. New Compile/Evaluate/Result types are proposed new owned APIs, never described as existing.

Compile captures Program by value, requires the actual expected Primary Source owner, obtains one defensive Inspect and verifies Primary role, no capped/findings/records and all source-owned token/command/operand coverage. It admits ONLY these two complete structural forms, independent of filenames/hashes or literal contents:

- Form A: nonempty printable literal prefix, FIELD1, one terminal native HR0A, then true primary end.
- Form B: IFBLANK2, nonempty printable true literal, ELSE, nonempty printable false literal, ENDIF, nonempty printable separator literal, FIELD1, then true primary end.

Printable literal means exact ASCII20..7E excluding tilde. No arbitrary controls, nested/second IF, HR in a branch, optional/absent ELSE, extra FIELD, arbitrary operand, PAGE OFF/ON, BREAK, NEST, EF/EOR, unknown function/formatter/command, tabs, HP or unowned terminator. This is intentionally smaller than all syntax admitted by native.Program. It must refuse an unsupported whole-primary element even in a branch that would be untaken. Literals may differ freely within this structural predicate; no exactHello/EMPTY/FILLED, fixture name/value/hash allowlist or native frame replay.

The gate accounts for every native token exactly once: literal, admitted terminalHR, command Function, or exact command-owned Operand.Data and Terminator footprint. Numeric operand bytes and their external tilde remain reader character tokens and NEVER become body literals. Validate all spans by the captured Program.Bytes and bounds; zero/foreign owner/spans fail. Do not duplicate outer native framing or fabricate aggregate native.Span values. Command.Match is a COMMAND index: validate IF→ENDIF, ELSE→ENDIF, ENDIF→IF; locate/compile the sole ELSE explicitly, never treat Match as a token index. No public Compile(Inspection), mutable instruction slice, callback, hand-made proof or JSON execution authority.

Build a small immutable compiled representation only AFTER whole-primary validation; no interpretation by replaying expected JSON. Zero/invalid/failed Compile returns no valid plan. Defensive copies and caller wrapper/inspection mutation must not retarget the accepted plan. No native ownership or reader admission is changed.

## B — evaluate one actual explicit record atomically

Evaluate a captured plan with actual by-value explicit.Data, expected Secondary Source owner and one-based record ordinal. Check exact source ownership, valid ordinal and every required actual Data.Field before returning any result. FIELD1 appends only Value.Bytes content. IFBLANK2 tests Value.ExplicitlyEmpty: valid explicitly empty selects true, valid nonempty selects false. Missing/outside-explicit field remains the existing typed ExplicitFieldMissing refusal, distinguishable with errors.As; never default it to empty or infer fields from StoredCount−1/tail. A correct FormA207 does not request field2; applying FormB to207 must refuse rather than emit EMPTY. Whitespace-only/named/arbitrary fields remain outside approved Data/candidate semantics.

Use existing source-owned Value.Provenance and Content.Bounds BEFORE a Value.Bytes copy to preflight its length and operation budget. Preserve content/EF/separator/EOR/record/interstitial ownership as diagnostic provenance; EF/separatorHR/EOR/D4/HP are NOT field bytes. FormA terminalHR comes from PRIMARY, not the Secondary separator. Compiler operands/terminators do not emit bytes. No D4 interpretation, metadata stripping from originals or HP insertion. In209 Result originals retain automatic D4+HP between copies even though Primary has no PAGE; keep that evidence unresolved, never call concatenated bodies full merge equivalence.

Assemble output/result privately after checked size/work reservation, exposing a result only after full success. Any source/field/limit/refusal produces invalid zero result and no caller-visible partial body/provenance. Native inputs, original exports, Program/Data owners and prior successful results remain unchanged. Result.Bytes and provenance return defensive copies; zero result is invalid, not a successful empty merge. No editor mutation, filesystem/network/process activity or native document serializer in evaluator code.

## C — actual compiled consumer and intrinsic acceptance

Create a real non-test main at evidence/evaluate/main.go that imports the NEW evaluator. Its actual path is raw Primary bytes→native.Parse/View(Primary)/Admit→Compile; raw Secondary bytes→native.Parse/View(Secondary)→explicit.Admit→Evaluate each explicit record→computed body/provenance diagnostics. Main is an offline maintainer component consumer, never cmd/wordling or an end-user Merge interface. No expected body or original result file is accepted as an execution input.

Use a closed bounded stdin request containing exactly primary/secondary byte payloads, no caller instructions/Inspection/Program/Result/callback/proof/budget override. Read cap before append/decode, reject trailing/unknown/duplicate keys, bound each decoded source before native.Parse. Retain parsed source objects for owner checks. Stage the complete finite diagnostic response before stdout; any semantic/size/refusal yields no successful body rows or partial success report. stdout write failure exits failure and records actual uncertainty rather than claiming OS-level rollback. No output/native file is created. At least one test invokes the freshly built binary from unrelated cwd with real native inputs; renderer-only, go-run scratch shim or projection replay is not sufficient.

Both paired actual207 and209 sources (four run associations, two records each) MUST traverse this compiled path. Independently expected per-record body observations are207 `Hello Alice\n` and `Hello Bob\n`;209 `FILLED Alice` and `EMPTY Bob`. Derive their evidence linkage from the pinned actual original body/projection spans without feeding the expected result to the consumer. Preserve all paired Primary/Secondary/Result owner/hash/run identities and D4/HP boundary spans. These body expectations are a constrained decomposition of original observations, not a fresh DOS run or complete native result equality.

Actual paired208/216/217 primaries are syntactically admitted but semantically rejected WHOLE by Compile because of PAGE, while their Secondary explicit.Data remains valid. Include an authored structurally valid FormB with PAGE/unsupported content in the untaken branch; it still refuses. Other synthetic literal/value transformations must use real native framing/approved public parsing and remain labeled host falsifiers, not new observed DOS semantics. No public fixture or frozen test is modified.

Read finite-bounds.md and acceptance-matrix.md for exact prospective maxima, atomicity, owner/copy attacks, boundary cases and semantic mutants. Meaningful mutants must compile and hit intended new public/binary consumers; setup/compiler failures are not kills. Any genuine survivor blocks completion. No unchanged parser fuzz/reference/VM campaign.

## Strict execution ownership and frozen source

The routing namespace is truthful new internal/merge/body/**. It is NOT expanded amendment permission. Only these genuinely NEW paths and evidence namespace may be created; there is NO old-file amendment authority:

```json
{
  "schema": "wordling.merge-field-body-proposed-execution-allowlist/v1",
  "routing_ownership": ["internal/merge/body/**"],
  "amend_existing": [],
  "create_files": [
    "internal/merge/body/body.go",
    "internal/merge/body/compile.go",
    "internal/merge/body/evaluate.go",
    "internal/merge/body/body_test.go",
    "internal/merge/body/original_test.go",
    "internal/merge/body/limits_test.go",
    "internal/merge/body/README.md",
    "internal/merge/body/evidence/evaluate/main.go",
    "internal/merge/body/evidence/evaluate/main_test.go"
  ],
  "create_namespaces": ["internal/merge/body/evidence/verification/"],
  "protected": "Every inherited path, test, source, module, fixture and old raw evidence remains exact; no delete/rename, old source amendment or dependency overlay."
}
```

A planning-only namespace zero-match warning does not prove actual new source installation. Prove old approved50/53/67 sources and actual new-path absence from dependency source independently. Capture current complete protected pathSET/Git/working bytes and actual compiler/module closure before edits; compare after. Preserve all native/explicit public source, old errors/limits/findings/opaque cohorts, Go modules, old tests, qualifiers, document/editor/TUI/storage/macro/layout, cmd/wordling, scripts/reference, canonical contracts/inventory/status and other packages byte-exact. Extra needed ownership/API requires precise ROOT clarification before widening; never weaken closure safeguards.

Actual Go formatting, build/go test ./.../go vet ./..., focused new/native/explicit tests, meaningful race/read-only observation checks, finite allocation measurements and discovered configured checks are intrinsic acceptance. Individual command≤300s; predeclared focused mutant campaign≤180s; each actual CLI≤30s+2s owned cleanup, stdout/stderr≤2MiB before retained append. New evidence≤512files/8MiB including nested historical seals/raw failures. Preserve full actual raw failures, mutants, source/toolchain/argv/environment/binary/input/run hashes and recursive seals excluding only exact root. Record source lint separately from retained raw whitespace and honest inapplicable configured checks; no false all-green claim.

At eventual implementation freeze commit only allowed new paths, request ROOT's quietpoint before any task/lifecycle advance and obtain a DIFFERENT independent CODE review. This task proposal itself needs DIFFERENT independent TASK review first. No self-approval, IDs, promotion, status, push, accept/merge, new original/private assets/manual/program/resource/VM/grant/physical-lock actions. Full FR012/merge/native/output/pagination/ordinary UI/M1 remains open;37 obligations plusFC010gate/91groups36lessons/SC001–005 retained and PDF/M2 gated.
