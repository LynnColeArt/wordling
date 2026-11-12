// Package explicit qualifies already-explicit, source-owned Secondary field
// DATA. It neither admits a merge Program nor evaluates or writes documents.
package explicit

import (
	"bytes"
	"fmt"

	"github.com/lynncoleart/wordling/internal/merge/native"
)

const Scope = "explicit-field-DATA-only"

// Failure is an atomic refusal of the whole closed DATA predicate.
type Failure struct{ Category string }

func (e *Failure) Error() string    { return "merge-explicit: " + e.Category }
func refused(category string) error { return &Failure{category} }

// ExplicitFieldMissing means no explicitly delimited field has this ordinal.
// It says nothing about the original application's implicit-field behavior.
type ExplicitFieldMissing struct{ Record, Field int }

func (e *ExplicitFieldMissing) Error() string {
	return fmt.Sprintf("merge-explicit: ExplicitFieldMissing %d/%d", e.Record, e.Field)
}

type proof struct {
	view native.View
	info native.Inspection
}

// Data is a by-value immutable whole-Secondary proof. A zero Data is invalid.
type Data struct{ proof *proof }

// Value is an immutable explicit presence handle; zero/missing is never empty.
type Value struct {
	proof         *proof
	record, field int
}

func (d Data) Valid() bool { return d.proof != nil }
func (d Data) Source() native.Source {
	if !d.Valid() {
		return native.Source{}
	}
	return d.proof.info.Source
}
func (d Data) RecordCount() int {
	if !d.Valid() {
		return 0
	}
	return len(d.proof.info.Records)
}
func (d Data) Field(recordOrdinal, fieldOrdinal int) (Value, error) {
	if !d.Valid() {
		return Value{}, refused("InvalidData")
	}
	if recordOrdinal < 1 || recordOrdinal > len(d.proof.info.Records) || fieldOrdinal < 1 || fieldOrdinal > len(d.proof.info.Records[recordOrdinal-1].Fields) {
		return Value{}, &ExplicitFieldMissing{recordOrdinal, fieldOrdinal}
	}
	return Value{d.proof, recordOrdinal - 1, fieldOrdinal - 1}, nil
}

// Inspect returns defensive reader provenance including unresolved findings,
// raw counts, unaddressed tails and opaque owners. It conveys DATA scope only.
func (d Data) Inspect() (native.Inspection, bool) {
	if !d.Valid() {
		return native.Inspection{}, false
	}
	return d.proof.view.Inspect()
}
func (v Value) Valid() bool {
	return v.proof != nil && v.record >= 0 && v.record < len(v.proof.info.Records) && v.field >= 0 && v.field < len(v.proof.info.Records[v.record].Fields)
}
func (v Value) Bytes() ([]byte, error) {
	if !v.Valid() {
		return nil, refused("InvalidValue")
	}
	b, ok := v.proof.view.Bytes(v.proof.info.Records[v.record].Fields[v.field].Content)
	if !ok {
		return nil, refused("SourceSpan")
	}
	return b, nil
}
func (v Value) ExplicitlyEmpty() (bool, error) {
	if !v.Valid() {
		return false, refused("InvalidValue")
	}
	return v.proof.info.Records[v.record].Fields[v.field].Empty, nil
}

// Provenance returns copied native records/fields, never private proof slices.
func (v Value) Provenance() (native.Record, native.Field, bool) {
	if !v.Valid() {
		return native.Record{}, native.Field{}, false
	}
	r := v.proof.info.Records[v.record]
	r.Fields = append([]native.Field(nil), r.Fields...)
	r.Interstitial = append([]native.Span(nil), r.Interstitial...)
	return r, r.Fields[v.field], true
}

