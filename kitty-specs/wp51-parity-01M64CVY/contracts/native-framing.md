# WP01 native framing and fixture contract

Research handoff, 2026-10-30. This document defines the first bounded reader
slice; it does not claim a reader, writer, macro interpreter or parity is
implemented. M1 remains full WP 5.1 DOS parity. PDF remains optional M2 export.
Authority: `spec.md` FR-002/003, NFR-001/003, C-002/004; `docs/compatibility.md`
FC-001–007/009; ADR 0002. Paths below are repository-relative unless stated.

## Evidence and applicability

SDK51 is the locally cached `research/cache/WP51DevelopersToolkit.pdf`,
SHA-256 `5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754`.
Its source/rights record is `docs/research/sources.json` and the mission's
`research/source-register.csv`. The ignored extracted text is
`research/cache/toolkit.txt`; its exact hash is in `native-fixtures.json`.
No manual text, binary or bundled resource is added by WP01. Field descriptions
below are independently written format facts, not a republication of the manual.

Page references use the printed WP subsection page and the **one-based PDF page**
(WP page + 13). Exact local text locators are included for reproducibility.
SDK51 publication is MNUSXTW511-12/93; WP pages carry intermediate `??/92`
marks. It includes WPWin/UNIX additions and is not evidence that all such features
exist in the selected plain DOS 1992-03-09 executable. The fixture headers and
framing corroborate the stated subset against that original executable.

| Topic | SDK51 locator | Local text lines |
| --- | --- | --- |
| Prefix field layout | WP-3, PDF 16, File Prefix | 530–553 |
| Signature, absolute document pointer, byte order | WP-4, PDF 17, WPCorp File ID / Start of Document | 580–603 |
| File types | WP-5–6, PDF 18–19, General Purpose / WordPerfect File Types | 632–715 |
| Version, encryption, reserved | WP-6, PDF 19, corresponding field headings | 697–715 |
| Linked block header | WP-7, PDF 20, Additional Prefix Area / Special Header Index | 717–741 |
| Packet index and sentinels | WP-8, PDF 21, General / Special Data Packet Types | 768–825 |
| Graphics packet exception | WP-12, PDF 25, Packet Type 8 | 989–1010 |
| End conditions / abbreviated prefix | WP-16, PDF 29, Abbreviated Prefix | 1251–1267 |
| Body framing, length definition | WP-17, PDF 30, Document Area | 1273–1319 |
| Nested text and unknown codes | WP-18, PDF 31, Text Fields | 1325–1343 |
| Fixed functions | WP-23–26, PDF 36–39, C0–CF definitions | 1517–1724 |

The original environment is pinned in `docs/research/reference-baseline.json`,
`reference-environment/environment.json` and `resource-profile.json` under
`docs/research/`. It uses QEMU 8.2.2, FreeDOS 1.4, the March executable and a July
1992 Standard Printer. It is not historical DOS or a graphics/font oracle.
Run manifests archive actual input traces, executable/profile identity, runner
sources and export hashes. They state original-reference-only and Wordling not
tested. The existing `scripts/reference/document.py` is a bounded fixture
inspector. Its assumptions (including mandatory packet 6 and skipping zero
entries) do not override SDK51, establish general codec validity or define errors.

## File prefix: absolute byte offsets

All reads require the complete width first. `short` is an unsigned 16-bit
little-endian integer and `long` an unsigned 32-bit little-endian integer for
these fields; individual signed semantic payloads require separate contracts.

| Offset | Width | Meaning and initial reader rule |
| --- | --- | --- |
| 0 | 4 | Signature `FF 57 50 43`; otherwise UnsupportedFormat. |
| 4 | 4 | Absolute body offset B; require `16 <= B <= file length`. No offset is relative to an index. |
| 8 | 1 | Product 1 for this document slice. Other products: UnsupportedProduct. |
| 9 | 1 | File type 10 for WP documents. WPM type 1 is a companion and returns UnsupportedFileType here. Extension is never authority. |
| 10 | 1 | Stored major 0 for supported documents. |
| 11 | 1 | Stored minor 1 for selected WP5.1. Major/minor differ from marketed version. Other tuples: UnsupportedVersion. |
| 12 | 2 | Password hash/key; zero unencrypted, nonzero UnsupportedEncryption before interpreting prefix/body. This contract implements no password/decryption. |
| 14 | 2 | Reserved, documented zero. Nonzero: UnsupportedVariant, retain source unchanged. |

