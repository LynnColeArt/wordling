package tui

import (
	"fmt"
	"math"
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
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
	printListedPages
	printDiskName
	printDiskPages
	printBinding
)

type printUI struct {
	screen              printScreen
	port, draft, notice string
	pages               []layout.StandardPage
	listed              *document.Document
	systemName, revised string
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
		case printDiskName, printDiskPages, printBinding:
			p.screen, p.listed, p.draft = printMenu, nil, ""
		default:
			p.screen, p.pages, p.listed = printClosed, nil, nil
		}
		p.notice = ""
		return m, nil
	}
	if !m.showEditorChrome() {
		return m, nil
	}
	p.notice = ""
	if p.screen == printBinding {
		switch key.Code {
		case tea.KeyEnter:
			inches, err := strconv.ParseFloat(strings.TrimSuffix(p.draft, "\""), 64)
			if p.draft == "" {
				p.screen = printMenu
				return m, nil
			}
			if err != nil || inches < 0 || inches > 1 {
				p.notice = "Enter a binding offset from 0 to 1 inch"
				return m, nil
			}
			next, err := m.session.SetBindingOffset(int(math.Round(inches * document.UnitsPerInch)))
			if err != nil {
				p.notice = err.Error()
				return m, nil
			}
			m.session, p.screen, p.draft = next, printMenu, ""
		case tea.KeyBackspace:
			if len(p.draft) != 0 {
				p.draft = p.draft[:len(p.draft)-1]
			}
		default:
			if len(p.draft)+len(key.Text) <= 12 && strings.Trim(key.Text, "0123456789.\"") == "" {
				p.draft += key.Text
			}
		}
		return m, nil
	}
	if p.screen == printListedPages || p.screen == printDiskPages {
		switch key.Code {
		case tea.KeyEnter:
			fromDisk := p.screen == printDiskPages
			if err := m.runPrint("listed"); err != nil {
				p.notice = err.Error()
			} else if fromDisk {
				p.screen = printMenu
			}
		case tea.KeyBackspace:
			if len(p.draft) != 0 {
				p.draft = p.draft[:len(p.draft)-1]
			}
		default:
			if key.Text != "" && strings.Trim(key.Text, "0123456789-, :ivxlcdmsIVXLCDMS") == "" && len(p.draft)+len(key.Text) <= 80 {
				p.draft += key.Text
			}
		}
		return m, nil
	}
	if p.screen == printFilename || p.screen == printDiskName {
		switch key.Code {
		case tea.KeyBackspace:
			if len(p.draft) != 0 {
				p.draft = p.draft[:len(p.draft)-1]
			}
		case tea.KeyEnter:
			if p.draft != "" {
				if p.screen == printDiskName {
					name, directory := p.draft, m.runtime.workspaceRoot
					var err error
					if i := strings.LastIndexAny(name, `\:`); i >= 0 {
						directory, err = directory.Navigate(name[:i+1])
						name = name[i+1:]
					}
					if err == nil {
						target, observeErr := directory.Observe(name)
						err = observeErr
						if err == nil {
							raw, readErr := directory.ReadDOSBytes(name)
							err = readErr
							if err == nil {
								p.listed, err = document.Parse(raw)
							}
							if stamp, ok := target.Identity(); ok {
								p.revised = fileStamp(stamp.Modified)
							}
							p.systemName = filePath(directory, strings.ToUpper(name))
						}
					}
					if err != nil {
						p.notice = err.Error()
						return m, nil
					}
					p.screen, p.draft = printDiskPages, ""
				} else {
					p.port, p.screen = p.draft, printEdit
				}
			}
		default:
			draft := fileBrowser{draft: p.draft, touched: true}
			draft.addDraft(strings.ToUpper(key.Text))
			if len(draft.draft) <= 80 {
				p.draft = draft.draft
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
		case "3":
			p.screen, p.draft = printDiskName, ""
		case "b":
			p.screen, p.draft = printBinding, ""
		case "4", "5", "7", "n", "u", "g", "t":
			p.notice = "This print option is not yet implemented"
		}
	}
	return m, nil
}

