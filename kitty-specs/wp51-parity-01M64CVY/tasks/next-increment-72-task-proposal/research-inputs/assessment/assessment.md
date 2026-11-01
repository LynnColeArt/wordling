# FIELD / IFBLANK next-slice assessment

## Finding and decision boundary

Approved WP67 removes the explicit-secondary-field access obstacle for its closed native cohort. The existing manual and paired original observations support considering a real, bounded **per-record primary-copy body evaluator** for FIELD1 and IFBLANK2 / ELSE / ENDIF, before adding copy-boundary pagination or native output materialization. This is a candidate architectural boundary, not a selected API, implementation plan, source-task approval, task reservation, or declaration of parity.

The smallest actual positive original contexts are CMD51-207 and CMD51-209. CMD51-207 supports literal `Hello `, FIELD1, and its observed terminal hard return for each record. CMD51-209 supports IFBLANK2 true/false branch selection, ELSE/ENDIF, a following literal space and FIELD1. Both paired runs agree. The 209 result contains an automatic opaque D4 object and hard page between copies even though its primary contains no PAGE command. Therefore body evaluation is independently useful, but calling its concatenated strings a complete merge would be false.

Three boundaries remain possible for the next design decision:

1. Per-record body evaluation with a closed whole-primary semantic predicate and an actual non-test compiled consumer. This has the narrowest existing original-backed positive behavior and does not require interpreting D4 or manufacturing a native document.
2. Full copy-loop semantics including top-level PAGE OFF/ON and default pagination. Existing 207/208/216/217 results constrain this, but it requires a larger explicit state/effect contract. It still cannot manufacture native output merely by concatenating text and form feeds.
3. Ordinary end-user Merge through the editor. This additionally requires target acquisition, revision/atomicity, error/partial-effect policy, layout and native writer contracts. Present evidence does not establish those contracts.

No task number is assigned here. The future E-controller work remains pending the separate approved64 dependency. This assessment does not reuse a historical E68 identity or rename a package.

## Exact authority and method

`pins.json` records actual Git blob identities, byte counts and SHA256s. Source analysis uses approved50 `376a37a6afd0d9f11594cadfefe0d557b874a56c`, approved53 `f70310abb1127a645bf14e984cfcb6da64082713`, and approved67 `5f3035c3efce23c96449458d2c2c783517528cf4`. The public native and explicit-data Go files were read using Git, never imported or executed. No new Go/Python product test, decoder or interpreter ran. No DOS, QEMU, private original resource, process helper, grant, canonical task/lifecycle mutation or source write was used.

The predecessor `/tmp/wordling-merge-execution-slice-assessment` closed manifest was independently verified, including its seal SHA256 `6e301ddc0ec0de3fa7da2c21c36845e88916961af46d6f3467aa18590026b5f0`. All30 actual frozen native input blobs were independently obtained through Git and matched its hashes, sizes and Git object identities. Existing approved53 audit JSON supplies observations; this is not a new native decode or original run. Five contexts each contain two original runs and three files. These observations remain bounded evidence rather than universal semantics.

WP67 approval event `01M6BTH4GXV2YHB7N0M5DGGCC1` was independently observed at immutable status source `6dea73b6e466c4c06eeaf8f5d89a2cfa34368d8d`. It records independent cycle2 approval of source5f3035c3 and explicitly leaves full M1 open. The parent-provided WP67 owned root seal is recorded as a pin; its entire publication packet was not independently located/revalidated here.

Researcher Robbie and action-scoped research governance were loaded read-only (`--no-mark-loaded`); compatibility and roadmap constraints were read. The PDF skill was applied for read-only rendering and visual inspection. `manual-observations.json` identifies seven visually checked pages and the rendering warnings. No manual pages or full copyrighted text are copied into this packet.

## Manual constraints

The cached WordPerfect 5.1 DOS Reference is edition **MNUS1WP51X1C-6/92**, June1992, later than the selected March9,1992 executable. PDF SHA256 is `ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531`; OCR text SHA256 is `f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c`. Exact public locators:

