# WP05 manual and workbook coverage concordance

Audited research handoff, 2026-10-30, for the M1 planner, later workstream
researchers and reviewers. Requirements: FR-001, NFR-004, C-003/005/006.
This is a contents-level concordance, not an exhaustive command/lesson-step
inventory, a complete manual study or a parity verdict. Full original parity
remains M1; PDF remains optional M2. Proposals stay in this owned artifact;
WP12 owns new executable prompts and continuation-queue changes.

## Sources, scope and status rules

Exact editions and PDF SHA-256 values are pinned in the input ledger below and
`docs/research/sources.json`: REF51 MNUS1WP51X1C-6/92; WB51 WKUS1WP51-11/89;
SDK51 MNUSXTW511-12/93 with intermediate WP revision marks; publisher change
notices DOC51, WBC51 and ENH51 retain their internal dates. These later/earlier
publications are not interchangeable with the selected plain U.S. English DOS
executable dated 1992-03-09. Baseline and resource declarations are in
`docs/research/reference-baseline.json` and
`docs/research/reference-environment/environment.json` / `resource-profile.json`.
The original runs use FreeDOS and a July 1992 text-only printer, not historical
MS-DOS or general graphics/font metrics.

Printed and PDF pages are distinct; PDF numbers are **one-based**. REF51 Arabic
printed p maps to PDF p+17, WB51 Arabic p to PDF p+9. The toolkit's section
prefix is part of its printed locator: WP-1 and AP-1 are different places.
Every row records a start location, not an invented fully studied page range.
Reference features were checked against the **actual five contents pages**, PDF
42–46 (printed 25–29), including visual review where duplicate OCR obscures
headings or numbers. Counts per page are 45/48/48/48/13: 202 entries. Themes are
independently worded factual labels, not copied instructions.

The concordance includes 202 reference feature sections; frontmatter/startup
contents; all 20 REF51 appendices A–T; glossary/index; nine Appendix M menu
roots with their immediate/submenu research obligations; all 36 WB51 lessons,
its introduction, three appendix/index entries and final index; and all 126
section-coded SDK51 contents entries. Other toolkit products/platforms are
context or interface/resource leads; their inclusion does not assert those
applications' complete parity or that their fields occur in DOS documents.
Historical publisher offices/ordering/support context has an explicit source
context disposition, not an implemented application feature.

Status dimensions must remain independent:

- **Indexed (I):** source entry and stable locator identified. Every functional
  concordance row is indexed. This task examines contents and WB feature lists;
  it does not claim all prose, steps or fields have been studied.
- **Studied (S):** the inventory currently marks 87 groups studied and four
  indexed. Its own definition is selected passages studied, not every page or
  subcommand. Tables show S/I **parent-group** status; they never promote the
  entire referenced entry or lesson to studied. SDK FMT51-004/005/006 and
  WP51-081 remain indexed in that registry.
- **Observed (O):** 53 of 236 command scenarios have partial original-app
  observations; 183 are not-run. Tables report **related** observed command IDs,
  inherited only as research leads through associated groups. That association
  does not prove this chapter, menu leaf or workbook step was executed. No whole
  contents entry or lesson is marked behaviorally complete by this audit.
- **Uncovered (U):** all functional entries retain unenumerated subcommands,
  branches or numbered steps and missing differential acceptance. Every lesson
  remains **not run as a lesson**. Candidate cases are building blocks, not
  substitutes for the lesson. Existing implementation fields are not promoted.

R/X/WB/M/SDK identifiers below are local concordance row IDs, not new canonical
feature or scenario IDs. Each row links existing WP51/FMT51 groups and concrete
CMD51 examples. The complete candidate set is the union of those groups'
`command_scenario_ids` in the hash-pinned inventory. `+n` means further existing
IDs through that union, not unlisted successful tests. The machine ledger and
validator reproduce all links and statuses without guessing coverage percentages.

## Reference feature-section concordance

Columns: row, independently worded topic, REF51 printed/PDF start, parent IDs,
parent documentary status, example candidate cases, related partial observations.
`S` means all associated groups have selected studied passages; `S/I` is mixed;
`I` means their documentary status is indexed. All rows are I/U at entry level.
A dash in O means no related scenario is partially observed, not no requirement.

| Row | Topic | Printed / PDF | Parent groups | S | CMD51 candidate examples | Related O examples |
| --- | --- | --- | --- | --- | --- | --- |
| R001 | Vertical/absolute advance | 31 / 48 | WP51-038 | S | CMD51-107, CMD51-108 | — |
| R002 | Append to files | 34 / 51 | WP51-010 | S | CMD51-155, CMD51-156 | — |
| R003 | Character attributes | 36 / 53 | WP51-030 | S | CMD51-032, CMD51-090, CMD51-091 +1 | — |
| R004 | Original backups | 41 / 58 | WP51-021 | S | CMD51-071, CMD51-072, CMD51-073 +1 | — |
| R005 | Timed backups | 43 / 60 | WP51-021 | S | CMD51-071, CMD51-072, CMD51-073 +1 | — |
| R006 | Audible signals | 45 / 62 | WP51-077 | S | CMD51-188 | — |
| R007 | Binding offsets | 46 / 63 | WP51-091 | S | CMD51-114 | — |
| R008 | Define blocks | 48 / 65 | WP51-009 | S | CMD51-027, CMD51-028, CMD51-029 +8 | CMD51-028, CMD51-202, CMD51-203 +1 |
| R009 | Protect blocks | 51 / 68 | WP51-009, WP51-042 | S | CMD51-027, CMD51-028, CMD51-029 +9 | CMD51-028, CMD51-202, CMD51-203 +1 |
| R010 | Cancel | 55 / 72 | WP51-007 | S | CMD51-002, CMD51-005, CMD51-006 | CMD51-005 |
| R011 | Capitalization | 56 / 73 | WP51-015 | S | CMD51-063, CMD51-064 | — |
| R012 | Cartridge/font/print-wheel resources | 57 / 74 | WP51-073 | S | CMD51-187 | — |
| R013 | Center a page | 63 / 80 | WP51-034 | S | CMD51-094, CMD51-095, CMD51-096 +4 | — |
| R014 | Center text | 65 / 82 | WP51-034 | S | CMD51-094, CMD51-095, CMD51-096 +4 | — |
| R015 | Screen colors/fonts/attributes | 68 / 85 | WP51-005 | S | CMD51-154 | — |
| R016 | Display columns | 74 / 91 | WP51-005, WP51-043 | S | CMD51-154, CMD51-168, CMD51-169 | — |
| R017 | Newspaper columns | 75 / 92 | WP51-043 | S | CMD51-168, CMD51-169 | — |
| R018 | Parallel columns | 79 / 96 | WP51-043 | S | CMD51-168, CMD51-169 | — |
| R019 | Compose characters | 84 / 101 | WP51-066 | S | CMD51-138 | — |
| R020 | Conditional page ending | 88 / 105 | WP51-040 | S | CMD51-112, CMD51-113 | — |
| R021 | Conversion utility | 89 / 106 | WP51-079 | S | CMD51-190 | — |
| R022 | Cross-references | 96 / 113 | WP51-089 | S | CMD51-129, CMD51-130 | — |
| R023 | Cursor movement | 103 / 120 | WP51-008 | S | CMD51-011, CMD51-012, CMD51-013 +14 | — |
| R024 | Cursor utility | 105 / 122 | WP51-079 | S | CMD51-190 | — |
| R025 | Cursor speed | 107 / 124 | WP51-079 | S | CMD51-190 | — |
| R026 | Dates | 109 / 126 | WP51-054 | S | CMD51-127, CMD51-128 | — |
| R027 | Code deletion | 112 / 129 | WP51-011, WP51-013 | S | CMD51-030, CMD51-031, CMD51-034 +21 | CMD51-043, CMD51-045, CMD51-048 +8 |
| R028 | File deletion | 114 / 131 | WP51-023 | S | CMD51-076, CMD51-077, CMD51-078 +3 | — |
| R029 | Text deletion | 115 / 132 | WP51-011 | S | CMD51-030, CMD51-031, CMD51-034 +19 | CMD51-043, CMD51-045, CMD51-050 +7 |
| R030 | Directories | 117 / 134 | WP51-023 | S | CMD51-076, CMD51-077, CMD51-078 +3 | — |
| R031 | Display pitch | 120 / 137 | WP51-005 | S | CMD51-154 | — |
| R032 | Display setup | 122 / 139 | WP51-005, WP51-077 | S | CMD51-154, CMD51-188 | — |
| R033 | Document comments | 124 / 141 | WP51-027 | S | CMD51-158, CMD51-159 | — |
| R034 | Document comparison | 127 / 144 | WP51-027 | S | CMD51-158, CMD51-159 | — |
| R035 | 4.2 to 5.1 conversion | 130 / 147 | WP51-026 | S | CMD51-157 | — |
| R036 | 5.1 to 4.2 conversion | 138 / 155 | WP51-026 | S | CMD51-157 | — |
| R037 | Document format | 143 / 160 | WP51-032 | S | CMD51-093 | — |
| R038 | Document summaries | 145 / 162 | WP51-090 | S | CMD51-088, CMD51-089 | — |
| R039 | DOS interactions | 150 / 167 | WP51-078 | S | CMD51-189 | — |
| R040 | Edit-screen choices | 157 / 174 | WP51-005, WP51-077 | S | CMD51-154, CMD51-188 | — |
| R041 | Environment setup | 159 / 176 | WP51-077 | S | CMD51-188 | — |
| R042 | Equation editing | 163 / 180 | WP51-058 | S | CMD51-177 | — |
| R043 | Equation commands/symbols | 174 / 191 | WP51-058 | S | CMD51-177 | — |
| R044 | Equation syntax | 184 / 201 | WP51-058 | S | CMD51-177 | — |
| R045 | Exit decisions | 194 / 211 | WP51-029 | S | CMD51-087 | — |
| R046 | Fast Save | 197 / 214 | WP51-022 | S | CMD51-075 | — |
| R047 | Find files/documents | 197 / 214 | WP51-028 | S | CMD51-085, CMD51-086 | — |
| R048 | Find conditions | 201 / 218 | WP51-028 | S | CMD51-085, CMD51-086 | — |
| R049 | Flush right | 203 / 220 | WP51-034 | S | CMD51-094, CMD51-095, CMD51-096 +4 | — |
| R050 | Font choice | 205 / 222 | WP51-031 | S | CMD51-160, CMD51-161 | — |
| R051 | Footnotes/endnotes | 209 / 226 | WP51-045 | S | CMD51-115, CMD51-116, CMD51-117 | — |
| R052 | Note options | 215 / 232 | WP51-045 | S | CMD51-115, CMD51-116, CMD51-117 | — |
| R053 | Odd/even page forcing | 217 / 234 | WP51-040, WP51-091 | S | CMD51-112, CMD51-113, CMD51-114 | — |
| R054 | Format menus | 218 / 235 | WP51-033 | S | CMD51-162, CMD51-163 | — |
| R055 | Generate references | 221 / 238 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R056 | Go To | 224 / 241 | WP51-008 | S | CMD51-011, CMD51-012, CMD51-013 +14 | — |
| R057 | Go to DOS | 225 / 242 | WP51-078 | S | CMD51-189 | — |
| R058 | Go to Shell | 226 / 243 | WP51-078 | S | CMD51-189 | — |
| R059 | Graphics conversion utility | 228 / 245 | WP51-056 | S | CMD51-175 | — |
| R060 | Create graphics | 232 / 249 | WP51-055 | S | CMD51-174 | — |
| R061 | Define graphics boxes | 235 / 252 | WP51-055 | S | CMD51-174 | — |
| R062 | Edit graphics | 246 / 263 | WP51-055 | S | CMD51-174 | — |
| R063 | Graphics formats/programs | 251 / 268 | WP51-056 | S | CMD51-175 | — |
| R064 | Graphic lines | 257 / 274 | WP51-057 | S | CMD51-176 | — |
| R065 | Graphics options | 261 / 278 | WP51-057 | S | CMD51-176 | — |
| R066 | Graphics display modes | 266 / 283 | WP51-005, WP51-057 | S | CMD51-154, CMD51-176 | — |
| R067 | Hard spaces | 269 / 286 | WP51-016 | S | CMD51-110, CMD51-111 | — |
| R068 | Headers/footers | 269 / 286 | WP51-044 | S | CMD51-170 | — |
| R069 | Help | 275 / 292 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| R070 | Hyphenation | 277 / 294 | WP51-039 | S | CMD51-109 | — |
| R071 | Hyphenation zones | 281 / 298 | WP51-039 | S | CMD51-109 | — |
| R072 | Indentation | 285 / 302 | WP51-034 | S | CMD51-094, CMD51-095, CMD51-096 +4 | — |
| R073 | Indexing | 287 / 304 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R074 | Index concordance/marks | 288 / 305 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R075 | Index definitions | 291 / 308 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R076 | Document initial codes | 292 / 309 | WP51-032 | S | CMD51-093 | — |
| R077 | Application initial settings | 295 / 312 | WP51-032 | S | CMD51-093 | — |
| R078 | Justification | 299 / 316 | WP51-034 | S | CMD51-094, CMD51-095, CMD51-096 +4 | — |
| R079 | Kerning | 303 / 320 | WP51-031 | S | CMD51-160, CMD51-161 | — |
| R080 | Keyboard layouts | 304 / 321 | WP51-003 | S | CMD51-009, CMD51-010 | — |
| R081 | Edit keyboard layouts | 308 / 325 | WP51-003 | S | CMD51-009, CMD51-010 | — |
| R082 | Map keyboard layouts | 313 / 330 | WP51-003 | S | CMD51-009, CMD51-010 | — |
| R083 | Labels | 319 / 336 | WP51-053 | S | CMD51-173 | — |
| R084 | Language selection | 328 / 345 | WP51-067 | S | CMD51-181 | — |
| R085 | Language resource files | 331 / 348 | WP51-067 | S | CMD51-181 | — |
| R086 | Text line drawing | 337 / 354 | WP51-017 | S | CMD51-142, CMD51-143 | — |
| R087 | Line format | 339 / 356 | WP51-033 | S | CMD51-162, CMD51-163 | — |
| R088 | Line height | 341 / 358 | WP51-036 | S | CMD51-104, CMD51-105, CMD51-106 | — |
| R089 | Line numbering | 344 / 361 | WP51-036 | S | CMD51-104, CMD51-105, CMD51-106 | — |
| R090 | Line spacing | 346 / 363 | WP51-036 | S | CMD51-104, CMD51-105, CMD51-106 | — |
| R091 | File lists | 347 / 364 | WP51-023 | S | CMD51-076, CMD51-077, CMD51-078 +3 | — |
| R092 | Generated lists | 355 / 372 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R093 | List definitions | 356 / 373 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R094 | List text marks | 357 / 374 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R095 | Resource file locations | 358 / 375 | WP51-023 | S | CMD51-076, CMD51-077, CMD51-078 +3 | — |
| R096 | Password-locked documents | 362 / 379 | WP51-024 | S | CMD51-082 | — |
| R097 | Document look | 364 / 381 | WP51-028 | S | CMD51-085, CMD51-086 | — |
| R098 | Macros overview | 369 / 386 | WP51-059 | S | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 |
| R099 | Macro conversion utility | 370 / 387 | WP51-061 | S | CMD51-179 | — |
| R100 | Define macros | 373 / 390 | WP51-059 | S | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 |
| R101 | Execute macros | 378 / 395 | WP51-059 | S | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 |
| R102 | International macro interface | 379 / 396 | WP51-059 | S | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 |
| R103 | Macro editor | 380 / 397 | WP51-059 | S | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 |
| R104 | Macro message display | 386 / 403 | WP51-059 | S | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 |
| R105 | Left/right margins | 394 / 411 | WP51-033 | S | CMD51-162, CMD51-163 | — |
| R106 | Top/bottom margins | 396 / 413 | WP51-033 | S | CMD51-162, CMD51-163 | — |
| R107 | Master documents | 397 / 414 | WP51-052 | S | CMD51-126 | — |
| R108 | Column math | 401 / 418 | WP51-064 | S | CMD51-180 | — |
| R109 | Math column definitions | 405 / 422 | WP51-064 | S | CMD51-180 | — |
| R110 | Math formulas | 408 / 425 | WP51-064 | S | CMD51-180 | — |
| R111 | Math row labels/numbers/functions | 412 / 429 | WP51-064 | S | CMD51-180 | — |
| R112 | Memory | 415 / 432 | WP51-080 | S | CMD51-191 | — |
| R113 | Menu option entry | 418 / 435 | WP51-001, WP51-062 | S | CMD51-001, CMD51-002, CMD51-134 +14 | CMD51-001, CMD51-134, CMD51-207 +13 |
| R114 | Merges | 420 / 437 | WP51-062 | S | CMD51-134, CMD51-207, CMD51-208 +12 | CMD51-134, CMD51-207, CMD51-208 +12 |
| R115 | Mouse setup | 431 / 448 | WP51-004 | S | CMD51-153 | — |
| R116 | Mouse interactions | 434 / 451 | WP51-004 | S | CMD51-153 | — |
| R117 | Mouse type | 438 / 455 | WP51-004 | S | CMD51-153 | — |
| R118 | Move content | 441 / 458 | WP51-010 | S | CMD51-155, CMD51-156 | — |
| R119 | Move blocks | 443 / 460 | WP51-010 | S | CMD51-155, CMD51-156 | — |
| R120 | Other Format menu | 449 / 466 | WP51-047 | S | CMD51-171 | — |
| R121 | Create outlines | 451 / 468 | WP51-047 | S | CMD51-171 | — |
| R122 | Define outlines | 458 / 475 | WP51-047 | S | CMD51-171 | — |
| R123 | Outline styles | 464 / 481 | WP51-047 | S | CMD51-171 | — |
| R124 | Overstrike | 469 / 486 | WP51-030 | S | CMD51-032, CMD51-090, CMD51-091 +1 | — |
| R125 | Hard/soft pages | 471 / 488 | WP51-040 | S | CMD51-112, CMD51-113 | — |
| R126 | Page format | 473 / 490 | WP51-033 | S | CMD51-162, CMD51-163 | — |
| R127 | Page numbering | 474 / 491 | WP51-041 | S | CMD51-165, CMD51-166 | — |
| R128 | Paper definitions | 478 / 495 | WP51-041 | S | CMD51-165, CMD51-166 | — |
| R129 | Paragraph numbering | 487 / 504 | WP51-047 | S | CMD51-171 | — |
| R130 | Print documents on disk | 490 / 507 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R131 | Print current document | 493 / 510 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R132 | Print color | 495 / 512 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R133 | Cancel print jobs | 496 / 513 | WP51-075 | S | CMD51-148 | — |
| R134 | Display print jobs | 498 / 515 | WP51-075 | S | CMD51-148 | — |
| R135 | Rush print jobs | 499 / 516 | WP51-075 | S | CMD51-148 | — |
| R136 | Print options | 500 / 517 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R137 | Print quality | 502 / 519 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R138 | Edit printers | 504 / 521 | WP51-071 | S | CMD51-185 | — |
| R139 | Select printers | 506 / 523 | WP51-071 | S | CMD51-185 | — |
| R140 | Printer commands | 510 / 527 | WP51-072 | S | CMD51-186 | — |
| R141 | Printer control | 512 / 529 | WP51-072 | S | CMD51-186 | — |
| R142 | Printer functions | 514 / 531 | WP51-072 | S | CMD51-186 | — |
| R143 | Printer-definition utility | 518 / 535 | WP51-073 | S | CMD51-187 | — |
| R144 | AutoFont utility choices | 525 / 542 | WP51-073 | S | CMD51-187 | — |
| R145 | Substitute-font customization | 528 / 545 | WP51-073 | S | CMD51-187 | — |
| R146 | Automatic font changes | 531 / 548 | WP51-073 | S | CMD51-187 | — |
| R147 | General printing | 533 / 550 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R148 | Landscape printing | 539 / 556 | WP51-070 | S | CMD51-183, CMD51-184 | — |
| R149 | Stop printing | 542 / 559 | WP51-070, WP51-075 | S | CMD51-148, CMD51-183, CMD51-184 | — |
| R150 | Print to disk | 543 / 560 | WP51-074 | S | CMD51-145 | — |
| R151 | Pull-down menu interaction | 544 / 561 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| R152 | Redline/strikeout | 549 / 566 | WP51-030 | S | CMD51-032, CMD51-090, CMD51-091 +1 | — |
| R153 | Repeat values | 550 / 567 | WP51-007, WP51-015 | S | CMD51-002, CMD51-005, CMD51-006 +2 | CMD51-005 |
| R154 | Replace | 551 / 568 | WP51-014 | S | CMD51-052, CMD51-053, CMD51-054 +8 | — |
| R155 | Retrieve documents | 554 / 571 | WP51-019 | S | CMD51-065 | — |
| R156 | Hard/soft returns | 557 / 574 | WP51-016 | S | CMD51-110, CMD51-111 | — |
| R157 | Reveal Codes | 560 / 577 | WP51-013 | S | CMD51-048, CMD51-049, CMD51-050 +6 | CMD51-048, CMD51-050, CMD51-051 +5 |
| R158 | Rewrite/reformat | 563 / 580 | WP51-018 | S | CMD51-144 | — |
| R159 | Save | 565 / 582 | WP51-020 | S | CMD51-066, CMD51-067, CMD51-068 +6 | CMD51-066, CMD51-067 |
| R160 | Screen choice | 567 / 584 | WP51-005 | S | CMD51-154 | — |
| R161 | Screen-capture utility | 567 / 584 | WP51-079 | S | CMD51-190 | — |
| R162 | Search | 571 / 588 | WP51-014 | S | CMD51-052, CMD51-053, CMD51-054 +8 | — |
| R163 | Setup | 574 / 591 | WP51-077 | S | CMD51-188 | — |
| R164 | Sheet feeders | 576 / 593 | WP51-075 | S | CMD51-148 | — |
| R165 | Sort | 577 / 594 | WP51-063 | S | CMD51-135 | — |
| R166 | Sort keys | 583 / 600 | WP51-063 | S | CMD51-135 | — |
| R167 | Select sort records | 585 / 602 | WP51-063 | S | CMD51-135 | — |
| R168 | Spelling checks | 587 / 604 | WP51-068 | S | CMD51-139, CMD51-140, CMD51-141 | — |
| R169 | Dictionaries | 595 / 612 | WP51-068 | S | CMD51-139, CMD51-140, CMD51-141 | — |
| R170 | Word lookup | 598 / 615 | WP51-068 | S | CMD51-139, CMD51-140, CMD51-141 | — |
| R171 | Word counts | 599 / 616 | WP51-068 | S | CMD51-139, CMD51-140, CMD51-141 | — |
| R172 | Speller utility | 600 / 617 | WP51-068 | S | CMD51-139, CMD51-140, CMD51-141 | — |
| R173 | Spreadsheet import/link | 606 / 623 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| R174 | Spreadsheet link choices | 615 / 632 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| R175 | Styles | 616 / 633 | WP51-046 | S | CMD51-118, CMD51-119 | — |
| R176 | Create styles | 621 / 638 | WP51-046 | S | CMD51-118, CMD51-119 | — |
| R177 | Suppress page features | 626 / 643 | WP51-044 | S | CMD51-170 | — |
| R178 | Switch documents | 628 / 645 | WP51-006 | S | CMD51-007, CMD51-008 | — |
| R179 | Tabs | 631 / 648 | WP51-035 | S | CMD51-101, CMD51-102, CMD51-103 | — |
| R180 | Tab alignment | 633 / 650 | WP51-035 | S | CMD51-101, CMD51-102, CMD51-103 | — |
| R181 | Tab definitions | 634 / 651 | WP51-035 | S | CMD51-101, CMD51-102, CMD51-103 | — |
| R182 | Create tables | 640 / 657 | WP51-048 | S | CMD51-120, CMD51-121 | — |
| R183 | Edit table structure | 651 / 668 | WP51-048 | S | CMD51-120, CMD51-121 | — |
| R184 | Table cell/column formatting | 665 / 682 | WP51-049 | S | CMD51-122, CMD51-123 | — |
| R185 | Table math | 670 / 687 | WP51-049 | S | CMD51-122, CMD51-123 | — |
| R186 | Authorities tables | 676 / 693 | WP51-051 | S | CMD51-172 | — |
| R187 | Authorities definitions | 677 / 694 | WP51-051 | S | CMD51-172 | — |
| R188 | Authorities marks | 679 / 696 | WP51-051 | S | CMD51-172 | — |
| R189 | Contents tables | 682 / 699 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R190 | Contents definitions | 683 / 700 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R191 | Contents marks | 685 / 702 | WP51-050 | S | CMD51-124, CMD51-125 | — |
| R192 | Text input/output | 685 / 702 | WP51-025 | S | CMD51-083, CMD51-084 | — |
| R193 | Text display type | 689 / 706 | WP51-005 | S | CMD51-154 | — |
| R194 | Thesaurus | 692 / 709 | WP51-069 | S | CMD51-182 | — |
| R195 | Typeover | 695 / 712 | WP51-012 | S | CMD51-046, CMD51-047 | CMD51-046 |
| R196 | Undelete | 697 / 714 | WP51-011 | S | CMD51-030, CMD51-031, CMD51-034 +19 | CMD51-043, CMD51-045, CMD51-050 +7 |
| R197 | Measurement units | 698 / 715 | WP51-037 | S | CMD51-164 | — |
| R198 | Document preview | 701 / 718 | WP51-076 | S | CMD51-146, CMD51-147 | — |
| R199 | Preview choices | 702 / 719 | WP51-076 | S | CMD51-146, CMD51-147 | — |
| R200 | Widow/orphan control | 705 / 722 | WP51-042 | S | CMD51-167 | — |
| R201 | Windows | 706 / 723 | WP51-006 | S | CMD51-007, CMD51-008 | — |
| R202 | Word/letter spacing | 708 / 725 | WP51-037 | S | CMD51-164 | — |

