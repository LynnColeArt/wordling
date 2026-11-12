package document

import (
	"bytes"
	"encoding/binary"

	"github.com/lynncoleart/wordling/internal/wp51"
)

const fastSavePrefixBytes = 564
const compactFastSavePrefixBytes = 324
const compactFastSaveStateOffset = 66

// CompactFastSave reproduces the observed Fast Save No rewrite for the
// Standard Printer Fast Save shapes. It returns a separate revision with the
// original acquisition retained as its birth. Ordinary Export remains exact.
func (d *Document) CompactFastSave() (*Document, error) {
	compact, err := d.compactFastSavePrefix()
	if err != nil {
		return nil, err
	}
	if err := compact.checkFastSaveMutation(); err != nil {
		return nil, err
	}
	return compact, nil
}

func (d *Document) compactFastSavePrefix() (*Document, error) {
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
	expected := fastSaveEntries(middle.Data.Offset)
	if expected == nil {
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
		if packet.Type != retiredFastSavePacket {
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

	return parseRevision(compactFastSaveCandidate(d.state.image, payload), d.state.birth)
}

func compactFastSaveCandidate(image *wp51.Image, payload map[uint16][]byte) []byte {
	info := image.Inspect()
	candidate := make([]byte, compactFastSavePrefixBytes+info.Body.Length)
	header, _ := image.Bytes(wp51.Span{Offset: 0, Length: 16})
	copy(candidate, header)
	binary.LittleEndian.PutUint32(candidate[4:], compactFastSavePrefixBytes)
	// Each FFFB root is a five-slot, 50-byte block. Type 8 stays last.
	writeFastSaveBlock(candidate, 16, 272)
	writeFastSaveBlock(candidate, 272, 0)
	position := compactFastSaveStateOffset
	for i, kind := range [...]uint16{6, 7, 15, 12, 8} {
		index := 26 + 10*i
		if kind == 8 {
			position = 322
			index = 282
		}
		data := payload[kind]
		writeFastSaveEntry(candidate, index, fastSaveEntry{kind, position, len(data)})
		copy(candidate[position:], data)
		position += len(data)
	}
	// DOS clears the pending-format bit when it reformats the document.
	candidate[compactFastSaveStateOffset] &^= 8
	body, _ := image.Bytes(info.Body)
	copy(candidate[compactFastSavePrefixBytes:], body)
	return candidate
}

func (d *Document) checkFastSaveMutation() error {
	err := d.CheckMutation()
	if err == nil || d.CheckMergeSource() == nil {
		return nil
	}
	return err
}

const retiredFastSavePacket = 0xffff

type fastSaveEntry struct {
	kind   uint16
	offset int
	size   int
}

func fastSaveEntries(middle int) []fastSaveEntry {
	const retired = retiredFastSavePacket
	switch middle {
	case 270:
		return []fastSaveEntry{
			{retired, 66, 14}, {6, 80, 16}, {retired, 166, 90}, {7, 256, 14},
			{15, 320, 86}, {12, 406, 90}, {retired, 496, 16}, {retired, 96, 70},
			{8, 562, 2},
		}
	case 272:
		return []fastSaveEntry{
			{retired, 66, 14}, {6, 80, 16}, {retired, 166, 90}, {retired, 256, 16},
			{7, 322, 14}, {15, 336, 86}, {12, 422, 90}, {retired, 96, 70},
			{8, 562, 2},
		}
	default:
		return nil
	}
}

func writeFastSaveBlock(raw []byte, offset, next int) {
	binary.LittleEndian.PutUint16(raw[offset:], 0xfffb)
	binary.LittleEndian.PutUint16(raw[offset+2:], 5)
	binary.LittleEndian.PutUint16(raw[offset+4:], 50)
	binary.LittleEndian.PutUint32(raw[offset+6:], uint32(next))
}

func writeFastSaveEntry(raw []byte, index int, entry fastSaveEntry) {
	binary.LittleEndian.PutUint16(raw[index:], entry.kind)
	binary.LittleEndian.PutUint32(raw[index+2:], uint32(entry.size))
	binary.LittleEndian.PutUint32(raw[index+6:], uint32(entry.offset))
}

// ExportFastSave encodes the checked edited body with the original Fast Save
// Yes index generation for its loaded acquisition. A fresh New document uses
// its ordinary compact image. Callers retain the exact acquired/published
// bytes for an unchanged Save rather than invoking this edited-output path.
func (d *Document) ExportFastSave() ([]byte, error) {
	if err := d.checkFastSaveMutation(); err != nil {
		return nil, err
	}
	if d.Birth().IsNew() {
		return d.Export()
	}
	return d.exportLoadedFastSave(d.CheckMergeSource() == nil, false)
}

// ExportCompactFastSave writes the observed pre-print Standard Printer graph.
// Fast Save Yes retains the pending-format bit after a successful purge.
func (d *Document) ExportCompactFastSave(fastSave bool) ([]byte, error) {
	if err := d.CheckMutation(); err != nil {
		return nil, err
	}
	image := d.state.image
	live := fastSaveLivePackets(image)
	if !prePrintFastSaveResources(live) {
		return d.Export()
	}
	return compactFastSaveResult(image, live, fastSave), nil
}

func compactFastSaveResult(image *wp51.Image, live map[uint16][]byte, preserveFormatState bool) []byte {
	candidate := compactFastSaveCandidate(image, live)
	if preserveFormatState {
		candidate[compactFastSaveStateOffset] |= live[6][0] & 8
	}
	return candidate
}

// exportLoadedFastSave uses the loaded receiver's original packet graph.
// Native merge edits witnessed by DOS mark the live state as unformatted.
func (d *Document) exportLoadedFastSave(markActive, formatted bool) ([]byte, error) {
	image := d.state.birth.originalImage
	info := image.Inspect()
	original, err := parseRevision(image.Export(), d.state.birth)
	if err != nil {
		return nil, err
	}
	middle := 272
	switch info.Prefix.Length {
	case compactFastSavePrefixBytes:
		if err := original.checkFastSaveMutation(); err != nil {
			return nil, err
		}
		// These two compact sources have the same owners but produce
		// different generations on the next loaded save in DOS.
		entries := info.Packets
		if info.Blocks[1].Data.Offset != 272 || entries[4].Data.Offset != 322 {
			return nil, failure(UnsupportedPrefix, -1, info.Prefix)
		}
		offsets := [4]int{66, 82, 96, 182}
		if entries[0].Type == 7 {
			offsets = [4]int{66, 80, 166, 256}
			middle = 270
		}
		for i, offset := range offsets {
			if entries[i].Data.Offset != offset {
				return nil, failure(UnsupportedPrefix, -1, info.Prefix)
			}
		}
	case fastSavePrefixBytes:
		if _, err := original.CompactFastSave(); err != nil {
			return nil, err
		}
	default:
		return nil, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	current := d.state.image
	live := fastSaveLivePackets(current)
	prior := fastSaveLivePackets(image)
	if err := checkFastSaveResources(live, prior, info.Prefix); err != nil {
		return nil, err
	}
	// Ordinary loaded saves retain the acquired unformatted bit. In the
	// original merge-source saves it belongs to the active edited state.
	active := prior[6]
	if markActive {
		active = live[6]
	}
	if formatted {
		active = bytes.Clone(active)
		active[0] &^= 8
	}
	return d.encodeFastSave(live, prior, middle, active)
}

func checkFastSaveResources(live, prior map[uint16][]byte, prefix wp51.Span) error {
	// The witnesses are pre-print default Standard Printer documents.
	// Preserve every resource field and reject a printer-cache transition.
	if !prePrintFastSaveResources(live) || !bytes.Equal(live[6][1:], prior[6][1:]) {
		return failure(UnsupportedResource, -1, prefix)
	}
	for _, kind := range [...]uint16{7, 15, 12, 8} {
		if !bytes.Equal(live[kind], prior[kind]) {
			return failure(UnsupportedResource, -1, prefix)
		}
	}
	return nil
}

func prePrintFastSaveResources(live map[uint16][]byte) bool {
	return live[6][8] == 1 && bytes.Equal(live[15][21:23], []byte{0xe7, 0x24})
}

func (d *Document) encodeFastSave(live, prior map[uint16][]byte, middle int, active []byte) ([]byte, error) {
	current := d.state.image
	bodyInfo := current.Inspect().Body
	if bodyInfo.Length > MaxMutationBytes-fastSavePrefixBytes {
		return nil, failure(MutationLimit, -1, bodyInfo)
	}
	header, _ := current.Bytes(wp51.Span{Offset: 0, Length: 16})
	body, _ := current.Bytes(bodyInfo)
	candidate := make([]byte, fastSavePrefixBytes+len(body))
	copy(candidate, header)
	binary.LittleEndian.PutUint32(candidate[4:], fastSavePrefixBytes)
	writeFastSaveBlock(candidate, 16, middle)
	writeFastSaveBlock(candidate, middle, 512)
	writeFastSaveBlock(candidate, 512, 0)
	blocks := [...]int{16, middle, 512}
	for i, entry := range fastSaveEntries(middle) {
		index := blocks[i/4] + 10*(i%4+1)
		writeFastSaveEntry(candidate, index, entry)
		data := live[entry.kind]
		if entry.kind == 6 {
			data = active
		}
		if entry.kind == retiredFastSavePacket {
			switch entry.size {
			case 14:
				data = prior[7]
			case 16:
				data = prior[6]
			case 70:
				data = prior[15][16:]
			case 90:
				data = prior[12]
			}
		}
		copy(candidate[entry.offset:], data)
	}
	copy(candidate[fastSavePrefixBytes:], body)
	checked, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return nil, err
	}
	if _, err := checked.CompactFastSave(); err != nil {
		return nil, err
	}
	return candidate, nil
}

func fastSaveLivePackets(image *wp51.Image) map[uint16][]byte {
	live := make(map[uint16][]byte, 5)
	for _, packet := range image.Inspect().Packets {
		if packet.Type != retiredFastSavePacket {
			live[packet.Type], _ = image.Bytes(packet.Data)
		}
	}
	return live
}
