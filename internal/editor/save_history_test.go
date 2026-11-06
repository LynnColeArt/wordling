package editor_test

import (
	"bytes"
	"errors"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestIndependentWP29QualifiedPairDeleteThenF10(t *testing.T) {
	raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-direct-normal-delete-on-r1/N0000.WP5")
	if e != nil {
		t.Fatal(e)
	}
	s, _ := loadNative(t, raw)
	s = key(t, s, editor.Delete)
	s = browse(t, s, 3)
	s = key(t, s, editor.Right)
	s = key(t, s, editor.Delete)
	if s.Snapshot().Mode == editor.DeleteQuestion {
		s = key(t, s, editor.Yes)
	}
	before := s.Snapshot()
	image, _ := s.Document().Export()
	h := s.History()
	entry, _ := h.Entry(0)
	t.Logf("beforeF10 mode=%s gap=%d dirty=%v qualified=%v countKnown=%v fragments=%d entry=%x", before.Mode, before.Gap, before.Dirty, before.HistoryQualified, before.HistoryCountKnown, before.HistoryCount, entry.Native)
	if before.Gap != 1 || !before.Dirty || !before.HistoryQualified || before.HistoryCountKnown {
		t.Fatal("not actual WP40 context")
	}
	next, intent, err := s.Reduce(editor.Event{Command: editor.Save})
	after, _ := next.Document().Export()
	if !bytes.Equal(image, after) || next.Document().Revision() != s.Document().Revision() {
		t.Fatal("F10 changed native")
	}
	if err != nil || intent != nil || next.Snapshot().Mode != editor.SaveName {
		t.Fatalf("known F10 filename transition blocked by optional history: mode=%s err=%v", next.Snapshot().Mode, err)
	}
}

// These are the exact qualified WP40 command contexts, not a new history recipe.
func savePairContext(t *testing.T, view, direction, target string) (editor.Session, fixture) {
	t.Helper()
	name := "direct-" + view + "-" + direction + "-" + target
	if direction == "block" {
		name = "closing-block-repair-yes"
	}
	raw, err := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-" + name + "-r1/N0000.WP5")
	if err != nil {
		t.Fatal(err)
	}
	s, f := loadNative(t, raw)
	if view == "reveal" {
		s = key(t, s, editor.Reveal)
	}
	s = key(t, s, editor.Delete)
	s = browse(t, s, 3)
	gap := 1
	if target == "off" {
		gap = 4
	}
	if direction == "backspace" {
		gap++
	}
	for s.Snapshot().Gap < gap {
		s = key(t, s, editor.Right)
	}
	if direction == "block" {
		s = key(t, s, editor.Block)
		s = key(t, s, editor.Right)
	}
	c := editor.Delete
	if direction == "backspace" || direction == "block" {
		c = editor.Backspace
	}
	s = key(t, s, c)
	if s.Snapshot().Mode == editor.DeleteQuestion {
		s = key(t, s, editor.Yes)
	}
	if !s.Snapshot().HistoryQualified || s.Snapshot().HistoryCountKnown {
		t.Fatal("not bounded immediate history")
	}
	return s, f
}
func assertSuspendedHistory(t *testing.T, s editor.Session, h document.History) {
	t.Helper()
	x := s.Snapshot()
	if x.HistoryQualified || x.HistoryCountKnown || x.HistoryCount != h.Count() || s.History().Revision() != h.Revision() {
		t.Fatal("history reset, changed or requalified")
	}
	for n := 0; n < h.Count(); n++ {
		a, _ := h.Entry(n)
		b, _ := s.History().Entry(n)
		if !bytes.Equal(a.Native, b.Native) {
			t.Fatal("lost historical fragment")
		}
	}
	if x.Mode == editor.Editing {
		for _, c := range []editor.Command{editor.F1, editor.Delete, editor.Backspace, editor.Restore} {
			expectRefusal(t, s, editor.Event{Command: c})
		}
	}
}
func TestSaveBoundedHistoryContextsRetainFragmentsAndForks(t *testing.T) {
	cases := [][3]string{{"normal", "delete", "on"}, {"normal", "delete", "off"}, {"normal", "backspace", "on"}, {"normal", "backspace", "off"}, {"reveal", "delete", "on"}, {"reveal", "delete", "off"}, {"reveal", "backspace", "on"}, {"reveal", "backspace", "off"}, {"reveal", "block", "off"}}
	for _, c := range cases {
		t.Run(strings.Join(c[:], "-"), func(t *testing.T) {
			s, _ := savePairContext(t, c[0], c[1], c[2])
			before := s.Snapshot()
			raw, _ := s.Document().Export()
			source := s.Source().Identity()
			h := s.History()
			// Earlier immutable fork still has its exact immediate preview/Restore.
			name := "direct-" + c[0] + "-" + c[1] + "-" + c[2]
			if c[1] == "block" {
				name = "closing-block-repair-yes"
			}
			browsed := matchPreview40(t, s, originalRows(t, name, "r1", "immediate-target-history"))
			restored := key(t, key(t, browsed, editor.F1), editor.Restore)
			if restored.Document().Revision() == s.Document().Revision() {
				t.Fatal("pre-F10 Restore unavailable")
			}
			for _, cmd := range []editor.Command{editor.F7, editor.Home, editor.Reveal} {
				expectRefusal(t, s, editor.Event{Command: cmd})
			}
			named := key(t, s, editor.Save)
			after := named.Snapshot()
			unchanged(t, named, raw)
			if after.Mode != editor.SaveName || after.NativeRevision != before.NativeRevision || after.Revision != before.Revision || after.Gap != before.Gap || after.Dirty != before.Dirty || after.Reveal != before.Reveal || named.Source().Identity() != source {
				t.Fatal("F10 changed ordinary state")
			}
			assertSuspendedHistory(t, named, h)
			cancelled := key(t, named, editor.F1)
			assertSuspendedHistory(t, cancelled, h)
			unchanged(t, cancelled, raw)
			typed := text(t, cancelled, "X")
			assertSuspendedHistory(t, typed, h)
			if typed.Document().Revision() == before.NativeRevision || !typed.Snapshot().Dirty {
				t.Fatal("independent ASCII edit blocked")
			}
			if !s.Snapshot().HistoryQualified || s.History().Revision() != h.Revision() {
				t.Fatal("mutated earlier fork")
			}
			// Distinct buffer permissions cannot restore the suspended first buffer.
			if c[0] == "normal" {
				other := key(t, cancelled, editor.SwitchDocument)
				back := key(t, other, editor.SwitchDocument)
				assertSuspendedHistory(t, back, h)
			}
		})
	}
}
func TestSaveBoundedHistoryRealPublicationAndOutcomes(t *testing.T) {
	for _, outcome := range []string{"success", "cancel", "fault", "stale", "uncertain", "source-change", "target-change", "wrong-operation", "wrong-revision", "wrong-kind"} {
		t.Run(outcome, func(t *testing.T) {
			s, f := savePairContext(t, "normal", "delete", "on")
			h := s.History()
			raw, _ := s.Document().Export()
			source := s.Source().Identity()
			rev := s.Document().Revision()
			s, i := queued(t, s, "CANDIDA")
			if i == nil || i.Kind != editor.PublishCandidate || !bytes.Equal(i.Candidate, raw) || i.Document.Identity() != source {
				t.Fatal("not actual candidate/source")
			}
			var r editor.Result
			switch outcome {
			case "cancel":
				s = key(t, s, editor.CancelOperation)
				r = perform(i)
			case "fault":
				r = editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Err: errors.New("host failed before publication")}
			case "uncertain":
				r = editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind, Err: &storage.Failure{Kind: storage.PublicationUncertain, DestinationMayExist: true, Candidate: "retained-witness"}}
			case "stale":
				s = text(t, s, "X")
				r = perform(i)
			case "source-change":
				if e := os.WriteFile(filepath.Join(f.path, "ORIGIN"), append(f.raw, 'Q'), 0600); e != nil {
					t.Fatal(e)
				}
				r = perform(i)
				if r.Err == nil {
					t.Fatal("stale source published")
				}
			case "target-change":
				if e := os.WriteFile(filepath.Join(f.path, "CANDIDA"), f.raw, 0600); e != nil {
					t.Fatal(e)
				}
				r = perform(i)
				if r.Err == nil {
					t.Fatal("late target overwritten")
				}
			default:
				r = perform(i)
			}
			switch outcome {
			case "wrong-operation":
				r.Operation++
			case "wrong-revision":
				r.Revision++
			case "wrong-kind":
				r.Kind = editor.Read
			}
			s, _ = done(t, s, r)
			assertSuspendedHistory(t, s, h)
			if s.Source().Identity() != source {
				t.Fatal("source rebased")
			}
			if outcome == "success" {
				x := s.Snapshot()
				if x.Dirty || x.SavedRevision != rev || x.PublishedRevision != rev || x.Name != "B:\\CANDIDA" {
					t.Fatal("matching publication not saved")
				}
				disk, e := f.dir.Read("CANDIDA")
				if e != nil || !bytes.Equal(disk.Export(), raw) {
					t.Fatal("published bytes differ")
				}
				s, _ = done(t, s, r)
				assertSuspendedHistory(t, s, h)
				if !s.Snapshot().Detached.DestinationMayExist {
					t.Fatal("duplicate outcome hidden")
				}
			} else {
				if !s.Snapshot().Dirty || s.Snapshot().Name != "B:\\ORIGIN" {
					t.Fatal("failed/stale outcome false clean/name")
				}
			}
			if outcome == "uncertain" && (s.Snapshot().SaveState != editor.SaveUncertain || !s.Snapshot().Last.DestinationMayExist) {
				t.Fatal("uncertain effects lost")
			}
		})
	}
}