## Other reference/workbook contents entries

X rows distinguish frontmatter, appendix and index entries in the machine ledger.
All 20 REF51 appendices retain their separate letter/topic dispositions; a broad
parent does not establish every appendix command/table is covered. Roman folios
are preserved. Context rows retain historical source information only.

| Row | Topic | Printed / PDF | Parent groups | S | CMD51 candidate examples | Related O examples |
| --- | --- | --- | --- | --- | --- | --- |
| X001 | Basics parent section | 3 / 20 | WP51-001, WP51-079 | S | CMD51-001, CMD51-002, CMD51-190 | CMD51-001 |
| X002 | Registration | 3 / 20 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X003 | Installation | 3 / 20 | WP51-079, WP51-080 | S | CMD51-190, CMD51-191 | — |
| X004 | Keyboard template | 5 / 22 | WP51-001, WP51-003 | S | CMD51-001, CMD51-002, CMD51-009 +1 | CMD51-001 |
| X005 | Program startup | 6 / 23 | WP51-080 | S | CMD51-191 | — |
| X006 | Clean screen | 8 / 25 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X007 | Known keys | 8 / 25 | WP51-001, WP51-003 | S | CMD51-001, CMD51-002, CMD51-009 +1 | CMD51-001 |
| X008 | Function keys | 9 / 26 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X009 | Pull-down menus introduction | 10 / 27 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X010 | Menu option entry introduction | 11 / 28 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X011 | Codes introduction | 11 / 28 | WP51-013 | S | CMD51-048, CMD51-049, CMD51-050 +6 | CMD51-048, CMD51-050, CMD51-051 +5 |
| X012 | Exit introduction | 11 / 28 | WP51-029 | S | CMD51-087 | — |
| X013 | Help introduction | 12 / 29 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| X014 | Help feature | 12 / 29 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| X015 | Using the reference manual | 12 / 29 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| X016 | Using the workbook | 12 / 29 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| X017 | On-line tutorial | 12 / 29 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| X018 | Customer support context | 14 / 31 | WP51-002 | S | CMD51-003, CMD51-004 | CMD51-004 |
| X019 | Ordering templates context | 17 / 34 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X020 | Brief introductory exercise | 18 / 35 | WP51-001, WP51-008, WP51-019, WP51-020 | S | CMD51-001, CMD51-002, CMD51-011 +26 | CMD51-001, CMD51-066, CMD51-067 |
| X021 | Alphabetical feature contents | 25 / 42 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X022 | Alphabetical reference parent section | 31 / 48 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X023 | Appendix contents index | 713 / 730 | WP51-082 | S | CMD51-193 | — |
| X024 | A: ASCII conversion chart | 715 / 732 | WP51-025, WP51-082 | S | CMD51-083, CMD51-084, CMD51-193 | — |
| X025 | B: Graphics image reference | 721 / 738 | WP51-055, WP51-056, WP51-082 | S | CMD51-174, CMD51-175, CMD51-193 | — |
| X026 | C: Code reference | 725 / 742 | WP51-013, WP51-082 | S | CMD51-048, CMD51-049, CMD51-050 +7 | CMD51-048, CMD51-050, CMD51-051 +5 |
| X027 | D: Equation palette | 729 / 746 | WP51-058 | S | CMD51-177 | — |
| X028 | E: Error messages | 741 / 758 | WP51-082 | S | CMD51-193 | — |
| X029 | F: Font programs | 763 / 780 | WP51-073 | S | CMD51-187 | — |
| X030 | G: Initial settings reference | 765 / 782 | WP51-032, WP51-082 | S | CMD51-093, CMD51-193 | — |
| X031 | H: Keyboard reference | 769 / 786 | WP51-003, WP51-082 | S | CMD51-009, CMD51-010, CMD51-193 | — |
| X032 | I: Macro/merge comparison | 777 / 794 | WP51-060, WP51-062 | S | CMD51-134, CMD51-178, CMD51-205 +30 | CMD51-134, CMD51-178, CMD51-205 +30 |
| X033 | J: Macro/merge expressions | 783 / 800 | WP51-060, WP51-062 | S | CMD51-134, CMD51-178, CMD51-205 +30 | CMD51-134, CMD51-178, CMD51-205 +30 |
| X034 | K: Programming commands | 791 / 808 | WP51-060, WP51-062 | S | CMD51-134, CMD51-178, CMD51-205 +30 | CMD51-134, CMD51-178, CMD51-205 +30 |
| X035 | L: Macro/merge variables | 887 / 904 | WP51-060, WP51-062 | S | CMD51-134, CMD51-178, CMD51-205 +30 | CMD51-134, CMD51-178, CMD51-205 +30 |
| X036 | M: Pull-down menu reference | 893 / 910 | WP51-001, WP51-082 | S | CMD51-001, CMD51-002, CMD51-193 | CMD51-001 |
| X037 | N: Startup options | 897 / 914 | WP51-080 | S | CMD51-191 | — |
| X038 | O: Troubleshooting | 905 / 922 | WP51-082, WP51-078, WP51-080 | S | CMD51-189, CMD51-191, CMD51-193 | — |
| X039 | P: Character identities | 913 / 930 | WP51-066 | S | CMD51-138 | — |
| X040 | Q: WordPerfect files | 921 / 938 | WP51-081 | I | CMD51-192 | — |
| X041 | R: Networking | 931 / 948 | WP51-081 | I | CMD51-192 | — |
| X042 | S: PIF integration | 961 / 978 | WP51-078, WP51-080, WP51-081 | S/I | CMD51-189, CMD51-191, CMD51-192 | — |
| X043 | T: Macro/merge value tables | 963 / 980 | WP51-060, WP51-062 | S | CMD51-134, CMD51-178, CMD51-205 +30 | CMD51-134, CMD51-178, CMD51-205 +30 |
| X044 | Glossary and index | 987 / 1004 | WP51-082 | S | CMD51-193 | — |
| X045 | Introduction: learning directory and prerequisites | v / 6 | WP51-023, WP51-071, WP51-076, WP51-079 | S | CMD51-076, CMD51-077, CMD51-078 +7 | — |
| X046 | Alphabetical feature list | 475 / 484 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X047 | Feature list by lesson (Appendix B in body) | 478 / 487 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| X048 | Two-disk-drive setup | 482 / 491 | WP51-023, WP51-080 | S | CMD51-076, CMD51-077, CMD51-078 +4 | — |
| X049 | Index | 487 / 496 | WP51-001 | S | CMD51-001, CMD51-002 | CMD51-001 |
| RF01 | Product/platform catalogue | iii / 6 | context | context | — | — |
| RF02 | International offices | v / 8 | context | context | — | — |
| RF03 | Distributor offices | ix / 12 | context | context | — | — |
| RF04 | Toolkit ordering context | xiii / 16 | context | context | — | — |

