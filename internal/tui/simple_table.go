package tui

import (
	tea "charm.land/bubbletea/v2"
	"fmt"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

func simpleTableFrame(table document.SimpleTable, gap int) (lines []string, x, y int, cell string) {
	const width = document.TableCellWidth
	bar := strings.Repeat("═", width)
	lines = []string{
		"╔" + bar + "╤" + bar + "╗",
		fmt.Sprintf("║%-*s│%-*s║", width, table.Cells[0].Text, width, table.Cells[1].Text),
		"╟" + bar + "┼" + bar + "╢",
		fmt.Sprintf("║%-*s│%-*s║", width, table.Cells[2].Text, width, table.Cells[3].Text),
		"╚" + bar + "╧" + bar + "╝",
	}
	if index, inside := table.CellAt(gap); inside {
		x = 1 + index%2*(width+1) + min(width-1, gap-table.Cells[index].Start)
		y = 1 + index/2*2
		cell = fmt.Sprintf("Cell %c%d", 'A'+rune(index%2), index/2+1)
	}
	return
}

type tablePrompt struct {
	stage int
	draft string
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
	case '2':
		switch p.stage {
		case 1:
			p.stage = 2
		case 3, 4:
			p.draft = "2"
		}
	case '1', '3', '0', '4', '5', '6', '7', '8', '9':
		if p.stage == 2 && key.Code == '1' {
			p.stage, p.draft = 3, "3"
		} else if p.stage == 3 || p.stage == 4 {
			p.draft = string(key.Code)
		}
	case tea.KeyBackspace:
		p.draft = ""
	case tea.KeyEnter:
		if p.stage < 3 {
			break
		}
		if p.draft != "2" {
			m.notice = "Choose 2 for the default table layout"
			break
		}
		m.notice = ""
		if p.stage == 3 {
			p.stage, p.draft = 4, "1"
		} else {
			m.tablePrompt = tablePrompt{}
			next, cmd := m.reduce(editor.Event{Command: editor.CreateTable})
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
