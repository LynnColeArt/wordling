package tui

import (
	"fmt"
	"regexp"
	"strings"
)

type findClause struct {
	operator rune
	pattern  *regexp.Regexp
}

type findPattern []findClause

func compileFindPattern(input string, filename bool) (findPattern, error) {
	input = strings.ToLower(strings.TrimSpace(input))
	if len(input) > 39 {
		return nil, fmt.Errorf("Find patterns can contain up to 39 characters")
	}
	var result findPattern
	var term strings.Builder
	quoted, quotedTerm := false, false
	operator := ' '
	addTerm := func() error {
		if term.Len() == 0 {
			return nil
		}
		if len(result) == 5 {
			return fmt.Errorf("Find patterns can contain up to five terms")
		}
		for _, word := range strings.Fields(term.String()) {
			if len(word) > 20 {
				return fmt.Errorf("Find terms can contain up to 20 characters per word")
			}
		}
		var expression strings.Builder
		if !filename {
			expression.WriteString(`(?:^|[^\pL\pN])`)
		}
		for _, c := range term.String() {
			switch c {
			case '*':
				expression.WriteString(`(?s:.*)`)
			case '?':
				expression.WriteString(`[^\s]`)
			default:
				expression.WriteString(regexp.QuoteMeta(string(c)))
			}
		}
		if !filename && !strings.Contains(term.String(), " ") && !(quotedTerm && strings.Contains(term.String(), "*")) {
			expression.WriteString(`(?:$|[^\pL\pN])`)
		}
		result = append(result, findClause{operator, regexp.MustCompile(expression.String())})
		term.Reset()
		quotedTerm = false
		operator = ' '
		return nil
	}
	for _, c := range input {
		switch {
		case c == '"':
			quotedTerm = true
			quoted = !quoted
		case !quoted && strings.ContainsRune(" ;,-", c):
			if err := addTerm(); err != nil {
				return nil, err
			}
			if c != ' ' || operator != ',' && operator != '-' {
				operator = c
			}
		default:
			term.WriteRune(c)
		}
	}
	if quoted {
		return nil, fmt.Errorf("Close the quoted Find phrase")
	}
	if err := addTerm(); err != nil {
		return nil, err
	}
	return result, nil
}

func (p findPattern) matches(fields ...[]byte) bool {
	matched := true
	for i, clause := range p {
		found := false
		for _, field := range fields {
			if clause.pattern.Match(field) {
				found = true
				break
			}
		}
		switch clause.operator {
		case '-':
			matched = matched && !found
		case ',':
			matched = (i > 0 && matched) || found
		default:
			matched = matched && found
		}
	}
	return len(p) > 0 && matched
}
