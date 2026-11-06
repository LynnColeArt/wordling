# WP78 reference qualification report

Candidate reference evidence for independent review. This package changes research
and replay tooling only; it does not implement the editor or establish milestone
completion. Original 03/09/92 behavior remains the oracle. Full M1 stays open.

## Deliverables and custody

- `profile.json` pins release, environment, resources, measured settings, logical
  screen geometry and explicit Linux/terminal/resource adaptation boundaries.
- `journey-contract.json` maps EE-A01–13 and A15 to exact original trace/frame
  evidence, full character/attribute hashes, focus witnesses and scope limitations.
- `fixture-manifest.json` pins user-authored native documents and body bytes.
- `proofreading-contract.md` specifies the continuous proofreading workflow,
  formatted/wrapped corrections, per-invocation state, dictionary persistence and
  correction/history interaction.
- `qualification-manifest.json` covers all new raw research artifacts, including
  failures and superseded captures. `validation.json` records reproducible checks.

The original repeated r2/r3 and settings observations, backup extension and spelling
extension remain unchanged. A partial research checkpoint was committed as
61f54d5c01ac5c835c152409dd1368610106d777. Its PARTIAL.md is a historical checkpoint,
not the current guest state. Every private guest is stopped before final export.
Per-run source.json records source HEAD and dependency hashes at start; immutable
runner snapshots and replay scripts identify inputs. No app, master installation,
planning artifact, user preview or proprietary dictionary was changed by research.

## Evidence and precise interpretation

The F1 cancellation claim is now corroborated by fresh focus-r1/r2 runs. F1,
Escape and Space each remove exactly eight child-selection attribute bytes while
leaving the character grid unchanged; Up then opens parent Endnote. F7 closes the
menus and permits ordinary text. Treat retained drawing and active focus as
separate states. The r2/r3 original profile/settings files are integrity checked.

The three-page flow was repeated successfully with slower key delivery and
content checkpoints; FLOW.WP is byte-identical across both successful runs.
Native SRt=0D, HRt=0A, unbroken-word DSRt=90, and Underline ON/OFF three-byte codes
are explicit. Tab and D4 page-information records have observed native examples.
The default is Full justification, but editing status/grid use nominal character
advance: first wrapped-line End Pos7.3, next line6.8. Do not implement expanded
print justification by stretching the editing screen. WP81 must preserve this
distinction and qualify printed results independently.

Corrections continue across save/retrieve. The probes cover overlapping Bold and
Underline, active-format save/continued typing, pair boundary deletion, insertion
inside a run, block cancel/delete/default No, three-level Undelete, two screens,
Save Yes before exit and continued New documents. Per-key block evidence records
the original inclusive selection behavior, including the first Left selecting the
last character without the expected insertion-position decrement.

List Files includes the two real display layouts, multi-screen scroll, Name
Search, Look Next/Prev and return selection, child/parent traversal, F5 cached
list, and Retrieve from blank/occupied text. Directories are entered with Look6
and directory-template confirmation. A file must actually be selected with arrows;
End did not select the last file. Enter at `Retrieve into current document? No
(Yes)` returns to the list; Yes inserts at the current point. INSERT.WP pins the
result. Original Document size is not simply the saved file size (527 versus337
in the captured small example); Linux statistics must use a reviewed definition.

Backup collision is explicit: A.TXT and A.WP share A.BK!, and its content is the
previous overwritten destination. Refusal preserved destination and backup bytes
exactly. Disabling Original Backup then successfully replacing removes that BK!.
F7 Save Yes follows the same filename and replacement continuation; Enter declines
replacement and F1 cancels the returned filename prompt without discarding edits.
Timed recovery and crash/fault-injection effects are not inferred.

The proofreading contract adds multi-page scope, whole-word versus interior
attributes, SRt/DSRt and history to the earlier continuous proofing study.
Exact proprietary lexicon equivalence is not licensed or established by a few
suggestion examples. Provider admission and failure behavior remain real gates.

## Method, repeats and failures

`guest.start` verifies boot/disk, QEMU and firmware hashes before each private
copy. Guests are offline with no host shares. Raw VGA captures pause the guest
and retain 4000 bytes, pixels and paused status. BIOS cursor dumps are diagnostic
and are read just after resuming; the displayed position and next-key behavior
remain necessary focus evidence. Outputs are extracted with mtools only after
QMP socket disappearance. No binary resource is bundled as a fixture.

Original baseline has no mouse driver. `prepare_mouse.py` produces a separately
hashed private derived profile with FreeDOS CTMouse2.1b4, pinned provenance and
GPL2 metadata. It adds only the driver/startup line; master untouched. The run
repeats original File-menu clicking and distinguishes emulator mouse transport
from original app behavior. No CTMouse executable is checked in.

