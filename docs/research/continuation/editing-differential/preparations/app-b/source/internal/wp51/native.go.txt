// Package wp51 validates the bounded WP 5.1 DOS document outer framing
// described in contracts/native-framing.md. It preserves exact native bytes;
// acceptance establishes neither semantic validity nor safe semantic editing.
package wp51

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"sort"
)

// Safety policies for this reader slice, not original application format limits.
const (
	MaxInputBytes                 = 16 << 20
	MaxIndexBlocks                = 4096
	MaxPacketEntries              = 16384
	OuterFramedPayloadUnvalidated = "outer-framed, payload-unvalidated"
)

// Category distinguishes unsupported variants from malformed input and limits.
type Category string

const (
	UnsupportedFormat     Category = "UnsupportedFormat"
	UnsupportedProduct    Category = "UnsupportedProduct"
	UnsupportedFileType   Category = "UnsupportedFileType"
	UnsupportedVersion    Category = "UnsupportedVersion"
	UnsupportedEncryption Category = "UnsupportedEncryption"
	UnsupportedVariant    Category = "UnsupportedVariant"
	UnsupportedStructure  Category = "UnsupportedStructure"
	InputLimit            Category = "InputLimit"
	TraversalLimit        Category = "TraversalLimit"
	TruncatedInput        Category = "TruncatedInput"
	MalformedPrefix       Category = "MalformedPrefix"
	MalformedBody         Category = "MalformedBody"
)

// Failure reports an absolute byte offset and the violated field or boundary.
// Detail further identifies cases such as Cycle and DelimiterMismatch.
type Failure struct {
	Category      Category
	Offset        int
	Field, Detail string
}

func (e *Failure) Error() string {
	return fmt.Sprintf("wp51: %s at %d (%s): %s", e.Category, e.Offset, e.Field, e.Detail)
}
func fail(c Category, o int, field, detail string) error { return &Failure{c, o, field, detail} }

// Span is an absolute half-open byte range, represented by offset and length.
type Span struct{ Offset, Length int }

// Block describes a checked special index block in native traversal order.
type Block struct {
	Data  Span
	Count int
	Next  uint32
}

// Packet retains its type, index relationship and opaque bounded data span.
type Packet struct {
	Type        uint16
	Index, Data Span
}

// Inspection describes framing only. Packet and function payloads are unvalidated.
// Every slice returned by Inspect is independent of the image.
type Inspection struct {
	Validation      string
	Prefix, Body    Span
	Blocks          []Block
	Packets         []Packet
	OuterTokenCount int
}

// Image owns its complete immutable input. Construct accepted images with Parse.
// Bytes not referenced by metadata remain preserved in this authoritative image.
type Image struct {
	data []byte
	info Inspection
}

// Export returns a fresh, byte-identical no-edit copy, including all gaps/tails.
func (i *Image) Export() []byte { return bytes.Clone(i.data) }

// Inspect returns an independent copy of framing metadata, without byte aliases.
func (i *Image) Inspect() Inspection {
	c := i.info
	c.Blocks = append([]Block(nil), c.Blocks...)
	c.Packets = append([]Packet(nil), c.Packets...)
	return c
}

// Bytes returns a fresh copy of a bounded span, or false for an invalid range.
func (i *Image) Bytes(s Span) ([]byte, bool) {
	if s.Offset < 0 || s.Length < 0 || s.Offset > len(i.data) || s.Length > len(i.data)-s.Offset {
		return nil, false
	}
	return bytes.Clone(i.data[s.Offset : s.Offset+s.Length]), true
}

// Parse checks identity, prefix/index/packet boundaries and body outer framing.
// The size limit is checked before copying. A refusal returns no accepted image
// and never changes caller data. Callers must not mutate input during Parse.
// File acquisition/replacement and semantic mutation belong to other packages.
func Parse(input []byte) (*Image, error) {
	if len(input) > MaxInputBytes {
		return nil, fail(InputLimit, 0, "input", "exceeds 16 MiB")
	}
	if len(input) < 16 {
		return nil, fail(TruncatedInput, len(input), "header", "requires 16 bytes")
	}
	if !bytes.Equal(input[:4], []byte{0xff, 'W', 'P', 'C'}) {
		return nil, fail(UnsupportedFormat, 0, "signature", "expected FF575043")
	}
	if input[8] != 1 {
		return nil, fail(UnsupportedProduct, 8, "product", "expected 1")
	}
	if input[9] != 10 {
		return nil, fail(UnsupportedFileType, 9, "file type", "only document type 10 is supported")
	}
	if input[10] != 0 || input[11] != 1 {
		return nil, fail(UnsupportedVersion, 10, "stored version", "expected 0/1")
	}
	if u16(input, 12) != 0 {
		return nil, fail(UnsupportedEncryption, 12, "password", "encrypted input is unsupported")
	}
	if u16(input, 14) != 0 {
		return nil, fail(UnsupportedVariant, 14, "reserved header", "nonzero reserved value")
	}
	boundary := u32(input, 4)
	if boundary < 16 || uint64(boundary) > uint64(len(input)) {
		return nil, fail(MalformedPrefix, 4, "body offset", "outside [16,EOF]")
	}
	b := int(boundary)
	info := Inspection{Validation: OuterFramedPayloadUnvalidated, Prefix: Span{0, b}, Body: Span{b, len(input) - b}}
	if err := prefix(input, b, &info); err != nil {
		return nil, err
	}
	count, err := body(input, b)
	if err != nil {
		return nil, err
	}
	info.OuterTokenCount = count
	return &Image{data: bytes.Clone(input), info: info}, nil
}
func u16(b []byte, o int) uint16 { return binary.LittleEndian.Uint16(b[o : o+2]) }
func u32(b []byte, o int) uint32 { return binary.LittleEndian.Uint32(b[o : o+4]) }

