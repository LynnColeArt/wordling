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
	WrapSpaceToPage
	InsertDeletedSoftPage
	PromoteDeletedSoftReturn
	SoftenPageBreak
	RefreshHardPage
	RefreshTabCache
)

// ReflowChange addresses a token (or an insertion gap) in the input revision.
// Page is the preceding printed page for operations producing page groups.
// Row is the zero-based physical row of an explicit hard page (RefreshHardPage).
type ReflowChange struct {
	At   int
	Kind ReflowKind
	Page uint16
	Row  uint16
	// Column is the zero-based text stop for RefreshTabCache.
	Column uint16
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
		var pageChange bool
		switch change.Kind {
		case PromoteHardReturn, RenumberSoftPage, WrapSpaceToPage,
			InsertDeletedSoftPage, PromoteDeletedSoftReturn, RefreshHardPage:
			pageChange = true
		}
		if change.Kind < WrapSpace || change.Kind > RefreshTabCache || pageChange != (change.Page != 0) ||
			change.Row > lastEverydayPageRow || change.Row != 0 && change.Kind != RefreshHardPage ||
			(change.Kind == RefreshTabCache && !validEverydayTabStop(int(change.Column))) ||
			(change.Kind != RefreshTabCache && change.Column != 0) {
			return ReflowPlan{}, failure(UnsupportedBody, change.At, noSpan)
		}
	}
	return ReflowPlan{owner: d.state, changes: slices.Clone(changes)}, nil
}

type everydayEditKind uint8

const (
	reflowEdit everydayEditKind = iota + 1
	retrieveEdit
	proofEdit
)

