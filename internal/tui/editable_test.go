package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

func key(t *testing.T, m Model, code rune, mod tea.KeyMod, text string) Model {
	t.Helper()
	next, c := press(m, code, mod, text)
	if c != nil {
		t.Fatal("unexpected IO")
	}
	return next
}
func queueEdited(t *testing.T, m Model, name string) (Model, tea.Cmd) {
	t.Helper()
	m = key(t, m, tea.KeyF10, 0, "")
	m = key(t, m, 'x', 0, name)
	m, c := press(m, tea.KeyEnter, 0, "")
	if c == nil {
		t.Fatal("missing Observe")
	}
	n, c := m.Update(c())
	m = n.(Model)
	if c == nil || m.Session().Snapshot().Pending.Kind != editor.PublishCandidate {
		t.Fatal("missing candidate", m.State())
	}
	return m, c
}
func TestLiveEditingAndCandidatePublication(t *testing.T) {
	_, m, source, root := testModel(t)
	m = retrieve(m)
	if m.Session().Source() == nil {
		t.Fatal(m.State())
	}
	m = key(t, m, 'q', 0, "q")
	if strings.Contains(m.View().Content, "Typeover") {
		t.Fatal("inactive Typeover status")
	}
	m = key(t, m, tea.KeyInsert, 0, "")
	if !strings.Contains(m.View().Content, "Typeover") {
		t.Fatal("missing active Typeover status")
	}
	m = key(t, m, 'Q', tea.ModShift, "Q")
	m = key(t, m, tea.KeyInsert, 0, "")
	x := m.Session().Snapshot()
	if !x.Dirty || x.Gap != 2 || x.Typeover || strings.Contains(m.View().Content, "Typeover") {
		t.Fatal(x)
	}
	candidate, _ := m.Session().Document().Export()
	m, c := queueEdited(t, m, "EDITED")
	m = drain(m, c)
	if m.Session().Snapshot().Dirty || m.Session().Snapshot().Name != "EDITED" || m.Session().Snapshot().SaveState != editor.NewNamePublished {
		t.Fatal(m.State())
	}
	disk, e := os.ReadFile(filepath.Join(root, "EDITED"))
	if e != nil || !bytes.Equal(disk, candidate) {
		t.Fatal("actual candidate", e)
	}
	old, e := os.ReadFile(filepath.Join(root, "ORIGIN"))
	if e != nil || !bytes.Equal(old, source) {
		t.Fatal("source modified")
	}
	if m.Session().Snapshot().HistoryCountKnown {
		if strings.Contains(m.View().Content, "bounded native editing") || m.View().Cursor == nil || m.View().Cursor.Y != 0 {
			t.Fatal(m.View().Content)
		}
	} else if !strings.Contains(m.View().Content, "history=unknown") || m.View().Cursor == nil || m.View().Cursor.Y != 1 {
		t.Fatal("unknown-history fallback hidden", m.View().Content)
	}
}
func TestCapturedDirectoryCapabilityNotWrapperOrInode(t *testing.T) {
	r, _, _, root := testModel(t)
	copy := *r.directory
	good := editor.Intent{Operation: 1, Kind: editor.Read, Directory: &copy, Name: "ORIGIN"}
	if msg := r.command(good)().(resultMsg); msg.result.Err != nil {
		t.Fatal("copied capability rejected", msg)
	}
	other, e := storage.OpenDirectory(root)
	if e != nil {
		t.Fatal(e)
	}
	defer other.Close()
	for i, d := range []*storage.Directory{other, {}, nil} {
		got := r.command(editor.Intent{Operation: uint64(2 + i), Kind: editor.Read, Directory: d, Name: "ORIGIN"})().(resultMsg)
		if got.result.Err == nil || got.result.Document != nil {
			t.Fatal("foreign/zero capability permitted")
		}
	}
	// Capture before public whole-wrapper rebinding; Close is still shared.
	pending := r.command(editor.Intent{Operation: 10, Kind: editor.Read, Directory: &copy, Name: "ORIGIN"})
	copy = *other
	if pending().(resultMsg).result.Err != nil {
		t.Fatal("queued capability borrowed wrapper")
	}
}
func TestLiveBlockAnswersAndOverlay(t *testing.T) {
	for _, answer := range []rune{'n', tea.KeyF1, tea.KeyEscape} {
		t.Run(string(answer), func(t *testing.T) {
			_, m, raw, _ := testModel(t)
			m = retrieve(m)
			m = key(t, m, tea.KeyF3, tea.ModAlt, "")
			m = key(t, m, tea.KeyRight, 0, "")
			m = key(t, m, tea.KeyF4, tea.ModAlt, "")
			m = key(t, m, tea.KeyRight, 0, "")
			before := m.Session().Snapshot()
			m = key(t, m, tea.KeyDelete, 0, "")
			if !reflect.DeepEqual(before, m.Session().Snapshot()) || m.State().Notice == "" {
				t.Fatal("selected Delete alias")
			}
			m = key(t, m, tea.KeyBackspace, 0, "")
			if m.Session().Snapshot().Prompt != "Delete Block? No (Yes)" {
				t.Fatal(m.State())
			}
			text := ""
			if answer == 'n' {
				text = "n"
			}
			m = key(t, m, answer, 0, text)
			got, _ := m.Session().Document().Export()
			if !bytes.Equal(got, raw) || m.Session().Snapshot().Dirty || !m.Session().Snapshot().Selection {
				t.Fatal("decline lost selection/native")
			}
			m = key(t, m, tea.KeyF1, 0, "")
			if m.Session().Snapshot().Selection {
				t.Fatal("separate cleanup")
			}
		})
	}
	_, m, _, _ := testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	m = key(t, m, tea.KeyRight, 0, "")
	m = key(t, m, tea.KeyF4, tea.ModAlt, "")
	for range 4 {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	m = key(t, m, tea.KeyBackspace, 0, "")
	m = key(t, m, 'y', 0, "y")
	m = key(t, m, tea.KeyF1, 0, "")
	if m.Session().Snapshot().Mode != editor.HistoryPreview || !strings.Contains(m.View().Content, "[Block]") || !strings.Contains(m.View().Content, "[BOLD]") {
		t.Fatal("preview not rendered", m.State(), m.View().Content)
	}
	before, _ := m.Session().Document().Export()
	m = key(t, m, tea.KeyF1, 0, "")
	after, _ := m.Session().Document().Export()
	if !bytes.Equal(before, after) {
		t.Fatal("preview serialized")
	}
	m = key(t, m, tea.KeyF1, 0, "")
	m = key(t, m, '1', 0, "1")
	if m.Session().Snapshot().Mode != editor.Editing || m.Session().Snapshot().Gap != 5 {
		t.Fatal("Restore routing", m.State())
	}
}

func TestCandidatePendingLateCancelAndUnknowns(t *testing.T) {
	for _, cancel := range []bool{false, true} {
		t.Run(map[bool]string{false: "newer typing", true: "host detach"}[cancel], func(t *testing.T) {
			_, m, source, root := testModel(t)
			m = retrieve(m)
			m = key(t, m, 'X', 0, "X")
			m, c := queueEdited(t, m, "COPY")
			pending := m.Session().Snapshot().Pending
			candidate := append([]byte(nil), pending.Candidate...)
			old := m.Session().Snapshot()
			n, _ := m.Update(tea.WindowSizeMsg{Width: 40, Height: 17})
			m = n.(Model)
			if m.Session().Snapshot().NativeRevision != old.NativeRevision || m.State().Width != 40 {
				t.Fatal("resize mutated revision")
			}
			for _, msg := range []tea.Msg{tea.PasteMsg{Content: "Y"}, tea.KeyReleaseMsg{Code: 'y', Text: "Y"}, tea.KeyPressMsg{Code: 'q', Mod: tea.ModCtrl}, tea.KeyPressMsg{Code: 's', Mod: tea.ModCtrl}, struct{}{}} {
				n, cmd := m.Update(msg)
				m = n.(Model)
				if cmd != nil || m.Session().Snapshot().NativeRevision != old.NativeRevision {
					t.Fatal("unsupported event edited")
				}
			}
			if cancel {
				n, _ = m.Update(CancelPendingMsg{})
				m = n.(Model)
				m = key(t, m, 'Y', 0, "Y")
				if m.Session().Snapshot().NativeRevision != old.NativeRevision {
					t.Fatal("detached IO admitted commands")
				}
			} else {
				m = key(t, m, 'Y', 0, "Y")
				if m.Session().Snapshot().NativeRevision == old.NativeRevision {
					t.Fatal("pending typing did not edit")
				}
			}
			result := c()
			n, _ = m.Update(result)
			m = n.(Model)
			x := m.Session().Snapshot()
			if !x.Dirty || x.Name != "ORIGIN" || x.SaveState == editor.NewNamePublished || !x.Detached.DestinationMayExist || x.Pending != nil || m.State().PendingIO != 0 {
				t.Fatal("late result false saved", m.State())
			}
			current := x.NativeRevision
			n, _ = m.Update(result)
			m = n.(Model)
			if m.Session().Snapshot().NativeRevision != current || !m.Session().Snapshot().Dirty {
				t.Fatal("duplicate changed revision")
			}
			disk, e := os.ReadFile(filepath.Join(root, "COPY"))
			if e != nil || !bytes.Equal(disk, candidate) {
				t.Fatal("actual old publication", e)
			}
			disk, e = os.ReadFile(filepath.Join(root, "ORIGIN"))
			if e != nil || !bytes.Equal(disk, source) {
				t.Fatal("source modified")
			}
		})
	}
}
func TestCandidateActualRacesAndFirstSourceAnchor(t *testing.T) {
	for _, kind := range []string{"source", "destination", "closed", "wrapper"} {
		t.Run(kind, func(t *testing.T) {
			r, m, source, root := testModel(t)
			m = retrieve(m)
			guard := m.Session().Source().Identity()
			m = key(t, m, 'X', 0, "X")
			m, c := queueEdited(t, m, "FIRST")
			m = drain(m, c)
			if m.Session().Snapshot().Dirty || m.Session().Snapshot().Name != "FIRST" || m.Session().Source().Identity() != guard {
				t.Fatal("first source guard rebased")
			}
			m = key(t, m, 'Y', 0, "Y")
			m, c = queueEdited(t, m, "SECOND")
			rev := m.Session().Snapshot().NativeRevision
			switch kind {
			case "source":
				if e := os.WriteFile(filepath.Join(root, "ORIGIN"), append(source, 'Z'), 0600); e != nil {
					t.Fatal(e)
				}
			case "destination":
				if e := os.WriteFile(filepath.Join(root, "SECOND"), []byte("external winner"), 0600); e != nil {
					t.Fatal(e)
				}
			case "closed":
				if e := r.Close(); e != nil {
					t.Fatal(e)
				}
			case "wrapper":
				*m.Session().Source() = storage.Document{}
				*m.Session().Snapshot().Pending.Directory = storage.Directory{}
			}
			m = drain(m, c)
			x := m.Session().Snapshot()
			if kind == "wrapper" {
				if x.Dirty || x.Name != "SECOND" {
					t.Fatal("owned request rebound", m.State())
				}
				return
			}
			if !x.Dirty || x.Name != "FIRST" || x.NativeRevision != rev || x.SaveState != editor.SaveFailed || x.PublishedName != "FIRST" {
				t.Fatal("failure changed saved/current state", m.State())
			}
			if kind == "destination" {
				raw, _ := os.ReadFile(filepath.Join(root, "SECOND"))
				if string(raw) != "external winner" {
					t.Fatal("overwrote race winner")
				}
			} else if _, e := os.Stat(filepath.Join(root, "SECOND")); !os.IsNotExist(e) {
				t.Fatal("failed publication exists")
			}
		})
	}
}
func TestActualPublishedGenericErrorRetainsUncertainty(t *testing.T) {
	_, m, _, root := testModel(t)
	m = retrieve(m)
	m = key(t, m, 'X', 0, "X")
	m, c := queueEdited(t, m, "COPY")
	msg := c().(resultMsg)
	if msg.result.Err != nil || msg.result.Outcome.State != storage.Published {
		t.Fatal(msg)
	}
	// Explicitly injected host-boundary error after real IO, not a simulated disk fault.
	msg.result.Err = &editor.Refusal{Reason: "host reported failure after actual Publish"}
	n, _ := m.Update(msg)
	m = n.(Model)
	if !m.Session().Snapshot().Dirty || m.Session().Snapshot().SaveState != editor.SaveUncertain || !m.Session().Snapshot().Last.DestinationMayExist || m.State().Reconciliation == "" {
		t.Fatal("published uncertainty lost", m.State())
	}
	before := m.Session().Snapshot()
	m = key(t, m, tea.KeyF7, 0, "")
	if !reflect.DeepEqual(m.Session().Snapshot(), before) {
		t.Fatal("uncertainty allowed exit")
	}
	if _, e := os.Stat(filepath.Join(root, "COPY")); e != nil {
		t.Fatal("actual publication absent", e)
	}
}
func TestPreparedCandidateOwnsInputAndCorrectPublicationID(t *testing.T) {
	r, m, _, root := testModel(t)
	m = retrieve(m)
	m = key(t, m, 'X', 0, "X")
	m, _ = queueEdited(t, m, "CAPTURED")
	request := *m.Session().Snapshot().Pending
	want := append([]byte(nil), request.Candidate...)
	cmd := r.command(request)
	clear(request.Candidate)
	*request.Document = storage.Document{}
	*request.Destination = storage.Destination{}
	*request.Directory = storage.Directory{}
	msg := cmd().(resultMsg)
	if msg.result.Err != nil || msg.result.Operation != request.Operation || msg.result.Revision != request.Revision || msg.result.Kind != editor.PublishCandidate {
		t.Fatal("capture/publication identity", msg)
	}
	raw, e := os.ReadFile(filepath.Join(root, "CAPTURED"))
	if e != nil || !bytes.Equal(raw, want) {
		t.Fatal("candidate borrowed mutable payload", e)
	}
}

func TestResizePreviewAndReturnedCopies(t *testing.T) {
	_, m, raw, _ := testModel(t)
	m = retrieve(m)
	m = key(t, m, tea.KeyF3, tea.ModAlt, "")
	m = key(t, m, tea.KeyRight, 0, "")
	m = key(t, m, tea.KeyF4, tea.ModAlt, "")
	for range 4 {
		m = key(t, m, tea.KeyRight, 0, "")
	}
	m = key(t, m, tea.KeyBackspace, 0, "")
	m = key(t, m, 'Y', tea.ModShift, "Y")
	m = key(t, m, tea.KeyF1, 0, "")
	before, _ := m.Session().Document().Export()
	snapshot := m.Session().Snapshot()
	for _, size := range []tea.WindowSizeMsg{{Width: 12, Height: 4}, {Width: 130, Height: 30}, {Width: 1, Height: 1}, {Width: 1000000000, Height: 1000000000}} {
		n, c := m.Update(size)
		m = n.(Model)
		if c != nil {
			t.Fatal("resize IO")
		}
		after, _ := m.Session().Document().Export()
		if !bytes.Equal(before, after) || !reflect.DeepEqual(snapshot, m.Session().Snapshot()) {
			t.Fatal("resize altered preview/session")
		}
		if len(m.View().Content) > 100000 || m.State().Width > 4096 || m.State().Height > 4096 {
			t.Fatal("view safety bound")
		}
	}
	m = key(t, m, tea.KeyF1, 0, "")
	m = key(t, m, tea.KeyF1, 0, "")
	m = key(t, m, '1', 0, "1")
	restored, _ := m.Session().Document().Export()
	if !bytes.Equal(restored[324:], raw[324:]) {
		t.Fatal("Restore lost attributed body")
	}
}

func TestRuntimeNoEditCrossDirectoryAndEditedCapabilityRefusal(t *testing.T) {
	r, _, raw, _ := testModel(t)
	otherRoot := t.TempDir()
	if e := os.WriteFile(filepath.Join(otherRoot, "FOREIGN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	other, e := storage.OpenDirectory(otherRoot)
	if e != nil {
		t.Fatal(e)
	}
	defer other.Close()
	source, e := other.Read("FOREIGN")
	if e != nil {
		t.Fatal(e)
	}
	dest, e := r.directory.Observe("SNAPSHOT")
	if e != nil {
		t.Fatal(e)
	}
	msg := r.command(editor.Intent{Operation: 101, Revision: 1, Kind: editor.WriteSnapshot, Directory: r.directory, Document: source, Destination: dest, Name: "SNAPSHOT"})().(resultMsg)
	if msg.result.Err != nil || msg.result.Outcome.State != storage.Published {
		t.Fatal("existing crossdirectory snapshot contract", msg)
	}
	dest, e = r.directory.Observe("EDITED")
	if e != nil {
		t.Fatal(e)
	}
	msg = r.command(editor.Intent{Operation: 102, Revision: 2, Kind: editor.PublishCandidate, Directory: r.directory, Document: source, Destination: dest, Candidate: raw, Name: "EDITED"})().(resultMsg)
	if msg.result.Err == nil || msg.result.Outcome.State == storage.Published {
		t.Fatal("edited source from foreign capability admitted")
	}
}
