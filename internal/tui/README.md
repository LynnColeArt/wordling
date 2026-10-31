# Bounded executable composition (WP18)

Run `go run ./cmd/wordling -root /absolute/local/directory -profile local-flat`
from a terminal. The operator chooses a validated local filesystem; the app does
not certify a network mount or interpret DOS drives. Only flat ASCII basenames
are supported. Shift+F10 retrieves, Alt+F3 toggles Reveal Codes, F10 invokes the
approved no-edit save workflow, and F7 invokes the original bounded exit prompts.
No global q/Ctrl+Q/Ctrl+S/Escape aliases exist. F1/Escape retain their observed
context-specific reducer meaning. Missing/unobserved branches refuse explicitly.

`Open(Config{Root, Profile: LocalFlat})` returns a directory-owning Runtime and
value Model. Model implements the pinned Bubble Tea v2.1.1 interface. Update
consumes input.Translate and calls the actual editor.Session.Reduce; View consumes
shared document.Presentation token positions. State() and Session() expose
immutable inspection for tests/measurement. Keep one authoritative model chain;
do not execute intents from forked old values. No terminal code serializes native
bytes or decides original page geometry. The normal pane styles supported Bold;
the Reveal pane shows the same tokens and gap. The presentation has a4096-token
safety window and horizontally clips terminal cells; it does not paginate.
Cursor beyond that window and opaque-token windows explicitly refuse presentation
while preserving the complete native snapshot for no-edit storage.

Production uses only the empty rooted prefix. Text Shift/CapsLock modifiers may
supply uppercase filenames; command modifiers remain exact. Paste, releases,
repeats, unknown messages and unsupported keys never replay editing commands.
Unknown/paste states are visible. Resize changes bounded terminal dimensions
(1..4096 cells per axis), never the document. Physical delivery remains UNQUALIFIED
in State and the application view; requesting keyboard enhancements is separate
from actual terminal capability or physical evidence. No original Pos inches,
line/page metrics, DOS raster, help/menu engine or unsupported writer is invented.
Original prompt wording and unmodified/Reveal status cues are preserved; their
row/spacing arrangement follows this bounded Linux presentation, not an accepted
pixel/whole-screen compatibility claim.

Each tea.Cmd captures one complete immutable editor.Intent. Runtime calls the
actual Directory.Read/Observe/Save and returns the exact operation/revision/kind.
The reducer validates document/directory/name/native fingerprint and source
identity. Observe and Save are separate operations, never a claimed atomic pair.
Same-source explicit Yes can yield SameFileNoOp; a new name yields
NewNamePublished only after real verified IO. Existing different inodes always
refuse replacement, even for identical bytes. Source is not rebound after Save As.

CancelPendingMsg is an explicitly programmatic host detach, with no physical key
alias or claim of disk cancellation. Further keys are held until its actual late
receipt arrives; detached publication requires filesystem reconciliation and
never becomes current success. Typed cleanup/uncertain failures retain candidate
and destination-may-exist details, block further commands, preserve source/native
state, and never auto-exit. No speculative rollback/unlink/recovery action occurs.
The owner must inspect filesystem state after abnormal termination; there is no
fake acknowledgement button claiming recovery.

Runtime.Close gates new operations under the same lock as worker registration,
drains every started call, then closes the pinned directory. Queued commands
executed afterward refuse before touching descriptors. Each operation envelope
can execute only once. A duplicate dispatch returns a distinct non-completion
notice, checked before shutdown/capacity; it cannot settle the admitted operation
or consume its pending receipt. A first dispatch rejected before admission by
shutdown/capacity returns a definitive failure because no worker owns that
operation. A1024-operation host safety cap bounds receipt/identity
history (not an original limit). Completed() returns copied outcome/error metadata
without retaining loaded native images/destination handles. The actual command
checks terminal restoration, waits for worker drain, checks receipts/residue, and
reports host signals as abnormal rather than original successful exit. SIGKILL,
power-loss durability and automatic startup recovery remain unqualified. Runtime
Close does not promise a time bound on a blocked external filesystem.

Tests use real temporary directories and actual executable PTYs; injectable
completion errors explicitly test the host result boundary, not filesystem fault
claims. Approved storage tests cover lower-level faults. No native framing or
semantic writer is added, so no new native-parser fuzz acceptance is claimed.
Evidence, exact original-capture associations and reproduction are in
`docs/research/continuation/composed-session/README.md`.
