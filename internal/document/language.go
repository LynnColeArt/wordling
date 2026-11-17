package document

import (
	"fmt"
	"strings"
)

var languageCodes = strings.Fields("CA HR CZ DK NL OZ UK US SU CF FR GA DE SD GR MA IS IT NO BR PO RU SL ES SV YK")

func validLanguage(code string) bool {
	if len(code) != 2 {
		return false
	}
	for _, known := range languageCodes {
		if code == known {
			return true
		}
	}
	return false
}

func languageOwner(raw []byte) bool {
	return len(raw) == 12 && raw[0] == 0xd3 && raw[1] == 0x11 && raw[2] == 8 && raw[3] == 0 &&
		raw[11] == 0xd3 && sameRecordTrailer(raw, 8) && validLanguage(string(raw[4:6])) && validLanguage(string(raw[6:8]))
}

func (d *Document) LanguageAt(gap int) string {
	for i := gap - 1; i >= 0; i-- {
		t, err := d.Token(i)
		if err == nil && t.Kind == LanguageCode {
			return string(t.Raw[6:8])
		}
	}
	return "US"
}

func (d *Document) HasNonUSLanguage() bool {
	for i := 0; i < d.TokenCount(); i++ {
		t, _ := d.Token(i)
		if t.Kind == LanguageCode && string(t.Raw[6:8]) != "US" {
			return true
		}
	}
	return false
}

func (d *Document) InsertLanguage(c Cursor, code string) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	code = strings.ToUpper(code)
	if !validLanguage(code) {
		return unchangedEdit(d, c), fmt.Errorf("enter a recognized two-letter WordPerfect language code")
	}
	prior := d.LanguageAt(c.gap)
	if code == prior {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	return d.editTokens(c, []byte{0xd3, 0x11, 8, 0, prior[0], prior[1], code[0], code[1], 8, 0, 0x11, 0xd3})
}
