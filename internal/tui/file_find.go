package tui

import (
	"bytes"
	"fmt"
	"strings"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/layout"
	"github.com/lynncoleart/wordling/internal/storage"
)

const findMenuPrompt = "Find: 1 Name; 2 Doc Summary; 3 First Pg; 4 Entire Doc; 5 Conditions; 6 Undo: "

type fileFindMissExpired struct{ result *storage.Listing }

func (b *fileBrowser) findPress(k input.Key, cancel bool) tea.Cmd {
	if b.findMiss != nil {
		return nil
	}
	if cancel {
		if b.phase == fileFindText && b.findConditions {
			b.phase = fileFindConditions
			return nil
		}
		b.findConditions = false
		b.phase, b.message = fileListing, ""
		return nil
	}
	if b.phase == fileFindConditions {
		switch k.Code {
		case '1':
			// The original treats a blank revision upper bound as an empty date.
			// A blank lower bound allows files through the entered upper bound.
			revisionFromOnly := b.findTerms[3] != "" && b.findTerms[4] == ""
			var patterns [15]findPattern
			for i, term := range b.findTerms {
				if term == "" || isFindDate(i) {
					continue
				}
				pattern, err := compileFindPattern(term, false)
				if err != nil {
					b.message = err.Error()
					return nil
				}
				patterns[i] = pattern
			}
			result := b.filterFind(func(selection *storage.EntrySelection) bool {
				if revisionFromOnly {
					return false
				}
				for i, term := range b.findTerms {
					if term != "" && !matchesFindCondition(selection, i, term, patterns[i]) {
						return false
					}
				}
				return true
			})
			if result.Metrics().Entries == 0 {
				b.findMiss = result
				b.message = "* Not found *"
				return tea.Tick(time.Second, func(time.Time) tea.Msg { return fileFindMissExpired{result} })
			} else {
				b.applyFind(result)
				b.findConditions = false
			}
		case '2':
			b.findTerms = [15]string{}
			b.message = ""
		case tea.KeyUp:
			b.findField = (b.findField + len(b.findTerms) - 1) % len(b.findTerms)
		case tea.KeyDown:
			b.findField = (b.findField + 1) % len(b.findTerms)
		case '3', '4', '5', tea.KeyEnter:
			switch k.Code {
			case '3':
				b.findField = 3
			case '4':
				if b.findField > 2 {
					b.findField = 0
				}
			case '5':
				b.findField = 5
			}
			b.phase, b.draft, b.touched = fileFindText, b.findTerms[b.findField], false
		}
		return nil
	}
	if b.phase == fileFindMenu {
		switch k.Code {
		case '1', '2', '3', '4':
			b.findScope = k.Code
			b.phase, b.draft, b.touched = fileFindText, "", true
		case '5':
			b.phase, b.findConditions, b.findField = fileFindConditions, true, 0
		case '6':
			if b.findHistory[0] != nil {
				b.list, b.marked = b.findHistory[0], b.findMarkHistory[0]
				copy(b.findMarkHistory[:], b.findMarkHistory[1:])
				b.findMarkHistory[len(b.findMarkHistory)-1] = nil
				copy(b.findHistory[:], b.findHistory[1:])
				b.findHistory[len(b.findHistory)-1] = nil
				b.entries = b.list.Entries()
			}
			b.phase, b.selected, b.first = fileListing, 0, 0
		}
		return nil
	}
	if b.findConditions && (k.Code == tea.KeyUp || k.Code == tea.KeyDown) {
		if !b.commitFindTerm() {
			return nil
		}
		direction := 1
		if k.Code == tea.KeyUp {
			direction = -1
		}
		b.findField = (b.findField + len(b.findTerms) + direction) % len(b.findTerms)
		b.draft, b.touched = b.findTerms[b.findField], false
		return nil
	}
	switch k.Code {
	case tea.KeyBackspace:
		if len(b.draft) > 0 {
			b.draft = b.draft[:len(b.draft)-1]
			b.touched = true
		}
	case tea.KeyEnter:
		if b.findConditions {
			if b.commitFindTerm() {
				b.phase = fileFindConditions
			}
			return nil
		}
		query, err := compileFindPattern(b.draft, b.findScope == '1')
		if err != nil {
			b.message = err.Error()
			return nil
		}
		if len(query) > 0 {
			b.applyFind(b.filterFind(func(selection *storage.EntrySelection) bool {
				return matchesFile(selection, b.findScope, query)
			}))
		}
	default:
		b.addDraft(k.Text)
	}
	return nil
}

func (b *fileBrowser) commitFindTerm() bool {
	term := strings.TrimSpace(b.draft)
	if isFindDate(b.findField) && term != "" {
		if _, err := parseFindDate(term); err != nil {
			b.message = "Enter a date as MM-DD-YY or MM/DD/YYYY"
			return false
		}
	}
	b.message = ""
	b.findTerms[b.findField] = term
	return true
}

