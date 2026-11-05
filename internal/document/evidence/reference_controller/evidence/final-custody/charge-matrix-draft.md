# WP68 static charge/effect matrix — pre-consolidation

Actual current production is the source frozen for attempt10; that attempt is
historical WHOLE1 (mutant classifier UNKNOWN). No further positives until the
consolidation below. Full-spend counters never refund; noncleanup faults HALT.
This matrix covers every DIMENSIONS key and the COMMON/R2/R3 effect sites.

| Dimension | Effect / reservation before effect | Retention / public control | Audit result |
|---|---|---|---|
| source_io | issuer 64KiB before store open; ledger selected IO before pread/pwrite; requested bytes charged before calls | short progress, readback fault and expiry retain maxima; CLI/API and kernel controls | Present. Add actual metadata decode work charge (below). |
| prepared_bytes | update reserves 4*max_record+1MiB before encode; both finite passes before write | CLI asserts two complete reservations; huge-string actual tracemalloc guard | Connected in10; keep. |
| commands | No command transport in68; existing process entry is not an Original command | Public phase reservation supports this dimension; add all-dimension full-spend assertion | No68 physical command effect;70 owns real command consumer. |
| output_bytes | audit currently reserves16KiB, but checkpoint can precede audit; final report follows finish | local _emit <=16KiB, <=one chosen checkpoint plus one result | GAP: move conservative32KiB report reservation to issuer entry, before any checkpoint, retain after terminal finish; audit reserves work only. Reporting after terminal account cannot mint operations. |
| processes |68 starts no child/worker; external acceptance coordinator starts installed CLI before account exists | public generic phase seam; real spawn/protocol consumer belongs70 | No68 runtime child effect; no fabricated controller proof. |
| rss_bytes | current physical runtime RSS measured <=256MiB (aggregate child high-water79–83MiB includes wheel/Go), but book counter remains0 | future generic phase seam exists | ROOT classification needed: worker preexists account; should selected worker reservation be separately charged (e.g. measured32MiB) vs common envelope peak/consumer reservations? Avoid inventing P64 grant/cap semantics. |
| fds | issuer8, parent selected<=33, ledger1 reserved before open; actual opens charged before syscall | public retarget/recycled-FD and syscall controls | Present; common64 cumulative bound retained. |
| wire_bytes | no socket/protocol/P wire in68 | all-dimension public phase test;70 owns actual wire use | No68 effect. |
| messages | no transport messages in68 | same phase seam;70 real protocol validation | No68 effect. |
| polls | no wait/poll protocol inside68; TEST driver's select is outside account | same phase seam;70 worker/protocol polls | No68 effect. |
| journal_events | one per update reserved before encode; actual successful update charged after full readback | CLI asserts two journal reservations; per-operation counters refuse reused permit | Connected in10; keep. |
| journal_bytes | selected max_record per update before encoding/writes | CLI asserts retained16384 for two8192 maxima; actual committed bytes charged | Connected in10; keep. |
| files | issuer marker1 + created ledger1 reserved before O_EXCL; open helper charges actual creation before syscall | CLI asserts exactly2; capacity/loss/replay controls retain files/markers | Connected in10; keep. Admin is separately bounded preprovisioning. |
| work | issuer65536 and ledger selected max (both passes) before operations; audit4096 before finite observation/hash | typed record limits/aliases/hooks tests and no-fullspend mutant | Add before-json-decode work=len(metadata), within existing65536. |
| syscalls | issuer1024 includes explicit deadline checks; acquire/create256/update1024 include bounded FS/stat/readback; all charged before call | real syscall fault/late-return controls; generic budget guard | Present. No timeout or end reset. |

Other COMMON/R2/R3 effect sites:

- **Cleanup:**64 syscall slots +16384 work reserved at book entry, no new global
  spend after HALT. `_cleanup_left` prevents overlapping syscall allocations.
  GAP: add `_cleanup_work_left` and spend full selected cleanup work from that
  same already reserved pool; direct store closes must deduct bounded work too.
  Public all-dimension phase controls + real recycled store FD verify failures
  refuse and terminal success rejects later phase use. No close of foreign FD.
- **Parent/store/ledger custody:** held root-chain links, held lock/metadata/
  marker FD+pathname identity and ledger nlink/identity checks before/after IO;
  actual replacements and SIGKILL boundaries use new IDs. No unlink/recovery.
- **Metadata type boundary:** bounded4096B JSON currently compared to exact
  expected dict. GAP: reject nonexact UID type (float can equal int), exact
  six-field shape and primitive types before equality. Charge its bounded parse
  work. Add finite UID-float negative under existing store quarantine case.
- **Durable issuance:** fixed six digests/identifiers/origin/end/boot binding,
  <=4096 construction, <=256B marker. File sync then parent sync then same-FD
  readback precede grant. Loss/collision/cap/quarantine controls and real syscall
  faults cover public consumer; Root issuer always blocked before caller paths.
- **Allocation/records:** exact builtin-only finite two-pass encoder, no alias,
  bounded pieces/buffer/IO; both full work + buffer maxima reserved before pass1.
  Wrong/consumed/forged permits refuse before record/FS effects. Reused-permit
  mutant now reaches OperationLimit; preserve10 UNKNOWN, strengthen the public
  no-second-effect assertion and classifier for the actual typed guard failure.
- **Full-phase seam:** existing8 phases, same earlier book/owner/absolute end,
  source-fixed dimensions, no refunds or scalar capability. Add one finite
  public loop asserting retained spend for every existing dimension and an
  attempted over-reservation; does not claim real70 protocol/export effects.
- **Terminal finish:** valid store close sets book closed; any close failure
  HALTs and returns refusal. Real recycled-store-FD/use-after-finish public
  controls passed09/10. No COMPLETE return after cleanup failure.

Consolidate only these identified within-scope corrections, freeze source/test/
roster/tool/argv/env/cwd, run targeted charge/type/permit controls, then the full
finite roster after ROOT's RSS classification. No new production files/APIs,
cap changes, original permissions, old-grant repair or lifecycle mutation.
