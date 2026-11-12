#!/usr/bin/env python3
"""Source-bound offline text-flow facts. No renderer, emitter, writer or VM driver."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/research/continuation/text-flow-contract'
BASE = 'docs/research/continuation/text-layout'
WP14 = 'd491d9584d7e5aa60ff12736b18c884a3c28075f'
WP39 = '419edc23d0739d490f2fd2c0094f5cc5eb0b1f80'
WP43 = '90ea1d4f4912e032061baccc6500f4d9ea232415'
SCHEMA = 'wordling.wp49.text-flow-evidence/v1'
FILE_LIMIT = 4*1024*1024
REPORT_LIMIT = 16*1024*1024
TOTAL_LIMIT = 2*1024*1024*1024
COUNT_LIMIT = 10000

class Refusal(ValueError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(detail)

def require(ok, code, detail):
    if not ok:
        raise Refusal(code, detail)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def bounded(path, limit=FILE_LIMIT):
    p=Path(path)
    require(stat.S_ISREG(p.lstat().st_mode),'RegularInput',str(p))
    with p.open('rb') as f:
        raw=f.read(limit+1)
    require(len(raw)<=limit,'InputLimit',str(p))
    return raw

class Custody:
    """Immutable Git tree + bounded working bytes; never checkout or touch disks."""
    def __init__(self):
        self.trees={};self.records={};self.total=0
    def tree(self, ref):
        if ref not in self.trees:
            raw=subprocess.check_output(['git','ls-tree','-r','--full-tree',ref],cwd=ROOT,timeout=20)
            self.trees[ref]={line.split(b'\t',1)[1].decode():line.split(b'\t',1)[0].split()[2].decode() for line in raw.splitlines()}
        return self.trees[ref]
    def read(self, path, ref=WP14):
        require(not Path(path).is_absolute()and '..'not in Path(path).parts,'SourcePath',path)
        key=(ref,path)
        raw=bounded(ROOT/path)
        oid=self.tree(ref).get(path)
        require(oid is not None,'MissingApprovedSource',path)
        observed=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(observed==oid,'ImmutableSourceMismatch',path)
        if key not in self.records:
            self.total+=len(raw)
            require(self.total<=TOTAL_LIMIT and len(self.records)<COUNT_LIMIT,'CustodyLimit','corpus budget')
            self.records[key]={'path':path,'commit':ref,'bytes':len(raw),'sha256':sha(raw),'git_blob':oid}
        return raw
    def json(self,path,ref=WP14):
        return json.loads(self.read(path,ref))
    def identities(self):
        return sorted(self.records.values(),key=lambda x:(x['commit'],x['path']))

def helpers(c):
    # All local import sources are pinned BEFORE importing any old executable.
    for path in ['scripts/reference/text_layout.py','scripts/reference/document.py','scripts/reference/guest.py','scripts/reference/qmp.py','scripts/reference/smoke.py','scripts/reference/extended.py','scripts/reference/advanced.py','scripts/reference/history_loops.py','scripts/reference/iteration_nesting.py','scripts/reference/value_secondary.py']:
        c.read(path)
    c.read(BASE+'/analyze.py')
    sys.path.insert(0,str(ROOT/'scripts/reference'))
    import text_layout
    spec=importlib.util.spec_from_file_location('wp49_approved14_analysis',ROOT/BASE/'analyze.py')
    analysis=importlib.util.module_from_spec(spec);spec.loader.exec_module(analysis)
    return text_layout,analysis

# Actual approved outer frame fields, not a new decoder or generation schema.
FIELD_WORDS={
 'Left/Right Margins':[(4,2,'old left','WPU'),(6,2,'old right','WPU'),(8,2,'new left','WPU'),(10,2,'new right','WPU')],
 'Top/Bottom Margins':[(4,2,'old top','WPU'),(6,2,'old bottom','WPU'),(8,2,'new top','WPU'),(10,2,'new bottom','WPU')],
 'Line Height':[(4,2,'old height','WPU'),(6,2,'new height','WPU; documented zero Automatic only')],
 'Line Spacing':[(4,2,'old spacing','1/256 line'),(6,2,'new spacing','1/256 line')],
 'Justification':[(4,1,'old justification','enum'),(5,1,'new justification','enum')],
 'Page Number Position':[(7,1,'new position','enum'),(8,2,'new font height','WPU')],
 'Leading Adjustment':[(4,2,'old primary','WPU'),(6,2,'old secondary','WPU'),(8,2,'new primary','WPU'),(10,2,'new secondary','WPU')],
 'Center/Align/Tab/Left Margin Release':[(1,1,'flags','bitfield'),(2,2,'absolute start','WPU'),(4,2,'absolute tab alignment','WPU'),(6,2,'screen column','SU; not terminal cells')],
 'Tab Set':[(104,80,'40 new position words','WPU/FFFF sentinel'),(184,20,'new type bytes','packed types'),(204,2,'old creation margin','WPU/FFFF absolute sentinel'),(206,2,'new creation margin','WPU/FFFF absolute sentinel')],
}

def observe_native(raw, tokenizer, analyzer):
    a=tokenizer.annotate(raw)
    require(b''.join(bytes.fromhex(t['hex'])for t in a['tokens'])==raw[a['document_offset']:],'TokenLoss','complete outer body')
    fields=analyzer.format_fields(a)
    for f in fields:
        packet=bytes.fromhex(f['raw_hex']);f['evidence_level']='documentary field applied to observed complete outer frame'
        f['fields']=[]
        for offset,width,label,unit in FIELD_WORDS.get(f['name'],[]):
            require(0<=offset<=len(packet)-width,'FieldBounds',f['name'])
            data=packet[offset:offset+width]
            f['fields'].append({'owner':'complete outer '+f.get('function','C1'),'frame_offset':f['offset'],'relative_offset':offset,'absolute_offset':f['offset']+offset,'width':width,'representation':'u8'if width==1 else'u16le'if width==2 else'raw array','endian':'little'if width==2 else'byte/array','unit':unit,'raw_hex':data.hex(),'value':int.from_bytes(data,'little')if width<=2 else None,'label':label,'source':f['source']})
        if not f['fields']:
            f['unsupported']='opaque payload; no additional field or metric derivation'
    return {'document_offset':a['document_offset'],'body_sha256':a['body_sha256'],'counts':a['counts'],'membership':analyzer.membership(a),'format_fields':fields,'tokens':a['tokens'],'generator_permission':False}

def prefix_font_fields(raw, tokenizer, definitions):
    """Literal live-owner fields from approved23 definitions; no glyph algorithm."""
    try:info=tokenizer.prefix(raw)
    except (ValueError,struct.error,StopIteration,IndexError)as e:raise Refusal('PrefixFields',str(e))from e
    selected={'printed character width','optimal space width','normal space width','horizontal motion units','horizontal fractional numerator','font flags'};out=[]
    for f in definitions:
        if f['name']not in selected:continue
        owners=[x for x in info['packets']if x['type']==int(f['owner'].split('-')[1])]
        require(len(owners)==1,'FontOwner','exact live field owner')
        owner=owners[0];a=f['offset'];n=f['width']
        require(0<=a<=owner['length']-n and owner['offset']+a+n<=info['document_offset'],'FontFieldBounds',f['name'])
        bits=raw[owner['offset']+a:owner['offset']+a+n]
        out.append({'name':f['name'],'owner':f['owner'],'owner_offset':owner['offset'],'relative_offset':a,'absolute_offset':owner['offset']+a,'width':n,'representation':f['representation'],'units':f['units'],'raw_hex':bits.hex(),'literal_u16le_or_u8':int.from_bytes(bits,'little'),'authority':'approved23 field_coverage through immutable43; SDK WP3–18/PDF16–31; observed selected native only','layout_permission':False})
    require(len(out)==6,'FontFieldCount','six selected documented literal fields')
    return out

def print_facts(raw):
    require(0<len(raw)<=FILE_LIMIT,'StreamBounds','complete nonempty PRN')
    return {'bytes':len(raw),'sha256':sha(raw),'full_hex':raw.hex(),'control_positions':{f'{x:02x}':[i for i,b in enumerate(raw)if b==x]for x in sorted(set(raw))if x<32 or x>126},'LF_segments':[{'ordinal':i,'hex':s.hex()}for i,s in enumerate(raw.split(b'\n'))],'first32_hex':raw[:32].hex(),'last32_hex':raw[-32:].hex(),'scope':'all literal initialization/control/termination bytes retained; no driver meanings or physical origins inferred'}

def manuals(c):
    catalog=c.json('docs/research/sources.json');result=[]
    pages={'SDK51':[16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,44,45,46,47,85], 'REF51':[411,412,413,488,489,490,491,492,493,494,495,574,575,576,577]}
    for item in catalog:
        if item['id']not in pages:continue
        p=Path('/home/lynn/projects/wordling/research/cache')/item['filename']
        require(p.stat().st_size==item['bytes'],'ManualIdentity',item['id'])
        with p.open('rb')as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
        require(digest==item['sha256'],'ManualIdentity',item['id'])
        result.append({'id':item['id'],'sha256':digest,'bytes':item['bytes'],'relevant_PDF_pages':pages[item['id']],'private_source':True,'text_published':False})
    require(len(result)==2,'ManualIdentity','SDK/REF sources')
    return result

def actual_reader(c, paths):
    # Validate the assigned existing reader/source closure, not a sibling tip.
    go_paths=subprocess.check_output(['git','ls-tree','-r','--name-only',WP43,'--','internal/wp51','internal/storage','go.mod','go.sum'],cwd=ROOT,text=True).splitlines()
    bound=[p for p in go_paths if p.endswith('.go')or p in ['go.mod','go.sum']]
    actual={str(p.relative_to(ROOT))for name in ['wp51','storage']for p in(ROOT/'internal'/name).rglob('*.go')}|{'go.mod','go.sum'}
    require(actual==set(bound),'ReaderSourceSet','actual inherited Go paths')
    for p in bound:c.read(p,WP43)
    gomod=subprocess.check_output(['go','env','GOMOD'],cwd=ROOT,text=True).strip()
    flags=subprocess.check_output(['go','env','GOFLAGS'],cwd=ROOT,text=True).strip()
    work=subprocess.check_output(['go','env','GOWORK'],cwd=ROOT,text=True).strip()
    require(gomod==str(ROOT/'go.mod')and not flags and work in ['', 'off'],'ReaderEnvironment','exact local module, no GOFLAGS/source overlay/workspace')
    listing=subprocess.check_output(['go','list','-deps','-json','./internal/wp51'],cwd=ROOT,text=True)
    dec=json.JSONDecoder();packages=[]
    while listing.strip():
        row,end=dec.raw_decode(listing.lstrip());listing=listing.lstrip()[end:]
        if row['ImportPath'].startswith('github.com/lynncoleart/wordling/'):
            directory=Path(row['Dir']);require(directory.is_relative_to(ROOT),'ReaderCompilePath',str(directory))
            files={name:sha(c.read(str((directory/name).relative_to(ROOT)),WP43))for name in row['GoFiles']}
            packages.append({'import':row['ImportPath'],'directory':str(directory.relative_to(ROOT)),'GoFiles':files})
    source='''package main
import("bytes";"crypto/sha256";"encoding/json";"fmt";"os";"github.com/lynncoleart/wordling/internal/wp51")
func main(){ rows:=[]map[string]any{};for _,p:=range os.Args[1:]{b,e:=os.ReadFile(p);if e!=nil{panic(e)};v,e:=wp51.Parse(b);row:=map[string]any{"path":p,"accepted":e==nil,"sha256":fmt.Sprintf("%x",sha256.Sum256(b))};if e==nil{row["exact_export"]=bytes.Equal(v.Export(),b)};rows=append(rows,row)};if e:=json.NewEncoder(os.Stdout).Encode(rows);e!=nil{panic(e)}}'''
    OUT.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='reader-',dir=OUT)as temp:
        p=Path(temp)/'main.go';p.write_text(source)
        binary=Path(temp)/'reader';command=['go','build','-trimpath','-buildvcs=false','-o',str(binary),str(p)]
        subprocess.run(command,cwd=ROOT,check=True,timeout=45)
        binary_sha256=sha(bounded(binary,8*1024*1024))
        raw=subprocess.check_output([str(binary),*[str(ROOT/x)for x in paths]],cwd=ROOT,timeout=30)
    rows=json.loads(raw)
    require(len(rows)==len(paths)and all(x['accepted']and x['exact_export']for x in rows),'ReaderRefusal','all64 originals exact export')
    return {'bridge_source_sha256':sha(source.encode()),'binary_sha256':binary_sha256,'build_flags':['-trimpath','-buildvcs=false'],'binary_not_published':True,'actual_cwd':str(ROOT),'actual_GOMOD':gomod,'GOFLAGS':flags,'GOWORK':work,'compiled_local_packages':packages,'go_version':subprocess.check_output(['go','version'],text=True).strip(),'source_paths':bound,'outputs':[{**x,'path':str(Path(x['path']).relative_to(ROOT))}for x in rows],'authority':WP43+' immutable inherited reader, not native writer'}

def check():
    c=Custody();catalog=c.json(BASE+'/analysis.json');tokenizer,analyzer=helpers(c);private_manuals=manuals(c)
    # Genesis supplies observations/metadata only, never layout generation defaults.
    genesis=c.json('docs/research/continuation/native-genesis/analysis/genesis-ledger.json',WP43)
    definitions=c.json('docs/research/continuation/native-edits/field-ledger.json',WP43)['field_coverage']
    c.read('docs/research/continuation/native-genesis/analysis/contract.md',WP43)
    c.read('scripts/reference/macro_quit.py',WP39)
    variants=catalog['repeated_variants'];require(len(variants)==9,'CorpusCardinality','nine paired14 variants')
    rows=[];native_paths=[];histories=[];artifact_count=0
    for pair in variants:
        ids=pair['run_ids'];require(len(ids)==2,'FreshPair','two original witnesses')
        pair_rows=[]
        for repetition,runid in enumerate(ids,1):
            directory=BASE+'/runs/'+runid;run=c.json(directory+'/run.json')
            require(run['variant']==pair['variant']and run['run_id']==runid and run['result']=='observed-local-variant'and run['clean_original_exit']and run['master_unchanged']and run['master_before']==run['master_after'],'RunScope',runid)
            require(all(x['passed']for x in run['checks']),'OriginalCheck',runid)
            evidence={};artifact_count+=len(run['evidence'])
            for item in run['evidence']:
                p=directory+'/'+item['path'];raw=c.read(p);require(len(raw)==item['bytes']and sha(raw)==item['sha256'],'ArtifactIdentity',p);
                if item['path'].endswith(('.WP5','.PRN','screen.txt')):evidence[item['path']]=raw
            profile=json.loads(c.read(directory+'/environment.json'));require(sha(c.read(directory+'/environment.json'))==run['environment_manifest_sha256'],'ProfileIdentity',runid)
            require(run['master_before']=={'harddisk.img':profile['master_disk_sha256'],'boot.img':profile['master_boot_sha256']},'MasterProfile',runid)
            settings=[]
            for x in run['settings']:
                raw=evidence[x['capture']];require(sha(raw)==x['screen_sha256'],'SettingIdentity',x['label']);settings.append({**x,'path':directory+'/'+x['capture'],'text':raw.decode()})
            states=[]
            for state in run['states']:
                before=evidence[state['native_before_print']];after=evidence[state['native_after_print']];prn=evidence[state['print_stream']]
                a=observe_native(before,tokenizer,analyzer);b=observe_native(after,tokenizer,analyzer)
                a['selected_font_fields']=prefix_font_fields(before,tokenizer,definitions);b['selected_font_fields']=prefix_font_fields(after,tokenizer,definitions)
                prior=next(x for x in catalog['runs']if x['run_id']==runid)
                prior_state=next(x for x in prior['states']if x['id']==state['id'])
                difference=analyzer.difference(before,after)
                require(all(prior_state['native_before_after_print'][k]==v for k,v in difference.items()),'DifferenceDisagreement',runid+'/'+state['id'])
                native_paths.extend([directory+'/'+state[k]for k in ['native_before_print','native_after_print']])
                states.append({'id':state['id'],'before_path':native_paths[-2],'after_path':native_paths[-1],'print_path':directory+'/'+state['print_stream'],'before':a,'after':b,'full_PRN':print_facts(prn),'native_difference':analyzer.difference(before,after),'difference_scope':'whole captured port-configuration/print/following-Save protocol; no single-action cache causation'})
            row={'variant':pair['variant'],'run_id':runid,'repetition':repetition,'profile_sha256':run['environment_manifest_sha256'],'master_identity':run['master_before'],'intended_settings':run['intended_settings'],'actual_settings':settings,'variant_input':run['variant_input'],'trace':run['trace'],'executing_runner_sources':run['runner_sources'],'states':states,'resource_metadata':next(x.get('private_resource_audit',[])for x in catalog['runs']if x['run_id']==runid),'VM_rerun':False}
            pair_rows.append(row);rows.append(row)
        left,right=pair_rows
        for name in ['profile_sha256','master_identity','intended_settings','variant_input']:require(left[name]==right[name],'PairPrecondition',pair['variant']+'/'+name)
        require([s['id']for s in left['states']]==[s['id']for s in right['states']],'StateMismatch',pair['variant'])
        for a,b in zip(left['states'],right['states']):
            require(a['before']==b['before']and a['after']==b['after']and a['full_PRN']==b['full_PRN'],'PairMismatch',pair['variant']+'/'+a['id'])
    require(len(rows)==18 and len(native_paths)==64 and artifact_count==6348,'CorpusCardinality','18 witnesses64 snapshots32 streams')
    for x in catalog['runs']:
        if x['run_id']not in {r['run_id']for r in rows}:histories.append({k:x.get(k)for k in ['run_id','variant','result','error','source_hash']})
    reader=actual_reader(c,native_paths)
    facts=rules(rows)
    data={'tool_source_sha256':sha(bounded(Path(__file__))), 'sources':c.identities(),'manuals':private_manuals,'runs':rows,'historical_other_runs':histories,'genesis_observation_only':{'source':WP43,'canonical_JSON_sha256':sha(canonical(genesis)),'not_generation_or_layout_permission':True,'original72_field_observations':genesis['facts']['field_table']},'actual_reader':reader,'rules':facts,'summary':{'original_variants':9,'fresh_witnesses':18,'native_snapshots':64,'complete_streams':32,'captured_artifacts':artifact_count,'rules':len(facts),'closed_layout_or_emitter':False,'stage2_justified':False,'Stage2_reason':'missing full selected resource/stream initialization/physical quantization and format scheduling algorithm cannot be established by at most4 further successful examples; existing14 already supplies the elementary contrasts; precise missing facts remain named','guest_attempts':0,'full_M1_accepted':False}}
    return {'schema':SCHEMA,'data':data,'data_sha256':sha(canonical(data))}

def rules(rows):
    def state(variant,name='BASE'):
        return next(s for r in rows if r['variant']==variant and r['repetition']==1 for s in r['states']if s['id']==name)
    def witnesses(variants):
        return [{'run':r['run_id'],'repetition':r['repetition'],'states':[{'id':s['id'],'native':s['after_path'],'stream':s['print_path'],'stream_sha256':s['full_PRN']['sha256']}for s in r['states']]}for r in rows if r['variant']in variants]
    def fact(ident,kind,variants,value,source,negative):
        return {'id':ident,'evidence_level':kind,'profile_scope':'exact selected mixed-date Standard Printer/US03-09-92/FreeDOS1.4 and individually captured command/settings state; NOT all font/resource/profile combinations','observable':value,'source':source,'witnesses':witnesses(variants),'supported_predicate':'only these source-bound documentary fields/paired empirical observations; no new input layout admission','unsupported_counterexample':negative,'layout_or_emitter_permission':False}
    out=[]
    hr=state('L1-HR')['after'];require(hr['counts'].get('hard-return')==1,'RuleMismatch','alpha Enter beta')
    require([r['text']for r in hr['membership']['rows']]==['alpha','beta'],'RuleMismatch','two HR paragraphs')
    out.append(fact('FLOW-HR','documentary identity + paired observation',['L1-HR'],{'native_code_hex':'0a','native_lines':['alpha','beta']},'REF51 printed557–560/PDF574–577; SDK51 WP19–23/PDF32–36','opaque-payload0A is not an outer return; no paragraph reflow/Enter/history semantics inferred'))
    hp=state('L2-HP')['after'];changed=state('L2-HP-LONG','CHANGE')['after'];require(hp['counts'].get('hard-page')==changed['counts'].get('hard-page')==1,'RuleMismatch','one hard page retained')
    marks=[[r['text'],r['native_page_ordinal']]for r in hp['membership']['rows']];require(marks==[['BEFORE',1],['AFTER',2]],'RuleMismatch','hard page membership')
    out.append(fact('FLOW-HP','documentary identity + paired observation',['L2-HP','L2-HP-LONG'],{'native_code_hex':'0c','baseline_marker_pages':marks,'prepend80words_retains_one_hard_page':True},'REF51 printed471–473/PDF488–490; SDK WP19–23/PDF32–36','native page ordinal from explicit breaks is not general automatic pagination or a PRN FF rule'))
    auto=state('L2-AUTO')['after'];dorm=state('L2-DORMANT','DORMANT');moved=state('L2-DORMANT','CHANGE');base=state('L2-DORMANT')
    starts=lambda s:[r['text'] for i,r in enumerate(s['membership']['rows'])if i==0 or r['native_page_ordinal']!=s['membership']['rows'][i-1]['native_page_ordinal']]
    require(starts(auto)==['P001','P044','P087']and starts(moved['after'])==['P001','P043','P084'],'RuleMismatch','observed page starts')
    require(auto['counts'].get('hard-return')==98 and auto['counts'].get('hard-return-soft-page')==2,'RuleMismatch','combined0x8c')
    require(dorm['after']['counts'].get('dormant-hard-return')==1 and moved['after']['counts'].get('dormant-hard-return',0)==0,'RuleMismatch','dormant native boundary')
    require(base['full_PRN']['full_hex']==dorm['full_PRN']['full_hex']and dorm['full_PRN']['full_hex']!=moved['full_PRN']['full_hex'],'RuleMismatch','complete dormant stream contrast')
    out.append(fact('FLOW-AUTO-DORMANT','paired empirical contrast',['L2-AUTO','L2-DORMANT'],{'auto_page_starts':starts(auto),'moved_top_margin_page_starts':starts(moved['after']),'combined_HRtSPg_hex':'8c','dormant_hex':'99','BASE_DORMANT_full_PRN_equal':True,'CHANGE_full_PRN_different':True},'SDK WP19–23/PDF32–36; REF51 page/return locators retained14','changing top margin alters this boundary; no universal43-lines/page or physical vertical-origin algorithm'))
    wrap=state('L1-WRAP-L3-LR');wrapchange=state('L1-WRAP-L3-LR','CHANGE');require(wrap['after']['counts'].get('soft-return')==6 and wrapchange['after']['counts'].get('soft-return')==7,'RuleMismatch','wrap contrast')
    out.append(fact('FLOW-WRAP-MARGINS','documentary units + paired empirical contrast',['L1-WRAP-L3-LR','L3-TB'],{'baseline_soft_0d':6,'changed_LR_soft_0d':7,'fields':[f for f in wrapchange['after']['format_fields']if f['name']in ['Left/Right Margins','Line Height','Line Spacing','Page Number Position']]},'SDK WP31–34/PDF44–47; REF51 printed394–396/PDF411–413','font10cpi label does not independently derive glyph advance, linebreak algorithm or arbitrary-word geometry'))
    tabs=[]
    for variant,margin,positions in [('L4-ABS',65535,[2400,3600,2400,3600]),('L4-REL',1200,[2700,3900,2700,3900])]:
        fs=state(variant,'CHANGE')['after']['format_fields'];tab=next(f for f in fs if f['name']=='Tab Set');align=[f['absolute_tab_align_wpu']for f in fs if f['name']=='Center/Align/Tab/Left Margin Release']
        require(tab['new_left_margin_word']==margin and align==positions,'RuleMismatch','absolute/relative tabs')
        tabs.append({'variant':variant,'recorded_creation_margin_word':margin,'absolute_alignment_WPU':align,'tab_fields':tab})
    out.append(fact('FLOW-TABS','documentary field units + paired empirical contrast',['L4-ABS','L4-REL'],tabs,'SDK WP23,32/PDF36,45; exact C1/D0/04 outer owners','relative shifts in this state do not qualify all tab kinds, centering, proportional fonts or terminal cell mapping'))
    differences=[{'run':r['run_id'],'state':s['id'],'literal_difference':s['native_difference']}for r in rows for s in r['states']]
    out.append(fact('CACHE-PROTOCOL','literal before/after observation',[r['variant']for r in rows],differences,'SDK WP11/PDF24; actual14 save/Other-port/print/subsequent-save trace','not printing-alone causation, counter increment algorithm, general cache invalidation or mutation admission'))
    allstreams=[s['full_PRN']for r in rows for s in r['states']]
    out.append(fact('PRINT-FULL-BYTES','complete raw paired observations',[r['variant']for r in rows],{'stream_count':len(allstreams),'full_lengths':sorted(set(s['bytes']for s in allstreams)),'form_feed_counts':sorted({len(s['control_positions'].get('0c',[]))for s in allstreams})},'actual selected Standard Printer full streams and captured job completion','full bytes including prefix/suffix preserved, but initialization/termination/CR/LF physical meaning and resource-dependent scheduling are NOT independently derived; no driver/emitter permitted'))
    return out

def plan():
    c=Custody();c.read(BASE+'/analysis.json');c.read(BASE+'/README.md');c.read('scripts/reference/macro_quit.py',WP39);c.read('docs/research/continuation/native-genesis/analysis/contract.md',WP43)
    return {'schema':SCHEMA+'/plan','sources':c.identities(),'mode':'offline-only','Stage1':'existing all9 paired14 native/settings/fullPRN; approved43 genesis observations only','Stage2_proposed':False,'run_enabled':False,'guest_attempts_authorized':0,'reason':'no experiment proposed to substitute for missing selected resource/initialization/geometry derivation; observations/refusals retained','layout_or_emitter_permission':False}

def result(path):
    try:value=json.loads(bounded(path,REPORT_LIMIT))
    except (ValueError,RecursionError)as e:raise Refusal('MalformedReport',str(e))from e
    expected=check()
    require(value==expected,'SemanticMismatch','exact source/units/owners/profile/pairs/rules/stream evidence differs; local rehash is not authority')
    return {'schema':SCHEMA+'/result','verified':True,'data_sha256':expected['data_sha256'],'layout_or_emitter_permission':False,'Stage2_proposed':False,'guest_attempts':0}

def publish(output,text):
    output=Path(output).resolve();require(output.is_relative_to(OUT.resolve()),'OutputScope','owned research JSON path only')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf8',dir=output.parent,prefix='.wp49-',delete=False)as f:
        temporary=Path(f.name);f.write(text)
    try:os.replace(temporary,output)
    finally:temporary.unlink(missing_ok=True)

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    for name in ['check','plan']:
        q=sub.add_parser(name);q.add_argument('--output',type=Path)
    q=sub.add_parser('result');q.add_argument('path',type=Path);sub.add_parser('run');args=p.parse_args()
    try:
        require(args.command!='run','Stage2NotJustified','no reviewed discriminating original plan/root grant; no guest configured')
        value=check()if args.command=='check'else plan()if args.command=='plan'else result(args.path)
        text=json.dumps(value,indent=2,sort_keys=True)+'\n'
        if getattr(args,'output',None):publish(args.output,text)
        else:sys.stdout.write(text)
    except (ValueError,OSError,subprocess.SubprocessError)as e:
        print(json.dumps({'status':'refused','code':getattr(e,'code',type(e).__name__),'detail':str(e),'guest_attempts':0,'layout_or_emitter_permission':False}),file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
