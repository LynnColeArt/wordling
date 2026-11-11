---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-11T20:57:16Z'
reviewer_agent: user
wp_id: WP85
---

# WP85 independent review, cycle 1

Request changes on frozen H source a8ddd67e5e129060d618da64c52882fedf1eea39. Approved WP84 16b3e446 and separately approved test-only e38997d7 are actual ancestors. The exact approved D-EE-04 design and review hashes are in the source. Settings validates the actual opened nonblocking nofollow descriptor, bounds and validates the whole record, atomically publishes within the pinned application directory, and applies visible state only after successful receipt. Fresh three-process normal CLI runs prove default Yes, persisted No and restored Yes with native edits and terminal restoration. Exact observed menu grids, nested focus, actual mouse/key routing, and WP84 file, Reveal and resize regression passed. Full Go build/test/vet and focused TUI and baseline race, format and diff passed. The separately tracked G Search caret discrepancy is outside this TUI review finding.

## R85-001 — Enhanced keyboard template loses original aliases and alternate view

T271 and EE-A03 require the original keyboard template and correct command and modifier labels. Original 03/09/92 raw frame qualification/menus/03-key-template/ shows End Field in the unmodified F9 cell, Reveal Codes in F11 and Block in F12, all four complete modifier legend labels, and Press 1 to view the PC/XT keyboard template on row 23. Independently repeated original F3→F3→1 actually switches to WordPerfect 5.1 Template (IBM Layout). Raw reference evidence is in /tmp/wordling-WP85-review.7sgkPs/original-enhanced/ and original-ibm/.

On the freshly built normal executable, internal/tui/everyday_help.go:67–70 puts Merge in F9 and leaves F11/F12 empty. Its common legend indent at 113–115 clips the key family text at column 79 on the original 80×25 grid, and the alternate-view hint is absent. Pressing physical 1 leaves Enhanced Layout unchanged because helpPress has no corresponding route. Actual terminal frame is /tmp/wordling-WP85-review.7sgkPs/F3-keyboard-template.txt. Physical 1 event, post-key screen, raw wire and key data are in pty-template/default-yes/ under that same directory. This is a visible Help defect. Existing editor F11/F12 command bindings are not disputed.

Restore the witnessed Enhanced labels, full legend at its original 80×25 positions and PC/XT option. Implement the observed display switch to IBM Layout and verify original return focus. Assert the original changed template regions by glyph and logical attribute, plus physical F3→F3→1/return from Help with unchanged native bytes and editing focus. Preserve the verified menu, Setup and WP84 paths.

| Check | Result |
| --- | --- |
| Dead code | PASS. Normal CLI reaches live menus, modal Help and Setup. |
| Synthetic fixture | PASS. Real production executable and raw original cells substantiate the observed differences. |
| Silent empty return | FAIL for the original visible template action dropped by Help dispatch. |
| FR coverage | FAIL for T271/EE-A03 keyboard template labels, geometry and original transition. |
| Frozen surface | PASS. Owned TUI paths only, plus distinct reviewed test intake in ancestry. |
| Locked decision | PASS on reviewed Linux persistence and native format. |
| Shared ownership | PASS. WP85 follows approved H WP84, with test-only intake independently reviewed. |
| Production fragility | PASS. Settings failure and pending async modal authority are bounded. |
