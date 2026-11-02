package tui

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
)

func TestCharacterRepeatPublic(t *testing.T) {
	for _, c := range []struct {
		digit            rune
		char, next, want string
	}{{'5', "x", "q", "xxxxx"}, {'3', "=", "z", "==="}, {'1', "!", "a", "!"}, {'9', "A", "b", "AAAAAAAAA"}} {
		t.Run(c.want, func(t *testing.T) {
			r, m, root := newModel(t)
			_ = root
			before := m.Session().Snapshot()
			raw, _ := m.Session().Document().Export()
			m = key(t, m, tea.KeyEscape, 0, "")
			if !strings.Contains(m.View().Content, "Repeat Value = ") || m.View().Cursor.Y != 2 {
				t.Fatal("no count prompt", m.View())
			}
			m = key(t, m, c.digit, 0, string(c.digit))
			if !strings.Contains(m.View().Content, "Repeat Value = "+string(c.digit)) {
				t.Fatal("no explicit count")
			}
			after, _ := m.Session().Document().Export()
			if !reflect.DeepEqual(before, m.Session().Snapshot()) || !bytes.Equal(raw, after) || len(r.Completed()) != 0 {
				t.Fatal("pending changed session/native/IO")
			}
			for i := 0; i < 3; i++ {
				_ = m.State()
				_ = m.View()
			}
			m = key(t, m, rune(c.char[0]), 0, c.char)
			s := m.Session().Snapshot()
			if s.Gap != len(c.want) || s.Revision != before.Revision+1 || !strings.Contains(m.View().Content, c.want) {
				t.Fatal("not one authoritative Text", m.State(), m.View().Content)
			}
			_, ordinary, _ := newModel(t)
			ordinary = key(t, ordinary, 'x', 0, c.want)
			actual, _ := m.Session().Document().Export()
			expected, _ := ordinary.Session().Document().Export()
			if !bytes.Equal(actual, expected) {
				t.Fatal("ordinary native output differs")
			}
			m = key(t, m, rune(c.next[0]), 0, c.next)
			if m.Session().Snapshot().Gap != len(c.want)+1 || !strings.Contains(m.View().Content, c.want+c.next) {
				t.Fatal("count reused")
			}
		})
	}
}

func TestCharacterRepeatRefusals(t *testing.T) {
	cases := []struct {
		name  string
		count bool
		k     tea.Key
	}{
		{"missing", false, tea.Key{Code: 'x', Text: "x"}}, {"zero", false, tea.Key{Code: '0', Text: "0"}},
		{"second9", true, tea.Key{Code: '9', Text: "9"}}, {"second0", true, tea.Key{Code: '0', Text: "0"}},
		{"huge", true, tea.Key{Code: 'x', Text: strings.Repeat("x", 65536)}}, {"empty", true, tea.Key{Code: 'x'}},
		{"unicode", true, tea.Key{Code: 'é', Text: "é"}}, {"control", true, tea.Key{Code: 1, Text: "x"}},
		{"space", true, tea.Key{Code: ' ', Text: " "}}, {"enter", true, tea.Key{Code: tea.KeyEnter}},
		{"ctrl", true, tea.Key{Code: 'x', Text: "x", Mod: tea.ModCtrl}}, {"alt", true, tea.Key{Code: 'x', Text: "x", Mod: tea.ModAlt}},
		{"repeat", true, tea.Key{Code: 'x', Text: "x", IsRepeat: true}}, {"menu", true, tea.Key{Code: '=', Mod: tea.ModAlt}},
		{"macro", true, tea.Key{Code: tea.KeyF10, Mod: tea.ModAlt}}, {"left", true, tea.Key{Code: tea.KeyLeft}},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			r, m, _ := newModel(t)
			before := m.Session().Snapshot()
			raw, _ := m.Session().Document().Export()
			m = key(t, m, tea.KeyEscape, 0, "")
			if c.count {
				m = key(t, m, '9', 0, "9")
			}
			n, cmd := m.Update(tea.KeyPressMsg(c.k))
			m = n.(Model)
			got, _ := m.Session().Document().Export()
			if cmd != nil || !reflect.DeepEqual(before, m.Session().Snapshot()) || !bytes.Equal(raw, got) || len(r.Completed()) != 0 || m.State().MenuBar.Visible || m.State().Notice == "" {
				t.Fatal("refusal changed authority", m.State())
			}
			m = key(t, m, '9', 0, "9")
			if m.Session().Snapshot().Gap != 1 {
				t.Fatal("following digit inherited count or swallowed")
			}
		})
	}
}