- [ELSE, printed816 / PDF833](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=833): an optional false branch; execution continues after ENDIF.
- [ENDIF / ENDRECORD, printed818 / PDF835](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=835): IF closure versus secondary record delimiter; readability hard pages in secondary editing do not authorize copying them into field values.
- [FIELD, printed819 / PDF836](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=836): identified field contents come from the current secondary record.
- [IFBLANK, printed825 / PDF842](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=842): tests the indicated field, requires ENDIF, and may use ELSE.
- [PAGE OFF, printed847 / PDF864](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=864) and [PAGE ON, printed848 / PDF865](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=865): hard-page separation is between primary copies; OFF/ON state is global across primary/secondary files until changed. The documented HR convention matters for line separation.
- [Notes, printed878 / PDF895](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=895): IFBLANK/IFNOTBLANK differ from the legacy ? shorthand; literal HR/tab/formatting codes are not generally discardable whitespace.

These pages plus originals support the explicit empty-field branch observed below. They do not qualify missing-field behavior, whitespace-only blank semantics, arbitrary expressions/named fields, nested conditionals, or all formatter/control behavior for a first native evaluator. Later manual prose does not override the selected executable's observed behavior.

## What the public source actually permits

The approved native `Program` is an immutable by-value handle with `Valid`, `Source`, defensive `Inspect`, and source-bound `Bytes`. Its private owner preserves source identity. Its validity is syntax admission, not permission to execute every admitted command. PAGE OFF/ON and BREAK can be syntactically admitted; NEST remains blocked. Thus a new evaluator needs a separate closed whole-program predicate before effects. A hand-assembled or modified Inspection cannot confer authority.

FIELD has only observed operand1; IFBLANK only observed operand2. Operand data and the external tilde terminator have explicit spans but remain ordinary character tokens in the token list. A naive character-token concatenation leaks `1~` / `2~` into output. Command frames plus their operand/terminator footprints must be accounted for exactly. Conditional `Match` is a command index, not a token index; IF matches ENDIF, ELSE matches ENDIF, and ENDIF matches IF. There is no direct IF-to-ELSE pointer. General well-formed conditional structure in the reader does not itself establish execution evidence for nesting.

Approved WP67 `explicit.Data` retains a captured native Secondary view, source owner, defensive inspection, explicit record count, and one-based `Field` access. `Value.Bytes`, `ExplicitlyEmpty`, and `Provenance` retain the correct field-content ownership and enclosing record provenance. Missing/out-of-range fields return a typed refusal and invalid value. An explicit zero-byte field remains a valid empty value with its own EF/HR sites. Values are not inferred from a stored count.

WP67's admission predicate stays narrow: one/two explicit fields, empty or printable non-tilde content excluding all-space values, exact observed EF/HR/EOR frames, empty unaddressed tail, and retained opaque D4+HP post-record metadata from the six observed cohorts. All coverage, caps, findings and source ownership checks remain required. RawStoredCount pairs are literal evidence only; **never infer field count as StoredCount minus1**. D4 payload meaning, raw count meaning, and tail semantics remain unresolved.

Generic native Secondary `Supported` and `Admit` remain blocked. Explicit Data does not promote Secondary to Program or create a writer/layout capability. The qualifier is a genuine compiled DATA consumer, but it reports field diagnostics; it does not execute a Primary. Reusing that diagnostic JSON as expected output would not create an evaluator.

## Original observations and smallest acceptance claims

`original-observations.json` retains both original run identities, owner paths, command spans, explicit field bytes and result projection evidence. Projections are diagnostics, not native result generation.

| Context | Actual whole-result selected bytes | Supported inference |
|---|---|---|
|207|`Hello Alice\n\fHello Bob\n`|Each copy emits Hello + FIELD1 + observed terminal HR. Default copy separation includes hard page; field2 is absent and has no qualified IFBLANK meaning.|
|208|`Hello Alice\nHello Bob\n`|PAGE OFF suppresses automatic separation. Outside the narrow no-PAGE evaluator candidate.|
|209|`FILLED Alice\fEMPTY Bob`|Alice has explicit field2 YES; Bob has an explicit zero-byte field2 with EF/HR. IFBLANK2 chooses FILLED/EMPTY respectively, then FIELD1. Default boundary remains separate.|
|216|`Hello Alice\n\fHello Bob\n`|OFF before text then ON after it restores subsequent between-copy pagination.|
|217|`Hello Alice\nHello Bob\nHello Carol\n\fHello Dave\n`|Conditional PAGE ON does not retroactively insert a boundary before Carol; it affects the next boundary before Dave.|

