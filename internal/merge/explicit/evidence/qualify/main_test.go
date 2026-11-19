package main

import (
	"bytes"
	"encoding/json"
	"os"
	"strings"
	"testing"
)

func TestActualQualificationPath(t *testing.T) {
	b, e := os.ReadFile("../../../../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-209/SECOND.WP5")
	if e != nil {
		t.Fatal(e)
	}
	r := Request{Inputs: []Input{{Name: "arbitrary", Role: "Secondary", Data: b}}}
	q, _ := json.Marshal(r)
	var out bytes.Buffer
	if e := run(bytes.NewReader(q), &out); e != nil {
		t.Fatal(e)
	}
	var report Report
	if e = json.Unmarshal(out.Bytes(), &report); e != nil {
		t.Fatal(e)
	}
	if report.Scope != "explicit-field-DATA-only" || len(report.Inputs) != 1 {
		t.Fatal("report")
	}
	x := report.Inputs[0]
	if !x.Qualified || x.GenericSupported || x.GenericAdmitted || len(x.Records) != 2 || x.Records[0].Fields[0].Hex != "416c696365" || !x.Records[1].Fields[1].ExplicitlyEmpty || x.Records[1].Missing.Category != "ExplicitFieldMissing" {
		t.Fatalf("invalid qualification %+v", x)
	}
	if x.Records[0].Tail.Length != 0 || len(x.Findings) != 4 || len(x.Records[0].OpaqueHex) != 64 {
		t.Fatal("provenance")
	}
	r.Inputs[0].Name = "unrelated"
	r.Inputs[0].Data = bytes.Replace(b, []byte("Alice"), []byte("Clara"), 1)
	q, _ = json.Marshal(r)
	out.Reset()
	if e = run(bytes.NewReader(q), &out); e != nil {
		t.Fatal(e)
	}
	if !strings.Contains(out.String(), "436c617261") {
		t.Fatal("observer/output replay")
	}
}
func TestAtomicDiagnosticRefusal(t *testing.T) {
	for _, b := range [][]byte{[]byte(`{"inputs":[]}`), []byte(`{"inputs":[],"extra":true}`), []byte(`{"inputs":`), []byte(`{"inputs":[{"name":"x","role":"Secondary","data":"AA=="}]}`)} {
		var o bytes.Buffer
		if e := run(bytes.NewReader(b), &o); e == nil || o.Len() != 0 {
			t.Fatalf("partial %v %s", e, o.String())
		}
	}
}
