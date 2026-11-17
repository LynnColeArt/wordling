package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

type styleUI struct {
	stage, selected  int
	name, draft, err string
	bold             bool
}

const (
	styleList = iota + 1
	styleEdit
	styleName
	styleCodes
)

func (m Model) openStyles() Model {
	m.closeMenus()
	m.styles = styleUI{stage: styleList}
	return m
}

func (m Model) stylePress(key input.Key) (tea.Model, tea.Cmd) {
	if key.IsRepeat || key.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	u := &m.styles
	if key.Code == tea.KeyF1 || key.Code == tea.KeyEscape {
		switch u.stage {
		case styleList:
			m.styles = styleUI{}
		case styleEdit:
			u.stage = styleList
		case styleName, styleCodes:
			u.stage = styleEdit
		}
		return m, nil
	}
	u.err = ""
	switch u.stage {
	case styleList:
		list := m.session.Document().NamedStyles()
		switch key.Code {
		case '3':
			m.styles = styleUI{stage: styleEdit, selected: u.selected}
		case tea.KeyF7:
			m.styles = styleUI{}
		case tea.KeyUp:
			u.selected = max(0, u.selected-1)
		case tea.KeyDown:
			u.selected = min(max(0, len(list)-1), u.selected+1)
		case '1', tea.KeyEnter:
			if u.selected >= len(list) {
				u.err = "Create a style first"
				break
			}
			next, err := m.session.ApplyNamedStyle(list[u.selected])
			if err != nil {
				u.err = err.Error()
			} else {
				m.session, m.styles, m.notice = next, styleUI{}, ""
			}
		case '2':
			next, err := m.session.CloseNamedStyle()
			if err != nil {
				u.err = err.Error()
			} else {
				m.session, m.styles, m.notice = next, styleUI{}, ""
			}
		}
	case styleEdit:
		switch key.Code {
		case '1':
			u.stage, u.draft = styleName, ""
		case '4':
			u.stage = styleCodes
		case tea.KeyF7:
			if !u.bold {
				u.err = "Add Bold in Codes (F6) before saving this paired style"
				break
			}
			next, err := m.session.CreateNamedStyle(u.name)
			if err != nil {
				u.err = err.Error()
			} else {
				m.session = next
				m.styles = styleUI{stage: styleList, selected: len(next.Document().NamedStyles()) - 1}
			}
		}
	case styleName:
		switch key.Code {
		case tea.KeyEnter:
			for _, style := range m.session.Document().NamedStyles() {
				if strings.EqualFold(u.draft, style.Name) {
					u.err = "ERROR: Style name already exists"
					return m, nil
				}
			}
			if strings.TrimSpace(u.draft) == "" {
				u.err = "Enter a style name"
				break
			}
			u.name, u.stage = u.draft, styleEdit
		case tea.KeyBackspace:
			if n := len(u.draft); n > 0 {
				u.draft = u.draft[:n-1]
			}
		default:
			if len(u.draft)+len(key.Text) <= 12 && strings.IndexFunc(key.Text, func(c rune) bool { return c < 32 || c > 126 }) < 0 {
				u.draft += key.Text
			}
		}
	case styleCodes:
		switch key.Code {
		case tea.KeyF6:
			u.bold = !u.bold
		case tea.KeyF7:
			u.stage = styleEdit
		}
	}
	return m, nil
}

func (m Model) styleView() tea.View {
	u := m.styles
	switch u.stage {
	case styleList:
		list := m.session.Document().NamedStyles()
		body := []string{"Styles", "", "  Name         Type     Description"}
		start := max(0, u.selected-max(1, m.height-5)+1)
		for i, s := range list[start:] {
			mark := "  "
			if i+start == u.selected {
				mark = "> "
			}
			body = append(body, mark+s.Name+strings.Repeat(" ", 13-len(s.Name))+"Paired")
		}
		return m.historicModalView(body, "1 On; 2 Off; 3 Create; 4 Edit; 5 Delete; 6 Save; 7 Retrieve; 8 Update: 1", u.err)
	case styleCodes:
		codes := ""
		if u.bold {
			codes = "[BOLD]                              [bold]"
		}
		return m.historicModalView([]string{codes, "Place Style On Codes above, and Style Off Codes below."}, "Style:  Press Exit when done", u.err)
	default:
		name := u.name
		footer := "Selection: 0"
		if u.stage == styleName {
			name = u.draft
			footer = "Selection: 1"
		}
		return m.historicModalView([]string{"Styles: Edit", "", "     1 - Name            " + name,
			"", "     2 - Type            Paired", "", "     3 - Description", "", "     4 - Codes", "", "     5 - Enter           HRt"}, footer, u.err)
	}
}
