# Independent WP108 STATIC03 R1 design review

**APPROVE_STATIC03_DESIGN_TEST_COMMAND_PACKET.** No blocking finding remains in the exact R1 scratch packet. The one requested test-gap correction is present. This is approval of the bounded source/test/command design for ROOT's staged test-first handoff, not approval of unimplemented reader source, actual STATIC03 inspection, reference/current-role acceptance or whole WP108/M1 completion.

Reviewer: actual resolved reviewer-renata, existing read-only review governance/profile context. Independent of qualification108_impl's draft. ROOT retains primary/index/Op/lifecycle ownership. I read known tracked STATIC02 evidence/current source and the exact scratch packet, parsed JSON/AST, and consulted only the two explicitly requested primary ABI pages. No draft/helper import, test run, production prototype, public-asset lookup or primary write was performed.

## Exact approved R1 packet

Directory: `/tmp/wordling-wp108-test-prep/STATIC03-design/`.

| File | SHA256 |
| --- | --- |
| proposal.json | `8690312688a038efaebf17d5ee43ad0bf9034513ab21ad67409b81bcbe695a24` |
| static03-reader-plan.json | `95ffd10711d3249b20e7fe7726bbfb5ccab60aa2838e9fb091797749806868d3` |
| command-manifest.json | `b1d5d7513269d815b8d29483f18877c54f5cb18e7bdd5cb62c9f67fbd6097c6a` |
| DATA test draft | `2ad7f50ac24c76717e7663a7f6b4c69d763208ed3a6a4b00e5a38cdcdf849782` |
| AST test draft | `53f12d42acbcc8d747c9a8c082f0f2257b7686dea06ca287b4fe8711dc1c09de` |
| SHA256SUMS.json | `bf9e7fdcfc1f90cdd9af83a44fa3455c688fbc72f04d3ba93a63e460c3031281` |

All19 manifest entries were independently rehashed. R0 bytes remain in history-r0-before-partial-overlap-case. Proposal and reader plan are unchanged by R1; the added negative tuple, explicit variant counts and dependent digests are updated. Method counts remain48 DATA+12 AST=60, with seven new methods covering12 explicitly counted new DATA variants. These are source-unit counts, not campaign case admission.

## Why the admission amendment is justified and bounded

Tracked raw STATIC02 facts reproduce109 items/19 incomplete and53 graph edges/18 unresolved. The recorded stable BASE table is VA[4191704,4233970), crossing two adjacent file-backed LOADs sharing bias4190208, hence file[1496,43762). The cc1 table maps to file[868656,2067657) within one file-backed LOAD. This arithmetic was independently checked against the retained diagnostics; no actual file was re-read and no runtime validity/producer/qualification conclusion is inferred.

