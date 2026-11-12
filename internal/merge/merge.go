// Package merge evaluates source-bound native merge programs and returns
// a logical fragment for insertion and reflow in the receiving document.
package merge

import (
	"bytes"
	"errors"
	"fmt"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/merge/explicit"
	"github.com/lynncoleart/wordling/internal/merge/native"
)

// Source identifies an authenticated native read in the caller's workspace.
type Source struct {
	ID    string
	Bytes []byte
}

// ResolveSource must return a pinned workspace read, not a mutable path.
// parentID is the ID of the source that owns the nested operand.
type ResolveSource func(parentID, name string) (Source, error)

// MissingSource identifies an absent native filename after a successful
// workspace directory resolution and listing.
type MissingSource struct{ Name string }

func (e *MissingSource) Error() string { return fmt.Sprintf("merge: nested file not found %q", e.Name) }

func (p Primary) Valid() bool { return p.view != nil }

func Evaluate(primary Primary, raw []byte) (*document.Document, error) {
	return EvaluateWithSources(primary, "", Source{Bytes: raw}, nil)
}

func EvaluateWithSources(primary Primary, primaryID string, secondary Source, resolve ResolveSource) (*document.Document, error) {
	if !primary.Valid() {
		return nil, invalidProgram("missing primary")
	}
	image, view, err := parseView(secondary.Bytes, native.Secondary)
	if err != nil {
		return nil, err
	}
	run := execution{
		page: true, resolve: resolve, primary: primary, primaryID: primaryID,
		pinned:          make(map[nestedReference]Source),
		primaries:       make(map[string]Primary),
		secondaries:     make(map[string][]secondaryRecord),
		activePrimary:   make(map[string]bool),
		activeSecondary: make(map[string]bool),
	}
	if data, err := explicit.Admit(view, image.Source()); err == nil && primary.body.Valid() && hasExplicitFields(data, primary.highestOrdinal) {
		for record := 1; record <= data.RecordCount(); record++ {
			result, err := primary.body.Evaluate(data, image.Source(), record)
			if err != nil {
				return nil, err
			}
			next, err := result.Bytes()
			if err != nil {
				return nil, err
			}
			if err := run.startRecord(); err != nil {
				return nil, err
			}
			if err := run.emit(next); err != nil {
				return nil, err
			}
		}
	} else {
		records, err := compileSecondary(view)
		if err != nil {
			return nil, err
		}
		if err := run.walkSecondary(secondary.ID, records, 0); err != nil {
			var missing *MissingSource
			if !errors.As(err, &missing) {
				return nil, err
			}
			// DOS keeps the prefix it emitted before a missing nested
			// file. It stops the entire merge at that point.
			partial, fragmentErr := document.NewMergeFragment(run.output)
			if fragmentErr != nil {
				return nil, fragmentErr
			}
			return partial, err
		}
	}
	return document.NewMergeFragment(run.output)
}

func hasExplicitFields(data explicit.Data, ordinal int) bool {
	for record := 1; record <= data.RecordCount(); record++ {
		if _, err := data.Field(record, ordinal); err != nil {
			return false
		}
	}
	return true
}

type nestedReference struct{ parent, name string }

type recordInput struct {
	fields  [][]byte
	missing error
}

func (r recordInput) field(ordinal int) ([]byte, error) {
	if r.missing != nil {
		return nil, r.missing
	}
	if ordinal > len(r.fields) {
		return nil, nil
	}
	return r.fields[ordinal-1], nil
}

type execution struct {
	page, started                  bool
	steps                          int
	output                         []byte
	resolve                        ResolveSource
	primary                        Primary
	primaryID                      string
	pinned                         map[nestedReference]Source
	primaries                      map[string]Primary
	secondaries                    map[string][]secondaryRecord
	activePrimary, activeSecondary map[string]bool
}

func (r *execution) load(parent, name string) (Source, error) {
	ref := nestedReference{parent, name}
	if source, ok := r.pinned[ref]; ok {
		return source, nil
	}
	if r.resolve == nil || len(r.pinned) >= maxSources {
		return Source{}, fmt.Errorf("merge: unavailable nested source %q", name)
	}
	source, err := r.resolve(parent, name)
	if err != nil {
		var missing *MissingSource
		if errors.As(err, &missing) {
			return Source{}, err
		}
		return Source{}, fmt.Errorf("merge: read nested source %q: %w", name, err)
	}
	if source.ID == "" || len(source.Bytes) == 0 || len(source.Bytes) > native.MaxBytes {
		return Source{}, invalidProgram("nested source identity or size")
	}
	source.Bytes = bytes.Clone(source.Bytes)
	r.pinned[ref] = source
	return source, nil
}

