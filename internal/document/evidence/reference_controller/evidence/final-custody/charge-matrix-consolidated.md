# WP68 consolidated static charge/effect matrix

Normative units: preserved integration-r2/ENVELOPE.md.txt, loader-r2/CONTRACT.md.txt,
R3 issuer contract and COMMON-E-CONTRACT. No tests on this revision yet.

| Category | Existing fields / actual implementation | Before effect / retained outcome / public control |
|---|---|---|
| Cumulative | source_io<=4GiB | issuer64KiB; ledger IO selected before transfer; sampler4097 before read. Full maxima never refund; real short-read/write/fsync/late controls. |
| Cumulative | prepared_bytes<=128MiB | each update reserves4*max_record+1MiB before either encode pass; CLI asserts two complete reservations; huge-string allocator control. |
| Cumulative | commands<=16 | selected stricter combined command/launch budget; no runtime spawn or protocol in68. Generic full-phase test exercises actual reservation/charge/close with no fake P command.70 must fund real use/fit. |
| Cumulative | output_bytes<=16MiB | issuer reserves32768 before any chosen checkpoint; at mostone <=16384B event plus one <=16384B result. Audit reserves work only. Final report is bounded data after terminal close, no operation/permission. CLI checks actual bytes and retained reservation. |
| Cumulative | wire_bytes<=64MiB/messages<=4096/polls<=100000 | no68 transport effects. Actual generic reservation/charge/close tests cover each existing dimension; real codec/wire/actor enforcement belongs70. |
| Cumulative | journal_events<=512/journal_bytes<=32MiB | source-selected E metadata ceilings, not a claim about separate P server journal; one event and max_record bytes reserved before each update, actual committed bytes/event after readback. CLI assertions and one-use OS-effect negative. |
| Cumulative | work<=16777216 | issuer65536 before effects, includes bounded metadata decode; ledger full selected work covers two passes; source audit and sampler fixed finite maxima. All-dimension retained-spend assertions plus no-fullspend mutant. |
| Cumulative | syscalls<=65536 | issuer1024 FS/time checks; acquire/create256; update1024. Cleanup128 fixed syscall slots inside SAME book;64 is CLOSE ATTEMPTS, not syscalls. All effect calls bounded/metered. Native scandir costs conservative bounded charge; source-controlled iterators remain capped. |
| Live, not credits | processes<=8/rss_bytes<=256MiB/fds<=64/files<=64 workspace allocations | removed from cumulative spent. Actual typed kernel coordinator sample retains baseline/current/peak, RSS VmRSS/VmHWM, FD count and source-owned actual created files. Missing data refuses/UNKNOWN; overshoot retained/HALT. No32MiB estimate debit or replenishment. Repeated max-ceiling selections create no credit. No claim of P/child totals or continuous sampling. |

Allocation/cleanup intersection is computed BEFORE resources open:

- Account reserves cleanup128 syscall /16384 work /4097 IO at entry;60 held
  close-attempt slots plus2 terminal-observer and2 emergency close slots retain the exact64 cap.
  Terminal observer suballowance is16 syscall/8192 work/4097 IO from that pool.
- Issuance reserves hold8/16syscall/64work before store effects. Actual store
  chain+lock+metadata+ticket uses <=6 held FDs; no unused reservation returns.
- Parent acquisition reserves exact component-count+root hold BEFORE traversal,
  <=33 closes/66syscall/164work. Ledger creation reserves1/2syscall/36work
  BEFORE O_EXCL. Their actual retained close requirements are data, not authority;
  only a genuine one-use cleanup permit consumes the source-held reservation.
- Worst allowed held path:8+33+1+2+2=46 close attempts <=64;
  16+66+2+16+4=104 syscalls <=128;64+164+36+8192+64=8520 work <=16384.
  Every actual selected intersection is checked against remaining headroom first.
- Genuine cleanup holds bind factory/actual account/resource and transfer once
  from provisional owner to returned lease; full selected costs stay spent on
  failure/loss/close. No automatic retry or foreign/recycled FD close.
- Actual sampled baseline includes coordinator descriptors. Before store setup,
  parent traversal and ledger creation, source adds the known additional FD
  requirement and blocks if shared64 cannot fit. Per-operation33/1 validity alone
  never establishes aggregate fit. Actual coordinator-only peaks remain explicit.

Typed observation seam:

`ownership.sample_coordinator` reads only bounded `/proc/self/status` and
`/proc/self/fd`; no arbitrary PID/callback/supervisor. It returns an actual opaque
source/account/owner-bound one-use observation. `account.record_live` is
filesystem-free and accepts that registered object only; it records diagnostics
or HALTs, never returns credits, grants or permits. The internal producer seam
is available for70's reviewed actual retained provider/session actor producer;
external copied Usage/public reports cannot substitute. Actual full combined
actor enforcement is70 acceptance. Public controls cover valid, malformed,
field-identical, copied, foreign, replayed and expired observations.

Other boundaries:

- Exact builtin LedgerRecordV1, aliases/depth/integer/string/Unicode/buffer/work
  checks precede encoding/IO. No JSON hooks or foreign authority.
- Source policy field-identical/copied/foreign values refuse before store effects.
  TEST parent must be the fixed store-ledger sibling or descendants; no arbitrary
  public TEST path. Original RootTicketIssuer always refuses before caller paths.
- Metadata exact six-field primitive types reject UID float/int equivalence;
  decode work charged before bounded4096B parsing. Store lock/metadata/marker and
  every ancestor/file link are checked, with actual replacement/foreign controls.
- Stable permanent O_EXCL marker, file-sync then directory-sync then readback
  precede genuine grant. Before marker creation the remaining1024 stage budget
  must fund a bounded tail; positive-write ceiling is tightened within<=16, never
  increased. All failures/losses stay spent, no parse/reconstruct/retry/GC.
- Successful finish closes the logical book. Failed store close refuses and HALTs
  without COMPLETE or usable noncleanup account. Public real recycled-FD and
  use-after-finish controls apply.
- New max-depth control actually traverses33 retained FDs, writes/reads a record,
  closes the full chain through exact reserved requirements and finishes the
  genuine public TEST transaction. No fake controller/P result.

Next: freeze this actual source/test/roster/tool/argv/env/cwd; run bounded targeted
controls first (including meaningful consumed-permit mutant). Preserve outcomes;
only then run one coherent full roster after any required corrections. Old10
UNKNOWN is not relabeled. Physical2048files/32MiB caps unchanged. No lifecycle,
P/private/reference operations or original authority.
