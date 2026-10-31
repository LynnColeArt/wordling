package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func pendingSave(t *testing.T) (*Runtime, Model, tea.Cmd, []byte, string) {
	t.Helper()
	r, m, b, root := testModel(t)
	m = retrieve(m)
	m, _ = press(m, tea.KeyF10, 0, "")
	m, _ = press(m, 'C', 0, "COPY")
	m, c := press(m, tea.KeyEnter, 0, "")
	n, save := m.Update(c())
	m = n.(Model)
	if save == nil {
		t.Fatal("no Save cmd")
	}
	return r, m, save, b, root
}
func holdAuthentic(t *testing.T, m Model, notice tea.Msg) Model {
	t.Helper()
	before := m.Session().Snapshot()
	n, c := m.Update(notice)
	m = n.(Model)
	if c != nil || m.State().PendingIO != 1 || m.Session().Snapshot().Pending == nil || m.Session().Snapshot().Mode != before.Mode || m.Session().Snapshot().SaveState != before.SaveState {
		t.Fatal("dispatch notice settled authentic operation", m.State())
	}
	m, _ = press(m, tea.KeyF1, 0, "")
	m, _ = press(m, tea.KeyF7, 0, "")
	m, _ = press(m, 'n', 0, "n")
	m, c = press(m, 'y', 0, "y")
	if c != nil || m.Session().Snapshot().Mode == editor.Exited {
		t.Fatal("dispatch notice permitted early exit")
	}
	return m
}
func TestDuplicateSaveBeforeAuthenticAtEveryGuard(t *testing.T) {
	for _, guard := range []string{"duplicate", "capacity", "closed"} {
		t.Run(guard, func(t *testing.T) {
			r, m, save, b, root := pendingSave(t)
			authentic := save()
			disk, e := os.ReadFile(filepath.Join(root, "COPY"))
			if e != nil || string(disk) != string(b) {
				t.Fatal("actual publication missing", e)
			}
			if guard == "capacity" {
				r.mu.Lock()
				r.issued = 1024
				r.mu.Unlock()
			}
			if guard == "closed" {
				if e = r.Close(); e != nil {
					t.Fatal(e)
				}
			}
			m = holdAuthentic(t, m, save())
			m = holdAuthentic(t, m, save())
			n, c := m.Update(authentic)
			m = n.(Model)
			if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().SaveState != editor.NewNamePublished {
				t.Fatal("authentic completion lost", m.State())
			}
			n, c = m.Update(save())
			m = n.(Model)
			if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().SaveState != editor.NewNamePublished || m.State().Reconciliation != "" {
				t.Fatal("post-completion duplicate changed outcome", m.State())
			}
			receipts := r.Completed()
			if len(receipts) != 3 || receipts[2].Outcome.State != "Published" {
				t.Fatal("shutdown lost actual publication", receipts)
			}
		})
	}
}
func TestConcurrentAdmittedDuplicateWhileReceiptUndelivered(t *testing.T) {
	r, m, save, _, _ := pendingSave(t)
	ready := make(chan tea.Msg, 1)
	go func() { ready <- save() }()
	pending := m.Session().Snapshot().Pending
	key := operation{pending.Operation, pending.Revision, pending.Kind}
	deadline := time.Now().Add(2 * time.Second)
	for {
		r.mu.Lock()
		admitted := r.executed[key]
		r.mu.Unlock()
		if admitted {
			break
		}
		if time.Now().After(deadline) {
			t.Fatal("worker not admitted")
		}
		time.Sleep(time.Millisecond)
	}
	// The worker is admitted, but its authentic result has never reached Update.
	// It may finish before this duplicate reaches Runtime; either ordering is safe.
	m = holdAuthentic(t, m, save())
	authentic := <-ready
	n, _ := m.Update(authentic)
	m = n.(Model)
	if m.Session().Snapshot().SaveState != editor.NewNamePublished || m.State().PendingIO != 0 {
		t.Fatal(m.State())
	}
}
func TestCancelledDuplicateStillNeedsAuthenticReconciliation(t *testing.T) {
	_, m, save, _, _ := pendingSave(t)
	authentic := save()
	n, _ := m.Update(CancelPendingMsg{})
	m = n.(Model)
	n, _ = m.Update(save())
	m = n.(Model)
	if m.State().PendingIO != 1 {
		t.Fatal("duplicate settled detached operation")
	}
	n, _ = m.Update(authentic)
	m = n.(Model)
	if m.State().PendingIO != 0 || m.State().Reconciliation == "" || m.Session().Snapshot().SaveState == editor.NewNamePublished {
		t.Fatal("actual detached publication lost", m.State())
	}
}
func TestFreshClosedAndCapacityRefusalsSettleWithoutIO(t *testing.T) {
	for _, guard := range []string{"closed", "capacity"} {
		t.Run(guard, func(t *testing.T) {
			r, m, _, _ := testModel(t)
			m, _ = press(m, tea.KeyF10, tea.ModShift, "")
			m, _ = press(m, 'O', 0, "ORIGIN")
			m, c := press(m, tea.KeyEnter, 0, "")
			if guard == "closed" {
				if e := r.Close(); e != nil {
					t.Fatal(e)
				}
			} else {
				r.mu.Lock()
				r.issued = 1024
				r.mu.Unlock()
			}
			n, next := m.Update(c())
			m = n.(Model)
			if next != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().Notice == "" || m.Session().Source() != nil {
				t.Fatal("definitive fresh dispatch failure did not settle", m.State())
			}
			if len(r.Completed()) != 0 {
				t.Fatal("nonadmitted operation performed IO")
			}
		})
	}
}

func TestDuplicateCannotReplaceLegitimateStorageFailure(t *testing.T) {
	_, m, save, b, root := pendingSave(t)
	changed := append([]byte(nil), b...)
	changed[len(changed)-1] = 'Z'
	if e := os.WriteFile(filepath.Join(root, "ORIGIN"), changed, 0600); e != nil {
		t.Fatal(e)
	}
	authentic := save()
	m = holdAuthentic(t, m, save())
	n, c := m.Update(authentic)
	m = n.(Model)
	if c != nil || m.State().PendingIO != 0 || m.Session().Snapshot().Pending != nil || m.Session().Snapshot().SaveState != editor.SaveFailed || m.Session().Snapshot().Notice == "" {
		t.Fatal("genuine storage failure did not settle", m.State())
	}
	if _, e := os.Stat(filepath.Join(root, "COPY")); !os.IsNotExist(e) {
		t.Fatal("failed save published")
	}
	native, e := m.Session().Document().Export()
	if e != nil || string(native) != string(b) {
		t.Fatal("loaded snapshot changed", e)
	}
}
