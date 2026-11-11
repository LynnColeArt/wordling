package tui

import (
	"crypto/rand"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync/atomic"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/storage"
	"golang.org/x/sys/unix"
)

const settingsHeader = "wordling-settings=1\nmenu_bar_remains_visible="

func readMenuPreference(dir string) (bool, error) {
	root, err := os.OpenRoot(dir)
	if errors.Is(err, os.ErrNotExist) {
		return true, nil
	}
	if err != nil {
		return true, err
	}
	defer root.Close()
	return readMenuPreferenceRoot(root)
}

func readMenuPreferenceRoot(root *os.Root) (bool, error) {
	file, err := root.OpenFile("settings", os.O_RDONLY|unix.O_NONBLOCK|unix.O_NOFOLLOW, 0)
	if errors.Is(err, os.ErrNotExist) {
		return true, nil
	}
	if err != nil {
		return true, err
	}
	defer file.Close()
	info, err := file.Stat()
	if err != nil {
		return true, err
	}
	if !info.Mode().IsRegular() {
		return true, errors.New("settings must be a regular file")
	}
	raw, err := io.ReadAll(io.LimitReader(file, int64(len(settingsHeader)+5)))
	if err != nil {
		return true, err
	}
	switch string(raw) {
	case settingsHeader + "yes\n":
		return true, nil
	case settingsHeader + "no\n":
		return false, nil
	default:
		return true, errors.New("unrecognized Wordling settings")
	}
}

func writeMenuPreference(dir string, visible bool) error {
	if dir == "" {
		return errors.New("user configuration directory unavailable")
	}
	if err := os.MkdirAll(dir, 0700); err != nil {
		return err
	}
	root, err := os.OpenRoot(dir)
	if err != nil {
		return err
	}
	defer root.Close()
	if _, err := readMenuPreferenceRoot(root); err != nil {
		return err
	}
	name := ".settings-" + rand.Text()
	file, err := root.OpenFile(name, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)
	if err != nil {
		return err
	}
	defer root.Remove(name)
	value := "no"
	if visible {
		value = "yes"
	}
	_, writeErr := io.WriteString(file, settingsHeader+value+"\n")
	err = errors.Join(writeErr, file.Sync(), file.Close())
	if err != nil {
		return err
	}
	return root.Rename(name, "settings")
}

func menuPreferenceDirectory() (string, error) {
	root, err := os.UserConfigDir()
	if err != nil {
		return "", err
	}
	if !filepath.IsAbs(root) {
		return "", errors.New("user configuration directory is not absolute")
	}
	return filepath.Join(root, "wordling"), nil
}

type setupPage uint8

const (
	setupClosed setupPage = iota
	setupRoot
	setupDisplay
	setupMenuOptions
	setupEnvironment
	setupBackup
)

type setupWrite struct {
	visible bool
	started atomic.Bool
}

type setupReply struct {
	request *setupWrite
	err     error
}

type setupUI struct {
	page     setupPage
	question bool
	pending  *setupWrite
	backup   storage.OriginalBackup
	notice   string
}

func (r *Runtime) saveMenuPreference(request *setupWrite) tea.Cmd {
	return func() tea.Msg {
		if !request.started.CompareAndSwap(false, true) {
			return nil
		}
		r.mu.Lock()
		if r.stopping {
			r.mu.Unlock()
			return setupReply{request, errors.New("settings host is closed")}
		}
		r.workers.Add(1)
		r.mu.Unlock()
		defer r.workers.Done()
		return setupReply{request, writeMenuPreference(r.preferenceDir, request.visible)}
	}
}

func (m Model) openSetup(page setupPage) Model {
	backup := m.setup.backup
	m.setup = setupUI{page: page, backup: backup}
	m.notice = ""
	return m
}

