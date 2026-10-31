package document

import "github.com/lynncoleart/wordling/internal/wp51"

// Transient implementation policies, not original disk/memory capacity limits.
const (
	HistoryCapacity         = 3
	MaxHistoryFragmentBytes = MaxMutationBytes
)

type HistoryBoundary uint8

const (
	SavedBoundary HistoryBoundary = iota + 1
	RightBoundary
)

// History wraps private immutable state. NewHistory explicitly creates a fresh
// transient context; Parse, retrieve and clearing a document NEVER reset history.
// Cross-document continuation is unqualified and refuses rather than clearing it.
type History struct{ state *historyState }
type HistoryRevision struct{ state *historyState }
type historyState struct {
	document                *revisionState
	entries                 [HistoryCapacity]historyEntry
	count                   int
	groupOpen, groupUnknown bool
	effectUnqualified       bool
	groupGap                int
}
type historyEntry struct {
	fragment fragment
	kind     DeletionKind
	commands int
}
type fragment struct {
	native      string
	kinds       []Kind
	codeIndices []uint16
}

func (f fragment) offset(index int) int {
	offset := index
	for _, code := range f.codeIndices {
		if int(code) < index {
			offset += 2
		}
	}
	return offset
}
func (d *Document) fragment(start, end int) fragment {
	span := wp51.Span{Offset: int(d.state.gaps[start]), Length: int(d.state.gaps[end] - d.state.gaps[start])}
	raw, _ := d.state.image.Bytes(span)
	f := fragment{native: string(raw), kinds: make([]Kind, end-start)}
	for i := start; i < end; i++ {
		s := d.span(i)
		local := s.Offset - span.Offset
		k := identify(raw[local : local+s.Length])
		f.kinds[i-start] = k
		if k == BoldOn || k == BoldOff {
			f.codeIndices = append(f.codeIndices, uint16(i-start))
		}
	}
	return f
}
func joinFragments(a, b fragment) fragment {
	f := fragment{native: a.native + b.native, kinds: make([]Kind, len(a.kinds)+len(b.kinds))}
	copy(f.kinds, a.kinds)
	copy(f.kinds[len(a.kinds):], b.kinds)
	f.codeIndices = append([]uint16(nil), a.codeIndices...)
	for _, index := range b.codeIndices {
		f.codeIndices = append(f.codeIndices, uint16(int(index)+len(a.kinds)))
	}
	return f
}
func NewHistory(d *Document) (History, error) {
	if !d.valid() {
		return History{}, failure(InvalidDocument, -1, noSpan)
	}
	if e := d.CheckMutation(); e != nil {
		return History{}, e
	}
	return History{&historyState{document: d.state}}, nil
}
func (h History) Revision() HistoryRevision { return HistoryRevision{h.state} }

// Qualified distinguishes enabled history behavior from preserved earlier
// entries after an edit whose immediate history effect has not been observed.
func (h History) Qualified() bool { return h.state != nil && !h.state.effectUnqualified }

