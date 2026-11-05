# WP11 classic session and terminal interaction contract

Research handoff,2026-10-30. Requirements FR-004/005 and C-001; file/save FC
rules remain binding. Authority: mission spec/plan/research/data-model,
compatibility/roadmap and approved WP01/04/06 contracts. This is a bounded
session/input proposal, not an editor or terminal support claim. Full classic
interaction remains M1; PDF remains M2. WP12 owns executable continuation WPs.
No code, canonical registry, queue, resource or raw evidence is changed.

## Identity and evidence boundary

Original reference remains plain U.S. English DOS WP5.1, Help03/09/92 under the
fingerprinted QEMU/FreeDOS1.4/July1992 Standard Printer profile. Original keyboard
is selected. This establishes bounded DOS command observations, not Linux
terminal input delivery, graphics layout or another keyboard/edition. WP04
editing and WP06 file/storage contracts are binding; WP07 layout/font limits
and WP10 native character identity remain separate from screen rendering.

REF51 is the pinned6/92 reference, not automatically March behavior. Printed/PDF
pages are distinct; PDF numbers are **one-based**, printed Arabic+17. Main
locators: cursor103–104/PDF120–121; Reveal Codes560–562/PDF577–579;
Retrieve554–557/PDF571–574; Save565–566/PDF582–583; Exit194–196/PDF211–213;
Cancel55/PDF72; Repeat550–551/PDF567–568. Sources and transcripts are sealed by
the ledger. Macro/merge incidental navigation does not promote a dedicated case.
All implementation fields remain not-implemented; observed means only these
bounded original recipes. Unrun transitions below remain unrun.

## Observed original session fragments (T031)

The following are fragments from separate fresh-copy runs, **not one executed
retrieve-to-exit workflow**. Exact prompts/cursor/status cues are audited against
captures; each transition also matches the archived trace. O8 uses runner-awaited
prompt substrings plus captured DOS return, not invented full intermediate
prompts. Canonical/repetition run IDs and paths are in the ledger.

| State | Canonical case and feature | From → event → to | Captured cues | Exact boundary and limitation |
| --- | --- | --- | --- | --- |
| O1 | CMD51-066 (Name a new document with F10); WP51-020 | editing unnamed → F10 → save filename | `Document to be saved:`; `WORDLING TEST` | The observed blank filename prompt belongs to a new original document. No dirty/cursor snapshot beyond the capture is inferred. |
| O2 | CMD51-066 (Name a new document with F10); WP51-020 | save filename → type C:\OUT\NEWTEST, Enter → editing named | `C:\OUT\NEWTEST`; `WORDLING TEST`; `Pos 2.3"` | Native NEWTEST saved; editing resumes. Prompt disappearance alone does not prove disk completion; later extraction/normal exit seals bytes. |
| O3 | CMD51-067 (Decline overwriting an existing file); WP51-020 | editing changed ORIGINALMODIFIED → F10, Enter displayed SAME → replace question | `Replace C:\OUT\SAME? No (Yes)`; `ORIGINALMODIFIED` | The exact captured replacement question is for SAME. Guest COPY had prepared BEFORE; it is incidental DOS setup, not full Shell acceptance. |
| O4 | CMD51-067 (Decline overwriting an existing file); WP51-020 | replace question → n → save filename with SAME retained | `Document to be saved: C:\OUT\SAME`; `ORIGINALMODIFIED` | Refusal requests another filename. Disk SAME equals BEFORE and retains ORIGINAL; no success state or overwrite occurs. |
| O5 | CMD51-067 (Decline overwriting an existing file); WP51-020 | save filename after refusal → F1 → editing changed buffer | `ORIGINALMODIFIED`; `C:\OUT\SAME`; `Pos 2.6"` | F1 here preserves changed in-memory content; it does not establish F1 at Retrieve, Exit, replacement question or every dialog. |
| O6 | CMD51-048 (Toggle Reveal Codes without editing); WP51-013 | normal editing at end → Alt+F3 → Reveal Codes visible | `[BOLD]alpha[bold]beta`; `Press Reveal Codes to restore screen`; `Pos 1.9"` | Normal text remains alphabeta; code-pane labels describe original formatting. There is no before/after native export for this recipe. |
| O7 | CMD51-048 (Toggle Reveal Codes without editing); WP51-013 | Reveal Codes visible → Alt+F3 → normal editing same end position | `alphabeta`; `Pos 1.9"` | Visible text and status position retained; exact no-edit native preservation is a future FC-002 requirement, not observed original save identity. |
| O8 | CMD51-067 (Decline overwriting an existing file); WP51-020 | editing changed buffer → F7, n, y → DOS prompt after exit | `C:\WP51>` | Archived clean_exit awaits Save document? then Exit WP?; intermediate full prompt choices are not separately captured. This is clean exit, not cancel-exit087. |
| O9 | CMD51-005 (Repeat a character a declared number of times); WP51-007 | normal editing → Esc,5,x → repeat consumed after insertion | `xxxxx` | Five x characters observed. Escape is not a global Cancel binding; menu/prompt Escape alternatives remain documentary. |
| O10 | CMD51-001 (Open and close pull-down menus); WP51-001 | menus hidden → Alt+= twice → menus shown then hidden | `Doc 1 Pg 1`; `Pos 1"` | Manifest checks appearance/disappearance and retained visible position; submenu navigation/cancellation002 remains unrun. |

The early smoke02 manifest predates runner-source archiving; smoke03 seals the
archived source used as the canonical recipe. Both seal the selected capture
bytes. The audit checks runner archives where recorded; it does not invent a
missing archive for the older repetition.

O3–O5 leave the disk SAME/BEFORE native images byte-identical with body ORIGINAL;
the screen has ORIGINALMODIFIED. O5 does not save or revert the in-memory edit.
O6/O7 use end-of-document Pos1.9 in that recipe; they do not establish cursor
preservation at every code gap. Native before/after exports do not exist for that
Reveal-only recipe. WP04 retains original deletion/Undelete/paired-code semantics;
no visual-only code list or independent duplicate document model is permitted.

### Documentary and unrun transitions

Exact prompt strings not captured are marked unknown, rather than invented from
modern editors. Canonical case status/title/feature links are audited below.

