package editor

import (
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/worksheet"
)

func (s Session) ImportSpreadsheet(path, area string, linked, refresh bool) (Session, error) {
	if s.mode != Editing || s.workspaceBase == nil || s.native == nil || s.selection || s.mergeSource {
		return s, refuse("Spreadsheet requires an editable workspace document")
	}
	var r worksheet.Range
	var err error
	if refresh {
		table, ok := s.native.SpreadsheetTable()
		if !ok || table.Link == nil {
			return s, refuse("This document has no worksheet link")
		}
		r, path, linked = table.Link.Range, table.Link.Path, true
	} else {
		r, err = worksheet.ParseRange(area)
		if err != nil {
			return s, err
		}
	}
	if !strings.HasSuffix(strings.ToUpper(path), ".WK1") {
		return s, refuse("Select a Lotus .WK1 worksheet")
	}
	raw, absolute, modified, err := s.workspaceBase.ReadDOSFile(path)
	if err != nil {
		return s, err
	}
	cells, err := worksheet.ReadWK1(raw, r)
	if err != nil {
		return s, err
	}
	var link *document.SpreadsheetLink
	if linked {
		link = &document.SpreadsheetLink{Path: absolute, Range: r, Modified: modified.UTC()}
		if refresh {
			link.Path = path
		}
	}
	edit, err := s.native.PutSpreadsheet(s.cursor, cells, link, refresh)
	if err != nil || !edit.Changed {
		return s, err
	}
	s.native, s.cursor = edit.Document, edit.Cursor
	s.historyValid, s.historyUsed = false, false
	s.revision++
	s.lastSave, s.notice = NotSaved, ""
	return s, nil
}
