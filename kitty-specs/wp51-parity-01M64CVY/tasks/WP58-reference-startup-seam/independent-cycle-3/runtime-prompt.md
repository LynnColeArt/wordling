---
work_package_id: WP58
created_at: '2026-11-01T03:59:09.637329Z'
base_ref: kitty/mission-wp51-parity-01M64CVY
invocation_id: 28b3ca5da9b248baa46149d7c188d537
lane_branch: kitty/mission-wp51-parity-01M64CVY-lane-p
lane_worktree: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p
mission_branch: kitty/mission-wp51-parity-01M64CVY
mission_id: 01M64CVYYRTDKBCYZ56H6XNTEQ
mission_slug: wp51-parity-01M64CVY
prompt_path: /tmp/spec-kitty-review-prompts/wordling-addc41014af6/wp51-parity-01M64CVY/WP58/28b3ca5da9b248baa46149d7c188d537.md
repo_root: /home/lynn/projects/wordling
---

================================================================================
REVIEW: WP58
================================================================================

Source: /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP58-reference-startup-seam.md

Workspace: /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p
Workspace contract: lane lane-p shared by WP38, WP58

Resolved agent identity:
  tool       : codex
  model      : unknown-model
  profile_id : researcher-robbie
  role       : researcher

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
║  YOU ARE REVIEWING: WP58                                                     ║
║                                                                          ║
║  ✅ DO:                                                                  ║
║     • Only modify status of WP58                                            ║
║     • Ignore git commits and status changes from other agents           ║
║                                                                          ║
║  ❌ DO NOT:                                                              ║
║     • Change status of any WP other than WP58                               ║
║     • React to or investigate other WPs' status changes                 ║
║     • Review or approve any WP other than WP58                             ║
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
  "current_wp": "WP58",
  "diff_command": "git diff kitty/mission-wp51-parity-01M64CVY..HEAD",
  "shared_lane": true,
  "note": "WP58 shares lane lane-p with WP38, WP58. Sequential WPs in the same lane reuse one worktree.",
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
        "WP47"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 830,
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
        "WP52"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 942,
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
        "WP58"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 883,
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
        "WP47"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 830,
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
        "WP52"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 942,
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
        "WP47"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 830,
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
        "WP52"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 942,
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
        "WP47"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-g",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 830,
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
        "WP52"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 942,
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
        "WP52"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-h",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 942,
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
      "status": "in_review",
      "execution_mode": "code_change",
      "workspace_kind": "lane_workspace",
      "lane_id": "lane-p",
      "lane_wp_ids": [
        "WP38",
        "WP58"
      ],
      "branch": "kitty/mission-wp51-parity-01M64CVY-lane-p",
      "base": "kitty/mission-wp51-parity-01M64CVY",
      "commits_ahead": 883,
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
    }
  ]
}
<!-- /WORKTREE_TOPOLOGY -->

─── GIT REVIEW CONTEXT ─────────────────────────────────────────────────────────
Branch:      kitty/mission-wp51-parity-01M64CVY-lane-p
Base branch: kitty/mission-wp51-parity-01M64CVY (883 commits ahead)

Review commands (run in the workspace):
  cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p
  git log kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-p --oneline           # WP commits only
  git diff kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-p --stat             # Changed files
  git diff kitty/mission-wp51-parity-01M64CVY..kitty/mission-wp51-parity-01M64CVY-lane-p                    # Full diff
────────────────────────────────────────────────────────────────────────────────

================================================================================
WHEN YOU'RE DONE:
================================================================================
✓ Review passed, no issues:
  spec-kitty agent tasks move-task WP58 --to approved --mission wp51-parity-01M64CVY --note "Review passed"

⚠️  Changes requested:
  1. Write feedback to (in-repo, committed with the project):
     /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP58-reference-startup-seam/review-feedback-3.md
  2. spec-kitty agent tasks move-task WP58 --to planned --review-feedback-file /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP58-reference-startup-seam/review-feedback-3.md --mission wp51-parity-01M64CVY
  3. move-task stores feedback reference in the event log and WP frontmatter
================================================================================