func prefix(data []byte, b int, info *Inspection) error {
	visited := make(map[int]bool)
	offset := 16
	graphics := false
	done := false
	for !done {
		if visited[offset] {
			return fail(MalformedPrefix, offset, "next block", "Cycle")
		}
		if len(info.Blocks) >= MaxIndexBlocks {
			return fail(TraversalLimit, offset, "index blocks", "exceeds 4096")
		}
		if offset < 16 || offset > b || b-offset < 10 {
			return fail(MalformedPrefix, offset, "block header", "outside prefix or truncated")
		}
		visited[offset] = true
		if u16(data, offset) != 0xfffb {
			return fail(MalformedPrefix, offset, "block type", "expected FFFB")
		}
		count := int(u16(data, offset+2))
		size := int(u16(data, offset+4))
		if count == 0 || size != count*10 {
			return fail(MalformedPrefix, offset+2, "block count/size", "zero count or inconsistent size")
		}
		if size > b-offset {
			return fail(MalformedPrefix, offset+4, "block size", "block crosses body boundary")
		}
		if count != 5 {
			return fail(UnsupportedVariant, offset+2, "block count", "only five-entry document blocks validated")
		}
		next := u32(data, offset+6)
		// Only the followed next pointer is interpreted; an early type 0 ends enumeration.
		block := Block{Data: Span{offset, size}, Count: count, Next: next}
		info.Blocks = append(info.Blocks, block)
		for j := 1; j < count; j++ {
			index := offset + 10*j
			k := u16(data, index)
			if k == 0 {
				done = true
				break
			}
			if graphics {
				return fail(UnsupportedStructure, index, "packet 8 ordering", "graphics index must be last")
			}
			if k == 0xfffb {
				return fail(UnsupportedStructure, index, "packet type", "special header in general entry")
			}
			if len(info.Packets) >= MaxPacketEntries {
				return fail(TraversalLimit, index, "packet entries", "exceeds 16384")
			}
			length, pos := u32(data, index+2), u32(data, index+6)
			if pos < 16 || uint64(pos) > uint64(b) || uint64(length) > uint64(b)-uint64(pos) {
				return fail(MalformedPrefix, index+2, "packet position/length", "outside prefix")
			}
			p := Packet{Type: k, Index: Span{index, 10}, Data: Span{int(pos), int(length)}}
			if k == 8 {
				if length != 2 {
					return fail(MalformedPrefix, index+2, "packet 8 length", "requires two-byte count")
				}
				if u16(data, int(pos)) != 0 {
					return fail(UnsupportedStructure, int(pos), "graphics count", "nonzero graphics extent unvalidated")
				}
				graphics = true
			}
			info.Packets = append(info.Packets, p)
		}
		if done || next == 0 {
			break
		}
		if next < 16 || uint64(next) >= uint64(b) {
			return fail(MalformedPrefix, offset+6, "next block", "outside prefix")
		}
		offset = int(next)
	}
	// Sort temporary spans only. Native metadata and bytes retain original order.
	type extent struct {
		span  Span
		block bool
	}
	ranges := make([]extent, 0, len(info.Blocks)+len(info.Packets))
	for _, block := range info.Blocks {
		ranges = append(ranges, extent{block.Data, true})
	}
	for _, packet := range info.Packets {
		if packet.Data.Length > 0 {
			ranges = append(ranges, extent{packet.Data, false})
		}
	}
	sort.Slice(ranges, func(i, j int) bool { return ranges[i].span.Offset < ranges[j].span.Offset })
	for j := 1; j < len(ranges); j++ {
		prev, cur := ranges[j-1], ranges[j]
		if cur.span.Offset < prev.span.Offset+prev.span.Length {
			if prev.block && cur.block {
				return fail(MalformedPrefix, cur.span.Offset, "index blocks", "overlapping blocks")
			}
			return fail(UnsupportedStructure, cur.span.Offset, "prefix spans", "overlapping packet/index or packet data")
		}
	}
	return nil
}

var fixedWidths = [16]int{4, 9, 11, 3, 3, 5, 6, 7, 4, 5, 6, 6, 8, 10, 10, 12}

func body(data []byte, start int) (int, error) {
	tokens := 0
	for q := start; q < len(data); tokens++ {
		code := data[q]
		remaining := len(data) - q
		if code == 0 || code == 0x7f {
			return 0, fail(MalformedBody, q, "single-byte token", "00 and 7F are not standalone tokens")
		}
		if code < 0xc0 {
			q++
			continue
		}
		if code <= 0xcf {
			width := fixedWidths[code-0xc0]
			if width > remaining {
				return 0, fail(MalformedBody, q, "fixed function", "truncated")
			}
			if data[q+width-1] != code {
				return 0, fail(MalformedBody, q+width-1, "fixed trailer", "DelimiterMismatch")
			}
			q += width
			continue
		}
		if remaining < 4 {
			return 0, fail(MalformedBody, q, "variable header", "truncated")
		}
		length := int(u16(data, q+2))
		if length < 4 {
			return 0, fail(MalformedBody, q+2, "variable length", "requires L>=4")
		}
		if length+4 > remaining {
			return 0, fail(MalformedBody, q+2, "variable length", "span crosses EOF")
		}
		if u16(data, q+length) != uint16(length) || data[q+length+2] != data[q+1] || data[q+length+3] != code {
			return 0, fail(MalformedBody, q+length, "variable trailer", "DelimiterMismatch")
		}
		q += length + 4
	}
	return tokens, nil
}
