#!/usr/bin/env python3
"""Index bounded original observations; never certifies product parity."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'docs/research/everyday-contract-2026-11-05'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def ref(p):
    return {'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)}

def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2) + '\n')

def captures(run, prefixes):
    result = []
    for prefix in prefixes.split():
        matches = sorted((BASE / run).glob(prefix + '-*'))
        assert len(matches) == 1, (run, prefix, matches)
        directory = matches[0]
        raw = (directory / 'vram.bin').read_bytes()
        assert len(raw) == 4000
        entry = {'path': str(directory.relative_to(BASE)), 'characters_sha256': hashlib.sha256(raw[::2]).hexdigest(),
                 'attributes_sha256': hashlib.sha256(raw[1::2]).hexdigest(), 'grid': ref(directory / 'vram.bin'),
                 'text': ref(directory / 'screen.txt'), 'image': ref(directory / 'screen.png'),
                 'logical_geometry': [80, 25], 'comparison': 'All characters and attributes unless a documented field mapping applies; no selection/content/status masks.'}
        bios = directory / 'bios-cursors.bin'
        if bios.exists():
            data = bios.read_bytes()
            entry['bios_page0_cursor'] = {'column': data[0], 'row': data[1], 'file': ref(bios),
                'qualification': 'Diagnostic BIOS state, read after capture resume. Semantic caret/focus also requires displayed position and following-key witness.'}
        result.append(entry)
    return result

selected = {
 'qualification/menus': '01 02 03 05 06 07 08 09 10 11 12 16 17 18 19 20 21 26 27 30 31 32 33 34 35 36 37 38 39 40 41 42',
 'qualification/flow': '03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 25 26 27 28 29 30 31 32 33 34',
 'qualification/flow-reliable': '01 02 03 04 05 06 07 08 09 10 11 12',
 'qualification/corrections': '01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 19 20 21 23 24 25 26 27 28 29 30 31 32 33 34',
 'qualification/history-repeat': '01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19',
 'qualification/mouse': '01 02 03 04 05 06 07',
 'qualification/proof-pages': '01 02 03 04 05 06 07 08 09 10 11',
 'qualification/proof-boundaries': '01 02 03 04 05 06 07 08',
 'qualification/proof-boundaries-repeat': '01 02 03 04',
 'qualification/files': '01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 17 19 22 23 24 25 26 27 28 29 30 42 43 44 45 46 47 48 49 50 51 61 62 63 64 65 66 67',
}
for run in ['scroll-search-r1','scroll-search-r2']:
    selected['qualification/'+run] = '01 02 03 04 05 06 07 08 09 10 11-not-found-burst-00 12 13 14 15 16'
# Focus runs use longer, unique prefixes because each numbered probe has 3 states.
for run in ['focus-r1','focus-r2']:
    selected['qualification/' + run] = '01 ' + ' '.join(f'{n:02d}-{key}-{phase}' for n,key in [(2,'f1'),(3,'esc'),(4,'spc'),(5,'f7')] for phase in ['before','after','up']) + ' 06'
# Resolve exact directory names rather than inventing labels; selected spelling
# frames follow the explicit accepted/failed distinctions in spelling/REPORT.md.
for run, excluded in [('spelling/proof', {'15','16'}), ('spelling/repeat', {'06','07','08','09','10'}), ('spelling/suggestions', set()), ('spelling/proof-restart2',set())]:
    selected[run] = ' '.join(p.name.split('-')[0] for p in sorted((BASE/run).iterdir()) if p.is_dir() and (p/'vram.bin').exists() and p.name[:2].isdigit() and p.name[:2] not in excluded)
frames = []
for run, prefixes in selected.items():
    # Exact label supports before/after capture identifiers.
    for prefix in prefixes.split():
        exact=BASE/run/prefix
        if (exact/'vram.bin').exists():
            # captures() expects a prefix plus hyphen; use the unique parent prefix.
            raw=(exact/'vram.bin').read_bytes()
            data={'path':str(exact.relative_to(BASE)), 'characters_sha256':hashlib.sha256(raw[::2]).hexdigest(), 'attributes_sha256':hashlib.sha256(raw[1::2]).hexdigest(), 'grid':ref(exact/'vram.bin'),'text':ref(exact/'screen.txt'),'image':ref(exact/'screen.png'),'logical_geometry':[80,25],'comparison':'All cells; no mask.'}
            if (exact/'bios-cursors.bin').exists():
                d=(exact/'bios-cursors.bin').read_bytes();data['bios_page0_cursor']={'column':d[0],'row':d[1],'file':ref(exact/'bios-cursors.bin'),'qualification':'Diagnostic; semantic focus requires next-key witness.'}
            frames.append(data)
        else:
            frames += captures(run,prefix)

contracts = [
 ('EE-A01',['menus','mouse'], 'Persistent bar Yes remains visible with ordinary editing focus; No hides inactive bar. Shift+F1,2,4,8 changes preference; F7 returns to editor. Exit/restart preserves it. Keyboard Alt+= then F opens File. Derived mouse profile proves clicking File opens that original menu.', 'Mouse driver is a disclosed derived profile; physical Linux transport and persistence implementation still require product tests.'),
 ('EE-A02',['menus','focus-r1','focus-r2'], 'Nested Layout>Justify F1/Escape/Space each removes only the selected child highlight; Up then selects parent Endnote. F7 removes menus and returns editing. F6 while menu is active dispatches Bold, then B enters bold text.', 'See focus checks for exact eight changed attribute cells; do not infer focus from remaining child text.'),
 ('EE-A03',['menus'], 'F3,F3 enhanced template and original Help topics for F10 Save, F2 Search, F6 Bold, F8 Underline, Alt+F3 Reveal and F5 List. Help returns without leaking text; enhanced F11 Reveal/F12 Block shown.', 'Keyboard delivery on Linux is a separate WP85 qualification; modern Ctrl+S/O/Q aliases are not original bindings.'),
 ('EE-A04',['flow','flow-reliable'], 'Authored paragraph, blank paragraphs, Underline, Tab, 75-character unbroken word, and 110 Returns create three physical pages. Save, further edit, save, clear/retrieve, append MORE and save. Both successful runs produce byte-identical FLOW.WP.', 'Physical paper remains fixed during Linux viewport resize; original fixed VGA cannot witness resize.'),
 ('EE-A05',['flow','flow-reliable','scroll-search-r1','scroll-search-r2'], 'End on first wrapped line yields Pos7.3, Down retains desired position through next line6.8, empty1, short2.7, tabbed3. Home sequences reach line/doc boundaries; PageDown reaches Pg2 thenPg3, PageUp returnsPg2. Reveal code-boundary Left/Right retains printed position while changing code focus.', 'Repeated scroll-search runs add Reveal PageDown2/3, PageUp2, document-end, fourteen Down steps and close/restore. Compare exact grids and positions; Linux edge clipping remains product verification.'),
 ('EE-A06',['corrections','history-repeat'], 'Typeover, Backspace across HRt, character deletion, three deletion groups, F1/2/2 history selection, cancel and restore; repeated after save/retrieve. F12 backward and Alt+F4 forward blocks; Delete No(default)/Yes and restored deleted text.', 'Block is an inclusive character selection: first Left from end while block starts can select last character without reducing printed insertion position; frames15–19 retain per-key grids. Stale/foreign-revision safety is a product assertion.'),
 ('EE-A07',['corrections','proof-pages','proof-boundaries','proof-boundaries-repeat'], 'Nested/overlapping Bold and Underline, saved while Bold active then continued typing, retrieved editing, Delete at initial Bold code removes its pair while retaining text and Underline; insert inside Underline.', 'Exact fixture bodies and Reveal grids govern supported code order; does not qualify arbitrary attributes or opaque pairs.'),
 ('EE-A08',['flow','corrections','scroll-search-r1','scroll-search-r2'], 'Reveal displays HRt/SRt/DSRt, Tab and attribute pairs in paragraph structure, ruler and lower caret; code Left/Right and Search witness same document positions; closing Reveal restores normal view.', 'Repeated Reveal scrolling is pinned in scroll-search-r1/r2. Linux resize must not change bytes/paper geometry; terminal-specific edges remain product tests.'),
 ('EE-A09',['flow','flow-reliable','scroll-search-r1','scroll-search-r2'], 'F2 text then F2 terminates forward search; F2,F2 repeats. Shift+F2 backward prompt/termination. Search crosses SRt. In Reveal F8 enters UND into search; result and code focus are captured. Failed and canceled search leave body unchanged.', 'Paused bursts capture exact * Not found * at row24 normal and row11 Reveal, columns0..12 attribute0x1f, followed by restored status/focus. Both fresh runs reproduce it; no exact timing promise. Native prefix byte80 changed00->08 on later original save, with identical body; product FC002 still requires no-edit byte identity. Menu Search entry equivalence must be tested in product; this research invokes function commands.'),
 ('EE-A10',['files'], 'F5 default directory/template, multi-screen list PageDown, Short/Long1/2 with directory confirmation, N name lookup, Look Next/Prev return same row, directory Look6+Enter enters child/parent. F5 from Retrieve; arrows select file; Retrieve1 loads blank doc or prompts before insertion into occupied doc.', 'Filename N lookup for directories uses leading backslash. End did not select last file in list; failed assumptions retained. Browser statistics need explicit DOS/Linux mapping; document size527 is not disk file337.'),
 ('EE-A11',['files','flow','corrections'], 'New save, repeated save, Save As, overwrite EnterNo returns filename, F1 cancels preserving edits. Original backup enabled uses basename.BK!, rotates previous destination bytes; A.TXT and A.WP collide in same A.BK!. Refusal preserves both destination and backup exactly. Disabled successful replacement deletes backup.', 'backup/REPORT.md supplies independent enabled/disabled repetitions. Exact shared-basename collision is a single new bounded observation; no timed-backup or host-failure semantics inferred.'),
 ('EE-A12',['corrections','menus','files'], 'Shift+F3 preserves two document contents/carets/names; F7 SaveYes new filename publishes before Exit docN? when other doc exists; No/Yes defaults and F1 cancel captured; closing Doc2 returns Doc1; continued New doc remains editable. One-screen exit asks Exit WP?.', 'Per-screen history isolation beyond witnessed visible groups remains mandatory product test; original captures do not prove internal representation.'),
 ('EE-A13',['files','flow'], 'Original overwrite-refusal preserves destination/backup; no-edit save preserves body but may update original prefix housekeeping. Original-produced native corpus provides reader/writer inputs.', 'FC002 untouched output byte identity, unrelated-byte conservation, unsafe-edit refusal, concurrent source/destination changes and temporary-write/replacement fault injection are mandatory Linux product assertions, NOT witnessed DOS behavior. Existing preservation corpus remains authoritative; no relaxations.'),
 ('EE-A15',['proof-pages','proof-boundaries','proof-boundaries-repeat','history-repeat'], 'Continuous context/suggestions/correction/skip/add/edit/resume/restart from spelling study; new physical-page scope, formatted words, SRt/DSRt boundaries and correction/Undelete behavior specified in proofreading-contract.md.', 'Lexicon/ranking equivalence requires admitted matching resource; modern dictionary is not silently equivalent. Resource faults are product tests. No exact unknown-word block options claim.'),
]
journeys=[]
for ident,runs,observed,limits in contracts:
    paths=['qualification/'+r for r in runs]
    if ident=='EE-A15': paths += ['spelling/proof','spelling/repeat','spelling/suggestions','spelling/proof-restart2']
    if ident=='EE-A11': paths += ['backup/enabled','backup/disabled']
    journeys.append({'id':ident,'reference_status':'observed-subcases-pending-independent-review','observed_contract':observed,'scope_limits_and_product_obligations':limits,'runs':paths,'frames':[f['path'] for f in frames if any(f['path'].startswith(p+'/') for p in paths)],'product_evidence':None,'reviewer_verdict':None})
write('journey-contract.json', {'schema_version':1,'status':'candidate-reference-contract-not-product-acceptance','reference_release':'US WordPerfect 5.1 DOS 03/09/92','full_m1_complete':False,'frames':frames,'journeys':journeys,'masks':[{'scope':'directory capture clock row0 columns0..20','reason':'Guest time advances with host-paced input; compare format separately, not clock value.'}],'mapping_policy':'All other varying fields require declared profile/fixture/Linux mapping before comparison. No blanket ignored-region or byte-normalization mask. Selection, filenames, content, printed Pg/Ln/Pos and focus are never masked.'})
profile={ 'schema_version':1,'release':ref(ROOT/'docs/research/reference-baseline.json'),'environment':ref(ROOT/'docs/research/reference-environment/environment.json'),'resources':ref(ROOT/'docs/research/reference-environment/resource-profile.json'),'mouse_variant':ref(BASE/'qualification/mouse/environment.json'),'settings':{'paper_inches':[8.5,11],'margins_inches':{'left':1,'right':1,'top':1,'bottom':1},'font':'Courier 10cpi','printer':'Standard Printer','justification':'Full','line_height':'Auto','line_spacing':1,'tab_stops':'Relative; -1 inch, every 0.5 inch','hyphenation':False,'widow_orphan':False,'menu_bar_visible_default':False,'original_document_backup_default':False,'timed_backup_default':'Yes, 30 minutes'},'settings_evidence':['REPORT.md','r3','r4-settings','r5-settings','backup/REPORT.md'],'screen':{'columns':80,'rows':25,'raster':[720,400],'encoding':'VGA CP437 character bytes plus original attribute bytes','cursor':'BIOS page0 diagnostics, rendered cursor, printed position and next-key behavior jointly; BIOS alone is insufficient'},'layout_contract':'Editing screen uses nominal 0.1-inch character/1/6-inch line advances in tested Courier profile despite Full justification. Do not stretch editing spaces to printed justification; do not claim print spacing from screen. Page membership and nominal printed-position status use exact original fixture results.','resources_rights':'WP executable, manuals, LEX/SPW/LCN, printer and master images remain private, proprietary references. No distribution rights inferred. User-authored native documents and generated one-word supplementary dictionaries are research fixtures.','linux_adaptations':[{'topic':'viewport','rule':'At80x25 compare exact logical cells. Larger/smaller terminal maps/clips a fixed-paper logical view; resizing must not reflow paper or mutate native document. Precise canvas extension policy belongs to WP85 and independent review.'},{'topic':'mouse','rule':'Map terminal cell coordinates to the same logical menu coordinates. CTMouse is a disclosed reference transport adaptation, not product dependency.'},{'topic':'filesystem','rule':'Confined workspace represents DOS drive/root. Declare ASCII case handling, 8.3 projection, symlink/ambiguity behavior and timestamp/statistics mapping before comparison. No traversal outside workspace, silent alias or misleading DOS free/used values. WP79 owns reviewed mapping.'},{'topic':'settings','rule':'Expose original setting labels/choices and persisted behavior. WP85 owns native SET compatibility or explicitly reviewed host-storage mapping; these screenshots alone do not define SET bytes.'},{'topic':'proofreading','rule':'Preserve original control/context flow. Provider must declare rights, bytes/version/locale and suggestion-equivalence level. Missing/locked/read-only resources yield explicit failure without corrupting document or supplementary bytes.'},{'topic':'keyboard','rule':'Original US/enhanced template governs commands. Physical escape-sequence delivery is separately qualified; no modern Ctrl convenience aliases in parity profile.'}]}
write('profile.json',profile)
fixtures=[]
for p in sorted(BASE.rglob('*')):
    if p.is_file() and ('exports' in p.parts or p.suffix.upper() in ('.WP','.SUP')):
        raw=p.read_bytes()
        if raw.startswith(b'\xffWPC'):
            offset=int.from_bytes(raw[4:8],'little');assert 16<=offset<=len(raw)
            fixtures.append({**ref(p),'document_offset':offset,'body_sha256':hashlib.sha256(raw[offset:]).hexdigest(),'body_hex':raw[offset:].hex(),'rights':'Original user-authored test content; no vendor lexicon/executable bytes.','use':'Original fixture and observed native effect; hash identifies evidence, never an admission whitelist.'})
write('fixture-manifest.json',{'schema_version':1,'fixtures':fixtures,'native_comparison':'Untouched product output is byte-identical. Edited output accounts for intended code/text changes and derived fields; preserve unrelated bytes and verify original interoperability. Original housekeeping differences do not authorize blanket normalization.'})
print(f'{len(frames)} indexed frames; {len(fixtures)} native fixtures')
