# WP06 file and Linux platform contracts

Research handoff, 2026-10-30, for file/session implementers and the M1 planner.
Requirements: FR-006, FR-007, FR-017, NFR-002, C-006; permanent FC-001–010.
Authority: mission `spec.md`, `plan.md`, `data-model.md`, `docs/compatibility.md`,
`docs/roadmap.md`, ADR0002 and approved WP05 `coverage-concordance.md`.
This is a bounded investigation and first-workflow proposal, not full original
file-operation or Linux adaptation acceptance. Full parity remains M1; PDF is M2.
WP12 owns executable continuation packages; this document creates none.

## Source and evidence boundary

REF51 is the pinned MNUS1WP51X1C-6/92 reference. SDK51 is
MNUSXTW511-12/93 with intermediate WP revision marks; its field meanings do not
prove all later/platform variants exist in the March DOS executable. Exact file
hashes and editions appear in the ledger and `docs/research/sources.json`.
REF51 PDF pages below are one-based and equal printed Arabic page+17; endpoints
are inclusive. This investigation used local sources only. No manual, resource,
original output or source registry is modified or newly redistributed.

The selected original is plain U.S. English WP5.1 DOS dated1992-03-09, in the
fingerprinted QEMU/FreeDOS profile with July1992 Standard Printer. This is not
historical DOS, network/graphics parity or proof of every original error branch.
The reference-release choice is an engineering selection under authorized
research, not an owner exclusion of other language or compatibility obligations.

The matrix distinguishes:

- **Partially observed original recipe:** exact traces/screens/native outputs
  support only that branch, repeated from fresh copies. No Wordling comparison.
- **Documentary / not-run:** original manual expectations and candidate cases,
  not executed evidence. Canonical case status remains not-run.
- **Indexed/investigation:** required behavior has unresolved semantics/resources.
- **Wordling integrity obligation:** FC/NFR requirements may be stronger than an
  original application's incidental rewrite behavior. Native no-edit identity is
  required of Wordling; original WP no-edit-save identity is not assumed.
- **Engineering proposal:** a Linux/UI/storage slice to test and review; not an
  owner-approved scope change or original-app observation.

Canonical case titles/feature associations are copied as metadata from the
hash-pinned registries, not inferred from neighboring IDs. Empty case cells
mean no dedicated scenario for that row; broad parent coverage is not invented
mode-specific evidence. The embedded validator binds every matrix case title,
feature association, source locator and evidence status to its canonical record.

## Original file/conversion/platform matrix

Each row is a bounded contract plus explicit remaining work. Known observations
are FP02/FP03; all other listed cases remain unexecuted as full canonical cases.
The incidental DOS COPY in FP03 prepares a fixture and does not verify FP22.

