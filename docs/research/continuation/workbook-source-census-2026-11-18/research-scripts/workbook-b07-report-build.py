from pathlib import Path
import json,itertools,hashlib
out=Path('/tmp/wordling-mission1-closeout-20261118');d=json.loads((out/'workbook-b07-source-census.json').read_text());c=d['counts']
lines=['# WB-B07 source census — lessons 19–21','',
'Documentary research for the Mission 1 source-expansion reviewer, under resolved `researcher-robbie` and action `research`. I am Researcher Robbie: I investigate unknowns and return structured evidence; I do not implement production code or make final decisions. No repository, index, Git ref, Op, lifecycle, runtime, original/candidate application, VM, Mac, private installed resource, or acceptance record was mutated. Parent owns the active mission and preservation commit. All 49 families remain open; WP103 remains unregistered and incomplete.','',
'**218 original numbered source steps:** WB19 38, WB20 82, WB21 98, across 27 section-local sequences. Companion JSON preserves **57 explicit menu alternatives** (10 / 18 / 29), **three physical mouse alternatives**, **30 context/resource/repeat/optional/ambiguity branches**, **three additional table rows**, and **seven publisher notice blocks**. These categories are not additive executable cases. Repeated targets remain explicit without inflating original source-step counts. The previous 18 lessons’ 856 steps are documentary source counts; the cumulative 21-lesson count is 1,074, with no execution or acceptance implied.','',
'## Sources and locator integrity','',
'- WB51: `research/cache/WPDOS51Workbook.pdf`, edition `WKUS1WP51-11/89`; SHA256 `868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d`. Registered public source: [WordPerfect 5.1 Workbook](https://mendelson.org/wpdos/WPDOS51Workbook.pdf).',
'- WBC51: `research/cache/WP51WKBK.pdf`; SHA256 `7e7b87786d4ac748af6603a98d084c38137a6e723954540b1153ad6ed64e7a0b`. The registered publisher notice has later 12/90 and 08/91 changes. Its internal header says LetterPerfect 1.0 Reference dated 11/90 despite workbook lesson content; retain that provenance mismatch.',
'- WB19 printed 185–190 / physical PDF 194–199; WB20 printed 191–206 / PDF 200–215; WB21 printed 207–221 / PDF 216–230. All 37 pages and notice physical pages 3–4 were rendered and visually inspected; no WB22 expansion.',
'- Each numbered action and menu/mouse alternative retains physical and printed page, section and original number, physical layout-text line, first-line SHA256, and relevant span hash. Context branches retain exact line spans and page hashes. Fresh single-page extraction independently rechecked all 288 numbered/alternative/row/notice first-line locators. All 22 pinned source, canonical mapping, audit, coverage, metadata and prior-census inputs stayed unchanged.',
'- Seven OCR source-number labels were visually normalized: PDF196:12 S→8; 197:15 S→5; 202:36 S→5; 209:5 S→8; 212:37 S→8; 218:7 S→8; 228:6 a→8. Nine mouse-icon or prose matches were excluded. All 27 remaining sequences are exactly 1 through N.',
'- The first invocation of the requested older PDF skill path failed because that version is absent; the installed current PDF skill at `pdf/26.1117.12345/skills/pdf/SKILL.md` was loaded instead. Spec Kitty profile and action governance resolved through the designated repaired CLI with SaaS sync disabled; required compatibility and roadmap context was read. No dispatch Op was opened by this read-only subtask.','',
'The 1989 workbook and later publisher notices are documentary evidence, not a pristine March 1992 shipping set or observations of that executable. Native file identity, round-trip preservation, exact cursor/owner semantics, printer metrics, and every original/candidate journey remain pending.','',
'## Complete numbered-source inventory','',
'Exact individual paraphrased actions and source hashes are in JSON; source numbering restarts at each section.','',
'| Lesson | Original section | Steps | Physical PDF pages | Family dependencies |','|---|---|---:|---|---|']
for(lesson,section),group in itertools.groupby(d['numbered_steps'],lambda s:(s['lesson'],s['source_section'])):
 a=list(group);lines.append(f"| {lesson} | {section} | {len(a)} | {a[0]['pdf_page']}–{a[-1]['pdf_page']} | {', '.join(a[0]['family_dependencies'])} |")
