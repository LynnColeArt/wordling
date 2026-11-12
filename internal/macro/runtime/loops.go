package runtime

func (m *Machine) startFor(f *frame, i instruction) {
	start, ok := m.number(f, f.values[0], i.at)
	if !ok {
		return
	}
	stop, ok := m.number(f, f.values[1], i.at)
	if !ok {
		return
	}
	step, ok := m.number(f, f.values[2], i.at)
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
	if !m.setValue(f, i.slot, value{number: start, numeric: true}, i.at) {
		return
	}
	f.loops = append(f.loops, loopState{start: f.pc, end: i.loop, kind: 0xfc12, name: i.name, slot: i.slot, current: start, stop: stop, step: step})
	f.pc++
}
func (m *Machine) startEach(f *frame, i instruction) {
	if uint32(len(f.loops)) >= m.limits.LoopDepth {
		m.stopWith("limited", "LoopLimit", "loop nesting budget", f.program.source, i.at)
		return
	}
	f.each = &eachPreparation{instruction: i}
}

func (m *Machine) nextFor(f *frame, i instruction) {
	if len(f.loops) == 0 || f.loops[len(f.loops)-1].start != i.jump {
		m.fail("refused", "LoopState", "missing current FOR/FOR EACH")
		return
	}
	loop := &f.loops[len(f.loops)-1]
	if loop.kind == 0xfc13 {
		loop.item = loop.item.next
		if loop.item == nil {
			f.loops = f.loops[:len(f.loops)-1]
			f.pc++
			return
		}
		if !m.setValue(f, loop.slot, loop.item.value, i.at) {
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
	if !m.setValue(f, loop.slot, value{number: next, numeric: true}, i.at) {
		return
	}
	f.pc = loop.start + 1
}