func matchesFile(selection *storage.EntrySelection, scope rune, query findPattern) bool {
	if scope == '1' {
		return query.matches(bytes.ToLower([]byte(selection.Name())))
	}
	raw, err := selection.ReadDOSBytes()
	if err != nil {
		return false
	}
	if !bytes.HasPrefix(raw, []byte("\xffWPC")) {
		if scope == '2' {
			return false
		}
		raw, _, _ = bytes.Cut(raw, []byte{0x1a})
		if scope == '3' {
			raw, _, _ = bytes.Cut(raw, []byte{'\f'})
			raw = raw[:min(4000, len(raw))]
		}
		return query.matches([]byte(strings.ToLower(strings.Join(strings.Fields(string(raw)), " "))))
	}
	native, err := document.Parse(raw)
	if err != nil {
		return false
	}
	if scope == '2' {
		summary, ok, err := native.Summary()
		if !ok || err != nil {
			return false
		}
		return query.matches(findSummaryText(summary.Name), findSummaryText(summary.Type), findSummaryText(summary.Subject),
			findSummaryText(summary.Author), findSummaryText(summary.Typist), findSummaryText(summary.Abstract),
			findSummaryText(summary.Account), findSummaryText(summary.Keywords))
	}
	limit := native.TokenCount()
	if scope == '3' {
		pages, err := layout.FromDocument(native, editor.EverydaySettings())
		if err != nil {
			return false
		}
		for _, line := range pages.Lines {
			if line.Page > 1 {
				limit = line.StartGap
				break
			}
		}
		limit = min(limit, 4000)
	}
	var text strings.Builder
	for i := 0; i < limit; i++ {
		token, err := native.Token(i)
		if err != nil {
			return false
		}
		if token.Kind.IsCharacter() {
			text.WriteString(token.CharacterText())
			continue
		}
		switch token.Kind {
		case document.SoftReturn, document.SoftPage, document.Tab, document.HardReturn, document.HardReturnSoftPage, document.HardPage:
			text.WriteByte(' ')
		}
	}
	return query.matches([]byte(strings.ToLower(text.String())))
}

func (b *fileBrowser) applyFind(result *storage.Listing) {
	copy(b.findHistory[1:], b.findHistory[:])
	copy(b.findMarkHistory[1:], b.findMarkHistory[:])
	b.findMarkHistory[0], b.marked = b.marked, nil
	b.findHistory[0], b.list = b.list, result
	b.entries = b.list.Entries()
	b.phase, b.selected, b.first, b.message = fileListing, 0, 0, ""
}

var findConditionLabels = [...]string{
	"     4 - Text - Document Summary", "                First Page", "                Entire Document",
	"     3 - Revision Date - From", "                         To",
	"         Creation Date - From", "                         To",
	"         Document Name", "         Document Type", "         Author", "         Typist",
	"         Subject", "         Account", "         Keywords", "         Abstract",
}

func isFindDate(field int) bool { return field >= 3 && field <= 6 }

func parseFindDate(value string) (time.Time, error) {
	value = strings.ReplaceAll(value, "/", "-")
	date, err := time.Parse("1-2-06", value)
	if err == nil {
		return date, nil
	}
	return time.Parse("1-2-2006", value)
}

func matchesFindCondition(selection *storage.EntrySelection, field int, term string, pattern findPattern) bool {
	if field < 3 {
		return matchesFile(selection, rune('2'+field), pattern)
	}
	if isFindDate(field) {
		bound, err := parseFindDate(term)
		if err != nil {
			return false
		}
		date := selection.Entry().Modified
		if field >= 5 {
			summary, ok := findSummary(selection)
			if !ok {
				return false
			}
			date, err = time.Parse("01-02-06", strings.SplitN(summary.Created, " ", 2)[0])
			if err != nil {
				return false
			}
		}
		date = time.Date(date.Year(), date.Month(), date.Day(), 0, 0, 0, 0, time.UTC)
		if field == 5 {
			return date.After(bound)
		}
		if field == 3 {
			return !date.Before(bound)
		}
		return !date.After(bound)
	}
	summary, ok := findSummary(selection)
	if !ok {
		return false
	}
	fields := [...]string{summary.Name, summary.Type, summary.Author, summary.Typist, summary.Subject, summary.Account, summary.Keywords, summary.Abstract}
	return pattern.matches(findSummaryText(fields[field-7]))
}

func findSummary(selection *storage.EntrySelection) (document.Summary, bool) {
	stored, err := selection.Read()
	if err != nil {
		return document.Summary{}, false
	}
	doc, err := document.Parse(stored.Export())
	if err != nil {
		return document.Summary{}, false
	}
	summary, ok, err := doc.Summary()
	return summary, ok && err == nil
}

var findConditionRows = [...]int{8, 9, 10, 5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}

func (b *fileBrowser) drawFindConditions(lines []string) {
	lines[0] = fmt.Sprintf("Find: Conditions                                     Files Selected: %3d", len(b.entries))
	lines[2] = "     1 - Perform Search"
	lines[3] = "     2 - Reset Conditions"
	lines[12] = "     5 - Document Summary"
	for i, label := range findConditionLabels {
		row := findConditionRows[i]
		if row >= len(lines)-2 {
			continue
		}
		value := b.findTerms[i]
		if i == b.findField {
			if b.phase == fileFindText {
				value = b.draft
			}
			value = fileHighlight(value)
		}
		lines[row] = fmt.Sprintf("%-34s %s", label, value)
	}
	if b.message != "" {
		lines[len(lines)-2] = b.message
	}
	lines[len(lines)-1] = "Selection: 1"
}

func findSummaryText(raw string) []byte {
	var result strings.Builder
	for len(raw) > 0 {
		width := document.SummaryOwnerWidth(raw)
		switch width {
		case 4:
			result.WriteString(document.CharacterGlyph(raw[2], raw[1]))
		case 1:
			result.WriteByte(raw[0])
		}
		raw = raw[width:]
	}
	return []byte(strings.ToLower(result.String()))
}

// Marks limit the current search only when a marked file is in the listing.
func (b *fileBrowser) filterFind(match func(*storage.EntrySelection) bool) *storage.Listing {
	markedOnly := false
	for _, entry := range b.entries {
		if b.marked[entry.Name] {
			markedOnly = true
			break
		}
	}
	return b.list.Filter(func(selection *storage.EntrySelection) bool {
		return (!markedOnly || b.marked[selection.Name()]) && match(selection)
	})
}