func TestCharacterRepeatCancel(t *testing.T) {
	for _, code := range []rune{tea.KeyEscape, tea.KeyF1} {
		for _, count := range []bool{false, true} {
			t.Run(fmt.Sprint(code, count), func(t *testing.T) {
				_, m, _ := newModel(t)
				before := m.Session().Snapshot()
				m = key(t, m, tea.KeyEscape, 0, "")
				if count {
					m = key(t, m, '3', 0, "3")
				}
				m = key(t, m, code, 0, "")
				if !reflect.DeepEqual(before, m.Session().Snapshot()) || m.State().Notice != "Character Repeat cancelled (host policy)" {
					t.Fatal(m.State())
				}
				m = key(t, m, 'z', 0, "z")
				if m.Session().Snapshot().Gap != 1 {
					t.Fatal("cancel replay")
				}
			})
		}
	}
}

func TestCharacterRepeatInvalidation(t *testing.T) {
	for _, msg := range []tea.Msg{tea.WindowSizeMsg{Width: 80, Height: 25}, tea.WindowSizeMsg{Width: 40, Height: 20}, tea.PasteStartMsg{}, tea.PasteMsg{Content: "xyz"}, tea.PasteEndMsg{}, tea.FocusMsg{}, tea.BlurMsg{}, tea.MouseClickMsg{}, struct{}{}} {
		t.Run(fmt.Sprintf("%T-%v", msg, msg), func(t *testing.T) {
			_, m, _ := newModel(t)
			before := m.Session().Snapshot()
			m = key(t, m, tea.KeyEscape, 0, "")
			m = key(t, m, '5', 0, "5")
			n, c := m.Update(msg)
			m = n.(Model)
			if c != nil || !reflect.DeepEqual(before, m.Session().Snapshot()) {
				t.Fatal("invalidator mutated session")
			}
			m = key(t, m, 'x', 0, "x")
			if m.Session().Snapshot().Gap != 1 {
				t.Fatal("invalidated count retained")
			}
		})
	}
}

func TestCharacterRepeatNeutralAndStale(t *testing.T) {
	_, m, _ := newModel(t)
	old := m
	m = key(t, m, tea.KeyEscape, 0, "")
	pending := m
	m = key(t, m, '5', 0, "5")
	for _, stale := range []Model{old, pending} {
		n, c := stale.Update(tea.KeyPressMsg{Code: 'x', Text: "x"})
		if c != nil || n.(Model).Session().Snapshot().Gap != 0 {
			t.Fatal("stale mutated")
		}
	}
	counted := m
	n, _ := m.Update(tea.EnvMsg{})
	m = n.(Model)
	oldCounted := counted
	n, c := oldCounted.Update(tea.KeyPressMsg{Code: 'x', Text: "x"})
	if c != nil || n.(Model).Session().Snapshot().Gap != 0 || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("stale counted Model admitted")
	}
	before := m.Session().Snapshot()
	for _, msg := range []tea.Msg{tea.KeyReleaseMsg{Code: 'x'}, tea.KeyboardEnhancementsMsg{}, tea.CapabilityMsg{}, tea.TerminalVersionMsg{}, tea.EnvMsg{}, tea.ColorProfileMsg{}} {
		n, c := m.Update(msg)
		m = n.(Model)
		if c != nil || !reflect.DeepEqual(before, m.Session().Snapshot()) {
			t.Fatal("neutral changed session")
		}
		_ = m.State()
		_ = m.View()
	}
	m = key(t, m, 'x', 0, "x")
	if m.Session().Snapshot().Gap != 5 {
		t.Fatal("neutral/stale consumed authentic state")
	}
}

func TestCharacterRepeatSourceExclusions(t *testing.T) {
	for _, setup := range []struct {
		name string
		keys []tea.Key
	}{{"nonblank", []tea.Key{{Code: 'a', Text: "a"}}}, {"edited-empty", []tea.Key{{Code: 'a', Text: "a"}, {Code: tea.KeyBackspace}}}, {"typeover", []tea.Key{{Code: tea.KeyInsert}}}, {"reveal", []tea.Key{{Code: tea.KeyF3, Mod: tea.ModAlt}}}, {"doc2", []tea.Key{{Code: tea.KeyF3, Mod: tea.ModShift}}}, {"menu", []tea.Key{{Code: '=', Mod: tea.ModAlt}}}, {"prompt", []tea.Key{{Code: tea.KeyF10}}}} {
		t.Run(setup.name, func(t *testing.T) {
			_, m, _ := newModel(t)
			for _, k := range setup.keys {
				n, _ := m.Update(tea.KeyPressMsg(k))
				m = n.(Model)
			}
			m = key(t, m, tea.KeyEscape, 0, "")
			if m.characterRepeat.active {
				t.Fatal("nonpristine admitted")
			}
		})
	}
}

