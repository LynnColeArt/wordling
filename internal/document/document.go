// Package document exposes immutable native revisions and shared normal/Reveal
// token gaps. Semantic writes require the narrower WP23 mutation admission.
package document

import (
	"bytes"
	"encoding/binary"
	"fmt"

	"github.com/lynncoleart/wordling/internal/wp51"
)

// Safety policies, not original application limits. The gap index is at most
// (MaxTokens+1)*4 bytes; a presentation allocates at most MaxWindowTokens elements.
const (
	MaxTokens       = 1 << 20
	MaxWindowTokens = 4096
)

type Category string

const (
	InvalidDocument  Category = "InvalidDocument"
	InvalidPosition  Category = "InvalidPosition"
	InvalidDirection Category = "InvalidDirection"
	TokenLimit       Category = "TokenLimit"
	WindowLimit      Category = "WindowLimit"
	UnsupportedToken Category = "UnsupportedToken"
)

// Failure identifies a document refusal. Native-reader errors pass through with
// their original *wp51.Failure type. A negative index/span denotes no token.
type Failure struct {
	Category   Category
	TokenIndex int
	Span       wp51.Span
}

func (e *Failure) Error() string {
	return fmt.Sprintf("document: %s at token %d, span %d+%d", e.Category, e.TokenIndex, e.Span.Offset, e.Span.Length)
}
func failure(k Category, index int, span wp51.Span) error { return &Failure{k, index, span} }

var noSpan = wp51.Span{Offset: -1}

type Kind uint8

const (
	Opaque Kind = iota
	ASCII
	BoldOn
	BoldOff
	HardReturn
	// Appended for the everyday milestone (WP80 T244). Existing values are
	// frozen because callers switch on them.
	SoftReturn
	UnderlineOn
	UnderlineOff
	Tab
	HardPage
	// Deleted soft return, observed as the single byte 90 in the captured
	// unbroken-word flow document (WP78: "unbroken-word DSRt=90").
	DeletedSoftReturn
	// Ordinary page structure (WP80 T244d). The D4 subfunction-0 record is the
	// Developer's Toolkit's Format Group 212 "End of Page" function; 8C and 99 are
	// its single-byte companions (function table: 140 = combination hard return/
	// soft page, 153 = dormant hard return). The D4 record is formatter metadata;
	// Reveal identifies its visible companions separately.
	EndOfPage
	HardReturnSoftPage
	DormantHardReturn
	// Original default-profile page-wrap companions. These distinct owners
	// carry space and no-space semantics, respectively.
	SoftPage
	DeletedSoftPage
	// These are exact observed merge function frames for presentation.
	// They do not confer mutation or execution authority.
	MergeField
	MergeEndField
	MergeEndRecord
	MergePageOff
	MergePageOn
	MergeNestPrimary
	MergeNestSecondary
	MergeIfBlank
	MergeElse
	MergeEndIf
	MergeBreak
	Indent
	EndIndent
	ExtendedCharacter
	DOSControl
	PageNumberReset
	BlockProtectOn
	BlockProtectOff
	HardSpace
	LineMargins
	PageMargins
	CenterLine
	FlushRight
	EndAlignment
	LineSpacing
	LineHeight
	ParagraphJustification
	ParagraphPosition
	DoubleIndent
	MarginRelease
	Footnote
	Endnote
	PageTextCode
	LineNumbering
	ConditionalPage
	WidowProtectionOn
	WidowProtectionOff
	TabSetCode
	DecimalTab
	FootnoteOptions
	DateCode
	SoftDecimalTab
	Comment
	ContentsMark
	ContentsDefinition
	ContentsEnd
	ContentsLeader
	Subdocument
	PageReference
	ReferenceTarget
	AuthorityMark
	OutlineOn
	OutlineNumber
	MathOn
	MathOff
	MathSubtotal
	PrinterCommand
	LanguageCode
	KerningCode
	StyleOn
	StyleOff
	StyleEndCodes
	RedlineOn
	RedlineOff
	StrikeoutOn
	StrikeoutOff
	ItalicsOn
	ItalicsOff
	PageNumberPosition
	SuppressPageNumber
)

