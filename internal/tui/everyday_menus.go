package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

// Each row carries its observed caption cells, mnemonic, native key and
// original block requirement. An empty row separates command groups.
type historicItem struct {
	label, cells string
	mnemonic     int
	key          input.Key
	needsBlock   bool
}

type historicMenu struct {
	label    string
	mnemonic int
	width    int
	items    []historicItem
}

func hk(code rune, mod tea.KeyMod) input.Key { return input.Key{Code: code, Mod: mod} }

var historicMenus = []historicMenu{
	{"File", 0, 23, []historicItem{
		{"Retrieve", " Retrieve   Shft-F10 ", 1, hk(tea.KeyF10, tea.ModShift), false},
		{"Save", " Save       F10      ", 1, hk(tea.KeyF10, 0), false},
		{"Text In", " Text In    Ctrl-F5 ►", 6, hk(tea.KeyF5, tea.ModCtrl), false},
		{"Text Out", " Text Out   Ctrl-F5 ►", 6, input.Key{}, false},
		{"Password", " Password   Ctrl-F5 ►", 5, input.Key{}, false},
		{},
		{"List Files", " List Files F5       ", 6, hk(tea.KeyF5, 0), false},
		{"Summary", " Summary             ", 3, input.Key{}, false},
		{},
		{"Print", " Print      Shft-F7  ", 1, hk(tea.KeyF7, tea.ModShift), false},
		{},
		{"Setup", " Setup      Shft-F1 ►", 3, input.Key{}, false},
		{},
		{"Open Shell", " Open Shell Ctrl-F1  ", 7, hk(tea.KeyF1, tea.ModCtrl), false},
		{"Close Document", " Close Doc  F7       ", 1, hk(tea.KeyF7, 0), false},
		{"Quit Wordling", " Quit Wordling       ", 1, input.Key{}, false},
		{"New Document", " New Document        ", 1, input.Key{}, false},
		{"Switch Document", " Switch Doc Shift-F3 ", 2, hk(tea.KeyF3, tea.ModShift), false},
	}},
	{"Edit", 0, 29, []historicItem{
		{"Move (Cut)", " Move (Cut)      Ctrl-Del  ", 1, input.Key{}, true},
		{"Copy", " Copy            Ctrl-Ins  ", 1, input.Key{}, true},
		{"Paste", " Paste                     ", 1, input.Key{}, false},
		{"Append", " Append                    ", 1, input.Key{}, true},
		{},
		{"Delete", " Delete          Del       ", 1, hk(tea.KeyDelete, 0), false},
		{"Undelete", " Undelete        F1        ", 1, hk(tea.KeyF1, 0), false},
		{},
		{"Block", " Block           Alt-F4    ", 1, hk(tea.KeyF4, tea.ModAlt), false},
		{"Select", " Select                   ►", 2, input.Key{}, false},
		{"Comment", " Comment         Ctrl-F5  ►", 2, input.Key{}, false},
		{"Convert Case", " Convert Case    Shft-F3   ", 4, hk(tea.KeyF3, tea.ModShift), true},
		{"Protect Block", " Protect Block   Shft-F8   ", 4, input.Key{}, true},
		{},
		{"Switch Document", " Switch Document Shft-F3   ", 1, hk(tea.KeyF3, tea.ModShift), false},
		{"Window", " Window          Ctrl-F3   ", 1, input.Key{}, false},
		{},
		{"Reveal Codes", " Reveal Codes    Alt-F3    ", 1, hk(tea.KeyF3, tea.ModAlt), false},
	}},
	{"Search", 0, 22, []historicItem{
		{"Forward", " Forward  F2        ", 1, hk(tea.KeyF2, 0), false},
		{"Backward", " Backward Shft-F2   ", 1, hk(tea.KeyF2, tea.ModShift), false},
		{"Next", " Next               ", 1, hk(tea.KeyF2, 0), false},
		{"Previous", " Previous           ", 1, hk(tea.KeyF2, tea.ModShift), false},
		{},
		{"Replace", " Replace  Alt-F2    ", 1, hk(tea.KeyF2, tea.ModAlt), false},
		{},
		{"Extended", " Extended          ►", 1, input.Key{}, false},
		{},
		{"Go to", " Go to    Ctrl-Home ", 1, hk(tea.KeyHome, tea.ModCtrl), false},
	}},
	{"Layout", 0, 20, []historicItem{
		{"Line", " Line     Shft-F8 ", 1, input.Key{}, false},
		{"Page", " Page     Shft-F8 ", 1, input.Key{}, false},
		{"Document", " Document Shft-F8 ", 1, input.Key{}, false},
		{"Other", " Other    Shft-F8 ", 1, input.Key{}, false},
		{},
		{"Columns", " Columns  Alt-F7 ►", 1, input.Key{}, false},
		{"Tables", " Tables   Alt-F7 ►", 1, hk(tea.KeyF7, tea.ModAlt), false},
		{"Math", " Math     Alt-F7 ►", 1, input.Key{}, false},
		{},
		{"Footnote", " Footnote Ctrl-F7►", 1, input.Key{}, false},
		{"Endnote", " Endnote  Ctrl-F7►", 1, input.Key{}, false},
		{},
		{"Justify", " Justify         ►", 1, input.Key{}, false},
		{"Align", " Align           ►", 1, input.Key{}, false},
		{},
		{"Styles", " Styles   Alt-F8  ", 1, input.Key{}, false},
	}},
	{"Mark", 0, 26, []historicItem{
		{"Index", " Index           Alt-F5 ", 1, input.Key{}, false},
		{"Table of Contents", " Table of Contents      ", 10, input.Key{}, true},
		{"List", " List                   ", 1, input.Key{}, true},
		{"Cross-Reference", " Cross-Reference Alt-F5►", 1, input.Key{}, false},
		{"Table of Authorities", " Table of Authorities  ►", 10, input.Key{}, false},
		{},
		{"Define", " Define          Alt-F5►", 1, input.Key{}, false},
		{},
		{"Generate", " Generate               ", 1, input.Key{}, false},
		{},
		{"Master Documents", " Master Documents      ►", 1, input.Key{}, false},
		{"Subdocument", " Subdocument     Alt-F5 ", 1, input.Key{}, false},
		{},
		{"Document Compare", " Document Compare      ►", 1, input.Key{}, false},
	}},
	{"Tools", 0, 28, []historicItem{
		{"Document Tabs", " Document Tabs    F13    ", 10, hk(tea.KeyF13, 0), false},
		{"Spell", " Spell            Ctrl-F2 ", 1, hk(tea.KeyF2, tea.ModCtrl), false},
		{"Thesaurus", " Thesaurus        Alt-F1  ", 2, input.Key{}, false},
		{},
		{"Macro", " Macro                   ►", 2, input.Key{}, false},
		{},
		{"Date Text", " Date Text        Shft-F5 ", 6, input.Key{}, false},
		{"Date Code", " Date Code        Shft-F5 ", 6, input.Key{}, false},
		{"Date Format", " Date Format      Shft-F5 ", 6, input.Key{}, false},
		{},
		{"Outline", " Outline          Shft-F5►", 1, input.Key{}, false},
		{"Paragraph Number", " Paragraph Number Shft-F5 ", 1, input.Key{}, false},
		{"Define", " Define           Shft-F5 ", 1, input.Key{}, false},
		{},
		{"Merge Codes", " Merge Codes      Shft-F9►", 3, hk(tea.KeyF9, tea.ModShift), false},
		{"Merge", " Merge            Ctrl-F9 ", 1, input.Key{Code: tea.KeyF9, Mod: tea.ModCtrl}, false},
		{},
		{"Sort", " Sort             Ctrl-F9 ", 1, input.Key{}, false},
		{},
		{"Line Draw", " Line Draw        Ctrl-F3 ", 1, input.Key{}, false},
	}},
	{"Font", 1, 23, []historicItem{
		{"Base Font", " Base Font   Ctrl-F8 ", 1, input.Key{}, false},
		{},
		{"Normal", " Normal      Ctrl-F8 ", 1, input.Key{}, false},
		{"Appearance", " Appearance  Ctrl-F8►", 1, input.Key{}, false},
		{"Superscript", " Superscript         ", 3, input.Key{}, false},
		{"Subscript", " Subscript           ", 3, input.Key{}, false},
		{"Fine", " Fine                ", 1, input.Key{}, false},
		{"Small", " Small               ", 1, input.Key{}, false},
		{"Large", " Large               ", 1, input.Key{}, false},
		{"Very Large", " Very Large          ", 1, input.Key{}, false},
		{"Extra Large", " Extra Large         ", 1, input.Key{}, false},
		{},
		{"Print Color", " Print Color Ctrl-F8 ", 7, input.Key{}, false},
		{},
		{"Characters", " Characters  Ctrl-V  ", 2, hk('v', tea.ModCtrl), false},
	}},
	{"Graphics", 0, 20, []historicItem{
		{"Figure", " Figure    Alt-F9►", 1, input.Key{}, false},
		{"Table Box", " Table Box Alt-F9►", 1, input.Key{}, false},
		{"Text Box", " Text Box  Alt-F9►", 3, input.Key{}, false},
		{"User Box", " User Box  Alt-F9►", 1, input.Key{}, false},
		{"Equation", " Equation  Alt-F9►", 1, input.Key{}, false},
		{},
		{"Line", " Line      Alt-F9►", 1, input.Key{}, false},
	}},
	{"Help", 0, 12, []historicItem{
		{"Help", " Help     ", 1, input.Key{}, false},
		{"Index", " Index    ", 1, input.Key{}, false},
		{"Template", " Template ", 1, input.Key{}, false},
	}},
}

