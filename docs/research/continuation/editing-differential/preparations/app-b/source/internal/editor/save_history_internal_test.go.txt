package editor

import (
	"errors"
	"github.com/lynncoleart/wordling/internal/document"
	"testing"
)

// Private invariant fault: a real InvalidHistory must never receive the bounded
// Save waiver. Public callers cannot replace the session's history handle.
func TestSaveHistoryDoesNotWaiveInvalidHandle(t *testing.T) {
	s := Session{historyValid: true}
	next, err := s.saveHistoryInterleaving()
	var failure *document.Failure
	if !errors.As(err, &failure) || failure.Category != document.InvalidHistory || !next.historyValid {
		t.Fatalf("invalid handle bypassed: %v", err)
	}
}
