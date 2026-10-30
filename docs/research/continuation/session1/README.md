# WP13 original SESSION1 observations

This is original-only research on the pinned U.S. English WP5.1 Help03/09/92
executable, QEMU8.2.2/FreeDOS1.4 and mixed-date July1992 Standard Printer. No
Wordling application, Linux terminal key delivery, historical DOS equivalence,
semantic writer or full original session parity is verified. PDF stays M2.
The source/helper changes and canonical session entries belong only to WP13.

The code lane contains approved native reader e7de080 and storage7deeaf6. Their
presence is separate from these original observations. Approved WP04/WP06/WP11
and WP12 continuation are read from primary without modifying their historical
snapshots; exact prerequisite hashes are in prerequisites.json.

## Source and capture method

Every execution copies the same hashed boot/master images. ORIGIN.WP5 is the
exact project-authored advanced04/CMD51-204 fixture, checked against its old
manifest and SHA-256 before execution. Its body is A/BoldOn/BC/BoldOff/D. A
new project-only seed floppy exposes it as B:\ORIGIN, attached read-only; this
additional drive is explicit in each run's QEMU arguments and seed image hash.
The private master and native source are never edited. Seed, source and master
hashes are checked again after the guest stops. The normal US keyboard/profile
is retained. Source/private media remain ignored, and no proprietary program,
dictionary, disk image or complete guest memory is published.

The runner uses the existing guest/QMP/Probe harness. Lane socket paths exceed
AF_UNIX limits, so the owned runner configures the existing short shared private
runtime and uses an exclusive lock. guest.start independently refuses a live
reference socket. Native extraction occurs only after guest.stop. The manifest
seals exact trace/checks, runtime/configuration, fixture/profile identity,
scenario snapshot, runner sources, raw screen/text/4000-byte VGA attributes,
lossless raster and native outputs. Original UI text in captures is not relicensed
as project prose. No existing historical evidence is modified or normalized.