| Row / family | REF51 printed / PDF | Features and canonical case leads | Evidence | Contract; remaining work |
| --- | --- | --- | --- | --- |
| FP01: Retrieve into blank or existing document | 554–557 / 571–574 | WP51-019; CMD51-065 (Retrieve inserts at the cursor) | documentary; dedicated case not-run | Shift+F10 asks filename and retrieves at cursor. Blank-screen retrieval retains incoming initial codes; insertion into existing document adopts on-screen initial settings. File-not-found redisplays editable name after error. List Files insertion has its own confirmation. **Remaining:** Need saved before/after insertion, code boundaries, cancel, missing/wrong-type/initial-code branches. First UI slice supports blank-screen no-edit acquisition only; insertion remains M1 work. |
| FP02: New document F10 save | 565–566 / 582–583 | WP51-020; CMD51-066 (Name a new document with F10) | partially observed original recipe | Captured Document to be saved prompt; enter C:\OUT\NEWTEST, Enter; native WORDLING TEST output and editing continue. **Remaining:** A new Wordling native writer is not supplied by copying an existing snapshot. Full filename/long-name/resource variations and failure modes remain. |
| FP03: Overwrite refusal and filename cancellation | 566–566 / 583–583 | WP51-020; CMD51-067 (Decline overwriting an existing file) | partially observed original recipe | After saving ORIGINAL as SAME, append MODIFIED. F10, Enter, n at Replace returns to filename prompt; F1 returns to changed ORIGINALMODIFIED buffer. SAME equals pre-edit BEFORE byte-for-byte. **Remaining:** Only this refusal/cancel branch observed; do not infer successful overwrite, no-edit original-save bytes or all cancel contexts. |
| FP04: Approved overwrite and filename editing | 565–566 / 582–583 | WP51-020; CMD51-068 (Approve overwriting an existing file); CMD51-069 (Edit the displayed save filename); CMD51-070 (Typing a save filename starts a new name) | documentary; dedicated cases not-run | Existing name appears at save. Enter requests replacement; y permits it. A character starts a fresh name; cursor/edit keys can edit the displayed name before typing that character. **Remaining:** Need approved replacement with backup/Fast Save settings; cursor-key and first-character name edits; unusual/colliding filenames. WP03 refuses actual replacement. |
| FP05: No-edit and failed-save integrity | 565–566 / 582–583 | WP51-020; CMD51-149 (Preserve an untouched native file byte for byte); CMD51-150 (Reject an unsafe opaque-structure edit before replacement); CMD51-151 (Preserve unrelated native data after a supported edit); CMD51-152 (Retain original after a failed save) | Wordling compatibility requirements; canonical cases not-run | FC-002 demands exact no-edit bytes; FC-003/004 preserve unrelated/unknown structures or refuse unsafe edits. FC-009/NFR-002 require explicit failure without damaging original. REF Save is contextual, not proof original WP saves untouched bytes identically. **Remaining:** Storage foundation and later writers need distinct acceptance. Interrupted publication, ambiguous outcomes and power loss must not be called successful or silently rolled back. |
| FP06: Original backup | 41–43 / 58–60 | WP51-021; CMD51-071 (Enable original-document backup) | documentary; dedicated case not-run | Replacement with Original Backup enabled rotates prior version into same-directory base-name .BK! artifact. Different extensions of same base share it; subsequent replacement updates the backup. Turning off the option deletes the backup at next save. **Remaining:** Capture exact names/extensions/collisions, rotation, settings and failure ordering; preserve old backup/original on failed attempted replacement until tested semantics are established. |
| FP07: Timed backup | 43–44 / 60–61 | WP51-021; CMD51-072 (Configure timed backup); CMD51-073 (Empty editing screen does not create a zero-byte timed backup) | documentary; dedicated cases not-run | Timed Backup interval is in minutes; backup location is configured separately from the native save destination; normal exit deletes timed backups. It is distinct from original-version backup and explicit Save. **Remaining:** Blank-document suppression and exact timed filenames, both screens, clock/suspension/space failures need fixtures and original observations. |
| FP08: Startup recovery | 44–44 / 61–61 | WP51-021; CMD51-074 (Startup checks backups for both document screens) | documentary; dedicated case not-run | Old Backup 1/2 prompt offers Rename or Delete; Rename retains recoverable content under a user-chosen name. Do not equate recovery with unlimited editor undo. **Remaining:** Test both document screens, names/bytes, cancel and interrupted recovery. No automatic candidate cleanup or new recovery sidecar is approved. |
| FP09: Fast Save | 197–197 / 214–214 | WP51-022; CMD51-075 (Disable Fast Save before saving) | documentary; dedicated option case not-run | Fast Save stores unformatted/deleted settings; disabling formats/purges obsolete information. Manual warns original save/fast-save/print-from-disk may need two copies worth of free space. **Remaining:** Original corpus deleted packets are incidental evidence, not an exercised setting toggle. Test on/off, purge/format effects and disk exhaustion. Never normalize Wordling no-edit images to imitate an original formatting pass. |
| FP10: File list, directory and resource operations | 114–119 / 131–136; 347–354 / 364–371; 358–361 / 375–378 | WP51-023; CMD51-076 (List files with a filename pattern); CMD51-077 (Copy a listed file); CMD51-078 (Rename a listed file); CMD51-079 (Decline deleting a file from List Files); CMD51-080 (Toggle long/short file display); CMD51-081 (Disable file-list sorting in March 1992) | documentary; dedicated cases not-run | F5 provides filename-pattern list, copy/move/rename/delete/long-short views and default-directory controls. March Sort List Files setting has documented directory-order/Name Search effects. **Remaining:** Exact prompts, wildcard/case/DOS ordering, overwrite/collision/permission failure, list printing and cancellation need probes. File deletion is not document Undelete. |
| FP11: Password lock and associated artifacts | 362–363 / 379–380 | WP51-024; CMD51-082 (Set a document password) | documentary; dedicated case not-run | Password Add/Change requires two hidden entries and save to take effect; Remove also requires save. Related temporary/backup artifacts are documented locked. Wrong password refuses retrieval. **Remaining:** No encrypted fixture/decryption or encrypted auxiliary-format support established. Password encryption is separate from shared-file access locking; do not implement one as the other. |
| FP12: DOS text input modes | 685–688 / 702–705 | WP51-025; CMD51-083 (Import DOS CR/LF as hard returns); CMD51-084 (Import DOS text using hyphenation-zone soft-return mode) | documentary; dedicated cases not-run | Ctrl+F5 distinguishes CR/LF to Hard Return from CR/LF to Soft Return in the hyphenation zone. Margins/zone and repeated newline runs affect conversion. **Remaining:** Need literal byte fixtures for CR/LF, repeated empty lines, extended characters and malformed/nontext input. No blanket newline normalization. |
| FP13: DOS, Generic, 5.0 and 4.2 exports | 685–688 / 702–705; 138–142 / 155–159 | WP51-025, WP51-026; no dedicated scenario | documentary; no dedicated export-mode case in these groups | Text Out DOS removes/reifies formatting according to original mode; Generic retains layout using spaces/tabs/CRLF; 5.0 preserves unrecognized 5.1 codes as Unknown, while 4.2 mapping may delete unsupported codes and uses .CRS. F10 after text input saves native format, not text. **Remaining:** Author mode-specific cases and original outputs/loss declarations. Documented character254 fallback is an original conversion loss, never native-save permission for silent replacement. Password 5.0/4.2 differences need explicit fixtures. |
| FP14: Legacy native input conversion | 130–142 / 147–159; 556–556 / 573–573 | WP51-026; CMD51-157 (Retrieve an original 4.2 document into 5.1) | documentary; dedicated case not-run | Retrieve converts older 4.2/5.0 files to 5.1. Conversion is separate from byte-identical supported 5.1 snapshot acquisition. **Remaining:** Acquire original legacy fixtures and .CRS/resources as applicable; keep input unchanged, declare losses/errors and independently test outputs. |
| FP15: Standalone CONVERT utility | 89–95 / 106–112 | WP51-079; no dedicated scenario | indexed/documentary; no dedicated CONVERT case in this group | The original conversion utility remains M1; its supported modes, switches and artifact formats must be enumerated from its own section. **Remaining:** Do not cite the cursor case as conversion evidence; create per-format conversion probes with lawful test inputs, failure/log outputs and exact settings. |
| FP16: Macro and graphics converters | 370–372 / 387–389; 228–231 / 245–248 | WP51-061, WP51-056; CMD51-179 (Convert a 4.x macro with MACROCNV); CMD51-175 (Convert an original graphics file with GRAPHCNV) | documentary; dedicated cases not-run | MACROCNV and GRAPHCNV produce original automation/graphics representations through distinct conversion procedures. **Remaining:** Need source-version inputs, option/loss behavior and original reopening; these converters are not a dependency of native document Save. |
| FP17: Spreadsheet import and links | 606–615 / 623–632 | WP51-065; CMD51-136 (Import a declared spreadsheet range); CMD51-137 (Create a spreadsheet link) | documentary; dedicated cases not-run | Spreadsheet import and persistent links have distinct source range/update/resource behavior. **Remaining:** Use original spreadsheet fixtures and preserve original link relationships. No invented CSV/intermediary format may replace required original formats. |
| FP18: Document comments and compare | 124–129 / 141–146 | WP51-027; CMD51-158 (Create a nonprinting document comment); CMD51-159 (Compare screen and disk document versions) | documentary; dedicated cases not-run | Comments are native nonprinting content; compare adds original redline/strikeout semantics using screen/disk versions. **Remaining:** Need cancellation, source preservation and original printed/native evidence; never treat comments as disposable unknown bytes. |
| FP19: Look and Find | 197–202 / 214–219; 364–368 / 381–385 | WP51-028; CMD51-085 (Find files by content); CMD51-086 (Display file contents through Look) | documentary; dedicated cases not-run | Look inspects without retrieving into current document; Find searches declared filename/content conditions. **Remaining:** Need encrypted/access-denied cases, search conditions and long/short/list interactions. Reading a file is not authorization to modify it. |
| FP20: Document summary and long names | 145–149 / 162–166; 565–566 / 582–583 | WP51-090; CMD51-088 (Commit a document summary); CMD51-089 (Cancel summary changes) | documentary; dedicated cases not-run | Descriptive long name/type metadata is distinct from DOS basename. Summary acceptance versus F1 cancellation must be separately preserved. **Remaining:** Need source-native fields, encoding, name/type prompt settings and filename collisions. Linux long filenames are not a substitute for original summary metadata. |
| FP21: Exit, clear and save decisions | 194–196 / 211–213 | WP51-029; CMD51-087 (Exit without saving and cancel application exit) | documentary; dedicated cancel-exit case not-run | F7 exit/save/clear/switch choices depend on document and second-screen state. Existing probe clean exits use a different bounded branch. **Remaining:** Do not infer buffer-clearing or cancel behavior for F7,n,n from F7,n,y evidence. Probe each relevant state before implementing irreversible buffer discard. |
| FP22: DOS and Shell integration | 150–156 / 167–173; 225–227 / 242–244 | WP51-078; CMD51-189 (Run a DOS command and return to the same cursor) | documentary; dedicated case not-run; incidental guest COPY in overwrite recipe | Ctrl+F1 DOS Command is used as fixture preparation in the refusal recipe. Dedicated read-only command/cursor-return behavior remains not-run. **Remaining:** A Linux child-shell mapping needs command/context/environment/return semantics; never pass a DOS command string straight to a Linux shell and claim equivalence. |
| FP23: Cursor and screen-capture utilities | 105–108 / 122–125; 567–570 / 584–587 | WP51-079; CMD51-190 (Choose an original cursor appearance) | documentary/indexed; cursor case not-run; no capture-utility case | Original cursor appearance and DOS screen capture utilities remain tracked separately from app snapshot tooling. **Remaining:** Declare terminal capabilities and equivalent meaningful controls; no claim a Linux terminal executes DOS hardware calls. Create a dedicated capture-utility contract. |
| FP24: Startup and memory/resource options | 415–417 / 432–434; 897–904 / 914–921 | WP51-080; CMD51-191 (Start WP with a declared macro) | documentary; dedicated case not-run | Startup macro and memory/resource switches must preserve original resolution/session behavior under an explicit Linux adaptation. **Remaining:** Probe actual switch spelling, resource paths, document2 flags and failure behavior; do not blindly forward DOS memory addresses/options. |
| FP25: Network and shared-file access | 921–960 / 938–977 | WP51-081; CMD51-192 (Investigate shared-file access with separate user setups) | indexed/investigation; no resolved conflict policy | Original network installation separates shared resources and personal settings; exact multi-user retrieval/save/lock decisions remain unresolved in the canonical case. **Remaining:** Need two-user original environment/rights and native artifacts. POSIX locks or local stale-source checks alone do not establish original network locking. No unsupported-network exclusion from M1. |
| FP26: Original print-to-disk output | 543–543 / 560–560 | WP51-074; CMD51-145 (Direct original printer output to a disk file) | documentary; dedicated case not-run | Original printer-language output must retain selected printer/resource behavior; it is separate from DOS Text, Generic and native Save. **Remaining:** Needs calibrated printer definition/output comparison. PDF is an optional M2 export and cannot replace this M1 mode. |
| FP27: PIF and OS integration context | 961–962 / 978–979 | WP51-078, WP51-080; no dedicated scenario | indexed; no dedicated PIF scenario | PIF integration is an original platform dependency needing explicit Linux applicability/mapping study, not automatically discarded as a Windows-associated source section. **Remaining:** Enumerate actual purpose/fields and user-visible invocation first. Any proposed removal/changed parity baseline requires an owner scope decision; none is supplied here. |