// Token is an independent inspection value. Raw always retains the exact native
// bytes, even for an opaque token whose movement/presentation is unsupported.
type Token struct {
	Kind Kind
	Span wp51.Span
	Raw  []byte
}

// Document must be constructed by Parse or New. It retains one immutable dependency
// image and a compact private absolute-gap index, with no mutable document state.
type Document struct{ state *revisionState }

// A caller may copy or replace the exported Document wrapper. Cursor and
// Revision capture this private immutable state, never that mutable wrapper.
// No state pointer, image pointer or gap slice is exposed to callers.
type revisionState struct {
	image           *wp51.Image
	gaps            []uint32
	birth           *birthLineage
	openWordRestore bool
	initialCodes    wp51.Span
	initialSpacing  int
}

func (s *revisionState) valid() bool {
	return s != nil && s.image != nil && s.birth != nil && len(s.gaps) > 0
}

// Parse delegates all native validity decisions to the approved reader. The
// following indexing pass only locates already-validated token spans; it does not
// decode opaque payloads, nested text, paired-code relationships or edit safety.
func Parse(input []byte) (*Document, error) { return parseRevision(input, nil) }

// One native parser/indexer. A nil birth means an explicit Loaded acquisition;
// internal validation and New supply their captured immutable lineage.
func parseRevision(input []byte, birth *birthLineage) (*Document, error) {
	image, err := wp51.Parse(input)
	if err != nil {
		return nil, err
	}
	info := image.Inspect()
	if info.OuterTokenCount > MaxTokens {
		return nil, failure(TokenLimit, -1, info.Body)
	}
	body, _ := image.Bytes(info.Body)
	gaps := make([]uint32, info.OuterTokenCount+1)
	offset := 0
	for i := 0; i < info.OuterTokenCount; i++ {
		gaps[i] = uint32(info.Body.Offset + offset)
		offset += framedWidth(body[offset:])
	}
	gaps[len(gaps)-1] = uint32(info.Body.Offset + len(body))
	if birth == nil {
		birth = &birthLineage{kind: loadedBirth, originalImage: image}
	}
	state := &revisionState{image: image, gaps: gaps, birth: birth}
	for _, packet := range info.Packets {
		if packet.Type != initialCodesPacket {
			continue
		}
		if state.initialCodes.Offset != 0 {
			state.initialSpacing = 0
			break
		}
		state.initialCodes = packet.Data
		if packet.Data.Length == 12 {
			raw, _ := image.Bytes(packet.Data)
			state.initialSpacing = initialSpacingValue(raw)
		}
	}
	return &Document{state: state}, nil
}

// These SDK WP51 outer-width facts are used only after wp51.Parse has checked
// every delimiter/length/bound. Reusing their span lengths is not another native
// validator or permission to interpret payloads. In particular C0 remains opaque.
func framedWidth(raw []byte) int {
	lead := raw[0]
	if lead < 0xc0 {
		return 1
	}
	if lead < 0xd0 {
		return [...]int{4, 9, 11, 3, 3, 5, 6, 7, 4, 5, 6, 6, 8, 10, 10, 12}[lead-0xc0]
	}
	return int(binary.LittleEndian.Uint16(raw[2:4])) + 4
}

const hardReturnByte = 0x0a

