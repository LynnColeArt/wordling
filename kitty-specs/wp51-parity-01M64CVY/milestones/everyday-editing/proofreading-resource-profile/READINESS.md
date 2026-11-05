# WP87 read-only readiness findings — 2026-11-05

No WP claim, repository edits, lifecycle changes or parity assertion. These are
proposed implementation/adaptation findings for review. Local code/research root:
`/home/lynn/projects/wordling`.

## Decision recommendation

Use an explicitly named, pinned **ESDB US 2026.02.25 plain-list provider implemented
in Go** for the admitted Linux lexical profile. Preserve the original contextual
proofreading state machine and native supplementary format independently. Keep
original LEX/SPW lexical equivalence open; do not claim that resource is decoded
or that modern ranking matches the original. Do not use a small sample table.

The original code/data decoder remains a real future compatibility task, not a
format extension that the existing document reader already supports. The current
approved WP87 contract allows qualified host lexical-resource differences; the
orchestrator/reviewer should record this exact adaptation before implementation.

## Original resources and existing evidence

- Main original: `research/cache/reference/everyday-spelling-proof/resource-hashes/WP{WP}US.LEX`,
  363165 bytes, SHA256 `58fdb7ffb840a3ef64467b693668a535d2d08672bf042392bcdf815d259c68a5`.
  Header FF575043, payload offset16, product1, type0x0B, version1/0.
- Original speller module: same directory `WP{WP}.SPW`, 13126 bytes,
  SHA256 `5ddcd58e53101f344f3b172cf86b7690bb57e6c7a2b395d46a6cde3bd9fc04bd`.
  Header type0x1D, offset16; this is code, not a plain word list.
- Pin/rights and actual original workflow:
  `docs/research/everyday-contract-2026-11-05/proofreading-contract.md`;
  `spelling/proof/dictionary-provenance.json`; `spelling/REPORT.md`.
  The vendor dictionary/module remain private proprietary references. No
  redistribution permission was established. Do not put their bytes in assets.
- `internal/wp51/native.go:108` Parse accepts only document type0x0A and stored
  version0/1. It explicitly rejects the original LEX/SPW headers. No existing
  internal/proofreading package or production spelling engine was found;
  `internal/tui/historic.go:56` still has the Spell menu entry with an empty key.
- `research/cache/toolkit.txt` lines414–418 lists TKSPELL.EXE containing SPELL.DOC,
  SPXMOD.ASM/BIN, WPCALLS.INC and a generic header-only WP{WP}TS.LEX. Lines646/661
  identify dictionary type0x0B and code0x1D; lines688–692 distinguish external
  speller types0x2E/0x2F. Line1050 names compressed supplementary prefix packet0x0E
  without its compression grammar. These are format identifiers, not a main LEX
  decoder. The local cache lacks those speller source files. Bounded public exact
  filename searches found no usable primary original module source; this was not
  an exhaustive archival hunt. Do not infer the vendor decoder from the existence
  of an external module interface.

## Concrete licensed resource, actually fetched and inspected

Primary maintainer release page: https://wordlist.aspell.net/dicts/
Primary release listing: https://sourceforge.net/projects/wordlist/files/speller/2026.02.25/
Downloaded from the maintainer's SourceForge project:
https://downloads.sourceforge.net/project/wordlist/speller/2026.02.25/wordlist-en_US-2026.02.25.zip

Temporary archive: `/tmp/wp87-readiness/wordlist-en_US-2026.02.25.zip`.
It is 296952 bytes, SHA256
`caeb6ee8a38e98ccbd6e5c717889a1bab68073dcba8a9c0ca6570641926913e9`.
Contents extracted only to `/tmp/wp87-readiness/`:

| Entry | Bytes | SHA256 |
|---|---:|---|
| en_US.txt | 1143387 | fe44d9ed8804beb4dfb78c10e1625e9a1f670f0b3074094c92e70bde6e6b0ac9 |
| README_en_US.txt | 6976 | d63c711523fc9504fb71e1278489c6d7bb8cafcba75158c107cd17844955470f |
| README.txt | 113 | 12830141b6e317ce68c4d6cbc9495b6b8a3f31b98e761be3c05206e02ca3c40d |