Original text/export behavior needs special care. REF51 printed687–688/PDF704–705
documents DOS export removing codes, reifying fields and losing some structures;
Generic uses its own space/tab/return rules. Some characters become character254
in original export modes. These are documentary mode-specific losses to declare
and test, never permission to replace native characters silently. Original .CRS,
macros, graphics, printer output and native files retain their own original
formats. No conversion through another word processor may implement native Save.

Password encryption, network sharing/conflict locks, editor Block Protect and
Linux access permissions are different mechanisms. A successful local immutable
read or stale-source check proves none of the other three. Original .BK! backup
rotation and timed recovery are not modern unlimited undo or a private required
Wordling sidecar. Temporary storage candidates are not original backup artifacts.

## Exact observed save/refusal sequence

The ledger pins four run manifests, six native files and ten screen captures.
The six originals are one new-save output per smoke run and SAME/BEFORE per
extended run. The host `.WP5` suffix is an extraction label; original scratch
names NEWTEST, SAME and BEFORE had no extension. These are project-authored
scratch contents from the original app, not bundled sample files.

| Step | Original input/state | Observed result and evidence |
| --- | --- | --- |
| O1 | Fresh document, type WORDLING TEST; F10 | Smoke02/03 FP02 `save-prompt` shows `Document to be saved:`. |
| O2 | Enter original DOS pathname C:\OUT\NEWTEST, Enter | FP02 `saved` retains text/editing; exported NEWTEST.WP5 is337bytes, body offset324, body `574f52444c494e472054455354`, SHA-256 `a42b87e3441dc422c5a348e5b6838e5949a3dabedddf49e947f784408db0dff6`. No Wordling new-document writer follows from this observation. |
| O3 | Type ORIGINAL, F10 save as SAME; guest DOS COPY SAME to BEFORE | FP03 trace records the preparation; source and comparison file are native originals. |
| O4 | Append MODIFIED; F10, Enter accepts displayed SAME | FP03 `replace-prompt` captures the replacement question. Approval branch is not executed. |
| O5 | Type n | FP03 `different-filename-requested` returns to `Document to be saved:`. No successful-save claim is made. |
| O6 | F1 at that filename prompt | FP03 `unsaved-buffer` contains ORIGINALMODIFIED. Disk SAME and BEFORE both remain332bytes and SHA-256 `22699462e095ce1a68ee016eb821210d194436b1c248908957db08db5fd46c62`; body is ORIGINAL. |

Each output pair repeats byte-identically across the two runs of its recipe.
The changed in-memory buffer is evidenced by screen capture; no saved native
ORIGINALMODIFIED output is claimed. The clean-exit branch in the extended recipe
is F7,n,y; it is not evidence of the dedicated cancel-exit F7,n,n branch in FP21.
F1 at Retrieve, backup/recovery, conversion, exit or a replacement question is
not established by F1 at this specific filename prompt.

## Storage foundation versus original Save

WP03's concurrently developed local storage foundation supports an observed
absent destination published atomically without replacement, and an explicit
existing-destination decision followed by verified same-file **no-edit no-op**.
Actual replacement of an existing file is refused even with overwrite permission;
another inode with identical content is still an actual replacement. These are
bounded engineering safety behaviors awaiting their own review/integration,
not original F10/backup/Fast Save/locking parity or owner-approved exclusions.

No-edit export must remain the exact owned input, including unknown packets,
body functions, padding and suffix data. A new destination publishes that
snapshot, not a newly authored native document. Same-file no-op checks identity/
bytes and does no disk rewrite; it cannot exercise original backup rotation,
purge/format state, replacement failure order or metadata changes. A future
semantic writer must justify all affected offsets/relationships and original
reopen/edit/print/save outcomes separately.

Snapshot freshness is checked at defined observations, not guaranteed against
all later external writes. New-name publication can become uncertain after a
link/verification/cleanup error: the destination may exist and a temporary
candidate may remain. UI must distinguish uncertainty from success or clean
cancellation; it must not blindly retry, overwrite, erase another writer's file,
or claim crash durability. Original-source integrity and uncertain new-destination
outcomes are separate invariants. No fsync/power-loss or hostile shared-directory
security claim is made by this foundation.

## First no-edit Retrieve / Save / Cancel workflow

This is a proposed initial UI integration contract under the full M1 scope.
It implements a narrow supported path and visibly refuses remaining functions;
it does not redefine original Retrieve as always replacing the editing buffer.
Normal original retrieval inserts at the cursor (FP01). First integration accepts
retrieval into a blank document only until insertion/initial-code semantics and
native writers are ready. An existing on-screen document must not be silently
cleared. Plain selected fixtures may be shown; unknown semantic content must be
identified as unsupported for editing rather than displayed as disposable text.

State comprises active owned image, source identity, selected/default name,
current directory context, prompt context, pending destination observation and
explicit decision. Candidate creation/publication is below the UI; rendering
never serializes the document. Paths are supplied through a declared validated
local-directory context in the first slice, not inferred DOS drive mappings.

| State/event | Required transition / boundary | Evidence classification |
| --- | --- | --- |
| Blank; Shift+F10 or File/Retrieve | Enter filename prompt; retain prior state until complete supported read succeeds. | Original command documentary FP01; blank-only support is an initial engineering restriction, not parity acceptance. |
| Retrieve prompt; F1 | Return to previous blank/active state with no file or document mutation; discard pending name/read. | Proposed cancellation invariant; exact original Retrieve-cancel wording/state still needs probe. |
| Retrieve prompt; Enter name | Resolve declared local context, acquire/validate supported native image; only then adopt it. Missing/unreadable/malformed/encrypted/unsupported input leaves previous state intact with explicit failure. Original file-not-found retry/edit behavior requires source-specific UI checks. | Native validation/integrity obligation plus documentary FP01. Initial-code cursor placement and arbitrary code rendering remain gated; do not guess them from byte offsets. |
| Active unchanged image; F10 | Open original-style filename prompt with current name/default context. Do not write on opening the prompt. | Documentary FP04; exact name editing/mode behavior still needs original probes. |
| Save filename prompt; F1 | Cancel pending save decision/observation and return to current buffer. Disk bytes unchanged; do not claim saved. | Observed for the FP03 changed-buffer branch; unchanged-buffer generalization is an engineering test obligation. |
| Name accepted; destination absent | Bind observed destination and request storage no-replace publication of exact owned bytes. Success returns to active unchanged state; raced destination/source or partial/uncertain outcome is explicit. | Proposed integration with WP03; native copy integrity is not FP02's new-document writer parity. |
| Name accepted; destination exists | Ask replacement decision before requesting any effect; n returns to filename prompt. y permits checking the requested operation but cannot make unsupported replacement safe. | Refusal branch observed FP03; y branch documentary/unverified FP04. |
| Explicit y; verified destination is still the same source file and image unchanged | Storage may report verified unchanged with no rewrite. Return to active state; do not simulate backup/Fast Save work. | Engineering no-op path; no original overwrite acceptance claim. |
| Explicit y; different existing file, or edited snapshot requiring replacement | Return explicit unsupported-replacement outcome, retain current buffer and both disk files; allow another name or cancel. | Interim refusal; original approved overwrite remains required M1 work. |
| Failure or ambiguous publication | Retain image, expose failure/uncertain destination state, re-observe before any retry; preserve original files. Cancellation after publication starts cannot promise no destination exists. | NFR-002/FC-009 and storage outcome contract, not original tested wording. |

