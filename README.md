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

Status: project charter and initial research/specification. **There is no working
editor yet, and no feature is claimed as compatible.**

Active mission on this branch: [WordPerfect 5.1 parity](kitty-specs/wp51-parity-01M64CVY/spec.md).

## Project documents

- [Charter](.kittify/charter/charter.md)
- [Mission roadmap](docs/roadmap.md)
- [Compatibility contract](docs/compatibility.md)
- [Research sources](docs/research/sources.md)
- [Feature inventory](docs/research/feature-inventory.md)
- [Initial findings](docs/research/findings.md)
- [Reference release decision](docs/decisions/0001-reference-release.md)
- [Command-level scenarios](docs/research/command-scenarios.md)
- [Scenario coverage](docs/research/scenario-coverage.md)
- [Workbook lesson map](docs/research/workbook-map.md)
- [Running DOS reference environment and observed smoke results](docs/research/reference-environment/README.md)

The structured charter at `.kittify/charter/charter.yaml` is the runtime governance
source and references the compatibility contract and roadmap.

## Development

The Go module is `github.com/lynncoleart/wordling`; Bubble Tea is pinned in
`go.mod` and `go.sum`. The application has not been implemented. Research tooling
uses Python 3 (standard library), curl, and Poppler's `pdftotext`.

```sh
./scripts/fetch-manuals.sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
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
