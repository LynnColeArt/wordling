package tui

import (
	"bytes"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"golang.org/x/sys/unix"
)

func TestMain(m *testing.M) {
	config, err := os.MkdirTemp("", "wordling-tui-config-")
	if err != nil {
		panic(err)
	}
	if err := os.Setenv("XDG_CONFIG_HOME", config); err != nil {
		panic(err)
	}
	code := m.Run()
	_ = os.RemoveAll(config)
	os.Exit(code)
}

type menuCell struct {
	glyph rune
	role  byte
}

func logicalMenuRow(row string) []menuCell {
	var cells []menuCell
	role := byte(0x17)
	for len(row) > 0 {
		if strings.HasPrefix(row, "\x1b[") {
			end := strings.IndexByte(row, 'm')
			if end < 0 {
				break
			}
			switch row[:end+1] {
			case menuGray:
				role = 0x71
			case menuMnemonic:
				role = 0x74
			case menuRed:
				role = 0x47
			case revealCode:
				role = 0x1f
			default:
				role = 0x17
			}
			row = row[end+1:]
			continue
		}
		for i, r := range row {
			if r == '\x1b' {
				row = row[i:]
				break
			}
			cells = append(cells, menuCell{r, role})
			if i+len(string(r)) == len(row) {
				row = ""
				break
			}
		}
	}
	return cells
}

func checkOriginalMenuCells(t *testing.T, m Model, source string, x, y, width, height int) {
	t.Helper()
	checkOriginalCells(t, m, source, referenceFile(t, source+"/vram.bin"), x, y, width, height)
}

func checkOriginalCells(t *testing.T, m Model, source string, raw []byte, x, y, width, height int) {
	t.Helper()
	rows := strings.Split(m.View().Content, "\n")
	for row := y; row < y+height; row++ {
		got := logicalMenuRow(rows[row])
		for len(got) < x+width {
			got = append(got, menuCell{' ', 0x17})
		}
		for col := x; col < x+width; col++ {
			offset := row*160 + col*2
			r := rune(raw[offset])
			if glyph, ok := originalMenuGlyphs[raw[offset]]; ok {
				r = glyph
			}
			want := menuCell{r, raw[offset+1]}
			if got[col] != want {
				t.Fatalf("%s (%d,%d): got %q/%02x, want %q/%02x", source, col, row, got[col].glyph, got[col].role, want.glyph, want.role)
			}
		}
	}
}

var originalMenuGlyphs = map[byte]rune{
	0x10: '►', 0xb3: '│', 0xb4: '┤', 0xbf: '┐', 0xc0: '└', 0xc1: '┴', 0xc2: '┬', 0xc3: '├', 0xc4: '─', 0xda: '┌', 0xd9: '┘',
	0xba: '║', 0xbb: '╗', 0xbc: '╝', 0xc8: '╚', 0xc9: '╔', 0xcd: '═', 0xcf: '╧', 0xd1: '╤',
}

func TestEverydayHelpOriginalKeyboardTemplatesAndReturn(t *testing.T) {
	m, _ := everydayUI(t)
	k := everydayKey
	m = inputKeys(t, m, textKey("EDIT"), k(tea.KeyLeft))
	before, raw := m.Session().Snapshot(), hBoldNative(t, m)
	caret := func() {
		t.Helper()
		if c := m.View().Cursor; c == nil || c.X != 11 || c.Y != 24 {
			t.Fatalf("original template help caret: %+v", c)
		}
	}
	m = inputKeys(t, m, k(tea.KeyF3), k(tea.KeyF3))
	checkOriginalMenuCells(t, m, "menus/03-key-template", 0, 0, 80, 25)
	caret()
	ibm, err := os.ReadFile("evidence/everyday-menus/ibm-template.vram")
	if err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, textKey("1"))
	checkOriginalCells(t, m, "IBM PC/XT template", ibm, 0, 0, 80, 25)
	caret()
	m = inputKeys(t, m, k(tea.KeyF3), k(tea.KeyF3))
	checkOriginalMenuCells(t, m, "menus/03-key-template", 0, 0, 80, 25)
	m = inputKeys(t, m, textKey("1"), textKey("1"))
	assertScreenRows(t, m, map[int]string{0: "Help                                                   WP 5.1   03/09/92"})
	m = inputKeys(t, m, k(tea.KeyF3), textKey("1"), k(tea.KeyEnter))
	if m.help.active || !reflect.DeepEqual(before, m.Session().Snapshot()) || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatal("template return moved the editor caret or changed native bytes")
	}
}

