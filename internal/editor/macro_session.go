package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	vm "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/storage"
	"strings"
)

type transitionIdentity struct{ marker byte }

func (s Session) advanced() Session { s.transition = &transitionIdentity{1}; return s }

type bufferIdentity struct{ value byte }
type macroIdentity struct{ run uint64 }
type macroAcquisition struct {
	request Intent
	source  *storage.Macro
}

func copyMacro(p *storage.Macro) *storage.Macro {
	if p == nil {
		return nil
	}
	v := *p
	return &v
}
func (s Session) MacroSource() *storage.Macro {
	if s.macroReady == nil {
		return nil
	}
	return copyMacro(s.macroReady.source)
}
func (s Session) resolveMacro(name string) (*storage.Directory, string, error) {
	dir, leaf, err := s.resolve(name)
	if err != nil {
		return nil, "", err
	}
	// Literal case and explicit profile prefixes remain significant. Only the
	// observed WPM default extension is supplied; no arbitrary host path lookup.
	if !strings.Contains(leaf, ".") {
		leaf += ".WPM"
	} else if !strings.HasSuffix(leaf, ".WPM") {
		return nil, "", refuse("macro name requires exact .WPM extension")
	}
	if len(leaf) > storage.MaxNameBytes {
		return nil, "", refuse("macro basename exceeds rooted name bound")
	}
	return dir, leaf, nil
}

// WithMacroRepeat admits the exact original Esc3/Macro context. It does not
// implement general Escape Repeat, OS repeats or expand the VM's total budget.
func (s Session) WithMacroRepeat(count uint32) (Session, error) {
	if !s.initialized || s.mode != Editing || s.native == nil || s.native.Birth().IsNew() || s.macroOwner != nil || s.selection || s.homes != 0 || (count != 1 && count != 3) {
		return s, refuse("only loaded Editing Macro repeat1/3 is qualified")
	}
	s.macroRepeat = count
	s = s.advanced()
	return s, nil
}
func (s Session) switchDocument() (Session, *Intent, error) {
	if (s.native != nil && s.native.Birth().IsNew()) || s.mode != Editing || s.pending != nil || s.selection || s.homes != 0 || s.macroOwner != nil || s.macroRepeat != 1 || s.over || s.cursor.Reveal() {
		return s, nil, refuse("document switch outside qualified editing context")
	}
	current := s
	current.other = nil
	current.historyValid = false
	var next Session
	if s.other == nil {
		next = Session{initialized: true, locations: s.locations, mode: Editing, lastSave: NotSaved, bufferID: &bufferIdentity{2}, screen: 2, historyUsed: true, macroRepeat: 1}
	} else {
		next = *s.other
	}
	next.other = &current
	next.sequence = s.sequence
	next.transition = s.transition
	next.historyValid = false
	// Preserved fragments remain available for inspection, never a guessed fresh
	// global/cross-document Undelete stack.
	return next, nil, nil
}
func (s Session) ScreenSnapshot(number uint8) (Snapshot, error) {
	if number == s.screen {
		return s.Snapshot(), nil
	}
	if s.other != nil && number == s.other.screen {
		return s.other.Snapshot(), nil
	}
	return Snapshot{}, refuse("screen has not been acquired")
}
func (s Session) SourceOnScreen(number uint8) (*storage.Document, error) {
	if number == s.screen {
		return s.Source(), nil
	}
	if s.other != nil && number == s.other.screen {
		return s.other.Source(), nil
	}
	return nil, refuse("screen has not been acquired")
}

// StartMacro consumes one accepted rooted source and returns a single-owner
// mutable execution driver, separate from persistent Session observations.
func (s Session) StartMacro(limits vm.Limits) (Session, *MacroExecution, error) {
	if s.mode != MacroReady || s.macroReady == nil || s.macroOwner != nil {
		return s, nil, refuse("no accepted macro acquisition")
	}
	original := s
	acquired := s.macroReady
	policy := vm.Policy{ASCII: true, DisplayControl: true} // Search is not an editor command.
	program, err := vm.Compile(acquired.source.Image(), policy, limits)
	if err != nil {
		return s, nil, err
	}
	token := &macroIdentity{acquired.request.MacroRun}
	s.macroOwner = token
	s.mode = MacroRunning
	s = s.advanced()
	run := &macroExecutionState{token: token, buffer: s.bufferID, expected: s.transition, source: copyMacro(acquired.source), program: program, limits: limits, repeat: acquired.request.Repeat, screen: s.screen, state: "ready"}
	run.machine, err = vm.New(program, run, run, limits)
	if err != nil {
		return original, nil, err
	}
	run.last = run.machine.State()
	return s, &MacroExecution{run}, nil
}

func (s Session) NativeOnScreen(number uint8) (*document.Document, error) {
	if number == s.screen {
		return s.Document(), nil
	}
	if s.other != nil && number == s.other.screen {
		return s.other.Document(), nil
	}
	return nil, refuse("screen has not been acquired")
}
