package tui

import (
	"bytes"
	tea "charm.land/bubbletea/v2"
	"encoding/binary"
	"errors"
	"fmt"
	"github.com/lynncoleart/wordling/internal/document"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
	"testing"
)

func inspectionModel(t testing.TB, raw []byte) (*Runtime, Model) {
	t.Helper()
	root := t.TempDir()
	if e := os.WriteFile(filepath.Join(root, "ORIGIN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	r, m, e := Open(Config{Root: root, Profile: LocalFlat})
	if e != nil {
		t.Fatal(e)
	}
	t.Cleanup(func() {
		if e := r.Close(); e != nil {
			t.Error(e)
		}
	})
	return r, retrieve(m)
}
func TestInspectionOriginalVisibleAndStateCopies(t *testing.T) {
	for _, family := range []string{"L1-HR", "L2-HP"} {
		for rep := 1; rep <= 2; rep++ {
			t.Run(fmt.Sprintf("%s-%d", family, rep), func(t *testing.T) {
				path := fmt.Sprintf("../../docs/research/continuation/text-layout/runs/wp14-r%02d-%s/BASEA.WP5", rep, family)
				raw, e := os.ReadFile(path)
				if e != nil {
					t.Fatal(e)
				}
				r, m := inspectionModel(t, raw)
				m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
				before := m.Session().Snapshot()
				sourceID, historyID := m.Session().Source().Identity(), m.Session().History().Revision()
				io := r.Completed()
				v := m.View()
				state := m.State()
				inspect := state.RevealInspection
				label := "[HRt]"
				if family == "L2-HP" {
					label = "[HPg]"
				}
				if !inspect.Available || !inspect.Partial || inspect.Revision != before.NativeRevision || v.Cursor != nil {
					t.Fatalf("inspection=%+v cursor=%v", inspect, v.Cursor)
				}
				lines := strings.Split(v.Content, "\n")
				if !strings.Contains(lines[1], "Unsupported") || !strings.Contains(lines[2], "HOST") {
					t.Fatal(v.Content)
				}
				text, roles := revealRoles(t, lines[3])
				at := strings.Index(text, label)
				if at < 0 || at+5 > 80 {
					t.Fatalf("label invisible %q", text)
				}
				for _, role := range roles[at : at+5] {
					if role != 0x1f {
						t.Fatalf("label role%x", role)
					}
				}
				if len(activeCells(roles)) != 0 {
					t.Fatal("invented active cell")
				}
				d := m.Session().Document()
				expected, e := document.InspectRevealCatalogue(d, before.NativeRevision, 0, min(d.TokenCount(), document.MaxWindowTokens))
				if e != nil {
					t.Fatal(e)
				}
				if !reflect.DeepEqual(inspect.Elements, expected.Elements) {
					t.Fatal("owners lost")
				}
				unknown := 0
				for _, entry := range inspect.Elements {
					if entry.Kind == document.Opaque && entry.Text == "" {
						unknown++
						if !strings.Contains(text, fmt.Sprintf("?%d", entry.TokenIndex)) {
							t.Fatal("unknown marker lost")
						}
					}
				}
				if unknown == 0 {
					t.Fatal("missing adversary")
				}
				inspect.Elements[0].Text = "FORGED"
				inspect.Elements[0].Span.Length = 0
				state.RevealInspection.Elements = nil
				if m.View().Content != v.Content || !reflect.DeepEqual(m.State().RevealInspection.Elements, expected.Elements) {
					t.Fatal("caller retargeted visible capture")
				}
				if m.Session().Source().Identity() != sourceID || m.Session().History().Revision() != historyID || !reflect.DeepEqual(m.Session().Snapshot(), before) || !reflect.DeepEqual(r.Completed(), io) {
					t.Fatal("view/state consumed authority or IO")
				}
				out, _ := m.Session().Document().Export()
				if !bytes.Equal(out, raw) {
					t.Fatal("native changed")
				}
				m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
				if m.State().RevealInspection.Available {
					t.Fatal("normal leaked diagnostics")
				}
				m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
				if !strings.Contains(m.View().Content, label) {
					t.Fatal("toggle lost label")
				}
			})
		}
	}
}

func TestInspectionBoundsPreflightBeforePresent(t *testing.T) {
	owner := bytes.Repeat([]byte{0x55}, 65536)
	owner[0] = 0xd0
	owner[1] = 1
	// Synthetic framed-valid payload is an adversary, never an original writer.
	binary.LittleEndian.PutUint16(owner[2:4], 65532)
	binary.LittleEndian.PutUint16(owner[len(owner)-4:len(owner)-2], 65532)
	owner[len(owner)-2] = 1
	owner[len(owner)-1] = 0xd0
	m := revealBody(t, append(bytes.Repeat(owner, 8), 'X'))
	f := m.visibleFrame()
	var fail *document.Failure
	if !errors.As(f.err, &fail) || fail.Category != document.WindowLimit || f.reveal != "" || m.State().RevealInspection.Available || m.View().Cursor != nil {
		t.Fatalf("budget not honest %+v", f)
	}
	var before, after runtime.MemStats
	runtime.GC()
	runtime.ReadMemStats(&before)
	for range 5 {
		m.View()
		m.State()
	}
	runtime.ReadMemStats(&after)
	if after.TotalAlloc-before.TotalAlloc > 256<<10 {
		t.Fatalf("Present copied before E: %d", after.TotalAlloc-before.TotalAlloc)
	}
	// Ineligible State must not create a NEW unbounded normal Present call.
	normal, _ := press(m, tea.KeyF3, tea.ModAlt, "")
	runtime.ReadMemStats(&before)
	for range 5 {
		normal.State()
	}
	runtime.ReadMemStats(&after)
	if after.TotalAlloc-before.TotalAlloc > 64<<10 {
		t.Fatalf("normal State silently materialized native: %d", after.TotalAlloc-before.TotalAlloc)
	}
	// Source-order/actual-window tests also guard a compile-valid zero-count
	// preflight followed by the legacy full-window copy; no unbounded heap case.
}
func TestInspectionIneligibleAndFrozenDiagnostics(t *testing.T) {
	m := revealBody(t, []byte{'A', 0x0a, 'B', 0x80})
	frame := m.visibleFrame()
	if !frame.inspection.Available {
		t.Fatal("setup")
	}
	cases := map[string]func(*Model){"notice": func(x *Model) { x.notice = "error" }, "reconcile": func(x *Model) { x.reconcile = "uncertain" }, "repeat": func(x *Model) { x.repeatEntry = true }, "pending": func(x *Model) { x.unsettled = []operation{{id: 1}} }, "macroCPU": func(x *Model) { x.macroCPU = true }, "macroActive": func(x *Model) { x.macroStatus.Active = true }, "macroWorker": func(x *Model) { x.macroStatus.WorkerPending = true }}
	for name, set := range cases {
		t.Run(name, func(t *testing.T) {
			x := m
			set(&x)
			if x.State().RevealInspection.Available || strings.Contains(x.View().Content, "HOST ?N") {
				t.Fatal("ineligible fallback")
			}
		})
	}
	// This structural frozen test is supplemental, not an original/macro-key run.
	old := frame.inspection
	old.Elements = append([]document.Element(nil), frame.inspection.Elements...)
	m.macroFrozen = &frame
	m.macroStatus.DisplaySuppressed = true
	replacement := revealBody(t, []byte{'X', 0x0c, 'Y'})
	m.session = replacement.session
	if !reflect.DeepEqual(m.State().RevealInspection, old) || !strings.Contains(m.View().Content, "[HRt]") || strings.Contains(m.View().Content, "[HPg]") {
		t.Fatal("live source leaked through frozen frame")
	}
	x := m.State()
	x.RevealInspection.Elements[0].Text = "alias"
	if !reflect.DeepEqual(m.State().RevealInspection, old) {
		t.Fatal("frozen State alias")
	}
}
func TestInspectionPublicModalStaleResizeAndDecoys(t *testing.T) {
	m := revealBody(t, []byte("[HRt]?9"))
	if m.State().RevealInspection.Available {
		t.Fatal("literal ASCII converted")
	}
	m = revealBody(t, []byte{'A', 0xc3, 0x0c, 0xc3, 'B', 0xc4, 0x0c, 0xc4, 0x80, 0x0c})
	f := m.State().RevealInspection
	if !f.Available {
		t.Fatal("setup")
	}
	if f.Elements[1].Kind != document.BoldOn || f.Elements[1].Text != "[BOLD]" || f.Elements[4].Text != "" || f.Elements[5].Text != "[HPg]" {
		t.Fatal(f)
	}
	stale := m
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	if stale.State().RevealInspection.Available {
		t.Fatal("stale model acquired inspection")
	}
	m, _ = press(m, tea.KeyF3, tea.ModAlt, "")
	for _, sz := range []int{0, 1, 7, 20, 80, 4096} {
		n, c := m.Update(tea.WindowSizeMsg{Width: sz, Height: 25})
		m = n.(Model)
		if c != nil {
			t.Fatal("resize IO")
		}
		if !m.State().RevealInspection.Available || m.View().Cursor != nil {
			t.Fatal("resize source")
		}
	}
	m, _ = press(m, tea.KeyF10, 0, "")
	if m.State().RevealInspection.Available {
		t.Fatal("save-name live fallback")
	}
	m, _ = press(m, tea.KeyF1, 0, "")
	if !m.State().RevealInspection.Available {
		t.Fatal("cancel did not restore")
	}
	d := m.Session().Document()
	*d = document.Document{}
	if !m.State().RevealInspection.Available {
		t.Fatal("public wrapper retarget")
	}
}
func TestInspectionExpandedBoundsAndEOF(t *testing.T) {
	m := revealBody(t, append(bytes.Repeat([]byte{0x80}, document.MaxWindowTokens), 0x0a))
	x := m.State().RevealInspection
	if !x.Available || x.TrueEOF || len(x.Elements) != 4096 {
		t.Fatal(x)
	}
	n := revealBody(t, []byte{0x80})
	if !n.State().RevealInspection.TrueEOF || len(activeCellsMust(t, n)) != 0 {
		t.Fatal("EOF invented active")
	}
	for _, bad := range []document.CatalogueInspection{{Elements: make([]document.Element, 4097)}, {Elements: []document.Element{{Kind: document.Opaque, TokenIndex: -1}}}, {Elements: []document.Element{{Kind: document.ASCII, Text: strings.Repeat("x", MaxInspectionRenderBytes+1)}}}} {
		if _, e := inspectionRuns(bad); e == nil {
			t.Fatal("render cap/invalid guard")
		}
	}
}
func activeCellsMust(t *testing.T, m Model) []int {
	_, roles := revealRoles(t, strings.Split(m.View().Content, "\n")[3])
	return activeCells(roles)
}

func TestInspectionPublicVirtualRepeatPendingAndZero(t *testing.T) {
	var zero Model
	if zero.State().RevealInspection.Available || zero.View().Cursor != nil {
		t.Fatal("zero state")
	}
	m := revealBody(t, []byte{'A', 0x0a, 'B'})
	m, _ = press(m, tea.KeyEscape, 0, "")
	if m.State().RevealInspection.Available {
		t.Fatal("repeat-entry live fallback")
	}
	_, m, _, _ = testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	m = key(t, m, tea.KeyRight, 0, "")
	m = key(t, m, tea.KeyF4, tea.ModAlt, "")
	if m.State().RevealInspection.Available {
		t.Fatal("selection inspected underlying native")
	}
	for range 4 {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	m = key(t, m, tea.KeyBackspace, 0, "")
	m = key(t, m, 'y', 0, "y")
	m = key(t, m, tea.KeyF1, 0, "")
	if m.State().RevealInspection.Available || !strings.Contains(m.View().Content, "[Block]") {
		t.Fatal("virtual history replaced")
	}
	_, m, _, _ = testModel(t)
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'O', 0, "ORIGIN")
	m, c := press(m, tea.KeyEnter, 0, "")
	if c == nil || m.State().RevealInspection.Available {
		t.Fatal("pending read inspected")
	}
	m = drain(m, c)
	if m.State().RevealInspection.Available {
		t.Fatal("pending startup Retrieve leaked diagnostics")
	}
}
func TestInspectionWholeOpaquePayload(t *testing.T) {
	owner := bytes.Repeat([]byte{0x55}, 32)
	owner[0] = 0xd0
	owner[1] = 1
	binary.LittleEndian.PutUint16(owner[2:4], 28)
	binary.LittleEndian.PutUint16(owner[28:30], 28)
	owner[30] = 1
	owner[31] = 0xd0
	owner[10] = 0x0a
	owner[11] = 0x0c
	m := revealBody(t, append(owner, 0x0a))
	x := m.State().RevealInspection
	if len(x.Elements) != 2 || x.Elements[0].Text != "" || x.Elements[0].Span.Length != 32 || x.Elements[1].Text != "[HRt]" {
		t.Fatal("inner scan/split", x)
	}
	text, _ := revealRoles(t, strings.Split(m.View().Content, "\n")[3])
	if text != "?0[HRt]" {
		t.Fatal(text)
	}
}
func BenchmarkInspectionRefusedWindow(b *testing.B) {
	owner := bytes.Repeat([]byte{0x55}, 65536)
	owner[0] = 0xd0
	owner[1] = 1
	binary.LittleEndian.PutUint16(owner[2:4], 65532)
	binary.LittleEndian.PutUint16(owner[len(owner)-4:len(owner)-2], 65532)
	owner[len(owner)-2] = 1
	owner[len(owner)-1] = 0xd0
	m := revealBody(b, append(bytes.Repeat(owner, 8), 'X'))
	b.ResetTimer()
	b.ReportAllocs()
	for range b.N {
		m.visibleFrame()
	}
}
