# Pure native layout engine

`internal/layout` projects already-decoded native tokens into physical lines
and pages. It intentionally owns only geometry, not rendering, and never
serializes a renderer's display text back into native bytes. The production
consumer may feed a `document.Document` through `FromDocument`, or a bounded
token slice through `Project` for testing.

The everyday profile is US Letter, one-inch margins, nominal Courier 10 CPI,
six rows per inch, Full justification and relative half-inch tab stops. The
editing viewport uses nominal columns. Print justification and other resource
profiles are separate. Neither projection nor reflow takes terminal dimensions.

Each line owns a physically ordered range of tokens. Every native token occurs
once, including zero-width attributes and page metadata. Rows and text columns
are zero-based, page numbers are one-based, and inches include the margin.
PositionAt maps every native gap when geometry is qualified. GapAt and the
navigation helpers choose real editable gaps. They skip interiors of compound
page records and preserve desired x through the caller's VerticalGap sequence.
PageGap moves to the top of a printed page. After an opaque owner, geometry
becomes unqualified. Projection retains final and blank physical rows.

FromDocument and Project are read-only. Layout of an original file honors its
stored derived boundaries and fills implicit wraps for unformatted text. The
D4 owner is zero width, its transition determines the physical page, and the
dormant HRt following a compound hard-return page transition appears at the
start of the next row. A Tab advances from its current column to the live next
profile stop. Cached bytes in the stored native Tab owner do not override the
physical position.

PlanReflow is for a semantic edit continuation. It computes a document-owned
revision-bound plan from lexical spaces, unbroken words, returns, tabs and
explicit page owners. A derived SRt or soft page still means a lexical space.
A DSRt or deletable soft page introduces no separator. The document package
validates and publishes changes, maps the caret and provides its history receipt.
The planner neither emits display text as native content nor adopts the plan.
Existing explicit hard pages remain semantic hard pages. Native refresh of
existing Tab cache fields is a separate document-owned operation.

## Verification

WP93 issued source c2443182 includes the approved WP81 layout ancestor 453b9219
and reviewed WP92 correction bfea5e24. Tests exercise the actual FLOW.WP and
FIRST.WP fixtures from the pinned US WP 5.1 DOS release of 03/09/92. The physical
row, page, status, tab, vertical and page movement assertions are grounded in
the WP78 flow and scroll-search runs. The original visible Dorm HRt placement
is in scroll-search-r1/04-reveal-page-two.

Native planner tests reconstruct the exact stopped-guest originals from their
shared EVERY.WP prefix and captured bodies, verifying the complete native
fixture SHA before using it. TABEDGE.WP 426c12a6 has 63 X, a Tab, DSRt and Y.
PAGEEDGE.WP d9329e2d has 53 hard returns, 65 Q, the D4/91 page transition and Q.
The ordinary soft-page witness 36fc35c9 has 53 hard returns, 61 X, D4/0B and
alpha. Exact matching body bytes, measured caret positions and no-op reflow
convergence are tested. The WP92 generated D4/91 candidate was also retrieved,
edited and resaved by the original, then reopened and edited in Wordling.

The 564-byte FastSave family remains read-only under the document admission
contract. Projection supports its admitted token shapes without altering bytes.
Reflow requires a mutation-admitted receiver. WP94 and WP84 must exercise these
APIs through live editor and terminal paths.
