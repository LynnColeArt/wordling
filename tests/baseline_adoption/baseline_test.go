// Package baseline_adoption_test exercises only exported application surfaces.
// These tests qualify retained foundations, not the everyday milestone as a whole.
package baseline_adoption_test

import (
	"bytes"
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"regexp"
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/tui"
)

type driver struct {
	t *testing.T
	m tui.Model
}

func open(t *testing.T, root string) *driver {
	t.Helper()
	r, m, e := tui.Open(tui.Config{Root: root, Profile: tui.LocalFlat, NativeProfile: tui.NativeProfile, EditorChrome: true})
	if e != nil {
		t.Fatal(e)
	}
	t.Cleanup(func() {
		if e := r.Close(); e != nil {
			t.Error(e)
		}
	})
	return &driver{t, m}
}
func (d *driver) send(msg tea.Msg) {
	d.t.Helper()
	next, cmd := d.m.Update(msg)
	d.m = next.(tui.Model)
	for steps := 0; cmd != nil; steps++ {
		if steps > 32 {
			d.t.Fatal("unbounded command chain")
		}
		msg = cmd()
		if _, quit := msg.(tea.QuitMsg); quit {
			return
		}
		next, cmd = d.m.Update(msg)
		d.m = next.(tui.Model)
	}
}
func (d *driver) key(code rune, mod tea.KeyMod) {
	d.t.Helper()
	d.send(tea.KeyPressMsg{Code: code, Mod: mod})
}
func (d *driver) text(s string) {
	d.t.Helper()
	for _, r := range s {
		d.send(tea.KeyPressMsg{Code: r, Text: string(r)})
	}
}
func (d *driver) raw() []byte {
	d.t.Helper()
	b, e := d.m.Session().Document().Export()
	if e != nil {
		d.t.Fatal(e)
	}
	return b
}
func (d *driver) clean() {
	d.t.Helper()
	if s := d.m.State(); s.Notice != "" || s.Reconciliation != "" {
		d.t.Fatalf("unexpected failure: %+v", s)
	}
}
func (d *driver) mode(want editor.Mode) {
	d.t.Helper()
	if got := d.m.State().Session.Mode; got != want {
		d.t.Fatalf("mode %s, want %s: %+v", got, want, d.m.State())
	}
}

func (d *driver) fileListing() bool {
	d.t.Helper()
	d.key(tea.KeyF5, 0)
	prompt := strings.Contains(ansi.Strip(d.m.View().Content), `Dir C:\*.*`)
	if prompt {
		d.key(tea.KeyEnter, 0)
	}
	return prompt
}

func (d *driver) retrieveFile(name string) {
	d.t.Helper()
	prompt := d.fileListing()
	ext := filepath.Ext(name)
	base := strings.TrimSuffix(name, ext)
	entry := regexp.MustCompile(`\b` + regexp.QuoteMeta(base) + ` *` + regexp.QuoteMeta(ext) + `\b`)
	if !entry.MatchString(ansi.Strip(d.m.View().Content)) {
		d.t.Fatalf("F5 did not observe %s", name)
	}
	if prompt {
		d.text("n")
		d.text(name)
	}
	d.key(tea.KeyEnter, 0)
	if prompt {
		d.text("1")
	}
	d.clean()
	if d.m.State().Session.Name != name {
		d.t.Fatalf("F5 did not retrieve %s", name)
	}
}

func TestStartupFocusBoundariesAndDefaultKeys(t *testing.T) {
	d := open(t, t.TempDir())
	original := d.raw()
	for _, sz := range []tea.WindowSizeMsg{{Width: 80, Height: 25}, {Width: 283, Height: 82}} {
		d.send(sz)
		v := d.m.View()
		if !v.AltScreen || v.Cursor == nil || v.Cursor.Y != 1 || !strings.HasPrefix(ansi.Strip(v.Content), "File Edit Search Layout") {
			t.Fatal("missing startup menu or document cursor")
		}
		for _, key := range []rune{tea.KeyLeft, tea.KeyRight, tea.KeyBackspace, tea.KeyDelete} {
			d.key(key, 0)
			d.clean()
		}
	}
	if !bytes.Equal(original, d.raw()) {
		t.Fatal("boundary keys changed empty native document")
	}
	d.text("a")
	before := d.raw()
	d.send(tea.MouseClickMsg{X: 1, Y: 0, Button: tea.MouseLeft})
	if !strings.Contains(ansi.Strip(d.m.View().Content), "Retrieve") {
		t.Fatal("File menu absent")
	}
	d.key(tea.KeyF7, 0)
	d.text("b")
	d.clean()
	if !bytes.HasSuffix(d.raw(), []byte("ab")) {
		t.Fatal("menu focus did not return to editing")
	}
	before = d.raw()
	for _, r := range "bsorq" {
		d.key(r, tea.ModCtrl)
		d.mode(editor.Editing)
		if !bytes.Equal(before, d.raw()) || d.m.State().PendingIO != 0 {
			t.Fatal("nonhistorical shortcut mutated or started I/O")
		}
	}
}

