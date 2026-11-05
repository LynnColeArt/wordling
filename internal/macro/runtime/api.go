// Package runtime compiles and evaluates a bounded, source-backed WPM subset.
// It owns no document, filesystem or terminal; effects and program resolution
// belong to injected clients. Its diagnostics are not original WP messages.
package runtime

import (
	"context"
	"fmt"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

type Limits struct {
	Steps, OutputWords                                                          uint64
	CallDepth, LoopDepth, Variables, VariableWords, ExpressionDepth, SliceSteps uint32
}
type Policy struct {
	Keys                  []uint16
	ASCII, DisplayControl bool
}
type Effect struct {
	Kind   string
	Words  []wpm.Word
	Source [32]byte
	At     wpm.Span
}
type Condition string

const (
	NoCondition   Condition = "none"
	NotFound      Condition = "not-found"
	CommandError  Condition = "command-error"
	UserCancelled Condition = "user-cancelled"
)

type EffectResult struct {
	Condition      Condition
	MayHaveEffects bool
}
type CommandSink interface {
	Capabilities() Policy
	Apply(context.Context, Effect) (EffectResult, error)
}
type ProgramRequest struct {
	ID     uint64
	Parent [32]byte
	Name   []wpm.Word
	At     wpm.Span
}
type Resolution struct {
	State     string
	Image     *wpm.Image
	Condition Condition
	Err       error
}
type Resolver interface {
	Resolve(context.Context, ProgramRequest) Resolution
}
type Failure struct {
	Code   string
	Source [32]byte
	At     wpm.Span
	Detail string
}

func (e *Failure) Error() string {
	return fmt.Sprintf("macro: %s at %d (%s)", e.Code, e.At.Offset, e.Detail)
}

type Result struct {
	State               string
	Steps, EmittedWords uint64
	NeedProgram         *ProgramRequest
	Err                 error
}

func DefaultLimits() Limits {
	return Limits{Steps: 1000000, OutputWords: 1048576, CallDepth: 16, LoopDepth: 32, Variables: 256, VariableWords: 4096, ExpressionDepth: 16, SliceSteps: 256}
}
func validLimits(l Limits) bool {
	c := DefaultLimits()
	return l.Steps > 0 && l.Steps <= c.Steps && l.OutputWords > 0 && l.OutputWords <= c.OutputWords && l.CallDepth > 0 && l.CallDepth <= c.CallDepth && l.LoopDepth > 0 && l.LoopDepth <= c.LoopDepth && l.Variables > 0 && l.Variables <= c.Variables && l.VariableWords > 0 && l.VariableWords <= c.VariableWords && l.ExpressionDepth > 0 && l.ExpressionDepth <= c.ExpressionDepth && l.SliceSteps > 0 && l.SliceSteps <= c.SliceSteps
}
func noCondition(c Condition) bool { return c == "" || c == NoCondition }
func noBroader(l, c Limits) bool {
	return l.Steps <= c.Steps && l.OutputWords <= c.OutputWords && l.CallDepth <= c.CallDepth && l.LoopDepth <= c.LoopDepth && l.Variables <= c.Variables && l.VariableWords <= c.VariableWords && l.ExpressionDepth <= c.ExpressionDepth && l.SliceSteps <= c.SliceSteps
}
func copiedPolicy(p Policy) Policy { p.Keys = append([]uint16(nil), p.Keys...); return p }
func hasKey(p Policy, k uint16) bool {
	for _, v := range p.Keys {
		if v == k {
			return true
		}
	}
	return false
}
func covers(have, need Policy) bool {
	if need.ASCII && !have.ASCII || need.DisplayControl && !have.DisplayControl {
		return false
	}
	for _, k := range need.Keys {
		if !hasKey(have, k) {
			return false
		}
	}
	return true
}
func intersect(a, b Policy) Policy {
	p := Policy{ASCII: a.ASCII && b.ASCII, DisplayControl: a.DisplayControl && b.DisplayControl}
	for _, k := range a.Keys {
		if hasKey(b, k) && !hasKey(p, k) {
			p.Keys = append(p.Keys, k)
		}
	}
	return p
}
func wordsCopy(w []wpm.Word) []wpm.Word { return append([]wpm.Word(nil), w...) }
func requestCopy(r *ProgramRequest) *ProgramRequest {
	if r == nil {
		return nil
	}
	x := *r
	x.Name = wordsCopy(x.Name)
	return &x
}
func failed(code string, source [32]byte, at wpm.Span, detail string) error {
	return &Failure{code, source, at, detail}
}