cursor.json records the hardware text cursor and display-start CRTC registers
while paused, restoring the selected register before resuming. The address
calculation is corroborated by the pinned [QEMU8.2.2 VGA implementation](https://gitlab.com/qemu-project/qemu/-/blob/v8.2.2/hw/display/vga.c)
and [register definitions](https://gitlab.com/qemu-project/qemu/-/blob/v8.2.2/hw/display/vga_regs.h);
URLs/cache hashes are in prerequisites.json. Hardware row/column and status inches
are not semantic token identities. The cursor audit combines those observations
with actual code-pane VGA attributes, exact native bodies and recorded key
sequences; it does not infer a code crossing from a stationary status value alone.

The run-ID prefix `2026-10-31-session1` is only a label; started_at fields retain
the actual UTC execution time. There is no claim that a label changes the clock.
Each selected branch has two fresh run identities. A blank unnamed unmodified
buffer is distinguished from a saved named file; there is no invented
"saved but unnamed" native-file state.

## Concrete findings for WP17

- Retrieve asks `Document to be retrieved:` and offers List Files. F1 and Esc
  cancel the typed missing-name draft back to blank editing. Submitting the
  missing name shows `ERROR: File not found -- B:\MISSING`, then redisplays the
  editable name; typing the correct source retrieves it. This observes blank
  retrieval only, not insertion into existing text or all Initial Codes rules.
- The normal and Reveal Right sequences around Bold On/Off retain the same
  visible hardware cursor while the code-pane selection changes. The additional
  leading-Bold fixture distinguishes Home/Home/Up from Home/Home/Home/Up by
  direct subsequent Right movement in both views. Document bodies remain exact.
  This tests leading body formatting, not every document Initial Codes resource.
- A retrieved file prefills its Save name. Cursor-key editing retains that name;
  the tested Right/Backspace/X sequence changes B:\ORIGIN to B:\OXIGIN. A
  character-first path starts a new filename. Declining replacement returns to
  filename entry; F1 there returns to the changed buffer. No Yes replacement is
  sent. The seed source stays exact and the saved destination retains the
  original document body after the refused overwrite.
- F1 at either Exit Save or application Exit questions returns to the original
  buffer in the declared contexts. Esc is different: at the Save question it
  advances to filename entry; at application Exit it returns with a cleared
  buffer, the same observed outcome as No. These are bounded state outcomes,
  not a theory about the original handler internals or a global Esc binding.
- F7,n,n clears the document and returns to blank editing. F7,n,y returns to DOS.
  Named/unnamed and unchanged/changed states are separate fresh-copy variants.
  Full prompts, filename, buffer, hardware cursor and unmodified-text indicator
  are retained per state in the branch index and captures.

Original WP Save changes the full file/prefix representation in these fixtures;
body preservation does not mean whole-file identity. The cursor audit retains
both lengths, hashes and raw changed offsets. FC-002 still independently requires
Wordling's untouched snapshot to export exact bytes; original WP reformat/save
is not a byte-identity oracle for that requirement.

## Retained diagnostics and scope

Initial private calibration had a case-sensitive guessed error message and an
oversized DOS filename; neither is counted as accepted evidence. The first public
suite also tested an incorrect global Esc-cancel/cleanup assumption. Those raw
attempts remain immutable. Corrected fresh runs observe the actual Esc state and
use separately observed F1 filename cancellation to unwind safely. Diagnostics
are listed separately from the explicit accepted run selection; no result or
capture is rewritten to manufacture a pass.

The accepted rerun set is complete. The branch matrix and reproducible offline
validation commands follow below. Canonical cases remain partially
observed and every Wordling implementation status stays not-implemented.

Unprobed areas remain M1: retrieval into nonblank documents, broad filename
editing/typeover/invalid names, successful replacement/backup/Fast Save failures,
menus/two documents/windows, complete cursor/code/selection/history behavior,
other Initial Codes/nested structures/resources, Linux input qualification,
all semantic writing, graphics/layout/printing and historical DOS. These
observations do not authorize silent refusal of full original scope or mission
acceptance. Downstream packages must use the actual branch table and refuse
unresearched branches explicitly.

## Accepted branch matrix and validation snapshot

Snapshot recorded2026-10-30 UTC:72 public attempts,56 selected fresh runs in28
branch pairs. Fourteen initial runs retain harness-error results; two additional
initial empty-buffer Exit/Esc successes are superseded by the corrected context
runs. These16 attempts remain diagnostic evidence, not accepted repetitions.
The canonical snapshot is244 cases:68 partially-observed and176 not-run; no
Wordling implementation or differential verification status is promoted.

Every link below identifies the exact selected manifest, including trace,
checks, runtime/lock paths, profile/source identity and artifact hashes. Exact
intermediate prompts, first-line buffer, hardware cursor and raw state paths are
in [state-index.json](state-index.json); that index preserves both repetitions.
[accepted-branches.json](accepted-branches.json) is the explicit selection,
[pair-audit.json](pair-audit.json) compares every accepted captured text/cursor
state, [cursor-audit.json](cursor-audit.json) checks code attributes/native bodies,
and [postrun-fingerprints.json](postrun-fingerprints.json) records stopped-disk
resource/settings identities for all72 attempts. Postrun fingerprinting reads
only each stopped private run disk; it does not access a later user's live VM.

| Branch/precondition | Canonical cases | Repetitions | Bounded observed result |
| --- | --- | --- | --- |
| retrieve | CMD51-065, CMD51-237, CMD51-238, CMD51-239 | [r1](runs/2026-10-31-session1-b00-r1/run.json) / [r2](runs/2026-10-31-session1-b00-r2/run.json) | F1/Esc cancel; missing-name error/retry; blank Retrieve and new-name save |
| cursor | CMD51-049, CMD51-019, CMD51-020 | [r1](runs/2026-10-31-session1-b01-r1/run.json) / [r2](runs/2026-10-31-session1-b01-r2/run.json) | normal/Reveal Right token gaps; leading-Bold Home variants; native body retained |
| filenames | CMD51-069, CMD51-067, CMD51-070 | [r1](runs/2026-10-31-session1-b02-r1/run.json) / [r2](runs/2026-10-31-session1-b02-r2/run.json) | prefilled caret edit/cancel; character-first name; replacement No then F1 |
| named-unchanged-save-f1 | CMD51-240 | [r1](runs/2026-10-31-session1-b03-r1/run.json) / [r2](runs/2026-10-31-session1-b03-r2/run.json) | F1 at Save question retains buffer |
| named-unchanged-exit-f1 | CMD51-242 | [r1](runs/2026-10-31-session1-b05-r1/run.json) / [r2](runs/2026-10-31-session1-b05-r2/run.json) | Save n; F1 at Exit retains buffer |
| named-unchanged-continue | CMD51-087 | [r1](runs/2026-10-31-session1-b07-r1/run.json) / [r2](runs/2026-10-31-session1-b07-r2/run.json) | F7,n,n clears buffer and returns editing |
| named-unchanged-quit | CMD51-244 | [r1](runs/2026-10-31-session1-b08-r1/run.json) / [r2](runs/2026-10-31-session1-b08-r2/run.json) | F7,n,y returns DOS |
| named-changed-save-f1 | CMD51-240 | [r1](runs/2026-10-31-session1-b09-r1/run.json) / [r2](runs/2026-10-31-session1-b09-r2/run.json) | F1 at Save question retains buffer |
| named-changed-exit-f1 | CMD51-242 | [r1](runs/2026-10-31-session1-b11-r1/run.json) / [r2](runs/2026-10-31-session1-b11-r2/run.json) | Save n; F1 at Exit retains buffer |
| named-changed-continue | CMD51-087 | [r1](runs/2026-10-31-session1-b13-r1/run.json) / [r2](runs/2026-10-31-session1-b13-r2/run.json) | F7,n,n clears buffer and returns editing |
| named-changed-quit | CMD51-244 | [r1](runs/2026-10-31-session1-b14-r1/run.json) / [r2](runs/2026-10-31-session1-b14-r2/run.json) | F7,n,y returns DOS |
| unnamed-unchanged-save-f1 | CMD51-240 | [r1](runs/2026-10-31-session1-b15-r1/run.json) / [r2](runs/2026-10-31-session1-b15-r2/run.json) | F1 at Save question retains buffer |
| unnamed-unchanged-exit-f1 | CMD51-242 | [r1](runs/2026-10-31-session1-b17-r1/run.json) / [r2](runs/2026-10-31-session1-b17-r2/run.json) | Save n; F1 at Exit retains buffer |
| unnamed-unchanged-continue | CMD51-087 | [r1](runs/2026-10-31-session1-b19-r1/run.json) / [r2](runs/2026-10-31-session1-b19-r2/run.json) | F7,n,n clears buffer and returns editing |
| unnamed-unchanged-quit | CMD51-244 | [r1](runs/2026-10-31-session1-b20-r1/run.json) / [r2](runs/2026-10-31-session1-b20-r2/run.json) | F7,n,y returns DOS |
| unnamed-changed-save-f1 | CMD51-240 | [r1](runs/2026-10-31-session1-b21-r1/run.json) / [r2](runs/2026-10-31-session1-b21-r2/run.json) | F1 at Save question retains buffer |
| unnamed-changed-exit-f1 | CMD51-242 | [r1](runs/2026-10-31-session1-b23-r1/run.json) / [r2](runs/2026-10-31-session1-b23-r2/run.json) | Save n; F1 at Exit retains buffer |
| unnamed-changed-continue | CMD51-087 | [r1](runs/2026-10-31-session1-b25-r1/run.json) / [r2](runs/2026-10-31-session1-b25-r2/run.json) | F7,n,n clears buffer and returns editing |
| unnamed-changed-quit | CMD51-244 | [r1](runs/2026-10-31-session1-b26-r1/run.json) / [r2](runs/2026-10-31-session1-b26-r2/run.json) | F7,n,y returns DOS |
| named-unchanged-save-esc | CMD51-241 | [r1](runs/2026-10-31-session1-correct-c00-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c00-r2/run.json) | Esc advances to filename; F1 there retains buffer |
| named-unchanged-exit-esc | CMD51-243 | [r1](runs/2026-10-31-session1-correct-c01-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c01-r2/run.json) | Save n; Esc at Exit clears buffer |
| named-changed-save-esc | CMD51-241 | [r1](runs/2026-10-31-session1-correct-c02-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c02-r2/run.json) | Esc advances to filename; F1 there retains buffer |
| named-changed-exit-esc | CMD51-243 | [r1](runs/2026-10-31-session1-correct-c03-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c03-r2/run.json) | Save n; Esc at Exit clears buffer |
| unnamed-unchanged-save-esc | CMD51-241 | [r1](runs/2026-10-31-session1-correct-c04-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c04-r2/run.json) | Esc advances to filename; F1 there retains buffer |
| unnamed-unchanged-exit-esc | CMD51-243 | [r1](runs/2026-10-31-session1-correct-c05-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c05-r2/run.json) | Save n; Esc at Exit clears buffer |
| unnamed-changed-save-esc | CMD51-241 | [r1](runs/2026-10-31-session1-correct-c06-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c06-r2/run.json) | Esc advances to filename; F1 there retains buffer |
| unnamed-changed-exit-esc | CMD51-243 | [r1](runs/2026-10-31-session1-correct-c07-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c07-r2/run.json) | Save n; Esc at Exit clears buffer |
| prefix-normal | CMD51-020, CMD51-019 | [r1](runs/2026-10-31-session1-correct-c08-r1/run.json) / [r2](runs/2026-10-31-session1-correct-c08-r2/run.json) | Home2/Home3 distinguished by subsequent Right in both views; native body retained |

Named contexts begin from B:\ORIGIN (ABCD); changed named contexts prepend
CHANGED, yielding CHANGEDABCD. Unnamed changed contexts contain UNNAMED;
unnamed unchanged contexts are fresh empty editing buffers. Save status differs
explicitly; these are not interchangeable “cancel” fixtures. Source integrity is
checked before/after each run against the immutable historical334-byte fixture.
Original WP saves CURSOR as574 bytes with equal native body, not equal full file.

Offline reproduction from repository root (no VM start):

```sh
python3 scripts/reference/session1.py 2026-10-31-session1 verify
python3 docs/research/continuation/session1/audit_states.py 2026-10-31-session1
python3 docs/research/continuation/session1/audit_catalogue.py
python3 docs/research/continuation/session1/audit_git_blobs.py --revision HEAD
python3 -m unittest discover -s docs/research/continuation/session1 -p test_session1.py
python3 -m py_compile scripts/reference/session1.py docs/research/continuation/session1/*.py
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp13-validation.xml
git diff --check
```

The five negative tests reject corrupt native source identity, malformed body
offsets, wrong-feature case assignment, tampered raw artifact hashes and a valid
Home-after case assigned a Home-before state. Catalogue auditing also compares
all unrelated rows and original ordered backlinks against approved7deeaf6.
The Git audit checks both raw workingtree equality and raw manifest SHA-256
references against staged/committed blobs; `.gitattributes` prevents evidence
normalization. The configured review gate exercises catalogue/adapter checks
and actual Go package discovery/build/test/vet in this code lane. Detailed final
command results are recorded in the review handoff; JUnit is generated by the
real checker, never synthesized.

Final precommit validation on2026-10-30: repeated-evidence verification passed
28 pairs with no audit errors; cursor/native audit and semantic catalogue audit
passed; all five unit tests passed; changed Python compilation and both renderer
checks passed. `scripts/review_checks.py` exited0 with all7 checks passing and no
skips (inventory, scenarios, review-adapter, go-package-discovery, go-build,
go-test, go-vet), writing actual JUnit to `/tmp/wp13-validation.xml`. Staged Git
blob auditing matched4398 raw files and5094 manifest hash references exactly;
`git diff --cached --check` passed. The same Git audit can be repeated against
HEAD after commit. No Go source changed and no Wordling/session implementation
was exercised by these original-only runs.
