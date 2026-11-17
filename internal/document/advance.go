package document

import (
	"bytes"
	"encoding/binary"
	"strconv"
)

type AdvanceMode byte

const (
	AdvanceDown     AdvanceMode = iota
	AdvanceRight    AdvanceMode = 2
	AdvancePosition AdvanceMode = 3
)

func (m AdvanceMode) label() string {
	switch m {
	case AdvanceDown:
		return "AdvDn"
	case AdvanceRight:
		return "AdvRgt"
	case AdvancePosition:
		return "AdvToPos"
	}
	return ""
}

func advanceOwner(raw []byte) bool {
	return len(raw) == 13 && raw[0] == 0xd3 && raw[1] == 6 &&
		raw[2] == 9 && raw[3] == 0 && AdvanceMode(raw[4]).label() != "" &&
		raw[9] == 9 && raw[10] == 0 && raw[11] == 6 && raw[12] == 0xd3
}

// Advance reports the requested distance or absolute position in formatter units.
func (t Token) Advance() (AdvanceMode, int, bool) {
	if t.Kind != AdvanceCode {
		return 0, 0, false
	}
	mode := AdvanceMode(t.Raw[4])
	return mode, int(binary.LittleEndian.Uint16(t.Raw[7:9])), true
}

func advanceLabel(raw []byte) string {
	t := Token{Kind: AdvanceCode, Raw: raw}
	mode, units, _ := t.Advance()
	return "[" + mode.label() + ":" + strconv.FormatFloat(float64(units)/UnitsPerInch, 'f', -1, 64) + "\"]"
}

func (d *Document) InsertAdvance(c Cursor, mode AdvanceMode, prior, value int) (EditResult, error) {
	if mode.label() == "" || prior < 0 || prior > 65535 || value < 0 || value > 65535 {
		return unchangedEdit(d, c), failure(UnsupportedBody, c.gap, noSpan)
	}
	raw := []byte{0xd3, 6, 9, 0, byte(mode), 0, 0, 0, 0, 9, 0, 6, 0xd3}
	binary.LittleEndian.PutUint16(raw[5:], uint16(prior))
	binary.LittleEndian.PutUint16(raw[7:], uint16(value))
	return d.editTokens(c, raw)
}

// HasAdvance reports whether the body contains any supported Advance records.
func (d *Document) HasAdvance() bool {
	for i := 0; i < d.TokenCount(); i++ {
		token, err := d.Token(i)
		if err == nil && token.Kind == AdvanceCode {
			return true
		}
	}
	return false
}

// ExportReopenedAdvanceSaveAs refreshes the Fast Save index for a reopened
// Advance document in the observed earlier packet layout. A nil result
// lets the caller preserve the acquired image when the graph is outside
// the checked Fast Save writer's scope.
func (d *Document) ExportReopenedAdvanceSaveAs() []byte {
	if !d.valid() || !d.Birth().IsLoaded() {
		return nil
	}
	original := d.state.birth.originalImage
	birth := original.Inspect()
	if birth.Prefix.Length != fastSavePrefixBytes || len(birth.Blocks) != 3 ||
		birth.Blocks[1].Data.Offset != 270 || d.state.image.Inspect().Prefix.Length != compactFastSavePrefixBytes ||
		!d.HasAdvance() {
		return nil
	}
	raw, err := d.ExportFastSave()
	if err != nil || binary.LittleEndian.Uint32(raw[4:8]) != fastSavePrefixBytes {
		return nil
	}
	body, _ := original.Bytes(birth.Body)
	if !bytes.Equal(raw[fastSavePrefixBytes:], body) {
		return nil
	}
	return raw
}

// ExportFreshAdvanceSave writes the formatted, original-order compact prefix
// seen in the fresh Advance captures.
func (d *Document) ExportFreshAdvanceSave() ([]byte, error) {
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return nil, err
	}
	raw, err := d.Export()
	if err != nil {
		return nil, err
	}
	raw[flags] &^= 8
	return raw, nil
}
