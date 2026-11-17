package wpm

import (
	"encoding/binary"
	"fmt"
)

const (
	RecordedEnter uint16 = 0x800a
	RecordedLeft  uint16 = 0x8019
	// ActionReturn is a visual line break inserted by unmodified Enter
	// in the Action editor. This word is also the companion of RecordedEnter.
	ActionReturn    uint16 = 0x000a
	EnterFollower          = ActionReturn
	MaxRecordedKeys        = 4096
)

// EncodeRecording writes the original Ctrl+F10 profile: a description and a
// run of printable keys, Enter and Left, bracketed by Display Off and EOF.
func EncodeRecording(description string, keys []uint16) ([]byte, error) {
	if len(description) > MaxEditedDescription || len(keys) == 0 || len(keys) > MaxRecordedKeys {
		return nil, fmt.Errorf("macro requires 1 to %d keys and a description of at most 79 characters", MaxRecordedKeys)
	}
	for _, c := range description {
		if c < 32 || c > 126 {
			return nil, fmt.Errorf("macro description requires printable ASCII")
		}
	}
	const descriptionStart = 56
	offset := descriptionStart + len(description) + 1
	raw := make([]byte, offset, offset+4+len(keys)*4)
	copy(raw, "\xffWPC")
	binary.LittleEndian.PutUint32(raw[4:], uint32(offset))
	copy(raw[8:], []byte{1, 1, 1, 1})
	copy(raw[16:], []byte{0xfb, 0xff, 4, 0, 40, 0})
	raw[26] = 1
	binary.LittleEndian.PutUint32(raw[28:], uint32(len(description)+1))
	raw[32] = descriptionStart
	copy(raw[descriptionStart:], description)
	for _, key := range keys {
		if key == ActionReturn {
			return nil, fmt.Errorf("recording Enter requires its command word")
		}
	}
	body, err := recordingBody(keys)
	if err != nil {
		return nil, err
	}
	return append(raw, body...), nil
}

func recordingBody(keys []uint16) ([]byte, error) {
	if len(keys) > MaxRecordedKeys {
		return nil, fmt.Errorf("macro exceeds %d keys", MaxRecordedKeys)
	}
	raw := binary.LittleEndian.AppendUint16(make([]byte, 0, 4+len(keys)*4), 0xfc0c)
	for _, k := range keys {
		switch {
		case k == RecordedEnter:
			raw = binary.LittleEndian.AppendUint16(raw, k)
			raw = binary.LittleEndian.AppendUint16(raw, EnterFollower)
		case k == RecordedLeft || k == ActionReturn || k >= 32 && k <= 126 && k != '~':
			raw = binary.LittleEndian.AppendUint16(raw, k)
		default:
			return nil, fmt.Errorf("unsupported recording key %04x", k)
		}
	}
	return binary.LittleEndian.AppendUint16(raw, 0), nil
}
