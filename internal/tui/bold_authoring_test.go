package tui

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	goruntime "runtime"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/wp51"
)

const (
	hBoldOn  = "\xc3\x0c\xc3"
	hBoldOff = "\xc4\x0c\xc4"
)

func hBoldUpdate(t *testing.T, m Model, msg tea.Msg) Model {
	t.Helper()
	next, cmd := m.Update(msg)
	if cmd != nil {
		t.Fatalf("unexpected queued command after %T", msg)
	}
	return next.(Model)
}

func hBoldPress(t *testing.T, m Model, key tea.KeyPressMsg) Model {
	t.Helper()
	return hBoldUpdate(t, m, key)
}

func hBoldSetup(t *testing.T) (*Runtime, Model, string) {
	t.Helper()
	r, m, root := newModel(t)
	return r, hBoldUpdate(t, m, tea.WindowSizeMsg{Width: 80, Height: 25}), root
}

func hBoldNative(t *testing.T, m Model) []byte {
	t.Helper()
	raw, err := m.Session().Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	return raw
}

func hBoldBody(t *testing.T, m Model) string {
	t.Helper()
	d := m.Session().Document()
	c, err := d.CursorAt(0)
	if err != nil {
		t.Fatal(err)
	}
	start, err := c.Offset()
	if err != nil {
		t.Fatal(err)
	}
	return string(hBoldNative(t, m)[start:])
}

func hBoldActive(m Model) bool {
	s := m.Session()
	_, active := s.History().ActiveBold(s.Document())
	return active
}

func hBoldSameSession(t *testing.T, before, after Model) {
	t.Helper()
	if !reflect.DeepEqual(before.Session().Snapshot(), after.Session().Snapshot()) ||
		before.Session().History().Revision() != after.Session().History().Revision() ||
		!bytes.Equal(hBoldNative(t, before), hBoldNative(t, after)) {
		t.Fatal("refusal or host observation changed authoritative Bold session")
	}
}

func hBoldDrain(t *testing.T, m Model, cmd tea.Cmd) Model {
	t.Helper()
	for n := 0; cmd != nil; n++ {
		if n == 12 {
			t.Fatal("unexpected command chain length")
		}
		next, c := m.Update(cmd())
		m, cmd = next.(Model), c
	}
	return m
}

func hBoldClosed(t *testing.T, m Model, text string) Model {
	t.Helper()
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: rune(text[0]), Text: text})
	return hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
}

func TestBoldModelLifecycle(t *testing.T) {
	_, m, root := hBoldSetup(t)
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: 'P', Text: "P"})
	before := m
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	s := m.State().Session
	if !hBoldActive(m) || hBoldBody(t, m) != "P"+hBoldOn+hBoldOff || s.Gap != 2 ||
		s.Revision != before.State().Session.Revision+1 || s.Provenance != editor.Bold ||
		s.HistoryQualified || s.HistoryCountKnown || m.State().PendingIO != 0 {
		t.Fatal("bare F6 did not open the real native span")
	}
	empty := hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, m, empty)
	if !strings.Contains(empty.State().Notice, "EmptyBoldSpan") {
		t.Fatal("empty close lacked explicit native refusal")
	}
	m = hBoldPress(t, empty, tea.KeyPressMsg{Code: 'a', Text: "ab"})
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF3, Mod: tea.ModAlt})
	visible := strings.Split(m.View().Content, "\n")
	if len(visible) < 4 || ansi.Strip(visible[1]) != "Pab" ||
		strings.TrimRight(ansi.Strip(visible[3]), " ") != "P[BOLD]ab[bold]" || m.View().Cursor.Y != 1 {
		t.Fatalf("unknown history did not keep native legacy panes: %q", visible)
	}
	before = m
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	if hBoldActive(m) || !m.State().Session.Reveal ||
		m.State().Session.NativeRevision != before.State().Session.NativeRevision ||
		m.State().Session.Revision != before.State().Session.Revision || m.State().Session.Gap != 5 {
		t.Fatal("nonempty F6 did not close on the same native revision")
	}
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF3, Mod: tea.ModAlt})
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: 's', Text: "s"})
	m = hBoldClosed(t, m, "YZ")
	if hBoldBody(t, m) != "P"+hBoldOn+"ab"+hBoldOff+"s"+hBoldOn+"YZ"+hBoldOff {
		t.Fatal("wrong plain suffix or second native pair")
	}
	hBoldSameSession(t, m, hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6}))
	files, err := os.ReadDir(root)
	if err != nil || len(files) != 0 {
		t.Fatal("Bold emitted a filesystem effect", files, err)
	}
}

