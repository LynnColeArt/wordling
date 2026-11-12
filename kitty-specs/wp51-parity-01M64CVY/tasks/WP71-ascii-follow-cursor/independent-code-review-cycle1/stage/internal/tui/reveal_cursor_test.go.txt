package tui

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

// Inspect the emitted ANSI, not an exported renderer side channel. The selected
// profile uses explicit SGR color/intensity, not reverse-video guessing.
func revealRoles(t *testing.T, line string) (string, []byte) {
	t.Helper()
	var text strings.Builder
	var roles []byte
	fg, bg := 37, 44
	for i := 0; i < len(line); {
		if line[i] == 27 {
			end := strings.IndexByte(line[i:], 'm')
			if end < 0 {
				t.Fatalf("bad SGR %q", line[i:])
			}
			seq := line[i : i+end+1]
			switch seq {
			case "\x1b[0m":
				fg, bg = 0, 0
			case "\x1b[22;37;44m":
				fg, bg = 37, 44
			case "\x1b[22;97;44m":
				fg, bg = 97, 44
			case "\x1b[22;37;41m":
				fg, bg = 37, 41
			default:
				t.Fatalf("unexpected lower SGR %q", seq)
			}
			i += end + 1
			continue
		}
		role := byte(0)
		if fg == 37 && bg == 44 {
			role = 0x17
		}
		if fg == 97 && bg == 44 {
			role = 0x1f
		}
		if fg == 37 && bg == 41 {
			role = 0x47
		}
		text.WriteByte(line[i])
		roles = append(roles, role)
		i++
	}
	if fg != 0 || bg != 0 {
		t.Fatal("lower style escaped its line")
	}
	return text.String(), roles
}
func activeCells(roles []byte) []int {
	var x []int
	for i, r := range roles {
		if r == 0x47 {
			x = append(x, i)
		}
	}
	return x
}
func TestRevealActiveNativeRangesPublicModel(t *testing.T) {
	_, m, raw, _ := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	want := [][]int{{0}, {1, 2, 3, 4, 5, 6}, {7}, {8}, {9, 10, 11, 12, 13, 14}, {15}, {16}}
	upper := []int{0, 1, 1, 2, 3, 3, 4}
	stale := m
	for g := 0; g <= 6; g++ {
		v := m.View()
		line := strings.Split(v.Content, "\n")[13]
		text, roles := revealRoles(t, line)
		expected := "A[BOLD]BC[bold]D"
		if g == 6 {
			expected += " "
		}
		if text != expected {
			t.Fatalf("g%d text=%q", g, text)
		}
		if got := activeCells(roles); !reflect.DeepEqual(got, want[g]) {
			t.Fatalf("g%d active=%v want%v", g, got, want[g])
		}
		if v.Cursor.X != upper[g] || v.Cursor.Y != 0 {
			t.Fatalf("g%d caret=%v", g, v.Cursor)
		}
		b, _ := m.Session().Document().Export()
		if string(b) != string(raw) {
			t.Fatal("render mutated native")
		}
		if g < 6 {
			m, _ = press(m, tea.KeyRight, 0, "")
		}
	}
	_, roles := revealRoles(t, strings.Split(stale.View().Content, "\n")[3])
	if !reflect.DeepEqual(activeCells(roles), []int{0}) {
		t.Fatal("stale model retargeted")
	}
}
func TestRevealClipContainsStyles(t *testing.T) {
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	m, _ = press(m, tea.KeyRight, 0, "")
	for _, width := range []int{1, 2, 5, 6, 7, 8, 80, 4096} {
		n, c := m.Update(tea.WindowSizeMsg{Width: width, Height: 25})
		if c != nil {
			t.Fatal("resize IO")
		}
		m = n.(Model)
		v := m.View()
		line := strings.Split(v.Content, "\n")[revealTestRow(width)]
		text, roles := revealRoles(t, line)
		if len(text) > width || ansi.StringWidth(line) > width {
			t.Fatalf("width%d %q", width, line)
		}
		if len(activeCells(roles)) != min(6, width-1) {
			t.Fatalf("width%d selected=%v", width, activeCells(roles))
		}
	}
}

