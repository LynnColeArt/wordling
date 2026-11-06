# WP90 — Resize/modal input safety repair

R77-001 is reproduced before this change and repaired in the proposed source. Both F5 List Files and Alt+= menus formerly lost their input guard when terminal height fell below 12 rows, while their modal state stayed active. Ordinary text reached the native document behind the hidden modal. This is an unwanted-edit defect, not an accepted historical limitation.

This package changes only `internal/tui/model.go`, its new exported-surface regression file, and this evidence directory. It does not approve the rest of the inherited preview candidate, reinterpret the rejected WP77 review, update the user's preview, or claim everyday/M1 completion. Independent WP90 review is pending.

## Custody and preserved rejection

The issued H source is `426c1bf5f2e38b76ade38d232e1b5578e74702fd`. Candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546` is an ancestor, with parent `f89a48627916b5cb9e360c35047350031b6f06a9`. There are no inherited product-file differences between candidate and issued HEAD under internal/, cmd/, go.mod or go.sum. [source-custody.json](source-custody.json) records exact identities, input model hash, scoped paths and independent feedback hash.

The preserved WP77 rejection is event `01M6NV9Z0CPE615HWJBBJK38Q8`, finding R77-001, in `kitty-specs/wp51-parity-01M64CVY/tasks/WP77-everyday-baseline/review-feedback-1.md`. Its public reproduction and disproval of WP77's earlier no-bypass statement remain valid historical evidence. This repair does not alter those records. No code from the rejected WP77 package was imported, used as a hidden dependency or merged through a source overlay.

## Correction

The input route now uses the configured historic UI, independently of the minimum height needed to render its normal layout. When a menu or browser is active below that height, it retains input ownership. Ordinary text, navigation and invisible action keys cannot reach either the menu command or the document reducer. F1 can back out; Escape/F7 can leave the modal using its existing handlers. Enlarging restores the retained state.

A small-window modal view explicitly says `Menu active` or `List Files active`, followed by an enlarge/cancel instruction when there is room. It has no document caret. This is an explicit Linux terminal-size adaptation, not a claim about original DOS screens. Output is clipped to the available width/height, including one-row windows. Existing session/native ownership, UI generation checks, repeat/macro handling, pending I/O and normal-size rendering remain in their existing paths. Entering a modal at small size is also acknowledged and protected. Ordinary document editing remains usable after the user cancels.

The production diff (27 added lines and one removed line) serve only input ownership and its truthful small-window view. There is no second document model, fixture-specific behavior or blanket editing disable.

## Red/green evidence

`internal/tui/historic_resize_test.go` is an external `tui_test` package. It uses exported `Open`, `Update`, `View`, `State`, session snapshot/history and native export. No private-state edits or fabricated I/O completion messages are used.

- [red-model.log](red-model.log) and [red-model.json](red-model.json): before changing product source, the native-conservation assertion fails separately for files and menu at 11 rows. Both change `a` to `ax`, gap 1 to 2 and the native revision. The exact source/test hashes are recorded.
- [green-model.log](green-model.log): the unchanged safety test now passes. It covers 25→11→25, 12→11, 11→12, repeated crossings and 1/2-row render safety; native bytes, the entire session snapshot (including revision/dirty state) and history are compared. Text and navigation remain modal-only. Small-window entry, F1/Escape/F7 cancellation, stale UI rejection and resumed typing are checked for both modes. A real pending-save command remains pending through resize/menu attempts and completes without native change when its actual commands are executed.
- [cli_resize.py](cli_resize.py) is an independently authored black-box PTY probe of the actual compiled CLI. It opens each modal at 80×25, sends x, changes terminal size to 80×11 using TIOCSWINSZ/SIGWINCH, sends x, restores 25 rows, cancels the modal, saves and exits normally. It checks actual native body bytes, process exit, alternate-screen restoration and termios identity.
- [red-cli.json](red-cli.json): the pre-fix binary saves `BASEx` for both modes; the safety probe exits 1. [green-cli.json](green-cli.json): the repaired binary saves exact `BASE` for both modes; probe exits 0. Both include binary hashes, small/restored terminal output, native output hashes and normal terminal cleanup. The CLI proof uses xterm-256color/truecolor under a Linux PTY, not a claim of certification for every physical terminal.

The PTY probe uses displayed-state waits for visible transitions and short event-draining intervals for keys expected to produce no visible change. The public Model tests separately establish precise input ordering and state conservation. Only temporary, newly created documents are used. Test binaries are `/tmp/wordling-WP90-before` and `/tmp/wordling-WP90-after`; no installed preview binary changed.

## Checks and reproduction

From the issued checkout:

```sh
go test ./internal/tui -run '^TestHistoricResize' -count=1 -v
go build -o /tmp/wordling-WP90-after ./cmd/wordling
python3 internal/tui/evidence/resize-modal/cli_resize.py /tmp/wordling-WP90-after
go build ./...
go test ./...
go vet ./...
```

All Go gates passed; [checks.json](checks.json) records commands and exit codes with logs. Changed Go files are gofmt-clean, Python parses without generated artifacts, and git diff checking passes. The baseline's existing admitted native, lifecycle, async and macro suites remain part of the full run. Red/green regression demonstrates that the safety assertion detects the original defect; no separate artificial product mutation was necessary.

## Independent handoff

T294–T297 evidence is complete. T298 requests a different reviewer to inspect the narrow production diff, rerun public Model and actual CLI cases, and record the actual verdict. If approved, the orchestrator must prepare a reviewed ordinary repair-source intake and canonical source/planning refresh before WP77 retry. WP77 must re-audit all original candidate changes plus the approved repair, preserve unaffected candidate bytes, and verify R77-001 closure on its actual retry source. WP84 retains these regressions and WP86 reruns the integrated behavior. Only the exact approved repair delta may be admitted as an exception to equality with the earlier unsafe candidate.
