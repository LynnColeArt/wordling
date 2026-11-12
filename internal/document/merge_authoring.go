package document

import (
	"bytes"
	"encoding/binary"
	"strconv"

	"github.com/lynncoleart/wordling/internal/merge/native"
)

// MergeCode names an observed structural editing command, not an arbitrary
// function frame. The native bytes are owned by the document layer.
type MergeCode uint8

const (
	AuthorMergeField MergeCode = iota + 1
	AuthorMergeEndField
	AuthorMergeEndRecord
	AuthorMergeHardPage
	AuthorMergeHardReturn
)

var (
	mergeFieldOwner     = []byte{0xde, 0x36, 4, 0, 4, 0, 0x36, 0xde}
	mergeEndFieldOwner  = []byte{0xde, 0x31, 4, 0, 4, 0, 0x31, 0xde}
	mergeEndRecordOwner = []byte{0xde, 0x34, 6, 0, 2, 0, 6, 0, 0x34, 0xde}
)

type mergeOperandKind uint8

const (
	noMergeOperand mergeOperandKind = iota
	numericMergeOperand
	filenameMergeOperand
)

type mergeAuthoringGap struct {
	page, row     uint16
	column, field int
	editable      bool
	operand       mergeOperandKind
}

type mergeAuthoringBody struct {
	gaps                      []mergeAuthoringGap
	primary, secondary, codes bool
}

// mergeAuthoring checks every owner, including the generated page cache. It
// admits incomplete authoring states while protecting framed codes, operands
// and the interior gap of a paired page cache.
func (d *Document) mergeAuthoring() (mergeAuthoringBody, error) {
	if _, err := d.prefixMutationAdmission(); err != nil {
		return mergeAuthoringBody{}, err
	}
	if d.TokenCount() > MaxMutationTokens {
		return mergeAuthoringBody{}, failure(MutationLimit, -1, noSpan)
	}
	body := mergeAuthoringBody{gaps: make([]mergeAuthoringGap, d.TokenCount()+1)}
	at := mergeAuthoringGap{page: 1, field: 1, editable: true}
	for i := 0; i < d.TokenCount(); {
		body.gaps[i] = at
		token, _ := d.Token(i)
		switch token.Kind {
		case ASCII:
			at.column++
		case MergeField, MergeIfBlank, MergeNestPrimary, MergeNestSecondary:
			body.secondary = body.secondary || token.Kind == MergeNestSecondary
			body.primary = body.primary || token.Kind != MergeNestSecondary
			numeric := token.Kind == MergeField || token.Kind == MergeIfBlank
			operand := filenameMergeOperand
			if numeric {
				operand = numericMergeOperand
			}
			end, valid := d.mergeOperand(i, numeric)
			if !valid {
				return mergeAuthoringBody{}, failure(UnsupportedBody, i, token.Span)
			}
			for i++; i <= end; i++ {
				body.gaps[i] = at
				body.gaps[i].editable = false
				body.gaps[i].operand = operand
				at.column++
			}
			i = end
		case MergePageOff, MergePageOn, MergeBreak:
			body.codes = true
		case MergeElse, MergeEndIf:
			body.primary = true
		case MergeEndField:
			body.secondary = true
			next, tokenErr := d.Token(i + 1)
			if tokenErr != nil || next.Kind != HardReturn {
				return mergeAuthoringBody{}, failure(UnsupportedBody, i, token.Span)
			}
			at.field++
		case HardReturn:
			at.row++
			at.column = 0
		case MergeEndRecord:
			body.secondary = true
			next, tokenErr := d.Token(i + 1)
			if tokenErr != nil || next.Kind != EndOfPage || int(binary.LittleEndian.Uint16(token.Raw[4:6])) != at.field {
				return mergeAuthoringBody{}, failure(UnsupportedBody, i, token.Span)
			}
		case EndOfPage:
			next, tokenErr := d.Token(i + 1)
			if tokenErr != nil || next.Kind != HardPage || at.page == 65535 || !bytes.Equal(token.Raw, everydayPageRecord(at.page, at.row)) {
				return mergeAuthoringBody{}, failure(UnsupportedBody, i, token.Span)
			}
			i++
			body.gaps[i] = at
			body.gaps[i].editable = false
			at.page++
			at.row, at.column, at.field = 0, 0, 1
		default:
			return mergeAuthoringBody{}, failure(UnsupportedBody, i, token.Span)
		}
		if at.column > 65 || at.row > lastEverydayPageRow || body.primary && body.secondary {
			return mergeAuthoringBody{}, failure(UnsupportedBody, i, token.Span)
		}
		i++
	}
	body.gaps[d.TokenCount()] = at
	return body, nil
}

func (d *Document) IsAuthoredMergeSource() bool {
	body, err := d.mergeAuthoring()
	return err == nil && (body.primary || body.secondary || body.codes)
}

// MergeFieldAt reports the active data field for original secondary status.
func (d *Document) MergeFieldAt(c Cursor) (int, bool) {
	if !d.valid() || c.state != d.state || c.gap < 0 || c.gap > d.TokenCount() {
		return 0, false
	}
	body, err := d.mergeAuthoring()
	if err != nil || !body.secondary {
		return 0, false
	}
	return body.gaps[c.gap].field, true
}

