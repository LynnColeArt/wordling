================================================================================
IMPLEMENT: WP100
================================================================================

Agent: codex
Mission: wp51-parity-01M64CVY
Mission Type: software-dev
Workspace: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-c
Workspace contract: lane lane-c shared by WP17, WP18, WP27, WP28, WP36, WP37, WP47, WP48, WP52, WP60, WP62, WP65, WP66, WP69, WP71, WP73, WP75, WP76, WP82, WP83, WP88, WP90, WP94, WP84, WP85, WP100, WP96, WP89

Mission-Type Governance Profile: software-dev
  template_set: software-dev-default
  selected_directives: (none)
  selected_tactics: (none)
  selected_paradigms: (none)
  selected_styleguides: (none)
  selected_toolguides: (none)
  selected_procedures: (none)
  selected_agent_profiles: (none)
  selected_mission_step_contracts: (none)

Governance:
  - Template set: software-dev-default
  - Paradigms: (none)
  - Tools: git, spec-kitty
Directive IDs:
  - DIRECTIVE_001
  - DIRECTIVE_010
  - DIRECTIVE_024
  - DIRECTIVE_025
  - DIRECTIVE_028
  - DIRECTIVE_029
  - DIRECTIVE_030
  - DIRECTIVE_033
  - DIRECTIVE_034
  - DIRECTIVE_036
  - DIRECTIVE_037
  - DIRECTIVE_040
  - DIRECTIVE_045
  - DIRECTIVE_046
  - DIRECTIVE_051
  - DISCIPLINED_REFACTORING
  - RECONCILE_CHANGE_SCOPE_TENSIONS
  - USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY
  - DIRECTIVE_003
  - DIRECTIVE_018
  - DIRECTIVE_031
  - DIRECTIVE_032
  - DIRECTIVE_035
  - DIRECTIVE_038
  - DIRECTIVE_039
  - DIRECTIVE_041
  - DIRECTIVE_042
  - DIRECTIVE_043
  - DIRECTIVE_044
  - DIRECTIVE_047
  - DIRECTIVE_048
  - DIRECTIVE_049
  - DIRECTIVE_050
  - USE_C4_MODEL_TECHNIQUES
  - WL-001
  - WL-002
  - WL-003
  - WL-004
  - WL-005
  - WL-006
  - WL-007
Tactic IDs:
  - acceptance-test-first
  - adversarial-qa-handoff
  - ammerse-impact-analysis
  - atdd-adversarial-acceptance
  - autonomous-operation-protocol
  - avoid-gold-plating
  - behavior-driven-development
  - black-box-integration-testing
  - boring-code-review
  - bug-fixing-checklist
  - change-apply-smallest-viable-diff
  - clean-linear-commit-history
  - code-review-incremental
  - connascence-analysis
  - dependency-hygiene
  - development-bdd
  - easy-to-change
  - eisenhower-prioritisation
  - five-paradigm-parallel-debugging
  - focused-function-complexity-check
  - forensic-repository-audit
  - formalized-constraint-testing
  - frozen-baseline-shrink-only-ratchet
  - function-over-form-testing
  - generated-code-stewardship
  - input-validation-fail-fast
  - no-parallel-duplicate-test-runs
  - paula-patterns-architecture-scout-review
  - premortem-risk-identification
  - problem-decomposition
  - quality-gate-verification
  - refactoring-change-function-declaration
  - refactoring-combine-functions-into-transform
  - refactoring-consolidate-conditional-expression
  - refactoring-extract-class-by-responsibility-split
  - refactoring-guard-clauses-before-polymorphism
  - refactoring-inline-temp
  - refactoring-introduce-null-object
  - refactoring-replace-magic-number-with-symbolic-constant
  - refactoring-replace-temp-with-query
  - refactoring-retry-pattern
  - review-intent-and-risk-first
  - reviewer-implementer-role-separation
  - safe-to-fail-experiment
  - secure-design-checklist
  - stakeholder-alignment
  - stopping-conditions
  - strategic-domain-classification
  - supply-chain-install-safety
  - tdd-red-green-refactor
  - test-boundaries-by-responsibility
  - test-pyramid-progression
  - testing-select-appropriate-level
  - usage-examples-sync
  - work-package-completion-validation