func TestPlainSaveSeparationRemainsQualified(t *testing.T) {
	f := setup(t)
	s := load(t, f)
	s = key(t, s, editor.Delete)
	if !s.Snapshot().HistoryCountKnown {
		t.Fatal("plain initial stack unknown")
	}
	s = key(t, key(t, s, editor.Save), editor.F1)
	if !s.Snapshot().HistoryQualified || !s.Snapshot().HistoryCountKnown {
		t.Fatal("plain filename cancel lost known history")
	}
	s, i := queued(t, s, "PLAIN")
	s, _ = done(t, s, perform(i))
	if !s.Snapshot().HistoryQualified || !s.Snapshot().HistoryCountKnown {
		t.Fatal("plain successful Save separation changed")
	}
	s = key(t, s, editor.Right)
	if !s.Snapshot().HistoryQualified {
		t.Fatal("plain Right separator changed")
	}
}

// Finite state-boundary fuzz: <=64 public events, no IO within the generated
// sequence, a single loaded/qualified immutable base and real captured fragments.
func FuzzSaveHistoryInterleavings(f *testing.F) {
	root := f.TempDir()
	raw, e := os.ReadFile("../../docs/research/continuation/code-pair-history/runs/wp40-direct-normal-delete-on-r1/N0000.WP5")
	if e != nil {
		f.Fatal(e)
	}
	if e = os.WriteFile(filepath.Join(root, "ORIGIN"), raw, 0600); e != nil {
		f.Fatal(e)
	}
	dir, e := storage.OpenDirectory(root)
	if e != nil {
		f.Fatal(e)
	}
	defer dir.Close()
	base, e := editor.New(editor.Config{Locations: []editor.Location{{Prefix: "B:\\", Directory: dir}}})
	if e != nil {
		f.Fatal(e)
	}
	send := func(c editor.Command, txt string) {
		var i *editor.Intent
		var err error
		base, i, err = base.Reduce(editor.Event{Command: c, Text: txt})
		if err != nil {
			f.Fatal(err)
		}
		if i != nil {
			r := perform(i)
			base, _, err = base.Reduce(editor.Event{Command: editor.Complete, Result: &r})
			if err != nil {
				f.Fatal(err)
			}
		}
	}
	send(editor.Retrieve, "")
	send(editor.Text, "B:\\ORIGIN")
	send(editor.Enter, "")
	send(editor.Delete, "")
	send(editor.F1, "")
	for range 3 {
		send(editor.Previous, "")
	}
	send(editor.F1, "")
	send(editor.Right, "")
	send(editor.Delete, "")
	send(editor.Yes, "")
	f.Add([]byte{0, 1, 2, 3, 4, 5, 6, 7, 8, 9})
	f.Add([]byte{0, 1, 0, 2, 4, 8, 9, 5})
	f.Fuzz(func(t *testing.T, in []byte) {
		if len(in) > 64 {
			t.Skip()
		}
		s := base
		h := base.History()
		suspended := false
		for _, v := range in {
			cmd := []editor.Command{editor.Save, editor.F1, editor.Text, editor.Enter, editor.CancelOperation, editor.Delete, editor.Backspace, editor.Right, editor.Reveal, editor.SwitchDocument}[v%10]
			txt := ""
			if cmd == editor.Text {
				txt = "X"
			}
			old := s
			next, _, err := s.Reduce(editor.Event{Command: cmd, Text: txt})
			if err != nil {
				if next.Document().Revision() != old.Document().Revision() {
					t.Fatal("refusal changed native")
				}
				continue
			}
			s = next
			if cmd == editor.Save && old.Snapshot().Mode == editor.Editing {
				if !suspended {
					h = old.History()
				}
				suspended = true
			}
			if suspended && s.Snapshot().Screen == 1 {
				assertSuspendedHistory(t, s, h)
			}
		}
	})
}