| Gap | Canonical case and feature | Proposed transition and event | Evidence boundary | Required original follow-up |
| --- | --- | --- | --- | --- |
| G1 | CMD51-065 (Retrieve inserts at the cursor); WP51-019 | blank editing → retrieve filename → retrieved editing; Shift+F10, enter owned fixture, Enter | REF554–556/PDF571–573 asks for filename and inserts retrieved text at cursor; cursor after initial codes. Exact prompt string/default-name/editor/cancel states are not captured. | Probe blank retrieval of the pinned ORIGIN fixture, missing path and F1/Esc separately; native input preserved. Existing-buffer insertion and initial-code interactions need later variants. |
| G2 | CMD51-019 (Go to start after initial codes); WP51-008 | editing → after initial codes at beginning; Home,Home,Up | Manual cursor destination; dedicated case not-run. | Compare token-gap position in both views without mutation; distinguish G3. |
| G3 | CMD51-020 (Go to start before initial codes); WP51-008 | editing → before initial codes at beginning; Home,Home,Home,Up | This sequence occurs incidentally in other archived editing recipes; that is not full dedicated case observation. | Capture before/after independently on retrieved formatted fixture, both views and prefix-sequence reset/cancel. |
| G4 | CMD51-049 (Traverse a code while visible text cursor appears stationary); WP51-008, WP51-013 | code gap → next code gap with stationary visible text cursor; Right | Manual requirement, dedicated case not-run. WP04 observed code-target setup is bounded evidence, not general cursor equivalence. | Use before/after Bold On and Off gaps in saved ORIGIN; record pane focus, token position, normal cursor and bytes. |
| G5 | CMD51-068 (Approve overwriting an existing file); WP51-020 | replace question → successful replacement; y | Canonical successful overwrite unrun; WP03 storage foundation refuses actual replacement. | Keep replacement refusal explicit until original backup/Fast Save/failure transaction and writer contracts are accepted. |
| G6 | CMD51-069 (Edit the displayed save filename); WP51-020 | save filename → edited existing name; Left/Right/Backspace then Enter | Documentary filename editing differs first-character replacement; exact state/cursor branches unrun. | Probe prefilled old name, edit keys/typeover/cancel and compare native destination/source effects. |
| G7 | CMD51-070 (Typing a save filename starts a new name); WP51-020 | save filename → fresh typed filename; character first then Enter | Documentary first character clears displayed name; not-run. | Needed before naming a new destination after Retrieve; do not assume generic text-input append semantics. |
| G8 | CMD51-087 (Exit without saving and cancel application exit); WP51-029 | exit save question → exit confirmation → editing/session; F7,n,n | Dedicated cancel-application-exit case not-run. Incidental clear_doc1 calls F7,n,n in merge setup; no dedicated buffer-state audit. F7,n,y clean exit does not prove this branch. | Probe named/unnamed and saved/changed buffers, capture both prompts and resulting buffer/filename/dirty state. F1 at each prompt is a separate documentary branch requiring case expansion. |
| G9 | CMD51-002 (Back one menu level versus leave menus); WP51-001, WP51-007 | submenu → parent versus leave all menus; F1 versus F7 | Manual distinction unrun; Escape alternate Cancel is documentary and context-dependent. | Capture exact submenu/cancel depth, original letter/navigation choices and return context; no generic menu engine guesses. |
| G10 | CMD51-149 (Preserve an untouched native file byte for byte); WP51-020 | retrieved no-edit image → same exact native image saved; F10 workflow plus bounded storage outcome | FC-002 is a Wordling guarantee, canonical comparison not-run. Original WP may format/alter metadata. | Use exact native length/hash/bytes under accepted storage boundary; original reopen separately. Do not label original-app new-document save as Wordling no-edit acceptance. |

Generic single-character Left/Right cases remain unrun; use original token-gap
positions, never byte offsets inside a code or terminal-cell coordinates as
semantic cursor identity. Their exact canonical titles and status are pinned in
the case ledger. Incidental Home/Right setup before deletion proves only its
captured source positions. Cursor navigation before/after initial codes, across
paired codes and in normal/Reveal panes must be tested independently before
claiming the bounded retrieval session accepted.

F1 is contextual: normal editing's original Undelete differs from filename or
menu cancellation. Esc in normal editing invokes Repeat Value (O9). REF550/PDF567
also documents Esc as alternate Cancel in menus/prompts; those branches remain
documentary/unrun. Therefore neither global Esc=Cancel nor global Esc=Repeat is
correct. F7 normal editing, menu exit and application/document exit decisions
likewise route through current context. F7,n,y clean exit must never become proof
of F7,n,n or F1 during exit. The generic q/Ctrl+Q/Ctrl+S/Esc bindings common in
example TUIs are not selected as original commands.

## First bounded composed session proposal

**SESSION1 is unrun end-to-end.** Its starting file is existing project-authored
`ORIGIN.WP5` from advanced04/CMD51-204 (exact path/hash/body in ledger):
`A[BOLD]BC[bold]D`. It was authored/saved in original WP for another editing
recipe; it is not evidence of this retrieval path. No new fixture is created.

Start a blank original document, Retrieve this file using a declared DOS scratch
path, and capture actual filename prompt, accepted path/default, missing-file
branch and resulting cursor/initial settings. Toggle Reveal Codes, use exact
Home-prefix then Right movements before/after each paired-code token, and toggle
back. Do not edit the semantic document in this first session. F10 should exercise
original filename behavior, new-name publication and refusal/cancel decisions
using fresh scratch files; prefilled names and character-first replacement require
G6/G7 evidence. Capture full intermediate Save/Exit prompts, then F1 cancel at
each specified point and the separate F7,n,n versus F7,n,y branches. Record
whether buffer/name/cursor/dirty state is retained or cleared rather than assuming
all exit cancellations restore the changed buffer.

Before implementation acceptance, repeat SESSION1 from two fresh copies with
input/output/native/capture hashes and exact command state after each step.
This probes original workflow, not a no-edit byte-identity claim about original
WP saves. Wordling's no-edit snapshot must remain exact under FC-002. The first
Wordling storage integration may use approved snapshot acquisition, same-file
no-op and absent-destination publication only; actual overwrite remains refused
by the bounded foundation. A safe refusal is not original Save/overwrite parity.
New-document/semantic writer, backup/Fast Save and failure/uncertain publication
states stay under WP06; the session cannot report generic successful save for
an unsupported replacement, failed write or uncertain destination.

