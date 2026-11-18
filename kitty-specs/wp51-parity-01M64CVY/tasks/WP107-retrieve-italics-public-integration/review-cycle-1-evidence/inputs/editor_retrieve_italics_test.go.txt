package editor_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"github.com/lynncoleart/wordling/internal/wp51"
)

var riOn = []byte{0xc3, 8, 0xc3}
var riOff = []byte{0xc4, 8, 0xc4}
var riBoldOn = []byte{0xc3, 12, 0xc3}
var riBoldOff = []byte{0xc4, 12, 0xc4}
var riUndOn = []byte{0xc3, 14, 0xc3}
var riUndOff = []byte{0xc4, 14, 0xc4}

func riCat(parts ...[]byte) []byte { return bytes.Join(parts, nil) }
func riOriginal(t *testing.T) []byte {
	t.Helper()
	b, e := os.ReadFile("../../docs/research/reference-runs/mission1-appearance/ITALICS.WP")
	if e != nil {
		t.Fatal(e)
	}
	if fmt.Sprintf("%x", sha256.Sum256(b)) != "24470a1f57bf84cd38527041d8e2d99b0f4330f5a8d442ce43230b334299f7c7" {
		t.Fatal("original fixture pin")
	}
	return b
}

// All substituted bodies are synthetic disposable test inputs. The constructor's
// receiver prefix never becomes the expected source of inserted body owners.
func riImage(t *testing.T, body []byte) []byte {
	t.Helper()
	d, e := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if e != nil {
		t.Fatal(e)
	}
	b, e := d.Export()
	if e != nil {
		t.Fatal(e)
	}
	return append(b, body...)
}
func riWrite(t *testing.T, path string, b []byte) {
	t.Helper()
	if e := os.WriteFile(path, b, 0600); e != nil {
		t.Fatal(e)
	}
}
func riSelect(t *testing.T, dir *storage.WorkspaceDirectory, name string) *storage.EntrySelection {
	t.Helper()
	l, e := dir.List(name)
	if e != nil {
		t.Fatal(e)
	}
	s, e := l.Select(l.Find(name))
	if e != nil {
		t.Fatal(e)
	}
	return s
}
func riNative(t *testing.T, s editor.Session) []byte {
	t.Helper()
	b, e := s.Document().Export()
	if e != nil {
		t.Fatal(e)
	}
	return b
}
func riFixture(t *testing.T, receiver, source []byte) (*storage.Workspace, *storage.WorkspaceDirectory, editor.Session, string) {
	t.Helper()
	root := t.TempDir()
	riWrite(t, filepath.Join(root, "RECEIVER.WP"), riImage(t, receiver))
	riWrite(t, filepath.Join(root, "SOURCE.WP"), source)
	w, dir, s := liveWorkspace(t, root)
	s, i := liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: riSelect(t, dir, "RECEIVER.WP")})
	s, _ = liveDispatch(t, s, i)
	if s.Source() == nil || s.Source().Name() != "RECEIVER.WP" || s.Snapshot().Dirty {
		t.Fatal("real loaded receiver setup")
	}
	return w, dir, s, root
}
func riGap(t *testing.T, s editor.Session, gap int) editor.Session {
	t.Helper()
	if !s.Snapshot().Reveal {
		s = liveKeys(t, s, editor.Reveal)
	}
	for n := 0; s.Snapshot().Gap != gap; n++ {
		if n > document.MaxMutationTokens+2 {
			t.Fatal("gap movement failed")
		}
		cmd := editor.Right
		if s.Snapshot().Gap > gap {
			cmd = editor.Left
		}
		s = liveKeys(t, s, cmd)
	}
	return s
}
func riRequest(t *testing.T, s editor.Session, selection *storage.EntrySelection) (editor.Session, *editor.Intent) {
	t.Helper()
	next, i := liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selection})
	if i != nil || next.Snapshot().Mode != editor.RetrieveInsertQuestion {
		t.Fatal("occupied retrieval read before Yes")
	}
	next, i = liveEvent(t, next, editor.Event{Command: editor.Yes})
	if i == nil || i.Kind != editor.ReadSelection {
		t.Fatal("missing authenticated selected read after Yes")
	}
	return next, i
}
func riRead(t *testing.T, s editor.Session, selection *storage.EntrySelection) (editor.Session, editor.Result) {
	t.Helper()
	s, i := riRequest(t, s, selection)
	result := editor.ExecuteEveryday(i)
	s, next := liveEvent(t, s, editor.Event{Command: editor.Complete, Result: &result})
	if next != nil {
		t.Fatal("unexpected continuation")
	}
	return s, result
}
func riExpected(t *testing.T, before []byte, gap int, body []byte) []byte {
	t.Helper()
	d, e := document.Parse(before)
	if e != nil {
		t.Fatal(e)
	}
	c, e := d.CursorAt(gap)
	if e != nil {
		t.Fatal(e)
	}
	off, e := c.Offset()
	if e != nil {
		t.Fatal(e)
	}
	want := riCat(before[:off], body, before[off:])
	im, e := wp51.Parse(before)
	if e != nil {
		t.Fatal(e)
	}
	flags := -1
	for _, p := range im.Inspect().Packets {
		if p.Type == 6 {
			flags = p.Data.Offset
		}
	}
	if flags < 0 {
		t.Fatal("missing receiver flag owner")
	}
	want[flags] |= 8
	return want
}
func riCategory(t *testing.T, e error, want document.Category) {
	t.Helper()
	var f *document.Failure
	if !errors.As(e, &f) || f.Category != want {
		t.Fatalf("want %s, actual %v", want, e)
	}
}
func riUnchanged(t *testing.T, before, after editor.Session) {
	t.Helper()
	a, b := before.Snapshot(), after.Snapshot()
	if !bytes.Equal(riNative(t, before), riNative(t, after)) || before.Document().Birth() != after.Document().Birth() || a.NativeRevision != b.NativeRevision || a.Gap != b.Gap || a.Dirty != b.Dirty || a.Name != b.Name || a.GenesisRevision != b.GenesisRevision || a.NewPhase != b.NewPhase || a.HistoryQualified != b.HistoryQualified || a.HistoryCountKnown != b.HistoryCountKnown || a.HistoryCount != b.HistoryCount || before.History().Revision() != after.History().Revision() {
		t.Fatal("refusal changed native/caret/birth/name/dirty/history")
	}
	if (before.Source() == nil) != (after.Source() == nil) {
		t.Fatal("receiver binding lost")
	}
	if before.Source() != nil && before.Source().Identity() != after.Source().Identity() {
		t.Fatal("receiver source rebound")
	}
}
func riEvidence(t *testing.T, s editor.Session, source []byte) {
	t.Helper()
	if dir := os.Getenv("WORDLING_WP107_EVIDENCE"); dir != "" {
		if e := os.MkdirAll(dir, 0700); e != nil {
			t.Fatal(e)
		}
		record := struct {
			Test                     string
			BodySHA256, SourceSHA256 [32]byte
			State                    editor.Snapshot
		}{t.Name(), sha256.Sum256(riNative(t, s)), sha256.Sum256(source), s.Snapshot()}
		b, e := json.MarshalIndent(record, "", "  ")
		if e != nil {
			t.Fatal(e)
		}
		name := fmt.Sprintf("editor-%x.json", sha256.Sum256([]byte(t.Name())))
		riWrite(t, filepath.Join(dir, name), b)
	}
}