Failures are useful evidence, never acceptance frames: flow-repeat lost rapid
queued input; early flow01/02 were premature; menus04 was premature Help and
several nested-menu assumptions were wrong; files includes wrong guesses about
Short/Long confirmation, directories, Name Search and selection. Successful later
frames are individually indexed. The failed DOS FOR copy command is retained.
No expected state is fabricated from a label containing the desired outcome.

Flow-reliable began with loaded runner SHA
cedcc507a8ca78c1d2f2ab363e1ba4595f4e84f017e524556efc3610c112a83b.
Its startup runner-source.py is authoritative. During that process an unused
mouse branch was added to disk, so older per-action disk-based runner hashes can
name later source rather than loaded code. The final driver freezes loaded bytes
at import. This provenance limitation is disclosed, not silently rewritten.

Repeated successful evidence: r2/r3 core; backup enabled/disabled sequences;
focus-r1/r2; full flow/flow-reliable native equality; spelling main/repeat/
suggestions scopes; proof-boundaries/repeat native equality; corrections/history-
repeat deletion groups. Single additional bounded witnesses (such as shared-base
backup collision) are identified as such and are candidates for independent
replay, not relabeled as repeated experiments.

## Remaining product obligations and scope

EE-A13 exact untouched bytes, unsupported-edit rejection, preservation of unrelated
native content, races, late completions, temporary-write/replacement failures and
backup atomicity remain mandatory Linux implementation tests. Original no-edit
save changed one prefix housekeeping byte80 from00 to08 while retaining body;
this does not weaken product FC002 exact byte identity or authorize normalization.
The existing preservation corpus remains required. Terminal resize cannot alter
paper geometry or bytes. Physical key delivery remains separately qualified.

This reference package supplies original observations to WP79–89 and final WP86;
all product_evidence/reviewer_verdict fields are intentionally empty. Linux path
projection, statistics, settings storage and canvas geometry policies need their
own reviewed implementations. No historical unavailable capability is silently
called complete, and no hash/fixture-name whitelist may replace general behavior.

## Narrow gap closure: Reveal scrolling and failed Search

`scroll-search-r1/r2` start from independently copied verified images. A disclosed
fixture-only derivative adds the already authored FLOW.WP to OUT; it does not
alter application/resources/settings. Both runs read the displayed release,
retrieve this fixture, toggle Reveal and capture PageDown to2/3, PageUp to2,
HomeHomeDown to the end, fourteen Down steps from the start, and closing Reveal.
Upper and lower panes, physical status and BIOS diagnostics are retained. No
native editing or saving occurs; the exported FLOW.WP remains byte-identical.

The usual 1.5-second settled capture missed a transient Search result. The narrow
probe dispatches F2 without the ordinary key/capture delay and takes a bounded
burst of paused VRAM/pixel snapshots. It witnesses exact `* Not found *` at
row24 in normal view and row11 in Reveal, columns0–12 using attribute0x1f. Later
settled frames restore status and editing focus. The burst records host elapsed
time, not a CPU-cycle or guaranteed duration contract. This resolves the previous
missing-wording gap without guessing text from a modern UI or a manual alone.

All raw PPM derivatives, including 23 older backup PPMs outside that extension's
original immutable manifest, are inventoried in the final qualification manifest.
Their original PNG/VRAM identities remain unchanged. The inventory records them
as screenshot derivatives, not additional independent observations.

## Verification and handoff

`python3 -m py_compile scripts/reference/everyday/*.py` passes. The contract
compiler indexes 303 individually selected frames and 45 native authored files.
The validator verifies all original manifests (164 baseline, 113 backup and 293
spelling entries), profile references, frame character/attribute grids, native
bytes, repeated focus/flow/formatted proofing/scrolling/Search results, refusal
and shared-basename backup outcomes, and shutdown-before-export custody. Full
results are in validation.json. All 2,796 artifacts in the final inventory are
hash checked, including raw failed observations and replay sources.

No Go source changed, so Go build/test/vet are not a research verification claim.
Replay scripts were actually executed against the private original. Whitespace
checks apply to authored Markdown/Python/JSON; raw DOS directory output and
screen.txt deliberately retain reference whitespace/25-row structure.

Charter code-review-checklist context was requested with the supported public
command. The runtime reported that this charter has no authored checklist
section; the issued package, charter, compatibility and milestone requirements
remain the review basis. No checklist or approval was fabricated. Independent
review must inspect this candidate and record its own verdict before dependent
packages consume it. The previous baseline candidate's source presence was never
used as evidence that the Wordling feature works.
