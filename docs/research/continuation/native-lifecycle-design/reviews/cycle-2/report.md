# Independent native lifecycle architecture review — cycle two

Reviewer codex/reviewer-renata, existing wp51-parity-01M64CVY mission. Refreshed
review action governance, retaining resolved reviewer boundaries. This independent
rereview changes no implementation, primary artifact, task, lifecycle or VM state.

**Verdict: DESIGN-READY for dependency-ordered task authoring. R1 closed; zero
unresolved findings.** This is architecture readiness, not package implementation,
original behavior qualification, product compatibility or full M1 approval.

Frozen decision SHA256:
`87544a5682f624a6f733c90ce9d9d50cd305f69f8e3ac62e710ddba3cb5ba676`.
Frozen manifest SHA256:
`d80913068eec2d0b15a73227c39440c0c1e9d3e6209b774c4296e9776cc85f5d`.

## R1 disposition

The revision now separates immutable native birth Origin, retained acquired source
guard, displayed name and last-publication receipt. Later sourced Save As never
implicitly Read/rebinds or replaces the guard. Loaded documents keep the original
acquired source; genuinely New documents retain their first positively acquired
anchor after the initial PublishNew plus matching Read. The native revision and
history remain independent of that first acquisition. Displayed name may update
to the successful draft, consistent with approved17 session.go:591. Saving is
not Retrieve, and no later guard migration is included in A–H.

This resolves the exact contradiction with approved b479983 source and the actual
cross-directory source-remains regression. The revised contract requires original
source or New first-anchor mutations to cause StaleSource on subsequent sourced
operations after Save As. A separately published output is not silently promoted
to a source guard; its mutation matters through actual destination observations
or an explicit acquisition. The distinction preserves source authority while
retaining name/receipt evidence.

The acceptance requirements now explicitly include retained-source/first-anchor
mutation, independently mutated prior output, cross-directory source retention,
displayed-name versus receipt separation and replacement refusal. Cross-directory
no-edit publication preserves approved Save behavior; PreparePublication's narrower
same-Directory requirement still applies to edited candidates and cannot be
escaped by rebinding or synthesizing a source. A displayed name for a distinct
existing output does not become a same-file no-op. Existing-file replacement
remains unsupported, and neither a prior receipt nor New birth grants overwrite
permission. A proposed later migration requires its own research, compatibility
decision and independent review rather than silently deleting existing tests.

## Regression and retained gates

Inspected the complete decision diff and machine-manifest changes. Storage A's
distinct private prepared type, one transaction, mandatory loaded-source checks,
caller-copy ownership, WPM refusal, destination checks, no-replace candidate
verification, cleanup/pin uncertainty and exact outcome limits remain unchanged.
First source-less PublishNew still needs exact matching storage.Read before its
anchor/name/clean state becomes authoritative. Published-but-unbound, uncertain,
late and duplicate results retain detached receipts and cannot authorize unsourced
retry, clean state or exit. The revision narrows follow-up acquisition to first
never-sourced publication; it does not weaken that safety state.

E still introduces an immutable in-memory Origin while retaining private Revision,
cursor/history identity, loaded OriginalExport semantics and current Export bytes.
OriginalExport remains ([]byte,error); New consumers explicitly handle
NoLoadedOriginal and publish current Export. No constructor defaults, native
schema or original first-save semantics are invented. D remains a prerequisite,
B/C retain original-resaved field/deleted/slack/FastSave duties, and approved final
27/36 and28/37 interfaces must be inspected before adapters are selected.
Unapproved26 remains labeled feasibility evidence only.

A–H dependencies, ownership direction and graph proof are unchanged. Actual
40-package dependencies and19-lane assignments still match the manifest, and
independent recomputation confirms both proposed package and lane quotient
orders valid and acyclic. Canonical ownership/glob/finalizer validation, actual
captured-exit research dependencies for B/D if used, production reducer/worker/
cmd integration and original differential evidence remain required at authoring
and implementation. H continues through the actual31 schema with honest input-less
startup evidence. No detached helper, fixture template or parser self-comparison
can substitute for the required production/native/original proof.

## Verification and evidence custody

All35 manifest sources match exact lengths and SHA256, including the newly listed
approved17 public-API regression Git blob. Independently verified the previous
exact decision and manifest drafts against their original cycle-one hashes and
all three sealed cycle-one review artifacts against the revision receipt. Cycle
one's report/findings/seals remain intact and still state their historical rejection.
The current graph proof equals the earlier graph proof byte-for-value; actual
prompt dependency and lane mappings were checked again. No unnecessary VM/build
or execution test was performed for a design-only correction.

Machine findings and source/deliverable seals accompany this report. Primary
remained clean at ebf5774007bec9e63a586ba078d85aa5d7bdb2ae. No repository/lifecycle
mutation, source fix, guest or pending process was introduced. Full38 obligations,
91 groups and M1 remain open. A–H are proposal labels until the supported authoring
workflow assigns and validates real tasks; design readiness does not authorize
scope waivers, accept/merge or M2/PDF.
