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

Status: bounded independently reviewed native-preservation and runnable no-edit
components exist, including the WP18 candidate `72369db`. Full original editing,
layout, utilities, resource and workflow parity remains open. No entire catalogue
scenario or feature family is claimed compatible by this tooling checkpoint.

[Current conformance evidence and remaining obligations](docs/conformance/v1/index.md)
is the current evidence authority. It retains all 38 obligations and 91 groups plus
discovered leaves/resources. The frozen research catalogues linked below describe
the approved original-reference snapshot at WP13 `18d6afe` (244 cases); embedded
present-tense unimplemented labels belong to that historical snapshot, not current
product verdicts. See [ADR 0004](docs/decisions/0004-conformance-evidence-layers.md).

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
`go.mod` and `go.sum`. The runnable application implements a bounded no-edit slice;
full M1 remains open. Research tooling
uses Python 3 (standard library), curl, and Poppler's `pdftotext`.

```sh
./scripts/fetch-manuals.sh
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
python3 scripts/conformance/v1/conformance.py check
python3 -m unittest discover -s tests/conformance/v1 -v
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
