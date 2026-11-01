package body

import (
	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

// Evaluate computes one body privately. All required fields and output bounds
// are checked before a value copy or successful result can escape.
func (p Plan) Evaluate(data explicit.Data, expectedSecondary native.Source, recordOrdinal int) (Result, error) {
	if !p.Valid() {
		return Result{}, fail("InvalidPlan")
	}
	q := p.proof
	if !data.Valid() || !expectedSecondary.Valid() || !data.Source().Equal(expectedSecondary) {
		return Result{}, fail("SecondaryOwner")
	}
	if recordOrdinal < 1 || recordOrdinal > data.RecordCount() {
		return Result{}, fail("RecordOrdinal")
	}
	b := budget{uint64(q.limits.WorkUnits), evaluateAllocation}
	if e := b.take(8, 0); e != nil {
		return Result{}, e
	}
	access := func(ordinal int, decision bool) (explicit.Value, Access, error) {
		if e := b.take(8, size[native.Field](2)+size[native.Span](2)); e != nil {
			return explicit.Value{}, Access{}, e
		}
		v, e := data.Field(recordOrdinal, ordinal)
		if e != nil {
			return explicit.Value{}, Access{}, wrapped(e)
		}
		r, f, ok := v.Provenance()
		if !ok || !v.Valid() || r.Ordinal != recordOrdinal || f.Ordinal != ordinal || len(r.Fields) > 2 || len(r.Interstitial) != 2 {
			return explicit.Value{}, Access{}, fail("FieldProvenance")
		}
		return v, Access{ordinal, decision, r, f}, nil
	}
	value, field, e := access(1, false)
	if e != nil {
		return Result{}, e
	}
	chosen := q.first
	pr := Provenance{Primary: q.source, Secondary: expectedSecondary, Record: recordOrdinal, Conditional: q.conditional}
	var decision Access
	if q.conditional {
		v, a, e := access(2, true)
		if e != nil {
			return Result{}, e
		}
		blank, e := v.ExplicitlyEmpty()
		if e != nil {
			return Result{}, e
		}
		decision = a
		pr.Blank = blank
		if !blank {
			chosen = q.second
		}
	}
	f, ok := field.Value.Content.Bounds()
	if !ok || f.Length < 0 {
		return Result{}, fail("ContentBounds")
	}
	literalCount := len(chosen) + len(q.after)
	total := uint64(literalCount) + uint64(f.Length)
	traces := literalCount + 1
	if total > uint64(q.limits.BodyBytes) || traces > maxTrace {
		return Result{}, fail("BodyLimit")
	}
	accessCount := 1
	if q.conditional {
		accessCount = 2
	}
	// Reserve field copy, emitted bytes, trace and provenance before any make/copy.
	alloc := uint64(f.Length) + total + size[Trace](traces) + size[Access](accessCount) + size[resultProof](1)
	if e := b.take(uint64(literalCount)*3+uint64(f.Length)*3+uint64(traces)+uint64(accessCount), alloc); e != nil {
		return Result{}, e
	}
	contents, e := value.Bytes()
	if e != nil {
		return Result{}, e
	}
	if len(contents) != f.Length {
		return Result{}, fail("ContentLength")
	}
	out := make([]byte, int(total))
	pr.Trace = make([]Trace, 0, traces)
	pr.Accesses = make([]Access, 0, accessCount)
	if q.conditional {
		pr.Accesses = append(pr.Accesses, decision)
	}
	pr.Accesses = append(pr.Accesses, field)
	at := 0
	emit := func(xs []literal) {
		for _, x := range xs {
			out[at] = x.code
			pr.Trace = append(pr.Trace, Trace{at, 1, x.span, false})
			at++
		}
	}
	emit(chosen)
	if q.conditional {
		emit(q.after)
	}
	copy(out[at:], contents)
	pr.Trace = append(pr.Trace, Trace{at, len(contents), field.Value.Content, true})
	at += len(contents)
	if !q.conditional {
		emit(q.after)
	}
	if at != len(out) {
		return Result{}, fail("OutputCoverage")
	}
	return Result{&resultProof{out, pr}}, nil
}
