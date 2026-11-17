package tui

import (
	"bytes"
	"encoding/binary"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
	"time"

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

func TestEverydayWordNavigation(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("alpha  beta,gamma delta-epsilon. next"), everydayKey(tea.KeyEnter), textKey("second line"),
		everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyUp))
	check := func(key rune, gaps ...int) {
		t.Helper()
		for _, gap := range gaps {
			m = inputKeys(t, m, tea.Key{Code: key, Mod: tea.ModCtrl})
			if got := m.Session().Snapshot().Gap; got != gap {
				t.Fatalf("word motion reached gap %d, want %d (%s)", got, gap, m.notice)
			}
		}
	}
	before := hBoldNative(t, m)
	check(tea.KeyRight, 7, 18, 33, 38, 45, 49, 49)
	check(tea.KeyLeft, 45, 38, 33, 18, 7, 0, 0)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	check(tea.KeyRight, 7, 18)
	if !bytes.Equal(hBoldNative(t, m), before) {
		t.Fatal("word motion changed the native document")
	}
}

func TestEverydayBlockSeeksCharacterOrHardReturn(t *testing.T) {
	m, _ := everydayUI(t)
	home, up, enter, cancel := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF1)
	block := tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}
	m = inputKeys(t, m, textKey("alpha beta gamma"), enter, textKey("next Alpha beta"))
	before := hBoldNative(t, m)
	m = inputKeys(t, m, home, home, up, block, textKey("G"))
	if s := m.Session().Snapshot(); !s.Selection || s.Gap != 0 {
		t.Fatalf("case-sensitive Block seek moved on a miss: %+v", s)
	}
	m = inputKeys(t, m, textKey("g"))
	if s := m.Session().Snapshot(); !s.Selection || s.Gap != 12 {
		t.Fatalf("Block seek should select through g: %+v", s)
	}
	m = inputKeys(t, m, cancel, home, home, up, block, enter)
	if s := m.Session().Snapshot(); !s.Selection || s.Gap != 17 {
		t.Fatalf("Block Enter should cross the next hard return: %+v", s)
	}
	if !bytes.Equal(hBoldNative(t, m), before) {
		t.Fatal("a Block seek changed the document")
	}
}

func TestEverydayGoTo(t *testing.T) {
	m, _ := everydayUI(t)
	home, up, enter := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyEnter)
	goTo := tea.Key{Code: tea.KeyHome, Mod: tea.ModCtrl}
	m = inputKeys(t, m, textKey("alpha beta gamma"), enter, textKey("next alpha"),
		tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl}, textKey("page two"), home, home, up)
	before := hBoldNative(t, m)
	m = inputKeys(t, m, goTo)
	if s := m.Session().Snapshot(); s.Mode != editor.GoToMode || !strings.HasPrefix(s.Prompt, "Go to") {
		t.Fatalf("missing Go to prompt: %+v", s)
	}
	m = inputKeys(t, m, textKey("b"))
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != 7 {
		t.Fatalf("Go to character did not stop after b: %+v", s)
	}
	m = inputKeys(t, m, goTo, enter, goTo, textKey("z"))
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != 17 {
		t.Fatalf("Go to hard return or character miss changed the wrong gap: %+v", s)
	}
	m = inputKeys(t, m, goTo, textKey("2"), enter)
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != m.Session().Document().TokenCount()-len("page two") || !strings.Contains(m.View().Content, "Pg 2") {
		t.Fatalf("Go to page did not reach page two: %+v", s)
	}
	m = inputKeys(t, m, tea.Key{Code: '=', Mod: tea.ModAlt, Text: "="}, textKey("s"), textKey("g"), textKey("w"))
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != m.Session().Document().TokenCount()-1 {
		t.Fatalf("Search menu did not reach Go to: %+v", s)
	}
	if !bytes.Equal(hBoldNative(t, m), before) {
		t.Fatal("Go to changed the native document")
	}
}

func TestEverydayWordAndLineDeletion(t *testing.T) {
	const text = "alpha beta gamma\nnext line"
	home, up, right := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyRight)
	for _, tc := range []struct {
		name, want string
		column     int
		keys       []tea.Key
	}{
		{"Ctrl Delete", "alpha gamma\nnext line", 6, []tea.Key{{Code: tea.KeyDelete, Mod: tea.ModCtrl}}},
		{"Ctrl Backspace inside word", "alpha gamma\nnext line", 7, []tea.Key{{Code: tea.KeyBackspace, Mod: tea.ModCtrl}}},
		{"Ctrl Delete on separator", "beta gamma\nnext line", 5, []tea.Key{{Code: tea.KeyDelete, Mod: tea.ModCtrl}}},
		{"Ctrl Delete at hard return", "alpha beta \nnext line", 16, []tea.Key{{Code: tea.KeyDelete, Mod: tea.ModCtrl}}},
		{"Home Backspace", "alpha ta gamma\nnext line", 8, []tea.Key{home, everydayKey(tea.KeyBackspace)}},
		{"Home Delete", "alpha begamma\nnext line", 8, []tea.Key{home, everydayKey(tea.KeyDelete)}},
		{"Ctrl End", "alpha b\nnext line", 7, []tea.Key{{Code: tea.KeyEnd, Mod: tea.ModCtrl}}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			m, _ := everydayUI(t)
			m = inputKeys(t, m, textKey("alpha beta gamma"), everydayKey(tea.KeyEnter), textKey("next line"), home, home, up)
			for range tc.column {
				m = inputKeys(t, m, right)
			}
			m = inputKeys(t, m, tc.keys...)
			if got := hBoldBody(t, m); got != tc.want {
				t.Fatalf("body = %q, want %q (%s)", got, tc.want, m.notice)
			}
			m = inputKeys(t, m, everydayKey(tea.KeyF1), textKey("1"))
			if got := hBoldBody(t, m); got != text {
				t.Fatalf("Undelete restored %q, want %q (%s)", got, text, m.notice)
			}
		})
	}
}

func TestEverydayDeleteFormattedWordKeepsEmptyPair(t *testing.T) {
	m, _ := everydayUI(t)
	home, bold := everydayKey(tea.KeyHome), everydayKey(tea.KeyF6)
	m = inputKeys(t, m, textKey("alpha "), bold, textKey("beta"), bold, textKey(" gamma"), home, home, everydayKey(tea.KeyUp),
		tea.Key{Code: tea.KeyRight, Mod: tea.ModCtrl}, everydayKey(tea.KeyRight), tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt},
		tea.Key{Code: tea.KeyDelete, Mod: tea.ModCtrl})
	const emptyPair = "\xc3\x0c\xc3\xc4\x0c\xc4"
	if got := hBoldBody(t, m); got != "alpha "+emptyPair+"gamma" {
		t.Fatalf("Delete Word kept %x (%s)", got, m.notice)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1), textKey("1"))
	if got := hBoldBody(t, m); got != "alpha "+emptyPair+"beta gamma" {
		t.Fatalf("Undelete kept %x (%s)", got, m.notice)
	}
}

