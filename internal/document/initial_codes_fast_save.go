package document

import (
	"bytes"
	"encoding/binary"

	"github.com/lynncoleart/wordling/internal/wp51"
)

const initialCodesFastPrefix = 576

// DOS compaction moves Initial Codes and Document State to the front.
func compactInitialCodes(image *wp51.Image, live map[uint16][]byte) []byte {
	const second, bodyOffset = 194, 336
	info := image.Inspect()
	raw := make([]byte, bodyOffset+info.Body.Length)
	header, _ := image.Bytes(wp51.Span{Offset: 0, Length: 16})
	copy(raw, header)
	binary.LittleEndian.PutUint32(raw[4:], bodyOffset)
	writeFastSaveBlock(raw, 16, second)
	writeFastSaveBlock(raw, second, 0)
	for i, entry := range [...]fastSaveEntry{
		{initialCodesPacket, 66, 12}, {6, 78, 16}, {7, 94, 14},
		{15, 108, 86}, {12, 244, 90}, {8, 334, 2},
	} {
		block := [...]int{16, second}[i/4]
		writeFastSaveEntry(raw, block+10*(i%4+1), entry)
		copy(raw[entry.offset:entry.offset+entry.size], live[entry.kind])
	}
	raw[78] &^= 8
	body, _ := image.Bytes(info.Body)
	copy(raw[bodyOffset:], body)
	return raw
}

// Replacing the initial-code owner in the original compact layout retires
// the previous printer, initial codes and state after allocating new slots.
var changedInitialCodesEntries = [...]fastSaveEntry{
	{initialCodesPacket, 66, 12}, {6, 80, 16}, {retiredFastSavePacket, 166, 90}, {7, 256, 14},
	{15, 320, 86}, {12, 406, 90}, {retiredFastSavePacket, 496, 12}, {retiredFastSavePacket, 508, 16},
	{8, 574, 2},
}

var changedInitialCodesBlocks = [...]int{16, 270, 524}

func encodeChangedInitialCodes(image *wp51.Image, live, prior map[uint16][]byte) []byte {
	info := image.Inspect()
	raw := make([]byte, initialCodesFastPrefix+info.Body.Length)
	header, _ := image.Bytes(wp51.Span{Offset: 0, Length: 16})
	copy(raw, header)
	binary.LittleEndian.PutUint32(raw[4:], initialCodesFastPrefix)
	writeFastSaveBlock(raw, 16, 270)
	writeFastSaveBlock(raw, 270, 524)
	writeFastSaveBlock(raw, 524, 0)
	// DOS leaves the unowned tails of the compact pool and font in place.
	copy(raw[78:80], prior[7][12:])
	copy(raw[96:166], prior[15][16:])
	retired := map[int][]byte{166: prior[12], 496: prior[initialCodesPacket], 508: prior[6]}
	for i, entry := range changedInitialCodesEntries {
		index := changedInitialCodesBlocks[i/4] + 10*(i%4+1)
		writeFastSaveEntry(raw, index, entry)
		data := live[entry.kind]
		if entry.kind == retiredFastSavePacket {
			data = retired[entry.offset]
		}
		copy(raw[entry.offset:entry.offset+entry.size], data)
	}
	raw[80] |= 8
	body, _ := image.Bytes(info.Body)
	copy(raw[initialCodesFastPrefix:], body)
	return raw
}

func (d *Document) exportChangedInitialCodes(live, prior map[uint16][]byte) ([]byte, error) {
	if info := d.state.image.Inspect(); info.Body.Length > MaxMutationBytes-initialCodesFastPrefix {
		return nil, failure(MutationLimit, -1, info.Body)
	}
	raw := encodeChangedInitialCodes(d.state.image, live, prior)
	candidate, err := parseRevision(raw, d.state.birth)
	if err != nil {
		return nil, err
	}
	if _, err := candidate.CompactFastSave(); err != nil {
		return nil, err
	}
	return raw, nil
}

func (d *Document) compactInitialCodesFastSave(info wp51.Inspection) (*Document, error) {
	refuse := func() (*Document, error) { return nil, failure(UnsupportedPrefix, -1, info.Prefix) }
	if len(info.Blocks) != len(changedInitialCodesBlocks) || len(info.Packets) != len(changedInitialCodesEntries) {
		return refuse()
	}
	if info.Body.Offset+info.Body.Length > MaxMutationBytes || d.TokenCount() > MaxMutationTokens {
		return nil, failure(MutationLimit, -1, info.Body)
	}
	prior := make(map[uint16][]byte)
	retiredKinds := map[int]uint16{166: 12, 496: initialCodesPacket, 508: 6}
	for i, entry := range changedInitialCodesEntries {
		packet := info.Packets[i]
		if packet.Type != entry.kind || packet.Data != (wp51.Span{Offset: entry.offset, Length: entry.size}) {
			return refuse()
		}
		if kind := retiredKinds[entry.offset]; kind != 0 {
			prior[kind], _ = d.state.image.Bytes(packet.Data)
		}
	}
	live := fastSaveLivePackets(d.state.image)
	prior[7], prior[15] = live[7], live[15]
	if d.state.initialSpacing == 0 || initialSpacingValue(prior[initialCodesPacket]) == 0 ||
		bytes.Equal(prior[initialCodesPacket], live[initialCodesPacket]) ||
		!bytes.Equal(prior[12], live[12]) || !bytes.Equal(prior[6][1:], live[6][1:]) ||
		prior[6][0] != 0 && prior[6][0] != 8 {
		return refuse()
	}
	expected := encodeChangedInitialCodes(d.state.image, live, prior)
	prefix, _ := d.state.image.Bytes(info.Prefix)
	if !bytes.Equal(prefix, expected[:initialCodesFastPrefix]) {
		return refuse()
	}
	return parseRevision(compactInitialCodes(d.state.image, live), d.state.birth)
}
