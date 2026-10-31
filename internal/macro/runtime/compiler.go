package runtime

import (
	"github.com/lynncoleart/wordling/internal/macro/wpm"
	"sort"
)

const (
	opLiteral uint16 = 1
	opKey     uint16 = 2
)

type instruction struct {
	op         uint16
	at         wpm.Span
	words      []wpm.Word
	name       string
	args       []*expression
	jump, loop int
}

// Program is immutable and reusable by independent Machines. Only Compile creates
// an accepted Program; a zero value carries no execution permission.
type Program struct {
	source                                           [32]byte
	image                                            *wpm.Image
	code                                             []instruction
	policy, required                                 Policy
	limits                                           Limits
	cost                                             uint64
	variables, maxLoop, maxExpression, maxValueWords uint32
	hasVariables, needsChild                         bool
}
type block struct {
	kind                uint16
	start, other        int
	references, written map[string]bool
}
type compiler struct {
	p         *Program
	words     []wpm.Word
	pos       int
	limits    Limits
	blocks    []*block
	loops     []*block
	variables map[string]bool
	assigned  map[string]bool
	labels    map[string]int
}

// Compile preflights the whole primary input before any effect. Source identity
// and native argument/word spans are retained; no text macro listing is parsed.
func Compile(image *wpm.Image, policy Policy, limits Limits) (*Program, error) {
	if !validLimits(limits) {
		return nil, failed("InvalidLimit", [32]byte{}, wpm.Span{}, "positive limits must not exceed declared maxima")
	}
	if image == nil {
		return nil, failed("InvalidImage", [32]byte{}, wpm.Span{}, "nil image")
	}
	// Copy the wrapper: whole-value assignment to the caller's *Image must not
	// retarget this compiled snapshot. Its private backing is immutable by API.
	imageSnapshot := *image
	image = &imageSnapshot
	info := image.Inspect()
	source := image.SHA256()
	if info.Header.Product != 1 || info.Header.FileType != 1 || info.Header.Major != 1 || info.Header.Minor != 1 || info.Body.Length < 2 {
		return nil, failed("InvalidImage", source, wpm.Span{}, "not a Parse-created WPM image")
	}
	if len(info.Findings) != 0 {
		return nil, failed("UnsupportedImage", source, info.Findings[0].Span, info.Findings[0].Code)
	}
	cost := uint64(info.Body.Length / 2)
	if cost > limits.Steps {
		return nil, failed("CompilationLimit", source, info.Body, "word scan exceeds run work budget")
	}
	words := image.BodyWords()
	// QUIT identity is known, but its behavior has not yet been qualified in the
	// required original contexts. Even an unreachable QUIT blocks compilation.
	for _, w := range words {
		if w.Value == 0xfc20 {
			return nil, failed("UnqualifiedQuit", source, w.Span, "original QUIT handoff prerequisite is not approved")
		}
	}
	p := &Program{source: source, image: image, policy: copiedPolicy(policy), limits: limits, cost: cost}
	c := compiler{p: p, words: words, limits: limits, variables: map[string]bool{}, assigned: map[string]bool{}, labels: map[string]int{}}
	for c.pos < len(words)-1 {
		if err := c.statement(); err != nil {
			return nil, err
		}
	}
	if len(c.blocks) != 0 {
		return nil, c.err("UnmatchedStructure", p.code[c.blocks[len(c.blocks)-1].start].at, "missing END")
	}
	for n := range p.code {
		i := &p.code[n]
		if i.op == 0xfc14 || i.op == 0xfc1c || i.op == 0xfc1d {
			target, ok := c.labels[i.name]
			if !ok {
				return nil, c.err("MissingLabel", i.at, i.name)
			}
			i.jump = target + 1
		}
	}
	if err := c.handlerReachability(); err != nil {
		return nil, err
	}
	if p.hasVariables {
		for _, i := range p.code {
			if i.op == 0xfc18 {
				return nil, c.err("UnsupportedVariableScope", i.at, "variables across nested files are unqualified")
			}
		}
	}
	variableNames := make([]string, 0, len(c.variables))
	for name := range c.variables {
		variableNames = append(variableNames, name)
	}
	sort.Strings(variableNames)
	for _, name := range variableNames {
		if !c.assigned[name] {
			return nil, c.err("UndefinedVariable", info.Body, "variable has no assignment in this program: "+name)
		}
	}
	p.variables = uint32(len(c.variables))
	if !covers(policy, p.required) {
		return nil, c.err("UnsupportedPolicy", info.Body, "policy does not admit every compiled effect")
	}
	return p, nil
}
func (c *compiler) err(code string, at wpm.Span, detail string) error {
	return failed(code, c.p.source, at, detail)
}
func (c *compiler) span(start int) wpm.Span {
	first := c.words[start].Span
	last := c.words[c.pos-1].Span
	return wpm.Span{Offset: first.Offset, Length: last.Offset + last.Length - first.Offset}
}
func (c *compiler) name() (string, []wpm.Word, error) {
	start := c.pos
	for c.pos < len(c.words) && c.words[c.pos].Value != '~' {
		w := c.words[c.pos]
		if w.Value < 0x20 || w.Value > 0x7e {
			return "", nil, c.err("MalformedOperand", w.Span, "name requires literal words and terminating tilde")
		}
		c.pos++
		if uint32(c.pos-start) > c.limits.VariableWords {
			return "", nil, c.err("ValueLimit", w.Span, "name exceeds word budget")
		}
	}
	if c.pos == start || c.pos == len(c.words) {
		return "", nil, c.err("MalformedOperand", c.words[start].Span, "empty/unterminated name")
	}
	words := c.words[start:c.pos]
	buf := make([]byte, len(words))
	for n, w := range words {
		buf[n] = byte(w.Value)
	}
	c.pos++
	if uint32(len(words)) > c.p.maxValueWords {
		c.p.maxValueWords = uint32(len(words))
	}
	return string(buf), words, nil
}
func (c *compiler) operand(literalOK bool) (*expression, error) {
	start := c.pos
	for c.pos < len(c.words) {
		w := c.words[c.pos]
		if w.Value == '~' {
			if c.pos == start {
				return nil, c.err("MalformedOperand", w.Span, "empty expression/list item is not qualified")
			}
			expr, err := parseExpression(c.words[start:c.pos], literalOK, c.limits.VariableWords)
			c.pos++
			if err != nil {
				return nil, c.err("UnsupportedExpression", w.Span, err.Error())
			}
			depth := expressionDepth(expr)
			if depth > c.limits.ExpressionDepth {
				return nil, c.err("ExpressionLimit", w.Span, "expression nesting budget")
			}
			if depth > c.p.maxExpression {
				c.p.maxExpression = depth
			}
			refs := map[string]bool{}
			expr.references(refs)
			for name := range refs {
				if err := c.variable(name, w.Span, false); err != nil {
					return nil, err
				}
			}
			if len(refs) == 0 {
				v, err := expr.eval(nil)
				if err != nil {
					return nil, c.err(err.Error(), w.Span, "constant expression is unsupported")
				}
				length := uint32(len(v.words()))
				if length > c.limits.VariableWords {
					return nil, c.err("ValueLimit", w.Span, "constant value exceeds word budget")
				}
				if length > c.p.maxValueWords {
					c.p.maxValueWords = length
				}
			}
			if expr.literal != nil && uint32(len(expr.literal)) > c.p.maxValueWords {
				c.p.maxValueWords = uint32(len(expr.literal))
			}
			return expr, nil
		}
		if w.Value == 0xfc34 {
			c.pos++
			if _, _, err := c.name(); err != nil {
				return nil, err
			}
			continue
		}
		if w.Value < 0x20 || w.Value > 0x7e {
			return nil, c.err("MalformedOperand", w.Span, "unexpected instruction in expression")
		}
		c.pos++
	}
	return nil, c.err("MalformedOperand", c.words[start].Span, "missing outer tilde")
}
func expressionDepth(e *expression) uint32 {
	if e == nil {
		return 0
	}
	if e.name != "" {
		return 2
	}
	a, b := expressionDepth(e.left), expressionDepth(e.right)
	if b > a {
		a = b
	}
	return a + 1
}
func (c *compiler) variable(name string, at wpm.Span, written bool) error {
	c.p.hasVariables = true
	c.variables[name] = true
	if uint32(len(c.variables)) > c.limits.Variables {
		return c.err("VariableLimit", at, "distinct variable budget")
	}
	if written {
		c.assigned[name] = true
		for _, b := range c.loops {
			if (b.kind == 0xfc12 || b.kind == 0xfc13) && c.p.code[b.start].name == name {
				return c.err("UnsupportedLoopVariableMutation", at, "body mutation/reuse of loop control variable is unqualified")
			}
			if b.kind == 0xfc13 {
				b.written[name] = true
			}
		}
	}
	return nil
}
func (c *compiler) top(at wpm.Span) error {
	if len(c.blocks) != 0 {
		return c.err("UnsupportedContext", at, "jump/label/handler/nested-file/return context is unqualified inside a structure")
	}
	return nil
}
func (c *compiler) push(kind uint16, index int, refs map[string]bool) error {
	b := &block{kind: kind, start: index, other: -1, references: refs, written: map[string]bool{}}
	c.blocks = append(c.blocks, b)
	if kind != 0xfc15 {
		c.loops = append(c.loops, b)
		depth := uint32(len(c.loops))
		if depth > c.limits.LoopDepth {
			return c.err("LoopLimit", c.p.code[index].at, "loop nesting budget")
		}
		if depth > c.p.maxLoop {
			c.p.maxLoop = depth
		}
	}
	return nil
}
func (c *compiler) statement() error {
	start := c.pos
	w := c.words[c.pos]
	c.pos++
	i := instruction{op: w.Value, at: w.Span, jump: -1, loop: -1}
	if w.Kind == wpm.Literal {
		for c.pos < len(c.words)-1 && c.words[c.pos].Kind == wpm.Literal {
			c.pos++
		}
		for _, literal := range c.words[start:c.pos] {
			if literal.Value == '~' {
				return c.err("UnexpectedDelimiter", literal.Span, "unowned tilde/literal escape context is unqualified")
			}
		}
		i.op = opLiteral
		i.words = c.words[start:c.pos]
		i.at = c.span(start)
		c.p.required.ASCII = true
		c.p.code = append(c.p.code, i)
		return nil
	}
	if w.Value == 0x8021 {
		if err := c.top(w.Span); err != nil {
			return err
		}
		i.op = opKey
		i.words = c.words[start:c.pos]
		if !hasKey(c.p.required, w.Value) {
			c.p.required.Keys = append(c.p.required.Keys, w.Value)
		}
		c.p.code = append(c.p.code, i)
		return nil
	}
	index := len(c.p.code)
	switch w.Value {
	case 0xfc0c:
		i.words = c.words[start:c.pos]
		c.p.required.DisplayControl = true
	case 0xfc01:
		name, _, err := c.name()
		if err != nil {
			return err
		}
		i.name = name
		if err = c.variable(name, w.Span, true); err != nil {
			return err
		}
		x, err := c.operand(false)
		if err != nil {
			return err
		}
		i.args = []*expression{x}
	case 0xfc34:
		name, _, err := c.name()
		if err != nil {
			return err
		}
		i.name = name
		if err = c.variable(name, w.Span, false); err != nil {
			return err
		}
		c.p.required.ASCII = true
	case 0xfc15, 0xfc2b:
		x, err := c.operand(false)
		if err != nil {
			return err
		}
		i.args = []*expression{x}
	case 0xfc12:
		name, _, err := c.name()
		if err != nil {
			return err
		}
		i.name = name
		if err = c.variable(name, w.Span, true); err != nil {
			return err
		}
		for n := 0; n < 3; n++ {
			x, err := c.operand(false)
			if err != nil {
				return err
			}
			refs := map[string]bool{}
			x.references(refs)
			if len(refs) != 0 {
				return c.err("UnsupportedForBounds", w.Span, "variable-dependent FOR bound timing is unqualified")
			}
			i.args = append(i.args, x)
		}
		begin, _ := i.args[0].eval(nil)
		end, _ := i.args[1].eval(nil)
		step, _ := i.args[2].eval(nil)
		if (step.number != 1 && step.number != -1) || (step.number > 0 && begin.number > end.number) || (step.number < 0 && begin.number < end.number) {
			return c.err("UnsupportedLoopRange", w.Span, "only qualified nonempty unit-step FOR ranges admitted")
		}
	case 0xfc13:
		name, _, err := c.name()
		if err != nil {
			return err
		}
		i.name = name
		if err = c.variable(name, w.Span, true); err != nil {
			return err
		}
		for c.pos < len(c.words) && c.words[c.pos].Value != '~' {
			x, err := c.operand(true)
			if err != nil {
				return err
			}
			i.args = append(i.args, x)
		}
		if len(i.args) == 0 || c.pos == len(c.words) {
			return c.err("MalformedOperand", w.Span, "nonempty list and final empty delimiter required")
		}
		c.pos++
	case 0xfc14, 0xfc16:
		if err := c.top(w.Span); err != nil {
			return err
		}
		name, _, err := c.name()
		if err != nil {
			return err
		}
		i.name = name
		if w.Value == 0xfc16 {
			if _, exists := c.labels[name]; exists {
				return c.err("DuplicateLabel", w.Span, name)
			}
			c.labels[name] = index
		}
	case 0xfc1c, 0xfc1d:
		if err := c.top(w.Span); err != nil {
			return err
		}
		if c.pos >= len(c.words) || c.words[c.pos].Value != 0xfc14 {
			return c.err("UnsupportedHandler", w.Span, "only original GO action qualified")
		}
		c.pos++
		name, _, err := c.name()
		if err != nil {
			return err
		}
		i.name = name
		if c.pos >= len(c.words) || c.words[c.pos].Value != '~' {
			return c.err("MalformedOperand", w.Span, "missing outer handler delimiter")
		}
		c.pos++
	case 0xfc18:
		if err := c.top(w.Span); err != nil {
			return err
		}
		_, name, err := c.name()
		if err != nil {
			return err
		}
		i.words = name
	case 0xfc22:
		if err := c.top(w.Span); err != nil {
			return err
		}
		c.p.needsChild = true
	case 0xfc19, 0xfc03:
		if len(c.loops) == 0 {
			if w.Value == 0xfc19 || len(c.blocks) != 0 {
				return c.err("UnsupportedLoopControl", w.Span, "only tested FOR and file-level BREAK contexts qualified")
			}
		} else {
			loop := c.loops[len(c.loops)-1]
			if loop.kind != 0xfc12 {
				return c.err("UnsupportedLoopControl", w.Span, "WHILE/FOR EACH NEXT/BREAK are unqualified")
			}
			i.loop = loop.start
		}
	case 0xfc0e:
		if len(c.blocks) == 0 {
			return c.err("UnmatchedStructure", w.Span, "ELSE without IF")
		}
		b := c.blocks[len(c.blocks)-1]
		if b.kind != 0xfc15 || b.other != -1 {
			return c.err("UnmatchedStructure", w.Span, "ELSE mismatches/duplicates IF")
		}
		b.other = index
		c.p.code[b.start].jump = index + 1
	case 0xfc10, 0xfc0f, 0xfc11:
		if len(c.blocks) == 0 {
			return c.err("UnmatchedStructure", w.Span, "END without opener")
		}
		b := c.blocks[len(c.blocks)-1]
		match := w.Value == 0xfc10 && b.kind == 0xfc15 || w.Value == 0xfc11 && b.kind == 0xfc2b || w.Value == 0xfc0f && (b.kind == 0xfc12 || b.kind == 0xfc13)
		if !match {
			return c.err("UnmatchedStructure", w.Span, "END mismatches opener")
		}
		i.jump = b.start
		c.p.code[b.start].loop = index
		if b.kind == 0xfc15 {
			if b.other == -1 {
				c.p.code[b.start].jump = index + 1
			} else {
				c.p.code[b.other].jump = index + 1
			}
		} else {
			c.p.code[b.start].jump = index + 1
			c.loops = c.loops[:len(c.loops)-1]
			if b.kind == 0xfc13 {
				for name := range b.references {
					if b.written[name] || name == c.p.code[b.start].name {
						return c.err("UnsupportedEvaluationTiming", w.Span, "FOR EACH referenced variable changes during iteration")
					}
				}
			}
		}
		c.blocks = c.blocks[:len(c.blocks)-1]
	default:
		return c.err("UnsupportedInstruction", w.Span, "instruction/context not qualified")
	}
	i.at = c.span(start)
	c.p.code = append(c.p.code, i)
	if w.Value == 0xfc15 || w.Value == 0xfc2b || w.Value == 0xfc12 || w.Value == 0xfc13 {
		refs := map[string]bool{}
		if w.Value == 0xfc13 {
			for _, arg := range i.args {
				arg.references(refs)
			}
		}
		return c.push(w.Value, index, refs)
	}
	return nil
}

// All registered handler entries are considered reachable regardless of whether
// the current fixture raises an error. Dynamic lookup/search/redefinition from
// an active handler is not qualified by the original corpus. This pass also
// supplies the static boundary for any later, separately qualified QUIT opcode.
func (c *compiler) handlerReachability() error {
	seen := make([]bool, len(c.p.code))
	pending := []int{}
	for _, i := range c.p.code {
		if i.op == 0xfc1c || i.op == 0xfc1d {
			pending = append(pending, i.jump)
		}
	}
	for len(pending) > 0 {
		pc := pending[len(pending)-1]
		pending = pending[:len(pending)-1]
		if pc == len(c.p.code) || seen[pc] {
			continue
		}
		seen[pc] = true
		i := c.p.code[pc]
		if i.op != opLiteral && i.op != 0xfc16 && i.op != 0xfc22 {
			return c.err("UnsupportedHandlerContext", i.at, "only observed literal/label/child-return handler body is qualified")
		}
		// The admitted handler region has no conditional/jump edges: such an
		// instruction is itself refused above, including a backward GO to QUIT.
		if i.op != 0xfc22 {
			pending = append(pending, pc+1)
		}
	}
	return nil
}
