---
work_package_id: WP66
created_at: '2026-11-01T10:13:30.092351Z'
base_ref: kitty/mission-wp51-parity-01M64CVY
invocation_id: 02a305a556ac4e058e07d74046703f8d
lane_branch: kitty/mission-wp51-parity-01M64CVY-lane-h
lane_worktree: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h
mission_branch: kitty/mission-wp51-parity-01M64CVY
mission_id: 01M64CVYYRTDKBCYZ56H6XNTEQ
mission_slug: wp51-parity-01M64CVY
prompt_path: /tmp/spec-kitty-review-prompts/wordling-addc41014af6/wp51-parity-01M64CVY/WP66/02a305a556ac4e058e07d74046703f8d.md
repo_root: /home/lynn/projects/wordling
---

================================================================================
REVIEW: WP66
================================================================================

Source: /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP66-new-doc1-macro-host.md

Workspace: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h
Workspace contract: lane lane-h shared by WP18, WP28, WP37, WP48, WP52, WP60, WP62, WP66

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

╔==============================================================================╗
║  🚨 CRITICAL: WORK PACKAGE ISOLATION RULES                              ║
╠==============================================================================╣
║  YOU ARE REVIEWING: WP66                                                     ║
║                                                                          ║
║  ✅ DO:                                                                  ║
║     • Only modify status of WP66                                            ║
║     • Ignore git commits and status changes from other agents           ║
║                                                                          ║
║  ❌ DO NOT:                                                              ║
║     • Change status of any WP other than WP66                               ║
║     • React to or investigate other WPs' status changes                 ║
║     • Review or approve any WP other than WP66                             ║
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
  "current_wp": "WP66",
  "diff_command": "git diff kitty/mission-wp51-parity-01M64CVY..HEAD",
  "shared_lane": true,
  "note": "WP66 shares lane lane-h with WP18, WP28, WP37, WP48, WP52, WP60, WP62, WP66. Sequential WPs in the same lane reuse one worktree.",
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
      "commits_ahead": 1236,
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
      "commits_ahead": 1236,
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
      "commits_ahead": 1236,
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
      "commits_ahead": 1236,
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
      "commits_ahead": 1236,
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
      "commits_ahead": 1236,
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
      "commits_ahead": 1236,
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
      "status": "in_review",
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
      "commits_ahead": 1236,
      "dependencies": [
        "WP65",
        "WP62"
      ]
    }
  ]
}
<!-- /WORKTREE_TOPOLOGY -->

─── GIT REVIEW CONTEXT ─────────────────────────────────────────────────────────
Branch:      kitty/mission-wp51-parity-01M64CVY-lane-h
Base branch: kitty/mission-wp51-parity-01M64CVY (1236 commits ahead)

Review commands (run in the workspace):
  cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h
  git log kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-h --oneline           # WP commits only
  git diff kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-h --stat             # Changed files
  git diff kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-h                    # Full diff
────────────────────────────────────────────────────────────────────────────────

================================================================================
WHEN YOU'RE DONE:
================================================================================
✓ Review passed, no issues:
  spec-kitty agent tasks move-task WP66 --to approved --mission wp51-parity-01M64CVY --note "Review passed"

⚠️  Changes requested:
  1. Write feedback to (in-repo, committed with the project):
     /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP66-new-doc1-macro-host/review-feedback-1.md
  2. spec-kitty agent tasks move-task WP66 --to planned --review-feedback-file /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP66-new-doc1-macro-host/review-feedback-1.md --mission wp51-parity-01M64CVY
  3. move-task stores feedback reference in the event log and WP frontmatter
================================================================================

