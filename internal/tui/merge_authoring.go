package tui

import (
	"strings"

	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
)

func mergeAuthoringModal(mode editor.Mode) bool {
	return mode == editor.MergeCodesMode || mode == editor.MergeFieldMode ||
		mode == editor.MergeChoicesMode || mode == editor.MergeOperandMode
}

func (m Model) mergeChoiceVisible(mode editor.Mode) bool {
	if !m.showEditorChrome() {
		return false
	}
	if mode == editor.MergeChoicesMode || mode == editor.MergeOperandMode {
		return m.width >= 40 && m.height >= 13
	}
	return m.width >= 16
}

func (m Model) paintMergeChoices(lines []string) {
	rows, selected, operand := m.session.MergeChoices()
	if len(rows) == 0 || !m.mergeChoiceVisible(m.session.Snapshot().Mode) {
		return
	}
	x := min(40, m.width-40)
	put := func(row int, panel string) {
		left := clip(lines[row], x)
		lines[row] = left + strings.Repeat(" ", max(0, x-ansi.StringWidth(left))) + revealBase + panel + screenReset
	}
	put(0, "╔"+strings.Repeat("═", 38)+"╗")
	for i, line := range rows {
		role := revealBase
		if i == selected {
			role = revealActive
			if operand {
				role = revealCode
			}
		}
		put(i+1, "║"+role+line+strings.Repeat(" ", max(0, 38-len(line)))+revealBase+"║")
	}
	put(len(rows)+1, "╚"+strings.Repeat("═", 38)+"╝")
}

func structuralUndeletePrompt() string {
	return revealCode + "Undelete:" + revealBase + " " + revealCode + "1" + revealBase + " " +
		revealCode + "R" + revealBase + "estore; " + revealCode + "2" + revealBase + " " +
		revealCode + "P" + revealBase + "revious Deletion: " + revealCode + "0" + screenReset
}
