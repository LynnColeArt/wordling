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
)

const everydayReference = "../../docs/research/everyday-contract-2026-11-05/qualification"

func referenceFile(t *testing.T, name string) []byte {
	t.Helper()
	data, err := os.ReadFile(filepath.Join(everydayReference, name))
	if err != nil {
		t.Fatal(err)
	}
	return data
}

func everydayFlow(t *testing.T) []byte {
	t.Helper()
	data, err := os.ReadFile("evidence/everyday/FLOW.WP")
	if err != nil {
		t.Fatal(err)
	}
	return data
}

func everydayUI(t *testing.T) (Model, string) {
	t.Helper()
	root := t.TempDir()
	r, m, err := Open(Config{Root: root, Profile: LocalFlat, EditorChrome: true})
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := r.Close(); err != nil {
			t.Error(err)
		}
	})
	return m, root
}

func inputKeys(t *testing.T, m Model, keys ...tea.Key) Model {
	t.Helper()
	for _, k := range keys {
		next, cmd := m.Update(tea.KeyPressMsg(k))
		m = next.(Model)
		for i := 0; cmd != nil; i++ {
			if i > 8 {
				t.Fatal("unbounded command chain")
			}
			next, cmd = m.Update(cmd())
			m = next.(Model)
		}
	}
	return m
}

func everydayKey(code rune) tea.Key { return tea.Key{Code: code} }
func textKey(text string) tea.Key   { return tea.Key{Code: rune(text[0]), Text: text} }

func assertScreenRows(t *testing.T, m Model, rows map[int]string) {
	t.Helper()
	lines := strings.Split(ansi.Strip(m.View().Content), "\n")
	for row, want := range rows {
		if row >= len(lines) || !strings.Contains(lines[row], want) {
			t.Fatalf("expected %q at row %d, got rows %q", want, row, lines)
		}
	}
}

func TestEverydayRevealSharesNativeLayoutAt80x25(t *testing.T) {
	m, root := everydayUI(t)
	raw := everydayFlow(t)
	if err := os.WriteFile(filepath.Join(root, "FLOW.WP"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("FLOW.WP"), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF11))
	if !m.Session().Snapshot().Reveal || !bytes.Equal(hBoldNative(t, m), raw) {
		t.Fatal("Reveal did not retain retrieved native revision", m.State())
	}
	assertScreenRows(t, m, map[int]string{
		1:  "A faithful reconstruction needs more than a blue screen. Menus,",
		5:  "     Tab alpha alpha",
		11: "Doc 1 Pg 1 Ln 1\" Pos 1\"",
		12: "{    ▲",
		13: "Menus,[SRt]",
		15: "[HRt]",
		16: "Plain [UND]UNDER[und] after[HRt]",
		17: "[Tab]Tab alpha alpha[HRt]",
		18: "XXXXXXXXXX[DSRt]",
		24: "Press Reveal Codes to restore screen",
	})
	if !strings.Contains(m.View().Content, revealActive+"A") {
		t.Fatal("original active Reveal owner lacks its red role")
	}
	before := m.Session().Snapshot()
	next, cmd := m.Update(tea.WindowSizeMsg{Width: 60, Height: 17})
	if cmd != nil {
		t.Fatal("resize dispatched IO")
	}
	m = next.(Model)
	if !reflect.DeepEqual(m.Session().Snapshot(), before) || !bytes.Equal(hBoldNative(t, m), raw) {
		t.Fatal("resize changed native state")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF11))
	if m.Session().Snapshot().Reveal || m.Session().Snapshot().Gap != before.Gap {
		t.Fatal("closing Reveal changed document caret")
	}
}

func TestEverydaySearchKeysAndMenuShareSession(t *testing.T) {
	m, root := everydayUI(t)
	raw := everydayFlow(t)
	if err := os.WriteFile(filepath.Join(root, "FLOW.WP"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("FLOW.WP"), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF2))
	assertScreenRows(t, m, map[int]string{24: "-> Srch:"})
	m = inputKeys(t, m, textKey("alpha"), everydayKey(tea.KeyF2))
	found := m.Session().Snapshot()
	if found.Mode != editor.Editing || found.Gap == 0 || !bytes.Equal(hBoldNative(t, m), raw) {
		t.Fatal(found)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF11), tea.Key{Code: tea.KeyF2, Mod: tea.ModShift})
	assertScreenRows(t, m, map[int]string{11: "<- Srch:"})
	m = inputKeys(t, m, everydayKey(tea.KeyF1))
	if m.Session().Snapshot().Gap != found.Gap {
		t.Fatal("cancel moved caret")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF2), textKey("nonesuch"))
	next, timer := m.Update(tea.KeyPressMsg{Code: tea.KeyF2})
	m = next.(Model)
	assertScreenRows(t, m, map[int]string{11: "* Not found *"})
	if timer == nil || m.Session().Snapshot().Gap != found.Gap || !bytes.Equal(hBoldNative(t, m), raw) {
		t.Fatal("not found altered the native document")
	}
	next, _ = m.Update(searchNoticeExpired{m.Session().Snapshot().Revision})
	m = next.(Model)
	if strings.Contains(ansi.Strip(m.View().Content), "* Not found *") {
		t.Fatal("search notice did not clear")
	}
	m = inputKeys(t, m, tea.Key{Code: '=', Mod: tea.ModAlt, Text: "="}, textKey("s"), textKey("f"))
	if m.Session().Snapshot().Mode != editor.SearchForwardMode {
		t.Fatal("Search menu bypassed forward session command")
	}
}

