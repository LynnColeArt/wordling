package tui

import (
	"fmt"
	"slices"
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
	_, joined := table.Cells[0].JoinedRight()
	topMiddle := "╤"
	if joined {
		topMiddle = "═"
	}
	lines = append(lines, border("╔", topMiddle, "╗", "═"))
	selected, inside := table.CellAt(gap)
	for start := 0; start < len(table.Cells); start += columns {
		if slices.Contains(table.PageStarts, start) {
			lines = append(lines, strings.Repeat("─", 65), border("╔", "╤", "╗", "═"))
		}
		contents := make([][]string, columns)
		height := 1
		for column := range columns {
			current := table.Cells[start+column]
			contents[column] = current.Lines()
			height = max(height, len(contents[column]))
			if inside && selected == start+column {
				before := string([]rune(current.DisplayText())[:gap-current.Start])
				x = 1 + len([]rune(before[strings.LastIndexByte(before, '\n')+1:]))
				x = min(x, table.Widths[column])
				for _, width := range table.Widths[:column] {
					x += width + 1
				}
				y = len(lines) + strings.Count(before, "\n")
				cell = fmt.Sprintf("Cell %c%d", 'A'+rune(column), start/columns+1)
			}
		}
		if joined && start == 0 {
			right, _ := table.Cells[0].JoinedRight()
			lines = append(lines, fmt.Sprintf("║%-*s %-*s║", table.Widths[0], table.Cells[0].DisplayText(), table.Widths[1], right))
			lines = append(lines, border("╟", "┬", "╢", "─"))
			continue
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
		if slices.Contains(table.PageStarts, start+columns) {
			lines = append(lines, border("╚", "╧", "╝", "═"))
		} else if start+columns < len(table.Cells) {
			lines = append(lines, border("╟", "┼", "╢", "─"))
		}
	}
	lines = append(lines, border("╚", "╧", "╝", "═"))
	return
}

// tableReveal displays the table structure and the current native character.
func tableReveal(table document.SimpleTable, gap, width, rows int) []string {
	var definition strings.Builder
	fmt.Fprintf(&definition, "[Tbl Def:I;%d", len(table.Widths))
	for range table.Widths {
		fmt.Fprintf(&definition, ",%.2f\"", 6.5/float64(len(table.Widths)))
	}
	definition.WriteByte(']')
	lines := []string{revealCode + definition.String() + screenReset}
	activeRow := 0
	for start := 0; start < len(table.Cells); start += len(table.Widths) {
		runs := []revealRun{{"[Row]", revealCode}}
		activeColumn, column := 0, 5
		for _, cell := range table.Cells[start : start+len(table.Widths)] {
			if cell.Covered() {
				continue
			}
			runs = append(runs, revealRun{"[Cell]", revealCode})
			column += 6
			value := cell.RevealText(-1)
			if tail, joined := cell.JoinedRight(); joined {
				value += "[Tab]" + tail
			}
			if gap >= cell.Start && gap <= cell.End {
				activeRow = len(lines)
				prefix, active, suffix := cell.RevealParts(gap)
				if tail, joined := cell.JoinedRight(); joined {
					suffix += "[Tab]" + tail
				}
				activeColumn = column + len([]rune(prefix))
				runs = append(runs, revealRun{prefix, revealBase}, revealRun{active, revealActive}, revealRun{suffix, revealBase})
				column += len([]rune(prefix + active + suffix))
				continue
			}
			runs = append(runs, revealRun{value, revealBase})
			column += len([]rune(value))
		}
		lines = append(lines, renderReveal(runs, max(0, activeColumn-width+1), width))
	}
	lines = append(lines, revealCode+"[Tbl Off]"+screenReset)
	first := max(0, activeRow-3)
	return lines[first:min(first+rows, len(lines))]
}

type tablePrompt struct {
	stage   int
	draft   string
	columns int
	typed   bool
	source  int
	block   bool
	anchor  int
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
	case 6:
		return "1 Calculate; 2 Formula; 3 Copy Formula: 0"
	case 7:
		return "Enter formula: " + p.draft
	case 8:
		return "1 Cell; 2 Down; 3 Right: 0"
	case 9:
		return "Move cursor; press Enter to retrieve."
	case 10:
		return "Join cells? No (Yes)"
	case 11:
		return "Math: 1 On; 2 Off; 3 Define; 4 Calculate: 0"
	case 5:
		return "1 Size; 2 Format; 3 Lines; 4 Header; 5 Math; 6 Options; 7 Join; 8 Split: 0"
	}
	return ""
}

