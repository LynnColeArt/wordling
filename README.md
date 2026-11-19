# Wordling 5.2

A faithful, independent reimplementation of **WordPerfect 5.1 for DOS**, for
Linux, written in **Go** with **Bubble Tea**.

Wordling 5.2 is the product name. It does **not** introduce a new document format:
native documents and companion artifacts retain their original WordPerfect
formats. No JSON, Markdown, ZIP, or proprietary Wordling wrapper replaces them.

## Two missions

1. **WordPerfect 5.1 parity.** Reproduce original workflows, editing and formatting
   semantics, native file behavior, automation, layout, utilities, and printing.
2. **Modern conveniences.** After parity acceptance, add PDF export and explicitly
   selected improvements while preserving compatibility and the classic workflow.

Status: a runnable Linux terminal editor implements bounded native editing,
formatting, tables, macros, merge, printing, and recovery workflows. Full
WordPerfect 5.1 parity remains open. Windows and macOS builds are currently
blocked by the Linux-only storage implementation.

The [current command audit](docs/research/mission-1-command-audit.md) records
verified, partial, and unimplemented workflows. The
[November 17 recovery and prerelease report](docs/reports/infra-recovery-2026-11-17.md)
records the synchronized source, fresh validation, and platform blockers.

[Historical conformance evidence](docs/conformance/v1/index.md) is a frozen WP31
checkpoint, not a verdict on the current editor. Its source guards deliberately
reject later specification and implementation changes. The research catalogues
below retain their original WP13 reference snapshot.

Active mission on this branch: [WordPerfect 5.1 parity](kitty-specs/wp51-parity-01M64CVY/spec.md).

## Project documents

- [Charter](.kittify/charter/charter.md)
- [Mission roadmap](docs/roadmap.md)
- [Compatibility contract](docs/compatibility.md)
- [Research sources](docs/research/sources.md)
- [Historical original-reference feature inventory (WP13 snapshot)](docs/research/feature-inventory.md)
- [Initial findings](docs/research/findings.md)
- [Reference release decision](docs/decisions/0001-reference-release.md)
- [Historical original-reference command scenarios (WP13 snapshot)](docs/research/command-scenarios.md)
- [Historical original-reference scenario coverage (WP13 snapshot)](docs/research/scenario-coverage.md)
- [Historical original-reference workbook map (WP13 snapshot)](docs/research/workbook-map.md)
- [Running DOS reference environment and observed smoke results](docs/research/reference-environment/README.md)

The structured charter at `.kittify/charter/charter.yaml` is the runtime governance
source and references the compatibility contract and roadmap.

## Development

The Go module is `github.com/lynncoleart/wordling`; Bubble Tea is pinned in
`go.mod` and `go.sum`. Build and regression checks use the Go toolchain. Research tooling
uses Python 3 (standard library), curl, and Poppler's `pdftotext`.

```sh
./scripts/fetch-manuals.sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
go build ./...
go test ./...
go vet ./...
```

Manual copies and extracted text stay in ignored `research/cache/`. The repository
contains source URLs, checksums, locators, and original research notes, rather than
redistributed manuals, proprietary application binaries, fonts, or dictionaries.

## License

Original project contributions are licensed under [Apache License 2.0](LICENSE).
Third-party dependencies retain their licenses. Referenced manuals and original
WordPerfect resources retain their owners' rights and are not covered by this
project's license. Wordling is an independent project with no claimed affiliation
with the owners of WordPerfect.
