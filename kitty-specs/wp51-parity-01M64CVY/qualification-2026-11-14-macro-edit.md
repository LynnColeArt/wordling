# Mission 1 Linux preflight: editing WPM and page numbering

The working-tree build has SHA-256
`4c251ec5e0dad3d9e965d705f9dc90b474e8847e7198918bbc13f922d5681642`.
A rebuild matched byte for byte. [Build inputs and exact source hashes](../../research/cache/mission1-wpm-edit.SIVZWC/working-tree-build.json)
capture the active checkout. The shared production tree contains
uncommitted work, so this is a preflight, not the formal candidate.

| Work | Result |
| --- | --- |
| Edit an existing WPM | The [four Linux terminal journeys](../../research/cache/mission1-wpm-edit.SIVZWC/pty-pages-macro) compare exact DOS bytes for a literal edit, a description edit, and Left plus an Action line break. Cancel leaves the original unchanged. Go tests cover a reverted edit and a concurrent replacement. |
| Native round trip | [WordPerfect 5.1 DOS replayed all three edited files](../../research/cache/mission1-wpm-edit.SIVZWC/dos-pages-macro.log) and kept the WPMs unchanged. The bare Action line break is display only; recorded Enter still executes exactly once. The edit and playback also passed in [GNOME Terminal](../../research/cache/mission1-wpm-edit.SIVZWC/gnome/run.log). |
| Macro control flow | The [16 terminal journeys](../../research/cache/mission1-wpm-edit.SIVZWC/pty-macro-control-r3) all reproduced the saved DOS native bodies and kept the original WPMs unchanged. Four cases used a loaded empty document: nested calls in a new unsaved document were refused in the [first run](../../research/cache/mission1-wpm-edit.SIVZWC/pty-macro-control-r2.log). Body bytes match; this does not assert equality of the save prefixes. DOS also [opened, edited and resaved](../../research/cache/mission1-wpm-edit.SIVZWC/dos-control-roundtrip/original-roundtrip.json) the Linux output of the quoted and raw list-value case. |
| Page number position | [Top Center, Bottom Right and first-page suppression](../../docs/research/reference-runs/mission1-page-number-position/README.md) match DOS native data and print output for the three explicit pages. The [Linux saves](../../research/cache/mission1-wpm-edit.SIVZWC/pty-pages) also reopened in DOS and produced the same printer files. |
| Initial Codes | [DOS captures](../../docs/research/reference-runs/mission1-initial-codes/README.md) show how setting and resetting line spacing stores a prefix packet while keeping the text body unchanged. Wordling implementation remains open. |
| Regression | All 73 cases in the [integrated Linux and DOS preflight](../../research/cache/mission1-wpm-edit.SIVZWC/suite-pages/suite.json) passed on the exact build. The control flow batch above ran separately against the same executable and is now wired into the runner. [Go tests](../../research/cache/mission1-wpm-edit.SIVZWC/go-test-pages.log), [go vet](../../research/cache/mission1-wpm-edit.SIVZWC/go-vet-pages.log), [race checks for the changed packages](../../research/cache/mission1-wpm-edit.SIVZWC/race-all.log), [fixture hashes](../../research/cache/mission1-wpm-edit.SIVZWC/fixtures.log), [terminal input](../../research/cache/mission1-wpm-edit.SIVZWC/terminal-keys/qualification.json) and [eight recovery journeys](../../research/cache/mission1-wpm-edit.SIVZWC/recovery) also passed. |

The [command audit](../../docs/research/mission-1-command-audit.md)
now has 180 verified, 41 partial and 23 unimplemented scenarios.
The verified profile for WPM editing is a recorded action with
ASCII text, Left and the captured Enter words. Arbitrary action
programs can still be inspected, but their editing and legacy
conversion remain open. The remaining parity obligations,
clean candidate, independent review and accepted preview are
still pending. The [formal candidate builder](../../research/cache/mission1-wpm-edit.SIVZWC/formal-candidate.log)
stopped at its clean production tree requirement.
