---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-11T20:20:51Z'
reviewer_agent: user
wp_id: WP84
---

# WP84 independent review, cycle 1

Request changes on frozen source `b9c574ab10f17ceb1fe67f8002fd6ac8704998d2`. The exact approved WP91 `5aa69050`, WP93 `2df0dd6d`, WP99 `1885c068` and WP94 `3ef16980` sources and the separately reviewed baseline refresh `ca9a5039` are actual ancestors. The refreshed baseline test matches the reviewed Git object exactly. The change is in TUI-owned files and keeps native editing, storage authority and layout with their existing owners. Full Go build, fresh tests, vet, focused TUI and baseline race, and diff checks pass. An independent run of the ordinary CLI at /tmp/wordling-WP84-review.eqgMO9/pty also passes, including the original Reveal comparison, the 12/11-row focus safety, authentic F5/Look/Retrieve, search cancellation/conservation, exact native publication and terminal restoration.

## R84-001 — Short/Long choice skips the original directory request

T266 and EE-A10 require the original Short/Long listing flow. The March 9, 1992 reference at `docs/research/everyday-contract-2026-11-05/qualification/files/trace.jsonl` lines 124–137 repeats both choices. After option 5, choosing 1 or 2 immediately presents the `Dir C:...` confirmation. Enter then lists that directory in the selected mode. The original frame 22 exposes the display-choice prompt before the digit and frames 23/24 show the confirmed results.

In the frozen executable, choosing 2 leaves `1 Short Display; 2 Long Display: 2` on row 24. Enter immediately renders the long list and its command footer. `internal/tui/everyday_files.go:135–143` changes the pending digit only, then toggles the layout on Enter. Independent physical terminal keys and exact screen rows are captured at `/tmp/wordling-WP84-review.eqgMO9/review-browser/everyday-pty-result.json`. The prior PTY runner did not traverse this command.

Route both digit choices through the witnessed directory-request state, preserving the rooted listing capability, current path/pattern and underlying editor state. Verify Short and Long on the normal terminal entry point with exact intermediate prompt/caret, confirmed listing format and original cancel behavior. Keep coverage for unchanged native bytes and focus.

## R84-002 — Expiration of an older failed search erases a newer result

The search notice expiry uses only the numeric native revision (`internal/tui/model.go:119–123,148–151`). Failed searches conserve the same native revision, so the timer from the first miss clears the second miss. Two ordinary F2 failures followed by delivery of the first timer reproducibly clear the new visible result. The independent model test drives exported Model.Update keys and invokes the real returned timer. It fails with `first missed search's timer erased the newer missed search notice` in `/tmp/wordling-WP84-review.eqgMO9/search-overlay.log`. The overlay exists only in the disposable reviewer directory.

Bind transient notices to the exact search-result occurrence or UI generation and add a test that delivers the first and then second timeout. The first timeout must leave the second result visible. The second timeout must restore the same document position/status. Keep search native bytes unchanged.

| Check | Result |
| --- | --- |
| Dead code | PASS. Production runtime, historic view and input dispatch call the new modules. |
| Synthetic fixture | PASS. Normal CLI, real original native inputs and original reference cells exercise the production paths. |
| Silent empty return | PASS. Bounded guard/no-op paths have specific state or refusal semantics. |
| FR coverage | FAIL for the original Short/Long transition and repeat search result settlement. |
| Frozen surface | PASS. Only owned TUI files changed in the package commit, with separately reviewed baseline source intake. |
| Locked decision | PASS apart from witnessed interaction differences above. Native format and unsafe-prefix policy remain unchanged. |
| Shared ownership | PASS. Same H lane source succession with WP76/WP90; approved G intake and independently reviewed Z test-only source intake are separate ancestors. WP85/WP89 should consume the approved retry. |
| Production fragility | FAIL for stale search timer settlement in R84-002. |