📍 WORKING DIRECTORY:
   cd /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p
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
work_package_id: WP58
title: Generic bounded artifact preparation process startup and readiness component
dependencies:
- WP38
requirement_refs:
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T172
- T173
- T174
phase: Offline generic component only; no original resources or acquisition
history: []
agent_profile: researcher-robbie
authoritative_surface: scripts/reference/startup_transport.py
create_intent:
- scripts/reference/startup_transport.py
- tests/reference/startup-seam/
- docs/research/continuation/macro-session/startup-seam/
execution_mode: code_change
owned_files:
- scripts/reference/startup_transport.py
- tests/reference/startup-seam/**
- docs/research/continuation/macro-session/startup-seam/**
role: researcher
tags:
- m1-continuation
- generic-reference-transport
- offline-os-tests-only
task_type: implementation
tracker_refs: []
---

# TEMP candidate WP58 — generic bounded preparation, process startup and readiness

## Identity, source scope and sequencing

This revision explicitly implements the NEW reviewed design revision2, dropping the old legacy-delegation requirement. IDs WP58/T172–T174 are NOT reserved. Resolve researcher-robbie and research governance at actual implementation. Read AGENTS/charter/spec/plan, files-platform/resource-readiness/session contracts, exact adjacent design revision2+NEW independent design review, their original history and source-resolution diagnostic, and approved38 source for provenance/unchanged compatibility checks ONLY. Actual57 SourceContractPrerequisiteBlocked0 is motivation, not an input to P behavior; do NOT read active57 implementation as authority. Hard dependency is ONLY WP38. No55/57/E import/semantic dependency. If implementation needs E semantics, stop and report the true dependency/design conflict.

Actual57 is now canonically APPROVED terminal SourceContractPrereq BLOCKED0 ONLY: sourced93097de0552e309a0dd9c0b653247ac49ec5536/event01M6AD9VM0GX3W6SDKV16NNEPV, codex/reviewer-renata/force:false/wholeCLI0/durable. This satisfies the external sequencing outcome condition, supplying NO original tickets/guests/full protocol/prelaunch/native Enter/M1 authority and NO P semantic dependency. Current committed31d731615562f8d0d9187e3c4f28619666d2ca2f is rebased as planning context only; no57 implementation/API is borrowed. NEW independent baseline TASK review/root promotion/current analysis/normal claim still remain separate gates. Design/task READY is not implementation approval or grant.

Own ONLY **scripts/reference/startup_transport.py**, **tests/reference/startup-seam/** and **docs/research/continuation/macro-session/startup-seam/**. All are genuinely NEW paths with truthful create_intent. Real public API/closed TEST CLI lives in the new script, real executed tests/fixtures in the tests namespace, and meaningful contracts/JUnit/source/resource/run evidence in38's macro-session subtree. No marker/dummy ownership. This is generic reference-support work on existing lane-p, not C13 or E. Do NOT modify or own macro_session.py, guest.py, qmp.py or ANY legacy caller/helper. All their bytes/default behavior remain unchanged and retain legacy limitations; they do not become newly safe. Preserve exact fixed source/caller closure; no historical pin/raw/result rewriting.

No E/native/core/module/Go/editor/TUI/storage/WordPerfect format/writer/current-registry/task/lifecycle source changes. No copied fresh_start/controller/decoder, original-specific resource resolver/settings filename/command/scratch sentinel/argv/startup-text/frame/mode/keys/normalDOS/stop/export recipe, no E peer/account/normal-stop import, no private/global patch or asserted ownership provider. Original crypto gates stay future E duty, not a P provider. **No original VM/QEMU, real guard/private ledger/master/program/font/SET/PRS/manual/failed-HD access in58 EVER.** Its actual OS tests use disposable authored files/profiles/tools/processes/unique sockets and TEST-only messages. No original guest permission follows from58 approval. All38/91/36/nested SC001–005 fullM1 open/M2 gated; Linux Go/Bubble Tea product remains unchanged.

## T172 — public generic artifact/preparation and actual bounded process core

Implement documented PUBLIC immutable artifact/tool/command/runtime-endpoint specs, result/error types and source-consistency contracts. Preparation verifies explicit regular-file size/hash/source identity, freshness/no-clobber/symlink policy, owned guarded copy/roundtrip/snapshot/atomic report actions and retains partial states. Artifacts/configuration are opaque project-authored test data or later consumer-supplied explicit descriptions; P does not decode original environment.json/SET or certify original profile validity. A hash/result/JSON boolean/callback assertion cannot mint original qualification, OS ownership, normalDOS, grant or safe stop. Return actual observed facts and explicit synthetic component limits.

Use one real default streaming command supervisor through PUBLIC calls: exact argv/env/cwd/executable identity, monotonic start/end/phases, separate stdout/stderr and aggregate caps, finite deadline/rate/poll/concurrency/file/journal/JSON/argv bounds and measured RSS. No shell, capture-then-slice, unbounded default callback capture, inherited-group kill or unlimited drain. Freeze explicit numeric budgets before positive evidence: initial envelope <=1MiB/stream/command, <=16MiB aggregate per component attempt, <=15s ordinary command/launcher, <=60s explicitly named readiness, <=256MiB runtime RSS, serial commands; freeze JSON bytes/depth/nodes, process/descendant count, file count/bytes, log cap/poll limits and any justified finite compiler/configured-check exception. These are test envelopes, not throughput/product SLOs. Record real elapsed/RSS/executions/env/argv and resource limitations; do not silently loosen limits to pass.

Reject nonzero/deadline/overflow even if eventual return0; preserve bounded exact raw/partial metadata and first fault. Actual fixture groups/processes are positively owned before TERM/KILL escalation; bound escalation/reap/EOF/drain and descendants holding pipes after launcher exit. No foreign signal, socket unlink, command or fabricated cleanup. Source swapped after validation, aliases/symlink/hardlink/replaced files, short writes/partial copy/permission/disk/atomic-replace/report failures must preserve prior/foreign artifacts and return truthful partial failure; failed persistence never equals durable report success. No implicit next/start/retry/resume/calibration after an operation fails. P low-level attempt journal is NOT E's whole-plan ledger.

## T173 — live PUBLIC fixture CLI, launch journal/readiness and future E interface

Make the new module genuinely executable/useful: a closed declared harmless TEST fixture CLI and public Python API exercise the actual core/default supervisor, copy/verification/launch/readiness path. Freeze CLI commands/roster/signatures/public source closure and expected actions before tests. Contract printer alone, dead helper or stub successful executor is insufficient. The CLI must not accept an arbitrary original/QEMU launch recipe or discover private original paths. Generic Python API remains composable with explicit specs, never an original grant. Synthetic fixtures do not impersonate WordPerfect/QMP accepted screen semantics; local protocol sends TEST messages only.

Publish pre-spawn observation before process creation and actual launcher spawn evidence. Exceptions (including actual start-then-raise, observer/readiness failure, overflow/deadline) retain the same invocation/journal/partial OS facts. After launch could have happened, missing returned argv/pidfile is **UNKNOWN, never proved0**. Distinguish intended/charged action, actual launcher, possible daemon, positively owned daemon and readiness. Observer may add observations but cannot replace kernel identity or assert ownership. Observe/bind actual PID/startticks/kernel argv/executable and owned endpoint/asset descriptors; parent/launcher reaped/group cleanup does NOT prove a daemon gone. Test delayed/missing/reused pidfile/child, executable/argv/disks/source/socket mismatch and child surviving launcher. Unknown ownership cannot authorize signals/protocol/unlink or successful stop.

Public readiness factory/callback is low-level: called only after positively bound launch identity, with identity/source/journal facts, bounded lifetime and ownership checks BEFORE greeting/capabilities/TEST action on EVERY connection. Foreign/unknown endpoints receive ZERO commands; no fallback to legacy QMP.__enter__. Caller-provided JSON/callback success is never kernel ownership or normal-stop proof. Ambiguous daemon launch/cleanup remains unsafe/UNKNOWN for future E to charge/halt permanently; P never reports original-qualified/normalDOS/native success. Freeze observer/result/error contracts and bound callback execution/outputs; do not call an unbounded callback on a trusted path.

**Legacy compatibility is BY NONMUTATION.** macro_session.fresh_start(qmp,guest,work,assets) does NOT delegate to this module and remains its inaccessible original-profile path; all five known caller files and other discovered legacy imports are byte-exact. No attempt to run that legacy path through fake profiles; no guest.py endpoint patch. The public new CLI/component is this package's live integration target. A later real E consumer must DIRECTLY compose approved P API plus approved E peer/account/normal-stop interfaces, own original resource interpretation/exact commands/settings/startup/full-frame keys/native/export/master/release protocol, and have independent actual source/prelaunch review + exact new ROOT grant. Using old fresh_start while claiming new guarantees is forbidden; no future task authored/reserved here. Do not duplicate a complete old controller to demonstrate that interface; provide a minimal generic typed-call contract and executable TEST consumer only.

## T174 — real public OS adversaries, unchanged-source proof and honest handoff

Freeze authored fixture rights/source hashes/default limits/public CLI roster/import closure before runs. Exercise real PUBLIC APIs/default supervisor/CLI with harmless actual OS processes/files/local TEST sockets. No private monkeypatches, merely mocked successful dependencies or forged original-profile checks. Required meaningful falsifiers:

- Valid generic prepare/copy/hash/roundtrip/snapshot then TEST readiness, synthetic observation never original authority; malformed wrappers/JSON bytes-depth-node limits, source alias/retarget/wrapper/field/hash changes, replaced files after validation, symlink/no-clobber/prior output and source-consistency refusal.
- Actual flood stdout AND stderr, aggregate overflow, hang, nonzero, partial output/copy, shortwrite/close/atomic replacement/permission/persistence failure, retained raw failures and prior artifact preservation; bounded cleanup even if descendant holds pipe EOF after launcher exits; real deadline/RSS/process-count enforcement and unknown failure telemetry, no report success after write fails.
- Actual spawn then exception/observer error/readiness error; daemon-like child remains after launcher; delayed/missing/reused PID/startticks; kernel argv/exe/asset/socket mismatch, foreign endpoint0commands/signals, no identity minted by callback/asserted JSON; positive group TERM/KILL/reap and bounded unsafe cleanup refusal; UNKNOWN never0/no extra start.
- Actual readiness-before-owner refusal and every-connection guard, malformed/stale/replayed observation or receipt cannot retarget authority, unbounded/throwing callback cannot bypass caps; TEST protocol results carry no QMP/original/native meaning.
- PUBLIC CLI covers declared success/failure roster, source-controlled executable fixture consumer calls new API directly; meaningful mutants bypassing output caps, start observer/identity, source validation, foreign readiness and atomic prior-output preservation must fail actual public tests with retained red logs. Do not mirror implementation or replace tested core with mocks.
- Exact immutable Git/source/caller inventory: macro_session/guest/qmp plus macro_quit/code_pair_history/native_genesis/resaved_prefix and discovered callers remain BYTE-UNCHANGED; actual import names/module paths cannot shadow old helpers. Assert old original source hashes and default semantics BY BYTEIDENTITY, not new legacy execution/bounds claims. All edited files lie ONLY in new owned paths. No real original/software resource reads/execution to make the test convenient.

Publish deterministic contract/CLI result/JUnit/source-custody/limit/runtime receipts under the real P evidence subtree. Check atomic outputs/source seal/working-vs-Git and all changed source paths. Discover configured charter checks/packages honestly; run actual configured7 and appropriate AST/compile/Python/component tests, distinguish pre-existing failures/legitimate no-target skips. This task affects no Go and permits no Go overlay/helper; do not repeat unchanged parser fuzz/Go resource budgets. If Go/core or other source becomes needed, stop for scope decision. Real configured Go commands may discover approved inherited packages; record actual targets/results, no false Python-only skips. Maintain every failed test/intentional mutant raw log and exact command/env/elapsed source disposition.

Commit ONLY owned new source/tests/evidence. Request root primary quietpoint before T172–T174 done marking/ONE normal for_review codex/researcher-robbie/mission; poll entire synchronous gate and CLI to full exit. No self-review/force/skip/bypass/other package advance or accept/merge. Independent code review must inspect reachable new CLI/default supervisor and process/source ownership. Handoff is generic component/API limits ONLY; P package never acquires original resources or guests. Future E integration/gates remain separate and fullM1 open.


╔==============================================================================╗
║  WORK PACKAGE PROMPT ENDS                                              ║
╚==============================================================================╝

================================================================================
🎯 REVIEW COMPLETE? RUN ONE OF THESE COMMANDS:
================================================================================

✅ APPROVE (no issues found):
   spec-kitty agent tasks move-task WP58 --to approved --mission wp51-parity-01M64CVY --note "Review passed: <summary>"

❌ REQUEST CHANGES (issues found):
   1. Write feedback to the in-repo path (committed with the project):
      cat > /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP58-reference-startup-seam/review-feedback-3.md <<'EOF'
**Issue 1**: <description and how to fix>
**Issue 2**: <description and how to fix>
EOF

   2. Move to planned with feedback:
      spec-kitty agent tasks move-task WP58 --to planned --review-feedback-file /home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP58-reference-startup-seam/review-feedback-3.md --mission wp51-parity-01M64CVY

⚠️  NOTE: You MUST run one of these commands to complete the review!
     The Python script handles all file updates automatically.
================================================================================