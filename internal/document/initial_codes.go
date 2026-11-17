package document

import (
	"encoding/binary"

	"github.com/lynncoleart/wordling/internal/wp51"
)

const initialCodesPacket = 3

// InitialLineSpacing reports the setting in the DOS Initial Codes packet.
// Zero with a present packet means its contents are outside the supported
// profile. With no packet, the Standard Printer default is one.
func (d *Document) InitialLineSpacing() (spacing int, present bool) {
	if !d.valid() || d.state.initialCodes.Offset == 0 {
		return 1, false
	}
	return d.state.initialSpacing, true
}

func initialSpacingValue(raw []byte) int {
	if spacingKind(raw) && raw[5] == 1 && (raw[7] == 1 || raw[7] == 2) {
		return int(raw[7])
	}
	return 0
}

// SetInitialLineSpacing preserves the body and rewrites only the captured
// Initial Codes graph. Returning to single spacing keeps the native owner.
func (d *Document) SetInitialLineSpacing(c Cursor, spacing int) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if spacing != 1 && spacing != 2 {
		return unchangedEdit(d, c), failure(UnsupportedMetadata, -1, noSpan)
	}
	oldSpacing, present := d.InitialLineSpacing()
	if present && oldSpacing == spacing {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	info := d.state.image.Inspect()
	raw := d.state.image.Export()
	if present {
		raw[d.state.initialCodes.Offset+7] = byte(spacing)
	} else {
		// DOS puts its new packet in the first block's last slot, shifting
		// Document State to the second block after the packet payload.
		if len(info.Blocks) != 2 || len(info.Packets) != 5 ||
			info.Packets[2].Type != 12 || info.Packets[3].Type != 6 {
			return unchangedEdit(d, c), failure(UnsupportedPrefix, -1, info.Prefix)
		}
		first, last := info.Blocks[0].Data.Offset, info.Blocks[1].Data.Offset
		state, graphics := info.Packets[3].Data, info.Packets[4].Data
		printer := info.Packets[2].Data
		if printer.Offset+printer.Length != state.Offset || state.Offset+state.Length != last ||
			graphics.Offset != last+50 || len(raw)+12 > MaxMutationBytes {
			return unchangedEdit(d, c), failure(UnsupportedPrefix, -1, info.Prefix)
		}
		at := state.Offset
		owner := []byte{0xd0, 2, 8, 0, 0, 1, 0, byte(spacing), 8, 0, 2, 0xd0}
		candidate := make([]byte, 0, len(raw)+len(owner))
		candidate = append(candidate, raw[:at]...)
		candidate = append(candidate, owner...)
		newLast := len(candidate)
		candidate = append(candidate, raw[last:last+50]...)
		candidate = append(candidate, raw[at:last]...)
		newGraphics := len(candidate)
		candidate = append(candidate, raw[graphics.Offset:]...)
		binary.LittleEndian.PutUint32(candidate[4:], uint32(newGraphics+graphics.Length))
		binary.LittleEndian.PutUint32(candidate[first+6:], uint32(newLast))
		writeFastSaveEntry(candidate, info.Packets[3].Index.Offset, fastSaveEntry{initialCodesPacket, at, len(owner)})
		writeFastSaveEntry(candidate, newLast+10, fastSaveEntry{6, newLast + 50, state.Length})
		writeFastSaveEntry(candidate, newLast+20, fastSaveEntry{8, newGraphics, graphics.Length})
		raw = candidate
	}
	next, err := parseRevision(raw, d.state.birth)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	if err := next.CheckMutation(); err != nil {
		return unchangedEdit(d, c), err
	}
	next.state.openWordRestore = d.state.openWordRestore
	cursor := c
	cursor.state = next.state
	tokenMap := make([]int, d.TokenCount())
	for i := range tokenMap {
		tokenMap[i] = i
	}
	return EditResult{Document: next, Cursor: cursor, Changed: true, everyday: &everydayReceipt{
		before: d.state, after: next.state, cursor: cursor, changed: true, kind: blockFormatEdit, tokenMap: tokenMap,
	}}, nil
}

// ExportInitialCodesSave retains the type 3 packet on F10. A loaded compact
// document with changed Initial Codes has a captured Fast Save generation.
func (d *Document) ExportInitialCodesSave(fast bool) ([]byte, error) {
	flags, err := d.mutationAdmission()
	if err != nil {
		return nil, err
	}
	if _, present := d.InitialLineSpacing(); !present {
		return nil, failure(UnsupportedMetadata, -1, wp51.Span{Offset: flags, Length: 1})
	}
	if d.Birth().IsLoaded() {
		live := fastSaveLivePackets(d.state.image)
		if !fast {
			return compactInitialCodes(d.state.image, live), nil
		}
		original := d.state.birth.originalImage
		prior := fastSaveLivePackets(original)
		entries := original.Inspect().Packets
		if len(entries) == 6 && entries[0].Type == 7 && entries[3].Type == initialCodesPacket &&
			entries[3].Data.Offset == 256 && initialSpacingValue(prior[initialCodesPacket]) != 0 &&
			len(prior[6]) == 16 &&
			string(live[initialCodesPacket]) != string(prior[initialCodesPacket]) &&
			checkFastSaveResources(live, prior, original.Inspect().Prefix) == nil {
			return d.exportChangedInitialCodes(live, prior)
		}
	}
	raw := d.state.image.Export()
	raw[flags] &^= 8
	return raw, nil
}
