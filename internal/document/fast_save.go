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
	if info.Prefix.Length == initialCodesFastPrefix && d.state.initialCodes.Offset != 0 {
		return d.compactInitialCodesFastSave(info)
	}
	if archives := nestedMergeArchiveCount(info.Prefix.Length); archives != 0 {
		return d.compactNestedMergePrefix(archives)
	}
	refuse := func() (*Document, error) {
		return nil, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	summarySize := 0
	for _, packet := range info.Packets {
		if packet.Type == 1 {
			summarySize = packet.Data.Length
			break
		}
	}
	prefixSize := fastSavePrefixBytes + summarySize
	lastOffset := 512 + summarySize
	if info.Body.Offset != prefixSize || len(info.Blocks) != 3 || len(info.Packets) != 9 {
		return refuse()
	}
	if info.Body.Offset+info.Body.Length > MaxMutationBytes || d.TokenCount() > MaxMutationTokens {
		return nil, failure(MutationLimit, -1, info.Body)
	}

	// Both observed graphs account for every prefix byte. The middle block
	// moves by two bytes when the original replaces its live resource packets.
	first, middle, last := info.Blocks[0], info.Blocks[1], info.Blocks[2]
	if first != (wp51.Block{Data: wp51.Span{Offset: 16, Length: 50}, Count: 5, Next: uint32(middle.Data.Offset)}) ||
		middle.Data.Length != 50 || middle.Count != 5 || middle.Next != uint32(lastOffset) ||
		last != (wp51.Block{Data: wp51.Span{Offset: lastOffset, Length: 50}, Count: 5}) {
		return refuse()
	}
	expected := fastSaveEntriesWithSummary(middle.Data.Offset, summarySize)
	if expected == nil {
		return refuse()
	}

	raw := d.state.image.Export()
	if !bytes.Equal(raw[lastOffset+20:lastOffset+50], make([]byte, 30)) {
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
	summarySize := len(payload[1])
	prefixSize := compactFastSavePrefixBytes + summarySize
	candidate := make([]byte, prefixSize+info.Body.Length)
	header, _ := image.Bytes(wp51.Span{Offset: 0, Length: 16})
	copy(candidate, header)
	binary.LittleEndian.PutUint32(candidate[4:], uint32(prefixSize))
	// Each FFFB root is a five-slot, 50-byte block. Type 8 stays last.
	writeFastSaveBlock(candidate, 16, 272+summarySize)
	writeFastSaveBlock(candidate, 272+summarySize, 0)
	position := compactFastSaveStateOffset
	kinds := []uint16{6, 7, 15, 12, 8}
	if summarySize > 0 {
		kinds = []uint16{6, 7, 15, 12, 1, 8}
	}
	for i, kind := range kinds {
		index := 26 + 10*i
		if i >= 4 {
			index = 282 + summarySize + 10*(i-4)
		}
		if kind == 8 {
			position = 322 + summarySize
		}
		data := payload[kind]
		writeFastSaveEntry(candidate, index, fastSaveEntry{kind, position, len(data)})
		copy(candidate[position:], data)
		position += len(data)
	}
	// DOS clears the pending-format bit when it reformats the document.
	candidate[compactFastSaveStateOffset] &^= 8
	body, _ := image.Bytes(info.Body)
	copy(candidate[prefixSize:], body)
	return candidate
}

func (d *Document) checkFastSaveMutation() error {
	err := d.CheckMutation()
	if _, sheet := d.SpreadsheetTable(); sheet {
		_, err = d.prefixMutationAdmission()
		return err
	}
	if err == nil || d.CheckMergeSource() == nil {
		return nil
	}
	if _, ok := d.SimpleTable(); ok {
		_, err = d.prefixMutationAdmission()
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

func fastSaveEntriesWithSummary(middle, size int) []fastSaveEntry {
	entries := fastSaveEntries(middle)
	if size == 0 {
		return entries
	}
	// The observed loaded compact Summary uses the 270-byte generation.
	if middle != 270 {
		return nil
	}
	entries[6] = fastSaveEntry{1, 496, size}
	entries[7] = fastSaveEntry{retiredFastSavePacket, 496 + size, 16}
	entries[8].offset += size
	return entries
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
	if _, present := d.InitialLineSpacing(); present {
		return d.ExportInitialCodesSave(true)
	}
	if err := d.checkFastSaveMutation(); err != nil {
		return nil, err
	}
	if _, sheet := d.SpreadsheetTable(); sheet {
		if d.Birth().IsNew() {
			return d.Export()
		}
		return d.exportLoadedFastSave(true, false)
	}
	if len(d.NamedStyles()) > 0 || d.hasGeneratedFeature() || d.Birth().IsNew() {
		return d.Export()
	}
	_, table := d.SimpleTable()
	return d.exportLoadedFastSave(table || d.CheckMergeSource() == nil, false)
}

// ExportCompactFastSave writes the observed pre-print Standard Printer graph.
// Fast Save Yes retains the pending-format bit after a successful purge.
func (d *Document) ExportCompactFastSave(fastSave bool) ([]byte, error) {
	if _, present := d.InitialLineSpacing(); present {
		return d.ExportInitialCodesSave(fastSave)
	}
	err := d.CheckMutation()
	table, isTable := d.SimpleTable()
	if _, sheet := d.SpreadsheetTable(); sheet {
		if _, err := d.prefixMutationAdmission(); err != nil {
			return nil, err
		}
		return d.Export()
	}
	if isTable {
		_, err = d.prefixMutationAdmission()
	}
	if err != nil {
		return nil, err
	}
	if len(d.NamedStyles()) > 0 {
		return d.Export()
	}
	image := d.state.image
	live := fastSaveLivePackets(image)
	if !prePrintFastSaveResources(live) {
		return d.Export()
	}
	raw := compactFastSaveResult(image, live, fastSave)
	if isTable && !fastSave {
		// A compact formatted table save refreshes the first row's
		// leading height to the actual height of that row.
		row := int(binary.LittleEndian.Uint32(raw[4:])) + int(d.state.gaps[1]-d.state.gaps[0])
		height := row + 13 + 2*(len(table.Widths)-2)
		copy(raw[row+5:row+7], raw[height:height+2])
	}
	return raw, nil
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
	prior := fastSaveLivePackets(image)
	live := fastSaveLivePackets(d.state.image)
	if len(live[1]) > 0 && len(prior[1]) > 0 {
		if len(info.Blocks) == 2 && info.Packets[0].Type == 7 || len(info.Blocks) == 3 && info.Blocks[1].Data.Offset == 270 {
			if err := checkFastSaveResources(live, prior, info.Prefix); err != nil {
				return nil, err
			}
			active := bytes.Clone(prior[6])
			active[0] |= 8
			return d.encodeFastSave(live, prior, 270, active)
		}
		return d.Export()
	}
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
		if nestedMergeArchiveCount(info.Prefix.Length) == 0 {
			return nil, failure(UnsupportedPrefix, -1, info.Prefix)
		}
		if _, err := original.CompactFastSave(); err != nil {
			return nil, err
		}
		markActive = true
	}
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
	summarySize := len(live[1])
	entries := fastSaveEntriesWithSummary(middle, summarySize)
	if entries == nil {
		return nil, failure(UnsupportedPrefix, -1, current.Inspect().Prefix)
	}
	prefixSize, lastOffset := fastSavePrefixBytes+summarySize, 512+summarySize
	if bodyInfo.Length > MaxMutationBytes-prefixSize {
		return nil, failure(MutationLimit, -1, bodyInfo)
	}
	header, _ := current.Bytes(wp51.Span{Offset: 0, Length: 16})
	body, _ := current.Bytes(bodyInfo)
	candidate := make([]byte, prefixSize+len(body))
	copy(candidate, header)
	binary.LittleEndian.PutUint32(candidate[4:], uint32(prefixSize))
	writeFastSaveBlock(candidate, 16, middle)
	writeFastSaveBlock(candidate, middle, lastOffset)
	writeFastSaveBlock(candidate, lastOffset, 0)
	blocks := [...]int{16, middle, lastOffset}
	if summarySize > 0 {
		copy(candidate[96:166], prior[15][16:])
	}
	for i, entry := range entries {
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
	copy(candidate[prefixSize:], body)
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
