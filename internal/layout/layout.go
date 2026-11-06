package layout

import (
	"github.com/lynncoleart/wordling/internal/document"
)

// Document is the minimum native-token provider the layout engine needs.  The
// production consumer passes *document.Document; tests may pass a bounded stub.
type Document interface {
	TokenCount() int
	Token(index int) (document.Token, error)
}

type Token = document.Token

// Settings are the exact original pinned profile for the everyday flow. They
// are not general-purpose options. The layout owns only physical geometry and
// never serializes a renderer's display text back into native bytes.
type Settings struct {
	PageWidthInches, PageHeightInches   float64
	MarginLeftInches, MarginRightInches float64
	MarginTopInches, MarginBottomInches float64
	CPI                                 float64
	LineSpacing                         float64
	HyphenationNo                       bool
	FullJustification                   bool
	RelativeTabSet                      bool
}

// Layout is an immutable projected result. It is deliberately a pure data
// model, not a terminal view and not a source of native serialization.
type Layout struct {
	Settings Settings
	Lines    []Line
}

// Line is one projected physical line. It keeps the exact token identity so a
// renderer can map code and glyph positions without changing native data.
type Line struct {
	Page         int
	TopInches    float64
	BottomInches float64
	LeftInches   float64
	RightInches  float64
	WidthInches  float64
	Tokens       []TokenPosition
}

// TokenPosition maps one native token into its physical line and position.
type TokenPosition struct {
	Token       Token
	LeftInches  float64
	WidthInches float64
	Text        string
}

// FromDocument projects one native document. It is the production entry point.
func FromDocument(d Document, s Settings) (Layout, error) {
	tokens, err := TokensFromDocument(d)
	if err != nil {
		return Layout{}, err
	}
	return Project(tokens, s), nil
}

// TokensFromDocument copies the native tokens into a bounded slice. It does not
// decode payloads and never changes the source image.
func TokensFromDocument(d Document) ([]Token, error) {
	if d == nil {
		return nil, errNoDocument
	}
	count := d.TokenCount()
	tokens := make([]Token, 0, count)
	for i := 0; i < count; i++ {
		tok, err := d.Token(i)
		if err != nil {
			return nil, err
		}
		tokens = append(tokens, tok)
	}
	return tokens, nil
}

// Project builds a pure physical layout from native tokens.
func Project(tokens []Token, s Settings) Layout {
	width, left := printable(s)
	page := 1
	line := 0
	current := 0.0
	var lines []Line
	for _, tok := range tokens {
		widthInches, text := widthFor(tok, s)
		if text == "" && widthInches == 0 {
			// Attributes and page-structure owners are physical zero-width
			// positions, not extra glyph cells.
			// The layout engine does not interpret their payload.
			if pageBreakFor(tok) {
				lines = append(lines, Line{Page: page, TopInches: current, WidthInches: width, Tokens: []TokenPosition{}})
				page++
				line = 0
				current = 0.0
				continue
			}
			if breakFor(tok) {
				line++ // keep zero-width code on the paragraph boundary before a new line.
				current = 0.0
				continue
			}
		}
		if current+widthInches > width {
			line++
			current = 0.0
		}
		leftInches := left + current
		current += widthInches
		lines = append(lines, Line{Page: page, TopInches: current, LeftInches: leftInches, WidthInches: width, Tokens: []TokenPosition{{Token: tok, LeftInches: leftInches, WidthInches: widthInches, Text: text}}})
	}
	return Layout{Settings: s, Lines: lines}
}

type layoutError string

func (e layoutError) Error() string { return "layout: " + string(e) }

var (
	errNoDocument = layoutError("no document")
)

func printable(s Settings) (float64, float64) {
	return s.PageWidthInches - s.MarginLeftInches - s.MarginRightInches, s.MarginLeftInches
}

func widthFor(tok Token, s Settings) (float64, string) {
	switch tok.Kind {
	case document.ASCII:
		return 1.0 / s.CPI, string(tok.Raw)
	case document.Tab:
		return 1.0 / s.CPI, "\t"
	default:
		return 0.0, ""
	}
}

func breakFor(tok Token) bool {
	switch tok.Kind {
	case document.HardReturn, document.SoftReturn, document.DeletedSoftReturn:
		return true
	default:
		return false
	}
}

func pageBreakFor(tok Token) bool {
	switch tok.Kind {
	case document.HardPage, document.EndOfPage, document.HardReturnSoftPage, document.DormantHardReturn:
		return true
	default:
		return false
	}
}
