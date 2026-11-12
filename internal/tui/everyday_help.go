package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/input"
)

type helpUI struct {
	active, template, ibm bool
	topic                 string
}

type helpTopic struct {
	title, key, text string
	input            input.Key
}

var everydayHelpTopics = []helpTopic{
	{"Save", "F10", "Save the document in its native format. Supply the filename and answer any replacement question.", hk(tea.KeyF10, 0)},
	{"Retrieve", "Shift-F10", "Enter a document name, or use List Files to choose it.", hk(tea.KeyF10, tea.ModShift)},
	{"Search", "F2", "Enter the text to find. Press F2 to search forward or Shift-F2 to search backward.", hk(tea.KeyF2, 0)},
	{"Backward Search", "Shift-F2", "Find matching text before the current position.", hk(tea.KeyF2, tea.ModShift)},
	{"Bold on/off", "F6", "Start or end Bold at the cursor. Reveal Codes displays both native boundaries.", hk(tea.KeyF6, 0)},
	{"Underline on/off", "F8", "Start or end Underline at the cursor.", hk(tea.KeyF8, 0)},
	{"Reveal Codes", "Alt-F3", "Show the native formatting codes below the document. Press Alt-F3 again to close the lower pane.", hk(tea.KeyF3, tea.ModAlt)},
	{"List", "F5", "Confirm the directory pattern, then choose a file to Look at or Retrieve.", hk(tea.KeyF5, 0)},
	{"Cancel / Undelete", "F1", "Cancel the active prompt or review earlier deletions while editing.", hk(tea.KeyF1, 0)},
	{"Exit", "F7", "Leave the current screen. From editing, answer the save and exit questions.", hk(tea.KeyF7, 0)},
	{"Setup", "Shift-F1", "Change the document and display preferences.", hk(tea.KeyF1, tea.ModShift)},
}

func (m Model) openHelp(template bool) Model {
	m.help = helpUI{active: true, template: template}
	return m
}

func (m Model) helpPress(k input.Key) (tea.Model, tea.Cmd) {
	switch {
	case k.Mod == 0 && (k.Code == tea.KeyEnter || k.Code == tea.KeyEscape || k.Code == tea.KeyF7):
		m.help = helpUI{}
	case k.Mod == 0 && k.Code == tea.KeyF3:
		m.help.template, m.help.ibm, m.help.topic = true, false, ""
	case k.Mod == 0 && k.Code == '1' && m.help.template:
		if m.help.ibm {
			m.help.template, m.help.ibm = false, false
		} else {
			m.help.ibm = true
		}
	default:
		for _, topic := range everydayHelpTopics {
			if k.Code == topic.input.Code && k.Mod == topic.input.Mod {
				m.help.template, m.help.ibm = false, false
				m.help.topic = topic.title
				return m, nil
			}
		}
		if len(k.Text) == 1 && strings.Contains("abcdefghijklmnopqrstuvwxyz", strings.ToLower(k.Text)) {
			m.help.template, m.help.ibm = false, false
			m.help.topic = strings.ToUpper(k.Text)
		}
	}
	return m, nil
}

// The four rows list the original Ctrl, Alt, Shift and unmodified functions.
var helpTemplateKeys = [12][4]string{
	{"Shell", "Thesaurus", "SETUP", "Cancel"},
	{"Spell", "Replace", "<-SEARCH", "->Search"},
	{"Screen", "Reveal Codes", "SWITCH", "Help"},
	{"Move", "Block", "->INDENT<-", "->Indent"},
	{"Text In/Out", "Mark Text", "DATE/OUTLINE", "List"},
	{"Tab Align", "Flush Right", "CENTER", "Bold"},
	{"Footnote", "Columns/Table", "PRINT", "Exit"},
	{"Font", "Style", "FORMAT", "Underline"},
	{"Merge/Sort", "Graphics", "MERGE CODES", "End Field"},
	{"Macro Define", "Macro", "RETRIEVE", "Save"},
	{"", "", "", "Reveal Codes"},
	{"", "", "", "Block"},
}

// The DOS tables center some odd-length labels toward the right and
// others toward the left. Keep the measured leading cells for each modifier.
var enhancedTemplatePadding = [12][4]int{
	{4, 2, 4, 3}, {4, 3, 2, 2}, {3, 0, 3, 4}, {5, 4, 1, 2},
	{1, 2, 0, 5}, {2, 1, 3, 4}, {2, 0, 4, 4}, {4, 4, 3, 2},
	{1, 2, 1, 2}, {0, 4, 2, 4}, {0, 0, 0, 0}, {0, 0, 0, 4},
}

var ibmTemplatePadding = [10][4]int{
	{6, 6, 4, 5}, {6, 4, 5, 4}, {5, 5, 2, 6}, {6, 3, 6, 4},
	{3, 2, 4, 6}, {4, 5, 3, 6}, {4, 6, 2, 6}, {6, 5, 6, 4},
	{3, 3, 4, 4}, {2, 4, 6, 6},
}

var templateModifierRoles = [4]string{revealCode, menuGray, "", ""}

func templateCell(label, fill string, leading, width, modifier int) string {
	cell := strings.Repeat(fill, leading)
	if role := templateModifierRoles[modifier]; role != "" && label != "" {
		cell += role + label + screenReset
	} else {
		cell += label
	}
	return cell + strings.Repeat(fill, width-leading-len(label))
}

