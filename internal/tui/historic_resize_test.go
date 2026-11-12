package tui_test

import (
	"bytes"
	"fmt"
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/tui"
)

func resizeModel(t *testing.T) tui.Model {
	t.Helper()
	r, m, e := tui.Open(tui.Config{Root: t.TempDir(), Profile: tui.LocalFlat, EditorChrome: true})
	if e != nil {
		t.Fatal(e)
	}
	t.Cleanup(func() {
		if e := r.Close(); e != nil {
			t.Error(e)
		}
	})
	return m
}
func resizeStep(t *testing.T, m tui.Model, msg tea.Msg) tui.Model {
	t.Helper()
	n, c := m.Update(msg)
	if c != nil {
		t.Fatal("unexpected command in modal-only input")
	}
	m = n.(tui.Model)
	_ = m.View()
	return m
}
func resizeKey(t *testing.T, m tui.Model, code rune, mod tea.KeyMod, text string) tui.Model {
	t.Helper()
	return resizeStep(t, m, tea.KeyPressMsg{Code: code, Mod: mod, Text: text})
}
func resizeRaw(t *testing.T, m tui.Model) []byte {
	t.Helper()
	b, e := m.Session().Document().Export()
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func resizeOpen(t *testing.T, m tui.Model, kind string) tui.Model {
	t.Helper()
	if kind == "files" {
		return resizeKey(t, m, tea.KeyF5, 0, "")
	}
	return resizeKey(t, m, '=', tea.ModAlt, "=")
}
func resizeConserved(t *testing.T, before, after tui.Model) {
	t.Helper()
	a, b := resizeRaw(t, before), resizeRaw(t, after)
	if !bytes.Equal(a, b) || !reflect.DeepEqual(before.State().Session, after.State().Session) || !reflect.DeepEqual(before.Session().History(), after.Session().History()) {
		t.Fatalf("R77-001 modal input changed document: before=%x after=%x; before_state=%+v after_state=%+v", a, b, before.State().Session, after.State().Session)
	}
}

func TestHistoricResizeModalConservation(t *testing.T) {
	for _, kind := range []string{"files", "menu"} {
		t.Run(kind, func(t *testing.T) {
			m := resizeModel(t)
			m = resizeKey(t, m, 'a', 0, "a")
			m = resizeOpen(t, m, kind)
			before := m
			m = resizeKey(t, m, 'q', 0, "q")
			resizeConserved(t, before, m)
			for _, height := range []int{11, 25, 12, 11, 12, 11, 1, 2, 11, 25} {
				m = resizeStep(t, m, tea.WindowSizeMsg{Width: 80, Height: height})
				m = resizeKey(t, m, 'q', 0, "q")
				resizeConserved(t, before, m)
				// Selection movement must not mutate the document either.
				m = resizeKey(t, m, tea.KeyDown, 0, "")
				resizeConserved(t, before, m)
				if height < 12 {
					v := m.View()
					if !strings.Contains(ansi.Strip(v.Content), "active") || v.Cursor != nil {
						t.Fatal("hidden modal needs truthful small-window presentation and no document caret", v.Content)
					}
				}
			}
			m = resizeKey(t, m, tea.KeyF7, 0, "")
			resizeConserved(t, before, m)
			m = resizeKey(t, m, 'z', 0, "z")
			if !bytes.HasSuffix(resizeRaw(t, m), []byte("az")) {
				t.Fatal("typing failed to resume after modal exit")
			}
		})
	}
}

func TestHistoricResizeSmallEntryCancellationAndStaleInput(t *testing.T) {
	for _, kind := range []string{"files", "menu"} {
		for _, cancel := range []rune{tea.KeyF1, tea.KeyEscape, tea.KeyF7} {
			t.Run(fmt.Sprintf("%s/%d", kind, cancel), func(t *testing.T) {
				m := resizeModel(t)
				m = resizeStep(t, m, tea.WindowSizeMsg{Width: 80, Height: 11})
				before := m
				m = resizeOpen(t, m, kind)
				if !strings.Contains(ansi.Strip(m.View().Content), "active") {
					t.Fatal("small-window modal was not acknowledged")
				}
				stale := m
				m = resizeKey(t, m, 'x', 0, "x")
				resizeConserved(t, before, m)
				rejected := resizeKey(t, stale, 'x', 0, "x")
				if !strings.Contains(rejected.State().Notice, "Stale UI transition refused") {
					t.Fatal("stale input acquired UI authority")
				}
				resizeConserved(t, before, rejected)
				m = resizeKey(t, m, tea.KeyEnter, 0, "")
				resizeConserved(t, before, m)
				m = resizeStep(t, m, tea.MouseClickMsg{X: 0, Y: 0, Button: tea.MouseLeft})
				resizeConserved(t, before, m)
				m = resizeKey(t, m, cancel, 0, "")
				resizeConserved(t, before, m)
				m = resizeKey(t, m, 'z', 0, "z")
				if !bytes.HasSuffix(resizeRaw(t, m), []byte("z")) || m.State().Session.Mode != editor.Editing {
					t.Fatal("small-window cancel did not return focus")
				}
			})
		}
	}
}

func TestHistoricResizeDoesNotConsumePendingSave(t *testing.T) {
	m := resizeModel(t)
	m = resizeKey(t, m, 'a', 0, "a")
	m = resizeKey(t, m, tea.KeyF10, 0, "")
	m = resizeKey(t, m, 'P', 0, "PENDING")
	n, cmd := m.Update(tea.KeyPressMsg{Code: tea.KeyEnter})
	m = n.(tui.Model)
	if cmd == nil || m.State().PendingIO != 1 {
		t.Fatal("expected real pending save")
	}
	before := resizeRaw(t, m)
	m = resizeStep(t, m, tea.WindowSizeMsg{Width: 80, Height: 11})
	m = resizeKey(t, m, tea.KeyF5, 0, "")
	m = resizeKey(t, m, '=', tea.ModAlt, "=")
	if m.State().PendingIO != 1 || !bytes.Equal(before, resizeRaw(t, m)) {
		t.Fatal("resize/modal keys consumed pending save or changed document")
	}
	for steps := 0; cmd != nil; steps++ {
		if steps > 16 {
			t.Fatal("unbounded I/O chain")
		}
		n, cmd = m.Update(cmd())
		m = n.(tui.Model)
	}
	if m.State().PendingIO != 0 || m.State().Session.Dirty || !bytes.Equal(before, resizeRaw(t, m)) {
		t.Fatal("real save completion lost after resize", m.State())
	}
}
