package body

import (
	"bytes"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

type compiler struct {
	p                  native.Program
	info               native.Inspection
	budget             budget
	token, command, at int
}

func (c *compiler) read(s native.Span) ([]byte, error) {
	b, ok := s.Bounds()
	if !ok {
		return nil, fail("InvalidSpan")
	}
	if e := c.budget.take(uint64(b.Length)+1, uint64(b.Length)); e != nil {
		return nil, e
	}
	raw, ok := c.p.Bytes(s)
	if !ok || len(raw) != b.Length {
		return nil, fail("ForeignSpan")
	}
	return raw, nil
}
func (c *compiler) next(s native.Span, kind native.TokenKind, code, sub byte) error {
	if e := c.budget.take(2, 0); e != nil {
		return e
	}
	if c.token >= len(c.info.Tokens) {
		return fail("TokenMissing")
	}
	t := c.info.Tokens[c.token]
	b, ok := s.Bounds()
	if !ok || b.Offset != c.at || t.Raw != s || t.Kind != kind || t.Code != code || t.Subfunction != sub {
		return fail("TokenCoverage")
	}
	c.at += b.Length
	c.token++
	return nil
}
func (c *compiler) literals() ([]literal, error) {
	start := c.token
	for c.token < len(c.info.Tokens) {
		t := c.info.Tokens[c.token]
		if t.Kind != native.Character || t.Code < 0x20 || t.Code > 0x7e || t.Code == '~' {
			break
		}
		raw, e := c.read(t.Raw)
		if e != nil {
			return nil, e
		}
		if len(raw) != 1 || raw[0] != t.Code {
			return nil, fail("Literal")
		}
		if e = c.next(t.Raw, native.Character, t.Code, 0); e != nil {
			return nil, e
		}
	}
	n := c.token - start
	if n == 0 {
		return nil, fail("NonemptyLiteralRequired")
	}
	if e := c.budget.take(uint64(n), size[literal](n)); e != nil {
		return nil, e
	}
	out := make([]literal, n)
	for j := range out {
		t := c.info.Tokens[start+j]
		out[j] = literal{t.Raw, t.Code}
	}
	return out, nil
}
func (c *compiler) cmd(kind native.CommandKind, number uint16, match int) error {
	if e := c.budget.take(4, 0); e != nil {
		return e
	}
	if c.command >= len(c.info.Commands) || c.token >= len(c.info.Tokens) {
		return fail("CommandMissing")
	}
	cmd := c.info.Commands[c.command]
	t := c.info.Tokens[c.token]
	if cmd.Kind != kind || cmd.Function != t.Raw || cmd.HasRawCount || cmd.RawCount != 0 || cmd.Match != match {
		return fail("CommandShape")
	}
	raw, e := c.read(cmd.Function)
	if e != nil {
		return e
	}
	if !bytes.Equal(raw, []byte{0xde, byte(kind), 4, 0, 4, 0, byte(kind), 0xde}) {
		return fail("CommandFrame")
	}
	payload, e := c.read(cmd.Payload)
	if e != nil {
		return e
	}
	f, _ := cmd.Function.Bounds()
	p, _ := cmd.Payload.Bounds()
	if len(payload) != 0 || p.Offset != f.Offset+4 {
		return fail("Payload")
	}
	if e = c.next(t.Raw, native.Function, 0xde, byte(kind)); e != nil {
		return e
	}
	c.command++
	if number == 0 {
		if cmd.Operand != (native.Operand{}) {
			return fail("UnexpectedOperand")
		}
		return nil
	}
	if cmd.Operand.Kind != native.FieldNumber || cmd.Operand.Number != number {
		return fail("Operand")
	}
	digits, e := c.read(cmd.Operand.Data)
	if e != nil {
		return e
	}
	term, e := c.read(cmd.Operand.Terminator)
	if e != nil {
		return e
	}
	if len(digits) != 1 || digits[0] != '0'+byte(number) || !bytes.Equal(term, []byte{'~'}) {
		return fail("OperandBytes")
	}
	if e = c.next(cmd.Operand.Data, native.Character, digits[0], 0); e != nil {
		return e
	}
	return c.next(cmd.Operand.Terminator, native.Character, '~', 0)
}

// Compile makes one precharged defensive inspection, then validates every token
// and command of the whole primary. No mutable inspection is accepted as input.
func Compile(primary native.Program, expectedPrimary native.Source, limits Limits) (Plan, error) {
	if !limits.valid() {
		return Plan{}, fail("InvalidLimits")
	}
	if !primary.Valid() || !expectedPrimary.Valid() || !primary.Source().Equal(expectedPrimary) {
		return Plan{}, fail("PrimaryOwner")
	}
	c := compiler{p: primary, budget: budget{uint64(limits.WorkUnits), compileAllocation}}
	if e := c.budget.take(inspectionWork, inspectAllocation); e != nil {
		return Plan{}, e
	}
	info, ok := primary.Inspect()
	if !ok || info.Role != native.Primary || !info.Source.Equal(expectedPrimary) || info.FindingsCapped || len(info.Findings) != 0 || len(info.Records) != 0 || len(info.Tokens) == 0 || len(info.Tokens) > limits.PrimaryTokens {
		return Plan{}, fail("WholePrimary")
	}
	c.info = info
	first, ok := info.Tokens[0].Raw.Bounds()
	if !ok {
		return Plan{}, fail("BodyStart")
	}
	c.at = first.Offset
	if e := c.budget.take(1, size[proof](1)); e != nil {
		return Plan{}, e
	}
	p := &proof{program: primary, source: expectedPrimary, limits: limits}
	var e error
	if len(info.Commands) == 1 && info.Commands[0].Kind == native.FieldCommand {
		p.first, e = c.literals()
		if e == nil {
			e = c.cmd(native.FieldCommand, 1, -1)
		}
		if e == nil {
			if c.token >= len(info.Tokens) {
				e = fail("TerminalHRMissing")
			} else {
				t := info.Tokens[c.token]
				var raw []byte
				raw, e = c.read(t.Raw)
				if e == nil && (!bytes.Equal(raw, []byte{0x0a})) {
					e = fail("TerminalHR")
				}
				if e == nil {
					e = c.next(t.Raw, native.Control, 0x0a, 0)
				}
				if e == nil {
					e = c.budget.take(1, size[literal](1))
					if e == nil {
						p.after = []literal{{t.Raw, 0x0a}}
					}
				}
			}
		}
	} else if len(info.Commands) == 4 {
		p.conditional = true
		e = c.cmd(native.IfBlank, 2, 2)
		if e == nil {
			p.first, e = c.literals()
		}
		if e == nil {
			e = c.cmd(native.Else, 0, 2)
		}
		if e == nil {
			p.second, e = c.literals()
		}
		if e == nil {
			e = c.cmd(native.EndIf, 0, 0)
		}
		if e == nil {
			p.after, e = c.literals()
		}
		if e == nil {
			e = c.cmd(native.FieldCommand, 1, -1)
		}
	} else {
		e = fail("UnsupportedForm")
	}
	if e != nil {
		return Plan{}, e
	}
	if c.token != len(info.Tokens) || c.command != len(info.Commands) {
		return Plan{}, fail("IncompleteCoverage")
	}
	return Plan{p}, nil
}