type historicChild struct {
	width int
	items []historicItem
}

var historicSubmenus = map[string]historicChild{
	"Layout/Footnote": {14, []historicItem{
		{"Create", " Create     ", 1, input.Key{}, false}, {"Edit", " Edit       ", 1, input.Key{}, false},
		{"New Number", " New Number ", 1, input.Key{}, false}, {"Options", " Options    ", 1, input.Key{}, false},
	}},
	"Layout/Justify": {10, []historicItem{
		{"Left", " Left   ", 1, input.Key{}, false},
		{"Center", " Center ", 1, input.Key{}, false},
		{"Right", " Right  ", 1, input.Key{}, false},
		{"Full", " Full   ", 1, input.Key{}, false},
	}},
	"Font/Appearance": {20, []historicItem{
		{"Bold", " Bold          F6 ", 1, hk(tea.KeyF6, 0), false},
		{"Underline", " Underline     F8 ", 1, hk(tea.KeyF8, 0), false},
		{"Double Underline", " Double Underline ", 1, input.Key{}, false},
		{"Italics", " Italics          ", 1, input.Key{}, false},
		{"Outline", " Outline          ", 1, input.Key{}, false},
		{"Shadow", " Shadow           ", 3, input.Key{}, false},
		{"Small Cap", " Small Cap        ", 7, input.Key{}, false},
		{"Redline", " Redline          ", 1, input.Key{}, false},
		{"Strikeout", " Strikeout        ", 1, input.Key{}, false},
	}},
	"File/Setup": {21, []historicItem{
		{"Mouse", " Mouse             ", 1, input.Key{}, false},
		{"Display", " Display           ", 1, input.Key{}, false},
		{"Environment", " Environment       ", 1, input.Key{}, false},
		{"Initial Settings", " Initial Settings  ", 1, input.Key{}, false},
		{"Keyboard Layout", " Keyboard Layout   ", 1, input.Key{}, false},
		{"Location of Files", " Location of Files ", 1, input.Key{}, false},
	}},
	"Layout/Endnote": {14, []historicItem{
		{"Create", " Create     ", 1, input.Key{}, false}, {"Edit", " Edit       ", 1, input.Key{}, false},
		{"New Number", " New Number ", 1, input.Key{}, false}, {"Options", " Options    ", 1, input.Key{}, false},
		{"Placement", " Placement  ", 1, input.Key{}, false},
	}},
	"Tools/Macro": {20, []historicItem{
		{"Define", " Define  Ctrl-F10 ", 1, input.Key{}, false},
		{"Execute", " Execute Alt-F10  ", 1, hk(tea.KeyF10, tea.ModAlt), false},
	}},
	"Graphics/Figure": {14, []historicItem{
		{"Create", " Create     ", 1, input.Key{}, false}, {"Edit", " Edit       ", 1, input.Key{}, false},
		{"New Number", " New Number ", 1, input.Key{}, false}, {"Options", " Options    ", 1, input.Key{}, false},
	}},
	"Layout/Align": {28, []historicItem{
		{"Indent ->", " Indent ->     F4         ", 1, hk(tea.KeyF4, 0), false},
		{"Indent -><-", " Indent -><-   Shft-F4    ", 1, hk(tea.KeyF4, tea.ModShift), false},
		{"Margin Rel <-", " Margin Rel <- Shft-Tab   ", 1, hk(tea.KeyTab, tea.ModShift), false},
		{},
		{"Center", " Center        Shft-F6    ", 1, hk(tea.KeyF6, tea.ModShift), false},
		{"Flush Right", " Flush Right   Alt-F6     ", 1, hk(tea.KeyF6, tea.ModAlt), false},
		{"Tab Align", " Tab Align     Ctrl-F6    ", 1, hk(tea.KeyF6, tea.ModCtrl), false},
	}},
	"Search/Extended": {12, []historicItem{
		{"Forward", " Forward  ", 1, input.Key{}, false}, {"Backward", " Backward ", 1, input.Key{}, false},
		{"Next", " Next     ", 1, input.Key{}, false}, {"Previous", " Previous ", 1, input.Key{}, false},
		{}, {"Replace", " Replace  ", 1, input.Key{}, false},
	}},
}