// Framed synthetic bodies exercise read-only presentation, not original writer
// admission or original-app semantics. The existing public Parse/Retrieve owns
// all token identity; tests do not manufacture a shadow cursor/model.
func revealBody(t testing.TB, body []byte) Model {
	t.Helper()
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	at := int(binary.LittleEndian.Uint32(raw[4:8]))
	raw = append(bytes.Clone(raw[:at]), body...)
	root := t.TempDir()
	if e = os.WriteFile(filepath.Join(root, "ORIGIN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	runtime, m, e := Open(Config{Root: root, Profile: LocalFlat})
	if e != nil {
		t.Fatal(e)
	}
	t.Cleanup(func() { runtime.Close() })
	m = retrieve(m)
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	return m
}
func TestRevealLiteralDuplicateAndEdgeTokens(t *testing.T) {
	for _, body := range [][]byte{nil, []byte("[BOLD][bold]xyz!"), []byte("Q[bold]R"), {0xc3, 12, 0xc3, 0xc4, 12, 0xc4, 0xc3, 12, 0xc3, 'Y', 0xc4, 12, 0xc4}} {
		m := revealBody(t, body)
		count := m.Session().Document().TokenCount()
		column := 0
		for gap := 0; gap <= count; gap++ {
			line := strings.Split(m.View().Content, "\n")[13]
			_, roles := revealRoles(t, line)
			length := 1
			if gap < count {
				tok, e := m.Session().Document().Token(gap)
				if e != nil {
					t.Fatal(e)
				}
				if tok.Kind == document.BoldOn || tok.Kind == document.BoldOff {
					length = 6
				}
			}
			want := make([]int, length)
			for i := range want {
				want[i] = column + i
			}
			if !reflect.DeepEqual(activeCells(roles), want) {
				t.Fatalf("body%x g%d got%v want%v", body, gap, activeCells(roles), want)
			}
			if gap < count {
				column += length
				m, _ = press(m, tea.KeyRight, 0, "")
			}
		}
	}
}
func TestRevealWindowEndIsNotEOFAndOpaqueRefusal(t *testing.T) {
	m := revealBody(t, bytes.Repeat([]byte{'a'}, document.MaxWindowTokens+1))
	for i := 0; i < document.MaxWindowTokens; i++ {
		m, _ = press(m, tea.KeyRight, 0, "")
	}
	line := strings.Split(m.View().Content, "\n")[13]
	_, roles := revealRoles(t, line)
	if !reflect.DeepEqual(activeCells(roles), []int{40}) {
		t.Fatal("actual owner at4096 missing")
	}
	m, _ = press(m, tea.KeyRight, 0, "")
	_, roles = revealRoles(t, strings.Split(m.View().Content, "\n")[13])
	if !reflect.DeepEqual(activeCells(roles), []int{40}) {
		t.Fatal("trueEOF at4097 blank missing")
	}
	m = revealBody(t, bytes.Repeat([]byte{'a'}, 16385))
	for range 4097 {
		m, _ = press(m, tea.KeyRight, 0, "")
	}
	if !strings.Contains(m.View().Content, "cursor beyond bounded") {
		t.Fatal("over-qualification presentation not refused")
	}
	m = revealBody(t, []byte{'a', 0x80, 'b'})
	if !strings.Contains(m.View().Content, "Unsupported document presentation") {
		t.Fatal("opaque presentation fabricated")
	}
}
func TestRevealObservationsCopiesAndNoEditPublication(t *testing.T) {
	_, m, raw, root := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	before := m.State()
	view := m.View().Content
	d := m.Session().Document()
	other := revealBody(t, []byte("other")).Session().Document()
	*d = *other
	s := m.Session()
	s = otherSession(t)
	_ = s
	for i := 0; i < 10; i++ {
		if m.View().Content != view || !reflect.DeepEqual(m.State(), before) {
			t.Fatal("observation/rebound copy changed captured source")
		}
	}
	n, c := m.Update(tea.WindowSizeMsg{Width: 6, Height: 3})
	if c != nil {
		t.Fatal("resize scheduled IO")
	}
	m = n.(Model)
	got, _ := m.Session().Document().Export()
	if !bytes.Equal(got, raw) {
		t.Fatal("resize changed native")
	}
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, 'C', 0, "COPY")
	m, c = press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	got, e := os.ReadFile(filepath.Join(root, "COPY"))
	if e != nil || !bytes.Equal(got, raw) {
		t.Fatal("style/virtual EOF leaked into noedit save", e)
	}
}
func otherSession(t *testing.T) editor.Session { return revealBody(t, []byte("replacement")).Session() }
func BenchmarkRevealMaximumWindow(b *testing.B) {
	m := revealBody(b, bytes.Repeat([]byte{'Z'}, document.MaxWindowTokens))
	n, _ := m.Update(tea.WindowSizeMsg{Width: 4096, Height: 4096})
	m = n.(Model)
	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.View()
	}
}