func TestRetrieveItalicsPublicSelectedBoundaries(t *testing.T) {
	receiver := riCat([]byte("L"), riOn, []byte("AB"), riOff, []byte("R"))
	for _, kind := range []string{"original", "surrounded", "multiple"} {
		for gap := 0; gap <= 6; gap++ {
			t.Run(fmt.Sprintf("%s/gap%d", kind, gap), func(t *testing.T) {
				source, body, count := riOriginal(t), riCat(riOn, []byte("alpha"), riOff, []byte("beta")), 11
				if kind == "surrounded" {
					body = riCat([]byte("p"), riOn, []byte("i"), riOff, []byte("s"))
					source = riImage(t, body)
					count = 5
				}
				if kind == "multiple" {
					body = riCat(riOn, []byte("a"), riOff, []byte("-"), riOn, []byte("b"), riOff)
					source = riImage(t, body)
					count = 7
				}
				w, dir, s, root := riFixture(t, receiver, source)
				s = riGap(t, s, gap)
				before := s
				raw := riNative(t, s)
				receiverDisk := liveReadBytes(t, filepath.Join(root, "RECEIVER.WP"))
				selected := riSelect(t, dir, "SOURCE.WP")
				pending, i := riRequest(t, s, selected)
				if !editor.EverydayIntentOwnedBy(i, w) {
					t.Fatal("request lost workspace authority")
				}
				r := editor.ExecuteEveryday(i)
				if r.Err != nil || r.Document == nil || !selected.MatchesDocument(r.Document) {
					t.Fatalf("actual selected read failed: %v", r.Err)
				}
				s, _ = liveEvent(t, pending, editor.Event{Command: editor.Complete, Result: &r})
				if gap >= 2 && gap <= 4 {
					riCategory(t, s.Snapshot().Last.Result.Err, document.UnsupportedBody)
					riUnchanged(t, before, s)
					if !s.Snapshot().Last.Applied || s.Snapshot().Last.Result.Document == nil {
						t.Fatal("real read/refusal accounting hidden")
					}
				} else {
					if e := s.Snapshot().Last.Result.Err; e != nil {
						t.Fatalf("balanced public source insertion failed: %v", e)
					}
					if !bytes.Equal(riNative(t, s), riExpected(t, raw, gap, body)) || s.Snapshot().Gap != gap+count || !s.Snapshot().Dirty || s.Source().Identity() != before.Source().Identity() || s.Document().Birth() != before.Document().Birth() || !s.Snapshot().HistoryQualified {
						t.Fatal("public exact owners/caret/dirty/receiver provenance")
					}
				}
				if !bytes.Equal(liveReadBytes(t, filepath.Join(root, "SOURCE.WP")), source) || !bytes.Equal(liveReadBytes(t, filepath.Join(root, "RECEIVER.WP")), receiverDisk) {
					t.Fatal("Retrieve changed disk inputs")
				}
				riEvidence(t, s, source)
			})
		}
	}
}

