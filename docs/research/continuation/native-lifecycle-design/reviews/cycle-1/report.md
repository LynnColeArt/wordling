# Independent native lifecycle architecture review

Reviewer: codex/reviewer-renata, existing wp51-parity-01M64CVY mission. Resolved
reviewer profile and loaded `charter context --action review`. I did not author
the proposal or change implementation, repository, tasks or lifecycle state.

**Verdict: changes requested before A–H authoring. One P2 design blocker.**
This is a temporary architecture review, not package or product approval.

Reviewed decision SHA256
`8ff3d32bf8708d4d9f38cce4617347c4972d61748ff31cf2490bd81041403fee`
and manifest SHA256
`f6500dc3ac538d88b79c6e0ae36c762c1ddab4b2c0f1c017080842132d2eaab2`.
All34 listed inputs match exact length/SHA, including Git source objects. Actual
40-package dependencies and19-lane assignments equal the manifest. Independently
recomputed proposed package/quotient graphs and checked both topological orders:
acyclic. Those proofs remain temporary, not canonical finalizer approval.

## Finding R1 — P2: qualify later Save As guard rebinding explicitly

Location: decision.md:60, “Any later successful Save As likewise needs a verified
acquired new anchor before switching the active guard/name”; F/G contract and
its claimed preservation of approved session behavior.

Approved WP17 b479983 does not switch the acquired source after publication.
`internal/editor/session.go:544` assigns source only on Read. The WriteSnapshot
result branch at561–593 validates the published receipt and updates displayed
name at591, while retaining the source snapshot. README:14–15 explicitly says
that storage source stays distinct from the displayed name and is never silently
rebound. The actual external-API regression
`TestGivenSeparatePinnedDirectoriesWhenPublishThenTargetIdentityAndSourceRemain`
at session_test.go:599–626 requires a COPY published in another pinned directory
to retain the original source directory. The proposed universal new-anchor switch
changes that existing contract. It can also change which external file mutation
causes subsequent StaleSource refusal: after rebinding, an altered original source
would no longer be the active guard. This is a material safety/consumer transition,
not merely storing an additional publication receipt.

The name and guard must not be conflated: approved17 DOES set the displayed name
to the successful draft. This finding does not claim that all original names stay
unchanged. The first acquired anchor for a genuinely source-less New document is
a reasonable distinct architectural choice; it does not establish later loaded
or already-bound Save As semantics. D currently qualifies genesis/first-name
transitions, and neither its stated scope nor an existing cited observation
qualifies a blanket later source rebind.

Required revision: explicitly preserve the approved loaded-source anchor behavior
for existing flows, with a separately named last-publication observation, OR
specify a deliberate compatibility migration and prerequisite original branch
research for later Save As, including name/source/dirty/cancel/retry semantics.
State which guard remains required for Loaded and already-bound New documents,
including original-source mutation, prior-output mutation and cross-directory
publication after Save As. Tie any migration to actual approved27/36 APIs and
meaningful source-stale/receipt/rebind tests before F/G authoring. Do not silently
remove the approved source-remains regression or present this as preservation.
No new package numbers or implementation fixes are prescribed by this review.

## Other architecture assessments

The separate NewPublication type is a reasonable way to keep the existing sourced
PreparePublication/Publish preconditions mandatory. The proposed private nonzero
guard kind, one no-replace candidate transaction, unchanged old Save behavior and
source checks at every existing prepare/publish/pre-link boundary preserve the
actual24 storage contract if implemented and tested as stated. Existing Save can
publish a source snapshot across directories; it must not acquire the narrower
same-directory requirement of PreparePublication during factoring. The decision
explicitly retains that distinction. No source-less storage type can prove native
genesis by itself; the required editor routing invariant makes this limit honest.

The transaction proposal preserves candidate creation/pinning, bounded write and
close checks, candidate exact identity/bytes, no-replace link, cleanup/final
verification and pin-close uncertainty. DestinationMayExist and candidate residue
remain visible; observed destinations are not removed as rollback. The explicit
published-but-unbound state after successful link but failed Read binding is
appropriate. Real storage.Read must match full final identity and payload and
must not replace the native revision/history. Late/duplicate/cancelled results
must remain detached, prevent a fresh unsourced bypass and require deliberate
reconciliation. Tests described in A/F/G are necessary implementation gates, not
proof already supplied by this document. No durability or atomic external-source
freshness guarantee is implied.

Origin is an additive internal lineage concept, distinct from private revision
identity, acquired source and saved receipt. Maintaining it across candidate
validation and Restore is consistent with approved25 immutability. Zero origin
must remain invalid and equal-byte independent acquisitions distinct. The New
birth tag is an architectural classification, not an original native field or
proved original command semantic. D remains a real prerequisite.

OriginalExport already has signature `([]byte,error)` in approved25
mutation.go:44. Returning a typed NoLoadedOriginal error only for a newly introduced
New lineage is therefore not a signature break. Loaded behavior must retain exact
initial-image copies across edits and saves. The proposal states that correctly.
Before E/F/G implementation, explicit consumer migration tests still need to show
that new-origin callers handle the refusal and use current Export for publication,
while every existing loaded consumer retains its behavior. No alternate byte
meaning, public origin setter or save-time Parse/reset is acceptable. Inspection
of final approved27/36 and28/37 interfaces before choosing exact adapters remains
a valid sequencing requirement; it does not authorize silently breaking them.

D correctly blocks construction until original empty-save/genesis/default,
resource and first-save transitions are established. Typed NewConfig must not
invent zero-config defaults, copy an unexplained fixture prefix, create a dummy
loaded source or infer new native field meanings. B/C remain mandatory for
original-resaved deleted/slack/FastSave admission; construction cannot normalize
those files or bypass that work. Candidate original Retrieve/edit/print/save and
Wordling reopen/edit remain required. No constructor schema is approved here.

A–H ownership and consumer direction are coherent at the proposed level: storage,
disjoint original research, document, editor, TUI/executable, existing conformance.
No code→planning→code cycle, F→37 or G→31 backedge is present. B/D must add actual
approved captured-exit helper dependencies before final authoring if used. Existing
prompt/ownership validation, new namespace allocation and actual final consumer
source inspection remain gates. F must exercise the actual reducer, G the actual
cmd/wordling worker path and original differential, and H the actual versioned31
schema with honest input-less startup evidence. Detached helpers cannot stand in
for production integration.

## Verification and limits

Read actual approved storage24/34, document25, editor17 and TUI18 source blobs,
referenced contracts/ADRs/current prompts and labeled unapproved26 checkpoint.
Unapproved26 is only seam feasibility evidence. Independently verified every
manifest source, plus approved17 public-API regression source; machine seals bind
all inspected versions. No VM, build, implementation test or lifecycle gate was
run: this review assesses the design against existing contracts, not implemented
behavior. No source/private binary/manual material is republished in this report.

Primary was clean at ebf5774007bec9e63a586ba078d85aa5d7bdb2ae during audit.
Only temporary report, findings and seals are deliverables. Full38 obligations,
91 groups and M1 remain open; no compatibility, package, mission, merge or M2 grant
follows from resolving this design finding.
