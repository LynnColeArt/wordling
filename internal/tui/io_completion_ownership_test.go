package tui

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

// Each row enters through actual Model.Update keys and holds the returned Cmd.
// No knowledge of a future private completion envelope is required to compile.
var ordinaryCompletionKinds = []editor.IntentKind{
	editor.Read, editor.Observe, editor.WriteSnapshot, editor.PublishCandidate,
	editor.ReadSelection, editor.ReadMergePrimary, editor.ReadMergeSecondary,
	editor.ObserveWorkspace, editor.PublishEveryday, editor.AppendWorkspace,
}

// A dropped/empty matrix must fail rather than silently skip the boundary.
func completionKinds(t *testing.T) []editor.IntentKind {
	t.Helper()
	if len(ordinaryCompletionKinds) != 10 {
		t.Fatal("ordinary completion matrix lost its ten-kind floor")
	}
	seen := make(map[editor.IntentKind]bool)
	for _, kind := range ordinaryCompletionKinds {
		if kind == "" || seen[kind] {
			t.Fatal("empty/duplicate ordinary completion matrix row", kind)
		}
		seen[kind] = true
	}
	return ordinaryCompletionKinds
}

func completionWorkspace(kind editor.IntentKind) bool {
	switch kind {
	case editor.Read, editor.Observe, editor.WriteSnapshot, editor.PublishCandidate:
		return false
	}
	return true
}
func completionFiles(t *testing.T, root string) {
	t.Helper()
	d, err := document.New(document.NewConfig{Profile: document.HistoricalUS51DosTextStandardPrinter})
	if err != nil {
		t.Fatal(err)
	}
	prefix, err := d.Export()
	if err != nil {
		t.Fatal(err)
	}
	for name, body := range map[string]string{"ORIGIN": "ABCDE", "INPUT": "SOURCE"} {
		raw := append(bytes.Clone(prefix), []byte(body)...)
		if err := os.WriteFile(filepath.Join(root, name), raw, 0600); err != nil {
			t.Fatal(err)
		}
	}
	for _, name := range []string{"PRIMARY.WP5", "SECOND.WP5"} {
		raw, err := os.ReadFile(filepath.Join("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-134", name))
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(filepath.Join(root, name), raw, 0600); err != nil {
			t.Fatal(err)
		}
	}
}
func completionRuntime(t *testing.T, root string, kind editor.IntentKind) (*Runtime, Model) {
	t.Helper()
	r, m, err := Open(Config{Root: root, Profile: LocalFlat, EditorChrome: completionWorkspace(kind)})
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
func completionNamedRead(t *testing.T, m Model, name string) (Model, tea.Cmd) {
	t.Helper()
	m = key(t, m, tea.KeyF10, tea.ModShift, "")
	m = key(t, m, 'x', 0, name)
	return press(m, tea.KeyEnter, 0, "")
}
func completionQueue(t *testing.T, m Model, kind editor.IntentKind, output string) (Model, tea.Cmd) {
	t.Helper()
	var cmd tea.Cmd
	if kind == editor.Read || kind == editor.ReadSelection {
		m, cmd = completionNamedRead(t, m, "INPUT")
	} else {
		m, cmd = completionNamedRead(t, m, "ORIGIN")
		m = drain(m, cmd)
		if m.Session().Source() == nil {
			t.Fatal("real initial read did not bind a source", m.State())
		}
		switch kind {
		case editor.ReadMergePrimary, editor.ReadMergeSecondary:
			m = key(t, m, tea.KeyF9, tea.ModCtrl, "")
			m = key(t, m, '1', 0, "1")
			m = key(t, m, 'P', 0, "PRIMARY.WP5")
			m, cmd = press(m, tea.KeyEnter, 0, "")
			if kind == editor.ReadMergeSecondary {
				m = drain(m, cmd)
				if m.Session().Snapshot().Mode != editor.MergeSecondaryName {
					t.Fatal("primary read did not reach secondary filename", m.State())
				}
				m = key(t, m, 'S', 0, "SECOND.WP5")
				m, cmd = press(m, tea.KeyEnter, 0, "")
			}
		case editor.AppendWorkspace:
			m = key(t, m, tea.KeyF4, tea.ModAlt, "")
			m = key(t, m, tea.KeyRight, 0, "")
			m = key(t, m, tea.KeyF4, tea.ModCtrl, "")
			m = key(t, m, '1', 0, "1")
			m = key(t, m, '4', 0, "4")
			m = key(t, m, 'O', 0, output)
			m, cmd = press(m, tea.KeyEnter, 0, "")
		default:
			if kind == editor.PublishCandidate || kind == editor.PublishEveryday {
				m = key(t, m, 'X', 0, "X")
			}
			m = key(t, m, tea.KeyF10, 0, "")
			m = key(t, m, 'O', 0, output)
			m, cmd = press(m, tea.KeyEnter, 0, "")
			if kind == editor.WriteSnapshot || kind == editor.PublishCandidate || kind == editor.PublishEveryday {
				if cmd == nil {
					t.Fatal("missing real Observe command")
				}
				n, next := m.Update(cmd())
				m, cmd = n.(Model), next
			}
		}
	}
	pending := m.Session().Snapshot().Pending
	if cmd == nil || pending == nil || pending.Kind != kind || m.State().PendingIO != 1 {
		t.Fatalf("expected actual queued %s, got %+v", kind, m.State())
	}
	return m, cmd
}

type completionObservation struct {
	snapshot editor.Snapshot
	native   []byte
	source   any
	birth    document.Birth
}

func completionObserve(t *testing.T, m Model) completionObservation {
	t.Helper()
	s := m.Session().Snapshot()
	s.Notice = "" // A host refusal may add a diagnostic only.
	raw, err := m.Session().Document().Export()
	if err != nil {
		t.Fatal(err)
	}
	var source any
	if m.Session().Source() != nil {
		source = m.Session().Source().Identity()
	}
	return completionObservation{s, raw, source, m.Session().Document().Birth()}
}
func completionConserved(t *testing.T, before completionObservation, m Model) {
	t.Helper()
	after := completionObserve(t, m)
	if !reflect.DeepEqual(before, after) {
		var fields []string
		a, b := reflect.ValueOf(before.snapshot), reflect.ValueOf(after.snapshot)
		typ := a.Type()
		for i := 0; i < a.NumField(); i++ {
			if !reflect.DeepEqual(a.Field(i).Interface(), b.Field(i).Interface()) {
				fields = append(fields, typ.Field(i).Name)
			}
		}
		t.Errorf("completion changed current state: fields=%v nativeEqual=%t sourceEqual=%t birthEqual=%t", fields, bytes.Equal(before.native, after.native), reflect.DeepEqual(before.source, after.source), before.birth == after.birth)
	}
}
func completionDeliver(t *testing.T, m Model, msg tea.Msg) (Model, tea.Cmd) {
	t.Helper()
	n, c := m.Update(msg)
	return n.(Model), c
}

func TestOrdinaryCompletionForeignRuntimeCannotConsumeQueuedWork(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range completionKinds(t) {
		for _, sameRoot := range []bool{false, true} {
			t.Run(fmt.Sprintf("%s/same-root=%t", kind, sameRoot), func(t *testing.T) {
				root := t.TempDir()
				completionFiles(t, root)
				otherRoot := root
				if !sameRoot {
					otherRoot = t.TempDir()
					completionFiles(t, otherRoot)
				}
				own, m := completionRuntime(t, root, kind)
				foreign, other := completionRuntime(t, otherRoot, kind)
				m, ownCallback := completionQueue(t, m, kind, "OWNOUT")
				other, foreignCallback := completionQueue(t, other, kind, "OTHEROUT")
				pending, fp := m.Session().Snapshot().Pending, other.Session().Snapshot().Pending
				if pending.Operation != fp.Operation || pending.Revision != fp.Revision || pending.Kind != fp.Kind {
					t.Fatal("test did not obtain colliding numeric request keys")
				}
				ownBefore, foreignBefore := len(own.Completed()), len(foreign.Completed())
				before := completionObserve(t, m)
				foreignMessage := foreignCallback()
				foreignReceipts := foreign.Completed()
				if len(foreignReceipts) != foreignBefore+1 || foreignReceipts[len(foreignReceipts)-1].Err != nil {
					t.Fatal("foreign positive control did not actually succeed", foreignReceipts)
				}
				m, c := completionDeliver(t, m, foreignMessage)
				if sameRoot && (kind == editor.Read || kind == editor.ReadSelection) {
					after := completionObserve(t, m)
					t.Logf("exact foreign witness: kind=%s op=%d rev=%d PendingIO=%d beforeNativeHex=%x afterNativeHex=%x nativeEqual=%t beforeSource=%#v afterSource=%#v sourceEqual=%t beforeBirthNew=%t beforeBirthLoaded=%t afterBirthNew=%t afterBirthLoaded=%t birthEqual=%t beforePending=%t afterPending=%t ownCompleted=%d foreignCompleted=%d", kind, pending.Operation, pending.Revision, m.State().PendingIO, before.native, after.native, bytes.Equal(before.native, after.native), before.source, after.source, reflect.DeepEqual(before.source, after.source), before.birth.IsNew(), before.birth.IsLoaded(), after.birth.IsNew(), after.birth.IsLoaded(), before.birth == after.birth, before.snapshot.Pending != nil, after.snapshot.Pending != nil, len(own.Completed()), len(foreign.Completed()))
				}
				if c != nil {
					t.Error("foreign callback issued another current command")
				}
				if m.State().PendingIO != 1 {
					t.Errorf("foreign actual Runtime completion consumed own unexecuted %s: PendingIO=%d ownCompleted=%d foreignCompleted=%d", kind, m.State().PendingIO, len(own.Completed()), len(foreign.Completed()))
				}
				completionConserved(t, before, m)
				if len(own.Completed()) != ownBefore || len(foreign.Completed()) != foreignBefore+1 {
					t.Error("independent Runtime execution accounting crossed owners")
				}
				if m.State().Reconciliation != "" {
					t.Error("foreign publication/error injected current reconciliation")
				}
				t.Logf("held own callback: %s op=%d rev=%d sameRoot=%t own=%d foreign=%d", kind, pending.Operation, pending.Revision, sameRoot, len(own.Completed()), len(foreign.Completed()))
				m, c = completionDeliver(t, m, ownCallback())
				m = drain(m, c)
				if m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil {
					t.Errorf("actual own callback could not settle after foreign delivery: %+v", m.State())
				}
				if len(own.Completed()) < ownBefore+1 {
					t.Error("actual own callback was never executed")
				}
			})
		}
	}
}

func TestOrdinaryCompletionOwnOneShotAndStaleModelDelivery(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range completionKinds(t) {
		t.Run(string(kind), func(t *testing.T) {
			root := t.TempDir()
			completionFiles(t, root)
			r, m := completionRuntime(t, root, kind)
			m, callback := completionQueue(t, m, kind, "OWNOUT")
			beforeCount := len(r.Completed())
			before := completionObserve(t, m)
			stale := m
			m, _ = completionDeliver(t, m, tea.WindowSizeMsg{Width: 81, Height: 25})
			actual := callback()
			_, c := completionDeliver(t, stale, actual)
			if c != nil || len(r.Completed()) != beforeCount+1 {
				t.Fatal("stale Model changed actual callback execution")
			}
			completionConserved(t, before, m)
			// A second invocation owns no completion and must not consume the first.
			m, c = completionDeliver(t, m, callback())
			if c != nil || m.State().PendingIO != 1 || len(r.Completed()) != beforeCount+1 {
				t.Error("duplicate invocation settled undelivered authentic completion or executed twice")
			}
			completionConserved(t, before, m)
			m, c = completionDeliver(t, m, actual)
			// Before executing any follow-up, a redelivery cannot consume its receipt.
			settled := completionObserve(t, m)
			pendingCount := m.State().PendingIO
			m, next := completionDeliver(t, m, actual)
			if next != nil || m.State().PendingIO != pendingCount {
				t.Error("redelivery consumed a later queued request")
			}
			completionConserved(t, settled, m)
			m = drain(m, c)
			if m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil {
				t.Error("authentic completion/follow-up did not settle")
			}
			done := completionObserve(t, m)
			doneCount := len(r.Completed())
			m, c = completionDeliver(t, m, actual)
			if c != nil || len(r.Completed()) != doneCount || m.State().PendingIO != 0 || m.State().Reconciliation != "" {
				t.Error("duplicate delivery changed terminal accounting or injected reconciliation")
			}
			completionConserved(t, done, m)
		})
	}
}

func TestOrdinaryCompletionClosedAndCapacityRefusalsOwnTheirQueue(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range completionKinds(t) {
		for _, guard := range []string{"Close", "capacity"} {
			t.Run(string(kind)+"/"+guard, func(t *testing.T) {
				root := t.TempDir()
				completionFiles(t, root)
				r, m := completionRuntime(t, root, kind)
				m, callback := completionQueue(t, m, kind, "OWNOUT")
				before := completionObserve(t, m)
				if guard == "Close" {
					if err := r.Close(); err != nil {
						t.Fatal(err)
					}
				} else {
					// Fill the genuine existing bounded diagnostic route; do not edit issued.
					for i := len(r.Completed()); i < 1024; i++ {
						r.command(editor.Intent{Operation: uint64(10000 + i), Kind: editor.Read, Directory: r.directory, Name: "ORIGIN"})()
					}
					if len(r.Completed()) != 1024 {
						t.Fatal("capacity control did not fill 1024 actual receipts")
					}
					for _, actual := range r.Completed() {
						if actual.Err != nil {
							t.Fatal("capacity positive control retained a failed IO", actual)
						}
					}
				}
				count := len(r.Completed())
				m, c := completionDeliver(t, m, callback())
				if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().Last.Result.Err == nil {
					t.Error("genuine guard refusal did not settle its own pending request", m.State())
				}
				if len(r.Completed()) != count {
					t.Error("guard refusal performed IO or grew Completed")
				}
				after := completionObserve(t, m)
				if !bytes.Equal(before.native, after.native) || !reflect.DeepEqual(before.source, after.source) || before.birth != after.birth {
					t.Error("guard refusal changed native/source/birth")
				}
				if _, err := os.Stat(filepath.Join(root, "OWNOUT")); !os.IsNotExist(err) {
					t.Error("closed/capacity guard wrote an output", err)
				}
			})
		}
	}
}

func TestOrdinaryCompletionCancelledLateCallbackRemainsTruthful(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range completionKinds(t) {
		for _, executeFirst := range []bool{false, true} {
			t.Run(fmt.Sprintf("%s/executed-before-cancel=%t", kind, executeFirst), func(t *testing.T) {
				root := t.TempDir()
				completionFiles(t, root)
				r, m := completionRuntime(t, root, kind)
				m, callback := completionQueue(t, m, kind, "OWNOUT")
				before := completionObserve(t, m)
				count := len(r.Completed())
				var actual tea.Msg
				if executeFirst {
					actual = callback()
				}
				m, _ = completionDeliver(t, m, CancelPendingMsg{})
				if m.Session().Snapshot().Pending != nil || m.State().PendingIO != 1 {
					t.Fatal("UI cancel pretended outstanding IO was settled")
				}
				if !executeFirst {
					actual = callback()
				}
				receipts := r.Completed()
				if len(receipts) != count+1 {
					t.Fatal("callback did not execute exactly once")
				}
				published := receipts[len(receipts)-1].Err == nil && receipts[len(receipts)-1].Outcome.State == storage.Published
				m, c := completionDeliver(t, m, actual)
				if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil {
					t.Error("own late completion failed to settle only detached IO")
				}
				after := completionObserve(t, m)
				if !bytes.Equal(before.native, after.native) || !reflect.DeepEqual(before.source, after.source) || before.birth != after.birth {
					t.Error("cancelled callback adopted source or changed current native")
				}
				if published {
					if m.State().Reconciliation == "" {
						t.Error("actual own late publication lost reconciliation")
					}
					if _, err := os.Stat(filepath.Join(root, "OWNOUT")); err != nil {
						t.Error("UI cancel hid an actual disk publication", err)
					}
				}
				settled := completionObserve(t, m)
				warning := m.State().Reconciliation
				m, c = completionDeliver(t, m, actual)
				if c != nil || m.State().PendingIO != 0 || m.State().Reconciliation != warning {
					t.Error("late duplicate changed accounting/reconciliation")
				}
				completionConserved(t, settled, m)
			})
		}
	}
}

func TestOrdinaryCompletionRealReadFailureAndRetry(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range []editor.IntentKind{editor.Read, editor.ReadSelection} {
		t.Run(string(kind), func(t *testing.T) {
			root := t.TempDir()
			completionFiles(t, root)
			r, m := completionRuntime(t, root, kind)
			m, callback := completionQueue(t, m, kind, "OWNOUT")
			if err := os.Remove(filepath.Join(root, "INPUT")); err != nil {
				t.Fatal(err)
			}
			msg := callback()
			m, c := completionDeliver(t, m, msg)
			if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().Last.Result.Err == nil || len(r.Completed()) != 1 {
				t.Fatal("actual missing-file refusal not settled", m.State())
			}
			// Re-enter through normal keys after exact fixture restoration, never revive a request.
			completionFiles(t, root)
			m = key(t, m, tea.KeyF1, 0, "")
			m, next := completionNamedRead(t, m, "INPUT")
			if next == nil || m.State().PendingIO != 1 {
				t.Fatal("real retry did not queue new request", m.State())
			}
			before := completionObserve(t, m)
			m, c = completionDeliver(t, m, msg)
			if c != nil || m.State().PendingIO != 1 {
				t.Error("old real error consumed retry")
			}
			completionConserved(t, before, m)
			m = drain(m, next)
			if m.State().PendingIO != 0 || m.Session().Source() == nil || len(r.Completed()) != 2 {
				t.Error("new actual retry did not settle")
			}
		})
	}
}

func TestOrdinaryCompletionRealStaleSourceRefusal(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range []editor.IntentKind{editor.WriteSnapshot, editor.PublishCandidate, editor.PublishEveryday} {
		t.Run(string(kind), func(t *testing.T) {
			root := t.TempDir()
			completionFiles(t, root)
			r, m := completionRuntime(t, root, kind)
			m, callback := completionQueue(t, m, kind, "OWNOUT")
			before := completionObserve(t, m)
			count := len(r.Completed())
			if err := os.WriteFile(filepath.Join(root, "ORIGIN"), []byte("outside replacement"), 0600); err != nil {
				t.Fatal(err)
			}
			m, c := completionDeliver(t, m, callback())
			if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().Last.Result.Err == nil || len(r.Completed()) != count+1 {
				t.Error("actual stale source did not refuse/settle", m.State())
			}
			after := completionObserve(t, m)
			if !bytes.Equal(before.native, after.native) || !reflect.DeepEqual(before.source, after.source) {
				t.Error("real source error changed loaded bytes/binding")
			}
			if _, err := os.Stat(filepath.Join(root, "OWNOUT")); !os.IsNotExist(err) {
				t.Error("stale source published an output", err)
			}
		})
	}
}

func TestOrdinaryCompletionBareEnvelopeCannotConsumeQueuedWork(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range completionKinds(t) {
		for _, forgery := range []string{"matching-keys", "uncertain-error", "published-outcome"} {
			t.Run(string(kind)+"/"+forgery, func(t *testing.T) {
				root := t.TempDir()
				completionFiles(t, root)
				r, m := completionRuntime(t, root, kind)
				m, callback := completionQueue(t, m, kind, "OWNOUT")
				p := m.Session().Snapshot().Pending
				before := completionObserve(t, m)
				count := len(r.Completed())
				raw := editor.Result{Operation: p.Operation, Revision: p.Revision, Kind: p.Kind}
				if forgery == "uncertain-error" {
					raw.Err = &storage.Failure{Kind: storage.PublicationUncertain, Stage: "bare forged negative", Name: "OWNOUT", Candidate: ".wordling-forged", DestinationMayExist: true}
				}
				if forgery == "published-outcome" {
					raw.Outcome = storage.Outcome{State: storage.Published}
				}
				m, c := completionDeliver(t, m, resultMsg{raw})
				if c != nil || m.State().PendingIO != 1 || m.Session().Snapshot().Pending == nil || m.State().Reconciliation != "" || len(r.Completed()) != count {
					t.Error("bare matching metadata acquired queued ownership or warning authority", m.State())
				}
				completionConserved(t, before, m)
				m, c = completionDeliver(t, m, callback())
				m = drain(m, c)
				if m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil {
					t.Error("bare negative destroyed authentic callback")
				}
			})
		}
	}
}

func TestOrdinaryCompletionOldSuccessCannotStealExecutedRetry(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range []editor.IntentKind{editor.Read, editor.ReadSelection} {
		t.Run(string(kind), func(t *testing.T) {
			root := t.TempDir()
			completionFiles(t, root)
			r, m := completionRuntime(t, root, kind)
			m, oldCallback := completionQueue(t, m, kind, "OWNOUT")
			firstKey := m.Session().Snapshot().Pending.Operation
			m, _ = completionDeliver(t, m, CancelPendingMsg{})
			oldMessage := oldCallback()
			m, c := completionDeliver(t, m, oldMessage)
			if c != nil || m.State().PendingIO != 0 {
				t.Fatal("actual detached first read not settled")
			}
			// The cancelled read did not occupy the document; retry is a new request.
			m = key(t, m, tea.KeyF1, 0, "")
			m, retry := completionNamedRead(t, m, "INPUT")
			p := m.Session().Snapshot().Pending
			if retry == nil || p == nil || p.Operation == firstKey {
				t.Fatal("retry reused first request")
			}
			retryMessage := retry() // Execute the newer IO before redelivering old success.
			before := completionObserve(t, m)
			m, c = completionDeliver(t, m, oldMessage)
			if c != nil || m.State().PendingIO != 1 || len(r.Completed()) != 2 {
				t.Error("old success consumed executed-but-undelivered retry")
			}
			completionConserved(t, before, m)
			m, c = completionDeliver(t, m, retryMessage)
			m = drain(m, c)
			if m.State().PendingIO != 0 || m.Session().Source() == nil || m.Session().Snapshot().Last.Result.Err != nil {
				t.Error("actual newer callback no longer deliverable")
			}
		})
	}
}

func TestOrdinaryCompletionOwnSuccessWithoutInterference(t *testing.T) {
	t.Setenv("XDG_CONFIG_HOME", t.TempDir())
	for _, kind := range completionKinds(t) {
		t.Run(string(kind), func(t *testing.T) {
			root := t.TempDir()
			completionFiles(t, root)
			r, m := completionRuntime(t, root, kind)
			m, callback := completionQueue(t, m, kind, "OWNOUT")
			count := len(r.Completed())
			m, c := completionDeliver(t, m, callback())
			m = drain(m, c)
			receipts := r.Completed()
			if len(receipts) < count+1 || receipts[count].Kind != kind || receipts[count].Err != nil {
				t.Fatal("real ordinary positive callback failed", receipts)
			}
			if m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().Last.Result.Err != nil || m.State().Reconciliation != "" {
				t.Fatal("real own completion did not settle cleanly", m.State())
			}
		})
	}
}
