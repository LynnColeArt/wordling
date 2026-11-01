---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-01T14:15:59Z'
reviewer_agent: reviewer-renata
wp_id: WP67
---

# WP67 cycle 1: changes requested

## F1 — [P2, blocking acceptance] Bind every local compiled source kind

Target: `scripts/reference/explicit_secondary_data.py:217` (`Session.build`, lines217–237).

The reviewed source gate validates only local `GoFiles` against the manifest. It rejects Cgo/C files, but SFiles/HFiles/SysoFiles and the other enumerated kinds are only recorded. Thus a new source member in the frozen native provider can pass qualification without an approved source pin.

I reproduced this through the public launcher in a disposable copy. All260 existing copied inputs were exact. Adding only `internal/merge/native/unreviewed.s`, a valid68-byte empty assembly file, made the actual Go package report `SFiles:["unreviewed.s"]`. That file is absent from the approved manifest. Nevertheless `audit --report prior.json` exited0, returned successful24/36/6 qualification and replaced the genuine prior report. The original product worktree was untouched. This is an authority/provenance acceptance failure; no malicious assembly or native-document corruption is claimed.

T200 requires checking **all actual compiled native/wp51 bytes against approved source**, and preserving prior reports on source substitution. Merely reporting the new source does not satisfy that gate.

Remediation:

1. Check every actual local compiled source kind against the complete reviewed source set, not just GoFiles. Under the current Go-only closure, rejecting unexpected non-Go local compiled members is sufficient. Do not modify frozen native/wp51 files or silently approve new provider inputs.
2. Add a public source-substitution regression using a build-valid extra assembly member in a disposable native/provider tree. Require nonzero refusal, unchanged prior report and unchanged input/source bytes. Include the exact runtime/public failure assertion, not merely a manifest-construction or compile failure.
3. Requalify the unchanged real30-image corpus and fresh-value path with the corrected launcher. Update source identities/evidence honestly; preserve prior frozen evidence and this counterexample.

Evidence: `source-closure-control-result.json`, `closure-added-assembly.stdout/.stderr`, `source-closure-commands.json`, `source-closure-unapproved-success.json`, and reproducible `source-closure-control-revision2.py`. The success report explicitly records the unapproved SFile and its SHA.

The Go DATA implementation and ordinary qualification tests otherwise passed this review. No unchanged Go/fuzz rerun is required solely for a launcher/test correction; validate affected changes and the actual final source closure.
