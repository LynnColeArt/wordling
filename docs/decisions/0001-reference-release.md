# ADR 0001 — Primary WordPerfect reference release

Date: 2026-10-29. Status: selected documentary target; binary validation pending.
Applies to M1 `wp51-parity-01M64CVY`; implements C-005 and WL-004.

## Decision

Use **plain WordPerfect 5.1 for DOS, U.S. English, dated March 9, 1992** as the
primary behavioral reference. This is an engineering selection within the
confirmed plain-5.1 scope, not a claim that an installation has been acquired,
run, fingerprinted or accepted. The machine-readable identity is
`docs/research/reference-baseline.json`.

Keep older plain-5.1 fixtures and language-specific cases as compatibility
obligations. A U.S. reference provides one reproducible initial oracle; it does
not exclude other original character sets or language behavior from the inventory.

## Evidence and reasoning

The publisher's enhancement notice ENH51 explicitly documents changes dated
03/09/92, including List Files (PDF 18), bundled keyboard macros (PDF 21),
printing (PDF 35-36), and printer-definition tooling. It is primary evidence
that this is a real maintenance target and that matching only the version
number “5.1” is insufficient. The WPDOS chronology lists March 9, 1992 as the
latest date in its U.S. plain-5.1 sequence. The recommendation combines those
facts: use the latest documented maintenance target within the selected edition.
It is not a claim that we independently proved the absence of every later build.

| Candidate | Assessment |
| --- | --- |
| 1989-11-06 plain 5.1 | Useful historical fixture target, but predates documented changes our manuals describe. |
| 1991-05-31 plain 5.1 | Includes alignment/other improvements, but predates the March 1992 changes. |
| 1992-02-19 plain 5.1 | Near-final candidate, but the printing notice warns about matching program and printer-resource revisions. No benefit over choosing the March release. |
| **1992-03-09 plain 5.1, U.S. English** | **Selected**: the latest U.S. maintenance date in the chronology, supported by dated publisher change entries. |
| Later English/Hebrew 5.1 editions | Distinct language-specific reference profiles, not an interchangeable “newer English build.” Investigate separately when testing those features. |
| 5.1+ or Windows 5.1/5.2 | Outside the confirmed primary application baseline. Do not import their extra capabilities into M1 by assumption. |

Secondary chronology and edition context:
[WPDOS chronology](https://mendelson.org/wpdos/chronology.html).
Primary maintenance evidence:
[publisher enhancement notice](https://mendelson.org/wpdos/WP51ENHA.pdf#page=18).
All primary PDFs are checksum-pinned in sources.json; the chronology is a
discovery/edition aid and is not the authority for command semantics.

## Consequences for acceptance

- **End Centering/Alignment is M1**, even though the first 1989 release lacked
  it (ENH51 PDF 1; REF51 pp. 66, 203). New code behavior cannot be inferred from
  “works in early 5.1.”
- **Unsorted file-list mode is M1** (ENH51 PDF 18). Name Search is unavailable
  in this mode. This differs from the later 5.1+ additions described by the
  chronology; do not confuse disabling sorting with sorting by size/date/type.
- **Printer resources must be paired with the executable** (ENH51 PDF 35-36).
  A filename or program date alone does not establish a print oracle.
- The 1989 workbook needs WBC51 corrections. DOC51 and ENH51 provide dated
  corrections; do not rewrite the pinned manuals or their page locators.
- The reference PDF has 6/92 identification leaves and ends its index at 1029,
  while the hosting chronology describes a final 3/94 edition ending at 1029.
  Treat this as edition uncertainty; preserve the observed identifiers and hash.
  Do not assert that scan pagination uniquely identifies the printing.

## Reference installation acceptance procedure

1. Obtain original installation media/resources with recorded provenance. The
   repository does not bundle them. Do not use patched 5.1+, localized executables,
   or mixed resource packs as an implicit substitute.
2. Record the in-application displayed release date/version and capture the screen.
   Compare to file dates, but do not treat DOS timestamps alone as identity proof.
3. Hash every installed file used by tests, including executable, overlays, setup,
   printer definitions, fonts, dictionaries, keyboard/macros and language resources.
4. Record emulator/DOS versions and configuration, mounted filesystems, clock,
   keyboard layout, text/graphics mode and printer capture configuration.
5. Use a fresh copied profile for each case. Keep mutable setup and backup files
   out of the immutable master installation; hash starting fixture/profile state.
6. Run smoke scenarios for End C/A, unsorted List Files, ordinary retrieval/save,
   Reveal Codes, and original printer-language output. Capture screens and files.
7. Only then change `installation_status` from `not-acquired` to `fingerprinted`
   with evidence paths. Individual command scenarios remain unverified until run.

An emulator is a reference-test environment, not Wordling's implementation.
We have not selected an emulator or DOS distribution yet; those are reproducibility
decisions, not reasons to delay documentary scenario authoring.
