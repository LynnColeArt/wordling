package tui

import (
	"fmt"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

func simpleTableFrame(table document.SimpleTable, gap int) (lines []string, x, y int, cell string) {
	const width = document.TableCellWidth
	bar := strings.Repeat("═", width)
	lines = []string{
		"╔" + bar + "╤" + bar + "╗",
		fmt.Sprintf("║%-*s│%-*s║", width, table.Cells[0].Text, width, table.Cells[1].Text),
		"╟" + bar + "┼" + bar + "╢",
		fmt.Sprintf("║%-*s│%-*s║", width, table.Cells[2].Text, width, table.Cells[3].Text),
		"╚" + bar + "╧" + bar + "╝",
	}
	if index, inside := table.CellAt(gap); inside {
		x = 1 + index%2*(width+1) + min(width-1, gap-table.Cells[index].Start)
		y = 1 + index/2*2
		cell = fmt.Sprintf("Cell %c%d", 'A'+rune(index%2), index/2+1)
	}
	return
}
