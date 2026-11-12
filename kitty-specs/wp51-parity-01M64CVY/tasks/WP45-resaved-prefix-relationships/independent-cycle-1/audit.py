from pathlib import Path
import hashlib,json,subprocess
r=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-s');o=Path('/tmp/wordling-WP45-independent-review');base='d77c5f550b821e2c2e18ec8b794ede9a5bc26d22';owned='docs/research/continuation/resaved-prefix-relationships';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();git=lambda *v:subprocess.check_output(['git',*v],cwd=r);j=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
assert git('rev-parse','HEAD').decode().strip()=='f9a66b8eb7240f3a107fdbb4fadf399c78ad3179'
changes=git('diff','--name-only','HEAD^','HEAD').decode().splitlines();assert len(changes)==25;assert all(p.startswith(owned+'/')or p=='scripts/reference/resaved_prefix_relationships.py'for p in changes)
seal=json.load(open(r/owned/'artifact-manifest.json'))
for x in seal['records']:
 p=r/x['path'];raw=p.read_bytes();assert len(raw)==x['size']and h(p)==x['sha256'];assert git('cat-file','blob',x['git_blob'])==raw;assert git('show','HEAD:'+x['path'])==raw
report=json.load(open(r/owned/'offline-result.json'));data=report['data'];assert hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()==report['data_sha256'];assert len(data['images'])==72
count=0;prefixes={};paired={};numeric=0
for row in data['images']:
 p=row['binding']['path'];raw=(r/p).read_bytes();assert git('show',base+':'+p)==raw;assert git('cat-file','blob',row['binding']['git_blob'])==raw;assert h(r/p)==row['binding']['sha256'];d=row['diagnostic'];B=int.from_bytes(raw[4:8],'little');assert B==d['body_offset'];prefixes[B]=prefixes.get(B,0)+1
 assert d['mutation_permission']is False and d['body_reference_absence_proven']is False
 assert len(d['fields'])==72
 for f in d['fields']:
  assert raw[f['offset']:f['offset']+f['width']].hex()==f['raw_hex'];assert f['offset']==f['owner_extent'][0]+f['relative_offset']
 for f in d['index_fields']:
  assert int.from_bytes(raw[f['offset']:f['offset']+f['width']],'little')==f['value']
 intervals=d['intervals'];last=0
 for x in intervals:assert x['offset']==last;last+=x['length']
 assert last==B
 for residual in d['residuals']:
  count+=1;a=residual['offset'];n=residual['length'];needle=raw[a:a+n];assert needle.hex()==residual['raw_hex'];assert hashlib.sha256(needle).hexdigest()==residual['sha256'];assert residual['unique_origin_proven']is False
  for c in residual['literal_provenance_candidates']:
   source=(r/c['path']).read_bytes();assert source[c['absolute_offset']:c['absolute_offset']+n]==needle
  key=(row['case'],row['stage'],a,n);paired.setdefault(key,[]).append(needle)
  numeric+=len(residual['body_numeric_candidates'])
assert count==126 and len(paired)==63 and all(len(v)==2 and v[0]==v[1]for v in paired.values())
# All inherited Go, module and approved42 sources preserved, including tests.
go=[p for p in git('ls-tree','-r','--name-only',base).decode().splitlines()if(p.startswith('internal/')and p.endswith('.go'))or p in ['go.mod','go.sum']]
assert all((r/p).read_bytes()==git('show',base+':'+p)for p in go)
for n in ['root-graphs.json','family-field-ledger.json']:
 d=json.load(open(r/owned/n));assert d['data_sha256']==report['data_sha256'];assert len(d['images'])==72 if n=='root-graphs.json' else len(d['families'])==6
j(o/'audit.json',{'source':'f9a66b8eb7240f3a107fdbb4fadf399c78ad3179','scope25files':changes,'manifest_exact_records':len(seal['records']),'all_Git_blobs_exact':True,'images':72,'field_values_independently_read_from_native':5184,'prefix_counts':prefixes,'residuals':126,'paired_extents':63,'all_literal_candidates_exact':True,'raw_numeric_coincidences_not_semantic_refs':numeric,'all_inherited_Go_module_paths_exact':len(go),'old42_immutable_native_blobs_preserved':True,'VM_or_originalHD_access':False})
print('Independent literal/source audit PASS:25owned paths,72images/5184fields,126residuals/63pairs, all exact immutable42/native+artifactGitblobs and inheritedGo.')