func TestEverydayBlockFormatsAndClearsSelection(t *testing.T) {
	m, _ := everydayUI(t)
	home, right := everydayKey(tea.KeyHome), everydayKey(tea.KeyRight)
	block := tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}
	m = inputKeys(t, m, textKey("alpha beta"), home, home, everydayKey(tea.KeyUp),
		block, right, right, right, right, right, everydayKey(tea.KeyF6))
	const bold = "\xc3\x0c\xc3alpha\xc4\x0c\xc4"
	if s, got := m.Session().Snapshot(), hBoldBody(t, m); s.Selection || got != bold+" beta" {
		t.Fatalf("bold Block left selection=%v and body=%x (%s)", s.Selection, got, m.notice)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt}, block,
		right, right, right, right, right, right, everydayKey(tea.KeyF8))
	const underlined = "\xc3\x0e\xc3 beta\xc4\x0e\xc4"
	if s, got := m.Session().Snapshot(), hBoldBody(t, m); s.Selection || got != bold+underlined {
		t.Fatalf("underline Block left selection=%v and body=%x (%s)", s.Selection, got, m.notice)
	}
}

func TestEverydayBlockConvertCase(t *testing.T) {
	home, up, right := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyRight)
	block := tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}
	convert := tea.Key{Code: tea.KeyF3, Mod: tea.ModShift}
	for _, tc := range []struct {
		body, selection, choice, want string
	}{
		{"alpha beta", "alpha", "1", "ALPHA beta"},
		{"BEFORE. I'M HERE! NEXT? THIRD. I SAID i'M HERE. lower.", "BEFORE. I'M HERE! NEXT? THIRD. I SAID i'M HERE. lower.", "2", "before. I'm here! Next? Third. I said i'm here. lower."},
	} {
		m, _ := everydayUI(t)
		m = inputKeys(t, m, textKey(tc.body), home, home, up, block)
		for range len(tc.selection) {
			m = inputKeys(t, m, right)
		}
		m = inputKeys(t, m, convert)
		if s := m.Session().Snapshot(); s.Mode != editor.ConvertCaseMode || s.Screen != 1 {
			t.Fatalf("Shift+F3 should open case conversion within Block: %+v", s)
		}
		m = inputKeys(t, m, textKey(tc.choice))
		if s, got := m.Session().Snapshot(), hBoldBody(t, m); s.Mode != editor.Editing || s.Selection || got != tc.want {
			t.Fatalf("case conversion returned %q, want %q (mode %s, selection %v)", got, tc.want, s.Mode, s.Selection)
		}
	}
}

func TestEverydayBlockCopy(t *testing.T) {
	m, _ := everydayUI(t)
	home, up, down, right := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyDown), everydayKey(tea.KeyRight)
	bold, enter := everydayKey(tea.KeyF6), everydayKey(tea.KeyEnter)
	block := tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}
	move := tea.Key{Code: tea.KeyF4, Mod: tea.ModCtrl}
	m = inputKeys(t, m, bold, textKey("alpha"), bold, textKey(" beta"), home, home, up, block)
	for range len("alpha") {
		m = inputKeys(t, m, right)
	}
	original := hBoldBody(t, m)
	m = inputKeys(t, m, move, textKey("1"), textKey("2"))
	if s := m.Session().Snapshot(); s.Mode != editor.CopyTargetMode || s.Selection || hBoldBody(t, m) != original {
		t.Fatalf("copy should leave the source intact while choosing a destination: %+v", s)
	}
	m = inputKeys(t, m, home, home, down, enter)
	const styled = "\xc3\x0c\xc3alpha\xc4\x0c\xc4"
	want := styled + " beta" + styled
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != 12 || hBoldBody(t, m) != want {
		t.Fatalf("copy should preserve the original and insert styled text at gap 12: %+v, body %x (%s)", s, hBoldBody(t, m), m.notice)
	}
}

func TestEverydayHardSpace(t *testing.T) {
	m, _ := everydayUI(t)
	prefix := "x " + strings.Repeat("a", 58)
	m = inputKeys(t, m, textKey(prefix+" alpha"), everydayKey(tea.KeyHome), textKey(" "), textKey("beta"), tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if got, want := hBoldBody(t, m), prefix+"\ralpha\xa0beta"; got != want {
		t.Fatalf("hard space did not keep the words together: got %x, want %x (%s)", got, want, m.notice)
	}
	if !strings.Contains(ansi.Strip(m.View().Content), "alpha[ ]beta") {
		t.Fatal("Reveal Codes did not show the hard space")
	}
	expected, err := os.ReadFile("../../docs/research/reference-runs/mission1-line-format/HSPACE.TXT")
	if err != nil {
		t.Fatal(err)
	}
	m, _ = everydayUI(t)
	m = inputKeys(t, m, textKey("alpha"), everydayKey(tea.KeyHome), textKey(" "), textKey("beta"))
	if got, err := m.Session().Document().ExportDOSText(); err != nil || !bytes.Equal(got, expected) {
		t.Fatalf("hard space DOS export = %x, %v; want %x", got, err, expected)
	}
}

func TestEverydayDeletePageRemainder(t *testing.T) {
	m, _ := everydayUI(t)
	home, up, enter := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyEnter)
	deletePage := tea.Key{Code: tea.KeyPgDown, Mod: tea.ModCtrl}
	m = inputKeys(t, m, textKey("keep remove"), enter, textKey("remove again"),
		tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl}, textKey("next page"), home, home, up)
	for range len("keep ") {
		m = inputKeys(t, m, everydayKey(tea.KeyRight))
	}
	original := hBoldBody(t, m)
	m = inputKeys(t, m, deletePage)
	if s := m.Session().Snapshot(); s.Prompt != "Delete Remainder of page? No (Yes)" || s.Gap != 5 {
		t.Fatalf("missing delete page confirmation: %+v", s)
	}
	m = inputKeys(t, m, enter)
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != 5 || hBoldBody(t, m) != original {
		t.Fatalf("declining originally leaves the page and caret intact: %+v", s)
	}
	m = inputKeys(t, m, deletePage, textKey("y"))
	fixture, err := os.ReadFile("../../docs/research/reference-runs/mission1-page-delete/DELPG.WP")
	if err != nil {
		t.Fatal(err)
	}
	expected := fixture[binary.LittleEndian.Uint32(fixture[4:8]):]
	if got := hBoldBody(t, m); got != string(expected) {
		t.Fatalf("delete page body = %x, want %x (%s)", got, expected, m.notice)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1), textKey("1"))
	if got := hBoldBody(t, m); got != original {
		t.Fatalf("expected one Undelete to restore the removed page text, got %x (%s)", got, m.notice)
	}
}

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
	next, _ = m.Update(searchNoticeExpired{m.searchNotice})
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

