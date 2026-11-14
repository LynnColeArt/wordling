package layout

import (
	"encoding/binary"
	"strconv"
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
)

type pageLabel struct {
	number, section int
	roman           bool
	upper           bool
}

// pageLabels resolves the same numbering for printing and generated
// references. A number reset applies to the whole physical page.
func (l Layout) pageLabels() []pageLabel {
	if len(l.Lines) == 0 {
		return nil
	}
	labels := make([]pageLabel, l.Lines[len(l.Lines)-1].Page)
	number, physical := 0, 0
	var sections [2]int
	roman, upper := false, false
	for _, line := range l.Lines {
		if physical != line.Page {
			physical = line.Page
			number++
		}
		for _, item := range line.Tokens {
			if item.Token.Kind != document.PageNumberReset {
				continue
			}
			value := binary.LittleEndian.Uint16(item.Token.Raw[6:8])
			number, roman = int(value&0x7fff), value&0x8000 != 0
			upper = item.Token.Raw[9] == 3
			if roman {
				sections[1]++
			} else {
				sections[0]++
			}
		}
		style := 0
		if roman {
			style = 1
		}
		sections[style] = max(1, sections[style])
		labels[physical-1] = pageLabel{number, sections[style], roman, upper}
	}
	return labels
}

// PageLabels returns the generated numbering for each physical page,
// indexed from zero, without changing the physical positions used by layout.
func (l Layout) PageLabels() []string {
	labels := l.pageLabels()
	result := make([]string, len(labels))
	for i, label := range labels {
		if !label.roman {
			result[i] = strconv.Itoa(label.number)
		} else {
			result[i] = romanPageNumber(label.number)
			if label.upper {
				result[i] = strings.ToUpper(result[i])
			}
		}
	}
	return result
}

func romanPageNumber(n int) string {
	var out strings.Builder
	for _, pair := range [...]struct {
		n    int
		text string
	}{
		{1000, "m"}, {900, "cm"}, {500, "d"}, {400, "cd"}, {100, "c"}, {90, "xc"},
		{50, "l"}, {40, "xl"}, {10, "x"}, {9, "ix"}, {5, "v"}, {4, "iv"}, {1, "i"},
	} {
		for n >= pair.n {
			out.WriteString(pair.text)
			n -= pair.n
		}
	}
	return out.String()
}
