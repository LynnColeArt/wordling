package tui

import (
	"fmt"
	"strconv"
	"strings"
	"time"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/storage"
)

const fileDisplayPrompt = "1 Short Display; 2 Long Display: "

type filePhase uint8

const (
	fileDirectory filePhase = iota
	fileListing
	fileOtherDirectory
	fileDisplay
	fileNameSearch
	fileLook
	fileRetrieving
)

type fileBrowser struct {
	directory, base           *storage.WorkspaceDirectory
	list                      *storage.Listing
	entries                   []storage.FileEntry
	phase                     filePhase
	selected, look, first     int // Row indices; . and .. occupy the first two rows.
	long, touched, onDocument bool
	displayChoice             rune
	displayPending            bool
	pattern, draft            string
	lookNative                *document.Document
	message                   string
	observed                  time.Time
}

func filePath(dir *storage.WorkspaceDirectory, pattern string) string {
	return strings.TrimSuffix(dir.DOSPath(), `\`) + `\` + pattern
}

func (m Model) openFiles() Model {
	m.historic.files = true
	m.historic.message = ""
	b := &m.historic.browser
	if b.directory == nil {
		b.directory = m.runtime.workspaceRoot
		b.pattern = "*.*"
		b.selected = -1
	}
	b.request(b.directory, filePath(b.directory, b.pattern))
	b.onDocument = true
	return m
}

func (b *fileBrowser) request(base *storage.WorkspaceDirectory, draft string) {
	b.phase, b.base, b.draft, b.touched, b.message = fileDirectory, base, draft, false, ""
	b.onDocument, b.displayPending = false, false
}

func (b *fileBrowser) submit() {
	dirName, pattern := "", b.draft
	if i := strings.LastIndexAny(pattern, `\:`); i >= 0 {
		dirName, pattern = pattern[:i+1], pattern[i+1:]
	}
	if pattern == "" {
		pattern = "*.*"
	}
	dir, err := b.base.Navigate(dirName)
	if err != nil {
		b.message = err.Error()
		return
	}
	l, err := dir.List(pattern)
	if err != nil {
		b.message = err.Error()
		return
	}
	b.directory, b.list, b.entries, b.pattern = dir, l, l.Entries(), pattern
	if b.displayPending {
		b.long = b.displayChoice == '2'
		b.displayPending = false
	}
	b.phase, b.selected, b.first, b.message, b.observed = fileListing, 0, 0, "", time.Now()
}

func (m Model) filePress(k input.Key) (tea.Model, tea.Cmd) {
	b := &m.historic.browser
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) != 0 {
		return m, nil
	}
	cancel := k.Code == tea.KeyF1 || k.Code == tea.KeyEscape || k.Code == tea.KeyF7
	if !m.showEditorChrome() && cancel {
		m.historic.files = false
		if b.phase == fileRetrieving && m.session.Snapshot().Mode == editor.RetrieveInsertQuestion {
			return m.reduce(editor.Event{Command: editor.No})
		}
		return m, nil
	}
	switch b.phase {
	case fileDirectory, fileOtherDirectory:
		switch {
		case b.phase == fileDirectory && b.displayPending && k.Code == tea.KeyF7:
			// Original F7 confirms a display request at the visible Dir prompt.
			b.submit()
		case cancel:
			b.displayPending = false
			if b.onDocument || b.list == nil || k.Code == tea.KeyF7 {
				m.historic.files = false
			} else {
				b.phase, b.message = fileListing, ""
			}
		case k.Code == tea.KeyF5 && b.phase == fileDirectory && b.onDocument && !b.touched && b.list != nil:
			b.phase = fileListing
		case k.Code == '=' && b.phase == fileDirectory && !b.touched:
			b.phase, b.draft = fileOtherDirectory, b.base.DOSPath()
		case k.Code == tea.KeyEnter:
			if b.phase == fileOtherDirectory {
				dir, err := b.base.Navigate(b.draft)
				if err != nil {
					b.message = err.Error()
					break
				}
				onDocument, displayPending := b.onDocument, b.displayPending
				b.request(dir, filePath(dir, "*.*"))
				b.onDocument, b.displayPending = onDocument, displayPending
			} else {
				b.submit()
			}
		case k.Code == tea.KeyBackspace:
			if len(b.draft) != 0 {
				b.draft = b.draft[:len(b.draft)-1]
			}
			b.touched = true
		default:
			b.addDraft(k.Text)
		}
	case fileDisplay:
		switch {
		case cancel:
			b.phase = fileListing
		case k.Code == '1' || k.Code == '2' || k.Code == tea.KeyEnter:
			if k.Code != tea.KeyEnter {
				b.displayChoice = k.Code
			}
			b.request(b.directory, filePath(b.directory, b.pattern))
			b.displayPending = true
		}
	case fileNameSearch:
		switch {
		case cancel || k.Code == tea.KeyEnter:
			b.phase = fileListing
		case k.Code == tea.KeyUp || k.Code == tea.KeyDown:
			b.phase = fileListing
			step := m.fileRowStep()
			if k.Code == tea.KeyUp {
				step = -step
			}
			b.move(step)
		default:
			if k.Code == tea.KeyBackspace && len(b.draft) != 0 {
				b.draft = b.draft[:len(b.draft)-1]
			} else {
				b.addDraft(k.Text)
			}
			switch b.draft {
			case ".":
				b.selected = 0
			case "..":
				b.selected = 1
			default:
				if index := b.list.Find(b.draft); index >= 0 {
					b.selected = index + 2
				}
			}
		}
	case fileLook:
		switch {
		case cancel:
			b.phase, b.lookNative, b.message = fileListing, nil, ""
		case k.Code == '1' || k.Code == '2':
			step := 1
			if k.Code == '2' {
				step = -1
			}
			for i := b.look + step; i >= 2 && i < len(b.entries)+2; i += step {
				if b.entries[i-2].Supported && b.entries[i-2].Mode.IsRegular() {
					b.openLook(i)
					break
				}
			}
		}
	case fileRetrieving:
		if cancel && m.session.Snapshot().Mode == editor.RetrieveInsertQuestion {
			return m.reduce(editor.Event{Command: editor.No})
		}
		state := m.session.Snapshot()
		if state.Mode == editor.Waiting {
			if k.Code == tea.KeyF1 && state.Pending != nil &&
				(state.Pending.Kind == editor.ReadMergePrimary || state.Pending.Kind == editor.ReadMergeSecondary) {
				m.historic.files = false
				return m.reduce(editor.Event{Command: editor.F1})
			}
			return m, nil
		}
		if command, ok := resolve(k, state.Mode); ok {
			return m.reduce(command)
		}
	default:
		b.message = ""
		switch k.Code {
		case tea.KeyF1, tea.KeyF7, tea.KeyEscape:
			m.historic.files = false
		case tea.KeyUp:
			b.move(-m.fileRowStep())
		case tea.KeyDown:
			b.move(m.fileRowStep())
		case tea.KeyLeft:
			if !b.long {
				b.move(-1)
			}
		case tea.KeyRight:
			if !b.long {
				b.move(1)
			}
		case tea.KeyPgUp:
			b.move(-m.filePageSize())
		case tea.KeyPgDown:
			b.move(m.filePageSize())
		case '5':
			b.phase = fileDisplay
			if b.long {
				b.displayChoice = '1'
			} else {
				b.displayChoice = '2'
			}
		case '6':
			b.lookSelection()
		case '7':
			b.request(b.directory, b.directory.DOSPath())
			b.phase = fileOtherDirectory
		case 'n', 'N':
			b.phase, b.draft, b.touched = fileNameSearch, "", true
		case tea.KeyEnter, '1':
			return m.retrieveSelection()
		case tea.KeyHome, tea.KeyEnd:
			// Original does not use End as a selection shortcut.
		default:
			b.message = "This List Files command is not yet implemented"
		}
	}
	b.first = m.fileFirst()
	return m, nil
}

func (b *fileBrowser) addDraft(text string) {
	if text == "" || len(text) > 1024 {
		return
	}
	for _, c := range text {
		if c < ' ' || c > '~' {
			return
		}
	}
	if !b.touched {
		b.draft, b.touched = "", true
	}
	if len(b.draft)+len(text) <= 1024 {
		b.draft += text
	}
}

func (b *fileBrowser) move(by int) {
	if b.selected < 0 {
		b.selected = 0
	} else {
		b.selected = max(0, min(b.selected+by, len(b.entries)+1))
	}
}

func (b *fileBrowser) lookSelection() {
	if b.selected < 0 {
		return
	}
	var dir *storage.WorkspaceDirectory
	var err error
	switch b.selected {
	case 0:
		dir = b.directory
	case 1:
		dir, err = b.directory.Navigate("..")
	default:
		entry := b.entries[b.selected-2]
		if !entry.Mode.IsDir() {
			b.openLook(b.selected)
			return
		}
		var selection *storage.EntrySelection
		selection, err = b.list.Select(b.selected - 2)
		if err == nil {
			dir, err = selection.Enter()
		}
	}
	if err != nil {
		b.message = err.Error()
		return
	}
	b.request(dir, filePath(dir, "*.*"))
}

func (b *fileBrowser) openLook(index int) {
	selection, err := b.list.Select(index - 2)
	if err == nil {
		var stored *storage.Document
		stored, err = selection.Read()
		if err == nil {
			var native *document.Document
			native, err = document.Parse(stored.Export())
			if err == nil {
				b.phase, b.look, b.lookNative, b.message = fileLook, index, native, ""
				return
			}
		}
	}
	b.message = err.Error()
}

func (m Model) retrieveSelection() (tea.Model, tea.Cmd) {
	b := &m.historic.browser
	if b.selected < 2 {
		return m, nil
	}
	entry := b.entries[b.selected-2]
	if !entry.Supported || !entry.Mode.IsRegular() {
		b.message = "Select a supported file to retrieve"
		return m, nil
	}
	selection, err := b.list.Select(b.selected - 2)
	if err != nil {
		b.message = err.Error()
		return m, nil
	}
	b.phase = fileRetrieving
	return m.reduce(editor.Event{Command: editor.RetrieveSelection, Selection: selection})
}

func (m Model) fileRowStep() int {
	if m.historic.browser.long {
		return 1
	}
	return 2
}

func (m Model) filePageSize() int {
	if m.historic.browser.long {
		return max(1, m.height-7)
	}
	return max(1, m.height-6) * 2
}

func (m Model) fileFirst() int {
	b := m.historic.browser
	step := m.fileRowStep()
	first := b.first / step * step
	if b.selected < first {
		return max(0, b.selected/step*step)
	}
	size := m.filePageSize()
	if b.selected >= first+size {
		return (b.selected - size + step) / step * step
	}
	return first
}

func fileStamp(t time.Time) string {
	return strings.ToLower(t.Format("01-02-06 03:04p"))
}

func fileCount(value uint64) string {
	digits := strconv.FormatUint(value, 10)
	if len(digits) <= 3 {
		return digits
	}
	var grouped strings.Builder
	for i, digit := range digits {
		if i > 0 && (len(digits)-i)%3 == 0 {
			grouped.WriteByte(',')
		}
		grouped.WriteRune(digit)
	}
	return grouped.String()
}

func fileActions(text string) string {
	var row strings.Builder
	for i, command := range strings.Split(text, "; ") {
		if i > 0 {
			row.WriteString("; ")
		}
		if len(command) >= 3 {
			row.WriteString(revealCode + command[:1] + screenReset + " " + revealCode + command[2:3] + screenReset + command[3:])
		} else {
			row.WriteString(command)
		}
	}
	return row.String()
}

func fileHighlight(s string) string { return menuRed + s + screenReset }

func fileEntryFields(entry storage.FileEntry) (name, size, stamp string) {
	name = entry.DOSName
	if name == "" {
		name = "(unsupported)"
	}
	if entry.Supported {
		stem, ext, _ := strings.Cut(name, ".")
		name = fmt.Sprintf("%-8s.%-3s", stem, ext)
	}
	size = fmt.Sprint(entry.Size)
	if entry.Mode.IsDir() {
		size = "<Dir>"
	}
	if !entry.Supported {
		size = "Host"
		if entry.Ambiguous {
			size = "Alias"
		}
	}
	return name, size, fileStamp(entry.Modified)
}

func (m Model) fileLines(documentLines []string) []string {
	b := m.historic.browser
	last := m.height - 1
	if (b.phase == fileDirectory || b.phase == fileOtherDirectory) && (b.onDocument || b.list == nil) {
		lines := append([]string(nil), documentLines...)
		lines[last] = browserDirectoryPrompt(b)
		if b.phase == fileDirectory && b.onDocument {
			hint := "(Type = to change default Dir)"
			if space := m.width - ansi.StringWidth(lines[last]) - len(hint); space > 0 {
				lines[last] += strings.Repeat(" ", space) + hint
			}
		}
		if b.message != "" {
			lines[last-1] = b.message
		}
		return lines
	}
	lines := make([]string, m.height)
	if b.phase == fileLook && b.lookNative != nil {
		entry := b.entries[b.look-2]
		header := fmt.Sprintf("File: %-37s WP5.1      Revised: %s", filePath(b.directory, entry.DOSName), fileStamp(entry.Modified))
		lines[0] = fileHighlight(header + strings.Repeat(" ", max(0, m.width-ansi.StringWidth(header))))
		// Look shares the document projection with ordinary editing and never
		// installs this native document into the live session.
		frame, err := projectEveryday(b.lookNative, 0, m.width, last-3)
		if err != nil {
			lines[3] = err.Error()
		} else {
			copy(lines[3:last], frame.normal)
		}
		lines[last] = revealCode + "Look: " + screenReset + fileActions("1 Next Doc; 2 Prev Doc: ") + revealCode + "0" + screenReset
		if b.message != "" {
			lines[last-1] = b.message
		}
		return lines
	}
	metrics := b.list.Metrics()
	var used int64
	files := 0
	for _, entry := range b.entries {
		if entry.Mode.IsRegular() {
			used += entry.Size
			files++
		}
	}
	docBytes := 0
	if d := m.session.Document(); d != nil {
		start, firstErr := d.CursorAt(0)
		end, lastErr := d.CursorAt(d.TokenCount())
		if firstErr == nil && lastErr == nil {
			lo, loErr := start.Offset()
			hi, hiErr := end.Offset()
			if loErr == nil && hiErr == nil {
				docBytes = hi - lo
				// Original standard-profile List Files reports the resident
				// buffer: 258 bytes for a written new document and 514 for
				// a retrieved one, plus its native body owners.
				if !d.Birth().IsNew() {
					docBytes += 514
				} else if docBytes > 0 {
					docBytes += 258
				}
			}
		}
	}
	stamp := strings.Replace(fileStamp(b.observed), " ", "  ", 1)
	head := fmt.Sprintf("%-27sDirectory %s", stamp, filePath(b.directory, b.pattern))
	stats := fmt.Sprintf("Document size:%9s   Free: %10s Used:%11s     Files:%8s", fileCount(uint64(docBytes)), fileCount(metrics.FreeBytes), fileCount(uint64(used)), fileCount(uint64(files)))
	for i, row := range []string{head, stats} {
		lines[i] = fileHighlight(row + strings.Repeat(" ", max(0, m.width-ansi.StringWidth(row))))
	}
	if b.long {
		headings := " Descriptive Name               Type      Filename       Size    Revision Date"
		lines[2] = fileHighlight(headings + strings.Repeat(" ", max(0, m.width-len(headings))))
	}
	pageSize := m.filePageSize()
	first := m.fileFirst()
	for offset := 0; offset < pageSize; offset++ {
		index := first + offset
		row := 4 + offset
		if !b.long {
			row = 3 + offset/2
		}
		cell := ""
		switch index {
		case 0:
			if b.long {
				cell = " Current Directory                        .               <Dir>"
			} else {
				cell = " .    Current    <Dir>"
			}
		case 1:
			if b.long {
				cell = " Parent Directory                         ..              <Dir>"
			} else {
				cell = " ..   Parent     <Dir>"
			}
		default:
			if index-2 < len(b.entries) {
				name, size, stamp := fileEntryFields(b.entries[index-2])
				if b.long {
					cell = strings.Repeat(" ", 42) + fmt.Sprintf("%-12s %8s  %s", name, size, stamp)
				} else {
					cell = fmt.Sprintf(" %-12s %7s  %s", name, size, stamp)
				}
			}
		}
		if !b.long {
			width := max(0, m.width/2-1)
			cell = clip(cell, width)
			cell += strings.Repeat(" ", max(0, width-ansi.StringWidth(cell)))
		}
		if index == b.selected {
			cell = fileHighlight(cell)
		}
		if !b.long && offset%2 == 1 {
			lines[row] += "│"
		}
		lines[row] += cell
	}
	lines[last-1] = fileActions("1 Retrieve; 2 Delete; 3 Move/Rename; 4 Print; 5 Short/Long Display;")
	lines[last] = fileActions("6 Look; 7 Other Directory; 8 Copy; 9 Find; N Name Search:")
	switch b.phase {
	case fileDirectory, fileOtherDirectory:
		lines[last-1], lines[last] = "", browserDirectoryPrompt(b)
		if b.displayPending {
			lines[last] = revealCode + lines[last] + screenReset
		}
	case fileDisplay:
		lines[last-1], lines[last] = "", fileActions(fileDisplayPrompt)+revealCode+string(b.displayChoice)+screenReset
	case fileNameSearch:
		lines[last-1], lines[last] = "", b.draft+"  (Name Search; Enter or arrows to Exit)"
	case fileRetrieving:
		lines[last-1], lines[last] = "", m.session.Snapshot().Prompt
	}
	if b.message != "" {
		lines[last-1] = b.message
	}
	return lines
}

func (m Model) fileCursor() *tea.Cursor {
	b := m.historic.browser
	x := 0
	switch b.phase {
	case fileDirectory, fileOtherDirectory:
		x = len(browserDirectoryPrompt(b))
		if !b.touched {
			x -= len(b.draft)
		}
	case fileDisplay:
		x = len(fileDisplayPrompt)
	case fileNameSearch:
		x = len(b.draft)
	default:
		return nil
	}
	return tea.NewCursor(min(m.width-1, x), m.height-1)
}

// Observe reducer settlement rather than deciding whether any native content
// was installed. Decline and failure return to the same listing and selection.
func (m *Model) finishBrowserRetrieve(before, after editor.Snapshot) {
	if !m.historic.files || m.historic.browser.phase != fileRetrieving ||
		after.Mode == editor.Waiting || after.Mode == editor.RetrieveInsertQuestion {
		return
	}
	b := &m.historic.browser
	if before.Pending != nil && fileReadSettled(before.Pending.Kind, after.Mode) && after.Last.Applied &&
		after.Last.Result.Kind == before.Pending.Kind &&
		after.Last.Result.Operation == before.Pending.Operation &&
		after.Last.Result.Revision == before.Pending.Revision &&
		after.Last.Result.Err == nil && m.notice == "" {
		m.historic.files = false
		return
	}
	b.phase = fileListing
	b.message = after.Notice
	if m.notice != "" {
		b.message = m.notice
	}
}

func fileReadSettled(kind editor.IntentKind, mode editor.Mode) bool {
	switch kind {
	case editor.ReadSelection, editor.ReadMergeSecondary:
		return mode == editor.Editing
	case editor.ReadMergePrimary:
		return mode == editor.MergeSecondaryName
	default:
		return false
	}
}

func browserDirectoryPrompt(b fileBrowser) string {
	if b.phase == fileOtherDirectory {
		return "New directory = " + b.draft
	}
	return "Dir " + b.draft
}
