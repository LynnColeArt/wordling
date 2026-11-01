// Component-only producer: actual editor reducer + storage41; no TUI/original claim.
package main

import (
	"encoding/json"
	"fmt"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/storage"
	"os"
	"path/filepath"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func main() {
	if len(os.Args) != 2 {
		panic("new output directory required")
	}
	out := os.Args[1]
	must(os.Mkdir(out, 0700))
	var records []any
	for _, body := range []string{"", "ASCII"} {
		label := "empty"
		if body != "" {
			label = "ascii"
		}
		root := filepath.Join(out, label)
		must(os.Mkdir(root, 0700))
		d, e := storage.OpenDirectory(root)
		must(e)
		s, e := editor.New(editor.Config{Locations: []editor.Location{{Directory: d}}})
		must(e)
		birth := s.Document().Birth()
		drive := func(event editor.Event) {
			var i *editor.Intent
			var e error
			s, i, e = s.Reduce(event)
			must(e)
			for i != nil {
				var r editor.Result
				switch i.Kind {
				case editor.Observe:
					r = editor.Result{Operation: i.Operation, Revision: i.Revision, Kind: i.Kind}
					r.Destination, r.Err = i.Directory.Observe(i.Name)
				case editor.PublishNewBuffer:
					r = editor.ExecuteNewPublication(i)
				case editor.BindNewSource:
					r = editor.ExecuteFirstRead(i)
				default:
					panic(fmt.Sprint("unexpected ", i.Kind))
				}
				s, i, e = s.Reduce(editor.Event{Command: editor.Complete, Result: &r})
				must(e)
			}
		}
		if body != "" {
			drive(editor.Event{Command: editor.Text, Text: body})
		}
		before := s.Document().Revision()
		raw, e := s.Document().Export()
		must(e)
		must(os.WriteFile(filepath.Join(root, "before.WP5"), raw, 0600))
		drive(editor.Event{Command: editor.Save})
		drive(editor.Event{Command: editor.Text, Text: "FIRST.WP5"})
		drive(editor.Event{Command: editor.Enter})
		if s.Snapshot().NewPhase != editor.NewAnchored || s.Document().Birth() != birth || s.Document().Revision() != before || s.Snapshot().SavedRevision != before {
			panic("binding changed native")
		}
		_, originalErr := s.Document().OriginalExport()
		records = append(records, map[string]any{"body": body, "phase": s.Snapshot().NewPhase, "source_identity": s.Source().Identity(), "publication": s.Snapshot().FirstPublication.Result.Outcome, "birth_preserved": true, "native_revision_preserved": true, "original_export_error": originalErr.Error(), "scope": "actual pure editor + real storage41 component; no PTY or original observation"})
		must(d.Close())
	}
	raw, e := json.MarshalIndent(records, "", "  ")
	must(e)
	must(os.WriteFile(filepath.Join(out, "outcomes.json"), append(raw, '\n'), 0600))
}
