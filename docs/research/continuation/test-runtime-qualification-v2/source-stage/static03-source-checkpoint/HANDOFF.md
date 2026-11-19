# Fixed STATIC03 source: review candidate only

After actual canonical adjacency RED cf54d912 and ROOT causal inspection7dd3a112,
this implements only the independently approved STATIC03 admission amendment.
It is not full WP108/T350/351/352 completion, current-context/reference authority,
producer/coordinator or execution permission. The actual generate Op stays open.

The single canonical mapper now proves the entire checked uint64 logical range
has exactly one file-backed translation, using ALL intersecting segments. It
rejects holes, any overlap (identical too), changed bias/file discontinuity,
memory-only tails and wrap. It cannot stop at an apparently complete first match.
The ELF caller then checks the continuous file range against actual snapshot
size, validates each referenced offset and reads only min(4096,remaining) windows
through unchanged canonical elf_string_data. No logical table buffer/read is
created. This deliberately supersedes old mapper/whole-table-copy admission;
it is not claimed as preservation of that old AST.

Exact117 plan95ffd107 is installed at the reviewed fixed path, retaining all109
old typed items in relative order. Twenty other AST bodies, two diagnostic names,
partial-identity/graph/path rules, blocked context/operations, three helpers and
17contracts are conserved. All old global bounds/check38912 remain unchanged.
New logical size<=64MiB is checked against file coverage; per-window<=4096 and
<=131references imply at most610368metadata bytes perELF under the existing1MiB.

The exact reviewed new7methods and full48DATA+12AST passed. Ten real source
postimages were each preceded by the original source passing in the same fresh
DATA fixture path: gap, overlap, bias/file gap, memsz, early first match, window,
suffix, whole table, read-before-mapping, and uint64. Nine produced intended
assertion failures. The whole-table request produced the real deterministic
StaticReadChunkBound before OS pread, reported as a separate canonical guard
kill/unittestERROR, never setup/exhaustion or the initial semantic RED. No actual
unexpected failure or partial output occurred. Every raw output/postimage and
same-path control remains preserved. The one stateless source fixture (three
files) was removed; no Preparation/live owner or worktree was made/reset.

A single shared capture source and three receipt files per command keep retained
purpose files within the explicit<=136 allocation; exact counts are in
allocation.json. No preexisting raw/history was removed. The 32file independent
review reserve is untouched; unused/future pools are not execution permission.

custody-packet contains the unexecuted future STATIC03 launcher, adapted from the
actual STATIC02 launcher only for fixed labels/source/plan pins. Source/test/plan,
wrapper/tool identities and independent SOURCE_FOR_STATIC03_ONLY plus exact
retention/writer allocation require ROOT verification and a deliberate separate
invocation. No actual STATIC03 directory/action or public lookup occurred here.
Unknown required-vs-wrong hypotheses (including Tcl), five roles, actual source/
cache/native behavior, full coordinator, all surviving writers, joint memory and
runtime case/time/clock closure remain pending. No absent hypothesis is forced
valid and no candidate output became an oracle.
