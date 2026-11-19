package uv

import (
	"bytes"
	"encoding/binary"
	xwindows "github.com/charmbracelet/x/windows"
	"testing"
)

func wordlingKey(vk uint16, char uint16, control uint32, down bool) xwindows.InputRecord {
	r := xwindows.InputRecord{EventType: xwindows.KEY_EVENT}
	if down {
		binary.LittleEndian.PutUint32(r.Event[:4], 1)
	}
	binary.LittleEndian.PutUint16(r.Event[4:6], 1)
	binary.LittleEndian.PutUint16(r.Event[6:8], vk)
	binary.LittleEndian.PutUint16(r.Event[10:12], char)
	binary.LittleEndian.PutUint32(r.Event[12:16], control)
	return r
}

func TestWordlingNativeConsoleRecords(t *testing.T) {
	for _, tc := range []struct {
		name    string
		records []xwindows.InputRecord
		want    string
	}{
		{"shifted text", []xwindows.InputRecord{
			wordlingKey(xwindows.VK_SHIFT, 0, xwindows.SHIFT_PRESSED, true), wordlingKey('K', 'K', xwindows.SHIFT_PRESSED, true),
			wordlingKey('K', 'K', xwindows.SHIFT_PRESSED, false), wordlingKey(xwindows.VK_SHIFT, 0, 0, false),
			wordlingKey(xwindows.VK_SHIFT, 0, xwindows.SHIFT_PRESSED, true), wordlingKey('E', 'E', xwindows.SHIFT_PRESSED, true),
			wordlingKey(xwindows.VK_SHIFT, 0, xwindows.SHIFT_PRESSED, true), wordlingKey('E', 'E', xwindows.SHIFT_PRESSED, true),
			wordlingKey(xwindows.VK_SHIFT, 0, xwindows.SHIFT_PRESSED, true), wordlingKey('P', 'P', xwindows.SHIFT_PRESSED, true),
		}, "KEEP"},
		{"real Ctrl Space", []xwindows.InputRecord{wordlingKey(xwindows.VK_CONTROL, 0, xwindows.LEFT_CTRL_PRESSED, true), wordlingKey(xwindows.VK_SPACE, 0, xwindows.LEFT_CTRL_PRESSED, true)}, "\x00"},
		{"real Ctrl At", []xwindows.InputRecord{wordlingKey(xwindows.VK_SHIFT, 0, xwindows.SHIFT_PRESSED, true), wordlingKey('2', 0, xwindows.SHIFT_PRESSED|xwindows.LEFT_CTRL_PRESSED, true)}, "\x00"},
		{"Alt modifier and VT", []xwindows.InputRecord{wordlingKey(xwindows.VK_MENU, 0, xwindows.LEFT_ALT_PRESSED, true), wordlingKey(0, 27, 0, true), wordlingKey('X', 'x', 0, true)}, "\x1bx"},
		{"Unicode", []xwindows.InputRecord{wordlingKey(0, 0x00fc, 0, true), wordlingKey(0, 0xd83d, 0, true), wordlingKey(0, 0xde00, 0, true)}, "ü😀"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			d := NewTerminalReader(nil, "xterm-256color")
			d.vtInput = true
			var out bytes.Buffer
			d.serializeWin32InputRecords(tc.records, &out)
			if out.String() != tc.want {
				t.Fatalf("native record serialization: got %q want %q", out.String(), tc.want)
			}
		})
	}
}
