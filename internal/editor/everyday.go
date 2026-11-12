package editor

import (
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

// EverydaySettings pins the D-EE-06 Standard Printer text profile that governs
// the everyday milestone: US Letter 8.5x11, one-inch margins, 10 CPI, single
// line spacing, Hyphenation No, Full justification default, relative half-inch
// tabs. It is the approved profile, not a general-purpose option set; other
// printers, fonts and language resources remain open obligations (D-EE-06).
func EverydaySettings() layout.Settings {
	return layout.Settings{
		PageWidthInches: 8.5, PageHeightInches: 11,
		MarginLeftInches: 1, MarginRightInches: 1,
		MarginTopInches: 1, MarginBottomInches: 1,
		CPI: 10, LineSpacing: 1,
		HyphenationNo:     true,
		FullJustification: true,
		RelativeTabSet:    true,
	}
}

// Printed geometry units for the pinned everyday profile, corroborated against
// the original EE-A05 qualification frames (WP82 evidence REPORT.md):
// six physical lines per rendered inch (Ln advances 1.00 → 1.17 → 1.33 for
// consecutive lines) and ten characters per horizontal inch ( sixty-three
// characters report Pos 7.3").
const (
	everydayLinesPerInch = 6.0
	everydayCharsPerInch = 10.0
	everydayMarginInches = 1.0
	// Physical line capacity implied by the printable width at the pinned
	// profile: 6.5" × 10 CPI = 65 character cells. The original's own frames
	// show a 75-character unbroken run rendered as 65 + 10 cells.
	everydayLineChars = 65
)

// Position is the printed everyday geometry for one native cursor gap.
// Page/Line/Pos are 1-based; a zero component means "not qualified" for that
// reading (unknown values must never be synthesized). Page is qualified
// whenever page-structure tokens are explicit; Line and Pos are additionally
// qualified whenever every physical line from document start to the cursor is
// explicit-boundary or deterministic (no Tab stops (GAP-1b) and no token with
// unknown layout effect). Printed inches are derived only from qualified
// components.
type Position struct {
	Page int
	Line int
	Pos  int
}

// Qualified reports which components carry engine-provided values.
func (p Position) Qualified() (page, line, pos bool) {
	return p.Page > 0, p.Line > 0, p.Pos > 0
}

// Printed converts qualified components into the original's printed units:
// Ln and Pos in inches at the pinned profile (Ln 1.17" = margin + (line-1)/6;
// Pos 7.3" = margin + (chars-1)/10). Unqualified components come back as
// zero. The rounding matches the original status line (two decimals).
func (p Position) Printed() (ln, pos float64) {
	if _, line, posOK := p.Qualified(); line && posOK {
		ln = everydayMarginInches + float64(p.Line-1)/everydayLinesPerInch
		pos = everydayMarginInches + float64(p.Pos-1)/everydayCharsPerInch
	}
	return ln, pos
}

// physicalState accumulates the qualified printed geometry while walking
// native tokens in order. Page knowledge survives a Tab (page structure stays
// explicit); Line/Pos knowledge does not (GAP-1b), and neither survives
// structure types with unknown layout effects.
type physicalState struct {
	page, line, col int
	pageKnown       bool
	flowKnown       bool
}

func (s *physicalState) add(tok document.Token) {
	switch tok.Kind {
	case document.ASCII:
		if !s.flowKnown {
			return
		}
		s.col += len(tok.Raw)
		for s.col > everydayLineChars {
			s.line++
			s.col -= everydayLineChars
		}
	case document.SoftReturn, document.HardReturn:
		if !s.flowKnown {
			return
		}
		s.line++
		s.col = 1
	case document.HardPage:
		// An explicit [HPg] token: the cursor resumes at the next page top.
		if s.pageKnown {
			s.page++
		}
		if s.flowKnown {
			s.line = 1
			s.col = 1
		}
	case document.EndOfPage, document.DormantHardReturn:
		// Zero-width companions of the composite page break (WP80 T244d):
		// the original emits HRtSP + 8C + 99 together; the HRtSP record
		// already carried the line and page increments. FLOW.WP evidence:
		// two such triples across the document, original prints Pg 3.
	case document.DeletedSoftReturn:
		// A deleted soft return joins the lines around it: zero width, not a
		// boundary (WP78 unbroken-word evidence).
	case document.HardReturnSoftPage:
		if s.pageKnown {
			s.page++
		}
		if s.flowKnown {
			s.line++
			s.col = 1
		}
	case document.BoldOn, document.BoldOff, document.UnderlineOn, document.UnderlineOff:
		// Attribute owners are zero-width physical positions.
	case document.Tab:
		// Tab stop decode is GAP-1b (WP81-owned payload mapping); the original
		// reports a tabbed line at Pos 3.0" that we cannot qualify yet. Page
		// structure beyond the tab remains explicit.
		s.flowKnown = false
	default:
		// Opaque and dormant tokens have unknown layout effects; no reading
		// past them can claim page or line qualification.
		s.pageKnown = false
		s.flowKnown = false
	}
}

// CursorPositionOf maps a native cursor gap to printed geometry under the
// approved everyday profile. The gap is a native token gap [0..TokenCount];
// the cursor sits before element `gap`, and an end-of-document gap takes the
// last element's reading. The walk never mutates the document and never
// invents values: components it cannot qualify are reported as zero.
func CursorPositionOf(native *document.Document, gap int) (Position, error) {
	if native == nil {
		return Position{}, refuse("position requires a loaded document")
	}
	total := native.TokenCount()
	if gap < 0 || gap > total {
		return Position{}, refuse("position gap outside document bounds")
	}
	st := physicalState{page: 1, line: 1, col: 1, pageKnown: true, flowKnown: true}
	for i := 0; i < gap; i++ {
		tok, err := native.Token(i)
		if err != nil {
			return Position{}, err
		}
		st.add(tok)
	}
	p := Position{}
	if st.pageKnown {
		p.Page = st.page
	}
	if st.flowKnown {
		p.Line = st.line
		p.Pos = st.col
	}
	return p, nil
}

// EverydayPosition maps the session's authoritative cursor through the
// approved everyday profile. It is the TUI-facing surface: WP84's port prints
// exactly what this returns, including the unqualified zeroes, and never
// synthesizes printed geometry on its own.
func (s Session) EverydayPosition() (Position, error) {
	if s.native == nil {
		return Position{}, refuse("position requires a loaded document")
	}
	if s.workspace == nil {
		return CursorPositionOf(s.native, s.cursor.Gap())
	}
	physical, err := layout.FromDocument(s.native, EverydaySettings())
	if err != nil {
		return Position{}, err
	}
	line, column, known := physical.PositionAt(s.cursor.Gap())
	if !known {
		return Position{}, nil
	}
	row := physical.Lines[line]
	return Position{Page: row.Page, Line: row.Row + 1, Pos: column + 1}, nil
}