// Everyday native facts observed in the approved WP78 reference exports
// (docs/research/everyday-contract-2026-11-05/REPORT.md, r2/r3 EVERY.WP):
// a soft return is one control byte 0D, a hard page is 0C, attribute ON is
// C3 <type> C3 and OFF is C4 <type> C4 with type 0C Bold and 0E Underline.
// Developer's Toolkit function 195/196 corroborate the paired encoding.
// These are the observed values, not an invitation to generalise any other
// attribute type or field payload.
const (
	softReturnByte    = 0x0d
	deletedSoftReturn = 0x90
	softPageByte      = 0x0b
	deletedSoftPage   = 0x91
	hardPageByte      = 0x0c
	attributeOn       = 0xc3
	attributeOff      = 0xc4
	boldAttribute     = 0x0c
	underlineAttr     = 0x0e
	tabLead           = 0xc1
	tabMark           = 0x02
	tabWidth          = 9
	// Developer's Toolkit Format Group 212 subfunction 0, "End of Page": the
	// observed DOS 5.1 capture carries length 0x1C (= record size - 4), a zero
	// group-0 marker and group-0 length 0x16. WPWin's variant is documented as a
	// different group length, so only the observed DOS value is admitted here.
	endOfPageLead      = 0xd4
	endOfPageGroup     = 0x00
	endOfPageGroupLen  = 0x16
	hardReturnPageByte = 0x8c
	dormantReturnByte  = 0x99
)

