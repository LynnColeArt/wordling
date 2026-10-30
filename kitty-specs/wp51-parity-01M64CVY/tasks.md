# M1 work packages: initial delivery and research queue

Inputs: spec.md, plan.md, research.md, data-model.md, quickstart.md. All packages start planned; none is implemented or approved. This initial queue is **not the complete parity implementation**. WP04–WP11 propose follow-up slices inside their contract artifacts; WP12 must append implementation packages from those contracts to this queue and create new WP13–WP99 prompts before completion; full mission acceptance remains SC-001–005.

Critical path: WP01 → WP02 → WP03. Evidence-backed editor work follows WP04/WP06/WP11. Other contract research closes complete-scope gaps without blocking the bounded reader. Dependencies express prerequisite outputs; no agents are automatically spawned.

## Work Package WP01: Native framing contract and fixture corpus (Priority: P0)

**Goal**: A reviewer can derive every checked native offset and boundary from the contract, validate every fixture hash, and identify which variants must be refused. No reader code or general companion-file support is claimed.

**Prompt**: `tasks/WP01-native-contract.md`

**Requirement Refs**: FR-002, FR-003, NFR-001, NFR-003, C-002, C-004

### Included Subtasks

T001 Specify SDK51 prefix, linked index/packet and body framing fields with widths, endian rules, validation and release applicability; include exact source/page locators.
T002 Select a small provenance-approved original-produced corpus spanning plain text, paired attributes, prefix packets, macros/merges as distinct file types, and opaque/trailing data; record paths, hashes and supported/refused variants without copying proprietary resources.
T003 Declare parser input/allocation/traversal limits, typed failure categories, malformed cases, fuzz seed corpus and reproducible budget. Measure the selected corpus against those limits and record unresolved variants.

### Dependencies

**Depends on**: None

## Work Package WP02: Lossless native reader and no-edit export (Priority: P0)

**Goal**: Every accepted WP01 fixture exports byte-identically; malformed cases fail without panic or uncontrolled work; opaque bytes and caller buffer isolation survive. Reader acceptance does not establish edit interoperability.

**Prompt**: `tasks/WP02-native-reader.md`

**Requirement Refs**: FR-002, NFR-001, NFR-003, C-001, C-002

### Included Subtasks

T004 Implement immutable owned native images, checked framing and typed failures in internal/wp51 using only the approved WP01 contract. Preserve opaque spans and trailing bytes; reject unsupported structural variants explicitly.
T005 Expose no-edit byte export and span inspection without caller mutation of owned storage. Keep semantic mutation, UI, filesystem replacement and dependency changes outside this package.
T006 Add original-fixture byte/length/SHA comparisons, buffer-isolation tests and malformed/cyclic/oversized/truncated cases plus fuzzing under the WP01 budget; run formatting, build, test and vet.

### Dependencies

**Depends on**: WP01

## Work Package WP03: Failure-safe no-edit filesystem save (Priority: P0)

**Goal**: The documented local-filesystem cases preserve originals under injected failures and refuse overwrite without an explicit decision. No original backup, locking or Fast Save behavior is falsely advertised.

**Prompt**: `tasks/WP03-native-safe-save.md`

**Requirement Refs**: FR-006, NFR-001, NFR-002, C-002

### Included Subtasks

T007 Specify the bounded new-file and existing-file no-edit transaction API with explicit destination/source identity and overwrite decision; leave original prompt UI and unobserved backup/Fast Save behavior unsupported.
T008 Implement candidate creation/write/close and safe replacement only under that contract. Refuse stale source identity, unsafe paths and unsupported replacement cases before changing the destination; avoid claiming network/durability semantics not tested.
T009 Inject write/close/rename failures and concurrent-source changes. Assert original bytes remain intact on refusal/failure and exported bytes are exact on success; run formatting, build, test and vet.

### Dependencies

**Depends on**: WP02

## Work Package WP04: Observed editing command contracts (Priority: P1)

**Goal**: Each proposed implemented transition has a linked original observation and native expected effect; unknown combinations are explicit and do not become guessed editor behavior.

