package editor_test

import (
	"bytes"
	"context"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/proofreading"
	"github.com/lynncoleart/wordling/internal/storage"
)

func proofLive(t *testing.T, path string) (editor.Session, *storage.WorkspaceDirectory) {
	t.Helper()
	w, err := storage.OpenWorkspace(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { w.Close() })
	dir, err := w.Root()
	if err != nil {
		t.Fatal(err)
	}
	lex, err := proofreading.LoadLexicon()
	if err != nil {
		t.Fatal(err)
	}
	sup, err := proofreading.OpenSupplementary(context.Background(), w, dir, "WP{WP}US.SUP")
	if err != nil {
		t.Fatal(err)
	}
	s, err := editor.New(editor.Config{
		Locations:    []editor.Location{{Directory: dir.Directory()}},
		Workspace:    w,
		Proofreading: &editor.ProofResources{Lexicon: lex, Workspace: w, Directory: dir, Supplementary: sup},
	})
	if err != nil {
		t.Fatal(err)
	}
	return s, dir
}

func proofLiveStep(t *testing.T, s editor.Session, event editor.Event) (editor.Session, *editor.Intent) {
	t.Helper()
	next, intent, err := s.Reduce(event)
	if err != nil {
		t.Fatalf("event %#v at %v: %v", event, s.Snapshot().Mode, err)
	}
	return next, intent
}

func proofKey(t *testing.T, s editor.Session, cmd editor.Command) editor.Session {
	t.Helper()
	next, intent := proofLiveStep(t, s, editor.Event{Command: cmd})
	if intent != nil {
		t.Fatalf("unexpected intent %#v", intent)
	}
	return next
}

func proofType(t *testing.T, s editor.Session, text string) editor.Session {
	t.Helper()
	next, intent := proofLiveStep(t, s, editor.Event{Command: editor.Text, Text: text})
	if intent != nil {
		t.Fatalf("unexpected intent %#v", intent)
	}
	return next
}

func proofAtTop(t *testing.T, s editor.Session) editor.Session {
	t.Helper()
	for _, k := range []editor.Command{editor.Home, editor.Home, editor.Up} {
		s = proofKey(t, s, k)
	}
	return s
}

func proofChooseSuggestion(t *testing.T, s editor.Session, wanted string) editor.Session {
	t.Helper()
	for {
		v := s.ProofStatus()
		for i, choice := range v.Suggestions {
			if strings.EqualFold(choice, wanted) {
				return proofType(t, s, string(rune('a'+i)))
			}
		}
		if !v.More {
			t.Fatalf("provider did not offer %q: %+v", wanted, v)
		}
		s = proofKey(t, s, editor.Enter)
	}
}

func proofLiveBytes(t *testing.T, s editor.Session) []byte {
	t.Helper()
	native, err := s.Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	return native
}

func TestLiveProofWordThenPageReusesActualSuggestion(t *testing.T) {
	s, _ := proofLive(t, t.TempDir())
	s = proofType(t, s, "quik fox quik fox quik")
	s = proofAtTop(t, s)
	s = proofKey(t, s, editor.ProofCtrlF2)
	s = proofType(t, s, "1")
	if got := s.ProofStatus().Word; got != "quik" {
		t.Fatalf("Word scope at caret: %q", got)
	}
	s = proofChooseSuggestion(t, s, "quick")
	if s.Snapshot().Mode != editor.ProofMenuMode || !bytes.HasSuffix(proofLiveBytes(t, s), []byte("quick fox quik fox quik")) {
		t.Fatal("Word scope corrected more than its chosen word")
	}
	s = proofType(t, s, "2")
	if s.Snapshot().Mode != editor.ProofAckMode || !bytes.HasSuffix(proofLiveBytes(t, s), []byte("quick fox quick fox quick")) {
		t.Fatal("Page scope did not apply remembered replacement to actual bytes")
	}
}

