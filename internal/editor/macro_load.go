package editor

import (
	"errors"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/storage"
	"io/fs"
)

// The request and observation identities are private. Public request/result
// wrappers remain independent inspection values, never mutable IO authority.
type macroReadProof struct {
	operation, revision, run, request uint64
	parent                            [32]byte
	screen                            uint8
	name                              string
	directory                         storage.Directory
	buffer                            *bufferIdentity
	target                            *newMacroTarget
	issued                            *transitionIdentity
	native                            document.Revision
}
type macroReadObservation struct {
	proof   *macroReadProof
	source  *storage.Macro
	err     error
	missing bool
}

func newMacroReadProof(i Intent, buffer *bufferIdentity) *macroReadProof {
	return &macroReadProof{operation: i.Operation, revision: i.Revision, run: i.MacroRun, request: i.MacroRequest, parent: i.MacroParent, screen: i.Screen, name: i.Name, directory: *i.Directory, buffer: buffer}
}
func (p *macroReadProof) matches(i *Intent) bool {
	return p != nil && i != nil && (p.target == nil || (i.NativeRevision == p.native && i.Repeat == 1 && i.MacroRequest == 0 && i.MacroParent == ([32]byte{}) && i.Document == nil && i.Destination == nil && len(i.Candidate) == 0 && i.Decision == storage.NoOverwrite)) && i.macroProof == p && i.Kind == ReadMacro && i.Operation == p.operation && i.Revision == p.revision && i.MacroRun == p.run && i.MacroRequest == p.request && i.MacroParent == p.parent && i.Screen == p.screen && i.Name == p.name && i.Directory != nil && i.Directory.ID() == p.directory.ID()
}

// ExecuteMacroRead is the host-side IO adapter. Invoke it outside Reduce/Step,
// then Complete (root) or MacroExecution.Resume (child). It delegates to the
// actual rooted storage34 acquisition; there is no second filesystem engine.
// Its accepted private directory copy controls IO even if a public wrapper was
// rebound to an independently opened equal root. It never uses arbitrary paths.
func ExecuteMacroRead(i *Intent) Result {
	if i == nil {
		return Result{Kind: ReadMacro, Err: refuse("nil macro read")}
	}
	r := Result{Kind: ReadMacro, Operation: i.Operation, Revision: i.Revision, macroProof: i.macroProof}
	p := i.macroProof
	if !p.matches(i) {
		r.Err = refuse("macro read wrapper differs from accepted request")
		return r
	}
	source, err := p.directory.ReadMacro(p.name)
	r.Macro = copyMacro(source)
	r.Err = copyResult(Result{Err: err}).Err
	r.macroObservation = &macroReadObservation{p, copyMacro(source), copyResult(Result{Err: err}).Err, errors.Is(err, fs.ErrNotExist)}
	return r
}
func acceptedMacroResult(i *Intent, r Result, buffer *bufferIdentity) (Result, error) {
	p := i.macroProof
	o := r.macroObservation
	if r.Document != nil || r.Destination != nil || r.Outcome != (storage.Outcome{}) {
		return r, refuse("macro result contains unrelated payload")
	}
	if p == nil || p.buffer != buffer || !p.matches(i) || r.macroProof != p || o == nil || o.proof != p {
		return r, refuse("macro result lacks matching accepted acquisition")
	}
	if o.err != nil {
		if r.Err == nil {
			return r, refuse("macro failure result was changed")
		}
	} else {
		if r.Err != nil || r.Macro == nil || o.source == nil || r.Macro.Name() != o.source.Name() || r.Macro.DirectoryID() != o.source.DirectoryID() || r.Macro.Identity() != o.source.Identity() || r.Macro.Image() == nil || r.Macro.Image().SHA256() != o.source.Identity().SHA256 {
			return r, refuse("macro result observation was changed")
		}
	}
	r.macroMissing = o.missing
	r.Macro = copyMacro(o.source)
	r.Err = copyResult(Result{Err: o.err}).Err
	return r, nil
}
