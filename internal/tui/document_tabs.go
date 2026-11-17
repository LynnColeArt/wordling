package tui

import (
	"fmt"
	"strings"

	"github.com/lynncoleart/wordling/internal/editor"
)

type documentTab struct {
	screen uint8
	label  string
}

func (m Model) showDocumentTabs() bool {
	return m.showEditorChrome() && m.width >= editor.MaxDocumentScreens*2 && m.documentTabs &&
		m.session.ProofStatus().Phase == editor.ProofInactive
}

func (m Model) documentTabRow() int {
	if m.historic.bar {
		return 1
	}
	return 0
}

func (m Model) documentTabLabels() []documentTab {
	tabs := make([]documentTab, 0, editor.MaxDocumentScreens)
	for screen := uint8(1); screen <= editor.MaxDocumentScreens; screen++ {
		snapshot, err := m.session.ScreenSnapshot(screen)
		name := snapshot.Name
		if err != nil {
			continue
		}
		if name == "" && snapshot.Dirty && m.recovery.screenIDs[screen-1] != "" {
			name = printableRecoveryLabel(m.recovery.parents[screen-1].Name)
		}
		if name == "" {
			name = "Untitled"
		}
		dirty := ""
		if snapshot.Dirty {
			dirty = "*"
		}
		tabs = append(tabs, documentTab{screen, name + dirty})
	}
	for i, tab := range tabs {
		width := m.width / len(tabs)
		prefix := fmt.Sprintf(" Doc %d", tab.screen)
		if width < 8 {
			prefix = fmt.Sprintf(" %d", tab.screen)
		}
		limit := width - len(prefix) - 2
		name := tab.label
		if limit < 1 {
			if strings.HasSuffix(name, "*") && len(prefix)+1 <= width {
				prefix += "*"
			}
			tabs[i].label = prefix
			continue
		}
		if len(name) > limit {
			if strings.HasSuffix(name, "*") {
				name = name[:limit-1] + "*"
			} else {
				name = name[:limit]
			}
		}
		tabs[i].label = prefix + " " + name + " "
	}
	return tabs
}

func (m Model) documentTabLine() string {
	var line strings.Builder
	active := m.session.Snapshot().Screen
	for _, tab := range m.documentTabLabels() {
		style := menuGray
		if tab.screen == active {
			style = menuRed
		}
		line.WriteString(style + tab.label + screenReset)
	}
	return line.String()
}
