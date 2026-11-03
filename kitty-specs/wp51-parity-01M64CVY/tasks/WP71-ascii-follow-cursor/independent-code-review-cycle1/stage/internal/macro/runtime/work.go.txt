package runtime

// Values only share private immutable backing. One list node is allocated per
// actual charged evaluation result: no aggregate allocation or geometric copy.
type eachItem struct {
	value value
	next  *eachItem
}
type eachPreparation struct {
	instruction instruction
	index       int
	head, tail  *eachItem
	evaluation  evaluator
}
type instructionPreparation struct {
	instruction instruction
	index       int
	values      [3]value
	evaluation  evaluator
}

// The admitted single-binary grammar needs at most two temporary values. This
// fixed stack avoids variable-size setup and every postfix node consumes a step.
type evaluator struct {
	index, depth int
	stack        [2]value
}

func (e *evaluator) next(expr *expression, vars []value) (value, bool, error) {
	n := expr.code[e.index]
	e.index++
	var v value
	switch {
	case n.op != 0:
		a, b := e.stack[0], e.stack[1]
		if !a.numeric || !b.numeric {
			return value{}, false, evalFailure("UnsupportedCoercion")
		}
		v.numeric = true
		switch n.op {
		case '+':
			var ok bool
			v.number, ok = checkedAdd(a.number, b.number)
			if !ok {
				return value{}, false, evalFailure("NumericOverflow")
			}
		case '<':
			if a.number < b.number {
				v.number = 1
			}
		case '=':
			if a.number == b.number {
				v.number = 1
			}
		default:
			return value{}, false, evalFailure("UnsupportedOperator")
		}
		e.depth = 0
	case n.literal != nil:
		v.text = n.literal
	case n.name != "":
		if int(n.slot) >= len(vars) || !vars[n.slot].assigned {
			return value{}, false, evalFailure("UndefinedVariable")
		}
		v = vars[n.slot]
	default:
		v = value{number: n.number, numeric: true}
	}
	e.stack[e.depth] = v
	e.depth++
	return v, e.index == len(expr.code), nil
}
func (f *frame) emitting() bool { return f.emission != nil || f.emitValues != nil }
func (f *frame) emissionLength() int {
	if f.emitValues != nil {
		return len(f.emitValues)
	}
	return len(f.emission)
}
func (f *frame) clearEmission() { f.emission = nil; f.emitValues = nil }
func (m *Machine) advanceInstruction(f *frame, remaining *uint64) {
	if !m.charge(remaining) {
		return
	}
	p := f.preparation
	v, done, err := p.evaluation.next(p.instruction.args[p.index], f.variables)
	if err != nil {
		m.stopWith("refused", err.Error(), "expression not qualified/evaluable", f.program.source, p.instruction.at)
		return
	}
	if done {
		p.values[p.index] = v
		p.index++
		p.evaluation = evaluator{}
		if p.index == len(p.instruction.args) {
			f.values = p.values
			f.evaluated = true
			f.preparation = nil
		}
	}
}
func (m *Machine) advanceEach(f *frame, remaining *uint64) {
	if !m.charge(remaining) {
		return
	}
	p := f.each
	if p.index < len(p.instruction.args) {
		v, done, err := p.evaluation.next(p.instruction.args[p.index], f.variables)
		if err != nil {
			m.stopWith("refused", err.Error(), "expression not qualified/evaluable", f.program.source, p.instruction.at)
			return
		}
		if !done {
			return
		}
		if uint32(v.wordLen()) > m.limits.VariableWords {
			m.stopWith("limited", "ValueLimit", "list item budget", f.program.source, p.instruction.at)
			return
		}
		node := &eachItem{value: v}
		if p.tail == nil {
			p.head = node
		} else {
			p.tail.next = node
		}
		p.tail = node
		p.index++
		p.evaluation = evaluator{}
		return
	}
	if !m.setValue(f, p.instruction.slot, p.head.value, p.instruction.at) {
		return
	}
	f.loops = append(f.loops, loopState{start: f.pc, end: p.instruction.loop, kind: 0xfc13, name: p.instruction.name, slot: p.instruction.slot, item: p.head})
	f.pc++
	f.each = nil
}