func TestEverydayHomeMovesAroundInitialFormatting(t *testing.T) {
	m, _ := everydayUI(t)
	home, up, left, right := everydayKey(tea.KeyHome), everydayKey(tea.KeyUp), everydayKey(tea.KeyLeft), everydayKey(tea.KeyRight)
	b, u := everydayKey(tea.KeyF6), everydayKey(tea.KeyF8)
	m = inputKeys(t, m, b, u, textKey("alpha"), b, u, textKey(" beta"), tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	before := hBoldNative(t, m)
	m = inputKeys(t, m, home, home, up)
	if got := m.Session().Snapshot().Gap; got != 2 {
		t.Fatalf("Home Home Up should pass the two opening codes, got gap %d", got)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnd), home, home, home, up)
	if got := m.Session().Snapshot().Gap; got != 0 {
		t.Fatalf("Home Home Home Up should stop before the opening codes, got gap %d", got)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnd), home, left)
	if got := m.Session().Snapshot().Gap; got != 2 {
		t.Fatalf("Home Left should reach the visible left edge, got gap %d", got)
	}
	m = inputKeys(t, m, home, right)
	if s := m.Session().Snapshot(); s.Gap != m.Session().Document().TokenCount() || !bytes.Equal(before, hBoldNative(t, m)) {
		t.Fatalf("Home Right should reach the visible right edge: %+v", s)
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

func TestEverydayFileDisplayConfirmsDirectoryAndConservesContext(t *testing.T) {
	m, root := everydayUI(t)
	if err := os.WriteFile(filepath.Join(root, "FLOW.WP"), everydayFlow(t), 0600); err != nil {
		t.Fatal(err)
	}
	key := everydayKey
	m = inputKeys(t, m, textKey("CURRENT"), key(tea.KeyF5), textKey(`F*.WP`), key(tea.KeyEnter),
		textKey("n"), textKey("FLOW.WP"), key(tea.KeyEnter))
	before, raw := m.Session().Snapshot(), hBoldNative(t, m)
	list, selected := m.historic.browser.list, m.historic.browser.selected
	caret := func(x int) {
		t.Helper()
		if c := m.View().Cursor; c == nil || c.X != x || c.Y != 24 {
			t.Fatalf("directory command caret: %+v, want [%d,24]", c, x)
		}
	}
	m = inputKeys(t, m, textKey("5"))
	assertScreenRows(t, m, map[int]string{24: "1 Short Display; 2 Long Display: 2"})
	caret(33)
	m = inputKeys(t, m, textKey("2"))
	assertScreenRows(t, m, map[int]string{24: `Dir C:\F*.WP`})
	caret(4)
	if m.historic.browser.phase != fileDirectory || m.historic.browser.long {
		t.Fatal("Long appeared before confirming the directory")
	}
	m = inputKeys(t, m, key(tea.KeyF1))
	if b := m.historic.browser; b.phase != fileListing || b.list != list || b.selected != selected || b.long {
		t.Fatal("F1 changed the cached short listing or its selection")
	}
	m = inputKeys(t, m, textKey("5"), key(tea.KeyEnter))
	assertScreenRows(t, m, map[int]string{24: `Dir C:\F*.WP`})
	caret(4)
	m = inputKeys(t, m, key(tea.KeyF7))
	assertScreenRows(t, m, map[int]string{0: `Directory C:\F*.WP`, 2: "Descriptive Name", 24: "N Name Search:"})
	if !m.historic.browser.long {
		t.Fatal("original F7 did not confirm Long at the directory request")
	}
	m = inputKeys(t, m, textKey("5"), textKey("1"))
	assertScreenRows(t, m, map[int]string{2: "Descriptive Name", 24: `Dir C:\F*.WP`})
	caret(4)
	m = inputKeys(t, m, key(tea.KeyEscape))
	if b := m.historic.browser; b.phase != fileListing || !b.long {
		t.Fatal("Escape changed the cached long display")
	}
	m = inputKeys(t, m, textKey("5"), textKey("1"), key(tea.KeyEnter))
	assertScreenRows(t, m, map[int]string{0: `Directory C:\F*.WP`, 3: "│", 24: "N Name Search:"})
	if !reflect.DeepEqual(m.Session().Snapshot(), before) || !bytes.Equal(hBoldNative(t, m), raw) || m.historic.browser.long {
		t.Fatal("changing the confirmed listing altered the editor or lost short display")
	}
}

func TestEverydaySearchExpiryBelongsToExactResult(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, textKey("ABCD"))
	raw := hBoldNative(t, m)
	before := m.Session().Snapshot()
	miss := func(query string) tea.Cmd {
		t.Helper()
		m = inputKeys(t, m, everydayKey(tea.KeyF2), textKey(query))
		next, timer := m.Update(tea.KeyPressMsg{Code: tea.KeyF2})
		m = next.(Model)
		assertScreenRows(t, m, map[int]string{24: "* Not found *"})
		if timer == nil {
			t.Fatal("failed search did not return its actual timer")
		}
		return timer
	}
	first := miss("missing")
	second := miss("absent")
	next, _ := m.Update(first())
	m = next.(Model)
	assertScreenRows(t, m, map[int]string{24: "* Not found *"})
	next, _ = m.Update(second())
	m = next.(Model)
	assertScreenRows(t, m, map[int]string{24: "Doc 1 Pg 1 Ln 1\" Pos 1.4\""})
	if after := m.Session().Snapshot(); after.Gap != before.Gap || after.NativeRevision != before.NativeRevision || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatal("settling timed notices moved the native cursor or changed bytes")
	}
}

func TestSearchBoldOffAlone(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, everydayKey(tea.KeyF6), textKey("bold"), everydayKey(tea.KeyF6), textKey(" plain"),
		everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyHome), everydayKey(tea.KeyUp),
		tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	raw := hBoldNative(t, m)
	m = inputKeys(t, m, everydayKey(tea.KeyF2), everydayKey(tea.KeyF6), everydayKey(tea.KeyF6),
		everydayKey(tea.KeyLeft), everydayKey(tea.KeyBackspace))
	if s := m.Session().Snapshot(); s.Draft != "[bold]" || s.Caret != 0 {
		t.Fatalf("wanted just the closing owner: %+v", s)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF2))
	if s := m.Session().Snapshot(); s.Mode != editor.Editing || s.Gap != 6 || !bytes.Equal(raw, hBoldNative(t, m)) {
		t.Fatalf("search did not land after the closing owner without editing: %+v", s)
	}
}

func TestListFilesCopyRenameAndDeclineDelete(t *testing.T) {
	m, root := everydayUI(t)
	raw := []byte("alpha\r\nbeta\r\n")
	if err := os.WriteFile(filepath.Join(root, "INPUT.TXT"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter, textKey("n"), textKey("INPUT.TXT"), enter,
		textKey("2"))
	assertScreenRows(t, m, map[int]string{24: `Delete C:\INPUT.TXT? No (Yes)`})
	m = inputKeys(t, m, textKey("n"), textKey("8"), textKey("COPY.TXT"), enter,
		textKey("n"), textKey("COPY.TXT"), enter, textKey("3"), textKey("RENAMED.TXT"), enter)
	for _, name := range []string{"INPUT.TXT", "RENAMED.TXT"} {
		if got, err := os.ReadFile(filepath.Join(root, name)); err != nil || !bytes.Equal(got, raw) {
			t.Fatalf("%s: %q, %v (%s)", name, got, err, m.historic.browser.message)
		}
	}
	if _, err := os.Stat(filepath.Join(root, "COPY.TXT")); !os.IsNotExist(err) {
		t.Fatalf("rename left the old name: %v", err)
	}
	m = inputKeys(t, m, textKey("n"), textKey("RENAMED.TXT"), enter, textKey("8"), textKey("INPUT.TXT"), enter)
	if m.historic.browser.message != "destination already exists" {
		t.Fatal("copy did not refuse the collision")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1), textKey("2"), textKey("y"))
	if _, err := os.Stat(filepath.Join(root, "RENAMED.TXT")); !os.IsNotExist(err) {
		t.Fatalf("confirmed deletion did not remove the selected copy: %v", err)
	}
}

func TestDOSHardReturnImportMatchesNativeReference(t *testing.T) {
	m, root := everydayUI(t)
	raw := referenceFile(t, "dos-text-file-operations-r3/exports/INPUT.TXT")
	if err := os.WriteFile(filepath.Join(root, "INPUT.TXT"), raw, 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("1"), textKey("2"),
		textKey("INPUT.TXT"), everydayKey(tea.KeyEnter))
	want := referenceFile(t, "dos-text-file-operations-r3/exports/HARD.WP")
	if got := hBoldBody(t, m); got != string(want[324:]) {
		t.Fatalf("import body = %q, DOS = %q (%s)", got, want[324:], m.notice)
	}
	if !m.Session().Snapshot().Dirty {
		t.Fatal("imported content needs a native save")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF10), textKey("OUT.WP"), everydayKey(tea.KeyEnter))
	if got, err := os.ReadFile(filepath.Join(root, "OUT.WP")); err != nil || !bytes.HasSuffix(got, want[324:]) {
		t.Fatalf("native save did not preserve the DOS body: %v (%s)", err, m.notice)
	}
}

