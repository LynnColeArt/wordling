// Package input preserves terminal event identity without resolving editor commands.
package input

import (
	"fmt"

	tea "charm.land/bubbletea/v2"
)

// Kind identifies an input transport event, never a WordPerfect command.
type Kind string

const (
	Press                Kind = "press"
	Release              Kind = "release"
	Paste                Kind = "paste"
	PasteStart           Kind = "paste-start"
	PasteEnd             Kind = "paste-end"
	Resize               Kind = "resize"
	MouseClick           Kind = "mouse-click"
	MouseRelease         Kind = "mouse-release"
	MouseMotion          Kind = "mouse-motion"
	MouseWheel           Kind = "mouse-wheel"
	KeyboardCapabilities Kind = "keyboard-capabilities"
	Capability           Kind = "capability"
	TerminalVersion      Kind = "terminal-version"
	Focus                Kind = "focus"
	Blur                 Kind = "blur"
	Unknown              Kind = "unknown"
)

// Key retains all fields delivered by pinned Bubble Tea v2.1.1. Zero alternate
// codes do not prove a physical key lacks an alternate identity.
type Key struct {
	Code        rune       `json:"code"`
	Mod         tea.KeyMod `json:"mod"`
	Text        string     `json:"text"`
	ShiftedCode rune       `json:"shifted_code"`
	BaseCode    rune       `json:"base_code"`
	IsRepeat    bool       `json:"is_repeat"`
}

// Support describes an actual KeyboardEnhancementsMsg, not requested features.
type Support struct {
	Flags          int  `json:"flags"`
	Disambiguation bool `json:"disambiguation"`
	EventTypes     bool `json:"event_types"`
	AlternateKeys  bool `json:"alternate_keys"`
	AllKeys        bool `json:"all_keys"`
	AssociatedText bool `json:"associated_text"`
}

// Event is a transport-only tagged value. Original retains opaque unknown
// messages in process; SourceType identifies them in diagnostics. Callers must
// ignore unknown and release events when dispatching contextual press commands.
type Event struct {
	Kind       Kind       `json:"kind"`
	Key        *Key       `json:"key,omitempty"`
	Text       string     `json:"text,omitempty"`
	Width      int        `json:"width,omitempty"`
	Height     int        `json:"height,omitempty"`
	Mouse      *tea.Mouse `json:"mouse,omitempty"`
	Support    *Support   `json:"support,omitempty"`
	SourceType string     `json:"source_type"`
	Original   tea.Msg    `json:"-"`
}

func key(k tea.Key) *Key {
	return &Key{k.Code, k.Mod, k.Text, k.ShiftedCode, k.BaseCode, k.IsRepeat}
}

// Translate is stateless: it never concatenates Escape with subsequent keys,
// infers modifiers, reparses paste, or assigns commands such as Cancel or Exit.
func Translate(msg tea.Msg) Event {
	e := Event{Kind: Unknown, SourceType: fmt.Sprintf("%T", msg), Original: msg}
	switch m := msg.(type) {
	case tea.KeyPressMsg:
		e.Kind, e.Key = Press, key(tea.Key(m))
	case tea.KeyReleaseMsg:
		e.Kind, e.Key = Release, key(tea.Key(m))
	case tea.PasteMsg:
		e.Kind, e.Text = Paste, m.Content
	case tea.PasteStartMsg:
		e.Kind = PasteStart
	case tea.PasteEndMsg:
		e.Kind = PasteEnd
	case tea.WindowSizeMsg:
		e.Kind, e.Width, e.Height = Resize, m.Width, m.Height
	case tea.MouseClickMsg:
		e.Kind = MouseClick
		v := m.Mouse()
		e.Mouse = &v
	case tea.MouseReleaseMsg:
		e.Kind = MouseRelease
		v := m.Mouse()
		e.Mouse = &v
	case tea.MouseMotionMsg:
		e.Kind = MouseMotion
		v := m.Mouse()
		e.Mouse = &v
	case tea.MouseWheelMsg:
		e.Kind = MouseWheel
		v := m.Mouse()
		e.Mouse = &v
	case tea.KeyboardEnhancementsMsg:
		e.Kind = KeyboardCapabilities
		e.Support = &Support{m.Flags, m.SupportsKeyDisambiguation(), m.SupportsEventTypes(), m.SupportsAlternateKeys(), m.SupportsAllKeysAsEscapeCodes(), m.SupportsAssociatedText()}
	case tea.CapabilityMsg:
		e.Kind, e.Text = Capability, m.Content
	case tea.TerminalVersionMsg:
		e.Kind, e.Text = TerminalVersion, m.Name
	case tea.FocusMsg:
		e.Kind = Focus
	case tea.BlurMsg:
		e.Kind = Blur
	}
	return e
}
