from pathlib import Path
import json,hashlib,subprocess,sys,tempfile
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-u');O=Path('/tmp/wordling-wp49-independent');D=R/'docs/research/continuation/text-flow-contract';h=lambda b:hashlib.sha256(b).hexdigest()
assert h((R/'scripts/reference/text_flow_contract.py').read_bytes())=='72bc04b22a2a0a06f7b8915bfb50432d6dfa043f5ccd05ee3d14c0eab26c6c43'
assert h((D/'artifact-manifest.json').read_bytes())=='a633130d8257d0b689c91fc6517dd219734f8f7da14349a2ec6d06f1bf2c02cd'
manifest=json.loads((D/'artifact-manifest.json').read_text());assert len(manifest['records'])==45
for row in manifest['records']:
 path=R/row['path'];assert h(path.read_bytes())==row['sha256']and path.stat().st_size==row.get('bytes',row.get('size'));b=subprocess.check_output(['git','show','HEAD:'+row['path']],cwd=R);assert h(b)==row['sha256']
actual_report=O/'actual-report.json';actual_report=actual_report if actual_report.exists()else D/'offline-result.json';v=json.loads(actual_report.read_text());assert actual_report.read_bytes()==(D/'offline-result.json').read_bytes()
pins=json.loads((O/'source-preflight.json').read_text())['inputs'];assert len(pins)==82
for n,pin in pins.items():
 assert h((R/n).read_bytes())==pin['sha256']and(R/n).stat().st_size==pin['size'];oid=subprocess.check_output(['git','rev-parse','HEAD:'+n],cwd=R,text=True).strip();assert oid==pin['git_blob']
# Independently stream and verify actual approved Git content per unique source object.
sources=v['data']['sources'];unique={x['git_blob']:(x['sha256'],x['bytes'])for x in sources}
with tempfile.TemporaryFile()as requests:
 requests.write(('\n'.join(unique)+'\n').encode());requests.seek(0);proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=requests,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for oid,(want,size)in unique.items():
  header=proc.stdout.readline().split();assert header[0].decode()==oid and header[1]==b'blob'and int(header[2])==size;left=size;digest=hashlib.sha256()
  while left:chunk=proc.stdout.read(min(left,65536));assert chunk;digest.update(chunk);left-=len(chunk)
  assert proc.stdout.read(1)==b'\n'and digest.hexdigest()==want
 assert proc.stdout.read(1)==b''and proc.wait(timeout=60)==0
native=prn=literal=0
for run in v['data']['runs']:
 for state in run['states']:
  for key,pathkey in [('before','before_path'),('after','after_path')]:
   raw=(R/state[pathkey]).read_bytes();data=state[key];body=raw[data['document_offset']:];assert b''.join(bytes.fromhex(x['hex'])for x in data['tokens'])==body and h(body)==data['body_sha256'];native+=1
   for f in data['selected_font_fields']:
    at=f['absolute_offset'];bits=raw[at:at+f['width']];assert bits.hex()==f['raw_hex']and int.from_bytes(bits,'little')==f['literal_u16le_or_u8']and not f['layout_permission'];literal+=1
   for frame in data['format_fields']:
    for f in frame['fields']:assert raw[f['absolute_offset']:f['absolute_offset']+f['width']].hex()==f['raw_hex']
  b=(R/state['print_path']).read_bytes();f=state['full_PRN'];assert b.hex()==f['full_hex']and len(b)==f['bytes']and h(b)==f['sha256'];assert b.split(b'\n')==[bytes.fromhex(x['hex'])for x in f['LF_segments']];prn+=1
assert native==64 and prn==32 and literal==384
changed=next(s for r in v['data']['runs']if r['variant']=='L2-DORMANT'and r['repetition']==1 for s in r['states']if s['id']=='CHANGE');assert changed['before']['body_sha256']!=changed['after']['body_sha256']and'no single-action'in changed['difference_scope']
assert len(v['data']['genesis_observation_only']['original72_field_observations'])==72
assert all(not x['layout_or_emitter_permission']for x in v['data']['rules'])and not v['data']['summary']['closed_layout_or_emitter']and not v['data']['summary']['stage2_justified']
(O/'audit.json').write_text(json.dumps({'source':'775f50c8b71e035973d0030f312521a4c0663917','owned_manifest_records':45,'owned_files_including_manifest':46,'82Go_module_owned_SET_SHA_Git_exact':True,'approved_source_paths':len(sources),'approved_source_bytes':sum(x['bytes']for x in sources),'unique_Git_blobs_hashed':len(unique),'native_snapshots':native,'literal_live_owner_field_observations':literal,'full_PRNs':prn,'all72_genesis_observations_only':True,'actual_report_bytes':actual_report.stat().st_size,'report_byte_exact_archived':True,'report_sha256':h(actual_report.read_bytes()),'reader':v['data']['actual_reader'],'dormant_CHANGE_body_counterexample_retained':True,'closed_layout_or_emitter':False,'Stage2_justified':False,'VM_runs':0},indent=2)+'\n');print('PASS45ownedGit82sourcepins6391approvedpaths/Gitcontent/64native384literalfields32wholePRN/72observations;9.23MB exactreport')