func TestDOSTextImportMatchesReferenceBodies(t *testing.T) {
	for _, tc := range []struct{ fixture, name, mode string }{
		{"dos-import-chars-r1", "CHARS", "2"},
		{"dos-import-other-r1", "OTHER", "2"},
		{"dos-import-zone-r1", "ZONE", "3"},
		{"dos-import-zone-r3", "ZONE", "3"},
		{"dos-import-zone-r5", "ZONE", "3"},
	} {
		t.Run(tc.fixture, func(t *testing.T) {
			m, root := everydayUI(t)
			prefix, source := tc.fixture+"/exports/"+tc.name, tc.name+".TXT"
			if err := os.WriteFile(filepath.Join(root, source), referenceFile(t, prefix+".TXT"), 0600); err != nil {
				t.Fatal(err)
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("1"),
				textKey(tc.mode), textKey(source), everydayKey(tea.KeyEnter))
			want := referenceFile(t, prefix+".WP")
			if got := hBoldBody(t, m); !bytes.Equal([]byte(got), want[324:]) {
				t.Fatalf("native body differs from the DOS save (got %d bytes, want %d): %s", len(got), len(want)-324, m.notice)
			}
			if s := m.Session().Snapshot(); s.Gap != 0 || !s.Dirty {
				t.Fatalf("import should leave the cursor before the unsaved text: %+v", s)
			}
		})
	}
}

func TestDOSFileWorkflow(t *testing.T) {
	m, root := everydayUI(t)
	const fixture = "dos-find-export-acceptance/exports/"
	for _, name := range []string{"AMBER.WP", "BLUE.WP"} {
		if err := os.WriteFile(filepath.Join(root, name), referenceFile(t, fixture+name), 0600); err != nil {
			t.Fatal(err)
		}
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("AMBER.WP"), enter)
	before := hBoldNative(t, m)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("1"), textKey("1"), textKey("AMBER.TXT"), enter)
	got, err := os.ReadFile(filepath.Join(root, "AMBER.TXT"))
	if err != nil || !bytes.Equal(got, referenceFile(t, fixture+"AMBER.TXT")) {
		t.Fatalf("DOS text output = %q, %v (%s)", got, err, m.notice)
	}
	if !bytes.Equal(before, hBoldNative(t, m)) {
		t.Fatal("text export changed the native document")
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter, textKey("9"), textKey("4"), textKey("amber"), enter)
	b := m.historic.browser
	if len(b.entries) != 2 || b.entries[0].DOSName != "AMBER.TXT" || b.entries[1].DOSName != "AMBER.WP" {
		t.Fatalf("unexpected Find results: %v", b.entries)
	}
	m = inputKeys(t, m, textKey("n"), textKey("AMBER.WP"), enter, textKey("8"), textKey("COPY.WP"), enter)
	if raw, err := os.ReadFile(filepath.Join(root, "COPY.WP")); err != nil || !bytes.Equal(raw, referenceFile(t, fixture+"AMBER.WP")) {
		t.Fatalf("copy from Find results used the wrong file: %v", err)
	}
	m = inputKeys(t, m, textKey("9"), textKey("4"), textKey("unmatched"), enter, textKey("9"), textKey("6"))
	if len(m.historic.browser.entries) != 4 {
		t.Fatalf("Undo Find did not restore the directory: %v", m.historic.browser.entries)
	}
}

func TestDOSTextControlBytesRoundTrip(t *testing.T) {
	for _, tc := range []struct{ input, native, output, first, second string }{
		{"CTRL.TXT", "CTRL.WP", "BACK.TXT", "00A^@B", "01A^AB"},
		{"LINES.TXT", "LINES.WP", "LINESOUT.TXT", "FG", "D"},
		{"CP437.TXT", "CP437.WP", "CP437OUT.TXT", "7FA", "80A"},
	} {
		t.Run(tc.input, func(t *testing.T) {
			checkDOSTextControlBytesRoundTrip(t, tc.input, tc.native, tc.output, tc.first, tc.second)
		})
	}
}

func checkDOSTextControlBytesRoundTrip(t *testing.T, inputName, nativeName, outputName, first, second string) {
	t.Helper()
	m, root := everydayUI(t)
	const fixture = "mission1-list-dos-text/"
	input := referenceFile(t, fixture+inputName)
	if err := os.WriteFile(filepath.Join(root, inputName), input, 0600); err != nil {
		t.Fatal(err)
	}
	enter := everydayKey(tea.KeyEnter)
	textInOut := tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}
	m = inputKeys(t, m, textInOut, textKey("1"), textKey("2"), textKey(inputName), enter)
	want := referenceFile(t, fixture+nativeName)
	if got := hBoldBody(t, m); !bytes.Equal([]byte(got), want[324:]) {
		t.Fatalf("control-byte import differs from DOS: %x (%s)", got, m.notice)
	}
	if frame := ansi.Strip(m.View().Content); !strings.Contains(frame, first) || !strings.Contains(frame, second) {
		t.Fatalf("the original control labels are missing from the editor: %q", frame)
	}
	m = inputKeys(t, m, textInOut, textKey("1"), textKey("1"), textKey("BACK.TXT"), enter)
	got, err := os.ReadFile(filepath.Join(root, "BACK.TXT"))
	if err != nil || !bytes.Equal(got, referenceFile(t, fixture+outputName)) {
		t.Fatalf("control-byte export differs from DOS: %x, %v (%s)", got, err, m.notice)
	}
	if got := hBoldBody(t, m); !bytes.Equal([]byte(got), want[324:]) {
		t.Fatal("DOS text export changed the native body")
	}
}

func TestListFilesFindUndoRetainsThreeSearches(t *testing.T) {
	m, root := everydayUI(t)
	for _, name := range []string{"AMBER.WP", "BLUE.WP", "A.TXT"} {
		if err := os.WriteFile(filepath.Join(root, name), nil, 0600); err != nil {
			t.Fatal(err)
		}
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter)
	for _, query := range []string{"WP", "AMBER", "MISSING", "AMBER"} {
		m = inputKeys(t, m, textKey("9"), textKey("1"), textKey(query), enter)
	}
	for _, want := range []int{0, 1, 2, 2} {
		m = inputKeys(t, m, textKey("9"), textKey("6"))
		if got := len(m.historic.browser.entries); got != want {
			t.Fatalf("Undo restored %d files, want %d", got, want)
		}
	}
}

