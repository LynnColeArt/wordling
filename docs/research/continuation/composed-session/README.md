# WP18 bounded runnable no-edit session

T052–T054 deliver an actual pinned Go/Bubble Tea application, composing the
approved input, immutable document, editor reducer and rooted storage. This is
implemented executable behavior, not full M1 parity or physical terminal support.
Run from the lane with a chosen validated local directory:

```sh
go run ./cmd/wordling -root /absolute/local/directory -profile local-flat
```

The profile accepts flat ASCII basenames only, never DOS aliases. The display
identifies the read-only slice and unqualified physical delivery. Production
consumers, API/lifetime limits and exact commands are in internal/tui/README.md.
The command directly calls tui.Open and tea.NewProgram; Update calls actual
input.Translate, editor.Session.Reduce and document presentations. Returned tea.Cmd
closures execute actual Directory.Read/Observe/Save; no replacement model/codec,
view serialization, semantic writer or fake completed-operation stub exists.

## Results and evidence levels

- `tests.txt`: actual composed-model tests, including exact source fixture
  fingerprints, all five original native fixtures through real temporary-file
  retrieve/new-name Save, and macro native-type refusal. Successful source,
  document export and published output retain identical bytes/length/SHA. Opaque
  originals may refuse projection while their complete snapshots remain saved
  losslessly. Export mutation cannot change internal data.
- Exact independently produced WP13 repeated captures supply selected original
  prompt/Reveal/status fragments and shared semantic cursor assertions. The
  composed test verifies the actual raw screen SHA before comparing each cue.
  Right across Bold changes gap1→2 with stationary normal text X; Reveal exposes
  `A[BOLD]BC[bold]D`. Save/Exit default text and unmodified indicator match original
  cues. Original DOS exit is a domain exit witness, never an invented Linux DOS
  prompt. Both original witnesses stay raw and unchanged.
- `original-audit.txt` reruns the approved22-association/78-state witness audit,
  plus four earlier Reveal witnesses and three rejecting semantic substitutions.
  This validates existing source bindings; it does not execute the oracle again.
  Main selected comparisons are CMD51-049 and CMD51-244; bounded retrieve/save,
  refusal, filename/cancel and no-edit safety also trace CMD51-065/067/069/070/149
  and237–243 through the inherited reducer evidence. No canonical verified label
  is changed. New document naming066 remains unsupported writer scope.
- `run-01/` and `run-02/` execute the actual first compiled binary through two
  synthetic Linux PTYs. `run-03-final/` and `run-04-final/` repeat against the final
  source binary after a diagnostic wording improvement. Each has exact injected
  raw bytes, raw terminal output, stderr, binary SHA/length, actual before/after
  native hashes, exit status, and actual termios restoration. No terminal-output
  normalization or byte mask is applied. Raw terminal output can vary across
  runs because of rendering timing; it is retained, not claimed identical.
- The PTY workflow retrieves ORIGIN, toggles Reveal, traverses ASCII/Bold, rejects
  unknown CSI/paste/release/q/CtrlQ/CtrlS as commands, resizes, executes explicit
  same-file no-op, refuses replacement of another identical-but-distinct inode,
  declines it, publishes COPY byte-identically, retains via F1 at both exit
  questions, and exits with F7/n/y. A separate actual SIGTERM run restores
  termios and returns abnormal status1 with host-interruption text; non-TTY launch
  refuses. Signals are host control, not original keyboard exit acceptance.
- `go-run-smoke.txt` records an actual terminal launch via go run, then F7/n/y
  and exit0. It is an execution transcript summary, not a physical-key witness.
- `race-tests.txt`: real full-lane race tests pass, including concurrent started
  reads/Close and queued-after-Close refusal before descriptor access. Model tests
  cover stale operation/revision/kind, copied states, cancel while IO pending,
  actual late publication, source mutation before Save, failed/uncertain cleanup
  receipt and no false exit/save. Receipt failures injected at the result boundary
  do not claim new lower-level filesystem fault injection; approved storage tests
  exercise those faults. No running original VM was used.
- `mutation-results.json`: four compiling Go-overlay mutants are killed by
  meaningful assertions: altered command modifier, suppressed detached-publication
  reconciliation, suppressed cleanup uncertainty, and removed actual Save call.
  Source is never mutated by the harness. `test-first.txt` records the actual
  initial undefined-API test failure; later tests developed incrementally.
- `validation.txt/xml`: all seven declared checks pass, including actual Go
  package discovery/build/test/vet and both catalogue validators, with no skips.
  gofmt emits no changed file; diff whitespace checks pass. Python sources compile.

Raw failed uppercase-text calibration is retained in attempt-uppercase-before-fix/
and explained in attempts.md. The final resolver accepts delivered Shift/CapsLock
ASCII Text only in filename/letter-answer contexts; it keeps exact modifiers for
original commands. No generic shortcuts or speculative remapping were added.

## Boundaries retained

Physical keyboard/emulator/config/layout/operator delivery and physical-to-paint
measurements remain **unqualified**. The enhanced capability response is injected
by the synthetic harness; it proves neither terminal negotiation nor physical
support. Original baseline is plain U.S. English WP5.1 Help03/09/92 under declared
QEMU/FreeDOS1.4 and mixed-date text Standard Printer limits, not historical DOS.
No original/native fixture was regenerated or silently normalized here.

Comparison is selected exact prompt/status text, shared token/cursor state and
native byte safety. DOS screen rows/spacing, Pos inches, printed layout/page metrics,
all original screens/menus, dirty semantic edits, typeover/delete/history/new native
writer, actual replacement/backup/Fast Save, resources and PDF remain unimplemented
or separately gated. This package does not close any full parent feature, FR,
NFR005 or M1 acceptance. WP24 candidate publication is inherited and approved,
but this WP calls only the original no-edit Save API; edited composition is WP28.

## Reproduction

```sh
go test ./internal/tui -v -count=1
go test -race ./... -count=1
python3 docs/research/continuation/composed-session/mutations.py
go build -o /tmp/wp18-wordling ./cmd/wordling
python3 docs/research/continuation/composed-session/pty_test.py /tmp/wp18-wordling /tmp/wp18-new-pty
python3 docs/research/continuation/composed-session/verify.py
python3 scripts/review_checks.py --junitxml /tmp/wp18-validation.xml
```

Use a new output directory. Source-manifest seals owned artifacts and current
source/module/dependency hashes; primary planning/review snapshots are recorded
as historical hashes, not claims that mutable runtime metadata never changes.
Proprietary binaries/resources remain external; only previously lawful project
scratch native fixtures are copied into public PTY evidence. Diagnostic files
are optional research output, never product-native wrappers or required sidecars.