func (d *Document) InsertMergeCode(c Cursor, code MergeCode, field int) (EditResult, error) {
	return d.editMergeOwners(c, false, func(body mergeAuthoringBody, at mergeAuthoringGap) (int, []byte, int, error) {
		switch code {
		case AuthorMergeField:
			if field >= 1 && field <= 999 && !body.secondary {
				raw := append([]byte{}, mergeFieldOwner...)
				raw = strconv.AppendInt(raw, int64(field), 10)
				raw = append(raw, '~')
				return 0, raw, 1 + len(raw) - len(mergeFieldOwner), nil
			}
		case AuthorMergeEndField:
			if !body.primary && c.gap == d.TokenCount() {
				raw := append([]byte{}, mergeEndFieldOwner...)
				return 0, append(raw, hardReturnByte), 2, nil
			}
		case AuthorMergeEndRecord:
			if !body.primary && c.gap == d.TokenCount() {
				raw := append([]byte{}, mergeEndRecordOwner...)
				binary.LittleEndian.PutUint16(raw[4:6], uint16(at.field))
				raw = append(raw, everydayPageRecord(at.page, at.row)...)
				return 0, append(raw, hardPageByte), 3, nil
			}
		case AuthorMergeHardReturn:
			if (body.primary || body.secondary || body.codes) && c.gap == d.TokenCount() {
				return 0, []byte{hardReturnByte}, 1, nil
			}
		case AuthorMergeHardPage:
			if body.primary && c.gap == d.TokenCount() {
				raw := everydayPageRecord(at.page, at.row)
				return 0, append(raw, hardPageByte), 2, nil
			}
		}
		return 0, nil, 0, failure(UnsupportedBody, c.gap, noSpan)
	})
}

// DeleteMergeCode removes only the selected recognized frame, preserving
// adjacent bytes. The original leaves a FIELD operand as ordinary text.
func (d *Document) DeleteMergeCode(c Cursor, backspace bool) (EditResult, error) {
	return d.deleteMerge(c, backspace, false)
}

// DeleteAuthoredMergeText deletes the adjacent printable token, or the
// observed whole owner in Reveal, without exposing a framing/terminator byte.
func (d *Document) DeleteAuthoredMergeText(c Cursor, backspace bool) (EditResult, error) {
	return d.deleteMerge(c, backspace, true)
}

func (d *Document) deleteMerge(c Cursor, backspace, textAllowed bool) (EditResult, error) {
	if backspace {
		if c.gap == 0 {
			return unchangedEdit(d, c), failure(InvalidPosition, 0, noSpan)
		}
		before := c
		before.gap--
		edit, err := d.deleteMerge(before, false, textAllowed)
		if err != nil {
			return unchangedEdit(d, c), err
		}
		return edit, nil
	}
	return d.editMergeOwners(c, textAllowed && c.reveal, func(body mergeAuthoringBody, at mergeAuthoringGap) (int, []byte, int, error) {
		token, err := d.Token(c.gap)
		if err != nil {
			return 0, nil, 0, err
		}
		if textAllowed && token.Kind == ASCII && (at.operand == noMergeOperand || token.Raw[0] != '~') {
			return 1, nil, 0, nil
		}
		if c.reveal {
			switch token.Kind {
			case MergeEndField:
				// The field count belongs to the next End Record on this
				// page. Its other bytes and the separator cache are conserved.
				for i := c.gap + 1; i < d.TokenCount(); i++ {
					next, _ := d.Token(i)
					if next.Kind == EndOfPage {
						break
					}
					if next.Kind == MergeEndRecord {
						raw := d.state.image.Export()
						count := binary.LittleEndian.Uint16(next.Raw[4:6])
						binary.LittleEndian.PutUint16(raw[next.Span.Offset+4:], count-1)
						return i - c.gap + 1, raw[d.state.gaps[c.gap+1]:d.state.gaps[i+1]], i - c.gap, nil
					}
				}
				return 1, nil, 0, nil
			case MergeField, MergeEndRecord, MergePageOff, MergePageOn, MergeNestPrimary, MergeNestSecondary, MergeIfBlank, MergeElse, MergeEndIf, MergeBreak:
				return 1, nil, 0, nil
			case HardReturn:
				// Removing the exposed return before an End Record also
				// updates that record's generated page row.
				record, recordErr := d.Token(c.gap + 1)
				cache, cacheErr := d.Token(c.gap + 2)
				if recordErr == nil && cacheErr == nil && record.Kind == MergeEndRecord && cache.Kind == EndOfPage {
					at := body.gaps[c.gap]
					raw := append([]byte{}, record.Raw...)
					raw = append(raw, everydayPageRecord(at.page, at.row)...)
					return 3, raw, 2, nil
				}
			}
		}
		return 0, nil, 0, failure(UnsupportedBody, c.gap, noSpan)
	})
}