The tuple `(1,10,0,1)` is necessary, not sufficient, to identify the DOS target:
WPWin 5.1/5.2 share stored versions. Never infer executable provenance from it.
WP5.0 minor 0, headerless WP4.2, blocks, dictionaries, styles, WPK, SET and printer
resources remain separate outstanding M1 formats. Merge primary and secondary
files in this corpus have document type 10; their roles are scenario metadata,
not distinct invented native type values. WPM has observed `(1,1,1,1)` and a
four-entry index, expressly outside document validation.

## Prefix traversal and spans

B separates the prefix `[0,B)` and body `[B,N)`. The 16-byte file header is
followed by the first index block at absolute offset 16. A document block header
is ten bytes. At block base I:

| Relative offset | Width | Meaning |
| --- | --- | --- |
| 0 | 2 | Special header type `0xFFFB`. |
| 2 | 2 | Number C of indexes, **including this header**. |
| 4 | 2 | Index block size S; require `S == C * 10`. |
| 6 | 4 | Absolute next block offset; zero terminates the chain. |

SDK51 WP-7 explicitly describes five entries / 50 bytes for WP5.0/5.1 documents.
The selected five documents agree. The first reader accepts `C=5,S=50` only;
other nonzero consistent counts are UnsupportedVariant, not automatically corrupt
and not generalized from the macro's observed `C=4,S=40`.
For zero count, bad type, inconsistent S, incomplete header/block or out-of-range
pointer return MalformedPrefix. Before multiplication or slicing use checked
arithmetic, e.g. `I <= B` then `S <= B-I`; never allow wrap into a valid slice.

Each general index begins at `I + 10*j`, `1 <= j < C`:

| Relative offset | Width | Meaning |
| --- | --- | --- |
| 0 | 2 | Packet type K. |
| 2 | 4 | Packet data length L. |
| 6 | 4 | Absolute packet data position P. |

For an ordinary/deleted/reserved packet require `16 <= P <= B` and `L <= B-P`.
A zero-length span may end exactly at B; do not allocate by L. Keep the index
bytes, packet span and order even when the packet is not semantically decoded.
Do not require packet 6, sort data physically on export, or compact deleted data.
This initial policy refuses nonempty packet/index overlap, overlapping nonempty
packet spans (including aliases), blocks overlapping header/other blocks, or
pointers into body/header as UnsupportedStructure/MalformedPrefix as applicable.
Such overlap is not proven prohibited for all original variants: it is an explicit
unvalidated variant, not a claim of universal format invalidity.

Traversal is iterative. Record visited block offsets, count blocks/entries and
validate each full block before reading its entries. A repeated offset is
MalformedPrefix/Cycle. A nonzero next pointer is checked when followed; a cycle
must never become a hang. A type 0 index terminates the prefix enumeration per
SDK51 WP-16, even when the next pointer is nonzero. Do not treat later zero slots
as ordinary packets, or follow links after that terminator. All remaining bytes
still belong to the retained image; unused index slots need not be rewritten.
If no type 0 was encountered, a zero next pointer ends enumeration. Data gaps,
unused indexes and any bytes between the last referenced span and B are retained;
not every prefix byte needs to be semantically claimed. No physical contiguity
assumption substitutes for absolute pointers.

`0xFFFF` denotes deleted packets, which may persist with Fast Save. `0xFFFC`–
`0xFFFE` are reserved; bounded spans may be retained as opaque, with no edit
support. `0xFFFB` is the special header and is refused in a general entry.
Unknown ordinary packet types remain opaque with their exact bounded spans and
index relationships. Their contents are **not structurally or semantically
validated** merely because P/L are in range.

**Packet 8 exception:** SDK51 WP-12 says its index is last except for a type 0
terminator and its indexed length is 2, a graphics count. Images have a following
size table and data not described by that index length alone. In the initial
slice require it last, L=2 and count=0; wrong/truncated indexed spans are malformed,
nonzero graphics count is UnsupportedStructure. Do not infer graphics ownership
from `[P,P+2)` or discard the subsequent bytes. All selected documents contain a
zero count at the end of the prefix. Nonzero graphics need a separate validated
extent/resource contract before acceptance, and remain M1 work.

