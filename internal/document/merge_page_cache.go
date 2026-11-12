package document

import "bytes"

// MatchMergeRecordPageCache checks the Standard Printer record separator
// for its exact native record ordinal and number of physical field lines.
func MatchMergeRecordPageCache(raw []byte, ordinal, fieldLines int) bool {
	return ordinal > 0 && ordinal <= 65535 && fieldLines > 0 && fieldLines <= lastEverydayPageRow &&
		bytes.Equal(raw, everydayPageRecord(uint16(ordinal), uint16(fieldLines)))
}
