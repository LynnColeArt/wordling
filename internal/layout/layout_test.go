package layout_test

import (
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
)

func TestProjectSimpleParagraph(t *testing.T) {
	s := layout.Settings{
		PageWidthInches: 8.5, PageHeightInches: 11,
		MarginLeftInches: 1, MarginRightInches: 1,
		MarginTopInches: 1, MarginBottomInches: 1,
		CPI: 10, LineSpacing: 1, HyphenationNo: true, FullJustification: true, RelativeTabSet: true,
	}
	tokens := make([]document.Token, 0, 80)
	for i := 0; i < 80; i++ {
		tokens = append(tokens, document.Token{Kind: document.ASCII, Raw: []byte("A")})
	}
	out := layout.Project(tokens, s)
	if len(out.Lines) < 2 {
		t.Fatalf("expected wrapped lines, got %d", len(out.Lines))
	}
	if out.Lines[0].Page != 1 || len(out.Lines[0].Tokens) == 0 {
		t.Fatalf("bad first line %v", out.Lines[0])
	}
}

func TestProjectThreePages(t *testing.T) {
	s := layout.Settings{
		PageWidthInches: 8.5, PageHeightInches: 11,
		MarginLeftInches: 1, MarginRightInches: 1,
		MarginTopInches: 1, MarginBottomInches: 1,
		CPI: 10, LineSpacing: 1, HyphenationNo: true,
	}
	// A hard page token should begin a new page, even with no other text.
	tokens := []document.Token{
		{Kind: document.ASCII},
		{Kind: document.HardPage},
		{Kind: document.ASCII},
	}
	out := layout.Project(tokens, s)
	if len(out.Lines) < 3 {
		t.Fatalf("expected at least three lines, got %d", len(out.Lines))
	}
}
