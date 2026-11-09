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

// Position is the printed everyday geometry for one native cursor gap. A zero
// component means "not qualified": the approved WP81 layout engine does not
// plan physical lines yet (WP82 evidence GAP-1), so Line and Pos are unknown,
// and Page is qualified only for explicit HardPage boundaries — flow
// pagination arrives with the layout amendment. Unknown values must never be
// synthesized from terminal wrapping or token counts; consumers print
// unknowns exactly as the current TUI placeholder does.
type Position struct {
	Page int
	Line int
	Pos  int
}

// Qualified reports which components carry engine-provided values.
func (p Position) Qualified() (page, line, pos bool) {
	return p.Page > 0, p.Line > 0, p.Pos > 0
}

// CursorPositionOf maps a native cursor gap to printed geometry under the
// approved everyday profile. The gap is a native token gap [0..TokenCount];
// the cursor sits before element `gap`, and an end-of-document gap takes the
// last element's page with zero tokens reported as page 1. Page counts only
// explicit HardPage structure tokens, which is the exact qualified subset;
// it never estimates flow pagination (GAP-1) and never mutates the document.
func CursorPositionOf(native *document.Document, gap int) (Position, error) {
	if native == nil {
		return Position{}, refuse("position requires a loaded document")
	}
	total := native.TokenCount()
	if gap < 0 || gap > total {
		return Position{}, refuse("position gap outside document bounds")
	}
	page := 1
	for i := 0; i < gap; i++ {
		tok, err := native.Token(i)
		if err != nil {
			return Position{}, err
		}
		if tok.Kind == document.HardPage {
			page++
		}
	}
	return Position{Page: page}, nil
}

// EverydayPosition maps the session's authoritative cursor through the
// approved everyday profile. It is the TUI-facing surface: WP84's port prints
// exactly what this returns, including the unqualified zeroes, and never
// synthesizes printed geometry on its own.
func (s Session) EverydayPosition() (Position, error) {
	if s.native == nil {
		return Position{}, refuse("position requires a loaded document")
	}
	return CursorPositionOf(s.native, s.cursor.Gap())
}
