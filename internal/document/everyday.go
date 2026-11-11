package document

import (
	"bytes"
	"encoding/binary"
	"slices"
)

// ReflowKind lists the formatter-owned changes allowed by the matched DOS
// profile. A plan cannot replace text, attributes, or explicit hard pages.
type ReflowKind uint8

const (
	WrapSpace ReflowKind = iota + 1
	UnwrapSpace
	InsertDeletedSoftReturn
	RemoveDeletedSoftReturn
	PromoteHardReturn
	DemoteSoftPage
	RenumberSoftPage
)

// ReflowChange addresses a token (or an insertion gap) in the input revision.
// Page is the preceding printed page for PromoteHardReturn and RenumberSoftPage.
type ReflowChange struct {
	At   int
	Kind ReflowKind
	Page uint16
}

type ReflowPlan struct {
	owner   *revisionState
	changes []ReflowChange
}

// NewReflowPlan captures a bounded copy of changes in native order. Coordinates
// refer to the original input, never to an intermediate edit.
func NewReflowPlan(d *Document, changes []ReflowChange) (ReflowPlan, error) {
	if !d.valid() {
		return ReflowPlan{}, failure(InvalidDocument, -1, noSpan)
	}
	if len(changes) > MaxMutationTokens {
		return ReflowPlan{}, failure(MutationLimit, -1, noSpan)
	}
	for i, change := range changes {
		if change.At < 0 || change.At > d.TokenCount() || i > 0 && change.At <= changes[i-1].At {
			return ReflowPlan{}, failure(InvalidPosition, change.At, noSpan)
		}
		pageChange := change.Kind == PromoteHardReturn || change.Kind == RenumberSoftPage
		if change.Kind < WrapSpace || change.Kind > RenumberSoftPage || pageChange != (change.Page != 0) {
			return ReflowPlan{}, failure(UnsupportedBody, change.At, noSpan)
		}
	}
	return ReflowPlan{owner: d.state, changes: slices.Clone(changes)}, nil
}

type everydayEditKind uint8

const (
	reflowEdit everydayEditKind = iota + 1
	retrieveEdit
)

type everydayReceipt struct {
	before, after *revisionState
	cursor        Cursor
	changed       bool
	kind          everydayEditKind
	tokenMap      []int
}

func unchangedEdit(d *Document, c Cursor) EditResult {
	return EditResult{Document: d, Cursor: c}
}

func (d *Document) checkEverydayCursor(c Cursor) error {
	if !d.valid() {
		return failure(InvalidDocument, -1, noSpan)
	}
	if c.state != d.state {
		return failure(RevisionMismatch, c.gap, noSpan)
	}
	if c.gap < 0 || c.gap > d.TokenCount() {
		return failure(InvalidPosition, c.gap, noSpan)
	}
	return d.CheckMutation()
}

// The matched Standard Printer flow captures use this Format Group 212 owner
// for a hard return at the bottom of a page. Keep every measured profile field;
// only the preceding page number varies in the repeated FLOW.WP fixtures.
func everydayPageRecord(page uint16) []byte {
	raw := []byte{
		0xd4, 0, 0x1c, 0, 0, 0x16, 0x68, 0x29,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a,
		0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4,
	}
	binary.LittleEndian.PutUint16(raw[8:10], page)
	return raw
}

func (d *Document) matchedSoftPage(index int) bool {
	if index < 0 || index+2 >= d.TokenCount() {
		return false
	}
	head, _ := d.Token(index)
	ret, _ := d.Token(index + 1)
	dormant, _ := d.Token(index + 2)
	if head.Kind != EndOfPage || len(head.Raw) != 32 || ret.Kind != HardReturnSoftPage || dormant.Kind != DormantHardReturn {
		return false
	}
	page := binary.LittleEndian.Uint16(head.Raw[8:10])
	return page != 0 && bytes.Equal(head.Raw, everydayPageRecord(page))
}

func (d *Document) reflowOwner(change ReflowChange) (remove int, native []byte, count int, err error) {
	index := change.At
	if change.Kind == InsertDeletedSoftReturn {
		// DSRt is a display break inside an unbroken word. It cannot invent
		// paragraph structure at an edge or substitute for a separating space.
		if index > 0 && index < d.TokenCount() && d.nonSpaceASCII(index-1) && d.nonSpaceASCII(index) {
			return 0, []byte{deletedSoftReturn}, 1, nil
		}
		return 0, nil, 0, failure(UnsupportedBody, index, noSpan)
	}
	if index >= d.TokenCount() {
		return 0, nil, 0, failure(InvalidPosition, index, noSpan)
	}
	token, _ := d.Token(index)
	switch change.Kind {
	case WrapSpace:
		if token.Kind == ASCII && token.Raw[0] == ' ' {
			return 1, []byte{softReturnByte}, 1, nil
		}
	case UnwrapSpace:
		if token.Kind == SoftReturn {
			return 1, []byte{' '}, 1, nil
		}
	case RemoveDeletedSoftReturn:
		if token.Kind == DeletedSoftReturn {
			return 1, nil, 0, nil
		}
	case PromoteHardReturn:
		if token.Kind == HardReturn && change.Page != 0 {
			return 1, append(everydayPageRecord(change.Page), hardReturnPageByte, dormantReturnByte), 3, nil
		}
	case DemoteSoftPage:
		if d.matchedSoftPage(index) {
			return 3, []byte{hardReturnByte}, 1, nil
		}
	case RenumberSoftPage:
		if change.Page != 0 && d.matchedSoftPage(index) {
			return 3, append(everydayPageRecord(change.Page), hardReturnPageByte, dormantReturnByte), 3, nil
		}
	}
	return 0, nil, 0, failure(UnsupportedBody, index, token.Span)
}

