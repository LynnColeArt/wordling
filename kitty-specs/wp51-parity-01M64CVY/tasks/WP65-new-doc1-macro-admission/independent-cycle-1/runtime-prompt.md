---
work_package_id: WP65
created_at: '2026-11-01T09:24:39.266494Z'
base_ref: kitty/mission-wp51-parity-01M64CVY
invocation_id: b966855fe284422a80c2c84185a112d1
lane_branch: kitty/mission-wp51-parity-01M64CVY-lane-g
lane_worktree: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g
mission_branch: kitty/mission-wp51-parity-01M64CVY
mission_id: 01M64CVYYRTDKBCYZ56H6XNTEQ
mission_slug: wp51-parity-01M64CVY
prompt_path: /tmp/spec-kitty-review-prompts/wordling-addc41014af6/wp51-parity-01M64CVY/WP65/b966855fe284422a80c2c84185a112d1.md
repo_root: /home/lynn/projects/wordling
---

================================================================================
REVIEW: WP65
================================================================================

Source: /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP65-new-doc1-macro-admission.md

Workspace: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g
Workspace contract: lane lane-g shared by WP17, WP27, WP36, WP47, WP65

Resolved agent identity:
  tool       : codex
  model      : unknown-model
  profile_id : implementer-ivan
  role       : implementer

Governance:
  - Template set: software-dev-default
  - Paradigms: (none)
  - Tools: git, spec-kitty
Directive IDs:
  - DIRECTIVE_001
  - DIRECTIVE_003
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
  - DIRECTIVE_041
  - DIRECTIVE_043
  - DIRECTIVE_045
  - DIRECTIVE_046
  - DIRECTIVE_051
  - DISCIPLINED_REFACTORING
  - RECONCILE_CHANGE_SCOPE_TENSIONS
  - USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY
  - DIRECTIVE_018
  - DIRECTIVE_031
  - DIRECTIVE_032
  - DIRECTIVE_035
  - DIRECTIVE_038
  - DIRECTIVE_039
  - DIRECTIVE_042
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
  - architectural-gate-non-vacuity
  - atdd-adversarial-acceptance
  - autonomous-operation-protocol
  - avoid-gold-plating
  - black-box-integration-testing
  - boring-code-review
  - bug-fixing-checklist
  - change-apply-smallest-viable-diff
  - clean-linear-commit-history
  - code-review-incremental
  - connascence-analysis
  - decision-marker-capture
  - delete-the-assertion-not-the-test
  - dependency-hygiene
  - development-bdd
  - easy-to-change
  - eisenhower-prioritisation
  - five-paradigm-parallel-debugging
  - forensic-repository-audit
  - formalized-constraint-testing
  - frozen-baseline-shrink-only-ratchet
  - no-parallel-duplicate-test-runs
  - paula-patterns-architecture-scout-review
  - premortem-risk-identification
  - problem-decomposition
  - quality-gate-verification
  - refactoring-change-function-declaration
  - refactoring-combine-functions-into-transform
  - refactoring-consolidate-conditional-expression
  - refactoring-extract-class-by-responsibility-split
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
  - testing-select-appropriate-level
  - traceable-decisions
  - usage-examples-sync
  - work-package-completion-validation
Styleguide IDs:
  - given-when-then-authoring
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
  - development-assist-test-cleanup
  - disciplined-defect-diagnosis
  - example-mapping-workshop
  - legacy-codebase-triage
  - mission-tracer-files
  - mission-wrap-up-sequence
  - post-merge-arch-gate-adjudication
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

Action-Critical Charter Sections (review):

### Terminology Canon
  Run: spec-kitty charter context --include section:terminology-canon
  When you rename or introduce a term in the diff, run this command and apply the returned rule.

### Code Review Checklist
  Run: spec-kitty charter context --include section:code-review-checklist
  When you prepare a WP for review, run this command and apply the returned rule.

### Regression Vigilance
  Run: spec-kitty charter context --include section:regression-vigilance
  When you perform a terminology cutover, run this command and apply the returned rule.

⚠️  Dependency Alert: WP66 depend on WP65 (not yet done)
   If you request changes, notify those agents to rebase.

╔==============================================================================╗
║  🚨 CRITICAL: WORK PACKAGE ISOLATION RULES                              ║
╠==============================================================================╣
║  YOU ARE REVIEWING: WP65                                                     ║
║                                                                          ║
║  ✅ DO:                                                                  ║
║     • Only modify status of WP65                                            ║
║     • Ignore git commits and status changes from other agents           ║
║                                                                          ║
║  ❌ DO NOT:                                                              ║
║     • Change status of any WP other than WP65                               ║
║     • React to or investigate other WPs' status changes                 ║
║     • Review or approve any WP other than WP65                             ║
║                                                                          ║
║  WHY: Multiple agents work in parallel. Each owns exactly ONE WP.       ║
║       Git commits from other WPs are other agents - ignore them.        ║
╚==============================================================================╝

