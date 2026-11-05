"""Record focused source provenance and verify prior runtime identities read-only."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MISSION = "kitty-specs/wp51-parity-01M64CVY"
CANDIDATE = "c7f14fd497da62bb577b6bdab7d4be3fb124e546"
PARENT = "f89a48627916b5cb9e360c35047350031b6f06a9"


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
    changed = git("diff", "--name-only", PARENT, CANDIDATE).decode().splitlines()
    assert len(changed) == 23
    paths = []
    for path in changed:
        candidate = git("show", f"{CANDIDATE}:{path}")
        actual = (ROOT / path).read_bytes()
        assert actual == candidate, f"Inherited candidate changed without explicit review: {path}"
        paths.append({"path": path, "sha256": digest(actual), "bytes": len(actual)})
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
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
