package document

import (
	"bytes"
	"encoding/binary"

	"github.com/lynncoleart/wordling/internal/wp51"
)

const (
	nestedMergeArchiveBytes = 256
	maxNestedMergeArchives  = 16
)

// WithLeadingPrimaries retains a resource-generation count only after matching
// each source that the merge entered before emitting output to the compact
// Standard Printer graph witnessed for this save family.
func (p MergeSaveProfile) WithLeadingPrimaries(sources [][]byte) (MergeSaveProfile, error) {
	if len(sources) == 0 {
		return p, nil
	}
	if !p.primary.valid() || len(sources) > maxNestedMergeArchives || !matchesNestedMergeSource(p.primary.image) {
		return MergeSaveProfile{}, failure(UnsupportedPrefix, -1, noSpan)
	}
	prior := fastSaveLivePackets(p.primary.image)
	states := make([]byte, 0, len(sources)+1)
	states = append(states, prior[6][0])
	for _, raw := range sources {
		child, err := Parse(raw)
		if err != nil {
			return MergeSaveProfile{}, err
		}
		if !matchesNestedMergeSource(child.state.image) {
			return MergeSaveProfile{}, failure(UnsupportedPrefix, -1, noSpan)
		}
		if _, err := child.prefixMutationAdmission(); err != nil {
			return MergeSaveProfile{}, err
		}
		current := fastSaveLivePackets(child.state.image)
		if !bytes.Equal(current[6][1:], prior[6][1:]) {
			return MergeSaveProfile{}, failure(UnsupportedMetadata, -1, noSpan)
		}
		for _, kind := range [...]uint16{7, 15, 12, 8} {
			if !bytes.Equal(current[kind], prior[kind]) {
				return MergeSaveProfile{}, failure(UnsupportedResource, -1, noSpan)
			}
		}
		states = append(states, current[6][0])
	}
	p.archiveStates = states
	return p, nil
}

func matchesNestedMergeSource(image *wp51.Image) bool {
	info := image.Inspect()
	if info.Prefix.Length != compactFastSavePrefixBytes || len(info.Packets) != 5 || len(info.Blocks) != 2 ||
		info.Blocks[1].Data.Offset != 272 {
		return false
	}
	layout := [...]fastSaveEntry{{7, 66, 14}, {15, 80, 86}, {12, 166, 90}, {6, 256, 16}, {8, 322, 2}}
	for i, p := range info.Packets {
		want := layout[i]
		index := 26 + 10*i
		if i == 4 {
			index = 282
		}
		if p.Type != want.kind || p.Data != (wp51.Span{Offset: want.offset, Length: want.size}) ||
			p.Index != (wp51.Span{Offset: index, Length: 10}) {
			return false
		}
	}
	packets := fastSaveLivePackets(image)
	return prePrintFastSaveResources(packets) && (packets[6][0] == 0 || packets[6][0] == 8)
}

func nestedMergeArchiveCount(prefixBytes int) int {
	delta := prefixBytes - fastSavePrefixBytes
	if delta < nestedMergeArchiveBytes || delta%nestedMergeArchiveBytes != 0 || delta/nestedMergeArchiveBytes > maxNestedMergeArchives {
		return 0
	}
	return delta / nestedMergeArchiveBytes
}

func nestedMergeCandidate(image *wp51.Image, packets map[uint16][]byte, active, archivedStates []byte) []byte {
	const retired = retiredFastSavePacket
	archives := len(archivedStates) - 1
	delta := nestedMergeArchiveBytes * archives
	bodyOffset := fastSavePrefixBytes + delta
	info := image.Inspect()
	candidate := make([]byte, bodyOffset+info.Body.Length)
	header, _ := image.Bytes(wp51.Span{Length: 16})
	copy(candidate, header)
	binary.LittleEndian.PutUint32(candidate[4:], uint32(bodyOffset))
	blocks := make([]int, 0, archives+3)
	blocks = append(blocks, 16)
	for generation := 0; generation <= archives; generation++ {
		blocks = append(blocks, 270+nestedMergeArchiveBytes*generation)
	}
	blocks = append(blocks, 512+delta)
	for i := 0; i < len(blocks)-1; i++ {
		writeFastSaveBlock(candidate, blocks[i], blocks[i+1])
	}
	writeFastSaveBlock(candidate, blocks[len(blocks)-1], 0)
	at := 0
	write := func(kind uint16, offset int, data []byte) {
		index := blocks[at/4] + 10*(at%4+1)
		writeFastSaveEntry(candidate, index, fastSaveEntry{kind, offset, len(data)})
		copy(candidate[offset:], data)
		at++
	}
	write(retired, 66, packets[7])
	write(6, 80, active)
	write(retired, 166, packets[12])
	state := bytes.Clone(packets[6])
	for generation := 0; generation <= archives; generation++ {
		shift := nestedMergeArchiveBytes * generation
		for _, p := range [...]fastSaveEntry{{7, 256, 14}, {15, 320, 86}, {12, 406, 90}} {
			kind := p.kind
			if generation < archives {
				kind = retired
			}
			write(kind, p.offset+shift, packets[p.kind])
		}
		state[0] = archivedStates[generation]
		write(retired, 496+shift, state)
	}
	write(retired, 96, packets[15][16:])
	write(8, 562+delta, packets[8])
	body, _ := image.Bytes(info.Body)
	copy(candidate[bodyOffset:], body)
	return candidate
}

func (d *Document) compactNestedMergePrefix(archives int) (*Document, error) {
	image := d.state.image
	info := image.Inspect()
	refuse := failure(UnsupportedPrefix, -1, info.Prefix)
	if len(info.Packets) != 9+4*archives || len(info.Blocks) != 3+archives ||
		info.Body.Offset+info.Body.Length > MaxMutationBytes || d.TokenCount() > MaxMutationTokens {
		return nil, refuse
	}
	packets := fastSaveLivePackets(image)
	if len(packets[7]) != 14 || len(packets[12]) != 90 || len(packets[15]) != 86 ||
		len(packets[6]) != 16 || len(packets[8]) != 2 || !prePrintFastSaveResources(packets) {
		return nil, refuse
	}
	active := packets[6]
	if active[0] != 0 && active[0] != 8 {
		return nil, refuse
	}
	states := make([]byte, archives+1)
	for generation := range states {
		prior, ok := image.Bytes(wp51.Span{Offset: 496 + nestedMergeArchiveBytes*generation, Length: 16})
		if !ok || (prior[0] != 0 && prior[0] != 8) || !bytes.Equal(active[1:], prior[1:]) {
			return nil, refuse
		}
		states[generation] = prior[0]
	}
	rawPrefix, _ := image.Bytes(info.Prefix)
	expected := nestedMergeCandidate(image, packets, active, states)
	if !bytes.Equal(rawPrefix, expected[:info.Body.Offset]) {
		return nil, refuse
	}
	return parseRevision(compactFastSaveCandidate(image, packets), d.state.birth)
}
