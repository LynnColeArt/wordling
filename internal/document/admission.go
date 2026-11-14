package document

import (
	"bytes"
	"encoding/binary"
	"github.com/lynncoleart/wordling/internal/wp51"
	"sort"
)

// Qualified resource field values transcribed from approved WP23 field-ledger.json
// (72 complete fields plus index schemas), SDK51 WP3–18 and WP103–105.
// These are individual closed resource/metadata values, not a serialized prefix
// template or a fixture whitelist. Input ordering/locations are preserved. The
// body pointer, packet references and span ownership are validated separately.
// Hash variants are literal caches; no hash/font/counter algorithm is invented.
type qualifiedField struct {
	name   string
	offset int
	value  string
}

var qualifiedPacketFields = map[uint16][]qualifiedField{
	7: {
		{"font name string pool", 0, "\x43\x6f\x75\x72\x69\x65\x72\x20\x31\x30\x63\x70\x69\x00"},
	},
	15: {
		{"font instance ID", 0, "\x00\x00"},
		{"proportional-spacing cache ID", 2, "\xff\xff"},
		{"top shoulder height", 4, "\x89\x00"},
		{"bottom shoulder height", 6, "\x3f\x00"},
		{"printed character width", 8, "\x78\x00"},
		{"optimal space width", 10, "\x78\x00"},
		{"normal space width", 12, "\x78\x00"},
		{"horizontal motion units", 14, "\x0a\x00"},
		{"horizontal fractional numerator", 16, "\x01\x00"},
		{"font string pool offset", 18, "\x00\x00"},
		{"font flags", 20, "\x00"},
		{"descriptor match hash", 21, "\xe7\x24"},
		{"descriptor: cell height", 23, "\xf4\x01"},
		{"descriptor: optimal width", 25, "\x78\x00"},
		{"descriptor: cap height", 27, "\xfe\x15"},
		{"descriptor: x height", 29, "\x36\x10"},
		{"descriptor: descender height", 31, "\x58\x07"},
		{"descriptor: italic adjustment", 33, "\x00\x00"},
		{"descriptor: typeface descriptor", 35, "\x00\x04\x11"},
		{"descriptor: 5.0 typeface flags", 38, "\x40"},
		{"descriptor: typeface-name hash", 39, "\xc9"},
		{"descriptor: display-resource quality", 40, "\x00"},
		{"descriptor: font-name hash", 41, "\x93\x38"},
		{"descriptor: character-set completeness", 43, "\x01\x00\x01\x00"},
		{"descriptor: 5.1 point size", 47, "\x58\x02"},
		{"descriptor: 5.1 typeface flags", 49, "\x40"},
		{"attribute AFC", 50, "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe"},
		{"character-set AFC", 66, "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"},
		{"orientation AFC", 82, "\xff\xff\xff\xff"},
	},
	12: {
		{"printer long name", 0, "\x53\x74\x61\x6e\x64\x61\x72\x64\x20\x50\x72\x69\x6e\x74\x65\x72\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"},
		{"PRS filename", 37, "\x53\x54\x41\x4e\x50\x52\x49\x4e\x2e\x50\x52\x53\x00"},
		{"initial font descriptor: cell height", 50, "\xdb\x01"},
		{"initial font descriptor: optimal width", 52, "\x78\x00"},
		{"initial font descriptor: cap height", 54, "\x14\x1e"},
		{"initial font descriptor: x height", 56, "\x0c\x17"},
		{"initial font descriptor: descender height", 58, "\x8c\x0a"},
		{"initial font descriptor: italic adjustment", 60, "\x00\x00"},
		{"initial font descriptor: typeface descriptor", 62, "\x00\x04\x11"},
		{"initial font descriptor: 5.0 typeface flags", 65, "\x40"},
		{"initial font descriptor: typeface-name hash", 66, "\xc9"},
		{"initial font descriptor: display-resource quality", 67, "\x00"},
		{"initial font descriptor: font-name hash", 68, "\x87\xcf"},
		{"initial font descriptor: character-set completeness", 70, "\x01\x00\x01\x00"},
		{"minimum top", 74, "\x00\x00"},
		{"minimum bottom", 76, "\x00\x00"},
		{"minimum left", 78, "\x00\x00"},
		{"minimum right", 80, "\x00\x00"},
		{"printer flags", 82, "\x18"},
		{"PRS date", 83, "\x69\x18"},
		{"PRS time", 85, "\x8a\x60"},
		{"current font point size", 87, "\x58\x02"},
		{"current typeface flags", 89, "\x40"},
	},
	6: {
		{"document flags", 0, "\x00"},
		{"quality nibbles", 1, "\x23"},
		{"redline character", 2, "\x7c\x00"},
		{"screen character width", 4, "\x78\x00"},
		{"binding width", 6, "\x00\x00"},
		{"printer-select counter for equation hash", 8, "\x01"},
		{"reserved", 9, "\x00"},
		{"display pitch", 10, "\x00\x00"},
		{"screen resolution", 12, "\x00\x00"},
		{"reserved", 14, "\x00\x00"},
	},
	8: {
		{"graphics count", 0, "\x00\x00"},
	},
}

