// wordling-input-probe records transport evidence; it is not an editor.
package main

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"runtime"
	"runtime/debug"
	"sync"
	"time"

	tea "charm.land/bubbletea/v2"
	uv "github.com/charmbracelet/ultraviolet"
	"github.com/charmbracelet/x/term"
	"github.com/lynncoleart/wordling/internal/input"
)

type record struct {
	Sequence    uint64 `json:"sequence"`
	Nanoseconds int64  `json:"nanoseconds_since_start"`
	Kind        string `json:"kind"`
	Value       any    `json:"value"`
}

// One lock orders raw read chunks, terminal output, and decoded events. These
// are separate streams: a raw chunk is not necessarily one decoded event.
type journal struct {
	mu      sync.Mutex
	start   time.Time
	seq     uint64
	err     error
	encoder *json.Encoder
}

func (j *journal) add(kind string, value any) error {
	j.mu.Lock()
	defer j.mu.Unlock()
	if j.err != nil {
		return j.err
	}
	j.seq++
	j.err = j.encoder.Encode(record{j.seq, time.Since(j.start).Nanoseconds(), kind, value})
	return j.err
}
func (j *journal) failure() error { j.mu.Lock(); defer j.mu.Unlock(); return j.err }

type captureFile struct {
	*os.File
	journal *journal
}

func (f *captureFile) Read(p []byte) (int, error) {
	n, err := f.File.Read(p)
	if n > 0 {
		if e := f.journal.add("raw-input", hex.EncodeToString(p[:n])); e != nil {
			return n, e
		}
	}
	return n, err
}
func (f *captureFile) Write(p []byte) (int, error) {
	n, err := f.File.Write(p)
	if n > 0 {
		if e := f.journal.add("terminal-output", hex.EncodeToString(p[:n])); e != nil {
			return n, e
		}
	}
	return n, err
}

type finish struct{}
type model struct {
	journal  *journal
	duration time.Duration
	enhanced bool
	finished bool
}

func (m model) Init() tea.Cmd {
	return tea.Batch(tea.RequestTerminalVersion, tea.Tick(m.duration, func(time.Time) tea.Msg { return finish{} }))
}
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if _, ok := msg.(finish); ok {
		m.finished = true
		return m, tea.Quit
	}
	e := input.Translate(msg)
	if err := m.journal.add("event", e); err != nil {
		return m, tea.Quit
	}
	// No key quits or changes recording mode. The deadline is a probe control.
	return m, nil
}
func (m model) View() tea.View {
	v := tea.NewView("Wordling input evidence probe. Recording only; ends at deadline.\n")
	v.ReportFocus = true
	if m.enhanced {
		v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	}
	return v
}

type identity struct {
	Path   string `json:"path"`
	SHA256 string `json:"sha256,omitempty"`
	Bytes  int64  `json:"bytes,omitempty"`
	Error  string `json:"error,omitempty"`
}

