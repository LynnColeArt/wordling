package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

func (m Model) dosTextPrompt() string {
	switch m.historic.dosTextStage {
	case 1:
		return "1 DOS Text; 2 Password; 3 Save As; 4 Comment; 5 Spreadsheet: "
	case 2:
		return "1 Save; 2 Retrieve (CR/LF to [HRt]); 3 Retrieve (CR/LF to [SRt] in HZone): "
	case 5:
		return "Replace " + m.historic.dosTextName + "? No (Yes)"
	case 4:
		return "Document to be saved (DOS Text): " + m.historic.dosTextName
	default:
		return "Document to be retrieved: " + m.historic.dosTextName
	}
}

func (m Model) dosTextPress(k input.Key) (tea.Model, tea.Cmd) {
	u := &m.historic
	if k.IsRepeat || k.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	if k.Code == tea.KeyF1 || k.Code == tea.KeyEscape {
		if u.dosTextStage == 5 {
			u.dosTextSave = nil
			u.dosTextStage = 0
		} else if u.dosTextStage == 4 {
			u.dosTextStage = 2
		} else {
			u.dosTextStage--
		}
		u.dosTextName, m.notice = "", ""
		return m, nil
	}
	switch u.dosTextStage {
	case 1, 2:
		if u.dosTextStage == 1 && k.Code == '5' {
			u.dosTextStage, m.sheet.stage, m.notice = 0, sheetMenu, ""
			return m, nil
		}
		if u.dosTextStage == 1 && k.Code == '4' {
			u.dosTextStage = 0
			return m.openComment(), nil
		}
		if u.dosTextStage == 2 && k.Code == '1' {
			u.dosTextStage, m.notice = 4, ""
		} else if (u.dosTextStage == 1 && k.Code == '1') || (u.dosTextStage == 2 && (k.Code == '2' || k.Code == '3')) {
			u.dosTextSoft = k.Code == '3'
			u.dosTextStage++
			m.notice = ""
		} else {
			m.notice = "This Text In/Out command is not yet implemented"
		}
	case 5:
		switch k.Code {
		case 'y', 'Y':
			return m.publishDOSText()
		case 'n', 'N', tea.KeyEnter:
			u.dosTextStage, u.dosTextName, u.dosTextSave = 4, "", nil
		}
	case 3, 4:
		switch k.Code {
		case tea.KeyEnter:
			if u.dosTextStage == 4 {
				data, err := m.session.Document().ExportDOSTextAt(m.runtime.now())
				if err == nil {
					u.dosTextSave, err = m.runtime.workspaceRoot.PrepareDOSTextSave(u.dosTextName, data)
				}
				if err != nil {
					m.notice = err.Error()
					return m, nil
				}
				if u.dosTextSave.Exists() {
					u.dosTextStage, m.notice = 5, ""
					return m, nil
				}
				return m.publishDOSText()
			}
			command := editor.ImportDOSHardReturns
			if u.dosTextSoft {
				command = editor.ImportDOSSoftReturns
			}
			next, cmd := m.reduce(editor.Event{Command: command, Text: u.dosTextName})
			result := next.(Model)
			if result.notice == "" {
				result.historic.dosTextStage, result.historic.dosTextName = 0, ""
			}
			return result, cmd
		case tea.KeyBackspace:
			if n := len(u.dosTextName); n > 0 {
				u.dosTextName = u.dosTextName[:n-1]
			}
		default:
			draft := fileBrowser{draft: u.dosTextName, touched: true}
			draft.addDraft(k.Text)
			u.dosTextName = draft.draft
		}
	}
	return m, nil
}

func (m Model) publishDOSText() (tea.Model, tea.Cmd) {
	u := &m.historic
	err := u.dosTextSave.Publish()
	u.dosTextSave = nil
	if err != nil {
		u.dosTextStage, m.notice = 4, err.Error()
	} else {
		u.dosTextStage, u.dosTextName, m.notice = 0, "", ""
	}
	return m, nil
}
