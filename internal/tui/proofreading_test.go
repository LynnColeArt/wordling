package tui

import (
	"bytes"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
)

func TestProofContextKeepsOriginalFocusAndPositions(t *testing.T) {
	_, m := openProofRuntime(t, t.TempDir())
	m = inputKeys(t, m, textKey("The quik fox."), tea.Key{Code: tea.KeyF2, Mod: tea.ModCtrl})
	assertScreenRows(t, m, map[int]string{0: "The quik fox.", 24: "Check: 1 Word; 2 Page; 3 Document;"})
	if cursor := m.View().Cursor; cursor == nil || cursor.X != 13 || cursor.Y != 0 || cursor.Shape != tea.CursorUnderline {
		t.Fatalf("Check cursor differs from original: %+v", cursor)
	}
	m = inputKeys(t, m, textKey("3"))
	assertScreenRows(t, m, map[int]string{
		0: "The quik fox.", 11: `Doc 1 Pg 1 Ln 1" Pos 1.4"`, 12: "{    ▲", 14: "  A. ", 24: "Not Found:",
	})
	if cursor := m.View().Cursor; cursor == nil || cursor.X != 76 || cursor.Y != 24 {
		t.Fatalf("Not Found cursor differs from original: %+v", cursor)
	}
	if !strings.Contains(strings.Split(m.View().Content, "\n")[0], revealActive+"quik") {
		t.Fatal("proof question lacks original red native range")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF7))
	if m.Session().ProofStatus().Phase != editor.ProofQuestioning {
		t.Fatal("F7 at a question must leave the question open")
	}
	m = inputKeys(t, m, textKey("4"))
	assertScreenRows(t, m, map[int]string{0: "The quik fox.", 24: "Spell Edit:  Press Exit when done"})
	if cursor := m.View().Cursor; cursor == nil || cursor.X != 4 || cursor.Y != 0 {
		t.Fatalf("Spell Edit lost its document caret: %+v", cursor)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF7), everydayKey(tea.KeyF1))
	assertScreenRows(t, m, map[int]string{24: "Word count: 2        Press any key to continue"})
	m = inputKeys(t, m, everydayKey(tea.KeyF3))
	assertScreenRows(t, m, map[int]string{0: "File Edit", 1: "The quik fox."})
	if m.help.active || m.Session().Snapshot().Gap != 4 {
		t.Fatal("acknowledgement leaked F3 to Help or lost the document position")
	}
}

func TestProofResizeKeepsHiddenChoicesOutOfDocument(t *testing.T) {
	_, m := openProofRuntime(t, t.TempDir())
	m = startZorbly(t, m)
	before, err := m.Session().Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	next, _ := m.Update(tea.WindowSizeMsg{Width: 40, Height: 12})
	m = inputKeys(t, next.(Model), textKey("4"), textKey("a"))
	assertScreenRows(t, m, map[int]string{0: "Proofreading active"})
	if m.Session().ProofStatus().Phase != editor.ProofQuestioning {
		t.Fatal("invisible choice reached Spell Edit")
	}
	next, _ = m.Update(tea.WindowSizeMsg{Width: 80, Height: 25})
	m = next.(Model)
	assertScreenRows(t, m, map[int]string{0: "zorbly", 24: "Not Found:"})
	after, err := m.Session().Document().Export()
	if err != nil || !bytes.Equal(before, after) {
		t.Fatal("resize or hidden text changed the document")
	}
}

func TestOriginalCheckMnemonicsOnlyInCheck(t *testing.T) {
	for _, tc := range []struct {
		key   string
		phase editor.ProofreadingPhase
		scope editor.ProofreadingScope
	}{
		{"w", editor.ProofQuestioning, editor.ProofWord},
		{"P", editor.ProofQuestioning, editor.ProofPage},
		{"d", editor.ProofQuestioning, editor.ProofDocument},
		{"N", editor.ProofDictionaryName, 0},
		{"l", editor.ProofLookupInput, 0},
		{"C", editor.ProofCompleteAck, editor.ProofCount},
	} {
		t.Run(tc.key, func(t *testing.T) {
			_, m := openProofRuntime(t, t.TempDir())
			m = inputKeys(t, m, textKey("The quik fox."), everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyUp))
			for range 4 {
				m = inputKeys(t, m, everydayKey(tea.KeyRight))
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF2, Mod: tea.ModCtrl}, textKey(tc.key))
			view := m.Session().ProofStatus()
			if view.Phase != tc.phase || view.Scope != tc.scope {
				t.Fatalf("Check mnemonic %s did not enter its original phase: %+v", tc.key, view)
			}
			switch tc.phase {
			case editor.ProofDictionaryName, editor.ProofLookupInput:
				m = inputKeys(t, m, textKey("c"))
				if after := m.Session().ProofStatus(); after.Phase != tc.phase || after.Draft != "c" {
					t.Fatalf("literal input left its active draft: %+v", after)
				}
			case editor.ProofQuestioning:
				if len(view.Suggestions) < 3 {
					t.Fatal("admitted suggestion page does not contain C")
				}
				want := view.Suggestions[2]
				m = inputKeys(t, m, textKey("c"))
				raw, err := m.Session().Document().Export()
				if err != nil || !bytes.HasSuffix(raw, []byte("The "+want+" fox.")) {
					t.Fatalf("C did not choose its visible suggestion %q: %v", want, err)
				}
			}
		})
	}
}
