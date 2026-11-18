package tui

import (
	"fmt"
	"strings"
	"time"
	"unicode/utf8"

	tea "charm.land/bubbletea/v2"
	"github.com/charmbracelet/x/ansi"
	"github.com/lynncoleart/wordling/internal/document"
	"github.com/lynncoleart/wordling/internal/editor"
	"github.com/lynncoleart/wordling/internal/input"
	"github.com/lynncoleart/wordling/internal/storage"
)

// CancelPendingMsg is an explicit host operation, never an original key alias.
// Disk IO continues; commands are held until the late receipt is reconciled.
type CancelPendingMsg struct{}

// RetryFirstReadMsg is explicit host safety, not an original-key alias.
// It cannot publish or acquire a replacement directory.
type RetryFirstReadMsg struct{}
type searchNoticeExpired struct{ notice *uiTransition }

type operation struct {
	id, revision uint64
	kind         editor.IntentKind
}
type Model struct {
	leaveVisited                 [editor.MaxDocumentScreens]bool
	recovery                     recoveryUI
	quitAfterSave                bool
	documentTabs                 bool
	historic                     historicUI
	shellOrigin                  uint8
	shellSavePrompt              bool
	setup                        setupUI
	print                        printUI
	compose                      composeEntry
	summary                      summaryForm
	summaryAuthor, summaryTypist string
	summaryNamesSaved            bool
	tablePrompt                  tablePrompt
	lineFormat                   lineFormatUI
	startupMacro                 string
	sheet                        spreadsheetUI
	recording                    macroRecording
	appearance                   int
	sort                         sortUI
	dateMenu, outlineMenu        bool
	lineDraw                     lineDrawUI
	screenMenu                   bool
	comment                      commentUI
	contents                     contentsUI
	styles                       styleUI
	note                         noteUI
	help                         helpUI
	everyday                     everydayViewport
	proofTop                     [editor.MaxDocumentScreens]int
	ascii                        asciiQualification
	menu                         menuDisplay
	runtime                      *Runtime
	session                      editor.Session
	width, height                int
	notice, reconcile            string
	searchNotice                 *uiTransition
	unsettled                    []operation
	ordinary                     []*ordinaryReceipt
	macro                        *macroFlow
	macroTicket                  *macroTicket
	macroCPU                     bool
	macroStatus                  MacroStatus
	macroFrozen                  *macroPane
	repeatEntry                  bool
	characterRepeat              characterRepeat
	uiAuthority                  *uiTransition
	macroDeferred                *macroIOReceipt
	firstPending                 *firstTicket
}
type State struct {
	MenuBar          MenuBar
	RevealInspection RevealInspection

	Session                   editor.Snapshot
	Width, Height             int
	Notice, Reconciliation    string
	PendingIO                 int
	PhysicalDeliveryQualified bool
	Macro                     MacroStatus
	Profile                   string
	NativeProfile             string
}

func (m Model) State() State {
	profile := ""
	if m.runtime != nil {
		profile = m.runtime.profile
	}
	return State{MenuBar: m.menuState(), RevealInspection: m.inspectionState(), NativeProfile: NativeProfile, Profile: profile, Session: m.session.Snapshot(), Width: m.width, Height: m.height, Notice: m.notice, Reconciliation: m.reconcile, PendingIO: len(m.unsettled) + firstPendingCount(m.firstPending), Macro: m.macroStatus}
}