func TestEverydayBrowseLookAndOccupiedRetrieve(t *testing.T) {
	m, root := everydayUI(t)
	child := filepath.Join(root, "CHILD")
	if err := os.Mkdir(child, 0700); err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{"A.TXT", "A.WP"} {
		if err := os.WriteFile(filepath.Join(child, name), referenceFile(t, "files/exports/"+name), 0600); err != nil {
			t.Fatal(err)
		}
	}
	m = inputKeys(t, m, textKey("CURRENT "), everydayKey(tea.KeyF5))
	assertScreenRows(t, m, map[int]string{24: `Dir C:\*.*`})
	m = inputKeys(t, m, everydayKey(tea.KeyEnter), textKey("n"), textKey(`\CHILD`), everydayKey(tea.KeyEnter), textKey("6"))
	assertScreenRows(t, m, map[int]string{24: `Dir C:\CHILD\*.*`})
	m = inputKeys(t, m, everydayKey(tea.KeyEnter), textKey("5"), textKey("2"), everydayKey(tea.KeyEnter), textKey("n"), textKey("A.TXT"), everydayKey(tea.KeyEnter))
	before, selection := hBoldNative(t, m), m.historic.browser.selected
	m = inputKeys(t, m, textKey("6"))
	assertScreenRows(t, m, map[int]string{0: `File: C:\CHILD\A.TXT`, 3: "SECOND CHANGE", 24: "Look: 1 Next Doc; 2 Prev Doc: 0"})
	m = inputKeys(t, m, textKey("1"))
	assertScreenRows(t, m, map[int]string{0: `File: C:\CHILD\A.WP`, 3: "SECOND CHANGE UNSAVED"})
	m = inputKeys(t, m, textKey("2"), everydayKey(tea.KeyF7))
	if selection != m.historic.browser.selected || !bytes.Equal(hBoldNative(t, m), before) {
		t.Fatal("Look changed selection or editor document")
	}
	m = inputKeys(t, m, textKey("1"))
	assertScreenRows(t, m, map[int]string{24: "Retrieve into current document? No (Yes)"})
	m = inputKeys(t, m, everydayKey(tea.KeyEnter))
	if m.historic.browser.phase != fileListing || selection != m.historic.browser.selected || !bytes.Equal(hBoldNative(t, m), before) {
		t.Fatal("default No changed list selection or editor document")
	}
	m = inputKeys(t, m, textKey("1"), textKey("y"))
	if m.historic.files || !bytes.HasSuffix(hBoldNative(t, m), []byte("CURRENT SECOND CHANGE")) {
		t.Fatal("confirmed selected acquisition did not insert at the editor caret", m.State())
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF5), everydayKey(tea.KeyF5), textKey("n"), textKey(".."), everydayKey(tea.KeyEnter), textKey("6"), everydayKey(tea.KeyEnter))
	assertScreenRows(t, m, map[int]string{0: `Directory C:\*.*`})
}