Release version2026.02.25, upstream revision7e99eda. en_US default size60, not
large70. List contains109902 unique LF-separated entries, all ASCII, longest23
characters; no spaces/slash flags. Upstream build command is
`mk-list --accents=strip en_US 60`. Thus accent stripping is already a property of
this particular dataset; it must NOT authorize silently transliterating native
characters. Raw words retain case/apostrophes. The plain list also does not carry
Hunspell affix/NOSUGGEST flags or an original frequency/ranking oracle.

The included README grants use/copy/modification/distribution/sale of SCOWLv2
word lists subject to keeping copyright and permission notices. Preserve the
entire included README with a bundled resource; do not relabel the word list as
Apache-2.0 or strip its notices. Current primary notice:
https://raw.githubusercontent.com/en-wl/wordlist/v2/Copyright
The release readme is authoritative for these exact bytes, not a generic license
assumption. Source release/readme identify modern vocabulary; no WP equivalence.

Available local fallback resources are older and DIFFERENT: Debian/Ubuntu
wamerican2020.12.07-2 `/usr/share/dict/american-english` has104334 lines,
985084 bytes, SHA2569f513f1ceadb6a01c5485b7dbdfd5118dc66cd70b59cae2851292112d4066a32;
its exact list composition/license are in `/usr/share/doc/wamerican/`.
Hunspell-en-us1:2020.12.07-2 supplies `/usr/share/hunspell/en_US.dic` and `.aff`.
They are not interchangeable with the proposed pinned release or a plain list.
Do not discover `/usr/share/dict/words` silently and let distro/locale decide.

Hunspell is an alternative mature engine, but its affix+dictionary parser and
C/C++ or external-process deployment are a different integration choice. Official
format: https://github.com/hunspell/hunspell/blob/master/man/hunspell.5
Official engine README describes LGPL/GPL/MPL tri-license and interfaces:
https://github.com/hunspell/hunspell/blob/master/README.md
A .dic-only loader would incorrectly omit affix semantics. The pure-Go plain-list
proposal avoids that mistake and an implicit native runtime dependency, at the
cost of explicitly different lexical/ranking behavior.

## Proposed resource profile and service boundaries

Profile ID proposal: `linux-esdb-en-us-2026.02.25-plain-v1`.
Record upstream URL/version, archive/list/license hashes, US locale, ASCII entry
encoding, size60/build options, provider algorithm version, resource limits and
`original_lexical_equivalence=false`. Supply bundled licensed bytes only with
notices, or load an explicitly selected matching external resource; absence,
malformed bytes, wrong encoding/format and changed identity are typed failures.
Never return a successful no-issues result because resource loading failed.

WP87 API should be an immutable admitted provider plus a separately captured
supplementary vocabulary. Suggested conceptual operations (names not API edits):

- Admit(ResourceBytes, Provenance) -> immutable Provider or typed ResourceError.
  Parse a declared format with bounds; reject binary LEX/SPW in the plain-list
  route. No shell commands or network during proofing. Hash the entire admitted
  resource; don't admit only a fixture-name/hash whitelist.
- Check(WordIdentity, VocabularyView) -> accepted/suspect/unsupported/error;
  Suggestions(word, query-budget) -> deterministic ordered candidates+continuation;
  Lookup(pattern, query-budget) -> candidates. Same input/profile gives same order.
  Candidate generation must search the actual full dataset (e.g. bounded
  Damerau-distance index with explicit case/lexical tie break), not sample-word
  tables. Any phonetic/lookup strategy is explicitly versioned and tested; do not
  claim original phonetic ranking. Paginate real results for the original A–X
  presentation without changing their order between pages.
- Scan uses WP80's admitted native-character/text identities and structural
  boundaries; it must never tokenize rendered Reveal labels, ANSI output or lossy
  flattened text. SRt separates words; DSRt and supported attribute boundaries
  need the exact WP78 continuation cases. Unsupported native identities yield an
  explicit result rather than replacement characters or silent normalization.