// Session returns an immutable value for measurements/inspection. Never fork it
// to execute independent intents: this Model owns the sole authoritative chain.
func (m Model) Session() editor.Session { return m.session }
func (m Model) Init() tea.Cmd {
	if m.runtime != nil && m.runtime.editorChrome {
		cmds := []tea.Cmd{tea.Raw(ansi.KeypadApplicationMode)}
		if m.recovery.store != nil {
			cmds = append(cmds, recoveryTimer(5*time.Second))
		}
		if m.startupMacro != "" {
			cmds = append(cmds, func() tea.Msg { return startupMacroMsg{name: m.startupMacro} })
		}
		return tea.Batch(cmds...)
	}
	return nil
}
func (m Model) reduce(event editor.Event) (tea.Model, tea.Cmd) {
	previousMode := m.session.Snapshot().Mode
	proofAdd := previousMode == editor.ProofAskMode
	next, intent, err := m.session.Reduce(event)
	m.session = next
	if err == nil && next.Snapshot().Mode == editor.MacroName && previousMode != editor.MacroName {
		m.macroStatus = MacroStatus{}
		m.macroFrozen = nil
	}
	m.notice = ""
	if err != nil {
		m.notice = err.Error()
	}
	if intent != nil {
		if firstKind(intent.Kind) {
			return m.queueFirst(*intent)
		}
		m.unsettled = append(append([]operation(nil), m.unsettled...), operation{intent.Operation, intent.Revision, intent.Kind})
		if intent.Kind == editor.ProofDictionaryIO || intent.Kind == editor.ReadMacro {
			return m, m.runtime.dispatch(*intent, proofAdd)
		}
		receipt, command := m.runtime.queueOrdinary(*intent)
		m.ordinary = append(append([]*ordinaryReceipt(nil), m.ordinary...), receipt)
		return m, command
	}
	if next.Snapshot().Mode == editor.Exited {
		return m, tea.Quit
	}
	return m, nil
}
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if m.runtime == nil {
		m.notice = "Uninitialized host runtime"
		return m, nil
	}
	token, valid := m.runtime.claimUI(m.uiAuthority)
	if !valid {
		m.notice = "Stale UI transition refused; authentic model retains authority"
		return m, nil
	}
	m.uiAuthority = token
	previous := m.session.Snapshot()
	wasProof := m.session.ProofStatus().Phase != editor.ProofInactive
	if _, press := msg.(tea.KeyPressMsg); press {
		m.searchNotice = nil
	}
	next, cmd := m.update(msg)
	model := next.(Model)
	after := model.session.Snapshot()
	if model.shellOrigin != 0 && !model.shellSavePrompt && cmd == nil {
		if model.reconcile != "" || after.Mode == editor.Editing && (after.Dirty || model.notice != "") {
			notice := model.notice
			model, cmd = model.finishShellSave(false)
			if notice != "" {
				model.notice = notice
			}
		} else if after.Mode == editor.Editing {
			model, cmd = model.nextShellDocument(false)
		}
		after = model.session.Snapshot()
	}
	model.advanceRecovery(previous)
	after = model.session.Snapshot()
	wasSearching := previous.Mode == editor.SearchForwardMode || previous.Mode == editor.SearchBackwardMode || previous.Mode == editor.ReplaceWithMode
	if wasSearching && after.Mode == editor.Editing && after.Notice == "NOT FOUND" {
		model, cmd = model.showSearchMiss(cmd)
	}
	model.finishBrowserRetrieve(previous, after)
	model.invalidateMenu()
	model.prepareASCIIViewport()
	model.prepareEverydayViewport()
	model.prepareProofViewport(wasProof)
	if key, ok := msg.(tea.KeyPressMsg); ok && key.Mod == 0 &&
		((key.Code == tea.KeyPgUp || key.Code == tea.KeyPgDown) && previous.Mode == editor.Editing ||
			key.Code == tea.KeyEnter && previous.Mode == editor.GoToMode && previous.Draft != "") &&
		after.Mode == editor.Editing && previous.Gap != after.Gap {
		model.scrollPageToCaret()
	}
	return model, cmd
}
func (m Model) showSearchMiss(cmd tea.Cmd) (Model, tea.Cmd) {
	token := m.uiAuthority
	m.searchNotice = token
	expiry := tea.Tick(time.Second, func(time.Time) tea.Msg { return searchNoticeExpired{token} })
	if cmd != nil {
		expiry = tea.Batch(cmd, expiry)
	}
	return m, expiry
}

