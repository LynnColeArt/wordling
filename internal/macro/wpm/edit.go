package wpm

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"strings"
)

const MaxEditedDescription = 79

// RecordingKeys decodes the bounded action profile that the editor can change.
// Display Off leads the action. Enter's two words form one editable key.
func (i *Image) RecordingKeys() ([]uint16, bool) {
	if i == nil || len(i.info.Findings) != 0 || i.info.Body.Length > 4+4*MaxRecordedKeys || i.info.Body.Length < 4 {
		return nil, false
	}
	body := i.data[i.info.Body.Offset:]
	if binary.LittleEndian.Uint16(body) != 0xfc0c {
		return nil, false
	}
	var keys []uint16
	for pos := 2; pos < len(body)-2; pos += 2 {
		word := binary.LittleEndian.Uint16(body[pos:])
		switch {
		case word == RecordedEnter:
			pos += 2
			if pos >= len(body)-2 || binary.LittleEndian.Uint16(body[pos:]) != EnterFollower {
				return nil, false
			}
		case word == RecordedLeft, word == ActionReturn, word >= 32 && word <= 126 && word != '~':
		default:
			return nil, false
		}
		if len(keys) == MaxRecordedKeys {
			return nil, false
		}
		keys = append(keys, word)
	}
	return keys, true
}

// Edit preserves the source's command stream unless replaceAction is set.
// It relocates only the witnessed contiguous description and body. Opaque
// body words can survive description editing, but opaque prefix indexes cannot.
func (i *Image) Edit(description string, keys []uint16, replaceAction bool) ([]byte, error) {
	if i == nil || len(i.data) == 0 {
		return nil, fmt.Errorf("no acquired WPM")
	}
	d := i.info.Description
	bodyAt := i.info.Header.BodyOffset
	if d.Offset != 56 || d.Offset+d.Length != bodyAt || bytes.IndexByte(i.data[d.Offset:bodyAt-1], 0) >= 0 ||
		!bytes.Equal(i.data[36:56], make([]byte, 20)) {
		return nil, fmt.Errorf("cannot relocate an unfamiliar WPM prefix")
	}
	oldDescription := string(i.data[d.Offset : bodyAt-1])
	if description != oldDescription && (len(description) > MaxEditedDescription || strings.IndexFunc(description, func(c rune) bool { return c < 32 || c > 126 }) >= 0) {
		return nil, fmt.Errorf("description requires at most %d printable ASCII characters", MaxEditedDescription)
	}
	body := i.data[bodyAt:]
	if replaceAction {
		if _, ok := i.RecordingKeys(); !ok {
			return nil, fmt.Errorf("this WPM's action cannot be edited")
		}
		var err error
		body, err = recordingBody(keys)
		if err != nil {
			return nil, err
		}
	}
	newBodyAt := d.Offset + uint32(len(description)) + 1
	if int(newBodyAt)+len(body) > MaxInputBytes {
		return nil, fmt.Errorf("edited WPM exceeds the native input limit")
	}
	raw := make([]byte, 0, int(newBodyAt)+len(body))
	raw = append(raw, i.data[:d.Offset]...)
	binary.LittleEndian.PutUint32(raw[4:], newBodyAt)
	binary.LittleEndian.PutUint32(raw[28:], uint32(len(description)+1))
	raw = append(raw, description...)
	raw = append(raw, 0)
	return append(raw, body...), nil
}
