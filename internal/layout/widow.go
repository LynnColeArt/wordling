package layout

import (
	"sort"

	"github.com/lynncoleart/wordling/internal/document"
)

// The formatter can move a paragraph past the preceding hard return,
// or move its last two lines by promoting one wrapped space.
func protectWidowRows(a []atom, g geometry, settings Settings, breaks []rowBreak) []rowBreak {
	enabled, started, protect := false, false, false
	previous, first := -1, -1
	var forced map[int]bool
	for _, item := range a {
		switch item.kind {
		case document.WidowProtectionOn, document.WidowProtectionOff:
			enabled = item.kind == document.WidowProtectionOn
		case document.HardReturn, document.HardPage:
			if protect && item.kind == document.HardReturn {
				start := sort.Search(len(breaks), func(i int) bool { return breaks[i].index >= first })
				end := sort.Search(len(breaks), func(i int) bool { return breaks[i].index >= item.start })
				if at, ok := widowBreak(breaks, start, end, previous); ok {
					if forced == nil {
						forced = make(map[int]bool)
					}
					forced[at] = true
					breaks = rowsFor(a, g, settings, forced)
				}
			}
			previous, started, protect = -1, false, false
			if item.kind == document.HardReturn {
				previous = item.start
			}
		case document.ASCII, document.ExtendedCharacter, document.HardSpace, document.DOSControl:
			if !started {
				first, started, protect = item.start, true, enabled
			}
		}
	}
	// DOS marks a possible widow at EOF and moves the preceding line when
	// a hard return closes the paragraph.
	if protect && len(breaks) >= 2 {
		i := len(breaks) - 1
		last, prior := &breaks[i], breaks[i-1]
		if prior.index >= first && last.last && !last.conditional && last.kind == wrapAtSpace && prior.page == last.page {
			last.pendingWidow = true
		}
	}
	return breaks
}

func widowBreak(breaks []rowBreak, start, end, previous int) (int, bool) {
	if end-start < 2 || end >= len(breaks) || breaks[start].page == breaks[end].page {
		return 0, false
	}
	if previous >= 0 && start > 0 && breaks[start-1].index == previous &&
		breaks[start].page != breaks[start+1].page &&
		breaks[start-1].page == breaks[start].page {
		return previous, true
	}
	if breaks[end-1].page != breaks[end].page && breaks[end-2].kind == wrapAtSpace &&
		breaks[end-2].page == breaks[end-1].page {
		return breaks[end-2].index, true
	}
	return 0, false
}