type everydayReceipt struct {
	cacheOnly     bool
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

const lastEverydayPageRow = 53

// The matched Standard Printer captures use this Format Group 212 owner.
// The default profile advances 200 formatter units per row. The record's
// profile fields and preceding page number follow the original captures.
func everydayPageRecord(page, row uint16) []byte {
	raw := []byte{
		0xd4, 0, 0x1c, 0, 0, 0x16, 0x68, 0x29,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a,
		0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4,
	}
	binary.LittleEndian.PutUint16(raw[6:8], row*200)
	binary.LittleEndian.PutUint16(raw[8:10], page)
	return raw
}

type pageGroup struct {
	tokens int
	kind   Kind
	row    uint16
}

// matchedPageGroup qualifies only the fixed-profile End of Page records and
// complete companions witnessed in the original. It never treats a lone
// soft-page byte or unknown D4 payload as editable.
func (d *Document) matchedPageGroup(index int) (pageGroup, bool) {
	if index < 0 || index+1 >= d.TokenCount() {
		return pageGroup{}, false
	}
	head, _ := d.Token(index)
	transition, _ := d.Token(index + 1)
	if head.Kind != EndOfPage || len(head.Raw) != 32 {
		return pageGroup{}, false
	}
	page := binary.LittleEndian.Uint16(head.Raw[8:10])
	units := binary.LittleEndian.Uint16(head.Raw[6:8])
	row := units / 200
	if page == 0 || units%200 != 0 || row > lastEverydayPageRow ||
		!bytes.Equal(head.Raw, everydayPageRecord(page, row)) {
		return pageGroup{}, false
	}
	group := pageGroup{tokens: 2, kind: transition.Kind, row: row}
	switch transition.Kind {
	case HardPage:
		return group, true
	case SoftPage, DeletedSoftPage:
		return group, row == lastEverydayPageRow
	case HardReturnSoftPage:
		dormant, err := d.Token(index + 2)
		group.tokens = 3
		return group, row == lastEverydayPageRow && err == nil && dormant.Kind == DormantHardReturn
	default:
		return pageGroup{}, false
	}
}

func pageOwners(kind Kind, page, row uint16) (native []byte, count int) {
	native = everydayPageRecord(page, row)
	switch kind {
	case HardReturnSoftPage:
		return append(native, hardReturnPageByte, dormantReturnByte), 3
	case SoftPage:
		return append(native, softPageByte), 2
	case DeletedSoftPage:
		return append(native, deletedSoftPage), 2
	case HardPage:
		return append(native, hardPageByte), 2
	default:
		return nil, 0
	}
}

func (d *Document) reflowOwner(change ReflowChange) (remove int, native []byte, count int, err error) {
	index := change.At
	if change.Kind == InsertDeletedSoftReturn || change.Kind == InsertDeletedSoftPage {
		if d.canInsertDeletableBreak(index) {
			if change.Kind == InsertDeletedSoftReturn {
				return 0, []byte{deletedSoftReturn}, 1, nil
			}
			native, count = pageOwners(DeletedSoftPage, change.Page, lastEverydayPageRow)
			return 0, native, count, nil
		}
		return 0, nil, 0, failure(UnsupportedBody, index, noSpan)
	}
	if index >= d.TokenCount() {
		return 0, nil, 0, failure(InvalidPosition, index, noSpan)
	}
	token, _ := d.Token(index)
	switch change.Kind {
	case RefreshTabCache:
		if token.Kind == Tab && matchedEverydayTab(token.Raw) {
			return 1, everydayTabOwner(int(change.Column)), 1, nil
		}
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
		if token.Kind == HardReturn {
			native, count = pageOwners(HardReturnSoftPage, change.Page, lastEverydayPageRow)
			return 1, native, count, nil
		}
	case WrapSpaceToPage:
		if token.Kind == SoftReturn || token.Kind == ASCII && token.Raw[0] == ' ' {
			native, count = pageOwners(SoftPage, change.Page, lastEverydayPageRow)
			return 1, native, count, nil
		}
	case PromoteDeletedSoftReturn:
		if token.Kind == DeletedSoftReturn {
			native, count = pageOwners(DeletedSoftPage, change.Page, lastEverydayPageRow)
			return 1, native, count, nil
		}
	case DemoteSoftPage, SoftenPageBreak, RenumberSoftPage:
		group, ok := d.matchedPageGroup(index)
		if ok && group.kind != HardPage {
			native, count = demotePage(group.kind, change.Kind == SoftenPageBreak)
			if change.Kind == RenumberSoftPage {
				native, count = pageOwners(group.kind, change.Page, group.row)
			}
			return group.tokens, native, count, nil
		}
	case RefreshHardPage:
		group, ok := d.matchedPageGroup(index)
		if token.Kind == HardPage || ok && group.kind == HardPage {
			remove = 1
			if ok {
				remove = group.tokens
			}
			native, count = pageOwners(HardPage, change.Page, change.Row)
			return remove, native, count, nil
		}
	}
	return 0, nil, 0, failure(UnsupportedBody, index, token.Span)
}

func demotePage(kind Kind, physicalLine bool) ([]byte, int) {
	switch kind {
	case SoftPage:
		if physicalLine {
			return []byte{softReturnByte}, 1
		}
		return []byte{' '}, 1
	case DeletedSoftPage:
		if physicalLine {
			return []byte{deletedSoftReturn}, 1
		}
		return nil, 0
	case HardReturnSoftPage:
		return []byte{hardReturnByte}, 1
	case HardPage:
		return []byte{hardPageByte}, 1
	default:
		return nil, 0
	}
}

func (d *Document) canInsertDeletableBreak(index int) bool {
	// Formatting owners can lie beside the gap, but no separator can be
	// crossed. The original also emits [Tab][DSRt] before the next glyph.
	// Zero-width formatting owners never turn a whitespace gap into a word.
	left := d.nearestInlineOwner(index-1, -1)
	right := d.nearestInlineOwner(index, 1)
	return (left == ASCII || left == Tab) && right == ASCII
}

func (d *Document) nearestInlineOwner(index, step int) Kind {
	for index >= 0 && index < d.TokenCount() {
		t, _ := d.Token(index)
		switch t.Kind {
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff:
			index += step
		case ASCII:
			if t.Raw[0] == ' ' {
				return Opaque
			}
			return ASCII
		default:
			return t.Kind
		}
	}
	return Opaque
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
	cacheOnly := true
	for i := 0; i <= n; {
		if c.gap == i {
			caret = next
		}
		if j < len(plan.changes) && plan.changes[j].At == i {
			change := plan.changes[j]
			cacheOnly = cacheOnly && change.Kind == RefreshTabCache
			remove, add, count, err := d.reflowOwner(change)
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
	result, err := d.publishEveryday(c, body, next, caret, tokenMap, reflowEdit)
	if err == nil {
		result.everyday.cacheOnly = cacheOnly
	}
	return result, err
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
			group, ok := source.matchedPageGroup(i)
			if !ok {
				return unchangedEdit(d, c), failure(UnsupportedBody, i, t.Span)
			}
			plain, count := demotePage(group.kind, false)
			body = append(body, plain...)
			i += group.tokens - 1
			added += count
			continue
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
