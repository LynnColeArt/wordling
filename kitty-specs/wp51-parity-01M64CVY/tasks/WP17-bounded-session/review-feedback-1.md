# WP17 independent review: changes requested

Reviewed6c93cc9, reviewer-renata. One P2 malformed-receipt invariant finding. Scope remains pure reducer; no filesystem call or arbitrary inode-existence proof is requested inside it.

## I1 — Reject impossible zero identity in Published completion

Affected internal/editor/session.go:566–581 (particularly568 and577–581).

A bound WriteSnapshot Result with correct Operation/Revision/Kind, target name/directory and source size/SHA, but Identity.ID=storage.FileID{}, is accepted as NewNamePublished. The reducer returns nil error, consumes pending, renames the displayed document and returns Editing. Independent external API overlay reproduces this without calling Directory.Save; the target is confirmed absent beforehand. This is an internally impossible success receipt from the real storage API, which always publishes a pinned candidate inode, but it slips through the reducer's existing malformed-success validation. T050/T051 require no false successful save from invalid outcomes.

The IO host receipt is trusted for actual side effects; a pure reducer cannot independently prove that any arbitrary nonzero inode exists. The finding is narrower: enforce the already established nonzero identity invariant before admitting Published success. Keep source fingerprint, destination observation and request/revision guards intact; no source rebind, fake storage.Document, filesystem execution or stronger atomicity promise.

Required fix: reject this malformed Published identity through an explicit error/failure outcome, preserving source/document/current name and preventing SameFileNoOp/NewNamePublished/Exited. Add an external reducer test with matching request and correct payload/name/directory but zero destination identity; prove it fails before the fix and passes after it. Retain real successful no-op/publication tests and late/stale/uncertain receipt tests. Rerun focused negative/race checks and actual declared gate. Missing/invalid results must not become complete success.

Retained repro: review-boundaries-1.go.txt and review-boundaries-output-1.txt. Overlay the text source as internal/editor/independent_boundaries_test.go, then run:

    go test -overlay=/tmp/wp17-review-overlay.json ./internal/editor -run TestIndependentZeroPublicationIdentity -count=1

The separate next-save continuity test passes: actual publication keeps Source.Name()==ORIGIN and displayed name COPY; another F10/Yes explicitly returns UnsupportedReplacement for that new inode without silent rebinding/no-op. README documents this bounded limitation; no additional finding is raised for it.
