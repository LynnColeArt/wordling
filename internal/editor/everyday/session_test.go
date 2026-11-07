package editor

import (
	"testing"
)

func TestDailyEmptyLayout(t *testing.T) {
	d, err := NewDaily()
	if err != nil {
		t.Fatal(err)
	}
	if len(d.Layout.Lines) != 0 {
		t.Fatalf("unexpected layout lines: %d", len(d.Layout.Lines))
	}
}
