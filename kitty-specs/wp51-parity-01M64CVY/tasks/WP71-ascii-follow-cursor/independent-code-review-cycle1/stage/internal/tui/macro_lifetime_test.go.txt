package tui

import (
	"bytes"
	"os"
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

func TestMacroCOUTIsExplicitExactAndSharesOneOpening(t *testing.T) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	for _, profile := range []string{LocalFlat, MacroCOUT} {
		t.Run(profile, func(t *testing.T) {
			r, m, root := macroModel(t, profile, raw)
			macroFile(t, root, "M38.WPM", "docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
			names := []string{"C:\\OUT\\M38", "c:\\OUT\\M38", "C:/OUT/M38", "C:\\out\\M38", "D:\\OUT\\M38", "C:\\OUT\\..\\M38", "C:\\OUT\\\\M38", "C:OUT\\M38", "C:\\OUT\\M38.wpm", "../M38"}
			for i, name := range names {
				m = key(t, m, tea.KeyF10, tea.ModAlt, "")
				m = key(t, m, 'M', 0, name)
				n, c := press(m, tea.KeyEnter, 0, "")
				m = n
				if profile == MacroCOUT && i == 0 {
					if c == nil {
						t.Fatal("explicit exact COUT mapping missing", m.State())
					}
					m = drain(m, c)
					if m.State().Macro.AppliedWords != 3 || m.State().Macro.Error != "" {
						t.Fatal(m.State())
					}
				} else {
					if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Mode != editor.MacroName {
						t.Fatal("near-miss mapping normalized", name, m.State())
					}
					m = key(t, m, tea.KeyF1, 0, "")
				}
			}
			m, c := queuedMacro(t, m, "M38")
			i := m.Session().Snapshot().Pending
			expected := *i.Directory
			other, e := storage.OpenDirectory(root)
			if e != nil {
				t.Fatal(e)
			}
			if expected == *other {
				t.Fatal("independent open acquired same capability")
			}
			*i.Directory = *other
			_ = other.Close()
			m = drain(m, c)
			if m.State().Macro.AppliedWords != 3 || m.State().Macro.Error != "" {
				t.Fatal("public wrapper retargeted read lifetime", m.State())
			}
			if profile == MacroCOUT {
				m, c = queuedMacro(t, m, "C:\\OUT\\M38")
				if *m.Session().Snapshot().Pending.Directory != expected {
					t.Fatal("aliases use different opening")
				}
				if e := r.Close(); e != nil {
					t.Fatal(e)
				}
				m = drain(m, c)
				if m.State().Macro.Active || m.Session().Snapshot().Pending != nil {
					t.Fatal("alias bypassed close", m.State())
				}
			}
		})
	}
	for _, profile := range []string{"", "Macro-cout", "macro-cout/", "dos", "local-flat+cout"} {
		if r, _, err := Open(Config{Root: t.TempDir(), Profile: profile}); err == nil {
			_ = r.Close()
			t.Fatal("unknown profile accepted", profile)
		}
	}
}
func TestMacroLiveF1DoesNotAliasHostContainment(t *testing.T) {
	_, m, root := macroLoaded(t)
	macroFile(t, root, "WHILELP.WPM", "docs/research/reference-runs/2026-10-29-history-02/CMD51-215/WHILELP.WPM")
	m, c := queuedMacro(t, m, "WHILELP")
	partial := false
	for turns := 0; c != nil && turns < 1000; turns++ {
		n, next := m.Update(c())
		m = n.(Model)
		c = next
		if m.State().Macro.Active && m.State().Macro.AppliedWords > 0 && c != nil {
			partial = true
			break
		}
	}
	if !partial {
		t.Fatal("original loop did not yield with real partial effects", m.State())
	}
	before := m.Session().Document().Revision()
	words := m.State().Macro.AppliedWords
	m = key(t, m, tea.KeyF1, 0, "")
	if !strings.Contains(m.State().Notice, "unsupported") || !m.State().Macro.Active || m.Session().Document().Revision() != before {
		t.Fatal("F1 invented stop behavior")
	}
	n, extra := m.Update(tea.WindowSizeMsg{Width: 40, Height: 12})
	m = n.(Model)
	if extra != nil || m.State().Width != 40 {
		t.Fatal("pending macro blocks resize")
	}
	n, extra = m.Update(HostStopMacroMsg{Reason: "component host containment"})
	m = n.(Model)
	if extra != nil {
		t.Fatal("queued CPU cancellation dispatched another worker")
	}
	m = drain(m, c)
	if m.State().Macro.State != "stopped" || m.State().Macro.Active || m.State().Macro.AppliedWords != words || m.Session().Document().Revision() != before || !m.Session().Snapshot().Dirty {
		t.Fatal("host stop lost/added partial effects", m.State())
	}
}
func TestMacroAuthenticNestedReadArrivesWhileHostStopWorkerPending(t *testing.T) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	_, m, root := macroModel(t, MacroCOUT, raw)
	for _, name := range []string{"PARENT", "CHILD"} {
		macroFile(t, root, name+".WPM", "docs/research/reference-runs/2026-10-29-history-02/CMD51-212/"+name+".WPM")
	}
	m, c := queuedMacro(t, m, "PARENT")
	waiting := false
	for turns := 0; c != nil && turns < 1000; turns++ {
		n, next := m.Update(c())
		m = n.(Model)
		c = next
		if m.macro != nil && !m.macroCPU && m.Session().Snapshot().Pending != nil {
			waiting = true
			break
		}
	}
	if !waiting || c == nil {
		t.Fatal("no actual child read", m.State())
	}
	actual := c()
	before := m.Session().Document().Revision()
	words := m.State().Macro.AppliedWords
	n, stop := m.Update(HostStopMacroMsg{Reason: "stop while actual child receipt undelivered"})
	m = n.(Model)
	if stop == nil {
		t.Fatal("host stop not queued")
	}
	n, extra := m.Update(actual)
	m = n.(Model)
	if extra != nil || m.macroDeferred == nil || m.State().PendingIO != 1 || m.Session().Document().Revision() != before {
		t.Fatal("actual IO lost/settled during worker", m.State())
	}
	m = drain(m, stop)
	if m.State().PendingIO != 0 || m.macroDeferred != nil || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().Mode != editor.Editing || m.State().Macro.AppliedWords != words || m.Session().Document().Revision() != before {
		t.Fatal("late child receipt changed target/settlement", m.State())
	}
	n, extra = m.Update(actual)
	m = n.(Model)
	if extra != nil || m.State().PendingIO != 0 || m.Session().Document().Revision() != before {
		t.Fatal("duplicate child read changed stopped frame")
	}
}
func TestMacroCloseAndQueuedCPUReceiptKeepTruthfulOutcome(t *testing.T) {
	r, m, _ := macroLoaded(t)
	m, read := queuedMacro(t, m, "M38")
	n, start := m.Update(read())
	m = n.(Model)
	before := m.Session().Document().Revision()
	if e := r.Close(); e != nil {
		t.Fatal(e)
	}
	if m.macro.ctx.Err() == nil {
		t.Fatal("Close did not cancel the actual queued/started worker context")
	}
	m = drain(m, start)
	if m.Session().Document().Revision() != before || m.State().Macro.AppliedWords != 0 || m.State().Macro.State != "host-closed" {
		t.Fatal("queued CPU executed after Close", m.State())
	}
	outcomes := r.CompletedMacros()
	if len(outcomes) != 1 || !outcomes[0].Interrupted || outcomes[0].AppliedWords != 0 {
		t.Fatal("lost truthful shutdown receipt", outcomes)
	}
	outcomes[0].Source = [32]byte{}
	outcomes[0].Error = "changed"
	if r.CompletedMacros()[0].Source == ([32]byte{}) || r.CompletedMacros()[0].Error == "changed" {
		t.Fatal("outcome observation aliases runtime")
	}
	// A history of receipts cannot retain opaque document.Revision pointers,
	// source images, interfaces or per-step document states.
	typ := reflect.TypeOf(MacroOutcome{})
	for i := 0; i < typ.NumField(); i++ {
		kind := typ.Field(i).Type.Kind()
		if kind == reflect.Pointer || kind == reflect.Interface || kind == reflect.Struct || kind == reflect.Slice || kind == reflect.Map {
			t.Fatal("macro ledger retains object graph", typ.Field(i))
		}
	}
}
func TestMacroStrictAuthorityRejectsOldIOAndForeignModelBeforeDelivery(t *testing.T) {
	_, m, _ := macroLoaded(t)
	m, read := queuedMacro(t, m, "M38")
	actual := read()
	old := m
	n, c := m.Update(tea.WindowSizeMsg{Width: 52, Height: 14})
	m = n.(Model)
	if c != nil {
		t.Fatal("resize dispatch")
	}
	n, c = old.Update(actual)
	if c != nil || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("old same-revision model consumed authentic IO")
	}
	_, foreign, _ := macroLoaded(t)
	foreign, _ = queuedMacro(t, foreign, "M38")
	raw, _ := foreign.Session().Document().Export()
	n, c = foreign.Update(actual)
	foreign = n.(Model)
	got, _ := foreign.Session().Document().Export()
	if c != nil || !bytes.Equal(raw, got) || foreign.State().PendingIO != 1 {
		t.Fatal("whole model retargeting accepted foreign IO")
	}
	n, c = m.Update(actual)
	m = drain(n.(Model), c)
	if m.State().Macro.AppliedWords != 3 {
		t.Fatal("authentic current model lost receipt", m.State())
	}
}

