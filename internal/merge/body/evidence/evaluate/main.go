// evaluate is an offline maintainer consumer of computed per-record bodies.
// Its JSON diagnostics are not a native document or an application Merge command.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
	"io"
	"os"
)

const (
	maxRequest    = 3 << 20
	maxEncoded    = 1 << 20
	maxTotalBody  = 256 << 10
	maxTotalTrace = 16384
)

type ledger struct{ work, allocation uint64 }

func (l *ledger) take(w, a uint64) error {
	if w > l.work || a > l.allocation {
		return errors.New("cumulative consumer budget")
	}
	l.work -= w
	l.allocation -= a
	return nil
}

type request struct{ primary, secondary []byte }

func decode(raw []byte) (request, error) {
	d := json.NewDecoder(bytes.NewReader(raw))
	t, e := d.Token()
	if e != nil || t != json.Delim('{') {
		return request{}, errors.New("request object required")
	}
	var r request
	seen := map[string]bool{}
	for d.More() {
		key, e := d.Token()
		if e != nil {
			return r, e
		}
		k, ok := key.(string)
		if !ok || seen[k] || (k != "primary" && k != "secondary") {
			return r, errors.New("unknown or duplicate key")
		}
		seen[k] = true
		var b []byte
		if e = d.Decode(&b); e != nil {
			return r, e
		}
		if len(b) == 0 || len(b) > native.MaxBytes {
			return r, errors.New("decoded source cap")
		}
		if k == "primary" {
			r.primary = b
		} else {
			r.secondary = b
		}
	}
	t, e = d.Token()
	if e != nil || t != json.Delim('}') {
		return r, errors.New("request end")
	}
	if !seen["primary"] || !seen["secondary"] {
		return r, errors.New("two source payloads required")
	}
	if _, e = d.Token(); e != io.EOF {
		return r, errors.New("trailing JSON")
	}
	return r, nil
}

type bounds struct {
	Offset int `json:"offset"`
	Length int `json:"length"`
}

func span(s native.Span) (bounds, error) {
	b, ok := s.Bounds()
	if !ok {
		return bounds{}, errors.New("invalid source provenance")
	}
	return bounds{b.Offset, b.Length}, nil
}

type trace struct {
	Start  int    `json:"start"`
	Length int    `json:"length"`
	Source string `json:"source"`
	Span   bounds `json:"span"`
}
type access struct {
	Field        int      `json:"field"`
	Decision     bool     `json:"decision"`
	Content      bounds   `json:"content"`
	EndField     bounds   `json:"end_field"`
	Separator    bounds   `json:"separator"`
	Record       bounds   `json:"record"`
	EndRecord    bounds   `json:"end_record"`
	Tail         bounds   `json:"tail"`
	StoredCount  uint16   `json:"stored_count"`
	Interstitial []bounds `json:"interstitial"`
}
type row struct {
	Record      int      `json:"record"`
	Body        []byte   `json:"body"`
	Conditional bool     `json:"conditional"`
	Blank       bool     `json:"blank"`
	Trace       []trace  `json:"trace"`
	Accesses    []access `json:"accesses"`
}
type report struct {
	Schema          string `json:"schema"`
	Scope           string `json:"scope"`
	PrimarySHA256   string `json:"primary_sha256"`
	SecondarySHA256 string `json:"secondary_sha256"`
	Rows            []row  `json:"rows"`
}