**Prompt**: `tasks/WP04-editing-contracts.md`

**Requirement Refs**: FR-004, FR-005, FR-008, NFR-004

### Included Subtasks

T010 Extract the existing cursor/code-boundary/typeover/blocked-pair deletion and three-level Undelete observations into a state-transition table with exact CMD51 IDs and fixture links.
T011 Write Given/When/Then contracts for document positions, paired-code repair and command-specific restoration; separate original observations from untested combinations.
T012 Define the smallest subsequent document/editor implementation packages and their native-write prerequisites; add original probes only for genuinely unanswered contract branches.

### Dependencies

**Depends on**: WP01

## Work Package WP05: Manual and workbook coverage concordance (Priority: P1)

**Goal**: Every contents-level manual/workbook entry has a disposition and owner-visible remaining step/subcommand gaps. This is an audited concordance, not a claim of exhaustive behavior verification.

**Prompt**: `tasks/WP05-coverage-concordance.md`

**Requirement Refs**: FR-001, NFR-004, C-003, C-005, C-006

### Included Subtasks

T013 Build a chapter/appendix/utility and 36-lesson concordance against existing inventory and scenario IDs, retaining exact edition and locator; mark indexed, studied, observed and uncovered separately.
T014 Identify version-sensitive entries between REF51 6/92, WB51 11/89, SDK51 12/93 and the selected executable. Assign each discrepancy a bounded probe or external-resource prerequisite.
T015 List unrepresented subcommands and lesson steps as actionable follow-up packages with coverage impact. Do not mark a lesson or chapter complete from a thematic mapping alone.

### Dependencies

**Depends on**: None

## Work Package WP06: File and Linux platform investigation (Priority: P1)

**Goal**: Each platform-sensitive behavior has an explicit mapping proposal, evidence status and next test; no hidden exclusions or fabricated historical-DOS result.

**Prompt**: `tasks/WP06-file-platform-contracts.md`

**Requirement Refs**: FR-006, FR-007, FR-017, C-006, NFR-002

### Included Subtasks

T016 Produce a matrix of original retrieval/save/list/backup/recovery/Fast Save/locking/conversion commands and required fixtures or reference prerequisites; include overwrite refusal and cancellation evidence already captured.
T017 Classify Linux path/key/shell/network mappings and owner decisions needed for actual scope changes. Prioritize one minimal no-edit retrieve/save workflow for UI integration; preserve unsupported functions visibly.
T018 Specify independent probe/implementation slices for each unresolved family with failure safety and original artifact-format acceptance.

### Dependencies

**Depends on**: WP05

## Work Package WP07: Layout and resource comparison profile (Priority: P1)

**Goal**: Another researcher can reproduce the declared comparison or identify the exact missing resource. No layout fidelity is claimed from terminal wrapping or unmatched printer metrics.

**Prompt**: `tasks/WP07-layout-resource-contract.md`

**Requirement Refs**: FR-009, FR-015, FR-016, NFR-005

### Included Subtasks

T019 Define acquisition/provenance and fingerprint requirements for historical DOS plus graphics-capable printer/font profiles; document current FreeDOS and Standard Printer limitations.
T020 Specify a small reference layout corpus covering returns/pages/margins/tabs/font metrics and original print-to-disk/preview, with units and comparison procedure. Set tolerances only with evidence before comparison.
T021 Separate blocked external resources from ready text-profile experiments and author follow-up layout/resource/print packages; retain remaining pagination and preview scope.

### Dependencies

**Depends on**: WP05

## Work Package WP08: Structured content and graphics contract map (Priority: P1)

**Goal**: The map identifies native structures, observable results and resource blockers without collapsing structured content into display-only approximations.

**Prompt**: `tasks/WP08-structured-graphics-contracts.md`

**Requirement Refs**: FR-010, FR-011

### Included Subtasks