## Body framing and evidence discrepancy

The file header provides **no body length or explicit document-end marker**.
The outer body spans all bytes `[B,N)`. A suffix of valid text is indistinguishable
from ordinary body content by this framing alone. Never truncate at a guessed
terminator, NUL, last recognized code, packet boundary or formatter record.

At position Q, ensure progress by consuming exactly one outer token:

- Values `01–1F`, `20–7E` and `80–BF`: one byte; reserved single-byte values
  retain their identity without invented semantics. Standalone `00` and `7F`
  are MalformedBody. `FF` must be handled as a possible multi-byte function,
  never as a standalone character.
- Fixed functions C0–CF have full widths respectively
  `4,9,11,3,3,5,6,7,4,5,6,6,8,10,10,12` bytes. Check available bytes and the final
  byte equals the opening function. Payload is opaque unless separately decoded.
  C8–CF are reserved with documented widths; unknown does not mean zero-width.
- D0–FF variable functions: `function:u8, subfunction:u8, L:u16le`, data,
  `L:u16le, subfunction:u8, function:u8`. The full span is **L+4 bytes**.
  The first four bytes are at Q..Q+3; closing length is at Q+L, closing
  subfunction at Q+L+2, closing function at Q+L+3. Require L>=4 and full span
  in the remaining body; require both lengths, subfunctions and function bytes
  to match. Data occupies `[Q+4,Q+L)`. Length arithmetic must be checked before
  access; no scanning ahead to find a convenient matching delimiter.

SDK51 WP-17's prose also calls nine bytes the smallest variable function. The
**original merge primary and secondary contain eight-byte `DE 36 04 00 04 00
36 DE` / `DE 31 04 00 04 00 31 DE` functions** (see manifest token offsets).
They have empty payloads and agree with the L+4 field equation, so the contract
accepts L=4 rather than enforcing the contradictory prose minimum. This is a
bounded observed exception, not a license to invent other lengths. Formatter
D4/00 examples have L=28 and full length 32. Attribute ON/OFF C3/C4 are three-byte
framing with matching delimiters; pairing semantics are separate from framing.

Nested text areas obey body rules (SDK51 WP-18), but the outer frame does not say
which bytes of an arbitrary payload are nested text. The initial reader keeps
all function payload bytes opaque and does **not** recursively validate nested
text, packet-internal offsets, character mappings, pairing or semantic references.
That distinction must be exposed as `outer-framed, payload-unvalidated`.
Unknown function/subfunction is safely retained only after outer length/trailer
checks; unknown bytes lacking those checks are structurally unvalidated, never a
successful fully validated body. Semantic edits remain refused for this slice.
A future nested decoder needs type-specific text boundaries and recursion limits.

## Preservation and failure interface

Successful no-edit export returns a fresh exact copy of the complete owned input
image: same length, bytes and SHA-256. Input buffers and returned buffers cannot
mutate that image. The parser must not rebuild indexes, headers, timestamps,
lengths, padding, reserved bytes or packet order. The image remains authoritative
regardless of semantic coverage. Trailing bytes are never dropped; a malformed
suffix returns explicit refusal, retaining caller/source bytes unchanged. A raw
image retained for diagnostics after refusal is not an accepted native document.

Required typed failure categories (names may be mapped explicitly in WP02):
UnsupportedFormat, UnsupportedProduct, UnsupportedFileType, UnsupportedVersion,
UnsupportedEncryption, UnsupportedVariant, UnsupportedStructure, InputLimit,
TraversalLimit, TruncatedInput, MalformedPrefix (including Cycle/Overflow), and
MalformedBody (including DelimiterMismatch/Overflow). Include absolute offset
and violated field/boundary where available. A header shorter than 16 is
TruncatedInput. Check size limit before copying; require full header before
identity fields; classify encrypted/type/version variants before body decoding.
All failures preserve original data and never imply a successful edit/save.
Filesystem replacement and save-transaction failures belong to WP03.

## Corpus, provenance and measurements