func hash(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func run(reader io.Reader, writer io.Writer) error {
	l := ledger{64 << 20, 256 << 20}
	if e := l.take(12<<20, 32<<20); e != nil {
		return e
	}
	raw, e := io.ReadAll(io.LimitReader(reader, maxRequest+1))
	if e != nil {
		return e
	}
	if len(raw) > maxRequest {
		return errors.New("request read cap")
	}
	r, e := decode(raw)
	if e != nil {
		return e
	}
	// Each reservation covers outer framing, native parse/view and (secondary)
	// explicit admission. Reject BEFORE either source is parsed on insufficient fit.
	for _, b := range [][]byte{r.primary, r.secondary} {
		if e = l.take(256*uint64(len(b))+(1<<20), 512*uint64(len(b))+(4<<20)); e != nil {
			return e
		}
	}
	pi, e := native.Parse(r.primary, native.DefaultLimits())
	if e != nil {
		return e
	}
	pv, e := pi.View(native.Primary)
	if e != nil {
		return e
	}
	p, e := pv.Admit()
	if e != nil {
		return e
	}
	si, e := native.Parse(r.secondary, native.DefaultLimits())
	if e != nil {
		return e
	}
	sv, e := si.View(native.Secondary)
	if e != nil {
		return e
	}
	d, e := explicit.Admit(sv, si.Source())
	if e != nil {
		return e
	}
	if d.RecordCount() < 1 || d.RecordCount() > 32 {
		return errors.New("record cap")
	}
	if e = l.take(1<<20, 64<<20); e != nil {
		return e
	}
	plan, e := body.Compile(p, pi.Source(), body.DefaultLimits())
	if e != nil {
		return e
	}
	if !plan.Valid() {
		return errors.New("invalid computed plan")
	}
	if e = l.take(4<<20, 8<<20); e != nil {
		return e
	}
	out := report{Schema: "wordling.merge-field-body.v1", Scope: "per-record-body-only-no-pagination-or-native-output", PrimarySHA256: hash(r.primary), SecondarySHA256: hash(r.secondary)}
	totalBody, totalTrace, encodedBound := 0, 0, 1024
	for n := 1; n <= d.RecordCount(); n++ {
		if e = l.take(2<<20, 5<<20); e != nil {
			return e
		}
		result, e := plan.Evaluate(d, si.Source(), n)
		if e != nil {
			return e
		}
		if !result.Valid() {
			return errors.New("invalid computed result")
		}
		pr, ok := result.Provenance()
		if !ok || !pr.Primary.Equal(pi.Source()) || !pr.Secondary.Equal(si.Source()) || pr.Record != n {
			return errors.New("computed owner mismatch")
		}
		b, e := result.Bytes()
		if e != nil {
			return e
		}
		totalBody += len(b)
		totalTrace += len(pr.Trace)
		if totalBody > maxTotalBody || totalTrace > maxTotalTrace {
			return errors.New("cumulative body or trace cap")
		}
		// Safe upper bound for the fixed schema, base64 bytes, decimal spans and
		// constant source tags; checked before row expansion or JSON marshaling.
		bound := 256 + 4*((len(b)+2)/3) + 128*len(pr.Trace) + 1024*len(pr.Accesses)
		if bound > maxEncoded-encodedBound {
			return errors.New("encoded response preflight")
		}
		encodedBound += bound
		rr := row{Record: n, Body: b, Conditional: pr.Conditional, Blank: pr.Blank}
		for _, t := range pr.Trace {
			b, e := span(t.Span)
			if e != nil {
				return e
			}
			source := "primary"
			if t.Field {
				source = "secondary"
			}
			rr.Trace = append(rr.Trace, trace{t.Start, t.Length, source, b})
		}
		for _, a := range pr.Accesses {
			x := access{Field: a.Field, Decision: a.Decision, StoredCount: a.Record.StoredCount}
			pairs := []struct {
				s native.Span
				b *bounds
			}{{a.Value.Content, &x.Content}, {a.Value.EndField, &x.EndField}, {a.Value.Separator, &x.Separator}, {a.Record.Raw, &x.Record}, {a.Record.EndRecord, &x.EndRecord}, {a.Record.Tail, &x.Tail}}
			for _, p := range pairs {
				*p.b, e = span(p.s)
				if e != nil {
					return e
				}
			}
			for _, s := range a.Record.Interstitial {
				b, e := span(s)
				if e != nil {
					return e
				}
				x.Interstitial = append(x.Interstitial, b)
			}
			rr.Accesses = append(rr.Accesses, x)
		}
		out.Rows = append(out.Rows, rr)
	}
	encoded, e := json.Marshal(out)
	if e != nil {
		return e
	}
	if len(encoded)+1 > maxEncoded || len(encoded)+1 > encodedBound {
		return errors.New("encoded response cap")
	}
	encoded = append(encoded, '\n')
	n, e := writer.Write(encoded)
	if e != nil {
		return e
	}
	if n != len(encoded) {
		return io.ErrShortWrite
	}
	return nil
}
func main() {
	if len(os.Args) != 1 {
		fmt.Fprintln(os.Stderr, "evaluate: no arguments permitted")
		os.Exit(2)
	}
	if e := run(os.Stdin, os.Stdout); e != nil {
		message := e.Error()
		if len(message) > 4096 {
			message = message[:4096]
		}
		fmt.Fprintln(os.Stderr, "evaluate:", message)
		os.Exit(1)
	}
}
