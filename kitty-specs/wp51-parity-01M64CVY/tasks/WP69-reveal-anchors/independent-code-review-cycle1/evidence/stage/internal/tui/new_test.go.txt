package tui

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

func newModel(t *testing.T) (*Runtime, Model, string) {
	t.Helper()
	root := t.TempDir()
	r, m, e := Open(Config{Root: root, Profile: LocalFlat, NativeProfile: NativeProfile})
	if e != nil {
		t.Fatal(e)
	}
	t.Cleanup(func() {
		if e := r.Close(); e != nil {
			t.Error(e)
		}
	})
	return r, m, root
}
func firstSave(t *testing.T, m Model, name string) (Model, tea.Cmd) {
	t.Helper()
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, 'N', 0, name)
	m, c := press(m, tea.KeyEnter, 0, "")
	if c == nil {
		t.Fatal("no Observe", m.State())
	}
	n, c := m.Update(c())
	m = n.(Model)
	if c == nil || m.State().Session.NewPhase != editor.AwaitPublish {
		t.Fatal("no source-less request", m.State())
	}
	return m, c
}
func exactNew(t *testing.T, m Model, birth document.Birth, revision document.Revision) {
	t.Helper()
	d := m.Session().Document()
	if d.Birth() != birth || d.Revision() != revision || !d.Birth().IsNew() {
		t.Fatal("New identity replaced")
	}
	_, e := d.OriginalExport()
	var f *document.Failure
	if !errors.As(e, &f) || f.Category != document.NoLoadedOriginal {
		t.Fatal("invented original", e)
	}
}
func TestNewLiveRuntimeFirstSaveActualBindAndLaterSourceGuard(t *testing.T) {
	for _, text := range []string{"", "G43ASCII"} {
		t.Run(text, func(t *testing.T) {
			r, m, root := newModel(t)
			if m.State().NativeProfile != NativeProfile || m.State().Session.Dirty {
				t.Fatal(m.State())
			}
			m, _ = press(m, 'G', 0, text)
			d := m.Session().Document()
			birth, rev := d.Birth(), d.Revision()
			before, _ := d.Export()
			m, publish := firstSave(t, m, "FIRST")
			if m.Session().Source() != nil || m.State().Session.Name != "" || !m.State().Session.Dirty {
				t.Fatal("premature save", m.State())
			}
			reply := publish()
			n, bind := m.Update(reply)
			m = n.(Model)
			if bind == nil || m.State().Session.NewPhase != editor.AwaitFirstRead || m.State().PendingIO != 1 || m.Session().Source() != nil {
				t.Fatal("no distinct binding", m.State())
			}
			m = drain(m, bind)
			exactNew(t, m, birth, rev)
			s := m.State().Session
			if s.NewPhase != editor.NewAnchored || s.Dirty || s.Name != "FIRST" || s.SavedRevision != rev || m.State().PendingIO != 0 {
				t.Fatal("not saved", m.State())
			}
			disk, e := os.ReadFile(filepath.Join(root, "FIRST"))
			if e != nil || !bytes.Equal(disk, before) {
				t.Fatal(e)
			}
			first := m.Session().Source().Identity()
			m, _ = press(m, tea.KeyF10, 0, "")
			m, _ = press(m, tea.KeyHome, 0, "")
			m, _ = press(m, 'C', 0, "COPY")
			m, c := press(m, tea.KeyEnter, 0, "")
			m = drain(m, c)
			if m.Session().Source().Identity() != first || m.State().Session.Name != "COPY" {
				t.Fatal("rebased first anchor", m.State())
			}
			exactNew(t, m, birth, rev)
			if e = os.WriteFile(filepath.Join(root, "FIRST"), append(disk, 'X'), 0600); e != nil {
				t.Fatal(e)
			}
			m, _ = press(m, tea.KeyF10, 0, "")
			m, _ = press(m, tea.KeyHome, 0, "")
			m, _ = press(m, 'T', 0, "THIRD")
			m, c = press(m, tea.KeyEnter, 0, "")
			m = drain(m, c)
			if m.State().Session.SaveState != editor.SaveFailed {
				t.Fatal("source guard bypass", m.State())
			}
			if _, e = os.Stat(filepath.Join(root, "THIRD")); !os.IsNotExist(e) {
				t.Fatal("published changed source")
			}
			if len(r.Completed()) < 4 {
				t.Fatal("no real custody")
			}
		})
	}
}
func TestNewRuntimeTicketsDuplicateForgeryForkAndStaleUI(t *testing.T) {
	r, m, root := newModel(t)
	m, _ = press(m, 'A', 0, "ABC")
	m, c := firstSave(t, m, "ONE")
	stale := m
	ticket := m.firstPending
	reply := c()
	duplicate := c()
	if len(r.Completed()) != 2 {
		t.Fatal("duplicate executor ran", len(r.Completed()))
	}
	n, next := m.Update(duplicate)
	m = n.(Model)
	if next != nil || m.State().PendingIO != 1 {
		t.Fatal("duplicate settled real IO")
	}
	// Public numeric/mirror result cannot consume private worker custody.
	n, next = m.Update(resultMsg{editor.Result{Kind: editor.PublishNewBuffer, Operation: ticket.request.Operation, Revision: ticket.request.Revision, Outcome: storage.Outcome{State: storage.Published}}})
	m = n.(Model)
	if next != nil || m.State().PendingIO != 1 {
		t.Fatal("forged result settled")
	}
	n, next = stale.Update(reply)
	if next != nil || n.(Model).State().Session.NewPhase != editor.AwaitPublish {
		t.Fatal("stale stole real reply")
	}
	n, bind := m.Update(reply)
	m = n.(Model)
	if bind == nil {
		t.Fatal(m.State())
	}
	m = drain(m, bind)
	n, next = m.Update(reply)
	m = n.(Model)
	if next != nil || m.State().Session.NewPhase != editor.NewAnchored {
		t.Fatal("late duplicate mutated")
	}
	disk, e := os.ReadFile(filepath.Join(root, "ONE"))
	if e != nil || len(disk) == 0 {
		t.Fatal(e)
	}
	// Independent accepted forks have equal numeric envelope but unique keys.
	d, e := storage.OpenDirectory(root)
	if e != nil {
		t.Fatal(e)
	}
	defer d.Close()
	s, e := editor.New(editor.Config{Locations: []editor.Location{{Directory: d}}})
	if e != nil {
		t.Fatal(e)
	}
	makeIntent := func() editor.Intent {
		x := s
		var i *editor.Intent
		for _, ev := range []editor.Event{{Command: editor.Save}, {Command: editor.Text, Text: "FORK"}, {Command: editor.Enter}} {
			x, i, e = x.Reduce(ev)
			if e != nil {
				t.Fatal(e)
			}
		}
		dest, e := d.Observe(i.Name)
		if e != nil {
			t.Fatal(e)
		}
		res := editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Destination: dest}
		_, i, e = x.Reduce(editor.Event{Command: editor.Complete, Result: &res})
		if e != nil {
			t.Fatal(e)
		}
		return *i
	}
	a, b := makeIntent(), makeIntent()
	if a.Operation != b.Operation || a.Revision != b.Revision || a.RequestKey() == b.RequestKey() {
		t.Fatal("bad fork premise")
	}
	ta, _ := r.firstCommand(a)
	tb, _ := r.firstCommand(b)
	if ta == tb || ta.key == tb.key {
		t.Fatal("counter collapsed fork")
	}
}
func TestNewRuntimeActualPostPublishReadMismatchRetryAndClose(t *testing.T) {
	for _, fault := range []string{"missing", "samebytes-inode", "metadata", "closed", "cancel-read"} {
		t.Run(fault, func(t *testing.T) {
			r, m, root := newModel(t)
			m, _ = press(m, 'A', 0, "ABC")
			m, c := firstSave(t, m, "FIRST")
			reply := c()
			n, read := m.Update(reply)
			m = n.(Model)
			before, _ := m.Session().Document().Export()
			source := filepath.Join(root, "FIRST")
			switch fault {
			case "missing":
				if e := os.Rename(source, source+"-held"); e != nil {
					t.Fatal(e)
				}
			case "samebytes-inode":
				if e := os.Rename(source, source+"-held"); e != nil {
					t.Fatal(e)
				}
				if e := os.WriteFile(source, before, 0600); e != nil {
					t.Fatal(e)
				}
			case "metadata":
				if e := os.Chmod(source, 0400); e != nil {
					t.Fatal(e)
				}
			case "closed":
				if e := r.Close(); e != nil {
					t.Fatal(e)
				}
			case "cancel-read":
				n, _ := m.Update(CancelPendingMsg{})
				m = n.(Model)
			}
			m = drain(m, read)
			if m.State().Session.NewPhase != editor.PublishedUnbound || m.Session().Source() != nil || !m.State().Session.Dirty || m.State().PendingIO != 0 {
				t.Fatal("false bind", m.State())
			}
			beforeCount := len(r.Completed())
			m, retry := press(m, tea.KeyF10, 0, "")
			if retry == nil {
				t.Fatal("no explicit Read-only retry", m.State())
			}
			m = drain(m, retry)
			if fault == "cancel-read" {
				if m.State().Session.NewPhase != editor.NewAnchored {
					t.Fatal("same receipt did not bind", m.State())
				}
			} else if m.State().Session.NewPhase != editor.PublishedUnbound {
				t.Fatal("reconciled wrong identity", m.State())
			}
			for _, r := range r.Completed()[beforeCount:] {
				if r.Kind != editor.BindNewSource {
					t.Fatal("retry republished")
				}
			}
			after, _ := m.Session().Document().Export()
			if !bytes.Equal(before, after) {
				t.Fatal("Read altered native")
			}
		})
	}
}
func TestNewRuntimeCancelledPublicationLateReplyCannotCleanOrRepublish(t *testing.T) {
	for _, when := range []string{"queued", "published", "closed-before-start"} {
		t.Run(when, func(t *testing.T) {
			r, m, root := newModel(t)
			m, _ = press(m, 'A', 0, "ABC")
			m, c := firstSave(t, m, "FIRST")
			var reply tea.Msg
			if when == "published" {
				reply = c()
			}
			if when == "closed-before-start" {
				if e := r.Close(); e != nil {
					t.Fatal(e)
				}
			} else {
				n, _ := m.Update(CancelPendingMsg{})
				m = n.(Model)
			}
			if reply == nil {
				reply = c()
			}
			m = drain(m, func() tea.Msg { return reply })
			if m.State().Session.NewPhase != editor.PublicationUncertain || !m.State().Session.Dirty || m.Session().Source() != nil {
				t.Fatal("false saved", m.State())
			}
			count := len(r.Completed())
			n, retry := m.Update(RetryFirstReadMsg{})
			m = n.(Model)
			if retry != nil {
				t.Fatal("uncertain Read reconciliation")
			}
			m, c = press(m, tea.KeyF10, 0, "")
			if c != nil || len(r.Completed()) != count {
				t.Fatal("uncertain republish")
			}
			if when == "closed-before-start" {
				if _, e := os.Stat(filepath.Join(root, "FIRST")); !os.IsNotExist(e) {
					t.Fatal("queued after Close touched disk")
				}
			}
		})
	}
}
func TestNewStartupRefusalsAndContextualCancel(t *testing.T) {
	_, m, root := newModel(t)
	m, _ = press(m, 'G', 0, "G43ASCII")
	birth := m.Session().Document().Birth()
	raw, _ := m.Session().Document().Export()
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, 'D', 0, "DRAFT")
	m, _ = press(m, tea.KeyF1, 0, "")
	after, _ := m.Session().Document().Export()
	if !bytes.Equal(raw, after) || m.Session().Document().Birth() != birth {
		t.Fatal("draft cancel changed native")
	}
	m, _ = press(m, tea.KeyF7, 0, "")
	m, _ = press(m, tea.KeyF1, 0, "")
	if m.State().Session.Mode != editor.Editing || !m.State().Session.Dirty {
		t.Fatal("Save question cancel", m.State())
	}
	m, c := firstSave(t, m, "RETRY")
	m = drain(m, c)
	if m.State().Session.Name != "RETRY" {
		t.Fatal(m.State())
	}
	// Existing different target remains refusal and source remains first anchor.
	if e := os.WriteFile(filepath.Join(root, "TAKEN"), raw, 0600); e != nil {
		t.Fatal(e)
	}
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, tea.KeyHome, 0, "")
	m, _ = press(m, 'T', 0, "TAKEN")
	m, c = press(m, tea.KeyEnter, 0, "")
	m = drain(m, c)
	m, c = press(m, 'y', 0, "y")
	m = drain(m, c)
	if !strings.Contains(m.State().Notice, "UnsupportedReplacement") || m.State().Session.Mode != editor.ReplaceQuestion {
		t.Fatal("replacement enabled", m.State())
	}
	for _, bad := range []string{"other", "historical", "local-flat"} {
		if r, _, e := Open(Config{Root: root, Profile: LocalFlat, NativeProfile: bad}); e == nil {
			r.Close()
			t.Fatal("unknown native profile accepted")
		}
	}
	if !strings.Contains(firstStateLine(editor.Snapshot{NewPhase: editor.PublishedUnbound}), "F10 retries verification") {
		t.Fatal("missing truthful state")
	}
}

