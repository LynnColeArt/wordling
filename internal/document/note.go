package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strconv"
	"strings"
)

type Note struct {
	Number         int
	Text           string
	End            bool
	FirstPageLines int
}

func (t Token) Note() (Note, bool) {
	if t.Kind != Footnote && t.Kind != Endnote {
		return Note{}, false
	}
	return parseNote(t.Raw)
}

func (t Token) NoteNumber() string {
	if (t.Kind != Footnote && t.Kind != Endnote) || len(t.Raw) < 7 {
		return ""
	}
	return strconv.Itoa(int(binary.LittleEndian.Uint16(t.Raw[5:7])))
}

func parseNote(raw []byte) (Note, bool) {
	if len(raw) < 14 || raw[0] != 0xd6 || raw[1] > 1 || raw[len(raw)-1] != 0xd6 {
		return Note{}, false
	}
	header := 19
	if raw[7] == 1 && raw[1] == 0 {
		header = 21
	}
	end := raw[1] == 1
	if end {
		header = 11
	}
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) {
		return Note{}, false
	}
	if stop <= header+1 || stop-header-1 > 512 || raw[header] != 0x8d || raw[4] != 0 {
		return Note{}, false
	}
	note := Note{Number: int(binary.LittleEndian.Uint16(raw[5:7])), End: end}
	if note.Number == 0 {
		return Note{}, false
	}
	body := raw[header+1 : stop]
	if raw[7] == 1 && !end {
		i := bytes.IndexByte(body, 0xd4)
		if i < 0 || i+33 >= len(body) || !endOfPageShaped(body[i:i+32]) || body[i+32] != hardReturnPageByte {
			return Note{}, false
		}
		note.FirstPageLines = 1 + bytes.Count(body[:i], []byte{hardReturnByte})
		body = append(append(bytes.Clone(body[:i]), hardReturnByte), body[i+33:]...)
		if int(binary.LittleEndian.Uint16(raw[8:10])) != note.FirstPageLines*200 ||
			int(binary.LittleEndian.Uint16(raw[10:12])) != (1+bytes.Count(body[i+1:], []byte{hardReturnByte}))*200 ||
			int(binary.LittleEndian.Uint16(raw[12:14])) != noteSplitHeight(1+bytes.Count(body, []byte{hardReturnByte}), note.FirstPageLines) {
			return Note{}, false
		}
	} else if raw[7] != 0 {
		return Note{}, false
	}
	for _, line := range strings.Split(string(body), "\n") {
		if len(line) == 0 || len(line) > 60 {
			return Note{}, false
		}
		for _, ch := range []byte(line) {
			if ch < 32 || ch > 126 {
				return Note{}, false
			}
		}
	}
	if !end && bytes.Contains(body, []byte{hardReturnByte}) {
		if (note.FirstPageLines == 0 && raw[17] == 0 && raw[18] == 0) || raw[14] != 0 || raw[15] != 0 || raw[16] != 0 || note.FirstPageLines > 0 && (raw[17] != 0 || raw[18] != 0) {
			return Note{}, false
		}
		if note.FirstPageLines == 0 && (int(binary.LittleEndian.Uint16(raw[8:10])) != (1+bytes.Count(body, []byte{hardReturnByte}))*200 ||
			raw[10] != 0 || raw[11] != 0) {
			return Note{}, false
		}
	} else {
		if raw[header-2] != 0x13 || raw[header-1] != 0x8f {
			return Note{}, false
		}
		for i := 8; i < header-2; i++ {
			if !end && (i == 8 && raw[i] == 200 || i == 12 || i == 13) {
				continue
			}
			if raw[i] != 0 {
				return Note{}, false
			}
		}
	}
	note.Text = string(body)
	return note, true
}

func sameRecordTrailer(raw []byte, stop int) bool {
	return int(binary.LittleEndian.Uint16(raw[stop:stop+2])) == stop && raw[stop+2] == raw[1]
}

func noteOwner(note Note, previousHeight uint16) []byte {
	raw := make([]byte, 19)
	raw[0] = 0xd6
	if note.End {
		raw = raw[:11]
		raw[1] = 1
	} else {
		raw[8] = 200
		binary.LittleEndian.PutUint16(raw[12:14], previousHeight)
	}
	binary.LittleEndian.PutUint16(raw[5:7], uint16(note.Number))
	raw[len(raw)-2], raw[len(raw)-1] = 0x13, 0x8f
	if !note.End && strings.Contains(note.Text, "\n") {
		rows := 1 + strings.Count(note.Text, "\n")
		binary.LittleEndian.PutUint16(raw[8:10], uint16(rows*200))
		// DOS stores a generated display value here. Use the ordinary
		// one-line initialized value; the rendered note text is independent.
	}
	raw = append(raw, 0x8d)
	raw = append(raw, note.Text...)
	length := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(length))
	return append(raw, byte(length), byte(length>>8), raw[1], 0xd6)
}