func TestListFilesFindPatterns(t *testing.T) {
	m, root := everydayUI(t)
	for name, content := range map[string]string{
		"BETWEEN.TXT": "replace the B diskette", "BLUE.TXT": "jade dark", "EXACT.TXT": "replace disk",
		"FOUR-WAY.TXT": "four-way wayward", "PHRASE.TXT": "replace diskette", "RICH.TXT": "amber jade", "Z.TXT": "amber slate",
	} {
		if err := os.WriteFile(filepath.Join(root, name), []byte(content+"\x1a"), 0600); err != nil {
			t.Fatal(err)
		}
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter)
	for _, tc := range []struct{ scope, query, want string }{
		{"4", "am*er", "RICH.TXT,Z.TXT"}, {"4", "j?de", "BLUE.TXT,RICH.TXT"},
		{"4", "amber jade", "RICH.TXT"}, {"4", "jade, slate", "BLUE.TXT,RICH.TXT,Z.TXT"},
		{"4", "jade,slate amber", "RICH.TXT,Z.TXT"}, {"4", "amber-slate", "RICH.TXT"},
		{"4", "-amber", "BETWEEN.TXT,BLUE.TXT,EXACT.TXT,FOUR-WAY.TXT,PHRASE.TXT"},
		{"4", `"replace disk"`, "EXACT.TXT,PHRASE.TXT"}, {"4", `"replace disk "`, ""},
		{"4", `"replace*disk"`, "BETWEEN.TXT,EXACT.TXT,PHRASE.TXT"}, {"4", `"four-way"`, "FOUR-WAY.TXT"},
		{"1", "?ich", "RICH.TXT"}, {"1", `"four-way"`, "FOUR-WAY.TXT"}, {"1", "ich.txt", "RICH.TXT"},
	} {
		m = inputKeys(t, m, textKey("9"), textKey(tc.scope), textKey(tc.query), enter)
		var got []string
		for _, entry := range m.historic.browser.entries {
			got = append(got, entry.DOSName)
		}
		if strings.Join(got, ",") != tc.want {
			t.Fatalf("Find %q returned %v, want %q", tc.query, got, tc.want)
		}
		m = inputKeys(t, m, textKey("9"), textKey("6"))
	}
}

func TestListFilesRevisionDatesAndSummaryFields(t *testing.T) {
	m, root := everydayUI(t)
	for day, name := range map[int]string{9: "FIELDS.WP", 10: "RICH.WP"} {
		fixture := "mission1-list-dos-text/" + name
		if name == "RICH.WP" {
			fixture = "dos-list-conditions-results/exports/RICH.WP"
		}
		path := filepath.Join(root, name)
		if err := os.WriteFile(path, referenceFile(t, fixture), 0600); err != nil {
			t.Fatal(err)
		}
		stamp := time.Date(1992, 3, day, 12, 0, 0, 0, time.Local)
		if err := os.Chtimes(path, stamp, stamp); err != nil {
			t.Fatal(err)
		}
	}
	enter, down := everydayKey(tea.KeyEnter), everydayKey(tea.KeyDown)
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter)
	search := func(want string, keys ...tea.Key) {
		t.Helper()
		m = inputKeys(t, m, textKey("9"), textKey("5"), textKey("2"))
		m = inputKeys(t, m, keys...)
		m = inputKeys(t, m, enter, textKey("1"))
		var got []string
		for _, entry := range m.historic.browser.entries {
			got = append(got, entry.DOSName)
		}
		if strings.Join(got, ",") != want {
			t.Fatalf("Find returned %v, want %q for %v", got, want, keys)
		}
		m = inputKeys(t, m, textKey("9"), textKey("6"))
	}
	search("", textKey("3"), textKey("03-08-92"))
	search("", textKey("3"), down, textKey("03-08-92"))
	search("FIELDS.WP", textKey("3"), textKey("03/09/1992"), down, textKey("03/09/1992"))
	search("FIELDS.WP,RICH.WP", textKey("3"), textKey("03/09/1992"), down, textKey("03/10/1992"))
	for index, term := range []string{"arbutus", "birch", "cedar", "dogwood", "elm", "fir", "ginkgo", "hawthorn"} {
		keys := []tea.Key{textKey("5")}
		for range index + 2 {
			keys = append(keys, down)
		}
		search("FIELDS.WP", append(keys, textKey(term))...)
	}
}

func TestDOSExportWrappedLinesAndHardPage(t *testing.T) {
	m, root := everydayUI(t)
	m = inputKeys(t, m, textKey(strings.Repeat("word ", 17)+"end"),
		tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl}, textKey("next"),
		tea.Key{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("1"), textKey("1"),
		textKey("LAYOUT.TXT"), everydayKey(tea.KeyEnter))
	got, err := os.ReadFile(filepath.Join(root, "LAYOUT.TXT"))
	if err != nil {
		t.Fatalf("export: %v (%s)", err, m.notice)
	}
	want := referenceFile(t, "dos-export-layout-probe/exports/LAYOUT.TXT")
	if !bytes.Equal(got, want) {
		t.Fatalf("DOS export = %q, want %q", got, want)
	}
}

func TestDOSTextOverwriteChoice(t *testing.T) {
	m, root := everydayUI(t)
	path := filepath.Join(root, "A.TXT")
	if err := os.WriteFile(path, []byte("old"), 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, textKey("amber"))
	openExport := []tea.Key{{Code: tea.KeyF5, Mod: tea.ModCtrl}, textKey("1"), textKey("1"),
		textKey("A.TXT"), everydayKey(tea.KeyEnter)}
	m = inputKeys(t, m, openExport...)
	if got := m.dosTextPrompt(); !strings.Contains(got, "Replace A.TXT? No (Yes)") {
		t.Fatal(got)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyEnter))
	if raw, err := os.ReadFile(path); err != nil || string(raw) != "old" {
		t.Fatalf("declining replacement changed the file: %q, %v", raw, err)
	}
	if got := m.dosTextPrompt(); got != "Document to be saved (DOS Text): " {
		t.Fatalf("decline should return to the filename prompt, got %q", got)
	}
	m = inputKeys(t, m, textKey("A.TXT"), everydayKey(tea.KeyEnter))
	m = inputKeys(t, m, textKey("y"))
	if raw, err := os.ReadFile(path); err != nil || string(raw) != "amber\x1a" {
		t.Fatalf("replacement failed: %q, %v (%s)", raw, err, m.notice)
	}
}