func (m Model) finishSetup(result setupReply) Model {
	if m.setup.pending == nil || result.request != m.setup.pending {
		return m
	}
	m.setup.pending = nil
	if result.err != nil {
		m.setup.notice = "Menu settings: " + result.err.Error()
		return m
	}
	m.historic.bar = result.request.visible
	m.setup.question, m.setup.notice = false, ""
	return m
}

func (m Model) setupPress(k input.Key) (tea.Model, tea.Cmd) {
	s := &m.setup
	if s.pending != nil {
		return m, nil
	}
	if k.Mod != 0 && k.Mod != tea.ModShift {
		return m, nil
	}
	if !m.showEditorChrome() && k.Code != tea.KeyF1 && k.Code != tea.KeyF7 && k.Code != tea.KeyEscape {
		return m, nil
	}
	s.notice = ""
	if s.question {
		switch k.Code {
		case tea.KeyEscape, tea.KeyF1:
			s.question = false
		case 'y', 'Y', 'n', 'N', tea.KeyEnter:
			yes := k.Code == 'y' || k.Code == 'Y'
			if k.Code == tea.KeyEnter {
				yes = (s.page == setupMenuOptions && m.historic.bar) ||
					(s.page == setupBackup && s.backup == storage.OriginalBackupOn)
			}
			if s.page == setupMenuOptions {
				s.pending = &setupWrite{visible: yes}
				return m, m.runtime.saveMenuPreference(s.pending)
			}
			value := storage.OriginalBackupOff
			if yes {
				value = storage.OriginalBackupOn
			}
			next, err := m.session.WithOriginalBackup(value)
			if err != nil {
				s.notice = err.Error()
				return m, nil
			}
			m.session, s.backup, s.question = next, value, false
		}
		return m, nil
	}
	if k.Code == tea.KeyF7 {
		s.page = setupClosed
		return m, nil
	}
	if k.Code == tea.KeyEscape || k.Code == tea.KeyF1 {
		switch s.page {
		case setupMenuOptions:
			s.page = setupDisplay
		case setupBackup:
			s.page = setupEnvironment
		case setupDisplay, setupEnvironment:
			s.page = setupRoot
		default:
			s.page = setupClosed
		}
		return m, nil
	}
	switch {
	case s.page == setupRoot && k.Code == '2':
		s.page = setupDisplay
	case s.page == setupRoot && k.Code == '3':
		s.page = setupEnvironment
	case s.page == setupDisplay && k.Code == '4':
		s.page = setupMenuOptions
	case s.page == setupEnvironment && k.Code == '1':
		s.page = setupBackup
	case s.page == setupMenuOptions && k.Code == '8',
		s.page == setupBackup && k.Code == '2':
		s.question = true
	case k.Code >= '1' && k.Code <= '9':
		s.notice = "This Setup option is not yet implemented"
	}
	return m, nil
}

func setupValue(value, asking bool) string {
	current, other := "No", "Yes"
	if value {
		current, other = other, current
	}
	if asking {
		return current + " (" + other + ")"
	}
	return current
}

