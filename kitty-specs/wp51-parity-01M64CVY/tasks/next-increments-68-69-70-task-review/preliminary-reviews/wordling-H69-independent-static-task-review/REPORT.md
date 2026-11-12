# Preliminary H69 static task review

**Two actionable task-design findings. This is not a final combined-task verdict or canonical lifecycle decision.** Reviewed stable H69 revision2 task SHA56630d34e6d8ef0ef0bbbb2b1f59f8200596dc0bf7db70f371222281f1c98783, author root76885bf001a72d864299be549624a3cf47a6de6f3a43d2fe4229f202965d5ad5. The composed H69 task was byte-identical when checked. All27 author members plus root verified. No product import, tests, implementation, model run, current guard, canonical write or private-resource action occurred.

The proposed small display increment is feasible through existing H66 public source/span presentation and read-only View/State. Real row0/13/24 anchors, footer36+44, logical role/caret tests, independent non-witness fixtures and actual executable PTY acceptance are appropriate. The task, however, currently freezes assertions that intentionally describe the old geometry and leaves conflicting fallback/overlay rules.

## F1 — frozen old tests contradict required new anchors

H69's ownership/scope paragraph explicitly keeps every other H test unchanged. T207 simultaneously requires full `go test ./...` and the healthy80x25 original seven-gap anchor comparison at row13/caret row0. Approved H66 commit66a65d4b311d81ab2699c9725a24d77cea3e7271 proves a direct conflict:

- `internal/tui/runtime.go:69` constructs the public Open model at80x25.
- `internal/tui/model_test.go:60–98` supplies `testModel` and genuine Retrieve through actual IO delivery.
- `internal/tui/reveal_cursor_test.go:77–115` uses that real model, Retrieve and AltF3, then asserts lower content at row3 (:86) and caretY1 (:98) across all seven gaps. This is precisely the new admitted geometry; keeping these assertions byte-exact prevents row13/Y0.
- The same file's original-run comparison at :275/:293 reads both public original captures and explicitly requires current appY1 rather than originalY0. Other row3 extraction sites mix healthy and fallback contexts; changing every `3` to `13` would be wrong.
- `internal/tui/editable_test.go:73` requires the `bounded native editing` branding after a successful real save. The new task requires removal of implementation branding from that healthy content area. Its active Typeover assertions (:49–51) also matter to F2 below.

**Required task remediation:** explicitly own narrow amendments to the existing affected test files, with an exact preservation rule: replace only superseded healthy geometry/branding assumptions, preserve genuine command/reducer/native-byte/source-span/active-role/save/IO/history assertions, retain original-vs-host evidence distinctions and retain row3/Y1 fallback assertions where they still apply. New `reveal_anchors_test.go` supplements these tests; it cannot override them. Freeze all other tests/evidence and prohibit fixture/hash/path/test-name recognition. Do not waive required regression failures or globally rewrite rows.

## F2 — shown-menu and Typeover eligibility needs one explicit contract

T205 excludes a shown menu from the new anchor layout and requires the existing bounded fallback outside admission. Meanwhile T206 requires menu preservation. Approved `menu_bar_test.go:99–143` captures the pristine public View, shows the real Alt+= menu, requires all body rows and caret to remain exactly unchanged (:128), then hides and requires the entire prior frame/reducer/history/source/receipt state to restore. If healthy pre-show uses anchored row0 but shown menu selects old fallback row1, body/caret necessarily change. The current wording cannot simultaneously require both.

Choose and state the intended view composition before implementation. The narrow preservation-compatible approach is to select the pristine underlying base frame/anchor geometry, then overlay only the already-qualified menu row0 while preserving body/caret and real refusal/prompt precedence; hide restores the identical prior base. This is an explicit menu-overlay exception to a blanket shown-menu fallback rule, not a new action menu or expanded availability. Alternatively, an intentional geometry transition would require a separately explicit task decision and corresponding bounded test changes; it must not occur accidentally.

T205 also leaves Typeover eligible as ordinary Editing, while existing `editable_test.go:49–51` requires visible active Typeover state and T206 says Typeover contexts retain semantics. The old visible Typeover prefix sits in a diagnostic line the new layout removes. Explicitly exclude Typeover from healthy admission and preserve its current truthful fallback, or explicitly specify a source-backed visible indicator. Do not silently hide active mode information or infer a new ruler/status algorithm. ROOT has selected the narrower Typeover fallback direction for the forthcoming amendment; this report does not itself rewrite the task.

## Preserved source facts and remaining review

The source context shows `visibleFrame` already selects frozen DISPLAY OFF data before live native presentation, and `macroStart` captures that frame. Extending its owned `macroPane` to retain the chosen layout is feasible; resize clipping must not choose geometry or styles from a newer live gap. Current `legacyPanes` independently derives upper text width and lower label width, so the proposed caret rule requires no new native/editor API. Partial HR/HP/unknown inspection and unsupported sizes must keep truthful existing fallback. View/State must remain observations, never UI claims or source IO.

`input-verification.json` pins seven additional exact immutable approved Git files; `approved-source/` contains literal inert copies, and `test-geometry-search.stdout` narrows old assertion sites without executing them. This static counterexample is a source contradiction, not a claimed observed failing test. One initial overly broad read-only Git search included historical evidence and produced a truncated tool display; it was narrowed to actual test source. No product or evidence bytes were changed.

Final combined68/69/70 task review remains held until a separately sealed author packet with exact revised H69 body, complete E acceptance mapping, ownership/dependency model and current guard is dispatched by ROOT. No task IDs or code permission are reserved by this preliminary review. Full parity remains open.
