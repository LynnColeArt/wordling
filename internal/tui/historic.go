package tui

import (
	"fmt"
	"os"
	"strings"
	"time"

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
	entries      []os.FileInfo
	selected     int
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
	{"Search", []historicItem{{"Forward", input.Key{}}, {"Backward", input.Key{}}, {"Next", input.Key{}}}},
	{"Layout", []historicItem{{"Line", input.Key{}}, {"Page", input.Key{}}, {"Document", input.Key{}}, {"Other", input.Key{}}, {"Columns", input.Key{}}, {"Tables", input.Key{}}, {"Math", input.Key{}}, {"Footnote", input.Key{}}, {"Endnote", input.Key{}}, {"Justify", input.Key{}}, {"Align", input.Key{}}, {"Styles", input.Key{}}}},
	{"Mark", nil}, {"Tools", []historicItem{{"Spell", input.Key{}}, {"Thesaurus", input.Key{}}, {"Macro", input.Key{}}, {"Date Text", input.Key{}}, {"Date Code", input.Key{}}, {"Date Format", input.Key{}}, {"Outline", input.Key{}}, {"Paragraph Number", input.Key{}}, {"Define", input.Key{}}, {"Merge Codes", input.Key{}}, {"Merge", input.Key{}}, {"Sort", input.Key{}}, {"Line Draw", input.Key{}}}},
	{"Font", []historicItem{{"Base Font", input.Key{}}, {"Normal", input.Key{}}, {"Appearance", input.Key{}}, {"Superscript", input.Key{}}, {"Subscript", input.Key{}}, {"Fine", input.Key{}}, {"Small", input.Key{}}, {"Large", input.Key{}}, {"Very Large", input.Key{}}, {"Extra Large", input.Key{}}, {"Print Color", input.Key{}}, {"Characters", input.Key{}}}},
	{"Graphics", nil}, {"Help", []historicItem{{"Help", input.Key{}}, {"Index", input.Key{}}, {"Template", input.Key{}}}},
}