## Workbook: all 36 lessons

Starts were reconciled with WB51 contents PDF 4–5. **Every row remains thematic/feature-list study only, numbered steps unmapped, lesson not-run.** Parent leads below use the workbook’s own Appendix B feature list (printed478–481 / PDF487–490), rather than treating the older `workbook-map.md` associations as complete. Related observed cases do not change the not-run lesson status. WBC51 correction pages are notice-PDF pages and may contain several entries; no correction is silently transplanted between editions.

| Lesson | Theme; WB51 printed/PDF start | Corrected parent leads | Candidate CMD51 examples | Related O examples | WBC51 PDF | Uncovered step/topic work; follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Basic text entry; 3 / 12 | WP51-015, WP51-008, WP51-029, WP51-070, WP51-016, WP51-020, WP51-076 | CMD51-011, CMD51-012, CMD51-013 +32 | CMD51-066, CMD51-067 | none indexed | Capitalization; cursor movement; exit; print; returns; save; preview; numbered step mapping/input/output/resource reconciliation missing; F-WB1 |
| 2 | Draft a letter; 6 / 15 | WP51-015, WP51-008, WP51-029, WP51-034, WP51-023, WP51-018, WP51-020, WP51-012 | CMD51-011, CMD51-012, CMD51-013 +42 | CMD51-046, CMD51-066, CMD51-067 | 1, 2 | Capitalization; cursor movement; exit; justification; file list; rewrite; save; typeover; numbered step mapping/input/output/resource reconciliation missing; F-WB1 |
| 3 | Reusable memo form; 12 / 21 | WP51-030, WP51-034, WP51-054, WP51-033, WP51-007, WP51-013, WP51-035 | CMD51-002, CMD51-005, CMD51-006 +27 | CMD51-005, CMD51-048, CMD51-050 +6 | none indexed | Attributes; page/text centering; dates; format/margins; repeat; Reveal Codes; tabs; numbered step mapping/input/output/resource reconciliation missing; F-WB1 |
| 4 | Revise a letter; 16 / 25 | WP51-009, WP51-034, WP51-008, WP51-011, WP51-033, WP51-023, WP51-028, WP51-010, WP51-070, WP51-019, WP51-013, WP51-020, WP51-035, WP51-012, WP51-076 | CMD51-011, CMD51-012, CMD51-013 +81 | CMD51-028, CMD51-043, CMD51-045 +12 | 2 | Blocks; page centering; movement/deletion; file list/look; margins; move; print/retrieve/save; codes; tabs; typeover; preview; numbered step mapping/input/output/resource reconciliation missing; F-WB1 |
| 5 | Fill a memo; 26 / 35 | WP51-030, WP51-007, WP51-034, WP51-008, WP51-054, WP51-011, WP51-013, WP51-033, WP51-016, WP51-035 | CMD51-002, CMD51-005, CMD51-006 +60 | CMD51-005, CMD51-043, CMD51-045 +9 | none indexed | Attributes; cancel; page centering; cursor; dates; code/text deletion; margins; repeat; returns; tabs; numbered step mapping/input/output/resource reconciliation missing; F-WB1 |
| 6 | Final letter; 35 / 44 | WP51-054, WP51-019, WP51-068 | CMD51-065, CMD51-127, CMD51-128 +3 | — | 2 | Dates; retrieve; speller; numbered step mapping/input/output/resource reconciliation missing; F-WB1 |
| 7 | Help workflows; 39 / 48 | WP51-007, WP51-029, WP51-002, WP51-011 | CMD51-002, CMD51-003, CMD51-004 +25 | CMD51-004, CMD51-005, CMD51-043 +9 | 2 | Cancel; exit; help; Undelete; numbered step mapping/input/output/resource reconciliation missing; F-WB2 |
| 8 | Second letter draft; 45 / 54 | WP51-007, WP51-011, WP51-040, WP51-041 | CMD51-002, CMD51-005, CMD51-006 +26 | CMD51-005, CMD51-043, CMD51-045 +8 | none indexed | Cancel; delete text; pages; page numbering; Undelete; numbered step mapping/input/output/resource reconciliation missing; F-WB2 |
| 9 | Editing screens; 61 / 70 | WP51-009, WP51-010, WP51-007, WP51-006 | CMD51-002, CMD51-005, CMD51-006 +15 | CMD51-005, CMD51-028, CMD51-202 +2 | none indexed | Block; move; repeat; switch; numbered step mapping/input/output/resource reconciliation missing; F-WB2 |
| 10 | Second letter completion; 70 / 79 | WP51-009, WP51-054, WP51-011, WP51-013, WP51-044, WP51-041, WP51-014, WP51-063 | CMD51-027, CMD51-028, CMD51-029 +43 | CMD51-028, CMD51-043, CMD51-045 +9 | 2 | Blocks; dates; code deletion; headers/footers; page numbering; search; sort; numbered step mapping/input/output/resource reconciliation missing; F-WB2 |
| 11 | Manage files; 80 / 89 | WP51-021, WP51-023 | CMD51-071, CMD51-072, CMD51-073 +7 | — | 1, 2 | Backup; delete files; directories; file list and its printing correction; numbered step mapping/input/output/resource reconciliation missing; F-WB2 |
| 12 | Editing techniques; 88 / 97 | WP51-021, WP51-009, WP51-054, WP51-031, WP51-032, WP51-034, WP51-023, WP51-010, WP51-070, WP51-014, WP51-077, WP51-063, WP51-011, WP51-006 | CMD51-007, CMD51-008, CMD51-027 +65 | CMD51-028, CMD51-043, CMD51-045 +8 | 2, 3 | Backup; block; dates; font; initial codes/settings; justification; file list; move; print; search/setup/sort; Undelete; windows; numbered step mapping/input/output/resource reconciliation missing; F-WB2 |
| 13 | Letter formatting I; 109 / 118 | WP51-043, WP51-033, WP51-034, WP51-036, WP51-035 | CMD51-094, CMD51-095, CMD51-096 +14 | — | 3 | Newspaper columns; format; indent; line height/spacing; margins; tabs; numbered step mapping/input/output/resource reconciliation missing; F-WB3 |
| 14 | Letter formatting II; 122 / 131 | WP51-038, WP51-057, WP51-044, WP51-033, WP51-041, WP51-014, WP51-068, WP51-042 | CMD51-052, CMD51-053, CMD51-054 +20 | — | 3 | Advance; graphic lines; headers/footers; margins; numbering; replace/search; speller; widow/orphan; numbered step mapping/input/output/resource reconciliation missing; F-WB3 |
| 15 | Office automation; 134 / 143 | WP51-059 | CMD51-131, CMD51-132, CMD51-133 +17 | CMD51-131, CMD51-132, CMD51-205 +16 | none indexed | Macro authoring/execution; numbered step mapping/input/output/resource reconciliation missing; F-WB3 |
| 16 | Newsletter formatting I; 143 / 152 | WP51-043, WP51-031, WP51-033, WP51-008, WP51-055, WP51-057 | CMD51-011, CMD51-012, CMD51-013 +22 | — | none indexed | Newspaper columns; font; format/margins; Go To; graphics; graphic lines; numbered step mapping/input/output/resource reconciliation missing; F-WB3 |
| 17 | Newsletter formatting II; 153 / 162 | WP51-030, WP51-031, WP51-055, WP51-033, WP51-041 | CMD51-032, CMD51-090, CMD51-091 +8 | — | none indexed | Attributes; font; graphics; margins; page numbering; numbered step mapping/input/output/resource reconciliation missing; F-WB3 |
| 18 | Report outline; 169 / 178 | WP51-047 | CMD51-171 | — | none indexed | Outline creation/definition; numbered step mapping/input/output/resource reconciliation missing; F-WB3 |
| 19 | Report indentation and spacing; 185 / 194 | WP51-034, WP51-036, WP51-033, WP51-035 | CMD51-094, CMD51-095, CMD51-096 +12 | — | 3 | Indentation; spacing; margins; tabs; numbered step mapping/input/output/resource reconciliation missing; F-WB4 |
| 20 | Report tabs; 191 / 200 | WP51-009, WP51-010, WP51-035 | CMD51-027, CMD51-028, CMD51-029 +13 | CMD51-028, CMD51-202, CMD51-203 +1 | 3, 4 | Blocks; move; tabs; numbered step mapping/input/output/resource reconciliation missing; F-WB4 |
| 21 | Report footers and notes; 207 / 216 | WP51-042, WP51-045, WP51-055, WP51-057, WP51-044, WP51-010, WP51-041, WP51-014 | CMD51-052, CMD51-053, CMD51-054 +19 | — | 4 | Block protect; notes; graphics/lines; headers/footers; move; numbering; search; numbered step mapping/input/output/resource reconciliation missing; F-WB4 |
| 22 | Report contents and index; 222 / 231 | WP51-045, WP51-050, WP51-055, WP51-057, WP51-041 | CMD51-115, CMD51-116, CMD51-117 +6 | — | 4 | Notes; generate; graphics/lines; indexing; numbering; contents; numbered step mapping/input/output/resource reconciliation missing; F-WB4 |
| 23 | Merge basics; 243 / 252 | WP51-062, WP51-005, WP51-006 | CMD51-007, CMD51-008, CMD51-134 +15 | CMD51-134, CMD51-207, CMD51-208 +12 | 4 | Merge; screen; windows; numbered step mapping/input/output/resource reconciliation missing; F-WB4 |
| 24 | Mass mailings; 254 / 263 | WP51-062, WP51-070 | CMD51-134, CMD51-183, CMD51-184 +14 | CMD51-134, CMD51-207, CMD51-208 +12 | 4 | Merge and printing; numbered step mapping/input/output/resource reconciliation missing; F-WB4 |
| 25 | Advanced editing techniques; 265 / 274 | WP51-038, WP51-042, WP51-043, WP51-089, WP51-005, WP51-050, WP51-039, WP51-062, WP51-014, WP51-035, WP51-006 | CMD51-007, CMD51-008, CMD51-052 +39 | CMD51-134, CMD51-207, CMD51-208 +12 | 4, 5 | Advance; protect; parallel columns; cross-reference; screen choices; generate; hyphenation; merge; search; tabs; windows; numbered step mapping/input/output/resource reconciliation missing; F-WB5 |
| 26 | Characters and keyboards; 293 / 302 | WP51-066, WP51-003, WP51-059 | CMD51-009, CMD51-010, CMD51-131 +20 | CMD51-131, CMD51-132, CMD51-205 +16 | 5 | Compose; keyboards; macros; numbered step mapping/input/output/resource reconciliation missing; F-WB5 |
| 27 | Document management; 309 / 318 | WP51-023, WP51-027, WP51-090, WP51-028, WP51-014, WP51-025 | CMD51-052, CMD51-053, CMD51-054 +22 | — | none indexed | Directories; comments/summary; find/look; file list; search; text input/output; numbered step mapping/input/output/resource reconciliation missing; F-WB5 |
| 28 | Labels and envelopes; 323 / 332 | WP51-032, WP51-053, WP51-062, WP51-041, WP51-070, WP51-077 | CMD51-093, CMD51-134, CMD51-165 +19 | CMD51-134, CMD51-207, CMD51-208 +12 | 5, 6 | Initial codes; labels; merge; paper definitions; printing; setup; numbered step mapping/input/output/resource reconciliation missing; F-WB5 |
| 29 | Equations; 335 / 344 | WP51-066, WP51-058, WP51-031 | CMD51-138, CMD51-160, CMD51-161 +1 | — | 7 | Compose; equations; fonts; numbered step mapping/input/output/resource reconciliation missing; F-WB5 |
| 30 | Form filling; 366 / 375 | WP51-038, WP51-027, WP51-062 | CMD51-107, CMD51-108, CMD51-134 +16 | CMD51-134, CMD51-207, CMD51-208 +12 | 7 | Advance; document comments; merge; numbered step mapping/input/output/resource reconciliation missing; F-WB5 |
| 31 | Graphics; 380 / 389 | WP51-043, WP51-031, WP51-055, WP51-057 | CMD51-160, CMD51-161, CMD51-168 +3 | — | 8 | Newspaper columns; fonts; graphics; graphic lines; numbered step mapping/input/output/resource reconciliation missing; F-WB6 |
| 32 | Record sorting; 397 / 406 | WP51-063 | CMD51-135 | — | none indexed | Sort keys/records; numbered step mapping/input/output/resource reconciliation missing; F-WB6 |
| 33 | Styles; 407 / 416 | WP51-046 | CMD51-118, CMD51-119 | — | 8 | Styles; numbered step mapping/input/output/resource reconciliation missing; F-WB6 |
| 34 | Tables I; 425 / 434 | WP51-048, WP51-049 | CMD51-120, CMD51-121, CMD51-122 +1 | — | 8 | Tables and their structure/formatting; numbered step mapping/input/output/resource reconciliation missing; F-WB6 |
| 35 | Tables II; 446 / 455 | WP51-031, WP51-048, WP51-049 | CMD51-120, CMD51-121, CMD51-122 +3 | — | 8 | Fonts; tables and calculations; numbered step mapping/input/output/resource reconciliation missing; F-WB6 |
| 36 | Thesaurus; 466 / 475 | WP51-069 | CMD51-182 | — | none indexed | Thesaurus; numbered step mapping/input/output/resource reconciliation missing; F-WB6 |

## Menu concordance and unrepresented leaves

REF51 Appendix M printed893–896 / PDF910–913 lists File, Edit, Search, Layout, Mark, Tools, Font, Graphics and Help. CMD51-001 observes opening/closing the menu bar only. **No row below claims its named leaves are observed by that global toggle.** Existing representative command IDs are candidates for parts of each root; each listed leaf still needs a path/prompt/state/branch mapping. This preserves submenus instead of turning one top-level menu scenario into complete menu coverage.

| Root / row | REF51 printed/PDF | Inventory leads | Candidate IDs | Leaf/branch mapping still required |
| --- | --- | --- | --- | --- |
| File / M1 | 893 / 910 | WP51-019, WP51-020, WP51-025, WP51-065, WP51-024, WP51-023, WP51-090, WP51-070, WP51-077, WP51-003, WP51-078, WP51-029 | CMD51-009, CMD51-010, CMD51-065 +27 | Retrieve; Save; Text In (DOS modes, Spreadsheet import/create/edit/link options); Text Out (DOS/Generic/WP5.0/WP4.2); Password add/change/remove; List Files; Summary; Print; Setup mouse/display/environment/initial settings; Keyboard Layout; Location of Files; DOS/Shell; Exit |
| Edit / M2 | 893 / 910 | WP51-010, WP51-011, WP51-009, WP51-027, WP51-015, WP51-042, WP51-006, WP51-013 | CMD51-007, CMD51-008, CMD51-027 +36 | Move/Cut; Copy; Paste; Append to file/clipboard; Delete; Undelete; Block; Select sentence/paragraph/page/tabular column/rectangle; Comment create/edit/convert; case upper/lower; Protect Block; Switch Document; Window; Reveal Codes |
| Search / M3 | 894 / 911 | WP51-014, WP51-008 | CMD51-011, CMD51-012, CMD51-013 +25 | Forward; Backward; Next; Previous; Replace; Extended forward/backward/next/previous/replace; Go To |
| Layout / M4 | 894 / 911 | WP51-033, WP51-043, WP51-048, WP51-049, WP51-064, WP51-045, WP51-034, WP51-035, WP51-040, WP51-046 | CMD51-094, CMD51-095, CMD51-096 +23 | Line; Page; Document; Other; Columns on/off/define; Tables create/edit; Math on/off/define/calculate; Footnote create/edit/number/options; Endnote create/edit/number/options/placement; Justify left/center/right/full; Align indent/margin release/center/flush right/tab align/hard page; Styles |
| Mark / M5 | 895 / 912 | WP51-050, WP51-089, WP51-051, WP51-052, WP51-027 | CMD51-124, CMD51-125, CMD51-126 +5 | Index; Contents; List; Cross-reference reference/target/both; Authorities short/full/edit; Define index/contents/list/authorities; Generate; Master expand/condense; Subdocument; Compare add/remove markings |
| Tools / M6 | 895 / 912 | WP51-068, WP51-069, WP51-059, WP51-054, WP51-047, WP51-062, WP51-063, WP51-017 | CMD51-127, CMD51-128, CMD51-131 +42 | Spell; Thesaurus; Macro define/execute; Date text/code/format; Outline on/off/move/copy/delete family; Paragraph Number; Define; Merge Codes field/end record/input/page off/next record/more; Merge; Sort; Line Draw |
| Font / M7 | 896 / 913 | WP51-031, WP51-030, WP51-070, WP51-066 | CMD51-032, CMD51-090, CMD51-091 +6 | Base font; Normal; Appearance bold/underline/double underline/italic/outline/shadow/small caps/redline/strikeout; super/subscript; fine/small/large/very large/extra large; print color; characters |
| Graphics / M8 | 896 / 913 | WP51-055, WP51-058, WP51-057 | CMD51-174, CMD51-176, CMD51-177 | Figure/Table Box/Text Box/User Box/Equation: create/edit/new number/options; Line horizontal/vertical create/edit |
| Help / M9 | 896 / 913 | WP51-002, WP51-001 | CMD51-001, CMD51-002, CMD51-003 +1 | Help; Index; Template |

