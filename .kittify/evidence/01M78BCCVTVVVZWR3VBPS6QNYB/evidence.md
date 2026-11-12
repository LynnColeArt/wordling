# Wider merges and structural Undelete review

Independent review approved source `d7ab79a473245fcfa9a24f92cbbc4eac0ba1bf2a`. The independent build and the release candidate both have SHA-256 `dab476d3b2ba9a135c02075dab77bbe2d957857a8d6d521b7bc898ace29efd19`. The reference was the pinned US March 9, 1992 WordPerfect 5.1 DOS release with Standard Printer.

- Wide secondary records and wrapper primaries match complete DOS saves. The Linux terminal also authors and saves the 53-field, exact decimal operand, and wrapper source files. For archived wrapper results, the original reopened actual Wordling 820- and 1076-byte-index saves, edited them, and produced the exact original 564-byte-index saves. [Original fixtures and replays](wide/README.md)
- An independent mixed-width nested secondary replay shows that an exhausted IF BLANK lookup stops its child stream and resumes the parent, with PAGE OFF still in effect. The complete F10 save matched DOS. [Original output](wide/nestedmissing/MERGED.WP5)
- Structural Undelete restores exact native owners and dependent record counts and page caches. The independent terminal runs covered the three-entry history, source preservation, current-caret insertion, editing between deletion and restore, and sharing across the tested Doc 1/2 lifecycle. [Structural replay](undelete.md) and [interleaving fixtures](undelete-mixed/README.md)

The exact preview binary passed 30 wide and wrapper terminal cases, six structural Undelete journeys, the extended authoring journey, 26 prior merge cases, and the 22-case everyday qualification with original DOS round trips. Independent review passed 42 terminal cases. Go build, tests, vet, and focused race tests passed. The approved digest was verified after installing the local preview.

The verified record form has up to 53 explicit one-line fields on a single page. Records that paginate internally, additional archived printer resource graphs, and global history in ordinary-only sessions remain open in Mission 1.
