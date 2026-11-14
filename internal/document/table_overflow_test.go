package document

import (
	"os"
	"strings"
	"testing"
)

func TestDOSTableOverflow(t *testing.T) {
	for _, tc := range []struct {
		name, visible, hidden string
		cell                  int
	}{
		{"OVRMID", "TAIL", "\n\n", 2},
		{"OVRLAST", "TAIL", "\n\n", 4},
		{"OVRWRAP", "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123", "IJGHEFCDAB896745", 0},
		{"OVRWORD", "ALPHA BRAVO CHARLIE DELTATROT", " ECHOOX F", 0},
	} {
		t.Run(tc.name, func(t *testing.T) {
			raw, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/tables/" + tc.name + ".WP")
			if err != nil {
				t.Fatal(err)
			}
			doc, err := Parse(raw)
			if err != nil {
				t.Fatal(err)
			}
			table, ok := doc.SimpleTable()
			if !ok {
				t.Fatal("DOS table not editable")
			}
			cell := table.Cells[tc.cell]
			if !strings.HasSuffix(cell.Text, tc.visible) || cell.Hidden != tc.hidden {
				t.Fatalf("visible=%q, hidden=%q", cell.Text, cell.Hidden)
			}
			caret, err := doc.CursorAt(cell.End)
			if err != nil {
				t.Fatal(err)
			}
			edit, err := doc.EditTableCell(caret, cell.End, cell.End, "Z")
			if err != nil || !edit.Changed {
				t.Fatalf("edit: %v, changed: %t", err, edit.Changed)
			}
			table, ok = edit.Document.SimpleTable()
			if !ok || !strings.Contains(table.Cells[tc.cell].Text+table.Cells[tc.cell].Hidden, "Z") {
				t.Fatal("edit did not survive native serialization")
			}
		})
	}
}
