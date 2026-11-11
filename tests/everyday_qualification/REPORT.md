# Everyday editing qualification

## Candidate

The Linux preview candidate was built from the approved integrated runtime at `d7343044f626721782e771c10dfa0754c988685c`. The production source tree has no diff against reviewed WP89 `20eb59a537da1fbd4e5833b22a64aa335fa0e320`. Approved WP85 `d60550ebe69c92606fc656b42162493888c49822`, the Search caret correction `a06b75841940843897221b7f912dba7fd8395dfa`, and proofreading interruption `18d2dcbf08323bb48881eecf3eb3a3b6f7a725a1` are actual ancestors. The production subtree identities and SHA-256 of all 72 local compiled inputs, including the bundled lexical resource, are recorded in [candidate.json](candidate.json).

- Binary SHA-256 `630913ee8dc45433db68db635eafd55c7fba4d3990f4d59106c28b859c69e6ed`.
- Candidate executable `/tmp/wordling-WP86-candidate.xSfy5m/build/wordling`. The deliverable uses these exact bytes following independent review.
- Normal Linux entry point `wordling -root /absolute/path/to/your/documents -profile local-flat`.
- Original US WordPerfect 5.1 DOS release 03/09/92. Physical layout uses the measured Standard Printer profile. Original re-edit and resave use Fast Save No.
- Linux PTYs deliver actual terminal key bytes and mouse sequences. Logical VGA roles and cells are compared with the original where the capture binds them. Host raster, fonts and physical terminal hardware are outside those comparisons.

`build_candidate.py` invokes `go build -trimpath -buildvcs=false` through the regular CLI package. A first build from the nested lane stamped the primary checkout commit in its Go VCS field. The final build omits that field and records the verified actual checkout, tracked production trees and compiled-input hashes externally. Every product case checks the same candidate binary hash before and after use. No preview executable or private DOS image is committed.

## Evidence by acceptance journey

| Acceptance | Executed evidence and outcome |
| --- | --- |
| EE-A01 | `menus` verifies editable startup with Yes, persisted No and restored Yes in separate normal processes. Physical Alt+= and SGR File selection preserve ordinary typing and native publication. |
| EE-A02 | `menus` compares original top bar, File, Edit and nested Justify grids. Physical F1, active-menu F6 and F7 exercise original routing. `help-focus` checks that Esc and Space remove the selected child role while the drawing persists, then Up activates Endnote. |
| EE-A03 | `menus` checks both complete original Help template grids and physical F3 and 1 switches. `help-focus` enters all six Help topics and checks editing return. `files-reveal` and `corrections` exercise physical F11 and F12. |
| EE-A04 | `flow` types three pages in New, including explicit returns, blanks, Tab, a long word and ordinary wrapping. It saves twice, reopens in Doc 2 and continues editing. `continuous` adds attributed wrapping and an exact preserved no-edit copy. |
| EE-A05 | `navigation-search` verifies the desired column across long and short lines in both views. `files-reveal` verifies Page Up/Down, End and Home Home Left. The other edit cases use Home Home Up and preserve native positions on resize. |
| EE-A06 | `corrections` checks loaded Backspace and hard-return join/restore, three exact highlighted Undelete groups, backward selection with default No then Yes, forward Alt+F4 with F1 cancel, typeover and exact output. |
| EE-A07 | `attributes` creates overlapping F6/F8 native pairs, reloads, deletes the Bold pair in Reveal and preserves the exact Underline owners and source bytes. `continuous` authors attributes on an original-produced document. |
| EE-A08 | `files-reveal` compares original text, formatting roles, physical status, lower code pane and ruler, including page navigation and 12/11/25-row modal behavior. `attributes` verifies a native mutation through the visible pane. |
| EE-A09 | `navigation-search` checks direct forward/repeat/backward positions, the same positions via Search Next/Previous and partial cancellation. `wrapped-search` checks the original caret after a match across a soft return and after the native UnderlineOn code. Both save exact unchanged source copies. `files-reveal` checks the transient failure notice. |
| EE-A10 | `files` checks F5 from Retrieve, list paging, child/parent traversal, default No and confirmed occupied retrieval. `files-reveal` checks the directory requests for Short/Long, Name Search, Look Next/Prev and selected acquisition. |
| EE-A11 | `save-policy` checks first save, repeated replacement, refusal and cancel, both backup settings and exact Save As. `flow` and `continuous` re-edit and reopen saved files. Independent original runs retrieved, edited and resaved every distinct native save-policy snapshot. The disabled replacement and its Save As have identical bytes. |
| EE-A12 | `save-policy` checks Doc 2 Save Yes through real publication, distinct close, and restored Doc 1. `continuous` opens and closes a retrieved Doc 2. `corrections` writes in a fresh Doc 2 after a prior close. |
| EE-A13 | `preservation-corpus` verifies same-name and Save As byte identity for admitted plain and paired originals, and an exact adjacent edit preserving the whole pair and unrelated bytes. `refusal` verifies blank 564 retrieval refusal, stale target refusal, unchanged destination and prior backup, and subsequent successful save. `storage-faults` executes the owned injected write/replacement and rollback tests with prior backup checks at the storage boundary. The remaining corpus limits are listed below. |
| EE-A14 | `continuous` runs one ordinary editable session through browse, Look, retrieve, exact copy, wrap, attributes, Reveal, Search, contextual proofreading, repeated saves, reopen, Doc 2 and exit. `original` and `reopen` complete the stopped original-app round trip with exact native body checks. |
| EE-A15 | `proofreading` drives real Check, Not Found, paged suggestions, Skip Once/pass, Edit and F7, interruption, Add, native SUP persistence, restart and alternate menu entry. `proof-pages` loads the original formatted document, checks each Page scope and returns to Check after both interrupted and completed Page. It compares the complete Page correction output with the original, with only the admitted format-on-edit flag set. `continuous` selects the actual displayed suggestion in Word scope and returns directly to Check. |