const (
	menuGray     = "\x1b[22;34;47m"
	menuMnemonic = "\x1b[22;31;47m"
	menuRed      = "\x1b[22;37;41m"
	screenReset  = "\x1b[0m"
)

func (m Model) menuVisible() bool {
	return m.historic.bar || m.historic.menu
}

func (m Model) activeItems() []historicItem {
	if m.historic.sub != "" {
		return historicSubmenus[m.historic.sub].items
	}
	return historicMenus[m.historic.column].items
}

func (m *Model) closeMenus() {
	h := &m.historic
	h.menu, h.drop, h.titleActive = false, false, false
	h.sub, h.drawnSub, h.message = "", "", ""
}

func (m *Model) openMenu(column int) {
	h := &m.historic
	h.menu, h.drop, h.titleActive = true, true, true
	h.column, h.item = column, 0
	for i, item := range historicMenus[column].items {
		if item.label != "" && (!item.needsBlock || m.session.Snapshot().Selection) {
			h.item = i
			break
		}
	}
	h.sub, h.drawnSub = "", ""
	menu := historicMenus[column]
	m.openSubmenu(menu.label + "/" + menu.items[h.item].label)
}

func (m *Model) openSubmenu(name string) bool {
	if _, exists := historicSubmenus[name]; !exists {
		return false
	}
	h := &m.historic
	h.parent, h.item = h.item, 0
	h.sub, h.drawnSub = name, name
	return true
}