func TestNewReturnCorrectionRevealFirstSaveAndRetrieve(t *testing.T) {
	root := t.TempDir()
	d := open(t, root)
	d.text("Alpha")
	d.key(tea.KeyEnter, 0)
	d.text("Betax")
	d.key(tea.KeyBackspace, 0)
	d.clean()
	before := d.raw()
	if !bytes.HasSuffix(before, []byte("Alpha\nBeta")) {
		t.Fatal("Enter/correction did not produce native hard return")
	}
	history := d.m.Session().History()
	if history.CountKnown() {
		entry, err := history.Entry(0)
		if err != nil || !history.Qualified() || history.Count() != 1 || !bytes.Equal(entry.Native, []byte("x")) {
			t.Fatalf("qualified Backspace did not retain the exact erased character: %v", err)
		}
	} else if history.Qualified() {
		t.Fatal("unknown history claimed qualification")
	}
	d.key(tea.KeyF3, tea.ModAlt)
	d.clean()
	if !strings.Contains(ansi.Strip(d.m.View().Content), "[HRt]") {
		t.Fatal("Reveal omitted paragraph code")
	}
	d.key(tea.KeyF3, tea.ModAlt)
	if !bytes.Equal(before, d.raw()) {
		t.Fatal("Reveal changed native bytes")
	}
	d.key(tea.KeyF10, 0)
	d.mode(editor.SaveName)
	d.text("LINES.WP")
	d.key(tea.KeyEnter, 0)
	d.clean()
	d.mode(editor.Editing)
	disk, e := os.ReadFile(filepath.Join(root, "LINES.WP"))
	if e != nil || !bytes.Equal(before, disk) {
		t.Fatalf("first save did not publish exact native bytes: %v", e)
	}
	if d.m.State().Session.Dirty {
		t.Fatal("successful verified first save remained dirty")
	}
	retrieved := open(t, root)
	retrieved.retrieveFile("LINES.WP")
	if !bytes.Equal(before, retrieved.raw()) {
		t.Fatal("F5 retrieval changed native source")
	}

	// FLOW.WP is the original Fast Save specimen with a 564-byte prefix.
	// Read-only admission must not turn into editing authority.
	opaque, err := os.ReadFile("../../docs/research/everyday-contract-2026-11-05/qualification/flow/exports/FLOW.WP")
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(root, "FLOW.WP")
	if err := os.WriteFile(path, opaque, 0600); err != nil {
		t.Fatal(err)
	}
	readonly := open(t, root)
	blank := readonly.raw()
	readonly.key(tea.KeyF10, tea.ModShift)
	readonly.text("FLOW.WP")
	readonly.key(tea.KeyEnter, 0)
	state := readonly.m.State().Session
	if state.Name == "FLOW.WP" {
		readonly.clean()
		if !bytes.Equal(opaque, readonly.raw()) {
			t.Fatal("original read-only source was not retrieved verbatim")
		}
		readonly.key(tea.KeyF6, 0)
		if readonly.m.State().Notice == "" || !bytes.Equal(opaque, readonly.raw()) || readonly.m.State().Session.Dirty {
			t.Fatal("unsupported Bold changed the read-only native document")
		}
	} else if state.Mode != editor.RetrieveName || state.Last.Result.Err == nil ||
		!strings.Contains(state.Last.Result.Err.Error(), "UnsupportedPrefix") ||
		!bytes.Equal(blank, readonly.raw()) || state.Dirty {
		t.Fatal("unsupported retrieval did not preserve the current native document")
	}
	disk, e = os.ReadFile(path)
	if e != nil || !bytes.Equal(opaque, disk) {
		t.Fatal("refused edit touched disk")
	}
}

