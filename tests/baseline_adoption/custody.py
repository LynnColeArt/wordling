"""Record focused source provenance and verify prior runtime identities read-only."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MISSION = "kitty-specs/wp51-parity-01M64CVY"
CANDIDATE = "c7f14fd497da62bb577b6bdab7d4be3fb124e546"
PARENT = "f89a48627916b5cb9e360c35047350031b6f06a9"
REPAIR = "78a05497dcf1d175049fe2c8e57fd502818521fe"
REPAIR_REVIEW = "01M6NWK5WXZEMEPGVN1YA8K7GY"
REJECTION = "01M6NV9Z0CPE615HWJBBJK38Q8"
INTAKE = "1561c87ee2c1f7c9532271c482ec97462cc7cbcf"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def worktrees(raw):
    result = {}
    for block in raw.strip().split("\n\n"):
        fields = dict(line.split(" ", 1) for line in block.splitlines() if " " in line)
        if "worktree" in fields:
            result[fields["worktree"]] = fields
    return result


def main():
    before_file = ROOT / MISSION / "milestones/everyday-editing/runtime-before.json"
    before = json.loads(before_file.read_text())
    # This issued workspace contains the finalized planning snapshot. Use that
    # snapshot, not live concurrent primary planning updates, for the claimed map.
    lanes = json.loads((ROOT / MISSION / "lanes.json").read_text())
    current = {wp: lane["lane_id"] for lane in lanes["lanes"] for wp in lane["wp_ids"]}
    assert all(current[wp] == lane for wp, lane in before["wp_lane"].items())
    prior_worktrees = worktrees(before["worktrees"])
    actual_worktrees = worktrees(git("worktree", "list", "--porcelain").decode())
    assert all(actual_worktrees[path].get("branch") == item.get("branch")
               for path, item in prior_worktrees.items())
    assert git("rev-parse", CANDIDATE + "^").decode().strip() == PARENT
    subprocess.run(["git", "merge-base", "--is-ancestor", CANDIDATE, "HEAD"], cwd=ROOT, check=True)
    receipt_file = ROOT / MISSION / "milestones/everyday-editing/resize-repair-intake.json"
    receipt = json.loads(receipt_file.read_text())
    assert receipt["repair_commit"] == REPAIR and receipt["repair_review_event"] == REPAIR_REVIEW
    assert receipt["intake_commit"] == INTAKE and receipt["original_candidate"] == CANDIDATE
    for ancestor in (REPAIR, INTAKE):
        subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, "HEAD"], cwd=ROOT, check=True)
    assert git("show", "-s", "--format=%P", INTAKE).decode().split() == receipt["intake_parents"]
    assert REPAIR in receipt["intake_parents"]
    assert digest((ROOT / MISSION / "lanes.json").read_bytes()) == receipt["preserved_metadata_sha256"][MISSION + "/lanes.json"]
    # Derive the exception from the actual independently approved commit delta.
    # A receipt cannot authorize arbitrary extra paths or arbitrary replacement bytes.
    repair_paths = git("diff", "--name-only", REPAIR + "^", REPAIR).decode().splitlines()
    assert set(repair_paths) == set(receipt["paths_sha256"])
    assert set(git("diff", "--name-only", CANDIDATE, "HEAD", "--", "internal", "cmd", "go.mod", "go.sum").decode().splitlines()) == set(repair_paths)
    repair_inventory = []
    for path in repair_paths:
        approved = git("show", f"{REPAIR}:{path}")
        actual = (ROOT / path).read_bytes()
        assert actual == approved and digest(actual) == receipt["paths_sha256"][path], path
        repair_inventory.append({"path": path, "sha256": digest(actual), "bytes": len(actual)})
    events = [json.loads(line) for line in (ROOT / MISSION / "status.events.jsonl").read_text().splitlines() if line.strip()]
    approval = next(event for event in events if event["event_id"] == REPAIR_REVIEW)
    rejection = next(event for event in events if event["event_id"] == REJECTION)
    assert approval["wp_id"] == "WP90" and approval["to_lane"] == "approved"
    assert approval["review_result"]["verdict"] == "approved" and REPAIR in approval["reason"]
    assert [event for event in events if event.get("wp_id") == "WP90" and "to_lane" in event][-1]["to_lane"] == "approved"
    assert rejection["wp_id"] == "WP77" and rejection["review_result"]["verdict"] == "changes_requested"
    changed = git("diff", "--name-only", PARENT, CANDIDATE).decode().splitlines()
    assert len(changed) == 23
    paths = []
    for path in changed:
        candidate = git("show", f"{CANDIDATE}:{path}")
        actual = (ROOT / path).read_bytes()
        expected = git("show", f"{REPAIR}:{path}") if path in repair_paths else candidate
        assert actual == expected, f"Inherited source diverged from candidate/reviewed repair: {path}"
        paths.append({"path": path, "original_candidate_sha256": digest(candidate),
                      "sha256": digest(actual), "bytes": len(actual),
                      "source": REPAIR if path in repair_paths else CANDIDATE})
    old_events = git("show", f"ee619218d6dbc9f57e00c400d03d940137c205a9:{MISSION}/status.events.jsonl")
    new_events = (ROOT / MISSION / "status.events.jsonl").read_bytes()
    # Existing events may be replayed/serialized by canonical runtime; compare
    # exact old event records instead of assuming a mutable status hash is frozen.
    old_records = old_events.splitlines()
    new_records = set(new_events.splitlines())
    assert all(record in new_records for record in old_records)
    return {
        "source_head": git("rev-parse", "HEAD").decode().strip(),
        "source_branch": git("branch", "--show-current").decode().strip(),
        "candidate": CANDIDATE, "candidate_parent": PARENT,
        "candidate_review_status": "UNREVIEWED until independent WP77 verdict",
        "source_intake": "876bbf85064a847fa0d5e745b6ceb7bcbc912d42",
        "root_preservation_checkpoint": "ee619218d6dbc9f57e00c400d03d940137c205a9",
        "runtime_before_sha256": digest(before_file.read_bytes()),
        "previous_wp_memberships_preserved": len(before["wp_lane"]),
        "previous_worktree_branch_identities_preserved": len(prior_worktrees),
        "prior_status_event_records_preserved": len(old_records),
        "prior_status_events_sha256": digest(old_events),
        "candidate_files": paths,
        "repair_commit": REPAIR,
        "repair_review_event": REPAIR_REVIEW,
        "preserved_rejection_event": REJECTION,
        "repair_intake_commit": INTAKE,
        "repair_intake_receipt_sha256": digest(receipt_file.read_bytes()),
        "repaired_epoch_lane_map_sha256": digest((ROOT / MISSION / "lanes.json").read_bytes()),
        "repair_files": repair_inventory,
        "review_scope": "Original 23-path delta plus approved repair; full WP77 retry review remains required",
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
