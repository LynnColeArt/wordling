# Deferred canonical task definitions

These complete task drafts remain planned scope. They are not finalized or issued. Canonical authoring is staged at WP77–WP78 while the runtime lane identifier capacity defect is repaired and independently reviewed.


## Work Package WP79: Support original file lifecycle and backups in navigable directories (Priority: P1)

**Goal**: Run full declared Go checks and relevant original file outcome comparisons. Deliver internal/storage/evidence/everyday/REPORT.md with API/acceptance mapping. Different reviewer approves storage behavior and conservation before document/session consumers.

**Prompt**: `tasks/WP79-everyday-storage.md`

**Requirement Refs**: FR-006, FR-017, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-010, EE-011, EE-013

### Included Subtasks

- [ ] T239 Define reviewed workspace path mapping. Implement the WP78 DOS-directory/workspace-root contract with pinned child directories, parent boundary, filename/case/wildcard and symlink policy. Preserve local-flat existing callers. Separate display observations from capabilities used for read/save.
- [ ] T240 Provide stable browser and Look acquisitions. Support directory enumeration and metadata needed by the original short/long list and Look. Revalidate selected files at retrieval. Bound resources and retain directory/cursor context without treating stale enumeration as authority.
- [ ] T241 Implement replacement and original backups. Reuse existing candidate/publication transactions for edited replacement and Save As. Implement Original Document Backup enabled/disabled rotation, naming and byte preservation exactly from WP78. Preserve original document and backup outcomes across cancellation, overwrite refusal and failures.
- [ ] T242 Test races and failure outcomes. Exercise first/repeated writes, existing backup, path replacement, changed source/destination, symlink/permission failure, interrupted or short write, retry and close concurrency. No success report before actual durable outcome. Preserve existing native read and macro callers.
- [ ] T243 Review storage contract. Run full declared Go checks and relevant original file outcome comparisons. Deliver internal/storage/evidence/everyday/REPORT.md with API/acceptance mapping. Different reviewer approves storage behavior and conservation before document/session consumers.

### Dependencies

**Dependencies**: WP77, WP78, WP41

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP80: Extend lossless native editing and history for everyday documents (Priority: P1)

**Goal**: Original app retrieves, edits and saves generated mutation fixtures; Wordling reopens them. Run malformed/fuzz and conservation checks, full Go checks, and independent review. Deliver internal/document/evidence/everyday/REPORT.md with byte-range explanations and fixture provenance.

**Prompt**: `tasks/WP80-everyday-document.md`

**Requirement Refs**: FR-002, FR-003, FR-005, FR-008, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-004, EE-007, EE-008, EE-013

### Included Subtasks

- [ ] T244 Admit actual everyday native structures. Extend semantic decoding/admission for observed Underline, soft/hard returns, tabs and ordinary page boundaries while retaining wp51 framing authority. Use original native samples and exact supported structure checks. Preserve unknown spans and existing enum/public caller contracts.
- [ ] T245 Generalize safe edit lifecycle. Implement supported text insertion/deletion/typeover and return/tab operations on New, saved and Loaded revisions. Remove birthplace/first-save/two-pair restrictions only where semantic safety is established. Maintain immutable revision/cursor/history ownership and atomic failure.
- [ ] T246 Implement paired attributes and block/history. Support repeated Bold/Underline, original permitted overlap, active toggles, pair boundary deletion and block selection/deletion. Preserve original three-level Undelete behavior across supported edits and save/retrieve transitions. Test stale/foreign history refusal.
- [ ] T247 Provide native reflow adoption contract. Expose a narrow atomic native operation for the validated layout boundary changes, preserving hard versus soft return meaning and required structural updates. A renderer must never serialize display text. Test untouched byte identity and conservation around unrelated opaque data.
- [ ] T248 Verify native interoperability. Original app retrieves, edits and saves generated mutation fixtures; Wordling reopens them. Run malformed/fuzz and conservation checks, full Go checks, and independent review. Deliver internal/document/evidence/everyday/REPORT.md with byte-range explanations and fixture provenance.

### Dependencies

**Dependencies**: WP79, WP74

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP81: Implement matched original layout and physical cursor mappings (Priority: P1)

