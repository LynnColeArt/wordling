# Initial manual study — 2026-10-29

This is a first pass, not a completed study or a compatibility claim. Source IDs
and exact editions are recorded in sources.json. All behavior below is documentary;
no original executable has been run. Derived engineering implications are labeled.

## Editing behavior with architectural consequences

- **Typeover does not overwrite formatting codes.** Text replaces characters but
  is inserted before codes when it encounters them. REF51 p. 695, PDF 712.
  Derived implication: generic text-area overwrite behavior is insufficient.
- **Undelete is a specific three-deletion mechanism.** Restoration of paired
  attribute codes depends on the deletion command used. REF51 p. 697, PDF 714.
  Derived implication: original undelete belongs in M1; modern unlimited undo
  must not replace its semantics by default.
- **Reveal Codes shares the document cursor and permits code deletion.** The
  normal and code views must track the same editing effects. REF51 pp. 112-113
  and 560-562, PDF 129-130 and 577-579. Derived implication: both views need
  one authoritative document interpretation.
- **Initial formatting is saved with a document.** The manual distinguishes
  application initial settings and document-format initial codes. F10 save has
  explicit filename and overwrite interactions. REF51 pp. 292-294, 565-566,
  PDF 309-311, 582-583. These cannot be replaced by generic host save dialogs.
- **Hard and soft returns are distinct.** Reflow and line-spacing behavior need
  original boundary semantics. REF51 pp. 557-560, PDF 574-577.
- **Advance uses document geometry.** Relative/absolute moves, page limits and
  text-box origins differ; it is not cursor movement by terminal cells. REF51
  pp. 31-34, PDF 48-51.
- **Preview depends on selected printer resources.** REF51 p. 702, PDF 719.
  Derived implication: pagination and print fidelity need declared metrics and
  resources; matching terminal wrapping is not sufficient.

## Native file structure

SDK51 WP pp. 3-8 and 17-18 (PDF 16-21 and 30-31) establish:

- A 16-byte prefix identifies product/type/version and points to document data;
  additional prefix data uses linked index blocks and packets.
- WP 5.1's stored document version fields differ from its product version name.
  Wordling 5.2 must not invent a stored version derived from its own name.
- Document content includes single-byte functions and framed fixed/variable
  multi-byte functions; nested text areas can contain formatting functions too.
- The toolkit anticipates unrecognized functions. Reader framing and lossless
  preservation must therefore be separate from semantic support.

Derived implication: a flat Unicode string with style spans cannot itself retain
all native information. Choose a representation that preserves original bytes,
packet relationships, nested code structure, and editable semantics. The exact
data structure remains a planning decision. Toolkit advice to skip unknown codes
when reading does not authorize discarding them when writing.

## Edition and research limits

The downloaded reference's copyright leaf identifies a 6/92 edition (PDF 3),
the workbook identifies 11/89 (PDF 2), and the toolkit identifies 12/93 (PDF 2).
These identities are more precise than the hosting index's description of a
final-edition manual. We have not selected an executable release that matches
all three. The SDK also discusses non-DOS products: extract only applicable
WP 5.1 DOS obligations and verify version-sensitive details.

The reference scan has duplicated/malformed OCR. Page references are reliable
navigation aids, but ambiguous key names, numbers, diagrams and menu labels need
visual checks before becoming exact tests.

The initial inventory groups 88 obligations for further decomposition. Most are
contents-indexed only. Full subcommand coverage, all workbook scenarios, encryption,
printer/resource formats, and original-app observations remain to be researched.

## Next research work within M1

1. Identify and fingerprint the reference application and its resources.
2. Reconcile every contents/appendix entry, then study groups in dependency order.
3. Expand original-format rules into fixture specifications and negative cases.
4. Rewrite workbook workflows as our own acceptance scenarios with feature IDs.
5. Capture original command sequences, saved bytes and printed results; distinguish
   observed behavior from manual descriptions when they disagree.
