from pathlib import Path
import json,itertools,hashlib,subprocess
out=Path('/tmp/wordling-mission1-closeout-20261118');root=Path('/home/lynn/projects/wordling');j=json.loads((out/'workbook-b06-source-census.json').read_text())
md='''# WB-B06 source census — lessons 16–18

Documentary research only, under the established Researcher Robbie profile/action `research`. Scope is canonical WB-B06: newsletter lessons16–17 and report-outline lesson18. No IDs, registration, status, recipe, repository/index/Git/runtime, private asset/guard, original execution, VM or Mac actions occurred. WP103 remains unregistered/incomplete and all original/candidate execution and acceptance remain pending.

**225 original numbered steps:** WB16 46, WB17 92, WB18 87. Companion JSON also contains **64 explicit menu alternatives** (14 /32 /18), **two physical mouse alternatives**, **33 context/resource/optional/ambiguity branches**, and **nine unnumbered final-diagram entries**. These are documentary counts, not accepted cases. Source numbering and displayed outline labels are retained without allocating new runtime coverage IDs.

## Registered sources, locator integrity and visual checks

- WB51 `research/cache/WPDOS51Workbook.pdf`, edition `WKUS1WP51-11/89`, SHA256 `868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d`.
- WBC51 `research/cache/WP51WKBK.pdf`, SHA256 `7e7b87786d4ac748af6603a98d084c38137a6e723954540b1153ad6ed64e7a0b`. Registered notice text was searched; it contains no notice for lessons16–18. Do not apply unrelated lesson corrections to fill a gap.
- WB16 printed143–152 / physical PDF152–161; WB17 printed153–168 / PDF162–177; WB18 printed169–184 / PDF178–193. All42 pages rendered and visually inspected. PDF193 additionally rendered at2400px to read the otherwise damaged OCR final-outline diagram. No lesson19 expansion.
- `workbook-b06-source-extract.txt` retains layout text; `workbook-b06-pages/` retains renders/contact sheets. Each numbered action/menu/mouse record has an exact physical page, printed page, section-local source number, extracted-text physical line and first-line SHA256. Fresh single-page extraction independently checked **all291** step/alternative hashes. Context branches retain precise cited page text spans and page hashes. Final diagram entries retain original displayed numbering, levels, source region, detail-render path/hash and pending execution.
- Nine OCR `S` labels were visually normalized only at the source positions: PDF154:3→8,166:45→5,172:32→8,174:17→8,176:4→8,184:40→5,185:42→8,189:27→8,192:3→8. Seven menu/footer OCR false positives were excluded, with all section-number sequences then independently checked.

The1989 workbook and later notices are versioned documentary sources, not proof of a pristine March1992 shipping set or that executable’s behavior. Installed-files resource metadata is retained only as existing provenance; no actual private installed resource was opened, probed or used.

## Complete numbered-source inventory

Original numbers restart by section. Exact individual actions and physical line hashes are in JSON.

| Lesson | Original section | Steps | Physical PDF pages | Current family links |
|---|---|---:|---|---|
'''
for(l,s),rows in itertools.groupby(j['numbered_steps'],lambda x:(x['lesson'],x['source_section'])):
 r=list(rows);ps=sorted({x['pdf_page']for x in r});pr=str(ps[0])if len(ps)==1 else f'{ps[0]}–{ps[-1]}'
 md+=f"| {l} | {s} | {len(r)} | {pr} | {', '.join(r[0]['family_dependencies'])} |\n"
md+='\n## Context, resources, optional exercises and unresolved branches\n\n'
for b in j['context_branches']:
 md+=f"**{b['lesson']} — {b['topic']}** (physical PDF{','.join(str(x)for x in b['pdf_pages'])}; {', '.join(b['family_dependencies'])}). {b['branch_paraphrase']}\n\n"