func (m Model) update(msg tea.Msg) (tea.Model, tea.Cmd) {
	m.invalidateCharacterMessage(msg)
	switch msg.(type) {
	case firstReply, RetryFirstReadMsg, macroIOReply, macroReply, macroDuplicateMsg, macroReadRefusedMsg, HostStopMacroMsg, duplicateDispatchMsg, ordinaryReply, resultMsg, proofReply, CancelPendingMsg:
		m.menu = menuDisplay{}
	}
	switch v := msg.(type) {
	case startupMacroMsg:
		return m.runStartupMacro(v.name)
	case recoveryTick:
		if err := m.writeRecovery(); err != nil {
			m.notice = "Autosave: " + err.Error()
		}
		return m, recoveryTimer(time.Minute)
	case shellReturned:
		if v.err != nil {
			m.notice = fmt.Sprintf("Shell: %v", v.err)
		}
		return m, tea.Raw(ansi.KeypadApplicationMode)
	case setupReply:
		return m.finishSetup(v), nil
	case searchNoticeExpired:
		if m.searchNotice == v.notice {
			m.searchNotice = nil
		}
		return m, nil
	case fileFindMissExpired:
		b := &m.historic.browser
		if b.findMiss == v.result {
			b.findMiss, b.findConditions = nil, false
			b.applyFind(v.result)
		}
		return m, nil
	case tea.EnvMsg, tea.ColorProfileMsg, tea.ModeReportMsg, tea.RawMsg:
		// Bubble Tea startup administration is not delivered user input.
		return m, nil
	case firstReply:
		return m.firstResult(v.ticket)
	case RetryFirstReadMsg:
		if m.firstPending != nil || len(m.unsettled) > 0 || m.macro != nil {
			m.notice = "Actual IO still pending; Read retry refused"
			return m, nil
		}
		return m.reduce(editor.Event{Command: editor.RetryFirstRead})
	case macroIOReply:
		return m.macroIO(v.receipt)
	case macroReply:
		return m.macroReply(v)
	case macroDuplicateMsg:
		m.notice = "Duplicate macro dispatch refused; authentic continuation retained"
		return m, nil
	case macroReadRefusedMsg:
		return m.macroReadRefused(v)
	case HostStopMacroMsg:
		return m.hostStopMacro(v.Reason)
	}
	if _, ok := msg.(duplicateDispatchMsg); ok {
		m.notice = "Duplicate IO dispatch refused; no additional operation executed"
		return m, nil
	}
	if reply, ok := msg.(proofReply); ok {
		if reply.owner != m.runtime || reply.result.Kind != editor.ProofDictionaryIO {
			m.notice = "Unbound supplementary dictionary result refused"
			return m, nil
		}
		next, cmd := m.completeIO(reply.result)
		if reply.notice != "" {
			model := next.(Model)
			model.notice = reply.notice
			return model, cmd
		}
		return next, cmd
	}
	if reply, ok := msg.(ordinaryReply); ok {
		return m.completeOrdinary(reply.receipt)
	}
	if reply, ok := msg.(resultMsg); ok {
		m.notice = "Unbound IO result refused; authentic queued receipt retained"
		if reply.result.Kind == editor.ProofDictionaryIO {
			m.notice = "Unbound supplementary dictionary result refused"
		}
		return m, nil
	}
	if _, ok := msg.(CancelPendingMsg); ok {
		return m.reduce(editor.Event{Command: editor.CancelOperation})
	}
	event := input.Translate(msg)
	if len(m.recovery.entries) > 0 && event.Kind != input.Resize {
		if event.Kind == input.Press {
			return m.recoveryPress(*event.Key)
		}
		return m, nil
	}
	if event.Kind == input.Press && m.runtime != nil && m.runtime.editorChrome {
		normalizeEditorKey(event.Key)
		if m.shellOrigin != 0 && !m.shellSavePrompt && m.session.Snapshot().Mode == editor.SaveName &&
			event.Key.Code == tea.KeyEscape && event.Key.Mod == 0 {
			event.Key.Code = tea.KeyF1
		}
	}
	if m.shellSavePrompt && event.Kind != input.Resize {
		if event.Kind == input.Press {
			return m.answerShellSave(*event.Key)
		}
		return m, nil
	}
	if event.Kind == input.Resize {
		m.menu = menuDisplay{}
		m.width = max(1, min(event.Width, 4096))
		m.height = max(1, min(event.Height, 4096))
		return m, nil
	}
	if m.recording.stage != 0 {
		if event.Kind == input.Press {
			return m.recordPress(*event.Key)
		}
		return m, nil
	}
	if m.appearance != 0 {
		if event.Kind == input.Press {
			return m.appearancePress(*event.Key)
		}
		return m, nil
	}
	if m.summary.open {
		if event.Kind == input.Press {
			return m.summaryPress(*event.Key)
		}
		return m, nil
	}
	if m.tablePrompt.stage != 0 {
		if event.Kind == input.Press {
			return m.tablePress(*event.Key)
		}
		return m, nil
	}
	if m.lineFormat.screen != formatClosed {
		if event.Kind == input.Press {
			return m.lineFormatPress(*event.Key)
		}
		return m, nil
	}
	if m.screenMenu {
		if event.Kind == input.Press {
			return m.screenPress(*event.Key)
		}
		return m, nil
	}
	if m.sheet.stage != 0 {
		if event.Kind == input.Press {
			return m.spreadsheetPress(*event.Key)
		}
		return m, nil
	}
	if m.sort.stage != 0 {
		if event.Kind == input.Press {
			return m.sortPress(*event.Key)
		}
		return m, nil
	}
	if m.dateMenu {
		if event.Kind == input.Press {
			return m.datePress(*event.Key)
		}
		return m, nil
	}
	if m.styles.stage != 0 {
		if event.Kind == input.Press {
			return m.stylePress(*event.Key)
		}
		return m, nil
	}
	if m.contents.stage != 0 {
		if event.Kind == input.Press {
			return m.contentsPress(*event.Key)
		}
		return m, nil
	}
	if m.comment.stage != commentClosed {
		if event.Kind == input.Press {
			return m.commentPress(*event.Key)
		}
		return m, nil
	}
	if m.note.stage != 0 {
		if event.Kind == input.Press {
			return m.notePress(*event.Key)
		}
		return m, nil
	}
	if m.print.screen != printClosed {
		if event.Kind == input.Press {
			return m.printPress(*event.Key)
		}
		return m, nil
	}
	if event.Kind == input.Press {
		if m.setup.page != setupClosed {
			return m.setupPress(*event.Key)
		}
		if m.help.active {
			return m.helpPress(*event.Key)
		}
	}
	if m.setup.page != setupClosed || m.help.active {
		return m, nil
	}
	if m.compose.active {
		if event.Kind == input.Press {
			return m.editorComposePress(*event.Key)
		}
		return m, nil
	}
	if m.showEditorChrome() && event.Kind == input.MouseClick {
		if m.historic.dosTextStage != 0 {
			return m, nil
		}
		return m.historicMouse(event.Mouse)
	}
	if event.Kind != input.Press {
		switch event.Kind {
		case input.Paste, input.PasteStart, input.PasteEnd, input.Unknown:
			m.notice = "Unsupported event: " + string(event.Kind) + " (" + event.SourceType + ")"
		}
		return m, nil
	}
	if m.runtime.editorChrome {
		proof := m.session.ProofStatus()
		if proof.Phase != editor.ProofInactive && proof.Phase != editor.ProofEditing {
			return m.proofPress(*event.Key, proof)
		}
	}
	if m.runtime.controlKeys {
		k := controlKey(*event.Key)
		event.Key = &k
	}
	if m.characterRepeat.active {
		return m.characterPress(*event.Key)
	}
	// Rendering may shrink below the historic layout's minimum height, but an
	// active menu or browser still owns input. Keep its state until the user
	// enlarges the window or explicitly backs out; invisible actions cannot
	// reach either a menu command or the document reducer.
	if m.runtime.editorChrome {
		mode := m.session.Snapshot().Mode
		if m.session.StructuralUndeleteActive() && !m.showEditorChrome() {
			key := event.Key
			if key.Mod != 0 || key.Code != tea.KeyF1 && key.Code != tea.KeyEscape {
				return m, nil
			}
		}
		if mergeAuthoringModal(mode) && !m.mergeChoiceVisible(mode) {
			key := event.Key
			if key.Mod != 0 || key.Code != tea.KeyF1 && key.Code != tea.KeyEscape {
				return m, nil
			}
		}
		if !m.showEditorChrome() && (m.historic.menu || m.historic.files || m.historic.dosTextStage != 0) {
			k := event.Key
			if k.Mod != 0 || (k.Code != tea.KeyF1 && k.Code != tea.KeyEscape && k.Code != tea.KeyF7) {
				return m, nil
			}
		}
		if next, cmd, handled := m.historicPress(*event.Key); handled {
			return next, cmd
		}
	}
	m.invalidateMenu()
	if next, handled := m.menuPress(*event.Key); handled {
		return next, nil
	}
	if m.reconcile != "" {
		m.notice = "Resolve filesystem uncertainty before further commands"
		return m, nil
	}
	if (len(m.unsettled) > 0 || m.firstPending != nil) && m.session.Snapshot().Mode != editor.Waiting {
		m.notice = "Detached IO still pending; awaiting its actual receipt"
		return m, nil
	}
	k := event.Key
	if k.IsRepeat {
		m.notice = "Unsupported repeated key event"
		return m, nil
	}
	if m.runtime.editorChrome && m.shellOrigin == 0 && m.session.Snapshot().Mode == editor.Editing &&
		k.Code == 'c' && k.Mod&^tea.ModCapsLock == tea.ModCtrl {
		return m.beginLeave(true)
	}
	// Contextual Linux verification retry, not an original WP command claim.
	if k.Code == tea.KeyF10 && k.Mod == 0 && m.session.Snapshot().NewPhase == editor.PublishedUnbound {
		return m.reduce(editor.Event{Command: editor.RetryFirstRead})
	}
	mode := m.session.Snapshot().Mode
	if m.runtime.editorChrome && (mode == editor.Editing || mode == editor.SearchForwardMode || mode == editor.SearchBackwardMode || editor.IsReplacePrompt(mode)) {
		if m.compose.begin(*k) {
			m.notice = ""
			return m, nil
		}
	}
	if m.runtime.editorChrome && isRecordKey(*k) {
		return m.openMacroRecording(), nil
	}
	if next, handled := m.beginCharacterRepeat(*k); handled {
		return next, nil
	}
	if next, cmd, handled := m.macroKey(k.Code, k.Mod, k.Text); handled {
		return next, cmd
	}
	if next, cmd, handled := m.boldKey(*k); handled {
		return next, cmd
	}
	if mode == editor.Editing && m.session.Snapshot().HomePrefix == 1 && k.Mod == 0 && k.Code == tea.KeySpace {
		return m.reduce(editor.Event{Command: editor.InsertHardSpace})
	}
	command, ok := resolve(*k, mode)
	if command.Command == editor.Left || command.Command == editor.Right {
		command.ViewportColumns = m.width
	}
	if !ok {
		m.notice = "Unsupported key (physical delivery unqualified)"
		if m.showEditorChrome() {
			m.notice = "Key has no command here"
			if isFunctionKey(k.Code) {
				m.notice = fmt.Sprintf("%s has no command here", tea.Key{Code: k.Code, Mod: k.Mod}.String())
			}
		}
		return m, nil
	}
	if command.Command == editor.ProofCtrlF2 {
		return m.startProof()
	}
	return m.reduce(command)
}
func (m Model) completeOrdinary(receipt *ordinaryReceipt) (tea.Model, tea.Cmd) {
	// Update has already claimed this Model's current UI authority. Check
	// exact queue custody before touching unsettled work, reconciliation or
	// Session; a stale/foreign/copied reply must not consume the live receipt.
	for i, queued := range m.ordinary {
		if queued != receipt {
			continue
		}
		result, ok := m.runtime.takeOrdinary(receipt)
		if !ok {
			break
		}
		remaining := make([]*ordinaryReceipt, 0, len(m.ordinary)-1)
		remaining = append(remaining, m.ordinary[:i]...)
		m.ordinary = append(remaining, m.ordinary[i+1:]...)
		return m.completeIO(result)
	}
	m.notice = "Foreign or duplicate IO delivery refused; authentic queued receipt retained"
	return m, nil
}

