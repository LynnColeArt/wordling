package merge

import (
	"bytes"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

type secondaryRecord struct {
	fields [][]byte
	page   native.CommandKind
	nested string
}

func compileSecondary(view *native.View) ([]secondaryRecord, error) {
	info, ok := view.Inspect()
	if !ok || info.Role != native.Secondary || info.FindingsCapped || len(info.Records) == 0 || len(info.Records) > maxSecondaryRecords {
		return nil, invalidProgram("secondary scope")
	}
	unresolved := make(map[native.Span]string, len(info.Findings))
	for _, finding := range info.Findings {
		switch finding.Code {
		case "RecordCountUnresolved", "FormatterUnresolved", "NestedResolutionRequired":
			unresolved[finding.At] = finding.Code
		default:
			return nil, invalidProgram(finding.Code)
		}
	}
	out := make([]secondaryRecord, 0, len(info.Records))
	token, command := 0, 0
	consume := func(span native.Span, kind native.TokenKind, code byte) bool {
		if token >= len(info.Tokens) {
			return false
		}
		t := info.Tokens[token]
		if t.Raw != span || t.Kind != kind || t.Code != code {
			return false
		}
		token++
		return true
	}
	for i, record := range info.Records {
		tail, tailOK := record.Tail.Bounds()
		if !tailOK || tail.Length != 0 || len(record.Fields) < 1 || len(record.Fields) > 2 ||
			int(record.StoredCount) != len(record.Fields)+1 || len(record.Interstitial) != 2 {
			return nil, invalidProgram("secondary record shape")
		}
		next := secondaryRecord{fields: make([][]byte, 0, len(record.Fields))}
		for j, field := range record.Fields {
			content, ok := field.Content.Bounds()
			if !ok {
				return nil, invalidProgram("field content")
			}
			start := content.Offset
			if token < len(info.Tokens) && info.Tokens[token].Kind == native.Function &&
				info.Tokens[token].Raw != field.EndField {
				if j != 0 || command >= len(info.Commands) {
					return nil, invalidProgram("secondary command placement")
				}
				c := info.Commands[command]
				if !commandFrame(view, c) || !consume(c.Function, native.Function, 0xde) {
					return nil, invalidProgram("secondary command owner")
				}
				command++
				switch c.Kind {
				case native.PageOn, native.PageOff:
					next.page = c.Kind
					bound, _ := c.Function.Bounds()
					start = bound.Offset + bound.Length
				case native.NestSecondary:
					if len(record.Fields) != 1 {
						return nil, invalidProgram("nested secondary record shape")
					}
					name, end, err := consumeOperand(view, info, token-1, c, native.NativeDOSName)
					if err != nil || unresolved[c.Operand.Data] != "NestedResolutionRequired" {
						return nil, invalidProgram("nested secondary name")
					}
					delete(unresolved, c.Operand.Data)
					next.nested = string(name)
					token = end + 1
					bound, _ := c.Operand.Terminator.Bounds()
					start = bound.Offset + bound.Length
				default:
					return nil, invalidProgram("command outside secondary role")
				}
			}
			var value []byte
			for pos := start; pos < content.Offset+content.Length; pos++ {
				if token >= len(info.Tokens) {
					return nil, invalidProgram("field token")
				}
				t := info.Tokens[token]
				bound, _ := t.Raw.Bounds()
				if bound.Offset != pos || bound.Length != 1 || t.Kind != native.Character || t.Code < 0x20 || t.Code > 0x7e {
					return nil, invalidProgram("field text")
				}
				value = append(value, t.Code)
				token++
			}
			if start < content.Offset || start > content.Offset+content.Length || command >= len(info.Commands) {
				return nil, invalidProgram("field coverage")
			}
			c := info.Commands[command]
			if c.Kind != native.EndField || c.Function != field.EndField || !commandFrame(view, c) ||
				!consume(field.EndField, native.Function, 0xde) || !consume(field.Separator, native.Control, 0x0a) {
				return nil, invalidProgram("field delimiter")
			}
			command++
			next.fields = append(next.fields, value)
		}
		if command >= len(info.Commands) {
			return nil, invalidProgram("missing record delimiter")
		}
		c := info.Commands[command]
		delimiter, _ := view.Bytes(record.EndRecord)
		if c.Kind != native.EndRecord || c.Function != record.EndRecord ||
			!bytes.Equal(delimiter, []byte{0xde, 0x34, 6, 0, byte(record.StoredCount), 0, 6, 0, 0x34, 0xde}) ||
			unresolved[c.Payload] != "RecordCountUnresolved" || !consume(record.EndRecord, native.Function, 0xde) {
			return nil, invalidProgram("record delimiter")
		}
		command++
		delete(unresolved, c.Payload)
		cache, _ := view.Bytes(record.Interstitial[0])
		if unresolved[record.Interstitial[0]] != "FormatterUnresolved" ||
			!document.MatchMergeRecordPageCache(cache, i+1, len(record.Fields)) ||
			!consume(record.Interstitial[0], native.Function, 0xd4) ||
			!consume(record.Interstitial[1], native.Control, 0x0c) {
			return nil, invalidProgram("record page cache")
		}
		delete(unresolved, record.Interstitial[0])
		out = append(out, next)
	}
	if command != len(info.Commands) || token != len(info.Tokens) || len(unresolved) != 0 {
		return nil, invalidProgram("incomplete secondary")
	}
	return out, nil
}