Styleguide IDs:
  - given-when-then-authoring
  - python-conventions
  - test-desiderata-and-boundaries
  - testing-principles
  - tiered-standards
Toolguide IDs:
  - efficient-local-tooling
  - gherkin
  - git-agent-commit-signing
  - sonar
Procedure IDs:
  - adversarial-squad-deployment
  - disciplined-defect-diagnosis
  - example-mapping-workshop
  - legacy-codebase-triage
  - mission-wrap-up-sequence
  - red-main-release-discipline
  - refactoring
  - situational-assessment
  - test-first-bug-fixing
Section Anchors:
  - Wordling 5.2 project charter
  - Purpose
  - Mission 1: WordPerfect 5.1 parity
  - Mission 2: Modern conveniences
  - Permanent file-format rules
  - Evidence and quality
  - Ownership, licensing, and delivery
  - Diagnostics: No activated directive set configured; using built-in catalog default (34 directives). | Merged 7 project-local directive(s) onto the catalog_fallback set: WL-001, WL-002, WL-003, WL-004, WL-005, WL-006, WL-007. | Template set not selected in charter; fallback 'software-dev-default' applied.
  - Project root: /home/lynn/projects/wordling/.kittify/doctrine

Required Governance Reading:
  - docs/compatibility.md
  - docs/roadmap.md

Action-Critical Charter Sections (implement):

### Terminology Canon
  Run: spec-kitty charter context --include section:terminology-canon
  When you rename or introduce a term in the diff, run this command and apply the returned rule.

### Code Review Checklist
  Run: spec-kitty charter context --include section:code-review-checklist
  When you prepare a WP for review, run this command and apply the returned rule.

### Regression Vigilance
  Run: spec-kitty charter context --include section:regression-vigilance
  When you perform a terminology cutover, run this command and apply the returned rule.

Profile-Cited Directives (implementer-ivan):
  - DIRECTIVE_010: Specification Fidelity Requirement — Implementations must faithfully reflect the design specifications without unauthorized deviations
    Intent: Implemented behavior and produced artifacts must remain faithful to approved specifications, with any necessary deviations explicitly documented and reviewed before acceptance.
    Scope: Applies to planning outputs, work-package implementation, and review checks where spec drift can silently change product behavior.
    Procedures:
      - Trace each implementation change to explicit requirements or acceptance criteria.
      - Flag and document deviations before merge when the spec must evolve.
      - Validate that final behavior matches committed scope and constraints.
    Integrity rules:
      - Unrecorded scope drift is not permitted.
      - Requirement-to-implementation traceability must remain inspectable.
    Validation criteria:
      - Review notes identify how changed behavior maps to specification language.
      - Any deliberate spec deviation has linked rationale and approval context.
  - DIRECTIVE_043: Close Defect Classes by Construction — Repeating defect patterns must be resolved structurally — AST gates, type invariants, or shrink-only ratchets — rather than by adding process rules; Ivan applies this during implementation to ensure the fix closes the class permanently
    Run: spec-kitty charter context --include directive:DIRECTIVE_043
    When you are about to apply a code change, run this command and apply the returned rule.
  - DIRECTIVE_044: Canonical Sources and Unification — Always use canonical templates and CLI surfaces; never copy from prior kitty-specs/ missions; when a split-brain surface is found, consolidate to one canonical authority rather than adding parity to non-canonical copies
    Run: spec-kitty charter context --include directive:DIRECTIVE_044
    When you are about to apply a code change, run this command and apply the returned rule.
  - DIRECTIVE_045: PRs-Only and Read-Intent Before High-Risk Operations — All changes to origin/main go through pull requests; every high-risk git operation (merge, rebase, deletion) requires reading the mission spec before execution; never push directly without explicit operator instruction
    Run: spec-kitty charter context --include directive:DIRECTIVE_045
    When you are about to apply a code change, run this command and apply the returned rule.
  - DIRECTIVE_051: Supply-Chain Install Safety — Every dependency addition or upgrade requires registry authenticity, package freshness, deny-by-default lifecycle-script handling, and Node Active LTS disclosure before it is accepted — never a silently-applied default
    Run: spec-kitty charter context --include directive:DIRECTIVE_051
    When you are about to apply a code change, run this command and apply the returned rule.

