================================================================================
IMPLEMENT: WP72
================================================================================

Source: /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP72-merge-field-body.md

Workspace: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-y
Workspace contract: lane lane-y shared by WP72

Resolved agent identity:
  tool       : unknown
  model      : unknown-model
  profile_id : implementer-ivan
  role       : implementer

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

╔==============================================================================╗
║  🚨 CRITICAL: WORK PACKAGE ISOLATION RULES                              ║
╠==============================================================================╣
║  YOU ARE ASSIGNED TO: WP72                                                    ║
║                                                                          ║
║  ✅ DO:                                                                  ║
║     • Only modify status of WP72                                            ║
║     • Only mark subtasks belonging to WP72                                 ║
║     • Ignore git commits and status changes from other agents           ║
║                                                                          ║
║  ❌ DO NOT:                                                              ║
║     • Change status of any WP other than WP72                               ║
║     • React to or investigate other WPs' status changes                 ║
║     • Mark subtasks that don't belong to WP72                              ║
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
  "current_wp": "WP72",
  "diff_command": "git diff kitty/mission-wp51-parity-01M64CVY..HEAD",
  "shared_lane": false,
  "note": "WP72 owns lane lane-y alone.",
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
      "commits_ahead": 1015,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
      "commits_ahead": 1015,
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
      "commits_ahead": 1015,
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
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
      "commits_ahead": 1015,
      "dependencies": [
        "WP61",
        "WP38"
      ]
    },
    {
      "wp": "WP64",
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
      "commits_ahead": 1015,
      "dependencies": [
        "WP63",
        "WP61",
        "WP38"
      ]
    },
    {
      "wp": "WP65",
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
        "WP47",
        "WP36"
      ]
    },
    {
      "wp": "WP66",
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
      "dependencies": [
        "WP65",
        "WP62"
      ]
    },
    {
      "wp": "WP67",
      "status": "approved",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-x",
      "lane_wp_ids": [
        "WP67"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-x",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1084,
      "dependencies": [
        "WP50",
        "WP53"
      ]
    },
    {
      "wp": "WP68",
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
      "dependencies": [
        "WP55",
        "WP57"
      ]
    },
    {
      "wp": "WP69",
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
      "dependencies": [
        "WP66"
      ]
    },
    {
      "wp": "WP70",
      "status": "in_progress",
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
        "WP59",
        "WP68",
        "WP70"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-e",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1277,
      "dependencies": [
        "WP68",
        "WP64",
        "WP55",
        "WP57",
        "WP39",
        "WP13"
      ]
    },
    {
      "wp": "WP71",
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
        "WP66",
        "WP69",
        "WP71"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1361,
      "dependencies": [
        "WP69"
      ]
    },
    {
      "wp": "WP72",
      "status": "in_progress",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-y",
      "lane_wp_ids": [
        "WP72"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-y",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 1164,
      "dependencies": [
        "WP50",
        "WP53",
        "WP67"
      ]
    }
  ]
}
<!-- /WORKTREE_TOPOLOGY -->

================================================================================
WHEN YOU'RE DONE:
================================================================================
✓ Implementation complete and tested:
  1. **Commit your implementation files:**
     git status  # Check what you changed
     git add <your-implementation-files>  # NOT WP status files
     git commit -m "feat(WP72): <brief description>"
     git log -1 --oneline  # Verify commit succeeded
  2. Mark all subtasks as done:
     spec-kitty agent tasks mark-status T214 T215 T216 --status done --mission wp51-parity-01M64CVY
  3. Move WP to review:
     spec-kitty agent tasks move-task WP72 --to for_review --mission wp51-parity-01M64CVY --note "Ready for review"

✗ Blocked or cannot complete:
  spec-kitty agent tasks add-history WP72 --mission wp51-parity-01M64CVY --note "Blocked: <reason>"
================================================================================

📍 WORKING DIRECTORY:
   cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-y
   # All implementation work happens in this workspace
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

╔==============================================================================╗
║  WORK PACKAGE PROMPT BEGINS                                            ║
╚==============================================================================╝

