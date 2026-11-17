# Mission 1 Linux preflight: native macros and Italics

The working-tree executable with the macro inspection view was
rebuilt byte for byte. It is
`e30e54e687a0dff1bdad00edd19ca78b07f5cce61d7fce679aab58f3fc38cca0`.
[Build identity](../../research/cache/mission1-macro-linux.p29NHn/working-tree-inspect-build.json)
includes the local compiled sources and their hashes.

| Scope | Evidence |
| --- | --- |
| Native WPM | The [Linux PTY cases](../../research/cache/mission1-macro-linux.p29NHn/pty-inspect-r2) cover recording two exact DOS WPMs, playback after recording, opening and closing an untouched DOS Action, and declining or confirming replacement. Go checks also cover stale replacement, an empty description, and keeping partial edits on F1 stop. |
| DOS round trip | WordPerfect 5.1 DOS ran the [Linux-authored macros](../../research/cache/mission1-macro-linux.p29NHn/dos-roundtrip-final): the first wrote `ABC`; in the second the operator's next key produced `A B\nXC`, confirming both Enter and Left. The WPM files remained unchanged, including the original WPM after its trip through Wordling. |
| Italics | [DOS native, print and screen fixtures](../../docs/research/reference-runs/mission1-appearance/README.md), the [Linux journey](../../research/cache/mission1-macro-linux.p29NHn/font-italics/qualification.json) and [DOS reopen](../../research/cache/mission1-macro-linux.p29NHn/dos-italics/compare/screen.txt) match for the captured Italics span. |
| Regression | [Full Go suite](../../research/cache/mission1-macro-linux.p29NHn/go-test-complete.log) [go vet](../../research/cache/mission1-macro-linux.p29NHn/go-vet-inspect.log), and the [focused race checks](../../research/cache/mission1-macro-linux.p29NHn/race-focused.log) passed. The [GNOME Terminal Ctrl+F10/Alt+F10 run](../../research/cache/mission1-macro-linux.p29NHn/gnome-inspect/run.log) passes on the inspection build. The preceding build with recording, replacement, stop and Italics passed all 70 [integrated cases](../../research/cache/mission1-macro-linux.p29NHn/suite-final/suite.json) and [crash recovery](../../research/cache/mission1-macro-linux.p29NHn/recovery-final). |

The [audit](../../docs/research/mission-1-command-audit.md)
has 166 verified, 53 partial, and 25 unimplemented scenarios.
Changing an existing macro action or description in place, CANCEL
override modes, older macro conversion, and the remaining nonmacro
gaps keep acceptance open. A clean release candidate and an
independent acceptance review are also still due. The accepted
preview was not replaced. The [older DOS converter prompt](../../docs/research/reference-runs/mission1-macro-converter/README.md) is captured; conversion awaits an original 4.x input and result.
