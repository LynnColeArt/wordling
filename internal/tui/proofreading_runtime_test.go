package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/proofreading"
	"github.com/lynncoleart/wordling/internal/storage"
)

func openProofRuntime(t *testing.T, root string) (*Runtime, Model) {
	t.Helper()
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	r, m, err := Open(Config{Root: root, Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := r.Close(); err != nil {
			t.Error(err)
		}
	})
	return r, m
}

func startZorbly(t *testing.T, m Model) Model {
	t.Helper()
	m = inputKeys(t, m, textKey("zorbly"), tea.Key{Code: tea.KeyF2, Mod: tea.ModCtrl}, textKey("3"))
	if view := m.Session().ProofStatus(); view.Phase != editor.ProofQuestioning || view.Word != "zorbly" {
		t.Fatalf("normal startup did not open proofreading: %+v", view)
	}
	return m
}

func queueProofAdd(t *testing.T, m Model) (Model, tea.Cmd) {
	t.Helper()
	waiting, cmd := press(m, '3', 0, "3")
	if cmd == nil || waiting.State().PendingIO != 1 || waiting.Session().ProofStatus().Phase != editor.ProofDictionaryPending {
		t.Fatalf("Add must queue authentic host I/O: %+v", waiting.State())
	}
	return waiting, cmd
}

func TestProofRuntimeAuthenticatedOneShotAdd(t *testing.T) {
	root := t.TempDir()
	r, m := openProofRuntime(t, root)
	waiting, cmd := queueProofAdd(t, startZorbly(t, m))
	intent := waiting.State().Session.Pending
	foreign, _ := openProofRuntime(t, root)
	wrong := foreign.command(*intent)()
	next, _ := waiting.Update(wrong)
	waiting = next.(Model)
	if waiting.State().PendingIO != 1 {
		t.Fatal("foreign host result consumed pending Add")
	}
	next, _ = waiting.Update(resultMsg{editor.Result{Operation: intent.Operation, Revision: intent.Revision, Kind: intent.Kind}})
	waiting = next.(Model)
	if waiting.State().PendingIO != 1 {
		t.Fatal("bare public Result consumed pending Add")
	}
	var deliveries [2]tea.Msg
	var workers sync.WaitGroup
	for index := range deliveries {
		workers.Go(func() { deliveries[index] = cmd() })
	}
	workers.Wait()
	authentic, duplicate := 0, 0
	for _, delivery := range deliveries {
		switch result := delivery.(type) {
		case proofReply:
			authentic++
			if result.owner != r || result.result.Err != nil || result.result.Outcome.State != storage.Published {
				t.Fatalf("bad sealed result: %+v", result)
			}
			next, _ := waiting.Update(delivery)
			waiting = next.(Model)
		case duplicateDispatchMsg:
			duplicate++
		default:
			t.Fatalf("unexpected host message %T", delivery)
		}
	}
	if authentic != 1 || duplicate != 1 || waiting.State().PendingIO != 0 || waiting.Session().ProofStatus().Phase != editor.ProofCompleteAck {
		t.Fatalf("checked Add did not settle exactly once: %d/%d %+v", authentic, duplicate, waiting.State())
	}
	actual, err := os.ReadFile(filepath.Join(root, proofreading.DefaultSupplementaryName))
	if err != nil {
		t.Fatal(err)
	}
	original, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/spelling/proof/supplementary/WP{WP}US.SUP")
	if err != nil || !bytes.Equal(actual, original) {
		t.Fatal("normal runtime did not publish the exact original native SUP")
	}
	if results := r.Completed(); len(results) != 1 || results[0].Outcome.State != storage.Published {
		t.Fatalf("unexpected diagnostic operation receipts: %+v", results)
	}
}