func (m *Model) runPrint(action string) error {
	doc := m.session.Document()
	if m.print.listed != nil {
		doc = m.print.listed
	}
	settings := editor.EverydaySettings()
	settings.Date = m.runtime.now()
	spec := strings.TrimSpace(strings.ToLower(m.print.draft))
	summaryOnly := action == "listed" && spec == "s"
	var pages []layout.StandardPage
	var err error
	if !summaryOnly {
		pages, err = layout.StandardPages(doc, settings)
		if err != nil {
			return err
		}
	}
	page := 0
	if m.print.listed == nil && m.everyday.ready && m.everyday.revision == m.session.Snapshot().NativeRevision {
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
	if action == "listed" {
		// Both DOS disk print entry points print the Summary only for a
		// standalone s. With a page selection DOS prints the body pages.
		withSummary := summaryOnly
		if !summaryOnly && spec != "s-" {
			pages, err = selectPrintPages(pages, strings.TrimPrefix(spec, "s,"))
			if err != nil {
				return err
			}
		}
		if withSummary {
			summary, ok, err := doc.Summary()
			if err != nil {
				return err
			}
			if !ok && summaryOnly {
				return fmt.Errorf("Document has no Summary")
			}
			if ok {
				page := layout.StandardSummary(summary, m.print.systemName, m.print.revised)
				pages = append([]layout.StandardPage{page}, pages...)
			}
		}
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
	m.print.screen, m.print.listed = printClosed, nil
	m.notice = "Printed to " + m.print.port
	return nil
}

func selectPrintPages(pages []layout.StandardPage, input string) ([]layout.StandardPage, error) {
	if strings.TrimSpace(input) == "" {
		return pages, nil
	}
	var result []layout.StandardPage
	lastPrinted := 0
	fields := strings.FieldsFunc(input, func(r rune) bool { return r == ' ' || r == ',' })
	for _, item := range fields {
		start, end, ranged := strings.Cut(item, "-")
		first, last := 1, len(pages)
		if start != "" {
			first = findPrintPage(pages, start, "", lastPrinted)
			if first == 0 {
				if findPrintPage(pages, start, "", 0) != 0 {
					continue
				}
				return nil, fmt.Errorf("Invalid page selection %q", item)
			}
		}
		if !ranged {
			last = first
		} else if end != "" {
			inherited, _, _ := strings.Cut(start, ":")
			if !strings.Contains(start, ":") {
				inherited = ""
			}
			last = findPrintPage(pages, end, inherited, first-1)
		}
		if last < first {
			return nil, fmt.Errorf("Invalid page selection %q", item)
		}

		// DOS scans forward through the document. Requests for pages already
		// passed do not restart the print job.
		if last > lastPrinted {
			first = max(first, lastPrinted+1)
			result = append(result, pages[first-1:last]...)
			lastPrinted = last
		}
	}
	if len(result) == 0 {
		return nil, fmt.Errorf("Enter at least one page")
	}
	return result, nil
}

func findPrintPage(pages []layout.StandardPage, target, inherited string, after int) int {
	sectionText, label, qualified := strings.Cut(target, ":")
	if !qualified {
		sectionText, label = inherited, target
	}
	section := 0
	if sectionText != "" {
		var err error
		section, err = strconv.Atoi(sectionText)
		if err != nil || section < 1 {
			return 0
		}
	}
	number, err := strconv.Atoi(label)
	roman := err != nil
	if roman {
		number = 0
		previous := 0
		for i := len(label) - 1; i >= 0; i-- {
			value := map[byte]int{'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}[label[i]]
			if value == 0 {
				return 0
			}
			if value < previous {
				number -= value
			} else {
				number += value
				previous = value
			}
		}
	}
	for i := after; i < len(pages); i++ {
		page := pages[i]
		if page.Number == number && page.Roman == roman && (section == 0 || page.Section == section) {
			return i + 1
		}
	}
	return 0
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
		footer := "Selection: 0"
		binding := printedInches(float64(m.session.Document().BindingOffset()) / document.UnitsPerInch)
		if p.screen == printBinding {
			footer = "Selection: b"
			if p.draft != "" {
				binding = p.draft
			}
		}
		if p.screen == printDiskName {
			footer = "Document name: " + p.draft
		} else if p.screen == printDiskPages {
			footer = "Page(s): " + p.draft
			if p.draft == "" {
				footer += "(All)"
			}
		}
		return m.historicModalView([]string{"Print", "", "     1 - Full Document", "     2 - Page",
			"     3 - Document on Disk", "     4 - Control Printer", "     5 - Multiple Pages", "     6 - View Document",
			"     7 - Initialize Printer", "", "", "Options", "", "     S - Select Printer                 Standard Printer",
			"     B - Binding Offset                 " + binding, "     N - Number of Copies               1",
			"     U - Multiple Copies Generated by   WordPerfect", "     G - Graphics Quality               Medium",
			"     T - Text Quality                   High"}, footer, p.notice)
	}
}

func (m Model) printListedFile() (tea.Model, tea.Cmd) {
	b := &m.historic.browser
	if b.selected < 2 {
		return m, nil
	}
	selection, err := b.list.Select(b.selected - 2)
	if err != nil {
		b.message = err.Error()
		return m, nil
	}
	stored, err := selection.Read()
	if err != nil {
		b.message = err.Error()
		return m, nil
	}
	doc, err := document.Parse(stored.Export())
	if err != nil {
		b.message = err.Error()
		return m, nil
	}
	m.print.listed = doc
	entry := selection.Entry()
	m.print.systemName, m.print.revised = filePath(b.directory, entry.DOSName), fileStamp(entry.Modified)
	if m.print.port != "" {
		m.print.screen, m.print.draft, m.print.notice = printListedPages, "", ""
	} else {
		m.print.screen = printMenu
	}
	return m, nil
}
