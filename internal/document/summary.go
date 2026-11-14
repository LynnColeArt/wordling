package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strings"
	"time"

	"github.com/lynncoleart/wordling/internal/wp51"
)

// Summary is the WP 5.1 document summary packet. The fixed fields retain their
// original date representation when another field is edited.
type Summary struct {
	Created                                                          string
	Date                                                             [10]byte
	Name, Type, Subject, Author, Typist, Abstract, Account, Keywords string
}

func NewSummary(now time.Time) Summary {
	s := Summary{Created: now.Format("01-02-06 03:04") + strings.ToLower(now.Format("PM")[:1])}
	binary.LittleEndian.PutUint16(s.Date[:], uint16(now.Year()))
	s.Date[2], s.Date[3], s.Date[4], s.Date[5] = byte(now.Month()), byte(now.Day()), byte(now.Hour()), byte(now.Minute())
	return s
}

func (d *Document) Summary() (Summary, bool, error) {
	if !d.valid() {
		return Summary{}, false, failure(InvalidDocument, -1, noSpan)
	}
	for _, p := range d.state.image.Inspect().Packets {
		if p.Type == 1 {
			raw, _ := d.state.image.Bytes(p.Data)
			s, err := parseSummary(raw)
			return s, true, err
		}
	}
	return Summary{}, false, nil
}

func parseSummary(raw []byte) (Summary, error) {
	var s Summary
	bad := fmt.Errorf("unsupported WordPerfect summary packet")
	if len(raw) < 115+6+12 || raw[25] != 0 || raw[114] != 0 || raw[len(raw)-12] != 255 || raw[len(raw)-1] != 255 {
		return s, bad
	}
	s.Created = strings.TrimRight(string(raw[:25]), " ")
	s.Name = strings.TrimRight(string(raw[26:94]), " ")
	s.Type = strings.TrimRight(string(raw[94:114]), " ")
	copy(s.Date[:], raw[len(raw)-11:len(raw)-1])
	var fields []string
	payload := raw[115 : len(raw)-12]
	start := 0
	for at := 0; at < len(payload); {
		if payload[at] == 0 {
			fields = append(fields, string(payload[start:at]))
			at++
			start = at
		} else {
			at += SummaryOwnerWidth(string(payload[at:]))
		}
	}
	if len(fields) != 6 || start != len(payload) {
		return s, bad
	}
	s.Subject, s.Author, s.Typist = string(fields[0]), string(fields[1]), string(fields[2])
	s.Abstract, s.Account, s.Keywords = string(fields[3]), string(fields[4]), string(fields[5])
	return s, nil
}

// SummaryOwnerWidth returns the size of a framed character or emphasis owner.
func SummaryOwnerWidth(text string) int {
	if len(text) >= 4 && text[0] == 0xc0 && text[3] == 0xc0 {
		return 4
	}
	if len(text) >= 3 && (text[0] == 0xc3 || text[0] == 0xc4) && text[2] == text[0] {
		return 3
	}
	return 1
}

func summaryFieldValid(text string) bool {
	for len(text) > 0 {
		width := SummaryOwnerWidth(text)
		if text[0] == 0 && width == 1 {
			return false
		}
		text = text[width:]
	}
	return true
}

func (s Summary) packet() ([]byte, error) {
	var raw []byte
	fixed := []struct {
		text  string
		width int
	}{{s.Created, 25}, {s.Name, 68}, {s.Type, 20}}
	for i, f := range fixed {
		if len(f.text) > f.width || !summaryFieldValid(f.text) {
			return nil, fmt.Errorf("summary field exceeds %d bytes", f.width)
		}
		raw = append(raw, f.text...)
		raw = append(raw, strings.Repeat(" ", f.width-len(f.text))...)
		if i == 0 || i == 2 {
			raw = append(raw, 0)
		}
	}
	variable := []struct {
		text  string
		limit int
	}{{s.Subject, 160}, {s.Author, 60}, {s.Typist, 60}, {s.Abstract, 780}, {s.Account, 160}, {s.Keywords, 160}}
	for _, f := range variable {
		if len(f.text) > f.limit || !summaryFieldValid(f.text) {
			return nil, fmt.Errorf("summary field exceeds %d bytes", f.limit)
		}
		raw = append(raw, f.text...)
		raw = append(raw, 0)
	}
	raw = append(raw, 255)
	raw = append(raw, s.Date[:]...)
	return append(raw, 255), nil
}

