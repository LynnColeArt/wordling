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
)

type formatScreen uint8

const (
	formatClosed formatScreen = iota
	formatMenu
	formatLine
	formatOther
	formatLeft
	formatRight
	formatPage
	formatTop
	formatBottom
	formatSpacing
	formatChooseHeight
	formatFixedHeight
	formatJustification
	formatPageTextSlot
	formatPageTextScope
	formatPageTextEdit
	formatLineNumbering
	formatConditionalPage
	formatWidowProtection
	formatTabSet
	formatLanguage
	formatPageNumbering
	formatPageNumberPosition
	formatPageSuppress
	formatPageSuppressNumber
	formatDocument
	formatInitialCodes
	formatInitialFormat
	formatInitialLine
	formatInitialSpacing
	formatPrinterFunctions
	formatPrinterCommand
	formatPrinterLiteral
	formatKerning
)

type lineFormatUI struct {
	screen        formatScreen
	left, right   int
	spacing       int
	height        int
	justification document.Justification
	draft, error  string
	pageText      document.PageText
	numbered      bool
	widow         bool
	tabs          tabSetUI
}

func (m Model) openLineFormat(screen formatScreen) Model {
	m.closeMenus()
	left, right := m.session.LineMargins()
	if screen == formatPage {
		left, right = m.session.PageMargins()
	}
	m.lineFormat = lineFormatUI{screen: screen, left: left, right: right, spacing: m.session.LineSpacing(),
		height: m.session.LineHeight(), justification: m.session.Justification(),
		numbered: m.session.LineNumbering(), widow: m.session.WidowProtection()}
	return m
}

