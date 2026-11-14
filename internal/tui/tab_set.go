package tui

import (
	"math"
	"slices"
	"strconv"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/input"
)

type tabSetUI struct {
	ruler      document.TabSet
	pos        int
	draft      string
	chooseType bool
}

func (m Model) openTabSet() Model {
	ruler, position, err := m.session.TabSetPosition()
	if err != nil {
		m.lineFormat.error = err.Error()
		return m
	}
	m.lineFormat.screen = formatTabSet
	m.lineFormat.tabs = tabSetUI{ruler: ruler, pos: position}
	return m
}

func (m Model) tabSetPress(key input.Key) Model {
	form := &m.lineFormat
	tab := &form.tabs
	form.error = ""
	if key.Code == tea.KeyF1 || key.Code == tea.KeyEscape {
		return m.openLineFormat(formatLine)
	}
	if tab.chooseType {
		if key.Code == '1' || key.Code == '2' {
			left, _ := m.session.LineMargins()
			shift := 0
			if !tab.ruler.Absolute {
				shift = left - tab.ruler.Margin
			}
			decimal := make(map[int]bool, len(tab.ruler.Decimal))
			for stop := range tab.ruler.Decimal {
				decimal[stop+shift] = true
			}
			tab.ruler.Decimal = decimal
			tab.ruler.Stops = tab.ruler.Positions(left)
			for len(tab.ruler.Stops) > 0 && tab.ruler.Stops[0] < 0 {
				tab.ruler.Stops = tab.ruler.Stops[1:]
			}
			for n := len(tab.ruler.Stops); n > 0 && tab.ruler.Stops[n-1] > 16800; n = len(tab.ruler.Stops) {
				tab.ruler.Stops = tab.ruler.Stops[:n-1]
			}
			tab.ruler.Absolute, tab.ruler.Margin, tab.chooseType = key.Code == '1', 0, false
			if !tab.ruler.Absolute {
				tab.ruler.Margin, _ = m.session.LineMargins()
			}
		}
		return m
	}
	switch key.Code {
	case tea.KeyF7:
		next, err := m.session.SetTabSet(tab.ruler)
		if err != nil {
			form.error = err.Error()
			return m
		}
		m.session = next
		return m.openLineFormat(formatLine)
	case tea.KeyEnter:
		if tab.draft == "" {
			break
		}
		n, err := strconv.ParseFloat(strings.TrimSuffix(tab.draft, "\""), 64)
		if err != nil {
			form.error = "Enter a tab position in inches"
			return m
		}
		position := tab.ruler.Margin + int(math.Round(n*document.UnitsPerInch))
		if position < 0 || position > 16800 {
			form.error = "Tab position is outside the ruler"
			return m
		}
		i, exists := slices.BinarySearch(tab.ruler.Stops, position)
		if !exists {
			if len(tab.ruler.Stops) == 40 {
				form.error = "The ruler holds at most 40 stops"
				return m
			}
			tab.ruler.Stops = slices.Insert(tab.ruler.Stops, i, position)
		}
		tab.pos, tab.draft = position, ""
	case tea.KeyHome:
		tab.pos = 0
		if key.Mod == tea.ModCtrl {
			tab.pos, _ = m.session.LineMargins()
		}
	case tea.KeyEnd:
		if key.Mod == tea.ModCtrl {
			i, _ := slices.BinarySearch(tab.ruler.Stops, tab.pos)
			for _, pos := range tab.ruler.Stops[i:] {
				delete(tab.ruler.Decimal, pos)
			}
			tab.ruler.Stops = tab.ruler.Stops[:i]
		} else {
			tab.pos = 16800
		}
	case tea.KeyDelete, tea.KeyBackspace:
		if n := len(tab.draft); n > 0 && key.Code == tea.KeyBackspace {
			tab.draft = tab.draft[:n-1]
			break
		}
		if i, ok := slices.BinarySearch(tab.ruler.Stops, tab.pos); ok {
			delete(tab.ruler.Decimal, tab.pos)
			tab.ruler.Stops = slices.Delete(tab.ruler.Stops, i, i+1)
		}
	case tea.KeyLeft:
		tab.pos = max(0, tab.pos-120)
	case tea.KeyRight:
		tab.pos = min(16800, tab.pos+120)
	case tea.KeyDown, tea.KeyUp:
		i, exact := slices.BinarySearch(tab.ruler.Stops, tab.pos)
		if key.Code == tea.KeyDown {
			i--
		} else if exact {
			i++
		}
		if i >= 0 && i < len(tab.ruler.Stops) {
			tab.pos = tab.ruler.Stops[i]
		}
	case 'd', 'D', 'l', 'L':
		if _, ok := slices.BinarySearch(tab.ruler.Stops, tab.pos); ok {
			if tab.ruler.Decimal == nil {
				tab.ruler.Decimal = make(map[int]bool)
			}
			if key.Code == 'd' || key.Code == 'D' {
				tab.ruler.Decimal[tab.pos] = true
			} else {
				delete(tab.ruler.Decimal, tab.pos)
			}
		}
	case 't', 'T':
		tab.chooseType = true
	default:
		if len(tab.draft)+len(key.Text) <= 12 && strings.Trim(key.Text, "0123456789.-\"") == "" {
			tab.draft += key.Text
		}
	}
	return m
}

func (m Model) tabSetView() tea.View {
	tab := m.lineFormat.tabs
	start := tab.ruler.Margin
	if tab.pos < start || tab.pos >= start+m.width*120 {
		start = max(0, (tab.pos/120-m.width/2)*120)
	}
	stops, scale, labels := make([]byte, m.width), make([]byte, m.width), make([]byte, m.width)
	for i := range stops {
		stops[i], scale[i], labels[i] = '.', ' ', ' '
		p := start + i*120
		if p%1200 == 600 {
			scale[i] = '^'
		}
		if p%1200 == 0 {
			scale[i] = '|'
			label := strconv.Itoa((p-tab.ruler.Margin)/1200) + "\""
			copy(labels[i:], label)
		}
	}
	for _, pos := range tab.ruler.Stops {
		i := int(math.Round(float64(pos-start) / 120))
		if i >= 0 && i < len(stops) {
			stops[i] = 'L'
			if tab.ruler.Decimal[pos] {
				stops[i] = 'D'
			}
		}
	}
	view := m.historicView()
	lines := strings.Split(view.Content, "\n")
	first := max(0, len(lines)-5)
	body := []string{string(stops), string(scale), string(labels), "Ctrl-End (clear tabs); Enter Number (set tab); Del (clear tab);", "Type; Left; Center; Right; Decimal; .= Dot Leader; Press Exit when done."}
	if tab.chooseType {
		body[4] = "Tab Type: 1 Absolute; 2 Relative to Margin: 0"
	} else if tab.draft != "" {
		body[4] = "Tab Position: " + tab.draft
	}
	if m.lineFormat.error != "" {
		body[4] = m.lineFormat.error
	}
	for i := first; i < len(lines); i++ {
		lines[i] = clip(body[i-first], m.width)
	}
	view.Content = strings.Join(lines, "\n")
	view.Cursor = tea.NewCursor(max(0, min(m.width-1, (tab.pos-start)/120)), first)
	return view
}
