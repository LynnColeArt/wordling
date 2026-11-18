# Index/parser revision R1

Authoring-only correction for the sole blocker in the independent concrete-task review (SHAb5d8b549b6fff71efff9ea86f122bfd759dab50c6c288b885089a1fa75a51e0e).

The original full packet is preserved byte-for-byte outside this directory at ../retrieve-italics-resliced-proposal-history/r0/; its manifest SHA is878db41509546e369dc4f75e8f9166a1cba7eaee2b8205e87cc2711a992a99b6. The immutable review is retained both beside that archive and under provenance/independent-concrete-task-review-r0.md here.

Only index recognition/proof changed. tasks-append.md now uses canonical `## Work Package WP106/WP107` headings and explicit **Prompt**, **Dependencies** and **Requirement Refs** fields. PROPOSAL/unreserved language remains separate. Both substantive task prompt files, receiver-contract.md and the29-row coverage-conservation.md are byte-identical to the independently reviewed packet. No scope, dependency, test chronology, case, owner or original-qualification gate changed.

project.py now invokes the actual shared parse_dependencies_from_tasks_md on both this append and a complete proposed index over the frozen metadata baseline. It asserts exact equality with both authored frontmatter dependency lists and preservation of every previously parsed edge. projected-tasks-index.md, projection.json and validation.json carry that proof. Canonical typed ownership/DAG/lane results still pass for core-only and core+integration; honest zero-match future evidence warnings remain.

The projection stays bound to its explicit frozen input snapshot. Current committed metadata equivalence is separately recorded rather than silently rebasing a reviewed plan. ROOT still performs fresh actual ID/ownership/lane/normal finalizer checks at adoption. No source/index/Op/lifecycle/test/reference/Mac or other runtime action occurred.