func TestEverydayRevealPageJumpAndLowerFocus(t *testing.T) {
	m, root := everydayUI(t)
	raw := everydayFlow(t)
	if err := os.WriteFile(filepath.Join(root, "FLOW.WP"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("FLOW.WP"), everydayKey(tea.KeyEnter),
		everydayKey(tea.KeyF11), everydayKey(tea.KeyPgDown))
	assertScreenRows(t, m, map[int]string{
		11: "Doc 1 Pg 2 Ln 1\" Pos 1\"",
		15: "[HRt-SPg]",
		16: "[Dorm HRt][HRt]",
	})
	lines := strings.Split(m.View().Content, "\n")
	if !strings.Contains(lines[16], revealActive+"[Dorm HRt]") {
		t.Fatal("page jump lost active code focus", lines[16])
	}
	m = inputKeys(t, m, everydayKey(tea.KeyPgDown))
	assertScreenRows(t, m, map[int]string{11: "Doc 1 Pg 3 Ln 1\" Pos 1\""})
	m = inputKeys(t, m, everydayKey(tea.KeyPgUp))
	assertScreenRows(t, m, map[int]string{11: "Doc 1 Pg 2 Ln 1\" Pos 1\""})
	if !bytes.Equal(hBoldNative(t, m), raw) {
		t.Fatal("page navigation altered native bytes")
	}
}

func TestEverydayUndeleteProjectsVirtualWrapAndHistory(t *testing.T) {
	m, _ := everydayUI(t)
	line := strings.Repeat("X", 64)
	m = inputKeys(t, m, textKey(line+"YZ"), everydayKey(tea.KeyBackspace), everydayKey(tea.KeyBackspace), everydayKey(tea.KeyBackspace))
	before := hBoldNative(t, m)
	m = inputKeys(t, m, everydayKey(tea.KeyF11), everydayKey(tea.KeyF1))
	assertScreenRows(t, m, map[int]string{
		1:  line + "Y",
		2:  "Z",
		13: line + "[Block]Y[DSRt]",
		14: "Z",
	})
	if m.Session().Snapshot().Mode != editor.HistoryPreview || !bytes.Equal(before, hBoldNative(t, m)) {
		t.Fatal("projecting Undelete mutated the original revision")
	}
	if !strings.Contains(strings.Split(m.View().Content, "\n")[1], revealActive+"Y") {
		t.Fatal("projected deleted character is missing the original red upper-pane role")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1))
	if !bytes.Equal(before, hBoldNative(t, m)) || m.Session().Snapshot().Mode != editor.Editing {
		t.Fatal("cancelling virtual preview changed native bytes")
	}
}

func TestEverydayOriginalHomeAndEndOnPhysicalLine(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("ABCDEFGHIJ"), everydayKey(tea.KeyEnter), textKey("XYZ"), everydayKey(tea.KeyLeft))
	raw := hBoldNative(t, m)
	m = inputKeys(t, m, everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyLeft))
	if m.Session().Snapshot().Gap != 11 {
		t.Fatal("Home Home Left did not reach the current physical line start")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnd))
	if m.Session().Snapshot().Gap != 14 {
		t.Fatal("End did not reach the current physical line end")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyUp))
	if m.Session().Snapshot().Gap != 0 || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatal("Home Home Up changed bytes or missed document start")
	}
}

func TestEverydayResizeRetainsDirectoryAndListingFocus(t *testing.T) {
	for _, mode := range []filePhase{fileDirectory, fileListing} {
		m, _ := everydayUI(t)
		m = inputKeys(t, m, textKey("BASE"), everydayKey(tea.KeyF5))
		if mode == fileListing {
			m = inputKeys(t, m, everydayKey(tea.KeyEnter))
		}
		before := m.Session().Snapshot()
		raw := hBoldNative(t, m)
		for _, height := range []int{12, 11, 25, 11, 12, 25} {
			next, cmd := m.Update(tea.WindowSizeMsg{Width: 80, Height: height})
			if cmd != nil {
				t.Fatal("resize dispatched document work")
			}
			m = inputKeys(t, next.(Model), textKey("x"))
			if !m.historic.files || m.historic.browser.phase != mode || !reflect.DeepEqual(m.Session().Snapshot(), before) || !bytes.Equal(raw, hBoldNative(t, m)) {
				t.Fatalf("input leaked out of browser phase %v at %d rows", mode, height)
			}
			if height < 12 && (m.View().Cursor != nil || !strings.Contains(m.View().Content, "List Files active")) {
				t.Fatal("small viewport concealed active browser focus")
			}
		}
		m = inputKeys(t, m, everydayKey(tea.KeyF7), textKey("Y"))
		if m.historic.files || !bytes.HasSuffix(hBoldNative(t, m), []byte("BASEY")) {
			t.Fatal("browser cancel did not return editor input focus")
		}
	}
}

func TestEverydayListFilesHistoricalCellsAndResidentSize(t *testing.T) {
	m, root := everydayUI(t)
	raw := everydayFlow(t)
	if err := os.WriteFile(filepath.Join(root, "FLOW.WP"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF5), everydayKey(tea.KeyEnter))
	rows := strings.Split(ansi.Strip(m.View().Content), "\n")
	if len(rows) != 25 || !strings.HasPrefix(rows[1], "Document size:        0   Free:") ||
		!strings.Contains(rows[3], "│") || []rune(rows[3])[39] != '│' {
		t.Fatalf("List Files 80×25 geometry: %q", rows[:4])
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF7), textKey("ABCD"), everydayKey(tea.KeyF5), everydayKey(tea.KeyEnter))
	assertScreenRows(t, m, map[int]string{1: "Document size:      262   Free:"})
	m = inputKeys(t, m, everydayKey(tea.KeyF7), tea.Key{Code: tea.KeyF3, Mod: tea.ModShift},
		tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("FLOW.WP"), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF5), everydayKey(tea.KeyEnter))
	assertScreenRows(t, m, map[int]string{1: "Document size:      963   Free:"})
}