func TestRetrieveItalicsPublicVariantsAndNew(t *testing.T) {
	for _, kind := range []string{"plain-inside", "bold", "underline", "both", "crossing-source", "empty"} {
		t.Run(kind, func(t *testing.T) {
			body := riCat(riOn, []byte("i"), riOff)
			receiver := []byte("LR")
			gap, count := 1, 3
			switch kind {
			case "plain-inside":
				receiver = riCat(riOn, []byte("AB"), riOff)
				body = []byte("plain")
				gap, count = 2, 5
			case "bold":
				receiver = riCat(riBoldOn, []byte("AB"), riBoldOff)
				gap = 2
			case "underline":
				receiver = riCat(riUndOn, []byte("AB"), riUndOff)
				gap = 2
			case "both":
				receiver = riCat(riBoldOn, riUndOn, []byte("AB"), riUndOff, riBoldOff)
				gap = 3
			case "crossing-source":
				body = riCat(riBoldOn, riOn, []byte("a"), riBoldOff, []byte("b"), riOff)
				count = 6
			case "empty":
				body = nil
				count = 0
			}
			source := riImage(t, body)
			_, dir, s, root := riFixture(t, receiver, source)
			s = riGap(t, s, gap)
			before := s
			s, read := riRead(t, s, riSelect(t, dir, "SOURCE.WP"))
			if read.Err != nil || s.Snapshot().Last.Result.Err != nil {
				t.Fatalf("public admitted variant refused: %v / %v", read.Err, s.Snapshot().Last.Result.Err)
			}
			if count == 0 {
				riUnchanged(t, before, s)
			} else if !bytes.Equal(riNative(t, s), riExpected(t, riNative(t, before), gap, body)) || s.Snapshot().Gap != gap+count {
				t.Fatal("variant native owners/caret")
			}
			if !bytes.Equal(liveReadBytes(t, filepath.Join(root, "SOURCE.WP")), source) {
				t.Fatal("source changed")
			}
		})
	}
	t.Run("edited-New", func(t *testing.T) {
		path := t.TempDir()
		source := riOriginal(t)
		riWrite(t, filepath.Join(path, "SOURCE.WP"), source)
		_, dir, s := liveWorkspace(t, path)
		birth, genesis := s.Document().Birth(), s.Snapshot().GenesisRevision
		s = liveText(t, s, "LEFTRIGHT")
		s = riGap(t, s, 4)
		before := s
		s, r := riRead(t, s, riSelect(t, dir, "SOURCE.WP"))
		if r.Err != nil || s.Snapshot().Last.Result.Err != nil {
			t.Fatalf("balanced public New source insertion failed: %v / %v", r.Err, s.Snapshot().Last.Result.Err)
		}
		want := riCat(riOn, []byte("alpha"), riOff, []byte("beta"))
		if !bytes.Equal(riNative(t, s), riExpected(t, riNative(t, before), 4, want)) || s.Document().Birth() != birth || s.Snapshot().GenesisRevision != genesis || s.Source() != nil || s.Snapshot().Name != "" || s.Snapshot().NewPhase != editor.NewUnpublished || !s.Snapshot().Dirty {
			t.Fatal("actual New genesis/body/name/binding")
		}
		riEvidence(t, s, source)
	})
}