func (m *Model) backToParent() {
	m.historic.sub = ""
	m.historic.item = m.historic.parent
}

func (m Model) activateMenu() (tea.Model, tea.Cmd) {
	items := m.activeItems()
	if len(items) == 0 || m.historic.item >= len(items) {
		return m, nil
	}
	item := items[m.historic.item]
	if !m.menuItemVisible(m.historic.item) || item.label == "" || item.needsBlock && !m.session.Snapshot().Selection {
		return m, nil
	}
	if m.historic.sub == "" && historicMenus[m.historic.column].label == "Tools" && m.runtime.workspaceRoot != nil {
		switch item.label {
		case "Date Text":
			return m.insertDateText(m.runtime.now()), nil
		case "Date Code":
			return m.insertDateCode(), nil
		case "Sort":
			return m.openSort()
		case "Line Draw":
			m.closeMenus()
			m.screenMenu, m.lineDraw = true, lineDrawUI{stage: 1}
			return m, nil
		case "Outline":
			m.closeMenus()
			m.dateMenu, m.outlineMenu = true, true
			return m, nil
		}
	}
	if m.historic.sub == "" && historicMenus[m.historic.column].label == "Layout" && m.runtime.workspaceRoot != nil {
		switch item.label {
		case "Styles":
			return m.openStyles(), nil
		case "Math":
			m.closeMenus()
			m.tablePrompt = tablePrompt{stage: 11}
			return m, nil
		case "Line":
			return m.openLineFormat(formatLine), nil
		case "Page":
			return m.openLineFormat(formatPage), nil
		case "Other":
			return m.openLineFormat(formatOther), nil
		}
	}
	if m.historic.sub == "" && historicMenus[m.historic.column].label == "Mark" && m.runtime.workspaceRoot != nil {
		switch item.label {
		case "Table of Contents":
			return m.openContents(true), nil
		case "Cross-Reference":
			m = m.openContents(false)
			m.contents.stage = contentsReference
			return m, nil
		case "Subdocument":
			m = m.openContents(false)
			m.contents.stage = contentsSubdocument
			return m, nil
		case "Define":
			m = m.openContents(false)
			m.contents.stage = contentsDefineMenu
			return m, nil
		case "Generate":
			m = m.openContents(false)
			m.contents.stage = contentsGenerate
			return m, nil
		}
	}
	if m.historic.sub == "" && historicMenus[m.historic.column].label == "Edit" && item.label == "Comment" && m.runtime.workspaceRoot != nil {
		return m.openComment(), nil
	}
	if m.historic.sub == "" && m.openSubmenu(historicMenus[m.historic.column].label+"/"+item.label) {
		return m, nil
	}
	if m.historic.sub == "Font/Appearance" && item.label == "Italics" {
		return m.applyItalics(), nil
	}
	if m.historic.sub == "Tools/Macro" && item.label == "Define" {
		return m.openMacroRecording(), nil
	}
	if m.historic.sub == "File/Setup" {
		var page setupPage
		switch item.label {
		case "Display":
			page = setupDisplay
		case "Environment":
			page = setupEnvironment
		}
		if page != setupClosed {
			m.closeMenus()
			return m.openSetup(page), nil
		}
	}
	if m.historic.sub == "Layout/Justify" && m.runtime.workspaceRoot != nil {
		switch item.label {
		case "Left":
			m.closeMenus()
			return m.setJustification(document.JustifyLeft, formatClosed), nil
		case "Full":
			m.closeMenus()
			return m.setJustification(document.JustifyFull, formatClosed), nil
		case "Center":
			m.closeMenus()
			return m.setJustification(document.JustifyCenter, formatClosed), nil
		case "Right":
			m.closeMenus()
			return m.setJustification(document.JustifyRight, formatClosed), nil
		}
	}
	if (item.label == "Create" || item.label == "Edit") && m.runtime.workspaceRoot != nil {
		stage := noteEditor
		if item.label == "Edit" {
			stage = noteNumber
		}
		switch m.historic.sub {
		case "Layout/Footnote":
			return m.openNotes(stage, false), nil
		case "Layout/Endnote":
			return m.openNotes(stage, true), nil
		}
	}
	if m.historic.column == len(historicMenus)-1 {
		m.closeMenus()
		m = m.openHelp(item.label == "Template")
		if item.label == "Index" {
			m.help.topic = "Index"
		}
		return m, nil
	}
	if m.historic.sub == "" && historicMenus[m.historic.column].label == "Search" {
		switch item.label {
		case "Next":
			return m.repeatMenuSearch(editor.SearchF2)
		case "Previous":
			return m.repeatMenuSearch(editor.SearchBackF2)
		}
	}
	if item.label == "Text Out" && m.runtime.workspaceRoot != nil {
		m.closeMenus()
		m.historic.dosTextStage = 4
		return m, nil
	}
	if item.label == "Summary" {
		return m.openSummary(), nil
	}
	if item.label == "New Document" {
		m.closeMenus()
		return m.reduce(editor.Event{Command: editor.NewDocumentScreen})
	}
	if item.label == "Quit Wordling" {
		return m.beginLeave(true)
	}
	if m.historic.sub == "" && historicMenus[m.historic.column].label == "Edit" {
		switch item.label {
		case "Copy":
			m.closeMenus()
			return m.reduce(editor.Event{Command: editor.CopyBlock})
		case "Append":
			m.closeMenus()
			return m.reduce(editor.Event{Command: editor.AppendBlock})
		}
	}
	if item.key.Code == 0 {
		m.historic.message = item.label + " is not yet implemented"
		return m, nil
	}
	m.closeMenus()
	return m.update(tea.KeyPressMsg(tea.Key{Code: item.key.Code, Mod: item.key.Mod}))
}