func TestBoldMalformedKeysNeverAliasText(t *testing.T) {
	_, m, _ := hBoldSetup(t)
	for _, key := range []tea.KeyPressMsg{{Code: tea.KeyF6, Mod: tea.ModAlt},
		{Code: tea.KeyF6, Text: "x"}, {Code: tea.KeyF6, IsRepeat: true}} {
		next := hBoldPress(t, m, key)
		hBoldSameSession(t, m, next)
		m = next
	}
	if m.State().Notice == "" {
		t.Fatal("malformed input was silently accepted")
	}
	m = hBoldClosed(t, m, "R")
	if hBoldBody(t, m) != hBoldOn+"R"+hBoldOff || m.State().Notice != "" {
		t.Fatal("benign host diagnostic trapped legitimate Bold")
	}
}

func TestBoldCharacterCountAndMenuOrdering(t *testing.T) {
	for _, menu := range []bool{false, true} {
		_, m, _ := hBoldSetup(t)
		if menu {
			m = hBoldPress(t, m, tea.KeyPressMsg{Code: '=', Mod: tea.ModAlt})
			if !m.State().MenuBar.Visible {
				t.Fatal("real startup menu did not open")
			}
		} else {
			m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyEscape})
			m = hBoldPress(t, m, tea.KeyPressMsg{Code: '5', Text: "5"})
			if !m.characterRepeat.active || m.characterRepeat.count != 5 {
				t.Fatal("real WP73 count did not arm")
			}
		}
		next := hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
		hBoldSameSession(t, m, next)
		if menu && !next.State().MenuBar.Visible || !menu && next.characterRepeat.active {
			t.Fatal("F6 did not use the existing menu/count disposition")
		}
		if menu {
			next = hBoldPress(t, next, tea.KeyPressMsg{Code: '=', Mod: tea.ModAlt})
		}
		next = hBoldClosed(t, next, "R")
		next = hBoldPress(t, next, tea.KeyPressMsg{Code: tea.KeyEscape})
		if next.characterRepeat.active {
			t.Fatal("native Bold entered pristine WP73 Repeat")
		}
	}
}

func TestBoldObserverAndAdministrativeRecovery(t *testing.T) {
	_, m, _ := hBoldSetup(t)
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	if !hBoldActive(m) {
		t.Fatal("expected genuine initial active owner")
	}
	for range 3 {
		_ = m.State()
		_ = m.View()
	}
	wrapper := m.Session().Document()
	*wrapper = document.Document{}
	_ = m.Session().History()
	for _, msg := range []tea.Msg{tea.WindowSizeMsg{Width: 65, Height: 20},
		tea.KeyReleaseMsg{Code: tea.KeyF6}, tea.PasteStartMsg{}, tea.PasteMsg{Content: "p"},
		tea.PasteEndMsg{}, tea.KeyboardEnhancementsMsg{}, tea.EnvMsg{}, tea.ColorProfileMsg{}, struct{}{}} {
		next := hBoldUpdate(t, m, msg)
		hBoldSameSession(t, m, next)
		m = next
	}
	refused := hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF10})
	hBoldSameSession(t, m, refused)
	m = hBoldPress(t, refused, tea.KeyPressMsg{Code: 'r', Text: "rv"})
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	if hBoldActive(m) || hBoldBody(t, m) != hBoldOn+"rv"+hBoldOff || m.State().Notice != "" {
		t.Fatal("observation or administrative message prevented recovery")
	}
}

