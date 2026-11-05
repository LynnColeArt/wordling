# WP77 integrated baseline adoption report

This is a bounded foundation qualification, **not everyday editing completion or full WP 5.1 parity**. The original c7 preview candidate was rejected as unsafe because of R77-001. This retry reviews that complete 23-file delta together with the independently approved WP90 repair and this package; it cannot approve the unrepaired candidate. A different WP77 reviewer must approve the complete repaired source before downstream consumption. This package changes only `tests/baseline_adoption/`; it does not silently repair or approve product source.

## Source custody

Candidate `c7f14fd497da62bb577b6bdab7d4be3fb124e546` has parent `f89a48627916b5cb9e360c35047350031b6f06a9`. The independently reviewed source intake is `876bbf85064a847fa0d5e745b6ceb7bcbc912d42`. Root preservation checkpoint is `ee619218d6dbc9f57e00c400d03d940137c205a9`. Approved repair is `78a05497dcf1d175049fe2c8e57fd502818521fe`, approval event `01M6NWK5WXZEMEPGVN1YA8K7GY`; reviewed repair intake is `1561c87ee2c1f7c9532271c482ec97462cc7cbcf`. Actual retry source is `5304c643a2d5362acef4e6f291ae517074bbbaa0` in lane-z. Full source identities, original and actual hashes are in [custody.json](custody.json).

[custody.py](custody.py) first verifies both approved repair and intake ancestry/parents, exact repair review event/verdict, and preserved WP77 rejection. It derives the 15 repair paths from the approved commit itself, requires the receipt path set and all bytes/hashes to match, and rejects any other inherited product delta. All 23 original candidate paths retain their separate c7 hashes; unaffected paths must remain exact c7 bytes, while the one affected original path (model.go) must match the approved repair. It also verifies every one of the 76 previous WP-to-lane memberships, every pre-existing worktree path/branch identity, and retention of every pre-intake status event record. It compares the finalized planning snapshot attached to this claim against `milestones/everyday-editing/runtime-before.json`; concurrent primary planning is not fabricated as source evidence. Root/H HEAD changes are explicitly recorded checkpoints, not an assertion that their pre-intake HEADs stayed frozen. No prior package was marked approved again. Candidate test success does not inherit WP76 approval.

## Audit of every inherited path

Paths are repository-relative. Review was by source diff and adjacent caller inspection, supplemented by the tests below. A retained partial behavior is not an original-app fidelity verdict.

