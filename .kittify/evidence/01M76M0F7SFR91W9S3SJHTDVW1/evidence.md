# Fast Save and merge document intake

The reference is US WordPerfect 5.1 for DOS dated 03/09/92, run in private copies
of the existing pinned QEMU reference. The everyday preview's broad corpus
refusals were caused by requiring mutable document history during retrieval.
Parsed documents with unsupported mutation shapes can now be inspected and
saved unchanged. Malformed native input still fails parsing. A no-edit save or
Save As preserves all bytes, including a Fast Save prefix and merge owners.

## Fast Save

Fresh original runs retrieved the 1,013-byte FLOW.WP with its 564-byte prefix.
With Fast Save Yes, appending ` ONEDIT` retained offset 564. Setting Setup →
Environment → 5 to No and appending ` OFFEDIT` saved with body offset 324. A
subsequent ` AGAIN` edit retained offset 324. Two private runs produced
byte-identical outputs. Original No also compacted a no-edit Save As into the
same 773-byte image already in `internal/tui/evidence/everyday/FLOW.WP`.

The measured compact layout packs live packets 6, 7, 15, 12 and 8 at 66, 82, 96,
182 and 322, respectively, with index blocks at 16 and 272. The original
cleared bit 3 of the document flags. The checked implementation admits only
the two observed index graphs with matching retired packet contents and
validates the compact result using the ordinary mutation rules. It keeps the
acquired original unchanged until a supported edit succeeds. Selecting No is
a session setting. Fast Save Yes incremental writes remain open.

A terminal run selected No, copied the 564-byte source exactly, edited it,
and saved a 324-offset document. Original WordPerfect retrieved that exact
Wordling output and resaved it with the same body, then performed two more
edits and saves with only the intended body appends.

## Merge documents

The pinned primary and secondary fixtures in the native corpus are native
documents. The original displays FIELD, END FIELD and END RECORD in normal
editing and shows the corresponding merge codes in Reveal. Original Save As
preserved the whole body for each fixture. Adding X before the primary text
and Z before the first secondary record preserved all existing owner bytes.
Original Ctrl+F9 merged those edited files into `XHello ZAlice` and
`XHello Bob`. The stopped result has SHA-256
`2cc117211ed1439481b86001290c817bc5335562ea7e2cc9de45e1434481c532`.

Wordling's increment covers read-only inspection and exact no-edit copies.
Merge text/owner editing, record status and Ctrl+F9 execution remain open.
Historical reader/compiler sources in lanes v, x and y are not part of the
live executable. The historical body compiler explicitly excludes
page-bearing primaries such as this fixture.

## Reproduce the product checks

Build the normal `./cmd/wordling` executable. Run
`tests/everyday_qualification/preservation_corpus.py` and
`tests/everyday_qualification/physical_cases.py` against it, passing the
repository, binary and a fresh output directory. Use the `refusal` case of
the latter for Fast Save and stale replacement. The focused public editor
tests also cover read-only copy and keeping the Fast Save choice when Doc 2
closes. This is an increment within 5.1 parity.
