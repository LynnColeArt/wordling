# WP108 STATIC01 R7 independent design review

**APPROVE_STATIC_INSPECTION_DESIGN** for the exact R7 proposal below. No blocking design finding remains. This verdict permits implementation of this dormant finite inspection design; it is neither reader/source approval nor permission to inspect the listed files, execute the command, accept reference data or advance WP108.

Reviewer: actual resolved reviewer-renata; existing read-only action-review governance/profile context reused as authorized. Independent of the source author. ROOT owns primary checkout/index, task lifecycle and all actual actions; no Op, claim, verdict event or state was written by this review.

## Exact reviewed inputs and performed checks

- `/tmp/wordling-wp108-test-prep/static-inspection-proposal-r7.json`: SHA256 `58a299ac5acebfd20b5c3ad1ad42a69985e6160ed13ab1ea97e722e451fd4fbd`, 18094 bytes.
- `/tmp/wordling-wp108-test-prep/STATIC-INSPECTION-r7.md`: SHA256 `0edf44f34ec6e3b460cf52fae9cca0e08136218482e7732d4628263afc3f8d49`, 2793 bytes.
- Both original R6 hashes remain exact: JSON `0d076465d8e39c1c62efa3ccd2bfa99378ee192ad06b07172bed1e04f8926d30`; MD `7412c0a63b2865eaaa3ad6deb123ad85d4b76ab4e9d9d372dd802c41b0fe0696`.
- Pure JSON/path-string checks independently verify all four R6 roster arrays unchanged: 18 ELF seeds, 14 aliases, 13 metadata directories and 3 loader-data files. The 28 ancestor entries equal the exact lexical-parent union of those literals; no observed filesystem name was adopted. The 76 typed operations and order match their arrays, with no extra operation. Repeated paths in distinct typed roles are explicit counted operations, not 76 distinct files. Exact argv/environment and every pre-existing ceiling are unchanged.
- Read only the frozen proposal, canonical WP108 task, existing review context and committed launcher metadata. No reviewed Python module was imported, no proposed reader/test/probe was run, and no listed public/BASE executable, library, directory or loader input was inspected. The check artifact is `static-proposal-checks.json`.

## Design findings resolved

**Independent-item discovery is compatible with the canonical task.** T350 says unknown discovered paths stop for review; it does not require discarding independent observations of already declared inputs. R7 stops the unresolved item's branch, never reads an unlisted target, continues only the original fixed roster, and marks the entire result INCOMPLETE and unusable for qualification. It therefore preserves that gate while avoiding a new source-review cycle merely to learn each already listed filename is absent. Missing/unsupported/unstable/ambiguous/unlisted input is an item result. Clock, read/memory/output/FD exhaustion, source/tool mismatch, unsafe I/O invariant or internal fault ends the whole run and preserves bounded partial INCOMPLETE evidence. There is no retry, fallback, dynamic search or roster growth.

**Parent traversal is now explicit.** R7 requires anchored directory descriptors and component-relative no-follow validation before file reads, not just final-component O_NOFOLLOW. Declared ancestors are metadata-only; declared aliases can resolve only to explicitly declared names under finite hop/text caps. Unexpected parent links/targets cannot be followed before being classified. A failed parent must also prevent dependent item reads while unrelated declared items may continue. The future source review must verify the actual implementation of these rules; this document does not assert they already exist in code.

**The memory/read contract is implementable.** Regular hashing uses chunks at most 65536 bytes, with every actual read including ELF rereads charged before the read. The 64 MiB per-file and 256 MiB aggregate values are byte-read limits, not permission to allocate those amounts. Metadata work is bounded to 16 MiB under 160 MiB address space; fixed ELF64 little-endian x86_64 format, table/entry/string bounds and in-file intervals prohibit unbounded decoder allocation. The actual parser, resource accounting, bounded serialization/error output, stable identity checks and partial-failure preservation await source review.