| Path | Delta and assessment |
| --- | --- |
| `cmd/wordling/main.go` | Normal CLI enables historic chrome. Optional nonhistorical Ctrl aliases default off. Real CLI/PTY probe exercises this entrypoint and normal cleanup. |
| `internal/document/admission.go` | Adds native 0A HardReturn to bounded mutation admission; does not permit arbitrary control bytes or opaque owners. Existing size/framing admission remains. |
| `internal/document/deletion.go` | Plain-New backspace bypasses only unqualified-history-effect refusal after owner/revision checks; whole body must have one byte per token and still pass mutation admission. Erasure preserves prior fragments but deliberately withholds Undelete qualification. No new arbitrary cross-code mutation authority established. |
| `internal/document/document.go` | Appends HardReturn enum without renumbering prior kinds; exact single-byte 0A identification and presentation. Native bytes remain authoritative. |
| `internal/document/history.go` | Separates owner checking from effect qualification. Other history operations still reject unqualified effects. New backspace is not a claim of original history semantics. |
| `internal/document/mutation.go` | Public InsertHardReturn uses existing checked publisher; only its explicit path allows 0A. ASCII APIs retain printable-only validation, cursor ownership and limits. |
| `internal/document/reveal_catalogue.go` | Transfers [HRt] labeling from opaque fallback to native HardReturn without losing its owner span. |
| `internal/document/reveal_catalogue_test.go` | Adjusts expected kind for newly understood HRt; preserves owner offsets/length and unknown-owner assertions. |
| `internal/editor/editing.go` | Enter dispatch uses native insertion and normal revision/history adoption. Boundary navigation traverses native owners and interrupts history through existing rules. Physical soft-wrap navigation is absent. |
| `internal/editor/session.go` | Appends End/Down commands, admits Enter and bounded Home sequences. Existing transition identity and modal checks retained. Known incomplete Home/vertical behavior is not accepted as original parity. |
| `internal/storage/list_linux.go` | Observes a separately opened handle beneath the pinned directory; sorting affects display only. Selected reads still use validated storage acquisition. No write/delete authority added. |
| `internal/tui/README.md` | Truthfully distinguishes default historical keys from explicit host-only flag. Broader flat/bounded limitations remain. |
| `internal/tui/ascii_viewport_test.go` | Replaces formerly unknown HR negative fixture with still-unknown HPg, preserving negative presentation coverage. New HR has separate positive coverage. |
| `internal/tui/chrome.go` | Establishes historical colors and row budget, but retains obsolete toolbar/chrome functions. These are not a second native model; WP85 must remove obsolete presentation routes. |
| `internal/tui/chrome_test.go` | Adds menu/focus/navigation/F5 probes. Existing F1 submenu-disappearance expectation is not the original reference oracle; WP85 must replace it with observed attributes/focus behavior. |
| `internal/tui/control_keys.go` | Pure opt-in translation to ordinary original command keys. Default model/CLI tests show Ctrl+B/S/O/R/Q neither mutate content nor invoke I/O/exit. |
| `internal/tui/historic.go` | Partial bar/menu/browser implementation uses normal reducer for implemented actions. Unsupported commands identify missing implementation. It does not implement full menu vocabulary, original focus semantics, browsing, Look, settings, Help or physical layout. F5 list read is synchronous and whole-directory, a scale/UI-latency concern for WP79/WP84. |
| `internal/tui/macro_model.go` | Adds display row and prevents Escape-as-repeat from intercepting an active Home prefix. Does not change macro document authority. |
| `internal/tui/model.go` | Routes visible chrome input, appends End/Down mapping and renders native paragraphs. Historic view bypasses previously qualified anchor route intentionally; therefore old anchor tests do not qualify the normal CLI view. Ordinary vertical navigation, wrap and multiline Reveal remain absent. |
| `internal/tui/new_test.go` | Tests New correction and native HR save/reopen. These are not post-retrieve repeated editing, history or overwrite acceptance. |
| `internal/tui/reveal_anchors_test.go` | Keeps opaque fallback negative coverage with HPg after HR became understood. Does not establish new historic view equivalence. |
| `internal/tui/reveal_inspection.go` | Propagates display row from legacy frame. Inspection remains read-only and separate from command authority. |
| `internal/tui/runtime.go` | Adds explicit opt-in flags/root display label and starts a visible bar for CLI chrome. Existing directory ownership/worker shutdown mechanisms remain. |

The first audit incorrectly reported that no authority bypass had been established. Independent review disproved that claim with R77-001: active menu/browser input leaked into native text at 11 rows. That first review remains rejected (event `01M6NV9Z0CPE615HWJBBJK38Q8`); the original report and checks remain accessible at commit `e44fc41925e74e3a348b21579f86b611dff86fd7`. [review-history.json](review-history.json) binds those historical artifacts and the rejection/repair evidence by hash. The separately owned WP90 fix now routes modal input independently of rendering height and gives a truthful small-window active/cancel view. This retry verifies the actual repaired source and regressions; no audit-only relaxation was adopted. The safety gate remains unchanged, and any additional unsafe finding requires correction and independent review before adoption.

## Reproducible verification

Run from the issued checkout:

```sh
python3 tests/baseline_adoption/custody.py
go test ./tests/baseline_adoption -count=1 -v
go build ./...
go test ./...
go vet ./...
```

No emulated original executable or proprietary dictionary is required by these baseline tests. Original comparison evidence remains in `docs/research/everyday-contract-2026-11-05/` and is qualified separately by WP78.

[baseline_test.go](baseline_test.go) uses exported `tui.Open`, `Model.Update`, `View`, `State`, and immutable session/native inspection. It executes actual returned commands; no fabricated completion messages, private field edits or fixture-specific product branches are used. It verifies:

- Startup menu and editable cursor at 80×25 and 283×82, safe empty-document boundaries, real mouse File entry and return to typing, and default Ctrl alias isolation.
- Ordinary text, Enter encoded as native 0A, Backspace correction, Reveal-only conservation, exact first-save file bytes, F5 retrieval and refusal conservation on the currently unsupported retrieved-Bold route.
- Save/exit cancellation with byte and filesystem preservation, and the actual F7/No/Yes normal exit reducer flow.
- R77-001 public Model conservation for both F5 and Alt+= across 12/11/25 rows, including actual render calls, native bytes, full session snapshot and history, truthful small-window focus, cancellation, resumed editing and exact post-modal native save.
- The compiled `cmd/wordling` under a Linux PTY, using actual xterm F10/F7 escape sequences. It types two paragraphs, publishes a native file, completes normal exit with return code zero, compares termios state and alternate-screen restoration, and verifies exit leaves the saved file unchanged.

The same built binary also runs the independently approved WP90 CLI resize probe, now present through actual source intake. Both modal cases retain exact BASE native body across 25→11→25, cancel, save and normal exit. No rejected WP77 source was used by WP90; this retry consumes its approved probe in place without an overlay.

The PTY probe uses an 80×25 xterm-256color/truecolor profile and minimal terminal query replies. It is not physical host function-key certification. Actual process exit also rejects unresolved publication according to the CLI's existing completion checks. The probe checks current candidate prompts; it does not certify those prompts as original fidelity.

Full build/test/vet passed at the source in custody.json. Logs and exit codes are in [checks/results.json](checks/results.json); focused output is [checks/baseline.log](checks/baseline.log). New Go source is gofmt-clean; Python scripts parse without generated bytecode. The first attempt also ran three deliberately corrupted test assertions (menu, native body and final exit state) each failed, then the original tests were restored and passed. This limited assertion-sensitivity check is recorded in [checks/assertion-sensitivity.json](checks/assertion-sensitivity.json); it is not a mutation score for the product.

During probe authoring, two runs failed because the test expected guessed strings: “Name of File” instead of the actual candidate's “Document to be saved:”, and a “Saved” label that is absent after successful binding. These were test synchronization errors. The final probe waits for the actual save prompt, native publication, returned document status and normal-exit questions. No product change was made to accommodate it.

## Known remaining product gaps and owners

| Observable gap | Intended package |
| --- | --- |
| Saved/retrieved documents and repeated attribute/correction cycles remain narrowly admitted; retrieved Bold refuses. Backspace history is unqualified. Ordinary block/Undelete scope is incomplete. | WP80, WP82 |
| Edited overwrite, backups, Save Yes from exit, repeat save, clear/New and Doc 2 journeys remain incomplete. | WP79, WP82 |
| No native soft-wrap/Underline implementation or matched physical pagination; nonempty status prints `Pg -- Ln -- Pos --`. | WP80, WP81, WP84 |
| Up/Down, Home/End on physical lines, multiline Reveal and viewport behavior remain incomplete. | WP81, WP82, WP84 |
| F5 is a flat regular-file retrieve list; displayed file commands such as Look and Other Directory are not implemented. | WP79, WP84 |
| Many menus are stubs; F1 child text/focus differs from the newly observed original; original Help/settings and visible-bar preference persistence are absent. | WP85 |
| Search and contextual proofreading are not delivered in this candidate. | WP83, WP87–WP89 |
| Real original-native interoperability and complete uninterrupted everyday journeys remain unqualified. | WP78, WP86 |

The retrieved-Bold probe intentionally tests refusal conservation, not successful Bold editing. Future successful implementation must replace that bounded expectation with the approved everyday acceptance criterion, rather than retaining this as a global frozen limitation. This package does not freeze historical test expectations or prohibit future tests/source changes.

## Acceptance and independent handoff

EE-001 is addressed only for source identity, startup, key delivery through the selected PTY and retained basic editing. EE-013 is addressed only for exact first-save/retrieve and cancellation/refusal conservation tested here. Neither complete milestone requirement is marked satisfied. T229–T232 evidence is ready. T233 hands off the entire `f89a4862..c7f14fd4` source delta, approved WP90 repair/source-intake receipt and new WP77 retry diff for independent review, including fresh confirmation that R77-001 no longer reproduces. Approval is still required before consumers proceed. The report does not accept M1, close the everyday milestone or enable M2.
