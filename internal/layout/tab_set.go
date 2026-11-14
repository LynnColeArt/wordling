package layout

import (
	"math"

	"github.com/lynncoleart/wordling/internal/document"
)

func layoutTab(g geometry, ruler *document.TabSet, margin, column, right int) int {
	next, _ := layoutTabStop(g, ruler, margin, column, right)
	return next
}

func layoutTabStop(g geometry, ruler *document.TabSet, margin, column, right int) (int, bool) {
	if ruler == nil {
		return min(right, g.tabAfter(column)), false
	}
	origin := 0
	if !ruler.Absolute {
		origin = margin - ruler.Margin
	}
	for _, stop := range ruler.Stops {
		pos := stop + origin
		cells := int(math.Round(float64(pos-margin) / 120))
		if cells > column && cells <= right {
			return cells, ruler.Decimal[stop]
		}
	}
	return column, false
}

type tabSetChange struct {
	index int
	ruler *document.TabSet
}

func (l Layout) tabsAt(gap int) *document.TabSet {
	lo, hi := 0, len(l.tabSets)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if l.tabSets[mid].index < gap {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo == 0 {
		return nil
	}
	return l.tabSets[lo-1].ruler
}

func (l Layout) DecimalAnchor(index int) int { return l.decimalAnchors[index] }
