package tui

import (
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type contentsUI struct {
	stage, level, definitionLevels int
	filename                       string
	referenceMode                  int
	origin                         int
	authoritySection               int
	authorityFull                  string
	originRevision                 document.Revision
	compareTyped                   bool
}

func (m Model) openContents(level bool) Model {
	m.closeMenus()
	m.contents = contentsUI{stage: contentsMark}
	if level {
		m.contents.stage = contentsLevel
	}
	return m
}

const (
	contentsMark = iota + 1
	contentsLevel
	contentsDefineMenu
	contentsDefinition
	contentsDefinitionLevels
	contentsGenerate
	contentsConfirm
	contentsCompare
	contentsSubdocument
	contentsReference
	contentsReferenceType
	contentsReferencePosition
	contentsReferenceName
	contentsAuthoritySection
	contentsAuthorityFull
	contentsAuthorityShort
	contentsRemoveComparison
)

func (m Model) contentsPress(key input.Key) (tea.Model, tea.Cmd) {
	menu := &m.contents
	if key.IsRepeat || key.Mod != 0 && menu.stage != contentsReferencePosition && ((menu.stage != contentsRemoveComparison && menu.stage != contentsCompare && menu.stage != contentsSubdocument && menu.stage != contentsReferenceName && menu.stage != contentsAuthorityFull && menu.stage != contentsAuthorityShort) || key.Mod & ^(tea.ModShift|tea.ModCapsLock) != 0) {
		return m, nil
	}
	if key.Code == tea.KeyEscape || key.Code == tea.KeyF1 {
		m.contents, m.notice = contentsUI{}, ""
		return m, nil
	}
	var apply func() (editor.Session, error)
	switch menu.stage {
	case contentsMark:
		switch key.Code {
		case '1':
			if m.session.Snapshot().Selection {
				menu.stage = contentsLevel
			} else {
				menu.stage = contentsReference
			}
		case '2':
			if !m.session.Snapshot().Selection {
				menu.stage = contentsSubdocument
			}
		case '4':
			if m.session.Snapshot().Selection {
				menu.stage = contentsAuthoritySection
			}
		case '5':
			if !m.session.Snapshot().Selection {
				menu.stage = contentsDefineMenu
			}
		case '6':
			if !m.session.Snapshot().Selection {
				menu.stage = contentsGenerate
			}
		}
	case contentsAuthoritySection:
		switch key.Code {
		case tea.KeyBackspace:
			if len(menu.filename) > 0 {
				menu.filename = menu.filename[:len(menu.filename)-1]
			}
		case tea.KeyEnter:
			section, err := strconv.Atoi(menu.filename)
			if err != nil || section < 1 || section > 16 {
				m.notice = "Enter a section number from 1 to 16"
				return m, nil
			}
			citation, err := m.session.AuthoritySelection()
			if err != nil {
				m.notice = err.Error()
				return m, nil
			}
			menu.stage, menu.authoritySection, menu.filename, m.notice = contentsAuthorityFull, section, citation, ""
		default:
			if len(menu.filename)+len(key.Text) <= 2 && strings.Trim(key.Text, "0123456789") == "" {
				menu.filename += key.Text
			}
		}
	case contentsAuthorityFull, contentsAuthorityShort:
		switch key.Code {
		case tea.KeyF7:
			if menu.stage == contentsAuthorityFull {
				menu.stage, menu.authorityFull = contentsAuthorityShort, menu.filename
				return m, nil
			}
		case tea.KeyEnter:
			if menu.stage == contentsAuthorityShort {
				apply = func() (editor.Session, error) {
					return m.session.MarkAuthority(menu.authoritySection, menu.filename, menu.authorityFull)
				}
			}
		case tea.KeyBackspace:
			if len(menu.filename) > 0 {
				menu.filename = menu.filename[:len(menu.filename)-1]
			}
		default:
			if len(menu.filename)+len(key.Text) <= 255 && strings.IndexFunc(key.Text, func(ch rune) bool { return ch < 32 || ch > 126 }) < 0 {
				menu.filename += key.Text
			}
		}
	case contentsReference:
		switch key.Code {
		case '1', '2', '3':
			menu.referenceMode = int(key.Code - '0')
			menu.origin = -1
			menu.stage = contentsReferenceType
			if menu.referenceMode == 2 {
				menu.stage = contentsReferenceName
			}
		}
	case contentsReferenceType:
		if key.Code == '1' {
			menu.stage = contentsReferenceName
			if menu.referenceMode == 3 {
				snap := m.session.Snapshot()
				menu.origin, menu.originRevision = snap.Gap, snap.NativeRevision
				menu.stage = contentsReferencePosition
			}
		}
	case contentsReferencePosition:
		if key.Code == tea.KeyEnter && key.Mod == 0 {
			menu.stage = contentsReferenceName
			return m, nil
		}
		switch key.Code {
		case tea.KeyUp, tea.KeyDown, tea.KeyLeft, tea.KeyRight, tea.KeyHome, tea.KeyEnd, tea.KeyPgUp, tea.KeyPgDown:
			event, ok := resolve(key, editor.Editing)
			if ok && event.Command != editor.Text {
				event.ViewportColumns = m.width
				return m.reduce(event)
			}
		}
		return m, nil
	case contentsReferenceName:
		switch key.Code {
		case tea.KeyBackspace:
			if len(menu.filename) > 0 {
				menu.filename = menu.filename[:len(menu.filename)-1]
			}
		case tea.KeyEnter:
			apply = func() (editor.Session, error) {
				return m.session.MarkPageReference(menu.filename, menu.referenceMode == 2, menu.originRevision, menu.origin)
			}
		default:
			if len(menu.filename)+len(key.Text) <= 40 && strings.IndexFunc(key.Text, func(ch rune) bool { return ch < 32 || ch > 126 }) < 0 {
				menu.filename += strings.ToUpper(key.Text)
			}
		}
	case contentsSubdocument:
		switch key.Code {
		case tea.KeyBackspace:
			if len(menu.filename) > 0 {
				menu.filename = menu.filename[:len(menu.filename)-1]
			}
		case tea.KeyEnter:
			apply = func() (editor.Session, error) { return m.session.InsertSubdocument(menu.filename) }
		default:
			if len(menu.filename)+len(key.Text) <= 127 && strings.IndexFunc(key.Text, func(ch rune) bool { return ch < 32 || ch > 126 }) < 0 {
				menu.filename += key.Text
			}
		}
	case contentsLevel:
		switch key.Code {
		case tea.KeyBackspace:
			menu.level = 0
		case tea.KeyEnter:
			if menu.level > 0 {
				apply = func() (editor.Session, error) { return m.session.MarkContents(menu.level) }
			}
		default:
			if key.Code >= '1' && key.Code <= '5' {
				menu.level = int(key.Code - '0')
			}
		}
	case contentsDefineMenu:
		if key.Code == '1' {
			menu.stage, menu.definitionLevels = contentsDefinition, 1
		}
	case contentsDefinition:
		if key.Code == '1' {
			menu.stage = contentsDefinitionLevels
		} else if key.Code == tea.KeyF7 {
			apply = func() (editor.Session, error) { return m.session.DefineContents(menu.definitionLevels) }
		}
	case contentsDefinitionLevels:
		if key.Code == '1' || key.Code == '2' {
			menu.definitionLevels, menu.stage = int(key.Code-'0'), contentsDefinition
		}
	case contentsGenerate:
		switch key.Code {
		case '1':
			menu.stage = contentsRemoveComparison
		case '2':
			menu.stage, menu.filename = contentsCompare, m.session.Snapshot().Name
		case '5':
			menu.stage = contentsConfirm
		}
	case contentsCompare:
		switch key.Code {
		case tea.KeyEnter:
			apply = func() (editor.Session, error) { return m.session.CompareDisk(menu.filename) }
		case tea.KeyBackspace:
			if len(menu.filename) > 0 {
				menu.filename = menu.filename[:len(menu.filename)-1]
			}
		default:
			if key.Text != "" && len(key.Text) <= 80 && strings.IndexFunc(key.Text, func(c rune) bool { return c < 32 || c > 126 }) < 0 {
				if !menu.compareTyped {
					menu.filename = ""
				}
				if len(menu.filename)+len(key.Text) <= 80 {
					menu.filename += key.Text
					menu.compareTyped = true
				}
			}
		}
	case contentsRemoveComparison:
		switch key.Code {
		case 'y', 'Y':
			apply = m.session.RemoveComparisonMarks
		case 'n', 'N', tea.KeyEnter:
			m.contents = contentsUI{}
		}
	case contentsConfirm:
		switch key.Code {
		case 'y', 'Y':
			apply = m.session.GenerateContents
		case 'n', 'N', tea.KeyEnter:
			m.contents = contentsUI{}
		}
	}
	if apply != nil {
		next, err := apply()
		if err != nil {
			m.notice = err.Error()
			return m, nil
		}
		m.session, m.contents, m.notice = next, contentsUI{}, ""
	} else if key.Code == tea.KeyF7 {
		m.contents = contentsUI{}
	}
	return m, nil
}

func (m Model) contentsView(view tea.View) tea.View {
	prompt := "Mark for: 1 ToC; 2 List; 3 Index; 4 ToA: 0"
	switch m.contents.stage {
	case contentsMark:
		if !m.session.Snapshot().Selection {
			prompt = "1 Cross-Ref; 2 Subdoc; 3 Index; 4 ToA Short Form; 5 Define; 6 Generate: 0"
		}
	case contentsAuthoritySection:
		prompt = "ToA Section Number (Press Enter for Short Form only): " + m.contents.filename
	case contentsAuthorityFull:
		return m.historicModalView([]string{m.contents.filename}, "ToA Full Form:  Press Exit when done", m.notice)
	case contentsAuthorityShort:
		prompt = "Short Form: " + m.contents.filename
	case contentsReference:
		return m.historicModalView([]string{"Mark Text: Cross-Reference", "", "     1 - Mark Reference", "", "     2 - Mark Target", "", "     3 - Mark Both Reference and Target"}, "Selection: 0", m.notice)
	case contentsReferenceType:
		return m.historicModalView([]string{"Tie Reference to:", "", "     1 - Page Number", "", "     2 - Paragraph/Outline Number", "", "     3 - Footnote Number", "", "     4 - Endnote Number", "", "     5 - Graphics Box Number"}, "Selection: 0", m.notice)
	case contentsReferencePosition:
		prompt = "Cross-Ref:  Move to page; Press Enter."
	case contentsReferenceName:
		prompt = "Target Name: " + m.contents.filename
	case contentsSubdocument:
		prompt = "Subdoc Filename: " + m.contents.filename
	case contentsLevel:
		prompt = "ToC Level:"
		if m.contents.level > 0 {
			prompt += " " + strconv.Itoa(m.contents.level)
		}
	case contentsDefineMenu:
		prompt = "Define: 1 Table of Contents; 2 List; 3 Index; 4 Table of Authorities: 0"
	case contentsDefinition, contentsDefinitionLevels:
		return m.historicModalView([]string{"Table of Contents Definition", "", "     1 - Number of Levels          " + strconv.Itoa(m.contents.definitionLevels),
			"", "     2 - Display Last Level in     No", "           Wrapped Format", "", "     3 - Page Numbering - Level 1  Flush right with leader",
			"                          Level 2", "                          Level 3", "                          Level 4", "                          Level 5"},
			"Selection: 0", m.notice)
	case contentsGenerate, contentsConfirm, contentsCompare, contentsRemoveComparison:
		prompt = "Selection: 0"
		if m.contents.stage == contentsRemoveComparison {
			prompt = "Remove redline markings and strikeout text? No (Yes)"
		}
		if m.contents.stage == contentsCompare {
			prompt = "Other Document: " + m.contents.filename
		}
		if m.contents.stage == contentsConfirm {
			prompt = "Existing tables, lists, and indexes will be replaced.  Continue? Yes (No)"
		}
		return m.historicModalView([]string{"Mark Text: Generate", "",
			"     1 - Remove Redline Markings and Strikeout Text from Document", "", "     2 - Compare Screen and Disk Documents and Add Redline and Strikeout",
			"", "     3 - Expand Master Document", "", "     4 - Condense Master Document", "", "     5 - Generate Tables, Indexes, Cross-References, etc."}, prompt, m.notice)
	}
	lines := strings.Split(view.Content, "\n")
	row := len(lines) - 1
	if m.notice != "" && row > 0 {
		lines[row-1] = clip(m.notice, m.width)
	}
	lines[row] = clip(prompt, m.width)
	view.Content = strings.Join(lines, "\n")
	view.Cursor = tea.NewCursor(min(m.width-1, len(prompt)), row)
	return view
}