`native-fixtures.json` is the machine-readable catalogue. It pins six existing
original-produced outputs: plain text, a real bold ON/OFF pair, recorded macro,
merge primary, merge secondary and merge result with deleted Fast Save packets.
Every file hash/size is checked against its run manifest's evidence entry, not
only recomputed from the current file. Each record gives scenario/run/runner
archive, baseline, header, index fields, packet spans/hashes and body hash.
CMD51-066/203/131/134 link stable command evidence; Story 1 scenarios 1/2 and
Story 4 scenario 1 remain acceptance obligations, not newly verified claims.
These are project-authored inputs recorded/exported through the original app,
not bundled samples, installers, dictionaries or copied manuals. Existing public
capture/resource identity rights are unchanged; the project license does not
relicense third-party resources. No new proprietary payload is redistributed.

Measured from these exact six outputs: maximum input 683 bytes; prefix/body
boundary 564; body 119; three linked index blocks; nine live/deleted packets;
six outer multi-byte tokens. Five documents have product/type/version
`1/10/0/1`; the macro has `1/1/1/1` and is an intentional document-parser negative.
All selected document outer tokens end exactly at EOF; no original-produced
trailing-garbage, encrypted or nonzero-graphics fixture has been established.
Opaque packet content is abundant but is not evidence of an unknown packet type.
These gaps remain explicit original-app research, never a compatibility claim.

Two supplemental recipes embed append bytes and resulting hashes in the JSON:
plain+ASCII suffix proves complete EOF retention; plain+`00 7F FF` requires
MalformedBody without losing source bytes. They are **synthetic**, not original
outputs and not proof that WP accepts trailing garbage. Neither alters raw files.
WP02 must materialize them in test-only storage or memory, preserving provenance.

## Resource limits and malformed/fuzz acceptance

These are conservative implementation safety policies, **not original DOS format
limits or measured product performance guarantees**. Larger/deeper valid variants
remain M1 obligations requiring measured follow-up rather than silently disappearing.

| Resource | Initial bound | Corpus maximum / rationale |
| --- | --- | --- |
| Input / owned image | 16 MiB | 683 bytes observed; bounded file acquisition reads at most limit+1 to detect excess, then refuses before owned copy. No unbounded ReadAll. |
| Export copy | 16 MiB | At most one full fresh image per call; caller copies outside parser ownership are not a parser guarantee. |
| Index blocks | 4,096 | 3 observed; check before append/traversal. |
| Packet entries | 16,384 | 9 nonterminator spans observed; includes deleted/unknown entries. Five-entry blocks cap general entries at 4 per block. |
| Outer body traversal | <= body bytes, at most 16 MiB tokens | 119 body bytes observed; every iteration advances and bytes are never revisited searching for delimiters. |
| Nested validation depth | 0 | No generic recursive decoding in this slice; nested payloads explicitly unvalidated and preserved. |
| Variable function size | u16 L + 4, at most 65,539 bytes | Format width; checked against actual remaining input before slicing. |

Do not allocate per declared packet length or per raw next pointer. Bound metadata
by the entry/block counts. Check overlap with bounded span comparisons; avoid
quadratic work over input bytes. The ownership budget is one <=16 MiB image plus
bounded metadata, and a <=16 MiB output copy per export; no runtime memory or
latency measurement exists yet. WP02 must measure its actual harness and record
results before parser acceptance, including at and beyond these bounds.

The deterministic malformed matrix must include every seed truncation point;
short header; wrong signature/product/type/version; encryption/reserved fields;
B below 16/past EOF; missing/partial index; wrong type/count/size; next pointer
into header/body/outside file; self and two-block cycles; packet starts/lengths
crossing prefix/body and u32 overflow; packet/index/data overlaps; early type 0
with malicious ignored next pointer; zero next with no terminator; deleted and
reserved packets; packet8 count/length/ordering/nonzero graphics; fixed function
truncation and trailer mismatch; variable L=0..3, L=4, maximum L, truncation at
each component, unequal lengths/subfunctions/functions; standalone 00/7F;
unknown framed fixed/variable functions; suffix retention/refusal; input and
traversal limit boundaries. Invalid mutations must never panic, hang, partially
succeed, or mutate caller bytes. Structurally consistent but unvalidated variants
must distinguish unsupported from malformed. An opaque nested payload is not a
negative test for recursive decoding that the first slice does not implement.

