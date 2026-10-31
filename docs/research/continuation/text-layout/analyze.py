#!/usr/bin/env python3
"""Derive checkable native-token/stream observations without rewriting evidence."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import subprocess
import struct
import sys


HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PRIVATE=Path(os.environ.get('WORDLING_REFERENCE_PRIMARY','/home/lynn/projects/wordling')).resolve()/'research/cache/reference'
sys.path.insert(0,str(ROOT/'scripts/reference'))
from document import prefix


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def membership(annotation):
    page=line=1;text=[];start=None;rows=[];hints=[]
    def flush(end):
        nonlocal text,start
        if text:
            rows.append({'native_page_ordinal':page,'native_line_ordinal':line,
                         'text':''.join(text),'first_ascii_offset':start,'ending_token_offset':end})
        text=[];start=None
    for token in annotation['tokens']:
        kind=token['kind']
        if 'formatter_page_number' in token:
            hints.append({'offset':token['offset'],'page_number_field':token['formatter_page_number']})
        if kind=='ascii':
            if start is None:start=token['offset']
            text.append(chr(int(token['hex'],16)))
        elif kind in ['hard-return','soft-return','deletable-soft-return']:
            flush(token['offset']);line+=1
        elif kind in ['soft-page','hard-page','hard-return-soft-page','deletable-soft-page','forward-format-deletable-page']:
            flush(token['offset']);page+=1;line=1
    flush(None)
    return {'scope':'single-byte-break-derived-membership-not-general-layout',
            'rows':rows,'formatter_page_hints':hints,'native_page_ordinals':page,
            'limitations':'Opaque payloads and tab advances are not interpreted. Ordinals follow outer break tokens; formatter fields remain separate corroboration, not an extra page increment.'}


def difference(a,b):
    return {'equal':a==b,'bytes':[len(a),len(b)],
            'sha256':[hashlib.sha256(x).hexdigest() for x in (a,b)],
            'differing_byte_count_in_common_extent':sum(x!=y for x,y in zip(a,b)),
            'first_differing_offsets':[i for i,(x,y) in enumerate(zip(a,b)) if x!=y][:128],
            'length_difference':len(b)-len(a),'normalized':False}


def format_fields(annotation):
    """Documentary field readings of checked selected outer frames, not edits."""
    rows=[]
    for token in annotation['tokens']:
        raw=bytes.fromhex(token['hex']);code=raw[0]
        if code==0xc1 and len(raw)==9:
            rows.append({'offset':token['offset'],'name':'Center/Align/Tab/Left Margin Release',
                         'source':'SDK51 WP23 / PDF36','raw_hex':raw.hex(),'flags':raw[1],
                         'absolute_start_wpu':struct.unpack_from('<H',raw,2)[0],
                         'absolute_tab_align_wpu':struct.unpack_from('<H',raw,4)[0],
                         'screen_column_su':struct.unpack_from('<H',raw,6)[0]})
            continue
        if code<0xd0 or len(raw)<8:continue
        sub=raw[1];row={'offset':token['offset'],'function':f'{code:02x}/{sub:02x}','raw_hex':raw.hex()}
        u16=lambda offset:struct.unpack_from('<H',raw,offset)[0]
        if code==0xd0 and sub in (1,5) and len(raw)==16:
            row.update(name='Left/Right Margins' if sub==1 else 'Top/Bottom Margins',
                       source='SDK51 WP31 / PDF44' if sub==1 else 'SDK51 WP33 / PDF46',
                       unit='WPU (1/1200 inch)',old_values=[u16(4),u16(6)],new_values=[u16(8),u16(10)])
        elif code==0xd0 and sub==0 and len(raw)==12:
            row.update(name='Line Height',source='SDK51 WP31 / PDF44',unit='WPU; zero=Automatic',old_value=u16(4),new_value=u16(6))
        elif code==0xd0 and sub==2 and len(raw)==12:
            row.update(name='Line Spacing',source='SDK51 WP31 / PDF44',unit='1/256 line; high byte=whole lines',old_value=u16(4),new_value=u16(6))
        elif code==0xd0 and sub==6 and len(raw)==10:
            row.update(name='Justification',source='SDK51 WP33 / PDF46',unit='enum:0 Left,1 Full,2 Center,3 Right,4 table Decimal',old_value=raw[4],new_value=raw[5])
        elif code==0xd0 and sub==8 and len(raw)==14:
            row.update(name='Page Number Position',source='SDK51 WP34 / PDF47',new_position_code=raw[7],new_font_height_wpu=u16(8))
        elif code==0xd0 and sub==4 and len(raw)==212:
            positions=[u16(104+2*i) for i in range(40)]
            row.update(name='Tab Set',source='SDK51 WP32 / PDF45',unit='WPU; rawFFFF unused/absolute sentinel retained',
                       new_position_words=positions,new_type_bytes=raw[184:204].hex(),old_left_margin_word=u16(204),new_left_margin_word=u16(206))
        elif code==0xd0 and sub==11:
            row.update(name='Form / Paper Definition',source='SDK51 WP34ff / PDF47ff',payload_interpretation='opaque; exact selected definition is corroborated by captured original menus')
        elif code==0xd9 and sub==5 and len(raw)==16:
            row.update(name='Leading Adjustment',source='SDK51 WP72 / PDF85',unit='WPU',old_values=[u16(4),u16(6)],new_values=[u16(8),u16(10)])
        else:continue
        rows.append(row)
    return rows


def resource_audit(run_dir,run):
    # Read only the stopped, cleanly-exited run image. Proprietary resource bytes
    # are retained privately; the public report contains identity metadata only.
    if not run.get('clean_original_exit'):raise ValueError('No clean original exit')
    work=PRIVATE/'text-layout-runs'/run['run_id']
    image=work/'harddisk.img'
    archive=work/'resource-archive';archive.mkdir(exist_ok=True)
    installed={x['path']:x for x in json.loads((ROOT/'docs/research/reference-environment/installed-files.json').read_text())['files']}
    rows=[]
    for name in ['WP.EXE','WP.FIL','WP.DRS','STANPRIN.PRS','WP{WP}.SET']:
        path=archive/name
        if not path.exists():
            subprocess.run(['mcopy','-i',str(image)+'@@1048576','::WP51/'+name,str(path)],check=True,capture_output=True)
        expected=installed['WP51/'+name]
        matched=sha(path)==expected['sha256'] and path.stat().st_size==expected['size']
        if name!='WP{WP}.SET' and not matched:raise ValueError('Pinned resource changed: '+name)
        rows.append({'guest_path':'C:\\WP51\\'+name,'bytes':path.stat().st_size,'sha256':sha(path),
                     'baseline_sha256':expected['sha256'],'matches_baseline':matched,
                     'mutable_original_settings':name=='WP{WP}.SET','private_raw_archive':str(path),
                     'redistribution':'not published; original resource/settings retained privately'})
    return rows


def inspect_run(path,private=False):
    run=json.loads((path/'run.json').read_text())
    if run['scope']!='original-reference-only' or run['wordling_tested'] is not False:raise ValueError('Bad scope')
    for row in run['evidence']:
        file=path/row['path']
        if sha(file)!=row['sha256'] or file.stat().st_size!=row['bytes']:raise ValueError('Evidence changed '+str(file))
    result={'run_id':run['run_id'],'variant':run['variant'],'result':run['result'],
            'master_unchanged':run['master_unchanged'],'source_hash':next(x['sha256'] for x in run['runner_sources'] if x['path'].endswith('/text_layout.py')),
            'profile_hash':run['environment_manifest_sha256'],'master_identity':run['master_before'],
            'intended_settings':run['intended_settings'],'variant_input':run['variant_input'],
            'error':run.get('error'),'states':[]}
    if run['result']!='observed-local-variant':return result
    if not run.get('clean_original_exit') or not run['master_unchanged']:raise ValueError('Unclean/mutated accepted run')
    if any(not row['passed'] for row in run['checks']):raise ValueError('Failed check in accepted run')
    for state in run['states']:
        before=path/state['native_before_print'];after=path/state['native_after_print'];stream=path/state['print_stream']
        a=json.loads((path/(after.name+'.annotation.json')).read_text())
        if a['body_sha256']!=hashlib.sha256(after.read_bytes()[a['document_offset']:]).hexdigest():raise ValueError('Body annotation mismatch')
        raw=stream.read_bytes()
        before_bytes=before.read_bytes();after_bytes=after.read_bytes()
        before_prefix=prefix(before_bytes);after_prefix=prefix(after_bytes)
        native_change=difference(before_bytes,after_bytes)
        native_change['document_flags']=[before_prefix['document_flags'],after_prefix['document_flags']]
        native_change['body_equal']=before_bytes[before_prefix['document_offset']:]==after_bytes[after_prefix['document_offset']:]
        native_change['byte_differences']=[{'offset':i,'before':x,'after':y} for i,(x,y) in enumerate(zip(before_bytes,after_bytes)) if x!=y][:128]
        flags=[next(p for p in info['packets'] if p['type']==6) for info in [before_prefix,after_prefix]]
        if all(p['length']>=9 for p in flags):
            native_change['printer_select_count_flag']={'source':'SDK51 WP11 / PDF24, Packet6+8',
                'offsets':[p['offset']+8 for p in flags],
                'values':[data[p['offset']+8] for data,p in zip([before_bytes,after_bytes],flags)],
                'scope':'Observed across Other-port configuration, print and subsequent save; not attributed to printing alone.'}
        ascii_native=''.join(chr(int(t['hex'],16)) for t in a['tokens'] if t['kind']=='ascii')
        if not raw:raise ValueError('Empty print stream')
        variant=run['variant']
        if variant=='L1-HR':
            if ascii_native!='alphabeta' or raw.count(b'alpha')!=1 or raw.count(b'beta')!=1:raise ValueError('Hard return fixture text lost')
        elif variant in ['L1-WRAP-L3-LR','L3-TB']:
            if raw.count(b'word')!=80:raise ValueError('Wrapping text lost')
        elif variant in ['L2-HP','L2-HP-LONG']:
            if a['counts'].get('hard-page')!=1 or raw.count(b'BEFORE')!=1 or raw.count(b'AFTER')!=1 or raw.index(b'BEFORE')>raw.index(b'AFTER'):raise ValueError('Hard page fixture lost')
            expected_words=80 if variant=='L2-HP-LONG' and state['id']=='CHANGE' else 0
            if raw.count(b'word')!=expected_words:raise ValueError('Prepend text lost')
        elif variant in ['L2-AUTO','L2-DORMANT']:
            positions=[]
            for n in range(1,101):
                marker=f'P{n:03}'.encode()
                if raw.count(marker)!=1 or ascii_native.count(marker.decode())!=1:raise ValueError('Paragraph marker lost')
                positions.append(raw.index(marker))
            if positions!=sorted(positions):raise ValueError('Paragraph order changed')
        elif variant in ['L4-ABS','L4-REL']:
            if ascii_native!='ABCAABBCC' or any(raw.count(bytes([c]))!=3 for c in b'ABC'):raise ValueError('Tab fixture text lost')
        result['states'].append({**state,'native_before_after_print':native_change,
                                 'native_counts':a['counts'],'membership':membership(a),'documentary_format_fields':format_fields(a),
                                 'raw_stream_bytes':len(raw),'raw_stream_sha256':sha(stream),
                                 'stream_lf_segments':[{'index':i,'hex':part.hex()} for i,part in enumerate(raw.split(b'\n')) if part.replace(b'\r',b'').strip(b' ')],
                                 'stream_control_counts':{f'{k:02x}':v for k,v in sorted(Counter(x for x in raw if x<32 or x>126).items())}})
    if private:result['private_resource_audit']=resource_audit(path,run)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-resources',action='store_true')
    p.add_argument('--require-complete-pairs',action='store_true')
    p.add_argument('--output',required=True)
    args=p.parse_args()
    output=Path(args.output)
    if output.exists():raise FileExistsError('Do not overwrite an analysis revision')
    runs=[inspect_run(x.parent,args.private_resources) for x in sorted((HERE/'runs').glob('*/run.json'))]
    groups=defaultdict(list)
    for run in runs:
        if run['run_id'].startswith('wp14-r') and run['result']=='observed-local-variant':groups[run['variant']].append(run)
    pairs=[]
    for variant,group in groups.items():
        pair={'variant':variant,'fresh_run_count':len(group),'run_ids':[x['run_id'] for x in group],
              'runner_hashes':[x['source_hash'] for x in group],'state_comparisons':[]}
        if len(group)==2:
            left,right=group
            pair['same_profile_and_inputs']=all(left[k]==right[k] for k in ['profile_hash','master_identity','intended_settings','variant_input'])
            if not pair['same_profile_and_inputs']:raise ValueError('Repeated profile/input changed')
            if [s['id'] for s in left['states']]!=[s['id'] for s in right['states']]:raise ValueError('Variant state mismatch')
            for a,b in zip(left['states'],right['states']):
                d1=HERE/'runs'/left['run_id'];d2=HERE/'runs'/right['run_id']
                pair['state_comparisons'].append({'state':a['id'],
                    'native_before_print':difference((d1/a['native_before_print']).read_bytes(),(d2/b['native_before_print']).read_bytes()),
                    'native_after_print':difference((d1/a['native_after_print']).read_bytes(),(d2/b['native_after_print']).read_bytes()),
                    'raw_print_stream':difference((d1/a['print_stream']).read_bytes(),(d2/b['print_stream']).read_bytes()),
                    'native_counts_equal':a['native_counts']==b['native_counts'],
                    'membership_equal':a['membership']==b['membership']})
        pairs.append(pair)
    complete={p['id'] for p in json.loads((HERE/'recipe-plan.json').read_text())['variants']}
    if args.require_complete_pairs and (set(groups)!=complete or any(len(x)!=2 for x in groups.values())):
        raise ValueError('Every planned local variant needs exactly two accepted fresh repetitions')
    if args.require_complete_pairs:
        for pair in pairs:
            for state in pair['state_comparisons']:
                if not all(state[k]['equal'] for k in ['native_before_print','native_after_print','raw_print_stream']) or not state['native_counts_equal'] or not state['membership_equal']:
                    raise ValueError('Unexplained repeated native/stream/membership difference: '+pair['variant']+'/'+state['state'])
    result={'scope':'original-reference-only-derived-observations','wordling_tested':False,
            'normalization':False,'runs':runs,'repeated_variants':pairs,
            'NFR005_accepted':False,'unresolved':['No historical DOS corroboration','No matched graphics/fonts/preview','Physical coordinate origins and printer metric quantization not qualified','No positional tolerance selected','Full M1 and all canonical scenarios remain open']}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('Analyzed',len(runs),'runs and',len(pairs),'variant groups without normalization')


if __name__=='__main__':main()
