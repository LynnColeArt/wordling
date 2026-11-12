package document_test

import (
	"bytes"
	"encoding/binary"
	"testing"

	"github.com/lynncoleart/wordling/internal/document"
)

func mergeCodeBody(t *testing.T, d *document.Document) []byte {
	t.Helper()
	raw := mustExport(t, d)
	return raw[binary.LittleEndian.Uint32(raw[4:8]):]
}

func TestAuthoredMergeOwnerBoundaries(t *testing.T) {
	d := newDocument(t)
	cursor, _ := d.CursorAt(0)
	field, err := d.InsertMergeCode(cursor, document.AuthorMergeField, "1")
	if err != nil {
		t.Fatal(err)
	}
	expected := []byte{0xde, 0x36, 4, 0, 4, 0, 0x36, 0xde, '1', '~'}
	if got := mergeCodeBody(t, field.Document); !bytes.Equal(got, expected) || field.Cursor.Gap() != 3 {
		t.Fatalf("native field and gap %x / %d", got, field.Cursor.Gap())
	}
	for i := 1; i <= 2; i++ {
		operand, _ := field.Document.CursorAt(i)
		if rejected, err := field.Document.InsertAuthoredMergeText(operand, []byte("X")); err == nil || rejected.Document != field.Document || rejected.Cursor != operand {
			t.Fatalf("operand gap %d accepted or modified: %+v / %v", i, rejected, err)
		}
	}
	if rejected, err := field.Document.InsertMergeCode(cursor, document.AuthorMergeHardPage, ""); err == nil || rejected.Document != field.Document {
		t.Fatalf("foreign revision accepted or modified: %+v / %v", rejected, err)
	}
	operand, _ := field.Document.CursorAt(1)
	operand = operand.WithReveal(true)
	if _, err := field.Document.InsertAuthoredMergeText(operand, []byte("X")); err == nil {
		t.Fatal("nondigit accepted in numeric operand")
	}
	if _, err := field.Document.DeleteAuthoredMergeText(operand, false); err == nil {
		t.Fatal("deletion left a missing operand")
	}
	inserted, err := field.Document.InsertAuthoredMergeText(operand, []byte("2"))
	if err != nil {
		t.Fatal(err)
	}
	corrected, err := inserted.Document.DeleteAuthoredMergeText(inserted.Cursor, false)
	if err != nil || !bytes.Equal(mergeCodeBody(t, corrected.Document), append(expected[:8:8], '2', '~')) {
		t.Fatalf("operand-only correction %+v / %v", corrected, err)
	}
	if _, err := corrected.Document.DeleteAuthoredMergeText(corrected.Cursor, false); err == nil {
		t.Fatal("operand terminator was removed")
	}
	owner, _ := field.Document.CursorAt(0)
	if _, err := field.Document.DeleteMergeCode(owner, false); err == nil {
		t.Fatal("merge owner deleted outside Reveal")
	}
	deleted, err := field.Document.DeleteMergeCode(owner.WithReveal(true), false)
	if err != nil || !bytes.Equal(mergeCodeBody(t, deleted.Document), []byte("1~")) || deleted.Cursor.Gap() != 0 {
		t.Fatalf("field-only removal %+v / %v", deleted, err)
	}
}

func TestAuthoredSecondaryRecordOwnsFieldCountAndPage(t *testing.T) {
	d := newDocument(t)
	cursor, _ := d.CursorAt(0)
	var err error
	for range 2 {
		var field document.EditResult
		field, err = d.InsertMergeCode(cursor, document.AuthorMergeEndField, "")
		if err != nil {
			t.Fatal(err)
		}
		d, cursor = field.Document, field.Cursor
	}
	if field, ok := d.MergeFieldAt(cursor); !ok || field != 3 {
		t.Fatalf("active field %d / %v", field, ok)
	}
	record, err := d.InsertMergeCode(cursor, document.AuthorMergeEndRecord, "")
	if err != nil {
		t.Fatal(err)
	}
	raw := mergeCodeBody(t, record.Document)
	if len(raw) != 61 || raw[22] != 3 || binary.LittleEndian.Uint16(raw[34:36]) != 400 ||
		binary.LittleEndian.Uint16(raw[36:38]) != 1 || raw[len(raw)-1] != 0x0c {
		t.Fatalf("record count/page %x", raw)
	}
	if field, ok := record.Document.MergeFieldAt(record.Cursor); !ok || field != 1 {
		t.Fatalf("new record field %d / %v", field, ok)
	}
}

func TestAuthoredNamedMergeFileIsLiteralAndProtected(t *testing.T) {
	d := newDocument(t)
	cursor, _ := d.CursorAt(0)
	for _, bad := range []string{"", "X~Y", "child", "C:\\HAS SPACE", string(bytes.Repeat([]byte("X"), 64))} {
		result, err := d.InsertNamedMergeCode(cursor, document.MergeNestPrimary, bad)
		if err == nil || result.Document != d || result.Cursor != cursor {
			t.Fatalf("invalid native operand %q: %+v / %v", bad, result, err)
		}
	}
	result, err := d.InsertNamedMergeCode(cursor, document.MergeNestPrimary, "C:\\OUT\\CHILD")
	if err != nil {
		t.Fatal(err)
	}
	body := mergeCodeBody(t, result.Document)
	frame := []byte{0xde, 0x45, 4, 0, 4, 0, 0x45, 0xde}
	if !bytes.Equal(body, append(frame, []byte("C:\\OUT\\CHILD~")...)) {
		t.Fatalf("native nest %x", body)
	}
	token, _ := result.Document.Token(0)
	if token.Kind.MergeLabel(true) != "[Mrg:NEST PRIMARY]" {
		t.Fatalf("recognized native owner %+v", token)
	}
}