func identify(raw []byte) Kind {
	if len(raw) > 1 && raw[0] == 0xd7 && (raw[1] == 7 || raw[1] == 8) {
		if ref, ok := readCrossReference(raw); ok {
			if ref.Target {
				return ReferenceTarget
			}
			return PageReference
		}
		return Opaque
	}
	switch {
	case len(raw) == 1 && raw[0] == 0xa1:
		return MathSubtotal
	case len(raw) == 1 && raw[0] == 0xa7:
		return MathOn
	case len(raw) == 1 && raw[0] == 0xa8:
		return MathOff
	case len(raw) == 1 && raw[0] == hardReturnByte:
		return HardReturn
	case len(raw) == 1 && raw[0] == softReturnByte:
		return SoftReturn
	case len(raw) == 1 && raw[0] == deletedSoftReturn:
		return DeletedSoftReturn
	case len(raw) == 1 && raw[0] == softPageByte:
		return SoftPage
	case len(raw) == 1 && raw[0] == deletedSoftPage:
		return DeletedSoftPage
	case len(raw) == 1 && raw[0] == hardPageByte:
		return HardPage
	case len(raw) == 1 && raw[0] == hardReturnPageByte:
		return HardReturnSoftPage
	case len(raw) == 1 && raw[0] == dormantReturnByte:
		return DormantHardReturn
	case len(raw) == 1 && raw[0] == 0xa0:
		return HardSpace
	case len(raw) == 1 && isDOSControl(raw[0]):
		return DOSControl
	case len(raw) == 1 && (raw[0] == endAlignmentByte || raw[0] == inlineAlignmentByte):
		return EndAlignment
	case spacingKind(raw):
		return LineSpacing
	case lineHeightKind(raw):
		return LineHeight
	case justificationKind(raw):
		return ParagraphJustification
	case justificationCache(raw):
		return ParagraphPosition
	case kerningOwner(raw):
		return KerningCode
	case languageOwner(raw):
		return LanguageCode
	case pageNumberPositionKind(raw):
		return PageNumberPosition
	case bytes.Equal(raw, suppressPageNumberOwner):
		return SuppressPageNumber
	case lineNumberKind(raw):
		return LineNumbering
	case bytes.Equal(raw, styleBodyEnd[:]):
		return StyleEndCodes
	case contentsDefinitionLevels(raw) != 0:
		return ContentsDefinition
	case len(raw) == 1 && raw[0] == 0x9b:
		return ContentsEnd
	case isOutlineStart(raw):
		return OutlineOn
	case isAuthority(raw):
		return AuthorityMark
	case isSubdocument(raw):
		return Subdocument
	case tocMarkKind(raw):
		return ContentsMark
	case dateCodeKind(raw):
		return DateCode
	case footnoteOptionsKind(raw):
		return FootnoteOptions
	case tabSetKind(raw):
		return TabSetCode
	case conditionalPageKind(raw):
		return ConditionalPage
	case len(raw) == 1 && raw[0] == 0x8a:
		return WidowProtectionOn
	case len(raw) == 1 && raw[0] == 0x8b:
		return WidowProtectionOff
	case len(raw) == 11 && raw[0] == 0xc2 && raw[1] <= 1 && raw[10] == 0xc2 &&
		validIndentPosition(raw[6:8]):
		if raw[1] == 1 {
			return DoubleIndent
		}
		return Indent
	case len(raw) == 6 && raw[0] == 0xc6 && raw[5] == 0xc6 &&
		validIndentPosition(raw[3:5]) && (binary.LittleEndian.Uint16(raw[1:3]) == 9000 ||
		int(binary.LittleEndian.Uint16(raw[1:3]))+int(binary.LittleEndian.Uint16(raw[3:5])) == 10200 ||
		bytes.Equal(raw, []byte{0xc6, 0xd0, 0x20, 0x60, 9, 0xc6})):
		return EndIndent
	case len(raw) == 9 && raw[0] == 0xc1 && raw[1] == 0x80 && raw[8] == 0xc1 &&
		raw[6] >= 10 && raw[6] <= 75 && raw[7] == 0 && (raw[6]-10)%5 == 0 &&
		binary.LittleEndian.Uint16(raw[2:4]) == uint16(raw[6])*120 && bytes.Equal(raw[2:4], raw[4:6]):
		return MarginRelease
	case len(raw) == 14 && raw[0] == 0xd3 && raw[1] == 4 && raw[2] == 10 && raw[3] == 0 &&
		raw[10] == 10 && raw[11] == 0 && raw[12] == 4 && raw[13] == 0xd3:
		return PageNumberReset
	case len(raw) == 5 && raw[0] == 0xc5 && raw[4] == 0xc5 && binary.LittleEndian.Uint16(raw[2:4])%200 == 0 && binary.LittleEndian.Uint16(raw[2:4]) >= 200:
		if raw[1] == 0 {
			return BlockProtectOn
		}
		if raw[1] == 1 {
			return BlockProtectOff
		}
		return Opaque
	case endOfPageShaped(raw):
		return EndOfPage
	case len(raw) == 8 && raw[0] == 0xde && raw[7] == 0xde &&
		raw[2] == 4 && raw[3] == 0 && raw[4] == 4 && raw[5] == 0 && raw[6] == raw[1]:
		return fixedMergeKind(raw[1])
	case len(raw) == 10 && raw[0] == 0xde && raw[1] == 0x34 &&
		raw[2] == 6 && raw[3] == 0 && binary.LittleEndian.Uint16(raw[4:6]) > 0 &&
		binary.LittleEndian.Uint16(raw[4:6]) <= MaxMergeRecordFields+1 &&
		raw[6] == 6 && raw[7] == 0 && raw[8] == 0x34 && raw[9] == 0xde:
		return MergeEndRecord
	case len(raw) == 4 && raw[0] == 0xc0 && raw[3] == 0xc0 && validExtendedCharacter(raw[2], raw[1]):
		return ExtendedCharacter
	case len(raw) == 1 && raw[0] >= 0x20 && raw[0] <= 0x7e:
		return ASCII
	case len(raw) == 3 && raw[0] == raw[2] && (raw[0] == attributeOn || raw[0] == attributeOff):
		on := raw[0] == attributeOn
		switch raw[1] {
		case 8:
			if on {
				return ItalicsOn
			}
			return ItalicsOff
		case 10:
			if on {
				return RedlineOn
			}
			return RedlineOff
		case 13:
			if on {
				return StrikeoutOn
			}
			return StrikeoutOff
		case boldAttribute:
			if on {
				return BoldOn
			}
			return BoldOff
		case underlineAttr:
			if on {
				return UnderlineOn
			}
			return UnderlineOff
		}
		return Opaque
	}
	if _, ok := outlineNumberFields(raw); ok {
		return OutlineNumber
	}
	if _, ok := decodeStyleOwner(raw); ok {
		if raw[1] == 0 {
			return StyleOn
		}
		return StyleOff
	}
	if isPrinterCommand(raw) {
		return PrinterCommand
	}
	if _, ok := commentText(raw); ok {
		return Comment
	}
	if kind := alignmentKind(raw); kind != Opaque {
		return kind
	}
	if kind := marginKind(raw); kind != Opaque {
		return kind
	}
	if note, ok := parseNote(raw); ok {
		if note.End {
			return Endnote
		}
		return Footnote
	}
	if _, ok := readPageText(raw); ok {
		return PageTextCode
	}
	// DOS Text Retrieve stores a Tab with an empty position cache.
	if bytes.Equal(raw, dosTextTab) || bytes.Equal(raw, outlineIndent[:]) || len(raw) == tabWidth && raw[0] == tabLead && raw[1] == tabMark && raw[tabWidth-1] == tabLead {
		return Tab
	}
	return Opaque
}