func (m Model) menuItemVisible(item int) bool {
	row := item + 1
	if m.historic.sub != "" {
		_, childTop := m.childOrigin()
		row += childTop
	}
	return row < m.height-1
}

func (m Model) repeatMenuSearch(command editor.Command) (tea.Model, tea.Cmd) {
	m.closeMenus()
	next, cmd := m.reduce(editor.Event{Command: command})
	m = next.(Model)
	if cmd != nil || m.notice != "" {
		return m, cmd
	}
	if m.session.Snapshot().Draft == "" {
		return m.reduce(editor.Event{Command: editor.F1})
	}
	next, cmd = m.reduce(editor.Event{Command: command})
	m = next.(Model)
	if m.session.Snapshot().Notice == "NOT FOUND" {
		return m.showSearchMiss(cmd)
	}
	return m, cmd
}

func menuTitleX(column int) int {
	x := 0
	for _, menu := range historicMenus[:column] {
		x += len(menu.label) + 1
	}
	return x
}

func (m Model) menuX() int {
	return min(menuTitleX(m.historic.column), max(0, m.width-historicMenus[m.historic.column].width))
}

func (m Model) childOrigin() (int, int) {
	parent := historicMenus[m.historic.column]
	child := historicSubmenus[m.historic.drawnSub]
	return min(m.menuX()+parent.width-2, max(0, m.width-child.width)), 1 + m.historic.parent
}