## Toolkit contents and release applicability

All 126 section-coded entries from SDK51 contents PDF4–6 are indexed below. The printed prefix and actual PDF start remain explicit. The Office Function58h label is reconstructed from its wrapped TOC line, not dropped as “Memory or Disk.” WP/PL/OF/DR/DP/DV/DOS/OS2/WPW/UNX/AP body offsets are respectively 13/120/145/203/232/284/336/356/367/419/499, using actual printed body folios. The AP Japanese TOC entry is an explicit exception: TOC AP-19 leads to an otherwise blank page; its body starts printed20/PDF519 (V08). WPW/OS2/UNX/other-product entries are **context/interface leads pending applicability study**, not automatic DOS feature support. AP-19 Japanese DOS differences retain language/resource obligations. Frontmatter pointers are separately marked as TOC pointers where body folios have not been reconciled; no guessed Roman pagination is used.

| Row | Topic | Printed / PDF | Parent groups | S | CMD51 candidate examples | Related O examples |
| --- | --- | --- | --- | --- | --- | --- |
| SDK-WP-1 | WordPerfect / WordPerfect 5.1 Document Format | WP-1 / 14 | FMT51-001 | S | CMD51-194 | — |
| SDK-WP-3 | Prefix Area | WP-3 / 16 | FMT51-001 | S | CMD51-194 | — |
| SDK-WP-7 | Additional Prefix Area | WP-7 / 20 | FMT51-002 | S | CMD51-195 | — |
| SDK-WP-9 | WordPerfect Packet Types | WP-9 / 22 | FMT51-002 | S | CMD51-195 | — |
| SDK-WP-17 | Document Area | WP-17 / 30 | FMT51-003 | S | CMD51-196 | — |
| SDK-WP-19 | Control Characters | WP-19 / 32 | FMT51-004 | I | CMD51-197 | — |
| SDK-WP-20 | ASCII Characters | WP-20 / 33 | FMT51-004 | I | CMD51-197 | — |
| SDK-WP-21 | Single-Byte Functions | WP-21 / 34 | FMT51-004 | I | CMD51-197 | — |
| SDK-WP-23 | Fixed-Length, Multi-Byte Functions | WP-23 / 36 | FMT51-004 | I | CMD51-197 | — |
| SDK-WP-27 | Variable-Length, Multi-Byte Functions | WP-27 / 40 | FMT51-004 | I | CMD51-197 | — |
| SDK-WP-36 | Font Group | WP-36 / 49 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-38 | Definition Group | WP-38 / 51 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-49 | Set Group | WP-49 / 62 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-55 | Format Group | WP-55 / 68 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-61 | Header/Footer Group | WP-61 / 74 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-62 | Footnote/Endnote Group | WP-62 / 75 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-64 | Generate Group | WP-64 / 77 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-69 | Display Group | WP-69 / 82 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-71 | Miscellaneous Group | WP-71 / 84 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-74 | Box Group | WP-74 / 87 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-79 | Style Group | WP-79 / 92 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-81 | Table End of Line Codes Group | WP-81 / 94 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-85 | Table End of Page Codes Group | WP-85 / 98 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-86 | Enhanced Merge Command Codes Group | WP-86 / 99 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-88 | Equation Nested Function Group | WP-88 / 101 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-89 | Tag Group | WP-89 / 102 | FMT51-005 | I | CMD51-198 | — |
| SDK-WP-92 | .WPM Macro File Formats for DOS, VAX, UNIX | WP-92 / 105 | FMT51-006 | I | CMD51-199 | — |
| SDK-WP-94 | Control Characters | WP-94 / 107 | FMT51-006 | I | CMD51-199 | — |
| SDK-WP-97 | Macro Commands | WP-97 / 110 | FMT51-006 | I | CMD51-199 | — |
| SDK-WP-100 | Detection of WordPerfect 4.2 Files by WP 5.0 and WP 5.1 | WP-100 / 113 | WP51-026 | S | CMD51-157 | — |
| SDK-WP-102 | Importing Lotus Files into WordPerfect | WP-102 / 115 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-WP-103 | WordPerfect Font Procedure | WP-103 / 116 | WP51-031, WP51-073 | S | CMD51-160, CMD51-161, CMD51-187 | — |
| SDK-PL-1 | PlanPerfect / PlanPerfect Worksheet File Format | PL-1 / 121 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-2 | PlanPerfect Record Types | PL-2 / 122 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-14 | Cell Value Type and Attributes | PL-14 / 134 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-15 | Format Information | PL-15 / 135 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-16 | Width/Font Information | PL-16 / 136 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-17 | WPCorp String Information | PL-17 / 137 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-18 | Floating-Point Number Representation | PL-18 / 138 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-PL-19 | Formula Encoding | PL-19 / 139 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-OF-1 | Office / Shell Overview | OF-1 / 146 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-2 | The Shell Program | OF-2 / 147 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-3 | Writing Programs that Interact with Shell | OF-3 / 148 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-4 | Function 35h—Check if Shell is Resident | OF-4 / 149 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-5 | Function 50h—Get Program ID | OF-5 / 150 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-6 | Function 51h—Go to Shell | OF-6 / 151 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-7 | Function 52h—Write Data to Clipboard | OF-7 / 152 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-8 | Function 53h—Append Data to Clipboard | OF-8 / 153 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-9 | Function 54h—Retrieve Data from Clipboard | OF-9 / 154 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-10 | Function 55h—Request Permission to Exit | OF-10 / 155 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-11 | Function 56h—Check Clipboard Format | OF-11 / 156 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-12 | Function 57h—Check if Shell is Installing Program Resident | OF-12 / 157 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-13 | Function 58h: shell swapping/expanded-memory/disk status | OF-13 / 158 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-14 | Function 59h—Test if Program is Highest in Memory | OF-14 / 159 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-15 | Function 5Ah—Get Shell's Colors | OF-15 / 160 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-16 | Function 5Bh—Shell Control Interface | OF-16 / 161 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-18 | Shell Macro Interaction | OF-18 / 163 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-22 | Office Program {STATE} Definitions | OF-22 / 167 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-25 | User Interface Guidelines and Suggestions | OF-25 / 170 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-26 | File Formats for the Clipboard | OF-26 / 171 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-27 | Memory Considerations | OF-27 / 172 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-28 | Notebook File Formats | OF-28 / 173 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-35 | WordPerfect Office 4.0 Third-Party Interface | OF-35 / 180 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-36 | WordPerfect Office 4.0 Call-Level Interface | OF-36 / 181 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-42 | DDE and WordPerfect Office 4.0 | OF-42 / 187 | WP51-078 | S | CMD51-189 | — |
| SDK-OF-50 | WordPerfect Office 4.0 Custom Commands | OF-50 / 195 | WP51-078 | S | CMD51-189 | — |
| SDK-DR-1 | DrawPerfect / WordPerfect Graphic (WPG) File Format | DR-1 / 204 | WP51-055, WP51-056 | S | CMD51-174, CMD51-175 | — |
| SDK-DR-5 | WordPerfect Graphic Record Types | DR-5 / 208 | WP51-055, WP51-056 | S | CMD51-174, CMD51-175 | — |
| SDK-DR-19 | Color Numbers and Color Maps in .WPG Files | DR-19 / 222 | WP51-055, WP51-056 | S | CMD51-174, CMD51-175 | — |
| SDK-DR-25 | AutoCAD, CGM, and HPGL Import Formats | DR-25 / 228 | WP51-055, WP51-056 | S | CMD51-174, CMD51-175 | — |
| SDK-DP-1 | DataPerfect / Introduction | DP-1 / 233 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-DP-2 | DataPerfect Engine Summary | DP-2 / 234 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-DP-3 | DataPerfect Engine Functions | DP-3 / 235 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-DP-51 | DataPerfect Engine Errors | DP-51 / 283 | WP51-065 | S | CMD51-136, CMD51-137 | — |
| SDK-DV-1 | Drivers / Printer Driver Development | DV-1 / 285 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-2 | Glossary of Terms | DV-2 / 286 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-9 | Information Placement and Retrieval in .DRS, .PRS, or .ALL Files | DV-9 / 293 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-12 | .PRS/.ALL File Format Map | DV-12 / 296 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-16 | .PRS/.ALL File Format | DV-16 / 300 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-19 | WordPerfect Printer Definition Language (WPDL) | DV-19 / 303 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-24 | WPDL Compact Form | DV-24 / 308 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-29 | AutoFont support | DV-29 / 313 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-33 | ADDALL Information | DV-33 / 317 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-34 | Video Driver Development | DV-34 / 318 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DV-48 | Mouse Driver | DV-48 / 332 | WP51-005, WP51-004, WP51-071, WP51-073 | S | CMD51-153, CMD51-154, CMD51-185 +1 | — |
| SDK-DOS-1 | DOS Third-Party / Introduction | DOS-1 / 337 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-DOS-6 | Interface / WordPerfect Keys | DOS-6 / 342 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-DOS-7 | PlanPerfect Keys | DOS-7 / 343 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-DOS-10 | Editor Keys | DOS-10 / 346 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-DOS-12 | DrawPerfect Keys | DOS-12 / 348 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-DOS-14 | Macro Commands | DOS-14 / 350 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-DOS-18 | WordPerfect and DOS | DOS-18 / 354 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-OS2-1 | OS/2 Third-Party / Messages | OS2-1 / 357 | WP51-078, WP51-080 | S | CMD51-189, CMD51-191 | — |
| SDK-OS2-6 | Interface / Control Character Commands | OS2-6 / 362 | WP51-078, WP51-080 | S | CMD51-189, CMD51-191 | — |
| SDK-OS2-7 | WordPerfect Function Key Commands | OS2-7 / 363 | WP51-078, WP51-080 | S | CMD51-189, CMD51-191 | — |
| SDK-OS2-8 | WordPerfect Key Commands | OS2-8 / 364 | WP51-078, WP51-080 | S | CMD51-189, CMD51-191 | — |
| SDK-OS2-9 | Macro Keyboard Commands | OS2-9 / 365 | WP51-078, WP51-080 | S | CMD51-189, CMD51-191 | — |
| SDK-WPW-1 | WordPerfect for / Introduction | WPW-1 / 368 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-2 | Windows Interface / WPWin 5.x Call-Level Interface (CLI) | WPW-2 / 369 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-3 | Registering Third-Party Programs with WPWin 5.x | WPW-3 / 370 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-6 | DDE Execute | WPW-6 / 373 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-8 | DLL Entry Points | WPW-8 / 375 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-9 | Dialog Box Manager | WPW-9 / 376 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-14 | Custom Controls | WPW-14 / 381 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-16 | Counter Control | WPW-16 / 383 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-17 | Dialog Entry Points | WPW-17 / 384 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-22 | DDE Entry Points | WPW-22 / 389 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-24 | .INI File Entry Points | WPW-24 / 391 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-34 | Application Execution Entry Points | WPW-34 / 401 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-37 | String Conversion Entry Points | WPW-37 / 404 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-39 | MCR Entry/Exit APIs | WPW-39 / 406 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-40 | Miscellaneous Entry Pointss | WPW-40 / 407 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-44 | List of Tokens | WPW-44 / 411 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-WPW-46 | New or Modified Macro Tokens in WPWin 5.2 | WPW-46 / 413 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-UNX-1 | UNIX Third-Party / Introduction | UNX-1 / 420 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-UNX-6 | Interface / WordPerfect Keys | UNX-6 / 425 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-UNX-9 | WordPerfect Commands | UNX-9 / 428 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-UNX-11 | WordPerfect Dialog Commands | UNX-11 / 430 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-UNX-15 | Graphical Commands | UNX-15 / 434 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-UNX-19 | Macro Commands | UNX-19 / 438 | WP51-059, WP51-078 | S | CMD51-131, CMD51-132, CMD51-133 +18 | CMD51-131, CMD51-132, CMD51-205 +16 |
| SDK-AP-1 | Appendixes / Appendix A: WordPerfect .SET File Packets | AP-1 / 500 | WP51-077 | S | CMD51-188 | — |
| SDK-AP-11 | Appendix B: .WPK Keyboard Macro File Formats | AP-11 / 510 | WP51-003 | S | CMD51-009, CMD51-010 | — |
| SDK-AP-13 | Appendix C: Screen Font Files | AP-13 / 512 | WP51-005, WP51-031 | S | CMD51-154, CMD51-160, CMD51-161 | — |
| SDK-AP-16 | Appendix D: General Font Terms | AP-16 / 515 | WP51-031, WP51-073 | S | CMD51-160, CMD51-161, CMD51-187 | — |
| SDK-AP-17 | Appendix E: Hex Chart | AP-17 / 516 | WP51-066 | S | CMD51-138 | — |
| SDK-AP-19 | Appendix F: Japanese Version of WP 5.1 for DOS | AP-20 / 519 (TOC says19) | WP51-066 | S | CMD51-138 | — |
| SDK-F1 | Disclaimer | TOC / 4 | context | context | — | — |
| SDK-F2 | Overview | TOC / 4 | context | context | — | — |
| SDK-F3 | Audience | TOC / 4 | context | context | — | — |
| SDK-F4 | Support | TOC / 4 | context | context | — | — |
| SDK-F5 | Toolkit media contents | TOC / 4 | context | context | — | — |

## Gaps that the current thematic registries conceal

These are source-coverage findings, not edits to the canonical registries. They
must be reconciled in an owned follow-up rather than quietly changing source
pages or treating a nearby case as the missing test.

| Source entry | Existing lead | Concrete uncovered work |
| --- | --- | --- |
| REF51 57/PDF74, cartridge/font/print-wheel resources | WP51-073; CMD51-187 | Current parent's locators begin much later. Enumerate resource selection, printer-specific availability and substitution from this section; map individual options. |
| REF51 114/PDF131, Delete Files | WP51-023; CMD51-076/077 | File-list parent locators omit this source section. Audit confirmations, selection and failed deletion; file-list entry alone does not cover deletion behavior. |
| REF51 157/PDF174, edit-screen options | WP51-005/077; CMD51-007/144 | Existing locator sets omit this start. Enumerate each setting and relation to screen/layout modes. |
| REF51 431/PDF448 and 438/PDF455, mouse setup/type | WP51-004; CMD51-143 | Current parent covers 434–437 only. Separate setup/type/native configuration from pointer actions and Linux input mappings. |
| REF51 469/PDF486, Overstrike | WP51-030; CMD51-089/090 | Attribute parent omits this section; no dedicated Overstrike case is established by broad attribute examples. Add command/code/character behavior research. |
| REF51 487/PDF504, paragraph numbering | WP51-047; CMD51-171 | Outline parent locators do not reach this section. Separate numbering setup, regeneration and native relationships from an outline example. |
| REF51 544/PDF561, pull-down menus | WP51-001; CMD51-001/002 | Parent cites startup 3–12; appendix M is aggregated under WP51-082. Audit full interaction section and every menu path independently of opening the bar. |
| REF51 567/PDF584, Screen | WP51-005; CMD51-007 | This start is absent from selected display locators. Distinguish Screen command from the separate screen-capture utility at the same page. |
| REF51 O 905/PDF922 and S 961/PDF978 | WP51-082 and WP51-078/080/081; CMD51-189/195/196 | Troubleshooting is outside the current code/error group locators, and PIF is beyond WP51-081's 921–960 range. Enumerate original diagnostics/integration and explicit Linux mappings; neither is removed from M1. |