The initial UI must not offer semantic editing/new-document saving as implemented
by a pass-through export. Unsupported insert/overwrite/backup/locking/conversion
commands remain visible with explicit status, not silently replaced by host
file dialogs or deferred into M2. User-visible wording beyond captured original
prompts must be labelled as proposed until compared with the reference.

## Linux adaptation classification

The owner's settled direction is Linux, Go/Bubble Tea, original native/companion
formats, full original M1 scope, and M2 PDF after acceptance. Decision records
DM-01M64CWKX056PQDXX2D3QW7QR0 and DM-01M64E57M11DW3X26VZBBJ6KRS, the roadmap
and ADR0002 are pinned inputs. They do **not** approve the mappings below,
network/graphics/language exclusions, renamed original files or a reduced save
contract. Engineering restrictions may bound an intermediate implementation
while keeping all remaining obligations queued. An actual exclusion/baseline
change needs an explicit owner decision; no new such decision is made here.

| Area | Proposed Linux approach | Still required test / decision boundary |
| --- | --- | --- |
| DOS drives/default directories | Use explicit configured drive/directory associations and original directory/default-resolution semantics; keep native path strings distinct from host paths. First slice uses a supplied pinned local directory and basename. | Test drive-relative versus absolute paths, current directory on each drive, resource locations, unavailable mounts and errors. Configuration model is proposed, not selected/accepted. FP01/FP10/FP24. |
| Case, 8.3 and descriptive names | Preserve source spelling; detect case/8.3 collisions explicitly rather than silently uppercasing/truncating or treating a Linux long basename as native descriptive metadata. | Test legal/reserved names, extensions, wildcard matching, ordering and Unicode/encoding. Original summary long names/types need their own native fields. FP04/FP10/FP20. |
| Symlinks/nonregular files/parent changes | First storage slice pins a validated local directory and refuses final symlinks/nonregular objects; basename limits are Linux safety policy, not original DOS format limits. | Test identity swaps and path races under declared local scope. Resolve broader path semantics later; do not claim DOS had Linux symlink semantics or remote mounts are automatically detected. |
| Function/modified keys and terminal input | Normalize proven terminal sequences into original command identities; preserve F10, Shift+F10, F1 and menu routes. Diagnose unavailable/ambiguous keys instead of routing a different command silently. | Capture actual terminal/key capability matrix, resize/escape ambiguity and user key configuration. A shortcut fallback is an adaptation proposal, not original keyboard parity. |
| DOS/Shell | Separate original command/menu state from a proposed Linux child-process environment and restore session/cursor on return. Never claim a DOS command string has the same meaning in a Linux shell. | Probe original DOS/Shell variants, environment, working directory, exit/failure/terminal ownership, missing executables and external mutation. Generic host-shell substitution is not accepted. FP22/FP24. |
| Network/shared settings | Keep shared original resources and private per-user configuration distinct; design conflict detection/locking only after original two-user probes. | Local stale-source checks and POSIX flock are insufficient evidence. Declare validated filesystem scope; unknown network semantics cannot inherit local guarantees. FP25 remains unresolved M1, not excluded. |
| Recovery/permissions/storage | Map failures explicitly while retaining original backup/recovery formats and user choices. Private publication candidates are transient implementation artifacts, never required native sidecars. | Test full disk/permissions/short writes, cleanup and uncertain publication, both-screen startup backups, recovery and metadata. Exact power-loss guarantees require independent work, not implied atomic visibility. FP05–FP09. |
| PIF/hardware/memory utilities | Study actual user-visible purpose before proposing Linux equivalents; preserve meaningful startup/display/resource control. | FP23/FP24/FP27 require independent applicability contracts. Removing a required original function or changing baseline scope requires owner adjudication, not a terminal limitation assumption. |

## Bounded follow-up proposals for WP12

These are proposals inside this owned artifact, not executable packages:

1. **Retrieve boundaries (FP01):** blank versus insertion and initial codes;
   missing-file retry/name edit/cancel; before/after native outputs and source
   preservation. Add explicit cases for unrepresented branches.
2. **Save decisions (FP02–FP05):** reproduce the existing refusal fixture first;
   probe approved replacement and filename keys with declared backup/Fast Save
   settings. Integrate only supported snapshot/no-op paths initially; implement
   actual replacement only after its transaction and original artifacts are tested.
3. **Backup/recovery/Fast Save (FP06–FP09):** separate original-version rotation,
   timed two-screen backup and startup recovery, then formatting/purge modes.
   Capture names/bytes/settings, pre-existing backup collisions and failures.
4. **File management (FP10/FP19/FP20):** one list/rename/delete/find/look/summary
   family per package, with qualified canonical cases and original error/cancel
   behavior. Native metadata and host names must remain distinct.
5. **Encryption and shared access (FP11/FP25):** independent original fixtures,
   password-associated artifacts and two-user network context. Never infer the
   encrypted codec or network lock protocol from local filesystem safety.
6. **Conversions (FP12–FP17/FP26):** one original mode/utility/version per package;
   committed lawful input/provenance, untouched source, exact output/loss policy,
   original reopening or printer-language comparison. Add missing export and
   CONVERT cases; retain conversion resources such as .CRS outside public commits.
7. **Platform/session (FP21–FP24/FP27):** one key/path/shell/startup/utility mapping
   per package, declared environment and original probes. Record adaptation ADRs;
   escalate actual scope changes to the owner while continuing independent work.

Every family needs failures that preserve original bytes and report truthful
outcomes, independent original comparisons, and source/resource provenance.
Changed Go requires build/test/vet; changed binary decoding requires malformed/
fuzz checks; semantic writers require original retrieve/edit/print/save and
unrelated-byte checks. Documentary study or a no-edit copy cannot close these
families or approve full M1.

## Audit ledger

Source hashes pin the exact canonical links/statuses and approved prior research.
Evidence records pin the untouched original bytes/screens against their run
manifests. Matrix data is structured solely for this research validation and is
not a new application or file format.