func (m Model) completeIO(result editor.Result) (tea.Model, tea.Cmd) {
	if firstKind(result.Kind) {
		m.notice = "Unbound first-save payload refused; authentic receipt retained"
		return m, nil
	}
	if result.Kind == editor.ReadMacro {
		m.notice = "Unbound macro IO payload refused; authentic receipt retained"
		return m, nil
	}
	remaining := make([]operation, 0, len(m.unsettled))
	for _, op := range m.unsettled {
		if op != (operation{result.Operation, result.Revision, result.Kind}) {
			remaining = append(remaining, op)
		}
	}
	m.unsettled = remaining
	if warning := Reconciliation(result); warning != "" && result.Kind != editor.ProofDictionaryIO {
		m.reconcile = warning
	}
	pending := m.session.Snapshot().Pending
	attached := pending != nil && pending.Operation == result.Operation && pending.Revision == result.Revision && pending.Kind == result.Kind
	if !attached && result.Err == nil && result.Outcome.State == storage.Published && result.Kind != editor.ProofDictionaryIO {
		m.reconcile = "Detached save published a destination; filesystem reconciliation required"
	}
	next, cmd := m.reduce(editor.Event{Command: editor.Complete, Result: &result})
	if attached && result.Kind == editor.PublishEveryday && result.Err == nil && result.Document != nil {
		model := next.(Model)
		if !model.session.Snapshot().Dirty {
			summary, present, err := model.session.Document().Summary()
			if err == nil && present {
				model.summaryAuthor, model.summaryTypist = summary.Author, summary.Typist
				model.summaryNamesSaved = true
			}
		}
		return model, cmd
	}
	return next, cmd
}

