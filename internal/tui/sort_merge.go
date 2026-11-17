package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type sortUI struct {
	stage             int
	merge, descending bool
}

const (
	sortInput = iota + 1
	sortOutput
	sortCriteria
	sortType
	sortOrder
	sortKeys
)

func (m Model) openSort() (tea.Model, tea.Cmd) {
	if m.session.Snapshot().Mode == editor.MergeMenuMode {
		next, _, err := m.session.Reduce(editor.Event{Command: editor.Enter})
		if err != nil {
			m.notice = err.Error()
			return m, nil
		}
		m.session = next
	}
	m.closeMenus()
	m.sort = sortUI{stage: sortInput}
	m.notice = ""
	return m, nil
}

func (m Model) sortPress(key input.Key) (tea.Model, tea.Cmd) {
	if key.IsRepeat || key.Mod != 0 {
		return m, nil
	}
	u := &m.sort
	switch key.Code {
	case tea.KeyF1, tea.KeyEscape:
		if u.stage > sortCriteria {
			u.stage = sortCriteria
		} else {
			m.sort = sortUI{}
		}
		m.notice = ""
		return m, nil
	case tea.KeyF7:
		if u.stage >= sortType {
			u.stage = sortCriteria
		} else {
			m.sort = sortUI{}
		}
		m.notice = ""
		return m, nil
	}
	switch u.stage {
	case sortInput, sortOutput:
		if key.Code == tea.KeyEnter {
			u.stage++
		}
	case sortCriteria:
		switch key.Code {
		case '1':
			if !u.merge {
				m.notice = "Choose Merge record type before sorting"
				return m, nil
			}
			next, err := m.session.SortMergeRecords(u.descending)
			if err != nil {
				m.notice = err.Error()
			} else {
				m.session, m.sort, m.notice = next, sortUI{}, ""
			}
		case '3':
			u.stage = sortKeys
		case '6':
			u.stage = sortOrder
		case '7':
			u.stage = sortType
		}
	case sortType:
		switch key.Code {
		case '1':
			u.merge, u.stage, m.notice = true, sortCriteria, ""
		case '2':
			u.merge, u.stage = false, sortCriteria
		}
	case sortOrder:
		switch key.Code {
		case '1', '2':
			u.descending, u.stage = key.Code == '2', sortCriteria
		}
	case sortKeys:
		if key.Code == tea.KeyEnter || key.Code == '1' {
			u.stage = sortCriteria
		}
	}
	return m, nil
}

func (m Model) sortView(view tea.View) tea.View {
	prompt := ""
	switch m.sort.stage {
	case sortInput:
		prompt = "Input file (press Enter for screen):"
	case sortOutput:
		prompt = "Output file (press Enter for screen):"
	default:
		title, record := "Sort by Line", "Line sort"
		if m.sort.merge {
			title, record = "Sort Secondary Merge File", "Merge sort"
		}
		order := "Ascending"
		if m.sort.descending {
			order = "Descending"
		}
		prompt = "1 Perform Action; 2 View; 3 Keys; 4 Select; 5 Action; 6 Order; 7 Type: 0"
		if m.sort.stage == sortType {
			prompt = "Type: 1 Merge; 2 Line; 3 Paragraph: 0"
		} else if m.sort.stage == sortOrder {
			prompt = "Order: 1 Ascending; 2 Descending: 0"
		} else if m.sort.stage == sortKeys {
			prompt = "Key 1: Alphabetical, Field 1, Line 1, Word 1"
		}
		return m.historicModalView([]string{title, "", "Key Typ Field Line Word", "1   a     1     1    1", "", "Action                     Order                     Type", "Sort                       " + order + "                 " + record}, prompt, m.notice)
	}
	lines := strings.Split(view.Content, "\n")
	last := len(lines) - 1
	lines[last] = clip(prompt, m.width)
	view.Content = strings.Join(lines, "\n")
	view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)), last)
	return view
}
