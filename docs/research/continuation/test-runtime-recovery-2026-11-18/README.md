---
type: reference
updated: 2026-11-18
audience: Mission 1 qualification implementer and reviewer
---

# Missing TEST baseline and proposed fresh qualification

The lost file remains unrecovered:
`/tmp/wordling-WP70-runtime-qualification-source-freeze-v19/expected-inputs.json.gz`,
1027525bytes, SHA256
`c5861dd98775ea3be3b36c7d6e88219cdca96f0d41e230a818c2a5eba089c012`.
The existing tracked pin is evidence of its identity, not a copy of the payload.

The recovery archive and Git metadata searches are documented beside this file.
Following the owner's home-directory suggestion, `/home/lynn/work-trees` was also
searched, including hidden filenames and a separate linked-path search. No
Wordling checkout or matching frozen artifact was found. A scoped archive census
examined31451files without errors and found only two unrelated Schema Baron
archives. That census excluded build/cache/dependency directories; the broader
linked-path pass reported unrelated broken dependency links. This is a bounded
negative search result, not proof about every inaccessible linked location.
`/home/lynn/workdir` was empty. Other projects' worktrees were left untouched.

The approved architecture review permits authoring a **new**, separately owned
current-TEST qualification prerequisite. It does not approve a capture or runtime.
The selected public CPython3.12.14 BASE and canonical current TEST20/P sources can
be reviewed as a fresh reference before candidate creation. Actual provenance,
complete role closure, cap fit, candidate qualification and genuine public TEST
CLI compatibility must still pass. Neither a current candidate nor the WP104
ORIGINAL/CONTROL deployment can replace the lost historical expected inputs.

The versioned plan preserves V19/188 history, operational TEST/P modules and
issuer limits. Its task-authoring review corrects the draft32/12 estimate to
include both construction targets; a complete source-reviewed command manifest
is required before effects. No new package ID is registered by these documents.
Full Mission1, WP104 compatibility and original qualification remain open.
