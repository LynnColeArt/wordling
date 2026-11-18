# Wordling Windows input correction

Production Go sources from `github.com/charmbracelet/ultraviolet`
`v0.0.0-20261008173134-6b8d4baf91b4` (commit
`6b8d4baf91b4`), the version required by Bubble Tea v2.1.1. Original license,
module files and README are retained. Upstream tests/examples are omitted.

The sole upstream production change is in `terminal_reader_windows.go`:
VT input serialization skips zero-character modifier/lock KEY_EVENT records.
The previous serializer emitted their zero Char fields as NUL, inventing
Ctrl+Space before shifted text or modified commands. Native ConPTY traces
reproduced `\x00K\x00E\x00E\x00P` for typing `KEEP` from both PowerShell 7
and Windows PowerShell 5.1. Genuine Ctrl+Space/Ctrl+@ NUL input remains intact;
no raw input bytes or editor key meanings are rewritten.

`wordling_windows_test.go` covers native record serialization including real
NUL input, modifier transitions, key releases and Unicode. The packaged
`console-input-smoke.exe` runs it on Windows. The real Wordling ConPTY tests
provide end-to-end coverage. All other upstream production files are unchanged.
The candidate builder hashes these local compiled inputs and requires a clean
`third_party` tree. Remove this local replacement when an upstream version
provides an equivalent verified correction.