// endOfPageShaped validates the observed D4 subfunction-0 record structurally:
// delimiters, the declared length against the actual owner width, the group-0
// marker and the observed DOS group-0 length. It deliberately does not interpret
// page geometry, page numbers, formatter lines or footnote counts — those are
// preserved literally and belong to the layout engine.
func endOfPageShaped(raw []byte) bool {
	if len(raw) < 8 || raw[0] != endOfPageLead || raw[len(raw)-1] != endOfPageLead {
		return false
	}
	if raw[1] != endOfPageGroup || binary.LittleEndian.Uint16(raw[2:4]) != uint16(len(raw)-4) {
		return false
	}
	return raw[4] == endOfPageGroup && raw[5] == endOfPageGroupLen
}

// displayText is the single Reveal/normal label source for every view, so the
// presentation window and the inspected catalogue cannot drift apart. Normal
// text is derived display only; the Tab separator is provisional until WP81
// computes real tab stops, and no view text is ever serializer input.
func displayText(kind Kind, raw []byte, reveal bool) string {
	switch kind {
	case ASCII:
		return string(raw)
	case Footnote, Endnote:
		return noteDisplay(kind, raw, reveal)
	case StyleOn, StyleOff:
		if reveal {
			style, _ := decodeStyleOwner(raw)
			if kind == StyleOn {
				return "[Style On:" + style.Name + "]"
			}
			return "[Style Off:" + style.Name + "]"
		}
		return ""
	case ContentsDefinition:
		if reveal {
			return fmt.Sprintf("[Def Mark:ToC,%d:5]", contentsDefinitionLevels(raw))
		}
		return ""
	case ContentsEnd:
		if reveal {
			return "[End Def]"
		}
		return ""
	case ContentsLeader:
		if reveal {
			return "[Flsh Rgt]"
		}
		return ""
	case PageReference, ReferenceTarget:
		ref, _ := readCrossReference(raw)
		if reveal {
			if ref.Target {
				return "[Target(" + ref.Name + ")]"
			}
			return "[Ref(" + ref.Name + "):Pg " + ref.Value + "]"
		}
		return ref.Value
	case KerningCode:
		if reveal {
			if raw[5] == 1 {
				return "[Kern:On]"
			}
			return "[Kern:Off]"
		}
		return ""
	case LanguageCode:
		if reveal {
			return "[Lang:" + string(raw[6:8]) + "]"
		}
		return ""
	case PrinterCommand:
		if reveal {
			return printerCommandLabel(raw)
		}
		return ""
	case MathSubtotal:
		if reveal {
			return "[+]"
		}
		return "+"
	case MathOn, MathOff:
		if reveal {
			if kind == MathOn {
				return "[Math On]"
			}
			return "[Math Off]"
		}
		return ""
	case OutlineOn:
		if reveal {
			return "[Outline On]"
		}
		return ""
	case OutlineNumber:
		if reveal {
			return "[Par Num:Auto]"
		}
		number, _ := outlineNumberFields(raw)
		return number.text
	case AuthorityMark:
		if reveal {
			section, short, _, _ := authorityFields(raw)
			return fmt.Sprintf("[ToA:%d;%s;Full Form]", section, short)
		}
		return ""
	case Subdocument:
		if reveal {
			name, _ := subdocumentName(raw)
			return "[Subdoc:" + name + "]"
		}
		return ""
	case ContentsMark:
		if reveal {
			return tocMarkLabel(raw)
		}
		return ""
	case Comment:
		if reveal {
			return "[Comment]"
		}
		return ""
	case DateCode:
		if reveal {
			return "[Date:" + defaultDateFormat + "]"
		}
		return ""
	case FootnoteOptions:
		if reveal {
			return "[Ftn Opt]"
		}
		return ""
	case PageTextCode:
		if reveal {
			return pageTextLabel(raw)
		}
		return ""
	case LineMargins, PageMargins:
		if reveal {
			return marginLabel(kind, raw)
		}
		return ""
	case LineSpacing:
		if reveal {
			return fmt.Sprintf("[Ln Spacing:%d]", raw[7])
		}
		return ""
	case LineHeight:
		if reveal {
			height := (Token{Kind: kind, Raw: raw}).LineHeight()
			if height == 0 {
				return "[Ln Height:Auto]"
			}
			return fmt.Sprintf("[Ln Height:%g\"]", float64(height)/UnitsPerInch)
		}
		return ""
	case ParagraphJustification:
		if reveal {
			return "[Just:" + Justification(raw[5]).String() + "]"
		}
		return ""
	case TabSetCode:
		if reveal {
			return tabSetLabel(raw)
		}
		return ""
	case SoftDecimalTab:
		if reveal {
			return "[Dec Tab]"
		}
		return ""
	case DecimalTab:
		if reveal {
			return "[DEC TAB]"
		}
		return ""
	case PageNumberPosition:
		if reveal {
			return "[Pg Numbering:" + PageNumberPositionName(int(raw[7])) + "]"
		}
		return ""
	case SuppressPageNumber:
		if reveal {
			return "[Suppress:PgNum]"
		}
		return ""
	case LineNumbering:
		if reveal {
			if raw[9] == 0xa1 {
				return "[Ln Num:On]"
			}
			return "[Ln Num:Off]"
		}
		return ""
	case ConditionalPage:
		if reveal {
			return fmt.Sprintf("[Cndl EOP:%d]", raw[4])
		}
		return ""
	case WidowProtectionOn, WidowProtectionOff:
		if reveal {
			if kind == WidowProtectionOn {
				return "[W/O On]"
			}
			return "[W/O Off]"
		}
		return ""
	case CenterLine, FlushRight, EndAlignment:
		if reveal {
			switch kind {
			case CenterLine:
				return "[Center]"
			case FlushRight:
				return "[Flsh Rgt]"
			case EndAlignment:
				if raw[0] == inlineAlignmentByte {
					return "[End C/A]"
				}
			}
		}
		return ""
	case HardSpace:
		if reveal {
			return "[ ]"
		}
		return " "
	case ExtendedCharacter:
		return CharacterGlyph(raw[2], raw[1])
	case DOSControl:
		return string([]byte{'^', raw[0] + '@'})
	case HardReturn:
		if reveal {
			return "[HRt]"
		}
		return "\n"
	case SoftReturn:
		if reveal {
			return "[SRt]"
		}
		return "\n"
	case DeletedSoftReturn, DeletedSoftPage:
		if reveal {
			return "[DSRt]"
		}
		return ""
	case SoftPage:
		if reveal {
			return "[SPg]"
		}
		return ""
	case HardReturnSoftPage:
		if reveal {
			return "[HRt-SPg]"
		}
		return ""
	case DormantHardReturn:
		if reveal {
			return "[Dorm HRt]"
		}
		return ""
	case BlockProtectOn:
		if reveal {
			return "[Block Pro:On]"
		}
		return ""
	case BlockProtectOff:
		if reveal {
			return "[Block Pro:Off]"
		}
		return ""
	case EndOfPage:
		return ""
	case HardPage:
		if reveal {
			return "[HPg]"
		}
		return ""
	case Indent:
		if reveal {
			return "[Indent]"
		}
		return ""
	case DoubleIndent:
		if reveal {
			return "[Indent→←]"
		}
		return ""
	case MarginRelease:
		if reveal {
			return "[←Mar Rel]"
		}
		return ""
	case EndIndent:
		if reveal {
			return "[End Indent]"
		}
		return ""
	case Tab:
		if reveal {
			return "[Tab]"
		}
		return "	"
	case RedlineOn, RedlineOff, StrikeoutOn, StrikeoutOff, ItalicsOn, ItalicsOff:
		if reveal {
			return [...]string{"[REDLN]", "[redln]", "[STKOUT]", "[stkout]", "[ITALC]", "[italc]"}[kind-RedlineOn]
		}
		return ""
	case BoldOn:
		if reveal {
			return "[BOLD]"
		}
	case BoldOff:
		if reveal {
			return "[bold]"
		}
	case UnderlineOn:
		if reveal {
			return "[UND]"
		}
	case UnderlineOff:
		if reveal {
			return "[und]"
		}
	case MergeField, MergeEndField, MergeEndRecord, MergePageOff, MergePageOn, MergeNestPrimary, MergeNestSecondary, MergeIfBlank, MergeElse, MergeEndIf, MergeBreak:
		return kind.MergeLabel(reveal)
	}
	return ""
}

