package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"os"
	"path/filepath"
	"sync"
	"testing"
)

func TestActualRetrieveAndSave(t *testing.T) {
	root := t.TempDir()
	native, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(root, "ORIGIN"), native, 0600); e != nil {
		t.Fatal(e)
	}
	r, m, e := Open(Config{Root: root, Profile: LocalFlat})
	if e != nil {
		t.Fatal(e)
	}
	defer r.Close()
	send := func(k tea.Key) {
		t.Helper()
		n, c := m.Update(tea.KeyPressMsg(k))
		m = n.(Model)
		for c != nil {
			n, c = m.Update(c())
			m = n.(Model)
		}
	}
	send(tea.Key{Code: tea.KeyF10, Mod: tea.ModShift})
	send(tea.Key{Code: 'O', Text: "ORIGIN"})
	send(tea.Key{Code: tea.KeyEnter})
	if m.Session().Snapshot().Name != "ORIGIN" {
		t.Fatal(m.State())
	}
	send(tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if !m.Session().Snapshot().Reveal {
		t.Fatal("Reveal")
	}
	send(tea.Key{Code: tea.KeyF10})
	send(tea.Key{Code: 'C', Text: "COPY"})
	send(tea.Key{Code: tea.KeyEnter})
	if m.Session().Snapshot().SaveState != editor.NewNamePublished {
		t.Fatal(m.State())
	}
	b, e := os.ReadFile(filepath.Join(root, "COPY"))
	if e != nil || string(b) != string(native) {
		t.Fatal("native export", e)
	}
}

