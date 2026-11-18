# Mission 1 resource discovery — 2026-11-18

Researcher: resolver-loaded `researcher-robbie`; parent Op and `mission-governance.json` apply. This is resource discovery, not an acceptance verdict. Full M1 scope is retained.

## Result

Do not ask the owner to supply keyboard, US thesaurus/hyphenation/language, or generic printer/graphics media: those resources already exist in the declared private reference cache. The gap is decoding and qualifying their behavior. A genuine WP4.2-produced public document pair has also been located with first-person producer provenance; its usage terms and bytes still need qualification. An original 4.x macro remains unidentified in inspected inventories. A qualified graphics/proportional printer profile is missing from the selected environment, but existing, uninspected printer installer packs may already provide it.

## Existing local inputs

Canonical evidence is `docs/research/reference-environment/installed-files.json` (158 installed entries), `resource-profile.json`, `media-manifest.json`, `environment.json`, and `README.md`. Both extracted trees exist at `research/cache/reference/build/installed-files/WP51` and `research/cache/reference/build/rebuild-02-files/WP51`. Filename/stat inventory in both agrees on the following counts; recorded hashes come from manifests and were not freshly recomputed.

| Category | Present input | Qualification still needed |
| --- | --- | --- |
| Keyboard maps | Five WPK files: ENHANCED (3837 bytes), EQUATION (2974), FASTKEYS (2999), MACROS (18281), SHORTCUT (11963) | Actual WPK selection, decoding, assignments and round-trip behavior. Current environment selects no custom WPK. |
| US language | `WP{WP}US.THS` 358472 bytes; `.HYC` 9676; `.LCN` 16; `.LEX` 363165; `WP{WP}.SPW` also inventoried | Native resource decoding and original comparison. Other locales are not established by this inventory. |
| Conversion tools | CONVERT.EXE, MACROCNV.EXE, GRAPHCNV.EXE, PTR.EXE | Source fixtures, successful output and failure/unsupported cases, not merely menu entry. |
| Printer/graphics | Three PRS files (STANDARD, STANPRIN, LEARN/WORKBOOK), WP.DRS, WPSMALL.DRS, WPDM3.ALL, STANDARD.CRS/IRS, ten FRS files, 34 WPG samples | Select/fingerprint a graphics and proportional printer/font profile; test output against original. FRS filenames alone do not establish printer font metrics. Other graphics input formats were not identified by bounded filename search. |
| Original bundled macros | Ten 5.1 WPM files, including CALC, CODES, EDIT, ENDFOOT, FOOTEND, INLINE, LABELS, PLEADING, POSTNET, REPLACE | These are not documented 4.x input macros and cannot close the 4.x conversion requirement. |

`resource-profile.json:2-5` identifies selected **Standard Printer, 10 cpi text only, no graphics**, with July 17, 1992 printer media. It is not a graphics/font/pagination oracle. The WP executable is the selected March 9, 1992 release. `media-manifest.json:23-44` already registers printer1.img, printer2.img and ptrgraph.img, including compressed WPR1/PTR packs. Their private contents were not inspected. Therefore “not yet installed/qualified” must not become “media absent.”

The US thesaurus has an existing original lookup/cancel observation (`docs/research/reference-runs/mission1-thesaurus/README.md:3-11`), while the product resource decoder remains open. THS/HYC/LEX SHA-256 values are already pinned in `resource-profile.json:47-60`.

## Narrow unresolved inputs and public leads

### Genuine WP4.2 document: public primary producer evidence found

