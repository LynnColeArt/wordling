package tui

import "github.com/lynncoleart/wordling/internal/storage"

func (m Model) WithPlatformNotice() Model {
	if m.notice == "" {
		m.notice = storage.CurrentPlatform().Notice
	}
	return m
}
