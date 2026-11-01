package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestMacroAltF10UsesRootedRuntimeAndOrdinaryDocument(t *testing.T) {
	_, m, _, root := testModel(t)
	m = retrieve(m)
	raw, e := os.ReadFile("../../docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(root, "M38.WPM"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	before := m.Session().Document().TokenCount()
	m, c := press(m, tea.KeyF10, tea.ModAlt, "")
	if c != nil || m.Session().Snapshot().Mode != editor.MacroName {
		t.Fatal("Alt-F10 did not enter original Macro prompt", m.State())
	}
	m = key(t, m, 'M', 0, "M38")
	m, c = press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	if m.Session().Snapshot().Mode != editor.Editing || m.Session().Document().TokenCount() != before+3 || !m.Session().Snapshot().Dirty || !strings.Contains(m.View().Content, "ABC") {
		t.Fatal("not actual ordinary macro effect", m.State(), m.View().Content)
	}
}

func macroFile(t *testing.T, root, name, source string) {
	t.Helper()
	raw, e := os.ReadFile("../../" + source)
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(root, name), raw, 0600); e != nil {
		t.Fatal(e)
	}
}
func macroLoaded(t *testing.T) (*Runtime, Model, string) {
	t.Helper()
	r, m, _, root := testModel(t)
	m = retrieve(m)
	macroFile(t, root, "M38.WPM", "docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	return r, m, root
}
func queuedMacro(t *testing.T, m Model, name string) (Model, tea.Cmd) {
	t.Helper()
	m = key(t, m, tea.KeyF10, tea.ModAlt, "")
	m = key(t, m, 'M', 0, name)
	m, c := press(m, tea.KeyEnter, 0, "")
	if c == nil {
		t.Fatal("missing actual rooted macro read")
	}
	return m, c
}
func TestMacroReadDuplicateCannotSettleAuthenticAndSnapshotsCannotRetarget(t *testing.T) {
	r, m, root := macroLoaded(t)
	m, read := queuedMacro(t, m, "M38")
	actual := read()
	n, c := m.Update(read())
	m = n.(Model)
	if c != nil || m.State().PendingIO != 1 || m.Session().Snapshot().Mode != editor.Waiting {
		t.Fatal("duplicate settled authentic read")
	}
	n, c = m.Update(actual)
	m = n.(Model)
	if c == nil || !m.State().Macro.Active || m.State().PendingIO != 0 {
		t.Fatal("root did not queue actual compile")
	}
	source := m.Session().MacroSource()
	*source = storage.Macro{}
	image := m.Session().MacroSource().Image()
	*image = wpm.Image{}
	request := m.State().Session.Last.Result.Macro
	if request != nil {
		*request = storage.Macro{}
	}
	m = drain(m, c)
	if m.State().Macro.AppliedWords != 3 || m.State().Macro.State != "complete" {
		t.Fatal(m.State())
	}
	disk, e := os.ReadFile(filepath.Join(root, "M38.WPM"))
	if e != nil || len(disk) == 0 {
		t.Fatal("source changed")
	}
	for _, receipt := range r.Completed() {
		if receipt.Macro != nil {
			t.Fatal("shutdown retained public macro image")
		}
	}
}
func TestMacroCompileAndStepDispatchDeliveryExactlyOnce(t *testing.T) {
	_, m, _ := macroLoaded(t)
	m, read := queuedMacro(t, m, "M38")
	n, start := m.Update(read())
	m = n.(Model)
	original := start()
	n, c := m.Update(start())
	m = n.(Model)
	if c != nil || !m.State().Macro.WorkerPending {
		t.Fatal("duplicate compile settled authentic")
	}
	old := m
	n, step := m.Update(original)
	m = n.(Model)
	if step == nil {
		t.Fatal("no bounded step")
	}
	n, c = old.Update(original)
	if c != nil || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("old model stole compile result")
	}
	actual := step()
	n, c = m.Update(step())
	m = n.(Model)
	if c != nil {
		t.Fatal("duplicate step queued work")
	}
	n, c = m.Update(actual)
	m = drain(n.(Model), c)
	if m.State().Macro.AppliedWords != 3 {
		t.Fatal("duplicate native effects", m.State())
	}
	before := m.Session().Document().Revision()
	n, c = m.Update(actual)
	if c != nil || n.(Model).Session().Document().Revision() != before {
		t.Fatal("double delivery changed native")
	}
}
func TestMacroModelSameRevisionForkAndResizeAuthority(t *testing.T) {
	_, m, _ := macroLoaded(t)
	base := m
	m = key(t, m, tea.KeyF10, tea.ModAlt, "")
	n, c := base.Update(tea.KeyPressMsg{Code: tea.KeyF3, Mod: tea.ModAlt})
	if c != nil || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("divergent same-revision fork accepted")
	}
	if base.Session().Document().Revision() != m.Session().Document().Revision() {
		t.Fatal("name entry invented native revision")
	}
	previous := m
	n, c = m.Update(tea.WindowSizeMsg{Width: 31, Height: 9})
	m = n.(Model)
	if c != nil || m.State().Width != 31 {
		t.Fatal("responsive resize")
	}
	n, c = previous.Update(tea.KeyPressMsg{Code: 'M', Text: "M38"})
	if c != nil || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("equal native revision/view fork accepted")
	}
	m = key(t, m, tea.KeyF1, 0, "")
	if m.Session().Snapshot().Mode != editor.Editing {
		t.Fatal("observed name F1 unavailable")
	}
}
func TestMacroMissingUnsupportedAndPendingSaveRemainDistinct(t *testing.T) {
	_, m, root := macroLoaded(t)
	m = key(t, m, tea.KeyF10, 0, "")
	before := m.Session().Snapshot()
	m = key(t, m, tea.KeyF10, tea.ModAlt, "")
	if m.Session().Snapshot().Mode != editor.SaveName || m.Session().Snapshot().Draft != before.Draft {
		t.Fatal("Alt-F10 nested into pending Save-name")
	}
	m = key(t, m, tea.KeyF1, 0, "")
	m, c := queuedMacro(t, m, "MISSING")
	m = drain(m, c)
	if m.Session().Snapshot().Mode != editor.MacroError || m.Session().Snapshot().Notice != "ERROR: File not found -- MISSING.WPM" {
		t.Fatal("actual missing-name branch", m.State())
	}
	m = key(t, m, tea.KeyF1, 0, "")
	macroFile(t, root, "BAD.WPM", "docs/research/continuation/macro-session/runs/wp38-stop-default-02/input/M38.WPM")
	beforeRev := m.Session().Document().Revision()
	m, c = queuedMacro(t, m, "BAD")
	m = drain(m, c)
	if m.Session().Document().Revision() != beforeRev || m.Session().Snapshot().Mode != editor.Editing || m.State().Macro.State != "refused" || m.State().Macro.AppliedWords != 0 {
		t.Fatal("unsupported source executed", m.State())
	}
}
func TestMacroRuntimeGuardsCloseCapacityAndForeignRoot(t *testing.T) {
	for _, guard := range []string{"closed", "capacity", "foreign"} {
		t.Run(guard, func(t *testing.T) {
			r, m, root := macroLoaded(t)
			m, read := queuedMacro(t, m, "M38")
			if guard == "closed" {
				if e := r.Close(); e != nil {
					t.Fatal(e)
				}
			}
			if guard == "capacity" {
				r.mu.Lock()
				r.issued = 1024
				r.mu.Unlock()
			}
			if guard == "foreign" {
				i := m.Session().Snapshot().Pending
				other, e := storage.OpenDirectory(root)
				if e != nil {
					t.Fatal(e)
				}
				defer other.Close()
				i.Directory = other
				read = r.command(*i)
			}
			before := m.Session().Document().Revision()
			m = drain(m, read)
			if m.State().PendingIO != 0 || m.Session().Document().Revision() != before || m.Session().Snapshot().Pending != nil || m.State().Notice == "" {
				t.Fatal("guard not truthful/no IO", m.State())
			}
		})
	}
}
