package editor

import (
	"github.com/lynncoleart/wordling/internal/layout"
)

// Daily is a narrow WP82 surface. It is intentionally scoped to keep the
// mission review small; production editor integration remains separate.
type Daily struct {
	Layout layout.Layout
}

// New returns a bounded Daily view with zero layout tokens. It is safe to copy.
func NewDaily() (Daily, error) {
	return Daily{Layout: layout.Layout{}}, nil
}
