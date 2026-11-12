package tui

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/storage"
)

const newABC = "docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM"

func newMacroModel(t *testing.T, source string) (*Runtime, Model, string, []byte) {
	t.Helper()
	r, m, root := newModel(t)
	raw, err := os.ReadFile("../../" + source)
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	return r, m, root, raw
}

// All positive entry/work/IO uses public Open/Update/Cmd, never a sink call or
// injected Session. Retaining the real reached driver is supplemental immutable
// receipt inspection: State/CompletedMacros separately assert public outcomes.
func drainNewMacro(t *testing.T, m Model, c tea.Cmd) (Model, *editor.MacroExecution) {
	t.Helper()
	var driver *editor.MacroExecution
	if m.macro != nil {
		driver = m.macro.driver
	}
	for events := 0; c != nil; events++ {
		if events >= 4096 {
			t.Fatal("Model event bound")
		}
		n, next := m.Update(c())
		m = n.(Model)
		c = next
		if m.macro != nil && m.macro.driver != nil {
			driver = m.macro.driver
		}
	}
	return m, driver
}
func observeNewMacro(t *testing.T, label string, r *Runtime, m Model) {
	t.Helper()
	if dir := os.Getenv("WORDLING_WP66_MODEL"); dir != "" {
		if err := os.MkdirAll(dir, 0700); err != nil {
			t.Fatal(err)
		}
		raw, _ := m.Session().Document().Export()
		row := struct {
			Label     string
			State     State
			View      string
			NativeSHA [32]byte
			IO        []editor.Result
			Macros    []MacroOutcome
		}{label, m.State(), m.View().Content, sha256.Sum256(raw), r.Completed(), r.CompletedMacros()}
		b, err := json.MarshalIndent(row, "", "  ")
		if err != nil {
			t.Fatal(err)
		}
		name := strings.ReplaceAll(t.Name(), "/", "_") + "-" + label + ".json"
		if err = os.WriteFile(filepath.Join(dir, name), b, 0600); err != nil {
			t.Fatal(err)
		}
	}
}
func TestNewMacroPublicFLOWMenuAndFirstSave(t *testing.T) {
	for _, sample := range []string{"03", "04"} {
		t.Run(sample, func(t *testing.T) {
			source := "docs/research/reference-runs/2026-10-29-advanced-" + sample + "/CMD51-205/"
			r, m, root, input := newMacroModel(t, source+"FLOW.WPM")
			before := m.Session().Snapshot()
			birth := m.Session().Document().Birth()
			history := m.Session().History().Revision()
			observeNewMacro(t, "initial", r, m)
			// The display-only shown bar refuses real Macro before G and disk IO.
			m = menuStep(t, m, menuToggle())
			shown := m.Session().Snapshot()
			m, c := press(m, tea.KeyF10, tea.ModAlt, "")
			if c != nil || !m.State().MenuBar.Visible || !reflect.DeepEqual(shown, m.Session().Snapshot()) || len(r.Completed()) != 0 {
				t.Fatal("shown menu dispatched Macro", m.State())
			}
			m = menuStep(t, m, menuToggle())
			if m.State().MenuBar.Visible || m.State().Notice != "" || m.Session().History().Revision() != history {
				t.Fatal("hide changed editor/notice/history")
			}
			m, c = press(m, tea.KeyF10, tea.ModAlt, "")
			if c != nil || m.Session().Snapshot().Mode != editor.MacroName {
				t.Fatal("actual New AltF10 did not enter", m.State())
			}
			observeNewMacro(t, "name", r, m)
			m = key(t, m, 'R', 0, "ROOT")
			m, c = press(m, tea.KeyEnter, 0, "")
			if c == nil || m.State().PendingIO != 1 || m.Session().Snapshot().Pending.Kind != editor.ReadMacro {
				t.Fatal("root wait", m.State())
			}
			observeNewMacro(t, "root-wait", r, m)
			n, start := m.Update(c())
			m = n.(Model)
			if start == nil || m.Session().Snapshot().Mode != editor.MacroReady || m.State().PendingIO != 0 || m.Session().Source() != nil || m.Session().Document().Revision() != before.NativeRevision {
				t.Fatal("root ready", m.State())
			}
			observeNewMacro(t, "start-queued", r, m)
			*m.Session().MacroSource() = storage.Macro{}
			*m.Session().MacroSource().Image() = wpm.Image{}
			*m.Session().Document() = document.Document{}
			m, driver := drainNewMacro(t, m, start)
			if driver == nil {
				t.Fatal("live caller never reached real G driver")
			}
			s := m.Session().Snapshot()
			p := driver.Snapshot()
			public := r.CompletedMacros()
			observeNewMacro(t, "terminal", r, m)
			if s.NewPhase != editor.NewUnpublished || s.Name != "" || m.Session().Source() != nil || !s.Dirty || s.GenesisRevision != before.GenesisRevision || m.Session().Document().Birth() != birth || s.Revision != 14 || s.Gap != 13 || !s.HistoryQualified || !s.HistoryCountKnown || s.HistoryCount != 0 || m.State().PendingIO != 0 || m.State().Macro.Active || m.State().Macro.DisplaySuppressed || m.State().Macro.State != "complete" || m.State().Macro.AppliedWords != 13 || len(public) != 1 || public[0].AppliedWords != 13 || public[0].Source != sha256.Sum256(input) || public[0].Steps != p.TotalSteps || public[0].Words != p.TotalWords || p.TotalSteps == 0 || m.State().Macro.Steps != p.TotalSteps || m.State().Macro.Words != p.TotalWords || p.Completed != 1 || p.Repeat != 1 || p.ReceiptCount != 14 {
				t.Fatalf("terminal public/live invariants %+v %+v", m.State(), p)
			}
			raw, _ := m.Session().Document().Export()
			if len(raw) != 337 || string(raw[324:]) != "TRUEFALSETAIL" || !strings.Contains(m.View().Content, "TRUEFALSETAIL") {
				t.Fatal("actual New output", m.View().Content)
			}
			receipts, err := driver.Receipts(0, 14)
			if err != nil {
				t.Fatal(err)
			}
			for _, receipt := range receipts {
				if !receipt.Applied || !receipt.Result.MayHaveEffects || receipt.Err != nil || receipt.Effect.Source != sha256.Sum256(input) || len(receipt.Effect.Words) != 1 {
					t.Fatal(receipt)
				}
				w := receipt.Effect.Words[0]
				at := int(w.Span.Offset)
				if at < 75 || w.Span.Length != 2 || at+2 > len(input) || (at-75)%2 != 0 || binary.LittleEndian.Uint16(input[at:]) != w.Value {
					t.Fatal("actual source word/span", receipt)
				}
				if receipt.Effect.Kind == "display-off" {
					if receipt.Before != receipt.After || receipt.BeforeGap != receipt.AfterGap {
						t.Fatal(receipt)
					}
				} else if receipt.After != receipt.Before+1 || receipt.AfterGap != receipt.BeforeGap+1 {
					t.Fatal(receipt)
				}
			}
			for _, original := range []string{"03", "04"} {
				want, err := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-" + original + "/CMD51-205/FLOWOUT.WP5")
				if err != nil {
					t.Fatal(err)
				}
				macroNative(t, raw, want)
			}
			if got, err := os.ReadFile(filepath.Join(root, "ROOT.WPM")); err != nil || !bytes.Equal(got, input) {
				t.Fatal("macro source changed")
			}
			m, publish := firstSave(t, m, "FIRST")
			currentHistory := m.Session().History().Revision()
			observeNewMacro(t, "publish-wait", r, m)
			n, bind := m.Update(publish())
			m = n.(Model)
			if bind == nil || m.Session().Snapshot().NewPhase != editor.AwaitFirstRead || m.Session().Source() != nil || m.Session().Snapshot().Name != "" || !m.Session().Snapshot().Dirty {
				t.Fatal("publication falsely saved", m.State())
			}
			observeNewMacro(t, "first-read", r, m)
			m = drain(m, bind)
			observeNewMacro(t, "anchored", r, m)
			exactNew(t, m, birth, s.NativeRevision)
			actual, err := os.ReadFile(filepath.Join(root, "FIRST"))
			if err != nil || !bytes.Equal(raw, actual) || m.Session().Snapshot().NewPhase != editor.NewAnchored || m.Session().Snapshot().Dirty || m.Session().Snapshot().Name != "FIRST" || m.Session().Snapshot().GenesisRevision != before.GenesisRevision || m.Session().History().Revision() == currentHistory || m.State().PendingIO != 0 {
				t.Fatal("real first save/readback", err, m.State())
			}
			m, c = press(m, tea.KeyF10, tea.ModAlt, "")
			if c != nil || m.Session().Snapshot().Mode != editor.Editing {
				t.Fatal("anchored regained pristine Macro")
			}
		})
	}
}
func TestNewMacroRefusesAuthenticHostNoticeBeforeG(t *testing.T) {
	_, m, _, _ := newMacroModel(t, newABC)
	n, c := m.Update(struct{}{})
	m = n.(Model)
	if c != nil || m.State().Notice == "" {
		t.Fatal("Unknown did not create authentic notice")
	}
	before := m.Session().Snapshot()
	notice := m.State().Notice
	m, c = press(m, tea.KeyF10, tea.ModAlt, "")
	if c != nil || !reflect.DeepEqual(before, m.Session().Snapshot()) || m.Session().Snapshot().Mode != editor.Editing || m.State().Notice != notice {
		t.Fatalf("host notice erased to enter New macro: prior %q state %+v", notice, m.State())
	}
}
func TestNewMacroThirdRootCurrentTicketsAndDuplicateWork(t *testing.T) {
	r, m, root, input := newMacroModel(t, newABC)
	base := m
	m, read := queuedMacro(t, m, "ROOT")
	actual := read()
	duplicate := read()
	if len(r.Completed()) != 1 {
		t.Fatal("root executed twice")
	}
	n, c := m.Update(duplicate)
	m = n.(Model)
	if c != nil || m.State().PendingIO != 1 {
		t.Fatal("duplicate settled current read")
	}
	stale, _ := base.Update(actual)
	if stale.(Model).State().Session.Mode != editor.Editing {
		t.Fatal("stale fork consumed actual receipt")
	}
	n, start := m.Update(actual)
	m = n.(Model)
	if start == nil {
		t.Fatal("authentic root lost")
	}
	reply := start()
	dup := start()
	n, c = m.Update(dup)
	m = n.(Model)
	if c != nil {
		t.Fatal("duplicate worker dispatched")
	}
	n, c = m.Update(reply)
	m = n.(Model)
	m, driver := drainNewMacro(t, m, c)
	if driver == nil || driver.Snapshot().AppliedWords != 3 || m.State().Macro.AppliedWords != 3 || m.State().Macro.Source != sha256.Sum256(input) || !strings.Contains(m.View().Content, "ABC") || strings.Contains(m.View().Content, "TRUEFALSETAIL") || len(r.CompletedMacros()) != 1 {
		t.Fatal("distinct real source/current driver", m.State())
	}
	data, _ := m.Session().Document().Export()
	if string(data[324:]) != "ABC" {
		t.Fatal("distinct native")
	}
	after, _ := os.ReadFile(filepath.Join(root, "ROOT.WPM"))
	if !bytes.Equal(after, input) {
		t.Fatal("changed source")
	}
}

