package tui

import (
	"errors"
	"fmt"
	"strconv"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
)

// MaxInspectionRenderBytes bounds expanded HOST markers, independently of E's
// native/text limits. This is host policy, not an original WP resource metric.
const MaxInspectionRenderBytes = 64 << 10

// RevealInspection is copied diagnostic data for the VISIBLE partial pane.
// It grants no native presentation, movement, mutation or IO authority.
type RevealInspection struct {
	Available, Partial            bool
	Revision                      document.Revision
	StartGap, EndGap, TotalTokens int
	TrueEOF                       bool
	Elements                      []document.Element
}

func copyInspection(x RevealInspection) RevealInspection {
	x.Elements = append([]document.Element(nil), x.Elements...)
	return x
}

// Merely reading State/View must not claim or advance UI authority.
func (m Model) inspectionEligible(s editor.Snapshot) bool {
	if m.runtime == nil || s.Mode != editor.Editing || !s.Reveal || s.Selection || s.Pending != nil ||
		m.repeatEntry || m.notice != "" || m.reconcile != "" || len(m.unsettled) != 0 || m.firstPending != nil ||
		m.macro != nil || m.macroTicket != nil || m.macroCPU || m.macroDeferred != nil ||
		m.macroStatus.Active || m.macroStatus.WorkerPending || m.macroStatus.DisplaySuppressed {
		return false
	}
	m.runtime.mu.Lock()
	defer m.runtime.mu.Unlock()
	return !m.runtime.stopping && m.uiAuthority != nil && m.runtime.uiAuthority == m.uiAuthority
}

func (m Model) visibleFrame() macroPane {
	// Select frozen pixels AND diagnostics before inspecting any live native data.
	if m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {
		frame := *m.macroFrozen
		if !m.session.Snapshot().Reveal {
			frame.inspection = RevealInspection{}
		}
		return frame
	}
	s := m.session.Snapshot()
	if !m.inspectionEligible(s) {
		return m.legacyFrame()
	}
	return m.liveInspectionFrame(s)
}

// State is an observation, not an implicit normal/virtual Present request.
func (m Model) inspectionState() RevealInspection {
	if m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {
		if !m.session.Snapshot().Reveal {
			return RevealInspection{}
		}
		return copyInspection(m.macroFrozen.inspection)
	}
	s := m.session.Snapshot()
	if !m.inspectionEligible(s) {
		return RevealInspection{}
	}
	return copyInspection(m.liveInspectionFrame(s).inspection)
}
func (m Model) liveInspectionFrame(s editor.Snapshot) macroPane {
	session := m.session
	d := session.Document()
	if d == nil {
		return m.legacyFrame()
	}
	count := min(d.TokenCount(), document.MaxWindowTokens)
	catalogue, err := document.InspectRevealCatalogue(d, s.NativeRevision, 0, count)
	if err != nil {
		return macroPane{err: err}
	}
	// E authenticates/bounds the SAME captured session/window before Present's
	// contiguous raw copy. The session is immutable; no caller wrapper is reused.
	frame := m.legacyFrame()
	var failure *document.Failure
	if !errors.As(frame.err, &failure) || failure.Category != document.UnsupportedToken {
		return frame
	}
	lower, err := inspectionRuns(catalogue)
	if err != nil {
		return macroPane{err: err}
	}
	frame.reveal = renderReveal(lower, 0, m.width)
	frame.inspection = RevealInspection{Available: true, Partial: true, Revision: catalogue.Revision,
		StartGap: catalogue.StartGap, EndGap: catalogue.EndGap, TotalTokens: catalogue.TotalTokens,
		TrueEOF: catalogue.TrueEOF, Elements: catalogue.Elements}
	return frame
}
func (m Model) legacyFrame() macroPane {
	normal, reveal, x, err := m.legacyPanes()
	return macroPane{normal: normal, reveal: reveal, x: x, err: err}
}

// Preflight lengths BEFORE run/marker/result construction. Elements come only
// from the approved E API; H neither reads native bytes nor reclassifies owners.
func inspectionRuns(c document.CatalogueInspection) ([]revealRun, error) {
	if len(c.Elements) > document.MaxWindowTokens {
		return nil, fmt.Errorf("inspection render owner limit")
	}
	size := 0
	for _, e := range c.Elements {
		n := len(e.Text)
		if e.Kind == document.Opaque && e.Text == "" {
			if e.TokenIndex < 0 {
				return nil, fmt.Errorf("inspection invalid owner ordinal")
			}
			n = 2
			for value := e.TokenIndex; value >= 10; value /= 10 {
				n++
			}
		}
		if n > MaxInspectionRenderBytes-size {
			return nil, fmt.Errorf("inspection expanded render limit")
		}
		size += n
	}
	runs := make([]revealRun, 0, len(c.Elements))
	for _, e := range c.Elements {
		text, role := e.Text, revealBase
		if e.Kind == document.Opaque && text == "" {
			text = "?" + strconv.Itoa(e.TokenIndex)
		} else if e.Kind != document.ASCII {
			role = revealCode
		}
		runs = append(runs, revealRun{text: text, role: role})
	}
	return runs, nil
}