func TestSaveCancelAndNormalExitConserveBuffer(t *testing.T) {
	root := t.TempDir()
	d := open(t, root)
	d.text("unsaved")
	before := d.raw()
	d.key(tea.KeyF10, 0)
	d.text("CANCEL.WP")
	d.key(tea.KeyF1, 0)
	d.mode(editor.Editing)
	if !bytes.Equal(before, d.raw()) {
		t.Fatal("save cancellation changed native")
	}
	entries, e := os.ReadDir(root)
	if e != nil || len(entries) != 0 {
		t.Fatal("cancel published a file")
	}
	d.key(tea.KeyF7, 0)
	d.mode(editor.ExitSaveQuestion)
	d.key(tea.KeyF1, 0)
	d.mode(editor.Editing)
	if !bytes.Equal(before, d.raw()) {
		t.Fatal("exit cancellation changed native")
	}
	d.key(tea.KeyF7, 0)
	d.text("n")
	d.mode(editor.ExitQuestion)
	d.text("y")
	d.mode(editor.Exited)
}

// R77-001 remains a safety regression, never an accepted baseline limitation.
func TestResizeModalInputCannotEditDocument(t *testing.T) {
	for _, mode := range []string{"files first screen", "files list", "menu"} {
		t.Run(mode, func(t *testing.T) {
			root := t.TempDir()
			d := open(t, root)
			d.text("baseline")
			if mode == "files list" {
				d.fileListing()
			} else if mode == "files first screen" {
				d.key(tea.KeyF5, 0)
			} else {
				d.send(tea.KeyPressMsg{Code: '=', Mod: tea.ModAlt, Text: "="})
			}
			raw := d.raw()
			snapshot := d.m.State().Session
			history := d.m.Session().History()
			for _, height := range []int{12, 11, 25, 11, 12, 25} {
				d.send(tea.WindowSizeMsg{Width: 80, Height: height})
				_ = d.m.View()
				d.text("x")
				if !bytes.Equal(raw, d.raw()) || !reflect.DeepEqual(snapshot, d.m.State().Session) || !reflect.DeepEqual(history, d.m.Session().History()) {
					t.Fatalf("%s at height%d leaked input into document", mode, height)
				}
				if height < 12 && (!strings.Contains(ansi.Strip(d.m.View().Content), "active") || d.m.View().Cursor != nil) {
					t.Fatal("small-window modal focus not represented truthfully")
				}
				t.Logf("%s height%d: native bytes, session revision/dirty state and history conserved", mode, height)
			}
			d.key(tea.KeyF7, 0)
			d.text("y")
			d.clean()
			if !bytes.HasSuffix(d.raw(), []byte("baseliney")) {
				t.Fatal("cancel did not return document focus")
			}
			expected := d.raw()
			d.key(tea.KeyF10, 0)
			d.text("FOCUS.WP")
			d.key(tea.KeyEnter, 0)
			d.clean()
			saved, e := os.ReadFile(filepath.Join(root, "FOCUS.WP"))
			if e != nil || !bytes.Equal(saved, expected) {
				t.Fatal("post-modal save failed native conservation", e)
			}
		})
	}
}

func TestCLIThroughPTY(t *testing.T) {
	if _, e := exec.LookPath("python3"); e != nil {
		t.Fatal("python3 is required for the Linux PTY acceptance probe")
	}
	binary := filepath.Join(t.TempDir(), "wordling")
	build := exec.Command("go", "build", "-o", binary, "./cmd/wordling")
	build.Dir = "../.."
	if b, e := build.CombinedOutput(); e != nil {
		t.Fatalf("build: %v\n%s", e, b)
	}
	cmd := exec.Command("python3", "cli_probe.py", binary)
	if b, e := cmd.CombinedOutput(); e != nil {
		t.Fatalf("real CLI probe: %v\n%s", e, b)
	} else {
		t.Log(string(b))
	}
	// The first F5 screen identifies which reviewed real-CLI journey applies.
	// Both probes must assert the same resize/focus and publication safety.
	d := open(t, t.TempDir())
	d.key(tea.KeyF5, 0)
	resize := exec.Command("python3", "../../internal/tui/evidence/resize-modal/cli_resize.py", binary)
	if strings.Contains(ansi.Strip(d.m.View().Content), `Dir C:\*.*`) {
		repo, err := filepath.Abs("../..")
		if err != nil {
			t.Fatal(err)
		}
		resize = exec.Command("python3", "../../internal/tui/evidence/everyday/pty-everyday.py",
			repo, binary, filepath.Join(t.TempDir(), "pty"))
	}
	if b, e := resize.CombinedOutput(); e != nil {
		t.Fatalf("real CLI modal resize: %v\n%s", e, b)
	} else {
		t.Log(string(b))
	}
}