func TestLiveProofCountAndInContextEdit(t *testing.T) {
	s, _ := proofLive(t, t.TempDir())
	s = proofType(t, s, "alpha 123abc 123 beta, don't can-t.")
	s = proofKey(t, s, editor.ProofCtrlF2)
	s = proofType(t, s, "6")
	if v := s.ProofStatus(); s.Snapshot().Mode != editor.ProofAckMode || v.Count != 6 || v.Partial {
		t.Fatalf("original Count flow: %+v", v)
	}
	s = proofKey(t, s, editor.ProofAdvance)
	if s.Snapshot().Mode != editor.ProofMenuMode {
		t.Fatal("Count acknowledgement must return to Check")
	}

	s, _ = proofLive(t, t.TempDir())
	s = proofType(t, s, "mispelled fox")
	s = proofKey(t, s, editor.ProofCtrlF2)
	s = proofType(t, s, "3")
	if s.ProofStatus().Word != "mispelled" {
		t.Fatalf("unexpected suspect: %+v", s.ProofStatus())
	}
	same := proofKey(t, s, editor.F7)
	if same.ProofStatus().Word != "mispelled" || same.Snapshot().Mode != editor.ProofAskMode {
		t.Fatal("F7 at Not Found unexpectedly exited")
	}
	s = proofType(t, s, "4")
	for range 3 {
		s = proofKey(t, s, editor.Right)
	}
	s = proofType(t, s, "s")
	s = proofKey(t, s, editor.F7)
	if s.Snapshot().Mode != editor.ProofAckMode || !bytes.HasSuffix(proofLiveBytes(t, s), []byte("misspelled fox")) {
		t.Fatal("Spell Edit typing did not resume the same proof pass")
	}
}

func TestLiveProofSkipLifetimeAndCheckedPersistentAdd(t *testing.T) {
	path := t.TempDir()
	s, _ := proofLive(t, path)
	s = proofType(t, s, "zorbly fox zorbly fox Zorbly")
	original := proofLiveBytes(t, s)
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	first := s.ProofStatus()
	s = proofKey(t, s, editor.ProofSkipOnce)
	second := s.ProofStatus()
	if second.Word != first.Word || second.Start <= first.Start {
		t.Fatal("Skip Once must move to the second occurrence only")
	}
	s = proofKey(t, s, editor.ProofSkip)
	if s.Snapshot().Mode != editor.ProofAckMode {
		t.Fatal("case-aware Skip should include the third occurrence")
	}
	s = proofKey(t, s, editor.ProofAdvance)
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	if v := s.ProofStatus(); v.Word != first.Word || v.Start != first.Start {
		t.Fatal("transient Skip leaked into a fresh pass")
	}
	pending, intent := proofLiveStep(t, s, editor.Event{Command: editor.ProofAdd})
	if intent == nil || intent.Kind != editor.ProofDictionaryIO {
		t.Fatal("Add has no real host I/O intent")
	}
	if _, err := os.Stat(filepath.Join(path, "WP{WP}US.SUP")); !os.IsNotExist(err) {
		t.Fatalf("reducer performed host I/O before intent: %v", err)
	}
	forged := editor.Result{Operation: intent.Operation, Revision: intent.Revision, Kind: intent.Kind}
	if _, _, err := pending.Reduce(editor.Event{Command: editor.Complete, Result: &forged}); err == nil {
		t.Fatal("a public result without provider receipt advanced Add")
	}
	result := editor.ExecuteProofreading(context.Background(), intent)
	if result.Err != nil {
		t.Fatal(result.Err)
	}
	applied, _ := proofLiveStep(t, pending, editor.Event{Command: editor.Complete, Result: &result})
	if !bytes.Equal(proofLiveBytes(t, applied), original) || applied.Snapshot().Mode != editor.ProofAckMode {
		t.Fatal("persistent Add either changed native content or failed to advance")
	}
	fresh, _ := proofLive(t, path)
	fresh = proofType(t, fresh, "Zorbly")
	fresh = proofType(t, proofKey(t, fresh, editor.ProofCtrlF2), "3")
	if fresh.Snapshot().Mode != editor.ProofAckMode {
		t.Fatal("fresh application resource observation did not accept the native SUP addition")
	}
}

