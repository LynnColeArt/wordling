# M1 domain model — discovery checkpoint

These are conceptual boundaries for planning, not a finalized on-disk schema or an implemented API. WP native files remain unchanged.

| Entity | Identity / state | Relationships and invariants |
| --- | --- | --- |
| Native image | Exact bytes, original file identity, validated bounds | Owns prefix, index/packet spans and body spans; no-edit serialization returns exact original bytes. Opaque spans stay intact. |
| Document | Native image plus interpreted editable structure | Original characters, text/code positions, paired codes and nested text areas; semantic support is explicit, never inferred from parse success. |
| Edit command | Original command, cursor/selection, declared preconditions | Produces a bounded document change or explicit refusal. Normal and Reveal Codes views share the same document and position mapping. |
| Undelete history | Up to three original deletion entries | Captures command-specific restoration content and code behavior, distinct from future modern undo. |
| Session | Documents/screens, modes, prompts, initial settings | Owns command routing; terminal cells display state without defining layout or native identity. |
| Resource profile | Fingerprinted printer/font/character/language settings | Determines layout and printing comparisons; executable date alone is insufficient identity. |
| Layout result | Document revision plus resource profile | Contains lines/pages/glyph placements used by original preview/printing; invalidated by relevant edits or settings. |
| Macro execution | Program, call stack, loops, handlers, variables | Uses original WPM representation. Loop NEXT/BREAK and error scope require explicit context. |
| Merge execution | Primary stack, secondary records, copy state, page mode | Distinct from macro execution; global PAGE state crosses nested primary/secondary return boundaries as observed. |
| Save transaction | Source identity, candidate bytes, destination decision | Refuses unsupported changes or unsafe replacement; failure preserves existing file. Original prompts are session behavior. |
| Acceptance scenario | Stable CMD51 ID, inventory links, manual citations | Separates authored expectations, original observation, implementation and differential verification. |
| Reference run | Recipe, executable/resources/environment, captures and hashes | Supplies bounded observations; never proves Wordling behavior unless Wordling was separately exercised. |

Translation boundaries: native bytes → validated spans → semantic document; document/session → terminal view; document/resources → layout/print; original automation tokens → context-specific execution. Each boundary needs its own failure behavior and evidence. Unknown bytes must never become silently disposable semantic defaults.
