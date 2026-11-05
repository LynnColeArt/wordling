package tui

import (
	"bytes"
	tea "charm.land/bubbletea/v2"
	"encoding/binary"
	"errors"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
	"time"
)

// Fixed authored ASCII pattern: boundary windows are not a uniform fill. This
// is a HOST parser-valid fixture, not a newly qualified original native writer.
func asciiBody(n int) []byte {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte(33 + (i*37+i/89+i/7919)%94)
	}
	return b
}
func asciiResize(t *testing.T, m Model, w, h int) Model {
	t.Helper()
	n, c := m.Update(tea.WindowSizeMsg{Width: w, Height: h})
	if c != nil {
		t.Fatal("resize IO")
	}
	return n.(Model)
}
func assertASCIIWindow(t *testing.T, m Model, body []byte) {
	t.Helper()
	s := m.Session().Snapshot()
	g := s.Gap
	w := m.State().Width
	start := max(0, g-w/2)
	count := min(w, len(body)-start)
	p, e := m.Session().Present(start, count)
	if e != nil {
		t.Fatal(e)
	}
	if p.CursorGap != g || len(p.Elements) != count {
		t.Fatal("present capture")
	}
	for i, x := range p.Elements {
		if x.TokenIndex != start+i || x.Text != string(body[start+i]) || x.Span.Length != 1 {
			t.Fatal("absolute owner/span", x)
		}
	}
	v := m.View()
	rows := strings.Split(v.Content, "\n")
	upper, lower, y := 1, 3, 1
	if w == 80 && m.State().Height == 25 {
		upper, lower, y = 0, 13, 0
	}
	want := string(body[start : start+count])
	if ansi.Strip(rows[upper]) != want {
		t.Fatalf("g%d w%d upper=%q want=%q", g, w, ansi.Strip(rows[upper]), want)
	}
	if v.Cursor == nil || v.Cursor.X != g-start || v.Cursor.Y != y || v.Cursor.X >= w {
		t.Fatalf("g%d w%d cursor %v", g, w, v.Cursor)
	}
	if s.Reveal {
		text, roles := revealRoles(t, rows[lower])
		expected := want
		if g == len(body) {
			expected += " "
		}
		if text != expected {
			t.Fatalf("g%d w%d lower=%q expected=%q", g, w, text, expected)
		}
		active := activeCells(roles)
		if len(active) != 1 || active[0] != g-start {
			t.Fatalf("g%d w%d active%v", g, w, active)
		}
		if w == 80 && m.State().Height == 25 {
			foot, roles := revealRoles(t, rows[24])
			if foot != "Press Reveal Codes to restore screen"+strings.Repeat(" ", 44) {
				t.Fatal("footer")
			}
			for i, r := range roles {
				want := byte(23)
				if i >= 6 && i < 18 {
					want = 31
				}
				if r != want {
					t.Fatal("footer roles")
				}
			}
		}
	}
}
func TestASCIIFollowPublicBoundaryTraversal(t *testing.T) {
	for _, n := range []int{4097, 16384} {
		t.Run(string(rune(n)), func(t *testing.T) {
			body := asciiBody(n)
			m := revealBody(t, body)
			before, _ := m.Session().Document().Export()
			check := func() {
				for _, w := range []int{1, 2, 7, 80, 4096} {
					m = asciiResize(t, m, w, 25)
					assertASCIIWindow(t, m, body)
				}
				m = asciiResize(t, m, 80, 25)
			}
			for g := 0; g <= n; g++ {
				if g == 0 || g == 4095 || g == 4096 || g == 4097 || g == 8192 || g == n {
					check()
					m = key(t, m, tea.KeyF3, tea.ModAlt, "")
					assertASCIIWindow(t, m, body)
					m = key(t, m, tea.KeyF3, tea.ModAlt, "")
				}
				if g < n {
					m = key(t, m, tea.KeyRight, 0, "")
				}
			}
			for g := n - 1; g >= 0; g-- {
				m = key(t, m, tea.KeyLeft, 0, "")
				if g == 0 || g == 4095 || g == 4096 || g == 4097 || g == 8192 {
					assertASCIIWindow(t, m, body)
				}
			}
			after, _ := m.Session().Document().Export()
			if !bytes.Equal(before, after) {
				t.Fatal("navigation changed native")
			}
		})
	}
}
func TestASCIIWholeNegativeAndObservation(t *testing.T) {
	m := revealBody(t, asciiBody(16385))
	for range 4097 {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	if !strings.Contains(m.View().Content, "cursor beyond bounded") {
		t.Fatal("16385 did not retain explicit refusal")
	}
	for _, at := range []int{0, 4096, 8192, 16383} {
		body := asciiBody(16384)
		body[at] = 0x0a
		m := revealBody(t, body)
		if m.ascii.whole {
			t.Fatal("offscreen HR falsely qualified", at)
		}
		if at == 0 && !m.State().RevealInspection.Partial {
			t.Fatal("first owner partial inspection lost")
		}
		if at >= 4096 && ansi.Strip(strings.Split(m.View().Content, "\n")[0]) != string(body[:80]) {
			t.Fatal("old supported prefix changed", at)
		}
	}
	m = revealBody(t, asciiBody(4097))
	v := m.View()
	s := m.State()
	raw, _ := m.Session().Document().Export()
	for range 5 {
		if m.View().Content != v.Content {
			t.Fatal("observation changed view")
		}
		if m.State().Session.NativeRevision != s.Session.NativeRevision {
			t.Fatal("revision")
		}
	}
	after, _ := m.Session().Document().Export()
	if !bytes.Equal(raw, after) {
		t.Fatal("observation wrote")
	}
}

func TestASCIICacheActualUpdateAndAllocations(t *testing.T) {
	body := asciiBody(16384)
	m := revealBody(t, body)
	if !m.ascii.whole {
		t.Fatal("public Update never qualified")
	}
	fact := m.ascii
	stale := m
	for range 4 {
		m = key(t, m, tea.KeyRight, 0, "")
		m = asciiResize(t, m, 80, 25)
		if m.ascii != fact {
			t.Fatal("unchanged revision not reused")
		}
	}
	n, _ := stale.Update(tea.WindowSizeMsg{Width: 7, Height: 25})
	if n.(Model).ascii != fact || !strings.Contains(n.(Model).State().Notice, "Stale UI") {
		t.Fatal("stale changed cache")
	}
	// A separate parse of equal bytes and a real clear/reacquisition of the same path
	// must not share the opaque revision key. Returned wrappers cannot steer it.
	other := revealBody(t, body)
	if other.ascii.revision == fact.revision {
		t.Fatal("equal-byte revision aliased")
	}
	wrapper := m.Session().Document()
	*wrapper = *other.Session().Document()
	if m.ascii != fact || m.Session().Snapshot().NativeRevision != fact.revision {
		t.Fatal("wrapper rebound captured source")
	}
	m = key(t, m, tea.KeyF7, 0, "")
	m = key(t, m, 'n', 0, "n")
	m = key(t, m, 'n', 0, "n")
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	if m.ascii.checked || m.State().Session.NativeRevision == fact.revision || m.State().Session.HistoryCountKnown || !strings.Contains(m.View().Content, "history=unknown") {
		t.Fatal("actual clear/retrieve uncertainty was hidden")
	}
	m = other // independently acquired equal bytes, not an old Session retry
	fact = m.ascii
	m = key(t, m, tea.KeyInsert, 0, "")
	if m.ascii.checked || !strings.Contains(m.View().Content, "Typeover") {
		t.Fatal("Typeover fact retained")
	}
	m = key(t, m, tea.KeyInsert, 0, "")
	if !m.ascii.whole {
		t.Fatal("Insert reentry failed")
	}
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	m = key(t, m, tea.KeyF3, tea.ModShift, "")
	if m.State().Session.Screen != 2 || m.ascii.checked {
		t.Fatal("Doc2 retained qualification")
	}
	m = key(t, m, tea.KeyF3, tea.ModShift, "")
	if m.State().Session.Screen != 1 || m.ascii.checked || m.State().Session.HistoryCountKnown {
		t.Fatal("Doc1 switch uncertainty lost")
	}
	m = revealBody(t, body)
	// Whole classification is measured on the exact helper called by Update;
	// warmed View checks go through the real public consumer.
	runtime.GC()
	var a, b runtime.MemStats
	runtime.ReadMemStats(&a)
	started := time.Now()
	q := qualifyASCII(m.Session().Document(), m.Session().Snapshot().NativeRevision)
	elapsed := time.Since(started)
	runtime.ReadMemStats(&b)
	if !q.whole || b.TotalAlloc-a.TotalAlloc > 4<<20 {
		t.Fatal("cold classification budget", b.TotalAlloc-a.TotalAlloc)
	}
	t.Logf("cold16384 bytes=%d elapsed=%s", b.TotalAlloc-a.TotalAlloc, elapsed)
	for _, w := range []int{80, 4096} {
		m = asciiResize(t, m, w, 25)
		_ = m.View()
		runtime.GC()
		runtime.ReadMemStats(&a)
		v := m.View()
		runtime.ReadMemStats(&b)
		limit := uint64(128 << 10)
		if w == 4096 {
			limit = 1 << 20
		}
		if b.TotalAlloc-a.TotalAlloc > limit || len(v.Content) > 24<<10 {
			t.Fatalf("warm%d bytes=%d content=%d", w, b.TotalAlloc-a.TotalAlloc, len(v.Content))
		}
		f := m.visibleFrame()
		if len(f.normal)+len(f.reveal) > 12<<10 {
			t.Fatal("combined strings")
		}
		t.Logf("warm%d bytes=%d content=%d", w, b.TotalAlloc-a.TotalAlloc, len(v.Content))
	}
}
func TestASCIIContextEditHeightsAndUnobserved(t *testing.T) {
	body := asciiBody(4097)
	m := revealBody(t, body)
	before := m.ascii.revision
	m = key(t, m, 'X', 0, "X")
	if !m.ascii.whole || m.ascii.revision == before {
		t.Fatal("edit failed invalidation", m.State())
	}
	body = append([]byte{'X'}, body...)
	assertASCIIWindow(t, m, body)
	for _, h := range []int{1, 24, 25, 26} {
		m = asciiResize(t, m, 7, h)
		v := m.View()
		if v.Cursor != nil && (v.Cursor.X >= 7 || v.Cursor.Y >= h) {
			t.Fatal("height caret")
		}
		if h > 3 {
			assertASCIIWindow(t, m, body)
		}
	}
	m = asciiResize(t, m, 80, 25)
	// Actual long macro flow is tested separately; structural capture additionally
	// proves frozen frame wins over a live gap and a stale fact.
	frame := m.visibleFrame()
	frozen := m.View()
	m = key(t, m, tea.KeyRight, 0, "")
	m.macroFrozen = &frame
	m.macroStatus.DisplaySuppressed = true
	if m.View().Content != frozen.Content || *m.View().Cursor != *frozen.Cursor {
		t.Fatal("frozen selected live state")
	}
	// Observations of an unclaimed initial model do not install a cache. Real
	// source acquisition remains exclusively through the authentic Update chain.
	root := t.TempDir()
	r, initial, e := Open(Config{Root: root, Profile: LocalFlat})
	if e != nil {
		t.Fatal(e)
	}
	defer r.Close()
	_ = initial.View()
	_ = initial.State()
	if initial.ascii.checked {
		t.Fatal("observation installed fact")
	}
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	at := int(binary.LittleEndian.Uint32(raw[4:8]))
	raw = append(bytes.Clone(raw[:at]), asciiBody(16384)...)
	if e = os.WriteFile(filepath.Join(root, "ORIGIN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	initial = retrieve(initial)
	if !initial.ascii.whole {
		t.Fatal("real initial read did not install")
	}
	initial = key(t, initial, tea.KeyF10, 0, "")
	if initial.ascii.checked {
		t.Fatal("save prompt retained fact")
	}
	initial = key(t, initial, 'C', 0, "COPY")
	var cmd tea.Cmd
	initial, cmd = press(initial, tea.KeyEnter, 0, "")
	initial = drain(initial, cmd)
	copy, e := os.ReadFile(filepath.Join(root, "COPY"))
	if e != nil || !bytes.Equal(copy, raw) {
		t.Fatal("noedit native publication", e)
	}
	if !initial.ascii.whole {
		t.Fatal("publication reentry not qualified")
	}
}
func TestASCIIWholeCodesAndRawLimit(t *testing.T) {
	for _, code := range [][]byte{{0xc3, 12, 0xc3}, {0xc4, 12, 0xc4}, {0x80}, {0x0a}, {0x0c}} {
		for _, at := range []int{0, 4096, 8192, 16383} {
			b := asciiBody(16384)
			b = append(append(append([]byte{}, b[:at]...), code...), b[at+1:]...)
			m := revealBody(t, b)
			if m.ascii.whole {
				t.Fatalf("code%x at%d qualified", code, at)
			}
		}
	}
	// Eight framed owners exceed the actual E raw-window preflight. No raw
	// scanner or unbounded Present may run to classify this source.
	owner := bytes.Repeat([]byte{0x55}, 65536)
	owner[0] = 0xd0
	owner[1] = 1
	binary.LittleEndian.PutUint16(owner[2:4], 65532)
	binary.LittleEndian.PutUint16(owner[len(owner)-4:len(owner)-2], 65532)
	owner[len(owner)-2] = 1
	owner[len(owner)-1] = 0xd0
	m := revealBody(t, append(bytes.Repeat(owner, 8), asciiBody(4097)...))
	if m.ascii.whole {
		t.Fatal("oversized raw qualified")
	}
	f := m.visibleFrame()
	var fail *document.Failure
	if !errors.As(f.err, &fail) || fail.Category != document.WindowLimit {
		t.Fatal("raw limit lost", f.err)
	}
}

func TestASCIILongActualMacroFrozenFlow(t *testing.T) {
	raw, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	at := int(binary.LittleEndian.Uint32(raw[4:8]))
	raw = append(bytes.Clone(raw[:at]), asciiBody(4097)...)
	_, m, root := macroModel(t, LocalFlat, raw)
	if !m.ascii.whole {
		t.Fatal("loaded long source not qualified")
	}
	macroFile(t, root, "M38.WPM", "docs/research/continuation/macro-session/runs/wp38-run-doc1-01/input/M38.WPM")
	mr, e := os.ReadFile(filepath.Join(root, "M38.WPM"))
	if e != nil {
		t.Fatal(e)
	}
	ma := int(binary.LittleEndian.Uint32(mr[4:8]))
	derived := append([]byte{}, mr[:ma+2]...)
	for range 64 {
		derived = binary.LittleEndian.AppendUint16(derived, uint16('A'))
	}
	derived = binary.LittleEndian.AppendUint16(derived, 0)
	if e = os.WriteFile(filepath.Join(root, "LONG.WPM"), derived, 0600); e != nil {
		t.Fatal(e)
	}
	m, c := queuedMacro(t, m, "LONG")
	found := false
	for count := 0; c != nil && count < 256; count++ {
		n, next := m.Update(c())
		m = n.(Model)
		c = next
		if m.State().Macro.DisplaySuppressed && m.State().Macro.Active {
			found = true
			v := m.View()
			if m.ascii.checked {
				t.Fatal("macro retained live fact")
			}
			m = asciiResize(t, m, 80, 25)
			if m.View().Content != v.Content {
				t.Fatal("actual frozen long source changed")
			}
			break
		}
	}
	if !found {
		t.Fatal("no actual suppressed slice")
	}
	m = drain(m, c)
	if m.State().Macro.Active || m.State().Macro.DisplaySuppressed || m.State().PendingIO != 0 {
		t.Fatal("macro did not settle")
	}
	if m.Session().Document().TokenCount() != 4097+64 {
		t.Fatal("actual macro edits missing")
	}
	// A macro terminal history outcome remains governed by real eligibility;
	// this test does not invent a new-target macro permission or anchor promise.
}