Seed WP02 fuzzing with all six original files (including macro refusal), both
synthetic append recipes and deterministic malformed boundary cases. Required
repeatable command after WP02 adds the named Go target:

```sh
GOMAXPROCS=2 go test ./internal/wp51 -run='^$' -fuzz=FuzzNativeFraming -fuzztime=60s -parallel=2
```

Run a 600-second budget with the same concurrency before parser release; retain
seed hashes, Go/toolchain/host identity, command, duration, executions, peak memory
and crashes as evidence. A 60-second time budget is reproducible configuration,
not a deterministic count of random cases or measured throughput. WP01 has no
parser/fuzzer and claims **no fuzz run or passing malformed implementation**.
The immediate corpus measurements above justify seed/input sizing only.

## Validation and implementation handoff

WP01 checks catalogue JSON, all paths/hashes against raw evidence, checked prefix
spans and outer body boundaries, plus both repository catalogue `--check`
commands. No source/code or proprietary evidence is edited. Claim-time runtime
baseline reports a single synthetic `<gate-coverage-junit>` failure:
`no JUnit XML artifact produced by the scoped run` under a pytest runner. The
repository currently has a Go module and no application tests. That report is a
gate/evidence collection failure, not an observed application assertion; it must
remain visible and be resolved by the runtime owner, not masked by fabricated
JUnit or skipped gates.

WP02: implement immutable image, checked prefix/outer framing and explicit support
states/errors with the deterministic and fuzz matrix; no semantic mutation.
WP03: implement safe filesystem transaction separately. Subsequent packages must
research encrypted/graphics/nested/Fast Save aliases/other-version variants,
produce original trailing/opaque-unknown fixtures, decode each companion format
independently, and validate every writer slice in the original app. A hash-copy
pass proves no-edit preservation only; it cannot establish new-document writing,
semantic edits, macro execution, layout, original print behavior or M1 acceptance.

The corpus/hash measurement can be reproduced from the repository root without
running an emulator or changing any fixture:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json, struct
m = json.loads(Path('kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json').read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
for source in m['sources']:
    assert sha(Path(source['path']).read_bytes()) == source['sha256']
for f in m['fixtures']:
    d = Path(f['path']).read_bytes()
    assert (len(d), sha(d), d[:16].hex()) == (f['size_bytes'], f['sha256'], f['header_hex'])
    assert struct.unpack_from('<I', d, 4)[0] == f['body_offset']
    assert sha(d[f['body_offset']:]) == f['body_sha256']
    run = json.loads(Path(f['run_manifest']).read_text())
    case = next(r for r in run['results'] if r['case_id'] == f['scenario_id'])
    assert any(e['path'] == f['path'] and e['sha256'] == f['sha256'] and
               e['size'] == len(d) for e in case['evidence'])
    for block in f['indexes']:
        assert struct.unpack_from('<HHHI', d, block['offset']) == (
            65531, block['count'], block['size'], block['next'])
        assert block['size'] == 10 * block['count']
        assert 16 <= block['offset'] <= f['body_offset'] - block['size']
    for p in f['packets']:
        assert 16 <= p['offset'] <= f['body_offset']
        assert p['length'] <= f['body_offset'] - p['offset']
        assert sha(d[p['offset']:p['offset'] + p['length']]) == p['sha256']
    for field in ('run_manifest', 'runner_archive', 'scenario_registry'):
        assert Path(f[field]).exists()
for r in m['supplemental_recipes']:
    seed = next(f for f in m['fixtures'] if f['id'] == r['seed_id'])
    d = Path(seed['path']).read_bytes() + bytes.fromhex(r['append_hex'])
    assert (len(d), sha(d)) == (r['size_bytes'], r['sha256'])
assert max(f['size_bytes'] for f in m['fixtures']) == m['measurements']['max_input_bytes']
assert all(f['size_bytes'] <= m['limits']['max_input_bytes'] for f in m['fixtures'])
print('six originals and two synthetic recipes: hashes, source evidence and bounds valid')
PY
```