func TestRevealBothOriginalAttributeAndNativeSpanWitnesses(t *testing.T) {
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	for gap := 0; gap <= 6; gap++ {
		projection, e := m.Session().Present(0, 6)
		if e != nil {
			t.Fatal(e)
		}
		offsets := []int{324, 325, 328, 329, 330, 333}
		lengths := []int{1, 3, 1, 1, 3, 1}
		for i, tok := range projection.Elements {
			if tok.TokenIndex != i || tok.Span.Offset != offsets[i] || tok.Span.Length != lengths[i] {
				t.Fatal("native span association", tok)
			}
		}
		line := strings.Split(m.View().Content, "\n")[13]
		text, roles := revealRoles(t, line)
		for rep := 1; rep <= 2; rep++ {
			folder := fmt.Sprintf("../../docs/research/continuation/session1/runs/2026-10-31-session1-b01-r%d/CMD51-049/codes-gap-%d/", rep, gap)
			raw, e := os.ReadFile(folder + "vram.bin")
			if e != nil || len(raw) != 4000 {
				t.Fatal(e)
			}
			for col := range len(text) {
				if raw[13*160+col*2] != text[col] || raw[13*160+col*2+1] != roles[col] {
					t.Fatalf("original r%d gap%d column%d char/attribute differs", rep, gap, col)
				}
			}
			var cursor struct{ Row, Column int }
			b, e := os.ReadFile(folder + "cursor.json")
			if e != nil || json.Unmarshal(b, &cursor) != nil {
				t.Fatal("cursor witness", e)
			}
			if cursor.Row != 0 || cursor.Column != m.View().Cursor.X || m.View().Cursor.Y != 0 {
				t.Fatal("original and admitted Wordling row0/caret column binding")
			}
		}
		if gap < 6 {
			m, _ = press(m, tea.KeyRight, 0, "")
		}
	}
}