var historicSubmenus = map[string][]historicItem{
	"Font/Appearance": {{"Bold", hk(tea.KeyF6, 0)}, {"Underline", input.Key{}}, {"Double Underline", input.Key{}}, {"Italics", input.Key{}}, {"Outline", input.Key{}}, {"Shadow", input.Key{}}, {"Small Cap", input.Key{}}, {"Redline", input.Key{}}, {"Strikeout", input.Key{}}},
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
func (m Model) openFiles() Model {
	entries, err := m.runtime.directory.List()
	m.historic.files, m.historic.selected, m.historic.message = true, 0, ""
	m.historic.entries = nil
	if err != nil {
		m.historic.message = err.Error()
		return m
	}
	for _, entry := range entries {
		name := entry.Name()
		safe := true
		for _, r := range name {
			if r < 32 || r > 126 {
				safe = false
			}
		}
		if safe && !strings.HasPrefix(name, ".wordling-") {
			m.historic.entries = append(m.historic.entries, entry)
		}
	}
	return m
}
func (m Model) filePress(k input.Key) (tea.Model, tea.Cmd) {
	h := &m.historic
	count := len(h.entries)
	switch k.Code {
	case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
		h.files, h.message = false, ""
	case tea.KeyUp:
		h.selected = max(0, h.selected-1)
	case tea.KeyDown:
		h.selected = min(max(0, count-1), h.selected+1)
	case tea.KeyLeft, tea.KeyPgUp:
		h.selected = max(0, h.selected-max(1, m.height-5))
	case tea.KeyRight, tea.KeyPgDown:
		h.selected = min(max(0, count-1), h.selected+max(1, m.height-5))
	case tea.KeyHome:
		h.selected = 0
	case tea.KeyEnd:
		h.selected = max(0, count-1)
	case tea.KeyEnter, '1':
		if count == 0 {
			return m, nil
		}
		entry := h.entries[h.selected]
		if !entry.Mode().IsRegular() {
			h.message = "Only regular files in the current directory can be retrieved"
			return m, nil
		}
		name := entry.Name()
		h.files, h.message = false, ""
		var next tea.Model = m
		var cmd tea.Cmd
		if m.session.Snapshot().Mode != editor.RetrieveName {
			next, cmd = m.reduce(editor.Event{Command: editor.Retrieve})
		}
		model := next.(Model)
		if model.session.Snapshot().Draft != "" {
			model.historic.files = true
			model.historic.message = "Clear the retrieve name before selecting a file"
			return model, nil
		}
		if cmd != nil || model.session.Snapshot().Mode != editor.RetrieveName {
			return model, cmd
		}
		for _, r := range name {
			next, cmd = model.reduce(editor.Event{Command: editor.Text, Text: string(r)})
			model = next.(Model)
			if cmd != nil {
				return model, cmd
			}
		}
		return model.reduce(editor.Event{Command: editor.Enter})
	default:
		h.message = "This List Files command is not yet implemented"
	}
	return m, nil
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
	top := 0
	if m.historic.bar {
		top = 1
	}
	bottom := max(top, m.height-1)
	if s.Reveal {
		bottom = max(top, m.height/2-1)
	}
	body := strings.Split(frame.normal, "\n")
	row := max(0, frame.y)
	start := max(0, row-max(1, bottom-top)+1)
	for i := start; i < len(body) && top+i-start < bottom; i++ {
		lines[top+i-start] = clip(body[i], m.width)
	}
	if frame.err != nil {
		lines[top] = "Unsupported document presentation"
	}
	if s.Reveal {
		lines[min(m.height-1, bottom+1)] = menuRed + strings.Repeat("-", m.width) + screenReset
		if bottom+2 < m.height {
			lines[bottom+2] = clip(frame.reveal, m.width)
		}
	}
	// Printed geometry requires a qualified layout engine. Unknown values must
	// not be synthesized from terminal wrapping or native token counts.
	status := fmt.Sprintf("Doc %d Pg -- Ln -- Pos --", s.Screen)
	if d := m.session.Document(); d != nil && d.TokenCount() == 0 {
		status = fmt.Sprintf("Doc %d Pg 1 Ln 1\" Pos 1\"", s.Screen)
	}
	lines[bottom] = strings.Repeat(" ", max(0, m.width-len(status))) + status
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
	if s.Reveal && prompt == "" {
		prompt = "Press Reveal Codes to restore screen"
	}
	if prompt != "" {
		lines[m.height-1] = prompt
	}
	notice := s.Notice
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
	if m.historic.bar {
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
		lines = m.fileLines()
	}
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	applyEditorChrome(&v)
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	if !m.historic.menu && !m.historic.files {
		v.Cursor = tea.NewCursor(min(frame.x, m.width-1), min(bottom-1, top+row-start))
		if s.Mode == editor.SaveName || s.Mode == editor.RetrieveName || s.Mode == editor.MacroName {
			v.Cursor = tea.NewCursor(min(m.width-1, len(s.Prompt)-len(s.Draft)+s.Caret), m.height-1)
		}
	}
	return v
}
func (m Model) fileLines() []string {
	lines := make([]string, m.height)
	h := m.historic
	lines[0] = menuRed + clip(time.Now().Format("01-02-06 03:04p")+"   Directory "+m.runtime.rootLabel+"/*", m.width) + screenReset
	lines[1] = menuRed + fmt.Sprintf("Files: %d", len(h.entries)) + strings.Repeat(" ", max(0, m.width-10)) + screenReset
	rows := max(1, m.height-5)
	first := h.selected / (rows * 2) * (rows * 2)
	for r := 0; r < rows; r++ {
		for c := 0; c < 2; c++ {
			index := first + c*rows + r
			cell := ""
			if index < len(h.entries) {
				entry := h.entries[index]
				size := fmt.Sprint(entry.Size())
				if entry.IsDir() {
					size = "<Dir>"
				}
				cell = fmt.Sprintf("%-16s %8s %s", clip(entry.Name(), 16), size, entry.ModTime().Format("01-02-06"))
			}
			width := max(1, m.width/2)
			cell = clip(cell, width)
			cell += strings.Repeat(" ", max(0, width-ansi.StringWidth(cell)))
			if index == h.selected && index < len(h.entries) {
				cell = menuRed + cell + screenReset
			}
			lines[r+3] += cell
		}
	}
	lines[m.height-2] = "1 Retrieve; 2 Delete; 3 Move/Rename; 4 Print; 5 Short/Long Display;"
	lines[m.height-1] = "6 Look; 7 Other Directory; 8 Copy; 9 Find; N Name Search:"
	if h.message != "" {
		lines[m.height-2] = h.message
	}
	return lines
}
