# WP22 selected native character evidence

Two independently fresh pinned master copies completed CHR1 in `runs/chr1-r1`
and `runs/chr1-r2`. These are original-only local subcases of CMD51-138,
feature WP51-066; the canonical case remains unchanged and Wordling is untested.
Both runs started at an empty ordinary document, typed ASCII A, saved BEFORE,
pressed Ctrl+V, typed `1,36`, pressed Enter, typed B and saved ORIGIN. Actual
screen prompts were `Key =` and `Key = 1,36`; Enter removed that prompt.
Captured CP437 screen text is a display witness only, not a Unicode mapping.

The runner froze ORIGIN with guest DOS COPY as SOURCE0, cleared the document,
retrieved ORIGIN and saved RETRIEV without edits under a new name. It cleared
again, retrieved ORIGIN again, moved to the beginning, inserted ASCII X and saved
EDIT under another new name. The final F7/No/Yes branch reached `C:\WP51>`.
The guest was stopped before native exports and resource reads. No failed
calibration occurred; both named attempts passed. The VM and shared lock were
released after the second extraction; no further VM work is queued.

| Own fixture | Bytes | Body offset | Exact body | C0 span (zero-based, half-open) |
| --- | ---: | ---: | --- | --- |
| BEFORE |325|324|41| absent |
| ORIGIN / SOURCE0 |330|324|41 C0 24 01 C0 42|[325,329) |
| RETRIEV |570|564|41 C0 24 01 C0 42|[565,569) |
| EDIT |571|564|58 41 C0 24 01 C0 42|[566,570) |

The native pair is character number36/set1. Its Unicode/glyph identity remains
unqualified. Full raw fixture size/SHA-256, byte offsets and token annotations
are recorded per run and in `native-comparison.json`. Both runs agree on every
listed body. ORIGIN remains whole-byte identical to frozen SOURCE0 after both
retrieval branches. Original no-edit/new-name RETRIEV differs from ORIGIN:
its prefix expands from324 to564 bytes, and its whole size from330 to570.
This is an observed original-app transformation, not byte-identical saving or
normalization by this harness. Raw comparison preserves differing spans; no
prefix packet meaning, fixed offset rule or writer/relocation contract is inferred.
RETRIEV→EDIT shares the first564 bytes and all six trailing body bytes; the
observed intervening insertion is58. A future writer contract must inspect real
prefix expansion/relationships rather than assume324 is fixed.

Every run archives the exact executed reference Python sources, selected case,
release baseline, emulator/environment and resource profile. `preflight.source_inputs`
pins baseline/case/contracts/go metadata. QEMU argv and stopped-copy resource
hashes retain installed settings differences (mutable SET flagged), while static
resources and master disk/boot remain unchanged. Only own scratch native files,
captures, project harness code and metadata are published; proprietary executables,
fonts, dictionaries, manuals and other resource bytes remain private. The selected
Help03/09/92 U.S. DOS executable under FreeDOS1.4 with July1992 Standard Printer
is a mixed-date text-only profile, not historical DOS or graphics qualification.
The source PDFs/locators and conflicting revision boundaries remain pinned by the
approved language-data/layout-resources contracts recorded in each preflight.

The executed runner archive predates the final offline verifier's extra prompt,
case/feature and mutation checks. The VM recipe did not change afterward. Archived
runner hashes are authoritative for execution; current source provides repeatable
verification. `negative-verification.json` records four rejected changes to temporary
evidence copies (wrong case, unaccepted status, false body annotation, raw native
byte tampering); originals revalidate afterward. `offline-tests.txt` records four
passing inspector tests including20,000 deterministic random bodies and measured
4096-token Python allocation. Unknown complete C0 FF FF C0 is synthetic and
preserved as an unqualified native identity; no original undefined-set test is claimed.

Reproduce offline checks from this lane:

```sh
python3 -m py_compile scripts/reference/character_identity.py
python3 scripts/reference/character_identity.py self-test
python3 scripts/reference/character_identity.py verify chr1-r
python3 scripts/reference/character_identity.py verify-negative chr1-r
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/review_checks.py --junitxml /tmp/wp22-validation.xml
```

Source/handwritten-document whitespace checks passed. The full raw-evidence
whitespace scan reports one trailing blank line in each `clean-dos-exit/screen.txt`
(two warnings); these are unchanged captured bytes and are deliberately retained.
Both catalogues passed (236 cases,91 groups). `validation.xml` reports four
passing checks and three honest Go skips because this lane contains no Go
packages; no production tokenization, writer, build or product performance is
claimed. `git-blob-proof.json` compares staged raw artifacts with their manifest
hashes/lengths under the subtree-local binary attributes. The proof is generated
before the implementation commit so its Git object IDs identify exact blobs.

The bounded handoff is in `tokenizer-handoff.md`. All other character sets/pairs,
foreign locales, Ctrl+2 contexts, macro/equation/search/filename composition,
unsupported original identities, missing-resource behavior, language tools and
original companion/resource formats remain open. Terminal Unicode/width, glyph,
font, print/preview metrics, semantic editing/writing and full differential
verification remain open. This package does not close FR-014, FC-006, NFR-004,
C-004/C-005 or full M1 parity. PDF remains optional M2.