func TestListFilesFindScopesAndPrint(t *testing.T) {
	m, root := everydayUI(t)
	for name, fixture := range map[string]string{
		"Z.WP":    "dos-list-conditions-results/exports/Z.WP",
		"A.WP":    "dos-list-all-modes-r2/exports/A.WP",
		"RICH.WP": "mission1-summary-rich/exports/RICH.WP",
	} {
		path := filepath.Join(root, name)
		if err := os.WriteFile(path, referenceFile(t, fixture), 0600); err != nil {
			t.Fatal(err)
		}
		stamp := time.Date(1992, 3, 9, 12, 0, 0, 0, time.Local)
		if err := os.Chtimes(path, stamp, stamp); err != nil {
			t.Fatal(err)
		}
	}
	enter, down := everydayKey(tea.KeyEnter), everydayKey(tea.KeyDown)
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter)
	check := func(want ...string) {
		t.Helper()
		var got []string
		for _, entry := range m.historic.browser.entries {
			got = append(got, entry.DOSName)
		}
		if strings.Join(got, ",") != strings.Join(want, ",") {
			t.Fatalf("listing = %v, want %v", got, want)
		}
	}
	for _, tc := range []struct{ scope, query, want string }{
		{"1", "Z", "Z.WP"}, {"2", "Bold", "RICH.WP"}, {"3", "amber", "Z.WP"},
		{"3", "late", ""}, {"4", "late", "Z.WP"},
	} {
		m = inputKeys(t, m, textKey("9"), textKey(tc.scope), textKey(tc.query), enter)
		if tc.want == "" {
			check()
		} else {
			check(tc.want)
		}
		m = inputKeys(t, m, textKey("9"), textKey("6"))
		check("A.WP", "RICH.WP", "Z.WP")
	}
	// DOS briefly reports a miss, then shows an empty listing. The creation
	// lower bound excludes the same day, while the upper bound includes it.
	m = inputKeys(t, m, textKey("9"), textKey("5"), textKey("5"), textKey("03-09-92"), enter, textKey("1"))
	check()
	m = inputKeys(t, m, textKey("9"), textKey("6"))
	check("A.WP", "RICH.WP", "Z.WP")
	m = inputKeys(t, m, textKey("9"), textKey("5"), textKey("2"), textKey("5"), textKey("03-08-92"), enter,
		down, enter, textKey("03/09/92"), enter, textKey("1"))
	check("RICH.WP")
	m = inputKeys(t, m, textKey("9"), textKey("6"), textKey("9"), textKey("5"), textKey("2"),
		textKey("5"), everydayKey(tea.KeyF1), down, down, down, down, down, down, enter, textKey("Bold"), enter, textKey("1"))
	check("RICH.WP")
	m = inputKeys(t, m, textKey("9"), textKey("6"), textKey("n"), textKey("Z.WP"), enter, textKey("4"), textKey("6"))
	if m.print.screen != printView || len(m.print.pages) != 2 {
		t.Fatalf("expected two pages from selected file, got %d (%s)", len(m.print.pages), m.print.notice)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF1))
	m.print.port = "Z.PRN"
	m = inputKeys(t, m, textKey("4"))
	if m.print.screen != printListedPages || !strings.Contains(m.View().Content, "Page(s): (All)") {
		t.Fatalf("expected DOS page selection, got %v", m.print.screen)
	}
	m = inputKeys(t, m, enter)
	output, err := os.ReadFile(filepath.Join(root, "Z.PRN"))
	if want := referenceFile(t, "mission1-list-dos-text/LIST.PRN"); err != nil || !bytes.Equal(output, want) {
		t.Fatalf("selected file printer bytes differ from DOS: got %d bytes, want %d, error %v", len(output), len(want), err)
	}
	m.print.port = "PAGE2.PRN"
	m = inputKeys(t, m, textKey("4"), textKey("2"), enter)
	output, err = os.ReadFile(filepath.Join(root, "PAGE2.PRN"))
	if want := referenceFile(t, "mission1-list-dos-text/PAGE2.PRN"); err != nil || !bytes.Equal(output, want) {
		t.Fatalf("selected page printer bytes differ from DOS: got %d bytes, want %d, error %v", len(output), len(want), err)
	}
	m.print.port = "ORDER.PRN"
	m = inputKeys(t, m, textKey("4"), textKey("2"), textKey(","), textKey("1"), textKey(","), textKey("2"), enter)
	output, err = os.ReadFile(filepath.Join(root, "ORDER.PRN"))
	if want := referenceFile(t, "mission1-list-dos-text/ORDER.PRN"); err != nil || !bytes.Equal(output, want) {
		t.Fatalf("out-of-order page requests differ from DOS: got %d bytes, want %d, error %v", len(output), len(want), err)
	}
	m = inputKeys(t, m, everydayKey(tea.KeyF7), tea.Key{Code: tea.KeyF1, Mod: tea.ModShift},
		textKey("3"), textKey("4"), textKey("5"), textKey("n"), everydayKey(tea.KeyF7),
		everydayKey(tea.KeyF5), enter, textKey("n"), textKey("Z.WP"), enter)
	if !m.historic.browser.unsorted || m.historic.browser.selected < 2 ||
		m.historic.browser.entries[m.historic.browser.selected-2].DOSName != "Z.WP" {
		t.Fatalf("sort=%v files=%v phase=%v selection=%d message=%q", m.setup.unsortedFiles, m.historic.files, m.historic.browser.phase, m.historic.browser.selected, m.historic.browser.message)
	}
}

func TestListFilesMarkedFindAndUndo(t *testing.T) {
	m, root := everydayUI(t)
	for _, name := range []string{"A.WP", "B.WP"} {
		fixture := referenceFile(t, "issue7-marked-files/exports/"+name)
		if err := os.WriteFile(filepath.Join(root, name), fixture, 0600); err != nil {
			t.Fatal(err)
		}
	}
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, everydayKey(tea.KeyF5), enter, textKey("n"), textKey("B.WP"), enter, textKey("*"))
	if !strings.Contains(ansi.Strip(m.View().Content), "*B") {
		t.Fatal("marked file has no visible asterisk")
	}
	m = inputKeys(t, m, textKey("9"), textKey("4"), textKey("amber"), enter)
	b := m.historic.browser
	if len(b.entries) != 1 || b.entries[0].DOSName != "B.WP" || len(b.marked) != 0 {
		t.Fatalf("expected an unmarked B.WP in Find results: %v, %v", b.entries, b.marked)
	}
	m = inputKeys(t, m, textKey("9"), textKey("6"))
	if b := m.historic.browser; len(b.entries) != 2 || !b.marked["B.WP"] {
		t.Fatal("Undo did not restore the original listing and its mark")
	}
}

func TestPrintDocumentOnDiskPreservesActiveDocument(t *testing.T) {
	m, root := everydayUI(t)
	const fixture = "dos-list-conditions-results/exports/Z.WP"
	if err := os.WriteFile(filepath.Join(root, "Z.WP"), referenceFile(t, fixture), 0600); err != nil {
		t.Fatal(err)
	}
	m = inputKeys(t, m, textKey("unsaved active document"))
	before, snapshot := hBoldNative(t, m), m.Session().Snapshot()
	m.print.port = "DISK.PRN"
	enter := everydayKey(tea.KeyEnter)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF7, Mod: tea.ModShift}, textKey("3"))
	if !strings.Contains(m.View().Content, "Document name:") {
		t.Fatal("Print Document on Disk did not ask for a filename")
	}
	m = inputKeys(t, m, textKey("Z.WP"), enter)
	if !strings.Contains(m.View().Content, "Page(s): (All)") {
		t.Fatal("Print Document on Disk did not ask for page selection")
	}
	m = inputKeys(t, m, enter)
	got, err := os.ReadFile(filepath.Join(root, "DISK.PRN"))
	if want := referenceFile(t, "mission1-list-dos-text/LIST.PRN"); err != nil || !bytes.Equal(got, want) {
		t.Fatalf("Print Document on Disk produced %d bytes, want %d: %v", len(got), len(want), err)
	}
	if m.print.screen != printMenu || !bytes.Equal(hBoldNative(t, m), before) || !reflect.DeepEqual(m.Session().Snapshot(), snapshot) {
		t.Fatal("Print Document on Disk altered the active document or failed to return to Print")
	}
}

