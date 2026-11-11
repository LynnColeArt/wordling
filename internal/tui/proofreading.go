package tui

import (
	"fmt"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

const (
	proofWidth       = 80
	proofHeight      = 25
	proofContextRows = 11
)

type proofRange struct{ start, end int }

func proofHighlighted(ranges []proofRange, index int) bool {
	for _, span := range ranges {
		if index >= span.start && index < span.end {
			return true
		}
	}
	return false
}

func (m Model) proofModal() bool {
	phase := m.session.ProofStatus().Phase
	return phase != editor.ProofInactive && phase != editor.ProofEditing
}

func (m Model) startProof() (tea.Model, tea.Cmd) {
	if !m.runtime.editorChrome {
		m.notice = "Proofreading requires the historical editor"
		return m, nil
	}
	if m.session.ProofStatus().Phase == editor.ProofEditing {
		m.notice = "Press Exit to resume Spell Edit"
		return m, nil
	}
	if err := m.runtime.proofLexiconError; err != nil {
		m.notice = "Proofreading lexicon: " + err.Error()
		return m, nil
	}
	return m.reduce(editor.Event{Command: editor.ProofCtrlF2})
}

func (m Model) proofPress(key input.Key, view editor.ProofView) (tea.Model, tea.Cmd) {
	if key.IsRepeat || view.Phase == editor.ProofDictionaryPending {
		return m, nil
	}
	if view.Phase == editor.ProofCompleteAck {
		return m.reduce(editor.Event{Command: editor.ProofAdvance})
	}
	if (m.width < proofWidth || m.height < proofHeight) && (key.Mod != 0 || key.Code != tea.KeyF1) {
		return m, nil
	}
	if key.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && key.Text != "" {
		if key.Text == "3" && view.Phase == editor.ProofQuestioning &&
			view.Issue == editor.ProofNotFound && view.Dictionary == "" && m.runtime.proofSupplementaryError != nil {
			m.notice = "Supplementary dictionary: " + m.runtime.proofSupplementaryError.Error()
			return m, nil
		}
		return m.reduce(editor.Event{Command: editor.Text, Text: key.Text})
	}
	if key.Mod == 0 {
		switch key.Code {
		case tea.KeyF1:
			return m.reduce(editor.Event{Command: editor.F1})
		case tea.KeyF7:
			return m.reduce(editor.Event{Command: editor.F7})
		case tea.KeyEnter:
			return m.reduce(editor.Event{Command: editor.Enter})
		case tea.KeyBackspace:
			return m.reduce(editor.Event{Command: editor.Backspace})
		}
	}
	return m, nil
}

func (m *Model) prepareProofViewport(wasProof bool) {
	if !m.runtime.editorChrome || m.session.ProofStatus().Phase == editor.ProofInactive || !m.everyday.ready {
		return
	}
	snapshot := m.session.Snapshot()
	if snapshot.Screen < 1 || snapshot.Screen > 2 {
		return
	}
	screen := snapshot.Screen - 1
	if !wasProof {
		m.proofTop[screen] = m.everyday.top[screen]
	}
	row, _, ok := m.everyday.layout.PositionAt(snapshot.Gap)
	if !ok || row < 0 || row >= len(m.everyday.visualRows) {
		return
	}
	rows := proofHeight - 1
	if proofShowsContext(m.session.ProofStatus()) {
		rows = proofContextRows
	}
	m.proofTop[screen] = exposeProofRow(m.proofTop[screen], m.everyday.visualRows[row], rows)
}

func exposeProofRow(top, row, rows int) int {
	return max(0, min(top, row)+max(0, row-min(top, row)-rows+1))
}

func proofShowsContext(view editor.ProofView) bool {
	switch view.Phase {
	case editor.ProofQuestioning, editor.ProofLookupInput, editor.ProofLookupSelection:
		return true
	case editor.ProofDictionaryPending:
		return view.Issue != ""
	default:
		return false
	}
}

func (m Model) proofView(state editor.ProofView) tea.View {
	editing := state.Phase == editor.ProofEditing
	if !editing && (m.width < proofWidth || m.height < proofHeight) {
		lines := []string{"Proofreading active", "Enlarge to 80 × 25 to continue"}
		if state.Phase == editor.ProofCompleteAck {
			lines[1] = "Enlarge to read the count, or press any key"
		}
		return m.makeProofView(lines, nil)
	}
	width, height := proofWidth, proofHeight
	if editing {
		width, height = m.width, m.height
	}
	lines := make([]string, max(height, m.height))
	footer := height - 1
	context := proofShowsContext(state)
	rows := footer
	if context {
		rows = proofContextRows
	}
	snapshot := m.session.Snapshot()
	var cursor *tea.Cursor
	if m.everyday.ready && snapshot.Screen >= 1 && snapshot.Screen <= 2 && rows > 0 {
		var spans []proofRange
		if context && state.Word != "" {
			spans = append(spans, proofRange{state.Start, state.End})
			if state.Issue == editor.ProofDoubleWord {
				spans = append(spans, proofRange{state.PreviousStart, state.PreviousEnd})
			}
		}
		top := m.proofTop[snapshot.Screen-1]
		if line, _, ok := m.everyday.layout.PositionAt(snapshot.Gap); ok && line >= 0 && line < len(m.everyday.visualRows) {
			top = exposeProofRow(top, m.everyday.visualRows[line], rows)
		}
		frame, err := paintEveryday(m.session.Document(), nil, m.everyday.layout, m.everyday.visualRows,
			snapshot.Gap, false, -1, -1, width, top, rows, 0, spans...)
		if err == nil {
			copy(lines, frame.normal)
			cursor = tea.NewCursor(max(0, min(width-1, frame.column)), max(0, min(rows-1, frame.row)))
		} else {
			lines[0] = "Unsupported document presentation"
		}
	}
	if context {
		lines[11] = m.positionStatus(width, snapshot.Name)
		lines[12] = everydayRuler(width, editor.EverydaySettings())
		paintProofSuggestions(lines[14:22], state.Suggestions)
		if state.More {
			lines[22] = "Press " + revealCode + "Enter" + screenReset + " for more words"
		}
	}
	promptCursor := func(x int) {
		cursor = tea.NewCursor(min(width-1, x), footer)
	}
	switch state.Phase {
	case editor.ProofMenu:
		lines[footer] = emphasizeProofActions(state.Prompt, true)
	case editor.ProofQuestioning:
		showDefault := state.Issue == editor.ProofNotFound
		lines[footer] = emphasizeProofActions(state.Prompt, showDefault)
		column := len(state.Prompt)
		if showDefault {
			column += 2
		}
		promptCursor(column)
	case editor.ProofLookupInput, editor.ProofDictionaryName:
		prefix := state.Prompt
		if state.Phase == editor.ProofDictionaryName {
			prefix = "Supplemental dictionary name:"
		}
		lines[footer] = revealCode + prefix + " " + screenReset + state.Draft
		promptCursor(len(prefix) + 1 + state.Caret)
	case editor.ProofLookupSelection:
		lines[footer] = revealCode + "Select Word: 0" + screenReset
		promptCursor(len("Select Word: "))
	case editor.ProofCompleteAck:
		text := fmt.Sprintf("Word count: %d        %s", state.Count, state.Prompt)
		lines[footer] = revealCode + text + screenReset
		promptCursor(len(text))
	case editor.ProofEditing:
		label := revealCode + "Spell Edit:  " + screenReset + "Press " + revealCode + "Exit" + screenReset + " when done"
		lines[footer] = label
		if width >= proofWidth {
			lines[footer] = m.positionStatus(width, label)
		}
	case editor.ProofDictionaryPending:
		lines[footer] = revealCode + "Supplementary dictionary" + screenReset
		cursor = nil
	}
	notice := snapshot.Notice
	if m.notice != "" {
		notice = m.notice
	}
	if notice != "" && footer > 0 {
		lines[footer-1] = notice
	}
	return m.makeProofView(lines, cursor)
}

func (m Model) makeProofView(lines []string, cursor *tea.Cursor) tea.View {
	lines = lines[:min(len(lines), m.height)]
	for i := range lines {
		line := clip(lines[i], m.width)
		line = strings.ReplaceAll(line, screenReset, revealBase)
		pad := max(0, min(m.width, proofWidth)-ansi.StringWidth(line))
		lines[i] = revealBase + line + revealBase + strings.Repeat(" ", pad) + screenReset
	}
	view := tea.NewView(strings.Join(lines, "\n"))
	view.AltScreen = true
	view.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	applyEditorChrome(&view)
	if cursor != nil {
		cursor.Shape = tea.CursorUnderline
		view.Cursor = cursor
	}
	return view
}

func paintProofSuggestions(lines []string, suggestions []string) {
	for row := range lines {
		var line strings.Builder
		for column := 0; column < 3; column++ {
			index := row*3 + column
			if index >= len(suggestions) {
				break
			}
			item := fmt.Sprintf("  %c. %s", 'A'+index, suggestions[index])
			line.WriteString(clip(item, 26))
			if index+1 < len(suggestions) && column < 2 {
				line.WriteString(strings.Repeat(" ", max(0, 26-len(item))))
			}
		}
		lines[row] = line.String()
	}
}

func emphasizeProofActions(prompt string, showDefault bool) string {
	head, options, _ := strings.Cut(prompt, ":")
	var out strings.Builder
	out.WriteString(revealCode + head + ":" + screenReset)
	for i, ch := range options {
		choice := ch >= '1' && ch <= '6' && i > 0 && options[i-1] == ' ' &&
			i+1 < len(options) && options[i+1] == ' '
		mnemonic := head == "Check" && i >= 3 && options[i-3] == ' ' &&
			options[i-2] >= '1' && options[i-2] <= '6' && options[i-1] == ' '
		if choice || mnemonic {
			out.WriteString(revealCode + string(ch) + screenReset)
		} else {
			out.WriteRune(ch)
		}
	}
	if showDefault {
		out.WriteString(": " + revealCode + "0" + screenReset)
	}
	return out.String()
}
