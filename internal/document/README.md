# Immutable native document positions and bounded edits (WP15/WP25)

T043–T045 implement a bounded consumer of approved `internal/wp51`. `Parse`
first calls its actual reader; malformed/unsupported native framing retains its
original typed error. This layer indexes complete already-validated body tokens
and recognizes only printable ASCII20–7E, C3 0C C3 Bold On and C4 0C C4 Bold Off.
All other complete tokens are opaque, retaining exact source spans and bytes.
Recognition is token identity, not validation of paired-code relationships,
packets, nested content, edit safety or printed attributes.

`Document` owns an immutable image and private gap-offset index. Export returns a
fresh exact native copy; token inspection copies raw bytes. A `Cursor` is a value
binding that same document to one token gap and a Reveal visibility flag. Move
supports one adjacent gap at a time across supported tokens, including a Bold
code with no normal-view text. It refuses crossing opaque tokens, invalid gaps,
invalid directions and end boundaries without changing the original cursor.
`CursorAt` constructs an explicit coordinate; it is not an implementation of an
original Home/GoTo command. Those endpoint command semantics remain WP13/WP17.

`Present(start,count)` returns bounded typed elements derived from the cursor's
view. Normal and Reveal share token indices/source spans and cursor gap. Normal
Bold text is empty but its element/identity remains; Reveal labels are `[BOLD]`
and `[bold]`, as observed in EC-048. Opaque presentation refuses with its token
and absolute span, rather than hiding bytes or guessing a glyph. Inspection and
exact export remain available after that refusal. No terminal cells, inches,
Unicode normalization, wrapping or native serialization define these positions.

The original paired fixture is the WP01-pinned advanced03/CMD51-203 ORIGIN.WP5:
334 bytes, SHA256 c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d.
It has body324 `41 C3 0C C3 42 43 C4 0C C4 44` and gaps
324,325,328,329,330,333,334. This is existing original-produced evidence;
no new original run, Wordling semantic write or full CMD51-049 comparison occurs.
The before/after presentation tests prove the specified immutable coordinate
model, not a new observation of the original app's internal data structures.

## Declared safety policies before implementation/fuzzing

WP02 enforces at most16MiB input,4096 index blocks and16384 packet entries.
This layer additionally refuses more than1,048,576 body tokens *before* allocating
its gap index. The index has exactly token-count+1 uint32 offsets (at most
4,194,308 bytes), plus one WP02-owned image. A temporary bounded body copy is used
for indexing; no per-token object/raw slice is retained. Body traversal is linear,
no recursion. Unsupported high-token inputs remain M1 follow-up; this is an
implementation work/memory policy, not an original DOS capacity claim.

Present accepts at most4096 tokens per call and fails before producing any partial
result if the requested window includes an opaque token. Token inspection copies
only the selected framed span. Only the requested contiguous native window is copied for presentation; an opaque
window is refused before element allocation. The copy remains bounded by input
size. Benchmarks report that cost; no product latency target is selected here.

Fuzz budget: two workers/GOMAXPROCS2,60s smoke then120s expanded run, maximum
native input16MiB, offset/index/window bounds above. Seed original fixtures and
labelled synthetic unknown/fixed/variable/invalid inputs. Assert no panic, source
mutation, unbounded indexing, byte loss or cursor inside a token. Resource and
wall-time measurements are host/harness observations, not exhaustive proof.

The historical WP15 slice above grants no mutation authority. WP25 adds only the
explicitly admitted ASCII insertion/typeover and original-format candidate writer
described in [its evidence checkpoint](evidence/wp25/README.md). Deletion/selection/
Undelete, file IO, Bubble Tea, C0 mapping and arbitrary attribute interpretation
remain separate. All FR/FC parent obligations and M1 parity remain open.
