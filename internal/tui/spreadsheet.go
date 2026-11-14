package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/worksheet"
)

type spreadsheetUI struct {
	stage             int
	link              bool
	path, area, draft string
}

const (
	sheetMenu = iota + 1
	sheetForm
	sheetFilename
	sheetRange
	sheetType
	sheetOptions
)

func (m Model) spreadsheetPress(k input.Key) (tea.Model, tea.Cmd) {
	if k.IsRepeat || k.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	u := &m.sheet
	if k.Code == tea.KeyF1 || k.Code == tea.KeyEscape || k.Code == tea.KeyF7 {
		switch u.stage {
		case sheetFilename, sheetRange, sheetType:
			u.stage, u.draft = sheetForm, ""
		case sheetForm, sheetOptions:
			u.stage = sheetMenu
		default:
			m.sheet = spreadsheetUI{}
		}
		m.notice = ""
		return m, nil
	}
	apply := func(refresh bool) {
		next, err := m.session.ImportSpreadsheet(u.path, u.area, u.link, refresh)
		if err != nil {
			m.notice = err.Error()
		} else {
			m.session, m.sheet, m.notice = next, spreadsheetUI{}, ""
		}
	}
	switch u.stage {
	case sheetMenu:
		switch k.Code {
		case '1', '2':
			*u = spreadsheetUI{stage: sheetForm, link: k.Code == '2'}
		case '4':
			u.stage = sheetOptions
		}
	case sheetForm:
		switch k.Code {
		case '1':
			u.stage, u.draft = sheetFilename, u.path
		case '2':
			u.stage, u.draft = sheetRange, u.area
		case '3':
			u.stage = sheetType
		case '4':
			apply(false)
		}
	case sheetOptions:
		if k.Code == '3' {
			apply(true)
		}
	case sheetType:
		if k.Code == '1' {
			u.stage = sheetForm
		}
	case sheetFilename, sheetRange:
		switch k.Code {
		case tea.KeyEnter:
			if u.stage == sheetFilename {
				u.path = strings.TrimSpace(u.draft)
			} else {
				r, err := worksheet.ParseRange(u.draft)
				if err != nil {
					m.notice = err.Error()
					return m, nil
				}
				u.area = r.String()
			}
			u.stage, u.draft, m.notice = sheetForm, "", ""
		case tea.KeyBackspace:
			if len(u.draft) > 0 {
				u.draft = u.draft[:len(u.draft)-1]
			}
		default:
			if len(u.draft)+len(k.Text) <= 80 && strings.IndexFunc(k.Text, func(c rune) bool { return c < 32 || c > 126 }) < 0 {
				u.draft += k.Text
			}
		}
	}
	return m, nil
}

func (m Model) spreadsheetView(view tea.View) tea.View {
	u := m.sheet
	switch u.stage {
	case sheetMenu:
		lines := strings.Split(view.Content, "\n")
		y := len(lines) - 1
		prompt := "Spreadsheet: 1 Import; 2 Create Link; 3 Edit Link; 4 Link Options: 0"
		lines[y] = clip(prompt, m.width)
		view.Content = strings.Join(lines, "\n")
		view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)), y)
		return view
	case sheetOptions:
		return m.historicModalView([]string{"Link Options:", "", "     1 - Update on Retrieve             No", "", "     2 - Show Link Codes                Yes", "", "     3 - Update All Links"}, "Selection: 0", m.notice)
	}
	title, verb := "Import", "Import"
	if u.link {
		title, verb = "Create Link", "Link"
	}
	prompt := "Selection: 0"
	switch u.stage {
	case sheetFilename:
		prompt = "Enter filename: " + u.draft
	case sheetRange:
		prompt = "Enter Range: " + u.draft
	case sheetType:
		prompt = "Type: 1 Table; 2 Text: 1"
	}
	return m.historicModalView([]string{"Spreadsheet: " + title, "", "     1 - Filename                 " + u.path, "", "     2 - Range                    " + u.area, "", "     3 - Type                     Table", "", "     4 - Perform " + verb}, prompt, m.notice)
}

func spreadsheetFrame(sheet document.SpreadsheetTable, width int) []string {
	var rows []string
	if sheet.Link != nil {
		rows = append(rows, commentBox("Link: "+sheet.Link.Path+"  "+sheet.Link.Range.String(), width)...)
	}
	display := func(i, w int) string {
		c := sheet.Cells[i]
		if c.Integer {
			signSpace := 2 - i%2
			return fmt.Sprintf("%*s%s", w-signSpace, c.Text, strings.Repeat(" ", signSpace))
		}
		return fmt.Sprintf("%-*s", w, c.Text)
	}
	rows = append(rows, "╔══════════╤═════════╗",
		"║"+display(0, 10)+"│"+display(1, 9)+"║",
		"╟──────────┼─────────╢",
		"║"+display(2, 10)+"│"+display(3, 9)+"║",
		"╚══════════╧═════════╝")
	if sheet.Link != nil {
		rows = append(rows, commentBox("Link End", width)...)
	}
	return rows
}
