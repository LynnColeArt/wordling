# Bounded Mission 1 product-slice research

Research only, 2026-11-18. Examined pinned public Git source at `d7433153c28355a694dfb52c4adf100d0f9f71e1`; all selected live source/fixture bytes were independently compared with that pin and matched. No repository/index/runtime/Op/status/claim write, worktree, Go build/test, CI, Mac, VM, original/private-resource, TEST/P/CONTROL or reference action occurred. Only this report was written in /tmp. This is a planner/reviewer handoff, not implementation/adoption authority or a reserved WP.

## Decision

**No unconditional new implementation slice was established under the strict requirement for an already-approved exact fixture contract.** One genuine, useful product gap has a recorded public original native fixture and can be planned independently of WP108/104: **the observed default 2×2 A1:A2 vertical join, limited to native admission/creation and public UI reachability**. Its exact fixture contract must first be explicitly adopted/reviewed; this research did not find a prior approval specifically accepting vertical behavior. WP103 approves the index, expressly not product/reference qualification. Do not confuse the fixture's presence in an approved index with accepted compatibility evidence.

Recommend taking this one bounded proposal to the normal planner/reviewer at the next safe source checkpoint. If the existing VERT capture's provenance is judged insufficient for fixture adoption, obtain a fresh original vertical-join capture after the current reference route is qualified; do not invent an oracle. No second implementation slice is recommended from this bounded scan.

The underlying product gap is real and does not duplicate approved WP100/106/107/109/110. CMD51-121 remains partial. Current public command refuses the vertical selection, and current SimpleTable reader/encoder does not model vertical continuation owners. This is distinct from the new-unsaved macro rows, whose implementation is already approved in WP100 and whose remaining debt belongs to WP101/102 original qualification.

## One provisional task: exact recorded default vertical join

### Existing public evidence and independent expected behavior

- `docs/research/reference-runs/mission1-table-join/README.md:3–13` states the exact default 2×2 ALPHA/BETA/GAMMA/DELTA setup, Alt+F7 → Alt+F4 → Down → Join7, and native vertical behavior. A1 receives `ALPHA` + native HardReturn + `GAMMA`; B1/B2 retain BETA/DELTA; both rows remain; A2 has its continuation owner rather than being removed like the horizontal join's B1.
- `docs/research/reference-runs/mission1-table-join/replay-vertical.py:28–57` is the retained producer recipe. It is evidence to inspect, **not** a safe current runtime entry point or authority to execute.
- `VERT.WP`: 578 bytes, SHA256 `931405b0fc53018597a91cc10579def06140326cddb6f1ec60f6f9b4f2196777`; native body offset324, body254 bytes. It and the README/recipe entered tracked history in `fac7e7b0b26a37f445f3a47b1b035b890471c68e` (recovered source/capture custody). Read these bytes directly as expected output; do not derive them from the candidate encoder.
- Exact VERT cell-owner vectors, zero-based byte positions within each complete19-byte DC/0 frame: first A1 owner `dc000f0000000102000000000000200f0000dc` (byte7=02); continuation A2 owner `dc000f0000008101000000000000200f0000dc` (byte6=81). These are literal fixture facts; general meanings/other values must not be guessed from one case. Full row/end owner byte equality also matters, not only these two fields.
- Existing regression oracle: `ROWJOIN.WP` 567 bytes SHA256 `84d3da85b0d747b9f46be36a602ddb59bc27add7957ac5d61837d2f9bb8d31d2`, `ROWJOIN.PRN`229 bytes SHA256 `7a8a6ea2d803272db370796c555168bb49e92e014f618e6e13163b7837abd07f`. `internal/tui/table_join_test.go:11` already checks the native horizontal result, No path and covered-cell navigation. Keep that behavior unchanged.
- Governing documentary/native contracts: `contracts/structured-graphics.md:45` S03, REF51 printed651–664/PDF668–681 and SDK WP44–45,81–87/PDF57–58,94–100; `contracts/native-framing.md`, `editing.md`, `session.md`, `files-platform.md`, compatibility conservation rules. WP103's D2 row (`mission1-closeout-coverage.md:94`) correctly retains vertical/combined joins as pending native relationships.

### Current absent behavior, with source anchors

- `internal/document/table_join.go:28–32`: `JoinTableTopRow` admits only min(first,last)=0/max=1, exactly2columns/4cells; A1:A2 (0,2) returns an unchanged-document error.
- `internal/document/simple_table.go:89,250,312,376`: table profile encoder, reader, horizontal join recognition, and body producer only understand horizontal `joinedRight` plus an absent logical cell. SimpleTable validates exact regenerated owners; merely dropping its rejection would misclassify unmodeled vertical owner relationships.
- `internal/editor/simple_table.go:198`: sole session join consumer calls that bounded native API; `internal/tui/simple_table.go:344` is the real confirmation route. `simpleTableFrame:15`/`tableReveal:80` currently understand horizontal spanning only.
- `internal/document/simple_table.go:445`: existing editing of joined cells is explicitly refused. It must not become enabled accidentally by reader admission.
- `internal/layout/standard_print.go:320–334`: current Standard Printer profile refuses multiline cells. **There is no tracked vertical PRN in this fixture directory.** Do not broaden printing or claim full vertical parity from horizontal PRN or terminal geometry.