**Goal**: Run Go checks and resource-bound tests. Deliver internal/layout/README.md and evidence/everyday/REPORT.md with an API contract used by the next editor package. Different reviewer checks original fidelity and terminal independence.

**Prompt**: `tasks/WP81-everyday-layout.md`

**Requirement Refs**: FR-008, FR-009, NFR-005, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-005, EE-006, EE-008, EE-013

### Included Subtasks

- [ ] T249 Bind observed layout resources. Read the reviewed WP78 profile: Standard8.5x11, margins1inch, Standard Printer/Courier10cpi, Full justification, Auto height, spacing1, HyphenationNo and original tabs. General metric assumptions require original evidence. Avoid terminal-size inputs to physical layout.
- [ ] T250 Compute lines and pages. Implement paragraph wrapping/reflow, tabs, hard/soft boundaries, ordinary pages and physical positions over native document tokens. Support long words, blank paragraphs, attributes and at least three-page fixtures. Preserve no-edit bytes until an authorized semantic edit requires derived boundary changes.
- [ ] T251 Map cursor and code positions. Produce native-gap to line/page/physical position mappings and reverse navigation targets needed for Up/Down/Home/End/Page movement and Reveal. Distinguish zero-width codes from glyph cells and retain desired horizontal navigation position.
- [ ] T252 Compare original layout. Replay matched-resource fixtures and compare wrap words, page membership, printed Pg/Ln/Pos rounding, ruler/tab locations and layout changes after editing. Full justification default must not silently become Left. Declare any justified tolerance before running comparisons.
- [ ] T253 Review pure layout API. Run Go checks and resource-bound tests. Deliver internal/layout/README.md and evidence/everyday/REPORT.md with an API contract used by the next editor package. Different reviewer checks original fidelity and terminal independence.

### Dependencies

**Dependencies**: WP80

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP82: Complete everyday session lifecycle navigation and save continuations (Priority: P1)

**Goal**: Run public Session tests with genuine storage receipts and original native fixtures, then full Go checks. Deliver internal/editor/evidence/everyday/REPORT.md. Independent review covers repeated edits/saves, failed/canceled operations and downstream live integration contract.

**Prompt**: `tasks/WP82-everyday-session.md`

**Requirement Refs**: FR-004, FR-005, FR-006, FR-008, FR-009, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-004, EE-005, EE-006, EE-007, EE-008, EE-011, EE-012, EE-013

### Included Subtasks

- [ ] T254 Integrate supported document commands. Route real editor commands through approved document/layout APIs for New/saved/retrieved text. Adopt native reflow changes atomically and preserve cursor/history. Replace narrow pristine-startup guard assumptions with supported-semantic state checks.
- [ ] T255 Complete navigation and correction. Implement original arrows, Home/End sequences, Page movement, desired horizontal position, scrolling targets, Insert/typeover, block correction and Undelete. Handle boundaries through original observable behavior without suppressing real malformed-state failures.
- [ ] T256 Complete save and retrieval lifecycle. First save, edited replacement, Save As, overwrite No/cancel, backups and failures use approved storage outcomes. F7 Save Yes saves then continues the correct exit flow. Retrieval into blank and occupied supported buffers follows original insertion semantics; no implicit destructive clear.
- [ ] T257 Complete two-document and continued-New state. Both screens retain content/name/dirty/cursor/history. Implement original Doc2 closure versus ExitWP, cancel and continuation, and creation of a usable new document after clear/close. Preserve stale/detached I/O guards and existing macro command callers.
- [ ] T258 Review public session journeys. Run public Session tests with genuine storage receipts and original native fixtures, then full Go checks. Deliver internal/editor/evidence/everyday/REPORT.md. Independent review covers repeated edits/saves, failed/canceled operations and downstream live integration contract.

### Dependencies

**Dependencies**: WP81, WP75

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP83: Implement original search across text and native codes (Priority: P1)

**Goal**: Run full Go checks and original comparison cases. Deliver internal/editor/evidence/search/REPORT.md and normal session command contract for TUI routing. Obtain independent review.

**Prompt**: `tasks/WP83-everyday-search.md`

**Requirement Refs**: FR-005, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-009, EE-013

### Included Subtasks