func TestLiveProofCancelledAddCannotPublish(t *testing.T) {
	path := t.TempDir()
	s, _ := proofLive(t, path)
	s = proofType(t, s, "zorbly")
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	original := proofLiveBytes(t, s)
	pending, intent := proofLiveStep(t, s, editor.Event{Command: editor.ProofAdd})
	cancelled := proofKey(t, pending, editor.CancelOperation)
	result := editor.ExecuteProofreading(context.Background(), intent)
	if result.Err == nil {
		t.Fatal("cancelled, not-started intent executed")
	}
	if _, err := os.Stat(filepath.Join(path, "WP{WP}US.SUP")); !os.IsNotExist(err) {
		t.Fatalf("cancelled Add produced a native file: %v", err)
	}
	if !bytes.Equal(proofLiveBytes(t, cancelled), original) || cancelled.ProofStatus().Word != "zorbly" {
		t.Fatal("cancelled Add changed suspect or document")
	}
}

func TestLiveProofStandaloneLookupAndInterruptKeepNativeBytes(t *testing.T) {
	s, _ := proofLive(t, t.TempDir())
	s = proofType(t, s, "alpha zorbly")
	original := proofLiveBytes(t, s)
	s = proofKey(t, s, editor.ProofCtrlF2)
	s = proofType(t, s, "5")
	s = proofType(t, s, "qu?ck")
	s = proofKey(t, s, editor.Enter)
	v := s.ProofStatus()
	if !strings.Contains(strings.Join(v.Suggestions, " "), "quick") || !bytes.Equal(original, proofLiveBytes(t, s)) {
		t.Fatal("lookup did not show actual provider results on unchanged text")
	}
	s = proofType(t, s, "a")
	if s.ProofStatus().Draft != "a" || !bytes.Equal(original, proofLiveBytes(t, s)) {
		t.Fatal("standalone lookup treated a pattern letter as a replacement")
	}
	s = proofKey(t, s, editor.F1)
	if s.Snapshot().Mode != editor.ProofMenuMode {
		t.Fatal("standalone lookup F1 must return to Check")
	}
	s = proofType(t, s, "3")
	at := s.ProofStatus().Start
	s = proofKey(t, s, editor.F1)
	if v := s.ProofStatus(); s.Snapshot().Mode != editor.ProofAckMode || !v.Partial {
		t.Fatal("F1 at Not Found must produce partial word-count acknowledgement")
	}
	s = proofKey(t, s, editor.ProofAdvance)
	if s.Snapshot().Mode != editor.Editing || s.Snapshot().Gap != at || !bytes.Equal(original, proofLiveBytes(t, s)) {
		t.Fatal("partial-count acknowledge lost the native suspect location")
	}
}

func proofLoadOriginal(t *testing.T, name string) editor.Session {
	t.Helper()
	raw, err := os.ReadFile(filepath.Join("../../docs/research/everyday-contract-2026-11-05/qualification/", name))
	name = filepath.Base(name)
	if err != nil {
		t.Fatal(err)
	}
	path := t.TempDir()
	if err := os.WriteFile(filepath.Join(path, name), raw, 0600); err != nil {
		t.Fatal(err)
	}
	s, root := proofLive(t, path)
	listing, err := root.List("*.WP")
	if err != nil {
		t.Fatal(err)
	}
	for i, row := range listing.Entries() {
		if row.DOSName != name {
			continue
		}
		selected, err := listing.Select(i)
		if err != nil {
			t.Fatal(err)
		}
		s, intent := proofLiveStep(t, s, editor.Event{Command: editor.RetrieveSelection, Selection: selected})
		if intent == nil {
			t.Fatal("blank native Retrieve has no acquisition intent")
		}
		r := editor.ExecuteEveryday(intent)
		if r.Err != nil {
			t.Fatal(r.Err)
		}
		next, _ := proofLiveStep(t, s, editor.Event{Command: editor.Complete, Result: &r})
		if !bytes.Equal(proofLiveBytes(t, next), raw) {
			t.Fatal("real selected-file Retrieve altered original native bytes")
		}
		return next
	}
	t.Fatalf("original fixture %s absent in real file listing", name)
	return editor.Session{}
}

