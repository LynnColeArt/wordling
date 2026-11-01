// Package body computes only the two closed FIELD1 / IFBLANK2 body forms.
// It does not paginate, serialize native documents, or perform host effects.
package body

import (
	"fmt"
	"github.com/lynncoleart/wordling/internal/merge/native"
	"unsafe"
)

const (
	MaxPrimaryTokens   = 4096
	MaxBodyBytes       = 65536
	MaxWorkUnits       = 1048576
	inspectionWork     = 4 * (native.MaxTokens + native.MaxFields + native.MaxRecords + native.MaxFindings)
	compileAllocation  = 64 << 20
	inspectAllocation  = 48 << 20
	evaluateAllocation = 4 << 20
	maxTrace           = 4098
)

type Limits struct{ PrimaryTokens, BodyBytes, WorkUnits int }

func DefaultLimits() Limits { return Limits{MaxPrimaryTokens, MaxBodyBytes, MaxWorkUnits} }
func (l Limits) valid() bool {
	return l.PrimaryTokens > 0 && l.PrimaryTokens <= MaxPrimaryTokens && l.BodyBytes > 0 && l.BodyBytes <= MaxBodyBytes && l.WorkUnits > 0 && l.WorkUnits <= MaxWorkUnits
}

type Failure struct{ Category string }

func (e *Failure) Error() string { return "merge-body: " + e.Category }
func fail(s string) error        { return &Failure{s} }

type budget struct{ work, allocation uint64 }

func (b *budget) take(work, allocation uint64) error {
	if work > b.work || allocation > b.allocation {
		return fail("Budget")
	}
	b.work -= work
	b.allocation -= allocation
	return nil
}
func size[T any](n int) uint64 { var z T; return uint64(n) * uint64(unsafe.Sizeof(z)) }

type literal struct {
	span native.Span
	code byte
}
type proof struct {
	program              native.Program
	source               native.Source
	limits               Limits
	conditional          bool
	first, second, after []literal
}

// Plan retains a private immutable proof; the zero Plan is invalid.
type Plan struct{ proof *proof }

func (p Plan) Valid() bool { return p.proof != nil }

// Trace associates an emitted output range with an authentic native span.
type Trace struct {
	Start, Length int
	Span          native.Span
	Field         bool
}

// Access retains the enclosing DATA provenance, including un-emitted metadata.
type Access struct {
	Field    int
	Decision bool
	Record   native.Record
	Value    native.Field
}
type Provenance struct {
	Primary, Secondary native.Source
	Record             int
	Conditional, Blank bool
	Trace              []Trace
	Accesses           []Access
}
type resultProof struct {
	bytes      []byte
	provenance Provenance
}
type Result struct{ proof *resultProof }

func (r Result) Valid() bool { return r.proof != nil }
func (r Result) Bytes() ([]byte, error) {
	if !r.Valid() {
		return nil, fail("InvalidResult")
	}
	return append([]byte(nil), r.proof.bytes...), nil
}
func cloneProvenance(p Provenance) Provenance {
	p.Trace = append([]Trace(nil), p.Trace...)
	p.Accesses = append([]Access(nil), p.Accesses...)
	for j := range p.Accesses {
		r := &p.Accesses[j].Record
		r.Fields = append([]native.Field(nil), r.Fields...)
		r.Interstitial = append([]native.Span(nil), r.Interstitial...)
	}
	return p
}
func (r Result) Provenance() (Provenance, bool) {
	if !r.Valid() {
		return Provenance{}, false
	}
	return cloneProvenance(r.proof.provenance), true
}
func wrapped(e error) error { return fmt.Errorf("merge-body: field: %w", e) }
