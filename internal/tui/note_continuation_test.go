package tui

import (
	"bytes"
	"fmt"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestFootnoteContinuationMatchesDOS(t *testing.T) {
	for _, tc := range []struct {
		name, value string
		rows        int
	}{{"ROOM", "1.25", 0}, {"SPLIT", "0.5", 6}, {"ASYM", "0.5", 5}, {"KEEP", "1.25", 6}} {
		t.Run(tc.name, func(t *testing.T) {
			m, _ := everydayUI(t)
			enter, f7 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
			format, note := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}, tea.Key{Code: tea.KeyF7, Mod: tea.ModCtrl}
			if tc.rows > 0 {
				m = inputKeys(t, m, format, textKey("2"), textKey("5"), textKey("2\""), enter, textKey("7\""), enter, f7)
			}
			m = inputKeys(t, m, note, textKey("1"), textKey("4"), textKey("2"))
			if !strings.Contains(ansi.Strip(m.View().Content), "Amount of Note to Keep Together") {
				t.Fatal(m.View().Content)
			}
			m = inputKeys(t, m, textKey(tc.value), enter, f7)
			for i := range tc.rows {
				m = inputKeys(t, m, textKey(fmt.Sprintf("Row %d", i+1)), enter)
			}
			m = inputKeys(t, m, textKey("Body"), note, textKey("1"), textKey("1"))
			for _, s := range []string{"First", "Second", "Third", "Fourth", "Fifth"} {
				m = inputKeys(t, m, textKey(s+" note line"), enter)
			}
			m = inputKeys(t, m, textKey("Last note line"), f7)
			if m.note.notice != "" || m.notice != "" {
				t.Fatal(m.note.notice, m.notice)
			}
			if tc.rows > 0 {
				m = inputKeys(t, m, enter, textKey("After note"))
			}
			normalize := func(body string) []byte {
				b := []byte(body)
				i := bytes.Index(b, []byte{0xd6, 0, 0x74, 0})
				if i < 0 {
					i = bytes.Index(b, []byte{0xd6, 0, 0x96, 0})
				}
				if i >= 0 {
					j := i + 17
					if b[i+7] == 1 {
						j += 2
					}
					b[j], b[j+1] = 0, 0
				}
				return b
			}
			got, want := normalize(hBoldBody(t, m)), normalize(lineFormatBody(t, "mission1-note-continuation/"+tc.name+".WP"))
			if !bytes.Equal(got, want) {
				t.Fatalf("body %x\nwant %x\n%s", got, want, m.notice)
			}
		})
	}
}
