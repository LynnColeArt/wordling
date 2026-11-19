# STATIC03: bounded admission amendment, test first

Scratch only: no production prototype, primary/index change, helper import,
test run, or public-asset lookup. ROOT retains primary/index ownership.

STATIC02's preserved diagnostics establish the two relevant shapes. BASE's
42266-byte logical table starts at VA4191704 and crosses two adjacent file-backed
LOADs with the same bias4190208: file[1496,43762). cc1's1199001-byte logical table
fits one LOAD: file[868656,2067657). These are static arithmetic facts from
unaccepted DATA, not a qualified runtime/reference or proof of actual execution.

This explicitly amends admission. The old one-whole-segment/65536-table-copy
predicate is NOT claimed preserved. The canonical mapping function must prove
the whole requested range has exactly one file-backed translation per byte,
with no gap, intersecting overlap (including identical mappings), file-offset
discontinuity, changed bias, memory-only coverage or uint64 wrap. It must examine
ALL intersecting segments before accepting; a full first match cannot hide a
partially overlapping second mapping. The actual caller checks the resulting
file interval against the frozen file length before reading strings.

The logical table is bounded by the existing64MiB file ceiling. It is never
allocated or read as a unit. Only referenced DT strings get windows of
min(4096,logical_size-offset), then the unchanged canonical elf_string_data is
called. Its65536 raw-buffer/4096 terminator bounds remain exact. With at most131
references the conservative per-ELF read work is610368bytes, below existing1MiB.
All global caps, operation38912, two-name diagnostics/partial-fact scope, graph,
path handling, helpers and unavailable context/operational producer stay intact.

The117-item plan retains all109 typed entries in relative order, then adds only
six exact previously unlisted symlink target spellings and an explicitly
unverified libsframe.so.1 hypothesis under the already-declared native directory
(alias+seed). No Tcl9 guesses or target discovery. Existing missing/wrong
hypotheses remain recorded INCOMPLETE; a later actual-role binding must explicitly
separate needed actual inputs from wrong/unneeded hypotheses. This inventory
cannot construct that binding or force all hypotheses valid.

Seven new test methods cover twelve new DATA variants. The six negative union
inputs are separately counted, and the existing identical-duplicate rejection
remains. Sparse fixtures allocate only small header/program/dynamic/string
replies, never the logical table. The exact five-command plan runs an existing
positive then one actual canonical adjacency RED before ANY production change.
Only after raw RED/test-only commit may implementation and post-source/full60
checks run. Missing APIs/setup/types/resource failures are never semantic RED.
The old bound fixture explicitly changes70000 to67108865 for the new logical cap;
its old source/negative raw history remains immutable. The old mapping AST pin
is explicitly replaced by canonical string decoder conservation; check38912
remains exact. No effect approval or broad WP108 completion follows from review.

ABI sources define segment file/VA fields and DT pointer/table-size/index
semantics: [program headers](https://gabi.xinuos.com/elf/07-pheader.html),
[dynamic entries](https://gabi.xinuos.com/elf/08-dynamic.html). The adjacent-union
proof is this proposal's inference from those fields plus the recorded intervals,
not a claim that the ABI or current diagnostics qualify BASE.
