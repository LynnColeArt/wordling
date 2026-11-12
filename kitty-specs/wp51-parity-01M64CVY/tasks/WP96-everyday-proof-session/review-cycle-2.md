---
affected_files: []
cycle_number: 2
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-11T20:36:01Z'
reviewer_agent: user
wp_id: WP96
---

# WP96 independent review, cycle 2

Request changes on frozen editor source 26e154ac45c0dddfb9d6d6d696e0e912aeb7368b. Metadata alignment b5c0346c changes no internal source. The independently approved two-file native source 6df2a2d7 is an actual ancestor. Existing and fresh independent production-session tests now agree with the original on both cycle-1 findings: ordinary hyphen constituents, exact zorbly at native [16,22), pure-number exclusion, separate duplicate spans, and exact two-space/three-space deletion including punctuation. Native correction/receipt/history and real ESDB/SUP persistence tests pass. Fresh full Go build/test/vet and race across editor, document, proofreading and storage pass. Original DOS hard hyphen 0xA9 remains a separately recorded unsupported native family.

## R96-003 — Quoted duplicate offers an unavailable correction

Fresh March 03/09/92 original typed the exact text `'the  the' fox`, moved to the top and ran Ctrl+F2 Document. The original completes with `Word count: 3        Press any key to continue`; it never enters the blocking Double Word prompt. Confirmed original screen and raw VGA are at /tmp/wordling-WP96-cycle2-independent.C9PbQf/no-duplicate-final/. The capture includes both straight apostrophes and both internal spaces. The release and input scripts are in that same reviewer directory.

The frozen normal public Session with the admitted ESDB returns `Double Word` with the earlier span [1,4) and the second span [6,9). Choosing its actual option 3 returns `document: UnsupportedBody at token 6, span -1+0`. The text remains unchanged, but the visible affirmative action cannot execute. Exact public probe source and output are in /tmp/wordling-WP96-cycle2-independent.C9PbQf/main.go and production.log. The detector at internal/editor/proofreading.go:396–416 checks interior owners and separator spaces but ignores the outer straight quotes. The checked native operation explicitly rejects that outer lexical boundary.

Match the witnessed original by suppressing this duplicate issue in the editor, preserving both words and the count of three. Keep the approved native owner restrictions intact. Add a public regression that contrasts the quoted original with the already qualified unquoted duplicate and checks that ordinary editing/proofreading resume, exact native bytes stay intact, and normal unquoted correction remains executable.

| Check | Result |
| --- | --- |
| Dead code | PASS. Public Session paths use the licensed provider and checked native operation. WP89 owns physical terminal presentation. |
| Synthetic fixture | PASS. Actual original captures and a public production-session check verify the discrepancy. |
| Silent empty return | PASS on resource and ordinary paths. The quoted correction produces a refusal after it was offered. |
| FR coverage | FAIL for T316 quoted duplicate detection and actionable question. |
| Frozen surface | PASS. Scope and metadata-only alignment verified. |
| Locked decision | PASS for licensed provider and native file compatibility. |
| Shared ownership | PASS. Approved G source progression and separately reviewed E native correction remain intact. |
| Production fragility | FAIL for an offered affirmative action that cannot execute. |
