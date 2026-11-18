package tui

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"
	"unsafe"

	"github.com/charmbracelet/x/ansi"
	"golang.org/x/sys/windows"
)

func TestNativePowerShellSelection(t *testing.T) {
	t.Setenv("SHELL", "")
	defaultShell := platformShell()
	if name := strings.ToLower(filepath.Base(defaultShell.Path)); name != "pwsh.exe" && name != "powershell.exe" {
		t.Fatal("Windows default is not PowerShell", defaultShell.Args)
	}
	if strings.Join(defaultShell.Args[1:], " ") != "-NoLogo" {
		t.Fatal("interactive profiles disabled", defaultShell.Args)
	}
	// PATH discovery prefers PowerShell 7, and cannot select the current directory.
	fake := t.TempDir()
	if err := os.WriteFile(filepath.Join(fake, "pwsh.exe"), nil, 0600); err != nil {
		t.Fatal(err)
	}
	t.Setenv("PATH", fake)
	if got := platformShell().Path; got != filepath.Join(fake, "pwsh.exe") {
		t.Fatal("PowerShell 7 not preferred", got)
	}
	t.Setenv("PATH", t.TempDir())
	builtin := filepath.Join(os.Getenv("SystemRoot"), "System32", "WindowsPowerShell", "v1.0", "powershell.exe")
	if got := platformShell().Path; !strings.EqualFold(got, builtin) {
		t.Fatal("Windows PowerShell fallback missing", got)
	}
	for _, name := range []string{"pwsh.exe", "powershell.exe", "cmd.exe", "bash.exe"} {
		path := filepath.Join(fake, name)
		t.Setenv("SHELL", path)
		cmd := platformShell()
		arg := "-NoLogo"
		if name == "cmd.exe" {
			arg = "/D"
		}
		if name == "bash.exe" {
			arg = "-i"
		}
		if cmd.Path != path || len(cmd.Args) != 2 || cmd.Args[1] != arg {
			t.Fatal("explicit shell override", cmd.Args)
		}
	}
}

// Drive the real packaged app through the Windows console API. This covers the
// Win32 input/terminal path and PowerShell, which cross-compilation cannot test.
type nativeConsole struct {
	t          *testing.T
	input      *os.File
	output     *os.File
	console    windows.Handle
	process    windows.Handle
	mu         sync.Mutex
	transcript []byte
	closed     bool
}

func startNativeConsole(t *testing.T, command []string, dir string) *nativeConsole {
	t.Helper()
	inR, inW, err := os.Pipe()
	if err != nil {
		t.Fatal(err)
	}
	outR, outW, err := os.Pipe()
	if err != nil {
		inR.Close()
		inW.Close()
		t.Fatal(err)
	}
	c := &nativeConsole{t: t, input: inW, output: outR}
	if err := windows.CreatePseudoConsole(windows.Coord{X: 80, Y: 25}, windows.Handle(inR.Fd()), windows.Handle(outW.Fd()), 0, &c.console); err != nil {
		t.Fatal(err)
	}
	inR.Close()
	outW.Close()
	t.Cleanup(c.close)
	go func() {
		buf := make([]byte, 8192)
		for {
			n, err := outR.Read(buf)
			if n > 0 {
				c.mu.Lock()
				c.transcript = append(c.transcript, buf[:n]...)
				c.mu.Unlock()
			}
			if err != nil {
				return
			}
		}
	}()
	attrs, err := windows.NewProcThreadAttributeList(1)
	if err != nil {
		t.Fatal(err)
	}
	defer attrs.Delete()
	// The pseudoconsole attribute takes the handle value, unlike handle-list
	// attributes which take a pointer to an array.
	consoleValue := *(*unsafe.Pointer)(unsafe.Pointer(&c.console))
	if err := attrs.Update(windows.PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE, consoleValue, unsafe.Sizeof(c.console)); err != nil {
		t.Fatal(err)
	}
	startup := windows.StartupInfoEx{StartupInfo: windows.StartupInfo{Cb: uint32(unsafe.Sizeof(windows.StartupInfoEx{}))}, ProcThreadAttributeList: attrs.List()}
	application, err := windows.UTF16PtrFromString(command[0])
	if err != nil {
		t.Fatal(err)
	}
	args, err := windows.UTF16PtrFromString(windows.ComposeCommandLine(command))
	if err != nil {
		t.Fatal(err)
	}
	working, err := windows.UTF16PtrFromString(dir)
	if err != nil {
		t.Fatal(err)
	}
	var process windows.ProcessInformation
	if err := windows.CreateProcess(application, args, nil, nil, false, windows.EXTENDED_STARTUPINFO_PRESENT, nil, working, &startup.StartupInfo, &process); err != nil {
		t.Fatal(err)
	}
	c.process = process.Process
	windows.CloseHandle(process.Thread)
	return c
}

