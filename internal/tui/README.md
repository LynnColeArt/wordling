# Bounded executable native editing composition (WP18/WP28)

Run `go run ./cmd/wordling -root /absolute/local/directory -profile local-flat`
from a terminal. The operator chooses a validated local filesystem; the app does
not certify a network mount or interpret DOS drives. Only flat ASCII basenames
are supported. Shift+F10 retrieves, Alt+F3 toggles Reveal Codes, F10 invokes the
approved snapshot or native-candidate save workflow, and F7 invokes the original bounded exit prompts.
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
actual Directory.Read/Observe/Save/PreparePublication/Publish and returns the exact operation/revision/kind.
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

## Native editing continuation (WP28)

Printable ASCII including q is document content in Editing/Waiting; q does not
quit. Ctrl+Q/Ctrl+S remain unsupported. Insert toggles typeover, Delete/Backspace
retain direction, Alt+F4 starts the approved forward Reveal block, and selected
Backspace asks the exact block question. Selected forward Delete refuses. Y/N,
F1 and Escape resolve only in the reducer's exact question contexts. Undelete
uses F1, numeric2 Previous, numeric1 Restore and preview F1 cancel. Selection and
preview [Block] display markers are never native bytes. HistoryCountKnown=false
renders as unknown, with the qualified flag separate. Normal/Reveal/preview use
the same immutable revision/gap and real Present/Preview data. The inherited
normal-pane hardware caret remains a terminal text position; the displayed gap
is the semantic authority, including positions adjacent to zero-width codes.
No original physical Pos, screen raster or printed layout is inferred.

Runtime captures independent Directory/Document/Destination wrappers and candidate
bytes before tea.Cmd dispatch. Directory value equality compares its one private
opened capability; copied wrappers are accepted, independent opens of the same
inode are refused. Close still closes the shared capability. PublishCandidate
uses the actual loaded-source PreparePublication followed by Publish with the
exact Operation/Revision PublicationID, never a snapshot Save shortcut or a new
publication constructor. The source guard stays the first loaded source after
later displayed Save As names. No-edit crossdirectory storage Save remains
supported; edited candidate cross-capability requests retain the storage refusal.
Production local-flat exposes one opened root only, not a crossdirectory dialog.

Pending candidate writes permit only reducer-admitted text/mode/navigation;
newer edits keep the old immutable candidate and cannot be cleaned or renamed by
its later result. A successful older publication is visible as a detached receipt.
Host detach is a separate programmatic message; keys wait for its actual receipt,
and detached publication needs reconciliation. Generic host errors paired with
Published retain destination-may-exist uncertainty, just like typed storage failures;
no current success or quit is manufactured. A successful older attached publication
is a known destination effect, not an atomic cancellation or a save of newer edits.

At the WP28 checkpoint, only loaded structurally admitted originals could mutate. Prefix564, unsupported
characters/opaque structures, more than two sequential qualified Bold pairs,
EC045 intermediate/unbrowsed history and wider unqualified lifecycles retain
component refusals. Normal block selection, reversed/partial text blocks, ASCII
Backspace grouping, original repeats, F6 creation and actual overwrite remain
unimplemented. Preserved history fragments do not establish hidden counts or
new interleavings. WP37 subsequently adds the reviewed macro host, and WP48 below adds startup New through the approved constructor. These additions do not widen the remaining editing/history limits.

Reproduction and exact source/native/synthetic-PTY/typed-failure distinctions are
in docs/research/continuation/editable-session/. WP29 must independently exercise
the emitted app files with the original application; this package adds no VM,
original printer/resource qualification or full canonical scenario/FR/M1 claim.

## Startup native creation (WP48)

Fresh command startup now uses the one approved closed historical native profile
through the actual editor constructor. No filename/retrieve is required before
admitted ASCII typing or true empty F10 Save. The existing `-profile local-flat`
and explicit `macro-cout` names still select path namespaces; native serialization
selection is separate and fixed internally. It supplies no fonts/printer runtime
resources or physical layout guarantee. Missing NativeProfile in the existing Go
Config defaults to this same sole profile; an unknown selection refuses.

First Save schedules genuine editor47 PublishNewBuffer, then separately schedules
same-capability BindNewSource Read. Private runtime tickets deduplicate the opaque
issued RequestKey, rather than Operation/Revision counters, and retain37's single
UI-transition authority. The reducer alone commits the source/name/saved revision.
No reducer/Update native IO, template, dummy loaded document or shadow editor is
used. Live New birth/NoLoadedOriginal remains after binding; later SaveAs keeps
the first source guard while display/last-saved receipt may change.

During waiting, Save is not confirmed. If a file was published but its Read could
not verify the original receipt, visible F10 retries verification ONLY against
that same captured capability/receipt. This contextual F10 action is a Linux
safety adaptation, not newly observed original behavior. It never republishes or
opens another root. Publication uncertainty refuses F10/retry/normal successful
exit and preserves data/receipts. Host shutdown remains possible and reports an
unresolved outcome. Programmatic CancelPendingMsg detaches real IO without
cancelling disk effects. Close drains started workers, then closes the shared
capability; later queued commands do no IO and cannot claim clean success.

This route is startup-only. F7 clear still does not make a new document or reset
history; new-target macros and second-screen New remain refused. Existing loaded
macro37, loaded-source publication41, history36/26, unknown count/EC045 and other
unqualified operations retain their guards. Full M1 remains open. Actual executable
PTY/native, public Runtime failures and explicitly instrumented TEST-only storage
ports are separated in docs/research/continuation/new-session/README.md.

