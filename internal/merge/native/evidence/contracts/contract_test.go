// Additional public-only semantic contract witnesses, independent of the timed
// fuzz target package. Fixtures are synthetic, not a native writer/product API.
package contracts_test

import (
	"bytes"
	n "github.com/lynncoleart/wordling/internal/merge/native"
	"testing"
)

func framed(body []byte) []byte {
	p := make([]byte, 66)
	copy(p, []byte{255, 'W', 'P', 'C', 66, 0, 0, 0, 1, 10, 0, 1})
	copy(p[16:], []byte{251, 255, 5, 0, 50, 0})
	return append(p, body...)
}

var field = []byte{0xde, 0x36, 4, 0, 4, 0, 0x36, 0xde}
var page = []byte{0xde, 0x4d, 4, 0, 4, 0, 0x4d, 0xde}

func TestMalformedOperandNeverSwallowsFollowingNativeCommand(t *testing.T) {
	raw := framed(append(append([]byte(nil), field...), page...))
	im, e := n.Parse(raw, n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v, e := im.View(n.Primary)
	if e != nil {
		t.Fatal(e)
	}
	i, _ := v.Inspect()
	if v.Supported() || len(i.Commands) != 2 || i.Commands[0].Kind != n.FieldCommand || i.Commands[0].Operand.Kind != 0 || i.Commands[1].Kind != n.PageOff {
		t.Fatalf("unresolved operand swallowed command: %+v", i.Commands)
	}
	s, _ := i.Commands[1].Function.Bounds()
	if s.Offset != 74 || s.Length != 8 {
		t.Fatal("following command ownership")
	}
}
func TestOperandDataAndTildeExactOutsideFrameOwnership(t *testing.T) {
	raw := framed(append(append([]byte(nil), field...), []byte("1~Z")...))
	im, e := n.Parse(raw, n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v, e := im.View(n.Primary)
	if e != nil {
		t.Fatal(e)
	}
	i, _ := v.Inspect()
	if !v.Supported() || len(i.Commands) != 1 {
		t.Fatal(i.Findings)
	}
	op := i.Commands[0].Operand
	data, ok := v.Bytes(op.Data)
	if !ok || !bytes.Equal(data, []byte("1")) {
		t.Fatal("wrong operand bytes")
	}
	bounds, _ := op.Data.Bounds()
	end, _ := op.Terminator.Bounds()
	if bounds.Offset != 74 || bounds.Length != 1 || end.Offset != 75 || end.Length != 1 {
		t.Fatal("argument not owned at exact outside-frame offsets")
	}
	if op.Number != 1 {
		t.Fatal("wrong numeric operand")
	}
	after, _ := v.Bytes(i.Tokens[len(i.Tokens)-1].Raw)
	if !bytes.Equal(after, []byte("Z")) {
		t.Fatal("following literal swallowed")
	}
}
func TestResultRoleAndCopiedBoundsCannotMintProgram(t *testing.T) {
	raw := framed([]byte("ordinary text"))
	im, e := n.Parse(raw, n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v, e := im.View(n.Result)
	if e != nil {
		t.Fatal(e)
	}
	inspection, _ := v.Inspect()
	inspection.Role = n.Primary
	inspection.Findings = nil
	if v.Supported() {
		t.Fatal("Result inspection asserted new role")
	}
	if p, e := v.Admit(); e == nil || p.Valid() {
		t.Fatal("Result admission")
	}
	s := inspection.Tokens[0].Raw
	b, ok := s.Bounds()
	if !ok {
		t.Fatal("span")
	}
	b.Offset = -1
	b.Length = 1 << 30
	actual, ok := v.Bytes(s)
	if !ok || !bytes.Equal(actual, []byte("o")) {
		t.Fatal("caller changed captured bounds")
	}
}
func TestMalformedOuterAndRetainedSemanticPayloads(t *testing.T) {
	raw := framed(field)
	for _, bad := range [][]byte{nil, raw[:15], append([]byte(nil), raw[:len(raw)-1]...), framed([]byte{0xde, 0x36, 0, 0, 0, 0, 0x36, 0xde}), framed([]byte{0xde, 0x34, 6, 0, 2}), framed([]byte{0})} {
		im, e := n.Parse(bad, n.DefaultLimits())
		if e == nil || im != nil {
			t.Fatalf("malformed accepted %x", bad)
		}
	}
	for _, payload := range [][]byte{{0xde, 0x34, 4, 0, 4, 0, 0x34, 0xde}, {0xde, 0x31, 6, 0, 2, 0, 6, 0, 0x31, 0xde}, {0xde, 0x34, 6, 0, 0, 0, 6, 0, 0x34, 0xde}} {
		input := framed(payload)
		im, e := n.Parse(input, n.DefaultLimits())
		if e != nil {
			t.Fatal(e)
		}
		v, e := im.View(n.Secondary)
		if e != nil {
			t.Fatal(e)
		}
		if v.Supported() || !bytes.Equal(v.Export(), input) {
			t.Fatal("semantic payload discarded/admitted")
		}
		i, _ := v.Inspect()
		if len(i.Findings) == 0 {
			t.Fatal("silent unsupported")
		}
	}
}
func TestMatchingRawCountAndMarkerCountStillUnresolved(t *testing.T) {
	// This synthetic coincidence is NOT a count algorithm or original witness.
	ef := []byte{0xde, 0x31, 4, 0, 4, 0, 0x31, 0xde}
	er := []byte{0xde, 0x34, 6, 0, 2, 0, 6, 0, 0x34, 0xde}
	body := []byte("a")
	body = append(body, ef...)
	body = append(body, 10, 'b')
	body = append(body, ef...)
	body = append(body, 10)
	body = append(body, er...)
	im, e := n.Parse(framed(body), n.DefaultLimits())
	if e != nil {
		t.Fatal(e)
	}
	v, e := im.View(n.Secondary)
	if e != nil {
		t.Fatal(e)
	}
	i, _ := v.Inspect()
	found := false
	for _, f := range i.Findings {
		found = found || f.Code == "RecordCountUnresolved"
	}
	if v.Supported() || !found || len(i.Records) != 1 || i.Records[0].StoredCount != 2 || len(i.Records[0].Fields) != 2 {
		t.Fatal("guessed rawcount==markers admission")
	}
}