**Static metadata confers no role.** Literal DT_NEEDED/interpreter/RPATH/RUNPATH strings are proposed facts only. An absent library, alias target, ambiguous address/edge, cache body or publisher claim remains unresolved. No ldd, ldconfig, loader execution, native import, tool/BASE execution, Preparation, issuer, TEST/P or operational context is introduced. Historical V19/188 evidence stays unchanged; five-role reference/native/tool/cache/source/writer/joint-memory/clock closure and independent acceptance remain outstanding.

## Launcher provenance and remaining execution gates

The referenced committed R4 artifact was independently rehashed: `kitty-specs/wp51-parity-01M64CVY/tasks/WP108-current-test-runtime-qualification/preparation/data-api-r3/quiet-turn-launcher-static-r4.json`, SHA256 `028a8ae6ee750dbe914cb2974991d9b27b3acab6cb4df76d6ef437afc890d90c`, 2001 bytes. It records three historical static launcher identities (timeout/prlimit/system Python), 8088344 bytes and dependencies NOT_ANALYZED. It is not a current byte/rights revalidation, full native dependency closure, accepted TOOL reference or authorization. R7 accurately retains this distinction.

Before any actual STATIC01 invocation, freeze and independently review the real reader source, imports/caller dispatch, exact literal rosters/order and all enforcement paths, including parent/alias races, streaming budgets, ELF bounds and output destinations. Bind its exact source hash and exact launcher identities to a deliberate ROOT action with bounded argv/environment/output. The invocation must be withheld when those identity/review facts are absent or wrong; this review does not invent a new actor-authentication API inside the DATA reader. No raw JSON/schema/CLI flag can create the trusted ROOT actor or accepted qualification context. These are already declared R7 gates, not approval to act now. Full operational qualification closure is not required merely to implement a dormant finite DATA inspector; it is required before its facts can be used for that later purpose.

## Contract disposition

This is a design-only inspection prerequisite, so no product payload, command result or native token is implemented or claimed to round-trip. Canonical WP108's exact staged order, unchanged old-purpose guards and independently accepted expected-before-candidate boundary govern the design. The current 17 contract files were inventoried:

| File | Disposition for this bounded design |
| --- | --- |
| resource-readiness.md | In scope: identity/access is separate from qualification; present-but-unqualified and unknown fields remain explicit. R7 overall INCOMPLETE and remaining-role limits preserve that distinction. |
| mission1-closeout-coverage.json | In scope only for claim boundary: no family, source obligation, platform or acceptance gate is promoted by inspection. No snapshot/index is edited. |
| mission1-closeout-coverage.md | Same claim boundary; no coverage or acceptance output is authored. |
| native-fixtures.json | Orthogonal: no native fixture byte or interpretation changes. |
| native-framing.md | Orthogonal: no native document parser/writer change. |
| macro-fixtures.json | Orthogonal: no macro fixture or expected result change. |
| macro-framing.md | Orthogonal: no macro token/framing implementation. |
| automation.md | Orthogonal to macro/merge/recording semantics; no controller or macro action is run. |
| session.md | Orthogonal: no editor/session lifecycle or buffer change. |
| editing.md | Orthogonal: no editing or Retrieve/Copy semantics change. |
| files-platform.md | Orthogonal to product file save/platform behavior; inspection changes no product filesystem policy. |
| layout-resources.md | Orthogonal: no layout/resource interpretation or original calibration. |
| structured-graphics.md | Orthogonal: no graphics codec or original comparison. |
| language-data.md | Orthogonal: no language/locale data access or codec. |
| startup-family-successors.md | Orthogonal: no product startup successor command or acceptance. |
| coverage-concordance.md | Orthogonal to index implementation; all full-census obligations remain pending. |
| coverage-leaves.md | Orthogonal to leaf-index implementation; no leaf is removed or accepted. |

No new runtime enum/constant exists in the reviewed design, so there is no implemented constant for the closed-set mirror rule to test yet. The independent proposal checks mirror the exact declared arrays/order and counts. The later source review must compare actual source constants against this exact finite proposal rather than assuming a generic open-ended roster.

No primary source, index, Git, runtime state, reference media, guard, TEST/P/CONTROL/Original/Mac action or qualification clock was changed. This is not an overall WP108 verdict.