- [ ] T259 Define original search state. Implement the WP78 forward/backward search prompts, input of text and supported native codes, defaults and termination commands. Preserve original callers and command enum identities.
- [ ] T260 Implement results and repetition. Find repeated text/code targets across wraps and paragraphs, repeat in both directions, and place the native cursor exactly as observed. Search remains independent of rendered ANSI strings.
- [ ] T261 Implement cancellation and failure. Not-found, empty/partial query, cancel and invocation from supported modes preserve document bytes and return to the original focus/position. Keep search state scoped to the correct document screen.
- [ ] T262 Prove semantic and native conservation. Exercise new, saved and retrieved fixtures in normal/Reveal state with hard/soft boundaries and attributes. Assert unchanged native bytes and exact result cursor, including repeated searches.
- [ ] T263 Review search delivery. Run full Go checks and original comparison cases. Deliver internal/editor/evidence/search/REPORT.md and normal session command contract for TUI routing. Obtain independent review.

### Dependencies

**Dependencies**: WP82

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP84: Integrate the original file browser document viewport and Reveal Codes (Priority: P1)

**Goal**: Build the normal cmd/wordling executable and prove end-user paths invoke the new logic. Run full Go checks and native conservation cases. Deliver internal/tui/evidence/everyday/REPORT.md and independent review; no helper-only feature completion.

**Prompt**: `tasks/WP84-everyday-editor-ui.md`

**Requirement Refs**: FR-004, FR-005, FR-006, FR-008, FR-009, FR-017, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-004, EE-005, EE-006, EE-008, EE-009, EE-010, EE-011, EE-014

### Included Subtasks

- [ ] T264 Route normal input into authoritative commands. Bind original keys/modifiers, navigation, corrections, search and storage replies through Model.Update and Session.Reduce. Keep modern aliases disabled in the accepted configuration. Resolve prototype shortcuts that bypass semantic/session ownership.
- [ ] T265 Render shared layout and multiline Reveal. Normal and code panes use one native revision/layout result, original physical status, multiline hard/soft codes, ruler/tab/margin information and caret emphasis. Maintain synchronized scroll and original restore behavior.
- [ ] T266 Implement complete browser journey. F5 directory prompt, current/parent/child navigation, short/long listing, scroll, filename location, Look Next/Prev/return and Retrieve operate through approved pinned storage/session APIs. Preserve list context and document bytes. Retain honest outside-milestone gaps.
- [ ] T267 Verify geometry and focus. Test 80x25 cell/attribute grids, actual terminal keys and mouse input, viewport resize without document reflow, modal input caret, code versus text position and filebrowser cancellation. Reuse host terminal restoration and async guards.
- [ ] T268 Review actual executable reachability. Build the normal cmd/wordling executable and prove end-user paths invoke the new logic. Run full Go checks and native conservation cases. Deliver internal/tui/evidence/everyday/REPORT.md and independent review; no helper-only feature completion.

### Dependencies

**Dependencies**: WP83, WP76

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP85: Complete original menus Help settings and prompt presentation (Priority: P1)

**Goal**: Compare observed grids/attributes/cursor and real terminal mouse/key journeys under both preference states. Run full Go checks and public CLI tests. Deliver internal/tui/evidence/everyday-menus/REPORT.md and independent review.

**Prompt**: `tasks/WP85-everyday-menus.md`

**Requirement Refs**: FR-004, FR-017, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-002, EE-003, EE-014

### Included Subtasks

- [ ] T269 Implement original menu model. Reproduce observed release ordering, groups, borders, shortcut columns, mnemonic colors, bracketed original availability and child-menu anchoring. Separate visibility, selected parent/child and keyboard focus. Implement F1 attribute+next-key behavior and original Esc/Space/F7 routes.
- [ ] T270 Unify command and pointer routing. Menus and function keys reach the same supported command path. Mouse selection, keyboard mnemonics, arrow navigation and function-key invocation during menus match original focus/cancel behavior. Missing implementations outside accepted paths cannot masquerade as original context-disabled entries.
- [ ] T271 Implement Help and menu preferences. F3 help/template and selected command descriptions work with correct return focus. Setup MenuBarRemainsVisible Yes/No uses the reviewed original-compatible persistence or explicit Linux adaptation. Original Ctrl families remain distinct from removed modern shortcuts.
- [ ] T272 Consolidate production presentation. Remove or redirect superseded prototype chrome/render/menu paths through one live composition. Keep authentic prompts at original positions, preserve document view under prompts, and protect async modal boundaries. Amend only tests whose old limitation is explicitly superseded.
- [ ] T273 Review screen and interaction fidelity. Compare observed grids/attributes/cursor and real terminal mouse/key journeys under both preference states. Run full Go checks and public CLI tests. Deliver internal/tui/evidence/everyday-menus/REPORT.md and independent review.

