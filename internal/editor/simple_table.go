package editor

func (s Session) editSimpleTable(event Event) (Session, bool, error) {
	switch event.Command {
	case Text, Delete, Backspace, Insert, Tab, Left, Right, Up, Down, Home, End, Enter:
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
		case Text, Enter:
			return s, true, refuse("Move into a table cell to edit")
		}
	} else {
		cell := table.Cells[index]
		switch event.Command {
		case Tab:
			gap = table.Cells[min(index+1, len(table.Cells)-1)].Start
		case Up, Down:
			target := index + 2
			if event.Command == Up {
				target = index - 2
			}
			if target < 0 {
				gap = 0
			} else if target < len(table.Cells) {
				next := table.Cells[target]
				gap = min(next.End, next.Start+gap-cell.Start)
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
			gap = cell.Start
		case End:
			gap = cell.End
		case Enter:
			return s, true, refuse("This table supports one line per cell")
		case Text, Delete, Backspace:
			start, end := gap, gap
			text := ""
			switch event.Command {
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