func (r *execution) emit(raw []byte) error {
	if len(raw) > document.MaxMutationTokens-len(r.output) {
		return fmt.Errorf("merge: output exceeds the editable native body limit")
	}
	r.output = append(r.output, raw...)
	return nil
}

func (r *execution) startRecord() error {
	page := r.started && r.page
	r.started = true
	if page {
		return r.emit([]byte{0x0c})
	}
	return nil
}

func (r *execution) tick() error {
	if r.steps >= maxSteps {
		return fmt.Errorf("merge: execution exceeds the native work limit")
	}
	r.steps++
	return nil
}

func (r *execution) walkSecondary(id string, records []secondaryRecord, depth int) error {
	if depth >= maxNesting || r.activeSecondary[id] {
		return fmt.Errorf("merge: recursive or overdeep secondary %q", id)
	}
	r.activeSecondary[id] = true
	defer delete(r.activeSecondary, id)
	for _, record := range records {
		if err := r.tick(); err != nil {
			return err
		}
		if record.nested != "" {
			source, err := r.load(id, record.nested)
			if err != nil {
				var missing *MissingSource
				if errors.As(err, &missing) {
					if boundaryErr := r.startRecord(); boundaryErr != nil {
						return boundaryErr
					}
					// DOS starts the next primary copy before the first
					// field access discovers the missing data file.
					if partialErr := r.runPrimary(r.primary, r.primaryID, recordInput{missing: err}, 0); partialErr != nil {
						return partialErr
					}
				}
				return err
			}
			if r.activeSecondary[source.ID] {
				return fmt.Errorf("merge: recursive secondary %q", source.ID)
			}
			child, exists := r.secondaries[source.ID]
			if !exists {
				_, view, err := parseView(source.Bytes, native.Secondary)
				if err != nil {
					return err
				}
				child, err = compileSecondary(view)
				if err != nil {
					return err
				}
				r.secondaries[source.ID] = child
			}
			if err := r.walkSecondary(source.ID, child, depth+1); err != nil {
				return err
			}
			continue
		}
		// The existing state decides the preceding separator. Commands
		// inside this record change only subsequent boundaries.
		if err := r.startRecord(); err != nil {
			return err
		}
		if record.page != 0 {
			r.page = record.page == native.PageOn
		}
		if err := r.runPrimary(r.primary, r.primaryID, recordInput{fields: record.fields}, 0); err != nil {
			return err
		}
	}
	return nil
}

func (r *execution) runPrimary(primary Primary, id string, record recordInput, depth int) error {
	if depth >= maxNesting || r.activePrimary[id] {
		return fmt.Errorf("merge: recursive or overdeep primary %q", id)
	}
	r.activePrimary[id] = true
	defer delete(r.activePrimary, id)
	for pc := 0; pc < len(primary.program); pc++ {
		if err := r.tick(); err != nil {
			return err
		}
		op := primary.program[pc]
		switch op.kind {
		case 0:
			if err := r.emit(op.value); err != nil {
				return err
			}
		case native.FieldCommand:
			value, err := record.field(op.ordinal)
			if err != nil {
				return err
			}
			if err := r.emit(value); err != nil {
				return err
			}
		case native.IfBlank:
			value, err := record.field(op.ordinal)
			if err != nil {
				return err
			}
			if len(bytes.Trim(value, " ")) != 0 {
				pc = op.jump - 1
			}
		case native.Else:
			pc = op.jump - 1
		case native.EndIf:
		case native.PageOn, native.PageOff:
			r.page = op.kind == native.PageOn
		case native.Break:
			return nil
		case native.NestPrimary:
			source, err := r.load(id, string(op.value))
			if err != nil {
				return err
			}
			if r.activePrimary[source.ID] {
				return fmt.Errorf("merge: recursive primary %q", source.ID)
			}
			child, exists := r.primaries[source.ID]
			if !exists {
				child, err = CompilePrimary(source.Bytes)
				if err != nil {
					return err
				}
				r.primaries[source.ID] = child
			}
			if err := r.runPrimary(child, source.ID, record, depth+1); err != nil {
				return err
			}
		}
	}
	return nil
}