### Dependencies

**Dependencies**: WP84

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP87: Implement the resource-backed original proofreading engine contract (Priority: P1)

**Goal**: Run Go checks and focused resource/native tests. Deliver internal/proofreading/README.md and evidence/REPORT.md. Different reviewer approves real resource behavior and the API consumed by session proofreading.

**Prompt**: `tasks/WP87-proofreading-provider.md`

**Requirement Refs**: FR-014, FR-005, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-015, EE-013

### Included Subtasks

- [ ] T274 Bind original proofreading resources. Adopt the reviewed CtrlF2 workflow/resource contract. Record original dictionary/supplemental resource identities and allowed host resource sources, formats and redistribution rights. Resource absence is explicit; no bundled proprietary data or silent pass-through success.
- [ ] T275 Implement lexical and suggestion services. Provide deterministic token/word boundary, suspect-word and suggestion operations needed by the original workflow using actual admitted resources. Preserve original character identities and dictionary distinctions. Any resource/lexical difference remains a qualified limitation, not a hidden generic modern replacement.
- [ ] T276 Implement supplementary dictionary operations. Implement the observed add/persistent dictionary behavior and per-run ignore vocabulary with the original semantic distinction. Use original-compatible formats or a reviewed explicit platform adaptation with conservation tests.
- [ ] T277 Test original corpus and resource failures. Test suspect words, correct words, suggestions/order where required, repeated occurrences, added words, encoding/resource failures and bounded work. Record differences from original under matched resources and resolve cases claimed by the milestone.
- [ ] T278 Review provider contract. Run Go checks and focused resource/native tests. Deliver internal/proofreading/README.md and evidence/REPORT.md. Different reviewer approves real resource behavior and the API consumed by session proofreading.

### Dependencies

**Dependencies**: WP78, WP80

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP88: Implement continuous contextual proofreading in the editor (Priority: P1)

**Goal**: Run full Go checks and original workflow comparisons. Deliver internal/editor/evidence/proofreading/REPORT.md with exact continuation/state evidence. Independent review must examine a continuous journey, not just isolated provider calls.

**Prompt**: `tasks/WP88-proofreading-session.md`

**Requirement Refs**: FR-014, FR-005, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-015, EE-013

### Included Subtasks

- [ ] T279 Model the original proofreading journey. Implement CtrlF2 scopes and contextual questionable-word state from WP78. Track native positions, current suggestion, dictionary/ignore decisions and continuation independently for the correct document screen.
- [ ] T280 Apply corrections through real native editing. Suggestion replacement and typed correction use approved document/history/session operations, preserve attributes and unrelated bytes, and update layout/search/proofreading positions consistently. No rendering-side string replacement or alternate document model.
- [ ] T281 Implement skip add and continuity. Implement only observed original skip/ignore-all/add choices, next-word advance, cancellation, interruption/resume and restart semantics. Preserve reading place and document focus at each transition, including after save/retrieve and in repeated sessions.
- [ ] T282 Verify public proofreading scenarios. Exercise misspellings across paragraphs/wraps/codes, repeated suspect words, replacements of different lengths, add/ignore behavior, cancellation and resource failures. Assert original native effects and unchanged bytes for skip/cancel paths.
- [ ] T283 Review session correctness. Run full Go checks and original workflow comparisons. Deliver internal/editor/evidence/proofreading/REPORT.md with exact continuation/state evidence. Independent review must examine a continuous journey, not just isolated provider calls.

### Dependencies

**Dependencies**: WP83, WP87

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP89: Recreate the original contextual proofreading screen and controls (Priority: P1)

