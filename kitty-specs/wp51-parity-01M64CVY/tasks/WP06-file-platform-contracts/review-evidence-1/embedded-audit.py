from pathlib import Path
import hashlib, json, re, struct
p = Path('kitty-specs/wp51-parity-01M64CVY/contracts/files-platform.md')
text = p.read_text()
a = text.split('<!-- WP06_AUDIT_BEGIN -->',1)[1]
a = json.loads(a.split('```json\n',1)[1].split('\n```',1)[0])
sha = lambda b: hashlib.sha256(b).hexdigest()
for source in a['source_inputs']:
    assert sha(Path(source['path']).read_bytes()) == source['sha256']
inv = {g['id']:g for g in json.loads(Path('docs/research/feature-inventory.json').read_text())}
cases = {c['id']:c for c in json.loads(Path('docs/research/command-scenarios.json').read_text())}
sources = {s['id']:s for s in json.loads(Path('docs/research/sources.json').read_text())}
assert len(a['rows']) == 27
assert {r['id'] for r in a['rows']} == {f'FP{n:02}' for n in range(1,28)}
assert set(re.findall(r'^\| (FP\d{2}):',text,re.M)) == {r['id'] for r in a['rows']}
used = set()
for row in a['rows']:
    assert set(row['feature_ids']) <= inv.keys()
    line = next(l for l in text.splitlines() if l.startswith('| '+row['id']+':'))
    cells = [c.strip() for c in line.split('|')]
    expected = ', '.join(row['feature_ids'])+'; '+('; '.join(
        c['case_id']+' ('+c['title']+')' for c in row['case_links']) or 'no dedicated scenario')
    assert cells[3] == expected, row['id']
    assert cells[4] == row['evidence_basis'], row['id']
    assert cells[5] == row['contract']+' **Remaining:** '+row['remaining'], row['id']
    assert set(re.findall(r'CMD51-\d{3}',line)) == {c['case_id'] for c in row['case_links']}
    for link in row['case_links']:
        cid,gid = link['case_id'],link['feature_id']
        assert gid in row['feature_ids'] and gid in cases[cid]['feature_ids'], (row['id'],cid,gid)
        assert cid in inv[gid]['command_scenario_ids'], (row['id'],cid,gid)
        assert link['title'] == cases[cid]['title']
        assert link['oracle_status'] == cases[cid]['oracle_status']
        used.add(cid)
    loc = '; '.join(f"{l['printed_start']}–{l['printed_end']} / {l['pdf_start']}–{l['pdf_end']}" for l in row['locators'])
    assert cells[2] == loc
    for l in row['locators']:
        assert 1 <= l['printed_start'] <= l['printed_end']
        assert l['pdf_start']==l['printed_start']+17 and l['pdf_end']==l['printed_end']+17
        assert l['pdf_end'] <= sources[row['source_id']]['pdf_pages']
assert {cid for cid in used if cases[cid]['oracle_status']=='partially-observed'} == {'CMD51-066','CMD51-067'}
assert set(re.findall(r'CMD51-\d{3}',text)) <= used
assert len(a['evidence']) == 20
for e in a['evidence']:
    d = Path(e['path']).read_bytes()
    assert (len(d),sha(d)) == (e['size'],e['sha256'])
    if 'case_id' in e:
        assert e['case_id'] in used
        assert e['run_manifest'] in cases[e['case_id']]['evidence_paths']
        run = json.loads(Path(e['run_manifest']).read_text())
        assert run['scope']=='original-reference-only' and not run['wordling_tested']
        case = next(c for c in run['results'] if c['case_id']==e['case_id'])
        assert any(x['path']==e['path'] and x['size']==len(d) and x['sha256']==sha(d) for x in case['evidence'])
    if e['kind']=='native':
        body = struct.unpack_from('<I',d,4)[0]
        assert body==e['body_offset'] and d[body:].hex()==e['body_hex']
        if e['case_id']=='CMD51-067':
            other = Path(e['path']).with_name('BEFORE.WP5' if Path(e['path']).name=='SAME.WP5' else 'SAME.WP5')
            assert other.read_bytes()==d
        repeat = e['path'].replace('smoke-03','smoke-02').replace('extended-04','extended-03')
        assert Path(repeat).read_bytes()==d
print('WP06 source hashes, 27 semantic matrices, canonical statuses and original evidence valid')