func templateLegend(row, label string, column int, role string) string {
	row += strings.Repeat(" ", max(0, column-ansi.StringWidth(row)))
	if role != "" {
		return row + role + label + screenReset
	}
	return row + label
}

func enhancedKeyboardTemplate() []string {
	rows := make([]string, 24)
	rows[0] = revealCode + "WordPerfect 5.1 Template (Enhanced Layout)" + screenReset
	for group := range 3 {
		x, y := group*11, group*7+2
		for line := range 6 {
			rows[y+line] = strings.Repeat(" ", x)
		}
		if group > 0 {
			rows[y], rows[y+5] = strings.Repeat(" ", x-1)+"─", strings.Repeat(" ", x-1)+"─"
		}
		for column := range 4 {
			key := group*4 + column
			name := fmt.Sprintf("F%d", key+1)
			top, bottom := "┬", "┴"
			if group == 0 && column == 0 {
				top, bottom = "┌", "└"
			}
			leading := 5
			if group < 2 && (column == 1 || column == 2) {
				leading = 6
			}
			rows[y] += top + strings.Repeat("─", leading) + name + strings.Repeat("─", 13-leading-len(name))
			rows[y+5] += bottom + strings.Repeat("─", 13)
			for modifier, label := range helpTemplateKeys[key] {
				rows[y+modifier+1] += "│" + templateCell(label, " ", enhancedTemplatePadding[key][modifier], 13, modifier)
			}
		}
		if group < 2 {
			rows[y] += "┬─"
			rows[y+5] += "┴─"
		} else {
			rows[y] += "┐"
			rows[y+5] += "┘"
		}
		for modifier := range 4 {
			rows[y+modifier+1] += "│"
		}
	}
	rows[2] = templateLegend(rows[2], "Legend:", 64, "")
	rows[3] = templateLegend(rows[3], "Ctrl + Function Key", 60, revealCode)
	rows[4] = templateLegend(rows[4], "Alt + Function Key", 61, menuGray)
	rows[5] = templateLegend(rows[5], "SHIFT + FUNCTION KEY", 59, "")
	rows[6] = templateLegend(rows[6], "Function Key alone", 61, "")
	rows[23] = revealCode + "Press 1 to view the PC/XT keyboard template" + screenReset
	return rows
}

func ibmKeyboardTemplate() []string {
	const inset = "       "
	rows := make([]string, 24)
	rows[0] = inset + revealCode + "WordPerfect 5.1 Template (IBM Layout)" + screenReset
	rows[2] = inset + "╔" + strings.Repeat("═", 17) + "╤" + strings.Repeat("═", 17) + "╗"
	for pair := range 5 {
		left, right := pair*2, pair*2+1
		for line, modifier := range [4]int{0, 2, 1, 3} {
			before, after, fill := inset, "", " "
			if line == 1 {
				before = fmt.Sprintf("     F%d", left+1)
				after = fmt.Sprintf("F%d", right+1)
			}
			if line == 3 && pair < 4 {
				fill = "_"
			}
			rows[3+pair*4+line] = before + "║" +
				templateCell(helpTemplateKeys[left][modifier], fill, ibmTemplatePadding[left][line], 17, modifier) + "│" +
				templateCell(helpTemplateKeys[right][modifier], fill, ibmTemplatePadding[right][line], 17, modifier) + "║" + after
		}
	}
	rows[7] = templateLegend(rows[7], "Legend:", 58, "")
	rows[9] = templateLegend(rows[9], "Ctrl + Function Key", 54, revealCode)
	rows[10] = templateLegend(rows[10], "SHIFT + FUNCTION KEY", 53, "")
	rows[11] = templateLegend(rows[11], "Alt + Function Key", 55, menuGray)
	rows[12] = templateLegend(rows[12], "Function Key alone", 55, "")
	rows[23] = inset + "╚" + strings.Repeat("═", 17) + "╧" + strings.Repeat("═", 17) + "╝"
	return rows
}

func (m Model) helpView() tea.View {
	const footer = "Selection: 0                                      (Press ENTER to exit Help)"
	if m.help.template {
		if m.help.ibm {
			return m.historicModalView(ibmKeyboardTemplate(), footer, "")
		}
		return m.historicModalView(enhancedKeyboardTemplate(), footer, "")
	}
	body := []string{revealCode + "Help" + screenReset + "                                                   WP 5.1   03/09/92", "", ""}
	if m.help.topic == "" {
		body = append(body, "     Press a letter for the alphabetical feature list.", "",
			"     Press a function key for information about that command.", "",
			"     Press Help again for the keyboard template.")
	} else if len(m.help.topic) == 1 || m.help.topic == "Index" {
		body = append(body, "     Features: "+m.help.topic, "")
		for _, topic := range everydayHelpTopics {
			if m.help.topic == "Index" || strings.HasPrefix(strings.ToUpper(topic.title), m.help.topic) {
				body = append(body, "     "+topic.title+"  "+topic.key)
			}
		}
	} else {
		for _, topic := range everydayHelpTopics {
			if m.help.topic == topic.title {
				body[0] = revealCode + topic.title + screenReset
				body[2] = "     " + topic.text
				body = append(body, "", "     "+topic.key)
				break
			}
		}
	}
	return m.historicModalView(body, footer, "")
}