func altEquals() tea.Key { return tea.Key{Code: '=', Mod: tea.ModAlt, Text: "="} }

func TestEverydayMenuOriginalCellsAndRetainedChild(t *testing.T) {
	for _, cancel := range []tea.Key{everydayKey(tea.KeyF1), everydayKey(tea.KeyEscape), textKey(" ")} {
		m, _ := everydayUI(t)
		m = inputKeys(t, m, textKey("BASE"))
		raw := hBoldNative(t, m)
		checkOriginalMenuCells(t, m, "menus/13-visible-bar", 0, 0, 80, 1)
		m = inputKeys(t, m, altEquals())
		checkOriginalMenuCells(t, m, "menus/14-focused-bar", 0, 0, 80, 1)
		m = inputKeys(t, m, textKey("l"), textKey("j"))
		checkOriginalMenuCells(t, m, "menus/21-layout-justify", 35, 13, 10, 6)
		m = inputKeys(t, m, cancel)
		checkOriginalMenuCells(t, m, "focus-r1/02-f1-after", 35, 13, 10, 6)
		m = inputKeys(t, m, everydayKey(tea.KeyUp))
		if m.historic.sub != "Layout/Endnote" {
			t.Fatal("Up did not replace retained Justify with Endnote")
		}
		m = inputKeys(t, m, everydayKey(tea.KeyF7))
		if m.historic.menu || !m.historic.bar || !bytes.Equal(raw, hBoldNative(t, m)) {
			t.Fatal("F7 failed to restore editing focus")
		}
	}
}

func TestEverydayMenuFileAndEditMnemonicGeometry(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, altEquals(), textKey("f"))
	checkOriginalMenuCells(t, m, "menus/18-file-menu", 0, 0, 80, 1)
	checkOriginalMenuCells(t, m, "menus/18-file-menu", 0, 1, 23, 16)
	m = inputKeys(t, m, everydayKey(tea.KeyRight))
	checkOriginalMenuCells(t, m, "menus/19-edit-menu", 5, 1, 29, 19)
	m = inputKeys(t, m, everydayKey(tea.KeyF7), altEquals(), textKey("o"), textKey("a"), textKey("b"), textKey("B"), everydayKey(tea.KeyF6))
	if m.historic.menu || !bytes.HasSuffix(hBoldNative(t, m), []byte("\xc3\x0c\xc3B\xc4\x0c\xc4")) {
		t.Fatal("Font Appearance Bold and F6 did not share native routing")
	}
}

func TestEverydayHelpAndFunctionInMenu(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("EDIT"))
	before, raw := m.Session().Snapshot(), hBoldNative(t, m)
	m = inputKeys(t, m, everydayKey(tea.KeyF3), everydayKey(tea.KeyF3))
	assertScreenRows(t, m, map[int]string{0: "WordPerfect 5.1 Template", 4: "Reveal Codes"})
	for _, topic := range everydayHelpTopics[:8] {
		m = inputKeys(t, m, tea.Key{Code: topic.input.Code, Mod: topic.input.Mod})
		assertScreenRows(t, m, map[int]string{0: topic.title, 4: topic.key})
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnter))
	if m.help.active || !reflect.DeepEqual(before, m.Session().Snapshot()) || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatal("Help changed the document or lost editing position")
	}
	m = inputKeys(t, m, altEquals(), textKey("o"), everydayKey(tea.KeyF6), textKey("B"), everydayKey(tea.KeyF6))
	if m.historic.menu || !bytes.HasSuffix(hBoldNative(t, m), []byte("\xc3\x0c\xc3B\xc4\x0c\xc4")) {
		t.Fatal("direct F6 was swallowed by the drop-down")
	}
}