func fingerprint(path string) identity {
	i := identity{Path: path}
	if path == "" {
		i.Error = "not supplied"
		return i
	}
	f, err := os.Open(path)
	if err != nil {
		i.Error = err.Error()
		return i
	}
	h := sha256.New()
	i.Bytes, err = io.Copy(h, f)
	err = errors.Join(err, f.Close())
	if err != nil {
		i.Error = err.Error()
		return i
	}
	i.SHA256 = hex.EncodeToString(h.Sum(nil))
	return i
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
func run() error {
	output := flag.String("output", "", "new evidence directory (must not exist)")
	duration := flag.Duration("duration", 45*time.Second, "recording deadline; no keyboard quit shortcut")
	profile := flag.String("profile", "", "operator label; does not confer qualification")
	transport := flag.String("transport", "unasserted", "physical-direct or synthetic-pty or unasserted; operator assertion only")
	terminal := flag.String("terminal-binary", "", "exact terminal emulator binary to fingerprint")
	version := flag.String("terminal-version", "", "operator-recorded terminal version")
	config := flag.String("terminal-config", "", "terminal configuration file to fingerprint")
	layout := flag.String("keyboard-layout", "unasserted", "operator-recorded layout")
	enhanced := flag.Bool("enhanced", true, "request additional pinned Bubble Tea keyboard enhancements (response is separate; library may still negotiate basic disambiguation)")
	flag.Parse()
	if *output == "" || *duration <= 0 || *duration > time.Hour {
		return errors.New("require -output and duration in (0,1h]")
	}
	if *transport != "physical-direct" && *transport != "synthetic-pty" && *transport != "unasserted" {
		return errors.New("invalid transport label")
	}
	if !term.IsTerminal(os.Stdin.Fd()) || !term.IsTerminal(os.Stdout.Fd()) {
		return errors.New("probe requires terminal stdin and stdout; use a direct terminal or explicitly labelled synthetic PTY")
	}
	if err := os.Mkdir(*output, 0700); err != nil {
		return err
	}
	f, err := os.OpenFile(filepath.Join(*output, "journal.jsonl"), os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0600)
	if err != nil {
		return err
	}
	j := &journal{start: time.Now(), encoder: json.NewEncoder(f)}
	before, beforeErr := term.GetState(os.Stdin.Fd())
	env := map[string]string{}
	for _, name := range []string{"TERM", "COLORTERM", "LANG", "LC_ALL", "LC_CTYPE", "XDG_SESSION_TYPE", "DISPLAY", "WAYLAND_DISPLAY", "TMUX", "STY", "SSH_TTY"} {
		env[name] = os.Getenv(name)
	}
	// Capture only terminfo, never the full environment or terminal config text.
	infoContext, cancelInfo := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancelInfo()
	info, infoErr := exec.CommandContext(infoContext, "infocmp", "-1", os.Getenv("TERM")).CombinedOutput()
	build, _ := debug.ReadBuildInfo()
	if err = j.add("profile", map[string]any{"label": *profile, "transport_assertion": *transport, "qualification": "unqualified-capture", "keyboard_layout_assertion": *layout, "terminal_binary": fingerprint(*terminal), "terminal_version_assertion": *version, "terminal_config": fingerprint(*config), "environment": env, "terminfo": string(info), "terminfo_error": errorText(infoErr), "goos": runtime.GOOS, "goarch": runtime.GOARCH, "build": build, "enhanced_requested": *enhanced, "uv_default_esc_timeout_ns": int64(uv.DefaultEscTimeout), "start_utc": j.start.UTC().Format(time.RFC3339Nano)}); err != nil {
		f.Close()
		return err
	}
	p := tea.NewProgram(model{journal: j, duration: *duration, enhanced: *enhanced}, tea.WithInput(&captureFile{os.Stdin, j}), tea.WithOutput(&captureFile{os.Stdout, j}))
	finalModel, runErr := p.Run()
	ended, _ := finalModel.(model)
	after, afterErr := term.GetState(os.Stdin.Fd())
	// State equality checks the actual terminal restoration, not original F7.
	stateSame := beforeErr == nil && afterErr == nil && reflect.DeepEqual(before, after)
	if !stateSame {
		runErr = errors.Join(runErr, errors.New("terminal state restoration not established"))
	}
	if !ended.finished {
		runErr = errors.Join(runErr, errors.New("recording stopped before probe deadline"))
	}
	endErr := j.add("end", map[string]any{"run_error": errorText(runErr), "deadline_reached": ended.finished, "terminal_state_restored": stateSame, "before_state_error": errorText(beforeErr), "after_state_error": errorText(afterErr), "qualification": "unqualified-capture"})
	return errors.Join(runErr, j.failure(), endErr, f.Close())
}
func errorText(err error) string {
	if err == nil {
		return ""
	}
	return err.Error()
}

var _ io.ReadWriteCloser = (*captureFile)(nil)
var _ term.File = (*captureFile)(nil)
