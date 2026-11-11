package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type historicUI struct {
	bar          bool // Visibility is independent of keyboard focus.
	sub          string
	drawnSub     string
	titleActive  bool
	parent       int
	menu         bool
	drop         bool
	column, item int
	files        bool
	browser      fileBrowser
	message      string
}

func (m Model) menuAvailable() bool {
	s := m.session.Snapshot()
	return s.Mode == editor.Editing && len(m.unsettled) == 0 && m.firstPending == nil &&
		m.macro == nil && m.reconcile == "" && !m.characterRepeat.active && !m.repeatEntry
}

func (m Model) historicPress(k input.Key) (tea.Model, tea.Cmd, bool) {
	s := m.session.Snapshot()
	if m.historic.files {
		next, cmd := m.filePress(k)
		return next, cmd, true
	}
	if s.Mode == editor.RetrieveName && k.Code == tea.KeyF5 && k.Mod == 0 {
		return m.openFiles(), nil, true
	}
	if !m.menuAvailable() {
		return m, nil, false
	}
	if k.IsRepeat && m.historic.menu {
		return m, nil, true
	}
	if menuKey(k) {
		if m.historic.menu {
			m.closeMenus()
		} else {
			m.historic.menu = true
		}
		return m, nil, true
	}
	if k.Code == tea.KeyF3 && k.Mod == 0 {
		m.closeMenus()
		return m.openHelp(false), nil, true
	}
	if k.Code == tea.KeyF1 && k.Mod == tea.ModShift {
		m.closeMenus()
		return m.openSetup(setupRoot), nil, true
	}
	if k.Code == tea.KeyF5 && k.Mod == 0 {
		m.closeMenus()
		return m.openFiles(), nil, true
	}
	if !m.historic.menu {
		d := m.session.Document()
		if d != nil && s.HomePrefix == 0 && !s.Selection && k.Mod == 0 {
			atStart := s.Gap == 0 && (k.Code == tea.KeyLeft || k.Code == tea.KeyBackspace)
			atEnd := s.Gap == d.TokenCount() && (k.Code == tea.KeyRight || k.Code == tea.KeyDelete)
			if atStart || atEnd {
				m.notice = ""
				return m, nil, true
			}
		}
		return m, nil, false
	}
	if k.Mod == 0 {
		switch k.Code {
		case tea.KeyF7:
			m.closeMenus()
			return m, nil, true
		case tea.KeyF1, tea.KeyEscape, ' ':
			if m.historic.sub != "" {
				m.backToParent()
			} else if k.Code == tea.KeyF1 && m.historic.drop {
				m.historic.drop, m.historic.drawnSub = false, ""
			} else {
				m.closeMenus()
			}
			return m, nil, true
		case tea.KeyLeft, tea.KeyRight:
			if m.historic.sub != "" {
				if k.Code == tea.KeyLeft {
					m.backToParent()
				}
				return m, nil, true
			}
			if k.Code == tea.KeyRight && m.historic.drop {
				parent := historicMenus[m.historic.column]
				if m.openSubmenu(parent.label + "/" + parent.items[m.historic.item].label) {
					return m, nil, true
				}
			}
			step := 1
			if k.Code == tea.KeyLeft {
				step = len(historicMenus) - 1
			}
			m.openMenu((m.historic.column + step) % len(historicMenus))
			return m, nil, true
		case tea.KeyUp, tea.KeyDown:
			if !m.historic.drop {
				m.openMenu(m.historic.column)
				return m, nil, true
			}
			items := m.activeItems()
			step := 1
			if k.Code == tea.KeyUp {
				step = len(items) - 1
			}
			for range items {
				m.historic.item = (m.historic.item + step) % len(items)
				if items[m.historic.item].label != "" && (!items[m.historic.item].needsBlock || s.Selection) {
					break
				}
			}
			if m.historic.sub == "" && m.historic.drawnSub != "" {
				m.historic.drawnSub = ""
				parent := historicMenus[m.historic.column]
				m.openSubmenu(parent.label + "/" + parent.items[m.historic.item].label)
			}
			return m, nil, true
		case tea.KeyEnter:
			if !m.historic.drop {
				m.openMenu(m.historic.column)
				return m, nil, true
			}
			next, cmd := m.activateMenu()
			return next, cmd, true
		}
	}
	if k.Code >= tea.KeyF1 && k.Code <= tea.KeyF12 {
		if _, supported := resolve(k, editor.Editing); supported || k.Code == tea.KeyF6 && k.Mod == 0 {
			m.closeMenus()
			next, cmd := m.update(tea.KeyPressMsg(tea.Key{Code: k.Code, Mod: k.Mod, Text: k.Text}))
			return next, cmd, true
		}
	}
	if len(k.Text) != 1 || k.Mod&^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil, true
	}
	letter := strings.ToLower(k.Text)
	if !m.historic.drop {
		for i, menu := range historicMenus {
			if strings.ToLower(menu.label[menu.mnemonic:menu.mnemonic+1]) == letter {
				m.openMenu(i)
				break
			}
		}
		return m, nil, true
	}
	for i, item := range m.activeItems() {
		cells := []rune(item.cells)
		if item.label != "" && item.mnemonic < len(cells) && strings.ToLower(string(cells[item.mnemonic])) == letter {
			if !m.menuItemVisible(i) {
				return m, nil, true
			}
			m.historic.item = i
			next, cmd := m.activateMenu()
			return next, cmd, true
		}
	}
	return m, nil, true
}