For209, the primary sequence is IFBLANK2, `EMPTY`, ELSE, `FILLED`, ENDIF, space, FIELD1. The original result has no residual merge commands. Its first copy is `FILLED Alice`, then retained opaque D4 and HP, then `EMPTY Bob`. The actual empty Bob field is not a missing trailing field. In207 the missing field2 must remain a refusal if a new consumer requests it; this assessment does not claim the DOS app itself refused it.

A minimal future acceptance surface could compute per-record bodies for both paired207 and209 runs using the actual immutable Program and explicit Data. Expected body observations would be `Hello Alice\n`, `Hello Bob\n`, and `FILLED Alice`, `EMPTY Bob`. That is an inferred decomposition constrained by original result spans, not a new DOS run and not a whole-result equivalence claim. The independent comparison must also retain the original D4/HP owner spans as unresolved boundary evidence, rather than silently erasing them.

A real next component must execute its compiled semantic representation against actual Data values. At least one non-test compiled consumer must traverse raw native primary → admitted Program and raw secondary → explicit Data → evaluator → computed effects. It may compare effects with independently owned original observations. It must not copy expected strings, replay old JSON, use filenames/hash allowlists as semantic switches, or call a fixture projection an implementation. A pure effect stream is not a replacement canonical document format and does not authorize saving it as native output.

## Minimal falsifiers and remaining witnesses

The next design must state its accepted grammar and finite work/output/memory limits before implementation. Native input caps alone do not bound expanded output tightly enough: record count multiplied by primary literal size can be large. Pre-append output limits and total work accounting need explicit failure semantics; no partially accepted result or editor mutation should become authoritative on refusal. Loops, nesting resolution, filesystem helpers and unbounded recursion are unnecessary for the narrow candidate.

Evidence-driven acceptance/falsifiers to carry forward:

- Both paired actual207/209 sources drive computed outputs; reversing branch selection must fail209, and using field2 instead of field1 must fail substitution.
- Explicit empty Bob field succeeds in209; requesting field2 from207 refuses. Conflating empty, missing, unaddressed tail, and stored-count arithmetic fails.
- Command operand/terminator bytes do not appear in literal output. Replaying token characters indiscriminately, misusing command Match as token position, or falling through ELSE/ENDIF fails.
- Field value extraction excludes EF, separator HR, EOR, opaque post-record D4 and HP. These stay source-owned provenance, never reinterpreted as value text or discarded from original evidence.
- A closed whole-primary gate refuses PAGE/BREAK/unknown commands, unqualified controls and unsupported shapes even in a branch that appears untaken. Programs208/216/217 provide actual PAGE negatives for the narrow candidate; their explicit Secondary Data remains valid.
- Zero/foreign owners, wrong role, malformed or capped reader input, missing field, stale/fabricated inspection and work/output limit exhaustion produce explicit refusal with no promoted partial output. Defensive copies and by-value immutable ownership must survive caller mutations.
- Synthetic alternate literal/value cases can expose hardcoding and prove a live implementation, but cannot enlarge claims of observed DOS semantics. Use existing source-closure/build-provider safeguards rather than weakening WP67's production closure.

Additional original witnesses would be needed before general claims for missing IFBLANK fields, whitespace-only values, arbitrary field numbers or expressions, nested conditionals, controls inside conditional branches, and PAGE state across nested primary/secondary files. For top-level PAGE, existing207/208/216/217 are already meaningful discriminators; a future plan should explain whether more witnesses are needed for its exact larger claim. No new witnesses were acquired here.

No native serialization/materialization claim follows from the body candidate. Existing ASCII editor limitations (including inability to insert0A/0C as ordinary text) and absence of a general ordinary Merge host contract remain predecessor-recorded gaps; this bounded assessment did not re-audit editor source outside approved50/53/67. Native writer bytes, resource/layout equivalence, acquisition, target revision, failure ordering, save/reload and end-user UI still need separate evidence and implementation. Full M1, all other command families, and PDF/M2 remain open.
