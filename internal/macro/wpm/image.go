// Package wpm implements the bounded, immutable WPM image contract in
// contracts/macro-framing.md. It neither executes macros nor writes their format.
package wpm

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"fmt"
)

const (
	MaxInputBytes       = 16 << 20
	MaxDescriptionBytes = 4096
	MaxWords            = 1 << 20
)

// Span is an absolute half-open byte extent. Words are aligned relative to B,
// not the beginning of the file.
type Span struct{ Offset, Length uint32 }
type Kind string

const (
	Literal   Kind = "literal"
	Character Kind = "character"
	Key       Kind = "key"
	Macro     Kind = "macro"
	Control   Kind = "control"
	Terminal  Kind = "terminal"
	Opaque    Kind = "opaque"
)

type Word struct {
	Value uint16
	Span  Span
	Kind  Kind
}
type Limits struct{ InputBytes, DescriptionBytes, Words uint32 }
type Finding struct {
	Code             string
	Span             Span
	ExecutionBlocked bool
}
type Header struct {
	BodyOffset                      uint32
	Product, FileType, Major, Minor byte
}
type Inspection struct {
	Header                              Header
	Description, Body, Terminal, Suffix Span
	Findings                            []Finding
	ReleaseEvidence                     string
}
type Failure struct {
	Code          string
	Offset        uint32
	Field, Detail string
}

func (e *Failure) Error() string {
	return fmt.Sprintf("wpm: %s at %d (%s): %s", e.Code, e.Offset, e.Field, e.Detail)
}
func fail(code string, offset uint32, field, detail string) error {
	return &Failure{code, offset, field, detail}
}

// Image owns a complete accepted input. Construct it with Parse; the zero value
// is not an accepted image. Caller buffers must not be modified during Parse.
type Image struct {
	data []byte
	info Inspection
	hash [32]byte
}

func DefaultLimits() Limits { return Limits{MaxInputBytes, MaxDescriptionBytes, MaxWords} }
func (i *Image) Export() []byte {
	if i == nil {
		return nil
	}
	return bytes.Clone(i.data)
}
func (i *Image) Inspect() Inspection {
	if i == nil {
		return Inspection{}
	}
	x := i.info
	x.Findings = append([]Finding(nil), x.Findings...)
	return x
}
func (i *Image) Description() []byte {
	if i == nil || len(i.data) == 0 {
		return nil
	}
	s := i.info.Description
	return bytes.Clone(i.data[s.Offset : s.Offset+s.Length])
}
func (i *Image) SHA256() [32]byte {
	if i == nil {
		return [32]byte{}
	}
	return i.hash
}
func (i *Image) BodyWords() []Word {
	if i == nil || len(i.data) == 0 {
		return nil
	}
	s := i.info.Body
	words := make([]Word, s.Length/2)
	for n := range words {
		offset := s.Offset + uint32(n)*2
		v := binary.LittleEndian.Uint16(i.data[offset : offset+2])
		kind, _ := classify(v)
		words[n] = Word{v, Span{offset, 2}, kind}
	}
	return words
}