func (m Model) lineFormatPress(key input.Key) (tea.Model, tea.Cmd) {
	form := &m.lineFormat
	if form.screen == formatTabSet {
		return m.tabSetPress(key), nil
	}
	if key.IsRepeat || key.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	if form.screen >= formatPrinterFunctions {
		return m.printerFunctionsPress(key), nil
	}
	if form.screen >= formatDocument && form.screen <= formatInitialSpacing {
		return m.initialCodesPress(key), nil
	}
	if form.screen >= formatPageNumbering && form.screen <= formatPageSuppressNumber {
		return m.pageNumberPress(key), nil
	}
	switch key.Code {
	case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
		if form.screen == formatLanguage {
			m = m.openLineFormat(formatOther)
		} else if form.screen == formatTop || form.screen == formatBottom {
			m = m.openLineFormat(formatPage)
		} else if form.screen == formatPageTextEdit && key.Code == tea.KeyF7 {
			record := form.pageText
			record.Text = form.draft
			next, err := m.session.CreatePageText(record)
			if err != nil {
				form.error = err.Error()
				return m, nil
			}
			m.session = next
			m = m.openLineFormat(formatPage)
		} else if form.screen == formatPageTextSlot || form.screen == formatPageTextScope || form.screen == formatPageTextEdit {
			m = m.openLineFormat(formatPage)
		} else if form.screen == formatConditionalPage {
			m = m.openLineFormat(formatOther)
		} else if form.screen == formatLeft || form.screen == formatRight || form.screen == formatSpacing ||
			form.screen == formatChooseHeight || form.screen == formatFixedHeight || form.screen == formatJustification ||
			form.screen == formatLineNumbering || form.screen == formatWidowProtection {
			m = m.openLineFormat(formatLine)
		} else {
			m.lineFormat = lineFormatUI{}
		}
		return m, nil
	}
	form.error = ""
	switch form.screen {
	case formatMenu:
		switch key.Code {
		case '1':
			form.screen = formatLine
		case '2':
			m = m.openLineFormat(formatPage)
		case '3':
			form.screen = formatDocument
		case '4':
			form.screen = formatOther
		}
	case formatLine:
		if key.Code == '7' {
			form.screen = formatLeft
		} else if key.Code == '6' {
			form.screen = formatSpacing
		} else if key.Code == '4' {
			form.screen = formatChooseHeight
		} else if key.Code == '3' {
			form.screen = formatJustification
		} else if key.Code == '5' {
			form.screen = formatLineNumbering
		} else if key.Code == '8' {
			return m.openTabSet(), nil
		} else if key.Code == '9' {
			form.screen = formatWidowProtection
		}
	case formatLineNumbering, formatWidowProtection:
		switch key.Code {
		case 'y', 'Y', 'n', 'N', tea.KeyEnter:
			current, set := form.numbered, m.session.SetLineNumbering
			if form.screen == formatWidowProtection {
				current, set = form.widow, m.session.SetWidowProtection
			}
			enabled := key.Code == 'y' || key.Code == 'Y' || key.Code == tea.KeyEnter && current
			next, err := set(enabled)
			if err != nil {
				form.error = err.Error()
				return m, nil
			}
			m.session = next
			m = m.openLineFormat(formatLine)
		}
	case formatJustification:
		if key.Code == '1' {
			m = m.setJustification(document.JustifyLeft, formatLine)
		} else if key.Code == '4' {
			m = m.setJustification(document.JustifyFull, formatLine)
		} else if key.Code == '2' {
			m = m.setJustification(document.JustifyCenter, formatLine)
		} else if key.Code == '3' {
			m = m.setJustification(document.JustifyRight, formatLine)
		}
	case formatChooseHeight:
		if key.Code == '1' {
			return m.commitLineHeight(0), nil
		}
		if key.Code == '2' {
			form.screen = formatFixedHeight
		}
	case formatFixedHeight:
		switch key.Code {
		case tea.KeyEnter:
			if form.draft == "" {
				return m.commitLineHeight(max(200, form.height)), nil
			}
			inches, err := strconv.ParseFloat(strings.TrimSuffix(form.draft, "\""), 64)
			if err != nil || inches <= 0 || inches > 10 {
				form.error = "Enter a positive line height in inches"
				return m, nil
			}
			return m.commitLineHeight(int(math.Round(inches * document.UnitsPerInch))), nil
		case tea.KeyBackspace:
			if n := len(form.draft); n > 0 {
				form.draft = form.draft[:n-1]
			}
		default:
			if len(form.draft)+len(key.Text) <= 12 && strings.Trim(key.Text, "0123456789.\"") == "" {
				form.draft += key.Text
			}
		}
	case formatSpacing:
		if key.Code >= '1' && key.Code <= '9' {
			form.spacing = int(key.Code - '0')
		} else if key.Code == tea.KeyEnter {
			next, err := m.session.SetLineSpacing(form.spacing)
			if err != nil {
				form.error = err.Error()
				return m, nil
			}
			m.session = next
			m = m.openLineFormat(formatLine)
		}
	case formatPage:
		if key.Code == '6' {
			form.screen = formatPageNumbering
		} else if key.Code == '8' {
			form.screen = formatPageSuppress
		}
		if key.Code == '5' {
			form.screen = formatTop
		}
		if key.Code == '3' || key.Code == '4' {
			form.screen = formatPageTextSlot
			if key.Code == '4' {
				form.pageText.Slot = 2
			}
		}
	case formatPageTextSlot:
		if key.Code == '1' || key.Code == '2' {
			form.pageText.Slot += int(key.Code - '1')
			form.screen = formatPageTextScope
		}
	case formatPageTextScope:
		if key.Code == '1' {
			next, err := m.session.CreatePageText(form.pageText)
			if err != nil {
				form.error = err.Error()
				return m, nil
			}
			m.session = next
			m = m.openLineFormat(formatPage)
		} else if key.Code >= '2' && key.Code <= '4' {
			form.pageText.Pages = 1 << (key.Code - '2')
			form.screen = formatPageTextEdit
		}
	case formatPageTextEdit:
		if key.Code == tea.KeyBackspace && len(form.draft) > 0 {
			form.draft = form.draft[:len(form.draft)-1]
		} else if len(form.draft)+len(key.Text) <= 60 && strings.IndexFunc(key.Text, func(r rune) bool {
			return r < 32 || r > 126
		}) == -1 {
			form.draft += key.Text
		}
	case formatOther:
		if key.Code == '4' {
			form.screen, form.draft = formatLanguage, ""
		} else if key.Code == '6' {
			form.screen = formatPrinterFunctions
		} else if key.Code == '2' {
			form.screen = formatConditionalPage
		} else if key.Code == '9' {
			m.lineFormat = lineFormatUI{}
			return m.reduce(editor.Event{Command: editor.EndCentering})
		}
	case formatLanguage:
		switch key.Code {
		case tea.KeyBackspace:
			if len(form.draft) > 0 {
				form.draft = form.draft[:len(form.draft)-1]
			}
		case tea.KeyEnter:
			next, err := m.session.SetLanguage(form.draft)
			if err != nil {
				form.error = err.Error()
			} else {
				m.session = next
				m = m.openLineFormat(formatOther)
			}
		default:
			text := strings.ToUpper(key.Text)
			if len(text)+len(form.draft) <= 2 && strings.Trim(text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") == "" {
				form.draft += text
			}
		}
	case formatConditionalPage:
		switch key.Code {
		case tea.KeyEnter:
			value, err := strconv.Atoi(form.draft)
			if err != nil || value < 1 || value > 255 {
				form.error = "Enter a line count from 1 to 255"
				return m, nil
			}
			next, err := m.session.InsertConditionalPage(value)
			if err != nil {
				form.error = err.Error()
				return m, nil
			}
			m.session = next
			m = m.openLineFormat(formatOther)
		case tea.KeyBackspace:
			if n := len(form.draft); n > 0 {
				form.draft = form.draft[:n-1]
			}
		default:
			if len(form.draft)+len(key.Text) <= 3 && strings.Trim(key.Text, "0123456789") == "" {
				form.draft += key.Text
			}
		}
	case formatLeft, formatRight, formatTop, formatBottom:
		page := form.screen == formatTop || form.screen == formatBottom
		second := form.screen == formatRight || form.screen == formatBottom
		switch key.Code {
		case tea.KeyBackspace:
			if n := len(form.draft); n > 0 {
				form.draft = form.draft[:n-1]
			}
		case tea.KeyEnter:
			current := form.left
			if second {
				current = form.right
			}
			if form.draft != "" {
				inches, err := strconv.ParseFloat(strings.TrimSuffix(form.draft, "\""), 64)
				if err != nil || inches < 0 || inches > 11 {
					form.error = "Enter a margin in inches"
					return m, nil
				}
				current = int(math.Round(inches * document.UnitsPerInch))
			}
			if !second {
				form.left, form.screen, form.draft = current, form.screen+1, ""
			} else {
				screen, set := formatLine, m.session.SetLineMargins
				if page {
					screen, set = formatPage, m.session.SetPageMargins
				}
				next, err := set(form.left, current)
				if err != nil {
					form.error = err.Error()
					return m, nil
				}
				m.session = next
				m = m.openLineFormat(screen)
			}
		default:
			if len(form.draft)+len(key.Text) <= 12 && strings.Trim(key.Text, "0123456789.\"") == "" {
				form.draft += key.Text
			}
		}
	}
	return m, nil
}