func (d *Document) InsertAuthoredMergeText(c Cursor, text []byte) (EditResult, error) {
	return d.editMergeOwners(c, c.reveal, func(body mergeAuthoringBody, at mergeAuthoringGap) (int, []byte, int, error) {
		if !body.primary && !body.secondary && !body.codes || len(text) == 0 || len(text) > 65 || !editableMergeLiteral(text) {
			return 0, nil, 0, failure(InvalidASCII, c.gap, noSpan)
		}
		for _, b := range text {
			if at.operand == numericMergeOperand && (b < '0' || b > '9') ||
				at.operand == filenameMergeOperand && !mergeFilenameByte(b) {
				return 0, nil, 0, failure(InvalidASCII, c.gap, noSpan)
			}
		}
		return 0, text, len(text), nil
	})
}

type mergeOwnerEdit func(mergeAuthoringBody, mergeAuthoringGap) (remove int, raw []byte, insert int, err error)

func (d *Document) editMergeOwners(c Cursor, allowOperand bool, change mergeOwnerEdit) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() || c.state != d.state || c.gap < 0 || c.gap > d.TokenCount() {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	body, err := d.mergeAuthoring()
	if err != nil {
		return unchanged, err
	}
	at := body.gaps[c.gap]
	if !at.editable && (!allowOperand || at.operand == noMergeOperand) {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	remove, insertBytes, insert, err := change(body, at)
	if err != nil {
		return unchanged, err
	}
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	raw := d.state.image.Export()
	start, end := int(d.state.gaps[c.gap]), int(d.state.gaps[c.gap+remove])
	size := len(raw) + len(insertBytes) - (end - start)
	if size > MaxMutationBytes || d.TokenCount()-remove+insert > MaxMutationTokens {
		return unchanged, failure(MutationLimit, c.gap, noSpan)
	}
	candidate := make([]byte, 0, size)
	candidate = append(candidate, raw[:start]...)
	candidate = append(candidate, insertBytes...)
	candidate = append(candidate, raw[end:]...)
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	if _, err := next.mergeAuthoring(); err != nil {
		return unchanged, err
	}
	if next.TokenCount() != d.TokenCount()-remove+insert {
		return unchanged, failure(UnsupportedBody, c.gap, noSpan)
	}
	c.state = next.state
	if remove == 0 {
		c.gap += insert
	}
	return EditResult{Document: next, Cursor: c, Changed: true}, nil
}

func (d *Document) mergeOperand(owner int, numeric bool) (int, bool) {
	bound := 63
	if numeric {
		bound = 3
	}
	for length := 0; length <= bound; length++ {
		i := owner + 1 + length
		t, err := d.Token(i)
		if err != nil || t.Kind != ASCII {
			break
		}
		c := t.Raw[0]
		if c == '~' {
			return i, length > 0
		}
		if numeric && (c < '0' || c > '9') || !numeric && !mergeFilenameByte(c) {
			break
		}
	}
	return owner, false
}

func mergeFilenameByte(c byte) bool {
	return c >= 'A' && c <= 'Z' || c >= '0' && c <= '9' || c == ':' || c == '\\' || c == '.' || c == '_'
}

// InsertNamedMergeCode inserts one witnessed Page, Nest or condition command.
// A nested filename remains native text and never gains host path authority.
func (d *Document) InsertNamedMergeCode(c Cursor, kind Kind, operand string) (EditResult, error) {
	return d.editMergeOwners(c, false, func(body mergeAuthoringBody, _ mergeAuthoringGap) (int, []byte, int, error) {
		var code native.CommandKind
		switch kind {
		case MergePageOff:
			code = native.PageOff
		case MergePageOn:
			code = native.PageOn
		case MergeNestPrimary:
			code = native.NestPrimary
		case MergeNestSecondary:
			code = native.NestSecondary
		case MergeIfBlank:
			code = native.IfBlank
		case MergeElse:
			code = native.Else
		case MergeEndIf:
			code = native.EndIf
		case MergeBreak:
			code = native.Break
		default:
			return 0, nil, 0, failure(UnsupportedBody, c.gap, noSpan)
		}
		required := kind == MergeNestPrimary || kind == MergeNestSecondary || kind == MergeIfBlank
		if len(operand) > 63 || required != (operand != "") ||
			kind == MergeNestPrimary && body.secondary || kind == MergeNestSecondary && body.primary {
			return 0, nil, 0, failure(UnsupportedBody, c.gap, noSpan)
		}
		raw := []byte{0xde, byte(code), 4, 0, 4, 0, byte(code), 0xde}
		if required {
			if kind == MergeIfBlank && len(operand) > 3 {
				return 0, nil, 0, failure(InvalidASCII, c.gap, noSpan)
			}
			for i := 0; i < len(operand); i++ {
				b := operand[i]
				if kind == MergeIfBlank && (b < '0' || b > '9') ||
					kind != MergeIfBlank && !mergeFilenameByte(b) {
					return 0, nil, 0, failure(InvalidASCII, c.gap, noSpan)
				}
			}
			raw = append(raw, operand...)
			raw = append(raw, '~')
			return 0, raw, 2 + len(operand), nil
		}
		return 0, raw, 1, nil
	})
}
