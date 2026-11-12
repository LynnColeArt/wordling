# WP52 active Reveal token/cell handoff

`Model.View → panes → renderReveal` is the live production path. The existing
Session.Present supplies immutable native token indices/spans and cursor gap.
ASCII selects one cell; native BoldOn/Off selects its entire six-character label;
literal bracket text remains separate ASCII tokens. A blank is emitted only at
actual TokenCount EOF, never the4096-window end when more tokens exist. The upper
caret keeps its existing normal-text width/row1. No domain, native, source, IO,
history, permission, macro engine or command source changed.

The selected original VGA profile uses17 normal white/blue,1F bright white/blue,
47 normal white/red. Explicit ANSI22/37/44,22/97/44,22/37/41 roles preserve that
logical distinction; this is not reverse video or physical palette/RGB/raster
qualification. Runs intersect visible cells before emitting SGR. Both horizontal
clipping edges and final line clipping reset styles. Block and HistoryPreview
have virtual elements without file spans and retain markers without newly claimed
active-token styling. DISPLAY OFF freezes the actual styled pane and caret;
resize/observation cannot mix a newer gap into that captured stream.

## Actual authority and source composition

Claim8d925243 included approved48H54763f71 and a moving E research-only tip.
`wordling-WP52-claim-source-proof.json.txt` records32 actual production Go inputs
and nine local packages exactly equal to approved48. The two added unreviewed51
research-probe Go paths are not imported by the app; they are not WP52 authority,
native permission or approved51 results. Broad `go test ./...` incidentally runs
that package; a pass does not approve51. No dependency overlay/removal occurred.
The production change is only model.go plus reveal.go; original_test.go now strips
ANSI for its pre-existing text-only assertion. New attribute assertions inspect
actual styles rather than stripping them.

`recon/` preserves the exact inert reconnaissance and its original seals.
`original_audit.py` recomputes211 historical source/artifact pins from Git,
28 selected original13 captures (7 gaps×2 modes×2fresh runs), all six artifacts
per capture, runner/environment/native provenance and raw VGA/CRTC facts.
`TestRevealBothOriginalAttributeAndNativeSpanWitnesses` joins those facts to real
rooted Retrieve/public Model and native324..334 spans. Original upper/lower rows
are0/13; Wordling rows remain1/3. This is selected stream/style/caret parity,
not whole-screen geometry, ruler/status layout, scrolling or printer metrics.

## Real executable and diagnostics

`pty-07/` is two fresh actual production executable processes,15 captured states
per process: all seven Right gaps, six Left returns, Reveal off/on; actual F10
no-edit absent-name publication and original exit keys. Both outputs are exact
334B native c6cffde2…; no display marker/style enters native bytes. Raw wire,
keys, process argv, child color environment, termios restoration, full decoded
cell/styles/cursor witnesses and transport/observer source archives are retained.
Both original runs' raw13th-row roles/text and upper caret columns are compared.
`audit.py` replays each raw-wire prefix through the bounded decoder and repeats
those joins; this is not a renderer-helper-only or copied-output proof.

The EXECUTED binary is `build/wordling.bin`, SHA7e6e5d27f427cb66f344a0ede2fa547e862afcc1fefa0e00ca91a1563458e9e0.
A corroborating final build is d23bc69837e2c6a173f2d2edb66d1a5d8d76dffac0f7a8cbedfe1429e07f19a9.
Complete35 compiled local/module path SET/SHA are identical. Build receipts bind
actual cwd/GOMOD/packageDirs/GoFiles/GOFLAGS/GOWORK/dependency versions and binaries.
The final complete local Go SET118 also binds final tests. Both raw buildinfos
show the known automatic worktree VCS stamp from unrelated primary tips883b/6324
and misleading modified=false; neither stamp is compiled-source authority. Binary
reproducibility is explicitly NOT claimed. The executed producer has the exact
same compiled source closure as the final implementation; no source-identical PTY
rerun was used just to improve metadata. No Cgo/Embed/extra local compiler inputs
or GOFLAGS/GOWORK injection exists in the captured production closure.