---
work_package_id: WP72
title: Bounded compiled FIELD1 and IFBLANK2 per-record body evaluation
dependencies:
- WP50
- WP53
- WP67
requirement_refs:
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
created_at: '2026-11-01T22:19:24.466417+00:00'
subtasks:
- T214
- T215
- T216
phase: Bounded per-record merge-body evaluation; full merge and M1 remain open
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/merge/body/
create_intent:
- internal/merge/body/body.go
- internal/merge/body/compile.go
- internal/merge/body/evaluate.go
- internal/merge/body/body_test.go
- internal/merge/body/original_test.go
- internal/merge/body/limits_test.go
- internal/merge/body/README.md
- internal/merge/body/evidence/evaluate/main.go
- internal/merge/body/evidence/evaluate/main_test.go
- internal/merge/body/evidence/verification/
execution_mode: code_change
owned_files:
- internal/merge/body/**
role: implementer
task_type: implementation
tracker_refs: []
---

# WP72 — bounded FIELD1 / IFBLANK2 per-record body evaluation

Reviewed task contracts and source authority are retained under
`tasks/next-increment-72-task-proposal/`: `api-contract.md`, `finite-bounds.md`,
`acceptance-matrix.md`, `source-pins.json`, `research-inputs/` and `project-inputs/`.
The DIFFERENT independent TASK verdict is
`tasks/next-increment-72-task-review/REPORT.md`. Basename contract references below
refer to those exact retained proposal files, not mutable substitutes or current
compiler inputs. Original seals retain original-name meaning; publication maps
and new seals bind any inert archival suffixes.

Audience: the implementer and independent CODE reviewer. WP72/T214–T216 are prospective mechanical identities for the independently approved TASK. Number-neutral/unreserved/proposed wording in retained history keeps its historical meaning. Implementation requires normal canonical gates, fresh actual CURRENT analysis and the issued claim; this document alone grants no implementation or original-software permission.

## Purpose and source authority

Deliver a real compiled per-record body evaluator for the two smallest original-backed forms below, plus a genuine non-test compiled maintainer consumer. Compute body bytes from actual immutable native.Program and explicit.Data. This advances a narrow part of merge semantics without copy-boundary pagination or native output materialization. No ordinary end-user Merge command, editor/reducer/storage/TUI integration, replacement file format, writer, complete merge, layout or pagination is delivered.

Read source-pins.json, the complete assessment.md and its DIFFERENT independent research review, project governance, compatibility/roadmap, mission spec/plan and applicable contracts. Actual sources are approved50 376a37a6afd0d9f11594cadfefe0d557b874a56c, approved53 f70310abb1127a645bf14e984cfcb6da64082713, approved67 5f3035c3efce23c96449458d2c2c783517528cf4. This proposal independently verified all39 declared Git pins:9 source/provenance artifacts and30 native input/result files, retaining both run associations. Manual evidence remains the already sealed later June1992 edition with exact printed/PDF locators; no new original/reference/manual/private execution or acquisition is authorized.

At eventual claim verify actual approved dependency installation, complete compiler/package/GoFiles closure, public signatures, exact protected pathSET/Git/working hashes and genuinely new namespace absence. A source stamp/task routing glob is not installed-source proof. Missing source/API is a precise blocker; never copy/replace a dependency, use a fake Go module/overlay, relax an old test/closure check or borrow moving WP68/70 source. Preserve the old native and DATA consumers' discovered closures exactly. The new package depends outward on native/explicit; neither approved package may gain a backedge/import.

## T214 — compile a closed WHOLE-primary semantic proof

Implement the proposed new body API in api-contract.md. The existing APIs are ONLY the actual pinned Program.Valid/Source/Inspect/Bytes, Source.Equal, Span.Bounds, and explicit.Data.Valid/Source/RecordCount/Field with Value.Valid/Bytes/ExplicitlyEmpty/Provenance. New Compile/Evaluate/Result types are proposed new owned APIs, never described as existing.

Compile captures Program by value, requires the actual expected Primary Source owner, obtains one defensive Inspect and verifies Primary role, no capped/findings/records and all source-owned token/command/operand coverage. It admits ONLY these two complete structural forms, independent of filenames/hashes or literal contents:

- Form A: nonempty printable literal prefix, FIELD1, one terminal native HR0A, then true primary end.
- Form B: IFBLANK2, nonempty printable true literal, ELSE, nonempty printable false literal, ENDIF, nonempty printable separator literal, FIELD1, then true primary end.

Printable literal means exact ASCII20..7E excluding tilde. No arbitrary controls, nested/second IF, HR in a branch, optional/absent ELSE, extra FIELD, arbitrary operand, PAGE OFF/ON, BREAK, NEST, EF/EOR, unknown function/formatter/command, tabs, HP or unowned terminator. This is intentionally smaller than all syntax admitted by native.Program. It must refuse an unsupported whole-primary element even in a branch that would be untaken. Literals may differ freely within this structural predicate; no exactHello/EMPTY/FILLED, fixture name/value/hash allowlist or native frame replay.

The gate accounts for every native token exactly once: literal, admitted terminalHR, command Function, or exact command-owned Operand.Data and Terminator footprint. Numeric operand bytes and their external tilde remain reader character tokens and NEVER become body literals. Validate all spans by the captured Program.Bytes and bounds; zero/foreign owner/spans fail. Do not duplicate outer native framing or fabricate aggregate native.Span values. Command.Match is a COMMAND index: validate IF→ENDIF, ELSE→ENDIF, ENDIF→IF; locate/compile the sole ELSE explicitly, never treat Match as a token index. No public Compile(Inspection), mutable instruction slice, callback, hand-made proof or JSON execution authority.

Build a small immutable compiled representation only AFTER whole-primary validation; no interpretation by replaying expected JSON. Zero/invalid/failed Compile returns no valid plan. Defensive copies and caller wrapper/inspection mutation must not retarget the accepted plan. No native ownership or reader admission is changed.

## T215 — evaluate one actual explicit record atomically

Evaluate a captured plan with actual by-value explicit.Data, expected Secondary Source owner and one-based record ordinal. Check exact source ownership, valid ordinal and every required actual Data.Field before returning any result. FIELD1 appends only Value.Bytes content. IFBLANK2 tests Value.ExplicitlyEmpty: valid explicitly empty selects true, valid nonempty selects false. Missing/outside-explicit field remains the existing typed ExplicitFieldMissing refusal, distinguishable with errors.As; never default it to empty or infer fields from StoredCount−1/tail. A correct FormA207 does not request field2; applying FormB to207 must refuse rather than emit EMPTY. Whitespace-only/named/arbitrary fields remain outside approved Data/candidate semantics.

Use existing source-owned Value.Provenance and Content.Bounds BEFORE a Value.Bytes copy to preflight its length and operation budget. Preserve content/EF/separator/EOR/record/interstitial ownership as diagnostic provenance; EF/separatorHR/EOR/D4/HP are NOT field bytes. FormA terminalHR comes from PRIMARY, not the Secondary separator. Compiler operands/terminators do not emit bytes. No D4 interpretation, metadata stripping from originals or HP insertion. In209 Result originals retain automatic D4+HP between copies even though Primary has no PAGE; keep that evidence unresolved, never call concatenated bodies full merge equivalence.

Assemble output/result privately after checked size/work reservation, exposing a result only after full success. Any source/field/limit/refusal produces invalid zero result and no caller-visible partial body/provenance. Native inputs, original exports, Program/Data owners and prior successful results remain unchanged. Result.Bytes and provenance return defensive copies; zero result is invalid, not a successful empty merge. No editor mutation, filesystem/network/process activity or native document serializer in evaluator code.

## T216 — actual compiled consumer and intrinsic acceptance

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

At eventual implementation freeze commit only allowed new paths, request ROOT's quietpoint before any task/lifecycle advance and obtain a DIFFERENT independent CODE review. Independent TASK approval is retained separately and is not implementation approval. No self-approval, automatic promotion/status, push, accept/merge, new original/private assets/manual/program/resource/VM/grant/physical-lock actions. Full FR012/merge/native/output/pagination/ordinary UI/M1 remains open;37 obligations plusFC010gate/91groups36lessons/SC001–005 retained and PDF/M2 gated.


╔==============================================================================╗
║  WORK PACKAGE PROMPT ENDS                                              ║
╚==============================================================================╝

================================================================================
🎯 IMPLEMENTATION COMPLETE? RUN THESE COMMANDS:
================================================================================

✅ Implementation complete and tested:
   1. **Commit your implementation files:**
      git status  # Check what you changed
      git add <your-implementation-files>  # NOT WP status files
      git commit -m "feat(WP72): <brief description>"
      git log -1 --oneline  # Verify commit succeeded
      (Use fix: for bugs, chore: for maintenance, docs: for documentation)
   2. Mark all subtasks as done:
      spec-kitty agent tasks mark-status T214 T215 T216 --status done --mission wp51-parity-01M64CVY
   3. Move WP to review (will check for uncommitted changes):
      spec-kitty agent tasks move-task WP72 --to for_review --mission wp51-parity-01M64CVY --note "Ready for review: <summary>"

⚠️  Blocked or cannot complete:
   spec-kitty agent tasks add-history WP72 --mission wp51-parity-01M64CVY --note "Blocked: <reason>"

⚠️  NOTE: The move-task command will FAIL if you have uncommitted changes!
     Commit all implementation files BEFORE moving to for_review.
     Dependent work packages need your committed changes.
================================================================================