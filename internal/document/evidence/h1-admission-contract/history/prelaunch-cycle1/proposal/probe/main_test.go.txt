package main

import (
	"go/ast"
	"go/parser"
	"go/token"
	"testing"
)

func TestReadOnlySelectorSurface(t *testing.T) {
	file, e := parser.ParseFile(token.NewFileSet(), "main.go", nil, 0)
	if e != nil {
		t.Fatal(e)
	}
	allowed := map[string]bool{}
	for _, name := range []string{"Stat", "Mode", "Equal", "IsRegular", "Size", "ReadFile", "Sum256", "EncodeToString", "Parse", "Export", "OriginalExport", "Inspect", "Bytes", "CheckMutation", "Error", "MarshalIndent", "Println"} {
		allowed[name] = true
	}
	ast.Inspect(file, func(node ast.Node) bool {
		if call, ok := node.(*ast.CallExpr); ok {
			if s, ok := call.Fun.(*ast.SelectorExpr); ok && !allowed[s.Sel.Name] {
				t.Errorf("unapproved probe call %s", s.Sel.Name)
			}
		}
		return true
	})
}
