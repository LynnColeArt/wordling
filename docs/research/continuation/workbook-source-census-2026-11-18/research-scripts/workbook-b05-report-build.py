from pathlib import Path
import json,hashlib,itertools,re,subprocess
out=Path('/tmp/wordling-mission1-closeout-20261118');root=Path('/home/lynn/projects/wordling');jp=out/'workbook-b05-source-census.json';j=json.loads(jp.read_text())
paragraphs=[
'Retrieve original MUSICBOX.WKB, not the edited MUSICBOX or MUSICBOX.LTR. The source starts with a 1in top margin; add returns until status Line is 2in. Backspace removes excess returns. This is blank-line insertion, distinct from the later absolute Advance Line exercise.',
'Line Height may be exact or Auto using the largest font on a line; Line Spacing multiplies height by 1.5 in this exercise. The address before the owner stays single-spaced; subsequent content changes. Other multipliers mentioned in prose are examples, not numbered exercises.',
'Single spacing affects text after the new owner until another 1.5 owner restores the body setting. Put the reset at the final list-line end so it stays with that list during edits. Steps12–14 require repeating the taught operation for the second list, representatives and closing without supplying every key again; exact owner positions remain pending.',
'Tab-indent each body paragraph, excluding inside address, lists and closing. The primary teaching input and declared edited state determine paragraph membership; no unsupported paragraph count is invented.',
'Six, six and three tabs initially align the named title pairs; Reveal then removes all but one tab per pair. Ctrl-End inside Tab Set clears its ruler rather than a document line. A 3.5in relative stop plus 1in margin gives a 4.5in page position. The source motivates one stop by the font sensitivity of repeated tabs.',
'Original step9 applies the same operation to Secrets, Black Forest Summer and Winter’s Wonder, listed on the following page. Retain all three repeated operations under that original number; allocate no new coverage IDs.',
'A single 3.5in stop also changes later paragraph indentation. The source offers resetting default tabs at the list end as an alternative; the numbered route deletes the local Tab Setting owner with Backspace/Yes, then installs 0.5in and 3.5in stops at document beginning. Inspect later paragraph indentation separately.',
'Original step1 applies Backspace/Tab to Always, Little Flower Girl, Easter Parade, Joplin, Happiness, Lazy River and Copenhagen Tales. Source promises alignment under font/printer changes with one tab; this remains unobserved.',
'The demonstration moves only Jayna Wilder-Smith’s name with two Backspaces and Tab, leaving address/phone behind. Remove that tab and restore two returns before defining columns. This intermediate result is intentionally incomplete, not an accepted final layout.',
'Accept the default two Newspaper columns, then select On. Home/Down reformats. The rest of the letter also flows into columns until Off at the list end, before the Line Spacing owner. Following text then returns to ordinary margins. Parallel columns and other definition variants are not selected.',
'Try 200%, Full Page and Facing Pages in addition to the numbered 100% route, with page/arrow navigation. Monitor resolution affects legibility. Save MUSICBOX.LTR as a distinct learner output. Optional partial save under a name such as LESSON13 and later Retrieve is a separate unrun continuity branch.',
'WBC51 PDF3 notice1848, dated08/91, claims printed110 and adds a second A pointer beside a partial list. This scan’s printed110 is the Line Spacing menu, with list illustrations elsewhere. Retain the versioned pointer correction without guessing its physical target or changing executable expectations.',
'Retrieve WB13’s MUSICBOX.LTR. Source expects three Sundheim replacements with SoundMaster and eight plural music boxes occurrences. Search retains its prior text; No Confirm replaces from the declared beginning. Forward/backward Not Found checks and the absent singular music box check are distinct expectations, not observed target results.',
'Yes at w/Confirm? creates per-match replacement decisions; the numbered route chooses No. Refusal, Cancel, Not Found, case/boundary details and I/O failures remain pending and are not fabricated numbered workbook steps.',
'Footer A Every Page is a separate editing context; Footer B is unselected. Graphics Horizontal defaults Full width, Baseline, 0.013in thickness and 100% black are embedded line-owner settings, not character line-draw strokes. The line is visible in preview/print. The page-number marker is special ^B, not literal AB; it can combine with centered text.',
'The source warns about accidentally typing document text inside a footer and offers Block/Move to transfer it to the body. Text, range and destination are unspecified; retain this as an optional recovery branch requiring finite later input, not an invented completed case.',
'100% shows the first-page footer; Facing Pages exposes the initially split first list and representatives. Breakpoints depend on Workbook Printer, font and defaults. Do not treat illustrated coordinates or page counts as invariant across other printer resources.',
'Three Homes then Up reaches the very beginning before existing format owners. The visually checked fraction in step5 is 1/2in for both top and bottom margins, despite OCR corruption. Other fractions3/8,7/32,13/64 illustrate conversion to decimal but are not numbered cases.',
'Source calls an isolated first line at the bottom an orphan and an isolated last line at the next top a widow; it notes terminology varies. Enable protection and scroll to observe the isolated line move. Broad prose does not establish every paragraph/column boundary algorithm.',
'Remove exactly six previously inserted blank lines. Absolute Advance Line2in updates status without displaying equivalent editing whitespace; preview/print must establish actual position. Margin, font, header or printer changes can invalidate blank-line spacing. This is distinct from the existing sampled Position/Right Advance evidence.',
'Go To/Left reaches the first Newspaper column; Hard Page at Mary Anna Pickford moves the remainder into the second column in this context. Source expects four representatives per column, list on page2 and closing on page3 after prior adjustments. Exact native/print behavior remains pending.',
'Save before Spell. Skip correctly spelled proper names for the rest of this document; Exit or another key dismisses Word Count. Select an actual printer after Workbook Printer formatting, inspect adjusted preview, Cancel back to Print and choose Full Document. The final save retains spelling edits and printer association.',
'Left-click highlighting is the explicit physical mouse alternative to keyboard arrows/Enter for printer selection. Actual host events, focus and real printer availability remain pending; automatic selection of a mock resource is not equivalent evidence.',
'WBC51 PDF3 notice1849, dated08/91, claims printed124 and repositions A/B pointers beside partial lists. This scan’s printed124 introduces Footer A, not that list spread. Retain the correction with unresolved edition/page alignment; do not guess remapped coordinates.',
'The Macro Def indicator bounds recording. HI receives the .WPM extension automatically. Text and corrections made by Backspace/Delete are recorded as keys rather than a screen snapshot. Returns outside recording and preexisting company/closing text are excluded. An empty description is explicitly allowed.',
'The unnumbered restart route stops Define, starts it again with the same name, chooses Replace1/Yes, then enters a description and records again. Refuse/Cancel preservation of the old macro/document remains unrun and is not implied by a later successful overwrite route.',
'CLOSE records four returns and an unspecified learner name plus role/company. Clear without saving, retrieve original MUSICBOX.WKB and confirm Delete End of Page to remove its old closing. Exact personal input needs a future declared value. No native document or macro write occurred in this research.',
'FORMAT records 2in margins, Full justification and Home/arrow reformat navigation. Owners are inserted during recording; delete them after recording, then execute to restore. Saving/retrieving a document containing codes is an optional alternative that cannot encode navigation keys. The Layout > Line menu alternative already selects Line; do not select Line a second time in the following step.',
'The introduction references the lesson3 form, but the numbered input is explicitly MEMO.WKB. MEMO.WPM’s description appears above the hard page in Look and special key characters below. *.WPM filters the list; pictured sizes/dates are examples. Exit Look/list, execute, retrieve the form and verify its first entry gap.',
'Reusing MEMO offers Replace, Edit Macro and Edit Description; only Replace/Yes is selected. Edit, description editing and Look Next/Previous remain unselected leads. An existing independent round-trip witness does not accept this whole lesson or every menu variant.',
'Pause1/Enter during recording continues Define rather than completing actual field input. Record three pauses at To, From and Subject. The unnumbered final exercise executes MEMO.WPM, supplies operator values and resumes with Enter between fields, then ends at the body. Values/body are unspecified; either save under a new name explicitly other than MEMO, or clear with Exit. All execution/native WPM provenance remains pending.',
'Pictured Display, Assign and Comment commands are unselected. This lesson has no nested macro invocation, Repeat Value, CANCEL ON/OFF, ON ERROR or BREAK instruction. Preserve canonical A1/A2 coarse mapping without treating this source slice as execution or acceptance of those broader families.',
'Generic menu Cancel/no routes, save/overwrite failures, missing teaching files/printers/macros and stopping recording/playback remain mission invariants requiring later finite inputs. No recipe or source step is invented to fill them. Illustrations and resource metadata establish documentary content only.'
]
assert len(paragraphs)==len(j['context_branches'])
for b,p in zip(j['context_branches'],paragraphs):b['branch_paraphrase']=p
# Improve readability of terse action labels while preserving source locators and native tokens.
for s in j['numbered_steps']:s['action_paraphrase']=re.sub(r'(?<=[a-z0-9])(?=[A-Z])',' ',s['action_paraphrase'])
j['source_number_policy']='Only original section-local step numbers; repeated operations stay within the original step. No new leaf, WP or CMD IDs.'
j['execution_claim']='No original/candidate lesson replay, recipe, new IDs, registration, status or matrix promotion. All execution pending; WP103 remains unregistered/incomplete. Historical core55/12/9 preserved.'
j['verification']='All206 numbered-step,53 menu-alternative and1 mouse-alternative first-line hashes independently re-extracted by physical PDF page; all34 scoped pages visually reviewed.'
jp.write_text(json.dumps(j,indent=2)+'\n')
md='''# WB-B05 source census — lessons 13–15

Documentary research only, under the resolved Researcher Robbie profile and action `research`. This finite batch expands source coverage; it does not register or complete WP103, allocate IDs or promote any audit/matrix status. No repository/index/Git/runtime, recipe, original/private guard, VM or Mac operation occurred.

**206 original numbered steps:** WB13 71, WB14 69, WB15 66. The companion JSON also retains **53 explicit menu alternatives** (14 / 18 / 21), **one physical mouse alternative**, and **33 context, resource, optional-exercise and ambiguity branches**. All original/candidate execution remains pending. Source counts are not acceptance counts.

## Sources and exact locators

- WB51: registered `research/cache/WPDOS51Workbook.pdf`, edition `WKUS1WP51-11/89`, SHA256 `868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d`.
- WBC51: registered `research/cache/WP51WKBK.pdf`, SHA256 `7e7b87786d4ac748af6603a98d084c38137a6e723954540b1153ad6ed64e7a0b`; relevant notices1848/1849 are dated08/91 on PDF3. The later notice’s stale LetterPerfect header is retained rather than silently treated as the workbook edition.
- WB13: printed109–121 / physical PDF118–130, Formatting a Letter Part I. WB14: printed122–133 / PDF131–142, Formatting a Letter Part II. WB15: printed134–142 / PDF143–151, Office Automation. No lesson16 expansion.
- Every physical page118–151 was rendered and visually inspected. The matching WBC51 PDF3 was visually checked in the retained correction render. The exact OCR text is retained as `workbook-b05-source-extract.txt` and `workbook-b05-corrections-extract.txt`; rendered pages/contact sheets are in `workbook-b05-pages/`.
- Every JSON numbered step and explicit alternative has the source section-local number, physical page, printed page, physical extracted-text line and SHA256 of its first line. Fresh single-page extraction independently verifies all260 numbered/menu/mouse hashes. Four OCR `S` labels are visually normalized to source step5 at PDF129:55,146:17,148:9,150:7. PDF137 step5 visually specifies **1/2in**, which OCR corrupts; the untouched raw-line hash remains recorded.

The 1989 scan and later dated notices are versioned documentary inputs. They do not prove March1992 executable behavior or a pristine shipping set. Fingerprints copied from installed-files metadata do not establish current private resource availability; no installed resource path was opened or checked.

## Full numbered-section inventory

Numbers restart within each original section. JSON enumerates every action and its exact line/hash, including repeated named-item operations under the original source number.

| Lesson | Original section | Steps | Physical PDF pages | Current family links |
|---|---|---:|---|---|
'''
for (l,s),rows in itertools.groupby(j['numbered_steps'],lambda v:(v['lesson'],v['source_section'])):
 r=list(rows);ps=sorted({v['pdf_page'] for v in r});pr=str(ps[0]) if len(ps)==1 else f'{ps[0]}–{ps[-1]}'
 md+=f"| {l} | {s} | {len(r)} | {pr} | {', '.join(r[0]['family_dependencies'])} |\n"