[Author's original report, October 6, 2020](https://github.com/digital-preservation/pronom-research-week/issues/10#issuecomment-704278134) explicitly describes installing **WordPerfect 4.2 for DOS**, saving a plain-text document, then saving another with an original font-change code. It supplies screenshots and an attachment containing both test files: [wp4-test.zip](https://github.com/digital-preservation/pronom-research-week/files/5333912/wp4-test.zip). This is a concrete original-producer path, stronger than a filename or inferred header.

No attachment was downloaded or opened in this task. The comment does not state an explicit fixture license. Before committing or redistributing it, establish the author's permitted use/fixture terms and record archive member inventory, checksums and provenance. If permitted, use it as an ignored private interoperability input first, then capture CONVERT option 8 and original retrieval results. It could remove the need for the owner to locate old document media. Do not fabricate an “authentic” file from the six-byte font-code description.

The issue's initial Tika fixture is **a separate sample exported by WP6.1 for Windows**; it does not meet the stricter original 4.x-producer requirement. The later comment above does. Pure ASCII is a valid original 4.2 save, so a magic prefix is not a universal authentication test.

`docs/research/reference-runs/mission1-convert-42/README.md:3-11` establishes the existing 5.1 CONVERT menu supports 4.2 input but no 4.2 output. It cannot manufacture the required original fixture from 5.1. After provenance qualification, actual conversion/retrieval observations remain required.

LibreOffice primary tree metadata was also checked: `writerperfect/qa/unit/data/writer/libwpd/pass/WP4.wp` exists (211 bytes; blob `6917b81e6619fed9892c3a13f8307c0bfb942ecc`), with [2014 organization history](https://github.com/LibreOffice/core/commit/b2719a71a268e824b8d1b9c1187a464c07018989). No original producer/version proof was found in that metadata. A secondary attribution's `wp42.wp` path was not present in the checked current primary subtree. Do not relabel WP4.wp as authenticated 4.2. LibreOffice's root MPL text alone does not prove the specific binary's original authorship or license. libwpd/LibreOffice may supply research fixtures; FC007 still excludes using them as runtime conversion intermediaries.

### Original4.x macro: not identified, not globally proven absent

`docs/research/reference-runs/mission1-macro-converter/README.md:3-10` establishes original MACROCNV 1.6 launch and source prompt only, without a 4.x source or converted WPM. No documented 4.x source macro was identified in the bounded local inventories below. Exact missing evidence is an authentic 4.x-produced macro, its producer/version/provenance, output from original MACROCNV, and unsupported-command behavior.

The declared [SDK source register](/home/lynn/projects/wordling/docs/research/sources.md) pins the SDK51 **PDF**, not an SDK binary/sample archive. No SDK ZIP/ISO was found in the inspected local reference cache. The declared [WPDOS utilities index](https://mendelson.org/wpdos/wpcsoftware.html) points to `https://mendelson.org/wpdos/wp51sdk.zip` and the archived 1994 WordPerfect SDK/PerfectFit collection. This hosting index is a discovery aid, not primary proof that an original 4.x macro sample or redistribution permission is included. No archive was acquired, installed or executed. A focused archive manifest/README and publisher license review is the next research path; do not promise it contains 4.x macros. If no permitted sample emerges, obtain a minimal original 4.x macro plus recording/version evidence from its owner or an original 4.x installation lawfully held by the owner.

### Additional locales/printer profile

Only US language resources are established. If M1 calls for another named locale, identify that locale and its precise input resources before acquisition. For graphics/proportional printing, first examine the already-declared printer packs and qualify a selected profile under the existing reference-environment procedure. Request additional owner media only after that focused inventory demonstrates the required files are actually absent. Public archive availability alone is not a proprietary redistribution grant.

## Scope and limits

Read only repository metadata/manifests/READMEs/source records; filename/stat inventories of the two extracted cache trees and bounded relevant names under the reference cache, tests, internal, canonical reference-runs, ~/Downloads and ~/Documents. No secrets scan, private disk-image content reads, fresh binary hashes, original-media modification, VM launch, source/git/runtime/tracker mutation, or binary acquisition occurred. Unnamed original documents can have arbitrary extensions; filename search cannot prove global absence. The `wp42-*` cache names found locally refer to **WP42 work-package probes**, not authenticated WordPerfect 4.2 producer fixtures.

The public issue/comment, LibreOffice tree/history metadata, and declared toolkit index were checked on 2026-11-18. Primary producer evidence and lawful usage terms must remain separate. The parent should continue qualified implementation/testing using present resources, pursue the genuine 4.2 attachment's permission/provenance path, and avoid treating this resource inventory as completed M1 acceptance.
