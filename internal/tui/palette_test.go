package tui

import (
	"image/color"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
)

func TestUbuntuPalettePreservesTextAndUsesOfficialAccents(t *testing.T) {
	original := tea.NewView(menuGray + "Menu" + revealActive + " Selected" + revealCode + " Code")
	view := applyAubergine(original)
	if ansi.Strip(view.Content) != ansi.Strip(original.Content) {
		t.Fatal("palette changed the visible text")
	}
	if view.BackgroundColor != (color.RGBA{R: 44, B: 30, A: 255}) {
		t.Fatal("expected Ubuntu dark aubergine")
	}
	for _, rgb := range []string{"233;84;32", "249;155;17", "91;48;41"} {
		if !strings.Contains(view.Content, rgb) {
			t.Fatalf("expected palette color %s", rgb)
		}
	}
}
