from pathlib import Path
import json,struct
root=Path('.')
for rid in ['2026-10-29-smoke-02','2026-10-29-smoke-03']:
 r=json.loads((root/f'docs/research/reference-runs/{rid}/run.json').read_text());c=next(c for c in r['results'] if c['case_id']=='CMD51-066')
 assert c['trace']==[{'type':'WORDLING TEST'},{'key':'f10'},{'capture':'save-prompt'},{'type':r'C:\OUT\NEWTEST'},{'key':'ret'},{'capture':'saved'}]
 d=(root/f'docs/research/reference-runs/{rid}/CMD51-066/NEWTEST.WP5').read_bytes();assert d[struct.unpack_from('<I',d,4)[0]:]==b'WORDLING TEST'
for rid in ['2026-10-29-extended-03','2026-10-29-extended-04']:
 r=json.loads((root/f'docs/research/reference-runs/{rid}/run.json').read_text());c=next(c for c in r['results'] if c['case_id']=='CMD51-067')
 t=c['trace'];i=t.index({'capture':'replace-prompt'});assert t[i-2:i+9]==[{'key':'f10'},{'key':'ret'},{'capture':'replace-prompt'},{'key':'n'},{'capture':'different-filename-requested'},{'key':'f1'},{'capture':'unsaved-buffer'},{'key':'f7'},{'key':'n'},{'key':'y'},{'capture':'clean-exit'}]
 base=root/f'docs/research/reference-runs/{rid}/CMD51-067'
 assert r'Replace C:\OUT\SAME? No (Yes)' in (base/'replace-prompt/screen.txt').read_text()
 assert r'Document to be saved: C:\OUT\SAME' in (base/'different-filename-requested/screen.txt').read_text()
 assert (base/'unsaved-buffer/screen.txt').read_text().startswith('ORIGINALMODIFIED')
 d=(base/'SAME.WP5').read_bytes();assert d==(base/'BEFORE.WP5').read_bytes();assert d[struct.unpack_from('<I',d,4)[0]:]==b'ORIGINAL'
cases={c['id']:c for c in json.loads((root/'docs/research/command-scenarios.json').read_text())}
for cid in ['CMD51-065','CMD51-068','CMD51-069','CMD51-070','CMD51-071','CMD51-072','CMD51-073','CMD51-074','CMD51-075','CMD51-087','CMD51-189','CMD51-192']:
 assert cases[cid]['oracle_status']=='not-run',cid
print('Independent repeated save/refusal/cancel native+trace+screen checks pass; other branches remain not-run')
