package input_test

import (
	"reflect"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

func TestOriginalKeyIdentities(t *testing.T) {
	for _, k := range []tea.Key{
		{Code: tea.KeyF1}, {Code: tea.KeyF3}, {Code: tea.KeyF7}, {Code: tea.KeyF10},
		{Code: tea.KeyF3, Mod: tea.ModAlt}, {Code: tea.KeyF10, Mod: tea.ModShift},
		{Code: '=', Mod: tea.ModAlt}, {Code: tea.KeyHome}, {Code: tea.KeyRight},
		{Code: tea.KeyEscape}, {Code: 'q', Text: "q"}, {Code: 's', Mod: tea.ModCtrl},
		{Code: 'a', Text: "A", Mod: tea.ModShift, ShiftedCode: 'A', BaseCode: 'a', IsRepeat: true},
	} {
		for _, release := range []bool{false, true} {
			var msg tea.Msg = tea.KeyPressMsg(k)
			want := input.Press
			if release {
				msg = tea.KeyReleaseMsg(k)
				want = input.Release
			}
			e := input.Translate(msg)
			if e.Kind != want || e.Key == nil || !reflect.DeepEqual(tea.Key{Code: e.Key.Code, Mod: e.Key.Mod, Text: e.Key.Text, ShiftedCode: e.Key.ShiftedCode, BaseCode: e.Key.BaseCode, IsRepeat: e.Key.IsRepeat}, k) {
				t.Fatalf("lost key: %#v -> %#v", msg, e)
			}
		}
	}
}

func TestNoEscapeOrPasteCommandInference(t *testing.T) {
	for _, m := range []tea.Msg{tea.KeyPressMsg{Code: tea.KeyEscape}, tea.KeyPressMsg{Code: '5', Text: "5"}, tea.KeyPressMsg{Code: 'x', Text: "x"}} {
		e := input.Translate(m)
		if e.Kind != input.Press || e.Key.Mod != 0 {
			t.Fatalf("guessed Alt: %#v", e)
		}
	}
	p := "\x1bOP\x1b[21;2~\x11\x13q\n☃"
	e := input.Translate(tea.PasteMsg{Content: p})
	if e.Kind != input.Paste || e.Text != p || e.Key != nil {
		t.Fatalf("paste reinterpreted: %#v", e)
	}
}

func TestNonKeyEvents(t *testing.T) {
	unknown := &struct{ Private int }{42}
	cases := []struct {
		msg  tea.Msg
		kind input.Kind
	}{
		{tea.PasteStartMsg{}, input.PasteStart}, {tea.PasteEndMsg{}, input.PasteEnd},
		{tea.WindowSizeMsg{Width: 80, Height: 25}, input.Resize},
		{tea.MouseClickMsg{X: 3, Y: 4, Button: tea.MouseLeft, Mod: tea.ModAlt}, input.MouseClick},
		{tea.MouseReleaseMsg{}, input.MouseRelease}, {tea.MouseMotionMsg{}, input.MouseMotion}, {tea.MouseWheelMsg{}, input.MouseWheel},
		{tea.FocusMsg{}, input.Focus}, {tea.BlurMsg{}, input.Blur},
		{tea.CapabilityMsg{Content: "RGB"}, input.Capability}, {tea.TerminalVersionMsg{Name: "test"}, input.TerminalVersion},
		{unknown, input.Unknown}, {nil, input.Unknown},
	}
	for _, c := range cases {
		e := input.Translate(c.msg)
		if e.Kind != c.kind || e.Key != nil || e.Original != c.msg {
			t.Fatalf("bad non-key: %#v", e)
		}
	}
	e := input.Translate(cases[2].msg)
	if e.Width != 80 || e.Height != 25 {
		t.Fatal("resize lost")
	}
	e = input.Translate(cases[3].msg)
	if e.Mouse == nil || e.Mouse.X != 3 || e.Mouse.Y != 4 || e.Mouse.Mod != tea.ModAlt {
		t.Fatal("mouse lost")
	}
}

func TestSupportsUsesActualResponse(t *testing.T) {
	for flags := 0; flags < 64; flags++ {
		m := tea.KeyboardEnhancementsMsg{Flags: flags}
		e := input.Translate(m)
		if e.Kind != input.KeyboardCapabilities || e.Support == nil || e.Support.Flags != flags || e.Support.Disambiguation != m.SupportsKeyDisambiguation() || e.Support.EventTypes != m.SupportsEventTypes() || e.Support.AlternateKeys != m.SupportsAlternateKeys() || e.Support.AllKeys != m.SupportsAllKeysAsEscapeCodes() || e.Support.AssociatedText != m.SupportsAssociatedText() {
			t.Fatalf("guessed support %d: %#v", flags, e)
		}
	}
}
