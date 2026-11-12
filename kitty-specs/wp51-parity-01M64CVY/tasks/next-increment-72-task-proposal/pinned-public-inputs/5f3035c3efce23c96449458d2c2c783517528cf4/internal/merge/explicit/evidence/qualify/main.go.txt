// qualify is an offline maintainer DATA qualifier. It never executes a primary,
// emits a native document, changes generic admission or calls the application.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

const maxJSON = 40 << 20

type Input struct {
	Name string `json:"name"`
	Role string `json:"role"`
	Data []byte `json:"data"`
}
type Request struct {
	Inputs []Input `json:"inputs"`
}
type Bounds struct {
	Offset int `json:"offset"`
	Length int `json:"length"`
}
type Field struct {
	Ordinal         int    `json:"ordinal"`
	Hex             string `json:"hex"`
	ExplicitlyEmpty bool   `json:"explicitly_empty"`
	Content         Bounds `json:"content"`
	EndField        Bounds `json:"end_field"`
	Separator       Bounds `json:"separator"`
}
type Missing struct {
	Record   int    `json:"record"`
	Field    int    `json:"field"`
	Category string `json:"category"`
	Valid    bool   `json:"valid"`
}
type Record struct {
	Ordinal     int     `json:"ordinal"`
	StoredCount uint16  `json:"stored_count"`
	Raw         Bounds  `json:"raw"`
	EndRecord   Bounds  `json:"end_record"`
	Tail        Bounds  `json:"tail"`
	Fields      []Field `json:"fields"`
	Opaque      Bounds  `json:"opaque"`
	OpaqueHex   string  `json:"opaque_hex"`
	Hardpage    Bounds  `json:"hardpage"`
	Missing     Missing `json:"missing"`
}
type Finding struct {
	Code   string `json:"code"`
	At     Bounds `json:"at"`
	Detail string `json:"detail"`
}
type Observation struct {
	Name             string    `json:"name"`
	Role             string    `json:"role"`
	Bytes            int       `json:"bytes"`
	SHA256           string    `json:"sha256"`
	ExportExact      bool      `json:"export_exact"`
	Qualified        bool      `json:"qualified"`
	GenericSupported bool      `json:"generic_supported"`
	GenericAdmitted  bool      `json:"generic_admitted"`
	Records          []Record  `json:"records"`
	Findings         []Finding `json:"findings"`
}
type Report struct {
	Schema          string        `json:"schema"`
	Scope           string        `json:"scope"`
	Inputs          []Observation `json:"inputs"`
	TotalInputBytes int           `json:"total_input_bytes"`
	TotalValueBytes int           `json:"total_value_bytes"`
}

