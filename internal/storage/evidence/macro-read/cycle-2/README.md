# WP34 review fix: independent Image wrappers

Cycle1 independent review b29d6b0 identified one P2 in source0793933: legal
whole-value assignment through Macro.Image's returned pointer changed the owned
snapshot while Macro.Identity still described its original acquired file.
Review rejection event:01M67Y328MVM08S1W8P5TE8G4T. This cycle fixes only that
storage wrapper boundary; signatures, rooted acquisition, source guards,
publication, codec implementation and native formats are unchanged.

Image now shallow-copies the private codec Image value into an independent returned
wrapper. The approved codec's data/info slices are private, Parse clones its input,
and its only accessors return cloned bytes/words/findings or value hashes/metadata.
There are no mutating Image methods. Sharing that immutable backing is safe;
replacing the public wrapper cannot replace Macro.image or another wrapper.
No deep reparse, new parser, filesystem engine or API widening is involved.
A zero Macro still returns nil Image/Export; a nil Macro receiver still panics.

The exact independent public-API reproducer is retained byte-identically as
reviewer-reproducer.go.txt and compiled with reviewer-overlay.json, without editing
reviewer files or the product working source. reviewer-red.txt captures both actual
zero/cross-image failures before the fix; reviewer-green.txt shows the unchanged
reproducer passing afterward. red-commands.json binds the initial source hash and
reviewer source hash. This overlay adds tests only; it does not replace production
code. Paths in the overlay identify this actual canonical lane checkout.

New external-package macro_image_test.go independently reproduces both assignments,
checks original Export/Identity/Name/DirectoryID and earlier/subsequent Image views,
then replaces a second view and verifies continued independence. A valid different
image comes from a second distinct approved original corpus export. The caller's
assigned view changes as requested while all acquired snapshot views remain original.
regression-red.txt and regression-green.txt retain actual before/after results.
The nil/zero test pins the pre-existing boundary without broadening it.

commands.json records exact commands, exit codes, timings and output hashes for
fresh build, test(count1), vet, race(count1), targeted before/after checks,
formatting and configured seven-check validation. configured.xml has7 tests,
0 failures/errors/skips. storage-events.txt supplies155 passing test nodes,
including all46 original WPM export cases (22 distinct hashes) plus actual
publication/source-guard/fault tests. results.json lists the affected cases.

The existing60s basename fuzz and earlier mutation/raw evidence were retained
unchanged. No new fuzz engine run is claimed for this pointer-only ownership fix;
ordinary go test runs the existing fuzz seed cases. There was no VM, original
application execution or macro interpreter validation in this cycle.

preservation.json checks the previous15 manifest entries: only source macro_linux.go
and its storage README changed. It also compares36 inherited codec/acquisition/
publication tree files to exact reviewed source0793933. The existing manifest is
refreshed only for changed owned source/doc entries and adds these new deliverables;
all historical raw entries keep their prior seals. The original manifest remains
available at0793933 for exact historical source binding. No review evidence edited.

Component repair does not close macro execution/recording/editor/conversion,
CMD51-199, resources/physical qualifications, FRs or M1. All38 obligations/91 groups
and discovered leaves remain retained; M2/PDF waits for full M1 acceptance.
Independent cycle2 review is required; this implementer issues no approval.