<!-- WP06_AUDIT_BEGIN -->
```json
{
  "schema_version":1,
  "work_package":"WP06",
  "source_inputs":[
    {"path":"docs/research/feature-inventory.json","sha256":"49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"},
    {"path":"docs/research/command-scenarios.json","sha256":"a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"},
    {"path":"docs/research/sources.json","sha256":"850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"},
    {"path":"docs/research/reference-baseline.json","sha256":"6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"},
    {"path":"docs/research/reference-environment/environment.json","sha256":"30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"},
    {"path":"docs/research/reference-environment/resource-profile.json","sha256":"e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"},
    {"path":"docs/compatibility.md","sha256":"98014cd41863f1d38186b45391408455f9410fd35ab88ff1f75bfc03c8a5f27a"},
    {"path":"docs/roadmap.md","sha256":"23b273639792f223097111526f2655fa3261c20539bf8714e524c3d61a3eca29"},
    {"path":"docs/decisions/0002-lossless-native-boundary.md","sha256":"29a97ba0379e35e9d20ada3d35609324a2f24fb9a49b9dde194f8d2a7099b325"},
    {"path":"kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md","sha256":"e2abc5792811326bab19b2d3edced4ccd7a72e26fc84c59d320fac1949c45919"},
    {"path":"kitty-specs/wp51-parity-01M64CVY/decisions/DM-01M64CWKX056PQDXX2D3QW7QR0.md","sha256":"f4b73eae1c5a6fe3222d89dd5aae2969ec9cc2fdc4187b281bf965020753eb7b"},
    {"path":"kitty-specs/wp51-parity-01M64CVY/decisions/DM-01M64E57M11DW3X26VZBBJ6KRS.md","sha256":"f338b13585947f0b1613bb37f865128c3a2e6ced85c17f07a4e6d037b61ca72c"},
    {"path":"research/cache/WPDOS51Reference.pdf","sha256":"ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531","source_id":"REF51","edition":"MNUS1WP51X1C-6/92 (copyright leaf; scan, OCR duplicated in places)","redistribute":false},
    {"path":"research/cache/WP51DevelopersToolkit.pdf","sha256":"5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754","source_id":"SDK51","edition":"MNUSXTW511-12/93; WP subsection carries intermediate revision marks","redistribute":false}
  ],
  "rows":[
    {"id":"FP01","topic":"Retrieve into blank or existing document","feature_ids":["WP51-019"],"case_links":[{"case_id":"CMD51-065","feature_id":"WP51-019","title":"Retrieve inserts at the cursor","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":554,"printed_end":557,"pdf_start":571,"pdf_end":574}],"evidence_basis":"documentary; dedicated case not-run","contract":"Shift+F10 asks filename and retrieves at cursor. Blank-screen retrieval retains incoming initial codes; insertion into existing document adopts on-screen initial settings. File-not-found redisplays editable name after error. List Files insertion has its own confirmation.","remaining":"Need saved before/after insertion, code boundaries, cancel, missing/wrong-type/initial-code branches. First UI slice supports blank-screen no-edit acquisition only; insertion remains M1 work."},
    {"id":"FP02","topic":"New document F10 save","feature_ids":["WP51-020"],"case_links":[{"case_id":"CMD51-066","feature_id":"WP51-020","title":"Name a new document with F10","oracle_status":"partially-observed"}],"source_id":"REF51","locators":[{"printed_start":565,"printed_end":566,"pdf_start":582,"pdf_end":583}],"evidence_basis":"partially observed original recipe","contract":"Captured Document to be saved prompt; enter C:\\OUT\\NEWTEST, Enter; native WORDLING TEST output and editing continue.","remaining":"A new Wordling native writer is not supplied by copying an existing snapshot. Full filename/long-name/resource variations and failure modes remain."},
    {"id":"FP03","topic":"Overwrite refusal and filename cancellation","feature_ids":["WP51-020"],"case_links":[{"case_id":"CMD51-067","feature_id":"WP51-020","title":"Decline overwriting an existing file","oracle_status":"partially-observed"}],"source_id":"REF51","locators":[{"printed_start":566,"printed_end":566,"pdf_start":583,"pdf_end":583}],"evidence_basis":"partially observed original recipe","contract":"After saving ORIGINAL as SAME, append MODIFIED. F10, Enter, n at Replace returns to filename prompt; F1 returns to changed ORIGINALMODIFIED buffer. SAME equals pre-edit BEFORE byte-for-byte.","remaining":"Only this refusal/cancel branch observed; do not infer successful overwrite, no-edit original-save bytes or all cancel contexts."},
    {"id":"FP04","topic":"Approved overwrite and filename editing","feature_ids":["WP51-020"],"case_links":[{"case_id":"CMD51-068","feature_id":"WP51-020","title":"Approve overwriting an existing file","oracle_status":"not-run"},{"case_id":"CMD51-069","feature_id":"WP51-020","title":"Edit the displayed save filename","oracle_status":"not-run"},{"case_id":"CMD51-070","feature_id":"WP51-020","title":"Typing a save filename starts a new name","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":565,"printed_end":566,"pdf_start":582,"pdf_end":583}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Existing name appears at save. Enter requests replacement; y permits it. A character starts a fresh name; cursor/edit keys can edit the displayed name before typing that character.","remaining":"Need approved replacement with backup/Fast Save settings; cursor-key and first-character name edits; unusual/colliding filenames. WP03 refuses actual replacement."},
    {"id":"FP05","topic":"No-edit and failed-save integrity","feature_ids":["WP51-020"],"case_links":[{"case_id":"CMD51-149","feature_id":"WP51-020","title":"Preserve an untouched native file byte for byte","oracle_status":"not-run"},{"case_id":"CMD51-150","feature_id":"WP51-020","title":"Reject an unsafe opaque-structure edit before replacement","oracle_status":"not-run"},{"case_id":"CMD51-151","feature_id":"WP51-020","title":"Preserve unrelated native data after a supported edit","oracle_status":"not-run"},{"case_id":"CMD51-152","feature_id":"WP51-020","title":"Retain original after a failed save","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":565,"printed_end":566,"pdf_start":582,"pdf_end":583}],"evidence_basis":"Wordling compatibility requirements; canonical cases not-run","contract":"FC-002 demands exact no-edit bytes; FC-003/004 preserve unrelated/unknown structures or refuse unsafe edits. FC-009/NFR-002 require explicit failure without damaging original. REF Save is contextual, not proof original WP saves untouched bytes identically.","remaining":"Storage foundation and later writers need distinct acceptance. Interrupted publication, ambiguous outcomes and power loss must not be called successful or silently rolled back."},
    {"id":"FP06","topic":"Original backup","feature_ids":["WP51-021"],"case_links":[{"case_id":"CMD51-071","feature_id":"WP51-021","title":"Enable original-document backup","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":41,"printed_end":43,"pdf_start":58,"pdf_end":60}],"evidence_basis":"documentary; dedicated case not-run","contract":"Replacement with Original Backup enabled rotates prior version into same-directory base-name .BK! artifact. Different extensions of same base share it; subsequent replacement updates the backup. Turning off the option deletes the backup at next save.","remaining":"Capture exact names/extensions/collisions, rotation, settings and failure ordering; preserve old backup/original on failed attempted replacement until tested semantics are established."},
    {"id":"FP07","topic":"Timed backup","feature_ids":["WP51-021"],"case_links":[{"case_id":"CMD51-072","feature_id":"WP51-021","title":"Configure timed backup","oracle_status":"not-run"},{"case_id":"CMD51-073","feature_id":"WP51-021","title":"Empty editing screen does not create a zero-byte timed backup","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":43,"printed_end":44,"pdf_start":60,"pdf_end":61}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Timed Backup interval is in minutes; backup location is configured separately from the native save destination; normal exit deletes timed backups. It is distinct from original-version backup and explicit Save.","remaining":"Blank-document suppression and exact timed filenames, both screens, clock/suspension/space failures need fixtures and original observations."},
    {"id":"FP08","topic":"Startup recovery","feature_ids":["WP51-021"],"case_links":[{"case_id":"CMD51-074","feature_id":"WP51-021","title":"Startup checks backups for both document screens","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":44,"printed_end":44,"pdf_start":61,"pdf_end":61}],"evidence_basis":"documentary; dedicated case not-run","contract":"Old Backup 1/2 prompt offers Rename or Delete; Rename retains recoverable content under a user-chosen name. Do not equate recovery with unlimited editor undo.","remaining":"Test both document screens, names/bytes, cancel and interrupted recovery. No automatic candidate cleanup or new recovery sidecar is approved."},
    {"id":"FP09","topic":"Fast Save","feature_ids":["WP51-022"],"case_links":[{"case_id":"CMD51-075","feature_id":"WP51-022","title":"Disable Fast Save before saving","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":197,"printed_end":197,"pdf_start":214,"pdf_end":214}],"evidence_basis":"documentary; dedicated option case not-run","contract":"Fast Save stores unformatted/deleted settings; disabling formats/purges obsolete information. Manual warns original save/fast-save/print-from-disk may need two copies worth of free space.","remaining":"Original corpus deleted packets are incidental evidence, not an exercised setting toggle. Test on/off, purge/format effects and disk exhaustion. Never normalize Wordling no-edit images to imitate an original formatting pass."},
    {"id":"FP10","topic":"File list, directory and resource operations","feature_ids":["WP51-023"],"case_links":[{"case_id":"CMD51-076","feature_id":"WP51-023","title":"List files with a filename pattern","oracle_status":"not-run"},{"case_id":"CMD51-077","feature_id":"WP51-023","title":"Copy a listed file","oracle_status":"not-run"},{"case_id":"CMD51-078","feature_id":"WP51-023","title":"Rename a listed file","oracle_status":"not-run"},{"case_id":"CMD51-079","feature_id":"WP51-023","title":"Decline deleting a file from List Files","oracle_status":"not-run"},{"case_id":"CMD51-080","feature_id":"WP51-023","title":"Toggle long/short file display","oracle_status":"not-run"},{"case_id":"CMD51-081","feature_id":"WP51-023","title":"Disable file-list sorting in March 1992","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":114,"printed_end":119,"pdf_start":131,"pdf_end":136},{"printed_start":347,"printed_end":354,"pdf_start":364,"pdf_end":371},{"printed_start":358,"printed_end":361,"pdf_start":375,"pdf_end":378}],"evidence_basis":"documentary; dedicated cases not-run","contract":"F5 provides filename-pattern list, copy/move/rename/delete/long-short views and default-directory controls. March Sort List Files setting has documented directory-order/Name Search effects.","remaining":"Exact prompts, wildcard/case/DOS ordering, overwrite/collision/permission failure, list printing and cancellation need probes. File deletion is not document Undelete."},
    {"id":"FP11","topic":"Password lock and associated artifacts","feature_ids":["WP51-024"],"case_links":[{"case_id":"CMD51-082","feature_id":"WP51-024","title":"Set a document password","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":362,"printed_end":363,"pdf_start":379,"pdf_end":380}],"evidence_basis":"documentary; dedicated case not-run","contract":"Password Add/Change requires two hidden entries and save to take effect; Remove also requires save. Related temporary/backup artifacts are documented locked. Wrong password refuses retrieval.","remaining":"No encrypted fixture/decryption or encrypted auxiliary-format support established. Password encryption is separate from shared-file access locking; do not implement one as the other."},
    {"id":"FP12","topic":"DOS text input modes","feature_ids":["WP51-025"],"case_links":[{"case_id":"CMD51-083","feature_id":"WP51-025","title":"Import DOS CR/LF as hard returns","oracle_status":"not-run"},{"case_id":"CMD51-084","feature_id":"WP51-025","title":"Import DOS text using hyphenation-zone soft-return mode","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":685,"printed_end":688,"pdf_start":702,"pdf_end":705}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Ctrl+F5 distinguishes CR/LF to Hard Return from CR/LF to Soft Return in the hyphenation zone. Margins/zone and repeated newline runs affect conversion.","remaining":"Need literal byte fixtures for CR/LF, repeated empty lines, extended characters and malformed/nontext input. No blanket newline normalization."},
    {"id":"FP13","topic":"DOS, Generic, 5.0 and 4.2 exports","feature_ids":["WP51-025","WP51-026"],"case_links":[],"source_id":"REF51","locators":[{"printed_start":685,"printed_end":688,"pdf_start":702,"pdf_end":705},{"printed_start":138,"printed_end":142,"pdf_start":155,"pdf_end":159}],"evidence_basis":"documentary; no dedicated export-mode case in these groups","contract":"Text Out DOS removes/reifies formatting according to original mode; Generic retains layout using spaces/tabs/CRLF; 5.0 preserves unrecognized 5.1 codes as Unknown, while 4.2 mapping may delete unsupported codes and uses .CRS. F10 after text input saves native format, not text.","remaining":"Author mode-specific cases and original outputs/loss declarations. Documented character254 fallback is an original conversion loss, never native-save permission for silent replacement. Password 5.0/4.2 differences need explicit fixtures."},
    {"id":"FP14","topic":"Legacy native input conversion","feature_ids":["WP51-026"],"case_links":[{"case_id":"CMD51-157","feature_id":"WP51-026","title":"Retrieve an original 4.2 document into 5.1","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":130,"printed_end":142,"pdf_start":147,"pdf_end":159},{"printed_start":556,"printed_end":556,"pdf_start":573,"pdf_end":573}],"evidence_basis":"documentary; dedicated case not-run","contract":"Retrieve converts older 4.2/5.0 files to 5.1. Conversion is separate from byte-identical supported 5.1 snapshot acquisition.","remaining":"Acquire original legacy fixtures and .CRS/resources as applicable; keep input unchanged, declare losses/errors and independently test outputs."},
    {"id":"FP15","topic":"Standalone CONVERT utility","feature_ids":["WP51-079"],"case_links":[],"source_id":"REF51","locators":[{"printed_start":89,"printed_end":95,"pdf_start":106,"pdf_end":112}],"evidence_basis":"indexed/documentary; no dedicated CONVERT case in this group","contract":"The original conversion utility remains M1; its supported modes, switches and artifact formats must be enumerated from its own section.","remaining":"Do not cite the cursor case as conversion evidence; create per-format conversion probes with lawful test inputs, failure/log outputs and exact settings."},
    {"id":"FP16","topic":"Macro and graphics converters","feature_ids":["WP51-061","WP51-056"],"case_links":[{"case_id":"CMD51-179","feature_id":"WP51-061","title":"Convert a 4.x macro with MACROCNV","oracle_status":"not-run"},{"case_id":"CMD51-175","feature_id":"WP51-056","title":"Convert an original graphics file with GRAPHCNV","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":370,"printed_end":372,"pdf_start":387,"pdf_end":389},{"printed_start":228,"printed_end":231,"pdf_start":245,"pdf_end":248}],"evidence_basis":"documentary; dedicated cases not-run","contract":"MACROCNV and GRAPHCNV produce original automation/graphics representations through distinct conversion procedures.","remaining":"Need source-version inputs, option/loss behavior and original reopening; these converters are not a dependency of native document Save."},
    {"id":"FP17","topic":"Spreadsheet import and links","feature_ids":["WP51-065"],"case_links":[{"case_id":"CMD51-136","feature_id":"WP51-065","title":"Import a declared spreadsheet range","oracle_status":"not-run"},{"case_id":"CMD51-137","feature_id":"WP51-065","title":"Create a spreadsheet link","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":606,"printed_end":615,"pdf_start":623,"pdf_end":632}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Spreadsheet import and persistent links have distinct source range/update/resource behavior.","remaining":"Use original spreadsheet fixtures and preserve original link relationships. No invented CSV/intermediary format may replace required original formats."},
    {"id":"FP18","topic":"Document comments and compare","feature_ids":["WP51-027"],"case_links":[{"case_id":"CMD51-158","feature_id":"WP51-027","title":"Create a nonprinting document comment","oracle_status":"not-run"},{"case_id":"CMD51-159","feature_id":"WP51-027","title":"Compare screen and disk document versions","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":124,"printed_end":129,"pdf_start":141,"pdf_end":146}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Comments are native nonprinting content; compare adds original redline/strikeout semantics using screen/disk versions.","remaining":"Need cancellation, source preservation and original printed/native evidence; never treat comments as disposable unknown bytes."},
    {"id":"FP19","topic":"Look and Find","feature_ids":["WP51-028"],"case_links":[{"case_id":"CMD51-085","feature_id":"WP51-028","title":"Find files by content","oracle_status":"not-run"},{"case_id":"CMD51-086","feature_id":"WP51-028","title":"Display file contents through Look","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":197,"printed_end":202,"pdf_start":214,"pdf_end":219},{"printed_start":364,"printed_end":368,"pdf_start":381,"pdf_end":385}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Look inspects without retrieving into current document; Find searches declared filename/content conditions.","remaining":"Need encrypted/access-denied cases, search conditions and long/short/list interactions. Reading a file is not authorization to modify it."},
    {"id":"FP20","topic":"Document summary and long names","feature_ids":["WP51-090"],"case_links":[{"case_id":"CMD51-088","feature_id":"WP51-090","title":"Commit a document summary","oracle_status":"not-run"},{"case_id":"CMD51-089","feature_id":"WP51-090","title":"Cancel summary changes","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":145,"printed_end":149,"pdf_start":162,"pdf_end":166},{"printed_start":565,"printed_end":566,"pdf_start":582,"pdf_end":583}],"evidence_basis":"documentary; dedicated cases not-run","contract":"Descriptive long name/type metadata is distinct from DOS basename. Summary acceptance versus F1 cancellation must be separately preserved.","remaining":"Need source-native fields, encoding, name/type prompt settings and filename collisions. Linux long filenames are not a substitute for original summary metadata."},
    {"id":"FP21","topic":"Exit, clear and save decisions","feature_ids":["WP51-029"],"case_links":[{"case_id":"CMD51-087","feature_id":"WP51-029","title":"Exit without saving and cancel application exit","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":194,"printed_end":196,"pdf_start":211,"pdf_end":213}],"evidence_basis":"documentary; dedicated cancel-exit case not-run","contract":"F7 exit/save/clear/switch choices depend on document and second-screen state. Existing probe clean exits use a different bounded branch.","remaining":"Do not infer buffer-clearing or cancel behavior for F7,n,n from F7,n,y evidence. Probe each relevant state before implementing irreversible buffer discard."},
    {"id":"FP22","topic":"DOS and Shell integration","feature_ids":["WP51-078"],"case_links":[{"case_id":"CMD51-189","feature_id":"WP51-078","title":"Run a DOS command and return to the same cursor","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":150,"printed_end":156,"pdf_start":167,"pdf_end":173},{"printed_start":225,"printed_end":227,"pdf_start":242,"pdf_end":244}],"evidence_basis":"documentary; dedicated case not-run; incidental guest COPY in overwrite recipe","contract":"Ctrl+F1 DOS Command is used as fixture preparation in the refusal recipe. Dedicated read-only command/cursor-return behavior remains not-run.","remaining":"A Linux child-shell mapping needs command/context/environment/return semantics; never pass a DOS command string straight to a Linux shell and claim equivalence."},
    {"id":"FP23","topic":"Cursor and screen-capture utilities","feature_ids":["WP51-079"],"case_links":[{"case_id":"CMD51-190","feature_id":"WP51-079","title":"Choose an original cursor appearance","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":105,"printed_end":108,"pdf_start":122,"pdf_end":125},{"printed_start":567,"printed_end":570,"pdf_start":584,"pdf_end":587}],"evidence_basis":"documentary/indexed; cursor case not-run; no capture-utility case","contract":"Original cursor appearance and DOS screen capture utilities remain tracked separately from app snapshot tooling.","remaining":"Declare terminal capabilities and equivalent meaningful controls; no claim a Linux terminal executes DOS hardware calls. Create a dedicated capture-utility contract."},
    {"id":"FP24","topic":"Startup and memory/resource options","feature_ids":["WP51-080"],"case_links":[{"case_id":"CMD51-191","feature_id":"WP51-080","title":"Start WP with a declared macro","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":415,"printed_end":417,"pdf_start":432,"pdf_end":434},{"printed_start":897,"printed_end":904,"pdf_start":914,"pdf_end":921}],"evidence_basis":"documentary; dedicated case not-run","contract":"Startup macro and memory/resource switches must preserve original resolution/session behavior under an explicit Linux adaptation.","remaining":"Probe actual switch spelling, resource paths, document2 flags and failure behavior; do not blindly forward DOS memory addresses/options."},
    {"id":"FP25","topic":"Network and shared-file access","feature_ids":["WP51-081"],"case_links":[{"case_id":"CMD51-192","feature_id":"WP51-081","title":"Investigate shared-file access with separate user setups","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":921,"printed_end":960,"pdf_start":938,"pdf_end":977}],"evidence_basis":"indexed/investigation; no resolved conflict policy","contract":"Original network installation separates shared resources and personal settings; exact multi-user retrieval/save/lock decisions remain unresolved in the canonical case.","remaining":"Need two-user original environment/rights and native artifacts. POSIX locks or local stale-source checks alone do not establish original network locking. No unsupported-network exclusion from M1."},
    {"id":"FP26","topic":"Original print-to-disk output","feature_ids":["WP51-074"],"case_links":[{"case_id":"CMD51-145","feature_id":"WP51-074","title":"Direct original printer output to a disk file","oracle_status":"not-run"}],"source_id":"REF51","locators":[{"printed_start":543,"printed_end":543,"pdf_start":560,"pdf_end":560}],"evidence_basis":"documentary; dedicated case not-run","contract":"Original printer-language output must retain selected printer/resource behavior; it is separate from DOS Text, Generic and native Save.","remaining":"Needs calibrated printer definition/output comparison. PDF is an optional M2 export and cannot replace this M1 mode."},
    {"id":"FP27","topic":"PIF and OS integration context","feature_ids":["WP51-078","WP51-080"],"case_links":[],"source_id":"REF51","locators":[{"printed_start":961,"printed_end":962,"pdf_start":978,"pdf_end":979}],"evidence_basis":"indexed; no dedicated PIF scenario","contract":"PIF integration is an original platform dependency needing explicit Linux applicability/mapping study, not automatically discarded as a Windows-associated source section.","remaining":"Enumerate actual purpose/fields and user-visible invocation first. Any proposed removal/changed parity baseline requires an owner scope decision; none is supplied here."}
  ],
  "evidence":[
    {"path":"docs/research/reference-runs/2026-10-29-smoke-02/run.json","kind":"run","sha256":"d361f81768a5ee9ea85d4590b013c53c2e68770af76ceaf91302b308281091d6","size":31814},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-02/CMD51-066/NEWTEST.WP5","kind":"native","sha256":"a42b87e3441dc422c5a348e5b6838e5949a3dabedddf49e947f784408db0dff6","size":337,"case_id":"CMD51-066","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-02/run.json","body_offset":324,"body_hex":"574f52444c494e472054455354"},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-02/CMD51-066/save-prompt/screen.txt","kind":"screen","sha256":"e159ddc42a63aa326eb8fedc4cc090a0206780305a087575872957eda0fb683b","size":59,"case_id":"CMD51-066","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-02/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-02/CMD51-066/saved/screen.txt","kind":"screen","sha256":"62eb80dbf709898463699c448129cc955a1db18836f39d9f45cfee9aa686a19c","size":115,"case_id":"CMD51-066","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-02/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-03/run.json","kind":"run","sha256":"c4cae074cc75e651eff994e62cb0917d5645477c906a1f975738ea4ab62de4fe","size":32746},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5","kind":"native","sha256":"a42b87e3441dc422c5a348e5b6838e5949a3dabedddf49e947f784408db0dff6","size":337,"case_id":"CMD51-066","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json","body_offset":324,"body_hex":"574f52444c494e472054455354"},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/save-prompt/screen.txt","kind":"screen","sha256":"e159ddc42a63aa326eb8fedc4cc090a0206780305a087575872957eda0fb683b","size":59,"case_id":"CMD51-066","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/saved/screen.txt","kind":"screen","sha256":"62eb80dbf709898463699c448129cc955a1db18836f39d9f45cfee9aa686a19c","size":115,"case_id":"CMD51-066","run_manifest":"docs/research/reference-runs/2026-10-29-smoke-03/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-03/run.json","kind":"run","sha256":"68450fd8efa5deea93e83021b043ad0a9ab1ada4867e5d5616c49fcf7c1d7809","size":63907},
    {"path":"docs/research/reference-runs/2026-10-29-extended-03/CMD51-067/BEFORE.WP5","kind":"native","sha256":"22699462e095ce1a68ee016eb821210d194436b1c248908957db08db5fd46c62","size":332,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-03/run.json","body_offset":324,"body_hex":"4f524947494e414c"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-03/CMD51-067/SAME.WP5","kind":"native","sha256":"22699462e095ce1a68ee016eb821210d194436b1c248908957db08db5fd46c62","size":332,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-03/run.json","body_offset":324,"body_hex":"4f524947494e414c"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-03/CMD51-067/replace-prompt/screen.txt","kind":"screen","sha256":"10b6100e603ad66451ba2ad3a0298853d8877bb13e2c74e95912e1fdfc58b0d8","size":70,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-03/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-03/CMD51-067/different-filename-requested/screen.txt","kind":"screen","sha256":"445164a93161ba21e18348079088e7c509478ab4f050d2c13255903d0aeeefd6","size":74,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-03/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-03/CMD51-067/unsaved-buffer/screen.txt","kind":"screen","sha256":"e0e6246125f667188ed3c07fa61cb2f75760cbcf108f29240555e5d5c0b5425a","size":118,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-03/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-04/run.json","kind":"run","sha256":"c7d98c6225892261dff38b88b3c9c044856ad43ad4e5776d4197089d885ac0fc","size":63907},
    {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/BEFORE.WP5","kind":"native","sha256":"22699462e095ce1a68ee016eb821210d194436b1c248908957db08db5fd46c62","size":332,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json","body_offset":324,"body_hex":"4f524947494e414c"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/SAME.WP5","kind":"native","sha256":"22699462e095ce1a68ee016eb821210d194436b1c248908957db08db5fd46c62","size":332,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json","body_offset":324,"body_hex":"4f524947494e414c"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/replace-prompt/screen.txt","kind":"screen","sha256":"10b6100e603ad66451ba2ad3a0298853d8877bb13e2c74e95912e1fdfc58b0d8","size":70,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/different-filename-requested/screen.txt","kind":"screen","sha256":"445164a93161ba21e18348079088e7c509478ab4f050d2c13255903d0aeeefd6","size":74,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"},
    {"path":"docs/research/reference-runs/2026-10-29-extended-04/CMD51-067/unsaved-buffer/screen.txt","kind":"screen","sha256":"e0e6246125f667188ed3c07fa61cb2f75760cbcf108f29240555e5d5c0b5425a","size":118,"case_id":"CMD51-067","run_manifest":"docs/research/reference-runs/2026-10-29-extended-04/run.json"}
  ]
}
```
<!-- WP06_AUDIT_END -->