// Count reports preserved known entries; check Qualified before treating this as
// the original stack after an edit with an unobserved immediate history effect.
func (h History) Count() int {
	if h.state == nil {
		return 0
	}
	return h.state.count
}
func (h History) check(d *Document) error {
	if h.state == nil {
		return failure(InvalidHistory, -1, noSpan)
	}
	if h.state.document != d.state {
		return failure(HistoryMismatch, -1, noSpan)
	}
	if h.state.effectUnqualified {
		return failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	return nil
}

// AfterEdit advances only a real immutable ASCII receipt. Native editing remains
// admitted independently of unobserved history effects: prior fragments survive,
// but subsequent history/deletion commands explicitly refuse after typeover
// replacement or insertion with existing history. The known Restore/reopen/X
// sequence remains admitted; no post-X history observation is invented.
func (h History) AfterEdit(r EditResult) (History, error) {
	if h.state == nil {
		return h, failure(InvalidHistory, -1, noSpan)
	}
	a := r.receipt
	if a == nil || !r.Document.valid() || r.Document.state != a.after || r.Cursor != a.cursor || r.Changed != a.changed {
		return h, failure(InvalidEditResult, -1, noSpan)
	}
	if a.before != h.state.document {
		return h, failure(HistoryMismatch, -1, noSpan)
	}
	if a.inputLength == 0 {
		return h, nil
	}
	next := *h.state
	next.document = a.after
	next.groupOpen = false
	next.groupUnknown = false
	if a.replaced > 0 || next.count > 0 {
		next.effectUnqualified = true
	}
	return History{&next}, nil
}

// EntryInfo is a copied inspection value; Native is original WP bytes, not labels.
type EntryInfo struct {
	Native           []byte
	Kind             DeletionKind
	Commands, Tokens int
	Qualified        bool
}

func (h History) Entry(index int) (EntryInfo, error) {
	if h.state == nil {
		return EntryInfo{}, failure(InvalidHistory, -1, noSpan)
	}
	if index < 0 || index >= h.state.count {
		return EntryInfo{}, failure(InvalidPosition, index, noSpan)
	}
	entry := h.state.entries[index]
	return EntryInfo{[]byte(entry.fragment.native), entry.kind, entry.commands, len(entry.fragment.kinds), h.Qualified()}, nil
}

// Separate records only the observed successful Save and Right grouping barriers.
// The dispatcher must report actual intervening commands; it may not reinterpret
// arbitrary keys/timing as these barriers or silently clear an existing stack.
func (h History) Separate(boundary HistoryBoundary) (History, error) {
	if h.state == nil {
		return h, failure(InvalidHistory, -1, noSpan)
	}
	if h.state.effectUnqualified {
		return h, failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	if boundary != SavedBoundary && boundary != RightBoundary {
		return h, failure(UnsupportedHistoryBoundary, -1, noSpan)
	}
	next := *h.state
	next.groupOpen = false
	next.groupUnknown = false
	return History{&next}, nil
}

// InterruptGrouping records a non-deleting interleaving whose grouping effect
// is unqualified (for example a view command between deletions). Entries and
// document state remain known; continuation refuses until an observed Save/Right
// separator. This is not a generic key router or a guessed new-deletion rule.
func (h History) InterruptGrouping() (History, error) {
	if h.state == nil {
		return h, failure(InvalidHistory, -1, noSpan)
	}
	if h.state.effectUnqualified {
		return h, failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	next := *h.state
	next.groupUnknown = next.groupUnknown || next.groupOpen
	next.groupOpen = false
	return History{&next}, nil
}
func (h History) record(s deletionState, f fragment, after *revisionState) (History, error) {
	if len(f.native) > MaxHistoryFragmentBytes || len(f.kinds) > MaxMutationTokens || len(f.codeIndices) > 2*MaxBoldPairs {
		return h, failure(MutationLimit, -1, noSpan)
	}
	next := *h.state
	next.document = after
	next.groupUnknown = false
	consecutive := s.kind == CharacterDeletion && s.direction == ForwardDelete && next.groupOpen && s.cursor.gap == next.groupGap && next.count > 0 && next.entries[0].kind == CharacterDeletion
	if consecutive {
		old := next.entries[0]
		if len(old.fragment.native) > MaxHistoryFragmentBytes-len(f.native) || len(old.fragment.kinds) > MaxMutationTokens-len(f.kinds) {
			return h, failure(MutationLimit, -1, noSpan)
		}
		old.fragment = joinFragments(old.fragment, f)
		old.commands++
		next.entries[0] = old
	} else {
		for i := HistoryCapacity - 1; i > 0; i-- {
			next.entries[i] = next.entries[i-1]
		}
		next.entries[0] = historyEntry{f, s.kind, 1}
		if next.count < HistoryCapacity {
			next.count++
		}
	}
	next.groupOpen = s.kind == CharacterDeletion && s.direction == ForwardDelete
	next.groupGap = s.target
	return History{&next}, nil
}

// Preview captures actual history/document state, not a mutable public handle.
// It is a read-only overlay at the current cursor, never an inserted document.
type Preview struct{ state *previewState }
type previewState struct {
	history *historyState
	cursor  Cursor
	index   int
}

func (p Preview) Active() bool {
	return p.state != nil && p.state.history != nil && p.state.history.count > 0
}
func (p Preview) Index() int {
	if !p.Active() {
		return -1
	}
	return p.state.index
}
func (p Preview) Cursor() Cursor {
	if p.state == nil {
		return Cursor{}
	}
	return p.state.cursor
}
func (p Preview) Prompt() string {
	if !p.Active() {
		return ""
	}
	return "Undelete: 1 Restore; 2 Previous Deletion: 0"
}
func (h History) Open(c Cursor) (Preview, error) {
	if h.state == nil {
		return Preview{}, failure(InvalidHistory, -1, noSpan)
	}
	if h.state.effectUnqualified {
		return Preview{}, failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	if c.state != h.state.document {
		return Preview{}, failure(RevisionMismatch, c.gap, noSpan)
	}
	if h.state.count == 0 {
		return Preview{}, nil
	}
	return Preview{&previewState{history: h.state, cursor: c}}, nil
}
func (p Preview) Previous() (Preview, error) {
	if !p.Active() {
		return p, failure(HistoryEmpty, -1, noSpan)
	}
	next := *p.state
	next.index = (next.index + 1) % next.history.count
	return Preview{&next}, nil
}
func (h History) CancelPreview(p Preview) (History, error) {
	if !p.Active() {
		return h, failure(HistoryEmpty, -1, noSpan)
	}
	if h.state != p.state.history {
		return h, failure(HistoryMismatch, -1, noSpan)
	}
	next := *h.state
	// No post-preview continued-delete grouping probe exists. Preserve entries;
	// refuse that unqualified interleaving until a known Save/Right separator.
	next.groupUnknown = next.groupUnknown || next.groupOpen
	next.groupOpen = false
	return History{&next}, nil
}
func (d *Document) Restore(h History, p Preview) (Deletion, error) {
	unchanged := unchangedDeletion(d, p.Cursor(), h)
	if !p.Active() {
		return unchanged, failure(HistoryEmpty, -1, noSpan)
	}
	if e := d.checkDeletion(p.Cursor(), h); e != nil {
		return unchanged, e
	}
	if p.state.history != h.state {
		return unchanged, failure(HistoryMismatch, -1, noSpan)
	}
	f := h.state.entries[p.state.index].fragment
	if len(f.kinds) > MaxMutationTokens-d.TokenCount() {
		return unchanged, failure(MutationLimit, p.Cursor().gap, noSpan)
	}
	raw := d.state.image.Export()
	start := int(d.state.gaps[0])
	at := int(d.state.gaps[p.Cursor().gap])
	bodyLength := len(raw) - start
	if len(f.native) > MaxMutationBytes-start-bodyLength {
		return unchanged, failure(MutationLimit, p.Cursor().gap, noSpan)
	}
	body := make([]byte, 0, bodyLength+len(f.native))
	body = append(body, raw[start:at]...)
	body = append(body, f.native...)
	body = append(body, raw[at:]...)
	edit, e := d.publishBody(p.Cursor(), body, d.TokenCount()+len(f.kinds), p.Cursor().gap+len(f.kinds), false)
	if e != nil {
		return unchanged, e
	}
	next := *h.state
	next.document = edit.Document.state
	next.groupOpen = false
	next.groupUnknown = false
	// EC204 proves one attributed Restore, not its later stack lifetime. Keep
	// prior bytes but refuse subsequent queries; plain/opening-repair retention
	// is independently observed and remains enabled.
	if h.state.entries[p.state.index].kind == AttributedDeletion {
		next.effectUnqualified = true
	}
	return Deletion{&deletionState{before: d.state, after: edit.Document.state, beforeHistory: h.state, afterHistory: &next, cursor: edit.Cursor, kind: Restoration, applied: true, bodyChanged: edit.Changed, nativeChanged: d.state != edit.Document.state}}, nil
}

type OverlayOrigin uint8

const (
	DocumentToken OverlayOrigin = iota
	DeletionFragment
)

// Fragment spans are absent (Offset=-1): they are not current native-file bytes.
// FragmentStart/End identify virtual selection; the UI's [Block] marker is not a
// native token and must never be serialized into either document or history.
type OverlayElement struct {
	Origin     OverlayOrigin
	TokenIndex int
	Kind       Kind
	Span       wp51.Span
	Raw        []byte
	Text       string
}
type Overlay struct {
	Elements                                           []OverlayElement
	FragmentStart, FragmentEnd, CursorGap, TotalTokens int
	Reveal                                             bool
}

func (p Preview) Present(start, count int, reveal bool) (Overlay, error) {
	if !p.Active() {
		return Overlay{}, failure(HistoryEmpty, -1, noSpan)
	}
	d := &Document{state: p.state.history.document}
	f := p.state.history.entries[p.state.index].fragment
	gap := p.state.cursor.gap
	total := d.TokenCount() + len(f.kinds)
	if start < 0 || start > total || count < 0 || count > total-start {
		return Overlay{}, failure(InvalidPosition, start, noSpan)
	}
	if count > MaxWindowTokens {
		return Overlay{}, failure(WindowLimit, start, noSpan)
	}
	out := Overlay{Elements: make([]OverlayElement, count), FragmentStart: gap, FragmentEnd: gap + len(f.kinds), CursorGap: gap, TotalTokens: total, Reveal: reveal}
	for i := start; i < start+count; i++ {
		var e OverlayElement
		if i >= gap && i < gap+len(f.kinds) {
			index := i - gap
			e = OverlayElement{Origin: DeletionFragment, TokenIndex: index, Kind: f.kinds[index], Span: noSpan, Raw: []byte(f.native[f.offset(index):f.offset(index+1)])}
		} else {
			index := i
			if i >= gap+len(f.kinds) {
				index -= len(f.kinds)
			}
			token, _ := d.Token(index)
			e = OverlayElement{Origin: DocumentToken, TokenIndex: index, Kind: token.Kind, Span: token.Span, Raw: token.Raw}
		}
		if e.Kind == ASCII {
			e.Text = string(e.Raw)
		} else if reveal {
			if e.Kind == BoldOn {
				e.Text = "[BOLD]"
			} else {
				e.Text = "[bold]"
			}
		}
		out.Elements[i-start] = e
	}
	return out, nil
}
