// wordling runs the bounded native editing Linux session; complete M1 parity remains open.
package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"reflect"

	tea "charm.land/bubbletea/v2"
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
	root := flags.String("root", "", "absolute operator-selected validated local directory")
	profile := flags.String("profile", "", "required local-flat or explicitly selected macro-cout profile; no generalized DOS paths")
	if err := flags.Parse(args); err != nil {
		return err
	}
	if flags.NArg() != 0 {
		return errors.New("unexpected positional arguments")
	}
	if !term.IsTerminal(in.Fd()) || !term.IsTerminal(out.Fd()) {
		return errors.New("wordling requires terminal stdin/stdout")
	}
	runtime, model, err := tui.Open(tui.Config{Root: *root, Profile: *profile})
	if err != nil {
		return err
	}
	before, beforeErr := term.GetState(in.Fd())
	final, runErr := tea.NewProgram(model, tea.WithInput(in), tea.WithOutput(out)).Run()
	// This waits for real started IO even when Bubble Tea stopped accepting msgs.
	closeErr := runtime.Close()
	after, afterErr := term.GetState(in.Fd())
	var issues []error
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
	if ok && ended.State().Reconciliation != "" {
		issues = append(issues, errors.New(ended.State().Reconciliation))
	}
	return errors.Join(issues...)
}