// MergeLabel returns the observed display label of a recognized merge owner.
// Operands and following native owners are separate tokens.
func (k Kind) MergeLabel(reveal bool) string {
	var name string
	switch k {
	case MergeField:
		name = "FIELD"
	case MergeEndField:
		name = "END FIELD"
	case MergeEndRecord:
		name = "END RECORD"
	case MergePageOff:
		name = "PAGE OFF"
	case MergePageOn:
		name = "PAGE ON"
	case MergeNestPrimary:
		name = "NEST PRIMARY"
	case MergeNestSecondary:
		name = "NEST SECONDARY"
	case MergeIfBlank:
		name = "IF BLANK"
	case MergeElse:
		name = "ELSE"
	case MergeEndIf:
		name = "END IF"
	case MergeBreak:
		name = "BREAK"
	default:
		return ""
	}
	if reveal {
		return "[Mrg:" + name + "]"
	}
	return "{" + name + "}"
}

func (d *Document) valid() bool { return d != nil && d.state.valid() }
func (d *Document) TokenCount() int {
	if !d.valid() {
		return 0
	}
	return len(d.state.gaps) - 1
}
func (d *Document) Export() ([]byte, error) {
	if !d.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	return d.state.image.Export(), nil
}
func (d *Document) span(index int) wp51.Span {
	return wp51.Span{Offset: int(d.state.gaps[index]), Length: int(d.state.gaps[index+1] - d.state.gaps[index])}
}
func (d *Document) Token(index int) (Token, error) {
	if !d.valid() {
		return Token{}, failure(InvalidDocument, index, noSpan)
	}
	if index < 0 || index >= d.TokenCount() {
		return Token{}, failure(InvalidPosition, index, noSpan)
	}
	span := d.span(index)
	raw, _ := d.state.image.Bytes(span)
	return Token{Kind: identify(raw), Span: span, Raw: raw}, nil
}

