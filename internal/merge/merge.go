// Package merge evaluates the observed native primary forms with explicit
// secondary records. It produces a logical fragment for document insertion.
package merge

import (
	"fmt"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge/body"
	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

func CompilePrimary(raw []byte) (body.Plan, error) {
	image, err := native.Parse(raw, native.DefaultLimits())
	if err != nil {
		return body.Plan{}, err
	}
	view, err := image.View(native.Primary)
	if err != nil {
		return body.Plan{}, err
	}
	program, err := view.Admit()
	if err != nil {
		return body.CompileHardPagePrimary(view, image.Source(), body.DefaultLimits())
	}
	return body.Compile(program, image.Source(), body.DefaultLimits())
}

func Evaluate(primary body.Plan, raw []byte) (*document.Document, error) {
	image, err := native.Parse(raw, native.DefaultLimits())
	if err != nil {
		return nil, err
	}
	view, err := image.View(native.Secondary)
	if err != nil {
		return nil, err
	}
	data, err := explicit.Admit(view, image.Source())
	if err != nil {
		return nil, err
	}
	var output []byte
	for record := 1; record <= data.RecordCount(); record++ {
		result, err := primary.Evaluate(data, image.Source(), record)
		if err != nil {
			return nil, err
		}
		next, err := result.Bytes()
		if err != nil {
			return nil, err
		}
		separator := 0
		if record > 1 {
			separator = 1
		}
		if len(next)+separator > document.MaxMutationTokens-len(output) {
			return nil, fmt.Errorf("merge: output exceeds the editable native body limit")
		}
		// Original default PAGE ON inserts a hard page between records,
		// even when the primary has its own trailing hard page.
		if separator != 0 {
			output = append(output, 0x0c)
		}
		output = append(output, next...)
	}
	return document.NewMergeFragment(output)
}
