package tui

import (
	"fmt"
	"io"
	"os/exec"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
)

type shellReturned struct{ err error }

type interactiveShell struct{ *exec.Cmd }

func (s interactiveShell) SetStdin(r io.Reader)  { s.Stdin = r }
func (s interactiveShell) SetStdout(w io.Writer) { s.Stdout = w }
func (s interactiveShell) SetStderr(io.Writer)   { s.Stderr = s.Stdout }

func (s interactiveShell) Run() error {
	if _, err := fmt.Fprint(s.Stdout, ansi.KeypadNumericMode+"Type exit to return to Wordling.\n"); err != nil {
		return err
	}
	return s.Cmd.Run()
}

func (m Model) exitToCLI() (Model, tea.Cmd) {
	return m.beginLeave(false)
}

func (m Model) beginLeave(quit bool) (Model, tea.Cmd) {
	m.closeMenus()
	if quit && len(m.recovery.queued) != 0 {
		m.notice = "Close a document to open the next recovered copy before quitting."
		return m, nil
	}
	m.quitAfterSave = quit
	m.notice = ""
	m.shellOrigin = m.session.Snapshot().Screen
	m.leaveVisited = [editor.MaxDocumentScreens]bool{}
	return m.nextShellDocument(false)
}

func (m Model) nextShellDocument(skipCurrent bool) (Model, tea.Cmd) {
	current := m.session.Snapshot()
	if current.Dirty && !skipCurrent {
		m.shellSavePrompt = true
		return m, nil
	}
	m.leaveVisited[current.Screen-1] = true
	for offset := uint8(1); offset < editor.MaxDocumentScreens; offset++ {
		screen := (current.Screen-1+offset)%editor.MaxDocumentScreens + 1
		other, err := m.session.ScreenSnapshot(screen)
		if err != nil || !other.Dirty || m.leaveVisited[screen-1] {
			continue
		}
		next, cmd := m.reduce(editor.Event{Command: editor.SwitchDocument, Screen: screen})
		m = next.(Model)
		if m.notice != "" {
			m.shellOrigin = 0
			return m, cmd
		}
		m.shellSavePrompt = true
		return m, nil
	}
	return m.finishShellSave(true)
}

func (m Model) finishShellSave(open bool) (Model, tea.Cmd) {
	origin, quit := m.shellOrigin, m.quitAfterSave
	m.quitAfterSave = false
	m.shellOrigin, m.shellSavePrompt = 0, false
	if m.session.Snapshot().Mode == editor.Editing && m.session.Snapshot().Screen != origin {
		next, cmd := m.reduce(editor.Event{Command: editor.SwitchDocument, Screen: origin})
		m = next.(Model)
		if m.notice != "" {
			return m, cmd
		}
	}
	if open && quit {
		next, cmd := m.reduce(editor.Event{Command: editor.QuitApplication})
		return next.(Model), cmd
	}
	if !open {
		return m, nil
	}
	if m.recovery.store != nil {
		if err := m.writeRecovery(); err != nil {
			m.notice = "Autosave: " + err.Error()
		}
	}
	cmd := platformShell()
	return m, tea.Exec(interactiveShell{cmd}, func(err error) tea.Msg {
		return shellReturned{err: err}
	})
}

func (m Model) answerShellSave(k input.Key) (tea.Model, tea.Cmd) {
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) != 0 || k.IsRepeat {
		return m, nil
	}
	switch {
	case k.Code == tea.KeyEscape || k.Code == tea.KeyF1:
		return m.finishShellSave(false)
	case k.Code == tea.KeyEnter || k.Text == "y" || k.Text == "Y":
		m.shellSavePrompt = false
		next, cmd := m.reduce(editor.Event{Command: editor.Save})
		return next, cmd
	case k.Text == "n" || k.Text == "N":
		m.shellSavePrompt = false
		return m.nextShellDocument(true)
	}
	return m, nil
}