// Admit captures the WHOLE View wrapper exactly once. Only private captured
// state and its source-owned spans are used thereafter. Concurrent replacement
// during this capture is outside the contract; subsequent immutable reads are
// race-safe. It makes at most one bounded full-source copy, never one per field.
func Admit(view *native.View, expected native.Source) (Data, error) {
	if view == nil {
		return Data{}, refused("InvalidView")
	}
	captured := *view
	if !captured.Valid() || !expected.Valid() {
		return Data{}, refused("InvalidSource")
	}
	info, ok := captured.Inspect()
	if !ok || info.Role != native.Secondary || !info.Source.Equal(expected) {
		return Data{}, refused("SourceRoleMismatch")
	}
	// Accepted native ownership can originate only from positive-capped Parse.
	// Cardinality guards precede all proof traversal/appends.
	if info.FindingsCapped || len(info.Tokens) == 0 || len(info.Tokens) > native.MaxTokens || len(info.Records) == 0 || len(info.Records) > native.MaxRecords || len(info.Commands) > 3*native.MaxRecords || len(info.Findings) > native.MaxFindings {
		return Data{}, refused("CardinalityOrFindings")
	}
	totalFields := 0
	for _, r := range info.Records {
		if len(r.Fields) < 1 || len(r.Fields) > 2 || len(r.Interstitial) != 2 {
			return Data{}, refused("RecordShape")
		}
		totalFields += len(r.Fields)
	}
	if totalFields > native.MaxFields {
		return Data{}, refused("FieldLimit")
	}
	whole := captured.Export()
	if len(whole) > native.MaxBytes {
		return Data{}, refused("InputLimit")
	}
	first, valid := info.Tokens[0].Raw.Bounds()
	if !valid || first.Offset < 0 || first.Offset > len(whole) {
		return Data{}, refused("BodyExtent")
	}
	c := checker{view: &captured, info: &info, at: first.Offset, eof: len(whole), copied: len(whole), maxWork: 12*(len(whole)-first.Offset+len(info.Tokens)+len(info.Commands)+totalFields+len(info.Records)+len(info.Findings)) + 65536}
	if err := c.records(); err != nil {
		return Data{}, err
	}
	if c.at != c.eof || c.token != len(info.Tokens) || c.command != len(info.Commands) || c.finding != len(info.Findings) {
		return Data{}, refused("IncompleteCoverage")
	}
	// This intentionally retains the native refusal and every old finding.
	if captured.Supported() {
		return Data{}, refused("GenericAdmissionChanged")
	}
	if p, e := captured.Admit(); e == nil || p.Valid() {
		return Data{}, refused("GenericAdmissionChanged")
	}
	return Data{&proof{captured, info}}, nil
}

type checker struct {
	view                                                    *native.View
	info                                                    *native.Inspection
	at, eof, token, command, finding, work, maxWork, copied int
}

