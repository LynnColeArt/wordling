package tui

import (
	"crypto/rand"
	"fmt"
	"strings"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type recoveryTick struct{}

type recoveryUI struct {
	store           *recoveryStore
	entries, queued []recoveryRecord
	selected        []bool
	row             int
	confirm         bool
	screenIDs       [editor.MaxDocumentScreens]string
	parents         [editor.MaxDocumentScreens]recoveryRecord
}

func (m Model) EnableRecovery(workspace string) Model {
	store, entries, err := openRecovery(workspace)
	if err != nil {
		m.notice = "Recovery: " + err.Error()
	}
	if store != nil {
		m.recovery = recoveryUI{store: store, entries: entries, selected: make([]bool, len(entries))}
		for i := range entries {
			m.recovery.selected[i] = true
		}
	}
	return m
}

func (m Model) CloseRecovery(clean bool) error {
	if m.recovery.store == nil {
		return nil
	}
	return m.recovery.store.close(clean && len(m.recovery.queued) == 0 && len(m.recovery.store.old) == 0)
}

func recoveryTimer(delay time.Duration) tea.Cmd {
	return tea.Tick(delay, func(time.Time) tea.Msg { return recoveryTick{} })
}

func (m *Model) writeRecovery() error {
	r := &m.recovery
	if len(r.entries) > 0 {
		return nil
	}
	records := append([]recoveryRecord(nil), r.queued...)
	for screen := uint8(1); screen <= editor.MaxDocumentScreens; screen++ {
		copy := m.session.RecoveryCopy(screen)
		i := screen - 1
		if copy.Native == nil {
			r.screenIDs[i] = ""
			r.parents[i] = recoveryRecord{}
			continue
		}
		raw, err := copy.Native.Export()
		if err != nil {
			return err
		}
		if r.screenIDs[i] == "" {
			r.screenIDs[i] = rand.Text()
		}
		if copy.Name == "" && r.parents[i].Name != "" {
			copy.Name, copy.Parent = r.parents[i].Name, r.parents[i].Parent
		}
		records = append(records, recoveryRecord{r.screenIDs[i], copy.Name, copy.Parent, time.Now(), copy.Gap, raw})
	}
	if len(records) == 0 && len(r.store.old) == 0 {
		return r.store.clearSnapshot()
	}
	return r.store.write(records)
}

func (m Model) recoveryPress(k input.Key) (tea.Model, tea.Cmd) {
	r := &m.recovery
	if r.confirm {
		switch strings.ToLower(k.Text) {
		case "y":
			return m.commitRecovery()
		case "n":
			r.confirm = false
		}
		if k.Code == tea.KeyEscape {
			r.confirm = false
		}
		return m, nil
	}
	switch k.Code {
	case tea.KeyUp:
		r.row = max(0, r.row-1)
	case tea.KeyDown:
		r.row = min(len(r.entries)-1, r.row+1)
	case ' ':
		r.selected = append([]bool(nil), r.selected...)
		r.selected[r.row] = !r.selected[r.row]
	case 'a', 'A', 'd', 'D':
		r.selected = make([]bool, len(r.entries))
		for i := range r.selected {
			r.selected[i] = k.Code == 'a' || k.Code == 'A'
		}
	case tea.KeyEnter:
		for _, selected := range r.selected {
			if !selected {
				r.confirm = true
				return m, nil
			}
		}
		return m.commitRecovery()
	}
	return m, nil
}

func (m Model) commitRecovery() (tea.Model, tea.Cmd) {
	next := m
	next.recovery.entries = nil
	next.recovery.confirm = false
	origin := next.session.Snapshot().Screen
	store := m.recovery.store
	resolved := append([]string(nil), store.resolved...)
	opened := 0
	for i, record := range m.recovery.entries {
		resolved = append(resolved, record.ID)
		if !m.recovery.selected[i] {
			continue
		}
		record.ID = rand.Text()
		if opened >= editor.MaxDocumentScreens {
			next.recovery.queued = append(next.recovery.queued, record)
			continue
		}
		if opened > 0 {
			session, _, err := next.session.Reduce(editor.Event{Command: editor.NewDocumentScreen})
			if err != nil {
				m.notice = err.Error()
				return m, nil
			}
			next.session = session
		}
		if err := next.restoreRecovery(record); err != nil {
			m.notice = err.Error()
			return m, nil
		}
		opened++
	}
	if next.session.Snapshot().Screen != origin {
		session, _, err := next.session.Reduce(editor.Event{Command: editor.SwitchDocument, Screen: origin})
		if err != nil {
			m.notice = err.Error()
			return m, nil
		}
		next.session = session
	}
	previous := store.resolved
	store.resolved = resolved
	if err := next.writeRecovery(); err != nil {
		store.resolved = previous
		m.notice = "Recovery commit: " + err.Error()
		return m, nil
	}
	next.notice = ""
	if err := store.resolve(); err != nil {
		next.notice = "Recovery cleanup: " + err.Error()
	} else {
		store.resolved = nil
	}
	return next, nil
}

func (m *Model) restoreRecovery(record recoveryRecord) error {
	session, err := m.session.RestoreRecovery(record.Native, record.Gap)
	if err != nil {
		return err
	}
	m.session = session
	i := session.Snapshot().Screen - 1
	m.recovery.screenIDs[i] = record.ID
	m.recovery.parents[i] = recoveryRecord{Name: record.Name, Parent: record.Parent}
	return nil
}

func (m Model) recoveryView() tea.View {
	r := m.recovery
	lines := []string{"Recover documents from an interrupted Wordling session", "Up/Down Move  Space Check  A Check all  D Uncheck all"}
	visible := max(1, m.height-5)
	start := max(0, r.row-visible+1)
	discard := 0
	for i, record := range r.entries {
		mark := " "
		if r.selected[i] {
			mark = "x"
		} else {
			discard++
		}
		if i < start || i >= start+visible {
			continue
		}
		pointer := " "
		if i == r.row {
			pointer = ">"
		}
		name := record.Name
		if name == "" {
			name = "Untitled"
		}
		name = printableRecoveryLabel(name)
		parent := printableRecoveryLabel(record.Parent)
		if parent != "" && !strings.HasSuffix(parent, "\\") {
			parent += "\\"
		}
		lines = append(lines, fmt.Sprintf("%s [%s] %s%s  %s", pointer, mark, parent, name, record.Time.Local().Format("Jan 02 15:04")))
	}
	footer := "Enter Restore checked documents"
	if discard > 0 {
		footer = "Enter Review deletion of unchecked copies"
	}
	if r.confirm {
		footer = fmt.Sprintf("Permanently delete %d unchecked copies? Y Confirm / N Back", discard)
	}
	return m.historicModalView(lines, footer, m.notice)
}

func printableRecoveryLabel(label string) string {
	return strings.Map(func(r rune) rune {
		if r < 32 || r > 126 {
			return '?'
		}
		return r
	}, label)
}

// Refill a freed screen with the next selected recovery, in checklist order.
func (m *Model) advanceRecovery(previous editor.Snapshot) {
	if m.recovery.store == nil || len(m.recovery.entries) != 0 {
		return
	}
	current := m.session.Snapshot()
	if current.Mode != editor.Editing {
		return
	}
	if previous.Mode == editor.ExitDocQuestion || previous.Mode == editor.ExitQuestion {
		if previous.Screen != current.Screen || !current.Dirty && current.Name == "" {
			m.recovery.screenIDs[previous.Screen-1] = ""
			m.recovery.parents[previous.Screen-1] = recoveryRecord{}
		}
	}
	needsWrite := false
	for i, id := range m.recovery.screenIDs {
		if id != "" && m.session.RecoveryCopy(uint8(i+1)).Native == nil {
			needsWrite = true
		}
	}
	if len(m.recovery.queued) > 0 && !current.Dirty && current.Name == "" {
		if err := m.restoreRecovery(m.recovery.queued[0]); err != nil {
			m.notice = "Recovery: " + err.Error()
			return
		}
		m.recovery.queued = m.recovery.queued[1:]
		needsWrite = true
	} else if len(m.recovery.queued) > 0 && previous.Mode == editor.ExitDocQuestion && previous.Screen != current.Screen {
		session, _, err := m.session.Reduce(editor.Event{Command: editor.NewDocumentScreen})
		if err == nil {
			before := m.session
			m.session = session
			if err = m.restoreRecovery(m.recovery.queued[0]); err == nil {
				m.recovery.queued = m.recovery.queued[1:]
				needsWrite = true
			} else {
				m.session = before
			}
		}
		if err != nil {
			m.notice = "Recovery: " + err.Error()
		}
	}
	if previous.Mode == editor.ExitDocQuestion || previous.Mode == editor.ExitQuestion {
		needsWrite = true
	}
	if needsWrite {
		if err := m.writeRecovery(); err != nil {
			m.notice = "Autosave: " + err.Error()
		}
	}
}