A candidate ID in this table is a starting point, not proof that its named branch
is covered. Parent cases may cite different passages. The embedded verifier
checks IDs and source association without upgrading original evidence status.
All main-TOC entry locator gaps can be recomputed by comparing row starts with
the selected parent locator sets; nine rows have no selected parent's locator
containing the start page. Appendix/source-context gaps are additional.

The WB51 feature list identifies concrete omissions in the old thematic map:

- Lesson 1 includes Save, Printing and View Document; its older groups focus
  mostly on screen/cursor/deletion. Lesson 6 explicitly lists Dates/Retrieve/
  Speller, rather than just Save/Backup/Print.
- Lesson 13 explicitly lists newspaper columns, line height/spacing and tabs;
  the old lead set misses these. Lesson 14 lists Advance, graphic lines,
  headers/footers, search/replace, spelling and widow/orphan alongside margins.
- Lesson 23 includes Screen and Window as well as Merge. Lesson 28 includes
  labels, initial codes, merge, paper and print/setup; a Macro association is
  not established by its feature list. Lesson 30 lists Advance, Document Comments
  and Merge; typeover is not its defining feature-list entry.
- Lesson 26 includes macros alongside compose/keyboards, and lesson 27 includes
  Text In/Out as well as file-management themes. Rich notes/graphics/reference
  dependencies in lessons 21–22 need their own steps, not just a broad report label.

These are corrected **research leads**, not complete lesson rewrites. Source
feature lists themselves are not every numbered step or all incidental command
use. The registry correction proposal must compare each whole lesson and its
notices before changing `workbook-map.md` or assigning complete coverage.

## Version-sensitive discrepancy register

Each row retains the uncertainty and a bounded next probe/resource prerequisite.
Dates establish a research question, not automatic proof of behavior in the
March executable. No baseline substitution or original-feature exclusion is made.

| ID | Exact documentary evidence | Affected links | Bounded disposition / next evidence |
| --- | --- | --- | --- |
| V01 | WB51 11/89 versus selected 1992-03-09; WBC51 PDF1–8 | WB01–36 and all their linked groups/cases | Reconcile one numbered lesson at a time with its listed correction pages, source learning files, settings and expected outputs. Store lesson-step identities and corrected edition-specific expectations before replay. No lesson has yet been run. |
| V02 | WBC51 PDF1: lesson11 printed85 change and introduction printedvii printer-test correction; WB51 introduction vii/PDF8 | WP51-023/071/073; CMD51-076/077/185/187 | The workbook printer cannot print the file list; declare a real selected printer before replaying list printing. `WORKBOOK.PRS` and `PRINTER.TST` are already fingerprinted in installed-files.json; availability is not execution or redistribution permission. Test the documented retrieve-and-print printer test and retain the actual resource hashes. |
| V03 | REF51 6/92 copyright PDF3 versus selected March program; DOC51 PDF12 international macro interface (notice refers to older page415; current REF51 section is379/PDF396) | WP51-059/060; CMD51-131/132/136; R102 | Match headings and exact editions, not copied old page numbers. Probe localized mnemonic versus international numeric/menu routing in a licensed language profile. The current U.S. macro probes do not establish every international interface branch. |
| V04 | ENH51 PDF1, Alignment dated05/31/91; older releases through12/31/90 show End C/A as unknown | WP51-034/013; CMD51-094/048/049/050/051 | Produce a bounded Center/Align termination fixture in the March target; preserve the code across no-edit saves. If older releases are compared, retain their unknown-code behavior separately rather than normalizing it. Chronology suggests availability; only a probe proves the target outcome. |
| V05 | ENH51 PDF35–36, Printing dated03/09/92 and related2/13/92 driver changes | WP51-070/071/073/076; CMD51-183/185/187/188 | Declare compatible printer ALL/PRS, fonts and look-ahead settings; test mixed text/graphics with the actual named driver family. A July Standard Printer cannot establish this release-dependent graphics result. Resource licensing/calibration precede comparison. |
| V06 | SDK51 WP-6/PDF19 stored versions shared with WPWin; WP-12/PDF25 graphics packets; platform additions across WP groups and WPW section | FMT51-001/002/005; WP51-055/056; CMD51-174/175 | Use WP01's supported/refused framing and separately investigate nonzero graphics and platform-specific payloads against original DOS output. Shared header versions do not prove Windows semantics belong to the March DOS file. |
| V07 | SDK51 WP-17/PDF30 nine-byte minimum prose versus original eight-byte merge functions documented in WP01 | FMT51-003/005; WP51-062; CMD51-134/207 | Preserve observed L=4/L+4 framing exception, exact fixture hashes and original release identity. Further code-group interpretations require their own original examples; no arbitrary length minimum or semantic writer is inferred. |
| V08 | SDK51 contents PDF6 names AP-19, but PDF518/printed19 is otherwise blank; Japanese appendix actually begins printed20/PDF519 | WP51-066/067/003; CMD51-138/181/009/010; SDK-AP-19 | Keep the TOC key and actual body locator distinct. Obtain the Japanese locale/resources and reconcile original character/code differences; U.S. fixtures do not prove language parity. This source pagination discrepancy does not remove original language obligations. |
| V09 | WB51 feature list478–481/PDF487–490 versus thematic workbook-map.md; WBC51 entries cite older lesson/page labels | WB01–36; especially WB06/13/14/23/28/30 | F-WB correction package must compare source heading, numbered step and notice date before updating a link. Screens, sample text and teaching file dependencies may differ; no automatic lesson-number equivalence across later editions. |

The Japanese appendix additionally identifies distinct document/macro/keyboard
file types58/59/60 and packet16 font data, whereas the WPWin annotation uses
packet16 for DDE. These are documentary variant facts, not U.S. reader support
claims or executed Japanese observations.

## Bounded proposed follow-ups for WP12

None of these creates or edits a WP prompt, canonical ID or queue. WP12 should
slice the named family into an executable package with the real owning surface
and review contract. A family is not a license to implement guessed behavior.

| Family | Bounded unit / deliverable | Coverage impact and prerequisite |
| --- | --- | --- |
| F-REF | One source feature section at a time from R001–R202; enumerate its actual named options, prompts, failure/cancel branches and native effects, then match/create canonical child scenarios | Close the nine whole-parent start-locator gaps listed above first. Attach exact edition/page and existing CMD links; retain parent groups as coverage groups. Source indexing is not a passing behavior test. |
| F-APP | One appendix letter at a time; separate tables, diagnostics and command rows; for K/T use a named command/value-table subsection per package | Preserve all A–T obligations, including Q/R resource/network, O diagnostics and S PIF/Linux adaptation questions. Existing broad WP51-060/062/081/082 cannot stand for every command or resource. |
| F-MENU | One of M1–M9 at a time; enumerate full leaf paths and accelerator/context/prompt/cancel/failure states, then link actual source scenarios | Start with File/Text In-Out, Edit/block-restoration, Search/Extended and Layout/Other Format gaps. Global CMD51-001 menu toggle is only a UI-shell observation. Resources, language and native write prerequisites remain explicit. |
| F-WB | One workbook introduction/appendix prerequisite or one discrepancy between workbook-map.md and actual feature list; propose corrections with both old/new links | Update canonical artifacts only in a later package that owns them. Confirm LEARN file/resource hashes and license boundaries before replay; PRS and screen settings affect lessons. |
| F-WB1 | Lessons1–6, one numbered lesson per package: text/files/letter/memo flows | Use WB starts3/6/12/16/26/35 and all actual feature-list dependencies; fix L1/L6 leads. Output every numbered step, retained sample-input identity, expected screen/native result and unresolved branch. No current full lesson replay. |
| F-WB2 | Lessons7–12, one lesson per package: help, document screens, editing and file management | Reconcile WBC51 PDF2–3 and list-print correction PDF1 for L11. Separate current command observations from exact workbook steps and teaching-printer behavior. |
| F-WB3 | Lessons13–18, one lesson per package: letters, macros, newsletters, outlines | Correct columns/spacing/tabs and L14 dependencies from feature-list PDF488; record printer/font/graphics prerequisites before rendered output comparisons. |
| F-WB4 | Lessons19–24, one lesson per package: reports, notes/generated references, merges | Reconcile WBC51 PDF3–4; preserve notes/graphics/headers/merge pagination dependencies. Existing scratch merges do not prove workbook learning-file results. |
| F-WB5 | Lessons25–30, one lesson per package: advanced editing, keyboards, management, labels/equations/forms | Reconcile WBC51 PDF4–7; correct L28/L30 group links. Record character/resource and merge/comment dependencies independently. |
| F-WB6 | Lessons31–36, one lesson per package: graphics/sort/styles/tables/thesaurus | Reconcile WBC51 PDF8 and resource prerequisites. No observations establish these complete lessons; split table structure/math and dictionary-dependent comparisons where needed. |
| F-SDK | One named SDK contents section/field family per package; distinguish DOS document, companion, resource and platform/locale variants | WP01 already researched bounded framing; remaining FMT51-004/005/006 are indexed only. Prioritize nonzero graphics, nested text, WPM and SET/WPK/font/printer resources; tie PL/DR/Office interfaces to actual WP import/interoperation obligations. OS2/WPW/UNX/DP are context pending applicability research, never automatic U.S. DOS semantics. |
| F-CONTEXT | One source-context metadata/pagination ambiguity at a time | Retain historical publisher context and bibliographic facts; correct verified TOC/body discrepancies without converting them into application features or dropping functional obligations. |

For every functional follow-up, acceptance needs source-level study, an explicit
unsupported/unknown disposition when blocked, and original observations under
pinned executable/resources before implementation claims. Writer packages also
need unchanged-byte preservation, safe failure and original retrieve/edit/print/
save comparisons. Resource or platform uncertainty narrows only the supported
implementation slice while remaining visible in M1; it never authorizes silently
removing a feature or moving an original obligation to M2.

## Reproducible audit ledger

The input hashes pin the exact registries used for the links/counts. The compact
row schema records source identity and parent links without duplicating canonical
scenario bodies. Derive each row's complete candidate and related-partial ID sets
by the explicit union rule above. Parent S/I comes from the pinned inventory;
entry-level whole study/observation is unestablished and functional gaps remain.
Workbook starts match contents/the existing map, while feature-list PDF locations
and correction-page indices describe the newly audited leads. The AP Japanese
exception records TOC and actual body folios separately. This data is a research
snapshot, not a replacement inventory or a new native format.

