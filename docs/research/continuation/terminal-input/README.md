# WP16 input adapter and transport evidence

2026-10-30. Implements T046–T048 against Bubble Tea v2.1.1 and Ultraviolet
v0.0.0-20261008173134-6b8d4baf91b4, with unchanged go.mod/go.sum. This is a
bounded component milestone. No native file mutation, WP command execution,
physical terminal qualification or complete M1 parity is claimed.

The live `wordling-input-probe` command calls `input.Translate` from its Bubble
Tea Update method. Its recording deadline is a probe control, with no invented
keyboard quit/save/cancel bindings. The command requires terminal stdin/stdout
and a new output directory, refusing existing captures. The capture wrapper
retains term.File/Fd so Bubble Tea performs actual raw-mode setup/restoration;
wrapping input as an ordinary io.Reader would lose that terminal identity.
Raw read chunks, terminal output and decoded events share one ordered JSONL
journal, with monotonic offsets and sequence numbers. Raw/output values are
hexadecimal. Multiple chunks can become one event, or one chunk several events;
the sequence is not a one-to-one attribution between keys and chunks. The
recorder preserves chunk boundaries rather than normalizing them. A journal
write failure ends recording and is returned as an error. SIGTERM/host shutdown
before the deadline is an abnormal capture, distinct from original F7 exit.

Each profile record includes build/module identity, Linux architecture, selected
locale/terminal/session environment, terminfo dump/error, explicit operator
assertions, optional binary/config hashes, requested enhanced flags and the
pinned library's default ESC timeout. It does not dump the full environment or
configuration content. Request flags and actual capability responses are
separate records. `-enhanced=false` omits the extra requested flags; pinned Bubble
Tea may still negotiate its default basic disambiguation. No application timeout
or original-key remapping is introduced. The end record includes actual terminal
state equality and deadline/error status. Failed restoration is an error.

## Reproduce the actual checks

From this lane/source checkout (Linux with Python3, `infocmp`, and Go):

```sh
go test ./...
go test -race ./...
go build -o /tmp/wordling-input-probe-wp16 ./cmd/wordling-input-probe
python3 cmd/wordling-input-probe/pty_test.py /tmp/wordling-input-probe-wp16 /tmp/wp16-new-capture
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp16-validation.xml
go vet ./...
git diff --check
```

The Python driver opens a new Linux PTY for each run, injects published authored
byte sequences and controlled delays, sets80x25, then changes100x30 and sends
SIGWINCH. It records exact injected chunks and wire output. Assertions check:
all required initial function/navigation chord Code/Mod pairs; enhanced Ctrl
collision partners; actual synthetic capability response; repeat/release;
paste containing escape/control-looking text remaining paste; a specific unknown
CSI event; focus/mouse; actual resize; exact raw byte capture; restored termios;
existing-output and non-TTY refusal; and abnormal SIGTERM. The enhanced response
`CSI ?31u` is injected by the driver, not a real terminal claim. The legacy fast
ESC+5 test produces Alt+5 while150ms separation produces Escape then plain5.
The5ms split CSI remains F1, while150ms split legacy CSI becomes separate keys.
These measured timings exercise the pinned library's50ms default and are not
a physical timing guarantee or a Wordling-selected timeout.
The injected legacy Alt+F3 sequence also yields a CursorPositionMsg alongside
the key in this pinned decoder. The journal retains that extra event as Unknown;
the adapter does not discard it or infer a terminal capability from it. That
transport ambiguity reinforces the need for actual profile qualification.

`run-01/` and `run-02/` contain independent synthetic PTY repetitions and
per-run manifests with lengths/SHA-256 for all retained captures. The driver and
binary hashes are in each manifest; the journal build information identifies
the actual module pins. `source-manifest.json` pins all WP16 source inputs and
dependency source anchors used for these assertions. Verify the manifests with
the check script below. No proprietary WP media/manual/resource is included.

```sh
python3 docs/research/continuation/terminal-input/verify.py
```

Go tests separately exercise every typed event family and exact symbolic
tea.Key identities, all support combinations0–63 via actual Supports APIs,
unknown retention, paste isolation, no Escape aggregation or fallback shortcuts,
deadline controls, journal failure handling and concurrent journal ordering.
No extra codec or hand-written terminal sequence parser was introduced.

