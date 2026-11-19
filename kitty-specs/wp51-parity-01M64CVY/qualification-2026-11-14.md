# Mission 1 Linux preflight, November 14, 2026

The current comparison build was rebuilt byte for byte.
Its SHA-256 is
`5b380148674c6bee227e1a10f5f22ca93f658f32a9aac948c1b30a751f08edc7`.
[Source and executable hashes](../../research/cache/mission1-compare-linux.6Cnr7M/working-tree-build-multiline.json)
bind it to the active working tree at `e9caa7e1`.
The source tree includes ongoing Mission 1 changes, so this is a
preflight build. The formal candidate builder requires a clean
production tree and an independent review is still due.

| Work | Evidence |
| --- | --- |
| Build and regression | [Go test](../../research/cache/mission1-compare-linux.6Cnr7M/go-test-multiline.log), [go vet](../../research/cache/mission1-compare-linux.6Cnr7M/go-vet-multiline.log), and [fixture checksums](../../research/cache/mission1-compare-linux.6Cnr7M/fixtures-multiline.log) passed. |
| Worksheet import and refresh | [Six Linux PTY cases](../../research/cache/mission1-compare-linux.6Cnr7M/sheet-final-pty) check exact range, a signed offset range, the native link, the saved cache across restart, unchanged saves, and explicit updates from both Wordling and original DOS link files. Fast Save Yes matches the DOS 564-byte prefix. The DOS printer streams match for both imported ranges and the cached link. [WordPerfect 5.1 reopened the three Wordling saves](../../research/cache/mission1-compare-linux.6Cnr7M/dos-sheet-multiline-build). |
| Document Compare | [Both Linux PTY cases](../../research/cache/mission1-compare-linux.6Cnr7M/compare-both-pty) match the native DOS bodies, assert that the prior file stays intact, and verify Reveal Codes. The one-line DOS printer stream matches. |
| Macro recording research | [The new DOS WPM capture](../../docs/research/reference-runs/mission1-macro-recording/README.md) identifies the two owners for Enter and the Left key owner. Wordling recording and WPM publication remain open. |

The [worksheet-only build passed all 65 integrated cases](../../research/cache/mission1-worksheet-final.e9jXgA/suite/suite.json), including proofreading, save failures and the original DOS round trips.

The preceding comparison build `efebfb60dfb114e8c1abd18959d550aad2e6d90100fe63ef3183430a1bf36e0d`
also has the [integrated run](../../research/cache/mission1-compare-linux.6Cnr7M/suite/suite.json),
[GNOME Terminal input run](../../research/cache/mission1-compare-linux.6Cnr7M/gnome.log),
[recovery evidence](../../research/cache/mission1-compare-linux.6Cnr7M/recovery),
and a [Wordling compare save that DOS reopened](../../research/cache/mission1-compare-linux.6Cnr7M/dos-compare/compare/screen.txt).
The build difference is the extension to compare a changed line
surrounded by unchanged lines.

The [command audit](../../docs/research/mission-1-command-audit.md)
now records 163 verified, 55 partial and 26 unimplemented. Full
Linux acceptance, the accepted preview, and follow-ups on macOS
and Windows remain pending. The passing preflight does not
replace acceptance against the full inventory.
