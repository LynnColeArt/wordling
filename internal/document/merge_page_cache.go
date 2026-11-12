package document

import "bytes"

// MatchMergeRecordPageCache checks the Standard Printer record separator
// against the current physical page and number of field lines on it.
func MatchMergeRecordPageCache(raw []byte, page, fieldLines int) bool {
	return page > 0 && page <= 65535 && fieldLines >= 0 && fieldLines <= lastEverydayPageRow &&
		bytes.Equal(raw, everydayPageRecord(uint16(page), uint16(fieldLines)))
}

// MatchMergeFieldPageSeparator checks the cache and return transition that
// replace an End Field's return on the last row of a Standard Printer page.
func MatchMergeFieldPageSeparator(raw []byte, page, precedingRows int) bool {
	return precedingRows == lastEverydayPageRow && len(raw) == 33 && raw[32] == hardReturnPageByte &&
		MatchMergeRecordPageCache(raw[:32], page, precedingRows)
}