func TestRetrieveItalicsPublicRefusalInputs(t *testing.T) {
	for name, body := range map[string][]byte{"duplicate": riCat(riOn, riOn, []byte("i"), riOff, riOff), "unmatched": riOff, "unclosed": riCat(riOn, []byte("i")), "opaque": {0x80}, "unsafe-page": {0x8c, 'x'}, "token-limit": bytes.Repeat([]byte("x"), document.MaxMutationTokens+1), "byte-limit": bytes.Repeat([]byte{0xc1, 2, 8, 7, 8, 7, 15, 0, 0xc1}, document.MaxMutationBytes/9+1), "duplicate-bold": riCat(riBoldOn, riOn, []byte("i"), riOff, riBoldOff)} {
		t.Run(name, func(t *testing.T) {
			receiver := []byte("LR")
			gap := 1
			if name == "duplicate-bold" {
				receiver = riCat(riBoldOn, []byte("LR"), riBoldOff)
				gap = 2
			}
			source := riImage(t, body)
			_, dir, s, root := riFixture(t, receiver, source)
			s = riGap(t, s, gap)
			before := s
			disk := liveReadBytes(t, filepath.Join(root, "RECEIVER.WP"))
			s, r := riRead(t, s, riSelect(t, dir, "SOURCE.WP"))
			if r.Err != nil {
				t.Fatalf("test source was not actually acquired: %v", r.Err)
			}
			want := document.UnsupportedBody
			if name == "token-limit" || name == "byte-limit" {
				want = document.MutationLimit
			}
			riCategory(t, s.Snapshot().Last.Result.Err, want)
			riUnchanged(t, before, s)
			if !bytes.Equal(liveReadBytes(t, filepath.Join(root, "SOURCE.WP")), source) || !bytes.Equal(liveReadBytes(t, filepath.Join(root, "RECEIVER.WP")), disk) {
				t.Fatal("refusal changed disks")
			}
			riEvidence(t, s, source)
		})
	}
}