Reproduce the audit from the repository root without running DOS or editing
raw evidence:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json, re, struct
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md')
text = p.read_text()
a = text.split('<!-- WP06_AUDIT_BEGIN -->',1)[1]
a = json.loads(a.split('```json\n',1)[1].split('\n```',1)[0])
sha = lambda b: hashlib.sha256(b).hexdigest()
for source in a['source_inputs']:
    assert sha(Path(source['path']).read_bytes()) == source['sha256']
inv = {g['id']:g for g in json.loads(Path('docs/research/feature-inventory.json').read_text())}
cases = {c['id']:c for c in json.loads(Path('docs/research/command-scenarios.json').read_text())}
sources = {s['id']:s for s in json.loads(Path('docs/research/sources.json').read_text())}
assert len(a['rows']) == 27
assert {r['id'] for r in a['rows']} == {f'FP{n:02}' for n in range(1,28)}
assert set(re.findall(r'^\| (FP\d{2}):',text,re.M)) == {r['id'] for r in a['rows']}
used = set()
for row in a['rows']:
    assert set(row['feature_ids']) <= inv.keys()
    line = next(l for l in text.splitlines() if l.startswith('| '+row['id']+':'))
    cells = [c.strip() for c in line.split('|')]
    expected = ', '.join(row['feature_ids'])+'; '+('; '.join(
        c['case_id']+' ('+c['title']+')' for c in row['case_links']) or 'no dedicated scenario')
    assert cells[3] == expected, row['id']
    assert cells[4] == row['evidence_basis'], row['id']
    assert cells[5] == row['contract']+' **Remaining:** '+row['remaining'], row['id']
    assert set(re.findall(r'CMD51-\d{3}',line)) == {c['case_id'] for c in row['case_links']}
    for link in row['case_links']:
        cid,gid = link['case_id'],link['feature_id']
        assert gid in row['feature_ids'] and gid in cases[cid]['feature_ids'], (row['id'],cid,gid)
        assert cid in inv[gid]['command_scenario_ids'], (row['id'],cid,gid)
        assert link['title'] == cases[cid]['title']
        assert link['oracle_status'] == cases[cid]['oracle_status']
        used.add(cid)
    loc = '; '.join(f"{l['printed_start']}–{l['printed_end']} / {l['pdf_start']}–{l['pdf_end']}" for l in row['locators'])
    assert cells[2] == loc
    for l in row['locators']:
        assert 1 <= l['printed_start'] <= l['printed_end']
        assert l['pdf_start']==l['printed_start']+17 and l['pdf_end']==l['printed_end']+17
        assert l['pdf_end'] <= sources[row['source_id']]['pdf_pages']
