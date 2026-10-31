package runtime

import (
	"strconv"

	"github.com/lynncoleart/wordling/internal/macro/wpm"
)

type value struct {
	number   int64
	text     []uint16
	numeric  bool
	assigned bool
}
type expression struct {
	slot        uint32
	code        []*expression
	number      int64
	name        string
	op          uint16
	left, right *expression
	literal     []uint16
}
type evalFailure string

func (e evalFailure) Error() string { return string(e) }

func (e *expression) eval(vars []value) (value, error) {
	if e == nil {
		return value{}, evalFailure("InvalidExpression")
	}
	if e.literal != nil {
		return value{text: e.literal}, nil
	}
	if e.op != 0 {
		a, err := e.left.eval(vars)
		if err != nil {
			return value{}, err
		}
		b, err := e.right.eval(vars)
		if err != nil {
			return value{}, err
		}
		if !a.numeric || !b.numeric {
			return value{}, evalFailure("UnsupportedCoercion")
		}
		switch e.op {
		case '+':
			n, ok := checkedAdd(a.number, b.number)
			if !ok {
				return value{}, evalFailure("NumericOverflow")
			}
			return value{number: n, numeric: true}, nil
		case '<':
			var n int64
			if a.number < b.number {
				n = 1
			}
			return value{number: n, numeric: true}, nil
		case '=':
			var n int64
			if a.number == b.number {
				n = 1
			}
			return value{number: n, numeric: true}, nil
		}
		return value{}, evalFailure("UnsupportedOperator")
	}
	if e.name != "" {
		if int(e.slot) >= len(vars) || !vars[e.slot].assigned {
			return value{}, evalFailure("UndefinedVariable")
		}
		return vars[e.slot], nil
	}
	return value{number: e.number, numeric: true}, nil
}
func (v value) words() []uint16 {
	if !v.numeric {
		return v.text
	}
	s := strconv.FormatInt(v.number, 10)
	out := make([]uint16, len(s))
	for n := range s {
		out[n] = uint16(s[n])
	}
	return out
}

// Private value backing is immutable. Runtime views share it; public effect
// words are constructed and copied independently at the callback boundary.
func (v value) wordLen() int {
	if !v.numeric {
		return len(v.text)
	}
	return len(strconv.FormatInt(v.number, 10))
}

// Names and evaluation order are compiled once. Runtime performs no name hash,
// textual number parse, recursive tree traversal, or long-value scan.
func (e *expression) bind(ids map[string]uint32) {
	var emit func(*expression)
	emit = func(n *expression) {
		if n == nil {
			return
		}
		if n.name != "" {
			n.slot = ids[n.name]
		}
		emit(n.left)
		emit(n.right)
		e.code = append(e.code, n)
	}
	emit(e)
}
func (e *expression) references(out map[string]bool) {
	if e == nil {
		return
	}
	if e.name != "" {
		out[e.name] = true
	}
	e.left.references(out)
	e.right.references(out)
}
func checkedAdd(a, b int64) (int64, bool) {
	const max = int64(^uint64(0) >> 1)
	const min = -max - 1
	if b > 0 && a > max-b || b < 0 && a < min-b {
		return 0, false
	}
	return a + b, true
}

// Parse the exact bounded numeric/reference/single-binary grammar, never a
// normalized textual macro listing. VARIABLE's inner tilde remains significant.
func parseExpression(words []wpm.Word, literalOK bool, limit uint32) (*expression, error) {
	pos := 0
	atom := func() (*expression, error) {
		if pos >= len(words) {
			return nil, evalFailure("UnsupportedExpression")
		}
		if words[pos].Value == 0xfc34 {
			pos++
			start := pos
			for pos < len(words) && words[pos].Value != '~' {
				if words[pos].Value < 0x20 || words[pos].Value > 0x7e {
					return nil, evalFailure("UnsupportedExpression")
				}
				pos++
			}
			if pos == start || pos == len(words) || uint32(pos-start) > limit {
				return nil, evalFailure("UnsupportedExpression")
			}
			buf := make([]byte, pos-start)
			for n, w := range words[start:pos] {
				buf[n] = byte(w.Value)
			}
			pos++
			return &expression{name: string(buf)}, nil
		}
		start := pos
		if words[pos].Value == '-' || words[pos].Value == '+' {
			pos++
		}
		digits := pos
		for pos < len(words) && words[pos].Value >= '0' && words[pos].Value <= '9' {
			pos++
		}
		if pos == digits || uint32(pos-start) > limit {
			return nil, evalFailure("UnsupportedExpression")
		}
		buf := make([]byte, pos-start)
		for n, w := range words[start:pos] {
			buf[n] = byte(w.Value)
		}
		n, err := strconv.ParseInt(string(buf), 10, 64)
		if err != nil {
			return nil, evalFailure("UnsupportedNumber")
		}
		return &expression{number: n}, nil
	}
	a, err := atom()
	if err == nil && pos == len(words) {
		return a, nil
	}
	if err == nil && pos < len(words) {
		op := words[pos].Value
		pos++
		if op == '+' || op == '<' || op == '=' {
			b, err := atom()
			if err == nil && pos == len(words) {
				return &expression{op: op, left: a, right: b}, nil
			}
		}
	}
	if literalOK && len(words) > 0 && uint32(len(words)) <= limit {
		quoted := words[0].Value == '"'
		if quoted && (len(words) < 3 || words[len(words)-1].Value != '"') {
			return nil, evalFailure("UnsupportedExpression")
		}
		out := make([]uint16, len(words))
		letters := false
		for n, w := range words {
			v := w.Value
			if v >= 'a' && v <= 'z' || v >= 'A' && v <= 'Z' {
				letters = true
			} else if v != ' ' && !(quoted && v == '"' && (n == 0 || n == len(words)-1)) {
				return nil, evalFailure("UnsupportedExpression")
			}
			out[n] = v
		}
		if letters {
			return &expression{literal: out}, nil
		}
	}
	return nil, evalFailure("UnsupportedExpression")
}