func TestMacroRuntimeRetainsActualSharedCloseFailure(t *testing.T) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	r, m, root := macroModel(t, MacroCOUT, raw)
	macroFile(t, root, "M38.WPM", "docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	m, c := queuedMacro(t, m, "C:\\OUT\\M38")
	cap := m.Session().Snapshot().Pending.Directory
	if e := cap.Close(); e != nil {
		t.Fatal(e)
	}
	before := m.Session().Document().Revision()
	m = drain(m, c)
	if m.Session().Document().Revision() != before || m.State().PendingIO != 0 || m.State().Macro.Active || m.Session().Snapshot().Mode != editor.Editing {
		t.Fatal("closed actual capability manufactured source/effects", m.State())
	}
	first := r.Close()
	second := r.Close()
	if first == nil || second == nil || first.Error() != second.Error() {
		t.Fatal("actual repeated shared Close failure lost", first, second)
	}
}
func TestMacroAuthorityBindsDistinctCursorViewForksBeforeFirstMacro(t *testing.T) {
	_, base, _ := macroLoaded(t)
	right := key(t, base, tea.KeyRight, 0, "")
	n, c := base.Update(tea.KeyPressMsg{Code: tea.KeyF3, Mod: tea.ModAlt})
	if c != nil || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("old pre-macro fork stole model state")
	}
	if right.Session().Document().Revision() != base.Session().Document().Revision() || right.Session().Snapshot().Gap == base.Session().Snapshot().Gap {
		t.Fatal("not distinct same-revision cursor fork")
	}
	right, c = queuedMacro(t, right, "M38")
	right = drain(right, c)
	if right.State().Macro.AppliedWords != 3 {
		t.Fatal("authentic cursor owner lost macro", right.State())
	}
}
func TestMacroZeroModelRefusesWithoutHostAccess(t *testing.T) {
	var m Model
	n, c := m.Update(tea.KeyPressMsg{Code: tea.KeyF10, Mod: tea.ModAlt})
	if c != nil || !strings.Contains(n.(Model).State().Notice, "Uninitialized") {
		t.Fatal("zero model attempted host work")
	}
}
