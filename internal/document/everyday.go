package document

import (
	"bytes"
	"encoding/binary"
	"slices"
	"strings"
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
	PromoteProtectedReturn
	OmitProtectedDormantReturn
	RefreshAlignmentCache
	InsertParagraphPosition
	RefreshParagraphPosition
	RemoveParagraphPosition
	RefreshNoteBreak
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
	Column    uint16
	CustomTab bool
	// Position and Anchor are WordPerfect units for RefreshAlignmentCache.
	Position, Anchor              uint16
	Top, Bottom                   uint16
	Vertical                      uint16
	CustomPage                    bool
	Header, Footer                bool
	OddHeader                     bool
	PageNumberPosition            uint8
	PageNumberSuppressed          bool
	PageProtection                uint8
	NoteLines                     uint8
	NotePage, NoteTop, NoteBottom uint16
	NoteReserve                   uint16
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
		case PromoteHardReturn, PromoteProtectedReturn, RenumberSoftPage, WrapSpaceToPage,
			InsertDeletedSoftPage, PromoteDeletedSoftReturn, RefreshHardPage:
			pageChange = true
		}
		customPage := change.CustomPage
		positionChange := change.Kind == InsertParagraphPosition || change.Kind == RefreshParagraphPosition
		if change.Kind < WrapSpace || change.Kind > RefreshNoteBreak || pageChange != (change.Page != 0) ||
			change.Row > 65 || !customPage && change.Row > lastEverydayPageRow ||
			change.Row != 0 && !customPage && change.Kind != RefreshHardPage && change.Kind != PromoteProtectedReturn ||
			customPage && (!pageChange || !ValidPageMargins(int(change.Top), int(change.Bottom)) ||
				int(change.Vertical) >= 13200-int(change.Top)-int(change.Bottom)-pageTextReserve(change.Header, change.Footer)) ||
			!customPage && (change.Top != 0 || change.Bottom != 0 || change.Vertical != 0 || change.Header || change.Footer) ||
			change.OddHeader && (!change.Header || !change.Footer) ||
			(change.PageNumberPosition != 0 || change.PageNumberSuppressed) && (change.Kind != RefreshHardPage || !customPage) ||
			change.PageNumberPosition != 0 && change.PageNumberPosition != PageNumberTopCenter && change.PageNumberPosition != PageNumberBottomRight ||
			change.PageNumberSuppressed && !customPage ||
			change.PageProtection > 2 ||
			change.NoteReserve != 0 && (change.Kind != PromoteProtectedReturn || !customPage || change.NoteReserve > 13200 || change.NoteReserve%200 != 0) ||
			(change.Kind != RefreshNoteBreak || change.NoteLines == 0) && (change.NoteLines != 0 || change.NotePage != 0 || change.NoteTop != 0 || change.NoteBottom != 0) ||
			change.Kind == RefreshNoteBreak && change.NoteLines != 0 && (change.NotePage == 0 || !ValidPageMargins(int(change.NoteTop), int(change.NoteBottom))) ||
			change.PageProtection != 0 && (!customPage || change.Kind != WrapSpaceToPage && change.Kind != RenumberSoftPage) ||
			(change.Kind == RefreshTabCache && !validEverydayTabStop(int(change.Column)) && (!change.CustomTab || !validTabColumn(int(change.Column)))) ||
			change.CustomTab && change.Kind != RefreshTabCache ||
			(change.Kind != RefreshTabCache && change.Column != 0) ||
			(change.Kind == RefreshAlignmentCache && (change.Position > change.Anchor || change.Anchor > 10200)) ||
			positionChange && (change.Position > 10200 || change.Anchor != 0) ||
			!positionChange && change.Kind != RefreshAlignmentCache && (change.Position != 0 || change.Anchor != 0) {
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
	summaryEdit
	searchPairEdit
	blockFormatEdit
	blockCaseEdit
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

func customPageRecord(page, vertical, top, bottom uint16) []byte {
	raw := everydayPageRecord(page, 0)
	binary.LittleEndian.PutUint16(raw[6:8], vertical)
	height := uint16(13200) - top - bottom
	for _, index := range []int{18, 20, 22} {
		binary.LittleEndian.PutUint16(raw[index:index+2], height)
	}
	binary.LittleEndian.PutUint16(raw[24:26], top)
	binary.LittleEndian.PutUint16(raw[26:28], top)
	return raw
}

func reservePageText(raw []byte, header, footer, oddHeader bool) {
	height := binary.LittleEndian.Uint16(raw[18:20])
	top := binary.LittleEndian.Uint16(raw[24:26])
	if oddHeader {
		binary.LittleEndian.PutUint16(raw[20:22], height-800)
		binary.LittleEndian.PutUint16(raw[22:24], height-400)
		binary.LittleEndian.PutUint16(raw[24:26], top+400)
		return
	}
	if header {
		binary.LittleEndian.PutUint16(raw[20:22], height-400)
		binary.LittleEndian.PutUint16(raw[24:26], top+400)
		binary.LittleEndian.PutUint16(raw[26:28], top+400)
	}
	if footer {
		binary.LittleEndian.PutUint16(raw[22:24], height-400)
	}
	if header {
		bodyHeight := height - 400
		if footer {
			bodyHeight -= 400
		}
		binary.LittleEndian.PutUint16(raw[22:24], bodyHeight)
	}
}

func pageTextReserve(header, footer bool) int {
	reserved := 0
	if header {
		reserved += 400
	}
	if footer {
		reserved += 400
	}
	return reserved
}

func (change ReflowChange) pageOwners(kind Kind, defaultRow uint16) ([]byte, int) {
	if !change.CustomPage {
		return pageOwners(kind, change.Page, defaultRow)
	}
	raw := customPageRecord(change.Page, change.Vertical, change.Top, change.Bottom)
	reservePageText(raw, change.Header, change.Footer, change.OddHeader)
	if kind == HardPage {
		reservePageNumber(raw, int(change.PageNumberPosition), change.PageNumberSuppressed, change.Header, change.Footer)
	}
	if change.NoteReserve != 0 {
		binary.LittleEndian.PutUint16(raw[10:12], change.NoteReserve)
		raw[12], raw[13] = 1, 1
	}
	switch kind {
	case HardReturnSoftPage:
		return append(raw, hardReturnPageByte), 2
	case SoftPage:
		return append(raw, softPageByte), 2
	case DeletedSoftPage:
		return append(raw, deletedSoftPage), 2
	default:
		return append(raw, hardPageByte), 2
	}
}

type pageGroup struct {
	tokens int
	kind   Kind
	row    uint16
}

// matchedPageGroup qualifies only the fixed-profile End of Page records and
// complete companions witnessed in the original. It excludes standalone
// soft pages produced by DOS text conversion and unknown D4 payloads.
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
	expected := everydayPageRecord(page, row)
	lastRow := uint16(lastEverydayPageRow)
	top := int(binary.LittleEndian.Uint16(head.Raw[24:26]))
	height := int(binary.LittleEndian.Uint16(head.Raw[18:20]))
	bottomStart := int(binary.LittleEndian.Uint16(head.Raw[26:28]))
	header, footer, oddHeader := false, false, false
	twenty, twentyTwo := int(binary.LittleEndian.Uint16(head.Raw[20:22])), int(binary.LittleEndian.Uint16(head.Raw[22:24]))
	switch {
	case twenty == height-800 && twentyTwo == height-400 && top == bottomStart+400:
		header, footer, oddHeader, top = true, true, true, top-400
	case twenty == height-400 && twentyTwo == height-800:
		header, footer, top = true, true, top-400
	case twenty == height-400 && twentyTwo == height-400 && top == bottomStart:
		header, top = true, top-400
	case twenty == height && twentyTwo == height-400 && bottomStart == top:
		footer = true
	}
	bottom := 13200 - height - top
	if ValidPageMargins(top, bottom) && (top != 1200 || bottom != 1200 || units%200 != 0) {
		expected = customPageRecord(page, units, uint16(top), uint16(bottom))
		lastRow = uint16(height/200 - 1)
	}
	if height >= 800 {
		reservePageText(expected, header, footer, oddHeader)
	}
	bodyHeight := int(binary.LittleEndian.Uint16(expected[22:24]))
	if oddHeader {
		bodyHeight -= 400
	}
	if bodyHeight > 0 {
		lastRow = uint16((bodyHeight - 1) / 200)
	}
	noteContinues := false
	if index > 0 && transition.Kind == HardReturnSoftPage && head.Raw[14] == 0 {
		prior, _ := d.Token(index - 1)
		if note, ok := prior.Note(); ok && !note.End && note.FirstPageLines > 0 {
			binary.LittleEndian.PutUint16(expected[10:12], uint16((strings.Count(note.Text, "\n")+1-note.FirstPageLines+2)*200))
			expected[12], expected[13] = 1, 1
			noteContinues = true
		}
	}
	if head.Raw[14] == 1 && (transition.Kind == HardReturnSoftPage || transition.Kind == SoftPage) {
		expected[14] = 1
	} else if head.Raw[14] == 2 && transition.Kind == SoftPage {
		expected[14] = 2
	}
	if !bytes.Equal(head.Raw, expected) && transition.Kind == HardPage {
		numberPosition, suppressed := d.pageNumberBeforeBreak(index)
		if numberPosition != 0 || suppressed {
			// A top number uses the same offsets as a header and was
			// already accounted for by the geometry inference above.
			if !(numberPosition == PageNumberTopCenter && !suppressed && header) {
				reservePageNumber(expected, numberPosition, suppressed, header, footer)
			}
		}
	}
	if page == 0 || int(units) >= bodyHeight || !bytes.Equal(head.Raw, expected) {
		return pageGroup{}, false
	}
	group := pageGroup{tokens: 2, kind: transition.Kind, row: row}
	atPageBottom := func() bool {
		if row == lastRow && units%200 == 0 {
			return true
		}
		spacing, lineHeight := 0, 0
		for i := index - 1; i >= 0; i-- {
			owner, _ := d.Token(i)
			if spacing == 0 {
				spacing = owner.LineSpacing()
			}
			if lineHeight == 0 && owner.Kind == LineHeight {
				lineHeight = owner.LineHeight()
				if lineHeight == 0 {
					lineHeight = 200
				}
			}
			if spacing > 0 && lineHeight > 0 {
				break
			}
		}
		if lineHeight == 0 {
			lineHeight = 200
		}
		if spacing == 0 {
			spacing, _ = d.InitialLineSpacing()
		}
		return int(units)+(max(1, spacing)+1)*lineHeight > bodyHeight
	}
	switch transition.Kind {
	case HardPage:
		return group, true
	case SoftPage, DeletedSoftPage:
		return group, atPageBottom() || head.Raw[14] == 1
	case HardReturnSoftPage:
		dormant, err := d.Token(index + 2)
		// DOS can save the page before the dormant return is materialized.
		// Both forms represent one logical hard return.
		if err == nil && dormant.Kind == DormantHardReturn {
			group.tokens = 3
		}
		return group, atPageBottom() || head.Raw[14] == 1 || noteContinues
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
	if change.Kind == InsertParagraphPosition {
		return 0, paragraphPositionOwner(change.Position), 1, nil
	}
	if change.Kind == InsertDeletedSoftReturn || change.Kind == InsertDeletedSoftPage {
		if d.canInsertDeletableBreak(index) {
			if change.Kind == InsertDeletedSoftReturn {
				return 0, []byte{deletedSoftReturn}, 1, nil
			}
			native, count = change.pageOwners(DeletedSoftPage, lastEverydayPageRow)
			return 0, native, count, nil
		}
		return 0, nil, 0, failure(UnsupportedBody, index, noSpan)
	}
	if index >= d.TokenCount() {
		return 0, nil, 0, failure(InvalidPosition, index, noSpan)
	}
	token, _ := d.Token(index)
	switch change.Kind {
	case RefreshNoteBreak:
		if note, ok := token.Note(); ok && !note.End && strings.Contains(note.Text, "\n") {
			raw, err := reflowNoteOwner(note, token.Raw, change)
			if err == nil {
				return 1, raw, 1, nil
			}
		}
	case RefreshParagraphPosition:
		if token.Kind == ParagraphPosition {
			return 1, paragraphPositionOwner(change.Position), 1, nil
		}
	case RemoveParagraphPosition:
		if token.Kind == ParagraphPosition {
			return 1, nil, 0, nil
		}
	case RefreshAlignmentCache:
		if token.Kind == CenterLine || token.Kind == FlushRight || token.Kind == DecimalTab || token.Kind == SoftDecimalTab {
			return 1, alignmentOwner(token.Kind, int(change.Position), int(change.Anchor)), 1, nil
		}
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
	case OmitProtectedDormantReturn:
		if token.Kind == DormantHardReturn && index >= 3 {
			head, _ := d.Token(index - 2)
			prior, _ := d.Token(index - 3)
			if head.Kind == EndOfPage && prior.Kind == BlockProtectOff {
				if group, ok := d.matchedPageGroup(index - 2); ok && group.kind == HardReturnSoftPage && group.tokens == 3 {
					return 1, nil, 0, nil
				}
			}
		}
	case PromoteProtectedReturn:
		remove = 1
		group, ok := d.matchedPageGroup(index)
		if ok && group.kind == HardReturnSoftPage {
			remove = group.tokens
		}
		if token.Kind == HardReturn || remove > 1 {
			native, _ = change.pageOwners(HardReturnSoftPage, change.Row)
			if change.NoteReserve == 0 {
				native[14] = 1
			}
			return remove, native[:33], 2, nil
		}
	case PromoteHardReturn:
		if token.Kind == HardReturn {
			native, count = change.pageOwners(HardReturnSoftPage, lastEverydayPageRow)
			return 1, native, count, nil
		}
	case WrapSpaceToPage:
		if token.Kind == SoftReturn || token.Kind == ASCII && token.Raw[0] == ' ' {
			native, count = change.pageOwners(SoftPage, lastEverydayPageRow)
			native[14] = change.PageProtection
			return 1, native, count, nil
		}
	case PromoteDeletedSoftReturn:
		if token.Kind == DeletedSoftReturn {
			native, count = change.pageOwners(DeletedSoftPage, lastEverydayPageRow)
			return 1, native, count, nil
		}
	case DemoteSoftPage, SoftenPageBreak, RenumberSoftPage:
		group, ok := d.matchedPageGroup(index)
		if ok && group.kind != HardPage && (change.PageProtection == 0 || group.kind == SoftPage) {
			native, count = demotePage(group.kind, change.Kind == SoftenPageBreak)
			if change.Kind == RenumberSoftPage {
				native, count = change.pageOwners(group.kind, group.row)
				native[14] = change.PageProtection
				if token.Raw[14] == 1 && group.kind == HardReturnSoftPage {
					native[14] = 1
					native, count = native[:33], 2
				}
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
			native, count = change.pageOwners(HardPage, change.Row)
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
	return (left.IsCharacter() || left == DOSControl || left == Tab) && (right.IsCharacter() || right == DOSControl)
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
			cacheOnly = cacheOnly && (change.Kind == RefreshTabCache || change.Kind == RefreshAlignmentCache ||
				change.Kind == RefreshParagraphPosition)
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
	return d.insertDocument(c, source, false)
}

// InsertBlockCopy retrieves the detached selection and leaves the cursor at
// the first inserted owner, as in WordPerfect's Move/Copy prompt.
func (d *Document) InsertBlockCopy(c Cursor, source *Document) (EditResult, error) {
	return d.insertDocument(c, source, true)
}

func (d *Document) insertDocument(c Cursor, source *Document, keepCursor bool) (EditResult, error) {
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
	var body []byte
	added := 0
	bold, underline, italics := false, false, false
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
		case BoldOn, BoldOff, UnderlineOn, UnderlineOff, ItalicsOn, ItalicsOff:
			active := &bold
			if t.Kind == UnderlineOn || t.Kind == UnderlineOff {
				active = &underline
			}
			if t.Kind == ItalicsOn || t.Kind == ItalicsOff {
				active = &italics
			}
			on := t.Kind == BoldOn || t.Kind == UnderlineOn || t.Kind == ItalicsOn
			if *active == on {
				return unchangedEdit(d, c), failure(UnsupportedBody, i, t.Span)
			}
			*active = on
			body = append(body, t.Raw...)
		case ASCII, ExtendedCharacter, HardSpace, DOSControl, Tab, HardReturn, HardPage:
			body = append(body, t.Raw...)
		default:
			return unchangedEdit(d, c), failure(UnsupportedBody, i, t.Span)
		}
		added++
	}
	if bold || underline || italics {
		return unchangedEdit(d, c), failure(UnsupportedBody, -1, noSpan)
	}
	gap := c.gap
	if !keepCursor {
		gap += added
	}
	return d.insertEverydayBody(c, body, added, gap)
}

func (d *Document) insertEverydayBody(c Cursor, inserted []byte, added, gap int) (EditResult, error) {
	if added == 0 {
		return d.everydayNoOp(c, retrieveEdit), nil
	}
	raw := d.state.image.Export()
	at := int(d.state.gaps[c.gap])
	body := append([]byte(nil), raw[d.state.gaps[0]:at]...)
	body = append(body, inserted...)
	body = append(body, raw[at:]...)
	tokenMap := make([]int, d.TokenCount())
	for i := range tokenMap {
		tokenMap[i] = i
		if i >= c.gap {
			tokenMap[i] += added
		}
	}
	return d.publishEveryday(c, body, d.TokenCount()+added, gap, tokenMap, retrieveEdit)
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

// OmitDeferredPageRecord preserves the soft page byte while reproducing the
// DOS save made before the cursor revisits the reformatted page boundary.
func (d *Document) OmitDeferredPageRecord(candidate []byte, index int) ([]byte, error) {
	group, ok := d.matchedPageGroup(index)
	if !ok || (group.kind != SoftPage && group.kind != DeletedSoftPage) {
		return nil, failure(UnsupportedBody, index, noSpan)
	}
	saved, err := Parse(candidate)
	if err != nil {
		return nil, err
	}
	before, _ := d.Token(index)
	after, err := saved.Token(index)
	if err != nil || !bytes.Equal(before.Raw, after.Raw) || saved.TokenCount() != d.TokenCount() {
		return nil, failure(UnsupportedBody, index, noSpan)
	}
	offset := after.Span.Offset
	return append(candidate[:offset:offset], candidate[offset+after.Span.Length:]...), nil
}

// RestoreDeferredSoftPage builds an editing revision for a saved soft page
// whose formatter record was deferred. The loaded source still owns its bytes.
func (d *Document) RestoreDeferredSoftPage(index int, page uint16) (*Document, error) {
	token, err := d.Token(index)
	if err != nil {
		return nil, err
	}
	if page == 0 || (token.Kind != SoftPage && token.Kind != DeletedSoftPage) {
		return nil, failure(UnsupportedBody, index, token.Span)
	}
	if index > 0 {
		prior, _ := d.Token(index - 1)
		if prior.Kind == EndOfPage {
			return nil, failure(UnsupportedBody, index, token.Span)
		}
	}
	raw := d.state.image.Export()
	at := token.Span.Offset
	record := everydayPageRecord(page, lastEverydayPageRow)
	candidate := append(raw[:at:at], record...)
	candidate = append(candidate, raw[at:]...)
	// The acquired wire bytes remain with the storage source. The loaded
	// editing lineage needs the complete body for Fast Save validation.
	next, err := Parse(candidate)
	if err != nil {
		return nil, err
	}
	if err := next.checkFastSaveMutation(); err != nil {
		// Validate a compact editing image if the source has a Fast Save prefix.
		return next.CompactFastSave()
	}
	return next, nil
}