func TestRevealClippedCodeIntersectionsAndTrueMaximumEOF(t *testing.T) {
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	for range 4 {
		m, _ = press(m, tea.KeyRight, 0, "")
	}
	for _, width := range []int{1, 2, 5, 6, 7, 80, 4096} {
		n, c := m.Update(tea.WindowSizeMsg{Width: width, Height: 25})
		if c != nil {
			t.Fatal("resize IO")
		}
		m = n.(Model)
		_, roles := revealRoles(t, strings.Split(m.View().Content, "\n")[revealTestRow(width)])
		left := max(0, 9-max(1, width/2))
		var want []int
		for col := max(9, left); col < min(15, left+width); col++ {
			want = append(want, col-left)
		}
		if !reflect.DeepEqual(activeCells(roles), want) {
			t.Fatalf("w%d clipped roles=%v want%v", width, activeCells(roles), want)
		}
	}
	m = revealBody(t, bytes.Repeat([]byte{'p'}, document.MaxWindowTokens))
	for range document.MaxWindowTokens {
		m, _ = press(m, tea.KeyRight, 0, "")
	}
	_, roles := revealRoles(t, strings.Split(m.View().Content, "\n")[13])
	if !reflect.DeepEqual(activeCells(roles), []int{40}) {
		t.Fatal("actual maximum-window EOF missing")
	}
}
func TestRevealVirtualOverlayAndFrozenDisplayStaySourceBound(t *testing.T) {
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	m = key(t, m, tea.KeyRight, 0, "")
	m = key(t, m, tea.KeyF4, tea.ModAlt, "")
	for range 4 {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	_, roles := revealRoles(t, strings.Split(m.View().Content, "\n")[3])
	if len(activeCells(roles)) != 0 {
		t.Fatal("Block display fabricated native active span")
	}
	m = key(t, m, tea.KeyBackspace, 0, "")
	m = key(t, m, 'y', 0, "y")
	m = key(t, m, tea.KeyF1, 0, "")
	if m.Session().Snapshot().Mode != editor.HistoryPreview {
		t.Fatal(m.State())
	}
	line := strings.Split(m.View().Content, "\n")[3]
	_, roles = revealRoles(t, line)
	if !strings.Contains(ansi.Strip(line), "[Block]") || len(activeCells(roles)) != 0 {
		t.Fatal("history virtual span styled as current native token")
	}
	// Test-only DISPLAY OFF capture seam: freeze actual panes, then advance the
	// real reducer. A changing gap cannot select cells in the old frozen stream.
	_, m, _, _ = testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	frame := m.visibleFrame()
	frozen := &frame // preserve the same captured pane AND geometry
	before := m.View()
	m = key(t, m, tea.KeyRight, 0, "")
	m = key(t, m, tea.KeyRight, 0, "")
	m.macroFrozen = frozen
	m.macroStatus.DisplaySuppressed = true
	if strings.Split(m.View().Content, "\n")[13] != strings.Split(before.Content, "\n")[13] || *m.View().Cursor != *before.Cursor {
		t.Fatal("DISPLAY OFF mixed live gap with frozen source")
	}
}
func BenchmarkRevealMaximumCodeWindow(b *testing.B) {
	body := bytes.Repeat([]byte{0xc3, 12, 0xc3, 0xc4, 12, 0xc4}, document.MaxWindowTokens/2)
	m := revealBody(b, body)
	n, _ := m.Update(tea.WindowSizeMsg{Width: 4096, Height: 4096})
	m = n.(Model)
	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.View()
	}
}

func TestRevealClippingAllLogicalRoles(t *testing.T) {
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	columns := []int{0, 1, 7, 8, 9, 15, 16}
	for gap := 0; gap <= 6; gap++ {
		n, _ := m.Update(tea.WindowSizeMsg{Width: 80, Height: 25})
		m = n.(Model)
		fullText, fullRoles := revealRoles(t, strings.Split(m.View().Content, "\n")[13])
		for _, width := range []int{1, 2, 3, 5, 6, 7, 80, 4096} {
			n, c := m.Update(tea.WindowSizeMsg{Width: width, Height: 25})
			if c != nil {
				t.Fatal("resize IO")
			}
			m = n.(Model)
			text, roles := revealRoles(t, strings.Split(m.View().Content, "\n")[revealTestRow(width)])
			left := max(0, columns[gap]-max(1, width/2))
			end := min(left+width, len(fullText))
			if text != fullText[left:end] || !reflect.DeepEqual(roles, fullRoles[left:end]) {
				t.Fatalf("g%d w%d clipping lost role/text", gap, width)
			}
		}
		if gap < 6 {
			m = key(t, m, tea.KeyRight, 0, "")
		}
	}
}

// These cases are current, supported native Editing at height25. Their explicit
// width matrix admits anchors only at80; all other widths keep old row3.
func revealTestRow(width int) int {
	if width == 80 {
		return 13
	}
	return 3
}
