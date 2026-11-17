package layout

import (
	"bytes"
	"errors"
	"math"
	"strconv"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

const standardPageLines = 66

// StandardPage is a Standard Printer page at ten columns and six lines per inch.
type StandardPage struct {
	lines           [standardPageLines]standardLine
	Number, Section int
	Roman           bool
}

type printedFootnote struct {
	number int
	lines  []string
}

type printCommand struct {
	column int
	data   []byte
}

type standardLine struct {
	commands                                  []printCommand
	text, bold, underline, redline, strikeout []byte
}

func StandardPages(d *document.Document, settings Settings) ([]StandardPage, error) {
	if !matchedProfile(settings) {
		return nil, errSettings
	}
	if sheet, ok := d.SpreadsheetTable(); ok {
		return standardSpreadsheetPages(sheet, settings), nil
	}
	if table, ok := d.SimpleTable(); ok {
		return standardTablePages(table, settings)
	}
	if err := d.CheckPrintBody(); err != nil {
		return nil, err
	}
	projected, err := FromDocument(d, settings)
	if err != nil {
		return nil, err
	}
	pages := make([]StandardPage, projected.Lines[len(projected.Lines)-1].Page)
	footnotes := make(map[int][]printedFootnote)
	var endnotes []document.Note
	bottom := settings.MarginBottomInches
	pageBottoms := make(map[int]int)
	var headers [4]document.PageText
	var runningText = make([][4]document.PageText, len(pages))
	labels := projected.pageLabels()
	pageFormat := make([]int, len(pages))
	suppressNumber := make([]bool, len(pages))
	position := 0
	for _, line := range projected.Lines {
		for _, item := range line.Tokens {
			if choice := item.Token.PageNumberPosition(); choice != 0 {
				position = choice
			}
			if item.Token.Kind == document.SuppressPageNumber {
				suppressNumber[line.Page-1] = true
			}
		}
		pageFormat[line.Page-1] = position
	}
	bold, underline := false, false
	redline, strikeout, italics := false, false, false
	numberLines, lineNumber := false, 0
	for _, line := range projected.Lines {
		for _, item := range line.Tokens {
			if _, b, ok := item.Token.PageMargins(); ok {
				bottom = float64(b) / document.UnitsPerInch
			}
			if text, ok := item.Token.PageText(); ok {
				headers[text.Slot] = text
			}
		}
		runningText[line.Page-1] = headers
		pageBottoms[line.Page] = int(math.Round((settings.PageHeightInches - bottom) * 6))
		row := int(math.Round(line.TopInches * 6))
		reservedHeader := headers[0].Text != "" || headers[1].Text != ""
		shownHeader := headers[0].Applies(line.Page) || headers[1].Applies(line.Page)
		if reservedHeader && !shownHeader {
			row -= 2
		}
		if row < 0 || row >= standardPageLines {
			return nil, errors.New("print: line outside Letter page")
		}
		if pageFormat[line.Page-1] == document.PageNumberTopCenter && !suppressNumber[line.Page-1] {
			row += 2
			if row >= standardPageLines {
				return nil, errors.New("print: top page number leaves no room for text")
			}
		}
		page := &pages[line.Page-1]
		label := labels[line.Page-1]
		page.Number, page.Section, page.Roman = label.number, label.section, label.roman
		out := &page.lines[row]
		spaces, padding := standardJustification(line)
		offset, used := 0, 0
		for index, token := range line.Tokens {
			advance := projected.advanceOffsets[token.Index]
			printRow := row + int(math.Round((line.TopInches+advance.down)*6)) - int(math.Round(line.TopInches*6))
			if printRow < 0 || printRow >= standardPageLines {
				return nil, errors.New("print: advance outside Letter page")
			}
			out = &page.lines[printRow]
			token.LeftInches += advance.right
			switch token.Token.Kind {
			case document.PrinterCommand:
				column := int(math.Floor(token.LeftInches*10+1e-9)) + offset
				out.commands = append(out.commands, printCommand{max(0, column), token.Token.PrinterBytes()})
			case document.LineNumbering:
				numberLines = token.Token.EnablesLineNumbering()
			case document.BoldOn:
				bold = true
			case document.BoldOff:
				bold = false
			case document.UnderlineOn:
				underline = true
			case document.UnderlineOff:
				underline = false
			case document.RedlineOn:
				redline = true
			case document.RedlineOff:
				redline = false
			case document.StrikeoutOn:
				strikeout = true
			case document.StrikeoutOff:
				strikeout = false
			case document.ItalicsOn:
				italics = true
			case document.ItalicsOff:
				italics = false
			case document.DateCode, document.PageReference, document.OutlineNumber:
				column := int(math.Floor(token.LeftInches*10+1e-9)) + offset
				for i := range token.Text {
					out.text = printCell(out.text, column+i, token.Text[i])
					if token.Text[i] != ' ' && bold {
						out.bold = printCell(out.bold, column+i, token.Text[i])
					}
					if token.Text[i] != ' ' && (underline || italics) {
						out.underline = printCell(out.underline, column+i, '_')
					}
				}
			case document.Footnote, document.Endnote:
				note, _ := token.Token.Note()
				if note.End {
					endnotes = append(endnotes, note)
				} else {
					rows := strings.Split(note.Text, "\n")
					if note.FirstPageLines > 0 {
						footnotes[line.Page] = append(footnotes[line.Page], printedFootnote{note.Number, rows[:note.FirstPageLines]})
						footnotes[line.Page+1] = append(footnotes[line.Page+1], printedFootnote{0, rows[note.FirstPageLines:]})
						if pageBottoms[line.Page+1] == 0 {
							pageBottoms[line.Page+1] = pageBottoms[line.Page]
						}
					} else {
						footnotes[line.Page] = append(footnotes[line.Page], printedFootnote{note.Number, rows})
					}
				}
				column := int(math.Floor(token.LeftInches*10+1e-9)) + offset
				for i := range len(token.Text) {
					out.text = printCell(out.text, column+i, token.Text[i])
				}
			case document.ContentsLeader:
				stop := int(math.Round(token.LeftInches * 10))
				for col := len(out.text) + 2; col < stop; col += 2 {
					out.text = printCell(out.text, col, '.')
				}
			case document.ASCII, document.ExtendedCharacter, document.HardSpace:
				if token.Text == "" {
					continue
				}
				column := int(math.Floor(token.LeftInches*10+1e-9)) + offset
				if line.Justification == document.JustifyCenter {
					column = int(math.Floor(token.LeftInches*10+0.5+1e-9)) + offset
				}
				character := token.Token.Raw[0]
				// Standard Printer reserves a cell for an unsupported glyph
				// and still emits any active overstrike passes.
				extended := token.Token.Kind == document.ExtendedCharacter
				if extended || token.Token.Kind == document.HardSpace {
					character = ' '
				}
				out.text = printCell(out.text, column, character)
				if redline {
					out.redline = printCell(out.redline, column, '.')
				}
				if strikeout {
					out.strikeout = printCell(out.strikeout, column, '-')
				}
				if bold && (extended || character != ' ') {
					out.bold = printCell(out.bold, column, character)
				}
				if (underline || italics) && (extended || character != ' ') {
					out.underline = printCell(out.underline, column, '_')
				}
				if spaces[index] {
					used++
					// DOS distributes the remainder from the first word gap
					// with an accumulator, keeping leading spaces fixed.
					offset = (used*padding + len(spaces) - 1) / len(spaces)
				}
			}
		}
		if numberLines && len(out.text) > 0 {
			lineNumber++
			label := strconv.Itoa(lineNumber)
			for i := range len(label) {
				out.text = printCell(out.text, 6-len(label)+i, label[i])
			}
		}
	}
	for i, slots := range runningText {
		for _, header := range slots {
			if header.Text == "" || !header.Applies(i+1) {
				continue
			}
			row := 6
			if header.Footer() {
				row = 59
			}
			if len(pages[i].lines[row].text) != 0 {
				return nil, errors.New("print: header or footer overlaps printed text")
			}
			pages[i].lines[row].text = []byte("          " + header.Text)
		}
	}
	formattedNumbers := projected.PageLabels()
	for i, position := range pageFormat {
		if position == 0 || suppressNumber[i] {
			continue
		}
		text := formattedNumbers[i]
		row, col := pageBottoms[i+1]-1, 75-len(text)
		if position == document.PageNumberTopCenter {
			row = int(math.Round(settings.MarginTopInches * 6))
			col = (85 - len(text)) / 2
		}
		if row < 0 || row >= standardPageLines || col < 0 || len(pages[i].lines[row].text) != 0 {
			return nil, errors.New("print: page number overlaps printed text")
		}
		pages[i].lines[row].text = []byte(strings.Repeat(" ", col) + text)
	}
	for len(pages) < projected.Lines[len(projected.Lines)-1].Page+1 && len(footnotes[len(pages)+1]) > 0 {
		last := pages[len(pages)-1]
		pages = append(pages, StandardPage{Number: last.Number + 1, Section: last.Section, Roman: last.Roman})
	}
	for number, notes := range footnotes {
		total := 0
		for _, note := range notes {
			total += len(note.lines)
		}
		first := pageBottoms[number] - total
		page := &pages[number-1]
		if first < 2 || len(page.lines[first-2].text) != 0 {
			return nil, errors.New("print: footnotes exceed available space on the page")
		}
		for _, line := range page.lines[first-2:] {
			if len(line.text) != 0 {
				return nil, errors.New("print: footnotes overlap document text")
			}
		}
		page.lines[first-2] = standardLine{
			text: bytes.Repeat([]byte{' '}, 30), underline: []byte("          ____________________"),
		}
		for _, note := range notes {
			for j, text := range note.lines {
				prefix := "          "
				if j == 0 && note.number > 0 {
					prefix = "               " + strconv.Itoa(note.number)
				}
				page.lines[first].text = []byte(prefix + text)
				first++
			}
		}
	}
	for start := 0; start < len(endnotes); start += 54 {
		page := StandardPage{Number: pages[len(pages)-1].Number + 1, Section: pages[len(pages)-1].Section}
		for i, note := range endnotes[start:min(start+54, len(endnotes))] {
			page.lines[6+i].text = []byte("          " + strconv.Itoa(note.Number) + "." + note.Text)
		}
		pages = append(pages, page)
	}
	if binding := d.BindingOffset(); binding != 0 {
		for i := range pages {
			shift := int(math.Floor(float64(binding)/120 + 0.5))
			if pages[i].Number%2 == 0 {
				shift = -binding / 120
			}
			for j := range pages[i].lines {
				line := &pages[i].lines[j]
				line.text = shiftPrintColumns(line.text, shift)
				for i := range line.commands {
					line.commands[i].column = max(0, line.commands[i].column+shift)
				}
				line.bold = shiftPrintColumns(line.bold, shift)
				line.underline = shiftPrintColumns(line.underline, shift)
				line.strikeout = shiftPrintColumns(line.strikeout, shift)
				line.redline = shiftPrintColumns(line.redline, shift)
			}
		}
	}
	return pages, nil
}

// The captured default standalone two-by-two table prints without rules
// on the pinned text printer, inset one cell from the left table edge.
func standardTablePages(table document.SimpleTable, settings Settings) ([]StandardPage, error) {
	if len(table.Widths) != 2 || len(table.Cells) != 4 || len(table.PageStarts) != 0 {
		return nil, errors.New("print: table layout has no Standard Printer profile")
	}
	var page StandardPage
	page.Number, page.Section = 1, 1
	row := int(math.Round(settings.MarginTopInches*6)) + 1
	left := int(math.Round(settings.MarginLeftInches*10)) + 1
	for i, cell := range table.Cells {
		text := cell.DisplayText()
		if right, joined := table.Cells[0].JoinedRight(); i == 1 && joined && cell.Covered() {
			text = right
		}
		if strings.ContainsAny(text, "\r\n\t") || cell.Hidden != "" {
			return nil, errors.New("print: multiline table cells have no Standard Printer profile")
		}
		for j := range len(text) {
			if text[j] < 32 || text[j] > 126 {
				return nil, errors.New("print: table cells require printable ASCII")
			}
			column := left + j
			if i%2 == 1 {
				column += table.Widths[0] + 1
			}
			line := &page.lines[row+i/2]
			line.text = printCell(line.text, column, text[j])
		}
	}
	return []StandardPage{page}, nil
}

func standardSpreadsheetPages(sheet document.SpreadsheetTable, settings Settings) []StandardPage {
	var page StandardPage
	page.Number, page.Section = 1, 1
	top := int(math.Round(settings.MarginTopInches*6)) + 1
	left := int(math.Round(settings.MarginLeftInches*10)) + 1
	for i, c := range sheet.Cells {
		text, col := c.Text, left+(i%2)*11
		if c.Integer {
			col += 8 - len(text)
			text += " "
		}
		line := &page.lines[top+i/2]
		for j := range len(text) {
			line.text = printCell(line.text, col+j, text[j])
		}
	}
	return []StandardPage{page}
}

func shiftPrintColumns(row []byte, shift int) []byte {
	if len(row) == 0 || shift == 0 {
		return row
	}
	if shift < 0 {
		return row[min(-shift, len(row)):]
	}
	return append(bytes.Repeat([]byte{' '}, shift), row...)
}

func standardJustification(line Line) (map[int]bool, int) {
	if !line.FullJustification || len(line.Tokens) == 0 {
		return nil, 0
	}
	last := line.Tokens[len(line.Tokens)-1]
	if last.Token.Kind != document.SoftReturn && last.Token.Kind != document.SoftPage {
		return nil, 0
	}
	slack := int(math.Round((line.RightInches - last.LeftInches) * 10))
	if slack <= 0 {
		return nil, 0
	}
	var spaces map[int]bool
	seenWord := false
	for i, token := range line.Tokens {
		switch token.Token.Kind {
		case document.Tab, document.DecimalTab, document.SoftDecimalTab, document.CenterLine, document.FlushRight, document.AdvanceCode:
			return nil, 0
		case document.ASCII:
			if token.Text == " " && seenWord {
				if spaces == nil {
					spaces = make(map[int]bool)
				}
				spaces[i] = true
				seenWord = false
			} else if token.Text != " " && token.Text != "" {
				seenWord = true
			}
		case document.ExtendedCharacter:
			seenWord = true
		}
	}
	return spaces, slack
}

func printCell(line []byte, column int, character byte) []byte {
	for len(line) <= column {
		line = append(line, ' ')
	}
	line[column] = character
	return line
}

// StandardPrint writes the pinned printer's carriage returns and overstrikes.
func StandardPrint(pages []StandardPage) []byte {
	var output bytes.Buffer
	for _, page := range pages {
		output.WriteByte('\r')
		last := 0
		for i, line := range page.lines {
			if len(line.text) != 0 || len(line.commands) != 0 {
				last = i
			}
		}
		for i, line := range page.lines {
			written := 0
			for _, command := range line.commands {
				column := max(written, command.column)
				stop := min(column, len(line.text))
				if stop > written {
					output.Write(line.text[written:stop])
				}
				for i := max(written, stop); i < column; i++ {
					output.WriteByte(' ')
				}
				written = column
				output.Write(command.data)
			}
			output.Write(line.text[min(written, len(line.text)):])
			for _, pass := range [][]byte{line.bold, line.underline, line.strikeout, line.redline} {
				if len(pass) != 0 {
					output.WriteByte('\r')
					output.Write(pass)
				}
			}
			if i == last && (len(line.text) != 0 || len(line.commands) != 0) {
				output.WriteByte('\r')
			}
			output.WriteString("\r\n")
		}
	}
	return output.Bytes()
}

// TextLines gives the page's character cells for terminal View Document.
func (p StandardPage) TextLines() []string {
	lines := make([]string, len(p.lines))
	for i, line := range p.lines {
		lines[i] = strings.TrimRight(string(line.text), " ")
	}
	return lines
}