Profile-Cited Tactics (implementer-ivan):
  - bug-fixing-checklist: Enforce test-first defect resolution — write a failing reproduction test before modifying production code. All specialist profiles (java-jenny, python-pedro, frontend-freddy, node-norris) inherit this discipline via union merge.

    Name: Test-First Bug Fixing Checklist
    Purpose: Resolve defects through a disciplined sequence that prevents speculative fixes, ensures the defect is reproducible as a test, and verifies no regressions are introduced. Applicable to any language or framework. Do not skip steps under time pressure — shortcuts in bug fixing cause regressions.
    Steps:
      - Understand the defect before acting
        Read the bug report completely. Confirm what SHOULD happen and what ACTUALLY happens. If either is unclear, gather more information before proceeding. Do not open a code editor until you can state both in one sentence each.
      - Write a failing test that reproduces the defect
        Before modifying any production code, write an automated test that fails because of the defect. The test documents the expected behavior and proves you can reproduce the problem deterministically. If you cannot write such a test, the defect is not yet understood well enough to fix. No exceptions: this step is mandatory even under time pressure.
      - Confirm the test fails for the right reason
        Run only the new test. Verify it fails with the error that reflects the defect — not a test setup error or a different assertion. A test that fails for the wrong reason will pass after a wrong fix.
      - Implement the minimal fix
        Make the smallest change that causes the failing test to pass. Avoid refactoring, adding features, or "improving" adjacent code during a bug fix unless the bug cannot be fixed without it. Document the root cause in a comment if it would not be obvious to a future reader.
      - Verify the full test suite
        Run the complete test suite. Any newly failing test indicates a regression introduced by the fix. Fix regressions before marking the defect as resolved — a fix that breaks something else is not a fix.
      - Document the fix
        In the commit message or PR description: state the root cause, the fix applied, and any edge cases the new test does not yet cover. Link to the bug report or ticket.
  - dependency-hygiene: Pin and audit dependencies, restrict resolution to approved registries, and regenerate the SBOM after any change; for JavaScript/TypeScript work this now also covers registry authenticity, package freshness, deny-by-default lifecycle-script handling, lockfile-driven installs, and Node runtime baseline checks per the supply-chain-install-safety directive/tactic.

    Run: spec-kitty charter context --include tactic:dependency-hygiene
    When you are about to apply a code change, run this command and apply the returned rule.