// WithSummary edits the native prefix while keeping body owners and history.
func (d *Document) WithSummary(c Cursor, s *Summary) (EditResult, error) {
	if !d.valid() || c.state != d.state {
		return unchangedEdit(d, c), failure(InvalidPosition, -1, noSpan)
	}
	if _, err := d.prefixMutationAdmission(); err != nil {
		return unchangedEdit(d, c), err
	}
	if _, present := d.InitialLineSpacing(); present {
		return unchangedEdit(d, c), failure(UnsupportedPrefix, -1, d.state.initialCodes)
	}
	info := d.state.image.Inspect()
	var packet []byte
	if s != nil {
		var err error
		packet, err = s.packet()
		if err != nil {
			return unchangedEdit(d, c), err
		}
	}
	first, last := info.Blocks[0].Data.Offset, info.Blocks[1].Data.Offset
	at := last
	for _, p := range info.Packets {
		if p.Type == 6 && p.Data.Offset > first+50 {
			at = p.Data.Offset
			break
		}
	}
	var old wp51.Packet
	for _, p := range info.Packets {
		if p.Type == 1 {
			old = p
			at = p.Data.Offset
			break
		}
	}
	raw := d.state.image.Export()
	oldEnd := at + old.Data.Length
	if bytes.Equal(raw[at:oldEnd], packet) {
		return d.everydayNoOp(c, summaryEdit), nil
	}
	delta := len(packet) - old.Data.Length
	move := func(offset int) int {
		if offset >= oldEnd {
			return offset + delta
		}
		return offset
	}
	// Rebuild the two fixed-size directory blocks, preserving packet order
	// except for inserting or removing the summary before the state packet.
	var entries []fastSaveEntry
	for _, p := range info.Packets {
		if p.Type == 1 {
			continue
		}
		if p.Type == 6 && len(entries) == 3 && s != nil {
			entries = append(entries, fastSaveEntry{1, at, len(packet)})
		}
		if p.Type == 8 && len(entries) == 4 && s != nil {
			entries = append(entries, fastSaveEntry{1, at, len(packet)})
		}
		entries = append(entries, fastSaveEntry{p.Type, move(p.Data.Offset), p.Data.Length})
	}
	out := make([]byte, 0, len(raw)+delta)
	out = append(out, raw[:at]...)
	out = append(out, packet...)
	out = append(out, raw[oldEnd:]...)
	last = move(last)
	binary.LittleEndian.PutUint32(out[4:], uint32(move(info.Body.Offset)))
	binary.LittleEndian.PutUint32(out[first+6:], uint32(last))
	clear(out[first+10 : first+50])
	clear(out[last+10 : last+50])
	for i, p := range entries {
		index := first + 10*(i+1)
		if i >= 4 {
			index = last + 10*(i-3)
		}
		writeFastSaveEntry(out, index, p)
	}
	next, err := parseRevision(out, d.state.birth)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	if _, err = next.prefixMutationAdmission(); err != nil {
		return unchangedEdit(d, c), err
	}
	cursor := Cursor{state: next.state, gap: c.gap, reveal: c.reveal}
	tokenMap := make([]int, d.TokenCount())
	for i := range tokenMap {
		tokenMap[i] = i
	}
	return EditResult{Document: next, Cursor: cursor, Changed: true, everyday: &everydayReceipt{before: d.state, after: next.state, cursor: cursor, changed: true, kind: summaryEdit, tokenMap: tokenMap}}, nil
}

func (h History) AfterSummary(r EditResult) (History, error) {
	return h.afterEveryday(r, summaryEdit)
}

// UsesSummaryPrefix identifies documents for which a legacy fast-save
// rewrite would discard the summary or depend on an unsupported birth graph.
func (d *Document) UsesSummaryPrefix() bool {
	if !d.valid() {
		return false
	}
	for _, image := range []*wp51.Image{d.state.image, d.state.birth.originalImage} {
		if image != nil {
			for _, p := range image.Inspect().Packets {
				if p.Type == 1 {
					return true
				}
			}
		}
	}
	return false
}

// ParseSummaryDate updates both native representations of the creation date.
func ParseSummaryDate(value string) (Summary, error) {
	value = strings.ToUpper(strings.TrimSpace(value))
	for _, layout := range []string{"1/2/2006 3:04PM", "1/2/06 3:04PM", "01-02-06 03:04PM"} {
		date, err := time.Parse(layout, value+"M")
		if err == nil {
			return NewSummary(date), nil
		}
	}
	return Summary{}, fmt.Errorf("Enter the creation date as month/day/year hour:minutea or p")
}

// CaptureSummary extracts the default RE: heading and the opening abstract.
func (d *Document) CaptureSummary(summary Summary) Summary {
	var abstract, line strings.Builder
	var subjectFound bool
	finishLine := func() {
		if !subjectFound {
			text := line.String()
			if at := strings.Index(strings.ToUpper(text), "RE:"); at >= 0 {
				subject := strings.TrimSpace(text[at+3:])
				summary.Subject = subject[:min(160, len(subject))]
				subjectFound = true
			}
		}
		line.Reset()
	}
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		var text string
		switch t.Kind {
		case ASCII:
			text = string(t.Raw)
		case SoftReturn, SoftPage, Tab:
			text = " "
		case HardReturn, HardReturnSoftPage, DormantHardReturn, HardPage:
			finishLine()
			if abstract.Len() > 0 && abstract.Len() <= 398 {
				abstract.WriteString("; ")
			}
		}
		line.WriteString(text)
		if abstract.Len() < 400 {
			abstract.WriteString(text)
		}
		if subjectFound && abstract.Len() >= 400 {
			break
		}
	}
	finishLine()
	summary.Abstract = strings.TrimSuffix(strings.TrimSpace(abstract.String()), ";")
	return summary
}

// ExportSummarySave retains the Summary packet in the witnessed Fast Save
// generation and uses the current compact graph for a new summary or removal.
func (d *Document) ExportSummarySave(fast bool) ([]byte, error) {
	if !fast || !d.Birth().IsLoaded() {
		return d.Export()
	}
	live := fastSaveLivePackets(d.state.image)
	prior := fastSaveLivePackets(d.state.birth.originalImage)
	if len(live[1]) == 0 || len(prior[1]) == 0 {
		return d.Export()
	}
	return d.ExportFastSave()
}