func TestRetrieveItalicsPublicDeclineStaleForeign(t *testing.T) {
	for _, answer := range []editor.Command{editor.No, editor.Enter, editor.F1, editor.Escape} {
		t.Run(fmt.Sprint(answer), func(t *testing.T) {
			source := riOriginal(t)
			_, dir, s, root := riFixture(t, []byte("LR"), source)
			selected := riSelect(t, dir, "SOURCE.WP")
			before := s
			pending, i := liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selected})
			if i != nil {
				t.Fatal("pre-answer read")
			}
			if e := os.Remove(filepath.Join(root, "SOURCE.WP")); e != nil {
				t.Fatal(e)
			}
			s, i = liveEvent(t, pending, editor.Event{Command: answer})
			if i != nil || s.Snapshot().Last.Result.Operation != before.Snapshot().Last.Result.Operation {
				t.Fatal("decline performed acquisition")
			}
			riUnchanged(t, before, s)
		})
	}
	t.Run("stale-selected-read", func(t *testing.T) {
		source := riOriginal(t)
		_, dir, s, root := riFixture(t, []byte("LR"), source)
		selected := riSelect(t, dir, "SOURCE.WP")
		before := s
		pending, i := riRequest(t, s, selected)
		riWrite(t, filepath.Join(root, "SOURCE.WP"), riImage(t, []byte("changed")))
		r := editor.ExecuteEveryday(i)
		if r.Err == nil {
			t.Fatal("stale selected source acquired")
		}
		s, _ = liveEvent(t, pending, editor.Event{Command: editor.Complete, Result: &r})
		riUnchanged(t, before, s)
	})
	t.Run("foreign-selection", func(t *testing.T) {
		source := riOriginal(t)
		_, _, s, root := riFixture(t, []byte("LR"), source)
		foreign, e := storage.OpenWorkspace(root)
		if e != nil {
			t.Fatal(e)
		}
		defer foreign.Close()
		dir, e := foreign.Root()
		if e != nil {
			t.Fatal(e)
		}
		next, i, e := s.Reduce(editor.Event{Command: editor.RetrieveSelection, Selection: riSelect(t, dir, "SOURCE.WP")})
		if e == nil || i != nil {
			t.Fatal("foreign selection accepted")
		}
		riUnchanged(t, s, next)
	})
}

func TestRetrieveItalicsPublicLateAndForeignCompletion(t *testing.T) {
	source := riOriginal(t)
	_, dir, a, _ := riFixture(t, []byte("FIRST"), source)
	_, otherDir, b, _ := riFixture(t, []byte("OTHER"), source)
	a = riGap(t, a, 2)
	before := a
	a, i := riRequest(t, a, riSelect(t, dir, "SOURCE.WP"))
	_, j := riRequest(t, b, riSelect(t, otherDir, "SOURCE.WP"))
	foreign := editor.ExecuteEveryday(j)
	a, _ = liveEvent(t, a, editor.Event{Command: editor.Complete, Result: &foreign})
	if a.Snapshot().Pending == nil || a.Snapshot().Pending.Operation != i.Operation {
		t.Fatal("genuine foreign read settled request")
	}
	riUnchanged(t, before, a)
	a = liveKeys(t, a, editor.CancelOperation)
	a, k := riRequest(t, a, riSelect(t, dir, "SOURCE.WP"))
	late := editor.ExecuteEveryday(i)
	a, _ = liveEvent(t, a, editor.Event{Command: editor.Complete, Result: &late})
	if a.Snapshot().Pending == nil || a.Snapshot().Pending.Operation != k.Operation || a.Snapshot().Detached.Applied {
		t.Fatal("late read consumed current request")
	}
	riUnchanged(t, before, a)
	fresh := editor.ExecuteEveryday(k)
	a, _ = liveEvent(t, a, editor.Event{Command: editor.Complete, Result: &fresh})
	if a.Snapshot().Last.Result.Err != nil {
		t.Fatalf("balanced public retry failed: %v", a.Snapshot().Last.Result.Err)
	}
}