### Minimal provisional ownership and dependency boundary

Production owners likely required: `internal/document/simple_table.go`, `internal/document/table_join.go`, `internal/editor/simple_table.go`, `internal/tui/simple_table.go`. New focused native/session tests and a separate vertical public UI test; existing horizontal tests remain regressions. The planner should explicitly approve these actual owners; avoid a broad table refactor. No wp51 parser enum/framing change, original controllers, resource decoder, macro, storage platform, runtime-completion owner, reference capture or fullcoverage index change is indicated.

Dependency is the approved current table/native/session/public UI source baseline and an adopted exact VERT fixture contract, not WP108/104 and not the New-macro original route. Nevertheless source/index work cannot run in primary while Ivan owns it; implementation starts only at root's source checkpoint or later approved isolation.

Initial admitted operation should remain the exact observed geometry/default resources/plain single-line ASCII setup, A1:A2 only. Model the continuation relationship explicitly, round-trip it, and preserve every unrelated native/prefix/resource owner. Do not silently add B1:B2, arbitrary rectangles, more rows/columns, repeated joins/splits, combined-content editing, formulas, wrapping/overflow or printing. Those need their own contracts/evidence. Normal UI failure/refusal must remain truthful for unsupported operations.

### Meaningful RED-first validation for future implementation

No test was executed here. Future author must first commit tests that compile unchanged on pre-code baseline and fail for product behavior, not missing new types:

1. Load exact VERT through existing native public API and demand a usable SimpleTable vertical relation plus exact no-edit export. Current semantic admission should fail even though outer framing/no-edit preservation may already pass; separate those assertions so parser pass is not reported as the feature's RED.
2. Create the ordinary default2×2 table with the actual existing APIs, fill ALPHA/BETA/GAMMA/DELTA, place cursor A2, invoke existing public join API with first0, and expect successful exact254-byte VERT native body (plus independently preserved receiver prefix and documented format-flag update). Current code returns its specific top-cells-only refusal. Compare **all** row/cell/end owner bytes, not a reconstructed candidate expectation.
3. Drive the real public Model through table creation/editing, Alt+F7/Alt+F4/Down/7/Y and native export. Current native refusal is the causal RED. Confirm explicit No/cancel are nonmutating, errors never report success, source/other screen/history/name/dirty/save state follow existing contracts, and horizontal regression remains exact.
4. Stale/foreign cursor, malformed continuation/owner bytes, wrong geometry/formula/overflow, resource/prefix uncertainty and byte/token ceilings must fail atomically. Avoid admitting a vertical-shaped file solely because two bytes resemble VERT. Valid-but-unknown variants retain no-edit bytes and refuse unsupported editing.
5. Exact final tests later replay on frozen pre-code source. GREEN requires native reader/producer and real public route; prepared native output injection is not public integration. Run normal required Go/race/build/vet checks only when authorized as implementation work. Native fixture equality is not original reopen/print/physical qualification.

### Approval/qualification limits

This is a **substantive code gap with a recorded-original-fixture adoption question**, not qualification-only debt. The retained vertical recipe lacks current source/grant protocol and must not be run. No retained vertical print oracle or physical/focus/navigation witness was found. The proposed component can deliver useful native/UI behavior once its exact fixture contract is accepted, while later original reopen/edit/print/save and broader CMD51-121 remain pending. If normal governance requires new repeated native capture before authoring the reader/writer contract, the strict no-new-evidence implementation route is blocked until that capture exists.

## Why no second slice

The bounded scan found the obvious neighboring public fixtures already consumed by delivered code: custom relative/absolute/decimal tabs; table two-relative-operand addition/copy; one changed ASCII compare line/cleanup; single-column subtotal; paired Bold styles; short notes. Their READMEs explicitly leave broader branches open without corresponding original outputs. Generalizing these would manufacture native/layout/runtime contracts from the implementation. Thesaurus has `quick` lookup/cancel evidence but explicitly lacks an original THS decoder; a hardcoded synonym display would not implement the resource behavior. Split windows/keyboard selection/timed-backup exact semantics remain documentary/resource/original-evidence work. This scan is not an exhaustive absence claim about every remaining source leaf.

No canonical audit/matrix/244scenario/91group/36lesson/49family/38obligation status changes follow. Full Mission1 remains open.
