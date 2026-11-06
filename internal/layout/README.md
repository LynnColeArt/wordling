# Pure native layout engine

`internal/layout` projects already-decoded native tokens into physical lines
and pages. It intentionally owns only geometry, not rendering, and never
serializes a renderer's display text back into native bytes. The production
consumer may feed a `document.Document` through `FromDocument`, or a bounded
token slice through `Project` for testing.