func (d *Document) nonSpaceASCII(i int) bool {
	t, err := d.Token(i)
	return err == nil && t.Kind == ASCII && t.Raw[0] != ' '
}

// AdoptReflow applies only checked formatter operations to the exact revision
// that was projected. All non-derived owners are copied from that revision.
func (d *Document) AdoptReflow(c Cursor, plan ReflowPlan) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if plan.owner != d.state {
		return unchangedEdit(d, c), failure(RevisionMismatch, c.gap, noSpan)
	}
	if len(plan.changes) == 0 {
		return d.everydayNoOp(c, reflowEdit), nil
	}
	raw := d.state.image.Export()
	n := d.TokenCount()
	body := make([]byte, 0, len(raw)-int(d.state.gaps[0]))
	tokenMap := make([]int, n)
	caret, next, j := 0, 0, 0
	for i := 0; i <= n; {
		if c.gap == i {
			caret = next
		}
		if j < len(plan.changes) && plan.changes[j].At == i {
			remove, add, count, err := d.reflowOwner(plan.changes[j])
			if err != nil {
				return unchangedEdit(d, c), err
			}
			j++
			if j < len(plan.changes) && plan.changes[j].At < i+remove {
				return unchangedEdit(d, c), failure(InvalidPosition, plan.changes[j].At, noSpan)
			}
			for k := 0; k < remove; k++ {
				tokenMap[i+k] = -1
			}
			if c.gap > i && c.gap < i+remove {
				caret = next
				if remove == count {
					caret += c.gap - i
				}
			}
			body = append(body, add...)
			next += count
			i += remove
			continue
		}
		if i == n {
			break
		}
		tokenMap[i] = next
		body = append(body, raw[d.state.gaps[i]:d.state.gaps[i+1]]...)
		i++
		next++
	}
	return d.publishEveryday(c, body, next, caret, tokenMap, reflowEdit)
}

// InsertDocument inserts the source's admitted body at the receiver's caret.
// The receiver retains its prefix and birth. Derived source boundaries become
// semantic separators so the receiver can reflow them in its own position.
func (d *Document) InsertDocument(c Cursor, source *Document) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if !source.valid() {
		return unchangedEdit(d, c), failure(InvalidDocument, -1, noSpan)
	}
	// Source is read-only and contributes no prefix packets. The allowlist
	// below admits only self-contained body owners; its resource/caches
	// never cross into the receiver. Bounds apply before copying.
	if source.TokenCount() > MaxMutationTokens || int(source.state.gaps[source.TokenCount()]-source.state.gaps[0]) > MaxMutationBytes {
		return unchangedEdit(d, c), failure(MutationLimit, -1, noSpan)
	}
	raw := d.state.image.Export()
	at := int(d.state.gaps[c.gap])
	body := append([]byte(nil), raw[d.state.gaps[0]:at]...)
	added := 0
	bold, underline := false, false
	for i := 0; i < source.TokenCount(); i++ {
		t, _ := source.Token(i)
		switch t.Kind {
		case SoftReturn:
			body = append(body, ' ')
		case DeletedSoftReturn:
			continue
		case EndOfPage:
			if !source.matchedSoftPage(i) {
				return unchangedEdit(d, c), failure(UnsupportedBody, i, t.Span)
			}
			body = append(body, hardReturnByte)
			i += 2
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff:
			active := &bold
			if t.Kind == UnderlineOn || t.Kind == UnderlineOff {
				active = &underline
			}
			on := t.Kind == BoldOn || t.Kind == UnderlineOn
			if *active == on {
				return unchangedEdit(d, c), failure(UnsupportedBody, i, t.Span)
			}
			*active = on
			body = append(body, t.Raw...)
		case ASCII, Tab, HardReturn, HardPage:
			body = append(body, t.Raw...)
		default:
			return unchangedEdit(d, c), failure(UnsupportedBody, i, t.Span)
		}
		added++
	}
	if bold || underline {
		return unchangedEdit(d, c), failure(UnsupportedBody, -1, noSpan)
	}
	if added == 0 {
		return d.everydayNoOp(c, retrieveEdit), nil
	}
	body = append(body, raw[at:]...)
	tokenMap := make([]int, d.TokenCount())
	for i := range tokenMap {
		tokenMap[i] = i
		if i >= c.gap {
			tokenMap[i] += added
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+added, c.gap+added, tokenMap, retrieveEdit)
}

func (d *Document) publishEveryday(c Cursor, body []byte, count, gap int, tokenMap []int, kind everydayEditKind) (EditResult, error) {
	result, err := d.publishBody(c, body, count, gap, false)
	if err == nil {
		result.everyday = &everydayReceipt{before: d.state, after: result.Document.state, cursor: result.Cursor, changed: result.Changed, kind: kind, tokenMap: tokenMap}
	}
	return result, err
}

func (d *Document) everydayNoOp(c Cursor, kind everydayEditKind) EditResult {
	result := unchangedEdit(d, c)
	result.everyday = &everydayReceipt{before: d.state, after: d.state, cursor: c, kind: kind}
	return result
}