func TestBoldCurrentUIAndIdleFences(t *testing.T) {
	r, m, _ := hBoldSetup(t)
	stale := m
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: 'X', Text: "X"})
	next := hBoldPress(t, stale, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, stale, next)
	if !strings.Contains(next.State().Notice, "Stale UI") {
		t.Fatal("stale model did not use claimUI refusal")
	}
	// Supplemental private impossible conjunctions bind the actual current
	// UI owner but retain incompatible runtime state.
	for _, set := range []func(*Model){
		func(m *Model) { m.macroDeferred = &macroIOReceipt{} },
		func(m *Model) { m.macroFrozen = &macroPane{} },
		func(m *Model) { m.macroStatus.Terminal = true },
	} {
		private := m
		set(&private)
		next := hBoldPress(t, private, tea.KeyPressMsg{Code: tea.KeyF6})
		hBoldSameSession(t, private, next)
		m.uiAuthority = next.uiAuthority
	}
	r.mu.Lock()
	r.results = append(r.results, editor.Result{Kind: editor.Observe})
	r.mu.Unlock()
	next = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, m, next)
	if err := r.Close(); err != nil {
		t.Fatal(err)
	}
	hBoldSameSession(t, next, hBoldPress(t, next, tea.KeyPressMsg{Code: tea.KeyF6}))
}

func TestBoldRealFrozenMacro(t *testing.T) {
	_, m, _ := newDerivedMacroModel(t, uint16(0xfc0c), strings.Repeat("Q", 160))
	m, cmd := queuedMacro(t, m, "ROOT")
	for n := 0; cmd != nil && n < 64; n++ {
		next, c := m.Update(cmd())
		m, cmd = next.(Model), c
		if m.State().Macro.Active && m.State().Macro.DisplaySuppressed && m.State().Macro.AppliedWords > 0 {
			break
		}
	}
	if cmd == nil || !m.State().Macro.DisplaySuppressed || m.macroFrozen == nil {
		t.Fatal("no real frozen macro frame")
	}
	frame := m.visibleFrame()
	next := hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, m, next)
	if !reflect.DeepEqual(frame, next.visibleFrame()) || !next.State().Macro.Active {
		t.Fatal("F6 disturbed genuine frozen display")
	}
	next = hBoldUpdate(t, next, HostStopMacroMsg{Reason: "bounded Bold test containment"})
	_ = hBoldDrain(t, next, cmd)
}

func TestBoldModelRootedSaveAndReceipts(t *testing.T) {
	r, m, root := hBoldSetup(t)
	m = hBoldClosed(t, m, "xy")
	raw := hBoldNative(t, m)
	m, c := firstSave(t, m, "FIRST")
	before := m
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, before, m)
	m = hBoldDrain(t, m, c)
	if m.State().Session.NewPhase != editor.NewAnchored || m.Session().Source() == nil ||
		m.State().Session.Name != "FIRST" || m.State().Session.Dirty || m.State().PendingIO != 0 {
		t.Fatal("actual first publication/read receipt did not settle", m.State())
	}
	source := m.Session().Source()
	identity := source.Identity()
	*source = storage.Document{}
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF10})
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: 'S', Text: "SECOND"})
	m, c = press(m, tea.KeyEnter, 0, "")
	m = hBoldDrain(t, m, c)
	if m.State().Session.Name != "SECOND" || m.State().Session.SaveState != editor.NewNamePublished ||
		m.State().PendingIO != 0 || m.Session().Source().Identity() != identity {
		t.Fatal("no-edit Save As did not preserve current binding")
	}
	for _, name := range []string{"FIRST", "SECOND"} {
		b, err := os.ReadFile(filepath.Join(root, name))
		if err != nil || !bytes.Equal(b, raw) {
			t.Fatal("actual rooted save differs", name, err)
		}
	}
	before = m
	m = hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, before, m)
	if len(r.Completed()) == 0 {
		t.Fatal("no real runtime completion retained")
	}
}

func TestBoldDetachedAndUncertainSaveRemainAuthoritative(t *testing.T) {
	_, m, root := hBoldSetup(t)
	m = hBoldClosed(t, m, "z")
	m, c := firstSave(t, m, "FIRST")
	reply := c()
	m = hBoldUpdate(t, m, CancelPendingMsg{})
	m = hBoldUpdate(t, m, reply)
	if m.State().Session.NewPhase != editor.PublicationUncertain || m.Session().Source() != nil {
		t.Fatal("real late publication lost uncertainty")
	}
	next := hBoldPress(t, m, tea.KeyPressMsg{Code: tea.KeyF6})
	hBoldSameSession(t, m, next)
	if _, err := os.Stat(filepath.Join(root, "FIRST")); err != nil {
		t.Fatal("did not retain genuine detached filesystem effect", err)
	}
}

