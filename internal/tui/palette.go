package tui

import (
	"image/color"
	"strings"

	tea "charm.land/bubbletea/v2"
)

// Ubuntu brand aubergine and Yaru GTK orange, yellow, and porcelain.
// Brown is a Wordling surface color.
// The original palette stays available for historical screenshots and terminals
// where the classic ANSI colors are preferred.
var auberginePalette = strings.NewReplacer(
	revealBase, "\x1b[22;38;2;247;247;247;48;2;44;0;30m",
	revealCode, "\x1b[1;38;2;249;155;17;48;2;44;0;30m",
	revealActive, "\x1b[22;38;2;44;0;30;48;2;233;84;32m",
	menuGray, "\x1b[22;38;2;255;242;225;48;2;91;48;41m",
	menuMnemonic, "\x1b[1;38;2;249;155;17;48;2;91;48;41m",
	boldUnderline, "\x1b[1;38;2;249;155;17;48;2;91;48;41m",
	"\x1b[1;30;46m", "\x1b[1;38;2;44;0;30;48;2;249;155;17m",
	"\x1b[1;37;41m", "\x1b[1;38;2;44;0;30;48;2;233;84;32m",
)

func applyAubergine(view tea.View) tea.View {
	view.Content = auberginePalette.Replace(view.Content)
	view.BackgroundColor = color.RGBA{R: 44, G: 0, B: 30, A: 255}
	view.ForegroundColor = color.RGBA{R: 247, G: 247, B: 247, A: 255}
	return view
}