func bounds(s native.Span) (Bounds, error) {
	b, ok := s.Bounds()
	if !ok {
		return Bounds{}, errors.New("invalid provenance span")
	}
	return Bounds{b.Offset, b.Length}, nil
}
func mustBounds(s native.Span) Bounds { b, _ := bounds(s); return b }
func observe(in Input) (Observation, int, error) {
	out := Observation{Name: in.Name, Role: in.Role, Bytes: len(in.Data), Findings: []Finding{}}
	if len(in.Name) == 0 || len(in.Name) > 512 || len(in.Data) > native.MaxBytes {
		return out, 0, errors.New("input bounds")
	}
	role := map[string]native.Role{"Primary": native.Primary, "Secondary": native.Secondary, "Result": native.Result}[in.Role]
	if role == 0 {
		return out, 0, errors.New("explicit role required")
	}
	image, e := native.Parse(in.Data, native.DefaultLimits())
	if e != nil {
		return out, 0, e
	}
	view, e := image.View(role)
	if e != nil {
		return out, 0, e
	}
	raw := image.Export()
	out.ExportExact = bytes.Equal(raw, in.Data)
	if !out.ExportExact {
		return out, 0, errors.New("native export changed")
	}
	sum := sha256.Sum256(raw)
	out.SHA256 = hex.EncodeToString(sum[:])
	out.GenericSupported = view.Supported()
	program, admitErr := view.Admit()
	out.GenericAdmitted = admitErr == nil && program.Valid()
	info, _ := view.Inspect()
	for _, f := range info.Findings {
		out.Findings = append(out.Findings, Finding{f.Code, mustBounds(f.At), f.Detail})
	}
	if role != native.Secondary {
		if d, e := explicit.Admit(view, image.Source()); e == nil || d.Valid() {
			return out, 0, errors.New("wrong role DATA accepted")
		}
		return out, 0, nil
	}
	data, e := explicit.Admit(view, image.Source())
	if e != nil {
		return out, 0, e
	}
	if !data.Valid() || !data.Source().Equal(image.Source()) || out.GenericSupported || out.GenericAdmitted {
		return out, 0, errors.New("DATA/generic authority mismatch")
	}
	provenance, ok := data.Inspect()
	if !ok {
		return out, 0, errors.New("provenance missing")
	}
	out.Qualified = true
	total := 0
	for r := 1; r <= data.RecordCount(); r++ {
		original := provenance.Records[r-1]
		rec := Record{Ordinal: r, StoredCount: original.StoredCount, Raw: mustBounds(original.Raw), EndRecord: mustBounds(original.EndRecord), Tail: mustBounds(original.Tail), Opaque: mustBounds(original.Interstitial[0]), Hardpage: mustBounds(original.Interstitial[1])}
		opaque, ok := view.Bytes(original.Interstitial[0])
		if !ok {
			return out, 0, errors.New("opaque source mismatch")
		}
		rec.OpaqueHex = hex.EncodeToString(opaque)
		for f := 1; f <= len(original.Fields); f++ {
			value, e := data.Field(r, f)
			if e != nil || !value.Valid() {
				return out, 0, errors.New("explicit value missing")
			}
			b, e := value.Bytes()
			if e != nil {
				return out, 0, e
			}
			empty, e := value.ExplicitlyEmpty()
			if e != nil {
				return out, 0, e
			}
			_, p, ok := value.Provenance()
			if !ok {
				return out, 0, errors.New("value provenance missing")
			}
			total += len(b)
			if total > len(in.Data) {
				return out, 0, errors.New("cumulative value bytes")
			}
			rec.Fields = append(rec.Fields, Field{f, hex.EncodeToString(b), empty, mustBounds(p.Content), mustBounds(p.EndField), mustBounds(p.Separator)})
		}
		absent, e := data.Field(r, len(original.Fields)+1)
		var missing *explicit.ExplicitFieldMissing
		if !errors.As(e, &missing) || absent.Valid() {
			return out, 0, errors.New("missing became empty")
		}
		rec.Missing = Missing{missing.Record, missing.Field, "ExplicitFieldMissing", false}
		out.Records = append(out.Records, rec)
	}
	if view.Supported() {
		return out, 0, errors.New("generic blocker changed")
	}
	if p, e := view.Admit(); e == nil || p.Valid() {
		return out, 0, errors.New("generic admitted after DATA")
	}
	return out, total, nil
}
func run(reader io.Reader, writer io.Writer) error {
	raw, e := io.ReadAll(io.LimitReader(reader, maxJSON+1))
	if e != nil {
		return e
	}
	if len(raw) > maxJSON {
		return errors.New("request JSON cap")
	}
	decoder := json.NewDecoder(bytes.NewReader(raw))
	decoder.DisallowUnknownFields()
	var request Request
	if e = decoder.Decode(&request); e != nil {
		return e
	}
	var extra any
	if decoder.Decode(&extra) != io.EOF {
		return errors.New("trailing JSON")
	}
	if len(request.Inputs) < 1 || len(request.Inputs) > 30 {
		return errors.New("input roster cap")
	}
	report := Report{Schema: "wordling.explicit-secondary-data.v1", Scope: explicit.Scope}
	names := map[string]bool{}
	for _, in := range request.Inputs {
		if names[in.Name] {
			return errors.New("duplicate name")
		}
		names[in.Name] = true
		report.TotalInputBytes += len(in.Data)
		if report.TotalInputBytes > 30*native.MaxBytes {
			return errors.New("total input cap")
		}
		o, n, e := observe(in)
		if e != nil {
			return fmt.Errorf("%s: %w", in.Name, e)
		}
		report.TotalValueBytes += n
		report.Inputs = append(report.Inputs, o)
	}
	encoded, e := json.Marshal(report)
	if e != nil {
		return e
	}
	if len(encoded) > 64<<20 {
		return errors.New("report cap")
	}
	encoded = append(encoded, '\n')
	_, e = writer.Write(encoded)
	return e
}
func main() {
	if len(os.Args) != 1 {
		fmt.Fprintln(os.Stderr, "qualify: no arguments permitted")
		os.Exit(2)
	}
	if e := run(os.Stdin, os.Stdout); e != nil {
		message := e.Error()
		if len(message) > 4096 {
			message = message[:4096]
		}
		fmt.Fprintln(os.Stderr, "qualify:", message)
		os.Exit(1)
	}
}