<!-- WORKTREE_TOPOLOGY -->
{
  "mission_slug": "wp51-parity-01M64CVY",
  "mission_number": "",
  "mission_type": "software-dev",
  "target_branch": "feat/wp51-parity",
  "mission_branch": "kitty/mission-wp51-parity-01M64CVY",
  "current_wp": "WP65",
  "diff_command": "git diff kitty/mission-wp51-parity-01M64CVY..HEAD",
  "shared_lane": true,
  "note": "WP65 shares lane lane-g with WP17, WP27, WP36, WP47, WP65. Sequential WPs in the same lane reuse one worktree.",
  "entries": [
    {
      "wp": "WP01",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0
    },
    {
      "wp": "WP02",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-a",
      "lane_wp_ids": [
        "WP02"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-a",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1,
      "dependencies": [
        "WP01"
      ]
    },
    {
      "wp": "WP03",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-b",
      "lane_wp_ids": [
        "WP03",
        "WP24",
        "WP34",
        "WP41"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-b",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 473,
      "dependencies": [
        "WP02"
      ]
    },
    {
      "wp": "WP04",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP01"
      ]
    },
    {
      "wp": "WP05",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0
    },
    {
      "wp": "WP06",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP05"
      ]
    },
    {
      "wp": "WP07",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP05"
      ]
    },
    {
      "wp": "WP08",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP05"
      ]
    },
    {
      "wp": "WP09",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP05"
      ]
    },
    {
      "wp": "WP10",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP05"
      ]
    },
    {
      "wp": "WP11",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP04",
        "WP06"
      ]
    },
    {
      "wp": "WP12",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11"
      ]
    },
    {
      "wp": "WP13",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-c",
      "lane_wp_ids": [
        "WP13"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-c",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 4,
      "dependencies": [
        "WP03",
        "WP04",
        "WP06",
        "WP11",
        "WP12"
      ]
    },
    {
      "wp": "WP14",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-d",
      "lane_wp_ids": [
        "WP14"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-d",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1,
      "dependencies": [
        "WP07",
        "WP12"
      ]
    },
    {
      "wp": "WP15",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP02",
        "WP04",
        "WP10",
        "WP12"
      ]
    },
    {
      "wp": "WP16",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-f",
      "lane_wp_ids": [
        "WP16"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-f",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 2,
      "dependencies": [
        "WP11",
        "WP12"
      ]
    },
    {
      "wp": "WP17",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-g",
      "lane_wp_ids": [
        "WP17",
        "WP27",
        "WP36",
        "WP47",
        "WP65"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1178,
      "dependencies": [
        "WP03",
        "WP11",
        "WP12",
        "WP13",
        "WP15"
      ]
    },
    {
      "wp": "WP18",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP03",
        "WP15",
        "WP16",
        "WP17"
      ]
    },
    {
      "wp": "WP19",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-i",
      "lane_wp_ids": [
        "WP19"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-i",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 293,
      "dependencies": [
        "WP14",
        "WP18"
      ]
    },
    {
      "wp": "WP20",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP07",
        "WP08",
        "WP10",
        "WP12"
      ]
    },
    {
      "wp": "WP21",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP05",
        "WP12"
      ]
    },
    {
      "wp": "WP22",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-j",
      "lane_wp_ids": [
        "WP22"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-j",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 2,
      "dependencies": [
        "WP10",
        "WP12"
      ]
    },
    {
      "wp": "WP23",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-k",
      "lane_wp_ids": [
        "WP23"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-k",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 218,
      "dependencies": [
        "WP01",
        "WP04",
        "WP13",
        "WP14"
      ]
    },
    {
      "wp": "WP24",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-b",
      "lane_wp_ids": [
        "WP03",
        "WP24",
        "WP34",
        "WP41"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-b",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 473,
      "dependencies": [
        "WP03",
        "WP06"
      ]
    },
    {
      "wp": "WP25",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP15",
        "WP23"
      ]
    },
    {
      "wp": "WP30",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-m",
      "lane_wp_ids": [
        "WP30",
        "WP31"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-m",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 815,
      "dependencies": [
        "WP13",
        "WP18",
        "WP20",
        "WP21"
      ]
    },
    {
      "wp": "WP32",
      "status": "approved",
      "execution_mode": "planning_artifact",
      "workspace_kind": "repo_root",
      "lane_id": "lane-planning",
      "lane_wp_ids": [
        "WP01",
        "WP04",
        "WP05",
        "WP06",
        "WP07",
        "WP08",
        "WP09",
        "WP10",
        "WP11",
        "WP12",
        "WP20",
        "WP21",
        "WP32"
      ],
      "branch": "feat/wp51-parity",
      "base": null,
      "commits_ahead": 0,
      "dependencies": [
        "WP01",
        "WP09",
        "WP10"
      ]
    },
    {
      "wp": "WP33",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-n",
      "lane_wp_ids": [
        "WP33"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-n",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 312,
      "dependencies": [
        "WP32",
        "WP02"
      ]
    },
    {
      "wp": "WP34",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-b",
      "lane_wp_ids": [
        "WP03",
        "WP24",
        "WP34",
        "WP41"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-b",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 473,
      "dependencies": [
        "WP24",
        "WP33"
      ]
    },
    {
      "wp": "WP38",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-p",
      "lane_wp_ids": [
        "WP38",
        "WP58",
        "WP61",
        "WP63",
        "WP64"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1013,
      "dependencies": [
        "WP09",
        "WP11",
        "WP32"
      ]
    },
    {
      "wp": "WP39",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-q",
      "lane_wp_ids": [
        "WP39"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-q",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 372,
      "dependencies": [
        "WP32",
        "WP38"
      ]
    },
    {
      "wp": "WP35",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-o",
      "lane_wp_ids": [
        "WP35"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-o",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 451,
      "dependencies": [
        "WP33",
        "WP39"
      ]
    },
    {
      "wp": "WP40",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-r",
      "lane_wp_ids": [
        "WP40"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-r",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 456,
      "dependencies": [
        "WP04",
        "WP13",
        "WP23",
        "WP39"
      ]
    },
    {
      "wp": "WP26",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP25",
        "WP23",
        "WP04",
        "WP40"
      ]
    },
    {
      "wp": "WP41",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-b",
      "lane_wp_ids": [
        "WP03",
        "WP24",
        "WP34",
        "WP41"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-b",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 473,
      "dependencies": [
        "WP02",
        "WP24",
        "WP34"
      ]
    },
    {
      "wp": "WP27",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-g",
      "lane_wp_ids": [
        "WP17",
        "WP27",
        "WP36",
        "WP47",
        "WP65"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1178,
      "dependencies": [
        "WP17",
        "WP24",
        "WP25",
        "WP26",
        "WP41"
      ]
    },
    {
      "wp": "WP28",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP18",
        "WP27",
        "WP16"
      ]
    },
    {
      "wp": "WP36",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-g",
      "lane_wp_ids": [
        "WP17",
        "WP27",
        "WP36",
        "WP47",
        "WP65"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1178,
      "dependencies": [
        "WP27",
        "WP34",
        "WP35",
        "WP38"
      ]
    },
    {
      "wp": "WP29",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-l",
      "lane_wp_ids": [
        "WP29"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-l",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 759,
      "dependencies": [
        "WP28",
        "WP23",
        "WP14",
        "WP36"
      ]
    },
    {
      "wp": "WP31",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-m",
      "lane_wp_ids": [
        "WP30",
        "WP31"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-m",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 815,
      "dependencies": [
        "WP30",
        "WP29"
      ]
    },
    {
      "wp": "WP37",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP28",
        "WP36",
        "WP38"
      ]
    },
    {
      "wp": "WP42",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-s",
      "lane_wp_ids": [
        "WP42",
        "WP45"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-s",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 623,
      "dependencies": [
        "WP23",
        "WP14",
        "WP22",
        "WP39"
      ]
    },
    {
      "wp": "WP43",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-t",
      "lane_wp_ids": [
        "WP43"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-t",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 482,
      "dependencies": [
        "WP23",
        "WP21",
        "WP14",
        "WP39"
      ]
    },
    {
      "wp": "WP44",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP25",
        "WP26",
        "WP42"
      ]
    },
    {
      "wp": "WP45",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-s",
      "lane_wp_ids": [
        "WP42",
        "WP45"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-s",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 623,
      "dependencies": [
        "WP23",
        "WP14",
        "WP22",
        "WP39",
        "WP42"
      ]
    },
    {
      "wp": "WP46",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP25",
        "WP26",
        "WP43",
        "WP44"
      ]
    },
    {
      "wp": "WP47",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-g",
      "lane_wp_ids": [
        "WP17",
        "WP27",
        "WP36",
        "WP47",
        "WP65"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1178,
      "dependencies": [
        "WP36",
        "WP41",
        "WP43",
        "WP46"
      ]
    },
    {
      "wp": "WP48",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP37",
        "WP41",
        "WP43",
        "WP46",
        "WP47"
      ]
    },
    {
      "wp": "WP49",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-u",
      "lane_wp_ids": [
        "WP49"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-u",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 679,
      "dependencies": [
        "WP07",
        "WP14",
        "WP21",
        "WP39",
        "WP43"
      ]
    },
    {
      "wp": "WP50",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-v",
      "lane_wp_ids": [
        "WP50"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-v",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 698,
      "dependencies": [
        "WP02",
        "WP09",
        "WP13",
        "WP14",
        "WP21"
      ]
    },
    {
      "wp": "WP51",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP44",
        "WP46"
      ]
    },
    {
      "wp": "WP52",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP48",
        "WP37",
        "WP47",
        "WP13",
        "WP11",
        "WP21"
      ]
    },
    {
      "wp": "WP53",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-w",
      "lane_wp_ids": [
        "WP53"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-w",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 809,
      "dependencies": [
        "WP50",
        "WP09"
      ]
    },
    {
      "wp": "WP54",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP51",
        "WP13",
        "WP39",
        "WP43",
        "WP46"
      ]
    },
    {
      "wp": "WP55",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP54",
        "WP13",
        "WP39",
        "WP43",
        "WP46"
      ]
    },
    {
      "wp": "WP56",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP55",
        "WP51",
        "WP46",
        "WP49",
        "WP14",
        "WP13",
        "WP43"
      ]
    },
    {
      "wp": "WP57",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP56",
        "WP55",
        "WP51",
        "WP46",
        "WP43",
        "WP39",
        "WP23",
        "WP14",
        "WP13",
        "WP02"
      ]
    },
    {
      "wp": "WP58",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-p",
      "lane_wp_ids": [
        "WP38",
        "WP58",
        "WP61",
        "WP63",
        "WP64"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1013,
      "dependencies": [
        "WP38"
      ]
    },
    {
      "wp": "WP59",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-e",
      "lane_wp_ids": [
        "WP15",
        "WP25",
        "WP26",
        "WP44",
        "WP46",
        "WP51",
        "WP54",
        "WP55",
        "WP56",
        "WP57",
        "WP59"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 986,
      "dependencies": [
        "WP46",
        "WP26",
        "WP14",
        "WP49"
      ]
    },
    {
      "wp": "WP60",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP59",
        "WP52",
        "WP47",
        "WP37",
        "WP14"
      ]
    },
    {
      "wp": "WP61",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-p",
      "lane_wp_ids": [
        "WP38",
        "WP58",
        "WP61",
        "WP63",
        "WP64"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1013,
      "dependencies": [
        "WP58",
        "WP38"
      ]
    },
    {
      "wp": "WP62",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP60",
        "WP16"
      ]
    },
    {
      "wp": "WP63",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-p",
      "lane_wp_ids": [
        "WP38",
        "WP58",
        "WP61",
        "WP63",
        "WP64"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1013,
      "dependencies": [
        "WP61",
        "WP38"
      ]
    },
    {
      "wp": "WP64",
      "status": "in_progress",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-p",
      "lane_wp_ids": [
        "WP38",
        "WP58",
        "WP61",
        "WP63",
        "WP64"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1013,
      "dependencies": [
        "WP63",
        "WP61",
        "WP38"
      ]
    },
    {
      "wp": "WP65",
      "status": "in_review",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-g",
      "lane_wp_ids": [
        "WP17",
        "WP27",
        "WP36",
        "WP47",
        "WP65"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1178,
      "dependencies": [
        "WP47",
        "WP36"
      ]
    },
    {
      "wp": "WP66",
      "status": "planned",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-h",
      "lane_wp_ids": [
        "WP18",
        "WP28",
        "WP37",
        "WP48",
        "WP52",
        "WP60",
        "WP62",
        "WP66"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1167,
      "dependencies": [
        "WP65",
        "WP62"
      ]
    }
  ]
}
<!-- /WORKTREE_TOPOLOGY -->

─── GIT REVIEW CONTEXT ─────────────────────────────────────────────────────────
Branch:      kitty/mission-wp51-parity-01M64CVY-lane-g
Base branch: kitty/mission-wp51-parity-01M64CVY (1178 commits ahead)

Review commands (run in the workspace):
  cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g
  git log kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-g --oneline           # WP commits only
  git diff kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-g --stat             # Changed files
  git diff kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-g                    # Full diff
────────────────────────────────────────────────────────────────────────────────

================================================================================
WHEN YOU'RE DONE:
================================================================================
✓ Review passed, no issues:
  spec-kitty agent tasks move-task WP65 --to approved --mission wp51-parity-01M64CVY --note "Review passed"

⚠️  Changes requested:
  1. Write feedback to (in-repo, committed with the project):
     /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP65-new-doc1-macro-admission/review-feedback-1.md
  2. spec-kitty agent tasks move-task WP65 --to planned --review-feedback-file /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP65-new-doc1-macro-admission/review-feedback-1.md --mission wp51-parity-01M64CVY
  3. move-task stores feedback reference in the event log and WP frontmatter
================================================================================

📍 WORKING DIRECTORY:
   cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g
   # Review the implementation in this workspace
   # Read code, run tests, check against requirements
   # When done, return to repo root: cd /home/lynn/projects/wordling

📚 SHARED MISSION ARTIFACTS:
   Spec, plan, and tasks are visible from the primary checkout: /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/
   Status authority resolves through the coordination worktree for modern missions.
   Use this lane workspace for code/tests; do not expect shared mission artifacts here

📋 STATUS TRACKING:
   kitty-specs/ status is tracked in feat/wp51-parity branch (visible to all agents)
   Status changes auto-commit to the coordination branch (visible to all agents)
   ⚠️  You will see commits from other agents - IGNORE THEM
================================================================================

Review the implementation against the requirements below.
Check code quality, tests, documentation, and adherence to spec.

## Anti-pattern checklist (WP-level cheap version of mission-review)

For each item below, state PASS / FAIL / N/A in your verdict. A FAIL on any
item blocks approval.

1. **Dead code**: every new public function, class, or module created by this
   WP has at least one live caller from production code, excluding tests. For
   each new module, run targeted import/call-site greps, for example
   `grep -r -e "from <new_module> import" -e "import <new_module>" src/ --include="*.<ext>"`.
   Zero production hits means dead code.

2. **Synthetic-fixture test**: every test marked as covering an FR listed in
   this WP's frontmatter actually invokes the production code path that would
   produce the asserted shape. A test that constructs a literal dict matching
   the assertion is a synthetic fixture. Ask: if I delete the implementation
   code, does this test still pass? If yes, the FR is untested.

3. **Silent empty return**: search every new code path for `except ...:
   return ""`, `return None`, `return []`, `return {}`, or `pass`. Each hit
   must have a documented reason; absent that, it is a silent failure
   candidate.

4. **FR coverage**: every FR in `requirement_refs` has at least one test
   assertion that references the behavior it names, not just a comment or
   frontmatter entry.

5. **Frozen surface**: no commit in this WP modifies a file the spec,
   contract, or WP prompt marks as frozen or untouchable. For each frozen file,
   `git log --oneline <base>..HEAD -- <frozen-file>` must be empty.

6. **Locked decision**: no new code path contradicts a `MUST NOT` clause in
   `spec.md`, `plan.md`, or `contracts/`. Grep the diff for forbidden patterns
   named by those clauses.

7. **Shared-file ownership**: any file modified by this WP that is also
   modified by another WP, visible in `lanes.json`, shared lane metadata, or
   the same mission merge, has an explicit coordination note in the move-task
   reason or review feedback.

8. **Production fragility**: any new `raise` in a production code path has a
   documented fail-loud rationale. A bare `raise` in a request handler, worker,
   or CLI path that can fire on a transient race is a fragility risk.


╔==============================================================================╗
║  WORK PACKAGE PROMPT BEGINS                                            ║
╚==============================================================================╝

---
work_package_id: WP65
title: Genuine pristine New Doc1 root macro admission and current-target composition
dependencies:
- WP47
- WP36
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
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T193
- T194
- T195
phase: Genuine New Doc1/default Repeat1/root WPM composition only; not general New macro parity
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/editor/
create_intent:
- internal/editor/evidence/new-doc1-macro/
execution_mode: code_change
owned_files:
- internal/editor/**
role: implementer
tags:
- m1-continuation
- new-doc1-macro
- unreserved-task-draft
task_type: implementation
tracker_refs: []
---

# WP65 — genuine pristine New Doc1 root macro admission (DRAFT, IDs UNRESERVED)

This is a temporary source-backed TASK draft, not code permission or a normal claim. This proposal binds clean post64 planning HEAD5a89172e16993351b4dca958367d7d939b8f0bd2, planning authoritydb2efc4a09b4df2bc529973057d0bf311d55d492;64 existing WPs/192 subtasks/24 lanes with63in_progress/64planned are metadata only. Full installed66/198 proof is separate proposal evidence, not canonical readiness. Do not implement from this draft. Tentative65/T193–195 are unreserved until canonical normalization/finalization, independent task review/CURRENT analysis and a normal issued code prompt. Generic P63/64 metadata may precede this task; their product source, semantics and implementation status are NOT inputs or dependencies. All38/91/36/nested SC001–005/M1 remain OPEN, M2/PDF gated; queue exhaustion does not authorize acceptance.

## Governed authority and source boundary

Resolve implementer-ivan and load scoped implement/software-dev governance. Read AGENTS.md, current spec/plan/research/data-model/continuation, contracts/automation.md/macro-framing.md/native-framing.md/session.md/editing.md, docs/compatibility.md/roadmap.md and actual issued prompt. Read the independently approved New Doc1 design revision2 and its independent ready review copied under this task's provenance (task promotion must install an exact path-map); review is for design only, not this future implementation.

Product source authority is approved H62 e71524f5435057bc6f8490dc7ec6930683c9ba8c and its actual approved G47/36, Doc46/storage41/WPM33/rooted34/VM35 closure. G47 first-binding source09db703822a97d41d9c4e4cd7a5e2f3c10d5f131 deliberately added the New Macro/Repeat/switch exclusions; they are not obsolete bugs. Approved Doc46 44aab36accdf14a370a67fd73945907871ab7193 and storage41 0df934ce3185d73ec53be6d887fba513b44ab803 remain immutable. Harddeps47+36 provide current G ownership/order; actual document46 is inherited through47, not a new native workstream. Verify actual approved dependencies before editing, never infer absent primary code means new files or use a moving lane tip as approval.

Own ONLY internal/editor/**. Existing session.go, macro_session.go, macro_load.go, macro_execution.go, editing.go/new_binding.go and source/read/history APIs exist in approved G; no false create_intent for them. New owned evidence may use internal/editor/evidence/new-doc1-macro/**. Do not change internal/document/wp51/storage/macro/input/tui, cmd/wordling, Go module/dependencies, original fixtures, old source/raw evidence, canonical registries/contracts or P code. No compiler/evaluator/reader/writer/format/geometry API or macro grammar expansion, hidden prototype/shadow Session, direct native byte insertion or loaded-delete-to-empty surrogate. Live reducer/root acquisition/driver callers must reach the implementation; an unused helper with passing tests is incomplete.

The normative design permits one genuine current pristine New Doc1/default Repeat1/root WPM invocation. Existing WithMacroRepeat and switchDocument New guards remain EXACTLY unchanged, including NewAnchored. Loaded-target behavior and18 integrated macro contexts remain unchanged. Broader New contexts/nesting/Repeat3/Doc2/search/recording/editor remain explicit gaps.

## T193 — actual initial admission and root request/ready proof

Implement a narrow New-only branch in the ACTUAL Editing/Macro reducer while preserving the loaded branch. Evaluate eligibility BEFORE MacroName: real initialized document.New Birth/nonzero buffer/transition; NewUnpublished; nil DOC Source/other screen/first publication; Doc1 Editing/revision1/sequence0; actual native revision equals nonzero retained genesis; token count0/gap0; Insert/no Reveal/selection/deletion/history preview/Home; repeat1/no macroOwner/macroReady/macroDelivery/pending; untouched name/draft/original/caret/target/targetDir/targetName/fromExit/touched/prefill/provenance/saved/publication/receipts/notices. Constructor Provenance is numeric0/Text, not a string. Zero/nil, parsed empty, edited-empty, post-attempt/cancellation/error, NewAnchored and any publication state do not become pristine by clearing state.

Observe actual constructor history: valid never-used NewHistory over the same genuine New, qualified known count0 with no stored/preview fragments. Do not equate unknown Count0 with empty or force Dirty/history defaults. Retain the existing interrupted()/InterruptGrouping barrier and actual returned history; legitimate handle/grouping changes do not reconstruct a new stack. Before/after measure native/Birth/genesis/history/name/source/dirty/save/first-save facts.

Capture a PRIVATE immutable New-target descriptor before filename(MacroName), carrying genuine Birth/genesis/admitted native revision/buffer/screen/entry revision/accepted transition. No exported mutable permission, fake source, serialized native mirror or second reducer. Actual filename Text/Enter changes draft/provenance/transitions legitimately; do NOT rerun constructor eligibility after naming/read/first ASCII. On name F1, detached/cancelled/error root acquisition, compile discard and terminal execution release only the proposed admission stage, preserving truthful source/receipt/history/notice state. Returning to Editing permits existing normal edit/save/exit, not a hidden reset for another pristine attempt.

Wire real editName→begin(ReadMacro)→ExecuteMacroRead→acceptedMacroResult→complete(ReadMacro)→StartMacro. New root private proof binds operation/reducer/native revision, run/default Repeat1, zero root request/parent, actual same screen/buffer/Birth/genesis/issued transition, basename and captured opened Directory. Public wrappers/getters remain observations. Existing private Directory copy controls IO even if an equal-path wrapper is rebound; never reopen to counterfeit capability/lifetime. WPM MacroSource/Last.Result.Macro is NOT native DOC Source/Name/SavedRevision/FirstPublication.

Current macroReadProof lacks some New-target/native/transition facts. Add the missing private New-only binding; merely dropping IsNew is insufficient. Resolve the existing Reduce final advanced() ordering explicitly: actual issued pending transition must equal private proof AFTER Enter, using an adoption seam analogous to firstProof.transition, not a pre-Enter token invalidated immediately. Existing complete() advances before macroReady; bind the actual accepted ready transition/source/target there. Validate authentic current pending proof/target BEFORE clearing Pending, recording Applied Last or constructing MacroReady; invalid/forged/foreign/stale replies do not consume current authority. Missing root follows existing MacroError/F1; late cancellation replies are detached diagnostics, never ready/running success.

StartMacro must validate actual accepted ready source/request/transition and unchanged admitted target with Repeat1, compile accepted immutable Image under the unchanged ASCII+DisplayControl policy/limits, then return the ACTUAL current Session/private driver. No fixture-name/hash/output allowlist, borrowed Source or production source overlay. Native WPM word spans are relative to true body offset; FLOW169/body75 is valid despite odd absolute body offset.

## T194 — current-target driver, effects, typed refusals and first-save conservation

Keep actual valid() owner/buffer/screen/exact expected-transition/busy/terminal checks and copied-handle driver ownership. For this New run retain genuine Birth/genesis/NewUnpublished/nil DOC Source/no first-save state across each owned current Step/HostStop; current native revision/cursor may legitimately advance through actual ASCII. Never require current revision==genesis after the first effect, replace/Parse/retrieve/rebase the target or reset an independent history/VM budget. Standalone persistent G forks remain legitimate; do not invent global old-Session revocation/shared mutable consumption tokens. An earlier Session cannot retarget the authentic driver's next expected transition; H66 must supply actual UI/request/worker once-only scheduling.

Use existing VM grammar/evaluator and existing ordinary Apply: one printable ASCII Word→same Reduce(Text) with real immutable edit/history receipt; DISPLAY OFF FC0C→metadata receipt with no native revision/gap edit. No key/Search/query/save/retrieve/switch/format/history/native effect support is enabled. Keep source SHA/actual word/span and before/after revision/gap, Applied/MayHaveEffects/typed failure; AppliedWords is actual accepted DOC words, VM EmittedWords/Steps remain real work/delivery counts. Pure IF/ELSE/GO/LABEL and already supported loops/variables/QUIT are reused, not reimplemented or claimed universally New-qualified.

For ALREADY COMPILABLE NEST FC18, New root-only Resolve returns existing typed host-error/Refusal BEFORE child-name lookup/read/IO. Existing VM maps this to failed/HostFailure; no synthetic CommandError/NotFound or handler success. Preserve earlier actually applied ASCII and honest failed state. New execution creates no child ReadMacro Intent and cannot consume foreign/late nested replies. Existing loaded nested resolution/handlers/QUIT stay unchanged. CHAIN remains statically excluded before ALL effects, including preceding literal text; no runtime ProgramRequest/Resolve/partial effects or compiler/VM widening. The independently ready CHAIN supplement narrowly prevails over R2's over-specific type clause: no qualified CHAIN encoding/fixture is supplied by the20/46 corpus. Preserve documentary CHAIN exclusion by source inspection; real Opaque/UNKNOWN preflight controls assert their actual typed UnsupportedImage path before all effects and are named UNKNOWN, never CHAIN. Statement-level UnsupportedInstruction remains the actual compiler default, not a promised code for an imagined native CHAIN input. No guessed opcode, fictitious execution/conformance test, reader/compiler change or new original acquisition.

Compile/root-read failure, actual VM/native limit, effect refusal or explicit HOST stop/cancel keeps authentic applied revisions/dirty/body/receipts and typed terminal state, never rollback/clean/saved/complete. Original operator F1 remains unsupported during execution; HOST containment is separate. Keep existing default work/output/depth/variable/list/slice/native/rooted acquisition/receipt budgets and cancellation boundaries; no New reset/increase. Actual lower native limit may win while VM budget remains. Unsupported/unknown outcomes remain explicit, not a guessed original condition.

History stays under existing interrupted/AfterEdit/Separate/preview semantics: no fresh global/cross-screen stack, stored fragment erasure or unknown-count qualification. Startup empty Undelete guard remains unchanged. After terminal completion, the same live New lineage/genesis/buffer/screen, actual edited native/history, nil DOC Source, empty DOC Name/no fabricated saved/publication state remain. Macro draft/source diagnostics may persist; ordinary F10 supplies the actual DOC-name prompt, not FLOW.WPM as an automatic saved name.

First publication is existing47→storage41 authority, not new code here: actual post-macro F10/absent name→PublishNewBuffer captures current Birth/native/reducer revision/buffer/screen/root/name/candidate. Success is AwaitFirstRead, not a clean/name/source claim. Only real same-capability BindNewSource with full identity and exact whole bytes attaches first Source/NewAnchored; no Parse/replacement of live New/history/Birth. OriginalExport stays NoLoadedOriginal. Retain missing/equal-bytes-different-inode/metadata/closed Read→PublishedUnbound, read-only retry/no republish, detached/cancelled/unknown publication→PublicationUncertain/reconciliation, existing overwrite refusal and immutable first anchor. Never clear/reset/waive to pass a macro test; no storage fault API/writer changes.

## T195 — real G public proof, whole-native comparison, mutants and bounded custody

Positives must start through actual editor.New on owned real rooted directories containing BOTH immutable original FLOW.WPM sources (advanced03/04 CMD51-205), no retrieved/deleted DOC. Route real Macro/name/Enter/root helper/Complete/StartMacro/Step. Compare full before/ready/running/terminal/first-save snapshots/receipts, native/Birth/genesis/buffer/screen/source/history and real files. FLOW must produce TRUEFALSETAIL/no BAD/SKIP through13 accepted ASCII plus one display metadata receipt, completed1/repeat1, actual gap13 and numeric revision14 as HOST/G invariants; never infer original hardware gap/caret. Source169B/SHA18b4ebb52e6e229bab82aa2aa0afbdfdab0139ccc02b4988a43e4430309938b4/body75 remains immutable. Test quota1 and normal16/work bounds; actual native revisions remain opaque genuine identities.

Use a THIRD distinct existing root program (e.g. M38 ABC at default Repeat1) plus bounded derived independent literal/control negatives; classify additional New-context checks as HOST composition, not extra original New qualification. A fixed FLOW output/name/hash branch must fail real source/span/effect and distinct-program assertions. Derived bytes are test-only supplementary sources, never a production WPM/DOC writer or original fixture. Public copies of snapshots/source/image/request/receipts cannot retarget accepted behavior.

Actual Document.Export AND actual first-published/read-back raw candidate must compare the ENTIRE337B to BOTH original FLOWOUT337B/SHA4737b9e891dda361a6b146e5dc3d571e73cef2e328a18f943032d73cb05a3c01 files through approved parsing/inspection. Existing WP46 empty324 prefix equality is a source fact, NOT future macro output. Preserve real publishBody indexed packet06 bit08 policy and direct-original00 distinction. Locate an actual sole00→08 difference through the real packet owner, retain all raw bytes/length/SHA/difference report, never normalize/clear/pretend byte-identical. Any additional unexplained difference halts the claim and reports a precise reviewed prerequisite; no comparator loosening, new writer/default/profile algorithm, body/manual-typing surrogate or original-run interoperability claim.

Reach real exclusions/adversaries via public actions wherever possible: zero/independent equal-byte New/edited-empty/loaded/anchored/typeover/Reveal/block/history/Home/Doc2/repeat; prior prompt/cancel/root failure/foreign or late request; same-count divergent Session/driver/current transition; source/getter/wrapper mutation; actual NEST partial/handler host failure versus distinct static-refusal preflight; real limits/stop/cancellation; genuine post-macro first publication/read mismatch/retry/detached/unknown reconciliation and stale candidate/source/root. Supplemental structural arrangements cannot substitute for public positives or causal file/receipt paths.

Meaningful ACTUAL owned-source mutants remove New pristine/target/source/issued/ready/current transition validation, broaden Repeat/switch or child IO, replace effect delivery with fixed text, lose receipt/source span/partial-error/work/native/first-save checks. Compile/import failures are not semantic kills; retain original survivors/failures and strengthen probes honestly. Integration deletion must fail at least one real public G positive. Existing18 supported loaded contexts/two-run inputs, four blocked Search178/206 repetitions, loaded Repeat/nesting/handlers/QUIT/history/first-save/source ownership remain real regressions.

Before positives freeze exact source/original public inputs/argv/cwd/env-without-secrets/expectations/resources. Actual configured7/discovered Go build/test/vet, race, scoped gofmt/lint/source compile, targeted relevant old G/document/storage regressions are required; no unrelated long parser fuzz/native reader budgets/new originals. Each Go/configured command≤300s; test case≤4096 explicit driver events, choose small limit probes; evidence≤512files/8MiB, raw diagnostics retained, no truncate/cap expansion. Record target/exit/elapsed/RSS/process/FD facts, no hostile-sandbox/hardRT claim. Only owned disposable HOST processes cleaned.

Custody must distinguish changed owned G SET from historical protected source/evidence SET. Recursive seals include every nested historical seal and exclude ONLY exact root manifest, bind actual Git and working bytes, approved dependency/input/module/public fixture pins and true new files. No huge history copying is needed merely to record hashes. Preserve all old source/raw evidence except genuinely owned G implementation changes and no current conformance/parent/M1 promotion.

Commit only owned G code/tests/evidence. STOP and request ROOT quietpoint BEFORE any T193–195 status/history/ONE normal for_review explicit codex/implementer-ivan/mission. Poll entire synchronous gates/CLI; no force/skip/bypass/kill/retry/manual status repair/self-review. Independent CODE review must approve genuine65 source before H66 consumes it. No accept/merge/push/original grant from this task. If the reviewed boundary cannot be implemented with actual source/private APIs, report the exact missing fact/API/prerequisite instead of widening E/native/storage/VM/H/P scope.


Exact shared design authority paths (installed once under65, not duplicated under66): `tasks/WP65-new-doc1-macro-admission/provenance/authority/design-r2/design.md`, `design-r2/acceptance-and-gaps.md`, `design-r2/package-boundaries.md`; independent `review-r2/report.md` SHA34ff04c788d331fcbbdec7b04f8b20ce5e4e193673baae6d835a8d7c76bf7723. Narrowly prevailing `chain-clarification/addendum.md` SHA031f6cfd309f7ccb0e2874b54b879a45cb818b48837cf1fd1f6334eb679e4786 and independent `chain-review/report.md` SHAab6dc2d33ab62ae1ff361c7d31499c410c904845375a8805fe19ee8803733d7c correct only exact static refusal typing/encoding provenance. All R2/history/old reviews/seals stay immutable; neither source nor code permission is implied.


╔==============================================================================╗
║  WORK PACKAGE PROMPT ENDS                                              ║
╚==============================================================================╝

================================================================================
🎯 REVIEW COMPLETE? RUN ONE OF THESE COMMANDS:
================================================================================

✅ APPROVE (no issues found):
   spec-kitty agent tasks move-task WP65 --to approved --mission wp51-parity-01M64CVY --note "Review passed: <summary>"

❌ REQUEST CHANGES (issues found):
   1. Write feedback to the in-repo path (committed with the project):
      cat > /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP65-new-doc1-macro-admission/review-feedback-1.md <<'EOF'
**Issue 1**: <description and how to fix>
**Issue 2**: <description and how to fix>
EOF

   2. Move to planned with feedback:
      spec-kitty agent tasks move-task WP65 --to planned --review-feedback-file /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP65-new-doc1-macro-admission/review-feedback-1.md --mission wp51-parity-01M64CVY

⚠️  NOTE: You MUST run one of these commands to complete the review!
     The Python script handles all file updates automatically.
================================================================================