assert {cid for cid in used if cases[cid]['oracle_status']=='partially-observed'} == {'CMD51-066','CMD51-067'}
assert set(re.findall(r'CMD51-\d{3}',text)) <= used
assert len(a['evidence']) == 20
for e in a['evidence']:
    d = Path(e['path']).read_bytes()
    assert (len(d),sha(d)) == (e['size'],e['sha256'])
    if 'case_id' in e:
        assert e['case_id'] in used
        assert e['run_manifest'] in cases[e['case_id']]['evidence_paths']
        run = json.loads(Path(e['run_manifest']).read_text())
        assert run['scope']=='original-reference-only' and not run['wordling_tested']
        case = next(c for c in run['results'] if c['case_id']==e['case_id'])
        assert any(x['path']==e['path'] and x['size']==len(d) and x['sha256']==sha(d) for x in case['evidence'])
    if e['kind']=='native':
        body = struct.unpack_from('<I',d,4)[0]
        assert body==e['body_offset'] and d[body:].hex()==e['body_hex']
        if e['case_id']=='CMD51-067':
            other = Path(e['path']).with_name('BEFORE.WP5' if Path(e['path']).name=='SAME.WP5' else 'SAME.WP5')
            assert other.read_bytes()==d
        repeat = e['path'].replace('smoke-03','smoke-02').replace('extended-04','extended-03')
        assert Path(repeat).read_bytes()==d
print('WP06 source hashes, 27 semantic matrices, canonical statuses and original evidence valid')
PY
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
```

The configured project regression runner must also pass before handoff. Its
planning-checkout results do not claim tests of a separate coding lane or any
original behavior beyond the linked recipes.

Author validation: the embedded source/semantic-link/evidence audit passes, as
do both catalogue checks and the genuine project regression runner. Go package
discovery succeeds; build/test/vet are explicitly skipped because the primary
planning checkout currently has no Go packages. This does not report on WP03's
separate implementation checkout. No new original probes or code were run for
this research package; no canonical registry, queue or raw evidence was changed.
