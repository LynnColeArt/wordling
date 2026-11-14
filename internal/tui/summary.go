package tui

import (
	"fmt"
	"github.com/charmbracelet/x/ansi"
	"strings"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/input"
)

const (
	summaryCapture = "Capture Document Summary Fields? No (Yes)"
	summaryDelete  = "Delete Document Summary? No (Yes)"
)

type summaryForm struct {
	open, present, changed bool
	value                  document.Summary
	field                  int
	question               rune
	draft, notice          string
	position               int
	bold, underline        bool
	revised                time.Time
	compose                composeEntry
}

var summaryLabels = []string{
	"1 - Creation Date", "2 - Document Name", "Document Type",
	"3 - Author", "Typist", "4 - Subject", "5 - Account", "6 - Keywords", "7 - Abstract",
}

var summaryRows = []int{4, 6, 7, 9, 10, 12, 14, 16, 18}
var summaryLimits = []int{25, 68, 20, 60, 60, 160, 160, 160, 780}

func (f *summaryForm) values() []*string {
	return []*string{&f.value.Created, &f.value.Name, &f.value.Type, &f.value.Author, &f.value.Typist, &f.value.Subject, &f.value.Account, &f.value.Keywords, &f.value.Abstract}
}

func (m Model) openSummary() Model {
	m.closeMenus()
	d := m.session.Document()
	if d == nil {
		return m
	}
	value, present, err := d.Summary()
	m.summary = summaryForm{open: true, field: -1, value: value, present: present, revised: m.session.SummaryRevisionDate()}
	if err != nil {
		m.summary.notice = err.Error()
	} else if !present {
		m.summary.value = document.NewSummary(time.Now())
	}
	return m
}

func (m Model) summaryPress(k input.Key) (tea.Model, tea.Cmd) {
	f := &m.summary
	if f.field < 0 && f.question == 0 && k.Code == tea.KeyF10 && k.Mod == tea.ModShift && f.notice == "" {
		f.question = tea.KeyF10
		return m, nil
	}
	if f.field > 0 && f.compose.begin(k) {
		return m, nil
	}
	if f.compose.active {
		character, ready, notice := f.compose.press(k)
		f.notice = notice
		if ready {
			f.insertComposed(character.set, character.number)
		}
		return m, nil
	}
	if k.Mod&^tea.ModShift != 0 {
		return m, nil
	}
	if f.question != 0 {
		switch k.Code {
		case 'y', 'Y':
			if f.question == tea.KeyDelete {
				return m.commitSummary(nil)
			}
			f.value = m.session.CaptureSummary(f.value)
			if m.summaryNamesSaved {
				f.value.Author, f.value.Typist = m.summaryAuthor, m.summaryTypist
			}
			f.present, f.changed = true, true
			f.question = 0
		case 'n', 'N', tea.KeyEnter, tea.KeyF1, tea.KeyEscape:
			f.question = 0
		}
		return m, nil
	}
	if f.field >= 0 {
		switch k.Code {
		case tea.KeyF1, tea.KeyEscape:
			f.field = -1
			f.notice = ""
		case tea.KeyEnter, tea.KeyTab:
			if f.bold {
				f.toggleAttribute(12)
			}
			if f.underline {
				f.toggleAttribute(14)
			}
			if f.field == 0 && f.value.Created != f.draft {
				date, err := document.ParseSummaryDate(f.draft)
				if err != nil {
					f.notice = err.Error()
					return m, nil
				}
				f.value.Date = date.Date
				f.draft = date.Created
			}
			f.notice = ""
			value := f.values()[f.field]
			f.changed = f.changed || *value != f.draft
			*value = f.draft
			f.present = f.present || f.changed
			if f.field == 1 || f.field == 3 {
				f.field++
				f.draft = *f.values()[f.field]
				f.position = len(f.draft)
				f.bold, f.underline = false, false
			} else {
				f.field = -1
			}
		case tea.KeyHome:
			f.position = 0
		case tea.KeyEnd:
			f.position = len(f.draft)
		case tea.KeyLeft:
			f.position = f.previous()
		case tea.KeyRight:
			f.position = f.following()
		case tea.KeyBackspace:
			if f.position > 0 {
				previous := f.previous()
				if f.draft[previous] != 0xc3 && f.draft[previous] != 0xc4 {
					f.draft = f.draft[:previous] + f.draft[f.position:]
				}
				f.position = previous
			}
		case tea.KeyDelete:
			if f.position < len(f.draft) {
				next := f.following()
				if f.draft[f.position] != 0xc3 && f.draft[f.position] != 0xc4 {
					f.draft = f.draft[:f.position] + f.draft[next:]
				}
			}
		case tea.KeyF6:
			if f.field >= 3 && f.position == len(f.draft) {
				f.toggleAttribute(12)
			}
		case tea.KeyF8:
			if f.field >= 3 && f.position == len(f.draft) {
				f.toggleAttribute(14)
			}
		default:
			for _, c := range k.Text {
				if c >= 32 && c <= 126 && len(f.draft)+f.reservedBytes() < summaryLimits[f.field] {
					f.draft = f.draft[:f.position] + string(c) + f.draft[f.position:]
					f.position++
				}
			}
		}
		return m, nil
	}
	switch k.Code {
	case tea.KeyEscape, tea.KeyF1:
		m.summary = summaryForm{}
	case tea.KeyDelete:
		if f.present && f.notice == "" {
			f.question = tea.KeyDelete
		}
	case tea.KeyF7:
		if f.changed {
			return m.commitSummary(&f.value)
		}
		m.summary = summaryForm{}
	default:
		if k.Code >= '1' && k.Code <= '7' && f.notice == "" {
			f.field = []int{0, 1, 3, 5, 6, 7, 8}[k.Code-'1']
			f.draft = *f.values()[f.field]
			f.position = len(f.draft)
			f.bold, f.underline = false, false
		}
	}
	return m, nil
}

