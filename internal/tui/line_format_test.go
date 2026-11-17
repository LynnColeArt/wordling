package tui

import (
	"bytes"
	"encoding/binary"
	"os"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/layout"
)

func TestStandardPrinterMatchesDOSLayout(t *testing.T) {
	const references = "../../docs/research/reference-runs/"
	for _, fixture := range []string{
		"mission1-line-format/LINEFMT", "mission1-line-format/CENTEND",
		"mission1-line-margins/MARGINS", "mission1-line-margins/INLINE",
		"mission1-page-margins/PAGEMAR", "mission1-page-margins/AUTO",
		"mission1-line-spacing/SPACING", "mission1-line-spacing/SPACEAUT",
		"mission1-line-spacing/HEIGHT", "mission1-line-spacing/HEIGHTPG",
		"mission1-initial-codes/DOUBLE", "mission1-initial-codes/RESET", "mission1-initial-codes/PAGES",
		"mission1-justification/JUSTIFY", "mission1-justification/CENTER",
		"mission1-notes/NOTES", "mission1-headers/HEADFOOT", "mission1-headers/MASKS",
		"mission1-line-numbering/LINENUM", "mission1-binding/BIND",
		"mission1-conditional-page/SHORT",
		"mission1-custom-tabs/RELATIVE", "mission1-custom-tabs/ABSOLUTE", "mission1-custom-tabs/DECIMAL",
		"mission1-note-continuation/SPLIT", "mission1-note-continuation/KEEP",
		"mission1-comment/COMMENT",
		"mission1-toc-mark/LEVEL1",
		"mission1-toc-generation/GEN", "mission1-style-authoring/BOLD", "mission1-subdocuments/MASTER",
		"mission1-cross-references/AFTER",
		"mission1-table-math/RECALC",
		"mission1-table-join/ROWJOIN",
		"mission1-outline/OUTLINE",
		"mission1-column-math/TOTAL",
		"mission1-printer-command/PRTCMD",
		"mission1-kerning/KERN", "mission1-appearance/ITALICS",
		"mission1-page-number-position/BOTTOM", "mission1-page-number-position/TOP", "mission1-page-number-position/TITLE",
		"mission1-spreadsheet/IMPORT",
		"mission1-spreadsheet/OFFSET",
		"mission1-spreadsheet/LINK",
		"mission1-document-compare/COMPARE",
	} {
		t.Run(fixture, func(t *testing.T) {
			source, err := os.ReadFile(references + fixture + ".WP")
			if err != nil {
				t.Fatal(err)
			}
			doc, err := document.Parse(source)
			if err != nil {
				t.Fatal(err)
			}
			pages, err := layout.StandardPages(doc, editor.EverydaySettings())
			if err != nil {
				t.Fatal(err)
			}
			want, err := os.ReadFile(references + fixture + ".PRN")
			if err != nil {
				t.Fatal(err)
			}
			got := layout.StandardPrint(pages)
			if !bytes.Equal(got, want) {
				t.Fatalf("print stream differs from DOS: got %q, want %q", got, want)
			}
		})
	}
}

func checkLineFormatTextExport(t *testing.T, m Model, path string) {
	t.Helper()
	want, err := os.ReadFile("../../docs/research/reference-runs/" + path)
	if err != nil {
		t.Fatal(err)
	}
	got, err := m.Session().Document().ExportDOSText()
	if err != nil || !bytes.Equal(got, want) {
		t.Fatalf("DOS text = %q, %v; want %q", got, err, want)
	}
}

func lineFormatBody(t *testing.T, fixture string) string {
	t.Helper()
	raw, err := os.ReadFile("../../docs/research/reference-runs/" + fixture)
	if err != nil {
		t.Fatal(err)
	}
	return string(raw[binary.LittleEndian.Uint32(raw[4:8]):])
}