### Proposed session model boundary

Keep semantic document and one token-gap cursor authoritative for normal and
Reveal views. A session owns active document/window, view visibility/focus,
original command context, pending Home/repeat prefixes, selection/Undelete context,
filename draft/caret and original name, pending save/exit decision and filesystem
operation outcome. Retain previous context on prompt entry; restore only what the
specific original branch establishes. Rendered prompt text and enabled choices
come from tested command states, not generic editor menus. Dirty state is a
semantic/saved-revision relation, distinct from prompt drafts or pane toggles;
its exact original exit behavior still needs the dedicated probe.

Session emits bounded domain/storage operations and consumes typed success,
refusal, failure or uncertainty results. A pending IO state cannot accept a late
result for another document/revision or turn cancelled work into a false success.
Actual cancellation/IO ordering is an implementation safety contract requiring
tests, not a claim about original DOS asynchrony. Filename/DOS-to-Linux mapping
must follow WP06. Display strings/status inches do not define layout geometry.

## Pinned Bubble Tea capability check (T032)

Actual go.mod pin is **charm.land/bubbletea/v2 v2.1.1**, with
`github.com/charmbracelet/ultraviolet` at
`v0.0.0-20261008173134-6b8d4baf91b4`. The cached v1 Bubble Tea API is not this
project's pin. This read-only check used the actual cached v2/UV sources and
go.mod/go.sum; no dependency or code was changed and no library/runtime test is
claimed. Paths/hashes/line anchors below are reproducible through GOMODCACHE;
this host's absolute cache paths are in the ledger.

| Pinned source anchor | Capability established by source | Remaining verification |
| --- | --- | --- |
| `v2@v2.1.1/key.go:302` | Typed Code/Mod/Text and optional enhanced fields | Physical terminal bytes/events and command delivery remain unrun. |
| `v2@v2.1.1/keyboard.go:9` | Negotiated flags and Supports methods, not guaranteed terminal support | Physical terminal bytes/events and command delivery remain unrun. |
| `v2@v2.1.1/tea.go:255` | Enhancement requests including repeats/alternate codes/all keys | Physical terminal bytes/events and command delivery remain unrun. |
| `v2@v2.1.1/input.go:8` | Key/paste/mouse/resize/capability translation | Physical terminal bytes/events and command delivery remain unrun. |
| `v2@v2.1.1/paste.go:5` | Paste carries text separately from key commands | Physical terminal bytes/events and command delivery remain unrun. |
| `v2@v2.1.1/screen.go:7` | Resize event contains dimensions | Physical terminal bytes/events and command delivery remain unrun. |
| `ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/decoder.go:234` | Legacy ESC and Alt-prefix parsing; Kitty parser elsewhere in same file | Physical terminal bytes/events and command delivery remain unrun. |
| `ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/key_table.go:554` | Legacy function-key terminfo mapping requires profile qualification | Physical terminal bytes/events and command delivery remain unrun. |
| `ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/terminal.go:233` | Buffered event timeout; no arbitrary Wordling timeout selected | Physical terminal bytes/events and command delivery remain unrun. |
| `v2@v2.1.1/tea.go:796` | OS interruption differs original Exit workflow | Physical terminal bytes/events and command delivery remain unrun. |

Use typed v2 KeyPressMsg fields Code/Mod/Text and the actual capability support
methods. Enhanced ShiftedCode/BaseCode/IsRepeat are conditional; a request is not
a supported response. Comments in tea.go show an older-looking example of flag
access; `keyboard.go` defines the actual Flags/Supports API. The adapter must
compile against the pinned source, not copy a v1 or comment-only example.
UV's legacy decoder exposes Ctrl+I/Tab, Ctrl+M/Enter, Ctrl+[/Esc, NUL combinations,
Backspace/Delete and high-F-key interpretation ambiguities. It parses ESC-prefixed
Alt and has buffered event timeouts; split/delayed bytes can matter. A parser's
recognition of a sequence proves nothing about whether a terminal/window manager
sends it. No arbitrary escape timeout is chosen as a Wordling requirement here.

### Candidate supported input profile and fallback decisions

This is a **proposed qualification target**, not a currently supported terminal:
Linux local direct PTY, UTF-8 locale, US keyboard selected, recorded terminal
binary/version/config/TERM/terminfo, enhanced keyboard negotiation with actual
response captured, no multiplexer/SSH/input remapper in the first profile, and
no desktop shortcuts consuming required chords. Start with a recorded80x25
viewport to compare original session state, then test resize; that viewport is a
test input, not document page dimensions or a new minimum product requirement.
Terminal brand alone does not qualify the profile. No captured Linux key delivery
exists in this research package.

