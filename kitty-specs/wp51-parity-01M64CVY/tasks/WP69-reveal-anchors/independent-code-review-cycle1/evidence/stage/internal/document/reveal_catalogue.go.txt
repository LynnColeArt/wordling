package document

import "github.com/lynncoleart/wordling/internal/wp51"

// Catalogue limits are host inspection policies, not original application limits.
const (
	MaxCatalogueRawBytes  = 256 << 10
	MaxCatalogueTextBytes = 32 << 10
)

// CatalogueInspection contains independent display values for complete native
// owners. An Opaque element with empty Text is explicitly unsupported; an Opaque
// element with Text is still NOT admitted for movement, editing or Present.
// Revision authenticates the captured source, not any caller-modified result.
type CatalogueInspection struct {
	Revision                      Revision
	StartGap, EndGap, TotalTokens int
	TrueEOF                       bool
	Elements                      []Element
}

// InspectRevealCatalogue inspects one bounded window of an actual immutable
// revision. It accepts neither caller Tokens nor presentation/semantic authority.
// The exported wrapper is read once; concurrent caller mutation of that wrapper
// remains outside the contract. Serialized replacement cannot retarget a capture.
func InspectRevealCatalogue(d *Document, expected Revision, start, count int) (CatalogueInspection, error) {
	if d == nil {
		return CatalogueInspection{}, failure(InvalidDocument, -1, noSpan)
	}
	state := d.state
	if !state.valid() {
		return CatalogueInspection{}, failure(InvalidDocument, -1, noSpan)
	}
	if expected.state != state {
		return CatalogueInspection{}, failure(RevisionMismatch, -1, noSpan)
	}
	total := len(state.gaps) - 1
	if start < 0 || start > total || count < 0 || count > total-start {
		return CatalogueInspection{}, failure(InvalidPosition, start, noSpan)
	}
	if count > MaxWindowTokens {
		return CatalogueInspection{}, failure(WindowLimit, start, noSpan)
	}
	end := start + count
	window := wp51.Span{Offset: int(state.gaps[start]), Length: int(state.gaps[end] - state.gaps[start])}
	// Both limits precede Bytes/Token and result allocation. Every gap belongs to
	// the reader-validated complete-owner index; no payload is scanned or split.
	if window.Length > MaxCatalogueRawBytes {
		return CatalogueInspection{}, failure(WindowLimit, start, window)
	}
	raw, ok := state.image.Bytes(window)
	if !ok {
		return CatalogueInspection{}, failure(InvalidDocument, start, window)
	}
	result := CatalogueInspection{Revision: Revision{state}, StartGap: start, EndGap: end, TotalTokens: total, TrueEOF: end == total, Elements: make([]Element, count)}
	textBytes := 0
	for i := start; i < end; i++ {
		span := wp51.Span{Offset: int(state.gaps[i]), Length: int(state.gaps[i+1] - state.gaps[i])}
		local := span.Offset - window.Offset
		owner := raw[local : local+span.Length]
		kind := identify(owner)
		text := ""
		switch kind {
		case ASCII:
			text = string(owner)
		case BoldOn:
			text = "[BOLD]"
		case BoldOff:
			text = "[bold]"
		case Opaque:
			if len(owner) == 1 {
				switch owner[0] {
				case 0x0a:
					text = "[HRt]"
				case 0x0c:
					text = "[HPg]"
				}
			}
		}
		textBytes += len(text)
		// Currently at most six bytes per element (24576 total), but keep the
		// independent output ceiling explicit if the closed catalogue ever changes.
		if textBytes > MaxCatalogueTextBytes {
			return CatalogueInspection{}, failure(WindowLimit, i, span)
		}
		result.Elements[i-start] = Element{TokenIndex: i, Kind: kind, Span: span, Text: text}
	}
	return result, nil
}