func resolve(k input.Key, mode editor.Mode) (editor.Event, bool) {
	// Delivered text keeps its identity. No q/CtrlQ/CtrlS command aliases.
	if k.Mod&^(tea.ModShift|tea.ModCapsLock) == 0 && k.Text != "" {
		switch mode {
		case editor.ReplaceFindMode, editor.ReplaceWithMode, editor.RetrieveName, editor.SaveName, editor.MacroName, editor.SearchForwardMode, editor.SearchBackwardMode, editor.Editing, editor.GoToMode, editor.ConvertCaseMode, editor.Waiting,
			editor.MoveMenuMode, editor.MoveBlockMode, editor.AppendBlockName, editor.MergeMenuMode, editor.MergePrimaryName, editor.MergeSecondaryName, editor.MergeCodesMode, editor.MergeFieldMode, editor.MergeChoicesMode, editor.MergeOperandMode:
			return editor.Event{Command: editor.Text, Text: k.Text}, true
		case editor.ReplaceConfirmMode, editor.ReplaceMatchMode, editor.ReplaceQuestion, editor.ExitSaveQuestion, editor.ExitQuestion, editor.ExitDocQuestion, editor.DeleteQuestion, editor.RetrieveInsertQuestion, editor.ProtectBlockMode:
			if k.Text == "y" || k.Text == "Y" {
				return editor.Event{Command: editor.Yes}, true
			}
			if k.Text == "n" || k.Text == "N" {
				return editor.Event{Command: editor.No}, true
			}
		case editor.HistoryPreview:
			if k.Text == "0" {
				return editor.Event{Command: editor.No}, true
			}
			if k.Text == "1" {
				return editor.Event{Command: editor.Restore}, true
			}
			if k.Text == "2" {
				return editor.Event{Command: editor.Previous}, true
			}
		}
	}
	event := editor.Event{}
	switch {
	case k.Code == tea.KeyF9 && k.Mod == tea.ModShift:
		event.Command = editor.MergeShiftF9
	case k.Code == tea.KeyEnter && k.Mod == tea.ModCtrl:
		event.Command = editor.MergeCtrlEnter
	case k.Code == tea.KeyF9 && k.Mod == tea.ModCtrl:
		event.Command = editor.MergeCtrlF9
	case k.Code == tea.KeyF2 && k.Mod == tea.ModAlt:
		event.Command = editor.SearchReplace
	case k.Code == tea.KeyF2 && k.Mod == tea.ModCtrl:
		event.Command = editor.ProofCtrlF2
	case k.Code == tea.KeyF2 && k.Mod == tea.ModShift:
		event.Command = editor.SearchBackF2
	case k.Code == tea.KeyF11 && k.Mod == 0:
		event.Command = editor.Reveal
	case k.Code == tea.KeyF12 && k.Mod == 0:
		event.Command = editor.Block
	case k.Code == tea.KeyF10 && k.Mod == tea.ModAlt:
		event.Command = editor.Macro
	case k.Code == tea.KeyF3 && k.Mod == tea.ModShift:
		event.Command = editor.SwitchDocument
	case k.Code == tea.KeyF10 && k.Mod == tea.ModShift:
		event.Command = editor.Retrieve
	case k.Code == tea.KeyF3 && k.Mod == tea.ModAlt:
		event.Command = editor.Reveal
	case k.Code == tea.KeyF8 && k.Mod == tea.ModShift && mode == editor.Editing:
		event.Command = editor.ProtectBlock
	case k.Code == tea.KeyF4 && k.Mod == tea.ModAlt:
		event.Command = editor.Block
	case k.Code == tea.KeyF4 && k.Mod == tea.ModShift && mode == editor.Editing:
		event.Command = editor.DoubleIndent
	case k.Code == tea.KeyTab && k.Mod == tea.ModShift && mode == editor.Editing:
		event.Command = editor.MarginRelease
	case k.Code == tea.KeyF6 && k.Mod == tea.ModShift && mode == editor.Editing:
		event.Command = editor.AlignCenter
	case k.Code == tea.KeyF6 && k.Mod == tea.ModCtrl && mode == editor.Editing:
		event.Command = editor.AlignDecimal
	case k.Code == tea.KeyF6 && k.Mod == tea.ModAlt && mode == editor.Editing:
		event.Command = editor.AlignRight
	case k.Code == tea.KeyF4 && k.Mod == tea.ModCtrl && mode == editor.Editing:
		event.Command = editor.MoveMenu
	case k.Code == tea.KeyLeft && k.Mod == tea.ModCtrl && (mode == editor.Editing || mode == editor.CopyTargetMode):
		event.Command = editor.WordLeft
	case k.Code == tea.KeyRight && k.Mod == tea.ModCtrl && (mode == editor.Editing || mode == editor.CopyTargetMode):
		event.Command = editor.WordRight
	case (k.Code == tea.KeyDelete || k.Code == tea.KeyBackspace) && k.Mod == tea.ModCtrl && mode == editor.Editing:
		event.Command = editor.DeleteWord
	case k.Code == tea.KeyEnd && k.Mod == tea.ModCtrl && mode == editor.Editing:
		event.Command = editor.DeleteToLineEnd
	case k.Code == tea.KeyPgDown && k.Mod == tea.ModCtrl && mode == editor.Editing:
		event.Command = editor.DeletePageRemainder
	case k.Code == tea.KeyHome && k.Mod == tea.ModCtrl && mode == editor.Editing:
		event.Command = editor.GoTo
	case k.Mod != 0:
		return event, false
	default:
		switch k.Code {
		case tea.KeyF4:
			event.Command = editor.Indent
		case tea.KeyF2:
			event.Command = editor.SearchF2
		case tea.KeyF8:
			event.Command = editor.Underline
		case tea.KeyF9:
			event.Command = editor.MergeF9
		case tea.KeyTab:
			event.Command = editor.Tab
		case tea.KeyPgUp:
			event.Command = editor.PageUp
		case tea.KeyPgDown:
			event.Command = editor.PageDown
		case tea.KeyF10:
			event.Command = editor.Save
		case tea.KeyF1:
			event.Command = editor.F1
		case tea.KeyF7:
			event.Command = editor.F7
		case tea.KeyEscape:
			event.Command = editor.Escape
		case tea.KeyHome:
			event.Command = editor.Home
		case tea.KeyEnd:
			event.Command = editor.End
		case tea.KeyDown:
			event.Command = editor.Down
		case tea.KeyUp:
			event.Command = editor.Up
		case tea.KeyRight:
			event.Command = editor.Right
		case tea.KeyLeft:
			event.Command = editor.Left
		case tea.KeyBackspace:
			event.Command = editor.Backspace
		case tea.KeyDelete:
			event.Command = editor.Delete
		case tea.KeyInsert:
			event.Command = editor.Insert
		case tea.KeyEnter:
			event.Command = editor.Enter
		default:
			return event, false
		}
	}
	return event, true
}

