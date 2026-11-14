package layout

import (
	"encoding/binary"
	"sort"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

type noteBreak struct {
	lines, page, top, bottom int
}

// noteFlow is the fixed-height profile for an explicit multiline footnote.
// Its minimum first fragment may push the reference line to the next page.
func noteFlow(a []atom, g geometry, settings Settings, breaks []rowBreak) ([]rowBreak, map[int]noteBreak) {
	keep := document.DefaultNoteKeep
	top, bottom := defaultPageMargins(settings)
	forced := map[int]bool{}
	reserves := map[int]int{}
	pending := map[int]bool{}
	for _, b := range breaks {
		if b.conditional && b.kind != explicitPage {
			forced[b.index] = true
		}
		if b.pendingWidow {
			pending[b.index] = true
		}
	}
	splits := map[int]noteBreak{}
	for _, item := range a {
		switch item.kind {
		case document.FootnoteOptions:
			keep = item.keepNote
		case document.PageMargins:
			top, bottom = item.top, item.bottom
		case document.Footnote:
			if item.noteLines < 2 {
				continue
			}
			i := sort.Search(len(breaks), func(i int) bool { return breaks[i].index >= item.start })
			vertical, page := 0, 1
			lineTop, lineBottom := top, bottom
			if i < len(breaks) {
				b := breaks[i]
				vertical, page, lineTop, lineBottom = b.vertical, b.page, b.top, b.bottom
			} else if i > 0 {
				b := breaks[i-1]
				vertical, page = b.vertical+200, b.page
				if b.last || b.kind == explicitPage {
					vertical = 0
					page++
				}
			}
			fit := max(0, (printableHeight(settings, lineTop, lineBottom)-vertical)/200-3)
			if fit >= item.noteLines {
				continue
			}
			minimum := min(item.noteLines, max(1, (keep+199)/200))
			if fit < minimum && i > 0 && breaks[i-1].kind == returnLine && !breaks[i-1].last {
				forced[breaks[i-1].index] = true
				breaks = rowsFor(a, g, settings, forced)
				continue
			}
			if fit == 0 || item.noteLines-fit > (printableHeight(settings, lineTop, lineBottom)/200)-3 {
				continue
			}
			splits[item.start] = noteBreak{fit, page, lineTop, lineBottom}
			if i < len(breaks) && breaks[i].kind == returnLine && !breaks[i].last {
				forced[breaks[i].index] = true
				reserves[breaks[i].index] = (item.noteLines - fit + 2) * 200
				breaks = rowsFor(a, g, settings, forced)
			}
		}
	}
	for i := range breaks {
		breaks[i].noteReserve = reserves[breaks[i].index]
		breaks[i].pendingWidow = breaks[i].last && pending[breaks[i].index]
	}
	return breaks, splits
}

func noteFlowChanges(a []atom, splits map[int]noteBreak, tokens []Token) []document.ReflowChange {
	var changes []document.ReflowChange
	for _, item := range a {
		if item.kind != document.Footnote || item.noteLines < 2 {
			continue
		}
		b := splits[item.start]
		note, _ := tokens[item.start].Note()
		if note.FirstPageLines == b.lines {
			if b.lines == 0 {
				continue
			}
			raw := tokens[item.start].Raw
			i := 20
			for ; i < len(raw)-4 && raw[i] != 0xd4; i++ {
			}
			if i+32 <= len(raw) && int(binary.LittleEndian.Uint16(raw[i+8:i+10])) == b.page &&
				int(binary.LittleEndian.Uint16(raw[i+24:i+26])) == b.top &&
				int(binary.LittleEndian.Uint16(raw[i+18:i+20])) == 13200-b.top-b.bottom {
				continue
			}
		}
		changes = append(changes, document.ReflowChange{At: item.start, Kind: document.RefreshNoteBreak,
			NoteLines: uint8(b.lines), NotePage: uint16(b.page), NoteTop: uint16(b.top), NoteBottom: uint16(b.bottom)})
	}
	return changes
}

func footnoteLineCount(t Token) int {
	note, ok := t.Note()
	if !ok || note.End {
		return 0
	}
	return 1 + strings.Count(note.Text, "\n")
}