func (d *Document) prefixMutationAdmission() (int, error) {
	if !d.valid() {
		return 0, failure(InvalidDocument, -1, noSpan)
	}
	info := d.state.image.Inspect()
	if info.Prefix.Length+info.Body.Length > MaxMutationBytes || d.TokenCount() > MaxMutationTokens {
		return 0, failure(MutationLimit, -1, info.Body)
	}
	if flags, styled, err := d.stylePrefixAdmission(info); styled {
		return flags, err
	}
	if len(info.Blocks) != 2 || (len(info.Packets) != 5 && len(info.Packets) != 6) {
		return 0, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	raw := d.state.image.Export()
	// The approved reader checks native identity, arithmetic, bounds, cycles and
	// delimiters. Consume its actual packet/block spans, never reparse a codec.
	first, last := info.Blocks[0], info.Blocks[1]
	if first.Data.Offset != 16 || first.Data.Length != 50 || last.Data.Length != 50 || first.Count != 5 || last.Count != 5 || first.Next != uint32(last.Data.Offset) || last.Next != 0 {
		return 0, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	// Reader deliberately ignores unused slots/terminator payload; mutation may not.
	used := 10 * (len(info.Packets) - 3)
	if !bytes.Equal(raw[last.Data.Offset+used:last.Data.Offset+50], make([]byte, 50-used)) {
		return 0, failure(UnsupportedPrefix, -1, last.Data)
	}
	types := []uint16{7, 15, 12, 6, 8}
	// WP42's complete pre-print field/extent proof qualifies one additional
	// linked index order. Physical payload offsets still come from Inspect.
	reordered := info.Packets[0].Type == 6
	if reordered {
		types = []uint16{6, 7, 15, 12, 8}
	}
	if len(info.Packets) == 6 {
		if info.Packets[0].Type == initialCodesPacket && d.state.initialSpacing != 0 {
			types = []uint16{initialCodesPacket, 6, 7, 15, 12, 8}
		} else if !reordered && info.Packets[3].Type == initialCodesPacket && d.state.initialSpacing != 0 {
			types = []uint16{7, 15, 12, initialCodesPacket, 6, 8}
		} else if reordered {
			types = []uint16{6, 7, 15, 12, 1, 8}
		} else {
			types = []uint16{7, 15, 12, 1, 6, 8}
		}
	}
	sizes := map[uint16]int{7: 14, 15: 86, 12: 90, 6: 16, 8: 2, initialCodesPacket: 12}
	spans := []wp51.Span{{Offset: 0, Length: 16}, first.Data, last.Data}
	flags := -1
	var pool, font []byte
	for i, p := range info.Packets {
		expectedIndex := first.Data.Offset + 10*(i+1)
		if i >= 4 {
			expectedIndex = last.Data.Offset + 10*(i-3)
		}
		if p.Type != types[i] || (p.Type != 1 && p.Data.Length != sizes[p.Type]) || p.Index != (wp51.Span{Offset: expectedIndex, Length: 10}) {
			return 0, failure(UnsupportedPrefix, -1, p.Index)
		}
		spans = append(spans, p.Data)
		packet := raw[p.Data.Offset : p.Data.Offset+p.Data.Length]
		if p.Type == 1 {
			if _, err := parseSummary(packet); err != nil {
				return 0, failure(UnsupportedMetadata, -1, p.Data)
			}
			continue
		}
		if p.Type == initialCodesPacket {
			switch i {
			case 0:
				if p.Data.Offset != first.Data.Offset+first.Data.Length ||
					info.Packets[1].Data.Offset != p.Data.Offset+p.Data.Length ||
					last.Data.Offset != 194 || info.Packets[4].Data.Offset != last.Data.Offset+last.Data.Length {
					return 0, failure(UnsupportedPrefix, -1, p.Data)
				}
			case 3:
				if p.Data.Offset+p.Data.Length != last.Data.Offset ||
					info.Packets[2].Data.Offset+info.Packets[2].Data.Length != p.Data.Offset ||
					info.Packets[4].Data.Offset != last.Data.Offset+last.Data.Length {
					return 0, failure(UnsupportedPrefix, -1, p.Data)
				}
			}
		}
		category := UnsupportedResource
		if p.Type == 6 {
			category = UnsupportedMetadata
			flags = p.Data.Offset
		}
		if p.Type == 8 {
			category = UnsupportedPrefix
		}
		for _, f := range qualifiedPacketFields[p.Type] {
			actual := packet[f.offset : f.offset+len(f.value)]
			allowed := string(actual) == f.value
			if p.Type == 15 && f.offset == 21 {
				// Printer-cache descriptor hash. Observed e7 24 in the captured
				// sources and resaved stages, and 11 72 after printing rebuilds the
				// cache (every WP42 FIN stage). The value follows the cache
				// generation, not the index ordering, so both observed literals are
				// admitted regardless of packet order. Nothing here rewrites it.
				allowed = allowed || string(actual) == "\x11\x72"
			}
			if p.Type == 6 && f.offset == 0 {
				allowed = actual[0] == 0 || actual[0] == 8
				if actual[0] == 0x10 || actual[0] == 0x18 {
					// The generation flag is meaningful only when the
					// document actually contains an admitted generated feature.
					allowed = d.hasGeneratedFeature()
				}
			}
			if p.Type == 6 && f.offset == 6 {
				allowed = binary.LittleEndian.Uint16(actual) <= UnitsPerInch
			}
			if p.Type == 6 && f.offset == 8 {
				// The original increments this printer-select counter to 02 after a
				// print in every captured FIN stage; 01 is the pre-print value. Both
				// are observed values in the WP42 resaved-prefix contract, and this
				// package never rewrites the counter — body edits leave it literal.
				allowed = actual[0] == 0x01 || actual[0] == 0x02
			}
			if !allowed {
				return 0, failure(category, -1, wp51.Span{Offset: p.Data.Offset + f.offset, Length: len(f.value)})
			}
		}
		if p.Type == 7 {
			pool = packet
		}
		if p.Type == 15 {
			font = packet
		}
		if p.Type == 8 && p.Data.Offset+p.Data.Length != info.Body.Offset {
			return 0, failure(UnsupportedPrefix, -1, p.Data)
		}
	}
	// All prefix bytes are owned exactly once, including physically relocated
	// packets. This derives prefix length; it never assumes B=324 or flags=256.
	sort.Slice(spans, func(i, j int) bool { return spans[i].Offset < spans[j].Offset })
	end := 0
	for _, span := range spans {
		if span.Offset != end {
			return 0, failure(UnsupportedPrefix, -1, span)
		}
		end += span.Length
	}
	if end != info.Body.Offset {
		return 0, failure(UnsupportedPrefix, -1, info.Prefix)
	}
	pointer := int(binary.LittleEndian.Uint16(font[18:20]))
	if pointer >= len(pool) || bytes.IndexByte(pool[pointer:], 0) < 0 {
		return 0, failure(UnsupportedResource, -1, info.Prefix)
	}
	// One font row. AFC FF=no chain, FE=unavailable; other values must index it.
	for _, ref := range font[50:86] {
		if ref != 254 && ref != 255 && ref >= 1 {
			return 0, failure(UnsupportedResource, -1, info.Prefix)
		}
	}
	if font[62] != 255 {
		return 0, failure(UnsupportedResource, -1, info.Prefix)
	}
	return flags, nil
}

func (d *Document) mutationAdmission() (int, error) {
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return 0, err
	}
	if err := d.checkOrdinaryBody(); err != nil {
		return 0, err
	}
	return flags, nil
}

// CheckPrintBody validates the owners consumed by the read-only printer.
// Printing uses the selected Standard Printer geometry rather than writing
// or relocating the source document's prefix packets.
func (d *Document) CheckPrintBody() error {
	if !d.valid() {
		return failure(InvalidDocument, -1, noSpan)
	}
	info := d.state.image.Inspect()
	if info.Prefix.Length+info.Body.Length > MaxMutationBytes || d.TokenCount() > MaxMutationTokens {
		return failure(MutationLimit, -1, info.Body)
	}
	if spacing, present := d.InitialLineSpacing(); present && spacing == 0 {
		return failure(UnsupportedMetadata, -1, d.state.initialCodes)
	}
	return d.checkOrdinaryBody()
}

func (d *Document) checkOrdinaryBody() error {
	raw := d.state.image.Export()
	// Ordinary body content plus independently nested attributes. Bold and
	// Underline are separate flags, so the observed overlapping/nested everyday
	// spans are admissible; a duplicate ON or an unmatched OFF stays malformed.
	// The former two-pair ceiling was a WP23 policy, not a format limit.
	bold, underline := false, false
	redline, strikeout, italics := false, false, false
	var styles map[uint16]NamedStyle
	var activeStyle uint16
	for i := 0; i < d.TokenCount(); i++ {
		span := d.span(i)
		switch identify(raw[span.Offset : span.Offset+span.Length]) {
		case ASCII, ExtendedCharacter, HardSpace, DOSControl, HardReturn, SoftReturn, Tab, HardPage, SoftPage, DeletedSoftReturn, Indent, EndIndent, PageNumberReset, BlockProtectOn, BlockProtectOff, LineMargins, PageMargins, CenterLine, FlushRight, EndAlignment, LineSpacing, LineHeight:
		case ParagraphJustification, ParagraphPosition, DoubleIndent, MarginRelease, Footnote, Endnote, PageTextCode, LineNumbering, ConditionalPage, PageNumberPosition, SuppressPageNumber,
			WidowProtectionOn, WidowProtectionOff, TabSetCode, DecimalTab, FootnoteOptions, DateCode, SoftDecimalTab, Comment, ContentsMark, ContentsDefinition, ContentsEnd, ContentsLeader, Subdocument, PageReference, ReferenceTarget, AuthorityMark, OutlineOn, OutlineNumber, MathOn, MathOff, MathSubtotal, PrinterCommand, LanguageCode, KerningCode:
		case StyleOn, StyleOff:
			if styles == nil {
				styles = map[uint16]NamedStyle{}
				for _, s := range d.NamedStyles() {
					styles[s.ID] = s
				}
			}
			style, ok := decodeStyleOwner(raw[span.Offset : span.Offset+span.Length])
			def, found := styles[style.ID]
			off := raw[span.Offset+1] == 1
			if !ok || !found || style.Name != def.Name || !off && (activeStyle != 0 || style.OnCache != def.OnCache) ||
				off && (activeStyle != style.ID || style.OffCache != def.OffCache) {
				return failure(UnsupportedBody, i, span)
			}
			boldKind := BoldOn
			if off {
				boldKind = BoldOff
				activeStyle = 0
			} else {
				activeStyle = style.ID
			}
			a, err := d.Token(i + 1)
			b, err2 := d.Token(i + 2)
			if err != nil || err2 != nil || a.Kind != boldKind || b.Kind != StyleEndCodes {
				return failure(UnsupportedBody, i, span)
			}
		case StyleEndCodes:
			if i < 2 {
				return failure(UnsupportedBody, i, span)
			}
			begin, _ := d.Token(i - 2)
			if begin.Kind != StyleOn && begin.Kind != StyleOff {
				return failure(UnsupportedBody, i, span)
			}
		case EndOfPage:
			group, ok := d.matchedPageGroup(i)
			if !ok {
				return failure(UnsupportedBody, i, span)
			}
			i += group.tokens - 1
		case RedlineOn, RedlineOff, StrikeoutOn, StrikeoutOff, ItalicsOn, ItalicsOff:
			kind := identify(raw[span.Offset : span.Offset+span.Length])
			active := &redline
			if kind == StrikeoutOn || kind == StrikeoutOff {
				active = &strikeout
			} else if kind == ItalicsOn || kind == ItalicsOff {
				active = &italics
			}
			on := kind == RedlineOn || kind == StrikeoutOn || kind == ItalicsOn
			if *active == on {
				return failure(UnsupportedBody, i, span)
			}
			*active = on
		case BoldOn:
			if bold {
				return failure(UnsupportedBody, i, span)
			}
			bold = true
		case BoldOff:
			if !bold {
				return failure(UnsupportedBody, i, span)
			}
			bold = false
		case UnderlineOn:
			if underline {
				return failure(UnsupportedBody, i, span)
			}
			underline = true
		case UnderlineOff:
			if !underline {
				return failure(UnsupportedBody, i, span)
			}
			underline = false
		default:
			return failure(UnsupportedBody, i, span)
		}
	}
	if (bold || underline) && !d.state.openWordRestore {
		return failure(UnsupportedBody, d.TokenCount(), d.state.image.Inspect().Body)
	}
	if activeStyle != 0 || redline || strikeout || italics {
		return failure(UnsupportedBody, d.TokenCount(), noSpan)
	}
	return nil
}
