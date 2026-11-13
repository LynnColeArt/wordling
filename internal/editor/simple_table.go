package editor

import (
	"errors"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

func (s Session) editSimpleTable(event Event) (Session, bool, error) {
	switch event.Command {
	case Text, Delete, Backspace, Insert, Tab, Left, Right, Up, Down, Home, End, Enter, PageUp, PageDown:
	default:
		return s, false, nil
	}
	table, ok := s.native.SimpleTable()
	if !ok {
		return s, false, nil
	}
	if s.selection || s.homes != 0 {
		return s, false, nil
	}
	gap := s.cursor.Gap()
	index, inside := table.CellAt(gap)
	if event.Command == Insert {
		s.over = !s.over
		return s, true, nil
	}
	if !inside {
		switch event.Command {
		case Down, Right, Tab:
			gap = table.Cells[0].Start
		case PageDown:
			if len(table.PageStarts) != 0 {
				gap = table.Cells[table.PageStarts[0]].Start
			}
		case PageUp:
			gap = table.Cells[0].Start
		case Text, Enter:
			return s, true, refuse("Move into a table cell to edit")
		}
	} else {
		cell := table.Cells[index]
		display := cell.DisplayText()
		switch event.Command {
		case PageUp, PageDown:
			target := 0
			for _, first := range table.PageStarts {
				if event.Command == PageDown && first > index {
					target = first
					break
				}
				if event.Command == PageUp && first <= index {
					if first == index {
						break
					}
					target = first
				}
			}
			if event.Command == PageUp || target != 0 {
				gap = table.Cells[target].Start
			}
		case Tab:
			gap = table.Cells[min(index+1, len(table.Cells)-1)].Start
		case Up, Down:
			offset := gap - cell.Start
			lineStart := strings.LastIndexByte(display[:offset], '\n') + 1
			column := offset - lineStart
			if event.Command == Up && lineStart > 0 {
				end := lineStart - 1
				start := strings.LastIndexByte(display[:end], '\n') + 1
				gap = cell.Start + min(end, start+column)
				break
			}
			if event.Command == Down {
				if end := strings.IndexByte(display[offset:], '\n'); end >= 0 {
					start := offset + end + 1
					stop := len(display)
					if next := strings.IndexByte(display[start:], '\n'); next >= 0 {
						stop = start + next
					}
					gap = cell.Start + min(stop, start+column)
					break
				}
			}
			target := index + len(table.Widths)
			if event.Command == Up {
				target = index - len(table.Widths)
			}
			if target < 0 {
				gap = 0
			} else if target < len(table.Cells) {
				next := table.Cells[target]
				gap = min(next.End, next.Start+column)
			}
		case Left:
			if gap > cell.Start {
				gap--
			} else if index > 0 {
				gap = table.Cells[index-1].End
			} else {
				gap = 0
			}
		case Right:
			if gap < cell.End {
				gap++
			} else if index+1 < len(table.Cells) {
				gap = table.Cells[index+1].Start
			}
		case Home:
			gap = cell.Start + strings.LastIndexByte(display[:gap-cell.Start], '\n') + 1
		case End:
			if next := strings.IndexByte(display[gap-cell.Start:], '\n'); next >= 0 {
				gap += next
			} else {
				gap = cell.End
			}
		case Enter, Text, Delete, Backspace:
			start, end := gap, gap
			text := ""
			switch event.Command {
			case Enter:
				text = "\n"
			case Delete:
				end = min(end+1, cell.End)
			case Backspace:
				start = max(start-1, cell.Start)
			case Text:
				text = event.Text
				if s.over {
					end = min(end+len(event.Text), cell.End)
				}
			}
			edit, err := s.native.EditTableCell(s.cursor, start, end, text)
			if err != nil {
				var failure *document.Failure
				if errors.As(err, &failure) && failure.Category == document.TableRowTooTall {
					return s, true, refuse("Table row must fit on one page. Continue in the next row.")
				}
				return s, true, err
			}
			s.native, s.cursor = edit.Document, edit.Cursor
			if edit.Changed {
				s.revision++
				s.lastSave = NotSaved
			}
			return s, true, nil
		}
	}
	cursor, err := s.native.CursorAt(gap)
	if err == nil {
		s.cursor = cursor.WithReveal(s.cursor.Reveal())
	}
	return s, true, err
}
