---
type: reference
updated: 2026-11-18
audience: Spec Kitty repair reviewer and Wordling mission orchestrator
---

# Planning-stage repair, approved after independent re-review

The held WP103 metadata reproduces a false cycle when early and late planning
work share one scheduling vertex. The independently approved plan separates
scheduling epochs while retaining one real planning root and every code-owner
and dependency guard. It does not address the separate combined Italics code
ownership cycle.

Candidate43869ef8 was independently reviewed against frozenb45. Despite622passing
affected tests and73architecture/performance checks, two live consumers omitted
the actual typed lane: bound context creation and topology rendering fail for a
later planning stage. The retained public reproducer proves both failures with
an early-stage positive control. The verdict is **REQUEST CHANGES**.

The author corrected those two consumers with two typed arguments, preceded by
genuine public-path RED tests. Independent re-review **APPROVES candidate8315a288**:
806 regression tests passed with two existing skips;96 architecture, ratchet and
actual performance checks passed; Ruff and strict typing passed. The new bounded
call-site gate checks all17 actual branch consumers and preserves every existing
baseline. See the cycle2 report and source-provenance.json for exact identities.

ROOT has activated ec868755 as the explicit per-invocation local source after
checking all14 source origins/hashes and the actual host's CLI/identity/topology/
workspace diagnostics. Global installations are unchanged. `AGENTS.md` and
rollout.json record the exact command; the distribution banner3.2.6 is distinct
from the selected repaired source. Actual live validate-only must still pass
before WP103 registration. The multistage manifest is local-only and deliberately
refuses older readers, including b45; it is not a hosted protocol upgrade.

## Recovery archive

`source/spec-kitty-planning-epochs-ec868755.bundle` preserves **both** the earlier
large-ID/retry repair and this reviewed scheduling repair, with implementation
and independent review history. Its only upstream prerequisite is commit
`fb4e8fa9810d053e31d94e9ccc71259b4946c7db` in the official Spec Kitty repository.
The MIT license is retained beside it. The bundle is tracked in Git rather than
depending solely on temporary directories or ignored caches.

An independent empty bare repository fetched that exact upstream base, verified
and imported the bundle, recovered ec868755 and the exact source tree, and passed
Git connectivity checks. The temporary verification repository was removed.
`spec-kitty-planning-epochs-bundle-restore.json` retains the commands and hashes.
