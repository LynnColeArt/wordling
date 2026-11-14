package runtime_test

import (
	"bytes"
	"context"
	"encoding/binary"
	"errors"
	"os"
	"testing"

	mac "github.com/lynncoleart/wordling/internal/macro/runtime"
	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

type recordingSink struct{ keys []uint16 }

func (s *recordingSink) Capabilities() mac.Policy {
	return mac.Policy{ASCII: true, DisplayControl: true, Keys: []uint16{wpm.RecordedEnter, wpm.RecordedLeft}}
}
func (s *recordingSink) Apply(_ context.Context, e mac.Effect) (mac.EffectResult, error) {
	if e.Kind == "key" {
		s.keys = append(s.keys, e.Words[0].Value)
	}
	return mac.EffectResult{}, nil
}

func TestCapturedRecordedEnterDeliversExactlyOneKey(t *testing.T) {
	raw, err := os.ReadFile("../../../docs/research/reference-runs/mission1-macro-recording/TYPED.WPM")
	if err != nil {
		t.Fatal(err)
	}
	limits := mac.DefaultLimits()
	sink := &recordingSink{}
	program, err := mac.Compile(image(t, raw), sink.Capabilities(), limits)
	if err != nil {
		t.Fatal(err)
	}
	vm, err := mac.New(program, sink, nil, limits)
	if err != nil {
		t.Fatal(err)
	}
	result := vm.Step(context.Background(), limits.SliceSteps)
	if result.State != "complete" || len(sink.keys) != 2 || sink.keys[0] != wpm.RecordedEnter || sink.keys[1] != wpm.RecordedLeft {
		t.Fatalf("state %+v, keys %x", result, sink.keys)
	}
	at := bytes.Index(raw, []byte{0x0a, 0x80, 0x0a, 0x00})
	if at < 0 {
		t.Fatal("DOS fixture misses Enter companion")
	}
	binary.LittleEndian.PutUint16(raw[at+2:], 'Z')
	_, err = mac.Compile(image(t, raw), sink.Capabilities(), limits)
	var bad *mac.Failure
	if !errors.As(err, &bad) || bad.Code != "MalformedOperand" {
		t.Fatalf("malformed Enter: %v", err)
	}
}