md+='''## Unnumbered final-outline exercise

WB18 printed184 / PDF193 instructs completion from the illustration, after the numbered steps have created “The Next Fifty Years” and “Expanding Markets.” The2400px rendering makes these remaining entries legible. The labels below are the book’s original outline labels, **not new runtime IDs**. Each remains unexecuted.

| Original outline label | Level | Remaining source heading |
|---|---:|---|
'''
for x in j['unnumbered_diagram_exercise_entries']:md+=f"| {x['original_outline_label']} | {x['level']} | {x['text']} |\n"
md+='''
Their parent relationships and the earlier two sections must remain intact. Enter inserts number/style plus indent, while Tab/Shift-Tab change levels. The source’s Backspace-style-owner-and-hard-return correction route remains separate from successful entry. Final-diagram capitalization varies from numbered heading text; exact future inputs must bind the chosen primary locator, not silently normalize visual variants. The introductory handwritten diagram on printed169 is context; it does not replace the clearer final exercise illustration or the numbered inputs.

## Family mapping, resources and evidence status

Canonical lesson metadata is preserved. Detailed current-family links refine it: G1 handles page/paragraph-anchored Figure owners, linked WPG, caption context, wrap and repeated-header interactions; G3 handles the masthead horizontal graphics line; L6 handles actual Newspaper flow and column-relative Hard Page/navigation; L1/P1/P3 handle font selection/fallback, printer resources and preview. D1 handles paragraph-number definitions and embedded per-level Open Outline Styles. E1/E3 carry exact native deletion/history and copy/restore; I3/I4 carry physical selection and context/status/navigation; Q1/Q2/Q3 retain full source leaves, journeys/physical input and native/save provenance.

Canonical L7 references do not establish a selected Parallel Columns exercise here: the instructions select Newspaper columns. No family is excluded or closed merely because these lessons do not select it. Eight available outline levels, pictured attribute lists and unselected style-list/library commands likewise remain wider pending scope, not inferred completed actions.

Existing sampled evidence stays separate: audit CMD51-168 Newspaper columns, CMD51-174 Figure graphics box, CMD51-176 horizontal graphics line and CMD51-160 initial base font remain unimplemented. CMD51-118 named-style creation remains partial; its compact paired Bold sample does not establish the Open Outline Styles and native owner transformations here. CMD51-171’s verified captured Roman/letter levels explicitly leaves other outline types and family commands open. No green primitive or cached metadata accepts the225 steps, final diagram exercise, full native reopen, print or physical-input journeys.

Future bounded execution needs the original teaching NEWSTEXT.WKB and OUTLINE.WKB, GRAPH.WPG, explicit WORKBOOK.PRS, real font/printer metrics/capabilities, declared graphics/display profile and a mouse for the alternate physical routes. Learner NEWSLTR before/afterWB17 and learner OUTLINE must be distinct from those teaching inputs. Source says the created outline-style list is saved with its document; this requires genuine native production/reopen and retained style contents, not just equivalent visible text. No resource acquisition, private path inspection, source conversion, fixture execution or printer operation was performed.

The source width mismatch on printed148–149 stays unresolved:1.25–4 and4.5–7.25 imply2.75in each, while prose says3.25in. The visual diagram confirms the endpoints. No guessed repair is made to source or implementation and no target executable result is assumed.

## Preservation

Historical WP21 core55 steps /12 contexts /9 menu alternatives is unchanged. Prior B01–B05 reports, seven canonical source/map/audit/ledger/metadata files, source PDFs and registered text pins were checked unchanged. JSON records all inherited hashes and exact page hashes. Only new artifacts under `/tmp/wordling-mission1-closeout-20261118/` were written; the parent owns later preservation at the WP104 quiet point. WP103 and full mission acceptance remain open.
'''
(out/'workbook-b06-source-census.md').write_text(md)
old=json.loads((out/'workbook-b05-source-census.json').read_text())
for p,h in old['immutable_input_hashes'].items():assert j['immutable_input_hashes'][p]==h,p
for p,h in old['prior_census_hashes'].items():assert j['prior_census_hashes'][p]==h,p
fixed={'research/cache/WPDOS51Workbook.pdf':'868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d','research/cache/WP51WKBK.pdf':'7e7b87786d4ac748af6603a98d084c38137a6e723954540b1153ad6ed64e7a0b','research/cache/workbook.txt':'4a99b406886f1e128ab673c9cefddc83ca9f53ddbc8dcfd621e38b7afe79ecce','research/cache/workbook-corrections.txt':'22217add5a9c6ee3236c466462d72ed7b50e473274c95ac0b066d2b3b17112b7'}
for p,h in{**j['immutable_input_hashes'],**fixed}.items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h,p
for p,h in j['prior_census_hashes'].items():assert hashlib.sha256((out/p).read_bytes()).hexdigest()==h,p
# Check all scoped page hashes and context spans against fresh per-page extraction, not only step lines.
for pg in range(152,194):
 raw=subprocess.check_output(['pdftotext','-f',str(pg),'-l',str(pg),'-layout',str(root/'research/cache/WPDOS51Workbook.pdf'),'-']).decode().split('\f')[0]
 assert hashlib.sha256(raw.encode()).hexdigest()==j['pdf_page_extracted_text_sha256'][str(pg)],pg
for p in('workbook-b06-source-census.md','workbook-b06-source-census.json'):print(p,hashlib.sha256((out/p).read_bytes()).hexdigest())
