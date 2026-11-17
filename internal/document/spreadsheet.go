package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/lynncoleart/wordling/internal/worksheet"
)

// SpreadsheetLink identifies the source of the cached native table.
type SpreadsheetLink struct {
	Path     string
	Range    worksheet.Range
	Modified time.Time
}

type SpreadsheetTable struct {
	Cells []worksheet.Cell
	Link  *SpreadsheetLink
}

const sheetWidth = 9

func sheetHeader() []byte {
	h := tableOwner(tableProfiles[2].header)
	for _, offset := range []int{67, 69} {
		binary.LittleEndian.PutUint16(h[offset:], 1344)
	}
	h[75], h[76] = 3, 3
	return h
}

func sheetBody(cells []worksheet.Cell) ([]byte, error) {
	if len(cells) != 4 {
		return nil, fmt.Errorf("this worksheet table requires a two-by-two range")
	}
	p := tableProfiles[2]
	owners, _ := p.encode(make([]TableCell, 4))
	body := sheetHeader()
	cell := 0
	for _, owner := range owners[1:] {
		if owner[0] != 0xdc || owner[1] != 0 {
			body = append(body, owner...)
			continue
		}
		c := cells[cell]
		owner[4], owner[14] = 3, 0
		if len(c.Text) > sheetWidth || !simpleJoinText(c.Text) {
			return nil, fmt.Errorf("worksheet values must fit the nine-character table columns")
		}
		if c.Integer {
			n, err := strconv.ParseInt(c.Text, 10, 16)
			if err != nil || strconv.FormatInt(n, 10) != c.Text {
				return nil, fmt.Errorf("invalid worksheet integer")
			}
			owner[4], owner[14] = 2, 3
		}
		body = append(body, owner...)
		if c.Integer {
			// The right flush owner includes the trailing numeric sign cell.
			col := 10 + (cell%2)*11 + sheetWidth - len(c.Text)
			cache := []byte{0xd4, 5, 8, 0, byte(col), 0, 0, 0, 8, 0, 5, 0xd4}
			binary.LittleEndian.PutUint16(cache[6:], uint16(col*120+44-(cell%2)*24))
			body = append(body, cache...)
		}
		body = append(body, c.Text...)
		if c.Integer {
			body = append(body, ' ')
		}
		cell++
	}
	return body, nil
}

func linkRangeBytes(r worksheet.Range) []byte {
	out := make([]byte, 8)
	for i, n := range []uint16{r.Left, r.Top, r.Right, r.Bottom} {
		binary.LittleEndian.PutUint16(out[i*2:], n)
	}
	return out
}

func (link SpreadsheetLink) owners() ([]byte, []byte, error) {
	rangeText := link.Range.String()
	if len(link.Path) == 0 || len(link.Path) > 80 || !simpleJoinText(link.Path) || strings.ContainsAny(link.Path, "/<>|") || len(rangeText) > 10 {
		return nil, nil, fmt.Errorf("invalid DOS worksheet link path or range")
	}
	p := []byte(link.Path)
	begin := []byte{0xd2, 13, 0, 0, 10, 0, 1, 1, 0, 0, 0, 0}
	if y := link.Modified.Year(); y >= 1980 && y <= 2107 {
		t := link.Modified
		binary.LittleEndian.PutUint16(begin[8:], uint16((y-1980)<<9|int(t.Month())<<5|t.Day()))
		binary.LittleEndian.PutUint16(begin[10:], uint16(t.Hour()<<11|t.Minute()<<5|t.Second()/2))
	}
	coordinates := linkRangeBytes(link.Range)
	begin = append(begin, coordinates...)
	begin = append(begin, byte(len(p)))
	begin = append(begin, p...)
	begin = append(begin, 0, byte(len(rangeText)))
	begin = append(begin, rangeText...)
	begin = append(begin, []byte(strings.Repeat(" ", 10-len(rangeText)))...)
	end := append([]byte{0xd2, 14, 0, 0, 10, 0, 1}, coordinates...)
	end = append(end, byte(len(p)))
	end = append(end, p...)
	trailer := func(b []byte) []byte {
		n := len(b)
		binary.LittleEndian.PutUint16(b[2:4], uint16(n))
		return append(b, byte(n), byte(n>>8), b[1], 0xd2)
	}
	return trailer(begin), trailer(end), nil
}