func TestLineMarginsMatchesDOS(t *testing.T) {
	for _, tc := range []struct {
		before, after, fixture string
	}{
		{"before", "after ", "MARGINS.WP"},
		{"before inline", " after ", "INLINE.WP"},
	} {
		t.Run(tc.fixture, func(t *testing.T) {
			m, _ := everydayUI(t)
			enter := everydayKey(tea.KeyEnter)
			m = inputKeys(t, m, textKey(tc.before))
			if tc.fixture == "MARGINS.WP" {
				m = inputKeys(t, m, enter)
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}, textKey("1"), textKey("7"),
				textKey("2\""), enter, textKey("1.5\""), enter, everydayKey(tea.KeyF7))
			m = inputKeys(t, m, textKey(tc.after+strings.Repeat("word ", 14)), tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-margins/"+tc.fixture); got != want {
				t.Fatalf("native body\ngot  %x\nwant %x\n%s", got, want, m.notice)
			}
			screen := ansi.Strip(m.View().Content)
			if !strings.Contains(screen, "[L/R Mar:2\",1.5\"]") || !strings.Contains(screen, "\n          "+tc.after) {
				t.Fatal(screen)
			}
			checkLineFormatTextExport(t, m, "mission1-line-margins/"+strings.TrimSuffix(tc.fixture, ".WP")+".TXT")
		})
	}
}

func TestLineAlignmentMatchesDOS(t *testing.T) {
	enter := everydayKey(tea.KeyEnter)
	center := tea.Key{Code: tea.KeyF6, Mod: tea.ModShift}
	right := tea.Key{Code: tea.KeyF6, Mod: tea.ModAlt}
	m, _ := everydayUI(t)
	m = inputKeys(t, m, center, textKey("Heading"))
	screen := ansi.Strip(m.View().Content)
	if !strings.Contains(screen, "\n"+strings.Repeat(" ", 29)+"Heading") || !strings.Contains(screen, "Pos 4.6\"") {
		t.Fatal(screen)
	}
	m = inputKeys(t, m, enter, textKey("Body"), enter, right, textKey("RIGHT"), enter, textKey("Second"), enter)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-format/LINEFMT.WP"); !strings.HasPrefix(want, got) || !strings.HasSuffix(got, "Second\n") {
		t.Fatalf("native body\ngot  %x\nwant prefix of %x\n%s", got, want, m.notice)
	}
	screen = ansi.Strip(m.View().Content)
	if !strings.Contains(screen, "\n"+strings.Repeat(" ", 60)+"RIGHT") || !strings.Contains(screen, "\nSecond") {
		t.Fatal(screen)
	}

	m, _ = everydayUI(t)
	m = inputKeys(t, m, textKey("before "), center, textKey("Heading"),
		tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}, textKey("4"), textKey("9"), textKey(" tail"),
		tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-format/CENTEND.WP"); got != want {
		t.Fatalf("native body\ngot  %x\nwant %x\n%s", got, want, m.notice)
	}
	screen = ansi.Strip(m.View().Content)
	if !strings.Contains(screen, "before "+strings.Repeat(" ", 22)+"Heading tail") ||
		!strings.Contains(screen, "before [Center]Heading[End C/A] tail") {
		t.Fatal(screen)
	}
	checkLineFormatTextExport(t, m, "mission1-line-format/CENTEND.TXT")
}

func TestPageMarginsMatchesDOS(t *testing.T) {
	for _, automatic := range []bool{false, true} {
		name := "PAGEMAR.WP"
		if automatic {
			name = "AUTO.WP"
		}
		t.Run(name, func(t *testing.T) {
			m, _ := everydayUI(t)
			enter := everydayKey(tea.KeyEnter)
			if !automatic {
				m = inputKeys(t, m, textKey("first page"), tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl})
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}, textKey("2"), textKey("5"),
				textKey("2\""), enter, textKey("1.25\""), enter, everydayKey(tea.KeyF7))
			if automatic {
				for range 49 {
					m = inputKeys(t, m, textKey("a"), enter)
				}
				m = inputKeys(t, m, textKey("second"))
			} else {
				m = inputKeys(t, m, textKey("second page"), enter, textKey("next line"), tea.Key{Code: tea.KeyF3, Mod: tea.ModAlt})
				screen := ansi.Strip(m.View().Content)
				if !strings.Contains(screen, "[T/B Mar:2\",1.25\"]") || !strings.Contains(screen, "Pg 2 Ln 2.17\"") {
					t.Fatal(screen)
				}
			}
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-page-margins/"+name); got != want {
				t.Fatalf("native body\ngot  %x\nwant %x\n%s", got, want, m.notice)
			}
		})
	}
}

func TestLineSpacingMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	enter := everydayKey(tea.KeyEnter)
	f7 := everydayKey(tea.KeyF7)
	format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
	m = inputKeys(t, m, textKey("before"), enter, format, textKey("1"), textKey("6"),
		textKey("2"), enter, f7, textKey("second"), enter, textKey("third"))
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Ln 1.5\"") {
		t.Fatal(screen)
	}
	m = inputKeys(t, m, enter, format, textKey("1"), textKey("6"), textKey("1"), enter, f7,
		textKey("fourth"), enter, textKey("fifth"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-spacing/SPACING.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
	m, _ = everydayUI(t)
	m = inputKeys(t, m, format, textKey("1"), textKey("6"), textKey("2"), enter, f7)
	for range 29 {
		m = inputKeys(t, m, textKey("a"), enter)
	}
	m = inputKeys(t, m, textKey("second page"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-spacing/SPACEAUT.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
}

func TestFixedLineHeightMatchesDOS(t *testing.T) {
	for _, name := range []string{"HEIGHT.WP", "HEIGHTPG.WP"} {
		t.Run(name, func(t *testing.T) {
			m, _ := everydayUI(t)
			enter := everydayKey(tea.KeyEnter)
			if name == "HEIGHT.WP" {
				m = inputKeys(t, m, textKey("before"), enter)
			}
			m = inputKeys(t, m, tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}, textKey("1"), textKey("4"),
				textKey("2"), textKey("0.2\""), enter, everydayKey(tea.KeyF7))
			if name == "HEIGHT.WP" {
				m = inputKeys(t, m, textKey("higher"), enter, textKey("next line"))
				if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Ln 1.37\"") {
					t.Fatal(screen)
				}
			} else {
				for range 47 {
					m = inputKeys(t, m, textKey("a"), enter)
				}
				m = inputKeys(t, m, textKey("after"))
			}
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-spacing/"+name); got != want {
				t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
			}
		})
	}
}

func TestFullJustificationMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	enter, f7 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
	format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
	line := "x " + strings.Repeat("a", 58) + " alpha"
	m = inputKeys(t, m, format, textKey("1"), textKey("3"), textKey("1"), f7,
		textKey(line), everydayKey(tea.KeyHome), textKey(" "), textKey("beta"), enter)
	m = inputKeys(t, m, format, textKey("1"), textKey("3"), textKey("4"), f7,
		textKey(line), everydayKey(tea.KeyHome), textKey(" "), textKey("beta"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-justification/JUSTIFY.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
	m = inputKeys(t, m, enter, format, textKey("1"), textKey("3"), textKey("2"), f7, textKey("Centered"),
		enter, format, textKey("1"), textKey("3"), textKey("3"), f7, textKey("Right"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-justification/CENTER.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
}

func TestDoubleAndHangingIndentMatchDOS(t *testing.T) {
	m, _ := everydayUI(t)
	m = inputKeys(t, m, tea.Key{Code: tea.KeyF4, Mod: tea.ModShift},
		textKey("double "+strings.Repeat("word ", 15)), everydayKey(tea.KeyEnter), everydayKey(tea.KeyF4),
		tea.Key{Code: tea.KeyTab, Mod: tea.ModShift}, textKey("hanging "+strings.Repeat("word ", 15)),
		everydayKey(tea.KeyEnter), textKey("normal"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-indents/INDENTS.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
	screen := ansi.Strip(m.View().Content)
	if !strings.Contains(screen, "\n     double ") || !strings.Contains(screen, "\nhanging ") ||
		!strings.Contains(screen, "\n     word ") || !strings.Contains(screen, "\nnormal") {
		t.Fatal(screen)
	}
}

func TestConditionalPageMatchesDOS(t *testing.T) {
	for _, tc := range []struct {
		fixture string
		rows    []string
		page    string
	}{
		{"ROOM", nil, "Pg 1"},
		{"SHORT", strings.Split("row 1;row 2;row 3;row 4;row 5;row 6;row 7;row 8", ";"), "Pg 2"},
		{"EDGE", []string{"row", "row", "row", "row", "row", "row", "row", "row", "row", "row"}, "Pg 2"},
	} {
		t.Run(tc.fixture, func(t *testing.T) {
			m, _ := everydayUI(t)
			enter, f7 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
			format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
			m = inputKeys(t, m, format, textKey("2"), textKey("5"), textKey("2\""), enter, textKey("7\""), enter, f7)
			for _, row := range tc.rows {
				m = inputKeys(t, m, textKey(row), enter)
			}
			m = inputKeys(t, m, textKey("first"), enter, textKey("second"), format, textKey("4"), textKey("2"))
			if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Number of Lines to Keep Together") {
				t.Fatal(screen)
			}
			m = inputKeys(t, m, textKey("3"), enter, f7, enter, textKey("Heading"), enter,
				textKey("first protected"), enter, textKey("second protected"))
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-conditional-page/"+tc.fixture+".WP"); got != want {
				t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
			}
			if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, tc.page) {
				t.Fatal(screen)
			}
		})
	}
}

func TestWidowProtectionMatchesDOS(t *testing.T) {
	for _, tc := range []struct {
		fixture string
		rows    int
	}{
		{"WIDOW", 10}, {"WIDEOF", 10}, {"ORPHAN", 11}, {"TOGGLE", 0},
	} {
		t.Run(tc.fixture, func(t *testing.T) {
			m, _ := everydayUI(t)
			enter, f7 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
			format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
			m = inputKeys(t, m, format, textKey("2"), textKey("5"), textKey("2\""), enter, textKey("7\""), enter, f7)
			for range tc.rows {
				m = inputKeys(t, m, textKey("row"), enter)
			}
			m = inputKeys(t, m, format, textKey("1"), textKey("9"), textKey("y"), f7)
			if tc.rows == 0 {
				m = inputKeys(t, m, textKey("enabled"), enter, format, textKey("1"), textKey("9"), textKey("n"), f7,
					textKey("disabled"))
			} else {
				m = inputKeys(t, m, textKey("test "+strings.Repeat("word ", 36)))
				if tc.fixture != "WIDEOF" {
					m = inputKeys(t, m, enter, textKey("after"))
				}
			}
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-widow-protection/"+tc.fixture+".WP"); got != want {
				t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
			}
		})
	}
}

func TestCreateNotesMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	note := tea.Key{Code: tea.KeyF7, Mod: tea.ModCtrl}
	f7 := everydayKey(tea.KeyF7)
	m = inputKeys(t, m, textKey("Sentence"), note, textKey("1"), textKey("1"), textKey("Footnote text"), f7,
		textKey(" then"), note, textKey("2"), textKey("1"), textKey("Endnote text"), f7, textKey(" end"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-notes/NOTES.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
	screen := ansi.Strip(m.View().Content)
	if !strings.Contains(screen, "Sentence1 then1 end") || !strings.Contains(screen, "Pos 2.9\"") {
		t.Fatal(screen)
	}
	m, _ = everydayUI(t)
	m = inputKeys(t, m, textKey("One"), note, textKey("1"), textKey("1"), textKey("A"), f7,
		textKey(" Two"), note, textKey("1"), textKey("1"), textKey("Longer two"), f7,
		textKey(" Three"), note, textKey("2"), textKey("1"), textKey("B"), f7,
		textKey(" Four"), note, textKey("2"), textKey("1"), textKey("Longer four"), f7, textKey(" Done"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-notes/NOTES2.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
}

func TestEditNoteByNumberMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	note := tea.Key{Code: tea.KeyF7, Mod: tea.ModCtrl}
	f7 := everydayKey(tea.KeyF7)
	m = inputKeys(t, m, textKey("Sentence"), note, textKey("1"), textKey("1"), textKey("Footnote text"), f7,
		textKey(" end"), note, textKey("1"), textKey("2"), everydayKey(tea.KeyEnter),
		everydayKey(tea.KeyEnd), textKey(" edit"), f7)
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-notes/NOTEEDIT.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
}

func TestHeadersAndFootersMatchDOS(t *testing.T) {
	for _, tc := range []struct {
		name, headerSlot, headerScope, header, footerSlot, footerScope, footer string
		pages                                                                  []string
	}{
		{"HEADFOOT.WP", "1", "2", "My Header", "2", "4", "Even Footer", []string{"First page", "Second page", "Third page"}},
		{"MASKS.WP", "2", "3", "Odd Head", "1", "2", "All Foot", []string{"One", "Two", "Three"}},
		{"FOOTONLY.WP", "", "", "", "2", "4", "Even Footer", []string{"First page", "Second page", "Third page"}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			m, _ := everydayUI(t)
			format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
			f7 := everydayKey(tea.KeyF7)
			if tc.header != "" {
				m = inputKeys(t, m, format, textKey("2"), textKey("3"), textKey(tc.headerSlot), textKey(tc.headerScope), textKey(tc.header), f7, f7)
			}
			m = inputKeys(t, m, format, textKey("2"), textKey("4"), textKey(tc.footerSlot), textKey(tc.footerScope), textKey(tc.footer), f7, f7)
			for i, page := range tc.pages {
				if i > 0 {
					m = inputKeys(t, m, tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl})
				}
				m = inputKeys(t, m, textKey(page))
			}
			if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-headers/"+tc.name); got != want {
				t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
			}
			baseline := "Pg 3 Ln 1.33\""
			if tc.header == "" {
				baseline = "Pg 3 Ln 1\""
			}
			if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, baseline) {
				t.Fatal(screen)
			}
		})
	}
}

func TestDiscontinueHeaderMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
	f7 := everydayKey(tea.KeyF7)
	m = inputKeys(t, m, format, textKey("2"), textKey("3"), textKey("1"), textKey("2"), textKey("My Header"), f7, f7,
		textKey("First page"), tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl},
		format, textKey("2"), textKey("3"), textKey("1"), textKey("1"), f7, textKey("Second page"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-headers/DISCONT.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
	if screen := ansi.Strip(m.View().Content); !strings.Contains(screen, "Pg 2 Ln 1\"") {
		t.Fatal(screen)
	}
}

func TestLineNumberingMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	format := tea.Key{Code: tea.KeyF8, Mod: tea.ModShift}
	enter, f7 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
	m = inputKeys(t, m, textKey("before"), enter, format, textKey("1"), textKey("5"), textKey("y"), f7,
		textKey("First numbered"), enter, textKey("Second numbered"), enter, textKey("Third numbered"), enter,
		format, textKey("1"), textKey("5"), textKey("n"), f7, textKey("After"))
	if got, want := hBoldBody(t, m), lineFormatBody(t, "mission1-line-numbering/LINENUM.WP"); got != want {
		t.Fatalf("got %x\nwant %x\n%s", got, want, m.notice)
	}
}

func TestBindingOffsetMatchesDOS(t *testing.T) {
	m, _ := everydayUI(t)
	printKey := tea.Key{Code: tea.KeyF7, Mod: tea.ModShift}
	enter, f7 := everydayKey(tea.KeyEnter), everydayKey(tea.KeyF7)
	m = inputKeys(t, m, textKey("Odd"), tea.Key{Code: tea.KeyEnter, Mod: tea.ModCtrl}, textKey("Even"))
	for _, tc := range []struct {
		value, file string
		offset      int
	}{
		{"0.25\"", "BIND.WP", 300},
		{"0\"", "ZERO.WP", 0},
	} {
		m = inputKeys(t, m, printKey, textKey("b"), textKey(tc.value), enter, f7)
		got, err := m.Session().Document().Export()
		if err != nil {
			t.Fatal(err)
		}
		want, err := os.ReadFile("../../docs/research/reference-runs/mission1-binding/" + tc.file)
		if err != nil {
			t.Fatal(err)
		}
		if !bytes.Equal(got[262:264], want[262:264]) || m.Session().Document().BindingOffset() != tc.offset ||
			hBoldBody(t, m) != lineFormatBody(t, "mission1-binding/"+tc.file) {
			t.Fatalf("binding %s did not match native document", tc.value)
		}
	}
}