func (c *nativeConsole) close() {
	if c.closed {
		return
	}
	c.closed = true
	if c.process != 0 {
		windows.TerminateProcess(c.process, 99)
		windows.WaitForSingleObject(c.process, 5000)
		windows.CloseHandle(c.process)
	}
	c.input.Close()
	// Drain output concurrently while closing: ClosePseudoConsole can flush a
	// final frame synchronously and must not wait on an unread pipe.
	windows.ClosePseudoConsole(c.console)
	c.output.Close()
	if dir := os.Getenv("WORDLING_NATIVE_REPORT_DIR"); dir != "" {
		os.MkdirAll(dir, 0700)
		c.mu.Lock()
		data := bytes.Clone(c.transcript)
		c.mu.Unlock()
		name := strings.NewReplacer("/", "-", "\\", "-").Replace(c.t.Name()) + ".vt"
		if err := os.WriteFile(filepath.Join(dir, name), data, 0600); err != nil {
			c.t.Error(err)
		}
	}
}
func (c *nativeConsole) mark() int { c.mu.Lock(); defer c.mu.Unlock(); return len(c.transcript) }
func (c *nativeConsole) wait(from int, text string) {
	c.t.Helper()
	deadline := time.Now().Add(25 * time.Second)
	for time.Now().Before(deadline) {
		c.mu.Lock()
		got := ansi.Strip(string(c.transcript[from:]))
		c.mu.Unlock()
		if strings.Contains(got, text) {
			return
		}
		time.Sleep(40 * time.Millisecond)
	}
	c.mu.Lock()
	got := string(c.transcript)
	c.mu.Unlock()
	if len(got) > 18000 {
		got = got[len(got)-18000:]
	}
	c.t.Fatalf("console did not show %q; transcript tail:\n%s", text, got)
}
func (c *nativeConsole) send(text string) int {
	c.t.Helper()
	mark := c.mark()
	if _, err := io.WriteString(c.input, text); err != nil {
		c.t.Fatal(err)
	}
	return mark
}
func (c *nativeConsole) step(text, want string) { c.t.Helper(); c.wait(c.send(text), want) }