func TestBoldPublicAllocationBounds(t *testing.T) {
	var updatePeak, viewPeak uint64
	for range 8 {
		_, m, _ := hBoldSetup(t)
		m = hBoldPress(t, m, tea.KeyPressMsg{Code: 'P', Text: "short"})
		var a, b, c goruntime.MemStats
		goruntime.ReadMemStats(&a)
		m = hBoldClosed(t, m, "data")
		goruntime.ReadMemStats(&b)
		v := m.View()
		goruntime.ReadMemStats(&c)
		if hBoldActive(m) || !strings.Contains(v.Content, "short") || !strings.Contains(v.Content, "history=unknown") {
			t.Fatal("allocation sample missed actual Bold legacy path")
		}
		updatePeak = max(updatePeak, b.TotalAlloc-a.TotalAlloc)
		viewPeak = max(viewPeak, c.TotalAlloc-b.TotalAlloc)
	}
	if updatePeak > 4<<20 || viewPeak > 256<<10 {
		t.Fatalf("public allocation bounds exceeded: update=%d view=%d", updatePeak, viewPeak)
	}
	t.Logf("three-Update peak=%d limit=%d, View peak=%d limit=%d, samples=8", updatePeak, 4<<20, viewPeak, 256<<10)
}

// Artifact-only reader path. Full routine validation skips it until the two
// independent real terminal roots have emitted both actual files.
func TestBoldPTYReadback(t *testing.T) {
	root := os.Getenv("WORDLING_WP76_PTY_OUTPUT")
	if root == "" {
		t.Skip("requires the two completed frozen PTY roots")
	}
	newDoc, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		t.Fatal(err)
	}
	newRaw, err := newDoc.Export()
	if err != nil {
		t.Fatal(err)
	}
	newImage, err := wp51.Parse(newRaw)
	if err != nil {
		t.Fatal(err)
	}
	meta := newImage.Inspect()
	prefix := bytes.Clone(newRaw[:meta.Body.Offset])
	for _, p := range meta.Packets {
		if p.Type == 6 {
			prefix[p.Data.Offset] |= 8
		}
	}
	families := []string{hBoldOn + "alpha" + hBoldOff + "beta", "A" + hBoldOn + "BC" + hBoldOff + "D"}
	for _, rep := range []string{"03", "04"} {
		path := "../../docs/research/reference-runs/2026-10-29-advanced-" + rep + "/CMD51-204/ORIGIN.WP5"
		raw, err := os.ReadFile(path)
		if err != nil || fmt.Sprintf("%x", sha256.Sum256(raw)) != "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d" {
			t.Fatal("original 204 association changed", path, err)
		}
		image, err := wp51.Parse(raw)
		if err != nil {
			t.Fatal(err)
		}
		body, ok := image.Bytes(image.Inspect().Body)
		if !ok || string(body) != families[1] {
			t.Fatal("original 204 completed body mismatch", path)
		}
	}
	for index, want := range families {
		var first []byte
		for _, name := range []string{"FIRST", "SECOND"} {
			path := filepath.Join(root, fmt.Sprintf("r%d", index+1), "files", name)
			raw, err := os.ReadFile(path)
			if err != nil {
				t.Fatal(err)
			}
			image, err := wp51.Parse(raw)
			if err != nil || !bytes.Equal(image.Export(), raw) {
				t.Fatal("native reader roundtrip failed", path, err)
			}
			span := image.Inspect().Body
			body, ok := image.Bytes(span)
			if !ok || string(body) != want || !bytes.Equal(raw[:span.Offset], prefix) {
				t.Fatal("native completed body or New packet prefix mismatch", path)
			}
			doc, err := document.Parse(raw)
			if err != nil {
				t.Fatal(err)
			}
			out, err := doc.Export()
			if err != nil || !bytes.Equal(out, raw) {
				t.Fatal("document reader roundtrip failed", path, err)
			}
			on, off := 0, 0
			for n := range doc.TokenCount() {
				tok, err := doc.Token(n)
				if err != nil {
					t.Fatal(err)
				}
				if tok.Kind == document.BoldOn {
					on++
				}
				if tok.Kind == document.BoldOff {
					off++
				}
			}
			if on != 1 || off != 1 {
				t.Fatal("document reader did not find one native pair", path)
			}
			if first == nil {
				first = raw
			} else if !bytes.Equal(first, raw) {
				t.Fatal("FIRST and SECOND differ", path)
			}
			t.Logf("%s SHA256=%x body=%x", path, sha256.Sum256(raw), body)
		}
	}
}
