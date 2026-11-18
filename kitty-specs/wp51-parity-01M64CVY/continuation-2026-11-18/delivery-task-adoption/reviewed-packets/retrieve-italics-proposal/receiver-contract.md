# Proposed frozen receiver contract — review before implementation

This is WP106 design input, not a new original behavior observation or scope exclusion. Native code semantics and conservative unsafe-edit refusal apply until genuine original occupied-Retrieve qualification. Existing unrelated admission remains unchanged.

“Active Italics at gap g” means an ItalicsOn occurs in native token indices `[0,g)` without its matching ItalicsOff before g. A gap before an ON is outside; a gap immediately after ON or immediately before matching OFF is inside; a gap immediately after OFF is outside. Use native identities, never text/ANSI styles.

| Receiver at insertion gap | Source | Required WP106 result |
|---|---|---|
| Outside Italics, including just before ON or just after OFF | One/multiple balanced self-contained Italics runs plus already admitted owners | Insert exact source owners; preserve receiver outside owners and caret/history rules. |
| Inside an existing Italics run | Source contains any Italics pair, even with leading/trailing plain text | Explicit atomic refusal. Never drop/merge source pair, toggle receiver, split/reopen surrounding run or silently flatten to plain text. |
| Inside an existing Italics run | Source has no Italics owners and is otherwise already admitted | Preserve existing insertion behavior; inserted text remains under receiver Italics. No regression or new refusal. |
| Active independent Bold/Underline, no active Italics | Balanced Italics source without conflicting duplicated same-attribute source owners | Insert if existing authoritative candidate validation admits the composition; preserve exact independent flags. |
| Any | Duplicate ON, unmatched OFF, unclosed source Italics or existing unsafe/opaque/foreign/stale input | Existing explicit atomic rejection; unchanged source and receiver bytes/revision/caret/history/dirty state, no replacement. |

Authoritative validation is `Document.publishBodyWithWordRestore` → `next.CheckMutation()` (`internal/document/mutation.go:327–378`), which already rejects independently duplicated Italics flags via `checkOrdinaryBody`. The minimal implementation can retain this refusal path; do not add a second state machine if actual tests prove the existing validator supplies the frozen result. Source must separately be balanced by the existing insertion scan as Bold/Underline are today. Never bypass final CheckMutation or loosen admission/prefix limits.

Refusal preserves document state and disk originals; public runtime may advance truthful read/accounting/notice state after a real authenticated source read. Decline/cancel before source acquisition must preserve existing no-read/no-publication behavior. Do not assert that a completed real IO never occurred.

Native prefix preservation means unrelated prefix/packet bytes are preserved, allowing only the existing publication flags/required offset changes already justified by the approved writer. Do not assert the entire post-edit prefix is always byte-identical if the existing publisher intentionally changes its documented save flags. No-edit save remains byte-identical.

Full M1 still owes original behavior for active-attribute insertion and all other Retrieve relationships. WP106's conservative refusal is a bounded source safety contract, not approval to exclude those original contexts permanently.