Profile-Resolved Procedures (implementer-ivan):
  - adversarial-squad-deployment
    Run: spec-kitty charter context --include procedure:adversarial-squad-deployment
    When you are about to run this procedure, run this command and apply the returned rule.
  - bdd-scenario-lifecycle
    Run: spec-kitty charter context --include procedure:bdd-scenario-lifecycle
    When you are about to run this procedure, run this command and apply the returned rule.
  - event-storming-discovery
    Run: spec-kitty charter context --include procedure:event-storming-discovery
    When you are about to run this procedure, run this command and apply the returned rule.
  - example-mapping-workshop
    Name: Example Mapping Workshop
    Purpose: Turn a behavior request into concrete rules, examples, and open questions that stakeholders and implementers can share as a canonical specification set.
    Steps:
      - Frame the behavior slice
        State the user goal, the system boundary under discussion, and what would count as success or rejection for this slice of behavior.
      - Collect concrete examples and counterexamples
        Gather representative happy-path, edge-case, and failure examples using domain language. Prefer real business situations over invented technical cases. Phrase each example in a Given / When / Then shape so the precondition, trigger, and observable outcome are explicit and reusable when the example is later promoted into an acceptance check.
      - Separate rules, examples, and questions
        Sort the conversation into stable rules, illustrative examples, and open questions that block shared understanding. Remove implementation detail from the examples.
      - Choose canonical examples
        Select the smallest example set that still exposes the important rules, boundaries, and exceptions. Mark which examples should become executable acceptance checks first.
      - Confirm the source-of-truth set
        Review the selected examples and rules with the stakeholder or human-in-charge. Resolve wording issues and confirm the examples match the intended business behavior.
      - Publish traceable outputs
        Record the approved examples, their linked requirement or task IDs, and the chosen verification approach so later implementation and review work can follow the chain.
  - legacy-codebase-triage
    Run: spec-kitty charter context --include procedure:legacy-codebase-triage
    When you are about to run this procedure, run this command and apply the returned rule.
  - mission-tracer-files
    Name: Mission Tracer Files
    Purpose: Give every mission a lightweight running log of tooling friction, approach evolution, and design rationale through three sparse tracer files. The files are seeded at mission start, appended to during implementation, and assessed at mission close. Captured friction and rationale feed the next mission's planning and make recurring tool and process gaps visible instead of repeatedly re-discovered.
    Steps:
      - Seed — create the three tracer files at mission start
        Create the directory traces/ under the mission's kitty-specs/ directory. Copy the three doctrine templates (tooling-friction.md, approach.md, design-decisions.md from src/doctrine/templates/mission-tracer-files/) into it. Fill in the initial context for each file: what tooling the mission touches, what approach is being tried (as stated in the spec or plan), and what design decisions have already been made in the spec or plan. The initial entries should take under five minutes per file.
      - Append — add dated entries during implementation
        At each significant decision point, when an unexpected blocker is encountered, or when tooling friction slows progress, append a brief dated entry (1-3 sentences) to the relevant tracer file. Tooling friction goes in tooling-friction.md; approach changes go in approach.md; design choices and their rationale go in design-decisions.md. Entries should be written at the moment they occur, not reconstructed at the end.
      - Assess — review and act at mission close
        Before marking the mission as done (or as part of the accept step and the mission wrap-up sequence's hand-off), review all three tracer files. Summarise the most significant insights in the mission retrospective. File any unresolved tooling-friction items in the tracker so they feed the tooling-gap backlog. Confirm the tracer files are committed to the mission branch before closing — note that the wrap-up sequence compacts the branch, so the tracer files must be part of the retained, logically-sliced history.
  - post-merge-arch-gate-adjudication
    Run: spec-kitty charter context --include procedure:post-merge-arch-gate-adjudication
    When you are about to run this procedure, run this command and apply the returned rule.
  - red-main-release-discipline
    Run: spec-kitty charter context --include procedure:red-main-release-discipline
    When you are about to run this procedure, run this command and apply the returned rule.
  - situational-assessment
    Run: spec-kitty charter context --include procedure:situational-assessment
    When you are about to run this procedure, run this command and apply the returned rule.

Profile-Suggested Paradigms (implementer-ivan):
  Run: spec-kitty charter context --include section:profile-citations
  When you need to consult the profile-cited directives and tactics, run this command and apply the returned rule.

# Governance payload: 1 sections substituted with fetch commands (budget=40000).

==============================================================================
  CRITICAL: WORK PACKAGE ISOLATION RULES
==============================================================================
  YOU ARE IMPLEMENTING: WP100

  DO:
    - Only modify status of WP100
    - Ignore git commits and status changes from other agents

  DO NOT:
    - Change status of any WP other than WP100
    - React to or investigate other WPs' status changes
==============================================================================

WORKING DIRECTORY:
  cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-c

==============================================================================
  WORK PACKAGE PROMPT BEGINS
==============================================================================

---
work_package_id: WP100
title: Admit authenticated nested macro reads on current New buffers
dependencies:
- WP65
- WP66
- WP82
- WP69
- WP71
- WP73
- WP76
- WP84
- WP85
requirement_refs:
- FR-002
- FR-004
- FR-005
- FR-006
- FR-012
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T326
- T327
- T328
phase: New-buffer nested source composition; original New-buffer qualification remains WP102
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/macro_execution.go
create_intent:
- internal/editor/new_macro_nested_test.go
- internal/editor/new_macro_nested_internal_test.go
- internal/tui/new_macro_nested_test.go
- internal/editor/evidence/new-macro-nesting/
execution_mode: code_change
owned_files:
- internal/editor/macro_execution.go
- internal/editor/new_macro_test.go
- internal/tui/new_macro_test.go
- internal/editor/new_macro_nested_test.go
- internal/editor/new_macro_nested_internal_test.go
- internal/tui/new_macro_nested_test.go
- internal/editor/evidence/new-macro-nesting/**
role: implementer
tags:
- m1-continuation
- draft-unreserved
- new-buffer-nesting
task_type: implementation
tracker_refs: []
---

# WP100 — authenticated nested source composition on a New buffer

PROPOSAL ONLY. Tentative IDs checked against f1ca9686febe3868fc5c344ba0f7f9d24ba201b9: existing WP01–99 and T001–325 stay unchanged. Root must independently review/finalize this append and issue the normal implement prompt before code work. No old approval is overwritten or interpreted as general New macro parity. Resolve implementer-ivan and current implementation governance. Read the mission spec, compatibility contract, continuation, this proposal's rationale and exact issued claim.

The actual product gap is the `r.target != nil` refusal in `macroExecutionState.Resolve`. Loaded execution already uses the native VM, rooted ReadMacro, private acquisition proofs, serialized Resume and authentic missing-file CommandError handling. New admission already captures private Birth/genesis/buffer/screen/transition authority. Compose those existing seams for current New targets; do not create a second VM, filesystem reader, mutable Session surrogate or direct native writer. This deliberately supersedes only the old root-source-only New limitation. Other scope protections remain unless separately reviewed and amended.

## T326 — demonstrate the gap through real New Session/Runtime paths

Add four failing, source-hash-bound tests using the actual original-cases.json WPM exports for CMD51-210/212/213/230. Reach a genuinely initialized NewUnpublished buffer via normal constructors and public Macro prompt/read/Complete/StartMacro. Do not retrieve EMPTY.WP, parse an empty file, inject a loaded source or delete a loaded document to simulate New. Use actual ExecuteMacroRead for every root/child/missing result. Show the existing New-only resolver refusal causes the intended failures. Keep loaded paths as regression controls.

Initial positive scope is pristine New Doc1, Repeat1, plus the ordinary edited New workspace path already admitted by CanRunWorkspaceMacro (a nonempty unsaved ASCII receiver at its real caret, Repeat1, no selection/Reveal/typeover). Existing source restrictions on otherwise unsupported New contexts, Repeat3, arbitrary nested grammar and workspace UI commands are not silently broadened. Those remain explicit M1 follow-ups.

## T327 — reuse authenticated child acquisition and the same serialized owner

Permit nested resolution for a still-current New macro target, preserving the same r.valid/current/expected-transition checks before/after every step and Resume. Root-only target.unedited checks must continue to guard root acquisition; a legitimate root/child edit must not be mistaken for a stale root acquisition. Bind each child request/result to its accepted operation/revision/run/request/parent, rooted directory/name, actual buffer and screen, source identity and current execution owner. Reuse `newMacroReadProof`, `ExecuteMacroRead`, `acceptedMacroResult` and actual VM Resume. Only a genuine rooted missing observation becomes CommandError; fabricated missing wrappers, permission/host I/O errors and wrong-source results must not acquire original ON ERROR semantics by convenience.

Preserve all already-applied native text/dirty/history on terminal errors or host stop, release one owner once, and preserve NewUnpublished/no-source/no-name/no-false-save state until actual first publication. Child-local handler, unhandled child propagation, parent handler resumption and nested file-level BREAK use the existing VM, not case-number/source-name switches. Production source edits are limited to macro_execution.go. The two named existing test files may receive only the contract updates described in T328. If an actual defect demands changing new_macro.go, macro_load.go, macro_session.go, Runtime or native/storage APIs, report the exact failing case and obtain a reviewed source amendment from the orchestrator; do not weaken a guard or expand ownership implicitly.

## T328 — public integration, adversarial provenance and first-save checks

Use both captured repetitions' source inputs where available and slice quotas 1 and16. For pristine New receivers, assert exact bodies HANDLED, PCHILDRPARENT, PCPARENT and PCCHILDBADRDONE. For edited New receivers, declare initial bytes and caret and assert the entire resulting receiver, preserving the initial text around inserted output; assert real caret, dirty/native revision and unchanged Birth/genesis, New phase/source/name, source WPM bytes, execution completion, parent/child receipt provenance and no duplicate application. Cover child request/source/name/root/parent/run/screen/revision/operation tampering; swapped result from another driver or buffer; stale pre-edit Session/fork replay; duplicate/out-of-order Resume; pending child cancellation/host stop; host error versus real not-found; and unsupported names refusing without mutation. Preserve existing loaded, new root, ownership/fork/ready/first-publication regression suites.

Replace the obsolete unconditional New-NEST refusal assertions in TestNewMacroNestIsHostFailureBeforeChildIOAndPartialEffectsRemain (internal/editor/new_macro_test.go) and TestNewMacroNestPartialHostFailureAndStaticUnknown (internal/tui/new_macro_test.go) with authenticated child-read/resume/result behavior. Preserve their setup, actual prior effects, dirty/native state, source/name identity, completion/receipt accounting and duplicate rejection. Preserve the UNKNOWN static-preflight zero-effect refusal unchanged. Retain actual host-error/cancel/partial-effect negative coverage through a real rooted host I/O error or cancellation; a valid child call must not be used as a fabricated host error. No deletion, skip/xfail, fixture-name special case or weakening of unrelated tests.

Reach the four workflows through public Runtime Open/Model.Update/Cmd using the actual rooted temporary files. Save through normal F10/ExecuteSave, reopen through normal storage/editor and prove exact native body, unchanged source WPMs and truthful save receipt. Include an existing-other-screen sentinel on the already admitted workspace path where constructible; otherwise retain the existing other-screen refusal and report that positive variant as uncovered. Do not fake Doc2 coverage. Original WP reopen/edit/print belongs WP102.

Run focused editor/TUI tests, focused race tests covering asynchronous ownership, full `go test ./...`, `go vet ./...`, `go build ./cmd/wordling`, gofmt and git diff --check. Freeze candidate/source hashes and independent review evidence. No mutation-surrogate test is required where the existing real negative cases already prove the seam; any selective mutation probe must demonstrate a meaningful provenance guard.

## Independent acceptance

- All four New product workflows pass through authentic I/O and the real reducer/Runtime, and loaded equivalents retain exact prior outcomes.
- The first source-only refusal is resolved without relaxing root freshness, constructor identity, pending result authentication, history or first-save guards.
- Negative results preserve actual state and never synthesize success or ON ERROR for unauthenticated I/O.
- Tests/build/vet/race/format results and exact commit are recorded; independent reviewer can reproduce without a VM.
- CMD51-210/212/213/230 remain **partial** in the canonical command audit until WP102 has actual fresh unsaved-New original comparisons. This WP may be approved as bounded product delivery while full M1 and original New-context qualification remain open.

No VM/original image access, archived source edits, canonical audit/matrix promotion or changes outside owned_files are permitted by this WP. Evidence namespace is new. Existing source fixtures are read-only provenance, not new permission to distribute private media.


==============================================================================
  WORK PACKAGE PROMPT ENDS
==============================================================================

WHEN DONE:
  spec-kitty agent tasks mark-status T326 T327 T328 --status done --mission wp51-parity-01M64CVY
  spec-kitty agent tasks move-task WP100 --to for_review --mission wp51-parity-01M64CVY --note "Ready for review"