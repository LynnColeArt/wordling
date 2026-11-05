#!/usr/bin/env python3
"""Audit SESSION1 cursor/native facts directly from sealed raw evidence."""
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[4]
RUNS = Path(__file__).parent/'runs'


def body(data):
    offset=struct.unpack_from('<I',data,4)[0]
    if not 16<=offset<=len(data):raise ValueError('Invalid captured offset')
    return data[offset:]


def active_columns(path):
    raw=path.read_bytes()
    if len(raw)!=4000:raise ValueError('Expected exact80x25 VGA text/attribute capture')
    return [column for column in range(80) if raw[(13*80+column)*2+1]==0x47]


def audit(prefix):
    reports=[]
    for manifest in sorted(RUNS.glob(prefix+'*/run.json')):
        run=json.loads(manifest.read_text())
        if run['branch']!='cursor':continue
        result=run['results'][0]
        if result['result']!='observed-matches-smoke-expectations':continue
        directory=manifest.parent/result['case_id']
        row={'run_id':run['run_id'],'cursor_pairs':[],'native':[]}
        for left,right,expected_left,expected_right in [('codes-gap-1','codes-gap-2',list(range(1,7)),[7]),('codes-gap-4','codes-gap-5',list(range(9,15)),[15]),('leading-codes-after-initial','leading-codes-before-initial',[6],list(range(6)))]:
            a=json.loads((directory/left/'cursor.json').read_text());b=json.loads((directory/right/'cursor.json').read_text())
            assert (a['row'],a['column'])==(b['row'],b['column'])
            actual=[active_columns(directory/label/'vram.bin') for label in (left,right)]
            assert actual==[expected_left,expected_right],(left,right,actual)
            row['cursor_pairs'].append({'captures':[left,right],'same_hardware_row_column':[a['row'],a['column']],'active_code_pane_columns':actual})
        native={Path(x['path']).name:ROOT/x['path'] for x in result['native_outputs']}
        original=ROOT/run['fixture']['path'];source=original.read_bytes();moved=native['CURSOR.WP5'].read_bytes()
        assert body(source)==body(moved)==bytes.fromhex('41c30cc34243c40cc444')
        assert body(native['LEAD.WP5'].read_bytes())==body(native['LEADPOST.WP5'].read_bytes())==bytes.fromhex('c30cc34c454144c40cc4')
        row['original_save_comparison']={'source_sha256':hashlib.sha256(source).hexdigest(),'output_sha256':hashlib.sha256(moved).hexdigest(),'whole_file_equal':source==moved,'body_equal':body(source)==body(moved),'changed_offsets':[i for i,(a,b) in enumerate(zip(source,moved)) if a!=b],'lengths':[len(source),len(moved)]}
        reports.append(row)
    assert len(reports)==2,'Two dedicated cursor repetitions required'
    prefix_reports=[]
    for manifest in sorted(RUNS.glob(prefix+'*/run.json')):
        run=json.loads(manifest.read_text())
        if run['branch']!='prefix-normal':continue
        result=run['results'][0]
        assert result['result']=='observed-matches-smoke-expectations'
        directory=manifest.parent/result['case_id']
        facts={'run_id':run['run_id'],'views':{}}
        for view in ('normal','codes'):
            captures=['prefix-'+view+'-after-right','prefix-'+view+'-before-right']
            cursors=[json.loads((directory/label/'cursor.json').read_text()) for label in captures]
            positions=[[c['row'],c['column']] for c in cursors]
            assert positions==[[0,1],[0,0]],(view,positions)
            facts['views'][view]={'captures':captures,'hardware_positions':positions}
        native={Path(x['path']).name:ROOT/x['path'] for x in result['native_outputs']}
        assert body(native['PREFIX0.WP5'].read_bytes())==body(native['PREFIX1.WP5'].read_bytes())==bytes.fromhex('c30cc34c454144c40cc4')
        prefix_reports.append(facts)
    assert len(prefix_reports)==2,'Two direct normal-prefix witnesses required'
    return {'cursor_crossing':reports,'direct_prefix':prefix_reports}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('prefix');a=p.parse_args()
    print(json.dumps(audit(a.prefix),indent=2))
