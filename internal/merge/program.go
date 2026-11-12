package merge

import (
	"bytes"
	"fmt"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

// Primary holds compiled commands and the immutable native source they came from.
type Primary struct {
	view           *native.View
	body           body.Plan
	program        []operation
	highestOrdinal int
}

type operation struct {
	kind    native.CommandKind
	value   []byte
	jump    int
	ordinal int
}

const (
	maxPrimaryTokens    = body.MaxPrimaryTokens
	maxSecondaryRecords = 32
	maxSecondaryFields  = 107 // One automatic page break and at most 53 rows on the next page.
	maxNesting          = 16
	maxSources          = 64
	maxSteps            = 1 << 20
)

func parseView(raw []byte, role native.Role) (*native.Image, *native.View, error) {
	image, err := native.Parse(raw, native.DefaultLimits())
	if err != nil {
		return nil, nil, err
	}
	view, err := image.View(role)
	return image, view, err
}

func CompilePrimary(raw []byte) (Primary, error) {
	image, view, err := parseView(raw, native.Primary)
	if err != nil {
		return Primary{}, err
	}
	var plan body.Plan
	if program, err := view.Admit(); err == nil {
		plan, _ = body.Compile(program, image.Source(), body.DefaultLimits())
	} else {
		plan, _ = body.CompileHardPagePrimary(view, image.Source(), body.DefaultLimits())
	}
	compiled, err := compileProgram(view)
	if err != nil {
		return Primary{}, err
	}
	var producesOutput bool
	highestOrdinal := 0
	for _, op := range compiled {
		highestOrdinal = max(highestOrdinal, op.ordinal)
		producesOutput = producesOutput || op.kind == 0 || op.kind == native.FieldCommand || op.kind == native.NestPrimary
	}
	if !producesOutput {
		return Primary{}, invalidProgram("primary role")
	}
	return Primary{view: view, body: plan, program: compiled, highestOrdinal: highestOrdinal}, nil
}

func invalidProgram(why string) error {
	return fmt.Errorf("merge: unsupported native program: %s", why)
}

func commandFrame(view *native.View, c native.Command) bool {
	raw, ok := view.Bytes(c.Function)
	kind := byte(c.Kind)
	return ok && !c.HasRawCount && bytes.Equal(raw, []byte{0xde, kind, 4, 0, 4, 0, kind, 0xde})
}

func consumeOperand(view *native.View, info native.Inspection, at int, c native.Command, kind native.OperandKind) ([]byte, int, error) {
	raw, ok := view.Bytes(c.Operand.Data)
	term, termOK := view.Bytes(c.Operand.Terminator)
	if c.Operand.Kind != kind || !ok || !termOK || len(raw) == 0 || len(term) != 1 || term[0] != '~' ||
		at+len(raw)+1 >= len(info.Tokens) {
		return nil, at, invalidProgram("operand")
	}
	for i, b := range raw {
		t := info.Tokens[at+1+i]
		if t.Kind != native.Character || t.Code != b {
			return nil, at, invalidProgram("operand coverage")
		}
	}
	end := at + len(raw) + 1
	if info.Tokens[end].Raw != c.Operand.Terminator {
		return nil, at, invalidProgram("operand terminator")
	}
	return raw, end, nil
}

func compileProgram(view *native.View) ([]operation, error) {
	info, ok := view.Inspect()
	if !ok || info.Role != native.Primary || info.FindingsCapped || len(info.Tokens) == 0 || len(info.Tokens) > maxPrimaryTokens {
		return nil, invalidProgram("primary scope")
	}
	unresolved := make(map[native.Span]string, len(info.Findings))
	for _, finding := range info.Findings {
		switch finding.Code {
		case "NestedResolutionRequired", "FormatterUnresolved", "UnobservedOperand", "LiteralTildeUnsupported":
			unresolved[finding.At] = finding.Code
		default:
			return nil, invalidProgram(finding.Code)
		}
	}
	program := make([]operation, 0, len(info.Tokens))
	type branch struct{ start, otherwise int }
	var branches []branch
	command := 0
	for i := 0; i < len(info.Tokens); i++ {
		t := info.Tokens[i]
		switch {
		case t.Kind == native.Function && t.Code == 0xd4:
			cache, _ := view.Bytes(t.Raw)
			if i+2 != len(info.Tokens) || info.Tokens[i+1].Code != 0x0c ||
				unresolved[t.Raw] != "FormatterUnresolved" || !document.MatchMergePrimaryPageCache(cache) {
				return nil, invalidProgram("page cache")
			}
			delete(unresolved, t.Raw)
		case t.Kind == native.Control && t.Code == 0x0a ||
			t.Kind == native.Character && t.Code >= 0x20 && t.Code <= 0x7e:
			if t.Code == '~' {
				if unresolved[t.Raw] != "LiteralTildeUnsupported" {
					return nil, invalidProgram("unowned tilde")
				}
				delete(unresolved, t.Raw)
			}
			program = append(program, operation{value: []byte{t.Code}})
		case t.Kind == native.Control && t.Code == 0x0c:
			if i == 0 || info.Tokens[i-1].Code != 0xd4 {
				return nil, invalidProgram("unowned hard page")
			}
			program = append(program, operation{value: []byte{t.Code}})
		case t.Kind == native.Function && t.Code == 0xde:
			if command >= len(info.Commands) {
				return nil, invalidProgram("missing command owner")
			}
			c := info.Commands[command]
			command++
			if c.Function != t.Raw || !commandFrame(view, c) {
				return nil, invalidProgram("command frame")
			}
			op := operation{kind: c.Kind}
			switch c.Kind {
			case native.FieldCommand, native.IfBlank:
				_, end, err := consumeOperand(view, info, i, c, native.FieldNumber)
				if err != nil {
					return nil, err
				}
				if unresolved[c.Operand.Data] == "UnobservedOperand" {
					delete(unresolved, c.Operand.Data)
				}
				op.ordinal = max(1, int(c.Operand.Number))
				i = end
				if c.Kind == native.IfBlank {
					branches = append(branches, branch{start: len(program), otherwise: -1})
				}
			case native.Else:
				if len(branches) == 0 || branches[len(branches)-1].otherwise >= 0 {
					return nil, invalidProgram("ELSE without IF")
				}
				branch := &branches[len(branches)-1]
				branch.otherwise = len(program)
				program[branch.start].jump = len(program) + 1
			case native.EndIf:
				if len(branches) == 0 {
					return nil, invalidProgram("END IF without IF")
				}
				branch := branches[len(branches)-1]
				branches = branches[:len(branches)-1]
				index := branch.start
				if branch.otherwise >= 0 {
					index = branch.otherwise
				}
				program[index].jump = len(program) + 1
			case native.NestPrimary:
				name, end, err := consumeOperand(view, info, i, c, native.NativeDOSName)
				if err != nil || unresolved[c.Operand.Data] != "NestedResolutionRequired" {
					return nil, invalidProgram("nested primary name")
				}
				delete(unresolved, c.Operand.Data)
				op.value, i = name, end
			case native.PageOn, native.PageOff:
			case native.Break:
				if len(branches) != 0 {
					return nil, invalidProgram("BREAK in conditional")
				}
			default:
				return nil, invalidProgram("command outside primary role")
			}
			program = append(program, op)
		default:
			return nil, invalidProgram("unowned primary token")
		}
	}
	if command != len(info.Commands) || len(branches) != 0 || len(unresolved) != 0 {
		return nil, invalidProgram("incomplete primary")
	}
	return program, nil
}