func TestLiveProofPageScopeAndFormattedOriginalOutput(t *testing.T) {
	s := proofLoadOriginal(t, "proof-pages/exports/BEFORE.WP")
	pageTwo := proofKey(t, s, editor.PageDown)
	pageTwo = proofType(t, proofKey(t, pageTwo, editor.ProofCtrlF2), "2")
	if pageTwo.ProofStatus().Word != "zorbly" {
		t.Fatalf("Page checks from current physical page, got %+v", pageTwo.ProofStatus())
	}

	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "2")
	if s.ProofStatus().Word != "quik" {
		t.Fatal("first formatted suspect missing")
	}
	s = proofChooseSuggestion(t, s, "quick")
	if s.ProofStatus().Word != "mispelled" {
		t.Fatal("second formatted suspect missing")
	}
	s = proofChooseSuggestion(t, s, "misspelled")
	if s.Snapshot().Mode != editor.ProofAckMode {
		t.Fatal("Page proof crossed its physical-page boundary")
	}
	want, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/proof-pages/exports/PAGEONLY.WP")
	if err != nil {
		t.Fatal(err)
	}
	// The qualified writer may set format flag bit 3, while all native owner
	// bytes must agree with the original proof-and-save observation.
	want[256] |= 8
	if !bytes.Equal(proofLiveBytes(t, s), want) {
		t.Fatal("Page correction, automatic repeated correction, or native owner retention differs from original")
	}
}

func TestLiveProofForeignResultAndStaleSupplementaryKeepActiveIssue(t *testing.T) {
	first, _ := proofLive(t, t.TempDir())
	path := t.TempDir()
	second, _ := proofLive(t, path)
	issue := func(s editor.Session) editor.Session {
		s = proofType(t, s, "zorbly")
		return proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	}
	first, firstRequest := proofLiveStep(t, issue(first), editor.Event{Command: editor.ProofAdd})
	second, secondRequest := proofLiveStep(t, issue(second), editor.Event{Command: editor.ProofAdd})
	success := editor.ExecuteProofreading(context.Background(), firstRequest)
	if success.Err != nil {
		t.Fatal(success.Err)
	}
	if _, _, err := second.Reduce(editor.Event{Command: editor.Complete, Result: &success}); err == nil {
		t.Fatal("another buffer's authentic result applied to same-looking pending Add")
	}
	first, _ = proofLiveStep(t, first, editor.Event{Command: editor.Complete, Result: &success})
	if first.Snapshot().Mode != editor.ProofAckMode {
		t.Fatal("authentic matching result did not apply")
	}
	external, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/spelling/proof/supplementary/SPELLADD")
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(path, "WP{WP}US.SUP"), external, 0600); err != nil {
		t.Fatal(err)
	}
	original := proofLiveBytes(t, second)
	failure := editor.ExecuteProofreading(context.Background(), secondRequest)
	if failure.Err == nil {
		t.Fatal("stale provider request overwrote an external dictionary")
	}
	after, _, _ := second.Reduce(editor.Event{Command: editor.Complete, Result: &failure})
	if after.ProofStatus().Word != "zorbly" || !bytes.Equal(original, proofLiveBytes(t, after)) {
		t.Fatal("failed Add changed native document or advanced current suspect")
	}
	got, err := os.ReadFile(filepath.Join(path, "WP{WP}US.SUP"))
	if err != nil || !bytes.Equal(got, external) {
		t.Fatal("failed Add altered external dictionary")
	}
}

