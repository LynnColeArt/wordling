import runpy,json,hashlib
from pathlib import Path
O=Path('/tmp/wordling-wp52-independent');r=runpy.run_path(str(O/'independent-wire.py'));decode=r['decode'];h=r['H'];receipt=json.loads((h/'pty-07/result.json').read_text());p=receipt['results'][0];w=p['witnesses'][0];raw=(h/'pty-07/native-r1/wire-output.bin').read_bytes()[:w['wire_bytes']];reference=decode(raw);rows=[]
for label,old,new in [('active-background',b'\x1b[37;41m',b'\x1b[37;44m'),('visible-native-label',b'[BOLD]',b'{BOLD]')]:
 assert old in raw;mut=raw.replace(old,new,1);result=decode(mut);assert len(mut)==len(raw)and result!=reference
 if label=='active-background':assert result[1][3]!=reference[1][3]
 else:assert result[0][3]!=reference[0][3]
 rows.append({'case':label,'changed_wire_sha256':hashlib.sha256(mut).hexdigest(),'same_length_offset':True,'independent_original_cell_style_comparison_refuses':True})
(O/'wire-falsifiers.json').write_text(json.dumps(rows,indent=2)+'\n');print('2 well-formed same-length/rehashed wire mutations change the required original-cell/style facts')
