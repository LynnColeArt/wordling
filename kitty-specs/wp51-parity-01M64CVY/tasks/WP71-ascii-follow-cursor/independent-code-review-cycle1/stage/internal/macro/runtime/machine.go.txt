package runtime

import (
	"context"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

type loopState struct {
	start, end          int
	kind                uint16
	name                string
	slot                uint32
	current, stop, step int64
	item                *eachItem
}
type frame struct {
	program             *Program
	pc                  int
	variables           []value
	loops               []loopState
	onError, onNotFound int
	handling            bool
	emission            []wpm.Word
	emitValues          []uint16
	each                *eachPreparation
	preparation         *instructionPreparation
	values              [3]value
	evaluated           bool
	emitIndex           int
	emitAt              wpm.Span
	emitKind            string
}

// Machine has one serialized owner. Independent Machines may run concurrently;
// clients serialize access to each Machine and their session/sink. Reentrant
// callback mutation is refused rather than duplicating or invalidating an effect.
type Machine struct {
	limits             Limits
	policy             Policy
	sink               CommandSink
	resolver           Resolver
	frames             []*frame
	state              string
	steps, emitted     uint64
	failure            *Failure
	busy               bool
	debt               uint64
	entry              *frame
	pending            *ProgramRequest
	sequence           uint64
	lastMayHaveEffects bool
}

func newFrame(p *Program) *frame {
	return &frame{program: p, variables: make([]value, p.variables), onError: -1, onNotFound: -1}
}
func New(program *Program, sink CommandSink, resolver Resolver, limits Limits) (*Machine, error) {
	if !validLimits(limits) {
		return nil, failed("InvalidLimit", [32]byte{}, wpm.Span{}, "invalid run limits")
	}
	if program == nil || program.image == nil {
		return nil, failed("InvalidProgram", [32]byte{}, wpm.Span{}, "Compile must create the program")
	}
	// Caller ownership includes the Program wrapper itself. A shallow value copy
	// shares only private immutable backing, not a replaceable caller handle.
	programSnapshot := *program
	program = &programSnapshot
	if !noBroader(limits, program.limits) {
		return nil, failed("BroadenedLimits", program.source, wpm.Span{}, "compile limits cannot be enlarged at run construction")
	}
	if program.needsChild {
		return nil, failed("UnsupportedReturnContext", program.source, wpm.Span{}, "explicit RETURN qualified only in nested child")
	}
	if sink == nil {
		return nil, failed("InvalidSink", program.source, wpm.Span{}, "nil sink")
	}
	capabilities := copiedPolicy(sink.Capabilities())
	if !covers(capabilities, program.required) {
		return nil, failed("UnsupportedSink", program.source, wpm.Span{}, "sink lacks a compiled capability")
	}
	if err := programFits(program, limits); err != nil {
		return nil, err
	}
	return &Machine{limits: limits, policy: intersect(program.policy, capabilities), sink: sink, resolver: resolver, frames: []*frame{newFrame(program)}, state: "ready", debt: program.cost}, nil
}
func programFits(p *Program, l Limits) error {
	if p.cost > l.Steps || p.variables > l.Variables || p.maxLoop > l.LoopDepth || p.maxExpression > l.ExpressionDepth || p.maxValueWords > l.VariableWords {
		return failed("ProgramLimit", p.source, wpm.Span{}, "compiled program exceeds requested run limits")
	}
	return nil
}
func (m *Machine) terminal() bool {
	return m.state == "complete" || m.state == "stopped" || m.state == "refused" || m.state == "failed" || m.state == "limited"
}
func (m *Machine) current() (*frame, wpm.Span) {
	if len(m.frames) == 0 {
		return nil, wpm.Span{}
	}
	f := m.frames[len(m.frames)-1]
	if f.emitting() {
		return f, f.emitAt
	}
	if f.pc < len(f.program.code) {
		return f, f.program.code[f.pc].at
	}
	return f, wpm.Span{}
}
func (m *Machine) stopWith(state, code, detail string, source [32]byte, at wpm.Span) Result {
	m.state = state
	m.failure = &Failure{code, source, at, detail}
	m.pending = nil
	m.entry = nil
	m.debt = 0
	return m.State()
}
func (m *Machine) fail(state, code, detail string) Result {
	f, at := m.current()
	var source [32]byte
	if f != nil {
		source = f.program.source
	}
	return m.stopWith(state, code, detail, source, at)
}
func (m *Machine) State() Result {
	if m == nil {
		return Result{State: "refused", Err: failed("InvalidMachine", [32]byte{}, wpm.Span{}, "nil machine")}
	}
	r := Result{State: m.state, Steps: m.steps, EmittedWords: m.emitted, NeedProgram: requestCopy(m.pending)}
	if m.failure != nil {
		x := *m.failure
		r.Err = &x
	}
	return r
}
func (m *Machine) busyResult() Result {
	r := m.State()
	r.State = "refused"
	r.Err = failed("Busy", [32]byte{}, wpm.Span{}, "mutating callback reentry is not admitted")
	return r
}

// Step's quota counts charged work, including the input-word compilation debt
// before a program's first effect. Compile itself/callbacks have separately
// bounded input but no instruction-derived wall-time guarantee.
func (m *Machine) Step(ctx context.Context, quota uint32) Result {
	if m == nil {
		return m.State()
	}
	if m.busy {
		return m.busyResult()
	}
	if m.terminal() {
		return m.State()
	}
	if quota == 0 || quota > m.limits.SliceSteps {
		return m.fail("refused", "InvalidQuota", "quota must be 1..SliceSteps")
	}
	if ctx == nil {
		return m.fail("refused", "InvalidContext", "nil context")
	}
	if err := ctx.Err(); err != nil {
		return m.fail("stopped", "HostCancelled", err.Error())
	}
	if m.state == "waiting" {
		return m.State()
	}
	m.busy = true
	defer func() { m.busy = false }()
	m.state = "running"
	remaining := uint64(quota)
	for remaining > 0 && !m.terminal() && m.state != "waiting" {
		if err := ctx.Err(); err != nil {
			return m.fail("stopped", "HostCancelled", err.Error())
		}
		if m.debt > 0 {
			n := m.debt
			if n > remaining {
				n = remaining
			}
			if n > m.limits.Steps-m.steps {
				n = m.limits.Steps - m.steps
			}
			m.steps += n
			m.debt -= n
			remaining -= n
			if m.debt > 0 && m.steps == m.limits.Steps {
				return m.fail("limited", "StepLimit", "program scan exhausts run work budget")
			}
			if m.debt == 0 && m.entry != nil {
				m.frames = append(m.frames, m.entry)
				m.entry = nil
			}
			continue
		}
		f, _ := m.current()
		if f == nil {
			m.state = "complete"
			break
		}
		if f.pc == len(f.program.code) && !f.emitting() {
			if len(m.frames) == 1 {
				m.state = "complete"
				break
			}
			if !m.charge(&remaining) {
				break
			}
			m.frames = m.frames[:len(m.frames)-1]
			continue
		}
		if f.each != nil {
			m.advanceEach(f, &remaining)
			continue
		}
		if f.preparation != nil {
			m.advanceInstruction(f, &remaining)
			continue
		}
		i := f.program.code[f.pc]
		if !f.emitting() && len(i.args) > 0 && i.op != 0xfc13 && !f.evaluated {
			if !m.charge(&remaining) {
				break
			}
			f.preparation = &instructionPreparation{instruction: i}
			continue
		}
		if !m.charge(&remaining) {
			break
		}
		if f.emitting() {
			m.deliver(ctx, f)
			continue
		}
		f.evaluated = false
		m.execute(ctx, f)
	}
	return m.State()
}
func (m *Machine) charge(remaining *uint64) bool {
	if m.steps >= m.limits.Steps {
		m.fail("limited", "StepLimit", "run work budget")
		return false
	}
	m.steps++
	*remaining--
	return true
}
func (m *Machine) setValue(f *frame, slot uint32, v value, at wpm.Span) bool {
	if uint32(v.wordLen()) > m.limits.VariableWords {
		m.stopWith("limited", "ValueLimit", "variable value word budget", f.program.source, at)
		return false
	}
	if int(slot) >= len(f.variables) {
		m.stopWith("limited", "VariableLimit", "variable slot budget", f.program.source, at)
		return false
	}
	v.assigned = true
	f.variables[slot] = v
	return true
}
func (m *Machine) number(f *frame, v value, at wpm.Span) (int64, bool) {
	if !v.numeric {
		m.stopWith("refused", "UnsupportedCoercion", "numeric control expression required", f.program.source, at)
		return 0, false
	}
	return v.number, true
}

func (m *Machine) startEmission(f *frame, i instruction, kind string, words []wpm.Word) {
	f.emission = words
	f.emitIndex = 0
	f.emitAt = i.at
	f.emitKind = kind
}
func (m *Machine) execute(ctx context.Context, f *frame) {
	i := f.program.code[f.pc]
	switch i.op {
	case opLiteral:
		m.startEmission(f, i, "literal", i.words)
	case opKey:
		m.startEmission(f, i, "key", i.words)
	case 0xfc0c:
		m.startEmission(f, i, "display-off", i.words)
	case 0xfc01:
		v, ok := f.values[0], true
		if ok && !v.numeric {
			m.stopWith("refused", "UnsupportedAssignment", "string assignment/coercion is unqualified", f.program.source, i.at)
			return
		}
		if ok && m.setValue(f, i.slot, v, i.at) {
			f.pc++
		}
	case 0xfc34:
		v := f.variables[i.slot]
		if !v.assigned {
			m.stopWith("refused", "UndefinedVariable", i.name, f.program.source, i.at)
			return
		}
		f.emitValues = v.words()
		f.emitIndex = 0
		f.emitAt = i.at
		f.emitKind = "literal"

	case 0xfc15:
		n, ok := m.number(f, f.values[0], i.at)
		if ok {
			if n == 0 {
				f.pc = i.jump
			} else {
				f.pc++
			}
		}
	case 0xfc0e, 0xfc14:
		f.pc = i.jump
	case 0xfc10, 0xfc16:
		f.pc++
	case 0xfc12:
		m.startFor(f, i)
	case 0xfc13:
		m.startEach(f, i)
	case 0xfc0f:
		m.nextFor(f, i)
	case 0xfc2b:
		n, ok := m.number(f, f.values[0], i.at)
		if !ok {
			return
		}
		active := len(f.loops) > 0 && f.loops[len(f.loops)-1].start == f.pc
		if n == 0 {
			if active {
				f.loops = f.loops[:len(f.loops)-1]
			}
			f.pc = i.jump
			return
		}
		if !active {
			if uint32(len(f.loops)) >= m.limits.LoopDepth {
				m.stopWith("limited", "LoopLimit", "loop depth budget", f.program.source, i.at)
				return
			}
			f.loops = append(f.loops, loopState{start: f.pc, end: i.loop, kind: 0xfc2b})
		}
		f.pc++
	case 0xfc11:
		f.pc = i.jump
	case 0xfc03:
		if i.loop < 0 {
			f.pc++
			return
		}
		if len(f.loops) == 0 || f.loops[len(f.loops)-1].start != i.loop {
			m.fail("refused", "LoopState", "missing enclosing FOR")
			return
		}
		loop := f.loops[len(f.loops)-1]
		f.loops = f.loops[:len(f.loops)-1]
		f.pc = loop.end + 1
	case 0xfc19:
		if len(f.loops) == 0 || f.loops[len(f.loops)-1].start != i.loop {
			m.fail("refused", "LoopState", "missing enclosing FOR")
			return
		}
		f.pc = f.loops[len(f.loops)-1].end
	case 0xfc1c:
		f.onError = i.jump
		f.pc++
	case 0xfc1d:
		f.onNotFound = i.jump
		f.pc++
	case 0xfc18:
		if m.resolver == nil {
			m.fail("refused", "MissingResolver", "NEST requires injected resolver")
			return
		}
		m.sequence++
		req := ProgramRequest{ID: m.sequence, Parent: f.program.source, Name: wordsCopy(i.words), At: i.at}
		f.pc++
		res := m.resolver.Resolve(ctx, *requestCopy(&req))
		m.acceptResolution(req, res)
	case 0xfc20:
		// The qualified normal-flow QUIT terminates the entire invocation,
		// including parent frames. Already delivered sink effects remain owned
		// by that sink; this does not imply rollback or an operator Stop action.
		m.frames = nil
		m.state = "complete"
	case 0xfc22:
		if len(m.frames) < 2 {
			m.fail("refused", "UnsupportedReturnContext", "RETURN qualified only in child")
			return
		}
		m.frames = m.frames[:len(m.frames)-1]
	default:
		m.fail("refused", "UnsupportedInstruction", "unqualified instruction")
	}
}
func (m *Machine) deliver(ctx context.Context, f *frame) {
	if f.emitIndex >= f.emissionLength() {
		f.clearEmission()
		f.pc++
		return
	}
	if m.emitted >= m.limits.OutputWords {
		m.fail("limited", "OutputLimit", "native word delivery budget")
		return
	}
	var word wpm.Word
	if f.emitValues != nil {
		word = wpm.Word{Value: f.emitValues[f.emitIndex], Kind: wpm.Literal, Span: wpm.Span{Offset: f.emitAt.Offset}}
	} else {
		word = f.emission[f.emitIndex]
	}
	kind := f.emitKind
	effect := Effect{Kind: kind, Words: []wpm.Word{word}, Source: f.program.source, At: f.emitAt}
	m.emitted++
	receipt, err := m.sink.Apply(ctx, effect)
	m.lastMayHaveEffects = receipt.MayHaveEffects
	if err != nil {
		m.stopWith("failed", "HostFailure", err.Error(), f.program.source, f.emitAt)
		return
	}
	f.emitIndex++
	if !noCondition(receipt.Condition) {
		f.clearEmission()
		if receipt.Condition != NotFound || kind != "key" || word.Value != 0x8021 {
			m.stopWith("refused", "UnsupportedConditionContext", string(receipt.Condition), f.program.source, f.emitAt)
			return
		}
		m.condition(receipt.Condition, f.program.source, f.emitAt)
		return
	}
	if f.emitIndex == f.emissionLength() {
		f.clearEmission()
		f.pc++
	}
}
func (m *Machine) condition(condition Condition, source [32]byte, at wpm.Span) {
	for len(m.frames) > 0 {
		f := m.frames[len(m.frames)-1]
		if f.handling {
			m.stopWith("refused", "UnsupportedHandlerReentry", "error within handler is unqualified", source, at)
			return
		}
		target := f.onError
		if condition == NotFound {
			target = f.onNotFound
		}
		if target >= 0 {
			f.pc = target
			f.evaluated = false
			f.preparation = nil
			f.each = nil
			f.clearEmission()
			f.loops = nil
			f.handling = true
			return
		}
		if len(m.frames) == 1 {
			m.stopWith("failed", "UnhandledCondition", string(condition), source, at)
			return
		}
		// Only the captured child command-error propagation is qualified.
		if condition != CommandError {
			m.stopWith("refused", "UnsupportedConditionPropagation", string(condition), source, at)
			return
		}
		m.frames = m.frames[:len(m.frames)-1]
	}
}
func validResolution(r Resolution) bool {
	switch r.State {
	case "ready":
		return r.Image != nil && r.Err == nil && noCondition(r.Condition)
	case "pending":
		return r.Image == nil && r.Err == nil && noCondition(r.Condition)
	case "condition":
		return r.Image == nil && r.Err == nil && r.Condition == CommandError
	case "host-error":
		return r.Image == nil && r.Err != nil && noCondition(r.Condition)
	}
	return false
}
func (m *Machine) acceptResolution(req ProgramRequest, r Resolution) {
	if !validResolution(r) {
		m.stopWith("refused", "InvalidResolution", "inconsistent/unsupported resolution fields", req.Parent, req.At)
		return
	}
	switch r.State {
	case "pending":
		m.pending = requestCopy(&req)
		m.state = "waiting"
	case "host-error":
		m.stopWith("failed", "HostFailure", r.Err.Error(), req.Parent, req.At)
	case "condition":
		m.condition(r.Condition, req.Parent, req.At)
	case "ready":
		if uint32(len(m.frames)) >= m.limits.CallDepth {
			m.stopWith("limited", "CallLimit", "nested-file depth budget", req.Parent, req.At)
			return
		}
		if uint64(r.Image.Inspect().Body.Length/2) > m.limits.Steps-m.steps {
			m.stopWith("limited", "StepLimit", "nested scan exceeds remaining work budget", req.Parent, req.At)
			return
		}
		p, err := Compile(r.Image, m.policy, m.limits)
		if err != nil {
			detail := err.Error()
			m.stopWith("refused", "NestedCompile", detail, req.Parent, req.At)
			return
		}
		if p.hasVariables {
			m.stopWith("refused", "UnsupportedVariableScope", "child variable scope unqualified", p.source, req.At)
			return
		}
		if p.cost > m.limits.Steps-m.steps {
			m.stopWith("limited", "StepLimit", "nested program scan budget", p.source, req.At)
			return
		}
		m.entry = newFrame(p)
		m.debt = p.cost
	}
}
func (m *Machine) Resume(id uint64, resolution Resolution) error {
	if m == nil {
		return failed("InvalidMachine", [32]byte{}, wpm.Span{}, "nil machine")
	}
	if m.busy {
		return failed("Busy", [32]byte{}, wpm.Span{}, "callback reentry")
	}
	if m.state != "waiting" || m.pending == nil || m.pending.ID != id {
		return failed("StaleResume", [32]byte{}, wpm.Span{}, "no matching pending request")
	}
	if resolution.State == "pending" || !validResolution(resolution) {
		return failed("InvalidResolution", m.pending.Parent, m.pending.At, "terminal resolution required; pending request unchanged")
	}
	request := *requestCopy(m.pending)
	m.busy = true
	defer func() { m.busy = false }()
	m.pending = nil
	m.state = "running"
	m.acceptResolution(request, resolution)
	if m.terminal() {
		return m.State().Err
	}
	return nil
}
func (m *Machine) Stop(reason string) Result {
	if m == nil {
		return m.State()
	}
	if m.busy {
		return m.busyResult()
	}
	if m.terminal() {
		return m.State()
	}
	return m.fail("stopped", "HostStop", reason)
}