// Supplemental impossible conjunctions verify defense; positive authority above
// always originates from Open and the authentic returned public Update chain.
func TestCharacterRepeatStructuralForeignAndControl(t *testing.T) {
	_, m, _ := newModel(t)
	m = key(t, m, tea.KeyEscape, 0, "")
	m = key(t, m, '5', 0, "5")
	_, foreign, _ := newModel(t)
	m.session = foreign.session
	before := m.Session().Snapshot()
	m = key(t, m, 'x', 0, "x")
	if !reflect.DeepEqual(before, m.Session().Snapshot()) {
		t.Fatal("foreign opaque owner admitted")
	}
	_, m, _ = newModel(t)
	m = key(t, m, tea.KeyEscape, 0, "")
	m = key(t, m, '9', 0, "9")
	m.characterRepeat.count = 255
	before = m.Session().Snapshot()
	m = key(t, m, 'x', 0, "x")
	if !reflect.DeepEqual(before, m.Session().Snapshot()) {
		t.Fatal("corrupt count expanded")
	}
	_, m, _ = newModel(t)
	m = key(t, m, tea.KeyEscape, 0, "")
	n, c := m.Update(CancelPendingMsg{})
	m = n.(Model)
	if c != nil || m.characterRepeat.active || m.State().Notice == "" {
		t.Fatal("control swallowed old handler", m.State())
	}
}

var characterAllocationSink string

func TestCharacterRepeatAllocations(t *testing.T) {
	for _, count := range []uint8{1, 9} {
		t.Run(fmt.Sprint(count), func(t *testing.T) {
			const samples = 10
			allocated := func(f func()) uint64 {
				runtime.GC()
				var a, b runtime.MemStats
				runtime.ReadMemStats(&a)
				for i := 0; i < samples; i++ {
					f()
				}
				runtime.ReadMemStats(&b)
				return (b.TotalAlloc - a.TotalAlloc) / samples
			}
			expansion := allocated(func() { characterAllocationSink = characterPayload('x', count) })
			if expansion > 256 {
				t.Fatal("expansion allocation", expansion)
			}
			_, m, _ := newModel(t)
			m = key(t, m, tea.KeyEscape, 0, "")
			m = key(t, m, rune('0'+count), 0, string(rune('0'+count)))
			view := allocated(func() { characterAllocationSink = m.View().Content })
			if view > 128<<10 {
				t.Fatal("View allocation", view)
			}
			cold := allocated(func() {
				r, n, e := Open(Config{Root: t.TempDir(), Profile: LocalFlat})
				if e != nil {
					t.Fatal(e)
				}
				n = key(t, n, tea.KeyEscape, 0, "")
				n = key(t, n, rune('0'+count), 0, string(rune('0'+count)))
				_ = key(t, n, 'x', 0, "x")
				if e = r.Close(); e != nil {
					t.Fatal(e)
				}
			})
			if cold > 1<<20 {
				t.Fatal("cold public sequence allocation", cold)
			}
			t.Logf("samples=%d expansion=%d pendingView=%d coldOpenAndThreeKeys=%d", samples, expansion, view, cold)
		})
	}
}
func TestCharacterRepeatPublicationAndLoadedExclusion(t *testing.T) {
	r, m, root := newModel(t)
	m = key(t, m, tea.KeyEscape, 0, "")
	m = key(t, m, '5', 0, "5")
	m = key(t, m, 'x', 0, "x")
	m = key(t, m, 'q', 0, "q")
	expected, _ := m.Session().Document().Export()
	m, c := firstSave(t, m, "FIRST")
	m = drain(m, c)
	if m.Session().Source() == nil || m.State().Session.Pending != nil {
		t.Fatal("no actual first binding", m.State())
	}
	disk, e := os.ReadFile(filepath.Join(root, "FIRST"))
	if e != nil || !bytes.Equal(disk, expected) {
		t.Fatal("native publication", e)
	}
	source := m.Session().Source().Identity()
	m = key(t, m, tea.KeyF10, 0, "")
	m = key(t, m, 'S', 0, "SECOND")
	m, c = press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	second, e := os.ReadFile(filepath.Join(root, "SECOND"))
	if e != nil || !bytes.Equal(disk, second) || m.Session().Source().Identity() != source {
		t.Fatal("no edit Save As", e, m.State())
	}
	m = key(t, m, tea.KeyEscape, 0, "")
	if m.characterRepeat.active {
		t.Fatal("published New admitted")
	}
	_ = r
}

func TestCharacterRepeatCLIReadback(t *testing.T) {
	dir := os.Getenv("WORDLING_CHARACTER_PTY")
	if dir == "" {
		t.Skip("separate real CLI artifacts not requested")
	}
	for i, text := range []string{"xxxxxq", "===z"} {
		_, ordinary, _ := newModel(t)
		ordinary = key(t, ordinary, 'x', 0, text)
		expected, _ := ordinary.Session().Document().Export()
		for _, name := range []string{"FIRST", "SECOND"} {
			raw, e := os.ReadFile(filepath.Join(dir, fmt.Sprint("r", i+1), "files", name))
			if e != nil || !bytes.Equal(raw, expected) {
				t.Fatal("real CLI native differs from constructor plus ordinary Text", i, name, e)
			}
			d, e := document.Parse(raw)
			if e != nil || d.TokenCount() != len(text) {
				t.Fatal("actual reader", e)
			}
			out, e := d.Export()
			if e != nil || !bytes.Equal(out, raw) {
				t.Fatal("reader roundtrip", e)
			}
		}
	}
}
