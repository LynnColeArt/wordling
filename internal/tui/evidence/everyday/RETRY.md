# WP84 cycle 2 verification

Cycle 1 source `b9c574ab10f17ceb1fe67f8002fd6ac8704998d2` and its approved dependencies remain in ancestry. This retry addresses the two findings in the independent review.

## R84-001. Confirm the directory for Short/Long Display

WP78 qualification/files trace lines 124–137 and the independent original reruns in `/tmp/wordling-WP84-short-long-original.GsHA6J`, `/tmp/wordling-WP84-display-controls.Ay1XJ4` and `/tmp/wordling-WP84-display-settlement.TvPSFC` document the 03/09/92 sequence. Option 5 shows the alternative display as the default with BIOS caret [33,24]. Choosing the digit or pressing Enter for the default displays the existing pinned directory and pattern, with the old listing visible and the entire initial Dir prompt in logical 0x1F. The BIOS caret is [4,24]. The visible directory prompt accepts Enter or F7 to apply the requested display. F1 and Escape restore the previous confirmed listing. The separate safety behavior for a hidden modal still prevents activating an unseen directory request.

The new model regression uses a non-default `F*.WP` pattern, preserves selection and listing identity across cancellation, and verifies both confirmed modes and unchanged native revision, bytes and history. The ordinary executable runner tests the physical sequence for both digits, the default Enter, F7 confirmation, F1/Escape cancellation, exact prompt positions and roles, the original short divider and the long header. Existing menu, resize, Reveal, browse, Look, retrieve, native save and terminal restoration tests remain in the same runner.

## R84-002. Settle each failed-search notice by its actual occurrence

Each visible miss retains the immutable UI transition of that result. An expiry only clears the matching transition. The regression delivers two real F2 failures and invokes their actual returned Bubble Tea timer commands. It applies the older expiry first and verifies the newer notice is still visible, then applies the matching expiry and checks original status, caret and native bytes.

## Checks

Full Go build, test and vet passed. Focused TUI and baseline adoption race, formatting, Python syntax and Git diff checks passed. Two fresh ordinary executable runs used 80×25 Linux PTYs and the same original FLOW.WP. The original glyph/role comparison, physical keys and SGR mouse path passed. Both F10 copies matched the fixture and both PTYs restored terminal attributes after normal exit.

- `/tmp/wordling-WP84-cycle2.vfQU6M/first/everyday-pty-result.json` recorded 50 steps. Binary SHA-256 `305204b67d1e69942c5f7601d200a5bb66a665d1aad5ac136fd019ecd90e61b2`, native copy SHA-256 `549b55dea301b159bc00ea7910de3695f6169630cfa72f1a2136f74ba39ed7f5`.
- `/tmp/wordling-WP84-cycle2.vfQU6M/repeat/everyday-pty-result.json` recorded 50 steps. Binary SHA-256 `305204b67d1e69942c5f7601d200a5bb66a665d1aad5ac136fd019ecd90e61b2`, native copy SHA-256 `549b55dea301b159bc00ea7910de3695f6169630cfa72f1a2136f74ba39ed7f5`.

Changed code and runner SHA-256

```text
7555cbe6efd513ea726dac3112794680642a183ef9b37e0b2747031a577c4cba  internal/tui/everyday_files.go
928c072696dc74354096e25ec71e3cb6e55f06f8789e28b85fc442987d746a4f  internal/tui/everyday_ui_test.go
f24d7e1a167763df675f1c01effdd369c2f1d4ea08834b0efcb4846fb32a8fda  internal/tui/historic.go
d4dce09697ff333a4f0a6fa4622c5f16e000d4166d94828041ecd42da7414eda  internal/tui/model.go
cf48ee3c95df568be99b4e7573cb3e3f6709410a73b89334c110042d48a72bc3  internal/tui/evidence/everyday/pty-everyday.py
```
