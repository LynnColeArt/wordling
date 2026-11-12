package document

import "encoding/binary"

// mergeEditReceipt authenticates structural authoring and records the single
// semantic deletion owner separately from any dependent count or cache update.
type mergeEditReceipt struct {
	before, after        *revisionState
	cursor, beforeCursor Cursor
	deleted              fragment
	direction            DeleteDirection
}

func (f fragment) hasMergeOwner() bool {
	if !f.merge {
		return false
	}
	for _, kind := range f.kinds {
		if kind.MergeLabel(false) != "" {
			return true
		}
	}
	return false
}

// NewMergeHistory initializes the same bounded Undelete ring for an admitted
// structural document opened from disk.
func NewMergeHistory(d *Document) (History, error) {
	if !d.IsAuthoredMergeSource() {
		return History{}, failure(UnsupportedBody, -1, noSpan)
	}
	return History{&historyState{document: d.state}}, nil
}

// AfterMergeEdit adopts an authentic edit without discarding earlier groups.
func (h History) AfterMergeEdit(result EditResult) (History, error) {
	a := result.merge
	if a == nil || !result.Document.valid() || result.Document.state != a.after || result.Cursor != a.cursor || !result.Changed {
		return h, failure(InvalidEditResult, -1, noSpan)
	}
	if err := h.check(&Document{state: a.before}); err != nil {
		return h, err
	}
	if len(a.deleted.kinds) != 0 {
		return h.record(deletionState{
			cursor: a.beforeCursor, target: a.cursor.gap, kind: CharacterDeletion,
			direction: a.direction, everyday: true,
		}, a.deleted, a.after)
	}
	return h.adoptEverydayReceipt(&everydayReceipt{before: a.before, after: a.after}), nil
}

func (d *Document) restoreMerge(h History, p Preview, f fragment) (Deletion, error) {
	cursor := p.Cursor()
	unchanged := unchangedDeletion(d, cursor, h)
	if err := h.check(d); err != nil {
		return unchanged, err
	}
	if p.state.history != h.state {
		return unchanged, failure(HistoryMismatch, -1, noSpan)
	}
	edit, err := d.editMergeOwners(cursor, cursor.reveal, func(_ mergeAuthoringBody, at mergeAuthoringGap) (int, []byte, int, error) {
		return d.mergeRestoreChange(cursor, at, f)
	})
	if err != nil {
		return unchanged, err
	}
	edit.Cursor.gap = cursor.gap + len(f.kinds)
	next := h.adoptEverydayReceipt(&everydayReceipt{before: d.state, after: edit.Document.state})
	return Deletion{&deletionState{
		before: d.state, after: edit.Document.state, beforeHistory: h.state,
		afterHistory: next.state, cursor: edit.Cursor, kind: Restoration,
		applied: true, bodyChanged: true, nativeChanged: true,
	}}, nil
}

// A restored End Field increments the same dependent count which deletion
// decrements. An exposed HRt before an End Record changes that record's
// physical page-cache row without adding the cache itself to Undelete.
func (d *Document) mergeRestoreChange(cursor Cursor, at mergeAuthoringGap, f fragment) (int, []byte, int, error) {
	raw := []byte(f.native)
	fields, rows := 0, 0
	for i, kind := range f.kinds {
		switch kind {
		case MergeEndField:
			fields++
		case HardReturn:
			rows++
		case MergeEndRecord:
			// A same-gap delete run may already have reduced the count
			// before removing the record frame itself.
			if !restoreMergeFieldCount(raw[f.offset(i)+4:], fields) {
				return 0, nil, 0, failure(MutationLimit, cursor.gap, noSpan)
			}
			fields = 0
		}
	}
	if fields == 0 && rows == 0 {
		return 0, raw, len(f.kinds), nil
	}
	body := d.state.image.Export()
	end := cursor.gap
	for i := cursor.gap; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		if t.Kind == MergeEndRecord && fields != 0 {
			if !restoreMergeFieldCount(body[t.Span.Offset+4:], fields) {
				return 0, nil, 0, failure(MutationLimit, cursor.gap, noSpan)
			}
			end, fields = i+1, 0
			if rows == 0 {
				break
			}
		}
		if t.Kind == EndOfPage {
			if rows != 0 {
				row := int(binary.LittleEndian.Uint16(t.Raw[6:8])/200) + rows
				if row > lastEverydayPageRow {
					return 0, nil, 0, failure(MutationLimit, cursor.gap, noSpan)
				}
				copy(body[t.Span.Offset:], everydayPageRecord(at.page, uint16(row)))
				end = i + 1
			}
			break
		}
	}
	raw = append(raw, body[d.state.gaps[cursor.gap]:d.state.gaps[end]]...)
	remove := end - cursor.gap
	return remove, raw, remove + len(f.kinds), nil
}

func restoreMergeFieldCount(raw []byte, fields int) bool {
	count := int(binary.LittleEndian.Uint16(raw)) + fields
	if count > lastEverydayPageRow+1 {
		return false
	}
	binary.LittleEndian.PutUint16(raw, uint16(count))
	return true
}

// UsesMergeRing identifies a preview using the observed structural history UI.
func (p Preview) UsesMergeRing() bool {
	return p.Active() && p.state.history.mergeShared
}

// HasShareableHistory reports a known, nonempty deletion ring.
func (h History) HasShareableHistory() bool {
	return h.CountKnown() && h.Count() > 0
}

// CarryHistory copies the session's immutable deletion
// entries onto the destination history's independently authenticated revision.
func (h History) CarryHistory(source *Document, receiver History, target *Document) (History, error) {
	if !h.HasShareableHistory() {
		return receiver, nil
	}
	if !source.valid() || !target.valid() {
		return receiver, failure(InvalidDocument, -1, noSpan)
	}
	if err := h.check(source); err != nil {
		return receiver, err
	}
	if err := receiver.check(target); err != nil {
		return receiver, err
	}
	if h.state.observed != nil || receiver.state.observed != nil {
		return receiver, failure(UnsupportedHistoryEffect, -1, noSpan)
	}
	next := *receiver.state
	next.entries, next.count = h.state.entries, h.state.count
	next.mergeShared = h.state.mergeShared
	next.groupOpen, next.groupUnknown = false, false
	next.seedStage = seedUnqualified
	return History{&next}, nil
}
