package document

import (
	"bytes"
	"encoding/binary"

	"github.com/lynncoleart/wordling/internal/wp51"
)

const fastSavePrefixBytes = 564
const compactFastSavePrefixBytes = 324

// CompactFastSave reproduces the observed Fast Save No rewrite for the
// Standard Printer Fast Save shapes. It returns a separate revision with the
// original acquisition retained as its birth. Ordinary Export remains exact.
func (d *Document) CompactFastSave() (*Document, error) {
	if !d.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	info := d.state.image.Inspect()
	refuse := func() (*Document, error) {
		return nil, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	if info.Body.Offset != fastSavePrefixBytes || len(info.Blocks) != 3 || len(info.Packets) != 9 {
		return refuse()
	}
	if info.Body.Offset+info.Body.Length > MaxMutationBytes || d.TokenCount() > MaxMutationTokens {
		return nil, failure(MutationLimit, -1, info.Body)
	}

	// Both observed graphs account for every prefix byte. The middle block
	// moves by two bytes when the original replaces its live resource packets.
	first, middle, last := info.Blocks[0], info.Blocks[1], info.Blocks[2]
	if first != (wp51.Block{Data: wp51.Span{Offset: 16, Length: 50}, Count: 5, Next: uint32(middle.Data.Offset)}) ||
		middle.Data.Length != 50 || middle.Count != 5 || middle.Next != 512 ||
		last != (wp51.Block{Data: wp51.Span{Offset: 512, Length: 50}, Count: 5}) {
		return refuse()
	}
	type entry struct {
		kind   uint16
		offset int
		size   int
	}
	const deleted = 0xffff
	var expected []entry
	switch middle.Data.Offset {
	case 270:
		expected = []entry{
			{deleted, 66, 14}, {6, 80, 16}, {deleted, 166, 90}, {7, 256, 14},
			{15, 320, 86}, {12, 406, 90}, {deleted, 496, 16}, {deleted, 96, 70},
			{8, 562, 2},
		}
	case 272:
		expected = []entry{
			{deleted, 66, 14}, {6, 80, 16}, {deleted, 166, 90}, {deleted, 256, 16},
			{7, 322, 14}, {15, 336, 86}, {12, 422, 90}, {deleted, 96, 70},
			{8, 562, 2},
		}
	default:
		return refuse()
	}

	raw := d.state.image.Export()
	if !bytes.Equal(raw[532:562], make([]byte, 30)) {
		return refuse()
	}
	payload := make(map[uint16][]byte, 5)
	var priorState []byte
	for i, packet := range info.Packets {
		want := expected[i]
		block := info.Blocks[i/4]
		index := block.Data.Offset + 10*(i%4+1)
		if packet.Type != want.kind || packet.Index != (wp51.Span{Offset: index, Length: 10}) ||
			packet.Data != (wp51.Span{Offset: want.offset, Length: want.size}) {
			return refuse()
		}
		data := raw[packet.Data.Offset : packet.Data.Offset+packet.Data.Length]
		if packet.Type != deleted {
			payload[packet.Type] = data
		} else if packet.Data.Length == 16 {
			priorState = data
		}
	}
	// The discarded entries must be the witnessed retired copies of live
	// pool, printer and font data and the prior document state. Refuse a
	// different residual rather than infer that arbitrary bytes are obsolete.
	if !bytes.Equal(raw[66:80], payload[7]) ||
		!bytes.Equal(raw[166:256], payload[12]) ||
		!bytes.Equal(raw[96:166], payload[15][16:]) ||
		!bytes.Equal(priorState[1:], payload[6][1:]) ||
		(priorState[0] != 0 && priorState[0] != 8) ||
		(payload[6][0] != 0 && payload[6][0] != 8) {
		return refuse()
	}

	candidate := make([]byte, compactFastSavePrefixBytes+info.Body.Length)
	copy(candidate, raw[:16])
	binary.LittleEndian.PutUint32(candidate[4:], compactFastSavePrefixBytes)
	writeIndex := func(offset int, kind uint16, size, dataOffset int) {
		binary.LittleEndian.PutUint16(candidate[offset:], kind)
		binary.LittleEndian.PutUint32(candidate[offset+2:], uint32(size))
		binary.LittleEndian.PutUint32(candidate[offset+6:], uint32(dataOffset))
	}
	// Each FFFB root is a five-slot, 50-byte block. Type 8 stays last.
	for _, block := range [...]struct{ offset, next int }{{16, 272}, {272, 0}} {
		binary.LittleEndian.PutUint16(candidate[block.offset:], 0xfffb)
		binary.LittleEndian.PutUint16(candidate[block.offset+2:], 5)
		binary.LittleEndian.PutUint16(candidate[block.offset+4:], 50)
		binary.LittleEndian.PutUint32(candidate[block.offset+6:], uint32(block.next))
	}
	position := 66
	for i, kind := range [...]uint16{6, 7, 15, 12, 8} {
		index := 26 + 10*i
		if kind == 8 {
			position = 322
			index = 282
		}
		data := payload[kind]
		writeIndex(index, kind, len(data), position)
		copy(candidate[position:], data)
		position += len(data)
	}
	// DOS clears the pending-format bit on this rewrite even after a
	// no-edit Save As. The existing mutation path sets it on later edits.
	candidate[66] &^= 8
	copy(candidate[compactFastSavePrefixBytes:], raw[info.Body.Offset:])

	compact, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return nil, err
	}
	if err := compact.CheckMutation(); err != nil {
		return nil, err
	}
	return compact, nil
}