lines+=['','## Context, optional exercises, resources and unresolved branches','']
for b in d['context_branches']:
 loc='; '.join(f"PDF{x['pdf_page']}/printed{x['printed_page']}:lines{x['physical_text_first_line']}–{x['physical_text_last_line']}"for x in b['primary_source_page_locators'])
 lines += [f"**{b['lesson']} — {b['topic']}** ({loc}; {', '.join(b['family_dependencies'])}). {b['branch_paraphrase']}",'']
lines+=['## Repeated exercises and scalar inputs','',
'WB19 first-line indentation covers every remaining report paragraph except titles and existing table; the source does not state a finite paragraph count. That count cannot be derived without opening the original draft, which this task prohibits. The two quotation targets each receive an additional bilateral indent. Single-spacing step 8 covers both quotations and the Operating Expenses table: each region gets a start owner at 1 and a trailing reset at 1.5. The JSON records these templates separately.','',
'WB20 table-entry step 3 includes these exact remaining rows, with generated dot leaders and tab-separated values. Initial first-quarter input is Retail $500,000.00, Mail Order $2,400,000.00; later column Move intentionally reverses order.','',
'| Original row | Retail amount | Mail Order amount | Locator |','|---|---:|---:|---|']
for row in d['structured_exercise_rows']:lines.append(f"| {row['original_row_label']} | {row['retail']} | {row['mail_order']} | PDF203 / printed194 / line{row['source_line_number']} |")
lines+=['',
'WB21 step 17 repeats footer-creation steps 3–11 for Footer B / Even Pages and the page number at the left margin. These are nine referenced source operations within one numbered repeat step, not nine additional source numbers. The source omits a full revised typing sequence for the left-number arrangement; preserve that ambiguity. A recovery paragraph directs deleting a wrongly created Footer A or Odd Pages owner and trying again.','',
'Footnote citation input is retained as bibliographic fields with exact source-span hash at PDF221 / printed212 / lines17–18; the work title is underlined. Source prose is not republished. The earlier Ibid reference uses page5; editing note1 replaces page39 with40. These note identifiers and page references are separate values.','',
'## Publisher notice reconciliation','',
'| Lesson | Notice PDF:lines | Manual date | Notice-declared workbook pages | Documentary change / applicability |','|---|---|---|---|']
for a in d['source_corrections']:
 lines.append(f"| {a['lesson']} | {a['pdf_page']}:{a['source_line_number']}–{a['source_line_end']} | {a['manual_date']} | {a['notice_declared_workbook_pages']} | {a['correction_paraphrase']} {a['applicability_uncertainty']} |")
lines+=['','No correction silently replaces the original 1989 step, screenshot, code label, or page locator. In particular, the printed207 Page Up/Page Down key-label reversal is visually present and has no identified notice correction here.','',
'## Resource provenance and open execution','',
'Only existing installed-file **metadata** was read:']
for m in d['registered_resource_metadata_only']:lines.append(f"- `{m['path']}`: {m['size']} bytes; SHA256 `{m['sha256']}`.")
lines+=['',
'No resource file was opened or tested. REPORT.WKB is the supplied original draft; learner REPORT evolves through lessons19–21 and becomes later input. Existing index, generated-list, footnote, endnote and formatting owners visible in illustrations must be preserved; their presence in a picture does not establish decoder support, availability, or execution.','',
'No new coverage/runtime IDs, recipes, registrations, source omissions, audit/matrix promotions, or completion claims were introduced. Menu refusal/Cancel, absent/invalid resources, original teaching-input mismatches, note errors, physical focus/selection cancellation, Move cancellation, save/overwrite refusal and host I/O failure remain original/candidate obligations. The source does not supply most exact failures, so this report does not invent messages or executed outcomes.','',
'## Reproduction and verification','',
'All outputs are under `/tmp/wordling-mission1-closeout-20261118/`: `workbook-b07-source-extract.txt`, `workbook-b07-corrections.txt`, `workbook-b07-pages/`, pinned `workbook-b07-input-hashes.json`, and bounded `workbook-b07-census-build.py` / `workbook-b07-report-build.py`. Page images, contact sheets and notice renders are hash-pinned in JSON. Re-running the census builder independently re-extracts each recorded first line, checks the exact numbered sequences and verifies all pinned inputs; it writes only the designated scratch JSON. The report builder writes only the scratch Markdown. Parent will preserve approved documentary artifacts and reproducibility scripts at a quiet point.','']
(out/'workbook-b07-source-census.md').write_text('\n'.join(lines))
print('Report written',len(lines),'lines')
