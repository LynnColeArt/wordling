package layout

import (
	"bytes"
	"errors"
	"math"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

const standardPageLines = 66

// StandardPage is a Standard Printer page at ten columns and six lines per inch.
type StandardPage struct {
	lines [standardPageLines]standardLine
}

type standardLine struct {
	text, bold, underline []byte
}

func StandardPages(d *document.Document, settings Settings) ([]StandardPage, error) {
	if !matchedProfile(settings) {
		return nil, errSettings
	}
	if err := d.CheckMutation(); err != nil {
		return nil, err
	}
	projected, err := FromDocument(d, settings)
	if err != nil {
		return nil, err
	}
	pages := make([]StandardPage, projected.Lines[len(projected.Lines)-1].Page)
	bold, underline := false, false
	for _, line := range projected.Lines {
		row := int(math.Round(line.TopInches * 6))
		if row < 0 || row >= standardPageLines {
			return nil, errors.New("print: line outside Letter page")
		}
		out := &pages[line.Page-1].lines[row]
		for _, token := range line.Tokens {
			switch token.Token.Kind {
			case document.BoldOn:
				bold = true
			case document.BoldOff:
				bold = false
			case document.UnderlineOn:
				underline = true
			case document.UnderlineOff:
				underline = false
			case document.ASCII:
				if token.Text == "" {
					continue
				}
				column := int(math.Round(token.LeftInches * 10))
				character := token.Token.Raw[0]
				out.text = printCell(out.text, column, character)
				if bold && character != ' ' {
					out.bold = printCell(out.bold, column, character)
				}
				if underline && character != ' ' {
					out.underline = printCell(out.underline, column, '_')
				}
			}
		}
	}
	return pages, nil
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
			if len(line.text) != 0 {
				last = i
			}
		}
		for i, line := range page.lines {
			output.Write(line.text)
			for _, pass := range [][]byte{line.bold, line.underline} {
				if len(pass) != 0 {
					output.WriteByte('\r')
					output.Write(pass)
				}
			}
			if i == last && len(line.text) != 0 {
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