| Ambiguity / event | Proposed decision preserving original command | Evidence needed before support claim |
| --- | --- | --- |
| Modified function keys | Require distinct original F1/F3/F7/F10, Alt+F3, Shift+F10 plus all later required combinations; qualify exact Code/Mod pairs. Do not silently interpret F13 or desktop shortcuts as a different original key. | Raw bytes and v2 decoded events for each physical chord, plus state outcome; include terminfo/high-F configuration. |
| Esc / Alt / prefixes | Emit original Escape or Alt chord, then let session context implement normal Repeat versus documentary prompt Cancel. Never synthesize Alt by consuming a standalone original Esc sequence in application logic. | Single Esc, Esc5x, Alt+=, Alt+F3, Esc followed rapidly/slowly by plain text and split packets; capability+timeout settings recorded. |
| Ctrl collisions / Backspace | Prefer negotiated disambiguation. When bytes alias distinct original keys, mark the missing distinction explicitly; terminal configuration may emit distinct sequences only after capture qualification. | Ctrl+I/Tab, Ctrl+M/Enter, Ctrl+[/Esc, Ctrl+Space/Ctrl+@ and Backspace/Delete, modified Enter/arrows/Home tested separately. |
| Legacy profile fallback | Publish an explicit narrower delivery matrix. First adjust terminal/desktop configuration for original chords; a documented original menu route may invoke the same command only after its own navigation probe. No invented command palette or silent replacement shortcut. | Qualify original File/Retrieve and other actual menu routes from WP05/REF; menus themselves are still unrun beyond O10. Missing keys remain open M1 work. |
| Text / paste / IME | Separate printable text from commands and native WP identities; preserve WP10 conversion/error rules. Bracketed PasteMsg is text, never replayed as function-key/escape commands. Paste behavior is an unqualified adaptation requiring its own contract. | Byte/event/text captures, pasted control/escape-looking content, Unicode/IME normalization tests and unsupported-character behavior before native mutation. |
| Key repeats / releases | Route presses once; don't execute release as another command. Preserve actual repeat events while keeping original Esc Repeat Value state separate from OS autorepeat. | Press/hold/release logs and capability flags; physical repeat rates are not invented original semantics. |
| Resize / mouse / focus | Resize changes viewport/pane presentation only; keep document/cursor/command state. Mouse and focus events must not become accidental editing commands. | WindowSizeMsg resize traces, original mouse selection/prompt comparison and focus/resume tests; none are qualified by source presence. |
| Signals / terminal loss | Treat OS SIGINT/SIGTERM/PTY failure as abnormal host lifecycle, distinct from original F7 exit. Do not advertise successful save or replace original quit keys with generic TUI shortcuts. | Pinned library cleanup/error behavior plus source-integrity and restored-terminal tests; crash durability/backup claims require WP06 work. |

Any alternative physical binding must be explicit, reversible and map to the same
original command/state; it needs adaptation evidence before support. A proposal
to remove original commands/graphics/mouse or change parity baseline requires an
owner decision recorded in git; none is requested or implied by this contract.
Unavailable keys do not silently shrink M1. Original keyboard layouts/remapping
WP51-003 and setup artifacts remain independent original features.

## Bounded continuation packages for WP12 (T033)

1. **Original SESSION1 probes:** close G1–G4/G6–G9 prompt and cursor branches with
   exact source fixture/settings/trace/captures and native outputs. Add/expand
   canonical cases for F1/Esc during exit/retrieve and original menu routes before
   treating them as acceptance. No new oracle run was done here.
2. **Typed input adapter and qualification harness:** pin v2 APIs above, record
   raw/decoded events and capability/profile identity without changing document
   bytes. Test fragmented/unknown/legacy/enhanced sequences, modifiers, paste,
   repeats/releases and reconnect/resize/capability changes. No terminal support
   label from synthetic event injection alone; actual physical delivery needed.
3. **Pure session reducer:** original command IDs/context, prompt/name/prefix
   state and transitions, independent of Bubble Tea views/storage implementation.
   Test O1–O10 exact prompt/cancel behavior in their supported contexts and new
   original G evidence; separately test unsupported states explicitly refuse
   rather than fabricate behavior. Same key in different contexts must resolve
   correctly; preserve native document/selection/cursor where required.
4. **Bounded Bubble Tea view and storage composition:** present the normal/Reveal
   panes and exact prompt/status states from the reducer, using a shared document
   model; no layout or native serialization inside View. Integrate approved
   snapshot storage with explicit pending/error/uncertain states and revision
   identity. Test byte-identical no-edit output and refused replacement separately
   from UI success/cancel states. Unsupported semantic writer stays explicit.
5. **Full classic interaction closure:** retain WP51-001 menus/status/functions,
   WP51-002 Help, WP51-003 keyboard maps, WP51-004 mouse, WP51-005 display,
   WP51-006 both documents/windows, WP51-007 Cancel/Repeat, WP51-008 complete
   cursor/GoTo and WP51-013 shared Reveal Codes editing; WP04 retains all remaining
   selection/delete/history/search/edit scope. File/list/exit/backup/conversion
   remains WP06. Graphics preview/printed layout stays M1 under WP07/08. The
   bounded session is a milestone, not full FR-004/005 or mission acceptance.

Validation must distinguish domain state tests, actual terminal input captures,
original command/session comparison and native preservation. No gold-plating
framework or dependency update is needed for these slices. No original prompt
literal, cancel branch, platform alias or code effect may be filled in merely
because it looks like a common modern editor.

## Reproducible evidence and source audit

The ledger contains only references/metadata, not proprietary programs/resources.
All selected capture and native bytes are existing immutable evidence. Cache
sources can be reacquired at the exact go.mod/go.sum module versions; replace
the absolute GOMODCACHE prefix only when validating on another host.

<!-- WP11_AUDIT_BEGIN -->
```json
{
"source_inputs": [
{"path": "go.mod", "sha256": "e3a752a3bb2a1bba71756f3d4fc74aef55e81e966746024aebdccc58cb5252b9"},
{"path": "go.sum", "sha256": "0d8ff3e7199749776a57c6dae8dabaadea99f17ccabd292dbd17cc2180a4358a"},
{"path": "docs/research/sources.json", "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"},
{"path": "docs/research/feature-inventory.json", "sha256": "49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"},
{"path": "docs/research/command-scenarios.json", "sha256": "a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"},
{"path": "docs/research/reference-baseline.json", "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"},
{"path": "docs/research/reference-environment/environment.json", "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"},
{"path": "docs/research/reference-environment/resource-profile.json", "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"},
{"path": "research/cache/WPDOS51Reference.pdf", "sha256": "ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531"},
{"path": "research/cache/reference.txt", "sha256": "f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md", "sha256": "6ff65887643570f264d4e71b362ae302eee1216ddd870b8febbd667b93a7e496"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json", "sha256": "f0f4c945ec6551b5eeff68dd2c4ee108f98633a9979bdbfff6eda2854436e2bd"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/editing.md", "sha256": "7f542edd647b8735575036b0be570a88b048c5ea97755f25dbddadf92ce3a4bd"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md", "sha256": "dee9951828b2176e0714e0434d8774e7d0e0d7f4cc591b797c29954be7ed63bb"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/layout-resources.md", "sha256": "aa6384662a74c1c0451a506bd9fdd169420614c558677a40715fbe0bab906631"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md", "sha256": "e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/automation.md", "sha256": "2529b6218b36fccba2c143c8158017ae853d10e8fe3d7afc1958d6407d50e6f6"},
{"path": "kitty-specs/wp51-parity-01M64CVY/contracts/language-data.md", "sha256": "ac75a7cc2840f863a7b2fe2af62b95f0a06caedfed271bd3e644aa21182f8a63"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/key.go", "sha256": "a8c6782b7109923371147c6d7fe528bb5fbe59f85c34f7637b6c8f5a70408742"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/keyboard.go", "sha256": "47431fcb753e78b9934af16f0e7bfddbb9e70053863977d4daf08f3acc54f4ea"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/tea.go", "sha256": "cdb78b79fb98cd28d97e691cd6879766ab5dcefdb3c33f347c5b39f24a112c18"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/input.go", "sha256": "29d670f3e9f050d8b93c7e49a0a913b448073b045c05ad726ec0a53094fda478"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/paste.go", "sha256": "cb91e047eb26da00f1632c9b3d208313a1fce4baba67c8356ea015cd47d4f7c9"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/screen.go", "sha256": "24ce3a14d7f8c4c5150d8e8a2d8949e01b8ad4fa05f855038fa9e94496a0edc5"},
{"path": "/home/lynn/go/pkg/mod/github.com/charmbracelet/ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/decoder.go", "sha256": "6a4f2106ddc551c10471922e515cdc36b55d6c43bb2625623523ccd4e8895e52"},
{"path": "/home/lynn/go/pkg/mod/github.com/charmbracelet/ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/key_table.go", "sha256": "d25985e55012ae1334b0c968f4d71d4f3f88cfbf2771488abc09e93c5759e553"},
{"path": "/home/lynn/go/pkg/mod/github.com/charmbracelet/ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/terminal.go", "sha256": "d8633c31ff80262f922314175cb5aff745946ffa6f9e5e3eebc7abba4163e4db"},
{"path": "docs/research/reference-runs/2026-10-29-smoke-03/run.json", "sha256": "c4cae074cc75e651eff994e62cb0917d5645477c906a1f975738ea4ab62de4fe"},
{"path": "docs/research/reference-runs/2026-10-29-smoke-02/run.json", "sha256": "d361f81768a5ee9ea85d4590b013c53c2e68770af76ceaf91302b308281091d6"},
{"path": "docs/research/reference-runs/2026-10-29-extended-04/run.json", "sha256": "c7d98c6225892261dff38b88b3c9c044856ad43ad4e5776d4197089d885ac0fc"},
{"path": "docs/research/reference-runs/2026-10-29-extended-03/run.json", "sha256": "68450fd8efa5deea93e83021b043ad0a9ab1ada4867e5d5616c49fcf7c1d7809"},
{"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5", "sha256": "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d"},
{"path": "docs/research/reference-runs/2026-10-29-advanced-04/run.json", "sha256": "ae9bc9fda6091903b04c07b2894c487074a4c01edec656667b8a75da8dbbceb8"},
{"path": "docs/research/reference-runs/2026-10-29-advanced-03/run.json", "sha256": "6abdb82bb54d9cd1a3d0a6089977cdfa1086c5cc484f27cc067e176626b16610"}
],
"library_sources": [
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/key.go", "line": 302, "needle": "type Key struct {", "meaning": "Typed Code/Mod/Text and optional enhanced fields"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/keyboard.go", "line": 9, "needle": "type KeyboardEnhancementsMsg struct {", "meaning": "Negotiated flags and Supports methods, not guaranteed terminal support"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/tea.go", "line": 255, "needle": "type KeyboardEnhancements struct {", "meaning": "Enhancement requests including repeats/alternate codes/all keys"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/input.go", "line": 8, "needle": "func (p *Program) translateInputEvent", "meaning": "Key/paste/mouse/resize/capability translation"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/paste.go", "line": 5, "needle": "type PasteMsg struct {", "meaning": "Paste carries text separately from key commands"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/screen.go", "line": 7, "needle": "type WindowSizeMsg struct {", "meaning": "Resize event contains dimensions"},
{"path": "/home/lynn/go/pkg/mod/github.com/charmbracelet/ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/decoder.go", "line": 234, "needle": "func (p *EventDecoder) Decode", "meaning": "Legacy ESC and Alt-prefix parsing; Kitty parser elsewhere in same file"},
{"path": "/home/lynn/go/pkg/mod/github.com/charmbracelet/ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/key_table.go", "line": 554, "needle": "\"kf13\":", "meaning": "Legacy function-key terminfo mapping requires profile qualification"},
{"path": "/home/lynn/go/pkg/mod/github.com/charmbracelet/ultraviolet@v0.0.0-20261008173134-6b8d4baf91b4/terminal.go", "line": 233, "needle": "timer := time.NewTimer(t.opts.EventTimeout)", "meaning": "Buffered event timeout; no arbitrary Wordling timeout selected"},
{"path": "/home/lynn/go/pkg/mod/charm.land/bubbletea/v2@v2.1.1/tea.go", "line": 796, "needle": "case InterruptMsg:", "meaning": "OS interruption differs original Exit workflow"}
],
"case_links": [
{"id": "CMD51-001", "title": "Open and close pull-down menus", "feature_ids": ["WP51-001"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 10, "printed_end": 11, "pdf_start": 27, "pdf_end": 28}]},
{"id": "CMD51-002", "title": "Back one menu level versus leave menus", "feature_ids": ["WP51-001", "WP51-007"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 55, "printed_end": 56, "pdf_start": 72, "pdf_end": 73}]},
{"id": "CMD51-004", "title": "Space exits help", "feature_ids": ["WP51-002"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 275, "printed_end": 275, "pdf_start": 292, "pdf_end": 292}]},
{"id": "CMD51-005", "title": "Repeat a character a declared number of times", "feature_ids": ["WP51-007"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 550, "printed_end": 551, "pdf_start": 567, "pdf_end": 568}]},
{"id": "CMD51-011", "title": "Move one visible character left", "feature_ids": ["WP51-008"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 103, "printed_end": 104, "pdf_start": 120, "pdf_end": 121}]},
{"id": "CMD51-012", "title": "Move one visible character right", "feature_ids": ["WP51-008"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 103, "printed_end": 104, "pdf_start": 120, "pdf_end": 121}]},
{"id": "CMD51-019", "title": "Go to start after initial codes", "feature_ids": ["WP51-008"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 103, "printed_end": 104, "pdf_start": 120, "pdf_end": 121}]},
{"id": "CMD51-020", "title": "Go to start before initial codes", "feature_ids": ["WP51-008"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 103, "printed_end": 104, "pdf_start": 120, "pdf_end": 121}]},
{"id": "CMD51-048", "title": "Toggle Reveal Codes without editing", "feature_ids": ["WP51-013"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 560, "printed_end": 562, "pdf_start": 577, "pdf_end": 579}]},
{"id": "CMD51-049", "title": "Traverse a code while visible text cursor appears stationary", "feature_ids": ["WP51-008", "WP51-013"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 103, "printed_end": 104, "pdf_start": 120, "pdf_end": 121}, {"source_id": "REF51", "printed_start": 560, "printed_end": 562, "pdf_start": 577, "pdf_end": 579}]},
{"id": "CMD51-065", "title": "Retrieve inserts at the cursor", "feature_ids": ["WP51-019"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 554, "printed_end": 556, "pdf_start": 571, "pdf_end": 573}]},
{"id": "CMD51-066", "title": "Name a new document with F10", "feature_ids": ["WP51-020"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 565, "printed_end": 565, "pdf_start": 582, "pdf_end": 582}]},
{"id": "CMD51-067", "title": "Decline overwriting an existing file", "feature_ids": ["WP51-020"], "oracle_status": "partially-observed", "source_locators": [{"source_id": "REF51", "printed_start": 566, "printed_end": 566, "pdf_start": 583, "pdf_end": 583}]},
{"id": "CMD51-068", "title": "Approve overwriting an existing file", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 566, "printed_end": 566, "pdf_start": 583, "pdf_end": 583}]},
{"id": "CMD51-069", "title": "Edit the displayed save filename", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 566, "printed_end": 566, "pdf_start": 583, "pdf_end": 583}]},
{"id": "CMD51-070", "title": "Typing a save filename starts a new name", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 566, "printed_end": 566, "pdf_start": 583, "pdf_end": 583}]},
{"id": "CMD51-087", "title": "Exit without saving and cancel application exit", "feature_ids": ["WP51-029"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 194, "printed_end": 194, "pdf_start": 211, "pdf_end": 211}]},
{"id": "CMD51-149", "title": "Preserve an untouched native file byte for byte", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 565, "printed_end": 566, "pdf_start": 582, "pdf_end": 583}]},
{"id": "CMD51-150", "title": "Reject an unsafe opaque-structure edit before replacement", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 565, "printed_end": 566, "pdf_start": 582, "pdf_end": 583}]},
{"id": "CMD51-151", "title": "Preserve unrelated native data after a supported edit", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 565, "printed_end": 566, "pdf_start": 582, "pdf_end": 583}]},
{"id": "CMD51-152", "title": "Retain original after a failed save", "feature_ids": ["WP51-020"], "oracle_status": "not-run", "source_locators": [{"source_id": "REF51", "printed_start": 565, "printed_end": 566, "pdf_start": 582, "pdf_end": 583}]}
],
"observed_states": [
{"id": "O1", "case_id": "CMD51-066", "from_state": "editing unnamed", "to_state": "save filename", "event": "F10", "run": "2026-10-29-smoke-03", "repeat": "2026-10-29-smoke-02", "capture": "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/save-prompt/screen.txt", "cues": ["Document to be saved:", "WORDLING TEST"], "trace_segment": [{"key": "f10"}, {"capture": "save-prompt"}], "limitation": "The observed blank filename prompt belongs to a new original document. No dirty/cursor snapshot beyond the capture is inferred."},
{"id": "O2", "case_id": "CMD51-066", "from_state": "save filename", "to_state": "editing named", "event": "type C:\\OUT\\NEWTEST, Enter", "run": "2026-10-29-smoke-03", "repeat": "2026-10-29-smoke-02", "capture": "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/saved/screen.txt", "cues": ["C:\\OUT\\NEWTEST", "WORDLING TEST", "Pos 2.3\""], "trace_segment": [{"type": "C:\\OUT\\NEWTEST"}, {"key": "ret"}, {"capture": "saved"}], "limitation": "Native NEWTEST saved; editing resumes. Prompt disappearance alone does not prove disk completion; later extraction/normal exit seals bytes."},
{"id": "O3", "case_id": "CMD51-067", "from_state": "editing changed ORIGINALMODIFIED", "to_state": "replace question", "event": "F10, Enter displayed SAME", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "capture": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/replace-prompt/screen.txt", "cues": ["Replace C:\\OUT\\SAME? No (Yes)", "ORIGINALMODIFIED"], "trace_segment": [{"key": "f10"}, {"key": "ret"}, {"capture": "replace-prompt"}], "limitation": "The exact captured replacement question is for SAME. Guest COPY had prepared BEFORE; it is incidental DOS setup, not full Shell acceptance."},
{"id": "O4", "case_id": "CMD51-067", "from_state": "replace question", "to_state": "save filename with SAME retained", "event": "n", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "capture": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/different-filename-requested/screen.txt", "cues": ["Document to be saved: C:\\OUT\\SAME", "ORIGINALMODIFIED"], "trace_segment": [{"key": "n"}, {"capture": "different-filename-requested"}], "limitation": "Refusal requests another filename. Disk SAME equals BEFORE and retains ORIGINAL; no success state or overwrite occurs."},
{"id": "O5", "case_id": "CMD51-067", "from_state": "save filename after refusal", "to_state": "editing changed buffer", "event": "F1", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "capture": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/unsaved-buffer/screen.txt", "cues": ["ORIGINALMODIFIED", "C:\\OUT\\SAME", "Pos 2.6\""], "trace_segment": [{"key": "f1"}, {"capture": "unsaved-buffer"}], "limitation": "F1 here preserves changed in-memory content; it does not establish F1 at Retrieve, Exit, replacement question or every dialog."},
{"id": "O6", "case_id": "CMD51-048", "from_state": "normal editing at end", "to_state": "Reveal Codes visible", "event": "Alt+F3", "run": "2026-10-29-smoke-03", "repeat": "2026-10-29-smoke-02", "capture": "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-048/codes-on/screen.txt", "cues": ["[BOLD]alpha[bold]beta", "Press Reveal Codes to restore screen", "Pos 1.9\""], "trace_segment": [{"key": "alt-f3"}, {"capture": "codes-on"}], "limitation": "Normal text remains alphabeta; code-pane labels describe original formatting. There is no before/after native export for this recipe."},
{"id": "O7", "case_id": "CMD51-048", "from_state": "Reveal Codes visible", "to_state": "normal editing same end position", "event": "Alt+F3", "run": "2026-10-29-smoke-03", "repeat": "2026-10-29-smoke-02", "capture": "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-048/codes-off/screen.txt", "cues": ["alphabeta", "Pos 1.9\""], "trace_segment": [{"key": "alt-f3"}, {"capture": "codes-off"}], "limitation": "Visible text and status position retained; exact no-edit native preservation is a future FC-002 requirement, not observed original save identity."},
{"id": "O8", "case_id": "CMD51-067", "from_state": "editing changed buffer", "to_state": "DOS prompt after exit", "event": "F7, n, y", "run": "2026-10-29-extended-04", "repeat": "2026-10-29-extended-03", "capture": "docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/clean-exit/screen.txt", "cues": ["C:\\WP51>"], "trace_segment": [{"key": "f7"}, {"key": "n"}, {"key": "y"}, {"capture": "clean-exit"}], "limitation": "Archived clean_exit awaits Save document? then Exit WP?; intermediate full prompt choices are not separately captured. This is clean exit, not cancel-exit087."},
{"id": "O9", "case_id": "CMD51-005", "from_state": "normal editing", "to_state": "repeat consumed after insertion", "event": "Esc,5,x", "run": "2026-10-29-smoke-03", "repeat": "2026-10-29-smoke-02", "capture": "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-005/repeated/screen.txt", "cues": ["xxxxx"], "trace_segment": [{"key": "esc"}, {"type": "5"}, {"type": "x"}, {"capture": "repeated"}], "limitation": "Five x characters observed. Escape is not a global Cancel binding; menu/prompt Escape alternatives remain documentary."},
{"id": "O10", "case_id": "CMD51-001", "from_state": "menus hidden", "to_state": "menus shown then hidden", "event": "Alt+= twice", "run": "2026-10-29-smoke-03", "repeat": "2026-10-29-smoke-02", "capture": "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-001/menu-off/screen.txt", "cues": ["Doc 1 Pg 1", "Pos 1\""], "trace_segment": [{"key": "alt-equal"}, {"capture": "menu-on"}, {"key": "alt-equal"}, {"capture": "menu-off"}], "limitation": "Manifest checks appearance/disappearance and retained visible position; submenu navigation/cancellation002 remains unrun."}
],
"gaps": [
{"id": "G1", "case_id": "CMD51-065", "transition": "blank editing \u2192 retrieve filename \u2192 retrieved editing", "event": "Shift+F10, enter owned fixture, Enter", "basis": "REF554\u2013556/PDF571\u2013573 asks for filename and inserts retrieved text at cursor; cursor after initial codes. Exact prompt string/default-name/editor/cancel states are not captured.", "probe": "Probe blank retrieval of the pinned ORIGIN fixture, missing path and F1/Esc separately; native input preserved. Existing-buffer insertion and initial-code interactions need later variants."},
{"id": "G2", "case_id": "CMD51-019", "transition": "editing \u2192 after initial codes at beginning", "event": "Home,Home,Up", "basis": "Manual cursor destination; dedicated case not-run.", "probe": "Compare token-gap position in both views without mutation; distinguish G3."},
{"id": "G3", "case_id": "CMD51-020", "transition": "editing \u2192 before initial codes at beginning", "event": "Home,Home,Home,Up", "basis": "This sequence occurs incidentally in other archived editing recipes; that is not full dedicated case observation.", "probe": "Capture before/after independently on retrieved formatted fixture, both views and prefix-sequence reset/cancel."},
{"id": "G4", "case_id": "CMD51-049", "transition": "code gap \u2192 next code gap with stationary visible text cursor", "event": "Right", "basis": "Manual requirement, dedicated case not-run. WP04 observed code-target setup is bounded evidence, not general cursor equivalence.", "probe": "Use before/after Bold On and Off gaps in saved ORIGIN; record pane focus, token position, normal cursor and bytes."},
{"id": "G5", "case_id": "CMD51-068", "transition": "replace question \u2192 successful replacement", "event": "y", "basis": "Canonical successful overwrite unrun; WP03 storage foundation refuses actual replacement.", "probe": "Keep replacement refusal explicit until original backup/Fast Save/failure transaction and writer contracts are accepted."},
{"id": "G6", "case_id": "CMD51-069", "transition": "save filename \u2192 edited existing name", "event": "Left/Right/Backspace then Enter", "basis": "Documentary filename editing differs first-character replacement; exact state/cursor branches unrun.", "probe": "Probe prefilled old name, edit keys/typeover/cancel and compare native destination/source effects."},
{"id": "G7", "case_id": "CMD51-070", "transition": "save filename \u2192 fresh typed filename", "event": "character first then Enter", "basis": "Documentary first character clears displayed name; not-run.", "probe": "Needed before naming a new destination after Retrieve; do not assume generic text-input append semantics."},
{"id": "G8", "case_id": "CMD51-087", "transition": "exit save question \u2192 exit confirmation \u2192 editing/session", "event": "F7,n,n", "basis": "Dedicated cancel-application-exit case not-run. Incidental clear_doc1 calls F7,n,n in merge setup; no dedicated buffer-state audit. F7,n,y clean exit does not prove this branch.", "probe": "Probe named/unnamed and saved/changed buffers, capture both prompts and resulting buffer/filename/dirty state. F1 at each prompt is a separate documentary branch requiring case expansion."},
{"id": "G9", "case_id": "CMD51-002", "transition": "submenu \u2192 parent versus leave all menus", "event": "F1 versus F7", "basis": "Manual distinction unrun; Escape alternate Cancel is documentary and context-dependent.", "probe": "Capture exact submenu/cancel depth, original letter/navigation choices and return context; no generic menu engine guesses."},
{"id": "G10", "case_id": "CMD51-149", "transition": "retrieved no-edit image \u2192 same exact native image saved", "event": "F10 workflow plus bounded storage outcome", "basis": "FC-002 is a Wordling guarantee, canonical comparison not-run. Original WP may format/alter metadata.", "probe": "Use exact native length/hash/bytes under accepted storage boundary; original reopen separately. Do not label original-app new-document save as Wordling no-edit acceptance."}
],
"starter_fixture": {"path": "docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5", "size": 334, "sha256": "c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d", "case_id": "CMD51-204", "body_hex": "41c30cc34243c40cc444"}
}
```
<!-- WP11_AUDIT_END -->

```sh
python3 - <<'PY_AUDIT'
from pathlib import Path
import hashlib,json,re,struct,subprocess
p=Path('kitty-specs/wp51-parity-01M64CVY/contracts/session.md');text=p.read_text()
a=json.loads(text.split('<!-- WP11_AUDIT_BEGIN -->',1)[1].split('```json\n',1)[1].split('\n```',1)[0])
sha=lambda b:hashlib.sha256(b).hexdigest()
for x in a['source_inputs']:assert sha(Path(x['path']).read_bytes())==x['sha256'],x['path']
cases={x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
features={x['id']:x for x in json.loads(Path('docs/research/feature-inventory.json').read_text())}
links={c['id']:c for c in a['case_links']}
for cid,c in links.items():
    assert all(c[k]==cases[cid][k] for k in c)
    assert cases[cid]['implementation_status']=='not-implemented'
    for f in c['feature_ids']:assert cid in features[f]['command_scenario_ids']
    for loc in c['source_locators']:assert loc['pdf_start']==loc['printed_start']+17 and loc['pdf_end']==loc['printed_end']+17
assert set(re.findall(r'CMD51-\d{3}',text))==set(links)|{a['starter_fixture']['case_id']}
required={'O1':'WP51-020','O2':'WP51-020','O3':'WP51-020','O4':'WP51-020','O5':'WP51-020','O6':'WP51-013','O7':'WP51-013','O8':'WP51-020','O9':'WP51-007','O10':'WP51-001'}
assert len(a['observed_states'])==10 and len(a['gaps'])==10
runs={}
for state in a['observed_states']:
    cid=state['case_id'];c=links[cid]
    assert required[state['id']] in c['feature_ids'],(state['id'],cid)
    assert c['oracle_status']=='partially-observed'
    line=next(x for x in text.splitlines() if x.startswith('| '+state['id']+' |'))
    cols=[x.strip() for x in line.split('|')]
    assert cols[2]==cid+' ('+c['title']+'); '+', '.join(c['feature_ids'])
    assert cols[3]==state['from_state']+' → '+state['event']+' → '+state['to_state']
    assert cols[4]=='; '.join('`'+x+'`' for x in state['cues']) and cols[5]==state['limitation']
    for rid in (state['run'],state['repeat']):
        rp=Path('docs/research/reference-runs')/rid/'run.json';run=json.loads(rp.read_text());runs[rid]=run
        assert str(rp) in cases[cid]['evidence_paths'] and run['scope']=='original-reference-only' and not run['wordling_tested']
        result=next(x for x in run['results'] if x['case_id']==cid)
        assert result['result']=='observed-matches-smoke-expectations' and all(x['passed'] for x in result['checks'])
        trace=result['trace'];segment=state['trace_segment']
        assert any(trace[i:i+len(segment)]==segment for i in range(len(trace)-len(segment)+1))
        capture=state['capture'].replace(state['run'],rid)
        content=Path(capture).read_text();assert all(x in content for x in state['cues'])
        for e in result['evidence']:
            b=Path(e['path']).read_bytes();assert (len(b),sha(b))==(e['size'],e['sha256'])
        assert any(e['path']==capture for e in result['evidence'])
        for e in result.get('native_outputs',[]):
            b=Path(e['path']).read_bytes();assert (len(b),sha(b))==(e['size'],e['sha256'])
        for source in run.get('runner_sources',[]):
            archive=rp.parent/'runner-source'/Path(source['path']).name
            assert sha(archive.read_bytes())==source['sha256']
req={'G1':'WP51-019','G2':'WP51-008','G3':'WP51-008','G4':'WP51-008','G5':'WP51-020','G6':'WP51-020','G7':'WP51-020','G8':'WP51-029','G9':'WP51-001','G10':'WP51-020'}
for r in a['gaps']:
    c=links[r['case_id']];assert req[r['id']] in c['feature_ids'] and c['oracle_status']=='not-run',(r['id'],r['case_id'])
    line=next(x for x in text.splitlines() if x.startswith('| '+r['id']+' |'))
    lead=r['case_id']+' ('+c['title']+'); '+', '.join(c['feature_ids'])
    assert [x.strip() for x in line.split('|')][2:6]==[lead,r['transition']+'; '+r['event'],r['basis'],r['probe']]
for rid in ('2026-10-29-extended-03','2026-10-29-extended-04'):
    d=Path('docs/research/reference-runs')/rid/'CMD51-067'
    before=(d/'BEFORE.WP5').read_bytes();assert before==(d/'SAME.WP5').read_bytes()
    assert before[struct.unpack_from('<I',before,4)[0]:]==b'ORIGINAL'
f=a['starter_fixture'];b=Path(f['path']).read_bytes();assert (len(b),sha(b))==(f['size'],f['sha256'])
assert b[struct.unpack_from('<I',b,4)[0]:].hex()==f['body_hex']
r=json.loads(Path('docs/research/reference-runs/2026-10-29-advanced-04/run.json').read_text())
c=next(x for x in r['results'] if x['case_id']==f['case_id'])
assert any(x['path']==f['path'] and x['sha256']==f['sha256'] for x in c['evidence'])
for r in a['library_sources']:
    assert r['needle'] in Path(r['path']).read_text().splitlines()[r['line']-1]
assert 'charm.land/bubbletea/v2 v2.1.1' in Path('go.mod').read_text()
for pg,needle in [(571,'Retrieve'),(582,'Save'),(567,'Alternate Keystroke')]:
    out=subprocess.check_output(['pdftotext','-f',str(pg),'-l',str(pg),'-layout','research/cache/WPDOS51Reference.pdf','-'],text=True)
    assert needle in out,(pg,needle)
print('WP11 canonical state/trace/capture/native/library-source and locator audits valid')
PY_AUDIT
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp11-review.xml
```

Author validation: embedded source/canonical-case/state/trace/capture/native and
cached-library anchor/hash/locator audit passes; both catalogue checks and the
genuine regression runner pass (JUnit `/tmp/wp11-review.xml`). Go discovery
passes; build/test/vet explicitly skip this planning checkout with no Go packages,
not approved implementation lanes. A negative full-audit substitution of a valid
save case into the Repeat state fails the independent state-to-feature binding.
No original probe, Linux terminal key capture or application implementation is
claimed. SESSION1 and its missing prompt/cursor/cancel branches remain unrun.