func (m Model) historicMouse(mouse *tea.Mouse) (tea.Model, tea.Cmd) {
	if mouse == nil || !m.menuAvailable() {
		return m, nil
	}
	if m.historic.files {
		return m.selectFileWithMouse(mouse), nil
	}
	if mouse.Button == tea.MouseRight {
		next, cmd, _ := m.historicPress(hk('=', tea.ModAlt))
		return next, cmd
	}
	if mouse.Button != tea.MouseLeft {
		return m, nil
	}
	if m.showDocumentTabs() && !m.historic.menu && mouse.Y == m.documentTabRow() {
		left := 0
		for _, tab := range m.documentTabLabels() {
			right := left + len(tab.label)
			if mouse.X >= left && mouse.X < right && mouse.X < m.width &&
				tab.screen != m.session.Snapshot().Screen {
				return m.reduce(editor.Event{Command: editor.SwitchDocument, Screen: tab.screen})
			}
			left = right
		}
		return m, nil
	}
	if mouse.Y == 0 && m.menuVisible() {
		for i, menu := range historicMenus {
			x := menuTitleX(i)
			if mouse.X >= x && mouse.X < x+len(menu.label) {
				m.openMenu(i)
				return m, nil
			}
		}
	}
	if m.historic.drop {
		if m.historic.drawnSub != "" {
			child := historicSubmenus[m.historic.drawnSub]
			x, y := m.childOrigin()
			i := mouse.Y - y - 1
			if mouse.X > x && mouse.X < x+child.width-1 && i >= 0 && i < len(child.items) {
				m.historic.sub, m.historic.item = m.historic.drawnSub, i
				return m.activateMenu()
			}
		}
		parent := historicMenus[m.historic.column]
		x, i := m.menuX(), mouse.Y-1
		if mouse.X > x && mouse.X < x+parent.width-1 && i >= 0 && i < len(parent.items) {
			m.historic.sub, m.historic.item = "", i
			m.historic.drawnSub = ""
			return m.activateMenu()
		}
	}
	return m, nil
}

