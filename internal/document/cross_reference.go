package document

import (
	"encoding/binary"
	"fmt"
	"strings"
)

type CrossReference struct {
	Name, Value string
	Target      bool
}

func readCrossReference(raw []byte) (CrossReference, bool) {
	if len(raw) < 10 || raw[0] != 0xd7 || raw[1] != 7 && raw[1] != 8 || raw[len(raw)-1] != 0xd7 {
		return CrossReference{}, false
	}
	stop := len(raw) - 4
	if int(binary.LittleEndian.Uint16(raw[2:4])) != stop || !sameRecordTrailer(raw, stop) {
		return CrossReference{}, false
	}
	ref := CrossReference{Target: raw[1] == 8}
	i := 4
	if !ref.Target {
		if raw[4] != 0 { // Page number.
			return CrossReference{}, false
		}
		i++
	}
	for i < stop && raw[i] != 0 {
		i++
	}
	if i == stop {
		return CrossReference{}, false
	}
	begin := 4
	if !ref.Target {
		begin++
	}
	ref.Name, ref.Value = string(raw[begin:i]), string(raw[i+1:stop])
	return ref, validReferenceName(ref.Name) && (ref.Target && ref.Value == "" || !ref.Target && validReferenceValue(ref.Value))
}

func validReferenceName(s string) bool {
	if len(s) == 0 || len(s) > 40 || strings.TrimSpace(s) != s {
		return false
	}
	for _, b := range []byte(s) {
		if b < 32 || b > 126 {
			return false
		}
	}
	return true
}

func validReferenceValue(s string) bool {
	if s == "?" {
		return true
	}
	if len(s) == 0 || len(s) > 5 {
		return false
	}
	for _, b := range []byte(s) {
		if (b < '0' || b > '9') && !strings.ContainsRune("ivxlcdmIVXLCDM", rune(b)) {
			return false
		}
	}
	return true
}

func referenceOwner(ref CrossReference) []byte {
	sub := byte(7)
	if ref.Target {
		sub = 8
	}
	raw := []byte{0xd7, sub, 0, 0}
	if !ref.Target {
		raw = append(raw, 0)
	}
	raw = append(raw, strings.ToUpper(ref.Name)...)
	raw = append(raw, 0)
	raw = append(raw, ref.Value...)
	n := len(raw)
	binary.LittleEndian.PutUint16(raw[2:4], uint16(n))
	return append(raw, byte(n), byte(n>>8), sub, 0xd7)
}

func (t Token) CrossReference() (CrossReference, bool) {
	if t.Kind != PageReference && t.Kind != ReferenceTarget {
		return CrossReference{}, false
	}
	return readCrossReference(t.Raw)
}

func (d *Document) MarkPageReference(c Cursor, name string, target bool) (EditResult, error) {
	if !validReferenceName(name) {
		return unchangedEdit(d, c), fmt.Errorf("enter a target name of 1 to 40 printable characters")
	}
	ref := CrossReference{Name: name, Target: target}
	if !target {
		ref.Value = "?"
	}
	return d.editTokens(c, referenceOwner(ref))
}

func (d *Document) MarkPageReferenceAndTarget(c Cursor, at int, name, page string) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	if !validReferenceName(name) || !validReferenceValue(page) {
		return unchangedEdit(d, c), fmt.Errorf("enter a target name of 1 to 40 printable characters at a known page")
	}
	if at < 0 || at > d.TokenCount() {
		return unchangedEdit(d, c), failure(InvalidPosition, at, noSpan)
	}
	raw := d.state.image.Export()
	body := make([]byte, 0, len(raw)-int(d.state.gaps[0]))
	mapping := make([]int, d.TokenCount())
	count, caret := 0, 0
	for i := 0; i <= d.TokenCount(); i++ {
		if i == at {
			body = append(body, referenceOwner(CrossReference{Name: name, Value: page})...)
			count++
			caret = count
		}
		if i == c.gap {
			body = append(body, referenceOwner(CrossReference{Name: name, Target: true})...)
			count++
		}
		if i < d.TokenCount() {
			mapping[i] = count
			body = append(body, raw[d.state.gaps[i]:d.state.gaps[i+1]]...)
			count++
		}
	}
	return d.publishEveryday(c, body, count, caret, mapping, blockFormatEdit)
}

func (d *Document) hasGeneratedFeature() bool {
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		if t.Kind == PageReference || t.Kind == ContentsDefinition {
			return true
		}
	}
	return false
}

// needsInitialGeneration covers pending definitions and references with no
// value. Generated records are retained until the user approves replacement.
func (d *Document) needsInitialGeneration() bool {
	definition, end := false, false
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		switch t.Kind {
		case ContentsDefinition:
			definition = true
		case ContentsEnd:
			end = true
		case PageReference:
			ref, _ := t.CrossReference()
			if ref.Value == "?" {
				return true
			}
		}
	}
	return definition && !end
}

func (d *Document) ResolvePageReferences(c Cursor, pages map[string]string) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	raw := d.state.image.Export()
	body := make([]byte, 0, len(raw)-int(d.state.gaps[0]))
	mapping := make([]int, d.TokenCount())
	changed := false
	for i := range mapping {
		mapping[i] = i
		t, _ := d.Token(i)
		if t.Kind == PageReference {
			ref, _ := t.CrossReference()
			page := pages[strings.ToUpper(ref.Name)]
			if page == "" {
				page = "?"
			}
			if !validReferenceValue(page) {
				return unchangedEdit(d, c), fmt.Errorf("unsupported page label for target %s", ref.Name)
			}
			if ref.Value != page {
				ref.Value = page
				body = append(body, referenceOwner(ref)...)
				changed = true
				continue
			}
		}
		body = append(body, t.Raw...)
	}
	if !changed {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	return d.publishEveryday(c, body, d.TokenCount(), c.gap, mapping, blockFormatEdit)
}