func menuSetupKeys(t *testing.T, m Model) Model {
	t.Helper()
	return inputKeys(t, m, tea.Key{Code: tea.KeyF1, Mod: tea.ModShift}, textKey("2"), textKey("4"), textKey("8"))
}

func TestEverydayMenuSettingsPersistOutsideDocumentRoot(t *testing.T) {
	config := t.TempDir()
	t.Setenv("XDG_CONFIG_HOME", config)
	m, workspace := everydayUI(t)
	if !m.historic.bar {
		t.Fatal("absent settings must choose the preview's visible default")
	}
	path := filepath.Join(config, "wordling", "settings")
	m = menuSetupKeys(t, m)
	assertScreenRows(t, m, map[int]string{0: "Setup: Menu Options", 20: "Yes (No)", 24: "Selection: 8"})
	m = inputKeys(t, m, everydayKey(tea.KeyEscape), everydayKey(tea.KeyF7))
	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Fatal("cancelled Setup created settings", err)
	}
	m = menuSetupKeys(t, m)
	next, cmd := m.Update(tea.KeyPressMsg(textKey("n")))
	m = next.(Model)
	if !m.historic.bar || cmd == nil {
		t.Fatal("preference adopted before publication")
	}
	m = inputKeys(t, m, textKey("x"))
	next, _ = m.Update(cmd())
	m = inputKeys(t, next.(Model), everydayKey(tea.KeyF7), textKey("HIDDEN"))
	if m.historic.bar || !strings.HasPrefix(ansi.Strip(m.View().Content), "HIDDEN") {
		t.Fatal("confirmed No lost editing focus")
	}
	if raw, err := os.ReadFile(path); err != nil || string(raw) != settingsHeader+"no\n" {
		t.Fatalf("settings content %q, %v", raw, err)
	}
	if entries, err := os.ReadDir(workspace); err != nil || len(entries) != 0 {
		t.Fatal("settings reached document workspace", err)
	}
	m, _ = everydayUI(t)
	if m.historic.bar {
		t.Fatal("fresh process state did not use persisted No")
	}
	m = inputKeys(t, m, altEquals(), textKey("f"), textKey("t"), textKey("d"), textKey("4"), textKey("8"))
	assertScreenRows(t, m, map[int]string{20: "No (Yes)"})
	m = inputKeys(t, m, textKey("y"), everydayKey(tea.KeyF7))
	if !m.historic.bar {
		t.Fatal("File Setup path did not use the same setting")
	}
	m, _ = everydayUI(t)
	if !m.historic.bar {
		t.Fatal("fresh Open did not adopt persisted Yes")
	}
}