func menuCellText(cells string, mnemonic int, selected bool) string {
	if selected {
		return menuRed + cells + menuGray
	}
	runes := []rune(cells)
	if mnemonic >= 0 && mnemonic < len(runes) {
		return menuGray + string(runes[:mnemonic]) + menuMnemonic + string(runes[mnemonic]) + menuGray + string(runes[mnemonic+1:])
	}
	return menuGray + cells
}

func menuOverlay(lines []string, x, y, width int, text string) {
	if y < 0 || y >= len(lines)-1 {
		return
	}
	old := lines[y]
	left := ansi.Truncate(old, x, "")
	left += strings.Repeat(" ", max(0, x-ansi.StringWidth(left)))
	lines[y] = left + text + screenReset + ansi.TruncateLeft(old, x+width, "")
}

func menuRowCells(item historicItem, width int, selected, selection bool) string {
	if item.label == "" {
		return menuGray + "├" + strings.Repeat("─", width-2) + "┤"
	}
	cells := []rune(item.cells)
	for len(cells) < width-2 {
		cells = append(cells, ' ')
	}
	if len(cells) > width-2 {
		cells = cells[:width-2]
	}
	if item.needsBlock && !selection {
		cells[0], cells[len(cells)-1] = '[', ']'
	}
	return menuGray + "│" + menuCellText(string(cells), item.mnemonic, selected) + "│"
}

func (m Model) paintMenus(lines []string) {
	h := m.historic
	if !m.menuVisible() || m.height < 3 {
		return
	}
	var bar strings.Builder
	for i, menu := range historicMenus {
		bar.WriteString(menuCellText(menu.label, menu.mnemonic, h.menu && h.titleActive && h.column == i))
		bar.WriteByte(' ')
	}
	bar.WriteString("       (Press F3 for Help)")
	lines[0] = bar.String() + menuGray + strings.Repeat(" ", max(0, m.width-ansi.StringWidth(bar.String()))) + screenReset
	if !h.drop {
		return
	}
	selection := m.session.Snapshot().Selection
	parent := historicMenus[h.column]
	for i, item := range parent.items {
		if item.key.Code == tea.KeyF13 {
			state := "Off"
			if m.documentTabs {
				state = "On"
			}
			item.cells = fmt.Sprintf(" Document Tabs %-3s F13", state)
		}
		selected := (h.drawnSub == "" && h.item == i) || (h.drawnSub != "" && h.parent == i)
		menuOverlay(lines, m.menuX(), i+1, parent.width, menuRowCells(item, parent.width, selected, selection))
	}
	menuOverlay(lines, m.menuX(), len(parent.items)+1, parent.width, menuGray+"└"+strings.Repeat("─", parent.width-2)+"┘")
	if h.drawnSub == "" {
		return
	}
	child := historicSubmenus[h.drawnSub]
	x, y := m.childOrigin()
	menuOverlay(lines, x, y, child.width, menuRed+"►"+menuGray+strings.Repeat("─", child.width-2)+"┐")
	for i, item := range child.items {
		menuOverlay(lines, x, y+i+1, child.width, menuRowCells(item, child.width, h.sub != "" && h.item == i, selection))
	}
	menuOverlay(lines, x, y+len(child.items)+1, child.width, menuGray+"└"+strings.Repeat("─", child.width-2)+"┘")
}