// Cursor is a value: view and movement operations return a new cursor, preserving
// the caller's previous cursor on failure. Its document remains immutable.
type Cursor struct {
	state  *revisionState
	gap    int
	reveal bool
}

// CursorAt constructs a valid token-gap coordinate, not an original GoTo/Home
// command. Zero and TokenCount are the body boundaries, never byte positions.
func (d *Document) CursorAt(gap int) (Cursor, error) {
	if !d.valid() {
		return Cursor{}, failure(InvalidDocument, -1, noSpan)
	}
	if gap < 0 || gap > d.TokenCount() {
		return Cursor{}, failure(InvalidPosition, gap, noSpan)
	}
	return Cursor{state: d.state, gap: gap}, nil
}
func (c Cursor) Gap() int                    { return c.gap }
func (c Cursor) Reveal() bool                { return c.reveal }
func (c Cursor) WithReveal(show bool) Cursor { c.reveal = show; return c }
func (c Cursor) Offset() (int, error) {
	if !c.state.valid() {
		return 0, failure(InvalidDocument, -1, noSpan)
	}
	return int(c.state.gaps[c.gap]), nil
}
func (c Cursor) Move(direction int) (Cursor, error) {
	d := &Document{state: c.state}
	if !c.state.valid() {
		return c, failure(InvalidDocument, -1, noSpan)
	}
	if direction != -1 && direction != 1 {
		return c, failure(InvalidDirection, c.gap, noSpan)
	}
	target := c.gap + direction
	if target < 0 || target > d.TokenCount() {
		return c, failure(InvalidPosition, target, noSpan)
	}
	index := c.gap
	if direction < 0 {
		index--
	}
	token, _ := d.Token(index)
	if token.Kind == Opaque {
		return c, failure(UnsupportedToken, index, token.Span)
	}
	c.gap = target
	return c, nil
}

