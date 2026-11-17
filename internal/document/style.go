package document

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strings"

	"github.com/lynncoleart/wordling/internal/wp51"
)

type NamedStyle struct {
	Name              string
	ID                uint16
	OnCache, OffCache uint16
}

const firstStylePacket = 257
const maxNamedStyles = 32

func validStyleName(name string) bool {
	if len(name) == 0 || len(name) > 12 || strings.TrimSpace(name) != name {
		return false
	}
	for _, c := range []byte(name) {
		if c < 32 || c > 126 {
			return false
		}
	}
	return true
}

// The captured paired Bold style has one three-byte formatting code in
// each half. DOS varies the two cache words across names. Retain them
// on loaded styles; a new definition starts with unset caches.
func stylePacket(style NamedStyle) []byte {
	p := make([]byte, 94)
	copy(p, style.Name)
	p[21] = 1
	p[77] = 1
	p[78] = 3
	binary.LittleEndian.PutUint16(p[80:82], style.OnCache)
	binary.LittleEndian.PutUint16(p[84:86], style.OffCache)
	p[86] = 3
	copy(p[88:], []byte{0xc3, 0x0c, 0xc3, 0xc4, 0x0c, 0xc4})
	return p
}

func parseNamedStyle(p []byte, id uint16) (NamedStyle, bool) {
	if len(p) != 94 {
		return NamedStyle{}, false
	}
	stop := bytes.IndexByte(p[:13], 0)
	if stop < 0 {
		return NamedStyle{}, false
	}
	name := string(p[:stop])
	if !validStyleName(name) {
		return NamedStyle{}, false
	}
	style := NamedStyle{Name: name, ID: id, OnCache: binary.LittleEndian.Uint16(p[80:82]), OffCache: binary.LittleEndian.Uint16(p[84:86])}
	expected := stylePacket(style)
	expected[77] = p[77] // current use count on DOS save
	if !bytes.Equal(p, expected) {
		return NamedStyle{}, false
	}
	return style, true
}

func (d *Document) NamedStyles() []NamedStyle {
	if !d.valid() {
		return nil
	}
	var result []NamedStyle
	for _, p := range d.state.image.Inspect().Packets {
		if p.Type < firstStylePacket || p.Type >= firstStylePacket+maxNamedStyles {
			continue
		}
		body, _ := d.state.image.Bytes(p.Data)
		if style, ok := parseNamedStyle(body, p.Type); ok {
			result = append(result, style)
		}
	}
	return result
}

func styleBodyOwner(style NamedStyle, off bool) []byte {
	var raw []byte
	if off {
		raw = make([]byte, 22)
		raw[1] = 1
		binary.LittleEndian.PutUint16(raw[10:12], style.ID)
		binary.LittleEndian.PutUint16(raw[20:22], style.OffCache)
	} else {
		raw = make([]byte, 16)
		binary.LittleEndian.PutUint16(raw[12:14], style.ID)
		binary.LittleEndian.PutUint16(raw[14:16], style.OnCache)
	}
	raw[0] = 0xdb
	raw = append(raw, style.Name...)
	raw = append(raw, 0)
	n := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(n))
	return append(raw, byte(n), byte(n>>8), raw[1], 0xdb)
}

var styleBodyEnd = [...]byte{0xdb, 3, 5, 0, 0, 5, 0, 3, 0xdb}

func decodeStyleOwner(raw []byte) (NamedStyle, bool) {
	if len(raw) < 21 || raw[0] != 0xdb || raw[1] > 1 {
		return NamedStyle{}, false
	}
	width, field := 16, 12
	if raw[1] == 1 {
		width, field = 22, 10
	}
	end := len(raw) - 5
	if end <= width {
		return NamedStyle{}, false
	}
	style := NamedStyle{Name: string(raw[width:end]), ID: binary.LittleEndian.Uint16(raw[field : field+2])}
	if !validStyleName(style.Name) || style.ID < firstStylePacket || style.ID >= firstStylePacket+maxNamedStyles {
		return NamedStyle{}, false
	}
	if raw[1] == 1 {
		style.OffCache = binary.LittleEndian.Uint16(raw[20:22])
	} else {
		style.OnCache = binary.LittleEndian.Uint16(raw[14:16])
	}
	return style, bytes.Equal(raw, styleBodyOwner(style, raw[1] == 1))
}

func (d *Document) CreateNamedStyle(c Cursor, name string) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if _, present := d.InitialLineSpacing(); present {
		return unchangedEdit(d, c), failure(UnsupportedPrefix, -1, d.state.initialCodes)
	}
	if !validStyleName(name) {
		return unchangedEdit(d, c), fmt.Errorf("enter a style name of 1 to 12 printable characters")
	}
	styles := d.NamedStyles()
	if len(styles) >= maxNamedStyles {
		return unchangedEdit(d, c), fmt.Errorf("too many named styles")
	}
	for _, s := range styles {
		if strings.EqualFold(s.Name, name) {
			return unchangedEdit(d, c), fmt.Errorf("Style name already exists")
		}
	}
	styles = append(styles, NamedStyle{Name: name, ID: firstStylePacket + uint16(len(styles))})
	info := d.state.image.Inspect()
	raw := d.state.image.Export()
	prefix := styledPrefix(d, styles)
	next, err := parseRevision(append(prefix, raw[info.Body.Offset:]...), d.state.birth)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	if err = next.CheckMutation(); err != nil {
		return unchangedEdit(d, c), err
	}
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
	}
	cursor := c
	cursor.state = next.state
	return EditResult{Document: next, Cursor: cursor, Changed: true, everyday: &everydayReceipt{before: d.state, after: next.state, cursor: cursor, changed: true, kind: blockFormatEdit, tokenMap: mapping}}, nil
}