<!-- WP05_AUDIT_BEGIN -->
```json
{
  "schema_version":1,
  "source_inputs":[{"path":"docs/research/feature-inventory.json","sha256":"49d37c3f13a537609346bc71751dabb8661676ecfa8fa40f25cee0752b5bccf8"},{"path":"docs/research/command-scenarios.json","sha256":"a38cb78c02983fd633cf8fa2553d68da563a86a5f591c5d41ad3112ca29e6df0"},{"path":"docs/research/workbook-map.md","sha256":"5a2b69cb6aa4cad061175ed3b93fde3b53a67df941d86739aa6dc2b3b0e10e2b"},{"path":"docs/research/sources.json","sha256":"850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"},{"path":"research/cache/WPDOS51Reference.pdf","sha256":"ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531","source_id":"REF51","edition":"MNUS1WP51X1C-6/92 (copyright leaf; scan, OCR duplicated in places)","pdf_pages":1048,"redistribute":false},{"path":"research/cache/WPDOS51Workbook.pdf","sha256":"868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d","source_id":"WB51","edition":"WKUS1WP51-11/89 (copyright leaf)","pdf_pages":512,"redistribute":false},{"path":"research/cache/WP51DevelopersToolkit.pdf","sha256":"5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754","source_id":"SDK51","edition":"MNUSXTW511-12/93; WP subsection carries intermediate revision marks","pdf_pages":547,"redistribute":false},{"path":"research/cache/WP51ENHA.pdf","sha256":"da633d605b719a5de4656ab52d89c3d59f7741bcfe1d4a91dbb992f123f3424f","source_id":"ENH51","edition":"Publisher-authored maintenance/documentation notice, hosted PDF transcription; internal dates retained","pdf_pages":55,"redistribute":false},{"path":"research/cache/WP51DOCU.pdf","sha256":"d5af65cb920f04e59d32f7ce1d0506616815ae58254423407ded68154b9043b6","source_id":"DOC51","edition":"Publisher-authored maintenance/documentation notice, hosted PDF transcription; internal dates retained","pdf_pages":72,"redistribute":false},{"path":"research/cache/WP51WKBK.pdf","sha256":"7e7b87786d4ac748af6603a98d084c38137a6e723954540b1153ad6ed64e7a0b","source_id":"WBC51","edition":"Publisher-authored maintenance/documentation notice, hosted PDF transcription; internal dates retained","pdf_pages":8,"redistribute":false},{"path":"docs/research/reference-baseline.json","sha256":"6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"},{"path":"docs/research/reference-environment/environment.json","sha256":"30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"},{"path":"docs/research/reference-environment/resource-profile.json","sha256":"e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"},{"path":"docs/research/reference-environment/installed-files.json","sha256":"a8532ce5be7caa5759799841c8c0e3128810f7631f49101978102244139a1238"}],
  "registry_counts":{"feature_groups":91,"documentary_studied":87,"documentary_indexed":4,"scenarios":236,"partially_observed":53,"not_run":183},
  "row_columns":["id","kind","source_id","printed_section","printed_start","pdf_start","inventory_ids","followup"],
  "rows":[
    ["R001","reference-feature","REF51",null,31,48,["WP51-038"],"F-REF"],
    ["R002","reference-feature","REF51",null,34,51,["WP51-010"],"F-REF"],
    ["R003","reference-feature","REF51",null,36,53,["WP51-030"],"F-REF"],
    ["R004","reference-feature","REF51",null,41,58,["WP51-021"],"F-REF"],
    ["R005","reference-feature","REF51",null,43,60,["WP51-021"],"F-REF"],
    ["R006","reference-feature","REF51",null,45,62,["WP51-077"],"F-REF"],
    ["R007","reference-feature","REF51",null,46,63,["WP51-091"],"F-REF"],
    ["R008","reference-feature","REF51",null,48,65,["WP51-009"],"F-REF"],
    ["R009","reference-feature","REF51",null,51,68,["WP51-009","WP51-042"],"F-REF"],
    ["R010","reference-feature","REF51",null,55,72,["WP51-007"],"F-REF"],
    ["R011","reference-feature","REF51",null,56,73,["WP51-015"],"F-REF"],
    ["R012","reference-feature","REF51",null,57,74,["WP51-073"],"F-REF"],
    ["R013","reference-feature","REF51",null,63,80,["WP51-034"],"F-REF"],
    ["R014","reference-feature","REF51",null,65,82,["WP51-034"],"F-REF"],
    ["R015","reference-feature","REF51",null,68,85,["WP51-005"],"F-REF"],
    ["R016","reference-feature","REF51",null,74,91,["WP51-005","WP51-043"],"F-REF"],
    ["R017","reference-feature","REF51",null,75,92,["WP51-043"],"F-REF"],
    ["R018","reference-feature","REF51",null,79,96,["WP51-043"],"F-REF"],
    ["R019","reference-feature","REF51",null,84,101,["WP51-066"],"F-REF"],
    ["R020","reference-feature","REF51",null,88,105,["WP51-040"],"F-REF"],
    ["R021","reference-feature","REF51",null,89,106,["WP51-079"],"F-REF"],
    ["R022","reference-feature","REF51",null,96,113,["WP51-089"],"F-REF"],
    ["R023","reference-feature","REF51",null,103,120,["WP51-008"],"F-REF"],
    ["R024","reference-feature","REF51",null,105,122,["WP51-079"],"F-REF"],
    ["R025","reference-feature","REF51",null,107,124,["WP51-079"],"F-REF"],
    ["R026","reference-feature","REF51",null,109,126,["WP51-054"],"F-REF"],
    ["R027","reference-feature","REF51",null,112,129,["WP51-011","WP51-013"],"F-REF"],
    ["R028","reference-feature","REF51",null,114,131,["WP51-023"],"F-REF"],
    ["R029","reference-feature","REF51",null,115,132,["WP51-011"],"F-REF"],
    ["R030","reference-feature","REF51",null,117,134,["WP51-023"],"F-REF"],
    ["R031","reference-feature","REF51",null,120,137,["WP51-005"],"F-REF"],
    ["R032","reference-feature","REF51",null,122,139,["WP51-005","WP51-077"],"F-REF"],
    ["R033","reference-feature","REF51",null,124,141,["WP51-027"],"F-REF"],
    ["R034","reference-feature","REF51",null,127,144,["WP51-027"],"F-REF"],
    ["R035","reference-feature","REF51",null,130,147,["WP51-026"],"F-REF"],
    ["R036","reference-feature","REF51",null,138,155,["WP51-026"],"F-REF"],
    ["R037","reference-feature","REF51",null,143,160,["WP51-032"],"F-REF"],
    ["R038","reference-feature","REF51",null,145,162,["WP51-090"],"F-REF"],
    ["R039","reference-feature","REF51",null,150,167,["WP51-078"],"F-REF"],
    ["R040","reference-feature","REF51",null,157,174,["WP51-005","WP51-077"],"F-REF"],
    ["R041","reference-feature","REF51",null,159,176,["WP51-077"],"F-REF"],
    ["R042","reference-feature","REF51",null,163,180,["WP51-058"],"F-REF"],
    ["R043","reference-feature","REF51",null,174,191,["WP51-058"],"F-REF"],
    ["R044","reference-feature","REF51",null,184,201,["WP51-058"],"F-REF"],
    ["R045","reference-feature","REF51",null,194,211,["WP51-029"],"F-REF"],
    ["R046","reference-feature","REF51",null,197,214,["WP51-022"],"F-REF"],
    ["R047","reference-feature","REF51",null,197,214,["WP51-028"],"F-REF"],
    ["R048","reference-feature","REF51",null,201,218,["WP51-028"],"F-REF"],
    ["R049","reference-feature","REF51",null,203,220,["WP51-034"],"F-REF"],
    ["R050","reference-feature","REF51",null,205,222,["WP51-031"],"F-REF"],
    ["R051","reference-feature","REF51",null,209,226,["WP51-045"],"F-REF"],
    ["R052","reference-feature","REF51",null,215,232,["WP51-045"],"F-REF"],
    ["R053","reference-feature","REF51",null,217,234,["WP51-040","WP51-091"],"F-REF"],
    ["R054","reference-feature","REF51",null,218,235,["WP51-033"],"F-REF"],
    ["R055","reference-feature","REF51",null,221,238,["WP51-050"],"F-REF"],
    ["R056","reference-feature","REF51",null,224,241,["WP51-008"],"F-REF"],
    ["R057","reference-feature","REF51",null,225,242,["WP51-078"],"F-REF"],
    ["R058","reference-feature","REF51",null,226,243,["WP51-078"],"F-REF"],
    ["R059","reference-feature","REF51",null,228,245,["WP51-056"],"F-REF"],
    ["R060","reference-feature","REF51",null,232,249,["WP51-055"],"F-REF"],
    ["R061","reference-feature","REF51",null,235,252,["WP51-055"],"F-REF"],
    ["R062","reference-feature","REF51",null,246,263,["WP51-055"],"F-REF"],
    ["R063","reference-feature","REF51",null,251,268,["WP51-056"],"F-REF"],
    ["R064","reference-feature","REF51",null,257,274,["WP51-057"],"F-REF"],
    ["R065","reference-feature","REF51",null,261,278,["WP51-057"],"F-REF"],
    ["R066","reference-feature","REF51",null,266,283,["WP51-005","WP51-057"],"F-REF"],
    ["R067","reference-feature","REF51",null,269,286,["WP51-016"],"F-REF"],
    ["R068","reference-feature","REF51",null,269,286,["WP51-044"],"F-REF"],
    ["R069","reference-feature","REF51",null,275,292,["WP51-002"],"F-REF"],
    ["R070","reference-feature","REF51",null,277,294,["WP51-039"],"F-REF"],
    ["R071","reference-feature","REF51",null,281,298,["WP51-039"],"F-REF"],
    ["R072","reference-feature","REF51",null,285,302,["WP51-034"],"F-REF"],
    ["R073","reference-feature","REF51",null,287,304,["WP51-050"],"F-REF"],
    ["R074","reference-feature","REF51",null,288,305,["WP51-050"],"F-REF"],
    ["R075","reference-feature","REF51",null,291,308,["WP51-050"],"F-REF"],
    ["R076","reference-feature","REF51",null,292,309,["WP51-032"],"F-REF"],
    ["R077","reference-feature","REF51",null,295,312,["WP51-032"],"F-REF"],
    ["R078","reference-feature","REF51",null,299,316,["WP51-034"],"F-REF"],
    ["R079","reference-feature","REF51",null,303,320,["WP51-031"],"F-REF"],
    ["R080","reference-feature","REF51",null,304,321,["WP51-003"],"F-REF"],
    ["R081","reference-feature","REF51",null,308,325,["WP51-003"],"F-REF"],
    ["R082","reference-feature","REF51",null,313,330,["WP51-003"],"F-REF"],
    ["R083","reference-feature","REF51",null,319,336,["WP51-053"],"F-REF"],
    ["R084","reference-feature","REF51",null,328,345,["WP51-067"],"F-REF"],
    ["R085","reference-feature","REF51",null,331,348,["WP51-067"],"F-REF"],
    ["R086","reference-feature","REF51",null,337,354,["WP51-017"],"F-REF"],
    ["R087","reference-feature","REF51",null,339,356,["WP51-033"],"F-REF"],
    ["R088","reference-feature","REF51",null,341,358,["WP51-036"],"F-REF"],
    ["R089","reference-feature","REF51",null,344,361,["WP51-036"],"F-REF"],
    ["R090","reference-feature","REF51",null,346,363,["WP51-036"],"F-REF"],
    ["R091","reference-feature","REF51",null,347,364,["WP51-023"],"F-REF"],
    ["R092","reference-feature","REF51",null,355,372,["WP51-050"],"F-REF"],
    ["R093","reference-feature","REF51",null,356,373,["WP51-050"],"F-REF"],
    ["R094","reference-feature","REF51",null,357,374,["WP51-050"],"F-REF"],
    ["R095","reference-feature","REF51",null,358,375,["WP51-023"],"F-REF"],
    ["R096","reference-feature","REF51",null,362,379,["WP51-024"],"F-REF"],
    ["R097","reference-feature","REF51",null,364,381,["WP51-028"],"F-REF"],
    ["R098","reference-feature","REF51",null,369,386,["WP51-059"],"F-REF"],
    ["R099","reference-feature","REF51",null,370,387,["WP51-061"],"F-REF"],
    ["R100","reference-feature","REF51",null,373,390,["WP51-059"],"F-REF"],
    ["R101","reference-feature","REF51",null,378,395,["WP51-059"],"F-REF"],
    ["R102","reference-feature","REF51",null,379,396,["WP51-059"],"F-REF"],
    ["R103","reference-feature","REF51",null,380,397,["WP51-059"],"F-REF"],
    ["R104","reference-feature","REF51",null,386,403,["WP51-059"],"F-REF"],
    ["R105","reference-feature","REF51",null,394,411,["WP51-033"],"F-REF"],
    ["R106","reference-feature","REF51",null,396,413,["WP51-033"],"F-REF"],
    ["R107","reference-feature","REF51",null,397,414,["WP51-052"],"F-REF"],
    ["R108","reference-feature","REF51",null,401,418,["WP51-064"],"F-REF"],
    ["R109","reference-feature","REF51",null,405,422,["WP51-064"],"F-REF"],
    ["R110","reference-feature","REF51",null,408,425,["WP51-064"],"F-REF"],
    ["R111","reference-feature","REF51",null,412,429,["WP51-064"],"F-REF"],
    ["R112","reference-feature","REF51",null,415,432,["WP51-080"],"F-REF"],
    ["R113","reference-feature","REF51",null,418,435,["WP51-001","WP51-062"],"F-REF"],
    ["R114","reference-feature","REF51",null,420,437,["WP51-062"],"F-REF"],
    ["R115","reference-feature","REF51",null,431,448,["WP51-004"],"F-REF"],
    ["R116","reference-feature","REF51",null,434,451,["WP51-004"],"F-REF"],
    ["R117","reference-feature","REF51",null,438,455,["WP51-004"],"F-REF"],
    ["R118","reference-feature","REF51",null,441,458,["WP51-010"],"F-REF"],
    ["R119","reference-feature","REF51",null,443,460,["WP51-010"],"F-REF"],
    ["R120","reference-feature","REF51",null,449,466,["WP51-047"],"F-REF"],
    ["R121","reference-feature","REF51",null,451,468,["WP51-047"],"F-REF"],
    ["R122","reference-feature","REF51",null,458,475,["WP51-047"],"F-REF"],
    ["R123","reference-feature","REF51",null,464,481,["WP51-047"],"F-REF"],
    ["R124","reference-feature","REF51",null,469,486,["WP51-030"],"F-REF"],
    ["R125","reference-feature","REF51",null,471,488,["WP51-040"],"F-REF"],
    ["R126","reference-feature","REF51",null,473,490,["WP51-033"],"F-REF"],
    ["R127","reference-feature","REF51",null,474,491,["WP51-041"],"F-REF"],
    ["R128","reference-feature","REF51",null,478,495,["WP51-041"],"F-REF"],
    ["R129","reference-feature","REF51",null,487,504,["WP51-047"],"F-REF"],
    ["R130","reference-feature","REF51",null,490,507,["WP51-070"],"F-REF"],
    ["R131","reference-feature","REF51",null,493,510,["WP51-070"],"F-REF"],
    ["R132","reference-feature","REF51",null,495,512,["WP51-070"],"F-REF"],
    ["R133","reference-feature","REF51",null,496,513,["WP51-075"],"F-REF"],
    ["R134","reference-feature","REF51",null,498,515,["WP51-075"],"F-REF"],
    ["R135","reference-feature","REF51",null,499,516,["WP51-075"],"F-REF"],
    ["R136","reference-feature","REF51",null,500,517,["WP51-070"],"F-REF"],
    ["R137","reference-feature","REF51",null,502,519,["WP51-070"],"F-REF"],
    ["R138","reference-feature","REF51",null,504,521,["WP51-071"],"F-REF"],
    ["R139","reference-feature","REF51",null,506,523,["WP51-071"],"F-REF"],
    ["R140","reference-feature","REF51",null,510,527,["WP51-072"],"F-REF"],
    ["R141","reference-feature","REF51",null,512,529,["WP51-072"],"F-REF"],
    ["R142","reference-feature","REF51",null,514,531,["WP51-072"],"F-REF"],
    ["R143","reference-feature","REF51",null,518,535,["WP51-073"],"F-REF"],
    ["R144","reference-feature","REF51",null,525,542,["WP51-073"],"F-REF"],
    ["R145","reference-feature","REF51",null,528,545,["WP51-073"],"F-REF"],
    ["R146","reference-feature","REF51",null,531,548,["WP51-073"],"F-REF"],
    ["R147","reference-feature","REF51",null,533,550,["WP51-070"],"F-REF"],
    ["R148","reference-feature","REF51",null,539,556,["WP51-070"],"F-REF"],
    ["R149","reference-feature","REF51",null,542,559,["WP51-070","WP51-075"],"F-REF"],
    ["R150","reference-feature","REF51",null,543,560,["WP51-074"],"F-REF"],
    ["R151","reference-feature","REF51",null,544,561,["WP51-001"],"F-REF"],
    ["R152","reference-feature","REF51",null,549,566,["WP51-030"],"F-REF"],
    ["R153","reference-feature","REF51",null,550,567,["WP51-007","WP51-015"],"F-REF"],
    ["R154","reference-feature","REF51",null,551,568,["WP51-014"],"F-REF"],
    ["R155","reference-feature","REF51",null,554,571,["WP51-019"],"F-REF"],
    ["R156","reference-feature","REF51",null,557,574,["WP51-016"],"F-REF"],
    ["R157","reference-feature","REF51",null,560,577,["WP51-013"],"F-REF"],
    ["R158","reference-feature","REF51",null,563,580,["WP51-018"],"F-REF"],
    ["R159","reference-feature","REF51",null,565,582,["WP51-020"],"F-REF"],
    ["R160","reference-feature","REF51",null,567,584,["WP51-005"],"F-REF"],
    ["R161","reference-feature","REF51",null,567,584,["WP51-079"],"F-REF"],
    ["R162","reference-feature","REF51",null,571,588,["WP51-014"],"F-REF"],
    ["R163","reference-feature","REF51",null,574,591,["WP51-077"],"F-REF"],
    ["R164","reference-feature","REF51",null,576,593,["WP51-075"],"F-REF"],
    ["R165","reference-feature","REF51",null,577,594,["WP51-063"],"F-REF"],
    ["R166","reference-feature","REF51",null,583,600,["WP51-063"],"F-REF"],
    ["R167","reference-feature","REF51",null,585,602,["WP51-063"],"F-REF"],
    ["R168","reference-feature","REF51",null,587,604,["WP51-068"],"F-REF"],
    ["R169","reference-feature","REF51",null,595,612,["WP51-068"],"F-REF"],
    ["R170","reference-feature","REF51",null,598,615,["WP51-068"],"F-REF"],
    ["R171","reference-feature","REF51",null,599,616,["WP51-068"],"F-REF"],
    ["R172","reference-feature","REF51",null,600,617,["WP51-068"],"F-REF"],
    ["R173","reference-feature","REF51",null,606,623,["WP51-065"],"F-REF"],
    ["R174","reference-feature","REF51",null,615,632,["WP51-065"],"F-REF"],
    ["R175","reference-feature","REF51",null,616,633,["WP51-046"],"F-REF"],
    ["R176","reference-feature","REF51",null,621,638,["WP51-046"],"F-REF"],
    ["R177","reference-feature","REF51",null,626,643,["WP51-044"],"F-REF"],
    ["R178","reference-feature","REF51",null,628,645,["WP51-006"],"F-REF"],
    ["R179","reference-feature","REF51",null,631,648,["WP51-035"],"F-REF"],
    ["R180","reference-feature","REF51",null,633,650,["WP51-035"],"F-REF"],
    ["R181","reference-feature","REF51",null,634,651,["WP51-035"],"F-REF"],
    ["R182","reference-feature","REF51",null,640,657,["WP51-048"],"F-REF"],
    ["R183","reference-feature","REF51",null,651,668,["WP51-048"],"F-REF"],
    ["R184","reference-feature","REF51",null,665,682,["WP51-049"],"F-REF"],
    ["R185","reference-feature","REF51",null,670,687,["WP51-049"],"F-REF"],
    ["R186","reference-feature","REF51",null,676,693,["WP51-051"],"F-REF"],
    ["R187","reference-feature","REF51",null,677,694,["WP51-051"],"F-REF"],
    ["R188","reference-feature","REF51",null,679,696,["WP51-051"],"F-REF"],
    ["R189","reference-feature","REF51",null,682,699,["WP51-050"],"F-REF"],
    ["R190","reference-feature","REF51",null,683,700,["WP51-050"],"F-REF"],
    ["R191","reference-feature","REF51",null,685,702,["WP51-050"],"F-REF"],
    ["R192","reference-feature","REF51",null,685,702,["WP51-025"],"F-REF"],
    ["R193","reference-feature","REF51",null,689,706,["WP51-005"],"F-REF"],
    ["R194","reference-feature","REF51",null,692,709,["WP51-069"],"F-REF"],
    ["R195","reference-feature","REF51",null,695,712,["WP51-012"],"F-REF"],
    ["R196","reference-feature","REF51",null,697,714,["WP51-011"],"F-REF"],
    ["R197","reference-feature","REF51",null,698,715,["WP51-037"],"F-REF"],
    ["R198","reference-feature","REF51",null,701,718,["WP51-076"],"F-REF"],
    ["R199","reference-feature","REF51",null,702,719,["WP51-076"],"F-REF"],
    ["R200","reference-feature","REF51",null,705,722,["WP51-042"],"F-REF"],
    ["R201","reference-feature","REF51",null,706,723,["WP51-006"],"F-REF"],
    ["R202","reference-feature","REF51",null,708,725,["WP51-037"],"F-REF"],
    ["X001","front","REF51",null,3,20,["WP51-001","WP51-079"],"F-REF"],
    ["X002","front","REF51",null,3,20,["WP51-001"],"F-REF"],
    ["X003","front","REF51",null,3,20,["WP51-079","WP51-080"],"F-REF"],
    ["X004","front","REF51",null,5,22,["WP51-001","WP51-003"],"F-REF"],
    ["X005","front","REF51",null,6,23,["WP51-080"],"F-REF"],
    ["X006","front","REF51",null,8,25,["WP51-001"],"F-REF"],
    ["X007","front","REF51",null,8,25,["WP51-001","WP51-003"],"F-REF"],
    ["X008","front","REF51",null,9,26,["WP51-001"],"F-REF"],
    ["X009","front","REF51",null,10,27,["WP51-001"],"F-REF"],
    ["X010","front","REF51",null,11,28,["WP51-001"],"F-REF"],
    ["X011","front","REF51",null,11,28,["WP51-013"],"F-REF"],
    ["X012","front","REF51",null,11,28,["WP51-029"],"F-REF"],
    ["X013","front","REF51",null,12,29,["WP51-002"],"F-REF"],
    ["X014","front","REF51",null,12,29,["WP51-002"],"F-REF"],
    ["X015","front","REF51",null,12,29,["WP51-002"],"F-REF"],
    ["X016","front","REF51",null,12,29,["WP51-002"],"F-REF"],
    ["X017","front","REF51",null,12,29,["WP51-002"],"F-REF"],
    ["X018","front","REF51",null,14,31,["WP51-002"],"F-REF"],
    ["X019","front","REF51",null,17,34,["WP51-001"],"F-REF"],
    ["X020","front","REF51",null,18,35,["WP51-001","WP51-008","WP51-019","WP51-020"],"F-REF"],
    ["X021","index","REF51",null,25,42,["WP51-001"],"F-REF"],
    ["X022","index","REF51",null,31,48,["WP51-001"],"F-REF"],
    ["X023","index","REF51",null,713,730,["WP51-082"],"F-REF"],
    ["X024","appendix","REF51",null,715,732,["WP51-025","WP51-082"],"F-APP"],
    ["X025","appendix","REF51",null,721,738,["WP51-055","WP51-056","WP51-082"],"F-APP"],
    ["X026","appendix","REF51",null,725,742,["WP51-013","WP51-082"],"F-APP"],
    ["X027","appendix","REF51",null,729,746,["WP51-058"],"F-APP"],
    ["X028","appendix","REF51",null,741,758,["WP51-082"],"F-APP"],
    ["X029","appendix","REF51",null,763,780,["WP51-073"],"F-APP"],
    ["X030","appendix","REF51",null,765,782,["WP51-032","WP51-082"],"F-APP"],
    ["X031","appendix","REF51",null,769,786,["WP51-003","WP51-082"],"F-APP"],
    ["X032","appendix","REF51",null,777,794,["WP51-060","WP51-062"],"F-APP"],
    ["X033","appendix","REF51",null,783,800,["WP51-060","WP51-062"],"F-APP"],
    ["X034","appendix","REF51",null,791,808,["WP51-060","WP51-062"],"F-APP"],
    ["X035","appendix","REF51",null,887,904,["WP51-060","WP51-062"],"F-APP"],
    ["X036","appendix","REF51",null,893,910,["WP51-001","WP51-082"],"F-APP"],
    ["X037","appendix","REF51",null,897,914,["WP51-080"],"F-APP"],
    ["X038","appendix","REF51",null,905,922,["WP51-082","WP51-078","WP51-080"],"F-APP"],
    ["X039","appendix","REF51",null,913,930,["WP51-066"],"F-APP"],
    ["X040","appendix","REF51",null,921,938,["WP51-081"],"F-APP"],
    ["X041","appendix","REF51",null,931,948,["WP51-081"],"F-APP"],
    ["X042","appendix","REF51",null,961,978,["WP51-078","WP51-080","WP51-081"],"F-APP"],
    ["X043","appendix","REF51",null,963,980,["WP51-060","WP51-062"],"F-APP"],
    ["X044","index","REF51",null,987,1004,["WP51-082"],"F-REF"],
    ["X045","front","WB51",null,"v",6,["WP51-023","WP51-071","WP51-076","WP51-079"],"F-WB"],
    ["X046","index","WB51",null,475,484,["WP51-001"],"F-WB"],
    ["X047","index","WB51",null,478,487,["WP51-001"],"F-WB"],
    ["X048","appendix","WB51",null,482,491,["WP51-023","WP51-080"],"F-APP"],
    ["X049","index","WB51",null,487,496,["WP51-001"],"F-WB"],
    ["RF01","source-context","REF51",null,"iii",6,[],"F-CONTEXT"],
    ["RF02","source-context","REF51",null,"v",8,[],"F-CONTEXT"],
    ["RF03","source-context","REF51",null,"ix",12,[],"F-CONTEXT"],
    ["RF04","source-context","REF51",null,"xiii",16,[],"F-CONTEXT"],
    ["WB01","workbook-lesson","WB51",null,3,12,["WP51-015","WP51-008","WP51-029","WP51-070","WP51-016","WP51-020","WP51-076"],"F-WB1"],
    ["WB02","workbook-lesson","WB51",null,6,15,["WP51-015","WP51-008","WP51-029","WP51-034","WP51-023","WP51-018","WP51-020","WP51-012"],"F-WB1"],
    ["WB03","workbook-lesson","WB51",null,12,21,["WP51-030","WP51-034","WP51-054","WP51-033","WP51-007","WP51-013","WP51-035"],"F-WB1"],
    ["WB04","workbook-lesson","WB51",null,16,25,["WP51-009","WP51-034","WP51-008","WP51-011","WP51-033","WP51-023","WP51-028","WP51-010","WP51-070","WP51-019","WP51-013","WP51-020","WP51-035","WP51-012","WP51-076"],"F-WB1"],
    ["WB05","workbook-lesson","WB51",null,26,35,["WP51-030","WP51-007","WP51-034","WP51-008","WP51-054","WP51-011","WP51-013","WP51-033","WP51-016","WP51-035"],"F-WB1"],
    ["WB06","workbook-lesson","WB51",null,35,44,["WP51-054","WP51-019","WP51-068"],"F-WB1"],
    ["WB07","workbook-lesson","WB51",null,39,48,["WP51-007","WP51-029","WP51-002","WP51-011"],"F-WB2"],
    ["WB08","workbook-lesson","WB51",null,45,54,["WP51-007","WP51-011","WP51-040","WP51-041"],"F-WB2"],
    ["WB09","workbook-lesson","WB51",null,61,70,["WP51-009","WP51-010","WP51-007","WP51-006"],"F-WB2"],
    ["WB10","workbook-lesson","WB51",null,70,79,["WP51-009","WP51-054","WP51-011","WP51-013","WP51-044","WP51-041","WP51-014","WP51-063"],"F-WB2"],
    ["WB11","workbook-lesson","WB51",null,80,89,["WP51-021","WP51-023"],"F-WB2"],
    ["WB12","workbook-lesson","WB51",null,88,97,["WP51-021","WP51-009","WP51-054","WP51-031","WP51-032","WP51-034","WP51-023","WP51-010","WP51-070","WP51-014","WP51-077","WP51-063","WP51-011","WP51-006"],"F-WB2"],
    ["WB13","workbook-lesson","WB51",null,109,118,["WP51-043","WP51-033","WP51-034","WP51-036","WP51-035"],"F-WB3"],
    ["WB14","workbook-lesson","WB51",null,122,131,["WP51-038","WP51-057","WP51-044","WP51-033","WP51-041","WP51-014","WP51-068","WP51-042"],"F-WB3"],
    ["WB15","workbook-lesson","WB51",null,134,143,["WP51-059"],"F-WB3"],
    ["WB16","workbook-lesson","WB51",null,143,152,["WP51-043","WP51-031","WP51-033","WP51-008","WP51-055","WP51-057"],"F-WB3"],
    ["WB17","workbook-lesson","WB51",null,153,162,["WP51-030","WP51-031","WP51-055","WP51-033","WP51-041"],"F-WB3"],
    ["WB18","workbook-lesson","WB51",null,169,178,["WP51-047"],"F-WB3"],
    ["WB19","workbook-lesson","WB51",null,185,194,["WP51-034","WP51-036","WP51-033","WP51-035"],"F-WB4"],
    ["WB20","workbook-lesson","WB51",null,191,200,["WP51-009","WP51-010","WP51-035"],"F-WB4"],
    ["WB21","workbook-lesson","WB51",null,207,216,["WP51-042","WP51-045","WP51-055","WP51-057","WP51-044","WP51-010","WP51-041","WP51-014"],"F-WB4"],
    ["WB22","workbook-lesson","WB51",null,222,231,["WP51-045","WP51-050","WP51-055","WP51-057","WP51-041"],"F-WB4"],
    ["WB23","workbook-lesson","WB51",null,243,252,["WP51-062","WP51-005","WP51-006"],"F-WB4"],
    ["WB24","workbook-lesson","WB51",null,254,263,["WP51-062","WP51-070"],"F-WB4"],
    ["WB25","workbook-lesson","WB51",null,265,274,["WP51-038","WP51-042","WP51-043","WP51-089","WP51-005","WP51-050","WP51-039","WP51-062","WP51-014","WP51-035","WP51-006"],"F-WB5"],
    ["WB26","workbook-lesson","WB51",null,293,302,["WP51-066","WP51-003","WP51-059"],"F-WB5"],
    ["WB27","workbook-lesson","WB51",null,309,318,["WP51-023","WP51-027","WP51-090","WP51-028","WP51-014","WP51-025"],"F-WB5"],
    ["WB28","workbook-lesson","WB51",null,323,332,["WP51-032","WP51-053","WP51-062","WP51-041","WP51-070","WP51-077"],"F-WB5"],
    ["WB29","workbook-lesson","WB51",null,335,344,["WP51-066","WP51-058","WP51-031"],"F-WB5"],
    ["WB30","workbook-lesson","WB51",null,366,375,["WP51-038","WP51-027","WP51-062"],"F-WB5"],
    ["WB31","workbook-lesson","WB51",null,380,389,["WP51-043","WP51-031","WP51-055","WP51-057"],"F-WB6"],
    ["WB32","workbook-lesson","WB51",null,397,406,["WP51-063"],"F-WB6"],
    ["WB33","workbook-lesson","WB51",null,407,416,["WP51-046"],"F-WB6"],
    ["WB34","workbook-lesson","WB51",null,425,434,["WP51-048","WP51-049"],"F-WB6"],
    ["WB35","workbook-lesson","WB51",null,446,455,["WP51-031","WP51-048","WP51-049"],"F-WB6"],
    ["WB36","workbook-lesson","WB51",null,466,475,["WP51-069"],"F-WB6"],
    ["SDK-WP-1","toolkit-section","SDK51","WP",1,14,["FMT51-001"],"F-SDK"],
    ["SDK-WP-3","toolkit-section","SDK51","WP",3,16,["FMT51-001"],"F-SDK"],
    ["SDK-WP-7","toolkit-section","SDK51","WP",7,20,["FMT51-002"],"F-SDK"],
    ["SDK-WP-9","toolkit-section","SDK51","WP",9,22,["FMT51-002"],"F-SDK"],
    ["SDK-WP-17","toolkit-section","SDK51","WP",17,30,["FMT51-003"],"F-SDK"],
    ["SDK-WP-19","toolkit-section","SDK51","WP",19,32,["FMT51-004"],"F-SDK"],
    ["SDK-WP-20","toolkit-section","SDK51","WP",20,33,["FMT51-004"],"F-SDK"],
    ["SDK-WP-21","toolkit-section","SDK51","WP",21,34,["FMT51-004"],"F-SDK"],
    ["SDK-WP-23","toolkit-section","SDK51","WP",23,36,["FMT51-004"],"F-SDK"],
    ["SDK-WP-27","toolkit-section","SDK51","WP",27,40,["FMT51-004"],"F-SDK"],
    ["SDK-WP-36","toolkit-section","SDK51","WP",36,49,["FMT51-005"],"F-SDK"],
    ["SDK-WP-38","toolkit-section","SDK51","WP",38,51,["FMT51-005"],"F-SDK"],
    ["SDK-WP-49","toolkit-section","SDK51","WP",49,62,["FMT51-005"],"F-SDK"],
    ["SDK-WP-55","toolkit-section","SDK51","WP",55,68,["FMT51-005"],"F-SDK"],
    ["SDK-WP-61","toolkit-section","SDK51","WP",61,74,["FMT51-005"],"F-SDK"],
    ["SDK-WP-62","toolkit-section","SDK51","WP",62,75,["FMT51-005"],"F-SDK"],
    ["SDK-WP-64","toolkit-section","SDK51","WP",64,77,["FMT51-005"],"F-SDK"],
    ["SDK-WP-69","toolkit-section","SDK51","WP",69,82,["FMT51-005"],"F-SDK"],
    ["SDK-WP-71","toolkit-section","SDK51","WP",71,84,["FMT51-005"],"F-SDK"],
    ["SDK-WP-74","toolkit-section","SDK51","WP",74,87,["FMT51-005"],"F-SDK"],
    ["SDK-WP-79","toolkit-section","SDK51","WP",79,92,["FMT51-005"],"F-SDK"],
    ["SDK-WP-81","toolkit-section","SDK51","WP",81,94,["FMT51-005"],"F-SDK"],
    ["SDK-WP-85","toolkit-section","SDK51","WP",85,98,["FMT51-005"],"F-SDK"],
    ["SDK-WP-86","toolkit-section","SDK51","WP",86,99,["FMT51-005"],"F-SDK"],
    ["SDK-WP-88","toolkit-section","SDK51","WP",88,101,["FMT51-005"],"F-SDK"],
    ["SDK-WP-89","toolkit-section","SDK51","WP",89,102,["FMT51-005"],"F-SDK"],
    ["SDK-WP-92","toolkit-section","SDK51","WP",92,105,["FMT51-006"],"F-SDK"],
    ["SDK-WP-94","toolkit-section","SDK51","WP",94,107,["FMT51-006"],"F-SDK"],
    ["SDK-WP-97","toolkit-section","SDK51","WP",97,110,["FMT51-006"],"F-SDK"],
    ["SDK-WP-100","toolkit-section","SDK51","WP",100,113,["WP51-026"],"F-SDK"],
    ["SDK-WP-102","toolkit-section","SDK51","WP",102,115,["WP51-065"],"F-SDK"],
    ["SDK-WP-103","toolkit-section","SDK51","WP",103,116,["WP51-031","WP51-073"],"F-SDK"],
    ["SDK-PL-1","toolkit-section","SDK51","PL",1,121,["WP51-065"],"F-SDK"],
    ["SDK-PL-2","toolkit-section","SDK51","PL",2,122,["WP51-065"],"F-SDK"],
    ["SDK-PL-14","toolkit-section","SDK51","PL",14,134,["WP51-065"],"F-SDK"],
    ["SDK-PL-15","toolkit-section","SDK51","PL",15,135,["WP51-065"],"F-SDK"],
    ["SDK-PL-16","toolkit-section","SDK51","PL",16,136,["WP51-065"],"F-SDK"],
    ["SDK-PL-17","toolkit-section","SDK51","PL",17,137,["WP51-065"],"F-SDK"],
    ["SDK-PL-18","toolkit-section","SDK51","PL",18,138,["WP51-065"],"F-SDK"],
    ["SDK-PL-19","toolkit-section","SDK51","PL",19,139,["WP51-065"],"F-SDK"],
    ["SDK-OF-1","toolkit-section","SDK51","OF",1,146,["WP51-078"],"F-SDK"],
    ["SDK-OF-2","toolkit-section","SDK51","OF",2,147,["WP51-078"],"F-SDK"],
    ["SDK-OF-3","toolkit-section","SDK51","OF",3,148,["WP51-078"],"F-SDK"],
    ["SDK-OF-4","toolkit-section","SDK51","OF",4,149,["WP51-078"],"F-SDK"],
    ["SDK-OF-5","toolkit-section","SDK51","OF",5,150,["WP51-078"],"F-SDK"],
    ["SDK-OF-6","toolkit-section","SDK51","OF",6,151,["WP51-078"],"F-SDK"],
    ["SDK-OF-7","toolkit-section","SDK51","OF",7,152,["WP51-078"],"F-SDK"],
    ["SDK-OF-8","toolkit-section","SDK51","OF",8,153,["WP51-078"],"F-SDK"],
    ["SDK-OF-9","toolkit-section","SDK51","OF",9,154,["WP51-078"],"F-SDK"],
    ["SDK-OF-10","toolkit-section","SDK51","OF",10,155,["WP51-078"],"F-SDK"],
    ["SDK-OF-11","toolkit-section","SDK51","OF",11,156,["WP51-078"],"F-SDK"],
    ["SDK-OF-12","toolkit-section","SDK51","OF",12,157,["WP51-078"],"F-SDK"],
    ["SDK-OF-13","toolkit-section","SDK51","OF",13,158,["WP51-078"],"F-SDK"],
    ["SDK-OF-14","toolkit-section","SDK51","OF",14,159,["WP51-078"],"F-SDK"],
    ["SDK-OF-15","toolkit-section","SDK51","OF",15,160,["WP51-078"],"F-SDK"],
    ["SDK-OF-16","toolkit-section","SDK51","OF",16,161,["WP51-078"],"F-SDK"],
    ["SDK-OF-18","toolkit-section","SDK51","OF",18,163,["WP51-078"],"F-SDK"],
    ["SDK-OF-22","toolkit-section","SDK51","OF",22,167,["WP51-078"],"F-SDK"],
    ["SDK-OF-25","toolkit-section","SDK51","OF",25,170,["WP51-078"],"F-SDK"],
    ["SDK-OF-26","toolkit-section","SDK51","OF",26,171,["WP51-078"],"F-SDK"],
    ["SDK-OF-27","toolkit-section","SDK51","OF",27,172,["WP51-078"],"F-SDK"],
    ["SDK-OF-28","toolkit-section","SDK51","OF",28,173,["WP51-078"],"F-SDK"],
    ["SDK-OF-35","toolkit-section","SDK51","OF",35,180,["WP51-078"],"F-SDK"],
    ["SDK-OF-36","toolkit-section","SDK51","OF",36,181,["WP51-078"],"F-SDK"],
    ["SDK-OF-42","toolkit-section","SDK51","OF",42,187,["WP51-078"],"F-SDK"],
    ["SDK-OF-50","toolkit-section","SDK51","OF",50,195,["WP51-078"],"F-SDK"],
    ["SDK-DR-1","toolkit-section","SDK51","DR",1,204,["WP51-055","WP51-056"],"F-SDK"],
    ["SDK-DR-5","toolkit-section","SDK51","DR",5,208,["WP51-055","WP51-056"],"F-SDK"],
    ["SDK-DR-19","toolkit-section","SDK51","DR",19,222,["WP51-055","WP51-056"],"F-SDK"],
    ["SDK-DR-25","toolkit-section","SDK51","DR",25,228,["WP51-055","WP51-056"],"F-SDK"],
    ["SDK-DP-1","toolkit-section","SDK51","DP",1,233,["WP51-065"],"F-SDK"],
    ["SDK-DP-2","toolkit-section","SDK51","DP",2,234,["WP51-065"],"F-SDK"],
    ["SDK-DP-3","toolkit-section","SDK51","DP",3,235,["WP51-065"],"F-SDK"],
    ["SDK-DP-51","toolkit-section","SDK51","DP",51,283,["WP51-065"],"F-SDK"],
    ["SDK-DV-1","toolkit-section","SDK51","DV",1,285,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-2","toolkit-section","SDK51","DV",2,286,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-9","toolkit-section","SDK51","DV",9,293,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-12","toolkit-section","SDK51","DV",12,296,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-16","toolkit-section","SDK51","DV",16,300,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-19","toolkit-section","SDK51","DV",19,303,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-24","toolkit-section","SDK51","DV",24,308,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-29","toolkit-section","SDK51","DV",29,313,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-33","toolkit-section","SDK51","DV",33,317,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-34","toolkit-section","SDK51","DV",34,318,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DV-48","toolkit-section","SDK51","DV",48,332,["WP51-005","WP51-004","WP51-071","WP51-073"],"F-SDK"],
    ["SDK-DOS-1","toolkit-section","SDK51","DOS",1,337,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-DOS-6","toolkit-section","SDK51","DOS",6,342,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-DOS-7","toolkit-section","SDK51","DOS",7,343,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-DOS-10","toolkit-section","SDK51","DOS",10,346,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-DOS-12","toolkit-section","SDK51","DOS",12,348,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-DOS-14","toolkit-section","SDK51","DOS",14,350,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-DOS-18","toolkit-section","SDK51","DOS",18,354,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-OS2-1","toolkit-section","SDK51","OS2",1,357,["WP51-078","WP51-080"],"F-SDK"],
    ["SDK-OS2-6","toolkit-section","SDK51","OS2",6,362,["WP51-078","WP51-080"],"F-SDK"],
    ["SDK-OS2-7","toolkit-section","SDK51","OS2",7,363,["WP51-078","WP51-080"],"F-SDK"],
    ["SDK-OS2-8","toolkit-section","SDK51","OS2",8,364,["WP51-078","WP51-080"],"F-SDK"],
    ["SDK-OS2-9","toolkit-section","SDK51","OS2",9,365,["WP51-078","WP51-080"],"F-SDK"],
    ["SDK-WPW-1","toolkit-section","SDK51","WPW",1,368,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-2","toolkit-section","SDK51","WPW",2,369,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-3","toolkit-section","SDK51","WPW",3,370,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-6","toolkit-section","SDK51","WPW",6,373,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-8","toolkit-section","SDK51","WPW",8,375,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-9","toolkit-section","SDK51","WPW",9,376,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-14","toolkit-section","SDK51","WPW",14,381,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-16","toolkit-section","SDK51","WPW",16,383,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-17","toolkit-section","SDK51","WPW",17,384,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-22","toolkit-section","SDK51","WPW",22,389,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-24","toolkit-section","SDK51","WPW",24,391,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-34","toolkit-section","SDK51","WPW",34,401,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-37","toolkit-section","SDK51","WPW",37,404,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-39","toolkit-section","SDK51","WPW",39,406,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-40","toolkit-section","SDK51","WPW",40,407,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-44","toolkit-section","SDK51","WPW",44,411,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-WPW-46","toolkit-section","SDK51","WPW",46,413,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-UNX-1","toolkit-section","SDK51","UNX",1,420,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-UNX-6","toolkit-section","SDK51","UNX",6,425,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-UNX-9","toolkit-section","SDK51","UNX",9,428,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-UNX-11","toolkit-section","SDK51","UNX",11,430,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-UNX-15","toolkit-section","SDK51","UNX",15,434,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-UNX-19","toolkit-section","SDK51","UNX",19,438,["WP51-059","WP51-078"],"F-SDK"],
    ["SDK-AP-1","toolkit-section","SDK51","AP",1,500,["WP51-077"],"F-SDK"],
    ["SDK-AP-11","toolkit-section","SDK51","AP",11,510,["WP51-003"],"F-SDK"],
    ["SDK-AP-13","toolkit-section","SDK51","AP",13,512,["WP51-005","WP51-031"],"F-SDK"],
    ["SDK-AP-16","toolkit-section","SDK51","AP",16,515,["WP51-031","WP51-073"],"F-SDK"],
    ["SDK-AP-17","toolkit-section","SDK51","AP",17,516,["WP51-066"],"F-SDK"],
    ["SDK-AP-19","toolkit-section","SDK51","AP",20,519,["WP51-066"],"F-SDK"],
    ["SDK-F1","source-context","SDK51",null,"TOC",4,[],"F-CONTEXT"],
    ["SDK-F2","source-context","SDK51",null,"TOC",4,[],"F-CONTEXT"],
    ["SDK-F3","source-context","SDK51",null,"TOC",4,[],"F-CONTEXT"],
    ["SDK-F4","source-context","SDK51",null,"TOC",4,[],"F-CONTEXT"],
    ["SDK-F5","source-context","SDK51",null,"TOC",4,[],"F-CONTEXT"],
    ["M1","menu-root","REF51",null,893,910,["WP51-019","WP51-020","WP51-025","WP51-065","WP51-024","WP51-023","WP51-090","WP51-070","WP51-077","WP51-003","WP51-078","WP51-029"],"F-MENU"],
    ["M2","menu-root","REF51",null,893,910,["WP51-010","WP51-011","WP51-009","WP51-027","WP51-015","WP51-042","WP51-006","WP51-013"],"F-MENU"],
    ["M3","menu-root","REF51",null,894,911,["WP51-014","WP51-008"],"F-MENU"],
    ["M4","menu-root","REF51",null,894,911,["WP51-033","WP51-043","WP51-048","WP51-049","WP51-064","WP51-045","WP51-034","WP51-035","WP51-040","WP51-046"],"F-MENU"],
    ["M5","menu-root","REF51",null,895,912,["WP51-050","WP51-089","WP51-051","WP51-052","WP51-027"],"F-MENU"],
    ["M6","menu-root","REF51",null,895,912,["WP51-068","WP51-069","WP51-059","WP51-054","WP51-047","WP51-062","WP51-063","WP51-017"],"F-MENU"],
    ["M7","menu-root","REF51",null,896,913,["WP51-031","WP51-030","WP51-070","WP51-066"],"F-MENU"],
    ["M8","menu-root","REF51",null,896,913,["WP51-055","WP51-058","WP51-057"],"F-MENU"],
    ["M9","menu-root","REF51",null,896,913,["WP51-002","WP51-001"],"F-MENU"]
  ],
  "contents_counts":{"reference-feature":202,"front":21,"index":7,"appendix":21,"source-context":9,"workbook-lesson":36,"toolkit-section":126,"menu-root":9},
  "reference_toc_counts":{"42":45,"43":48,"44":48,"45":48,"46":13},
  "workbook_feature_list_pdf":{"WB01":487,"WB02":487,"WB03":487,"WB04":487,"WB05":487,"WB06":487,"WB07":488,"WB08":488,"WB09":488,"WB10":488,"WB11":488,"WB12":488,"WB13":488,"WB14":488,"WB15":488,"WB16":489,"WB17":489,"WB18":489,"WB19":489,"WB20":489,"WB21":489,"WB22":489,"WB23":489,"WB24":489,"WB25":489,"WB26":489,"WB27":490,"WB28":490,"WB29":490,"WB30":490,"WB31":490,"WB32":490,"WB33":490,"WB34":490,"WB35":490,"WB36":490},
  "workbook_correction_pdf_pages":{"WB01":[],"WB02":[1,2],"WB03":[],"WB04":[2],"WB05":[],"WB06":[2],"WB07":[2],"WB08":[],"WB09":[],"WB10":[2],"WB11":[1,2],"WB12":[2,3],"WB13":[3],"WB14":[3],"WB15":[],"WB16":[],"WB17":[],"WB18":[],"WB19":[3],"WB20":[3,4],"WB21":[4],"WB22":[4],"WB23":[4],"WB24":[4],"WB25":[4,5],"WB26":[5],"WB27":[],"WB28":[5,6],"WB29":[7],"WB30":[7],"WB31":[8],"WB32":[],"WB33":[8],"WB34":[8],"WB35":[8],"WB36":[]},
  "pagination_exceptions":{"SDK-AP-19":{"toc_section":"AP","toc_printed_start":19,"toc_target_pdf":518,"actual_printed_start":20,"actual_pdf_start":519,"basis":"actual heading and footer visually verified; TOC target is otherwise blank"}}
}
```
<!-- WP05_AUDIT_END -->