Original sources are indexed in `docs/research/everyday-contract-2026-11-05/journey-contract.json`. The per-case originals and raw-reference mapping are in [coverage.md](coverage.md). Probe outcomes and paths are in [results.json](results.json).

## Native interoperability and boundaries

The continuous run saves an untouched original file byte for byte, then continues editing and saves again. The pinned DOS reference guest retrieves the exact final candidate file, inserts `Original ` after its leading native BoldOn, and saves a second file. Wordling retrieves that stopped guest output and inserts `Continued ` at the same native location. Both comparisons check the whole native body against the single expected insertion. The original save is observed to settle before the disk is read.

| Exact output | Bytes | SHA-256 |
| --- | ---: | --- |
| Wordling WPLIVE.WP | 907 | `2cd0c63a77d9de7aaea6d8f91b758be24c5da374f7f864e158b762846c074b81` |
| Original WordPerfect ROUND.WP | 916 | `883d3c8303e5edd1cf0395829d49ec54a2307e5c235f39abd55a904cd5bc72f0` |
| Wordling BACK.WP | 926 | `ef9079297c975605fb3ed2b0686360e868fbe88010ff0d1ef0a02380fcd20a8e` |

All three files have body offset 324. Separate original-app probes re-edited the first save, backup-enabled replacement and backup-disabled replacement from the same tested binary, checking every unrelated body byte. The raw evidence root is recorded in results.json.

- Standalone normal editor Retrieve refuses the witnessed 564-byte Fast Save prefix. The witnessed FLOW document can supply its admitted body for a confirmed occupied-document insertion without rewriting the source. The standalone input and the broader Fast Save family remain outside this preview's editable set.
- The WP01 merge primary and secondary documents retain their original bytes and explicitly refuse standalone editor acquisition at their unsupported native owners. Macros use a separate native resource path. These results establish safe refusal, while full open-and-save of the broad WP01 corpus remains open. EE-A13's admitted-document preservation and fault checks have separate evidence.
- The original DOS hard-hyphen owner `0xA9` is outside native mutation admission. Ordinary ASCII hyphen constituent checking is verified. The original's terminal deleted-soft-return regeneration on save remains a separate parity edge.
- The licensed `en_US-2026.02.25` ESDB bundle uses the reviewed lexical adaptation. Its suggestion inventory and ordering can differ from the original proprietary dictionary. Native supplementary persistence supports the witnessed uncompressed SUP family. Compressed dictionaries and the original proprietary lexicon are outside this preview.
- The menu preference uses the reviewed Linux application config outside the document workspace. Native documents, native backups and supplementary dictionary outputs retain their own authorities.

## Reproduce

From the approved candidate checkout, choose fresh absolute output directories. The original runner requires the pinned private reference master and QEMU tools in the separate reference checkout. It copies that guest before use.

```sh
python3 tests/everyday_qualification/build_candidate.py "$PWD" /tmp/wordling-candidate
python3 tests/everyday_qualification/run_suite.py "$PWD" /tmp/wordling-candidate/wordling /tmp/wordling-qualification \
  --candidate-record /tmp/wordling-candidate/candidate.json
```

The runner records exact child commands, terminal frames, captured cursor and roles, injected keys, raw wire hashes, native hashes and original release/Setup/output. Keep raw original disk images private. The full raw qualification directory is retained for independent review. Earlier failed harness runs remain in the temporary evidence. One used an outdated Page-interrupt return expectation and was corrected to the independently witnessed Check return before the final rerun.

Go verification used isolated user configuration and passed fresh `go build ./...`, `go test -count=1 ./...`, `go vet ./...` and race tests for document, editor, storage, TUI, proofreading and baseline adoption. The Python runners passed syntax checks. The qualification does not accept all of Mission 1.