func (c *checker) read(s native.Span) ([]byte, error) {
	b, ok := c.view.Bytes(s)
	if !ok {
		return nil, refused("ForeignSpan")
	}
	c.copied += len(b)
	c.work += len(b) + 1
	if c.copied > 4*native.MaxBytes || c.work > c.maxWork {
		return nil, refused("ProofBudget")
	}
	return b, nil
}
func (c *checker) bounds(s native.Span, length int) error {
	b, ok := s.Bounds()
	if !ok || b.Offset != c.at || b.Length != length {
		return refused("SpanCoverage")
	}
	return nil
}
func (c *checker) next(s native.Span, kind native.TokenKind, code, sub byte) error {
	if c.token >= len(c.info.Tokens) {
		return refused("TokenMissing")
	}
	t := c.info.Tokens[c.token]
	c.token++
	c.work++
	if t.Raw != s || t.Kind != kind || t.Code != code || t.Subfunction != sub {
		return refused("TokenCoverage")
	}
	b, e := c.read(s)
	if e != nil {
		return e
	}
	if e = c.bounds(s, len(b)); e != nil {
		return e
	}
	c.at += len(b)
	return nil
}
func (c *checker) commandAt(s native.Span, k native.CommandKind, count uint16) (native.Command, error) {
	if c.command >= len(c.info.Commands) {
		return native.Command{}, refused("CommandMissing")
	}
	cmd := c.info.Commands[c.command]
	c.command++
	c.work++
	if cmd.Function != s || cmd.Kind != k || cmd.Match != -1 || cmd.Operand.Kind != 0 || cmd.Operand.Number != 0 {
		return cmd, refused("CommandContext")
	}
	b, e := c.read(cmd.Payload)
	if e != nil {
		return cmd, e
	}
	p, ok := cmd.Payload.Bounds()
	f, _ := s.Bounds()
	if !ok || p.Offset != f.Offset+4 {
		return cmd, refused("PayloadSite")
	}
	if k == native.EndField {
		if len(b) != 0 || cmd.HasRawCount || cmd.RawCount != 0 {
			return cmd, refused("EndFieldPayload")
		}
	} else {
		if len(b) != 2 || !cmd.HasRawCount || cmd.RawCount != count || b[0] != byte(count) || b[1] != 0 {
			return cmd, refused("EndRecordPayload")
		}
	}
	return cmd, nil
}
func (c *checker) findingAt(code string, s native.Span) error {
	if c.finding >= len(c.info.Findings) {
		return refused("FindingMissing")
	}
	f := c.info.Findings[c.finding]
	c.finding++
	c.work++
	if f.Code != code || f.At != s {
		return refused("FindingSite")
	}
	_, e := c.read(f.At)
	return e
}
func (c *checker) records() error {
	for ri, r := range c.info.Records {
		start := c.at
		if r.Ordinal != ri+1 {
			return refused("RecordOrdinal")
		}
		if !((r.StoredCount == 2 && len(r.Fields) == 1) || (r.StoredCount == 3 && len(r.Fields) == 2)) {
			return refused("LiteralCountFieldPair")
		}
		for fi, f := range r.Fields {
			content, e := c.read(f.Content)
			if e != nil {
				return e
			}
			if e = c.bounds(f.Content, len(content)); e != nil {
				return e
			}
			spaces := len(content) > 0
			for _, b := range content {
				c.work++
				if b < 0x20 || b > 0x7e || b == '~' {
					return refused("ContentProfile")
				}
				if b != ' ' {
					spaces = false
				}
				if c.token >= len(c.info.Tokens) {
					return refused("ContentTokenMissing")
				}
				t := c.info.Tokens[c.token]
				if e = c.next(t.Raw, native.Character, b, 0); e != nil {
					return e
				}
			}
			if spaces || f.Ordinal != fi+1 || f.Empty != (len(content) == 0) || f.WhitespaceOnly != spaces || !f.PlainASCII {
				return refused("FieldShape")
			}
			ef, e := c.read(f.EndField)
			if e != nil {
				return e
			}
			if !bytes.Equal(ef, []byte{0xde, 0x31, 4, 0, 4, 0, 0x31, 0xde}) {
				return refused("EndFieldFrame")
			}
			if _, e = c.commandAt(f.EndField, native.EndField, 0); e != nil {
				return e
			}
			if e = c.next(f.EndField, native.Function, 0xde, 0x31); e != nil {
				return e
			}
			hr, e := c.read(f.Separator)
			if e != nil {
				return e
			}
			if !bytes.Equal(hr, []byte{0x0a}) {
				return refused("EndFieldSeparator")
			}
			if e = c.next(f.Separator, native.Control, 0x0a, 0); e != nil {
				return e
			}
		}
		if _, e := c.read(r.Tail); e != nil {
			return e
		}
		if e := c.bounds(r.Tail, 0); e != nil {
			return refused("NonemptyOrForeignTail")
		}
		er, e := c.read(r.EndRecord)
		if e != nil {
			return e
		}
		if !bytes.Equal(er, []byte{0xde, 0x34, 6, 0, byte(r.StoredCount), 0, 6, 0, 0x34, 0xde}) {
			return refused("EndRecordFrame")
		}
		cmd, e := c.commandAt(r.EndRecord, native.EndRecord, r.StoredCount)
		if e != nil {
			return e
		}
		if e = c.next(r.EndRecord, native.Function, 0xde, 0x34); e != nil {
			return e
		}
		raw, ok := r.Raw.Bounds()
		if !ok || raw.Offset != start || raw.Length != c.at-start {
			return refused("RecordCoverage")
		}
		if _, e = c.read(r.Raw); e != nil {
			return e
		}
		if e = c.findingAt("RecordCountUnresolved", cmd.Payload); e != nil {
			return e
		}
		opaque, e := c.read(r.Interstitial[0])
		if e != nil {
			return e
		}
		if !opaqueProfile(opaque) {
			return refused("OpaqueCohort")
		}
		if e = c.next(r.Interstitial[0], native.Function, 0xd4, 0); e != nil {
			return e
		}
		if e = c.findingAt("FormatterUnresolved", r.Interstitial[0]); e != nil {
			return e
		}
		hp, e := c.read(r.Interstitial[1])
		if e != nil {
			return e
		}
		if !bytes.Equal(hp, []byte{0x0c}) {
			return refused("RecordHardpage")
		}
		if e = c.next(r.Interstitial[1], native.Control, 0x0c, 0); e != nil {
			return e
		}
	}
	return nil
}

// Six whole-owner opaque octet cohorts. No interpretation, mask, arithmetic,
// profile generation, original file digest/path/value or formatter removal.
func opaqueProfile(b []byte) bool {
	if len(b) != 32 {
		return false
	}
	for _, p := range [6][32]byte{
		{0xd4, 0, 0x1c, 0, 0, 0x16, 0xc8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4},
		{0xd4, 0, 0x1c, 0, 0, 0x16, 0xc8, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4},
		{0xd4, 0, 0x1c, 0, 0, 0x16, 0x90, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4},
		{0xd4, 0, 0x1c, 0, 0, 0x16, 0x90, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4},
		{0xd4, 0, 0x1c, 0, 0, 0x16, 0x90, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4},
		{0xd4, 0, 0x1c, 0, 0, 0x16, 0x90, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x30, 0x2a, 0x30, 0x2a, 0x30, 0x2a, 0xb0, 4, 0xb0, 4, 0x1c, 0, 0, 0xd4},
	} {
		if bytes.Equal(b, p[:]) {
			return true
		}
	}
	return false
}
