{
  "schema": "wordling.reviewed-delivery-registration/v1",
  "status": "PASS",
  "source": "normal pinned-b45 owned finalize-tasks",
  "input_commit": "00fb65a3680ac76cfd511b47f7edcd3c0c2a274d",
  "finalizer_commit": "dac618ceab761ff7b4bf8f0922f925636c55aac5",
  "planning_commit": {
    "sha": "aed8af3203228fab082f6fe67b8c21ee43282d62",
    "action": "refreshed",
    "previous_sha": "09fdf133323055d0b86e226651c92f82ea6fec1a",
    "branch_tip": "aed8af3203228fab082f6fe67b8c21ee43282d62"
  },
  "wp_count": 107,
  "lane_count": 30,
  "all_104_prior_status_records_equal": true,
  "old_event_prefix_bytes": 1062040,
  "old_event_prefix_sha256": "48c85d4d6311eed7b2d192d821cb51b00d407c628839a2d32ff665ec74c53264",
  "appended_events": [
    {
      "aggregate_id": "WP107",
      "aggregate_type": "WorkPackage",
      "event_id": "01M7QTCH54ATCDYENXWWDF5GMX",
      "event_type": "WPCreated",
      "payload": {
        "actor": "spec-kitty agent mission finalize-tasks",
        "created_at": "2026-11-18T17:13:33.597678Z",
        "depends_on": [
          "WP106",
          "WP94",
          "WP84",
          "WP85"
        ],
        "mission_number": null,
        "mission_slug": "wp51-parity-01M64CVY",
        "wp_id": "WP107",
        "wp_path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP107-retrieve-italics-public-integration.md",
        "wp_title": "Verify rooted public Italics Retrieve and Runtime native publication"
      },
      "project_slug": null,
      "project_uuid": null,
      "schema_version": "5.0.0",
      "timestamp": "2026-11-18T17:13:33.604371+00:00"
    },
    {
      "aggregate_id": "WP108",
      "aggregate_type": "WorkPackage",
      "event_id": "01M7QTCHFHJYPN8KXYCE8V3978",
      "event_type": "WPCreated",
      "payload": {
        "actor": "spec-kitty agent mission finalize-tasks",
        "created_at": "2026-11-18T17:13:33.931818Z",
        "depends_on": [
          "WP70",
          "WP63",
          "WP64",
          "WP68",
          "WP74"
        ],
        "mission_number": null,
        "mission_slug": "wp51-parity-01M64CVY",
        "wp_id": "WP108",
        "wp_path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP108-current-test-runtime-qualification.md",
        "wp_title": "Qualify a fresh current TEST runtime through canonical Preparation"
      },
      "project_slug": null,
      "project_uuid": null,
      "schema_version": "5.0.0",
      "timestamp": "2026-11-18T17:13:33.937495+00:00"
    },
    {
      "aggregate_id": "WP106",
      "aggregate_type": "WorkPackage",
      "event_id": "01M7QTCHJRVXQA9ZZ1CMKE7X7T",
      "event_type": "WPCreated",
      "payload": {
        "actor": "spec-kitty agent mission finalize-tasks",
        "created_at": "2026-11-18T17:13:34.034760Z",
        "depends_on": [
          "WP99"
        ],
        "mission_number": null,
        "mission_slug": "wp51-parity-01M64CVY",
        "wp_id": "WP106",
        "wp_path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP106-retrieve-balanced-italics-native.md",
        "wp_title": "Admit balanced native Italics at the checked document insertion seam"
      },
      "project_slug": null,
      "project_uuid": null,
      "schema_version": "5.0.0",
      "timestamp": "2026-11-18T17:13:34.040461+00:00"
    },
    {
      "actor": "finalize-tasks",
      "at": "2026-11-18T17:13:39.477615+00:00",
      "event_id": "01M7QTCPWNSF2QYQWEKMK9A99T",
      "evidence": null,
      "execution_mode": "worktree",
      "force": false,
      "from_lane": "genesis",
      "mission_id": "01M64CVYYRTDKBCYZ56H6XNTEQ",
      "mission_slug": "wp51-parity-01M64CVY",
      "policy_metadata": null,
      "reason": "canonical bootstrap",
      "review_ref": null,
      "to_lane": "planned",
      "wp_id": "WP106"
    },
    {
      "actor": "finalize-tasks",
      "at": "2026-11-18T17:13:43.083896+00:00",
      "event_id": "01M7QTCTDB97XHF7YW2PJRV4KH",
      "evidence": null,
      "execution_mode": "worktree",
      "force": false,
      "from_lane": "genesis",
      "mission_id": "01M64CVYYRTDKBCYZ56H6XNTEQ",
      "mission_slug": "wp51-parity-01M64CVY",
      "policy_metadata": null,
      "reason": "canonical bootstrap",
      "review_ref": null,
      "to_lane": "planned",
      "wp_id": "WP107"
    },
    {
      "actor": "finalize-tasks",
      "at": "2026-11-18T17:13:46.693583+00:00",
      "event_id": "01M7QTCXY58NAZJN4K6GYM5R47",
      "evidence": null,
      "execution_mode": "worktree",
      "force": false,
      "from_lane": "genesis",
      "mission_id": "01M64CVYYRTDKBCYZ56H6XNTEQ",
      "mission_slug": "wp51-parity-01M64CVY",
      "policy_metadata": null,
      "reason": "canonical bootstrap",
      "review_ref": null,
      "to_lane": "planned",
      "wp_id": "WP108"
    }
  ],
  "other_103_prior_canonical_prompts_byte_identical": true,
  "product_source_changed": false,
  "summary": {
    "approved": 97,
    "blocked": 0,
    "canceled": 0,
    "claimed": 0,
    "done": 3,
    "for_review": 0,
    "in_progress": 1,
    "in_review": 0,
    "planned": 6
  },
  "new_WPs": {
    "WP106": {
      "actor": "finalize-tasks",
      "force_count": 0,
      "lane": "planned",
      "last_event_id": "01M7QTCPWNSF2QYQWEKMK9A99T",
      "last_transition_at": "2026-11-18T17:13:39.477615+00:00"
    },
    "WP107": {
      "actor": "finalize-tasks",
      "force_count": 0,
      "lane": "planned",
      "last_event_id": "01M7QTCTDB97XHF7YW2PJRV4KH",
      "last_transition_at": "2026-11-18T17:13:43.083896+00:00"
    },
    "WP108": {
      "actor": "finalize-tasks",
      "force_count": 0,
      "lane": "planned",
      "last_event_id": "01M7QTCXY58NAZJN4K6GYM5R47",
      "last_transition_at": "2026-11-18T17:13:46.693583+00:00"
    }
  },
  "WP104_still_in_progress": true,
  "WP104_approval_held_until_WP108": true,
  "operational_reference_actions": 0,
  "Mac_testing": false,
  "proof_check_correction": "Initial read-only proof assumed wp_id at top level for both WPCreated and lane events; corrected to their actual distinct schemas and asserted both exact sets. No event or state was modified."
}