func TestNewForeignTicketAndIndependentRootNeverRun(t *testing.T) {
	r, m, root := newModel(t)
	m, c := firstSave(t, m, "FIRST")
	reply := c().(firstReply)
	other, foreign, err := Open(Config{Root: t.TempDir(), Profile: LocalFlat})
	if err != nil {
		t.Fatal(err)
	}
	defer other.Close()
	if _, _, ok := other.deliverFirst(reply.ticket); ok {
		t.Fatal("foreign runtime consumed ticket")
	}
	n, cmd := foreign.Update(reply)
	if cmd != nil || n.(Model).State().PendingIO != 0 {
		t.Fatal("foreign model accepted")
	}
	n, bind := m.Update(reply)
	m = n.(Model)
	m = drain(m, bind)
	if m.State().Session.NewPhase != editor.NewAnchored {
		t.Fatal(m.State())
	}
	// Genuine accepted proof from another open is not this runtime's root.
	d, e := storage.OpenDirectory(root)
	if e != nil {
		t.Fatal(e)
	}
	defer d.Close()
	s, e := editor.New(editor.Config{Locations: []editor.Location{{Directory: d}}})
	if e != nil {
		t.Fatal(e)
	}
	var i *editor.Intent
	for _, ev := range []editor.Event{{Command: editor.Save}, {Command: editor.Text, Text: "FOREIGN"}, {Command: editor.Enter}} {
		s, i, e = s.Reduce(ev)
		if e != nil {
			t.Fatal(e)
		}
	}
	dest, e := d.Observe(i.Name)
	if e != nil {
		t.Fatal(e)
	}
	res := editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Destination: dest}
	_, i, e = s.Reduce(editor.Event{Command: editor.Complete, Result: &res})
	if e != nil {
		t.Fatal(e)
	}
	tkt, run := r.firstCommand(*i)
	msg := run().(firstReply)
	if msg.ticket != tkt {
		t.Fatal("wrong custody")
	}
	if _, refused, ok := r.deliverFirst(tkt); !ok || refused == nil {
		t.Fatal("foreign acquisition executed")
	}
	if _, e := os.Stat(filepath.Join(root, "FOREIGN")); !os.IsNotExist(e) {
		t.Fatal("independent root bypassed host")
	}
}
func FuzzNewHostDispatch(f *testing.F) {
	for _, b := range [][]byte{{}, {0}, {1}, {2}, {3}, {0, 1, 2, 3}, {4, 5, 6}} {
		f.Add(b)
	}
	f.Fuzz(func(t *testing.T, b []byte) {
		if len(b) > 32 {
			t.Skip()
		}
		r, m, root := newModel(t)
		m, _ = press(m, 'A', 0, "G43ASCII")
		before, _ := m.Session().Document().Export()
		m, c := firstSave(t, m, "FIRST")
		var msg tea.Msg
		for _, v := range b {
			switch v % 7 {
			case 0:
				if msg == nil {
					msg = c()
				}
			case 1:
				if msg != nil {
					n, extra := m.Update(c())
					m = n.(Model)
					if extra != nil {
						t.Fatal("duplicate scheduled")
					}
				}
			case 2:
				n, _ := m.Update(CancelPendingMsg{})
				m = n.(Model)
			case 3:
				n, extra := m.Update(resultMsg{editor.Result{Kind: editor.PublishNewBuffer, Outcome: storage.Outcome{State: storage.Published}}})
				m = n.(Model)
				if extra != nil {
					t.Fatal("forgery scheduled")
				}
			case 4:
				m, _ = press(m, tea.KeyF7, 0, "")
			case 5:
				m, _ = press(m, 'X', 0, "X")
			case 6:
				m, _ = press(m, tea.KeyF1, 0, "")
			}
		}
		if msg == nil {
			msg = c()
		}
		n, next := m.Update(msg)
		m = n.(Model)
		m = drain(m, next)
		after, _ := m.Session().Document().Export()
		if !bytes.Equal(before, after) {
			t.Fatal("pending altered native")
		}
		disk, e := os.ReadFile(filepath.Join(root, "FIRST"))
		if e != nil || !bytes.Equal(before, disk) {
			t.Fatal("actual publication", e)
		}
		phase := m.State().Session.NewPhase
		if phase != editor.NewAnchored && phase != editor.PublicationUncertain {
			t.Fatal("false state", m.State())
		}
		if len(r.Completed()) > 3 {
			t.Fatal("duplicate worker")
		}
	})
}
func BenchmarkNewHostStartup(b *testing.B) {
	root := b.TempDir()
	b.ReportAllocs()
	for b.Loop() {
		r, _, e := Open(Config{Root: root, Profile: LocalFlat})
		if e != nil {
			b.Fatal(e)
		}
		if e = r.Close(); e != nil {
			b.Fatal(e)
		}
	}
}

