// Package tui composes the approved read-only session with Bubble Tea and rooted IO.
package tui

import (
	"errors"
	"fmt"
	"path/filepath"
	"sync"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
)

const LocalFlat = "local-flat"

type Config struct{ Root, Profile string }

// Runtime owns the pinned directory and worker lifetime. Close prevents new IO,
// waits for every started operation and closes only then. A queued Cmd invoked
// after Close returns an explicit refusal without touching closed descriptors.
// Completed returns copied receipts, including results Bubble Tea could not
// deliver during a host signal. A cancelled UI operation never cancels disk IO.
type Runtime struct {
	mu        sync.Mutex
	directory *storage.Directory
	stopping  bool
	workers   sync.WaitGroup
	done      chan struct{}
	closeErr  error
	results   []editor.Result
	issued    int
	executed  map[operation]bool
}

func Open(config Config) (*Runtime, Model, error) {
	if config.Profile != LocalFlat || !filepath.IsAbs(config.Root) {
		return nil, Model{}, errors.New("require absolute -root and explicit -profile local-flat (operator-selected validated local filesystem; flat ASCII basenames only)")
	}
	d, err := storage.OpenDirectory(config.Root)
	if err != nil {
		return nil, Model{}, err
	}
	s, err := editor.New(editor.Config{Locations: []editor.Location{{Directory: d}}})
	if err != nil {
		return nil, Model{}, errors.Join(err, d.Close())
	}
	r := &Runtime{directory: d, done: make(chan struct{}), executed: make(map[operation]bool)}
	return r, Model{runtime: r, session: s, width: 80, height: 25}, nil
}
func copyResult(r editor.Result) editor.Result {
	var failure *storage.Failure
	if errors.As(r.Err, &failure) {
		f := *failure
		r.Err = &f
	}
	return r
}
func (r *Runtime) Completed() []editor.Result {
	r.mu.Lock()
	defer r.mu.Unlock()
	out := make([]editor.Result, len(r.results))
	for i, v := range r.results {
		out[i] = copyResult(v)
	}
	return out
}
func (r *Runtime) Close() error {
	r.mu.Lock()
	if r.stopping {
		done := r.done
		r.mu.Unlock()
		<-done
		r.mu.Lock()
		defer r.mu.Unlock()
		return r.closeErr
	}
	r.stopping = true
	r.mu.Unlock()
	r.workers.Wait()
	err := r.directory.Close()
	r.mu.Lock()
	r.closeErr = err
	close(r.done)
	r.mu.Unlock()
	return err
}

type resultMsg struct{ result editor.Result }

func (r *Runtime) command(request editor.Intent) tea.Cmd {
	// Capture the complete immutable intent value, never a pointer into the model.
	return func() tea.Msg {
		result := editor.Result{Operation: request.Operation, Revision: request.Revision, Kind: request.Kind}
		r.mu.Lock()
		if r.stopping {
			r.mu.Unlock()
			result.Err = errors.New("host IO is closed")
			return resultMsg{result}
		}
		if r.issued >= 1024 {
			r.mu.Unlock()
			result.Err = errors.New("host receipt safety limit reached (1024 operations); restart after checking filesystem outcomes")
			return resultMsg{result}
		}
		key := operation{request.Operation, request.Revision, request.Kind}
		if r.executed[key] {
			r.mu.Unlock()
			result.Err = errors.New("duplicate host IO request refused")
			return resultMsg{result}
		}
		r.executed[key] = true
		r.issued++
		r.workers.Add(1)
		r.mu.Unlock()
		defer r.workers.Done()
		if request.Directory != r.directory {
			result.Err = errors.New("foreign rooted directory intent")
		} else {
			switch request.Kind {
			case editor.Read:
				result.Document, result.Err = request.Directory.Read(request.Name)
			case editor.Observe:
				result.Destination, result.Err = request.Directory.Observe(request.Name)
			case editor.WriteSnapshot:
				result.Outcome, result.Err = request.Directory.Save(request.Document, request.Destination, request.Decision)
			default:
				result.Err = fmt.Errorf("unsupported IO intent %q", request.Kind)
			}
		}
		r.mu.Lock()
		receipt := copyResult(result)
		// Shutdown receipts retain outcomes/errors, not entire native images.
		receipt.Document, receipt.Destination = nil, nil
		r.results = append(r.results, receipt)
		r.mu.Unlock()
		return resultMsg{result}
	}
}

// Reconciliation describes any outcome that must not be presented as clean
// exit/save. It does not remove residue or roll back an ambiguous destination.
func Reconciliation(result editor.Result) string {
	var f *storage.Failure
	if errors.As(result.Err, &f) && (f.DestinationMayExist || f.Candidate != "") {
		return fmt.Sprintf("Filesystem reconciliation required: %v; candidate=%q; destination may exist=%t", result.Err, f.Candidate, f.DestinationMayExist)
	}
	return ""
}