The ABI distinguishes file offset, virtual address, file bytes and memory-only tail; extra memory size does not supply file bytes. [ELF program headers](https://gabi.xinuos.com/elf/07-pheader.html). DT_STRTAB is a virtual-address pointer, DT_STRSZ is a table byte count, and dynamic name values index that table. [ELF dynamic entries](https://gabi.xinuos.com/elf/08-dynamic.html). Proving a strict contiguous file-backed union is this design's conservative inference from those fields and the recorded intervals, not an ABI mandate to qualify BASE.

The proposal explicitly amends the old whole-one-segment/65536-logical-table predicate. The canonical mapper remains the sole decision implementation, using strict uint64/nonwrapping endpoints and all intersecting file-backed LOAD intervals. Every requested byte must be covered exactly once. Any intersecting overlap, even identical, rejects; a first whole match cannot hide a partial second mapping. Gaps, bias changes/file discontinuity and memory-only coverage reject. Adjacent pieces must produce one contiguous file interval; the caller verifies the full result against frozen file length before any referenced-string read. No first-match shortcut, p_memsz substitute, section fallback or load-base guess is permitted.

A logical table can be at most the existing64MiB file ceiling and must have whole-range coverage, but is never allocated/read as a unit. Each referenced offset must satisfy0<=offset<logical_size. Read only min(4096,logical_size-offset), then call the unchanged canonical elf_string_data(window,0). Its64KiB buffer and4096-byte terminator guard remain unchanged. At most131 references plus existing header/program/dynamic/interpreter reads yield the stated conservative610368-byte per-ELF work ceiling, below1MiB. Actual reads still charge existing per-file/aggregate counters. No table-sized cache, incremental whole-table scan or budget renewal is proposed.

The original global caps remain30s+2s,160MiB AS,FD32,nproc0,64KiB chunks,64MiB/file read requests,256MiB aggregate,1MiB/ELF,16MiB metadata/working bound,262144 JSON and38912 component operations. The two-path diagnostic/partial-identity scope, graph/path handling, stable-vs-observed hash distinction, helpers and unavailable operational/current-context producer remain unchanged. Source still must be independently reviewed; this is not a claim that the new algorithm already exists or is correct.

## Roster, authority and explicit source scope

Pure checks prove the exact117 typed entries mirror the declared arrays and retain all109 old entries in relative order, without duplicate kind/path pairs. Additions are only six exact target spellings found in actual STATIC02 incomplete reasons and one expressly unverified libsframe.so.1 hypothesis under the existing native directory, declared as alias+seed. No ancestors, Tcl9 guesses, discovery traversal or fallback are added. Old absent/wrong hypotheses remain INCOMPLETE rather than forced valid or silently dropped. Future needed-role binding is separately accepted work.

Activating the exact new source-defined plan includes only the necessary STATIC03/117 lower DATA grammar in addition to retained STATIC01/76 and STATIC02/109, with one fixed actual action hash/path. A JSON id/count cannot raise caps or create a role. The canonical mapping API preserves existing three positional arguments; an optional diagnostic output is only metadata. Removing the old report-only duplicate mapping calculation in elf() makes the canonical mapper the single decision/proof source, not an alternate validator or authority seam.

ROOT's87348bf3 retention amendment permits1024 retained evidence files, with actual546 noted in the packet; it changes no runtime/class/case/memory/time/read limit and grants no action/role. Future complete writer/capacity/joint-memory/case/clock and five-role reference closure remain unproven. This bounded inspector plan does not manufacture those facts.

## Genuine RED, preserved negatives and command staging

The first selector is an existing one-segment positive plus identical-duplicate refusal. The initial new RED calls the actual existing elf_string_table_offset with its existing three-argument signature and recorded adjacent interval DATA. Old source must hit its real MappingAmbiguous guard; checked_offset converts that known refusal to the explicit STATIC03_CANONICAL_CONTIGUOUS_FILE_COVERAGE_REQUIRED assertion. No new API, missing keyword, setup/import/type/resource failure is counted as RED. No RED has been run or observed by this review.

The five staged commands are: existing positive; one actual canonical adjacency RED; seven new methods; full48 DATA; full12 AST. Exact timeout/prlimit/system-Python/env bounds remain finite; no automatic batch/retry/follow-on exists. Only after genuine raw RED and its test-only commit may ROOT assign narrow production implementation. Fixed source safety, post-source tests and actual source-valid mutants/controls must then be reviewed before a distinct ROOT STATIC03 action. Future source/wrapper pins remain unresolved, so the actual public inspection remains blocked.

Sparse mock replies exercise a large logical table without allocating it. New tests assert exact read positions/sizes, one referenced4096-byte window, suffix truncation at table end, missing NUL refusal, and offset-at-end refusal before read. New union negatives separately cover VA gap, file gap/bias change, partial conflicting overlap, partial identical-bias overlap, memory-only tail and uint64 wrap. Existing identical-duplicate refusal remains. The old70000 whole-copy-bound case is preserved historically and explicitly amended to67108865 for the new logical64MiB cap, still checking exact refusal/raw value/no read. The old mapper AST pin is explicitly retired for this reviewed policy change; canonical string decoding and check()/38912 pins remain.

The one R0 review finding was the missing partial same-bias overlap variant. R1 adds LOAD(100,0,40)+LOAD(116,16,32), request[108,128), in the existing negative method. This rejects a uniform-bias merge bug even though the first LOAD covers the entire request. The exact tuple and six-case list were statically verified. Seven methods/60 full methods stay unchanged; new variants increase11→12. No source/prototype or resource/gate change was needed. This finding is closed.

The17 canonical contract dispositions from the prior source review remain applicable: no product/native/session/automation/platform examples are changed; resource-readiness identity-versus-qualification and closeout pending-acceptance boundaries remain explicit. New117 roster/cap mirroring is in the structural draft, and the exact two diagnostic path mirror is retained. This is a parser admission amendment with source-only tests, not original/Mac/TEST/P/CONTROL or full-M1 acceptance.

## Result and retained evidence

No remaining blocker. ROOT can proceed with the normal quiet test/plan-DATA adoption and reviewed positive→actual RED→observed test-only commit sequence. Production source review and actual STATIC03 action are later separate gates. Scratch audits: tracked-baseline-facts.json and static-packet-checks-r1.json. The reviewer audit note records one corrected case-label assertion in the metadata audit; it was not a product/test execution or semantic result. No worktree or effectful isolation was created.