func TestLiveProofOriginalCappedWordAndInteriorAttributeOutput(t *testing.T) {
	s := proofLoadOriginal(t, "proof-boundaries/exports/BEFORE.WP")
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	s = proofChooseSuggestion(t, s, "quick")
	s = proofChooseSuggestion(t, s, "misspelled")
	view := s.ProofStatus()
	if view.Word != strings.Repeat("X", 64) || view.End-view.Start != 64 {
		t.Fatalf("long word did not own exactly the first 64 native letters: %+v", view)
	}
	s = proofType(t, s, "5")
	s = proofType(t, s, "qu?ck")
	s = proofKey(t, s, editor.Enter)
	s = proofChooseSuggestion(t, s, "quick")
	if view := s.ProofStatus(); view.Word != "XYYYYYYYYYY" || view.Phase != editor.ProofQuestioning {
		t.Fatalf("the unconsumed residue was not checked next: %+v", view)
	}
	s = proofKey(t, proofKey(t, s, editor.F1), editor.ProofAdvance)
	root := "../../docs/research/everyday-contract-2026-11-05/qualification/proof-boundaries/exports/"
	expected, err := os.ReadFile(filepath.Join(root, "BOUNDARY.WP"))
	if err != nil {
		t.Fatal(err)
	}
	if actual := proofLiveBytes(t, s); !bytes.Equal(actual, expected) {
		t.Fatalf("native correction does not match stopped DOS fixture: %x versus %x", actual[324:], expected[324:])
	}
}

func TestLiveProofDoubleWordCaseAndIgnoreNumbers(t *testing.T) {
	s, _ := proofLive(t, t.TempDir())
	s = proofType(t, s, "The the the fox tWo 123abc 456abc")
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	if issue := s.ProofStatus().Issue; issue != editor.ProofDoubleWord {
		t.Fatalf("first issue %q", issue)
	}
	s = proofType(t, s, "3")
	if issue := s.ProofStatus().Issue; issue != editor.ProofDoubleWord {
		t.Fatalf("next adjacent duplicate issue %q", issue)
	}
	s = proofType(t, s, "3")
	if view := s.ProofStatus(); view.Issue != editor.ProofIrregularCase || view.Word != "tWo" {
		t.Fatalf("second issue %+v", view)
	}
	s = proofType(t, s, "3")
	if view := s.ProofStatus(); view.Issue != editor.ProofNotFound || view.Word != "123abc" {
		t.Fatalf("third issue %+v", view)
	}
	s = proofType(t, s, "6")
	if view := s.ProofStatus(); view.Phase != editor.ProofCompleteAck || view.Count != 5 {
		t.Fatalf("ignored numbers did not finish the pass: %+v", view)
	}
	if !bytes.HasSuffix(proofLiveBytes(t, s), []byte("The fox Two 123abc 456abc")) {
		t.Fatal("issue correction changed unrelated native words")
	}
}

func TestLiveProofBlockAndCustomDictionaryShareAcrossScreens(t *testing.T) {
	path := t.TempDir()
	s, _ := proofLive(t, path)
	s = proofAtTop(t, proofType(t, s, "the fox zorbly"))
	s = proofKey(t, s, editor.Block)
	for range len("the fox") {
		s = proofKey(t, s, editor.Right)
	}
	s = proofKey(t, s, editor.ProofCtrlF2)
	if view := s.ProofStatus(); view.Scope != editor.ProofBlock || view.Count != 2 || view.Phase != editor.ProofCompleteAck {
		t.Fatalf("Block did not go straight to its own count: %+v", view)
	}
	s = proofKey(t, s, editor.ProofAdvance)
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "4")
	s = proofType(t, s, "SPELLADD")
	s, request := proofLiveStep(t, s, editor.Event{Command: editor.Enter})
	result := editor.ExecuteProofreading(context.Background(), request)
	if result.Err != nil {
		t.Fatal(result.Err)
	}
	s, _ = proofLiveStep(t, s, editor.Event{Command: editor.Complete, Result: &result})
	if s.ProofStatus().Dictionary != "SPELLADD" || s.Snapshot().Mode != editor.ProofMenuMode {
		t.Fatal("custom dictionary creation did not return to Check")
	}
	s = proofType(t, s, "3")
	s, request = proofLiveStep(t, s, editor.Event{Command: editor.ProofAdd})
	result = editor.ExecuteProofreading(context.Background(), request)
	if result.Err != nil {
		t.Fatal(result.Err)
	}
	s, _ = proofLiveStep(t, s, editor.Event{Command: editor.Complete, Result: &result})
	s = proofKey(t, proofKey(t, s, editor.ProofAdvance), editor.SwitchDocument)
	s = proofType(t, s, "Zorbly")
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	if s.ProofStatus().Dictionary != "SPELLADD" || s.Snapshot().Mode != editor.ProofAckMode {
		t.Fatal("the second screen did not use the active dictionary")
	}
	got, err := os.ReadFile(filepath.Join(path, "SPELLADD"))
	if err != nil || !bytes.HasSuffix(got, []byte("zorbly\n")) {
		t.Fatalf("missing checked exact-name supplementary file: %v", err)
	}
}