📍 WORKING DIRECTORY:
   cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h
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
work_package_id: WP66
title: Production New Doc1 root macro route and first native Save composition
dependencies:
- WP65
- WP62
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
- T196
- T197
- T198
phase: Real New Doc1/default Repeat1/root WPM product composition; not general New macro parity
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/tui/
create_intent:
- internal/tui/evidence/new-doc1-macro/
execution_mode: code_change
owned_files:
- internal/tui/**
role: implementer
tags:
- m1-continuation
- new-doc1-macro
- actual-production-composition
- unreserved-task-draft
task_type: implementation
tracker_refs: []
---

# WP66 — real New Doc1 macro route and first Save (DRAFT, IDs UNRESERVED)

Temporary TASK draft only. Tentative66/T196–198 are UNRESERVED until independent task review, normal canonical normalization/finalization/full snapshot/refresh/CURRENT analysis and an actual issued claim. This proposal binds clean post64 planning HEAD5a89172e16993351b4dca958367d7d939b8f0bd2/authoritydb2efc4a09b4df2bc529973057d0bf311d55d492;63in_progress/64planned are metadata only, not source or dependencies. Do not implement from this draft. P63/64 are generic separate P metadata/order context only, never source/semantic/dependency inputs. Full38/91/36/nested SC001–005/M1 remain OPEN; M2/PDF gated; queue exhaustion is not acceptance.

## Authority, actual source and ownership

Read AGENTS.md and current spec/plan/session/editing/automation/macro-framing/native/new-publication context, docs/compatibility.md/roadmap.md, the actual issued prompt and independent ready New Doc1 design revision2/review installed under this task's exact provenance mapping. Resolve implementer-ivan and scoped implement governance. Consume genuine independently CODE-approved WP65 implementation and its actual public G contract; design/task approval is not code. Directdeps65+62 preserve new G consumption and approved H ordering;62 already inherits37/48/60/52/47/16 and actual Doc46/storage41/WPM33/rooted34/VM35. Do not introduce P or new E/H/G backedges or assume a planning-only primary contains source.

Approved H62 source e71524f5435057bc6f8490dc7ec6930683c9ba8c is the immutable starting H baseline. Before writes record actual clean claim HEAD, actual complete inherited H/protected source+Go/module/fixture SET/Git+working hashes and approved65 dependency commit/hash/API closure. A normal claim or automatic VCS stamp alone is not proof new G is installed. Use actual cwd/GOMOD/go-list compiler packageDirs/GoFiles/source hashes to prove production uses65. Run the actual installed branch-currency predicate/callback: None requires no merge; any non-None blocker requires exact path/source classification and ROOT resolution BEFORE a dependency merge. No production overlay, module replacement, manual source copy/reset/rebase, fake API or fallback to old G. Missing source or incompatible API is a concrete prerequisite to report.

Own ONLY internal/tui/**, new evidence internal/tui/evidence/new-doc1-macro/**. Existing H model/runtime/macro/new files are approved source, not create_intent. Preserve unmodified cmd/wordling, input/decoder, editor/document/storage/native/macro packages and Go modules/dependencies; no P imports/resource/tool/controller/original authority. Existing old H/native/module/contracts/raw evidence are exact except genuinely owned H changes. New rendering or helper-only demo cannot substitute for actual production entry/async callers.

Normative product slice is genuine pristine New Doc1, default Repeat1, root WPM only, existing ASCII/DISPLAY effects and existing VM grammar. WithMacroRepeat and switchDocument New guards remain unchanged; loaded macros/Repeat/nesting/handlers/QUIT and actual New first-save semantics remain. Original205 supports selected Doc1 TRUEFALSETAIL after recorded Macro Editor prelude, no untouched-startup default/hardware caret/full native equality claim;132 is explicit blank Doc2 after ShiftF3, not startup Doc1 Repeat3.

## T196 — actual current Model/runtime entry and owned async lifetime

Wire the ACTUAL Runtime.Open→editor.New→Model.Update→existing macroKey/resolve/reduce route. No zero/copied/injected Session, retrieved-and-erased DOC, private renderer switch, shadow macro buffer or static output path. Preserve the FIRST original claimUI boundary, exact input.Translate delivery and existing lifecycle/reply/stop handling before keys. State/View/Session/receipt observations never mint/claim authority. Read-only diagnostics must be copied data, not mutable capabilities.

Before forwarding Editing/AltF10 for a New birth, verify current non-stopping runtime/UI and untouched HOST-only orchestration: no repeatEntry, H notice/reconciliation, unsettled/detached IO, firstPending/old first tickets/deferred receipt, macro flow/ticket/CPU/active/worker/suppressed/frozen state or another Model's active runtime macro, no prior issued/completed operation history disguised as idle. G65 alone authenticates initialized Doc1/NewUnpublished/nonzero genuine Birth/genesis/current native/buffer/screen/history/source/receipts and captures admission BEFORE MacroName. H never clears native/session/IO/notices to regain eligibility. Keep legitimate typed refusals and actual existing prompt precedence; no string-derived authority.

H62 shown menu remains display-only. Actual shown AltF10 MUST be refused before any macro/editor command, with unchanged native/session/IO. The user hides it with exact Alt+=, which clears only its own display diagnostic; then the still genuine pristine current Model can enter Macro. No auto-dismiss-and-run or shown key fallthrough. Exact H62 Alt+= identity,80-cell styles/row restoration/frozen/resize behavior and nonpress routing remain. Native/source/history/IO are not reset on hide.

After legitimate MacroName/name/Enter, do not reapply the constructor or untouched HOST-start predicates to each reply/first effect. Follow the actual current chain: real rooted ReadMacro command/private receipt→Complete→MacroReady→macroStart→real start/step worker. Preserve Runtime.command/execute-once/settle, macroIO ownership, startMacro/nextMacro/macroCommand/deliverMacro private tickets, captured source, expected current G transition, other-model/stale/duplicate/late guards and actual pending/first-save separation. Source wrappers/getters can be replaced by callers without retargeting authentic target/source/lifetime. No matching-counter mirror, manufactured receipt or detached helper may complete work.

An independent pure G Session fork remains a legitimate independent value; it cannot replace the actual H chain or satisfy the authentic driver's next expected transition. Enforce actual single-use UI/request/ticket/driver progression, not invented global old-Session revocation. During macro ownership, manual Save/Retrieve/Reveal/Repeat/switch/history/edit keys retain existing refusal; original F1 remains unsupported live stop. HOST stop/context cancellation/Close remains containment with genuine admitted read/worker reconciliation and partial-state receipts, not rollback/original-cancel/false clean exit. Host administrative EnvMsg/ColorProfileMsg exact no-ops remain after claimUI, other Unknown refusals/authentic notices stay unchanged.

Use approved G65 NEST root-only runtime failure and static CHAIN exclusion without new H conditions/search/error suppression. Already compilable NEST→existing resolver New HostFailure before child lookup/read/IO; earlier actual ASCII remains and no CommandError/NotFound/handler success. CHAIN never becomes runtime/partial success. The independently ready CHAIN supplement narrowly prevails: CHAIN has no qualified native encoding/fixture in the supplied corpus; inspect its documentary exclusion and run only real source-backed UNKNOWN/static controls with truthful typed codes (Opaque findings may yield UnsupportedImage before statement UnsupportedInstruction). Never relabel UNKNOWN as CHAIN or invent a CHAIN runtime test/opcode.

## T197 — real public Model, DISPLAY OFF and post-macro first-publication proof

Public positives begin at actual Open on owned real directories with both immutable original FLOW.WPM copies, actual delivered AltF10/name/Enter, actual Cmd executions/replies and real current View/State/Session/Runtime.Completed/CompletedMacros. No direct private sink/flag/renderer as sole positive. Bind before/name/root-wait/worker-start/active-suppression/terminal/save-name/publish/first-read/anchored phases. Compare complete actual snapshots/native/Birth/genesis/current revisions/gap/history/dirty/name/source/save/publication/first receipt and returned Cmd/IO counts. Mutating diagnostic/source/request/image/receipt copies cannot steer the authentic execution. Test real current/stale/zero/closed runtime and another model's macro, duplicate/repeated/root/worker replies and same-counter divergent native/UI transitions.

FLOW source169B/SHA18b4ebb52e6e229bab82aa2aa0afbdfdab0139ccc02b4988a43e4430309938b4/body75 must stay immutable. Run each original through actual root read/Compile/VM/ordinary ASCII, finish New Doc1 TRUEFALSETAIL/no BAD/SKIP, completed1/repeat1 and genuine source/span/13 literal+1 DISPLAY receipts. Source WPM is not DOC Source, current New Birth/genesis remain, edited native/history/dirty are real; no fabricated loaded Name or save success. The G gap13/revision14 checks are HOST/domain invariants, not original hardware proof.

Require a THIRD distinct actual existing root (e.g. M38 ABC/default Repeat1) through public Model and production PTY, plus labeled bounded derived negatives. Additional New-context checks are HOST composition, not fresh original Doc1 qualification. Distinct source/receipt/output assertions must fail a fixed TRUEFALSETAIL/name/hash branch or insertion bypassing VM effects. Do not add a product fixture switch, output observer hook or new grammar/writer.

Reach actual nonterminal DISPLAY OFF worker slices: use FLOW work slicing if exposed plus a supplemental derived longer bounded root as needed, parsed/acquired/executed through the actual path. Select the SAME frozen normal/reveal/error/inspection/source capture before any live data; no live menu/diagnostic/inspection leak. Resize retains ordinary normalization1..4096 and view recomputation, not native work/restart/retry/constructor permission; terminal state releases suppression and shows actual current text/error. Actual replies/deferred settlement/Stop/Close must not be swallowed by display/refusal paths.

Use real public actions wherever reachable for loaded/nonblank/edited-empty/anchored/Doc2/selection/typeover/Reveal/history/Home/Repeat, name F1/missing/malformed/compile refusal, real root/nested/static failure, IO/first-save/deferred/uncertainty/reconciliation, worker/other-model/stale/lifetime exclusions. Supplemental private arrangements are explicitly labeled and cannot replace real positives/causal ownership. Retain18 supported loaded contexts/two-run inputs, four explicit blocked Search178/206 repetitions, loaded Repeat/nesting/handlers/QUIT, all47/48/60/62 chosen-visible/native/history/IO/source/admission behavior.

After ACTUAL terminal macro completion, ordinary F10/absent DOC basename uses existing first-save path on the SAME post-macro New target. Macro draft does not become DOC name automatically. PublishNewBuffer captures real Birth/current native+reducer revision/buffer/screen/root/name/candidate; successful publication is AwaitFirstRead, not clean/source/name binding. Only authentic same-capability BindNewSource/full identity and whole candidate bytes attaches first DOC Source/NewAnchored/current saved/name while preserving live New Birth/genesis/history/cursor. No Parse/retrieve/object replacement; OriginalExport remains NoLoadedOriginal. Test actual post-macro first-read missing/equal-bytes-different-inode/metadata/closed failure, explicit readonly retry/no republish, pending/detached/cancelled/unknown publication and retained truthful reconciliation. Matching digest/reopened root cannot repair unknown outcome; no overwrite/writer/fault-port expansion. Saved/anchored/publication contexts cannot regain pristine New macro/menu/Repeat/switch permission by clearing state.

## T198 — unchanged production decoder/PTY/native comparison, adversaries and custody

Freshly build UNCHANGED cmd/wordling after final production changes in actual approved closure. Record exact cwd/GOMOD/module/source tree, actual go-list packageDirs/GoFiles/compiled inputs, build argv/nonsecret env, binarySHA and executed CLI argv. No automatic Git stamp, source overlay/test flags or cached unrelated binary substitutes for compiler source authority. At least two independent80×25 production PTYs use both original FLOW sources; a THIRD distinct root PTY case kills fixed FLOW output. Actual terminal input must drive real decode→Model→rooted read→Compile/worker/effects→macro completion, observe text/no sentinel and later normal interaction, ordinary F10/absent filename/save and clean original exit workflow/termios restoration. No posthoc frame or fake source/native object. PTY only proves observable decoded route/render/real file/terminal effects; private birth/receipt/history/IO proof stays in G/public Model.

Actual candidate/export/first publication/read-back must compare the FULL337 raw bytes against BOTH original FLOWOUT337B/SHA4737b9e891dda361a6b146e5dc3d571e73cef2e328a18f943032d73cb05a3c01 through existing approved parse/inspection. The known existing WP46 empty324 prefix match is NOT future output proof. Keep ordinary publishBody indexed packet06 bit08 emitter and original direct00 distinction. If actual sole00→08 difference occurs, bind it to its real indexed owner and report exact rawlength/SHA/byte/field; never clear/normalize it or call byte-identical. Additional unexplained differences HALT the claim/report precise prerequisite, no comparator weakening/new default/profile/native/writer semantics. Body equality/manual typing cannot establish wholefile/native/original-context parity; hardware caret/default/resource geometry remains unqualified.

Meaningful actual-owned-source mutants remove current/pristine/context/IO/worker/source/receipt/frozen/lifetime checks, let shown menu or manual active keys fall through, drop real G integration or replace it with fixed text, invent saved/source binding or reset a budget. Public Model AND fresh actual production PTY must fail integration deletion/fixed-output substitutions; compile/import failures are not semantic kills. Retain initial survivors, strengthen probes and preserve all raw failed attempts. G65 source/receipts faults may be run only in separately owned disposable approved-source mutation setups with explicit restoration/custody, never silently amend another owner's live lane. No new native/IO/VM test seam is authorized.

Freeze original public inputs/expectations/argv/env/cwd/source/resources BEFORE positives. No original/private controller/resource/manual/font/SET/PRS/master/failedHD/VM/QEMU reads/stat/exec or grant; only public captured Git outputs and owned disposable HOST processes. Each PTY≤30s+2s TERM/KILL/reap; live retained combinedstdout/stderr≤2MiB enforced before append (no capture-then-slice); each Go/configured command≤300s; Model case≤4096 explicit events; code evidence≤512files/8MiB. Retain raw failures, actual elapsed/RSS/process/FD/exit/target observations; no hostile-sandbox/hardRT/original-performance claim. Stop/report on insufficient bounds, no truncate/unreviewed expansion.

Run actual configured7/discovered Go build/test/vet/race, scoped gofmt/lint/Python source compile for evidence scripts, targeted actual oldG/H/source/first-save/resource checks. No unrelated long parser fuzz or native-reader/new-original budgets. Verify actual public callers: existing real Update/macro route consumes G65, no orphan helper; old loaded routes remain reachable. Preserve module/input/G/E/storage/native/oldH source+fixtures/raw evidence except genuinely owned H implementation; distinguish true WP66 changedSET from historical protectedSET. Recursive current Git+working seals include ALL nested historical seals and exclude only exact root manifest; bind actual approved65/input/G/E/Go/public fixture/compiler/binary closure. No current conformance/parentFR/fullM1 promotion.

Commit only owned H code/tests/evidence; STOP for ROOT quietpoint BEFORE T196–198 status/history/ONE normal for_review explicit codex/implementer-ivan/mission. Poll entire synchronous gates/CLI, no force/skip/bypass/kill/retry/manual state repair/self-review. Independent CODE review required. No accept/merge/push/original authority; concrete missing source/API/policy must be reported, not solved by G/E/storage/VM/cmd/input/P widening or a demonstration-only product facade.


Exact shared design authority paths (installed once under65, not duplicated under66): `tasks/WP65-new-doc1-macro-admission/provenance/authority/design-r2/design.md`, `design-r2/acceptance-and-gaps.md`, `design-r2/package-boundaries.md`; independent `review-r2/report.md` SHA34ff04c788d331fcbbdec7b04f8b20ce5e4e193673baae6d835a8d7c76bf7723. Narrowly prevailing `chain-clarification/addendum.md` SHA031f6cfd309f7ccb0e2874b54b879a45cb818b48837cf1fd1f6334eb679e4786 and independent `chain-review/report.md` SHAab6dc2d33ab62ae1ff361c7d31499c410c904845375a8805fe19ee8803733d7c correct only exact static refusal typing/encoding provenance. All R2/history/old reviews/seals stay immutable; neither source nor code permission is implied.


╔==============================================================================╗
║  WORK PACKAGE PROMPT ENDS                                              ║
╚==============================================================================╝

================================================================================
🎯 REVIEW COMPLETE? RUN ONE OF THESE COMMANDS:
================================================================================

✅ APPROVE (no issues found):
   spec-kitty agent tasks move-task WP66 --to approved --mission wp51-parity-01M64CVY --note "Review passed: <summary>"

❌ REQUEST CHANGES (issues found):
   1. Write feedback to the in-repo path (committed with the project):
      cat > /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP66-new-doc1-macro-host/review-feedback-1.md <<'EOF'
**Issue 1**: <description and how to fix>
**Issue 2**: <description and how to fix>
EOF

   2. Move to planned with feedback:
      spec-kitty agent tasks move-task WP66 --to planned --review-feedback-file /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP66-new-doc1-macro-host/review-feedback-1.md --mission wp51-parity-01M64CVY

⚠️  NOTE: You MUST run one of these commands to complete the review!
     The Python script handles all file updates automatically.
================================================================================