`diagnostic-attempts.json` retains the preceding observer failures honestly:
one prelaunch import failure/zero processes, six incomplete synthetic processes,
then the two passing processes. The first three decoder exceptions rethrew in
inherited cleanup after stopping the child, so their raw wire/exit receipts were
not persisted; only archived producer and exception logs survive. No such missing
receipt is backfilled or called success. Later diagnostics retain raw argv/wire,
exit1 and restored termios. One retained NO_COLOR=1 attempt correctly lost colors
through BubbleTea policy; the qualified child profile explicitly removes NO_COLOR
and declares xterm-256color/COLORTERM=truecolor. These are synthetic Linux PTYs,
not original guests or physical keyboard/palette claims. Observer fixes handle
actual private keyboard/query controls, DECST8C (pinned x/ansi screen.go locator),
line insertion/deletion and empty SGR reset. Four offline decoder tests falsify
styles/reset/erasure/unknown-control handling. No product source changed during
these diagnostic attempts; all use the same executed binary.

## Validation and bounds

Final genuine `review_checks.py`: seven applicable checks PASS,0skip (inventory,
scenarios, adapter, actual package discovery/build/test/vet). Final affected TUI
race run:182 passing test/subtest/seed nodes,0skip. Initial standalone full-tree
JSON retains1626 passes and8 honest package-level no-test-file skips; final
configured full-tree run includes the subsequently added clipping-role test.
The compiled cmd has actual PTY coverage rather than a fictitious unit-test pass.
Six compiling production mutants are killed by real public Model tests: one-cell
Bold, first text match/literal/duplicates, lower-width upper caret, window-end EOF,
lost clipped role and omitted reset. Exact production source is restored and the
full Reveal tests pass afterward. No parser fuzz budget is rerun for this display
change. Existing macro/history/pending/first-bind/source guards run in the real
suite; the explicit frozen-pane test is labelled a test seam, not new original
macro evidence. Gofmt and diff-scoped whitespace lint are clean.

Maximum requested presentation4096 tokens, viewport4096×4096, one-row existing
streams: measured ASCII679155B/op60allocs and458169ns/op; code-window803147B/op
66allocs and326661ns/op on the recorded Ryzen5600X/Linux host. These are measured
View allocations/timing, not total document parse costs, hard resource guarantees,
historical DOS capacities or physical terminal latency. Work remains bounded by
the existing requested4096-token window and visible intersections; no full-file
scan/new pagination/scroll model was introduced. Tests cover widths1/2/3/5/6/7/80/
4096, tiny/capped heights, both clipping edges, genuine maximum-window EOF,
off-window refusal, Opaque refusal, literal/adjacent/empty/repeated codes, stale
Models, copied/replaced exported wrappers, virtual overlays, frozen panes and
actual no-edit publication.

Reproduce offline with `python internal/tui/evidence/wp52/original_audit.py`,
`python internal/tui/evidence/wp52/audit.py --git`, `python -m unittest discover
-s internal/tui/evidence/wp52 -p test_observer.py`, and genuine configured checks.
PTY/mutant/build scripts create fresh evidence directories; existing attempts are
immutable and must not be overwritten. No original VM was used or authorized.
All38 obligations/91groups/36lessons/nested/full M1 remain open. Full catalogue,
custom styles, native layout/resources, screen geometry/scroll/window settings,
unknown format support and physical delivery are not closed by this slice.

The final audit found that the initial observer's optional full `styles` matrix
in each PTY receipt retained a live list reference and was retargeted by later
screen writes. Those old fields and their raw receipts are preserved unchanged
and excluded from accepted assertions. Copied per-state roles/text/cursor/wire
offsets were unaffected. `seal_replay.py` independently replays each ALREADY
captured raw prefix and immediately serializes frozen values into raw-replay.json;
it first requires exact equality to all those copied per-state facts. `audit.py`
recomputes the immutable matrices and compares them and both original VGA runs.
This append-only correction is offline recovery of complete existing wire, not a
new application/original run or backfilled missing diagnostic wire. The failed
initial matrix-equality audit is retained under checks/.
The fifth offline observer test reproduces the old matrix mismatch on actual raw
prefixes (RED) and proves immediately deep-copied replay matrices stay unchanged
after all later wire is consumed (GREEN). Replay refuses incomplete escape/end
state; the exact Alt-F3/Right/Left/off/on input sequence, recorded argv/binary,
receipt SHA, wire offsets and corresponding displayed gap are checked.