func testModel(t *testing.T) (*Runtime, Model, []byte, string) {
	t.Helper()
	root := t.TempDir()
	b, e := os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5")
	if e != nil {
		t.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(root, "ORIGIN"), b, 0600); e != nil {
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
	return r, m, b, root
}
func press(m Model, code rune, mod tea.KeyMod, text string) (Model, tea.Cmd) {
	n, c := m.Update(tea.KeyPressMsg{Code: code, Mod: mod, Text: text})
	return n.(Model), c
}
func drain(m Model, c tea.Cmd) Model {
	for c != nil {
		n, next := m.Update(c())
		m = n.(Model)
		c = next
	}
	return m
}
func retrieve(m Model) Model {
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'O', 0, "ORIGIN")
	m, c := press(m, tea.KeyEnter, 0, "")
	return drain(m, c)
}
func TestUnknownPasteReleaseResizeAndNoAliases(t *testing.T) {
	_, m, b, _ := testModel(t)
	m = retrieve(m)
	before := m.Session().Snapshot()
	for _, msg := range []tea.Msg{tea.KeyReleaseMsg{Code: tea.KeyF7}, tea.PasteMsg{Content: "\x1b[18~ny"}, tea.PasteStartMsg{}, tea.PasteEndMsg{}, struct{}{}, tea.WindowSizeMsg{Width: 42, Height: 12}, tea.KeyPressMsg{Code: 'q', Text: "q"}, tea.KeyPressMsg{Code: 'q', Mod: tea.ModCtrl}, tea.KeyPressMsg{Code: 's', Mod: tea.ModCtrl}, tea.KeyPressMsg{Code: tea.KeyRight, IsRepeat: true}} {
		n, c := m.Update(msg)
		m = n.(Model)
		if c != nil {
			t.Fatal("unexpected command")
		}
		if m.Session().Snapshot().Mode != before.Mode || m.Session().Snapshot().Gap != before.Gap {
			t.Fatal("input changed state")
		}
		got, _ := m.Session().Document().Export()
		if string(got) != string(b) {
			t.Fatal("native changed")
		}
	}
	if m.State().Width != 42 || m.State().PhysicalDeliveryQualified {
		t.Fatal(m.State())
	}
}
func TestPendingCancelLateReadAndStaleDoNotConsumeCurrent(t *testing.T) {
	_, m, _, _ := testModel(t)
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'O', 0, "ORIGIN")
	m, c := press(m, tea.KeyEnter, 0, "")
	pending := m.Session().Snapshot().Pending
	n, _ := m.Update(CancelPendingMsg{})
	m = n.(Model)
	m, _ = press(m, tea.KeyF7, 0, "")
	if m.Session().Snapshot().Mode != editor.RetrieveName {
		t.Fatal("detached pending allowed exit")
	}
	result := c()
	n, _ = m.Update(result)
	m = n.(Model)
	if m.Session().Source() != nil || m.State().PendingIO != 0 {
		t.Fatal("cancelled read applied")
	}
	m, c = press(m, tea.KeyEnter, 0, "")
	if c == nil {
		t.Fatal("retry missing")
	}
	n, _ = m.Update(result)
	m = n.(Model)
	if m.Session().Snapshot().Pending.Operation == pending.Operation || m.State().PendingIO != 1 {
		t.Fatal("stale result consumed retry")
	}
	m = drain(m, c)
	if m.Session().Source() == nil {
		t.Fatal("retry failed")
	}
}
func TestLatePublicationRequiresReconciliation(t *testing.T) {
	_, m, b, root := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, 'C', 0, "COPY")
	m, c := press(m, tea.KeyEnter, 0, "")
	n, c := m.Update(c())
	m = n.(Model)
	if c == nil {
		t.Fatal("missing actual Save")
	}
	n, _ = m.Update(CancelPendingMsg{})
	m = n.(Model)
	n, _ = m.Update(c())
	m = n.(Model)
	if m.State().Reconciliation == "" || m.Session().Snapshot().SaveState == editor.NewNamePublished {
		t.Fatal("late publication false success")
	}
	disk, e := os.ReadFile(filepath.Join(root, "COPY"))
	if e != nil || string(disk) != string(b) {
		t.Fatal("actual late save missing", e)
	}
	m, _ = press(m, tea.KeyF7, 0, "")
	if m.Session().Snapshot().Mode == editor.ExitSaveQuestion {
		t.Fatal("uncertainty allowed exit")
	}
}
func TestRealSourceRaceAndRefusedReplacement(t *testing.T) {
	_, m, b, root := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF10, 0, "")
	m, c := press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	m, c = press(m, 'y', 0, "y")
	m = drain(m, c)
	if m.Session().Snapshot().SaveState != editor.SameFileNoOp {
		t.Fatal("no-op")
	}
	if e := os.WriteFile(filepath.Join(root, "OTHER"), b, 0600); e != nil {
		t.Fatal(e)
	}
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, 'O', 0, "OTHER")
	m, c = press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	m, c = press(m, 'y', 0, "y")
	if c != nil || m.State().Notice == "" {
		t.Fatal("replacement not refused")
	}
	m, _ = press(m, 'n', 0, "n")
	m, _ = press(m, 'C', 0, "COPY")
	m, c = press(m, tea.KeyEnter, 0, "")
	n, c := m.Update(c())
	m = n.(Model)
	changed := append([]byte(nil), b...)
	changed[len(changed)-1] = 'Z'
	if e := os.WriteFile(filepath.Join(root, "ORIGIN"), changed, 0600); e != nil {
		t.Fatal(e)
	}
	m = drain(m, c)
	if m.Session().Snapshot().SaveState != editor.SaveFailed {
		t.Fatal("stale source saved")
	}
	if _, e := os.Stat(filepath.Join(root, "COPY")); !os.IsNotExist(e) {
		t.Fatal("destination created")
	}
	got, _ := m.Session().Document().Export()
	if string(got) != string(b) {
		t.Fatal("loaded snapshot mutated")
	}
}
func TestCloseGatesQueuedIOAndRetainsStartedReceipts(t *testing.T) {
	r, m, _, _ := testModel(t)
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'O', 0, "ORIGIN")
	_, c := press(m, tea.KeyEnter, 0, "")
	if e := r.Close(); e != nil {
		t.Fatal(e)
	}
	msg := c().(resultMsg)
	if msg.result.Err == nil || msg.result.Document != nil {
		t.Fatal("closed host executed IO")
	}
	if e := r.Close(); e != nil {
		t.Fatal(e)
	}
}
func TestExplicitProfileAndFlatRoot(t *testing.T) {
	for _, config := range []Config{{Root: t.TempDir()}, {Root: "relative", Profile: LocalFlat}, {Root: t.TempDir(), Profile: "DOS"}} {
		if r, _, e := Open(config); e == nil {
			r.Close()
			t.Fatal("invalid profile accepted")
		}
	}
	_, m, _, _ := testModel(t)
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'x', 0, "../ORIGIN")
	m, c := press(m, tea.KeyEnter, 0, "")
	if c != nil || m.State().Notice == "" {
		t.Fatal("path accepted")
	}
}