// Element preserves source/token identity in both views, including the empty
// normal text of Bold codes. Text is derived display, never native serialization.
type Element struct {
	TokenIndex int
	Kind       Kind
	Span       wp51.Span
	Text       string
}
type Presentation struct {
	StartGap, EndGap, CursorGap int
	Reveal                      bool
	Elements                    []Element
}

// Present renders a bounded token window, refusing an opaque token before
// returning any elements. It does not wrap, count terminal cells or infer layout.
func (c Cursor) Present(start, count int) (Presentation, error) {
	d := &Document{state: c.state}
	if !d.valid() {
		return Presentation{}, failure(InvalidDocument, -1, noSpan)
	}
	if start < 0 || start > d.TokenCount() || count < 0 || count > d.TokenCount()-start {
		return Presentation{}, failure(InvalidPosition, start, noSpan)
	}
	if count > MaxWindowTokens {
		return Presentation{}, failure(WindowLimit, start, noSpan)
	}
	// Acquire only the requested contiguous window, not the full body. Indexes
	// already identify valid complete-token spans, so this remains input bounded.
	window := wp51.Span{Offset: int(d.state.gaps[start]), Length: int(d.state.gaps[start+count] - d.state.gaps[start])}
	raw, _ := d.state.image.Bytes(window)
	for i := start; i < start+count; i++ {
		span := d.span(i)
		local := span.Offset - window.Offset
		if identify(raw[local:local+span.Length]) == Opaque {
			return Presentation{}, failure(UnsupportedToken, i, span)
		}
	}
	p := Presentation{StartGap: start, EndGap: start + count, CursorGap: c.gap, Reveal: c.reveal, Elements: make([]Element, count)}
	for i := start; i < start+count; i++ {
		span := d.span(i)
		local := span.Offset - window.Offset
		token := raw[local : local+span.Length]
		kind := identify(token)
		text := displayText(kind, token, c.reveal)
		p.Elements[i-start] = Element{TokenIndex: i, Kind: kind, Span: span, Text: text}
	}
	return p, nil
}
