package layout

import "github.com/lynncoleart/wordling/internal/document"

type advanceOffset struct {
	right, down float64
}

func advanceHorizontalOffset(mode document.AdvanceMode, value int, screenLeft, offset float64) float64 {
	distance := float64(value) / document.UnitsPerInch
	switch mode {
	case document.AdvancePosition:
		return distance - screenLeft
	case document.AdvanceRight:
		return offset + distance
	}
	return offset
}

// PrintedBaseline reports the formatter baseline while the screen stays on its text row.
func (l Layout) PrintedBaseline(gap int) (float64, bool) {
	row, _, ok := l.PositionAt(gap)
	if !ok {
		return 0, false
	}
	return l.Lines[row].TopInches + l.advanceOffsets[gap].down, true
}

func (l *Layout) recordAdvance(gap int, right, down float64) {
	if right != 0 || down != 0 {
		if l.advanceOffsets == nil {
			l.advanceOffsets = make(map[int]advanceOffset)
		}
		l.advanceOffsets[gap] = advanceOffset{right, down}
	}
}

func (l Layout) PrintedPageDepth(gap int) (float64, bool) {
	row, _, ok := l.PositionAt(gap)
	if !ok {
		return 0, false
	}
	top := l.Settings.MarginTopInches
	for i := 0; i <= row; i++ {
		for _, item := range l.Lines[i].Tokens {
			if item.Index >= gap {
				break
			}
			if units, _, ok := item.Token.PageMargins(); ok {
				top = float64(units) / document.UnitsPerInch
			}
		}
	}
	baseline, _ := l.PrintedBaseline(gap)
	return baseline - top, true
}

func clampAdvanceDown(vertical, distance, body int) int {
	return min(distance, max(0, body-vertical))
}