// panes uses only bounded authoritative document projections. It never interprets native bytes,
// wraps original pages, computes printed positions or serializes view text.
func (m Model) panes() (normal, reveal string, x int, err error) {
	f := m.visibleFrame()
	return f.normal, f.reveal, f.x, f.err
}
func (m Model) legacyPanes() (normal, reveal string, x, y int, err error) {
	d := m.session.Document()
	if d == nil {
		return "", "", 0, 0, nil
	}
	s := m.session.Snapshot()
	gap := s.Gap
	if gap > document.MaxWindowTokens {
		return "", "", 0, 0, fmt.Errorf("cursor beyond bounded %d-token presentation", document.MaxWindowTokens)
	}
	count := min(d.TokenCount(), document.MaxWindowTokens)
	p, err := m.session.Present(0, count)
	if err != nil {
		return "", "", 0, 0, err
	}
	elements := p.Elements
	blockStart, blockEnd := -1, -1
	if s.Selection {
		blockStart, blockEnd = s.SelectionStart, s.SelectionEnd
	}
	if s.Mode == editor.HistoryPreview {
		info, e := m.session.Preview(0, 0)
		if e != nil {
			return "", "", 0, 0, e
		}
		if info.TotalTokens > document.MaxWindowTokens {
			return "", "", 0, 0, fmt.Errorf("preview exceeds bounded %d-token presentation", document.MaxWindowTokens)
		}
		overlay, e := m.session.Preview(0, info.TotalTokens)
		if e != nil {
			return "", "", 0, 0, e
		}
		elements = make([]document.Element, len(overlay.Elements))
		for i, v := range overlay.Elements {
			elements[i] = document.Element{TokenIndex: i, Kind: v.Kind, Text: v.Text}
		}
		blockStart, blockEnd = overlay.FragmentStart, overlay.FragmentEnd
	}
	var n strings.Builder
	var lower []revealRun
	nativeActive := !s.Selection && s.Mode != editor.HistoryPreview
	nx, rx := 0, 0
	for i := 0; i <= len(elements); i++ {
		if i == blockStart {
			n.WriteString("[Block]")
			lower = append(lower, revealRun{text: "[Block]", role: revealBase})
			if i < gap {
				nx += 7
				rx += 7
			}
		}
		if i == blockEnd {
			n.WriteString("[Block]")
			lower = append(lower, revealRun{text: "[Block]", role: revealBase})
			if i < gap {
				nx += 7
				rx += 7
			}
		}
		if i == len(elements) {
			break
		}
		e := elements[i]
		rt := e.Text
		switch e.Kind {
		case document.BoldOn:
			n.WriteString("\x1b[1m")
			rt = "[BOLD]"
		case document.BoldOff:
			n.WriteString("\x1b[22m")
			rt = "[bold]"
		case document.ASCII, document.ExtendedCharacter, document.HardSpace, document.DOSControl:
			n.WriteString(e.Text)
			if e.Kind == document.HardSpace {
				rt = "[ ]"
			}
			if i < gap {
				nx += utf8.RuneCountInString(e.Text)
			}
		case document.HardReturn:
			n.WriteByte('\n')
			rt = "[HRt]"
			if i < gap {
				nx = 0
				y++
			}
		default:
			return "", "", 0, 0, fmt.Errorf("unsupported token presentation")
		}
		role := revealBase
		if e.Kind == document.BoldOn || e.Kind == document.BoldOff || e.Kind == document.HardReturn {
			role = revealCode
		}
		// Overlay elements deliberately have no native span. Only an element
		// returned by the authoritative native Present can own active cells.
		if nativeActive && e.TokenIndex == p.CursorGap && e.Span.Length > 0 {
			role = revealActive
			if e.Kind == document.ExtendedCharacter {
				token, err := d.Token(e.TokenIndex)
				if err == nil {
					rt = token.RevealCharacter()
				}
			}
		}
		lower = append(lower, revealRun{text: rt, role: role})
		if i < gap {
			rx += utf8.RuneCountInString(rt)
		}
	}
	if nativeActive && p.CursorGap == d.TokenCount() {
		lower = append(lower, revealRun{text: " ", role: revealActive})
	}
	// Terminal cell scrolling is view-only, never original pagination or Pos.
	ns, rs := max(0, nx-max(1, m.width/2)), max(0, rx-max(1, m.width/2))
	x = nx - ns
	normalLines := strings.Split(n.String()+"\x1b[0m", "\n")
	normalLines[y] = ansi.TruncateLeft(normalLines[y], ns, "")
	return strings.Join(normalLines, "\n"), renderReveal(lower, rs, m.width), x, y, nil
}
func clip(s string, width int) string {
	out := ansi.Truncate(s, width, "")
	if strings.Contains(s, "\x1b[") {
		out += "\x1b[0m"
	}
	return out
}
func (m Model) View() tea.View {
	view := m.renderView()
	if m.recording.stage != 0 {
		view = m.macroRecordingView(view)
	}
	if m.sheet.stage != 0 {
		view = m.spreadsheetView(view)
	}
	if m.appearance != 0 {
		view = m.appearanceView(view)
	}
	if m.sort.stage != 0 {
		view = m.sortView(view)
	}
	if m.dateMenu {
		view = m.dateView(view)
	}
	if m.screenMenu {
		view = m.screenView(view)
	}
	if m.contents.stage != 0 {
		view = m.contentsView(view)
	}
	if m.runtime != nil && m.runtime.aubergine {
		return applyAubergine(view)
	}
	return view
}

