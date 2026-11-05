# WP80 evidence — everyday document core

Status: **in progress.** T244 delivered; T245–T248 open. No parity or M1
acceptance claim. All statements below are backed by committed native witnesses
in this repository or by captured reference evidence named in place.

## Environment

- Root: `/home/lynn/projects/wordling`, lane `lane-e`,
  branch `kitty/mission-wp51-parity-01M64CVY-lane-e`.
- Commits: `cbe5976f` (T244a), `cadaa2ce` (T244b), `3d8bef1e` (T244c),
  `53c31bd9` (T244d).
- Gates after every commit: `gofmt -l`, `go build ./...`, `go vet ./...`,
  `go test ./...` — all clean, 12 packages.

## T244 — admit actual everyday native structures

### Observed native facts used

| Fact | Value | Source |
| --- | --- | --- |
| Soft return | one byte `0D` | `docs/research/everyday-contract-2026-11-05/REPORT.md:107` |
| Hard return | one byte `0A` | same, `:108` |
| Underline ON / OFF | `C3 0E C3` / `C4 0E C4` | same, `:109` |
| Bold ON / OFF | `C3 0C C3` / `C4 0C C4` | toolkit function 195/196, attribute 12 |
| Tab owner | 9 bytes, lead/trailer `C1`, mark `02` | `qualification/flow/files.json` body hex |
| Deleted soft return | one byte `90` | `WP78-REPORT.md:38`, `[DSRt]` screens |
| Hard page | one byte `0C` | toolkit single-byte table, function 12 |
| End of Page record | `D4` subfunction 0, declared length = owner − 4, group marker `00`, group length `16` | toolkit Format Group 212 |
| `8C` / `99` companions | combination hard return/soft page; dormant hard return | toolkit single-byte table, 140 / 153 |

Reveal labels used come from captured screens (`[SRt] [HRt] [UND] [und] [DSRt]`),
not from the manual. One label source now feeds both the presentation window and
the inspected catalogue, so the two views cannot disagree.

### Corpus result — 72 captured WP42 witnesses

Probe: `internal/document/evidence/everyday/admission_probe`, read-only, walks the
corpus through the public API.

| Family | Witnesses | Readable | Mutable | Note |
| --- | ---: | ---: | ---: | --- |
| Initial sources (324) | 12 | 12 | 12 | |
| Disabled resaves G1–G3, EDIT (324) | 24 | 24 | 24 | already admitted before this work |
| Disabled resave FIN (post-print) | 6 | 6 | 6 | admitted now |
| FastSave baseline (564) | 30 | 30 | **0** | blocked by WP42 |

All 72 witnesses are readable and Reveal-inspectable with **zero** opaque owners.

### Two fields widened, observed values only

- Packet 6 printer-select counter: `01` before print, `02` after. The original
  increments it on print; this package never writes it.
- Packet 15 descriptor match hash: `E7 24` in sources and resaves, `11 72` after
  a print rebuilds the printer cache. Earlier code allowed the second value only
  when packet order was not reordered; the corpus shows it follows the cache
  generation instead.

### Left refused, deliberately

The FastSave baseline family keeps its index-deleted 564 prefix. WP42's
resaved-prefix contract blocks it for writer admission because its four `FFFF`
extents can change across Retrieve/Save/print and are not proven
body-independent. Tests pin 30 mutable / 30 refused so neither side can drift
unnoticed.

### Declared gaps

1. **FastSave 564 family** — needs a research qualification of the `FFFF`
   extents, not a code change in this package.
2. **Reveal rendering of page owners** — no captured screen shows how the
   original draws the `D4` record or its `8C`/`99` companions, so they render as
   nothing in both views. Deliberate silence, not a claim.
3. **Executable reachability for these owners belongs to WP84.** The normal
   executable still answers `Unsupported document presentation` for a retrieved
   original containing everyday codes. Cause: `internal/tui/model.go:380-416`
   switches on the token kind and its `default` returns an error; the new kinds
   land there. This is **pre-existing behaviour, not a regression** — the same
   binary built before these commits produces the identical screen for the same
   files, because the owners were opaque and `Present` refused them. The WP80
   briefing forbids editing `internal/tui` to make a WP80 demonstration pass, so
   this is recorded rather than patched. WP84 owns the renderer.
4. **History fragment offsets** — `history.go` still assumes `index+2` per
   attribute boundary. Tab is 9 bytes and `D4` variable, so real per-token
   offsets are T246 work.

## Consumers named

| WP | Needs from this package |
| --- | --- |
| WP81 | typed page/attribute owners and revision-bound reflow adoption (T247) |
| WP82 | atomic edit/history results, correction distinct from delete+insert |
| WP84 | render the admitted kinds in normal and Reveal views (gap 3 above) |
| WP87/88 | native identities for proofreading; safe correction without new history |

## Guard-removal probes (run, not asserted)

Each new refusal was probed by disabling it and confirming a test reddens:

| Guard | Probe | Result |
| --- | --- | --- |
| Underline pair tracking | neutralised both ON/OFF cases | `TestEverydayAttributeRefusalsRetained` red; restored green |
| Page-record shape | group-length invariant AND → OR | `TestMalformedPageRecordRefused` red at group marker `1`; restored green |

The first duplicate-attribute test proved nothing until it was rewritten with
balanced duplicate pairs — the unterminated check had been carrying it. Recorded
because a test that cannot fail is not evidence.
