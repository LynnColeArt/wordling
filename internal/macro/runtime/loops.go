package runtime

func (m *Machine) startFor(f *frame, i instruction) {
	start, ok := m.number(f, i.args[0], i.at)
	if !ok {
		return
	}
	stop, ok := m.number(f, i.args[1], i.at)
	if !ok {
		return
	}
	step, ok := m.number(f, i.args[2], i.at)
	if !ok {
		return
	}
	if step == 0 || step > 0 && start > stop || step < 0 && start < stop {
		m.stopWith("refused", "UnsupportedLoopRange", "zero-step/empty-direction FOR context unqualified", f.program.source, i.at)
		return
	}
	if uint32(len(f.loops)) >= m.limits.LoopDepth {
		m.stopWith("limited", "LoopLimit", "loop nesting budget", f.program.source, i.at)
		return
	}
	if !m.setValue(f, i.name, value{number: start, numeric: true}, i.at) {
		return
	}
	f.loops = append(f.loops, loopState{start: f.pc, end: i.loop, kind: 0xfc12, name: i.name, current: start, stop: stop, step: step})
	f.pc++
}
func (m *Machine) startEach(f *frame, i instruction) {
	if uint32(len(f.loops)) >= m.limits.LoopDepth {
		m.stopWith("limited", "LoopLimit", "loop nesting budget", f.program.source, i.at)
		return
	}
	items := make([]value, 0, len(i.args))
	for _, arg := range i.args {
		v, ok := m.evaluate(f, arg, i.at)
		if !ok {
			return
		}
		if uint32(len(v.words())) > m.limits.VariableWords {
			m.stopWith("limited", "ValueLimit", "list item budget", f.program.source, i.at)
			return
		}
		items = append(items, v)
	}
	if !m.setValue(f, i.name, items[0], i.at) {
		return
	}
	f.loops = append(f.loops, loopState{start: f.pc, end: i.loop, kind: 0xfc13, name: i.name, items: items})
	f.pc++
}
func (m *Machine) nextFor(f *frame, i instruction) {
	if len(f.loops) == 0 || f.loops[len(f.loops)-1].start != i.jump {
		m.fail("refused", "LoopState", "missing current FOR/FOR EACH")
		return
	}
	loop := &f.loops[len(f.loops)-1]
	if loop.kind == 0xfc13 {
		loop.item++
		if loop.item == len(loop.items) {
			f.loops = f.loops[:len(f.loops)-1]
			f.pc++
			return
		}
		if !m.setValue(f, loop.name, loop.items[loop.item], i.at) {
			return
		}
		f.pc = loop.start + 1
		return
	}
	if loop.current == loop.stop {
		f.loops = f.loops[:len(f.loops)-1]
		f.pc++
		return
	}
	next, ok := checkedAdd(loop.current, loop.step)
	if !ok {
		m.stopWith("refused", "NumericOverflow", "FOR increment overflow", f.program.source, i.at)
		return
	}
	if loop.step > 0 && next > loop.stop || loop.step < 0 && next < loop.stop {
		f.loops = f.loops[:len(f.loops)-1]
		f.pc++
		return
	}
	loop.current = next
	if !m.setValue(f, loop.name, value{number: next, numeric: true}, i.at) {
		return
	}
	f.pc = loop.start + 1
}
