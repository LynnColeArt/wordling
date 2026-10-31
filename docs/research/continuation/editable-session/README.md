# WP28 bounded live native editing — review handoff

T082–T084 extends actual WP18 cmd/wordling/Model/Runtime in runtime-selected lane-h.
Core083b4ed and active-only Typeover display correction ac1d5d9 are the production
source checkpoints. Real approved27 source5d5c767, document26 source9519032,
storage41 source5ad84e4 and the original16 input adapter are consumed unchanged.
No native codec, alternate document/history/session, IO engine, new constructor,
source-less/new publication, macro UI, original VM or primary lifecycle is added.
Shared TUI18→28→37 ownership is sequential. Resolve implementer-ivan and implement
governance; unchanged compatibility/roadmap/spec/plan/data model/continuation and
independent18/25/26/27/41 reviews informed these bounded transitions. No authored
charter Code Review Checklist exists. Connected-teamspace login warnings are
separate from local execution; no auth/framework/global-setting change was made.

## Real production path and supported profile

Run `go run ./cmd/wordling -root /absolute/local/directory -profile local-flat`
from a Linux terminal. Root is an explicit operator-selected validated local
filesystem. One opened root and flat ASCII basenames are supported; there are no
DOS drive/path aliases, host file dialog, arbitrary mount/durability certification
or new blank-document save. Model.Update consumes actual WP16 input.Translate,
then actual Session.Reduce, real Document Present/Preview, and Runtime tea.Cmd IO.
Model/Runtime/State/Session public seams remain the inherited ones.

| Actual keys/context | Composition |
| --- | --- |
| ShiftF10 / F10 / F7 | Approved retrieve/name/save/exit prompts; original13 first-character/caret/cancel semantics |
| Printable ASCII / Insert | Actual InsertASCII/TypeoverASCII and original mode toggle; q is literal text, CtrlQ/CtrlS do not become commands |
| AltF3 / Left / Right | Shared immutable native revision and semantic token gap; terminal text-cell caret is not an inferred native byte offset |
| Delete / Backspace, no selection | Original direction forwarded; normal paired-code questions and Reveal bypass remain document-qualified |
| AltF4, Right, Backspace | Approved forward Reveal block; exact question, Yes/No/F1/Escape and separate F1 cleanup; selected forward Delete refuses |
| F1 / numeric2 / numeric1 / preview F1 | Actual Open/Previous/Restore/cancel; display overlay markers never enter native data |
| Resize / unknown / paste / release / repeated event | Resize only bounds terminal cells; others never become guessed editing commands; unsupported events/keys visible |

Typeover status is emitted only while active. Normal/Reveal/preview read the same
revision/gap. Normal-pane hardware caret remains inherited text position; zero-width
code positions stay distinct in reducer state and displayed gap. [Block] is display
only. Dirty/current/name/save and history count-known/qualified status are projected
from Snapshot. Unknown count is literally unknown, never empty. Presentation is
bounded to4096 tokens; oversized/opaque windows explicitly refuse presentation.
Terminal horizontal clipping is not original line wrap, pagination, raster, printed
Pos or layout/graphics/physical qualification.

## Actual candidate IO and failure semantics

Initial integration baseline failed because18 compared public Directory wrapper
addresses while27 correctly returned defensive copies. Runtime now captures full
independent Directory/Document/Destination wrappers and candidate bytes before Cmd
execution. Directory **value equality** compares its single private openedDirectory
capability: same acquisition copies work; independent opens of the same path/inode,
zero/nil/foreign wrappers refuse. Shared Close lifetime remains real and is tested.
No inode/name-only authorization or storage/editor patch replaces that boundary.

Read/Observe/no-edit Save remain actual APIs. PublishCandidate calls actual41
PreparePublication(source,target,candidate,PublicationID{Operation,Revision}), then
Publish with that same ID. It never writes loaded snapshot bytes instead of edited
bytes, fabricates a source, bypasses guard/absence observation or replaces an existing
file. No-edit crossdirectory storage Save remains supported in a real runtime test;
edited cross-capability publication retains its actual InvalidRequest. Production
local-flat still selects only one root, so this is no invented crossdirectory UI.

First loaded source guard is never rebased after a displayed Save As name changes.
Matching success alone marks the candidate revision saved. Real original-source
mutation, a late destination winner or actual Close preserves dirty/current/previous
published state and refuses. IO wrappers/bytes survive returned getter and queued
request reassignment. Observe and Publish remain separate observations, not a lock,
CAS or transaction over arbitrary external writers.

While an attached write is pending, only reducer-admitted text/mode/navigation can
continue. The older immutable payload stays fixed; later completion cannot clean or
rename newer edits and is retained as Detached with actual destination effect.
CancelPendingMsg is programmatic detachment without a key alias or disk cancellation.
Further keys wait for the authentic late receipt. Duplicate dispatch is a separate
non-completion message and cannot consume authentic IO;1024-operation receipt and
Close/drain policies remain inherited. Typed cleanup/residue/uncertainty and generic
host error paired with Published remain non-success, visible and block exit; no
rollback/removal/retry/recovery sidecar is attempted. Generic post-Publish error test
is explicitly an injected **host receipt** after real Publish, not a claimed disk
fault. Inherited storage tests cover filesystem-hook failures at their real boundary.

## Executed evidence, failures and reproducibility

Final accepted executable suite is **pty-final-02**, binary SHA256
0bbbb85f7db33f8e1a422d1efecbf1843158c576b356c6d1f1ba7e8d24f9a8e6
(5925080 bytes). Its prelaunch inputs.json binds ac1d5d9 lane source, every actual
local Go/module input and fixture; runner.py.txt archives the executing helper before
any child launch. Each child has actual argv, injected labelled key bytes, unmodified
wire-output.bin, stderr, result and before/after files. No physical input is qualified.