func TestConcurrentShutdownAndReceiptIsolation(t *testing.T) {
	r, _, _, _ := testModel(t)
	var wg sync.WaitGroup
	start := make(chan struct{})
	for i := 1; i <= 64; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			<-start
			msg := r.command(editor.Intent{Operation: uint64(id), Kind: editor.Read, Directory: r.directory, Name: "ORIGIN"})().(resultMsg)
			if msg.result.Err != nil && msg.result.Err.Error() != "host IO is closed" {
				t.Errorf("unexpected shutdown result %v", msg.result.Err)
			}
		}(i)
	}
	close(start)
	if e := r.Close(); e != nil {
		t.Fatal(e)
	}
	wg.Wait()
	for _, result := range r.Completed() {
		if result.Err != nil || result.Document != nil || result.Destination != nil {
			t.Fatal("shutdown metadata receipt retained image or failed real read", result)
		}
	}
	// A command rejected by the stop gate cannot acquire a closed descriptor.
	result := r.command(editor.Intent{Operation: 1000, Kind: editor.Read, Directory: r.directory, Name: "ORIGIN"})().(resultMsg)
	if result.result.Err == nil || result.result.Err.Error() != "host IO is closed" {
		t.Fatal("closed-gate contract", result)
	}
}
func TestReceiptLimitAndDuplicateRefuseBeforeIO(t *testing.T) {
	r, _, _, _ := testModel(t)
	intent := editor.Intent{Operation: 1, Kind: editor.Read, Directory: r.directory, Name: "ORIGIN"}
	if r.command(intent)().(resultMsg).result.Err != nil {
		t.Fatal("read failed")
	}
	if r.command(intent)().(resultMsg).result.Err.Error() != "duplicate host IO request refused" {
		t.Fatal("replayed IO")
	}
	r.mu.Lock()
	r.issued = 1024
	r.mu.Unlock()
	intent.Operation = 2
	if r.command(intent)().(resultMsg).result.Err == nil {
		t.Fatal("receipt cap missing")
	}
	if len(r.Completed()) != 1 {
		t.Fatal("refusals performed IO")
	}
}
func TestRetrieveCancelFilenameCancelAndExitEscape(t *testing.T) {
	_, m, b, _ := testModel(t)
	for _, code := range []rune{tea.KeyF1, tea.KeyEscape} {
		m, _ = press(m, tea.KeyF10, tea.ModShift, "")
		m, _ = press(m, 'D', 0, "DRAFT")
		m, _ = press(m, code, 0, "")
		if m.Session().Snapshot().Mode != editor.Editing || m.Session().Source() != nil {
			t.Fatal("Retrieve cancel")
		}
	}
	m = retrieve(m)
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, tea.KeyRight, 0, "")
	m, _ = press(m, tea.KeyRight, 0, "")
	m, _ = press(m, tea.KeyBackspace, 0, "")
	m, _ = press(m, 'X', 0, "X")
	if m.Session().Snapshot().Draft != "OXIGIN" {
		t.Fatal(m.State())
	}
	m, _ = press(m, tea.KeyF1, 0, "")
	if m.Session().Snapshot().Name != "ORIGIN" {
		t.Fatal("filename cancel lost original")
	}
	m, _ = press(m, tea.KeyF7, 0, "")
	m, _ = press(m, tea.KeyEscape, 0, "")
	if m.Session().Snapshot().Mode != editor.SaveName {
		t.Fatal("exit Save Esc")
	}
	m, _ = press(m, tea.KeyF1, 0, "")
	got, _ := m.Session().Document().Export()
	if string(got) != string(b) {
		t.Fatal("cancel changed native")
	}
	m, _ = press(m, tea.KeyF7, 0, "")
	m, _ = press(m, 'n', 0, "n")
	m, _ = press(m, tea.KeyEscape, 0, "")
	if m.Session().Source() != nil || m.Session().Snapshot().Mode != editor.Editing {
		t.Fatal("Exit Esc must clear")
	}
}

func TestResultEnvelopeMismatchAndCopiedValues(t *testing.T) {
	_, m, _, _ := testModel(t)
	m, _ = press(m, tea.KeyF10, tea.ModShift, "")
	m, _ = press(m, 'O', 0, "ORIGIN")
	m, c := press(m, tea.KeyEnter, 0, "")
	p := m.Session().Snapshot().Pending
	for _, wrong := range []editor.Result{{Operation: p.Operation + 1, Revision: p.Revision, Kind: p.Kind}, {Operation: p.Operation, Revision: p.Revision + 1, Kind: p.Kind}, {Operation: p.Operation, Revision: p.Revision, Kind: editor.Observe}} {
		n, _ := m.Update(resultMsg{wrong})
		m = n.(Model)
		if m.State().PendingIO != 1 || m.Session().Snapshot().Pending.Operation != p.Operation {
			t.Fatal("wrong result consumed operation")
		}
	}
	original := m
	m = drain(m, c)
	if original.Session().Source() != nil || original.State().PendingIO != 1 || m.Session().Source() == nil {
		t.Fatal("model copies not persistent")
	}
	state := m.State()
	state.Session.Name = "tampered"
	if m.Session().Snapshot().Name != "ORIGIN" {
		t.Fatal("state aliases")
	}
}
