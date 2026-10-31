# Read-only session reducer (WP17)

`New(Config)` creates an empty session. `Session.Reduce(Event)` returns the next
session value, at most one storage `Intent`, and an explicit refusal error. Keep
one authoritative state chain; forking old session values and executing their
intents concurrently would reuse deterministic operation numbers. It is safe to
inspect/project immutable values concurrently. This package has no Bubble Tea,
filesystem execution, native byte editing or new-document serializer.

`Snapshot()` supplies mode, prompt, filename draft/caret/original name, Home
prefix, document revision, shared token-gap/Reveal state, pending request, last
save status and applied/detached storage receipts. `Document()`, `Source()` and
`Present(start,count)` consume the actual immutable document/storage APIs. The
storage source snapshot remains distinct from the displayed name after a new
publication; it is never silently rebound to a newly written file. Opening a
snapshot calls document.Parse on its exact export, never a duplicate codec.

## Host composition contract

`Intent` carries Operation, Revision, Kind and the actual Directory, Document,
Destination and overwrite Decision. The host executes exactly one dependency
call and returns `Result` with the same operation/revision/kind:

| Intent | Host call | Result field |
| --- | --- | --- |
| Read | `Directory.Read(Name)` | Document, Err |
| Observe | `Directory.Observe(Name)` | Destination, Err |
| WriteSnapshot | `Directory.Save(Document, Destination, Decision)` | Outcome, Err |

Use handles returned by those constructors/APIs, not zero storage handles or
caller-fabricated observations. A successful Observe of an absent name emits a
new WriteSnapshot request with a new operation number. Existing names require a
separate explicit Yes decision; only the actual same-inode source can proceed
with AllowOverwrite. Other replacements return typed UnsupportedReplacement.
Storage retains final freshness/destination checks and all filesystem safety;
the session does not infer freshness from an earlier observation.

Published success requires a nonzero destination inode as well as the bound
name/directory and source size/hash. Device zero is permitted. This rejects an
impossible receipt; it does not independently authenticate host IO or prove an
arbitrary inode exists. No-op and new publication have different SaveState values. A nonnil storage error
never becomes complete success, even if paired with an optimistic Outcome.
Typed errors, candidate residue, wrapped cause and DestinationMayExist remain
available. Publication uncertainty stays SaveUncertain and never exits. A result
must match the pending operation, revision and kind; duplicate, stale or cancelled
results become Detached receipts without consuming another pending request.
`CancelOperation` is a host safety action, not F1/Escape emulation or proof of IO
cancellation. Late publication may already have a destination: its detached
receipt exposes that fact. The host must surface reconciliation/residue; this
package cannot roll back disk effects. It never auto-exits after a save.

Locations are explicit pinned rooted handles. Empty display Prefix accepts only
flat basenames and is the production composition default. Nonempty prefixes are
exact caller-declared comparison/profile bindings, with no case folding, drive
resolution, environment expansion or host path joining. The tests bind B:\ and
C:\OUT\ to their own temporary directory solely to compare original prompt
states. This is test provenance, not a supported DOS filesystem mapping. A real
CLI must declare its validated local rooted location/profile and visibly explain
flat-basename limitations. Slashes, residual colons/backslashes, dot/dot-dot,
reserved candidate names and drafts over255 ASCII bytes are refused. The255-byte
bound is a storage safety policy, not an original DOS filename-length claim.

## Supported state matrix

| Context | Supported bounded transition | Explicit boundary |
| --- | --- | --- |
| Blank Editing | Shift+F10 → Retrieve filename | Retrieve into any loaded document is refused |
| Retrieve filename | ASCII draft; Enter emits Read; F1/Esc return blank; missing-file error/retry | No List Files, cursor editing, nested paths, insertion or other errors styled as original messages |
| Loaded Editing | Alt+F3; Right across supported ASCII/Bold; Home2/3 Up endpoints | One document cursor supplies both views; opaque movement/presentation refused; Home only body-leading Bold, not all Initial Codes |
| Save filename | Prefilled caret0; Right/Backspace/text; character-first restart; F1 return | Enter after editing a prefilled name is refused; only edit-and-cancel observed |
| Replacement question | No → retained filename; explicit Yes only same-file no-op foundation | Actual overwrite always UnsupportedReplacement; generic F1/Esc defaults unobserved |
| Clean Editing F7 | Save question with unmodified indicator; F1 retains; Esc advances filename; No → Exit question | No dirty or new-document writer. Save-on-exit completion refused; F1 safely returns from filename |
| Exit question | F1 retains; No/Esc clears and returns blank; Yes exits | Clean named/fresh-empty contexts only; final DOS is domain Exited, not invented terminal delivery |
| Waiting | Bound result or explicit host detach | Original keys during asynchronous IO are unobserved and refused |
| Normal Editing | Unsupported F1 Undelete, Escape Repeat, text edits, generic Left/Up | Full original editing remains M1 follow-up |

Original observations and native/export promises are distinct. A Wordling same-
file no-op or byte-identical new-name publication implements FC-002 using the
approved storage contract; original WP's no-edit Save changes representation.
No original overwrite or byte-identity observation is invented. Reveal is a
read-only projection, not full code editing. No dirty flag can be injected into
this session: changed original contexts in WP13 remain unsupported here.

Tests and source associations live in evidence/. Full menus, selection, search,
Undelete/Repeat, semantic writers, two documents, layout/print, physical Linux key
delivery and complete FR-004/005/006 remain open. This component is neither a
complete editor nor full original/differential scenario verification.