func TestEverydaySettingsRefuseCorruptSpecialAndSymlinkFiles(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "settings")
	corrupt := []byte("wordling-settings=2\n")
	if err := os.WriteFile(path, corrupt, 0600); err != nil {
		t.Fatal(err)
	}
	if yes, err := readMenuPreference(dir); !yes || err == nil {
		t.Fatal("malformed config did not report error with Yes fallback")
	}
	if err := writeMenuPreference(dir, false); err == nil {
		t.Fatal("unknown version was overwritten")
	}
	if raw, err := os.ReadFile(path); err != nil || !bytes.Equal(raw, corrupt) {
		t.Fatalf("unknown version changed: %q %v", raw, err)
	}
	if err := os.Remove(path); err != nil {
		t.Fatal(err)
	}
	if err := unix.Mkfifo(path, 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := readMenuPreference(dir); err == nil {
		t.Fatal("FIFO accepted as regular settings")
	}
	if err := os.Remove(path); err != nil {
		t.Fatal(err)
	}
	target := filepath.Join(t.TempDir(), "outside")
	if err := os.WriteFile(target, []byte(settingsHeader+"no\n"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(target, path); err != nil {
		t.Fatal(err)
	}
	if _, err := readMenuPreference(dir); err == nil {
		t.Fatal("external symlink accepted as settings")
	}
	if err := writeMenuPreference(dir, true); err == nil {
		t.Fatal("external symlink accepted for publication")
	}
}

func TestEverydaySetupFailureRetainsPreviousPreference(t *testing.T) {
	config := t.TempDir()
	t.Setenv("XDG_CONFIG_HOME", config)
	m, _ := everydayUI(t)
	m = menuSetupKeys(t, m)
	if err := os.WriteFile(filepath.Join(config, "wordling"), []byte("blocked"), 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, textKey("n"))
	if !m.historic.bar || !m.setup.question || !strings.Contains(m.setup.notice, "Menu settings:") || m.Session().Snapshot().Mode != editor.Editing {
		t.Fatal("failed write changed the preference or abandoned the question")
	}
}

func TestEverydaySearchMenuRepeatsOriginalCommand(t *testing.T) {
	m, _ := everydayUI(t)
	k := everydayKey
	m = inputKeys(t, m, textKey("alpha beta alpha gamma alpha"), k(tea.KeyHome), k(tea.KeyHome), k(tea.KeyUp),
		k(tea.KeyF2), textKey("alpha"), k(tea.KeyF2))
	raw := hBoldNative(t, m)
	first := m.Session().Snapshot()
	if first.Mode != editor.Editing || first.Notice != "" {
		t.Fatal("function-key search failed", first.Mode, first.Notice)
	}
	m = inputKeys(t, m, altEquals(), textKey("s"), textKey("n"))
	if s := m.Session().Snapshot(); s.Gap != first.Gap+11 || s.Mode != editor.Editing {
		t.Fatal("original Search Next did not execute immediately", s.Gap, s.Mode)
	}
	m = inputKeys(t, m, altEquals(), textKey("s"), textKey("p"))
	if s := m.Session().Snapshot(); s.Gap != first.Gap || s.Mode != editor.Editing || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatal("original Search Previous did not return to the first match")
	}
}

func TestEverydaySetupBackupReachesNativePublication(t *testing.T) {
	m, root := everydayUI(t)
	k := everydayKey
	m = inputKeys(t, m, textKey("BASE"), k(tea.KeyF10), textKey("BACK.WP"), k(tea.KeyEnter))
	source := filepath.Join(root, "BACK.WP")
	backup := filepath.Join(root, "BACK.BK!")
	first, err := os.ReadFile(source)
	if err != nil {
		t.Fatal(err)
	}
	backupSetting := func(m Model, answer string) Model {
		return inputKeys(t, m, tea.Key{Code: tea.KeyF1, Mod: tea.ModShift}, textKey("3"), textKey("1"),
			textKey("2"), textKey(answer), k(tea.KeyF7))
	}
	m = backupSetting(m, "y")
	m = inputKeys(t, m, textKey("EDIT"), k(tea.KeyF10), k(tea.KeyEnter), textKey("y"))
	if previous, err := os.ReadFile(backup); err != nil || !bytes.Equal(first, previous) {
		t.Fatal("enabled Setup did not preserve the actual prior native file", err)
	}
	m = backupSetting(m, "n")
	m = inputKeys(t, m, textKey("NEXT"), k(tea.KeyF10), k(tea.KeyEnter), textKey("y"))
	if _, err := os.Stat(backup); !os.IsNotExist(err) {
		t.Fatal("disabled Setup did not remove the earlier backup", err)
	}
	if saved, err := os.ReadFile(source); err != nil || !bytes.HasSuffix(saved, []byte("BASEEDITNEXT")) || !bytes.Equal(saved, hBoldNative(t, m)) {
		t.Fatal("ordinary replacement did not publish the current native document", err)
	}
}

func TestEverydayClippedExitCannotLeaveMenu(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("BASE"), altEquals(), textKey("f"))
	raw := hBoldNative(t, m)
	next, _ := m.Update(tea.WindowSizeMsg{Width: 80, Height: 12})
	m = next.(Model)
	m = inputKeys(t, m, textKey("x"), everydayKey(tea.KeyUp), everydayKey(tea.KeyEnter))
	if !m.historic.menu || m.Session().Snapshot().Mode != editor.Editing || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatal("clipped File Exit activated through a hidden row")
	}
}
