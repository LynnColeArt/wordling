package tui

import (
	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/input"
)

func isFunctionKey(code rune) bool {
	return code >= tea.KeyF1 && code <= tea.KeyF63
}

func normalizeEditorKey(key *input.Key) {
	// Lock state does not modify a WordPerfect command.
	key.Mod &^= tea.ModNumLock
	if key.Text == "" || isFunctionKey(key.Code) {
		key.Mod &^= tea.ModCapsLock
	}
	if isFunctionKey(key.Code) {
		key.Text = ""
	}

	// Application keypad mode keeps the Alt modifier on keypad Plus in
	// VTE. Translate the keypad identities so regular typing still works.
	if key.Code >= tea.KeyKp0 && key.Code <= tea.KeyKp9 {
		key.Code = '0' + key.Code - tea.KeyKp0
	} else if code, ok := keypadCodes[key.Code]; ok {
		key.Code = code
	} else {
		return
	}
	if key.Code >= 32 && key.Code <= 126 && key.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 {
		key.Text = string(key.Code)
	}
}

var keypadCodes = map[rune]rune{
	tea.KeyKpPlus: '+', tea.KeyKpMinus: '-', tea.KeyKpMultiply: '*',
	tea.KeyKpDivide: '/', tea.KeyKpEqual: '=', tea.KeyKpDecimal: '.', tea.KeyKpComma: ',',
	tea.KeyKpEnter: tea.KeyEnter, tea.KeyKpHome: tea.KeyHome, tea.KeyKpEnd: tea.KeyEnd,
	tea.KeyKpUp: tea.KeyUp, tea.KeyKpDown: tea.KeyDown, tea.KeyKpLeft: tea.KeyLeft,
	tea.KeyKpRight: tea.KeyRight, tea.KeyKpPgUp: tea.KeyPgUp, tea.KeyKpPgDown: tea.KeyPgDown,
	tea.KeyKpInsert: tea.KeyInsert, tea.KeyKpDelete: tea.KeyDelete,
}
