# Wordling proofreading resources

Wordling admits the `linux-esdb-en-us-2026.02.25-plain-v1` profile. The
English Speller Database US English size-60 plain wordlist was produced with
`--accents=strip`. The original archive and all three embedded members have
these SHA-256 digests:

| File | SHA-256 |
| --- | --- |
| wordlist-en_US-2026.02.25.zip | `caeb6ee8a38e98ccbd6e5c717889a1bab68073dcba8a9c0ca6570641926913e9` |
| en_US.txt | `fe44d9ed8804beb4dfb78c10e1625e9a1f670f0b3074094c92e70bde6e6b0ac9` |
| README.txt | `12830141b6e317ce68c4d6cbc9495b6b8a3f31b98e761be3c05206e02ca3c40d` |
| README_en_US.txt | `d63c711523fc9504fb71e1278489c6d7bb8cafcba75158c107cd17844955470f` |

The original notices are kept under [resources](resources) and in the embedded
resource. The wordlist is distributed under the terms in its accompanying
notice. Wordling's source code is Apache-2.0. Keep the original notices with any
redistribution of the list. [ESDB release downloads](https://wordlist.aspell.net/dicts/).

`LoadLexicon` checks the complete embedded bytes before admission. The list
contains 109,902 unique exact spellings, at most 23 bytes per entry, using
CRLF terminators. Admission preserves exact spelling and removes only the
declared line terminator. A missing, changed or invalid resource is an error.

Membership accepts exact spelling as well as title case and all uppercase
variants of admitted lowercase words. Query words may use up to 64 ASCII letters
and internal apostrophes. Other inputs are explicitly unsupported. The application
does not transliterate native characters. Suggest ranks spelling variants at
optimal string alignment distance at most two, with deterministic case and
lexical tie-breaking. Suggestions are bounded to 72 distinct spellings so the
editor can paginate 24 at a time. Lookup matches ASCII `?` and `*` patterns
case-insensitively. A literal lookup includes an exact spelling and nearby
spellings. The wordlist and ranking are a declared adaptation
(`original_lexical_equivalence=false`). Original WP 5.1 LEX and SPW resources,
affix rules and phonetic ranking are outside this profile.

`OpenSupplementary` selects a pinned, bounded native uncompressed dictionary.
It defaults to `WP{WP}US.SUP` and accepts a custom DOS filename verbatim apart
from the workspace's normal case resolution. The admitted prefix is the
66-byte uncompressed family witnessed in the WP78 default and custom files.
A body contains at most 8,192 qualified words terminated by native HRt, with
preserved case and order. Supplementary membership and duplicate detection are
ASCII case-insensitive. Other prefix families, compressed or mixed dictionaries,
encrypted inputs and malformed bodies are refused. A missing file can be
created empty or when a word is added. Existing bytes survive a duplicate Add.

`Add` and `Create` use the immutable observed source and destination and the
prepared storage transaction. Existing same-stem document backups are preserved.
Cancellation before publication leaves the file unchanged. A conflicting
observation or an uncertain committed result returns an error without adopting
new vocabulary. Reopening uses the file on disk. Supplementary state is distinct
from the editor's per-pass skips and remembered corrections.

WP96 connects the editor session to these APIs and removes the legacy cohort
call site. WP89 loads the resources in normal application startup and connects
the contextual controls. This package contains the resource and native I/O
implementation.

## Original application check

A native default dictionary produced by two checked Add operations for
`zorbly` and `vimward` was copied into a private, offline copy of the pinned
March 9, 1992 WP 5.1 DOS reference. Ctrl+F2 Document on
`zorbly vimward xxqzzqq` highlighted only `xxqzzqq`, with attribute 0x47
on all seven letters. Skip Once then reported three words checked. The
81-byte SUP extracted after guest shutdown matched the input exactly.

- SUP SHA-256: `0918d9d72da85a4ae3d7b8d0d304d73f2b1f211d44fffac7a3695a002ceb9884`
- 4,000-byte question screen SHA-256: `743845dd0681c8fd1dae979c7251fb6ab217d1b8c959b4cf8767a6e518f18e17`

Tests cover ordinary dictionary words, typo suggestions, lookup limits and case
policy, exact native framing, persistence across workspace reopening,
unsupported bodies, cancellation, permissions, ambiguous names, stale targets
and concurrent Add. The embedded notices preserve the upstream physical bytes,
including their original line endings and whitespace.
