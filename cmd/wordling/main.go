// wordling runs the bounded native editing Linux session; complete M1 parity remains open.
package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"reflect"
	"strings"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/charmbracelet/x/term"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/tui"
)

func main() {
	if err := run(os.Args[1:], os.Stdin, os.Stdout); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
func run(args []string, in, out *os.File) error {
	flags := flag.NewFlagSet("wordling", flag.ContinueOnError)
	root := flags.String("root", "", "absolute workspace directory (default: current directory)")
	profile := flags.String("profile", "local-flat", "workspace profile: local-flat or macro-cout")
	startupMacro := flags.String("macro", "", "run this native WPM macro at startup")
	tabs := flags.Bool("tabs", true, "show document tabs (use -tabs=false for the classic layout)")
	theme := flags.String("theme", "ubuntu", "terminal palette: ubuntu or classic")
	controlKeys := flags.Bool("control-keys", false, "opt into nonhistorical Linux shortcuts: Ctrl+B Bold, Ctrl+R Reveal Codes, Ctrl+S Save, Ctrl+O Retrieve, Ctrl+Q Exit")
	normalized := make([]string, 0, len(args))
	for _, arg := range args {
		if strings.HasPrefix(strings.ToLower(arg), "/m-") && len(arg) > 3 {
			arg = "-macro=" + arg[3:]
		}
		normalized = append(normalized, arg)
	}
	if err := flags.Parse(normalized); err != nil {
		return err
	}
	if flags.NArg() != 0 {
		return errors.New("unexpected positional arguments")
	}
	if *theme != "ubuntu" && *theme != "classic" {
		return fmt.Errorf("unknown theme %q (choose ubuntu or classic)", *theme)
	}
	if !term.IsTerminal(in.Fd()) || !term.IsTerminal(out.Fd()) {
		return errors.New("wordling requires terminal stdin/stdout")
	}
	// Default only the CLI root. Runtime validation still checks the resolved
	// directory and explicit roots must still be absolute.
	if *root == "" {
		cwd, err := os.Getwd()
		if err != nil {
			return fmt.Errorf("resolve current workspace: %w", err)
		}
		*root = cwd
	}
	runtime, model, err := tui.Open(tui.Config{Root: *root, Profile: *profile, NativeProfile: tui.NativeProfile, ControlKeys: *controlKeys, EditorChrome: true, DocumentTabs: *tabs, Aubergine: *theme == "ubuntu"})
	if err != nil {
		return err
	}
	model = model.EnableRecovery(*root).WithStartupMacro(*startupMacro)
	before, beforeErr := term.GetState(in.Fd())
	final, runErr := tea.NewProgram(model, tea.WithInput(in), tea.WithOutput(out)).Run()
	_, keypadErr := out.WriteString(ansi.KeypadNumericMode)
	// This waits for real started IO even when Bubble Tea stopped accepting msgs.
	closeErr := runtime.Close()
	after, afterErr := term.GetState(in.Fd())
	var issues []error
	if keypadErr != nil {
		issues = append(issues, keypadErr)
	}
	if beforeErr != nil || afterErr != nil || !reflect.DeepEqual(before, after) {
		issues = append(issues, errors.New("terminal restoration not established"))
	}
	if runErr != nil {
		issues = append(issues, runErr)
	}
	if closeErr != nil {
		issues = append(issues, closeErr)
	}
	ended, ok := final.(tui.Model)
	if ok {
		issues = append(issues, ended.CloseRecovery(runErr == nil && ended.Session().Snapshot().Mode == editor.Exited))
	} else {
		issues = append(issues, model.CloseRecovery(false))
	}
	if !ok || ended.Session().Snapshot().Mode != editor.Exited {
		issues = append(issues, errors.New("host interruption; original exit workflow did not complete"))
	}
	for _, receipt := range runtime.CompletedMacros() {
		if receipt.Interrupted {
			issues = append(issues, fmt.Errorf("host interrupted macro %d after %d actual ordinary effects; partial state is not a saved output or original Cancel", receipt.Run, receipt.AppliedWords))
		}
	}
	for _, receipt := range runtime.Completed() {
		if warning := tui.Reconciliation(receipt); warning != "" {
			issues = append(issues, errors.New(warning))
		}
	}
	if ok {
		phase := ended.State().Session.NewPhase
		if phase == editor.AwaitPublish || phase == editor.AwaitFirstRead || phase == editor.PublishedUnbound || phase == editor.PublicationUncertain {
			issues = append(issues, fmt.Errorf("unresolved New-buffer publication state %s; no saved/recovered claim", phase))
		}
	}
	if ok && ended.State().Reconciliation != "" {
		issues = append(issues, errors.New(ended.State().Reconciliation))
	}
	return errors.Join(issues...)
}
