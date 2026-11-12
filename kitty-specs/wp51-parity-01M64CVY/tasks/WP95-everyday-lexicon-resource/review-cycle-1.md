---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-11-11T18:57:45Z'
reviewer_agent: user
wp_id: WP95
---

# WP95 independent review, cycle 1

**Request changes** for frozen `6a25f650abf2405089a4f8b0405ea1fc21490414`.
The actual provider, original SUP witness and prepared resource publication
passed independent checks. A public lifetime issue blocks T312's immutable
resource contract.

## R95-001 — LoadLexicon exposes the globally cached wrapper

`internal/proofreading/lexicon.go` caches `*Lexicon` with
`sync.OnceValues` and returns that same pointer from every public
`LoadLexicon` call. Although its maps and slices are private, the exported
`Lexicon` wrapper is assignable. In a fresh process, obtain
`alias, _ := proofreading.LoadLexicon()` and assign
`*alias = proofreading.Lexicon{}`. A later `LoadLexicon` reports success
but now has Count 0 and Accepts reports “proofreading lexicon is unavailable.”
The first wrapper, another consumer's wrapper, and future loads all refer to
the same now-empty object. This is externally reproducible through public
operations. It does not require mutating an internal map, changing an embedded
resource, or racing the caller.

Return a fresh wrapper value or a fresh shallow pointer wrapper around the
private immutable cached backing. Keep the cached object itself private,
preserve errors, and prove that reassigning one returned wrapper cannot change
an existing independent load or a later load. No need to clone the vocabulary
or reload the word list.

## Checks and evidence

Verified ten owned paths, issued parent `9837a349`, and actual approved
WP98 source `fb92b0fc` as an ancestor. Compared exact checked-in resources
against all three original archive members, including CRLF and both notices.
All match the reviewed release. The independent public probe at
`/tmp/wordling-WP95-independent/main.go` verified unrelated actual dictionary
entries, independent typo suggestions and bounded wildcard matching, then
produced the exact SUP accepted in the original, preserved same-stem opaque
backup bytes, and reopened through a fresh workspace. `result.txt` records
that success followed by the mutable-wrapper failure.

Independently compared the original pinned guest's before/after 81-byte
SUP (SHA-256 `0918d9d72da85a4ae3d7b8d0d304d73f2b1f211d44fffac7a3695a002ceb9884`).
The files are identical. Reading actual row 0–10 VRAM attributes yields
exactly `xxqzzqq` under attribute 0x47, with question VRAM SHA-256
`743845dd0681c8fd1dae979c7251fb6ab217d1b8c959b4cf8767a6e518f18e17`.

Build, test, vet, focused fresh provider/storage race, scoped gofmt and
diff checks passed. CRLF and whitespace of embedded upstream raw resources
were checked by exact byte comparison rather than text normalization.
WP96 and WP89 remain the actual live consumer gates.

| Check | Verdict |
| --- | --- |
| Dead code | N/A for approved next-package provider consumers; compatibility cohort remains only for existing WP88, to be removed by WP96. |
| Synthetic fixture | PASS. Actual embedded list, checked prepared storage and original-read native SUP. |
| Silent empty return | FAIL. Reassigned cached wrapper leaves later LoadLexicon returning an unusable resource with nil error. |
| FR coverage | FAIL for T312 immutable lifecycle only. Actual lexical and native persistence behavior passed. |
| Frozen surface | PASS. Only ten owned resource/provider paths changed. |
| Locked decision | PASS. Pinned adaptation, notices, no proprietary resources or backup side effects. |
| Shared ownership | PASS. WP87 successor provider scope and WP98 storage dependency are explicit. |
| Production fragility | PASS. Checked publication outcomes and resource errors are explicit, apart from R95-001. |