func (m Model) renderView() tea.View {
	if m.styles.stage != 0 {
		return m.styleView()
	}
	if m.comment.stage != commentClosed {
		return m.commentView()
	}
	if m.note.stage != 0 {
		return m.noteView()
	}
	if m.lineFormat.screen != formatClosed {
		return m.lineFormatView()
	}
	if m.summary.open {
		return m.summaryView()
	}
	if len(m.recovery.entries) > 0 {
		return m.recoveryView()
	}
	if m.print.screen != printClosed && m.print.screen != printListedPages {
		return m.printViewScreen()
	}
	if m.runtime != nil && m.runtime.editorChrome && !m.showEditorChrome() && (m.historic.menu || m.historic.files || m.historic.dosTextStage != 0) {
		label := "Menu active"
		if m.historic.files {
			label = "List Files active"
		}
		lines := []string{label, "Enlarge window to continue; Esc or F7 returns"}
		lines = lines[:min(len(lines), m.height)]
		for i := range lines {
			lines[i] = clip(lines[i], m.width)
		}
		v := tea.NewView(strings.Join(lines, "\n"))
		v.AltScreen = true
		applyEditorChrome(&v)
		v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
		return v
	}
	if m.runtime != nil && m.runtime.editorChrome {
		return m.historicView()
	}
	s := m.session.Snapshot()
	frame := m.visibleFrame()
	if frame.anchors {
		return m.anchorView(frame, s.Reveal)
	}
	normal, reveal, x, err := frame.normal, frame.reveal, frame.x, frame.err
	documentLines := strings.Split(normal, "\n")
	cursorRow := frame.y
	if visible := m.documentRows(s.Reveal); len(documentLines) > visible {
		start := min(max(0, cursorRow-visible+1), len(documentLines)-visible)
		documentLines = documentLines[start : start+visible]
		cursorRow -= start
	}
	lines := append([]string{"Wordling 5.2 | bounded native editing"}, documentLines...)
	if err != nil {
		lines[1] = "Unsupported document presentation: " + err.Error()
	}
	chrome := m.showEditorChrome()
	var revealLines []string
	if s.Reveal {
		banner := "Press Reveal Codes to restore screen"
		if frame.inspection.Partial {
			banner = "Partial Reveal inspection | HOST ?N = unsupported owner"
		}
		revealLines = append([]string{banner}, strings.Split(reveal, "\n")...)
		if !chrome {
			lines = append(lines, revealLines...)
		}
	}
	promptRow := len(lines)
	prompt := s.Prompt
	if s.HomePrefix > 0 && s.Mode == editor.Editing {
		prompt = "Home prefix: Home again for line/document movement, Esc cancels"
		if s.HomePrefix == 2 {
			prompt = "Home Home: Left line start | Up document start | Down document end"
		}
	}
	if m.characterRepeat.active {
		prompt = "Repeat Value = "
		if m.characterRepeat.count != 0 {
			prompt += string(rune('0' + m.characterRepeat.count))
		}
	} else if m.repeatEntry {
		prompt = "Repeat Value = "
	} else if s.Mode == editor.Editing && s.MacroRepeat == 3 {
		prompt = "Repeat Value = 3"
	}
	prompt = m.menuPrompt(s, prompt)
	lines = append(lines, prompt, s.Notice)
	if line := m.macroLine(); line != "" {
		lines = append(lines, line)
	}
	if s.Screen > 1 {
		lines = append(lines, fmt.Sprintf("Doc%d", s.Screen))
	}
	if line := firstStateLine(s); line != "" {
		lines = append(lines, line)
	}
	if s.Mode == editor.Waiting {
		lines = append(lines, "Filesystem operation pending")
	}
	if m.notice != "" {
		lines = append(lines, m.notice)
	}
	if m.reconcile != "" {
		lines = append(lines, m.reconcile)
	}
	history := "unknown"
	if s.HistoryCountKnown {
		history = fmt.Sprint(s.HistoryCount)
	}
	typing := ""
	if s.Typeover {
		typing = "Typeover "
	}
	profileLabel := "local-flat: ASCII basenames only; physical key delivery UNQUALIFIED"
	if m.runtime != nil && m.runtime.profile == MacroCOUT {
		profileLabel = "macro-cout: exact C:\\OUT\\ and flat names; physical key delivery UNQUALIFIED"
	}
	if !chrome {
		lines = append(lines, fmt.Sprintf("%s | %s | gap %d | %s", s.Mode, s.Name, s.Gap, s.SaveState),
			fmt.Sprintf("%sDirty=%t Block=%t revision=%d history=%s qualified=%t", typing, s.Dirty, s.Selection, s.Revision, history, s.HistoryQualified), profileLabel)
		if m.runtime != nil && m.runtime.controlKeys {
			lines = append(lines, "Ctrl+B Bold | Ctrl+R Codes | Ctrl+S Save | Ctrl+O Open | Ctrl+Q Exit")
		}
	}
	if m.menuState().Visible {
		lines[0] = renderMenuBar()
	}
	if chrome {
		lines = m.editorChromeLines(lines, revealLines, s)
	}
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	if len(lines) > m.height {
		lines = lines[:m.height]
	}
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	if chrome {
		applyEditorChrome(&v)
	}
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	if (s.Mode == editor.Editing || s.Mode == editor.DeleteQuestion || s.Mode == editor.HistoryPreview || s.Mode == editor.Waiting) && err == nil && m.height > 1 {
		y := 1 + cursorRow
		if y < m.height {
			v.Cursor = tea.NewCursor(min(x, m.width-1), y)
		}
	}
	// Prompt caret refers to the original reducer draft, not document position.
	if (s.Mode == editor.RetrieveName || s.Mode == editor.SaveName || s.Mode == editor.MacroName) && len(lines) > 2 {
		prefix := "Document to be retrieved: "
		if s.Mode == editor.SaveName {
			prefix = "Document to be saved: "
		} else if s.Mode == editor.MacroName {
			prefix = "Macro: "
		}
		y := promptRow
		if y < m.height {
			v.Cursor = tea.NewCursor(min(len(prefix)+s.Caret, m.width-1), y)
		}
	}
	if m.characterRepeat.active && promptRow < m.height {
		v.Cursor = tea.NewCursor(min(len(prompt), m.width-1), promptRow)
	}
	if (m.repeatEntry || s.Mode == editor.Editing && s.MacroRepeat == 3) && promptRow < m.height {
		x := len("Repeat Value = ")
		if !m.repeatEntry {
			x++
		}
		v.Cursor = tea.NewCursor(min(x, m.width-1), promptRow)
	}
	return v
}

