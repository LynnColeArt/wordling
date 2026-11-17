package document

func kerningOwner(raw []byte) bool {
	return len(raw) == 10 && raw[0] == 0xd9 && raw[1] == 3 && raw[2] == 6 && raw[3] == 0 &&
		raw[4] <= 1 && raw[5] <= 1 && sameRecordTrailer(raw, 6) && raw[9] == 0xd9
}

func (d *Document) KerningAt(gap int) bool {
	for i := gap - 1; i >= 0; i-- {
		t, err := d.Token(i)
		if err == nil && t.Kind == KerningCode {
			return t.Raw[5] == 1
		}
	}
	return false
}

func (d *Document) InsertKerning(c Cursor, enabled bool) (EditResult, error) {
	if err := d.checkEverydayCursor(c); err != nil {
		return unchangedEdit(d, c), err
	}
	prior := d.KerningAt(c.gap)
	if prior == enabled {
		return d.everydayNoOp(c, blockFormatEdit), nil
	}
	oldValue, newValue := byte(0), byte(0)
	if prior {
		oldValue = 1
	}
	if enabled {
		newValue = 1
	}
	return d.editTokens(c, []byte{0xd9, 3, 6, 0, oldValue, newValue, 6, 0, 3, 0xd9})
}
