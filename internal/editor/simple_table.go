package editor

import (
	"errors"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

func (s Session) editSimpleTable(event Event) (Session, bool, error) {
	switch event.Command {
	case ComposeCharacter, Text, Delete, Backspace, Insert, Tab, Left, Right, Up, Down, Home, End, Enter, PageUp, PageDown:
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
		case ComposeCharacter, Text, Enter:
			return s, true, refuse("Move into a table cell to edit")
		}
	} else {
		cell := table.Cells[index]
		display := strings.Map(func(r rune) rune {
			if r != '\n' {
				return ' '
			}
			return r
		}, cell.DisplayText())
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
			for next := index + 1; next < len(table.Cells); next++ {
				if !table.Cells[next].Covered() {
					gap = table.Cells[next].Start
					break
				}
			}
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
			} else if target < len(table.Cells) && !table.Cells[target].Covered() {
				next := table.Cells[target]
				gap = min(next.End, next.Start+column)
			}
		case Left:
			if gap > cell.Start {
				gap--
			} else {
				gap = 0
				for previous := index - 1; previous >= 0; previous-- {
					if !table.Cells[previous].Covered() {
						gap = table.Cells[previous].End
						break
					}
				}
			}
		case Right:
			if gap < cell.End {
				gap++
			} else {
				for next := index + 1; next < len(table.Cells); next++ {
					if !table.Cells[next].Covered() {
						gap = table.Cells[next].Start
						break
					}
				}
			}
		case Home:
			gap = cell.Start + strings.LastIndexByte(display[:gap-cell.Start], '\n') + 1
		case End:
			if next := strings.IndexByte(display[gap-cell.Start:], '\n'); next >= 0 {
				gap += next
			} else {
				gap = cell.End
			}
		case Enter, Text, Delete, Backspace, ComposeCharacter:
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
			var edit document.EditResult
			var err error
			if event.Command == ComposeCharacter {
				edit, err = s.native.WriteTableCharacter(s.cursor, event.Character.Set, event.Character.Number, s.over)
			} else {
				edit, err = s.native.EditTableCell(s.cursor, start, end, text)
			}
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

func (s Session) TableMath(formula string, source int, recalculate bool) (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection {
		return s, refuse("Table Math requires ordinary table editing")
	}
	edit, err := s.native.TableMath(s.cursor, formula, source, recalculate)
	if err != nil {
		return s, err
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	if edit.Changed {
		s.revision++
		s.lastSave = NotSaved
	}
	return s, nil
}

func (s Session) JoinTableTopRow(first int) (Session, error) {
	if s.mode != Editing || s.native == nil || s.workspace == nil || s.selection {
		return s, refuse("Join requires ordinary table editing")
	}
	edit, err := s.native.JoinTableTopRow(s.cursor, first)
	if err != nil {
		return s, err
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	if edit.Changed {
		s.revision++
		s.lastSave = NotSaved
	}
	return s, nil
}
