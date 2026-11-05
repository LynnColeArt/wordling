# WP78 contextual proofreading contract, version 1

Candidate for independent reference review, not a Wordling parity verdict. The
original US WordPerfect 5.1 DOS executable dated 03/09/92 is the oracle. The
complete initial continuous transcript is [spelling/REPORT.md](spelling/REPORT.md),
with exact inputs in its per-run trace.jsonl files. `journey-contract.json` selects
accepted screen/attribute evidence; `fixture-manifest.json` pins authored bytes.
No implementation may replace the real workflow with this fixed demonstration.

## Context and transitions

Ctrl+F2 in ordinary editing opens `Check: 1 Word; 2 Page; 3 Document; 4 New Sup.
Dictionary; 5 Look Up; 6 Count`. Block checking starts directly from an existing
Block selection. Word returns to this Check menu after correction. Page scope
stops at the physical-page boundary and returns to Check after word-count
acknowledgement. F7 then returns to editing. Document completion acknowledges
word count and returns directly to editing. Do not merge these continuations.

The questioning screen keeps context in rows 0–10, position status in row 11,
red ruler in row 12, A–X suggestions in three columns from row 14, more-words hint
at row 22, and action prompt at row 24. Coordinates are zero-based at 80×25.
The initial `quik` cells use 0x47, ordinary document 0x17, ruler 0x47 and emphasized
prompt/status portions 0x1f. Exact remaining cells are in VRAM fixtures. Keep the
questionable word in its sentence while advancing; this is not an isolated dialog.

For Not Found: 1 Skip Once, 2 Skip, 3 Add, 4 Edit, 5 Look Up, 6 Ignore Numbers.
Letter selection applies the shown suggestion and advances immediately. Enter
shows another suggestion page, retaining the context and using letters again.
The exact original resources give first-page C=quick and next-page P=quick for
this particular `quik`. These examples do not establish general ranking.

A corrected spelling is remembered and applied when encountered later in the same
invocation; it can survive returning to Check from Word. Skip applies to the rest
of that pass, including the observed initial-capital variant. Exiting and starting
another check resets these transient decisions. Add is different: it writes a
supplementary dictionary and survives application restart.

Edit restores full document view at the suspect, with the original Spell Edit
footer. Ordinary cursor movement and insertion work there. F7 resumes checking.
F7 alone on active Not Found does **not** exit. F1 interrupts checking, then a
partial word-count acknowledgement returns to editing at the interrupted word.
The initial Check menu itself accepts F1 cancellation. These states require
distinct continuations; an unconditional Escape/Exit handler is insufficient.

Look Up retains context/list, accepts an input pattern and presents Select Word;
it is not direct typed replacement. In the observed `quick` lookup A actually
selects displayed `cache`. Use Edit for the witnessed typed correction.
Double Word and Irregular Case have different prompts/actions, recorded in the
spelling report. Unknown-word block option differences and nested lookup cancel
are not qualified by these examples.

## Formatted and wrapped text

`qualification/proof-pages` starts with a wrapped first-page paragraph containing
whole-word Bold `quik` and Underline `mispelled`, a repeated `quik`, then a hard
page break and `zorbly quik` on page 2. Page check corrects first-page occurrences
and leaves the second page unchanged. New Document check Add accepts zorbly,
then flags page-2 quik again because the previous invocation ended. Correcting it
preserves the enclosing Bold/Underline wrappers in the native output. BEFORE,
PAGEONLY and PAGES files pin exact effects, including soft/hard page structure.

Interior attribute boundaries behave differently. Independent fresh runs
`qualification/proof-boundaries` and `proof-boundaries-repeat` produce identical
BOUNDARY.WP. Input `qu[BOLD]ik[bold]` becomes `quick[BOLD][bold]`; input
`mi[UND]spel[und]led` becomes `misspelled[UND][und]`. The codes survive as empty
pairs at the end of the replacement. Do not silently preserve their former
character offsets or expand them around the replacement. This is an original
behavior contract for these supported cases, not authorization to discard codes.

An unbroken 75-character word with DSRt after character 65 exposes a bounded
original behavior: the suspect/highlight covers the first 64 characters. Lookup
`qu?ck` lists A.quack B.quick; choosing B results in `qUICKXYYYYYYYYYY`, retaining
character 65 and the ten trailing Ys, removing the now-unneeded DSRt, and flagging
the residue. Both runs reproduce the same native result. This surprising case
must not be generalized into an inferred arbitrary-word algorithm. The long-word
screen also retains a prior list; qualification is limited to the recorded trace.

SRt is a word boundary, not a joiner: the separately saved `SRWORDS.WP` has 15
`the` words followed by `a qu[SRt]ik`; Count reports 18. This distinguishes an
ordinary soft return replacing a space from an unbroken-word DSRt.

## Correction and deletion history

`qualification/history-repeat` establishes an existing latest deleted group NE,
previews and cancels it, performs a real spelling correction quik→quick, then
previews F1 again. It still previews NE: `  ONENE` before and `  ONE quickNE`
after. The correction does not create a new latest Undelete entry in this case.
This does not prove all history depths or all correction types; it does prevent
inventing a new deletion-history group for every accepted suggestion.

## Dictionary contract and rights

The selected main/supplementary directories are C:\WP51. Main resource
WP{WP}US.LEX is 363165 bytes, SHA-256
58fdb7ffb840a3ef64467b693668a535d2d08672bf042392bcdf815d259c68a5;
WP{WP}.SPW is 13126 bytes, SHA-256
5ddcd58e53101f344f3b172cf86b7690bb57e6c7a2b395d46a6cde3bd9fc04bd.
These private proprietary reference resources are not licensed for redistribution
by this project. Do not ship their bytes or claim a modern dictionary equivalent.
A provider must disclose version, language, rights, accepted bytes and comparison
level before exact suggestion-order or lexicon acceptance claims.

Add creates WP{WP}US.SUP when absent. New Sup. Dictionary with SPELLADD creates
that exact filename, with no implicit .SUP suffix. The authored examples are
identical 73-byte native WP files, body offset 66 and body `zorbly` plus 0A.
Those user-authored fixture bytes are in the manifest; proprietary lexicon bytes
are not. Restart confirms added-word acceptance. Custom selected dictionary
persistence across restart is not independently established.

Missing/read-only/locked/full resource errors must be explicit product tests;
this reference did not inject them. Failure must preserve document and dictionary
bytes. WP87 owns resource/provider proof, WP88 owns document/correction state and
WP89 owns the contextual TUI; WP86 must repeat the uninterrupted real executable
journey with admitted resources. A passing component or this original-only study
does not complete EE-A15.
