package tui

import (
	"strings"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
)

// A single copied display fact, not native authority or a payload cache. The
// opaque revision is the authentic owner key; equal bytes do not compare equal.
// Invalidating the slot releases its one previous revision. Persistent Model
// values still own their respective immutable observations.
type asciiQualification struct {
	revision       document.Revision
	total          int
	checked, whole bool
}

const maxASCIIViewportOwners = 16384

func (m Model) ordinaryViewEligible(s editor.Snapshot) bool {
	if m.runtime == nil || s.Mode != editor.Editing || s.Selection || s.Typeover || !s.HistoryCountKnown || s.Screen != 1 || s.MacroRepeat != 1 ||
		s.Pending != nil || s.Prompt != "" || s.Notice != "" || m.characterRepeat.active || m.repeatEntry || m.notice != "" || m.reconcile != "" ||
		len(m.unsettled) != 0 || m.firstPending != nil || m.macro != nil || m.macroTicket != nil || m.macroCPU || m.macroFrozen != nil ||
		m.macroDeferred != nil || m.macroStatus.Active || m.macroStatus.WorkerPending || m.macroStatus.DisplaySuppressed ||
		s.NewPhase == editor.PublishedUnbound || s.NewPhase == editor.PublicationUncertain || m.menuReason() == "" || m.menu.diagnostic != "" {
		return false
	}
	m.runtime.mu.Lock()
	defer m.runtime.mu.Unlock()
	return !m.runtime.stopping && m.runtime.macro == nil && m.uiAuthority != nil && m.uiAuthority == m.runtime.uiAuthority
}

// Only the returned authentic Update chain prepares the fact, after dispatch.
// View/State and stale Update returns never enter this path.
func (m *Model) prepareASCIIViewport() {
	s := m.session.Snapshot()
	if !m.ordinaryViewEligible(s) {
		m.ascii = asciiQualification{}
		return
	}
	d := m.session.Document()
	if d == nil || d.TokenCount() <= document.MaxWindowTokens {
		m.ascii = asciiQualification{}
		return
	}
	if m.ascii.checked && m.ascii.revision == s.NativeRevision {
		return
	}
	m.ascii = qualifyASCII(d, s.NativeRevision)
}
func qualifyASCII(d *document.Document, revision document.Revision) asciiQualification {
	total := d.TokenCount()
	fact := asciiQualification{revision: revision, total: total, checked: true}
	// Preflight total before requesting any catalogue allocation. This is only a
	// HOST view limit, never a native open/edit limit.
	if total <= document.MaxWindowTokens || total > maxASCIIViewportOwners {
		return fact
	}
	rawBytes, textBytes := 0, 0
	previousEnd := -1
	for start := 0; start < total; start += document.MaxWindowTokens {
		count := min(document.MaxWindowTokens, total-start)
		c, err := document.InspectRevealCatalogue(d, revision, start, count)
		if err != nil || c.Revision != revision || c.StartGap != start || c.EndGap != start+count || c.TotalTokens != total || c.TrueEOF != (start+count == total) || len(c.Elements) != count {
			return fact
		}
		for i, e := range c.Elements {
			if e.TokenIndex != start+i || e.Kind != document.ASCII || e.Span.Length != 1 || len(e.Text) != 1 || e.Text[0] < 32 || e.Text[0] > 126 || e.Span.Offset < 0 || (previousEnd >= 0 && e.Span.Offset != previousEnd) {
				return fact
			}
			rawBytes += e.Span.Length
			textBytes += len(e.Text)
			previousEnd = e.Span.Offset + e.Span.Length
			if rawBytes > 1<<20 || textBytes > 128<<10 {
				return fact
			}
		}
	}
	fact.whole = true
	return fact
}
func (m Model) asciiViewportFrame(s editor.Snapshot) (macroPane, bool) {
	f := m.ascii
	if !f.checked || !f.whole || f.revision != s.NativeRevision || !m.ordinaryViewEligible(s) {
		return macroPane{}, false
	}
	start := max(0, s.Gap-m.width/2)
	count := min(m.width, f.total-start)
	if start < 0 || start > s.Gap || s.Gap > f.total || count < 0 || count > document.MaxWindowTokens || (s.Gap < f.total && s.Gap >= start+count) {
		return macroPane{}, false
	}
	p, err := m.session.Present(start, count)
	if err != nil {
		return macroPane{err: err}, true
	}
	var normal strings.Builder
	runs := make([]revealRun, 0, len(p.Elements)+1)
	for _, e := range p.Elements {
		normal.WriteString(e.Text)
		role := revealBase
		if e.TokenIndex == p.CursorGap && e.Span.Length > 0 {
			role = revealActive
		}
		runs = append(runs, revealRun{text: e.Text, role: role})
	}
	if p.CursorGap == f.total {
		runs = append(runs, revealRun{text: " ", role: revealActive})
	}
	// Already an absolute owner window: render from local zero, never scroll again.
	return macroPane{normal: normal.String() + "\x1b[0m", reveal: renderReveal(runs, 0, m.width), x: s.Gap - start, anchors: m.width == 80 && m.height == 25}, true
}
