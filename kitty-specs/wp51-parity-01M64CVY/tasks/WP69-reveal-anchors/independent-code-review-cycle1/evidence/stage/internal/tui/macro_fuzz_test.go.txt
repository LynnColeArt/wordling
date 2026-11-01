package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"

	tea "charm.land/bubbletea/v2"
)

// Host-boundary fuzz, not another VM/codec fuzz: at most64 generated events,
// eight held commands/messages and one16-unit slice per invoked CPU command.
func FuzzMacroHostContinuations(f *testing.F) {
	root := f.TempDir()
	sources := map[string]string{
		"ORIGIN":     "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5",
		"M38.WPM":    "docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM",
		"PARENT.WPM": "docs/research/reference-runs/2026-10-29-history-02/CMD51-212/PARENT.WPM",
		"CHILD.WPM":  "docs/research/reference-runs/2026-10-29-history-02/CMD51-212/CHILD.WPM",
	}
	originals := map[string][]byte{}
	for name, path := range sources {
		b, e := os.ReadFile("../../" + path)
		if e != nil {
			f.Fatal(e)
		}
		if e = os.WriteFile(filepath.Join(root, name), b, 0600); e != nil {
			f.Fatal(e)
		}
		originals[name] = b
	}
	for _, seed := range [][]byte{{3, 4, 5, 0, 1, 0, 1, 0, 1, 0, 1}, {3, 4, 5, 0, 1, 0, 1, 8, 0, 1, 0, 1}, {3, 4, 5, 0, 1, 7, 11, 1, 2, 6, 9}, {15, 16, 17, 0, 1, 0, 1, 0, 1, 0, 1, 8}} {
		f.Add(seed)
	}
	f.Fuzz(func(t *testing.T, input []byte) {
		if len(input) > 64 {
			t.Skip()
		}
		profile := LocalFlat
		if len(input) > 0 && input[0]&1 == 1 {
			profile = MacroCOUT
		}
		r, m, e := Open(Config{Root: root, Profile: profile})
		if e != nil {
			t.Fatal(e)
		}
		t.Cleanup(func() { _ = r.Close() })
		m = retrieve(m)
		old := m
		commands := []tea.Cmd{}
		messages := []tea.Msg{}
		var duplicate tea.Msg
		update := func(msg tea.Msg) {
			old = m
			n, c := m.Update(msg)
			m = n.(Model)
			if c != nil && len(commands) < 8 {
				commands = append(commands, c)
			}
		}
		for _, v := range input {
			switch v % 12 {
			case 0:
				if len(commands) > 0 {
					c := commands[0]
					commands = commands[1:]
					msg := c()
					if len(messages) < 8 {
						messages = append(messages, msg)
					}
					duplicate = msg
				}
			case 1:
				if len(messages) > 0 {
					msg := messages[0]
					messages = messages[1:]
					update(msg)
				}
			case 2:
				if duplicate != nil {
					update(duplicate)
				}
			case 3:
				update(tea.KeyPressMsg{Code: tea.KeyF10, Mod: tea.ModAlt})
			case 4:
				name := "M38"
				if v&16 != 0 {
					name = "PARENT"
				}
				update(tea.KeyPressMsg{Code: 'M', Text: name})
			case 5:
				update(tea.KeyPressMsg{Code: tea.KeyEnter})
			case 6:
				update(tea.KeyPressMsg{Code: tea.KeyF1})
			case 7:
				update(tea.WindowSizeMsg{Width: 1 + int(v), Height: 1 + int(v%40)})
			case 8:
				update(HostStopMacroMsg{Reason: "generated explicit host containment"})
			case 9:
				update(tea.KeyPressMsg{Code: tea.KeyF3, Mod: tea.ModShift})
			case 10:
				update(tea.KeyPressMsg{Code: tea.KeyF10})
			case 11:
				if old.uiAuthority != m.uiAuthority {
					before := old.Session().Document().Revision()
					n, c := old.Update(tea.KeyPressMsg{Code: tea.KeyRight})
					if c != nil || n.(Model).Session().Document().Revision() != before {
						t.Fatal("stale model executed work")
					}
				}
			}
			state := m.State()
			state.Macro.Source[0] ^= 255
			if state.Macro.Source == m.State().Macro.Source {
				t.Fatal("public scalar observation aliases model")
			}
		}
		if e := r.Close(); e != nil {
			t.Fatal(e)
		}
		before := r.CompletedMacros()
		for _, c := range commands {
			_ = c()
		}
		after := r.CompletedMacros()
		// Existing effects may be reclassified as closed, but no queued work can add
		// effects after Close or write any original native/macro source.
		var a, b uint64
		for _, x := range before {
			a += x.AppliedWords
		}
		for _, x := range after {
			b += x.AppliedWords
		}
		if a != b {
			t.Fatal("closed queued worker added effects", a, b)
		}
		for name, want := range originals {
			got, e := os.ReadFile(filepath.Join(root, name))
			if e != nil || !bytes.Equal(got, want) {
				t.Fatal("original source changed", name, e)
			}
		}
	})
}