From the repository root, verify the recorded inputs, all row/group/case links,
all 36 starts, source bounds, menu/appendix counts and exact SDK contents keys:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json, re, collections
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/coverage-concordance.md')
text = p.read_text()
a = text.split('<!-- WP05_AUDIT_BEGIN -->',1)[1]
a = json.loads(a.split('```json\n',1)[1].split('\n```',1)[0])
for src in a['source_inputs']:
    assert hashlib.sha256(Path(src['path']).read_bytes()).hexdigest() == src['sha256']
inv = {x['id']:x for x in json.loads(Path('docs/research/feature-inventory.json').read_text())}
cases = {x['id']:x for x in json.loads(Path('docs/research/command-scenarios.json').read_text())}
sources = {x['id']:x for x in json.loads(Path('docs/research/sources.json').read_text())}
rows = [dict(zip(a['row_columns'],r)) for r in a['rows']]
assert len({r['id'] for r in rows}) == len(rows) == 431
assert collections.Counter(r['kind'] for r in rows) == a['contents_counts']
assert len(inv) == a['registry_counts']['feature_groups'] == 91
assert len(cases) == a['registry_counts']['scenarios'] == 236
assert sum(c['oracle_status']=='partially-observed' for c in cases.values()) == 53
assert sum(c['oracle_status']=='not-run' for c in cases.values()) == 183
seen = set()
for row in rows:
    assert 1 <= row['pdf_start'] <= sources[row['source_id']]['pdf_pages']
    assert all(g in inv for g in row['inventory_ids'])
    seen.update(row['inventory_ids'])
    candidate = {c for g in row['inventory_ids'] for c in inv[g]['command_scenario_ids']}
    assert candidate <= cases.keys()
    for cid in candidate:
        assert set(cases[cid]['feature_ids']) & set(row['inventory_ids'])
        for path in cases[cid]['evidence_paths']:
            assert Path(path).exists()
    if row['source_id']=='REF51' and isinstance(row['printed_start'],int):
        assert row['pdf_start']==row['printed_start']+17
    if row['source_id']=='WB51' and isinstance(row['printed_start'],int):
        assert row['pdf_start']==row['printed_start']+9