Executed validation: both independent synthetic PTY repetitions pass all driver
assertions. `go test ./...`, `go test -race ./...`, `go vet ./...`, Go build,
Python compilation, both catalogue checks, and the declared seven-check JUnit
gate all pass (seven passes, zero skips). `validation.xml` retains the actual
gate output. Diff-scoped gofmt check and `git diff --check` pass. The profile
resolver and action-scoped governance were loaded; Terminology Canon and Code
Review Checklist selectors report no authored section. These outcomes qualify
the bounded code/evidence handoff only.

## Physical qualification remains blocked

Every row below is **unqualified physical delivery**. A synthetic PTY is not a
terminal emulator, desktop, hardware keyboard or configured direct-user profile.
No terminal binary/version/configuration, US hardware layout, desktop shortcut
configuration or physical key operator is available to this execution session.
Empty optional identity inputs are recorded as `not supplied`, not support.
The driver assertion `synthetic-pty` and `physical_qualified:false` prevent a
capture being promoted into an accepted physical profile.

| Required physical test | Synthetic evidence | Missing input / next qualification action |
| --- | --- | --- |
| F1/F3/F7/F10 | Exact decoded Code with Mod0 in enhanced and legacy injections | Press each key in a recorded direct Linux terminal; match raw/event and observed WP session outcome. Canonical leads CMD51-001/005/048/065/066/087 retain their actual titles and scope; no inventory status is promoted. |
| Alt+F3, Shift+F10, Alt+= | ModAlt/ModShift distinct in both injected transports | Record desktop interception/configuration and exact physical chords, then compare original Reveal/Retrieve/math command context. No F13 alias is inferred. |
| Home/Right, modified variants | Home/Right exact basic transport values; typed adapter preserves all modifiers | Capture actual keys and modified combinations before session navigation qualification. WP token-gap semantics are outside WP16. |
| Escape5x, standalone Escape, rapid/slow Esc followed by text | Delayed and split injections expose actual decoder distinction | Record physical timing and negotiated profile. The adapter never reconstructs a guessed original Escape from Alt+5. Original Repeat Value remains a session decision. |
| Ctrl+I/Tab, Ctrl+M/Enter, Ctrl+[/Esc | Enhanced injected pairs differ; legacy HT/CR/ESC cannot establish which physical key generated them | Negotiate actual enhanced response and capture both members separately. Legacy indistinguishability stays unresolved. |
| Ctrl+Space/Ctrl+@, Backspace/Delete | Enhanced injected pairs distinct; legacy NUL aliases Ctrl+Space | Record actual terminal configuration and physical bytes, including BS/DEL behavior. No guessed lost modifier or native character identity. |
| Repeats/releases, paste, focus, mouse and resize | Actual synthetic PTY decode and resize plus typed tests | Physical hold/release/rates, paste/IME, window focus/mouse and reconnect remain unrun adaptations. Paste is never replayed as command chords. |
| Keyboard protocol and terminal identity | Injected31 response, build metadata, xterm-256color terminfo and default timeout recorded | Fingerprint actual emulator binary/version/config, keyboard/layout, locale and terminfo; record real request/reply and no SSH/multiplexer/remapper in first candidate. |

The direct candidate remains Linux local PTY, UTF-8, recorded US keyboard,
enhanced negotiation with captured response, initially80x25. Terminal brand or
TERM alone cannot qualify it. For a physical capture run the command directly
in that terminal, supply its actual identity inputs, press the matrix keys in a
declared order, preserve journals and adjudicate exact Code/Mod/session outcomes:

```sh
/tmp/wordling-input-probe-wp16 -output /tmp/wp16-physical-new -duration 90s -transport physical-direct -profile recorded-candidate -terminal-binary /absolute/path/to/emulator -terminal-version recorded-version -terminal-config /absolute/path/to/config -keyboard-layout US
```

The `physical-direct` flag is an operator assertion, never automatic
qualification. Keep SSH/multiplexer/desktop conflicts explicit. Adjusting and
recording terminal configuration can be tested; excluding original commands or
changing their bindings requires an owner decision and is not selected here.
No global q/Ctrl+Q/Ctrl+S/Escape shortcut or new command palette is provided.
Unqualified keys remain open M1 work, not silently removed requirements.
