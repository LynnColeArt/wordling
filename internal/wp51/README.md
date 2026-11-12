# Native outer framing and exact no-edit export

WP02 implements T004–T006 against the approved
[WP01 contract](../../kitty-specs/wp51-parity-01M64CVY/contracts/native-framing.md)
and its [fixture catalogue](../../kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json).
It traces FR-002, NFR-001/003, C-001/002 and FC-002/004 to native preservation.
Story 1 scenario 1 supplies the no-edit obligation; the complete user workflow
and original-app semantic interoperability remain later acceptance work.

`Parse([]byte)` returns an immutable owned `Image` or a typed `*Failure` with a
category, absolute offset, field and detail. It checks the 16 MiB input limit
before an owned copy, validates the full header, iterates bounded linked index
blocks and packet spans, checks unsupported overlaps in a sorted temporary view,
and traverses body tokens exactly once. Packet spans and blocks remain in native
traversal order. Empty DE functions use the approved L=4 field equation.

`Export()` copies the complete image without reconstructing any field.
`Inspect()` copies framing metadata; `Bytes(Span)` copies a bounded range.
Input, exported bytes, inspected metadata and span copies cannot mutate owned
storage. The body span ends at EOF: valid suffix text is retained as body content,
and malformed suffixes refuse the entire input. Gaps and unused indexes survive
because the original byte image is authoritative. There is no guessed end marker.

The support declaration is `outer-framed, payload-unvalidated`. Packet contents,
function payloads, nested text, character identity, semantic references, paired
attributes and edit safety are not validated. Unknown framed function/packet
contents and deleted/reserved packets remain opaque. WPM and other companion
formats, other stored versions, encryption, nonzero reserved headers, alternate
index counts, nonzero graphics and overlapping packet structures receive explicit
refusal; they remain M1 obligations. A successful parse is not edit permission.

This package has no filesystem, terminal, external dependency, semantic edit or
general writer surface. WP03 must perform bounded acquisition (limit+1 for excess
detection), safe file replacement and storage failure handling. `Parse` accepts an
already acquired buffer; callers must not mutate it during the call.

## Validation

External-package tests use the exported API. All six original fixture hashes and
sizes are pinned against original run manifests; five document exports match
bytes, length and SHA-256, and the macro returns `UnsupportedFileType`.
CMD51-066/203/131/134 provenance is inherited from WP01, not newly observed in the
original app. Both synthetic append recipes retain their synthetic status.
Tests exercise seed truncations, identity and prefix failures, cycle/boundary/
overlap refusals, reserved/deleted/unknown data, graphics ordering/counts,
all fixed widths, D0–FF trailers, L<4/L=4/max-u16 lengths, opaque payloads,
caller isolation and exact/over input and traversal limits. Truncation after
complete body tokens can legitimately be accepted: the format has no body length
or document-end marker. The tests check preserved bytes in those cases.

The 16 MiB maximum body needs no per-token allocation. Metadata is bounded by
4,096 blocks / 16,384 packet entries, with O(E log E) overlap validation. The
packet-entry ceiling also follows from four general entries per accepted block.
Single-byte body token count is bounded by body bytes; no generic recursion runs.
These are conservative reader policies, not historical format limits.

Validation records and reproducible commands are in `evidence/`. Resource results
measure the declared host/harness only. Fuzz execution counts are nondeterministic;
no crashes or passing tests establish complete file semantics or full M1 parity.