func TestNewCaptureDefensiveWrappersAndDupAfterCapacityOrClose(t *testing.T) {
	for _, guard := range []string{"capacity", "close"} {
		t.Run(guard, func(t *testing.T) {
			r, m, root := newModel(t)
			m, _ = press(m, 'G', 0, "G43ASCII")
			m, c := firstSave(t, m, "FIRST")
			snapshot := m.State()
			pending := snapshot.Session.Pending
			foreign, e := storage.OpenDirectory(t.TempDir())
			if e != nil {
				t.Fatal(e)
			}
			defer foreign.Close()
			*pending.Directory = *foreign
			*pending.Destination = storage.Destination{}
			clear(pending.Candidate)
			pending.Name = "OTHER"
			if _, e = os.Stat(filepath.Join(root, "FIRST")); !os.IsNotExist(e) {
				t.Fatal("Update performed publication")
			}
			msg := c()
			before := len(r.Completed())
			if guard == "capacity" {
				r.mu.Lock()
				r.issued = 1024
				r.mu.Unlock()
			} else {
				if e = r.Close(); e != nil {
					t.Fatal(e)
				}
			}
			n, extra := m.Update(c())
			m = n.(Model)
			if extra != nil || m.State().PendingIO != 1 || len(r.Completed()) != before {
				t.Fatal("duplicate after guard consumed/reran")
			}
			n, bind := m.Update(msg)
			m = n.(Model)
			m = drain(m, bind)
			if m.State().Session.NewPhase != editor.PublishedUnbound {
				t.Fatal("closed/capped read falsely saved", m.State())
			}
			disk, e := os.ReadFile(filepath.Join(root, "FIRST"))
			if e != nil || !bytes.Equal(disk, mustNewExport(t, m)) {
				t.Fatal("getter retargeted candidate", e)
			}
		})
	}
}
func mustNewExport(t *testing.T, m Model) []byte {
	t.Helper()
	raw, e := m.Session().Document().Export()
	if e != nil {
		t.Fatal(e)
	}
	return raw
}
