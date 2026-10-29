# Research source register

Retrieved 2026-10-29. These are external references; PDFs and OCR text stay in
ignored `research/cache/` and are not redistributed by Wordling. `sources.json`
pins exact source bytes and editions for reproducible page citations.

## Primary sources

### REF51 — WordPerfect 5.1 for DOS Reference

- Source: [WPDOS51Reference.pdf](https://mendelson.org/wpdos/WPDOS51Reference.pdf)
- Edition: MNUS1WP51X1C-6/92 (copyright leaf; scan, OCR duplicated in places)
- PDF pages: 1048; bytes: 61124991
- SHA-256: `ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531`

### WB51 — WordPerfect 5.1 Workbook

- Source: [WPDOS51Workbook.pdf](https://mendelson.org/wpdos/WPDOS51Workbook.pdf)
- Edition: WKUS1WP51-11/89 (copyright leaf)
- PDF pages: 512; bytes: 28520554
- SHA-256: `868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d`

### SDK51 — WordPerfect Corporation Developer’s Toolkit

- Source: [WP51DevelopersToolkit.pdf](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf)
- Edition: MNUSXTW511-12/93; WP subsection carries intermediate revision marks
- PDF pages: 547; bytes: 1907150
- SHA-256: `5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754`

## Locator conventions

REF51 printed Arabic pages map to PDF page +17 in this scan; the contents are
PDF 42-46. SDK51 WP-section printed pages map to PDF page +13. These offsets
are specific to the pinned files; other SDK sections restart their numbering.
The WB51 contents are PDF 3-4. Roman front matter is cited by PDF page explicitly.

## Discovery aids and implementation documentation

- [WPDOS manual index](https://mendelson.org/wpdos/manuals.html): discovery and provenance context.
- [WPDOS utilities/SDK index](https://mendelson.org/wpdos/wpcsoftware.html): original toolkit and resource leads.
- [WPDOS version chronology](https://mendelson.org/wpdos/chronology.html): leads for release differences; verify against primary materials.
- [Bubble Tea upstream](https://github.com/charmbracelet/bubbletea): framework API and licensing.

Hosting indexes are secondary aids; product behavior is established from the
original documents and, ultimately, the original application. No emulator run,
executable acquisition, fixture validation, or full-manual study has occurred yet.

## Refresh and verification

Run `./scripts/fetch-manuals.sh`. Existing or downloaded files must match the
registered checksums before extraction. A mismatch requires investigating the
edition change; do not silently update hashes and reuse old page locators.

Source originals and OCR extractions are not included in the Apache-2.0 grant.
Summaries and scenarios here are independently authored, with locators for audit.
