"""Closed DATA/static invariants, never actual tool/runtime qualification."""
from pathlib import Path
import json,gzip,copy,hashlib,importlib.util,importlib.machinery
F=Path('/tmp/wordling-WP70-tool-selection-DATA-freeze-01')
def validate_selection(old,new,pins,graph,reviewed_graph,source_root):
    selected={r['path']:dict(size=r['bytes'],sha256=r['sha256'],mode=r['mode'],uid=r['uid'],gid=r['gid']) for r in pins}
    external=lambda x:{n:r for n,r in x['files'].items() if not Path(n).is_relative_to(source_root)}
    a=external(old);b=external(new)
    if set(b)-set(a)!=set(selected) or set(a)-set(b):raise RuntimeError('ExternalAdditionSet')
    if any(b[n]!=r for n,r in a.items()):raise RuntimeError('OldExternalRowChanged')
    if any(b[n]!=r for n,r in selected.items()):raise RuntimeError('SelectedRecordMismatch')
    for k in ('links','directories','closed_roots','runtime_elf','runtime_mapped_data','tool_startup_hook_sets','approved_providers'):
        if new[k]!=old[k]:raise RuntimeError('ProtectedManifestSet:'+k)
    if graph!=reviewed_graph:raise RuntimeError('CompilerGraphMismatch')
    if {n['path'] for n in graph['nodes']}!=set(selected) or len(graph['nodes'])!=6:raise RuntimeError('CompilerNodeSet')
    for node in graph['nodes']:
        if node['sha256']!=selected[node['path']]['sha256']:raise RuntimeError('CompilerNodePin')
        for edge in node['needed']+node['loader']:
            if edge['target'] not in a and edge['target'] not in selected:raise RuntimeError('CompilerEdgeTarget')
    return 'EXACT_OLD_PLUS_SIX_STATIC_ONLY'

def main():
    old=json.loads(gzip.decompress((F/'old-expected.json.gz').read_bytes()));new=json.loads(gzip.decompress((F/'new-expected.json.gz').read_bytes()));pins=json.loads((F/'six-selected-inputs.json').read_text())['inputs'];graph=json.loads((F/'compiler-tool-ELF-graph.json').read_text());reviewed=copy.deepcopy(graph)
    source_root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e/internal/document/evidence/reference_controller')
    loader=importlib.machinery.SourceFileLoader('genuine_V7_helper_DATA',str(F/'new-helper.py.txt'));spec=importlib.util.spec_from_loader(loader.name,loader);helper=importlib.util.module_from_spec(spec);loader.exec_module(helper)
    observation=json.loads((F/'recorded-stdlib.stdout.raw').read_text());base=copy.deepcopy(observation);base.update(modules={},maps={},project=None)
    rows=[]
    def outcome(label,fn,wanted):
        try:fn();actual=None
        except RuntimeError as ex:actual=str(ex)
        assert actual==wanted,(label,wanted,actual)
        rows.append(dict(id=len(rows)+1,label=label,status='EXPECTED_RED' if not rows else 'PASS',reason=actual,synthetic_DATA=True))
    actual_error=(F/'actual03-stderr.raw').read_text()
    def historical_refusal():
        assert 'RuntimeError: UnclassifiedToolInput:/usr/libexec/gcc/x86_64-linux-gnu/13/cc1' in actual_error
        assert '/usr/libexec/gcc/x86_64-linux-gnu/13/cc1' not in old['files']
    outcome('genuine-actual03-RED-RECEIPT-ONLY',historical_refusal,None)
    rows[-1]['historical_actual_reason']='UnclassifiedToolInput:/usr/libexec/gcc/x86_64-linux-gnu/13/cc1'
    rows[-1]['old_checker_rerun']=False
    index=json.loads((F/'complete-trace-candidate-index.json').read_text());assert set(index['complete_unknown_candidates'])=={r['path'] for r in pins}
    def complete():
        validate_selection(old,new,pins,graph,reviewed,source_root)
        for r in index['all_successful_open_exec_events']:
            name=r['path'];target=old['links'].get(name,{}).get('resolved',name)
            assert Path(name).is_relative_to('/tmp/wordling-WP70-codex312-qualified-runtime-v3') or target in new['files'] or target in new['directories'],name
    outcome('full-historical-index-static-covered',complete,None)
    def seventh():
        name='/usr/libexec/UNSELECTED-SEVENTH';assert name not in new['files'];d=copy.deepcopy(new);d['files'][name]=copy.deepcopy(new['files'][pins[0]['path']]);validate_selection(old,d,pins,graph,reviewed,source_root)
    outcome('seventh-static-admission-refused',seventh,'ExternalAdditionSet')
    for label,change,want in [
      ('missing-selected',lambda d:d['files'].pop(pins[0]['path']),'ExternalAdditionSet'),
      ('extra-selected',lambda d:d['files'].update({'/usr/libexec/UNSELECTED-EXTRA':copy.deepcopy(d['files'][pins[0]['path']])}),'ExternalAdditionSet'),
      ('changed-hash',lambda d:d['files'][pins[0]['path']].update(sha256='0'*64),'SelectedRecordMismatch'),
      ('changed-mode',lambda d:d['files'][pins[0]['path']].update(mode=0),'SelectedRecordMismatch'),
      ('changed-uid',lambda d:d['files'][pins[0]['path']].update(uid=1),'SelectedRecordMismatch'),
      ('changed-gid',lambda d:d['files'][pins[0]['path']].update(gid=1),'SelectedRecordMismatch')]:
        d=copy.deepcopy(new);change(d);outcome(label,lambda d=d:validate_selection(old,d,pins,graph,reviewed,source_root),want)
    for label,change in [('missing-graph-edge',lambda g:g['nodes'][0]['needed'].pop()),('extra-graph-edge',lambda g:g['nodes'][0]['needed'].append(dict(soname='forged',target='/usr/FORGED',authority='forged')))]:
        g=copy.deepcopy(graph);change(g);outcome(label,lambda g=g:validate_selection(old,new,pins,g,reviewed,source_root),'CompilerGraphMismatch')
    d=copy.deepcopy(new);n=next(n for n in old['files'] if not Path(n).is_relative_to(source_root));d['files'][n]['sha256']='0'*64
    outcome('changed-old-external-row',lambda:validate_selection(old,d,pins,graph,reviewed,source_root),'OldExternalRowChanged')
    for role in ('module','map'):
        for r in pins:
            d=copy.deepcopy(base);name=r['path']
            if role=='module':d['modules']={'synthetic_selected_tool':{'__file__':dict(exists=True,path=name,size=r['bytes'],sha256=r['sha256'])}};want='UnexpectedModuleOrigin:synthetic_selected_tool:'+name
            else:d['maps']={name:dict(size=r['bytes'],sha256=r['sha256'])};want='UnexpectedMappedELF:'+name
            outcome(role+'-denied:'+name,lambda d=d:helper.compare_observation(d,Path(observation['executable']),new,{},False),want)
    assert len(rows)==24
    print(json.dumps(dict(groups=1,variants=rows,production_capture=False,TCB=False,P=False,empty_origins_SYNTHETIC=True,static_manifest_not_execution=True)))
if __name__=='__main__':main()