func TestListPrintRomanSectionsAndSummary(t *testing.T) {
	const fixtures = "issue7-roman-native-r2/exports/"
	for _, tc := range []struct{ spec, file, output string }{
		{"ii", "PAGES.WP", "single.PRN"},
		{"2:1", "PAGES.WP", "section.PRN"},
		{"1:ii-2:1", "PAGES.WP", "range.PRN"},
		{"s", "RICH.WP", "SUMMARY.PRN"},
		{"s,1", "RICH.WP", "SUMPLUS.PRN"},
		{"s-", "RICH.WP", "SUMALL.PRN"},
	} {
		t.Run(tc.spec, func(t *testing.T) {
			m, root := everydayUI(t)
			if err := os.Mkdir(filepath.Join(root, "OUT"), 0700); err != nil {
				t.Fatal(err)
			}
			source := fixtures + tc.file
			if tc.file == "RICH.WP" {
				source = "mission1-summary-rich/exports/RICH.WP"
			}
			path := filepath.Join(root, "OUT", tc.file)
			if err := os.WriteFile(path, referenceFile(t, source), 0600); err != nil {
				t.Fatal(err)
			}
			date := time.Date(2026, 11, 13, 15, 29, 0, 0, time.Local)
			if err := os.Chtimes(path, date, date); err != nil {
				t.Fatal(err)
			}
			m.print.port = "TEST.PRN"
			enter := everydayKey(tea.KeyEnter)
			m = inputKeys(t, m, everydayKey(tea.KeyF5), textKey(`C:\OUT\*.*`), enter, textKey("n"), textKey(tc.file), enter, textKey("4"), textKey(tc.spec), enter)
			got, err := os.ReadFile(filepath.Join(root, "TEST.PRN"))
			want := referenceFile(t, fixtures+tc.output)
			if err != nil {
				t.Fatalf("%v (%s)", err, m.print.notice)
			}
			if !bytes.Equal(got, want) {
				for i := 0; i < min(len(got), len(want)); i++ {
					if got[i] != want[i] {
						t.Fatalf("first difference at %d: got %q, want %q", i, got[i:min(i+40, len(got))], want[i:min(i+40, len(want))])
					}
				}
				t.Fatalf("got %d bytes, want %d", len(got), len(want))
			}
		})
	}
}