func (m Model) historicView() tea.View {
	if m.setup.page != setupClosed {
		return m.setupView()
	}
	if m.help.active {
		return m.helpView()
	}
	lines := make([]string, m.height)
	frame := m.visibleFrame()
	s := m.session.Snapshot()
	bar := m.historic.bar && m.height >= 3
	reveal := s.Reveal && m.height >= 8
	top := 0
	if bar {
		top = 1
	}
	bottom := max(top, m.height-1)
	if reveal {
		bottom = max(top, m.height/2-1)
	}
	body := strings.Split(frame.normal, "\n")
	row := max(0, frame.y)
	start := max(0, row-max(1, bottom-top)+1)
	var projected everydayFrame
	useProjection := false
	if !m.macroStatus.DisplaySuppressed && s.Mode == editor.HistoryPreview {
		if p, err := m.paintEverydayPreview(bottom-top, max(0, m.height-bottom-4)); err == nil {
			projected, useProjection = p, true
			body, row, frame.x, start = p.normal, p.row, p.column, 0
		}
	} else if !m.macroStatus.DisplaySuppressed && m.everyday.ready && m.everyday.revision == s.NativeRevision && s.Screen >= 1 && s.Screen <= 2 {
		if d := m.session.Document(); d != nil {
			first, last := -1, -1
			if s.Selection {
				first, last = s.SelectionStart, s.SelectionEnd
			}
			if p, err := paintEveryday(d, nil, m.everyday.layout, m.everyday.visualRows, s.Gap, reveal, first, last, m.width, m.everyday.top[s.Screen-1], bottom-top, max(0, m.height-bottom-4)); err == nil {
				projected = p
				useProjection = true
				body, row, frame.x = p.normal, p.row, p.column
				start = 0
			}
		}
	}
	for i := start; i < len(body) && top+i-start < bottom; i++ {
		lines[top+i-start] = clip(body[i], m.width)
	}
	if frame.err != nil && !useProjection {
		lines[top] = "Unsupported document presentation"
	}
	if reveal {
		lines[min(m.height-1, bottom+1)] = everydayRuler(m.width, editor.EverydaySettings())
		if bottom+2 < m.height {
			if useProjection {
				for i := start; i < len(projected.codes) && bottom+2+i-start < m.height-1; i++ {
					lines[bottom+2+i-start] = projected.codes[i]
				}
			} else {
				lines[bottom+2] = clip(frame.reveal, m.width)
			}
		}
	}
	// Printed geometry requires a qualified layout engine. Unknown values must
	// not be synthesized from terminal wrapping or native token counts.
	status := fmt.Sprintf("Doc %d Pg -- Ln -- Pos", s.Screen)
	statusValue := " --"
	if position, err := m.session.EverydayPosition(); err == nil {
		page, line, column := "--", "--", "--"
		pageOK, lineOK, columnOK := position.Qualified()
		if pageOK {
			page = fmt.Sprint(position.Page)
		}
		ln, pos := position.Printed()
		if lineOK {
			line = printedInches(ln)
		}
		if columnOK {
			column = printedInches(pos)
		}
		status = fmt.Sprintf("Doc %d Pg %s Ln %s Pos", s.Screen, page, line)
		statusValue = " " + column
	}
	statusLeft := max(0, m.width-8-len(status))
	statusName := clip(s.Name, max(0, statusLeft-1))
	lines[bottom] = revealCode + statusName + screenReset + strings.Repeat(" ", max(0, statusLeft-ansi.StringWidth(statusName))) + revealCode + status + screenReset + statusValue
	prompt := s.Prompt
	if m.characterRepeat.active {
		prompt = "Repeat Value = "
		if m.characterRepeat.count != 0 {
			prompt += fmt.Sprint(m.characterRepeat.count)
		}
	} else if m.repeatEntry {
		prompt = "Repeat Value = "
	} else if s.Mode == editor.Editing && s.MacroRepeat == 3 {
		prompt = "Repeat Value = 3"
	}
	if s.HomePrefix > 0 {
		prompt = "Home prefix: Home again for line/document movement, Esc cancels"
	}
	if reveal && prompt == "" {
		prompt = "Press " + revealCode + "Reveal Codes" + screenReset + " to restore screen"
	}
	promptRow := m.height - 1
	searching := s.Mode == editor.SearchForwardMode || s.Mode == editor.SearchBackwardMode
	searchPrefix := "-> Srch: "
	if searching {
		if s.Mode == editor.SearchBackwardMode {
			searchPrefix = "<- Srch: "
		}
		prompt = revealCode + searchPrefix + screenReset + s.Draft
		if reveal {
			promptRow = bottom
		}
	}
	if prompt != "" {
		lines[promptRow] = prompt
	}
	notice := s.Notice
	if notice == "NOT FOUND" {
		notice = ""
	}
	if s.NewPhase != editor.NewUnpublished {
		if state := firstStateLine(s); state != "" {
			notice = state
		}
	}
	if macro := m.macroLine(); macro != "" {
		notice = macro
	}
	if m.notice != "" {
		notice = m.notice
	}
	if m.reconcile != "" {
		notice = m.reconcile
	}
	if m.historic.message != "" {
		notice = m.historic.message
	}
	if notice != "" {
		lines[max(0, m.height-2)] = notice
	}
	if m.searchNotice != nil {
		lines[bottom] = revealCode + "* Not found *" + screenReset
	}
	m.paintMenus(lines)
	if m.historic.files {
		lines = m.fileLines(lines)
	}
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	applyEditorChrome(&v)
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	if m.historic.files {
		v.Cursor = m.fileCursor()
	}
	if !m.historic.menu && !m.historic.files {
		v.Cursor = tea.NewCursor(max(0, min(frame.x, m.width-1)), max(0, min(bottom-1, top+row-start)))
		if s.Mode == editor.SaveName || s.Mode == editor.RetrieveName || s.Mode == editor.MacroName || searching {
			prefix := s.Prompt
			if searching {
				prefix = searchPrefix
			} else if s.Draft != "" {
				if i := strings.Index(prefix, s.Draft); i >= 0 {
					prefix = prefix[:i]
				}
			} else if s.Mode == editor.RetrieveName {
				prefix = strings.TrimSuffix(prefix, " (List Files)")
			}
			v.Cursor = tea.NewCursor(min(m.width-1, ansi.StringWidth(prefix)+s.Caret), promptRow)
		}
	}
	return v
}
func printedInches(value float64) string {
	return strings.TrimRight(strings.TrimRight(fmt.Sprintf("%.2f", value), "0"), ".") + `"`
}
