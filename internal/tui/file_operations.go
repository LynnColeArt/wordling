package tui

import (
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

func (b *fileBrowser) beginOperation(key rune) {
	if b.selected < 2 || b.selected-2 >= len(b.entries) ||
		!b.entries[b.selected-2].Supported || !b.entries[b.selected-2].Mode.IsRegular() {
		b.message = "Select a supported regular file"
		return
	}
	b.draft, b.touched = "", false
	switch key {
	case '2':
		b.phase = fileDelete
	case '3':
		b.phase = fileRename
		b.draft = filePath(b.directory, b.entries[b.selected-2].DOSName)
	case '8':
		b.phase = fileCopy
	}
}

func (b *fileBrowser) operationPrompt() string {
	switch b.phase {
	case fileDelete:
		return "Delete " + filePath(b.directory, b.entries[b.selected-2].DOSName) + "? No (Yes)"
	case fileRename:
		return "New name: " + b.draft
	default:
		return "Copy this file to: " + b.draft
	}
}

func (b *fileBrowser) editOperation(k input.Key, cancel bool) {
	if cancel || b.phase == fileDelete && (k.Code == tea.KeyEnter || k.Code == 'n' || k.Code == 'N') {
		b.phase, b.message = fileListing, ""
		return
	}
	if b.phase == fileDelete {
		if k.Code != 'y' && k.Code != 'Y' {
			return
		}
	} else if k.Code != tea.KeyEnter {
		if k.Code == tea.KeyBackspace {
			b.touched = true
			if len(b.draft) > 0 {
				b.draft = b.draft[:len(b.draft)-1]
			}
		} else {
			b.addDraft(k.Text)
		}
		return
	}
	entry := b.entries[b.selected-2]
	selection, err := b.list.Select(b.selected - 2)
	if err == nil {
		switch b.phase {
		case fileDelete:
			err = selection.Delete()
		case fileRename:
			if !strings.EqualFold(b.draft, filePath(b.directory, entry.DOSName)) {
				err = selection.Transfer(b.draft, true)
			}
		case fileCopy:
			err = selection.Transfer(b.draft, false)
		}
	}
	if err != nil {
		b.message = err.Error()
		return
	}
	b.request(b.directory, filePath(b.directory, b.pattern))
	b.submit()
}
