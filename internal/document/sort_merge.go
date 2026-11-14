package document

import (
	"bytes"
	"fmt"
	"slices"
	"strings"
)

// SortMergeRecords orders simple secondary records by the first ASCII word
// of their first field. It moves each record intact and rebuilds its page
// cache according to its new position.
func (d *Document) SortMergeRecords(c Cursor, descending bool) (EditResult, error) {
	unchanged := unchangedEdit(d, c)
	if !d.valid() || c.state != d.state {
		return unchanged, failure(RevisionMismatch, c.gap, noSpan)
	}
	profile, err := d.mergeAuthoring()
	if err != nil {
		return unchanged, err
	}
	if !profile.secondary || profile.primary || profile.wrapped || profile.codes {
		return unchanged, fmt.Errorf("sort needs complete, single-line secondary merge fields")
	}
	type record struct {
		key         string
		first, last int
		row         uint16
	}
	raw := d.state.image.Export()
	var records []record
	first, fieldStart, fields := 0, 0, 0
	key := ""
	for i := 0; i < d.TokenCount(); i++ {
		token, _ := d.Token(i)
		switch token.Kind {
		case ASCII:
			continue
		case MergeEndField:
			if i == fieldStart {
				return unchanged, fmt.Errorf("sort needs a nonempty text value in each field")
			}
			if fields == 0 {
				words := strings.Fields(string(raw[d.state.gaps[fieldStart]:d.state.gaps[i]]))
				if len(words) == 0 {
					return unchanged, fmt.Errorf("sort needs a word in the first field")
				}
				key = strings.ToUpper(words[0])
			}
			next, _ := d.Token(i + 1)
			if next.Kind != HardReturn {
				return unchanged, fmt.Errorf("sort needs an explicit return after each field")
			}
			fields++
			i++
			fieldStart = i + 1
		case MergeEndRecord:
			if fields == 0 || i != fieldStart || i+2 >= d.TokenCount() {
				return unchanged, fmt.Errorf("complete each record with End Record")
			}
			cache, _ := d.Token(i + 1)
			page, _ := d.Token(i + 2)
			if cache.Kind != EndOfPage || page.Kind != HardPage {
				return unchanged, fmt.Errorf("sort needs a hard page after each record")
			}
			records = append(records, record{key, first, i + 1, profile.gaps[i].row})
			i += 2
			first, fieldStart, fields = i+1, i+1, 0
		default:
			return unchanged, fmt.Errorf("sort supports ASCII fields separated by native End Field and End Record")
		}
	}
	if len(records) == 0 || first != d.TokenCount() {
		return unchanged, fmt.Errorf("sort needs complete secondary merge records")
	}
	slices.SortStableFunc(records, func(a, b record) int {
		order := strings.Compare(a.key, b.key)
		if descending {
			return -order
		}
		return order
	})
	flags, err := d.prefixMutationAdmission()
	if err != nil {
		return unchanged, err
	}
	candidate := bytes.Clone(raw[:d.state.gaps[0]])
	for i, r := range records {
		candidate = append(candidate, raw[d.state.gaps[r.first]:d.state.gaps[r.last]]...)
		candidate = append(candidate, everydayPageRecord(uint16(i+1), r.row)...)
		candidate = append(candidate, hardPageByte)
	}
	c.gap = 0
	if bytes.Equal(raw, candidate) {
		return EditResult{Document: d, Cursor: c}, nil
	}
	candidate[flags] |= 8
	next, err := parseRevision(candidate, d.state.birth)
	if err != nil {
		return unchanged, err
	}
	if _, err = next.mergeAuthoring(); err != nil {
		return unchanged, err
	}
	c.state = next.state
	return EditResult{Document: next, Cursor: c, Changed: true, merge: &mergeEditReceipt{before: d.state, after: next.state, cursor: c}}, nil
}