// Parse validates bounded framing and preserves the exact input. Opaque findings
// block future execution; parse success establishes no operand/VM/edit support.
func Parse(input []byte, limits Limits) (*Image, error) {
	if limits.InputBytes == 0 || limits.InputBytes > MaxInputBytes || limits.DescriptionBytes == 0 || limits.DescriptionBytes > MaxDescriptionBytes || limits.Words == 0 || limits.Words > MaxWords {
		return nil, fail("InvalidLimit", 0, "limits", "positive limits must not exceed declared maxima")
	}
	if uint64(len(input)) > uint64(limits.InputBytes) {
		return nil, fail("InputLimit", 0, "input", "exceeds configured input budget")
	}
	if len(input) < 16 {
		return nil, fail("TruncatedInput", uint32(len(input)), "header", "requires 16 bytes")
	}
	if !bytes.Equal(input[:4], []byte{0xff, 'W', 'P', 'C'}) {
		return nil, fail("UnsupportedFormat", 0, "signature", "expected FF575043")
	}
	for _, field := range []struct {
		offset int
		want   byte
		code   string
		name   string
	}{{8, 1, "UnsupportedProduct", "product"}, {9, 1, "UnsupportedFileType", "file type"}, {10, 1, "UnsupportedVersion", "major"}, {11, 1, "UnsupportedVersion", "minor"}} {
		if input[field.offset] != field.want {
			return nil, fail(field.code, uint32(field.offset), field.name, "outside admitted WPM tuple 1/1/1/1")
		}
	}
	u16 := func(o int) uint16 { return binary.LittleEndian.Uint16(input[o : o+2]) }
	u32 := func(o int) uint32 { return binary.LittleEndian.Uint32(input[o : o+4]) }
	if u16(12) != 0 {
		return nil, fail("UnsupportedEncryption", 12, "key", "nonzero key")
	}
	if u16(14) != 0 {
		return nil, fail("UnsupportedVariant", 14, "reserved", "nonzero reserved field")
	}
	if len(input) < 26 {
		return nil, fail("TruncatedInput", uint32(len(input)), "index header", "requires ten bytes")
	}
	if u16(16) != 0xfffb {
		return nil, fail("MalformedPrefix", 16, "index header type", "expected FFFB")
	}
	count, blockSize := uint32(u16(18)), uint32(u16(20))
	if count == 0 || count*10 != blockSize {
		return nil, fail("MalformedPrefix", 18, "index count/size", "nonzero count must agree with count*10")
	}
	if blockSize > uint32(len(input))-16 {
		return nil, fail("TruncatedInput", 20, "index block", "incomplete declared block")
	}
	if count != 4 {
		return nil, fail("UnsupportedVariant", 18, "index count", "only four-entry macros qualified")
	}
	n, b := uint32(len(input)), u32(4)
	if b < 56 || b > n {
		return nil, fail("MalformedPrefix", 4, "body offset", "requires 56 <= B <= input length")
	}
	if next := u32(22); next != 0 {
		if next < 16 || next > b || 10 > b-next {
			return nil, fail("MalformedPrefix", 22, "next index", "pointer outside complete prefix header")
		}
		return nil, fail("UnsupportedVariant", 22, "next index", "linked WPM blocks unqualified; not followed")
	}
	if u16(26) != 1 {
		return nil, fail("UnsupportedVariant", 26, "description type", "only type 1 qualified")
	}
	l, p := u32(28), u32(32)
	if p < 56 || p > b || l > b-p {
		return nil, fail("MalformedPrefix", 28, "description extent", "extent outside [56,B)")
	}
	if l == 0 {
		return nil, fail("UnsupportedVariant", 28, "description length", "zero-length editor producer unqualified")
	}
	if l > limits.DescriptionBytes {
		return nil, fail("TraversalLimit", 28, "description length", "exceeds configured description budget")
	}
	if input[p+l-1] != 0 {
		return nil, fail("MalformedPrefix", p+l-1, "description terminator", "expected final zero byte")
	}
	info := Inspection{Header: Header{b, input[8], input[9], input[10], input[11]}, Description: Span{p, l}, ReleaseEvidence: "unknown-from-bytes"}
	// One finding per category bounds diagnostics independently of hostile words.
	add := func(code string, span Span) {
		for _, existing := range info.Findings {
			if existing.Code == code {
				return
			}
		}
		info.Findings = append(info.Findings, Finding{code, span, true})
	}
	if p != 56 || p+l != b || bytes.IndexByte(input[p:p+l-1], 0) >= 0 {
		add("UnsupportedVariant", Span{p, l})
	}
	extents := []Span{{p, l}}
	for _, offset := range []int{36, 46} {
		if bytes.Equal(input[offset:offset+10], make([]byte, 10)) {
			continue
		}
		length, pos := u32(offset+2), u32(offset+6)
		if length != 0 {
			if pos < 56 || pos > b || length > b-pos {
				return nil, fail("MalformedPrefix", uint32(offset+2), "opaque extent", "outside [56,B)")
			}
			for _, previous := range extents {
				if pos < previous.Offset+previous.Length && previous.Offset < pos+length {
					return nil, fail("UnsupportedStructure", uint32(offset), "opaque extent", "unqualified overlapping/aliased spans")
				}
			}
			extents = append(extents, Span{pos, length})
		}
		add("OpaquePrefixIndex", Span{uint32(offset), 10})
	}
	for offset, words := b, uint32(0); ; offset, words = offset+2, words+1 {
		if offset == n {
			return nil, fail("MalformedBody", offset, "MissingTerminator", "no terminal word")
		}
		if 2 > n-offset {
			return nil, fail("MalformedBody", offset, "OddWord", "unpaired body byte before terminal")
		}
		if words >= limits.Words {
			return nil, fail("TraversalLimit", offset, "body words", "exceeds configured word budget")
		}
		value := binary.LittleEndian.Uint16(input[offset : offset+2])
		_, finding := classify(value)
		if finding != "" {
			add(finding, Span{offset, 2})
		}
		if value == 0 {
			info.Body = Span{b, offset + 2 - b}
			info.Terminal = Span{offset, 2}
			info.Suffix = Span{offset + 2, n - offset - 2}
			if info.Suffix.Length != 0 {
				add("OpaqueSuffix", info.Suffix)
			}
			break
		}
	}
	owned := bytes.Clone(input)
	return &Image{owned, info, sha256.Sum256(owned)}, nil
}

func classify(value uint16) (Kind, string) {
	if value == 0 {
		return Terminal, ""
	}
	if value >= 0x20 && value <= 0x7e {
		return Literal, ""
	}
	if value == 0x8021 {
		return Key, ""
	}
	if value>>8 == 0xfc {
		switch value {
		case 0xfc01, 0xfc03, 0xfc0c, 0xfc0e, 0xfc0f, 0xfc10, 0xfc11, 0xfc12, 0xfc13, 0xfc14, 0xfc15, 0xfc16, 0xfc18, 0xfc19, 0xfc1c, 0xfc1d, 0xfc20, 0xfc22, 0xfc2b, 0xfc34:
			return Macro, ""
		default:
			return Opaque, "UnqualifiedMacro"
		}
	}
	if value>>8 == 0x80 || value>>8 == 0xfe || value>>8 == 0xff {
		return Key, "UnqualifiedKey"
	}
	if value < 0x20 {
		return Control, "UnqualifiedControl"
	}
	if value>>8 <= 12 {
		return Character, "UnqualifiedCharacter"
	}
	return Opaque, "UnknownWord"
}
