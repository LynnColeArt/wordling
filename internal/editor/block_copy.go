package editor

import (
	"bytes"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/layout"
	"github.com/lynncoleart/wordling/internal/storage"
)

func (s Session) beginBlockCopy() (Session, *Intent, error) {
	copy, err := s.native.CopyEverydayBlock(s.anchor, s.cursor)
	if err != nil {
		return s, nil, err
	}
	s.blockCopy = copy
	s.selection, s.blockMoved, s.anchor = false, false, document.Cursor{}
	s.mode, s.notice = CopyTargetMode, ""
	return s, nil, nil
}

func (s Session) beginBlockAppend() (Session, *Intent, error) {
	next, intent, err := s.beginBlockCopy()
	if err != nil {
		return s, intent, err
	}
	return next.filename(AppendBlockName), nil, nil
}

func (s Session) blockCopyInput(event Event) (Session, *Intent, error) {
	if event.Command == F1 || event.Command == Escape {
		s.blockCopy, s.mode, s.homes = nil, Editing, 0
		return s, nil, nil
	}
	switch s.mode {
	case MoveMenuMode:
		if event.Command == Text && event.Text == "1" {
			s.mode = MoveBlockMode
		}
	case MoveBlockMode:
		if event.Command == Text && event.Text == "2" {
			return s.beginBlockCopy()
		}
		if event.Command == Text && event.Text == "4" {
			return s.beginBlockAppend()
		}
	case CopyTargetMode:
		if event.Command == Enter {
			edit, err := s.native.InsertBlockCopy(s.cursor, s.blockCopy)
			if err != nil {
				return s, nil, err
			}
			history := s.history
			if s.historyValid {
				history, err = history.AfterRetrieval(edit)
				if err != nil {
					return s, nil, err
				}
			}
			next, err := s.finishEverydayEdit(edit, history)
			if err != nil {
				return s, nil, err
			}
			next.blockCopy, next.mode, next.homes = nil, Editing, 0
			return next, nil, nil
		}
		switch event.Command {
		case Home, End, Left, Right, Up, Down, WordLeft, WordRight, PageUp, PageDown, Reveal:
			s.mode = Editing
			next, _, err := s.reduce(event)
			next.mode = CopyTargetMode
			return next, nil, err
		}
	}
	return s, nil, nil
}

func appendWorkspaceBlock(dir *storage.WorkspaceDirectory, name string, intent Intent) Result {
	target, err := dir.Observe(name)
	if err != nil {
		return Result{Err: err}
	}
	id := storage.PublicationID{Operation: intent.Operation, Revision: intent.Revision}
	disk := dir.Directory()
	if !target.Exists() {
		prepared, err := disk.PrepareNewSave(target, intent.Candidate, storage.NoOverwrite, storage.OriginalBackupPreserve, id)
		if err != nil {
			return Result{Err: err}
		}
		saved, err := disk.PublishNewSave(prepared, id)
		return blockAppendResult(saved, err, target, id, intent.Candidate)
	}
	source := readWorkspaceName(dir, name)
	if source.Err != nil {
		return source
	}
	current, err := document.Parse(source.Document.Export())
	if err != nil {
		return Result{Err: err}
	}
	fastSave := false
	if compact, err := current.CompactFastSave(); err == nil {
		current, fastSave = compact, true
	}
	block, err := document.Parse(intent.Candidate)
	if err != nil {
		return Result{Err: err}
	}
	end, err := current.CursorAt(current.TokenCount())
	if err != nil {
		return Result{Err: err}
	}
	edit, err := current.InsertDocument(end, block)
	if err != nil {
		return Result{Err: err}
	}
	plan, err := layout.PlanReflow(edit.Document, EverydaySettings())
	if err != nil {
		return Result{Err: err}
	}
	edit, err = edit.Document.AdoptReflow(edit.Cursor, plan)
	if err != nil {
		return Result{Err: err}
	}
	var data []byte
	if fastSave {
		data, err = edit.Document.ExportFastSave()
	} else {
		data, err = edit.Document.Export()
	}
	if err != nil {
		return Result{Err: err}
	}
	prepared, err := disk.PrepareSave(source.Document, target, data, storage.AllowOverwrite, storage.OriginalBackupPreserve, id)
	if err != nil {
		return Result{Err: err}
	}
	saved, err := disk.PublishSave(prepared, id)
	return blockAppendResult(saved, err, target, id, data)
}

func blockAppendResult(saved storage.SaveResult, err error, target *storage.Destination, id storage.PublicationID, data []byte) Result {
	if err != nil {
		return Result{Err: err}
	}
	if saved.ID != id || saved.Document == nil || !bytes.Equal(saved.Document.Export(), data) ||
		saved.Outcome.Name != target.Name() || saved.Outcome.Identity != saved.Document.Identity() {
		return Result{Err: &storage.Failure{Kind: storage.PublicationUncertain, Stage: "workspace append receipt", Name: target.Name(), DestinationMayExist: true}}
	}
	return Result{Document: saved.Document, Outcome: saved.Outcome}
}
