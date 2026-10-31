# Revision-bound session reducer (WP17/WP27)

`Session.Reduce(Event)` extends the original persistent reducer. It owns one
immutable `document.Document`, token-gap cursor and qualified `document.History`;
normal and Reveal projections use that same revision. It executes no filesystem
IO and has no alternate text buffer, native serializer, terminal or worker.
Keep one authoritative state chain: deterministic operation numbers are local to
that chain, not global authentication tokens. Inspecting immutable values is safe
concurrently; executing intents from forked historical chains is not supported.

`New(Config)` captures independent Directory wrappers over the real opened
capability. Closing any copy closes that shared capability; no reopen or lifetime
extension is inferred. Returned `Source()`, `Document()`, `Snapshot().Pending`,
receipts and emitted intents are independent public wrappers/buffers. Reassigning
or clearing them cannot retarget accepted source, revision, location or request.
Arbitrary host error causes remain host-owned diagnostics; known top-level domain
failure records are copied. Callers must not mutate supplied arguments during a call.

## Typed command routing

- `Text` delegates actual ASCII Insert/Typeover; `Insert` toggles the original
  insertion mode in qualified contexts. Same-byte typeover moves the cursor
  without manufacturing native dirtiness. Prefix/resource/character/size refusals
  come from the actual document API. No paste/release/physical-key inference.
- `Delete`/`Backspace` delegate actual directional deletion. Normal code questions
  route distinct Yes/No/F1/Escape answers. ASCII Backspace grouping remains refused.
  `Block` starts a forward Reveal selection; Right extends it, Backspace asks the
  exact block question. Declines retain the block; separate F1 clears it. Selected forward Delete remains
  unqualified and explicitly refused; it is not aliased to Backspace.
- Editing F1 opens actual history preview; `Previous` and `Restore` represent
  original numeric2/1. Only preview F1 cancels it. `Preview(start,count)` returns
  the real overlay; `Present` continues to project the current native document.
  Preview/decline/cancel never serialize their labels into native bytes.
- Right reports the actual grouping separator. View/prefix/name/exit interleavings
  preserve history and invalidate unproved grouping. Document qualification stays
  authoritative: EC045 empty/unbrowsed pair deletion, arbitrary histories, extra
  WP40 Previous/repeat Restore, nonempty question declines and other shapes refuse.
  `HistoryCountKnown=false` is not an empty stack. Clearing/retrieving does not
  manufacture a fresh cross-document history: native editing remains independent,
  while later history commands explicitly refuse that unqualified lifecycle.

## Revision and IO composition

Snapshot exposes `NativeRevision`, `SavedRevision`, `Dirty`, `PublishedRevision`,
`PublishedName`, `Published`, selection, mode, preview index and history knowledge.
Numeric `Revision` advances for a different native revision, including body-equal
metadata repair; no-change commands leave it intact. Loaded source guard, current
revision, last published receipt and displayed filename are separate. Later Save As
changes the display name after matching success but never rebases the original
source guard. No source-less/NewPublication or new-document constructor is used.

Host executes the real APIs, then returns the same Operation/Revision/Kind:

| Intent | Actual host composition |
| --- | --- |
| Read | `Directory.Read(Name)` → Result.Document/Err |
| Observe | `Directory.Observe(Name)` → Result.Destination/Err |
| WriteSnapshot | `Directory.Save(Document,Destination,Decision)` → Outcome/Err |
| PublishCandidate | `p,err := Directory.PreparePublication(Document,Destination,Candidate,storage.PublicationID{Operation,Revision})`; if nil error, `Directory.Publish(p,p.ID())` → Outcome/Err |

All candidate fields are captured independently. Host code must execute the supplied
request as-is. An actual absent observation emits a separate numbered publication.
The reducer checks operation/revision/kind, name/root, candidate length/SHA and
possible inode/state shape. This detects malformed/forged envelopes; it cannot
independently authenticate a dishonest host's structurally valid fabricated IO
receipt. Storage remains the real freshness/capability/no-replace authority.

No-edit snapshots retain cross-directory Save support. Edited loaded-source
PreparePublication requires the approved same opened capability; an edited
cross-directory attempt reports its real InvalidRequest, never a second transaction.
Existing-target replacement refuses except actual unchanged same-source no-op.
Changed/current or earlier-published edited revisions cannot route through a
source-snapshot overwrite shortcut. Successful matching candidate saves alone
advance saved revision/name. Failed/uncertain operations retain dirty state and
previous published receipt, including candidate residue and DestinationMayExist.

While a write is pending, bounded typed text/mode/navigation commands may proceed
under the same ordinary command rules. The pending payload remains the older
candidate. Its later completion becomes a detached receipt and cannot mark newer
edits saved or rename them. CancelOperation is host detachment, not an original
key alias or proof of IO cancellation; a late publication may already exist.
Duplicate/stale/foreign envelopes cannot consume a different request. No automatic
exit/rollback follows any write result.

F10 names and F7 questions retain approved WP13 semantics. F1 returns from Save
question/name; Escape advances Save question to filename. Save-on-exit completion
remains unobserved/refused. Save No reaches Exit question; its F1 retains, No/Escape
clears, Yes exits. Dirty named buffers omit the unmodified notice. Generic Escape
cancel/repeat, overwrite, unnamed creation and full menu/edit/history families are
not inferred. Exact rooted prefixes are declared profiles, not DOS path emulation.

## Evidence and remaining scope

[evidence/wp27/report.md](evidence/wp27/report.md) binds original-derived component
sequences, native comparisons, source/ownership proofs and real checks. Tests use
approved APIs and original files; no new original VM run occurred. Eighteen approved
WP40 source/command paths reproduce literal original native output through this
actual reducer. This is component composition, not physical keyboard or executable
UI acceptance. WP28 and WP36 must consume these actual commands/intents; their
files are untouched. Original-resaved prefix564 remains mutation-refused here.
All38 requirements/91 groups/discovered leaves, wider history/edit/storage/native
variants, nonASCII/resource/DOS/graphics/physical obligations and full M1 remain
open. PDF belongs to M2 after genuine M1 acceptance.

Independent review I1 corrected the selected Backspace route and original-derived
replays. The historical cycle1 evidence is unchanged; the remediation and current
seals are in [evidence/wp27/fix-i1/report.md](evidence/wp27/fix-i1/report.md).
