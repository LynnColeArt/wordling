# CHR1 read-only character handoff

Two fresh original runs `chr1-r1` and `chr1-r2` observed ordinary-document
Ctrl+V Compose1,36 as native `C0 24 01 C0` (number36, set1). See
`verification.json`, `native-comparison.json` and immutable run manifests.
This promotes only this selected local observation; synthetic unfamiliar pairs
and ASCII fixture tests do not establish any other original identity.

The proposed future Go read-only extension consumes approved native framing and
retains source span/raw bytes plus WP character-set/number. C0 is four bytes:
lead, character number, character set, matching trailer. ASCII20–7E remains a
separate class;80–BF is not CP437/Latin1 text. Other complete framed structures
stay opaque. A valid unfamiliar pair remains a native identity; lack of a known
glyph/locale does not prove malformed data and never permits silent replacement.
No Unicode normalization, glyph equivalence, terminal-width, print metric or
reverse-glyph writer is proposed here. Ctrl+2 in Macro/Equation/search/filename
contexts is documentary and not executed by this ordinary-document Ctrl+V probe.

A future read-only package must separately test source/export/caller isolation,
C0 token-gap atomicity, exact no-edit native length/SHA/bytes and opaque retention.
Mutations require their own field/relationship/writer contracts, unrelated-byte
preservation and original retrieve/edit/print/save witness, not a no-edit copy.
Source bytes may remain exact even when an original re-save changes its metadata;
all actual raw differences must be retained and explained rather than normalized.

Required negative cases, all synthetic planning obligations (not original inputs):

| Case | Bytes / situation | Proposed disposition |
| --- | --- | --- |
| Truncated C0 | C0; C0 24; C0 24 01 | Checked framing refusal, unchanged input |
| Mismatched delimiter | C0 24 01 C3 | Malformed frame; no accepted editable identity |
| Unfamiliar complete pair | C0 FF FF C0 | Preserve raw identity or refuse semantic interaction; not universally malformed |
| Opaque valid function | C3 0C C3 or other complete code | Preserve complete source span; this fixture inspector declines interpretation |
| Control identity |80–BF values | Never silently cast to display text |
| Input/token budgets | Exact/over declared limits | Explicit typed policy refusal before unbounded allocation/traversal |
| Missing glyph/resource | Complete supported identity, no qualified rendering | Preserve identity; explicit unsupported presentation |
| Unsafe edit | Unknown related/native structure | Refuse before changing/replacing source |

The Python evidence inspector is deliberately limited to own ASCII/C0 fixtures,
64KiB total and4096 annotated tokens; it does not validate arbitrary prefix
relationships, code groups or semantic characters. Offline self-tests exercise
20,000 deterministic random bodies and malformed/truncated/unsupported boundaries;
tracemalloc reports the maximum-token fixture inspection cost. Those are harness
measurements, not DOS limits or a production tokenizer performance claim.

Proposed future Go budget starts with existing native16MiB and document1,048,576
token policies, measured allocation/traversal before acceptance, 60s smoke then
120s bounded fuzz with two workers, original seeds plus the explicit negative
corpus above. Reconcile with actual changed API/host measurements before freezing
that package; synthetic fuzz success cannot qualify original composition, all
sets/foreign locales/dictionaries/graphics/printing. All of those remain M1.
