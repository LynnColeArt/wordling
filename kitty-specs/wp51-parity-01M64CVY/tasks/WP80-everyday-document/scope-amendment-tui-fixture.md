# WP80 scope amendment — cross-owner test fixture (2026-11-05)

Probe that found it: `go test ./...` on lane-e after the T244 everyday
body-owner change.

T244 made `0x0c` a first-class `HardPage` owner. Two tests in `internal/tui/`
used `0x0c` purely as "a byte the catalogue cannot name" to provoke the truthful
partial-inspection fallback, and both failed once the byte became supported.

`internal/tui/` is owned by **WP84** (lane-h), not WP80. The change committed on
lane-e is a probe-byte substitution only — `0x0c` → `0x80` — with every assertion
and its intent preserved, because WP84 is planned and unstarted and WP80's own
gate (`go test ./...`) cannot be green without it. The scope guard warning on
that commit is expected and is the mechanism this note documents.

No WP80 source change was made in `internal/tui/`; no product behaviour changed
there. WP84 still owns the file, the fallback behaviour, and any future
expectation in it.

Lane commit: `cbe5976f`.