func (m Model) setJustification(value document.Justification, returnTo formatScreen) Model {
	next, err := m.session.SetJustification(value)
	if err != nil {
		if returnTo == formatClosed {
			m.notice = err.Error()
		} else {
			m.lineFormat.error = err.Error()
		}
		return m
	}
	m.session = next
	if returnTo != formatClosed {
		return m.openLineFormat(returnTo)
	}
	return m
}

func (m Model) commitLineHeight(height int) Model {
	next, err := m.session.SetLineHeight(height)
	if err != nil {
		m.lineFormat.error = err.Error()
		return m
	}
	m.session = next
	return m.openLineFormat(formatLine)
}

func (m Model) lineFormatView() tea.View {
	form := m.lineFormat
	if form.screen >= formatDocument && form.screen <= formatInitialSpacing && form.screen != formatInitialLine && form.screen != formatInitialSpacing {
		return m.initialCodesView()
	}
	switch form.screen {
	case formatPrinterFunctions, formatPrinterCommand, formatPrinterLiteral, formatKerning:
		return m.printerFunctionsView()
	case formatPageNumbering, formatPageNumberPosition, formatPageSuppress, formatPageSuppressNumber:
		return m.pageNumberView()
	case formatTabSet:
		return m.tabSetView()
	case formatMenu:
		return m.historicModalView([]string{"Format: 1 Line; 2 Page; 3 Document; 4 Other"}, "Selection: 0", "")
	case formatOther, formatConditionalPage, formatLanguage:
		footer := "Selection: 0"
		language := m.session.Language()
		if form.screen == formatLanguage {
			footer = "Selection: 4"
			if form.draft != "" {
				language = form.draft
			}
		}
		if form.screen == formatConditionalPage {
			footer = "Number of Lines to Keep Together: " + form.draft
		}
		return m.historicModalView([]string{"Format: Other", "", "     1 - Advance", "",
			"     2 - Conditional End of Page", "",
			"     3 - Decimal/Align Character       .", "         Thousands' Separator        ,", "",
			"     4 - Language                     " + language, "",
			"     5 - Overstrike", "", "     6 - Printer Functions", "",
			"     7 - Underline - Spaces           Yes", "                    Tabs             No", "",
			"     8 - Border Options", "", "     9 - End Centering/Alignment"}, footer, form.error)
	case formatPageTextEdit:
		view := m.historicModalView([]string{form.draft}, form.pageText.Label()+":  Press Exit when done", form.error)
		view.Cursor = tea.NewCursor(min(m.width-1, len(form.draft)), 0)
		return view
	default:
		left := printedInches(float64(form.left) / document.UnitsPerInch)
		right := printedInches(float64(form.right) / document.UnitsPerInch)
		footer := "Selection: 0"
		page := form.screen == formatPage || form.screen == formatTop || form.screen == formatBottom ||
			form.screen == formatPageTextSlot || form.screen == formatPageTextScope
		entry := form.screen == formatLeft || form.screen == formatRight || form.screen == formatTop || form.screen == formatBottom
		second := form.screen == formatRight || form.screen == formatBottom
		if entry {
			footer = "Selection: 7"
			if page {
				footer = "Selection: 5"
			}
			if form.draft != "" {
				if second {
					right = form.draft
				} else {
					left = form.draft
				}
			}
		}
		if form.screen == formatSpacing || form.screen == formatInitialSpacing {
			footer = "Selection: 6"
		}
		numbered := "No"
		if form.numbered {
			numbered = "Yes"
		}
		if form.screen == formatLineNumbering {
			footer = "Selection: 5"
			if form.numbered {
				numbered = "Yes (No)"
			} else {
				numbered = "No (Yes)"
			}
		}
		widow := "No"
		if form.widow {
			widow = "Yes"
		}
		if form.screen == formatWidowProtection {
			footer = "Selection: 9"
			if form.widow {
				widow = "Yes (No)"
			} else {
				widow = "No (Yes)"
			}
		}
		if form.screen == formatJustification {
			footer = "Justification: 1 Left; 2 Center; 3 Right; 4 Full: 0"
		}
		if form.screen == formatPageTextSlot {
			footer = "1 Header A; 2 Header B: 0"
			if form.pageText.Footer() {
				footer = "1 Footer A; 2 Footer B: 0"
			}
		} else if form.screen == formatPageTextScope {
			footer = "1 Discontinue; 2 Every Page; 3 Odd Pages; 4 Even Pages; 5 Edit: 0"
		}
		height := "Auto"
		if form.height != 0 || form.screen == formatFixedHeight {
			value := form.height
			if value == 0 {
				value = 200
			}
			height = strconv.FormatFloat(float64(value)/document.UnitsPerInch, 'f', 3, 64)
			height = strings.TrimRight(strings.TrimRight(height, "0"), ".") + "\""
		}
		if form.screen == formatChooseHeight || form.screen == formatFixedHeight {
			footer = "1 Auto; 2 Fixed: 0"
			if form.screen == formatFixedHeight {
				footer = "1 Auto; 2 Fixed: 2"
				if form.draft != "" {
					height = form.draft
				}
			}
		}
		body := []string{"Format: Line", "", "     1 - Hyphenation                    No", "",
			"     2 - Hyphenation Zone - Left        10%", "                            Right       4%", "",
			"     3 - Justification                  " + form.justification.String(), "", "     4 - Line Height                    " + height, "",
			"     5 - Line Numbering                 " + numbered, "", fmt.Sprintf("     6 - Line Spacing                   %d", form.spacing), "",
			fmt.Sprintf("     7 - Margins - Left                 %s", left),
			fmt.Sprintf("                   Right                %s", right), "",
			"     8 - Tab Set                        Rel; -1\", every 0.5\"", "",
			"     9 - Widow/Orphan Protection        " + widow}
		row := 15
		if page {
			body = []string{"Format: Page", "", "     1 - Center Page (top to bottom)    No", "",
				"     2 - Force Odd/Even Page", "", "     3 - Headers", "", "     4 - Footers", "",
				fmt.Sprintf("     5 - Margins - Top                  %s", left),
				fmt.Sprintf("                   Bottom               %s", right), "", "     6 - Page Numbering", "",
				"     7 - Paper Size                     8.5\" x 11\"", "         Type                           Standard", "",
				"     8 - Suppress (this page only)"}
			row = 10
		}
		view := m.historicModalView(body, footer, form.error)
		if entry {
			if second {
				row++
			}
			view.Cursor = tea.NewCursor(min(m.width-1, 40+len(form.draft)), min(m.height-1, row))
		}
		if form.screen == formatFixedHeight {
			view.Cursor = tea.NewCursor(min(m.width-1, 40+len(form.draft)), min(m.height-1, 9))
		}
		return view
	}
}