func (d *Document) ApplyNamedStyle(c Cursor, style NamedStyle) (EditResult, error) {
	found := false
	for _, s := range d.NamedStyles() {
		found = found || s == style
	}
	if !found {
		return unchangedEdit(d, c), fmt.Errorf("style is not defined in this document")
	}
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	active := false
	for i := 0; i < c.gap; i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case StyleOn:
			active = true
		case StyleOff:
			active = false
		}
	}
	t, _ := d.Token(c.gap)
	if active || t.Kind == StyleOff {
		return unchangedEdit(d, c), fmt.Errorf("finish the current style before applying another")
	}
	raw := append(styleBodyOwner(style, false), 0xc3, 0x0c, 0xc3)
	raw = append(raw, styleBodyEnd[:]...)
	raw = append(raw, styleBodyOwner(style, true)...)
	raw = append(raw, 0xc4, 0x0c, 0xc4)
	raw = append(raw, styleBodyEnd[:]...)
	return d.insertNamedTokensAt(c, raw, 6, 3)
}

func (d *Document) AtStyleEnd(c Cursor) bool {
	t, err := d.Token(c.gap)
	return err == nil && t.Kind == StyleOff
}

// A compact styled image uses the usual resource entries, followed by
// definition packets and the final type 8 entry. No bundled style-library
// payload is required. A loaded styled image retains its own bytes.
func styledPrefix(d *Document, styles []NamedStyle) []byte {
	info := d.state.image.Inspect()
	type entry struct {
		kind uint16
		data []byte
	}
	var entries []entry
	var graphics []byte
	existingStyles := make(map[uint16][]byte, len(styles))
	for _, p := range info.Packets {
		body, _ := d.state.image.Bytes(p.Data)
		switch p.Type {
		case 1, 6, 7, 12, 15:
			entries = append(entries, entry{p.Type, body})
		case 8:
			graphics = body
		default:
			if p.Type >= firstStylePacket && p.Type < firstStylePacket+maxNamedStyles {
				existingStyles[p.Type] = body
			}
		}
	}
	for _, s := range styles {
		body, ok := existingStyles[s.ID]
		if !ok {
			body = stylePacket(s)
		}
		entries = append(entries, entry{s.ID, body})
	}
	entries = append(entries, entry{8, graphics})
	// Keep the first index at 16 and emit each next index before
	// writing the data owned by its entries.
	head, _ := d.state.image.Bytes(wp51.Span{Offset: 0, Length: 16})
	raw := bytes.Clone(head)
	last := -1
	for i := 0; i < len(entries); i += 4 {
		at := len(raw)
		raw = append(raw, make([]byte, 50)...)
		writeFastSaveBlock(raw, at, 0)
		if last >= 0 {
			binary.LittleEndian.PutUint32(raw[last+6:last+10], uint32(at))
		}
		last = at
		for j, p := range entries[i:min(i+4, len(entries))] {
			writeFastSaveEntry(raw, at+10*(j+1), fastSaveEntry{p.kind, len(raw), len(p.data)})
			raw = append(raw, p.data...)
		}
	}
	binary.LittleEndian.PutUint32(raw[4:8], uint32(len(raw)))
	return raw
}

// For the isolated compact DOS profile, revalidate the base packets via
// the existing compact admission path. Compare the complete styled graph
// separately, including every block and extent; unknown packets stay opaque.
func (d *Document) stylePrefixAdmission(info wp51.Inspection) (int, bool, error) {
	styles := d.NamedStyles()
	if len(styles) == 0 {
		return 0, false, nil
	}
	refuse := func() (int, bool, error) { return 0, true, failure(UnsupportedPrefix, -1, info.Prefix) }
	if len(info.Packets) != 5+len(styles) && len(info.Packets) != 6+len(styles) {
		return refuse()
	}
	seen := map[string]bool{}
	for i, s := range styles {
		key := strings.ToUpper(s.Name)
		if s.ID != firstStylePacket+uint16(i) || seen[key] {
			return refuse()
		}
		seen[key] = true
	}
	flags := -1
	live := map[uint16][]byte{}
	for _, p := range info.Packets {
		if p.Type >= firstStylePacket {
			continue
		}
		if p.Type == 6 {
			flags = p.Data.Offset
		}
		if _, ok := live[p.Type]; ok {
			return refuse()
		}
		live[p.Type], _ = d.state.image.Bytes(p.Data)
	}
	if flags < 0 || len(live[6]) != 16 || len(live[15]) != 86 || len(live[7]) != 14 || len(live[12]) != 90 || len(live[8]) != 2 {
		return refuse()
	}
	// Compaction is only a validation view. No bytes from it replace
	// the loaded styled file.
	base, err := parseRevision(compactFastSaveCandidate(d.state.image, live), d.state.birth)
	if err != nil {
		return refuse()
	}
	if _, err = base.prefixMutationAdmission(); err != nil {
		return 0, true, err
	}
	original, _ := d.state.image.Bytes(info.Prefix)
	expected := styledPrefix(d, styles)
	if len(original) != len(expected) {
		return refuse()
	}
	if !bytes.Equal(original, expected) {
		return refuse()
	}
	return flags, true, nil
}