WP52 adds an active native-token range in the existing lower Reveal row: one
ASCII cell, all six cells of an actual Bold label, or one display-only blank at
actual EOF. Literal bracket text stays ASCII. The source is the same immutable
Present token index/span and cursor gap as the normal pane; the upper caret still
uses normal text width. The selected original VGA roles map to explicit Linux
ANSI white/blue, bright white/blue and white/red, with resets through clipping.
Physical colors and complete pane geometry remain unqualified. Selection/history
virtual overlays retain their existing markers without claiming native active
spans. Macro DISPLAY OFF retains the already captured styled pane/caret. See
[evidence/wp52/README.md](evidence/wp52/README.md) for original and live-app proof.

## Bounded display anchors (WP69)

At exactly80x25, a current healthy ordinary Insert view places its actual native
text and text-width caret at row0. Reveal places that same document's styled
code stream at row13 and the36-character restore-screen footer plus44 spaces at
row24. Footer logical VGA roles17/1F/17 map through the existing Linux ANSI
profile; physical palette/raster/key delivery and full-screen equality remain
unqualified. Rows11/12 remain neutral HOST omission, not a fabricated ruler or
Pg/Ln/Pos calculation. Existing4096-token and horizontal clipping limits remain.
Implementation diagnostics remain available through State/Session.

This small layout admits no selection, history preview, active Typeover, modal
prompt, genuine notice/error, source-stale UI, partial unsupported inspection,
active/pending/deferred macro or IO, or unresolved publication. Actual unknown
history count is genuine uncertainty: HistoryCountKnown=false retains the legacy
visible history=unknown fallback without changing history knowledge. Other sizes
retain the bounded legacy display. The supported seven-gap loaded native stream
and genuine first ordinary ASCII edit remain reachable anchor positives.

The authentic menu-capable pristine startup context retains its SAME legacy base
whether the menu is hidden or shown. Alt+= overlays only existing row0, preserving
body/caret and full hide restoration. After a real first edit or Retrieve leaves
that pristine context, healthy Insert may use anchors; no state is reset to gain
eligibility. Typeover keeps its visible legacy indicator until actual Insert
returns. Frozen DISPLAY OFF captures source, styles, inspection, caret AND layout
before consulting live state; resize clips that captured layout rather than
choosing geometry from a newer gap. Partial HR/HP/unknown inspection remains the
existing inactive HOST view with upper unsupported error and no native caret.
This adds no page layout, ruler, general scrolling, native API, writer or IO.

## Whole-ASCII follow-cursor view (WP71)

Current healthy Doc1 Insert revisions with4097..16384 owners may use one bounded
HOST horizontal window. After an authentic Update dispatch, at most four existing
E catalogues authenticate the complete immutable revision in contiguous chunks
of4096. Each owner must be one printable ASCII byte with its complete one-byte
native span. This rejects an offscreen code as well as an onscreen one. E checks
owner/raw bounds before copying; its independent text ceiling is checked during
construction. The closed mapping is at most24576 bytes per4096-owner chunk.
Totals16385+ are refused before catalogue allocation; this is a presentation
ceiling, not a native document/open/edit limit. Short sources keep the old path.

One private constant-size copied positive/negative fact is bound to the opaque
native revision. Only the authentic returned Update chain prepares it; View,
State and Session observations never install it. An unchanged eligible revision
reuses its fact across Left/Right/Reveal/resize. New revision, acquisition or
leaving eligibility invalidates it; equal-byte independent acquisitions have
different keys. No source payload, rendered strings, command/IO permit or global
cache is retained. Stale Models still fail their normal source/UI gates.

The window starts at max(0,gap-width/2) and contains min(width,total-start) actual
owners, up to width4096. Both panes use that same Session.Present window and
absolute native token indices; rendering starts at local zero. The real active
owner remains included at width1; only trueEOF gets a display-only active blank.
At exactly80x25, WP69's row0/13/24 anchors and complete footer remain. Other sizes
retain existing legacy composition. This is a HOST policy, not observation of
original WP long-line thresholds, hysteresis or general scrolling/page layout.

All old menu, Typeover, partial inspection, error, source, IO, macro and uncertain
history exclusions remain. Actual clear/retrieve and Doc1/Doc2 switching can make
history unknown; those outcomes deliberately keep visible history=unknown instead
of claiming requalification. Frozen DISPLAY OFF is selected before live facts or
windows. Source/native bytes, reducer/history and save behavior are unchanged.
Prospective classifier/warm allocation limits and actual bounded measurements,
public Model tests, unmodified CLI PTYs and failures are recorded in
[evidence/ascii-viewport](evidence/ascii-viewport/).

Character Repeat is a bounded host composition for untouched constructor New
Doc1 at 80x25: Escape, one explicit digit 1–9, then one nonnumeric printable
ASCII key inserts one atomic Text payload. Escape/F1 cancel; other unsupported
pending input consumes that event and cancels. The next ordinary key has no
inherited count. The legacy row-2 count prompt is host UI. Loaded macro Repeat
remains separate. Only final `xxxxx` has original CMD51-005 screen witnesses;
other counts, cancellation, native conservation and history are host contracts.
General Repeat and full M1 parity remain open.
