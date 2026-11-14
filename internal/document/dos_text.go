package document

import (
	"encoding/binary"
	"fmt"
	"time"
)

// DOS code page 437 to native WordPerfect set and character number.
// Captured from US WordPerfect 5.1 DOS Text Retrieve for bytes 7F–FE.
// The same converter drops FF and stops at DOS EOF (1A).
var dosTextCharacters = [...]struct{ set, number byte }{
	{5, 12}, {1, 38}, {1, 71}, {1, 41}, {1, 29}, {1, 31}, {1, 33}, {1, 35},
	{1, 39}, {1, 43}, {1, 45}, {1, 47}, {1, 53}, {1, 51}, {1, 55}, {1, 30},
	{1, 34}, {1, 40}, {1, 37}, {1, 36}, {1, 61}, {1, 63}, {1, 65}, {1, 69},
	{1, 73}, {1, 139}, {1, 62}, {1, 70}, {4, 19}, {4, 11}, {4, 12}, {4, 13},
	{4, 14}, {1, 27}, {1, 49}, {1, 59}, {1, 67}, {1, 57}, {1, 56}, {4, 15},
	{4, 16}, {4, 8}, {5, 16}, {6, 20}, {4, 17}, {4, 18}, {4, 7}, {4, 9},
	{4, 10}, {3, 0}, {3, 1}, {3, 2}, {3, 9}, {3, 16}, {3, 40}, {3, 44},
	{3, 35}, {3, 31}, {3, 27}, {3, 20}, {3, 22}, {3, 23}, {3, 36}, {3, 32},
	{3, 11}, {3, 13}, {3, 17}, {3, 15}, {3, 14}, {3, 8}, {3, 18}, {3, 38},
	{3, 42}, {3, 24}, {3, 21}, {3, 28}, {3, 26}, {3, 25}, {3, 19}, {3, 29},
	{3, 45}, {3, 41}, {3, 43}, {3, 39}, {3, 37}, {3, 33}, {3, 30}, {3, 34},
	{3, 46}, {3, 47}, {3, 12}, {3, 10}, {3, 3}, {3, 7}, {3, 4}, {3, 6},
	{3, 5}, {8, 1}, {1, 23}, {8, 6}, {8, 33}, {8, 36}, {8, 37}, {8, 25},
	{8, 41}, {8, 44}, {8, 16}, {8, 50}, {8, 9}, {6, 19}, {8, 45}, {8, 11},
	{6, 16}, {6, 14}, {6, 1}, {6, 3}, {6, 2}, {7, 0}, {7, 1}, {6, 8},
	{6, 13}, {6, 36}, {6, 31}, {6, 32}, {7, 4}, {4, 21}, {4, 20}, {4, 2},
}

var dosTextTab = []byte{0xc1, 0, 0, 0, 0, 0, 0, 0, 0xc1}

// DOS Text Retrieve preserves these single-byte native owners. The line,
// page, tab and EOF controls are interpreted by the converter instead.
func isDOSControl(b byte) bool {
	return b <= 0x08 || b >= 0x0e && b <= 0x19 || b >= 0x1b && b <= 0x1f
}

// InsertDOSText imports a bounded DOS byte stream as one editing operation.
// DOS preserves the input line lengths on retrieval. A later edit can reflow
// the imported soft returns in the same way as other native soft returns.
func (d *Document) InsertDOSText(c Cursor, raw []byte, softReturns bool) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	body, count, err := convertDOSText(raw, softReturns)
	if err != nil {
		return unchangedEdit(d, c), err
	}
	// Retrieve leaves the cursor before the inserted text.
	return d.insertEverydayBody(c, body, count, c.gap)
}

func convertDOSText(raw []byte, softReturns bool) ([]byte, int, error) {
	var body []byte
	count, column := 0, 0
	// With the standard DOS setup (65 columns, default hyphenation zone),
	// DOS starts emitting soft returns at input column 59.
	const zoneStart = 59
	inReturnRun := false
	for i := 0; i < len(raw); i++ {
		b := raw[i]
		if b == 0x1a {
			break
		}
		switch {
		case b == '\r' && (i+1 == len(raw) || raw[i+1] != '\n'):
			continue
		case b == '\r' || b == '\n':
			crlf := b == '\r'
			if crlf {
				i++
			}
			next := raw[i+1:]
			followedByReturn := len(next) > 0 && (next[0] == '\n' || len(next) > 1 && next[0] == '\r' && next[1] == '\n')
			atEnd := len(next) == 0 || next[0] == 0x1a
			if softReturns && crlf && atEnd && !inReturnRun {
				continue
			}
			ret := byte(hardReturnByte)
			if softReturns && crlf && !inReturnRun && !followedByReturn && column >= zoneStart {
				ret = softReturnByte
			}
			body = append(body, ret)
			column, inReturnRun = 0, true
		case b == 0xff:
			continue
		default:
			inReturnRun = false
			switch {
			case b == '\f':
				body = append(body, hardPageByte)
				column = 0
			case b == softPageByte:
				body = append(body, softPageByte)
				column = 0
			case b == '\t':
				body = append(body, dosTextTab...)
				column += 5 - column%5
			case isDOSControl(b):
				body = append(body, b)
				column += 2
			case b >= 32 && b <= 126:
				body = append(body, b)
				column++
			case b >= 127:
				ch := dosTextCharacters[b-127]
				body = append(body, CharacterBytes(ch.set, ch.number)...)
				column++
			default:
				return nil, 0, fmt.Errorf("unsupported DOS text control byte %02X at offset %d", b, i)
			}
		}
		count++
		if count > MaxMutationTokens || len(body) > MaxMutationBytes {
			return nil, 0, failure(MutationLimit, -1, noSpan)
		}
	}
	return body, count, nil
}