func TestPrintOnDiskCombinedSummaryMatchesDOS(t *testing.T) {
	for _, tc := range []struct{ spec, file, output string }{
		{"s,1", "RICH.WP", "SUM1.PRN"},
		{"s-", "RICH.WP", "SUMALL.PRN"},
		{"s,2", "MULTI.WP", "PAGE2.PRN"},
		{"s-", "MULTI.WP", "MULTIALL.PRN"},
	} {
		t.Run(tc.spec+"/"+tc.file, func(t *testing.T) {
			m, root := everydayUI(t)
			dir := filepath.Join(root, "OUT")
			if err := os.Mkdir(dir, 0700); err != nil {
				t.Fatal(err)
			}
			const evidence = "disk-print-combined-summary/"
			source := "mission1-summary-rich/exports/RICH.WP"
			if tc.file != "RICH.WP" {
				source = evidence + tc.file
			}
			if err := os.WriteFile(filepath.Join(dir, tc.file), referenceFile(t, source), 0600); err != nil {
				t.Fatal(err)
			}
			m = inputKeys(t, m, textKey("Unsaved active document"))
			before := m.Session().Snapshot()
			m.print.port = "DISK.PRN"
			enter := everydayKey(tea.KeyEnter)
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF7, Mod: tea.ModShift}, textKey("3"), textKey(`C:\OUT\`+tc.file), enter)
			if m.print.screen != printDiskPages {
				t.Fatalf("did not reach disk page prompt: %s", m.print.notice)
			}
			m = inputKeys(t, m, textKey(tc.spec), enter)
			got, err := os.ReadFile(filepath.Join(root, "DISK.PRN"))
			want := referenceFile(t, evidence+tc.output)
			if err != nil || !bytes.Equal(got, want) {
				t.Fatalf("printer output: got %d bytes, want %d: %v (%s)", len(got), len(want), err, m.print.notice)
			}
			if m.print.screen != printMenu || !reflect.DeepEqual(m.Session().Snapshot(), before) {
				t.Fatal("disk print did not return to Print with the active document intact")
			}
		})
	}
}

func TestBlockSearchAndAutomaticPageDeletionMatchDOS(t *testing.T) {
	key := everydayKey
	enter := key(tea.KeyEnter)
	top := []tea.Key{key(tea.KeyHome), key(tea.KeyHome), key(tea.KeyUp)}
	t.Run("block search", func(t *testing.T) {
		m, _ := everydayUI(t)
		m = inputKeys(t, m, textKey("alpha beta gamma"))
		m = inputKeys(t, m, top...)
		m = inputKeys(t, m, tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt}, key(tea.KeyF2), textKey("beta"), key(tea.KeyF2))
		if s := m.Session().Snapshot(); !s.Selection || s.SelectionEnd != 10 {
			t.Fatalf("expected Block through beta: %+v", s)
		}
		m = inputKeys(t, m, key(tea.KeyF6))
		if got := hBoldBody(t, m); got != "\xc3\x0c\xc3alpha beta\xc4\x0c\xc4 gamma" {
			t.Fatalf("DOS Block Search + Bold body mismatch: %q", got)
		}
	})
	t.Run("automatic page", func(t *testing.T) {
		m, root := everydayUI(t)
		const fixture = "issue7-auto-page-delete/exports/"
		raw := referenceFile(t, fixture+"BEFORE.WP")
		if err := os.WriteFile(filepath.Join(root, "BEFORE.WP"), raw, 0600); err != nil {
			t.Fatal(err)
		}
		m = inputKeys(t, m, tea.Key{Code: tea.KeyF10, Mod: tea.ModShift}, textKey("BEFORE.WP"), enter)
		m = inputKeys(t, m, top...)
		deletePage := tea.Key{Code: tea.KeyPgDown, Mod: tea.ModCtrl}
		m = inputKeys(t, m, key(tea.KeyRight), key(tea.KeyRight), deletePage)
		if s := m.Session().Snapshot(); s.Prompt != "Delete Remainder of page? No (Yes)" {
			t.Fatalf("missing confirmation: %+v (%s)", s, m.notice)
		}
		m = inputKeys(t, m, textKey("y"))
		want := referenceFile(t, fixture+"AFTER.WP")
		if got := hBoldBody(t, m); got != string(want[324:]) {
			t.Fatalf("delete got %q (%s)", got, m.notice)
		}
		m = inputKeys(t, m, key(tea.KeyF1), textKey("1"))
		if got := hBoldBody(t, m); !strings.HasPrefix(got, "keep \n"+strings.Repeat("a\n", 52)+"a") || !strings.HasSuffix(got, "next page") {
			t.Fatalf("Undo got %q (%s)", got, m.notice)
		}
	})
}

func TestDeleteFormattedLineEndAndUndeleteMatchDOS(t *testing.T) {
	m, _ := everydayUI(t)
	key := everydayKey
	m = inputKeys(t, m, textKey("keep "), key(tea.KeyF6), textKey("bold word"), key(tea.KeyF6),
		textKey(" tail"), key(tea.KeyEnter), textKey("next"), key(tea.KeyHome), key(tea.KeyHome), key(tea.KeyUp))
	for range 5 {
		m = inputKeys(t, m, key(tea.KeyRight))
	}
	const fixture = "issue7-format-delete/exports/"
	m = inputKeys(t, m, tea.Key{Code: tea.KeyEnd, Mod: tea.ModCtrl})
	if got, want := hBoldBody(t, m), referenceFile(t, fixture+"DELETED.WP"); got != string(want[324:]) {
		t.Fatalf("deleted body = %q (%s)", got, m.notice)
	}
	m = inputKeys(t, m, key(tea.KeyF1), textKey("1"))
	if got, want := hBoldBody(t, m), referenceFile(t, fixture+"RESTORE.WP"); got != string(want[324:]) {
		t.Fatalf("restored body = %q (%s)", got, m.notice)
	}
}

func TestProtectBlockMovesAcrossPageLikeDOS(t *testing.T) {
	m, _ := everydayUI(t)
	key := everydayKey
	for range 52 {
		m = inputKeys(t, m, textKey("a"), key(tea.KeyEnter))
	}
	m = inputKeys(t, m, textKey("first"), key(tea.KeyEnter), textKey("second"), key(tea.KeyEnter), textKey("third"),
		key(tea.KeyUp), key(tea.KeyUp), tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt},
		key(tea.KeyDown), key(tea.KeyDown), key(tea.KeyEnd), tea.Key{Code: tea.KeyF8, Mod: tea.ModShift})
	if s := m.Session().Snapshot(); s.Prompt != "Protect block? No (Yes)" {
		t.Fatalf("protection prompt = %q (%s)", s.Prompt, m.notice)
	}
	m = inputKeys(t, m, textKey("y"))
	want := referenceFile(t, "issue7-protection-boundary/exports/KEPT.WP")
	got := hBoldBody(t, m)
	if got != string(want[324:]) {
		t.Fatalf("protected native body = %q (%s)", got, m.notice)
	}
}

func TestDeleteWrappedLineWithinBoldMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	key := everydayKey
	m = inputKeys(t, m, key(tea.KeyF6), textKey(strings.Repeat("word ", 16)+"last tail"), key(tea.KeyF6),
		key(tea.KeyHome), key(tea.KeyHome), key(tea.KeyUp), key(tea.KeyRight), key(tea.KeyRight),
		tea.Key{Code: tea.KeyEnd, Mod: tea.ModCtrl})
	for _, file := range []string{"DEL.WP", "REST.WP"} {
		want := referenceFile(t, "issue7-wrap-delete/exports/"+file)
		if got := hBoldBody(t, m); got != string(want[324:]) {
			t.Fatalf("%s: got %q, want %q (%s)", file, got, want[324:], m.notice)
		}
		if file == "DEL.WP" {
			m = inputKeys(t, m, key(tea.KeyF1), textKey("1"))
		}
	}
}

func TestHomeArrowsUseVisibleColumns(t *testing.T) {
	m, _ := everydayUI(t)
	key := everydayKey
	m = inputKeys(t, m, textKey(strings.Repeat("a", 60)), key(tea.KeyHome), key(tea.KeyHome), key(tea.KeyUp))
	next, _ := m.Update(tea.WindowSizeMsg{Width: 40, Height: 25})
	m = next.(Model)
	m = inputKeys(t, m, key(tea.KeyHome), key(tea.KeyRight))
	if got := m.Session().Snapshot().Gap; got != 39 {
		t.Fatalf("right edge gap = %d", got)
	}
	m = inputKeys(t, m, key(tea.KeyEnd), key(tea.KeyHome), key(tea.KeyLeft))
	if got := m.Session().Snapshot().Gap; got != 30 {
		t.Fatalf("left edge gap = %d", got)
	}
	m = inputKeys(t, m, key(tea.KeyHome), key(tea.KeyHome), key(tea.KeyLeft))
	if got := m.Session().Snapshot().Gap; got != 0 {
		t.Fatalf("line start gap = %d", got)
	}
}

func TestSplitAttributeLineUndeleteMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	k := everydayKey
	m = inputKeys(t, m, k(tea.KeyF6), textKey("front "), k(tea.KeyF8), textKey("overlap"), k(tea.KeyF6),
		textKey(" tail"), k(tea.KeyF8), k(tea.KeyEnter), textKey("next"), k(tea.KeyHome), k(tea.KeyHome), k(tea.KeyUp),
		k(tea.KeyRight), k(tea.KeyRight), k(tea.KeyRight), tea.Key{Code: tea.KeyEnd, Mod: tea.ModCtrl})
	for i, name := range []string{"SPLIT.WP", "UNDO.WP"} {
		if i == 1 {
			m = inputKeys(t, m, k(tea.KeyF1), textKey("1"))
		}
		want := referenceFile(t, "issue7-split-attributes/exports/"+name)
		if got := hBoldBody(t, m); got != string(want[324:]) {
			t.Fatalf("%s got %q, want %q (%s)", name, got, want[324:], m.notice)
		}
	}
}

func TestMidParagraphAndOversizedProtectionMatchDOS(t *testing.T) {
	for _, large := range []bool{false, true} {
		name := "mid"
		if large {
			name = "large"
		}
		t.Run(name, func(t *testing.T) {
			m, _ := everydayUI(t)
			k := everydayKey
			if large {
				for range 56 {
					m = inputKeys(t, m, textKey("a"), k(tea.KeyEnter))
				}
				m = inputKeys(t, m, textKey("end"))
			} else {
				m = inputKeys(t, m, textKey("prefix protected suffix"))
			}
			m = inputKeys(t, m, k(tea.KeyHome), k(tea.KeyHome), k(tea.KeyUp))
			if !large {
				for range 7 {
					m = inputKeys(t, m, k(tea.KeyRight))
				}
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF4, Mod: tea.ModAlt})
			if large {
				m = inputKeys(t, m, k(tea.KeyHome), k(tea.KeyHome), k(tea.KeyDown))
			} else {
				for range 9 {
					m = inputKeys(t, m, k(tea.KeyRight))
				}
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}, textKey("y"))
			want := referenceFile(t, "issue7-protect-"+name+"/exports/"+strings.ToUpper(name)+".WP")
			if got := hBoldBody(t, m); got != string(want[324:]) {
				t.Fatalf("got %q, want %q (%s)", got, want[324:], m.notice)
			}
		})
	}
}

func TestWordDeletionFormattingEdgesMatchDOS(t *testing.T) {
	k := everydayKey
	home := k(tea.KeyHome)
	for _, tc := range []struct {
		name  string
		right int
		keys  []tea.Key
	}{
		{"current", 7, []tea.Key{{Code: tea.KeyBackspace, Mod: tea.ModCtrl}}},
		{"alternate", 7, []tea.Key{{Code: tea.KeyDelete, Mod: tea.ModCtrl}}},
		{"backward", 7, []tea.Key{home, k(tea.KeyBackspace)}},
		{"forward", 7, []tea.Key{home, k(tea.KeyDelete)}},
		{"left-edge", 5, []tea.Key{home, k(tea.KeyBackspace)}},
		{"right-edge", 9, []tea.Key{home, k(tea.KeyDelete)}},
		{"single-forward", 7, []tea.Key{home, k(tea.KeyDelete)}},
		{"single-backward", 7, []tea.Key{home, k(tea.KeyBackspace)}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			m, _ := everydayUI(t)
			if strings.HasPrefix(tc.name, "single-") {
				m = inputKeys(t, m, k(tea.KeyF6), textKey("alphabeta"), k(tea.KeyF6), textKey("gamma tail"))
			} else {
				m = inputKeys(t, m, k(tea.KeyF6), textKey("alpha"), k(tea.KeyF8), textKey("beta"), k(tea.KeyF6), textKey("gamma"), k(tea.KeyF8), textKey(" tail"))
			}
			m = inputKeys(t, m, home, home, k(tea.KeyUp))
			for range tc.right {
				m = inputKeys(t, m, k(tea.KeyRight))
			}
			m = inputKeys(t, m, tc.keys...)
			for i, name := range []string{"DEL.WP", "UNDO.WP"} {
				if i == 1 {
					m = inputKeys(t, m, k(tea.KeyF1), textKey("1"))
				}
				want := referenceFile(t, "issue7-word-edge-"+tc.name+"/exports/"+name)
				if got := hBoldBody(t, m); got != string(want[324:]) {
					t.Fatalf("%s got %q, want %q (%s)", name, got, want[324:], m.notice)
				}
			}
		})
	}
}