func (m Model) tablePress(key input.Key) (tea.Model, tea.Cmd) {
	p := &m.tablePrompt
	if key.IsRepeat || key.Mod != 0 && (p.stage != 7 || key.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0) && !(p.stage == 5 && key.Code == tea.KeyF4 && key.Mod == tea.ModAlt) {
		return m, nil
	}
	if p.stage == 11 {
		switch key.Code {
		case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
			m.tablePrompt, m.notice = tablePrompt{}, ""
		case '4':
			next, err := m.session.CalculateColumnSubtotal()
			if err != nil {
				m.notice = err.Error()
			} else {
				m.session, m.tablePrompt, m.notice = next, tablePrompt{}, ""
			}
		case '1', '2':
			next, err := m.session.SetColumnMath(key.Code == '1')
			if err != nil {
				m.notice = err.Error()
			} else {
				m.session, m.tablePrompt, m.notice = next, tablePrompt{}, ""
			}
		}
		return m, nil
	}
	if p.stage >= 5 {
		return m.tableEditPress(key)
	}
	switch key.Code {
	case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
		m.tablePrompt = tablePrompt{}
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		switch {
		case p.stage == 1 && key.Code == '2':
			p.stage = 2
		case p.stage == 1 && key.Code == '3':
			p.stage = 11
		case p.stage == 2 && key.Code == '1':
			p.stage, p.draft, p.typed = 3, "3", false
		case p.stage == 3 || p.stage == 4:
			if !p.typed {
				p.draft = ""
				p.typed = true
			}
			if len(p.draft) < 3 {
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

func (m Model) tableEditPress(key input.Key) (tea.Model, tea.Cmd) {
	p := &m.tablePrompt
	switch key.Code {
	case tea.KeyF1, tea.KeyEscape:
		if p.stage == 5 {
			m.tablePrompt = tablePrompt{}
		} else {
			p.stage, p.draft = 5, ""
		}
		m.notice = ""
		return m, nil
	case tea.KeyF7:
		m.tablePrompt, m.notice = tablePrompt{}, ""
		return m, nil
	}
	table, ok := m.session.Document().SimpleTable()
	if !ok {
		m.tablePrompt = tablePrompt{}
		return m, nil
	}
	current, inside := table.CellAt(m.session.Snapshot().Gap)
	if !inside {
		p.stage = 5
		return m, nil
	}
	calculate := func(formula string, source int, recalc bool) (tea.Model, tea.Cmd) {
		next, err := m.session.TableMath(formula, source, recalc)
		if err != nil {
			m.notice = err.Error()
		} else {
			m.session, m.notice = next, ""
			p.stage, p.draft = 5, ""
		}
		return m, nil
	}
	switch p.stage {
	case 5:
		switch key.Code {
		case tea.KeyF4:
			if key.Mod == tea.ModAlt {
				p.block = !p.block
				p.anchor = current
				return m, nil
			}
		case '5':
			p.stage = 6
			return m, nil
		case '7':
			if p.block {
				p.stage = 10
			} else {
				m.notice = "Use Block to select cells before joining"
			}
			return m, nil
		}
	case 6:
		switch key.Code {
		case '1':
			return calculate("", -1, true)
		case '2':
			p.stage, p.draft = 7, table.Cells[current].Formula(current, len(table.Widths))
		case '3':
			if table.Cells[current].Formula(current, len(table.Widths)) == "" {
				m.notice = "Move to a cell that contains a formula"
			} else {
				p.stage, p.source = 8, current
			}
		}
		return m, nil
	case 7:
		switch key.Code {
		case tea.KeyEnter:
			return calculate(p.draft, -1, false)
		case tea.KeyBackspace:
			if len(p.draft) != 0 {
				p.draft = p.draft[:len(p.draft)-1]
			}
		default:
			value := strings.ToUpper(key.Text)
			if len(p.draft)+len(value) <= 32 && strings.Trim(value, " ABCD0123456789+") == "" {
				p.draft += value
			}
		}
		return m, nil
	case 8:
		if key.Code == '1' {
			p.stage = 9
		}
		return m, nil
	case 9:
		if key.Code == tea.KeyEnter {
			return calculate("", p.source, false)
		}
	case 10:
		switch key.Code {
		case 'n', 'N':
			p.stage, p.block = 5, false
		case 'y', 'Y', tea.KeyEnter:
			next, err := m.session.JoinTableTopRow(p.anchor)
			if err != nil {
				m.notice = err.Error()
			} else {
				m.session, m.notice = next, ""
			}
			p.stage, p.block = 5, false
		}
		return m, nil
	}
	switch key.Code {
	case tea.KeyUp, tea.KeyDown, tea.KeyLeft, tea.KeyRight, tea.KeyHome, tea.KeyEnd, tea.KeyTab, tea.KeyPgUp, tea.KeyPgDown:
		if event, ok := resolve(key, editor.Editing); ok {
			return m.reduce(event)
		}
	}
	return m, nil
}