func newDerivedMacroModel(t *testing.T, parts ...any) (*Runtime, Model, string) {
	t.Helper()
	r, m, root := newModel(t)
	base, err := os.ReadFile("../../" + newABC)
	if err != nil {
		t.Fatal(err)
	}
	raw := append([]byte(nil), base[:70]...)
	word := func(w uint16) { raw = append(raw, byte(w), byte(w>>8)) }
	for _, part := range parts {
		switch v := part.(type) {
		case string:
			for _, c := range []byte(v) {
				word(uint16(c))
			}
		case uint16:
			word(v)
		default:
			t.Fatal("bounded host source type")
		}
	}
	word(0)
	if err = os.WriteFile(filepath.Join(root, "ROOT.WPM"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	return r, m, root
}
func TestNewMacroFrozenDisplayManualRefusalsResizeAndHostStop(t *testing.T) {
	for _, stop := range []bool{false, true} {
		t.Run(fmt.Sprint(stop), func(t *testing.T) {
			r, m, _ := newDerivedMacroModel(t, uint16(0xfc0c), strings.Repeat("Q", 160))
			m, c := queuedMacro(t, m, "ROOT")
			var driver *editor.MacroExecution
			reached := false
			for turn := 0; c != nil && turn < 4096; turn++ {
				n, next := m.Update(c())
				m = n.(Model)
				c = next
				if m.macro != nil {
					driver = m.macro.driver
				}
				if m.State().Macro.Active && m.State().Macro.DisplaySuppressed && m.State().Macro.AppliedWords > 0 {
					reached = true
					break
				}
			}
			if !reached || c == nil || driver == nil {
				t.Fatal("no actual nonterminal DISPLAY slice", m.State())
			}
			before := m.Session().Snapshot()
			frame := m.visibleFrame()
			inspection := m.State().RevealInspection
			if strings.Contains(strings.Split(m.View().Content, "\n")[1], "Q") || m.State().MenuBar.Available {
				t.Fatal("live normal/menu leaked under DISPLAY OFF")
			}
			for _, k := range []tea.KeyPressMsg{{Code: tea.KeyF10}, {Code: tea.KeyF10, Mod: tea.ModShift}, {Code: tea.KeyF3, Mod: tea.ModAlt}, {Code: tea.KeyF3, Mod: tea.ModShift}, {Code: tea.KeyEscape}, {Code: tea.KeyF1}, {Code: 'X', Text: "X"}, {Code: '=', Mod: tea.ModAlt}} {
				n, extra := m.Update(k)
				m = n.(Model)
				if extra != nil || m.Session().Snapshot().NativeRevision != before.NativeRevision || m.Session().Snapshot().Gap != before.Gap || m.State().PendingIO != 0 || !m.State().Macro.Active || !reflect.DeepEqual(m.visibleFrame(), frame) || !reflect.DeepEqual(m.State().RevealInspection, inspection) {
					t.Fatal("manual/frozen ownership", k, m.State())
				}
			}
			for _, size := range []tea.WindowSizeMsg{{Width: 40, Height: 12}, {Width: 0, Height: -2}, {Width: 5000, Height: 5000}, {Width: 80, Height: 25}} {
				n, extra := m.Update(size)
				m = n.(Model)
				if extra != nil || m.State().Width != max(1, min(size.Width, 4096)) || m.Session().Snapshot().NativeRevision != before.NativeRevision || !reflect.DeepEqual(m.visibleFrame(), frame) {
					t.Fatal("resize native/frozen mutation")
				}
			}
			observeNewMacro(t, "active-frozen", r, m)
			if stop {
				n, extra := m.Update(HostStopMacroMsg{Reason: "bounded New containment"})
				m = n.(Model)
				if extra != nil {
					t.Fatal("queued CPU stop double dispatched")
				}
			}
			m, _ = drainNewMacro(t, m, c)
			p := driver.Snapshot()
			if m.State().Macro.DisplaySuppressed || m.State().Macro.Active || m.State().PendingIO != 0 || !p.Terminal || m.Session().Source() != nil || !m.Session().Snapshot().Dirty {
				t.Fatal("terminal containment/frozen leak", m.State())
			}
			if stop {
				if p.State != "stopped" || p.AppliedWords != before.Revision-1 || m.Session().Snapshot().NativeRevision != before.NativeRevision {
					t.Fatal("host stop changed accepted partial effects", p)
				}
			} else if p.State != "complete" || p.AppliedWords != 160 || !strings.Contains(m.View().Content, "QQQ") {
				t.Fatal("final actual text", m.State())
			}
		})
	}
}
func TestNewMacroPublicExclusionsAndRecovery(t *testing.T) {
	for _, context := range []string{"typed", "edited-empty", "typeover", "reveal", "block", "home", "name-cancel", "missing", "root-cancel", "repeat", "unknown", "closed"} {
		t.Run(context, func(t *testing.T) {
			r, m, _, _ := newMacroModel(t, newABC)
			switch context {
			case "typed":
				m = key(t, m, 'A', 0, "A")
			case "edited-empty":
				m = key(t, m, 'A', 0, "A")
				m = key(t, m, tea.KeyLeft, 0, "")
				m = key(t, m, tea.KeyDelete, 0, "")
				if m.Session().Document().TokenCount() != 0 {
					t.Fatal("edited-empty precondition")
				}
			case "typeover":
				m = key(t, m, tea.KeyInsert, 0, "")
			case "reveal":
				m = key(t, m, tea.KeyF3, tea.ModAlt, "")
			case "block":
				m = key(t, m, tea.KeyF3, tea.ModAlt, "")
				m = key(t, m, tea.KeyF4, tea.ModAlt, "")
			case "home":
				m = key(t, m, tea.KeyHome, 0, "")
			case "name-cancel":
				m = key(t, m, tea.KeyF10, tea.ModAlt, "")
				m = key(t, m, tea.KeyF1, 0, "")
			case "missing":
				var c tea.Cmd
				m, c = queuedMacro(t, m, "MISSING")
				m, _ = drainNewMacro(t, m, c)
				if m.Session().Snapshot().Mode != editor.MacroError {
					t.Fatal(m.State())
				}
				m = key(t, m, tea.KeyF1, 0, "")
			case "root-cancel":
				var c tea.Cmd
				m, c = queuedMacro(t, m, "ROOT")
				reply := c()
				n, extra := m.Update(CancelPendingMsg{})
				m = n.(Model)
				if extra != nil {
					t.Fatal("cancel issued IO")
				}
				m, _ = drainNewMacro(t, m, func() tea.Msg { return reply })
				m = key(t, m, tea.KeyF1, 0, "")
			case "repeat":
				m = key(t, m, tea.KeyEscape, 0, "")
			case "unknown":
				n, _ := m.Update(struct{}{})
				m = n.(Model)
			case "closed":
				if err := r.Close(); err != nil {
					t.Fatal(err)
				}
			}
			before := m.Session().Snapshot()
			raw, _ := m.Session().Document().Export()
			count := len(r.Completed())
			next, c := press(m, tea.KeyF10, tea.ModAlt, "")
			after, _ := next.Session().Document().Export()
			if c != nil || next.Session().Snapshot().Mode == editor.MacroName || !bytes.Equal(raw, after) || next.Session().Snapshot().NativeRevision != before.NativeRevision || len(r.Completed()) != count {
				t.Fatal("nonpristine New admitted", next.State())
			}
		})
	}
}
func TestNewMacroHostOrchestrationStructuralExclusions(t *testing.T) {
	// These deliberately inconsistent private combinations supplement the public
	// lifecycle cases; none is used to manufacture a positive Session or receipt.
	for _, field := range []string{"issued", "results", "executed", "first-history", "macro-history", "ticket", "cpu", "frozen", "deferred", "terminal-status"} {
		t.Run(field, func(t *testing.T) {
			r, m, _, _ := newMacroModel(t, newABC)
			switch field {
			case "issued":
				r.issued = 1
			case "results":
				r.results = []editor.Result{{}}
			case "executed":
				r.executed[operation{1, 1, editor.ReadMacro}] = true
			case "first-history":
				r.firstTickets[editor.RequestKey{}] = &firstTicket{}
			case "macro-history":
				r.macroResults = []MacroOutcome{{Terminal: true}}
			case "ticket":
				m.macroTicket = &macroTicket{}
			case "cpu":
				m.macroCPU = true
			case "frozen":
				m.macroFrozen = &macroPane{}
			case "deferred":
				m.macroDeferred = &macroIOReceipt{}
			case "terminal-status":
				m.macroStatus.Terminal = true
			}
			before := m.Session().Snapshot()
			m, c := press(m, tea.KeyF10, tea.ModAlt, "")
			if c != nil || !reflect.DeepEqual(m.Session().Snapshot(), before) {
				t.Fatal("host orchestration manufactured pristine entry", m.State())
			}
		})
	}
}
func TestNewMacroNestPartialHostFailureAndStaticUnknown(t *testing.T) {
	for _, kind := range []string{"nest", "handler-nest", "UNKNOWN"} {
		t.Run(kind, func(t *testing.T) {
			parts := []any{uint16(0xfc0c), "BEFORE", uint16(0xfc18), "CHILD~AFTER"}
			if kind == "handler-nest" {
				parts = append([]any{uint16(0xfc1c), uint16(0xfc14), "ERR~~"}, parts...)
				parts = append(parts, uint16(0xfc16), "ERR~HANDLED")
			}
			if kind == "UNKNOWN" {
				parts = []any{"BEFORE", uint16(0xfc3a), "AFTER"}
			}
			r, m, root := newDerivedMacroModel(t, parts...)
			macroFile(t, root, "CHILD.WPM", newABC)
			m, c := queuedMacro(t, m, "ROOT")
			m, driver := drainNewMacro(t, m, c)
			if kind == "UNKNOWN" {
				if driver != nil || m.State().Macro.State != "refused" || m.State().Macro.AppliedWords != 0 || !strings.Contains(m.State().Macro.Error, "UnsupportedImage") || m.Session().Snapshot().Dirty {
					t.Fatal("UNKNOWN static preflight", m.State())
				}
			} else {
				if driver == nil || m.State().Macro.State != "failed" || m.State().Macro.AppliedWords != 6 || !strings.Contains(m.State().Macro.Error, "HostFailure") || strings.Contains(m.View().Content, "AFTER") || strings.Contains(m.View().Content, "HANDLED") || !m.Session().Snapshot().Dirty {
					t.Fatal("New NEST host policy/partial truth", m.State())
				}
			}
			if len(r.Completed()) != 1 || len(r.CompletedMacros()) != 1 || m.State().PendingIO != 0 {
				t.Fatal("New child IO escaped", r.Completed())
			}
		})
	}
}
func TestNewMacroPostTerminalFirstReadFaultsAndUnknownPublication(t *testing.T) {
	for _, fault := range []string{"missing", "equal-new-inode", "metadata", "closed", "cancel-read", "cancel-publish"} {
		t.Run(fault, func(t *testing.T) {
			r, m, root, _ := newMacroModel(t, newABC)
			m, c := queuedMacro(t, m, "ROOT")
			m, _ = drainNewMacro(t, m, c)
			birth := m.Session().Document().Birth()
			rev := m.Session().Document().Revision()
			raw, _ := m.Session().Document().Export()
			m, publish := firstSave(t, m, "FIRST")
			history := m.Session().History().Revision()
			reply := publish()
			if fault == "cancel-publish" {
				n, _ := m.Update(CancelPendingMsg{})
				m = n.(Model)
				m = drain(m, func() tea.Msg { return reply })
				if m.Session().Snapshot().NewPhase != editor.PublicationUncertain || m.State().Reconciliation == "" || m.Session().Source() != nil || !m.Session().Snapshot().Dirty {
					t.Fatal("unknown publication falsely clean", m.State())
				}
				count := len(r.Completed())
				n, retry := m.Update(RetryFirstReadMsg{})
				m = n.(Model)
				if retry != nil || len(r.Completed()) != count {
					t.Fatal("unknown read repair invented")
				}
				return
			}
			n, read := m.Update(reply)
			m = n.(Model)
			if read == nil || m.Session().Snapshot().NewPhase != editor.AwaitFirstRead {
				t.Fatal("no first read")
			}
			file := filepath.Join(root, "FIRST")
			switch fault {
			case "missing":
				if err := os.Rename(file, file+".held"); err != nil {
					t.Fatal(err)
				}
			case "equal-new-inode":
				if err := os.Rename(file, file+".held"); err != nil {
					t.Fatal(err)
				}
				if err := os.WriteFile(file, raw, 0600); err != nil {
					t.Fatal(err)
				}
			case "metadata":
				if err := os.Chmod(file, 0644); err != nil {
					t.Fatal(err)
				}
			case "closed":
				if err := r.Close(); err != nil {
					t.Fatal(err)
				}
			case "cancel-read":
				n, _ := m.Update(CancelPendingMsg{})
				m = n.(Model)
			}
			m = drain(m, read)
			exactNew(t, m, birth, rev)
			if m.Session().Snapshot().NewPhase != editor.PublishedUnbound || m.Session().Source() != nil || !m.Session().Snapshot().Dirty || m.Session().History().Revision() != history || m.State().PendingIO != 0 {
				t.Fatal("failed first read replaced lineage/history", m.State())
			}
			before := len(r.Completed())
			m, retry := press(m, tea.KeyF10, 0, "")
			if retry == nil {
				t.Fatal("missing read-only retry")
			}
			m = drain(m, retry)
			for _, receipt := range r.Completed()[before:] {
				if receipt.Kind != editor.BindNewSource {
					t.Fatal("retry republished")
				}
			}
			want := editor.PublishedUnbound
			if fault == "cancel-read" {
				want = editor.NewAnchored
			}
			after, _ := m.Session().Document().Export()
			if m.Session().Snapshot().NewPhase != want || !bytes.Equal(after, raw) {
				t.Fatal("retry source/native truth", m.State())
			}
		})
	}
}

func TestNewMacroAdministrativeNoopsPreserveAuthenticNoticeAndPristineTarget(t *testing.T) {
	for _, notice := range []bool{false, true} {
		t.Run(fmt.Sprint(notice), func(t *testing.T) {
			_, m, _, _ := newMacroModel(t, newABC)
			if notice {
				n, _ := m.Update(struct{}{})
				m = n.(Model)
			}
			before := m.Session().Snapshot()
			view := m.View().Content
			diagnostic := m.State().Notice
			for _, msg := range []tea.Msg{tea.EnvMsg{"HOST_TEST=redacted"}, tea.ColorProfileMsg{}} {
				n, c := m.Update(msg)
				m = n.(Model)
				if c != nil || !reflect.DeepEqual(before, m.Session().Snapshot()) || m.State().Notice != diagnostic || m.View().Content != view {
					t.Fatal("startup administration changed actual context")
				}
			}
			m, c := press(m, tea.KeyF10, tea.ModAlt, "")
			if c != nil {
				t.Fatal("entry should not execute IO")
			}
			if notice {
				if m.Session().Snapshot().Mode != editor.Editing || m.State().Notice != diagnostic {
					t.Fatal("administration rehabilitated notice")
				}
			} else if m.Session().Snapshot().Mode != editor.MacroName {
				t.Fatal("exact administration blocked genuine startup")
			}
		})
	}
}
func TestNewMacroCloseRetainsPendingOrActualPartialTruth(t *testing.T) {
	for _, partial := range []bool{false, true} {
		t.Run(fmt.Sprint(partial), func(t *testing.T) {
			r, m, _ := newDerivedMacroModel(t, uint16(0xfc0c), strings.Repeat("Q", 160))
			m, c := queuedMacro(t, m, "ROOT")
			if partial {
				for events := 0; events < 4096; events++ {
					n, next := m.Update(c())
					m = n.(Model)
					c = next
					if m.State().Macro.AppliedWords > 0 {
						break
					}
					if c == nil {
						t.Fatal("no partial worker")
					}
				}
			}
			before := m.Session().Snapshot()
			native, _ := m.Session().Document().Export()
			if err := r.Close(); err != nil {
				t.Fatal(err)
			}
			m, _ = drainNewMacro(t, m, c)
			after, _ := m.Session().Document().Export()
			if !bytes.Equal(native, after) || m.Session().Snapshot().NativeRevision != before.NativeRevision || m.Session().Source() != nil || m.Session().Snapshot().SaveState == editor.NewNamePublished || m.State().Macro.Active || m.State().PendingIO != 0 {
				t.Fatal("Close lost or invented effects/source", m.State())
			}
			if partial {
				receipts := r.CompletedMacros()
				if len(receipts) != 1 || !receipts[0].Interrupted || receipts[0].AppliedWords != before.Revision-1 || !m.Session().Snapshot().Dirty {
					t.Fatal("Close partial receipt", receipts)
				}
			} else if len(r.Completed()) != 0 || m.Session().Snapshot().Dirty {
				t.Fatal("closed queued root read executed")
			}
		})
	}
}