- Supplement read/add outputs original-compatible bytes plus expected-source
  identity for checked publication. Storage integration uses an admitted confined
  resource I/O seam and compare-before-publication guarantees. Any necessary
  shared API belongs to its owning WP; do not reach into private storage fields.
  Resource failure/cancellation leaves both document and dictionary untouched.
- WP88 owns scope/cursor/revision, skip-once/pass, replacement memory, Edit/F7
  resume, history and actual native replacements. WP87 can provide vocabulary
  values; WP88 controls their lifetime/reset. WP89 owns context panes/keys/prompts.
  Provider operations do not move caret, edit content or fabricate UI completion.

Concrete first implementation: strict list admission, real membership, bounded
indexed suggestions/lookup, explicit identity/case rules, separate supplementary
reader/writer, provenance diagnostics, then broad corpus and cancellation/resource
failure tests. Keep exact original suggestion fixtures separate from declared
adaptation comparisons: original quick may occupy C while modern engine chooses
another rank. UI tests select the actual candidate's letter; never special-case C.

## Native supplementary dictionary contract and caution

Actual observed Add output is native document type0x0A, stored version0/1,
73 bytes, body offset66, body `zorbly` followed by HRt0A. SHA256
c82c4ec8e16ff67d5295b1afe6944c2f6d07621dfe369d9597b7031234f337ea.
Exact complete bytes: approved `spelling/proof/supplementary.json` and its authored
SUP fixtures. Default filename is WP{WP}US.SUP. Custom SPELLADD gets no appended
extension. Add persists; per-pass Skip does not. Preserve unrelated native bytes.
Use the existing lossless native framing API where its preconditions apply;
SUP vocabulary semantics still require a separate validated reader, and document
mutation admission must not be weakened to accept arbitrary resource formats.

Reference manual `research/cache/reference.txt` lines46726–46750 (printed p595)
explains uncompressed words are one per HRt and editable in WP; optimization
moves words into the prefix, while later added words remain in the body.
Toolkit packet0x0E identifies that compressed data but does not supply its
algorithm. Initially admit the observed uncompressed native SUP family, preserve
unrelated bytes, and explicitly refuse unsupported compressed/encrypted/malformed
resources. Do not silently ignore compressed words or rewrite them as plaintext.
Broader compression needs a qualified decoder, not a fake empty vocabulary.

The same manual lines46921–46935 says selected custom dictionary lasts until
exiting WP or choosing another. This is documentary support, distinguished from
WP78's live default-dictionary restart witness. Add at least multiword/case/
repeated-add/native-reopen and original interoperability tests during WP87; the
one-word fixture is not a universal format whitelist.

## Proposed adaptation text for review (not an applied plan change)

“Everyday proofreading preserves the reviewed US WP5.1 DOS 03/09/92 contextual
workflow, scope/focus, correction and native supplementary-dictionary semantics.
The Linux lexical profile linux-esdb-en-us-2026.02.25-plain-v1 uses the pinned,
licensed US English ESDB plain word list and a documented deterministic Go
suggestion/lookup algorithm. Main-dictionary vocabulary, accent policy, case
acceptance and suggestion/phonetic ordering are qualified platform differences,
not claims of original LEX/SPW equivalence. The selected profile and resource
identity are explicit; a missing or unsupported resource cannot silently select
a replacement or report success. No proprietary dictionary is distributed, no
native document format is changed, and full M1 original lexicon/ranking parity
remains open. Original exact-list fixtures remain independent comparison evidence;
implementation must not hardcode their words, letters or output transcript.”

Risks needing review: the proposed lexical deviation is material despite preserved
workflow; plain-list suggestions need useful deterministic quality/boundedness;
original case/word-boundary behavior must not be replaced by generic Unicode
segmentation; compressed SUP is not decoded; resource publication must inherit
real safety guarantees; final executable must ship/find the declared resources
and run the continuous original-style journey. WP87 approval alone is not that
product integration verdict.
