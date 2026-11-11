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
	parent       int
	menu         bool
	drop         bool
	column, item int
	files        bool
	browser      fileBrowser
	message      string
}

type historicItem struct {
	label string
	key   input.Key
}
type historicMenu struct {
	label string
	items []historicItem
}

func hk(code rune, mod tea.KeyMod) input.Key { return input.Key{Code: code, Mod: mod} }

var historicMenus = []historicMenu{
	{"File", []historicItem{
		{"Retrieve", hk(tea.KeyF10, tea.ModShift)}, {"Save", hk(tea.KeyF10, 0)},
		{"Text In", input.Key{}}, {"Text Out", input.Key{}}, {"Password", input.Key{}},
		{"List Files", hk(tea.KeyF5, 0)}, {"Summary", input.Key{}}, {"Print", input.Key{}},
		{"Setup", input.Key{}}, {"Keyboard Layout", input.Key{}}, {"Location of Files", input.Key{}},
		{"Go to DOS", input.Key{}}, {"Exit", hk(tea.KeyF7, 0)},
	}},
	{"Edit", []historicItem{
		{"Move (Cut)", input.Key{}}, {"Copy", input.Key{}}, {"Paste", input.Key{}}, {"Append", input.Key{}},
		{"Delete", hk(tea.KeyDelete, 0)}, {"Undelete", hk(tea.KeyF1, 0)}, {"Block", hk(tea.KeyF4, tea.ModAlt)},
		{"Select", input.Key{}}, {"Comment", input.Key{}}, {"Convert Case", input.Key{}},
		{"Protect Block", input.Key{}}, {"Switch Document", hk(tea.KeyF3, tea.ModShift)},
		{"Window", input.Key{}}, {"Reveal Codes", hk(tea.KeyF3, tea.ModAlt)},
	}},
	{"Search", []historicItem{{"Forward", hk(tea.KeyF2, 0)}, {"Backward", hk(tea.KeyF2, tea.ModShift)}, {"Next", hk(tea.KeyF2, 0)}}},
	{"Layout", []historicItem{{"Line", input.Key{}}, {"Page", input.Key{}}, {"Document", input.Key{}}, {"Other", input.Key{}}, {"Columns", input.Key{}}, {"Tables", input.Key{}}, {"Math", input.Key{}}, {"Footnote", input.Key{}}, {"Endnote", input.Key{}}, {"Justify", input.Key{}}, {"Align", input.Key{}}, {"Styles", input.Key{}}}},
	{"Mark", nil}, {"Tools", []historicItem{{"Spell", input.Key{}}, {"Thesaurus", input.Key{}}, {"Macro", input.Key{}}, {"Date Text", input.Key{}}, {"Date Code", input.Key{}}, {"Date Format", input.Key{}}, {"Outline", input.Key{}}, {"Paragraph Number", input.Key{}}, {"Define", input.Key{}}, {"Merge Codes", input.Key{}}, {"Merge", input.Key{}}, {"Sort", input.Key{}}, {"Line Draw", input.Key{}}}},
	{"Font", []historicItem{{"Base Font", input.Key{}}, {"Normal", input.Key{}}, {"Appearance", input.Key{}}, {"Superscript", input.Key{}}, {"Subscript", input.Key{}}, {"Fine", input.Key{}}, {"Small", input.Key{}}, {"Large", input.Key{}}, {"Very Large", input.Key{}}, {"Extra Large", input.Key{}}, {"Print Color", input.Key{}}, {"Characters", input.Key{}}}},
	{"Graphics", nil}, {"Help", []historicItem{{"Help", input.Key{}}, {"Index", input.Key{}}, {"Template", input.Key{}}}},
}

var historicSubmenus = map[string][]historicItem{
	"Font/Appearance": {{"Bold", hk(tea.KeyF6, 0)}, {"Underline", hk(tea.KeyF8, 0)}, {"Double Underline", input.Key{}}, {"Italics", input.Key{}}, {"Outline", input.Key{}}, {"Shadow", input.Key{}}, {"Small Cap", input.Key{}}, {"Redline", input.Key{}}, {"Strikeout", input.Key{}}},
	"Tools/Macro":     {{"Define", input.Key{}}, {"Execute", hk(tea.KeyF10, tea.ModAlt)}},
}

