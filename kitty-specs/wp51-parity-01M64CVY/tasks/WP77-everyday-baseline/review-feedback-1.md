# WP77 independent review — REQUEST_CHANGES

Reviewer: `/root/everyday_baseline_audit`, independent of the WP77 implementer and inherited source author.
Issued review invocation: `979efd24c8ed4351a9747d6c63c958c7`.
Reviewed inherited delta: `f89a48627916b5cb9e360c35047350031b6f06a9..c7f14fd497da62bb577b6bdab7d4be3fb124e546` (all 23 paths).
Reviewed package: `e44fc41925e74e3a348b21579f86b611dff86fd7` (12 paths under `tests/baseline_adoption/`).
This verdict is against the issued current contract, especially T230/T233; no proposed planning amendment is applied retroactively.

## Blocking finding R77-001 (high): resizing bypasses active menu/browser input ownership

`internal/tui/model.go:203` calls `historicPress` only when `showEditorChrome()` is true. `internal/tui/chrome.go:46` makes that depend on height >= 12. Resize updates dimensions but retains the historic menu/browser state. At height 11, ordinary typing therefore reaches the document reducer despite the still-active modal state. Resizing back restores the menu/browser over a silently changed document. This is unintended document mutation, not merely incomplete historical presentation.

Reproduced independently through exported `tui.Open`, `Model.Update`, `Model.View`, `State` and `Session().Document().Export`; no private-field edits or source overlays. For both F5 List Files and Alt+= menus: type `a`, enter the mode, press `x` at normal height (native bytes conserved), resize to 80x11 and render, press `x` (native bytes change, gap becomes 2, mode Editing, empty notice), restore 80x25 (the same modal view returns). Full render/input guards are exercised.

Observed at the reviewed package HEAD:

```text
files normal-height text-mutated=false
files height11 text-mutated=true gap=2 mode=Editing notice=""
files restored view prefix="\x1b[22;37;41m11-05-26 06:33p   Directory /"
menu normal-height text-mutated=false
menu height11 text-mutated=true gap=2 mode=Editing notice=""
menu restored view prefix="\x1b[22;37;41mFile \x1b[22;34;47mEdit \x1b[22;34;"
```

Required correction: keep modal input ownership independent of available rendering height, or explicitly cancel the mode with truthful state/presentation before permitting document edits. Add public-entry regression coverage for both modes, crossing 12/11 and restoring, including native-byte conservation and small-height render safety. Update REPORT.md's claim that no authority bypass was established. The existing normal-size focus tests do not cover this boundary.

WP77 owns only `tests/baseline_adoption/**`; it must not silently modify TUI source. Resolve the ownership/gating conflict through a separately reviewed planning amendment or normal source-owner correction and rereview. The current T230/T233 contract requires unsafe findings corrected and independently reviewed before downstream approval, so merely adding a known-gap note cannot pass this review. A later explicit custody/audit-only contract may distinguish permission to continue implementation from candidate safety approval, but must retain this finding, its public reproducer, named repair owner and mandatory independently verified closure before product delivery.

## Verification and scope assessment

- Independently reran `go test ./tests/baseline_adoption -count=1 -v`: all four tests PASS, including compiled CLI PTY first save, normal exit and terminal restoration.
- Independently reran `python3 tests/baseline_adoption/custody.py`: PASS; prior identity/event retention and exact inherited path custody verified.
- Independently reran the public modal reproducer against current lane-z: finding reproduced for both modes.
- Inspected all new tests, PTY harness, custody checks, reports and reported build/test/vet records. No product source edits were introduced by WP77.
- Existing documented limits (retrieved editing, wrapping, status, history qualification, menus, search, proofreading) remain assigned future owners; they are not represented as new safety findings here.
- An earlier suspected tiny-height render panic was retracted: the complete public render guard prevents that path. It is not part of this rejection.

## Required anti-pattern checklist

| Check | Verdict | Basis |
|---|---|---|
| Dead code | PASS | WP77 adds only actual executable probes; inherited obsolete chrome routes are documented for WP85 removal, not claimed as delivered features. |
| Synthetic-fixture test | PASS | Go probes call exported production Model APIs; PTY probe runs compiled CLI and compares actual file bytes and termios. |
| Silent empty return | PASS | No new production paths in WP77; no additional silent failure identified in inherited audit beyond the explicit modal defect above. |
| FR coverage | FAIL | FR-004 / EE-001 menu input ownership and EE-013 conservation are violated by R77-001; current safety qualification is unsupported. Other frontmatter requirements retain bounded inherited checks, not full M1 acceptance. |
| Frozen surface | PASS | WP77 changes only its owned test/evidence directory. The candidate is a separately identified unreviewed input. |
| Locked decision | FAIL | T230/T233 prohibit unsafe candidate adoption before correction/rereview; R77-001 remains open. |
| Shared-file ownership | PASS | No shared product file edited; this feedback explicitly returns repair to reviewed TUI ownership rather than bypassing lane ownership. |
| Production fragility | PASS | No new exceptions/panics added by package; no additional fail-loud race issue established. |

## Self-contained public reproducer

Use a temporary module named `github.com/lynncoleart/wordling/pre_review`, require the main module, and `replace github.com/lynncoleart/wordling => /home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-z`; copy the checked-out dependency declarations. Run `GOTOOLCHAIN=local GOPROXY=off go run -mod=mod .`. Existing temporary runner: `/tmp/wordling-WP77-public-probe`.

```go
package main
import("fmt";"os";"bytes"; tea "charm.land/bubbletea/v2"; "github.com/lynncoleart/wordling/internal/tui")
func step(m tui.Model,msg tea.Msg) tui.Model {n,c:=m.Update(msg);if c!=nil {panic("unexpected I/O")};return n.(tui.Model)}
func key(m tui.Model,code rune,mod tea.KeyMod,text string)tui.Model{return step(m,tea.KeyPressMsg(tea.Key{Code:code,Mod:mod,Text:text}))}
func raw(m tui.Model)[]byte{b,e:=m.Session().Document().Export();if e!=nil{panic(e)};return b}
func main(){for _,kind:=range []string{"files","menu"}{root,e:=os.MkdirTemp("","wordling-public-audit-");if e!=nil{panic(e)};r,m,e:=tui.Open(tui.Config{Root:root,Profile:tui.LocalFlat,EditorChrome:true});if e!=nil{panic(e)};m=key(m,'a',0,"a");if kind=="files"{m=key(m,tea.KeyF5,0,"")}else{m=key(m,'=',tea.ModAlt,"=")};before:=raw(m);m=key(m,'x',0,"x");fmt.Printf("%s normal-height text-mutated=%v\n",kind,!bytes.Equal(before,raw(m)));m=step(m,tea.WindowSizeMsg{Width:80,Height:11});_=m.View();before=raw(m);m=key(m,'x',0,"x");fmt.Printf("%s height11 text-mutated=%v gap=%d mode=%s notice=%q\n",kind,!bytes.Equal(before,raw(m)),m.State().Session.Gap,m.State().Session.Mode,m.State().Notice);m=step(m,tea.WindowSizeMsg{Width:80,Height:25});fmt.Printf("%s restored view prefix=%q\n",kind,m.View().Content[:40]);r.Close();os.RemoveAll(root)}}

```
