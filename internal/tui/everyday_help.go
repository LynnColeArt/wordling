package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

type helpUI struct {
	active, template bool
	topic            string
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
		m.help.template = !m.help.template
		m.help.topic = ""
	default:
		for _, topic := range everydayHelpTopics {
			if k.Code == topic.input.Code && k.Mod == topic.input.Mod {
				m.help.template = false
				m.help.topic = topic.title
				return m, nil
			}
		}
		if len(k.Text) == 1 && strings.Contains("abcdefghijklmnopqrstuvwxyz", strings.ToLower(k.Text)) {
			m.help.template = false
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
	{"Merge/Sort", "Graphics", "MERGE CODES", "Merge"},
	{"Macro Define", "Macro", "RETRIEVE", "Save"},
	{}, {},
}

func templateKeyRow(first, inset int) []string {
	rows := make([]string, 6)
	for i := range rows {
		rows[i] = strings.Repeat(" ", inset)
	}
	for i, group := range helpTemplateKeys[first : first+4] {
		name := fmt.Sprintf("F%d", first+i+1)
		leader := "┬"
		if i == 0 {
			leader = "┌"
		}
		rows[0] += leader + "─────" + name + strings.Repeat("─", 8-len(name))
		for line, label := range group {
			spaces := 13 - len(label)
			role := ""
			if line == 0 {
				role = revealCode
			} else if line == 1 {
				role = menuGray
			}
			rows[line+1] += "│" + strings.Repeat(" ", spaces/2) + role + label + screenReset + strings.Repeat(" ", spaces-spaces/2)
		}
		leader = "┴"
		if i == 0 {
			leader = "└"
		}
		rows[5] += leader + "─────────────"
	}
	rows[0] += "┐"
	for i := 1; i <= 4; i++ {
		rows[i] += "│"
	}
	rows[5] += "┘"
	return rows
}

func (m Model) helpView() tea.View {
	const footer = "Selection: 0                                      (Press ENTER to exit Help)"
	if m.help.template {
		body := []string{revealCode + "WordPerfect 5.1 Template (Enhanced Layout)" + screenReset, ""}
		first := templateKeyRow(0, 0)
		for i, label := range []string{"Legend:", "Ctrl + Function Key", "Alt + Function Key", "Shift + Function Key", "Function Key alone"} {
			first[i] += "      " + label
		}
		body = append(body, first...)
		body = append(body, "")
		body = append(body, templateKeyRow(4, 10)...)
		body = append(body, "")
		body = append(body, templateKeyRow(8, 21)...)
		return m.historicModalView(body, footer, "")
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