assert seen == inv.keys()
assert {m for m in re.findall(r'CMD51-\d{3}',text)} <= cases.keys()
wb = [r for r in rows if r['kind']=='workbook-lesson']
assert {int(r['id'][2:]) for r in wb} == set(range(1,37))
old = Path('docs/research/workbook-map.md').read_text()
for r in wb:
    n = int(r['id'][2:])
    m = re.search(r'\| '+str(n)+r' \| .*?p\. (\d+); PDF (\d+)',old)
    assert m and (int(m[1]),int(m[2])) == (r['printed_start'],r['pdf_start'])
    assert a['workbook_feature_list_pdf'][r['id']] == (487 if n<=6 else 488 if n<=15 else 489 if n<=26 else 490)
    assert all(1<=pg<=8 for pg in a['workbook_correction_pdf_pages'][r['id']])
sdk = Path('research/cache/toolkit.txt').read_text().split('\f')
keys = set()
for page in (4,5,6):
    keys.update(re.findall(r'((?:WP|PL|OF|DR|DP|DV|DOS|OS2|WPW|UNX|AP)-\d+)\s*$',sdk[page-1],re.M))
assert {'SDK-'+k for k in keys} == {r['id'] for r in rows if r['kind']=='toolkit-section'}
assert len(keys)==126
exception = next(r for r in rows if r['id']=='SDK-AP-19')
assert (exception['printed_start'],exception['pdf_start']) == (20,519)
assert 'Japanese Version' in sdk[518]
ref = [r for r in rows if r['kind']=='reference-feature']
assert len(ref)==202 and len([r for r in rows if r['kind']=='menu-root'])==9
assert len([r for r in rows if r['kind']=='appendix' and r['source_id']=='REF51'])==20
print('WP05 inputs, 431 dispositions, source locators and canonical links validated')
PY
python3 scripts/render-inventory.py --check
python3 scripts/render-scenarios.py --check
```

No original runs or application tests are claimed by this documentary audit.
The actual configured project regression command must pass at review handoff;
Go build/test/vet execute only when real Go packages exist in that checkout.
A planning-lane skip is not a claim about another implementation lane.

Author validation completed: the embedded source/ID/locator audit and both catalogue checks pass. The genuine project regression runner exits zero; Go package discovery succeeds and build/test/vet are explicitly skipped because no Go packages exist in this planning checkout. No original probe, canonical registry, executable queue, code or raw evidence was changed.
