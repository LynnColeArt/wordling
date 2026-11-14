package document

import "encoding/binary"

func (d *Document) BindingOffset() int {
	if !d.valid() {
		return 0
	}
	var offset int
	for _, packet := range d.state.image.Inspect().Packets {
		if packet.Type == 6 && packet.Data.Length == 16 {
			raw, _ := d.state.image.Bytes(packet.Data)
			offset = int(binary.LittleEndian.Uint16(raw[6:8]))
		}
	}
	return offset
}

func (d *Document) SetBindingOffset(c Cursor, units int) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if units < 0 || units > UnitsPerInch {
		return unchangedEdit(d, c), failure(UnsupportedMetadata, -1, noSpan)
	}
	if units == d.BindingOffset() {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchangedEdit(d, c), err
	}
	raw := d.state.image.Export()
	binary.LittleEndian.PutUint16(raw[flags+6:flags+8], uint16(units))
	next, err := parseRevision(raw, d.state.birth)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	cursor := Cursor{state: next.state, gap: c.gap, reveal: c.reveal}
	mapping := make([]int, d.TokenCount())
	for i := range mapping {
		mapping[i] = i
	}
	return EditResult{Document: next, Cursor: cursor, Changed: true, everyday: &everydayReceipt{
		before: d.state, after: next.state, cursor: cursor, changed: true, kind: blockFormatEdit, tokenMap: mapping,
	}}, nil
}