func (d *Document) InsertNote(c Cursor, text string, end bool, pageStart int) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if pageStart < 0 || pageStart > c.gap {
		return unchangedEdit(d, c), failure(InvalidPosition, pageStart, noSpan)
	}
	number, footnotes := 1, 0
	for i := 0; i < d.TokenCount(); i++ {
		token, _ := d.Token(i)
		note, ok := token.Note()
		if !ok || note.End != end {
			continue
		}
		if i >= c.gap {
			return unchangedEdit(d, c), fmt.Errorf("append new notes after existing notes of the same type")
		}
		number++
		if i >= pageStart {
			footnotes++
		}
	}
	height := 0
	if !end && footnotes > 0 {
		height = 400 + 200*footnotes
	}
	raw := noteOwner(Note{Number: number, Text: text, End: end}, uint16(height))
	if _, ok := parseNote(raw); !ok {
		return unchangedEdit(d, c), fmt.Errorf("enter nonempty note lines of up to 60 printable characters")
	}
	return d.editTokens(c, raw)
}

func (d *Document) ReplaceNote(c Cursor, index int, text string) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	token, err := d.Token(index)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	note, ok := token.Note()
	if !ok {
		return unchangedEdit(d, c), failure(UnsupportedBody, index, token.Span)
	}
	if note.Text == text {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	note.Text = text
	previousHeight := uint16(0)
	if !note.End && note.FirstPageLines == 0 {
		previousHeight = binary.LittleEndian.Uint16(token.Raw[12:14])
	}
	owner := noteOwner(note, previousHeight)
	if _, ok := parseNote(owner); !ok {
		return unchangedEdit(d, c), fmt.Errorf("enter 1 to 60 printable characters for the note")
	}
	raw := d.state.image.Export()
	body := append([]byte(nil), raw[d.state.gaps[0]:token.Span.Offset]...)
	body = append(body, owner...)
	body = append(body, raw[token.Span.Offset+token.Span.Length:]...)
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
	}
	return d.publishEveryday(c, body, d.TokenCount(), c.gap, mapping, blockFormatEdit)
}

func noteDisplay(kind Kind, raw []byte, reveal bool) string {
	note, ok := (Token{Kind: kind, Raw: raw}).Note()
	if !ok {
		return ""
	}
	if !reveal {
		return strconv.Itoa(note.Number)
	}
	label := "Footnote"
	if note.End {
		label = "Endnote"
	}
	return fmt.Sprintf("[%s:%d;[Note Num]%s]", label, note.Number, strings.ReplaceAll(note.Text, "\n", "[HRt]"))
}

func noteSplitHeight(total, first int) int {
	if total-first == first {
		return total * 200
	}
	return (first + 1) * 200
}

func reflowNoteOwner(note Note, prior []byte, change ReflowChange) ([]byte, error) {
	rows := strings.Split(note.Text, "\n")
	split := int(change.NoteLines)
	if split >= len(rows) {
		return nil, fmt.Errorf("footnote continuation has no following text")
	}
	raw := noteOwner(note, 0)
	if note.FirstPageLines > 0 {
		copy(raw[17:19], prior[19:21])
	} else {
		copy(raw[17:19], prior[17:19])
	}
	if split == 0 {
		return raw, nil
	}
	raw = append(bytes.Clone(raw[:17]), 0, 0, raw[17], raw[18], 0x8d)
	raw[7] = 1
	binary.LittleEndian.PutUint16(raw[8:10], uint16(split*200))
	binary.LittleEndian.PutUint16(raw[10:12], uint16((len(rows)-split)*200))
	binary.LittleEndian.PutUint16(raw[12:14], uint16(noteSplitHeight(len(rows), split)))
	raw = append(raw, strings.Join(rows[:split], "\n")...)
	height := 13200 - int(change.NoteTop) - int(change.NoteBottom)
	page := customPageRecord(change.NotePage, uint16(height-200), change.NoteTop, change.NoteBottom)
	page[14] = 1
	raw = append(raw, page...)
	raw = append(raw, hardReturnPageByte)
	raw = append(raw, strings.Join(rows[split:], "\n")...)
	n := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(n))
	return append(raw, byte(n), byte(n>>8), 0, 0xd6), nil
}