T022 Decompose styles/outlines/tables/calculation/generated references/master documents into native structure, original command and output obligations.
T023 Do the same for boxes/graphics/rules/equations and original conversion utilities; identify resource-dependent cases and native format documentation boundaries.
T024 Choose one independently verifiable starter slice for each family and specify fixture/probe and implementation prerequisites; retain every deferred obligation with inventory IDs.

### Dependencies

**Depends on**: WP05

## Work Package WP09: Macro and merge execution contract matrix (Priority: P1)

**Goal**: Every rule has its context and evidence level. File-level BREAK and PAGE state are not generalized across macro/primary/secondary contexts without original evidence.

**Prompt**: `tasks/WP09-automation-contracts.md`

**Requirement Refs**: FR-003, FR-012

### Included Subtasks

T025 Consolidate observed strings/expressions/FOR EACH/NEXT/BREAK/loops/handlers into distinct macro and merge execution-context tables, preserving exact unexpected results.
T026 Record nested primary/secondary record/copy/page transitions and partial-output behavior using existing original run hashes and fixtures; identify unanswered branches without normalizing bytes.
T027 Define bounded decoder/interpreter implementation packages and additional original-only probes for missing branches, including explicit unsupported commands and error paths.

### Dependencies

**Depends on**: WP05

## Work Package WP10: Character language and data contract map (Priority: P1)

**Goal**: Each family has explicit native identity, resource and comparison requirements; no proprietary dictionary redistribution or unapproved substitute behavior.

**Prompt**: `tasks/WP10-language-data-contracts.md`

**Requirement Refs**: FR-013, FR-014, FC-006

### Included Subtasks

T028 Map original character identity/composition/display and spelling/dictionary/thesaurus resources to native obligations and redistribution constraints; do not substitute Unicode identity for native codes.
T029 Map sort/record selection/column math/spreadsheet import/links to observable commands, source formats and fixtures.
T030 Specify a first character-preservation and data-operation slice with source locators, original-app probes and follow-up packages; expose missing resources and variants.

### Dependencies

**Depends on**: WP05

## Work Package WP11: Classic session and terminal interaction contracts (Priority: P1)

**Goal**: A subsequent implementer can build the bounded session without guessing original prompts, while the rest of classic interaction remains visible in M1.

**Prompt**: `tasks/WP11-session-contracts.md`

**Requirement Refs**: FR-004, FR-005, C-001

### Included Subtasks

T031 Specify the first retrieve/Reveal Codes/cursor/save/cancel/exit session as original command/prompt states linked to original transcripts; include both display and input adaptation boundaries.
T032 Declare Linux terminal key ambiguities and supported terminal profile, with explicit fallback decisions that preserve original commands; do not invent menus from generic text editor conventions.
T033 Author bounded Bubble Tea/session implementation packages independent of document/layout semantics, with observable state tests and the necessary original command probes.

### Dependencies

**Depends on**: WP04, WP06

## Work Package WP12: Queue continuation and parity gap audit (Priority: P1)

**Goal**: There is an actionable expanded queue and an explicit gap ledger for every requirement. This package cannot complete by merely recommending future work; no parity acceptance while known obligations remain unimplemented/unverified.

**Prompt**: `tasks/WP12-continuation-audit.md`

**Requirement Refs**: FR-001, NFR-004, C-003, C-006

### Included Subtasks

T034 Reconcile every FR/NFR/FC and inventory obligation with completed evidence, queued implementation and still-blocked research; include measured Linux performance/size investigation packages.
T035 Append reviewable dependency-correct implementation packages from the approved contracts to kitty-specs/wp51-parity-01M64CVY/tasks.md with matching new WP13–WP99 prompts under kitty-specs/wp51-parity-01M64CVY/tasks/; preserve existing WP01–WP12 prompts and validate derived ownership, requirement mappings, dependencies and prompt completeness before completing this package.
T036 Record remaining reference/resource gaps and ensure runtime cannot interpret completion of the initial queue as full parity acceptance. Require the expanded queue and all M1 coverage checks before any accept/merge request.

### Dependencies

**Depends on**: WP04, WP05, WP06, WP07, WP08, WP09, WP10, WP11