func TestLiveProofOriginalSoftReturnCountAndUndelete(t *testing.T) {
	s := proofLoadOriginal(t, "history-repeat/exports/SRWORDS.WP")
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "6")
	if view := s.ProofStatus(); view.Count != 18 || view.Phase != editor.ProofCompleteAck {
		t.Fatalf("original SRt should separate words in Count: %+v", view)
	}
	s, _ = proofLive(t, t.TempDir())
	s = proofType(t, s, "  ONENE quik")
	s = proofAtTop(t, s)
	for range 5 {
		s = proofKey(t, s, editor.Right)
	}
	s = proofKey(t, proofKey(t, s, editor.Delete), editor.Delete)
	if s.Snapshot().HistoryCount != 1 {
		t.Fatal("missing original-style deleted group")
	}
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "3")
	s = proofChooseSuggestion(t, s, "quick")
	s = proofKey(t, s, editor.ProofAdvance)
	if s.Snapshot().HistoryCount != 1 {
		t.Fatal("proofing changed prior Undelete depth")
	}
	s = proofKey(t, s, editor.F1)
	s = proofKey(t, s, editor.Restore)
	if !bytes.HasSuffix(proofLiveBytes(t, s), []byte("  ONE quickNE")) {
		t.Fatal("proofing did not retain the exact prior NE fragment")
	}
}

func TestLiveProofWordFromNativeFormatBoundary(t *testing.T) {
	s := proofLoadOriginal(t, "proof-pages/exports/BEFORE.WP")
	for range 4 {
		s = proofKey(t, s, editor.Right)
	}
	s = proofType(t, proofKey(t, s, editor.ProofCtrlF2), "1")
	if view := s.ProofStatus(); view.Word != "quik" || view.Start != 5 || view.End != 9 {
		t.Fatalf("Word did not cross its zero-width enclosing Bold marker: %+v", view)
	}
}

func TestLiveProofDetachedDictionaryWriteDoesNotBindAnotherScreen(t *testing.T) {
	path := t.TempDir()
	s, _ := proofLive(t, path)
	s = proofType(t, proofKey(t, proofType(t, s, "zorbly"), editor.ProofCtrlF2), "3")
	pending, request := proofLiveStep(t, s, editor.Event{Command: editor.ProofAdd})
	result := editor.ExecuteProofreading(context.Background(), request)
	if result.Err != nil {
		t.Fatal(result.Err)
	}
	cancelled := proofKey(t, pending, editor.CancelOperation)
	cancelled = proofKey(t, proofKey(t, cancelled, editor.F1), editor.ProofAdvance)
	other := proofKey(t, cancelled, editor.SwitchDocument)
	other, _ = proofLiveStep(t, other, editor.Event{Command: editor.Complete, Result: &result})
	if !other.Snapshot().Detached.DestinationMayExist || other.Snapshot().Dirty ||
		other.Snapshot().Screen != 2 || other.ProofStatus().Phase != editor.ProofInactive {
		t.Fatal("detached real write was adopted or its disk effect was hidden")
	}
	if _, _, err := other.Reduce(editor.Event{Command: editor.Complete, Result: &result}); err == nil {
		t.Fatal("a settled dictionary completion could be replayed")
	}
	other = proofType(t, proofKey(t, proofType(t, other, "zorbly"), editor.ProofCtrlF2), "3")
	if other.ProofStatus().Word != "zorbly" {
		t.Fatal("detached receipt updated another screen's active vocabulary")
	}
}