func TestNativePowerShellConsole(t *testing.T) {
	binary := os.Getenv("WORDLING_NATIVE_BINARY")
	if binary == "" {
		executable, err := os.Executable()
		if err != nil {
			t.Fatal(err)
		}
		sibling := filepath.Join(filepath.Dir(executable), "wordling.exe")
		if info, err := os.Stat(sibling); err == nil && info.Mode().IsRegular() {
			binary = sibling
		}
	}
	if binary == "" {
		// Source-tree runs build the same normal executable. Packaged CI always
		// supplies the hash-verified application, never a different test double.
		binary = filepath.Join(t.TempDir(), "wordling.exe")
		cmd := exec.Command("go", "build", "-o", binary, "../../cmd/wordling")
		if out, err := cmd.CombinedOutput(); err != nil {
			t.Fatalf("build application: %v\n%s", err, out)
		}
	}
	builtin := filepath.Join(os.Getenv("SystemRoot"), "System32", "WindowsPowerShell", "v1.0", "powershell.exe")
	for _, version := range []struct {
		name, shell string
		major       int
	}{{"default", "", 7}, {"WindowsPowerShell", builtin, 5}} {
		t.Run(version.name, func(t *testing.T) {
			t.Setenv("SHELL", version.shell)
			shell := platformShell().Path
			major := version.major
			if strings.EqualFold(filepath.Base(shell), "powershell.exe") {
				major = 5
			}
			root := filepath.Join(t.TempDir(), "workspace space ü 文")
			if err := os.Mkdir(root, 0700); err != nil {
				t.Fatal(err)
			}
			t.Setenv("LOCALAPPDATA", t.TempDir())
			t.Setenv("XDG_CACHE_HOME", t.TempDir())
			t.Setenv("TERM", "xterm-256color")
			t.Setenv("COLORTERM", "truecolor")
			quote := func(s string) string { return "'" + strings.ReplaceAll(s, "'", "''") + "'" }
			launch := "& " + quote(binary) + " -root " + quote(root) + " -control-keys -theme classic -tabs=false; exit $LASTEXITCODE"
			c := startNativeConsole(t, []string{shell, "-NoLogo", "-NoProfile", "-Command", launch}, root)
			c.wait(0, "Doc 1 Pg")
			c.step("KEEP", "KEEP")
			c.step("\x1b[1;5P", "Save document 1 before opening shell?")
			c.send("\x1b")
			time.Sleep(150 * time.Millisecond)
			c.step("\x1b[1;5P", "Save document 1 before opening shell?")
			c.step("n", "Type exit to return to Wordling.")
			c.wait(0, "PS ")
			c.step("Write-Output ('POWERSHELL-' + $PSVersionTable.PSVersion.Major + '-OK')\r", fmt.Sprintf("POWERSHELL-%d-OK", major))
			c.step("Write-Output ('PIPELINE-' + (1..3 | Measure-Object -Sum).Sum)\r", "PIPELINE-6")
			c.step("if ((Get-Location).Path -eq "+quote(root)+") { Write-Output ('WORKSPACE-' + 'OK') }\r", "WORKSPACE-OK")
			c.step("exit\r", "KEEP")
			c.step("SAFE", "SAFE")
			c.step("\x1b[21~", "Document to be saved:")
			c.send("FIRST.WP\r")
			deadline := time.Now().Add(15 * time.Second)
			for time.Now().Before(deadline) {
				if _, err := os.Stat(filepath.Join(root, "FIRST.WP")); err == nil {
					break
				}
				time.Sleep(40 * time.Millisecond)
			}
			data, err := os.ReadFile(filepath.Join(root, "FIRST.WP"))
			if err != nil || !bytes.Contains(data, []byte("KEEPSAFE")) {
				t.Fatal("save after PowerShell return", err, string(data))
			}
			time.Sleep(200 * time.Millisecond)
			c.step("OVER", "OVER")
			c.step("\x1b[21~", "Document to be saved:")
			c.step("\r", "Replace FIRST.WP? No (Yes)")
			c.send("n")
			time.Sleep(150 * time.Millisecond)
			if got, err := os.ReadFile(filepath.Join(root, "FIRST.WP")); err != nil || !bytes.Equal(got, data) {
				t.Fatal("cancelled overwrite changed disk", err)
			}
			c.send("\x1b")
			time.Sleep(150 * time.Millisecond)
			c.step("\x1b[21~", "Document to be saved:")
			c.step("\r", "Replace FIRST.WP? No (Yes)")
			c.send("y")
			deadline = time.Now().Add(15 * time.Second)
			for time.Now().Before(deadline) {
				got, err := os.ReadFile(filepath.Join(root, "FIRST.WP"))
				if err == nil && bytes.Contains(got, []byte("KEEPSAFEOVER")) {
					break
				}
				time.Sleep(40 * time.Millisecond)
			}
			if got, err := os.ReadFile(filepath.Join(root, "FIRST.WP")); err != nil || !bytes.Contains(got, []byte("KEEPSAFEOVER")) {
				t.Fatal("confirmed overwrite failed", err, string(got))
			}
			time.Sleep(200 * time.Millisecond)
			// Resizing must preserve the edited buffer and native console input.
			mark := c.mark()
			if err := windows.ResizePseudoConsole(c.console, windows.Coord{X: 100, Y: 30}); err != nil {
				t.Fatal(err)
			}
			c.wait(mark, "KEEPSAFE")
			mark = c.mark()
			if err := windows.ResizePseudoConsole(c.console, windows.Coord{X: 80, Y: 25}); err != nil {
				t.Fatal(err)
			}
			c.wait(mark, "KEEPSAFE")
			c.send("\x1b=")
			time.Sleep(150 * time.Millisecond)
			c.step("f", "Open Shell")
			c.step("h", "Type exit to return to Wordling.")
			c.step("exit 13\r", "Shell: exit status 13")
			c.send("\x1b=")
			time.Sleep(150 * time.Millisecond)
			c.step("f", "Quit Wordling")
			c.send("q")
			if state, err := windows.WaitForSingleObject(c.process, 15000); err != nil || state != windows.WAIT_OBJECT_0 {
				t.Fatalf("console app failed to exit: %v %v", state, err)
			}
			var code uint32
			if err := windows.GetExitCodeProcess(c.process, &code); err != nil || code != 0 {
				t.Fatalf("console app exit: %d %v", code, err)
			}
			t.Logf("PowerShell %d: launched app, cancel/skip dirty save, pipeline, Unicode cwd, shell return, save, cancel/confirm overwrite, resize, menu shell and error return passed", major)
		})
	}
}
