package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/storage"
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
	dosTextStage uint8
	dosTextSoft  bool
	dosTextName  string
	dosTextSave  *storage.DOSTextSave
}

func (m Model) menuAvailable() bool {
	s := m.session.Snapshot()
	return s.Mode == editor.Editing && m.session.ProofStatus().Phase == editor.ProofInactive && len(m.unsettled) == 0 && m.firstPending == nil &&
		m.macro == nil && m.recording.stage == 0 && m.reconcile == "" && !m.characterRepeat.active && !m.repeatEntry
}

func mergeFilename(mode editor.Mode) bool {
	return mode == editor.MergePrimaryName || mode == editor.MergeSecondaryName
}

func (m Model) historicPress(k input.Key) (tea.Model, tea.Cmd, bool) {
	s := m.session.Snapshot()
	if m.historic.dosTextStage != 0 {
		next, cmd := m.dosTextPress(k)
		return next, cmd, true
	}
	if m.historic.files {
		next, cmd := m.filePress(k)
		return next, cmd, true
	}
	if (s.Mode == editor.RetrieveName || mergeFilename(s.Mode)) && k.Code == tea.KeyF5 && k.Mod == 0 {
		return m.openFiles(), nil, true
	}
	if s.Mode == editor.MergeMenuMode && k.Code == '2' && k.Mod == 0 && !k.IsRepeat && m.runtime.workspaceRoot != nil {
		next, cmd := m.openSort()
		return next, cmd, true
	}
	if !m.menuAvailable() {
		return m, nil, false
	}
	if k.IsRepeat && m.historic.menu {
		return m, nil, true
	}
	// A plain Escape can focus the visible bar when the terminal
	// reserves Alt+= or the user cannot send function keys.
	menuEscape := !m.historic.menu && m.historic.bar && k.Code == tea.KeyEscape &&
		k.Mod == 0 && !k.IsRepeat && s.HomePrefix == 0 && !s.Selection
	if menuEscape {
		if next, ok := m.beginCharacterRepeat(k); ok {
			return next, nil, true
		}
	}
	altPlus := k.Code == '+' && (k.Mod == tea.ModAlt || k.Mod == tea.ModAlt|tea.ModShift) &&
		!k.IsRepeat && (k.Text == "" || k.Text == "+")
	if menuKey(k) || altPlus || menuEscape {
		if m.historic.menu {
			m.closeMenus()
		} else {
			m.historic.menu = true
		}
		return m, nil, true
	}
	if k.Code == tea.KeyF5 && k.Mod == tea.ModAlt && m.runtime.workspaceRoot != nil {
		return m.openContents(false), nil, true
	}
	if k.Code == tea.KeyF5 && k.Mod == tea.ModCtrl && !s.Selection && s.HomePrefix == 0 && m.runtime.workspaceRoot != nil {
		m.closeMenus()
		m.historic.dosTextStage = 1
		m.notice = ""
		return m, nil, true
	}
	if k.Code == tea.KeyF13 && k.Mod == 0 && !k.IsRepeat {
		m.closeMenus()
		m.documentTabs = !m.documentTabs
		return m, nil, true
	}
	if k.Code == tea.KeyF3 && k.Mod == tea.ModCtrl && s.HomePrefix == 0 && m.runtime.workspaceRoot != nil {
		m.closeMenus()
		m.screenMenu = true
		return m, nil, true
	}
	if k.Code == tea.KeyF3 && k.Mod == 0 {
		m.closeMenus()
		return m.openHelp(false), nil, true
	}
	if k.Code == tea.KeyF1 && k.Mod == tea.ModCtrl && !k.IsRepeat &&
		s.HomePrefix == 0 && !m.session.StructuralUndeleteActive() {
		next, cmd := m.exitToCLI()
		return next, cmd, true
	}
	if k.Code == tea.KeyF1 && k.Mod == tea.ModShift {
		m.closeMenus()
		return m.openSetup(setupRoot), nil, true
	}
	if k.Code == tea.KeyF8 && k.Mod == tea.ModCtrl && !k.IsRepeat {
		m.closeMenus()
		m.appearance = appearanceFont
		return m, nil, true
	}
	if k.Code == tea.KeyF8 && k.Mod == tea.ModAlt && !s.Selection && m.runtime.workspaceRoot != nil {
		return m.openStyles(), nil, true
	}
	if k.Code == tea.KeyF8 && k.Mod == tea.ModShift && !s.Selection && s.HomePrefix == 0 && m.runtime.workspaceRoot != nil {
		return m.openLineFormat(formatMenu), nil, true
	}
	if k.Code == tea.KeyF5 && k.Mod == tea.ModShift && !s.Selection && s.HomePrefix == 0 && m.runtime.workspaceRoot != nil {
		m.closeMenus()
		m.dateMenu = true
		return m, nil, true
	}
	if k.Code == tea.KeyF7 && k.Mod == tea.ModCtrl && !s.Selection && s.HomePrefix == 0 && m.runtime.workspaceRoot != nil {
		return m.openNotes(noteMenu, false), nil, true
	}
	if k.Code == tea.KeyF7 && k.Mod == tea.ModAlt && m.showEditorChrome() && !s.Selection && s.HomePrefix == 0 {
		m.closeMenus()
		m.tablePrompt.stage = 1
		if table, ok := m.session.Document().SimpleTable(); ok {
			if _, inCell := table.CellAt(s.Gap); inCell {
				m.tablePrompt.stage = 5
			}
		}
		return m, nil, true
	}
	if k.Code == tea.KeyF7 && k.Mod == tea.ModShift && m.showEditorChrome() && !s.Selection && s.HomePrefix == 0 && m.runtime.workspaceRoot != nil {
		m.closeMenus()
		m.print.screen = printMenu
		return m, nil, true
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
	proof := m.session.ProofStatus()
	if proof.Phase != editor.ProofInactive &&
		(proof.Phase != editor.ProofEditing || m.session.Snapshot().Mode == editor.Editing) {
		return m.proofView(proof)
	}
	if m.setup.page != setupClosed {
		return m.setupView()
	}
	if m.help.active {
		return m.helpView()
	}
	lines := make([]string, m.height)
	frame := m.visibleFrame()
	s := m.session.Snapshot()
	bar := m.historic.bar && m.height >= 3 && proof.Phase == editor.ProofInactive
	reveal := s.Reveal && m.height >= 8
	top := 0
	if bar {
		top = 1
	}
	if m.showDocumentTabs() {
		lines[top] = m.documentTabLine()
		top++
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
	} else if !m.macroStatus.DisplaySuppressed && m.everyday.ready && m.everyday.revision == s.NativeRevision && s.Screen >= 1 && s.Screen <= editor.MaxDocumentScreens {
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
	tableStatus, tableFormula := "", ""
	var tableCodes []string
	if table, ok := m.session.Document().SimpleTable(); ok && !m.macroStatus.DisplaySuppressed {
		body, frame.x, row, tableStatus = simpleTableFrame(table, s.Gap)
		if index, inside := table.CellAt(s.Gap); inside {
			if formula := table.Cells[index].Formula(index, len(table.Widths)); formula != "" {
				tableFormula = "=" + formula
			}
		}
		start = max(0, row-max(1, bottom-top)+1)
		frame.err = nil
		if reveal {
			tableCodes = tableReveal(table, s.Gap, m.width, max(0, m.height-bottom-3))
		}
	}
	if sheet, ok := m.session.Document().SpreadsheetTable(); ok && !m.macroStatus.DisplaySuppressed {
		body, start, row, frame.x, frame.err = spreadsheetFrame(sheet, m.width), 0, 0, 0, nil
		useProjection = false
		if reveal {
			tableCodes = []string{"[Tbl Def][Row][Cell]" + sheet.Cells[0].Text + "[Cell]" + sheet.Cells[1].Text,
				"[Row][Cell]" + sheet.Cells[2].Text + "[Cell]" + sheet.Cells[3].Text + "[Tbl Off]"}
			if sheet.Link != nil {
				tableCodes = append([]string{"[Link:" + sheet.Link.Path + "  " + sheet.Link.Range.String() + "]"}, tableCodes...)
				tableCodes = append(tableCodes, "[Link End]")
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
		left, right := m.session.LineMargins()
		lines[min(m.height-1, bottom+1)] = tabRuler(m.width, editor.EverydaySettings(), m.session.TabSetAt(s.Gap), left, right)
		if bottom+2 < m.height {
			if tableCodes != nil {
				copy(lines[bottom+2:m.height-1], tableCodes)
			} else if useProjection {
				for i := start; i < len(projected.codes) && bottom+2+i-start < m.height-1; i++ {
					lines[bottom+2+i-start] = projected.codes[i]
				}
			} else {
				lines[bottom+2] = clip(frame.reveal, m.width)
			}
		}
	}
	statusName := strings.TrimSpace(s.Name + " " + tableStatus)
	if tableFormula != "" {
		statusName = tableFormula + " " + tableStatus
	}
	if m.session.ColumnMathActive() && tableStatus == "" {
		statusName = "Math " + statusName
	}
	if m.tablePrompt.block {
		statusName = "Block on    " + tableStatus
	}
	if s.Mode == editor.CopyTargetMode {
		statusName = "Move cursor; press Enter to retrieve."
	}
	lines[bottom] = m.positionStatus(m.width, statusName)
	prompt := s.Prompt
	if m.shellSavePrompt {
		action := "opening shell"
		if m.quitAfterSave {
			action = "quitting"
		}
		prompt = fmt.Sprintf("Save document %d before %s? Y Save / N Skip / Esc Cancel", s.Screen, action)
	}
	if m.tablePrompt.stage != 0 {
		prompt = m.tablePrompt.footer()
	}
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
	revealFooter := "Press " + revealCode + "Reveal Codes" + screenReset + " to restore screen"
	if reveal && prompt == "" {
		prompt = revealFooter
	}
	promptRow := m.height - 1
	structuralUndelete := m.session.StructuralUndeleteActive()
	if structuralUndelete {
		prompt = structuralUndeletePrompt()
		if reveal {
			lines[promptRow] = revealFooter
			promptRow = bottom
		}
	}
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
	if editor.IsReplacePrompt(s.Mode) && reveal {
		promptRow = bottom
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
	if m.compose.active && m.compose.echo {
		lines[bottom] = m.compose.prompt()
	}
	if notice != "" {
		lines[max(0, m.height-2)] = notice
	}
	if m.searchNotice != nil {
		lines[bottom] = revealCode + "* Not found *" + screenReset
	}
	if proof.Phase == editor.ProofInactive {
		m.paintMenus(lines)
		m.paintMergeChoices(lines)
	}
	if m.historic.files {
		lines = m.fileLines(lines)
	}
	if m.historic.dosTextStage != 0 {
		lines[bottom] = m.dosTextPrompt()
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
		if m.compose.active && m.compose.echo {
			v.Cursor = tea.NewCursor(min(m.width-1, len(m.compose.prompt())), bottom)
		}
		if s.Mode == editor.MergeChoicesMode {
			v.Cursor = tea.NewCursor(min(m.width-1, s.Caret), promptRow)
		}
		if s.Mode == editor.GoToMode {
			v.Cursor = tea.NewCursor(min(m.width-1, ansi.StringWidth(s.Prompt)), promptRow)
		}
		if s.Mode == editor.MergeMenuMode || s.Mode == editor.MergeCodesMode || s.Mode == editor.ConvertCaseMode ||
			s.Mode == editor.MoveMenuMode || s.Mode == editor.MoveBlockMode || structuralUndelete {
			v.Cursor = tea.NewCursor(min(m.width-1, ansi.StringWidth(prompt)-1), promptRow)
		}
		if s.Mode == editor.SaveName || s.Mode == editor.RetrieveName || s.Mode == editor.MacroName || s.Mode == editor.AppendBlockName ||
			mergeFilename(s.Mode) || s.Mode == editor.MergeFieldMode || s.Mode == editor.MergeOperandMode || searching || editor.IsReplacePrompt(s.Mode) {
			prefix := s.Prompt
			switch {
			case searching:
				prefix = searchPrefix
			case editor.IsReplacePrompt(s.Mode):
				prefix = strings.TrimSuffix(s.Prompt, s.Draft)
			case s.Mode == editor.MergeFieldMode:
				prefix = "Enter Field: "
			case s.Mode == editor.MergePrimaryName:
				prefix = "Primary file: "
			case s.Mode == editor.MergeSecondaryName:
				prefix = "Secondary file: "
			case s.Mode == editor.AppendBlockName:
				prefix = "Append to: "
			case s.Draft != "":
				if i := strings.Index(prefix, s.Draft); i >= 0 {
					prefix = prefix[:i]
				}
			case s.Mode == editor.RetrieveName:
				prefix = strings.TrimSuffix(prefix, " (List Files)")
			}
			v.Cursor = tea.NewCursor(min(m.width-1, ansi.StringWidth(prefix)+s.Caret), promptRow)
		}
	}
	if m.historic.dosTextStage != 0 {
		v.Cursor = tea.NewCursor(min(m.width-1, ansi.StringWidth(m.dosTextPrompt())), bottom)
	}
	return v
}
func (m Model) positionStatus(width int, name string) string {
	s := m.session.Snapshot()
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
	statusLeft := max(0, width-8-len(status))
	if field, ok := m.session.MergeField(); ok {
		name = fmt.Sprintf("Field: %d", field)
	}
	statusName := clip(name, max(0, statusLeft-1))
	return revealCode + statusName + screenReset + strings.Repeat(" ", max(0, statusLeft-ansi.StringWidth(statusName))) + revealCode + status + screenReset + statusValue
}

func printedInches(value float64) string {
	return strings.TrimRight(strings.TrimRight(fmt.Sprintf("%.2f", value), "0"), ".") + `"`
}
