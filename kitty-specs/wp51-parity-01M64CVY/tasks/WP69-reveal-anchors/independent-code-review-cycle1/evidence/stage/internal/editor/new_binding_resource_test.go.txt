package editor_test

import (
	"github.com/lynncoleart/wordling/internal/editor"
	"testing"
)

func BenchmarkNewStartupState(b *testing.B) {
	b.ReportAllocs()
	for n := 0; n < b.N; n++ {
		s, e := editor.New(editor.Config{})
		if e != nil || s.Snapshot().NewPhase != editor.NewUnpublished {
			b.Fatal(e)
		}
	}
}
