// Command inspect is a read-only HOST demonstrator, not a Wordling product
// command, original reference runner or native exporter. No discovery or writes.
package inspect

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"syscall"

	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/wp51"
)

const maxOutputBytes = 1 << 20

type entry struct {
	TokenIndex  int           `json:"token_index"`
	Kind        document.Kind `json:"kind"`
	Span        wp51.Span     `json:"span"`
	Text        string        `json:"text"`
	Unsupported bool          `json:"unsupported"`
}
type report struct {
	Schema       string  `json:"schema"`
	SourceSHA256 string  `json:"source_sha256"`
	SameRevision bool    `json:"same_revision"`
	StartGap     int     `json:"start_gap"`
	EndGap       int     `json:"end_gap"`
	TotalTokens  int     `json:"total_tokens"`
	TrueEOF      bool    `json:"true_eof"`
	Elements     []entry `json:"elements"`
}

func readNative(path string) ([]byte, error) {
	before, e := os.Lstat(path)
	if e != nil {
		return nil, e
	}
	if !before.Mode().IsRegular() {
		return nil, errors.New("input must be a regular native file, not a symlink/device/pipe")
	}
	f, e := os.OpenFile(path, os.O_RDONLY|syscall.O_NOFOLLOW, 0)
	if e != nil {
		return nil, e
	}
	defer f.Close()
	opened, e := f.Stat()
	if e != nil {
		return nil, e
	}
	if !opened.Mode().IsRegular() || !os.SameFile(before, opened) {
		return nil, errors.New("input identity changed")
	}
	if opened.Size() > wp51.MaxInputBytes {
		return nil, errors.New("input exceeds reader byte limit")
	}
	raw, e := io.ReadAll(io.LimitReader(f, wp51.MaxInputBytes+1))
	if e != nil {
		return nil, e
	}
	if len(raw) > wp51.MaxInputBytes {
		return nil, errors.New("input exceeds reader byte limit")
	}
	after, e := f.Stat()
	if e != nil {
		return nil, e
	}
	if opened.Size() != after.Size() || opened.ModTime() != after.ModTime() {
		return nil, errors.New("input changed while reading")
	}
	return raw, nil
}

// Run is the public host CLI entry. It returns failures, including broken output,
// to its caller; diagnostic JSON contains no serialized opaque identity/authority.
func Run(args []string, out, diagnostics io.Writer) int {
	if out == nil || diagnostics == nil {
		return 2
	}
	if len(args) > 16 {
		return 2
	}
	size := 0
	for _, a := range args {
		size += len(a)
		if size > 65536 {
			return 2
		}
	}
	flags := flag.NewFlagSet("reveal-inspect", flag.ContinueOnError)
	flags.SetOutput(diagnostics)
	input := flags.String("input", "", "explicit public native input file")
	start := flags.Int("start", 0, "first complete token index")
	count := flags.Int("count", -1, "owner count (-1: bounded remainder)")
	if e := flags.Parse(args); e != nil {
		return 2
	}
	if *input == "" || flags.NArg() != 0 {
		fmt.Fprintln(diagnostics, "-input is required; no positional arguments")
		return 2
	}
	fail := func(e error) int { fmt.Fprintln(diagnostics, e); return 1 }
	raw, e := readNative(*input)
	if e != nil {
		return fail(e)
	}
	d, e := document.Parse(raw)
	if e != nil {
		return fail(e)
	}
	n := *count
	if n == -1 {
		if *start < 0 || *start > d.TokenCount() {
			return fail(errors.New("invalid start"))
		}
		n = min(d.TokenCount()-*start, document.MaxWindowTokens)
	}
	rev := d.Revision()
	p, e := document.InspectRevealCatalogue(d, rev, *start, n)
	if e != nil {
		return fail(e)
	}
	hash := sha256.Sum256(raw)
	r := report{Schema: "wordling.reveal-catalogue/v1", SourceSHA256: hex.EncodeToString(hash[:]), SameRevision: p.Revision == rev, StartGap: p.StartGap, EndGap: p.EndGap, TotalTokens: p.TotalTokens, TrueEOF: p.TrueEOF, Elements: make([]entry, len(p.Elements))}
	for i, x := range p.Elements {
		r.Elements[i] = entry{x.TokenIndex, x.Kind, x.Span, x.Text, x.Kind == document.Opaque && x.Text == ""}
	}
	data, e := json.Marshal(r)
	if e != nil {
		return fail(e)
	}
	if len(data)+1 > maxOutputBytes {
		return fail(errors.New("JSON output limit"))
	}
	data = append(data, '\n')
	nWritten, e := out.Write(data)
	if e != nil {
		return fail(e)
	}
	if nWritten != len(data) {
		return fail(io.ErrShortWrite)
	}
	return 0
}
