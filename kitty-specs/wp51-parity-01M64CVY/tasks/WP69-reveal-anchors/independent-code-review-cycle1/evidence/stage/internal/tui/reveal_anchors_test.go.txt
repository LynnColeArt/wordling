package tui

import (
	"bytes"
	tea "charm.land/bubbletea/v2"
	"fmt"
	"github.com/charmbracelet/x/ansi"
	"os"
	"reflect"
	"strings"
	"testing"
)

func anchorFooter(t *testing.T, m Model) {
	t.Helper()
	v := m.View()
	lines := strings.Split(v.Content, "\n")
	if len(lines) != 25 {
		t.Fatalf("anchor rows=%d", len(lines))
	}
	text, roles := revealRoles(t, lines[24])
	if text != "Press Reveal Codes to restore screen"+strings.Repeat(" ", 44) {
		t.Fatalf("footer cells %q", text)
	}
	for i, r := range roles {
		want := byte(0x17)
		if i >= 6 && i < 18 {
			want = 0x1f
		}
		if r != want {
			t.Fatalf("footer%d role%x", i, r)
		}
	}
	if v.Cursor == nil || v.Cursor.Y != 0 {
		t.Fatalf("anchor caret %v", v.Cursor)
	}
	for _, y := range []int{11, 12} {
		if strings.TrimSpace(ansi.Strip(lines[y])) != "" {
			t.Fatal("invented status/ruler")
		}
	}
}
func TestAnchorPublicSevenGaps(t *testing.T) {
	r, m, raw, _ := testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	before := m.State()
	receipts := r.Completed()
	native := m.Session().Source().Identity()
	upper := []int{0, 1, 1, 2, 3, 3, 4}
	ranges := [][2]int{{0, 1}, {1, 7}, {7, 8}, {8, 9}, {9, 15}, {15, 16}, {16, 17}}
	check := func(g int) {
		t.Helper()
		anchorFooter(t, m)
		v := m.View()
		lines := strings.Split(v.Content, "\n")
		text, roles := revealRoles(t, lines[13])
		if ansi.Strip(lines[0]) != "ABCD" || v.Cursor.X != upper[g] {
			t.Fatal("upper/caret", g, v.Cursor, lines[0])
		}
		var want []int
		for i := ranges[g][0]; i < ranges[g][1]; i++ {
			want = append(want, i)
		}
		if !reflect.DeepEqual(activeCells(roles), want) {
			t.Fatalf("gap%d active%v", g, activeCells(roles))
		}
		for rep := 1; rep <= 2; rep++ {
			b, e := os.ReadFile(fmt.Sprintf("../../docs/research/continuation/session1/runs/2026-10-31-session1-b01-r%d/CMD51-049/codes-gap-%d/vram.bin", rep, g))
			if e != nil || len(b) != 4000 {
				t.Fatal(e)
			}
			for c := range text {
				if b[13*160+c*2] != text[c] || b[13*160+c*2+1] != roles[c] {
					t.Fatal("original native role/cell mismatch", rep, g, c)
				}
			}
		}
		got, _ := m.Session().Document().Export()
		if !bytes.Equal(got, raw) || m.Session().Source().Identity() != native || m.State().Session.NativeRevision != before.Session.NativeRevision || m.State().Session.Dirty != before.Session.Dirty || !reflect.DeepEqual(r.Completed(), receipts) {
			t.Fatal("view/navigation mutated source or IO")
		}
		observed := m.State()
		for range 3 {
			_ = m.View()
			_ = m.State()
		}
		if !reflect.DeepEqual(observed, m.State()) {
			t.Fatal("observation mutation")
		}
	}
	for g := 0; g <= 6; g++ {
		check(g)
		if g < 6 {
			m = key(t, m, tea.KeyRight, 0, "")
		}
	}
	for g := 5; g >= 0; g-- {
		m = key(t, m, tea.KeyLeft, 0, "")
		check(g)
	}
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	v := m.View()
	if v.Cursor.Y != 0 || strings.Contains(v.Content, "Press Reveal Codes") || strings.Contains(v.Content, "[BOLD]") {
		t.Fatal("off left stale Reveal content")
	}
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	check(0)
}
func TestAnchorStartupTypeoverMenuResize(t *testing.T) {
	_, m := menuModel(t)
	before := m.View()
	if before.Cursor.Y != 1 {
		t.Fatal("pristine legacy base")
	}
	m = menuStep(t, m, menuToggle())
	shown := m.View()
	if !reflect.DeepEqual(before.Cursor, shown.Cursor) || strings.Join(strings.Split(before.Content, "\n")[1:], "\n") != strings.Join(strings.Split(shown.Content, "\n")[1:], "\n") {
		t.Fatal("menu base jump")
	}
	m = menuStep(t, m, menuToggle())
	if m.View().Content != before.Content {
		t.Fatal("menu hide changed base")
	}
	initial := m.State().Session
	m = key(t, m, 'X', 0, "X")
	if m.View().Cursor.Y != 0 || m.State().MenuBar.Available || m.State().Session.NativeRevision == initial.NativeRevision {
		t.Fatal("first ordinary edit failed anchor entry")
	}
	m = key(t, m, tea.KeyInsert, 0, "")
	if m.View().Cursor.Y != 1 || !strings.Contains(m.View().Content, "Typeover") {
		t.Fatal("active Typeover hidden")
	}
	m = key(t, m, tea.KeyInsert, 0, "")
	if m.View().Cursor.Y != 0 || strings.Contains(m.View().Content, "Typeover") {
		t.Fatal("Insert restoration")
	}
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	anchorFooter(t, m)
	for _, size := range [][2]int{{1, 1}, {79, 25}, {80, 24}, {81, 25}, {80, 26}, {80, 25}} {
		state := m.State().Session
		n, c := m.Update(tea.WindowSizeMsg{Width: size[0], Height: size[1]})
		m = n.(Model)
		if c != nil || !reflect.DeepEqual(state, m.State().Session) {
			t.Fatal("resize changed native")
		}
		if size == [2]int{80, 25} {
			anchorFooter(t, m)
		} else if strings.Contains(m.View().Content, "\n"+strings.Repeat(" ", 44)) {
			t.Fatal("anchored footer at unsupported size")
		}
	}
}
func TestAnchorIndependentInputsAndRefusals(t *testing.T) {
	for _, body := range [][]byte{nil, []byte("[BOLD][bold]Other"), {'Z', 0xc3, 12, 0xc3, 'Y', 0xc4, 12, 0xc4, 'X'}} {
		m := revealBody(t, body)
		anchorFooter(t, m)
		if strings.Contains(m.View().Content, "ABCD") {
			t.Fatal("fixed witness output")
		}
		b, _ := m.Session().Document().Export()
		_ = m.View()
		after, _ := m.Session().Document().Export()
		if !bytes.Equal(b, after) {
			t.Fatal("padding leaked")
		}
	}
	m := revealBody(t, []byte{'A', 0x0a, 'B'})
	if m.View().Cursor != nil || !strings.Contains(m.View().Content, "Partial Reveal inspection") || strings.Contains(m.View().Content, strings.Repeat(" ", 44)) {
		t.Fatal("partial inspection lost truthful fallback")
	}
	_, m, _, _ = testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	stale := m
	m = key(t, m, tea.KeyRight, 0, "")
	if stale.View().Cursor.Y != 1 {
		t.Fatal("stale value claimed current anchors")
	}
	m = key(t, m, tea.KeyF10, 0, "")
	if m.View().Cursor == nil || m.View().Cursor.Y != 4 || !strings.Contains(m.View().Content, "Document to be saved") {
		t.Fatal("modal caret/prompt hidden")
	}
}
func TestAnchorFrozenGeometry(t *testing.T) {
	// Supplemental structural freeze: genuine current public capture, never a user macro witness.
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	f := m.visibleFrame()
	before := m.View()
	m = key(t, m, tea.KeyRight, 0, "")
	m.macroFrozen = &f
	m.macroStatus.DisplaySuppressed = true
	if m.View().Content != before.Content || !reflect.DeepEqual(m.View().Cursor, before.Cursor) {
		t.Fatal("frozen source/layout uses live gap")
	}
	n, c := m.Update(tea.WindowSizeMsg{Width: 80, Height: 24})
	m = n.(Model)
	if c != nil || m.View().Cursor.Y != 0 {
		t.Fatal("resize chose live fallback geometry")
	}
}

func TestAnchorUnknownHistoryRemainsVisible(t *testing.T) {
	_, m, _, root := testModel(t)
	// Existing original history witness and its authentic qualified public path;
	// plain ORIGIN does not grant this code-deletion/history lifecycle.
	raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-direct-normal-delete-on-r1/N0000.WP5")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(root+"/ORIGIN", raw, 0600); e != nil {
		t.Fatal(e)
	}
	m = retrieve(m)
	if m.View().Cursor.Y != 0 {
		t.Fatal("loaded anchor prerequisite")
	}
	m = key(t, m, tea.KeyDelete, 0, "")
	m = browseModel(t, m, 3)
	for m.Session().Snapshot().Gap < 1 {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	m = key(t, m, tea.KeyDelete, 0, "")
	m = key(t, m, 'y', 0, "y") // answer actual native-code deletion question
	if m.State().Session.HistoryCountKnown || !strings.Contains(m.View().Content, "history=unknown") || m.View().Cursor.Y != 1 {
		t.Fatal("real post-deletion uncertainty concealed", m.State())
	}
	before := m.State()
	_ = m.View()
	if !reflect.DeepEqual(before, m.State()) {
		t.Fatal("uncertainty observation changed history")
	}
}