Five actual command processes cover ASCII insertion/typeover/Reveal/resize/unsupported
input, whole attributed block Restore, opening literal repair/Restore/browse/cancel/X,
normal directional question declines and abnormal SIGTERM. All four ordinary workflows
exercise existing-target refusal, first-character fresh Save As and original F7 No/Yes
exit. Sources and OTHER are whole-byte unchanged; COPY is real published native output.
Whole block COPY equals original04/204 RESTORED.WP5; repair COPY equals BOTH original23
repair-Restore r1/r2 N0001.WP5, with literal empty first pair. No-edit declined-question
COPY equals source. ASCII body is independently asserted and actual candidate whole-
byte publication is checked in model tests; WP29 original interoperability on app
outputs remains pending. App restoration check plus external termios-equality assertion
pass; raw termios flags are not separately archived. SIGTERM exits1 as host interruption,
never original exit; SIGKILL/power failure/physical terminals remain unqualified.

Earlier pty-attempt-01 and pty-final-01 are preserved, not overwritten or promoted as
final source. Initial helper consumed stderr before archival; its custody note is
explicit. pty-final-01 is the successful prior display source, superseded only because
inactive `Typeover=false` still showed the original cue. The active-only correction
has an explicit test; final suite/gates/race/mutants bind that final Go source.

`typed-integration.txt` retains real model/view/native-hash/state traces and tests.
Eighteen approved40 command paths go through actual WP16→Model.Update→27→26 and match
whole original N0001 files, including closing On+Off, with unknown counts and postX
history refusals retained. PTY whole/repair commands use original Backspace, never a
Delete alias. Inherited session13 raw prompt/cursor/native associations remain in the
existing original_test.go. associations.json binds exact canonical ID/title/features/
requirements/status/locators; audit rejects a valid-ID/wrong-feature control. Canonical
registry is unchanged, including the historical not-run047 lead; later bounded23/25
proof is consumed distinctly, not retroactively converted into a full scenario status.

Actual baseline and test-first failures are retained. Legacy18 duplicate tests formerly
sent n/y during pending IO expecting no effect;27 now admits those printable edits.
Those tests now probe non-edit keys and still enforce duplicate/authentic completion,
while dedicated newer-edit tests check genuine detached outcomes. q was removed from
the immutable unknown-event set because it is ordinary document content. A host-error
test initially overexpected Editing rather than the reducer's real SaveName resume;
it now asserts complete pre-key preservation. These are explicit test-expectation
corrections; no source failures were hidden by skipping or weakening guard behavior.

Final configured runner passes7 checks/0 skips: inventory, scenarios, adapter, actual
Go discovery/build/test/vet. Fresh `go test -race ./internal/tui ./cmd/wordling -count=1
-timeout=120s` passes (command package itself has no Go tests; actual executable tests
are Python PTYs). Six compiling live-composition faults are killed: wrapper-address
comparison, snapshot-for-candidate substitution, selected Delete alias, missing virtual
block, borrowed candidate and lost generic publication uncertainty. No binary parser/
writer changed, so native fuzz budgets were not redundantly rerun. Actual25/26 private
state/fuzz/resource policies remain binding. Python compiles; changed Go gofmt/diff checks
pass. Reproduce final checks from this exact code lane, not the Go-empty primary.

View resource observation uses actual4096-token document normal/Reveal views:52/53
allocations per call; TotalAlloc deltas24580800/24615112 bytes for101calls plus
measurement overhead on this host. These are cumulative observations, not peak RSS,
allocation hard caps, universal refusal costs, DOS limits or product SLOs. The added
UI arrays are bounded to the existing4096-token presentation; mutation65KiB/16384token/
two-pair admission and inherited broader16MiB readonly reader limits are unchanged.

## Automatic Go VCS stamp versus compiled source

Raw binary-buildinfo-final.txt reports primary332a4b2, **not** actual lane ac1d5d9.
This misleading metadata is preserved. Installed Go1.26.4 vcs.go lines214–221 declares
.git must be a directory; isVCSRoot lines626–647 checks fi.IsDir against that marker.
Lane .git is a file, so FromDir scans to the parent's primary .git directory. Exact
installed-source SHA/snippets/marker SHA and read-only reproduction facts are in
go-worktree-stamp.json. Actual GOMOD/cwd/lane HEAD/prelaunch source hashes plus go-list
packageDir/GoFiles hashes (actual-build-package-inputs.json) bind the compiled local
files to lane-h. The tested binary executes changed live editing/candidate APIs
absent from the old primary. No product version/behavior reads the stamp. No framework,
global environment, stamp suppression or extra source-identical PTY rerun was used to
make metadata look better; an independent reviewer must verify this distinction.

## Remaining scope and next consumer

All38 requirements/91 groups/full M1 remain open. Initial two nonnested Bold pairs,
literal empty pairs and approved metadata/resource values remain component admission
policies, not format limits. Prefix564, opaque/nested/formatter/resource variants,
nonASCII, normal/reversed/partial block selection, ASCII Backspace grouping, EC045
unbrowsed/intermediate, nonempty declines, higher-order hidden counts/interleavings/
repeat Restore and later attributed/postX history retain explicit refusals. Wider
menus/help/repeat/mouse/windows/search, actual overwrite/backup/FastSave/new creation,
macros/merge/structured/layout/print/resources/DOS/foreign-locale/platform work remain
required. No undocumented key alias, schema narrowing, full FR/case/physical UI
acceptance, original print output or M2/PDF follows from this bounded composition.

WP29 must consume actual app-produced native files and independently run original
Retrieve/edit/print/Save/reopen against pinned profiles; source23/25/26 library writer
qualification and current exact native comparisons do not replace that acceptance.