// ExportDOSText writes the document's text using the original DOS encoding.
func (d *Document) ExportDOSText() ([]byte, error) { return d.ExportDOSTextAt(time.Now()) }

func (d *Document) ExportDOSTextAt(now time.Time) ([]byte, error) {
	if !d.valid() {
		return nil, failure(InvalidDocument, -1, noSpan)
	}
	var out []byte
	column := 0
	alignedColumn := 0
	left := 10
	customRuler := false
	for i := 0; i < d.TokenCount(); i++ {
		token, err := d.Token(i)
		if err != nil {
			return nil, err
		}
		if token.Kind.IsCharacter() || token.Kind == DOSControl || token.Kind == Tab || token.Kind == DateCode || token.Kind == PageReference || token.Kind == OutlineNumber {
			for column < alignedColumn {
				out = append(out, ' ')
				column++
			}
			alignedColumn = 0
		}
		switch token.Kind {
		case LineMargins:
			margin, _, _ := token.LineMargins()
			left = margin / 120
		case TabSetCode:
			customRuler = true
		case CenterLine, FlushRight, DecimalTab, SoftDecimalTab, ParagraphPosition:
			position := 0
			if token.Kind == ParagraphPosition {
				position = int(binary.LittleEndian.Uint16(token.Raw[4:6]))
			} else {
				units := int(binary.LittleEndian.Uint16(token.Raw[2:4]))
				position = units / 120
			}
			// DOS text output omits ordinary page margins but keeps the
			// horizontal positioning introduced by alignment owners.
			alignedColumn = max(0, position-left)
		case OutlineNumber:
			text := token.OutlineText()
			out = append(out, text...)
			column += len(text)
		case PageReference:
			ref, _ := token.CrossReference()
			out = append(out, ref.Value...)
			column += len(ref.Value)
		case DateCode:
			date := FormatDate(now)
			out = append(out, date...)
			column += len(date)
		case ASCII:
			out = append(out, token.Raw[0])
			column++
		case HardSpace:
			out = append(out, ' ')
			column++
		case DOSControl:
			if token.Raw[0] != 0 {
				out = append(out, token.Raw[0])
				column += 2
			}
		case ExtendedCharacter:
			found := false
			for code, ch := range dosTextCharacters {
				if ch.set == token.Raw[2] && ch.number == token.Raw[1] {
					out = append(out, byte(code+127))
					column++
					found = true
					break
				}
			}
			if !found {
				return nil, fmt.Errorf("character %d,%d has no DOS text equivalent", token.Raw[2], token.Raw[1])
			}
		case HardReturn, SoftReturn, DeletedSoftReturn:
			out = append(out, '\r', '\n')
			column = 0
			alignedColumn = 0
		case SoftPage:
			if i > 0 {
				prior, _ := d.Token(i - 1)
				if prior.Kind == EndOfPage {
					out = append(out, '\f')
					column = 0
					continue
				}
			}
			out = append(out, ' ')
			column++
		case HardPage, DeletedSoftPage, HardReturnSoftPage:
			out = append(out, '\f')
			column, alignedColumn = 0, 0
		case Tab:
			spaces := 5 - column%5
			if customRuler && matchedEverydayTab(token.Raw) {
				target := int(binary.LittleEndian.Uint16(token.Raw[6:8])) - left
				spaces = max(0, target-column)
			}
			for _ = range spaces {
				out = append(out, ' ')
			}
			column += spaces
		case EndOfPage, DormantHardReturn, BoldOn, BoldOff, UnderlineOn, UnderlineOff, RedlineOn, RedlineOff, StrikeoutOn, StrikeoutOff, ItalicsOn, ItalicsOff, PageNumberPosition, SuppressPageNumber,
			PageMargins, LineHeight, LineSpacing, ParagraphJustification, EndAlignment, Comment, ContentsMark, StyleOn, StyleOff, StyleEndCodes, ContentsDefinition, ContentsEnd, Subdocument, ReferenceTarget, AuthorityMark, OutlineOn, MathOn, MathOff, MathSubtotal, PrinterCommand, LanguageCode, KerningCode:
			// These codes have no separate text representation.
		default:
			return nil, failure(UnsupportedBody, i, token.Span)
		}
	}
	return append(out, 0x1a), nil
}