**Goal**: Independent reviewer runs the actual terminal workflow and checks resource provenance, truthful limitations and exact screen behavior. Deliver internal/tui/evidence/proofreading/REPORT.md, full Go checks and native-output comparison.

**Prompt**: `tasks/WP89-proofreading-ui.md`

**Requirement Refs**: FR-004, FR-005, FR-014, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-015, EE-014

### Included Subtasks

- [ ] T284 Render original proofreading context. Display questionable words in their document context, original suggestion list and original scope/action prompts, preserving layout and emphasis. Exact controls and labels come from WP78; do not introduce a generic modern spell modal.
- [ ] T285 Wire original proofreading interactions. Bind CtrlF2 and original menu routes, suggestion navigation/selection, correction, observed skip/ignore/add choices and cancellation through the approved editor state. Keep input focus and document cursor distinct where original requires it.
- [ ] T286 Preserve continuous reading and correction. Advance to the next questionable word with the same contextual continuity as original. Verify interruption/resume, restart, long/wrapped paragraphs and return to ordinary editing without losing place or leaking prompt input.
- [ ] T287 Exercise the golden proofreading journey. Run a real executable sequence with multiple suspect words, one accepted suggestion, one typed correction where observed, skip, persistent dictionary add, interruption, resume and final save/reopen. Compare original grids, cursor/focus and native effects.
- [ ] T288 Review proofreading product experience. Independent reviewer runs the actual terminal workflow and checks resource provenance, truthful limitations and exact screen behavior. Deliver internal/tui/evidence/proofreading/REPORT.md, full Go checks and native-output comparison.

### Dependencies

**Dependencies**: WP85, WP88

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.


## Work Package WP86: Independently qualify and deliver the complete everyday editing milestone (Priority: P1)

**Goal**: Run final formatting/build/test/vet checks and record the tested binary hash. Publish the exact candidate to preview atomically using authorized host delivery, without committing binaries. Deliver tests/everyday_qualification/REPORT.md with EE coverage, launch command and explicit remaining M1 gaps. Do not accept the entire mission or start M2.

**Prompt**: `tasks/WP86-everyday-qualification.md`

**Requirement Refs**: FR-004, FR-005, FR-006, FR-008, FR-009, FR-014, NFR-005, NFR-001, NFR-002, NFR-003, NFR-004, C-001, C-002, C-003, C-004, C-005, C-006

**Milestone Refs**: EE-001, EE-002, EE-003, EE-004, EE-005, EE-006, EE-007, EE-008, EE-009, EE-010, EE-011, EE-012, EE-013, EE-014, EE-015

### Included Subtasks

- [ ] T289 Bind final integrated candidate. Record all independently approved dependency commits and current canonical source, resource profile and actual build identity. Verify no source/lane drift and no unreviewed inherited delta. Build through normal cmd/wordling.
- [ ] T290 Run full original and product journeys. Execute EE-A01–A15 with real files and terminal input, including golden continuous editing and proofreading. Compare original character/attribute grids, focus/cursor, physical layout and native outcomes. Preserve failed runs and report exact unmet criteria.
- [ ] T291 Prove original interoperability and conservation. Original retrieves/edits/saves Wordling outputs, then Wordling reopens/continues. Check no-edit byte identity, unrelated preservation, repeat saves/backups and refusal/failure outcomes. Resource and terminal adaptations are declared.
- [ ] T292 Close integration findings independently. Different reviewer audits the complete product journey and all requirement mappings. Return product-code findings to the owning package, repair there under review, then rerun affected integration scenarios. This package does not gain broad product source ownership.
- [ ] T293 Deliver exact reviewed preview and milestone report. Run final formatting/build/test/vet checks and record the tested binary hash. Publish the exact candidate to preview atomically using authorized host delivery, without committing binaries. Deliver tests/everyday_qualification/REPORT.md with EE coverage, launch command and explicit remaining M1 gaps. Do not accept the entire mission or start M2.

### Dependencies

**Dependencies**: WP85, WP89

This is an everyday-editing milestone inside M1. Canonical ownership validation must preserve prior lane/lifecycle identities and approved histories. Full parity and M2 gates remain open.