func TestRetrieveItalicsPublicHistory(t *testing.T) {
	source := riOriginal(t)
	_, dir, s, _ := riFixture(t, []byte("XLEFTRIGHT"), source)
	s = riGap(t, s, 0)
	s = liveKeys(t, s, editor.Delete)
	if s.Snapshot().HistoryCount != 1 {
		t.Fatal("actual deletion did not create history")
	}
	entry, e := s.History().Entry(0)
	if e != nil || string(entry.Native) != "X" {
		t.Fatal("deletion history setup")
	}
	s = riGap(t, s, 4)
	s, _ = riRead(t, s, riSelect(t, dir, "SOURCE.WP"))
	if e := s.Snapshot().Last.Result.Err; e != nil {
		t.Fatalf("balanced public history insertion failed: %v", e)
	}
	entry, e = s.History().Entry(0)
	if e != nil || string(entry.Native) != "X" {
		t.Fatal("Retrieval lost prior deletion")
	}
	before := riNative(t, s)
	gap := s.Snapshot().Gap
	s = liveKeys(t, s, editor.F1, editor.Restore)
	if s.Snapshot().Gap != gap+1 || !bytes.Equal(riNative(t, s), riExpected(t, before, gap, []byte("X"))) {
		t.Fatal("public history restoration/caret")
	}
}

func TestRetrieveItalicsPublicCopyProducer(t *testing.T) {
	source, err := os.ReadFile("../../docs/research/reference-runs/mission1-appearance/ITALICS.WP")
	if err != nil {
		t.Fatal(err)
	}
	if fmt.Sprintf("%x", sha256.Sum256(source)) != "24470a1f57bf84cd38527041d8e2d99b0f4330f5a8d442ce43230b334299f7c7" {
		t.Fatal("fixture pin")
	}
	path := t.TempDir()
	if err = os.WriteFile(filepath.Join(path, "ITALICS.WP"), source, 0600); err != nil {
		t.Fatal(err)
	}
	_, root, s := liveWorkspace(t, path)
	listing, err := root.List("*.WP")
	if err != nil {
		t.Fatal(err)
	}
	selected, err := listing.Select(listing.Find("ITALICS.WP"))
	if err != nil {
		t.Fatal(err)
	}
	s, intent := liveEvent(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selected})
	s, _ = liveDispatch(t, s, intent)
	s = liveKeys(t, s, editor.Reveal, editor.Block)
	for range 7 {
		s = liveKeys(t, s, editor.Right)
	}
	if snap := s.Snapshot(); !snap.Selection || snap.SelectionStart != 0 || snap.SelectionEnd != 7 {
		t.Fatalf("real public whole-run selection: %+v", snap)
	}
	before, _ := s.Document().Export()
	s = liveKeys(t, s, editor.MoveMenu)
	s = liveText(t, s, "1")
	next, intent, err := s.Reduce(editor.Event{Command: editor.Text, Text: "2"})
	if err != nil {
		t.Fatalf("public Italics Copy producer refused complete real acquired run before InsertBlockCopy: %v", err)
	}
	if intent != nil || next.Snapshot().Mode != editor.CopyTargetMode {
		t.Fatal("missing genuine Copy target")
	}
	next = liveKeys(t, next, editor.Right, editor.Right, editor.Right, editor.Right, editor.Enter)
	raw, _ := next.Document().Export()
	if !bytes.Equal(raw, riExpected(t, before, 11, riCat(riOn, []byte("alpha"), riOff))) || next.Snapshot().Gap != 11 || !next.Snapshot().HistoryQualified {
		t.Fatal("public Copy exact source owners/caret/history")
	}
}