func (f summaryForm) previous() int {
	previous := 0
	for at := 0; at < f.position; at += document.SummaryOwnerWidth(f.draft[at:]) {
		previous = at
	}
	return previous
}

func (f summaryForm) following() int {
	if f.position == len(f.draft) {
		return f.position
	}
	return f.position + document.SummaryOwnerWidth(f.draft[f.position:])
}

func (f summaryForm) reservedBytes() int {
	size := 0
	if f.bold {
		size += 3
	}
	if f.underline {
		size += 3
	}
	return size
}

func (f *summaryForm) toggleAttribute(attribute byte) {
	active := &f.bold
	if attribute == 14 {
		active = &f.underline
	}
	code := byte(0xc4)
	if !*active {
		if len(f.draft)+f.reservedBytes()+6 > summaryLimits[f.field] {
			return
		}
		code = 0xc3
	}
	f.draft += string([]byte{code, attribute, code})
	f.position = len(f.draft)
	*active = !*active
}

func (f *summaryForm) insertComposed(set, number byte) {
	raw := string(document.CharacterBytes(set, number))
	if len(f.draft)+f.reservedBytes()+len(raw) <= summaryLimits[f.field] {
		f.draft = f.draft[:f.position] + raw + f.draft[f.position:]
		f.position += len(raw)
		f.notice = ""
	}
}

func summaryText(raw string, skip int) string {
	var display strings.Builder
	bold, underline := false, false
	lastRole := ""
	for len(raw) > 0 {
		width := document.SummaryOwnerWidth(raw)
		glyph := " "
		switch width {
		case 3:
			if raw[1] == 12 {
				bold = raw[0] == 0xc3
			}
			if raw[1] == 14 {
				underline = raw[0] == 0xc3
			}
			raw = raw[width:]
			continue
		case 4:
			glyph = document.CharacterGlyph(raw[2], raw[1])
		default:
			if raw[0] >= 32 && raw[0] <= 126 {
				glyph = raw[:1]
			}
		}
		raw = raw[width:]
		if skip > 0 {
			skip--
			continue
		}
		role := revealBase
		switch {
		case bold && underline:
			role = boldUnderline
		case bold:
			role = revealCode
		case underline:
			role = underlined
		}
		if role != lastRole {
			display.WriteString(role)
			lastRole = role
		}
		display.WriteString(glyph)
	}
	if lastRole != "" {
		display.WriteString(screenReset)
	}
	return display.String()
}

func (m Model) commitSummary(value *document.Summary) (tea.Model, tea.Cmd) {
	next, err := m.session.SetSummary(value)
	if err != nil {
		m.summary.notice = err.Error()
		m.summary.question = 0
		return m, nil
	}
	m.session = next
	m.summary = summaryForm{}
	return m, nil
}

func (m Model) summaryView() tea.View {
	f := m.summary
	lines := make([]string, 19)
	lines[0] = "Document Summary"
	lines[2] = "         Revision Date"
	if !f.revised.IsZero() {
		lines[2] += "  " + document.NewSummary(f.revised.Local()).Created
	}
	for i, value := range f.values() {
		label := summaryLabels[i]
		if i == 2 || i == 4 {
			label = "    " + label
		}
		raw, skip := *value, 0
		if f.field == i {
			raw = f.draft
			position := ansi.StringWidth(summaryText(f.draft[:f.position], 0))
			skip = max(0, position-max(0, m.width-24))
		}
		text := summaryText(raw, skip)
		lines[summaryRows[i]] = fmt.Sprintf("     %-18s%s", label, text)
	}
	footer := "Selection: 0                      (Retrieve to capture; Del to remove summary)"
	if f.field >= 0 {
		footer = fmt.Sprintf("Selection: %c", summaryLabels[[]int{0, 1, 1, 3, 3, 5, 6, 7, 8}[f.field]][0])
	}
	if f.question == tea.KeyF10 {
		footer = summaryCapture
	} else if f.question == tea.KeyDelete {
		footer = summaryDelete
	}
	if f.compose.active && f.compose.echo {
		footer = f.compose.prompt()
	}
	v := m.historicModalView(lines, footer, f.notice)
	if f.field >= 0 && summaryRows[f.field] < m.height-1 {
		v.Cursor = tea.NewCursor(min(m.width-1, 23+ansi.StringWidth(summaryText(f.draft[:f.position], 0))), summaryRows[f.field])
	}
	return v
}
