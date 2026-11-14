package layout

import "github.com/lynncoleart/wordling/internal/document"

// StandardSummary formats the metadata sheet used by Print, Document on Disk.
func StandardSummary(summary document.Summary, name, revised string) StandardPage {
	var page StandardPage
	rows := []struct {
		row          int
		label, value string
	}{
		{7, "System Name", name}, {8, "System Filetype", "WP5.1"},
		{9, "Document Name", summary.Name}, {10, "Document Type", summary.Type},
		{12, "Creation Date", summary.Created}, {13, "Revision Date", revised},
		{15, "Author", summary.Author}, {16, "Typist", summary.Typist},
		{17, "Subject", summary.Subject}, {18, "Account", summary.Account},
		{19, "Keywords", summary.Keywords}, {21, "Abstract", summary.Abstract},
	}
	for _, field := range rows {
		line := &page.lines[field.row]
		line.text = []byte("          " + field.label + ":  ")
		bold, underline := false, false
		var overstrike []byte
		for raw := field.value; len(raw) > 0; {
			width := document.SummaryOwnerWidth(raw)
			switch width {
			case 3:
				if raw[1] == 12 {
					bold = raw[0] == 0xc3
				}
				if raw[1] == 14 {
					underline = raw[0] == 0xc3
				}
			default:
				char := byte(' ')
				if width == 1 {
					char = raw[0]
				}
				col := len(line.text)
				line.text = append(line.text, char)
				if bold && char != ' ' {
					overstrike = printCell(overstrike, col, char)
				}
				if underline && char != ' ' {
					overstrike = printCell(overstrike, col, '_')
				}
			}
			raw = raw[width:]
		}
		line.bold = overstrike
	}
	return page
}