md+='\n## Context, optional exercises, resources and unresolved branches\n\n'
for branch in j['context_branches']:
 ps=','.join(str(v) for v in branch['pdf_pages']);families=', '.join(branch['family_dependencies'])
 md+=f"**{branch['lesson']} — {branch['topic']}** (PDF{ps}; {families}). {branch['branch_paraphrase']}\n\n"
md+='''## Mapping and evidence limits

The canonical WB-B05 lesson map stays unchanged. The detailed census refines its coarse dependencies: L3 carries tab stops, Advance and page-boundary contexts; L6 carries actual Newspaper columns; G3 carries the footer’s native horizontal graphics line; L1/P1/P3 carry printer metrics, real printer selection and preview; E1/E3 carry deletion and native insertion; I3 carries the explicit mouse route. Q1/Q2/Q3 retain remaining source leaves, complete journeys/physical input and native/save provenance. Canonical WB14 L5 does not imply a selected paper-definition exercise here. Canonical WB15 A1/A2 do not imply nested invocation, Repeat Value or CANCEL ON/OFF: those instructions are absent from this lesson. No feature family is excluded or closed because this batch does not exercise it.

The existing audit remains separate evidence: CMD51-168 Newspaper columns and CMD51-176 horizontal graphics lines remain unimplemented; CMD51-107 Advance remains partial. Verified CMD51-105 double spacing, CMD51-167 sampled widow/orphan behavior, CMD51-131 basic recording and CMD51-199 sampled WPM round-trip are narrower than these lessons’ complete state, resources, pauses, menus and native/print journeys. Do not promote those witnesses to lesson acceptance.

Resources for later bounded execution include distinct original `MUSICBOX.WKB` and `MEMO.WKB`, learner `MUSICBOX.LTR`, fresh authored `HI.WPM`/`CLOSE.WPM`/`FORMAT.WPM`/`MEMO.WPM`, actual descriptions and personal/field values, printer definitions/fonts/metrics, spell resources, declared status units and a real printer for physical output. An existing macro collision must be declared before exercising Replace; examples do not authorize overwriting unrelated files. Metadata, historical screenshots and green isolated primitives do not supply native producer/reopen/print or original/candidate execution evidence.

All53 menu occurrences remain source records with exact lines, including a Print alternative printed after the scroll instruction but semantically belonging to the Print step. The mouse selection has its own exact record. Alternative paths need not be concatenated into a single replay; the macro Layout > Line alternative already performs a selection that the keyboard path performs in its next numbered step. Unselected illustrations and unspecified field/paragraph repetitions remain explicit leads and preconditions rather than guessed completed cases.

## Preservation

Historical WP21 core55 steps /12 contexts /9 menu alternatives is unchanged. Existing B01–B04 reports and all seven canonical source/map/audit/ledger/metadata inputs were hashed and checked unchanged; JSON retains those pins plus the source PDF and page hashes. Registered source text and all prior report hashes are preserved. Only new `/tmp/wordling-mission1-closeout-20261118/` research artifacts were written. The parent controls later preservation at WP104’s quiet point. WP103 remains unregistered/incomplete; the full mission and all lesson execution/acceptance remain open.
'''
(out/'workbook-b05-source-census.md').write_text(md)
# Preserve inherited prior pins and verify all canonical/source inputs after the work.
old=json.loads((out/'workbook-b04-source-census.json').read_text())
for p,h in old['prior_census_hashes'].items():assert j['prior_census_hashes'][p]==h,p
fixed={'research/cache/WPDOS51Workbook.pdf':'868646c7fd5f5fb8f8fe9945af6afcae2fb36eb9aaee687e705db81ae1d5dc4d','research/cache/WP51WKBK.pdf':'7e7b87786d4ac748af6603a98d084c38137a6e723954540b1153ad6ed64e7a0b','research/cache/workbook.txt':'4a99b406886f1e128ab673c9cefddc83ca9f53ddbc8dcfd621e38b7afe79ecce','research/cache/workbook-corrections.txt':'22217add5a9c6ee3236c466462d72ed7b50e473274c95ac0b066d2b3b17112b7'}
for p,h in {**j['immutable_input_hashes'],**fixed}.items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h,p
for p,h in j['prior_census_hashes'].items():assert hashlib.sha256((out/p).read_bytes()).hexdigest()==h,p
raw=subprocess.check_output(['pdftotext','-f','3','-l','3','-layout',str(root/'research/cache/WP51WKBK.pdf'),'-']).decode().split('\f')[0].splitlines()
for s in j['source_corrections']:assert hashlib.sha256(raw[s['source_line_number']-1].strip().encode()).hexdigest()==s['source_first_line_sha256']
for p in ('workbook-b05-source-census.md','workbook-b05-source-census.json'):print(p,hashlib.sha256((out/p).read_bytes()).hexdigest())