func (m Model) activeItems() []historicItem {
	if m.historic.sub != "" {
		return historicSubmenus[m.historic.sub]
	}
	return historicMenus[m.historic.column].items
}

const menuGray = "\x1b[22;34;47m"
const menuRed = "\x1b[22;37;41m"
const screenReset = "\x1b[0m"

func (m Model) historicPress(k input.Key) (tea.Model, tea.Cmd, bool) {
	s := m.session.Snapshot()
	if m.historic.files {
		next, cmd := m.filePress(k)
		return next, cmd, true
	}
	if s.Mode == editor.RetrieveName && k.Code == tea.KeyF5 && k.Mod == 0 {
		return m.openFiles(), nil, true
	}
	if s.Mode != editor.Editing || len(m.unsettled) != 0 || m.firstPending != nil || m.macro != nil || m.reconcile != "" || m.characterRepeat.active || m.repeatEntry {
		return m, nil, false
	}
	if menuKey(k) {
		m.historic.menu = !m.historic.menu
		m.historic.bar = m.historic.menu
		m.historic.drop = false
		m.historic.sub = ""
		m.historic.message = ""
		return m, nil, true
	}
	if k.Mod == 0 && k.Code == tea.KeyF5 {
		return m.openFiles(), nil, true
	}
	if !m.historic.menu {
		// An ordinary boundary key leaves the caret in place. Keep the native
		// reader's strict bounds checking for callers that request invalid gaps.
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
	switch k.Code {
	case tea.KeyF7, tea.KeyEscape:
		m.historic.menu, m.historic.drop = false, false
		m.historic.sub = ""
	case tea.KeyF1:
		if m.historic.sub != "" {
			m.historic.sub = ""
			m.historic.item = m.historic.parent
			return m, nil, true
		}
		if m.historic.drop {
			m.historic.drop = false
			m.historic.sub = ""
		} else {
			m.historic.menu = false
		}
	case tea.KeyLeft:
		if m.historic.sub != "" {
			m.historic.sub = ""
			m.historic.item = m.historic.parent
			return m, nil, true
		}
		m.historic.column = (m.historic.column + len(historicMenus) - 1) % len(historicMenus)
		m.historic.item = 0
		m.historic.sub = ""
	case tea.KeyRight:
		if m.historic.drop {
			items := m.activeItems()
			if len(items) > 0 && historicSubmenus[historicMenus[m.historic.column].label+"/"+items[m.historic.item].label] != nil {
				next, cmd := m.activateMenu()
				return next, cmd, true
			}
		}
		m.historic.column = (m.historic.column + 1) % len(historicMenus)
		m.historic.item = 0
		m.historic.sub = ""
	case tea.KeyUp, tea.KeyDown:
		items := m.activeItems()
		if !m.historic.drop {
			m.historic.drop = true
		} else if len(items) > 0 {
			step := 1
			if k.Code == tea.KeyUp {
				step = len(items) - 1
			}
			m.historic.item = (m.historic.item + step) % len(items)
		}
	case tea.KeyEnter:
		if !m.historic.drop {
			m.historic.drop = true
		} else {
			next, cmd := m.activateMenu()
			return next, cmd, true
		}
	default:
		letter := strings.ToLower(k.Text)
		if letter != "" {
			if !m.historic.drop {
				for i, menu := range historicMenus {
					if strings.HasPrefix(strings.ToLower(menu.label), letter) {
						m.historic.column, m.historic.item, m.historic.drop = i, 0, true
						m.historic.sub = ""
						break
					}
				}
			} else {
				for i, item := range m.activeItems() {
					if strings.HasPrefix(strings.ToLower(item.label), letter) {
						m.historic.item = i
						next, cmd := m.activateMenu()
						return next, cmd, true
					}
				}
			}
		}
	}
	return m, nil, true
}
func (m Model) activateMenu() (tea.Model, tea.Cmd) {
	items := m.activeItems()
	if len(items) == 0 {
		m.historic.message = "This menu is not yet implemented"
		return m, nil
	}
	item := items[m.historic.item]
	sub := historicMenus[m.historic.column].label + "/" + item.label
	if historicSubmenus[sub] != nil {
		m.historic.sub = sub
		m.historic.parent = m.historic.item
		m.historic.item = 0
		return m, nil
	}
	if item.key.Code == 0 {
		m.historic.message = item.label + " is not yet implemented"
		return m, nil
	}
	m.historic.menu, m.historic.drop, m.historic.message = false, false, ""
	if item.key.Code == tea.KeyF5 {
		return m.openFiles(), nil
	}
	return m.update(tea.KeyPressMsg(tea.Key{Code: item.key.Code, Mod: item.key.Mod}))
}
func (m Model) historicMouse(mouse *tea.Mouse) (tea.Model, tea.Cmd) {
	if m.session.Snapshot().Mode != editor.Editing || len(m.unsettled) != 0 || m.firstPending != nil || m.macro != nil || m.reconcile != "" {
		return m, nil
	}
	if mouse == nil {
		return m, nil
	}
	if mouse.Button == tea.MouseRight {
		next, cmd, _ := m.historicPress(hk('=', tea.ModAlt))
		return next, cmd
	}
	if mouse.Button != tea.MouseLeft || m.historic.files {
		return m, nil
	}
	if mouse.Y == 0 && m.historic.bar {
		m.historic.menu = true
		x := 0
		for i, menu := range historicMenus {
			if mouse.X >= x && mouse.X < x+len(menu.label) {
				m.historic.column, m.historic.item, m.historic.drop = i, 0, true
				m.historic.sub = ""
				return m, nil
			}
			x += len(menu.label) + 1
		}
	}
	if m.historic.drop {
		x := m.menuX()
		items := m.activeItems()
		if mouse.X >= x && mouse.X < x+22 && mouse.Y >= 1 && mouse.Y <= len(items) {
			m.historic.item = mouse.Y - 1
			return m.activateMenu()
		}
	}
	return m, nil
}
func (m Model) menuX() int {
	x := 0
	for _, menu := range historicMenus[:m.historic.column] {
		x += len(menu.label) + 1
	}
	if m.historic.sub != "" {
		x += 18
	}
	return min(x, max(0, m.width-22))
}
func (m Model) historicView() tea.View {
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
	if bar {
		var bar strings.Builder
		for i, menu := range historicMenus {
			role := menuGray
			if m.historic.menu && i == m.historic.column {
				role = menuRed
			}
			bar.WriteString(role + menu.label + " ")
		}
		lines[0] = bar.String() + menuGray + strings.Repeat(" ", max(0, m.width-ansi.StringWidth(bar.String()))) + screenReset
		if m.historic.drop {
			if m.historic.sub != "" {
				parentModel := m
				parentModel.historic.sub = ""
				x := parentModel.menuX()
				for i, item := range historicMenus[m.historic.column].items {
					if i+1 >= m.height-1 {
						break
					}
					role := menuGray
					if i == m.historic.parent {
						role = menuRed
					}
					old := lines[i+1]
					left := ansi.Truncate(old, x, "")
					left += strings.Repeat(" ", max(0, x-ansi.StringWidth(left)))
					lines[i+1] = left + role + fmt.Sprintf(" %-20s ", item.label) + screenReset + ansi.TruncateLeft(old, x+22, "")
				}
			}
			items := m.activeItems()
			x := m.menuX()
			for i, item := range items {
				if i+1 >= m.height-1 {
					break
				}
				role := menuGray
				if i == m.historic.item {
					role = menuRed
				}
				old := lines[i+1]
				left := ansi.Truncate(old, x, "")
				left += strings.Repeat(" ", max(0, x-ansi.StringWidth(left)))
				lines[i+1] = left + role + fmt.Sprintf(" %-20s ", item.label) + screenReset + ansi.TruncateLeft(old, x+22, "")
			}
		}
	}
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