func readSpreadsheetLink(raw []byte) (SpreadsheetLink, bool) {
	if len(raw) < 38 || raw[0] != 0xd2 || raw[1] != 13 || raw[7] != 1 {
		return SpreadsheetLink{}, false
	}
	stop := len(raw) - 4
	n := int(raw[20])
	if n < 1 || 23+n > stop || raw[21+n] != 0 {
		return SpreadsheetLink{}, false
	}
	rsize := int(raw[22+n])
	if rsize < 1 || 23+n+rsize > stop {
		return SpreadsheetLink{}, false
	}
	r, err := worksheet.ParseRange(string(raw[23+n : 23+n+rsize]))
	if err != nil || !bytes.Equal(raw[12:20], linkRangeBytes(r)) {
		return SpreadsheetLink{}, false
	}
	d, t := binary.LittleEndian.Uint16(raw[8:]), binary.LittleEndian.Uint16(raw[10:])
	link := SpreadsheetLink{Path: string(raw[21 : 21+n]), Range: r}
	if d != 0 {
		link.Modified = time.Date(1980+int(d>>9), time.Month((d>>5)&15), int(d&31), int(t>>11), int((t>>5)&63), int(t&31)*2, 0, time.UTC)
	}
	begin, _, err := link.owners()
	return link, err == nil && bytes.Equal(begin, raw)
}

// SpreadsheetTable recognizes the compact table produced by the bounded
// import profile, with an optional matching pair of link records.
func (d *Document) SpreadsheetTable() (SpreadsheetTable, bool) {
	var result SpreadsheetTable
	first, err := d.Token(0)
	if err != nil {
		return result, false
	}
	lo, hi := 0, d.TokenCount()
	if link, ok := readSpreadsheetLink(first.Raw); ok {
		_, end, _ := link.owners()
		last, err := d.Token(hi - 1)
		if err != nil || !bytes.Equal(last.Raw, end) {
			return result, false
		}
		result.Link = &link
		lo, hi = 1, hi-1
		first, err = d.Token(lo)
	}
	if err != nil || !bytes.Equal(first.Raw, sheetHeader()) {
		return SpreadsheetTable{}, false
	}
	var current *worksheet.Cell
	for i := lo + 1; i < hi; i++ {
		t, _ := d.Token(i)
		switch {
		case len(t.Raw) == 19 && t.Raw[0] == 0xdc && t.Raw[1] == 0 && len(result.Cells) < 4:
			result.Cells = append(result.Cells, worksheet.Cell{Integer: t.Raw[4] == 2})
			current = &result.Cells[len(result.Cells)-1]
		case t.Kind == ASCII && current != nil:
			if len(current.Text) > sheetWidth {
				return SpreadsheetTable{}, false
			}
			current.Text += string(t.Raw)
		}
	}
	for i, c := range result.Cells {
		if c.Integer {
			result.Cells[i].Text = strings.TrimSuffix(c.Text, " ")
		}
	}
	expected, err := sheetBody(result.Cells)
	if err != nil {
		return SpreadsheetTable{}, false
	}
	actual := d.state.image.Export()[d.state.gaps[lo]:d.state.gaps[hi]]
	if !bytes.Equal(expected, actual) {
		return SpreadsheetTable{}, false
	}
	return result, true
}

func (d *Document) PutSpreadsheet(c Cursor, cells []worksheet.Cell, link *SpreadsheetLink, refresh bool) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() || c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	if refresh {
		old, ok := d.SpreadsheetTable()
		if !ok || old.Link == nil || link == nil || old.Link.Path != link.Path || old.Link.Range != link.Range {
			return unchanged, fmt.Errorf("there is no matching worksheet link to refresh")
		}
	} else if d.TokenCount() != 0 || c.gap != 0 {
		return unchanged, fmt.Errorf("import this worksheet table into a blank document")
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	body, err := sheetBody(cells)
	if err != nil {
		return unchanged, err
	}
	if link != nil {
		begin, end, err := link.owners()
		if err != nil {
			return unchanged, err
		}
		body = append(append(begin, body...), end...)
	}
	raw := d.state.image.Export()
	at := d.state.gaps[0]
	if bytes.Equal(body, raw[at:]) {
		return unchanged, nil
	}
	candidate := append(raw[:at], body...)
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	if _, ok := next.SpreadsheetTable(); !ok {
		return unchanged, failure(UnsupportedBody, -1, noSpan)
	}
	c.state, c.gap = next.state, 0
	return EditResult{Document: next, Cursor: c, Changed: true}, nil
}