func (m Model) setupView() tea.View {
	s := m.setup
	if !m.showEditorChrome() {
		v := m.historicModalView([]string{"Setup active", "Enlarge window to continue"}, "", s.notice)
		v.Cursor = nil
		return v
	}
	var body []string
	selection := 0
	switch s.page {
	case setupRoot:
		body = []string{"Setup", "", "     1 - Mouse", "", "     2 - Display", "", "     3 - Environment", "",
			"     4 - Initial Settings", "", "     5 - Keyboard Layout", "", "     6 - Location of Files"}
	case setupDisplay:
		body = []string{"Setup: Display", "", "     1 - Colors/Fonts/Attributes", "",
			"     2 - Graphics Screen Type      None Selected", "", "     3 - Text Screen Type          Auto Selected", "",
			"     4 - Menu Options", "", "     5 - View Document Options", "", "     6 - Edit-Screen Options"}
	case setupMenuOptions:
		body = []string{"Setup: Menu Options", "", "     1 - Menu Letter Display            BOLD", "", "Pull-Down Menu", "",
			"     2 - Pull-Down Letter Display       REDLN", "", "     3 - Pull-Down Text                 SHADW", "",
			"     4 - Alt Key Selects Pull-Down Menu No", "", "Menu Bar", "", "     5 - Menu Bar Letter Display        REDLN", "",
			"     6 - Menu Bar Text                  SHADW", "", "     7 - Menu Bar Separator Line        No", "",
			"     8 - Menu Bar Remains Visible       " + setupValue(m.historic.bar, s.question)}
		if s.question {
			selection = 8
		}
	case setupEnvironment:
		body = []string{"Setup: Environment", "", "     1 - Backup Options", "", "     2 - Beep Options", "",
			"     3 - Cursor Speed                             50 cps", "", "     4 - Document Management/Summary", "",
			"     5 - Fast Save (unformatted)", "", "     6 - Hyphenation", "", "     7 - Prompt for Hyphenation", "",
			"     8 - Units of Measure", "", "     9 - Alternate Keyboard"}
	case setupBackup:
		body = []string{"Setup: Backup", "", "", "", "", "", "", "         Backup Directory", "",
			"     1 - Timed Document Backup", "", "", "     Original backup retains the prior native document as .BK!.", "", "",
			"     2 - Original Document Backup            " + setupValue(s.backup == storage.OriginalBackupOn, s.question)}
		if s.question {
			selection = 2
		}
	}
	body[0] = revealCode + body[0] + screenReset
	for i, row := range body[1:] {
		if strings.HasPrefix(row, "     ") && len(row) > 9 && row[6:9] == " - " {
			row = highlightSetupCell(row, 5)
			if s.page != setupMenuOptions && s.page != setupBackup {
				row = highlightSetupCell(row, 9+len(revealCode)+len(screenReset))
			}
			body[i+1] = row
		}
	}
	if s.page == setupMenuOptions {
		for _, row := range []int{4, 12} {
			body[row] = revealCode + body[row] + screenReset
		}
		for _, row := range []int{2, 6, 8, 10, 14, 16, 18, 20} {
			base := body[row]
			plain := strings.Index(base, " - ") + 3
			if row == 20 {
				plain = strings.Index(base, "Visible")
			}
			body[row] = highlightSetupCell(base, plain)
		}
		body[20] = styleSetupValue(body[20], setupValue(m.historic.bar, s.question), s.question)
	}
	if s.page == setupBackup {
		body[15] = styleSetupValue(body[15], setupValue(s.backup == storage.OriginalBackupOn, s.question), s.question)
	}
	footer := fmt.Sprintf("Selection: %d", selection)
	notice := s.notice
	if s.pending != nil {
		notice = "Saving menu preference"
	}
	return m.historicModalView(body, footer, notice)
}

func highlightSetupCell(row string, at int) string {
	return row[:at] + revealCode + row[at:at+1] + screenReset + row[at+1:]
}

func styleSetupValue(row, value string, asking bool) string {
	at := len(row) - len(value)
	if !asking {
		return row[:at] + revealCode + value + screenReset
	}
	other := strings.IndexByte(value, '(') + 1
	row = highlightSetupCell(row, at+other)
	return highlightSetupCell(row, at)
}

func (m Model) historicModalView(body []string, footer, notice string) tea.View {
	lines := make([]string, m.height)
	copy(lines, body)
	cursor := len(footer)
	if strings.HasPrefix(footer, "Selection: ") && len(footer) >= 12 {
		lines[m.height-1] = revealCode + footer[:12] + screenReset + footer[12:]
		cursor = 11
	} else if footer != "" {
		lines[m.height-1] = footer
	}
	if notice != "" && m.height > 1 {
		lines[m.height-2] = notice
	}
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	applyEditorChrome(&v)
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	v.Cursor = tea.NewCursor(min(m.width-1, cursor), m.height-1)
	return v
}
