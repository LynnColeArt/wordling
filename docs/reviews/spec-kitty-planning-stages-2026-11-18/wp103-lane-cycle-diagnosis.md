# WP103 late planning-lane cycle — bounded diagnosis

2026-11-18. **No supported registration route exists for the exact retained WP103 metadata in frozen CLI b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3.** The authored WP graph is acyclic; mandatory aggregation into the one canonical planning lane creates a cyclic quotient graph. Holding WP103 is honest. Changing its kind, erasing its real WP86 predecessor, rewriting old approvals or marking it completed would not repair that defect.

Read-only source/retained evidence plus pure in-memory lane calls only. No tool/Wordling source/index/lifecycle/install/worktree/VM/original/Mac effects. Frozen tool HEAD is still b45b48fd; relevant compute/finalizer source has no diff from it. WP104's tool remains untouched.

## Exact retained failure reproduced

Evidence: `/tmp/wordling-mission1-closeout-20261118/finalize-continuation-diagnose-r3.json`; canonical continuation registration-review.md and registration-scope.md explain the hold. The retained R3 error is:

`lane-a → lane-planning → lane-e → lane-c → lane-b → lane-a`

Reconstructed exact authoring snapshot `c94dd461` using git-show reads of canonical WP01–102 frontmatter/bodies plus that commit's retained, unchanged WP103 proposal. Pure `topological_sort` succeeds for all103 WPs. Pure `compute_lanes` succeeds without103 (30 lanes), and adding exact103 reproduces the **same complete cycle path** as retained R3. No finalizer command or write was invoked. Reproduction record: `/tmp/wordling-mission1-closeout-20261118/wp103-lane-cycle-reproduction.json`.

Edges below mean “depends on,” matching the tool graph orientation:

| Aggregated edge | Actual WP dependency causing it |
|---|---|
| lane-a → lane-planning | WP02 → WP01 |
| lane-planning → lane-e | **WP103 → WP86** |
| lane-e → lane-c | WP86 → WP85 or WP89; also WP102 → WP100 |
| lane-c → lane-b | WP17/WP18 → WP03; WP27 → WP24/WP41; WP36 → WP34; WP47/WP48 → WP41; WP94 → WP91 |
| lane-b → lane-a | WP03/WP41 → WP02 |

Relevant memberships are exact retained groups: lane-a={WP02}; lane-planning includes old WP01,04,05,06,07,08,09,10,11,12,20,21,32,78 **plus new103**; lane-e={WP86,WP102}; lane-c includes WP17,85,89,94,100 and the other recorded UI/session owners; lane-b includes WP03,41,79,91,98. Code grouping comes from transitive real write-scope overlap, not dependency edges alone: e.g.86's `tests/everyday_qualification/**` overlaps102's new qualification file;03's `internal/storage/` overlaps91's explicit storage files. The crucial new quotient edge is103→86 from a late planning node that has been identified with old early planning prerequisites.

This does **not** mean WP01 depends on86, or that WP02/103 form a WP cycle. The tool makes all planning WPs one vertex, then treats any member's incoming/outgoing dependency as an edge of that whole vertex. The order early planning → code → late planning is valid at WP level and impossible after that contraction.

## Smallest structural control

Pure in-memory, non-Wordling IDs/metadata for three conceptual tasks:

- early planning A, no dependencies;
- source B depends on A;
- late planning C depends on B, with disjoint owned outputs.

WP topological order is A,B,C. The unchanged public compute function nevertheless raises `lane-a → lane-planning → lane-a`, because A and C are unconditionally grouped. This is enough to prove the defect without historical Wordling owner complexity, extra code owners or an actual second mission.

## Why current supported switches do not fix it

- `lanes/compute.py:409–429` classifies by real execution_mode; all planning_artifact WPs map to PLANNING_LANE_ID. `:559–600` adds cross-mode dependencies over **every WP** and refuses the quotient cycle. `_build_planning_lane:678+` documents the single canonical planning lane/root checkout. There is no authored lane-epoch override in OwnershipManifest.
- Both dry-run (`mission_finalize.py:1937+`) and actual lane-write (`:2438+`) call that same pure compute function. It accepts no topology, lifecycle/completion snapshot or override-lane mapping. `--owned-checkout` supports honest single-branch placement, but does not bypass or alter this preceding aggregate-cycle calculation.
- `--validate-only` reports the same failure; `--refresh-planning-commit` adjusts recorded ancestry, not lane grouping; `--target-branch` cannot change the graph. Neither is a recovery route. A manual lanes.json edit is not authoritative: normal finalization recomputes and refuses.
- WP86 is already approved in the actual status snapshot. Waiting for more approvals or finishing WP104 cannot remove its historic graph edge: computation is status-agnostic. No need to unapprove/reapprove anything.
- `task_type: research`, researcher profile, scope/codebase-wide, or exact disjoint output paths do not override planning_artifact grouping. Disjoint103 ownership already passed the original ownership validation. Relabelling the index code_change would misstate its real work; using a completed ID or adding a separate product mission would violate current constraints rather than repair registration.

One could mechanically remove103→86 and the graph would lose the new edge, but the retained package explicitly depends on that delivered qualification and binds current candidate/evidence. This audit does not authorize deleting a genuine consumption dependency to satisfy grouping. Any materially different contract would need independent review and could not be presented as registering the exact held103.

## Minimal required tooling capability, not permission to implement now

The defect is **unconditional equivalence of early and late planning artifacts at lane-DAG scheduling time**, independent of WP graph acyclicity and the current single-branch owned execution topology.

The smallest graph-level correction for this exact packet is to keep the historical planning group intact and assign late103 a distinct downstream planning scheduling vertex: that vertex depends on the old planning prerequisites05/21 and code86; it still resolves to the **same owned checkout**, remains planning_artifact and does not allocate a worktree. Code lanes must retain dependency ordering; do not ignore all cross-mode edges or suppress LaneDependencyCycleError. Current `is_planning_lane`/PLANNING_LANE_ID and root-workspace/branch consumers assume a single ID, so this requires an explicit reviewed tooling change across the planning-vertex classification/resolution seam, not hand-authored new lane metadata. An equivalent topology-aware single-branch scheduling contract would also need to preserve the actual WP DAG and all root-placement/ownership checks; none exists in the frozen API.

Required narrowly scoped future acceptance, before any rollout: RED minimal A→B→C and exact retained103 reproduction; all authored WPs represented exactly once with actual kinds; dependency-respecting early-code-late ordering; same root/no worktree for both planning stages; no existing99 approval/history/prompt mutation; old all-planning/early-planning and owned single-branch behavior preserved; no generic lane-cycle suppression, implicit approval or hosted contract changes. This identifies the necessary capability only. No repair code, installation, source proposal or live CLI replacement was performed; retain frozen b45 for104.

## Current disposition

Keep exact WP103/T335–337 proposal retained and unregistered. Its full census (244 scenarios,91 parents,36 lessons,38 obligations,5SC plus unclassified leaves) and coverage-index/matrix schema remain required full-M1 work. Root can continue bounded read-only research/planning artifacts outside registration, but cannot claim WP103 lifecycle completion or mission coverage acceptance from that interim work. A tool correction must be separately reviewed and proved before normal registration can proceed with unchanged honest semantics.

Source pins read: compute.py SHA256 `84927ad5ce621140c86f40ba0ea3b5a6049dd92783749f86e565bd17c5df4bb5`; mission_finalize.py SHA256 `357dc338029fbddd06f7caef716a32c930d62e0a2b980611758bac222c77aafb`.