// anchorEligible observes existing source/UI owners. It grants no command or IO
// authority. The pristine menu uses its qualified legacy base on BOTH toggles.
func (m Model) anchorEligible(s editor.Snapshot, frame macroPane) bool {
	if m.showEditorChrome() || (m.runtime != nil && m.runtime.controlKeys) || strings.Contains(frame.normal, "\n") || m.width != 80 || m.height != 25 || m.runtime == nil || frame.err != nil || frame.inspection.Partial ||
		s.Mode != editor.Editing || s.Selection || s.Typeover || !s.HistoryCountKnown || s.Screen != 1 || s.MacroRepeat != 1 ||
		m.characterRepeat.active || s.Pending != nil || s.Prompt != "" || s.Notice != "" || m.repeatEntry || m.notice != "" || m.reconcile != "" ||
		len(m.unsettled) != 0 || m.firstPending != nil || m.macro != nil || m.macroTicket != nil || m.macroCPU ||
		m.macroDeferred != nil || m.macroStatus.Active || m.macroStatus.WorkerPending || m.macroStatus.DisplaySuppressed ||
		s.NewPhase == editor.PublishedUnbound || s.NewPhase == editor.PublicationUncertain ||
		m.menuReason() == "" || m.menu.diagnostic != "" {
		return false
	}
	m.runtime.mu.Lock()
	defer m.runtime.mu.Unlock()
	return !m.runtime.stopping && m.runtime.macro == nil && m.uiAuthority != nil && m.uiAuthority == m.runtime.uiAuthority
}

// A fixed bounded display composition, not original page/ruler/status layout.
// Frozen frames retain this choice even when later live state/size is different.
func (m Model) anchorView(frame macroPane, reveal bool) tea.View {
	lines := make([]string, 25)
	lines[0] = revealBase + frame.normal
	if reveal {
		lines[13] = frame.reveal
		lines[24] = renderReveal([]revealRun{
			{text: "Press ", role: revealBase},
			{text: "Reveal Codes", role: revealCode},
			{text: " to restore screen" + strings.Repeat(" ", 44), role: revealBase},
		}, 0, 80)
	}
	for i := range lines {
		lines[i] = clip(lines[i], m.width)
	}
	lines = lines[:min(len(lines), m.height)]
	v := tea.NewView(strings.Join(lines, "\n"))
	v.AltScreen = true
	v.KeyboardEnhancements = tea.KeyboardEnhancements{ReportEventTypes: true, ReportAlternateKeys: true, ReportAllKeysAsEscapeCodes: true, ReportAssociatedText: true}
	v.Cursor = tea.NewCursor(min(frame.x, m.width-1), 0)
	return v
}