func TestProofRuntimeResourceFailureAndCustomSelection(t *testing.T) {
	root := t.TempDir()
	path := filepath.Join(root, proofreading.DefaultSupplementaryName)
	invalid := []byte("not a native dictionary")
	if err := os.WriteFile(path, invalid, 0o600); err != nil {
		t.Fatal(err)
	}
	_, m := openProofRuntime(t, root)
	m = startZorbly(t, m)
	m, cmd := press(m, '3', 0, "3")
	if cmd != nil || !strings.Contains(m.State().Notice, "native framing") || m.Session().ProofStatus().Word != "zorbly" {
		t.Fatalf("malformed supplementary resource was silent: %+v", m.State())
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1), everydayKey(tea.KeyEnter),
		tea.Key{Code: tea.KeyF2, Mod: tea.ModCtrl}, textKey("4"), textKey("SPELLADD"), everydayKey(tea.KeyEnter))
	if view := m.Session().ProofStatus(); view.Phase != editor.ProofMenu || view.Dictionary != "SPELLADD" {
		t.Fatalf("replacement selection did not recover from invalid default: %+v", view)
	}
	m = inputKeys(t, m, textKey("3"), textKey("3"))
	if m.Session().ProofStatus().Phase != editor.ProofCompleteAck {
		t.Fatal("checked Add to selected dictionary failed")
	}
	got, err := os.ReadFile(path)
	if err != nil || !bytes.Equal(got, invalid) {
		t.Fatal("invalid original dictionary was overwritten")
	}
}

func TestProofRuntimeCancelAndClosePreventQueuedAdd(t *testing.T) {
	for _, closed := range []bool{false, true} {
		root := t.TempDir()
		r, m := openProofRuntime(t, root)
		waiting, cmd := queueProofAdd(t, startZorbly(t, m))
		if closed {
			if err := r.Close(); err != nil {
				t.Fatal(err)
			}
		} else {
			next, _ := waiting.Update(CancelPendingMsg{})
			waiting = next.(Model)
		}
		next, _ := waiting.Update(cmd())
		after := next.(Model)
		if after.State().PendingIO != 0 || after.Session().ProofStatus().Word != "zorbly" {
			t.Fatalf("settlement lost the suspect or left phantom I/O: %+v", after.State())
		}
		if _, err := os.Stat(filepath.Join(root, proofreading.DefaultSupplementaryName)); !os.IsNotExist(err) {
			t.Fatalf("unstarted Add escaped cancellation/close: %v", err)
		}
	}
}

func TestProofRuntimeStaleSupplementaryKeepsQuestion(t *testing.T) {
	root := t.TempDir()
	_, m := openProofRuntime(t, root)
	waiting, cmd := queueProofAdd(t, startZorbly(t, m))
	path := filepath.Join(root, proofreading.DefaultSupplementaryName)
	external := []byte("externally created")
	if err := os.WriteFile(path, external, 0o600); err != nil {
		t.Fatal(err)
	}
	next, _ := waiting.Update(cmd())
	after := next.(Model)
	if view := after.Session().ProofStatus(); after.State().PendingIO != 0 || view.Word != "zorbly" || view.Phase != editor.ProofQuestioning {
		t.Fatalf("stale publication advanced the suspect: %+v", view)
	}
	got, err := os.ReadFile(path)
	if err != nil || !bytes.Equal(got, external) || after.State().Session.Last.Result.Err == nil {
		t.Fatal("stale Add changed the external file or hid its failure")
	}
}

func TestProofRuntimeReadOnlySupplementaryRefusalPreservesBytes(t *testing.T) {
	root := t.TempDir()
	path := filepath.Join(root, proofreading.DefaultSupplementaryName)
	original, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/spelling/proof/supplementary/WP{WP}US.SUP")
	if err != nil {
		t.Fatal(err)
	}
	body := int(original[4])
	resource := append(bytes.Clone(original[:body]), []byte("another\n")...)
	if err := os.WriteFile(path, resource, 0o444); err != nil {
		t.Fatal(err)
	}
	_, m := openProofRuntime(t, root)
	waiting, cmd := queueProofAdd(t, startZorbly(t, m))
	next, _ := waiting.Update(cmd())
	after := next.(Model)
	receipt := after.State().Session.Last
	if receipt.Result.Err == nil || !strings.Contains(after.State().Notice, "read-only") || after.Session().ProofStatus().Word != "zorbly" {
		t.Fatalf("read-only dictionary should refuse and retain current suspect: %+v", receipt)
	}
	after = inputKeys(t, after, everydayKey(tea.KeyF1), everydayKey(tea.KeyEnter),
		tea.Key{Code: tea.KeyF2, Mod: tea.ModCtrl}, textKey("4"),
		textKey(proofreading.DefaultSupplementaryName), everydayKey(tea.KeyEnter))
	if view := after.Session().ProofStatus(); view.Phase != editor.ProofMenu || view.Dictionary != proofreading.DefaultSupplementaryName {
		t.Fatalf("read-only dictionary remains selectable for reading: %+v", view)
	}
	got, err := os.ReadFile(path)
	if err != nil || !bytes.Equal(got, resource) {
		t.Fatal("read-only dictionary changed")
	}
}
