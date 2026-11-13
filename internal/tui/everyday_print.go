package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/layout"
)

type printScreen uint8

const (
	printClosed printScreen = iota
	printMenu
	printSelect
	printEdit
	printPort
	printFilename
	printView
)

type printUI struct {
	screen              printScreen
	port, draft, notice string
	pages               []layout.StandardPage
	page, top           int
}

func (m Model) printPress(key input.Key) (tea.Model, tea.Cmd) {
	p := &m.print
	if key.IsRepeat || key.Mod & ^tea.ModShift != 0 {
		return m, nil
	}
	if key.Code == tea.KeyF7 || key.Code == tea.KeyF1 || key.Code == tea.KeyEscape {
		switch p.screen {
		case printFilename, printPort:
			p.screen = printEdit
		case printEdit:
			p.screen = printMenu
		case printSelect:
			p.screen = printMenu
		default:
			p.screen, p.pages = printClosed, nil
		}
		p.notice = ""
		return m, nil
	}
	if !m.showEditorChrome() {
		return m, nil
	}
	p.notice = ""
	if p.screen == printFilename {
		switch key.Code {
		case tea.KeyBackspace:
			if len(p.draft) != 0 {
				p.draft = p.draft[:len(p.draft)-1]
			}
		case tea.KeyEnter:
			if p.draft != "" {
				p.port, p.screen = p.draft, printEdit
			}
		default:
			if len(key.Text) == 1 && key.Text[0] >= 32 && key.Text[0] < 127 && len(p.draft) < 80 {
				p.draft += strings.ToUpper(key.Text)
			}
		}
		return m, nil
	}
	if p.screen == printView {
		switch key.Code {
		case tea.KeyPgUp:
			p.page, p.top = max(0, p.page-1), 0
		case tea.KeyPgDown:
			p.page, p.top = min(len(p.pages)-1, p.page+1), 0
		case tea.KeyHome:
			p.page, p.top = 0, 0
		case tea.KeyUp:
			p.top = max(0, p.top-1)
		case tea.KeyDown:
			p.top = min(max(0, 67-m.height), p.top+1)
		}
		return m, nil
	}
	action := strings.ToLower(key.Text)
	if action == "" && key.Code >= '0' && key.Code <= '9' {
		action = string(key.Code)
	}
	switch p.screen {
	case printSelect:
		switch action {
		case "1":
			p.screen = printMenu
		case "3":
			p.screen = printEdit
		}
	case printEdit:
		if action == "2" {
			p.screen = printPort
		}
	case printPort:
		if action == "8" {
			p.screen, p.draft = printFilename, ""
		}
	case printMenu:
		switch action {
		case "s":
			p.screen = printSelect
		case "1", "2", "6":
			if err := m.runPrint(action); err != nil {
				m.print.notice = err.Error()
			}
		case "3", "4", "5", "7", "b", "n", "u", "g", "t":
			p.notice = "This print option is not yet implemented"
		}
	}
	return m, nil
}

func (m *Model) runPrint(action string) error {
	doc := m.session.Document()
	settings := editor.EverydaySettings()
	pages, err := layout.StandardPages(doc, settings)
	if err != nil {
		return err
	}
	page := 0
	if m.everyday.ready && m.everyday.revision == m.session.Snapshot().NativeRevision {
		projected := m.everyday.layout
		if line, _, ok := projected.PositionAt(m.session.Snapshot().Gap); ok {
			page = min(len(pages)-1, projected.Lines[line].Page-1)
		}
	}
	if action == "6" {
		m.print.screen, m.print.pages, m.print.page, m.print.top = printView, pages, page, 0
		return nil
	}
	if m.print.port == "" {
		return fmt.Errorf("Select a disk filename in Select Printer, Edit, Port, Other")
	}
	if action == "2" {
		pages = pages[page : page+1]
	}
	dir, name := m.runtime.workspaceRoot, m.print.port
	if i := strings.LastIndexByte(name, '\\'); i >= 0 {
		dir, err = dir.Navigate(name[:i+1])
		name = name[i+1:]
	} else if len(name) >= 2 && name[1] == ':' {
		dir, err = dir.Navigate(name[:2])
		name = name[2:]
	}
	if err != nil {
		return err
	}
	if err := dir.PrintToNewFile(name, layout.StandardPrint(pages)); err != nil {
		return err
	}
	m.print.screen = printClosed
	m.notice = "Printed to " + m.print.port
	return nil
}

func (m Model) printViewScreen() tea.View {
	p := m.print
	if !m.showEditorChrome() {
		return m.historicModalView([]string{"Print", "Enlarge the window to continue"}, "", "")
	}
	switch p.screen {
	case printView:
		lines := p.pages[p.page].TextLines()
		view := m.historicModalView(lines[p.top:], fmt.Sprintf("View Document   Page %d of %d", p.page+1, len(p.pages)), "")
		view.Cursor = nil
		return view
	case printSelect:
		return m.historicModalView([]string{"Print: Select Printer", "", "* Standard Printer"},
			"1 Select; 2 Additional Printers; 3 Edit; 4 Copy; 5 Delete; 6 Help; 7 Update: 1", p.notice)
	case printEdit, printPort, printFilename:
		port := p.port
		if port == "" {
			port = "LPT1:"
		}
		body := []string{"Select Printer: Edit", "", "         Filename                       STANPRIN.PRS", "",
			"     1 - Name                           Standard Printer", "", "     2 - Port                           " + port, "",
			"     3 - Sheet Feeder                   None", "", "     4 - Cartridges/Fonts/Print Wheels", "",
			"     5 - Initial Base Font              Courier 10cpi", "", "     6 - Path for Downloadable",
			"           Fonts and Printer", "           Command Files", "", "     7 - Print to Hardware Port         No"}
		footer := "Selection: 0"
		if p.screen == printPort {
			footer = "Port: 1 LPT 1; 2 LPT 2; 3 LPT 3; 4 COM 1; 5 COM 2; 6 COM 3; 7 COM 4; 8 Other: 0"
		} else if p.screen == printFilename {
			footer = "Device or Filename: " + p.draft
		}
		return m.historicModalView(body, footer, p.notice)
	default:
		return m.historicModalView([]string{"Print", "", "     1 - Full Document", "     2 - Page",
			"     3 - Document on Disk", "     4 - Control Printer", "     5 - Multiple Pages", "     6 - View Document",
			"     7 - Initialize Printer", "", "", "Options", "", "     S - Select Printer                 Standard Printer",
			"     B - Binding Offset                 0\"", "     N - Number of Copies               1",
			"     U - Multiple Copies Generated by   WordPerfect", "     G - Graphics Quality               Medium",
			"     T - Text Quality                   High"}, "Selection: 0", p.notice)
	}
}
