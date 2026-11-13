package tui

import (
	"fmt"
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

func simpleTableFrame(table document.SimpleTable, gap int) (lines []string, x, y int, cell string) {
	columns := len(table.Widths)
	border := func(left, middle, right, fill string) string {
		parts := make([]string, columns)
		for i, width := range table.Widths {
			parts[i] = strings.Repeat(fill, width)
		}
		return left + strings.Join(parts, middle) + right
	}
	lines = append(lines, border("╔", "╤", "╗", "═"))
	selected, inside := table.CellAt(gap)
	for start := 0; start < len(table.Cells); start += columns {
		contents := make([][]string, columns)
		height := 1
		for column := range columns {
			current := table.Cells[start+column]
			contents[column] = strings.Split(current.Text, "\n")
			height = max(height, len(contents[column]))
			if inside && selected == start+column {
				before := current.Text[:gap-current.Start]
				x = 1 + len(before) - strings.LastIndexByte(before, '\n') - 1
				x = min(x, table.Widths[column])
				for _, width := range table.Widths[:column] {
					x += width + 1
				}
				y = len(lines) + strings.Count(before, "\n")
				cell = fmt.Sprintf("Cell %c%d", 'A'+rune(column), start/columns+1)
			}
		}
		for line := range height {
			parts := make([]string, columns)
			for column, width := range table.Widths {
				value := ""
				if line < len(contents[column]) {
					value = contents[column][line]
				}
				parts[column] = fmt.Sprintf("%-*s", width, value)
			}
			lines = append(lines, "║"+strings.Join(parts, "│")+"║")
		}
		if start+columns < len(table.Cells) {
			lines = append(lines, border("╟", "┼", "╢", "─"))
		}
	}
	lines = append(lines, border("╚", "╧", "╝", "═"))
	return
}

type tablePrompt struct {
	stage   int
	draft   string
	columns int
	typed   bool
}

func (p tablePrompt) footer() string {
	switch p.stage {
	case 1:
		return "1 Columns; 2 Tables; 3 Math: 0"
	case 2:
		return "Table: 1 Create; 2 Edit: 0"
	case 3:
		return "Number of Columns: " + p.draft
	case 4:
		return "Number of Rows: " + p.draft
	case 5:
		return "1 Size; 2 Format; 3 Lines; 4 Header; 5 Math; 6 Options; 7 Join; 8 Split: 0"
	}
	return ""
}

func (m Model) tablePress(key input.Key) (tea.Model, tea.Cmd) {
	p := &m.tablePrompt
	if key.Mod != 0 || key.IsRepeat {
		return m, nil
	}
	switch key.Code {
	case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
		m.tablePrompt = tablePrompt{}
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		switch {
		case p.stage == 1 && key.Code == '2':
			p.stage = 2
		case p.stage == 2 && key.Code == '1':
			p.stage, p.draft, p.typed = 3, "3", false
		case p.stage == 3 || p.stage == 4:
			if !p.typed {
				p.draft = ""
				p.typed = true
			}
			if len(p.draft) < 2 {
				p.draft += string(key.Code)
			}
		}
	case tea.KeyBackspace:
		if len(p.draft) > 0 {
			p.draft = p.draft[:len(p.draft)-1]
			p.typed = true
		}
	case tea.KeyEnter:
		if p.stage < 3 || p.stage > 4 {
			break
		}
		value, _ := strconv.Atoi(p.draft)
		limit := 4
		if p.stage == 4 {
			limit = document.MaxTableRows
		}
		if value < 2 || value > limit {
			m.notice = fmt.Sprintf("Enter a number from 2 to %d", limit)
			break
		}
		m.notice = ""
		if p.stage == 3 {
			p.stage, p.draft, p.columns, p.typed = 4, "1", value, false
		} else {
			columns := p.columns
			m.tablePrompt = tablePrompt{}
			next, cmd := m.reduce(editor.Event{Command: editor.CreateTable, TableColumns: columns, TableRows: value})
			result, ok := next.(Model)
			if ok && result.session.Snapshot().NativeRevision != m.session.Snapshot().NativeRevision {
				result.tablePrompt.stage = 5
				return result, cmd
			}
			return next, cmd
		}
	}
	return m, nil
}
