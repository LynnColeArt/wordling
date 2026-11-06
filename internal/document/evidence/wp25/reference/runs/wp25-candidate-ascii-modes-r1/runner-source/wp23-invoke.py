#!/usr/bin/env python3
"""Owned T075 invocation of UNCHANGED approved WP23 engine; no VM at import.

The only engine configuration change is evidence destination routing during
execute(). Source/candidate/relationship semantics remain the approved modules.
Controls add the explicitly declared original typeover-Q command, then reuse the
approved Retrieve/edit-Z/print/Save chain. Baselines are NOT candidate verdicts.
"""
import argparse,hashlib,json,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
APPROVED=ROOT/'docs/research/continuation/native-edits'
sys.path[:0]=[str(ROOT/'scripts/reference'),str(APPROVED)]
import native_edits as n
import candidate_mode as cm
import classify_reader
import codepane_cursor,print_audit
CANDIDATES=HERE.parent/'candidates'

def write(p,value):p.write_text(json.dumps(value,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def snapshot_helpers():
 # Archive exact executing helper sources before every guest. These snapshots are
 # not imported; module objects continue to execute original approved paths.
 source_map={}
 for p in sorted(APPROVED.glob('*.py')):
  target=HERE/('approved-'+p.name)
  if target.exists() and target.read_bytes()!=p.read_bytes():raise ValueError('Approved helper changed after sealing')
  if not target.exists():shutil.copyfile(p,target)
  source_map[str(p)]={'snapshot':str(target.relative_to(ROOT)),'sha256':sha(p)}
 probe=APPROVED/'reader_probe.go.txt';target=HERE/'reader_probe.go.txt'
 if target.exists() and target.read_bytes()!=probe.read_bytes():raise ValueError('Reader probe snapshot changed')
 if not target.exists():shutil.copyfile(probe,target)
 source_map[str(probe)]={'snapshot':str(target.relative_to(ROOT)),'sha256':sha(probe)}
 for p in sorted((ROOT/'scripts/reference').glob('*.py')):source_map[str(p)]={'sha256':sha(p)}
 for p in sorted((ROOT/'internal/document').glob('*.go')):source_map[str(p)]={'sha256':sha(p)}
 source_map[str(Path(__file__))]={'sha256':sha(__file__)}
 return source_map

def control(p):
 p.retrieve('B:\\CANDIDAT','candidate-retrieved')
 retrieved=p.snapshot('candidate-retrieved-native')
 p.at(4,True);p.key('insert');p.q.wait_for('Typeover');p.capture('control-before-typeover-Q')
 p.type('Q');p.capture('control-after-typeover-Q')
 p.key('insert');p.q.wait_absent('Typeover');final=p.snapshot('control-Q-native');p.normal()
 interop=p.interop(final,'control-Q')
 p.cases.append({'id':'candidate-interop','canonical_leads':['CMD51-065','CMD51-066','CMD51-145'],
  'scope':'original two-pair control; local CMD51-047 typeover-Q atgap4 Reveal, not Go candidate acceptance',
  'source':'inputs/candidate.WP5','retrieved':retrieved,'control_final':final,
  'edited':interop['edited'],'after_print':interop['after_print'],'print_stream':interop['print_stream'],
  'control_command':{'mode':'typeover','view':'reveal','gap':4,'text':'Q','result_gap':5},'interop':interop})

def prepared_control():
 source=ROOT/'docs/research/continuation/native-edits/runs/wp23-b-history-follow-repair-restore-r1/N0001.WP5'
 directory=HERE/'control-inputs';directory.mkdir(exist_ok=True)
 body=n.inspect(source.read_bytes(),True)['body_hex']
 assert body=='41c30cc3c40cc4c30cc3584243c40cc444'
 # Existing X+Z stream is a pinned profile/input provenance anchor only. Q+Z
 # baseline has no previous reference and is qualified by two independent raw
 # streams + literal ink/native checks, not by treating this X stream as equal.
 ref=ROOT/'docs/research/continuation/native-edits/runs/wp23-b-history-follow-repair-restore-r1/P0004.PRN'
 expected={'schema_version':1,'candidate_sha256':sha(source),'input_body_hex':body,
  'subsequent_edit':{'command':'append-ascii-at-end','text':'Z','expected_body_hex':'41c30cc3c40cc4c30cc3514243c40cc4445a'},
  'control_extra_original_command':{'mode':'typeover','view':'reveal','gap':4,'text':'Q','expected_gap':5},
  'reference_print':{'path':str(ref),'sha256':sha(ref),'size':ref.stat().st_size},
  'reference_role':'X+Z source/profile anchor; NOT Q+Z expected output. Qualify Q+Z controls by paired exact streams and native/literal ink.',
  'environment_sha256':sha(n.PROFILE)}
 provenance={'rights':'project-authored scratch','producer':'actual approved original repair-Restore source; owned T075 original typeover-Q control',
  'source_sha256':sha(source),'description':'two-pair original control, literal empty first pair retained; no Go candidate verdict'}
 for filename,value in [('expectations.json',expected),('provenance.json',provenance)]:
  path=directory/filename
  if path.exists() and json.loads(path.read_text())!=value:raise ValueError('Changed frozen control input')
  if not path.exists():write(path,value)
 return cm.prepare(source,directory/'provenance.json',directory/'expectations.json')

def invoke(kind,name,repeat):
 if repeat not in (1,2):raise ValueError('Only two declared fresh repetitions')
 sources=snapshot_helpers()
 if kind=='control':
  if name!='two-pair-typeover-Q':raise ValueError('Only declared two-pair control')
  prepared=prepared_control();fn=control
 else:
  directory=CANDIDATES/name
  prepared=cm.prepare(directory/'candidate.WP5',directory/'provenance.json',directory/'expectations.json')
  fn=lambda p:cm.run(p,prepared)
 run_id=f'wp25-{kind}-{name}-r{repeat}'
 invocations=HERE/'invocations';invocations.mkdir(exist_ok=True);invocation=invocations/(run_id+'.json')
 if invocation.exists():raise FileExistsError('Fresh invocation required')
 write(invocation,{'argv':sys.argv,'kind':kind,'name':name,'repeat':repeat,'run_id':run_id,
  'engine_source':str(Path(n.__file__)),'engine_sha256':sha(n.__file__),
  'routing_override':'native_edits.OUT during execute only; restore before relationship comparison; classify_reader.HERE routes unchanged reader-probe temporary acquisition into owned evidence',
  'executing_sources':sources,'prepared_metadata':prepared['metadata']})
 n.configure();original_out=n.OUT
 try:
  n.OUT=HERE
  r=n.execute(run_id,'candidate',fn,prepared)
 finally:n.OUT=original_out
 directory=HERE/'runs'/run_id
 classify_reader.HERE=HERE # same snapshotted reader probe, owned transient directory
 comparison=cm.compare(directory,r) if r['result']=='observed' else {'accepted':False,'run_error':r.get('error')}
 if kind=='candidate':
  write(directory/'comparison.json',comparison)
  if not comparison['accepted']:raise ValueError('Required Go candidate interoperability failed: '+run_id)
 else:
  # Preserve the official candidate comparison as a diagnostic: its X reference
  # is intentionally not the new Q baseline. Do not claim official CLI acceptance.
  write(directory/'candidate-checks-not-a-candidate-verdict.json',comparison)
  if r['result']!='observed':raise ValueError('Original control failed')
  c=r['cases'][0];failed=[v['check'] for v in comparison['checks'] if not v['passed']]
  if failed!=['exact complete reference printer bytes'] or comparison['unresolved']!=failed:raise ValueError('Unresolved control checks: '+str(comparison['unresolved']))
  expected='41c30cc3c40cc4c30cc3514243c40cc444'
  if n.inspect((directory/c['control_final']).read_bytes())['body_hex']!=expected:raise ValueError('Wrong actual control-Q native')
  before=codepane_cursor.gap(directory/c['source'],directory/'control-before-typeover-Q')
  after=codepane_cursor.gap(directory/c['control_final'],directory/'control-after-typeover-Q')
  if (before['gap'],after['gap'])!=(4,5):raise ValueError('Wrong observed original control gaps')
  import relationships
  relation=relationships.compare(directory/c['source'],directory/c['control_final'])
  ink=print_audit.audit(directory/c['after_print'],directory/c['print_stream'])
  write(directory/'control-observation.json',{'status':'observed bounded original control; paired baseline qualification pending',
   'not_candidate_acceptance':True,'before_cursor':before,'after_cursor':after,'final_body_hex':expected,
   'control_relationship':relation,'literal_ink_audit':ink,'other_candidate_protocol_checks':comparison['checks'],
   'new_reference_stream':c['print_stream'],'reference_exception':'No prior Q+Z reference; paired exact original stream qualification required.'})
 print(run_id,'completed',flush=True)

def seal_control():
 observations=[];streams=[]
 for repeat in (1,2):
  directory=HERE/'runs'/f'wp25-control-two-pair-typeover-Q-r{repeat}'
  observation=json.loads((directory/'control-observation.json').read_text());observations.append(observation)
  stream=directory/observation['new_reference_stream'];streams.append(stream)
 if streams[0].read_bytes()!=streams[1].read_bytes():raise ValueError('Fresh control stream mismatch')
 candidate_dir=CANDIDATES/'two-pair-typeover-Q'
 pending=candidate_dir/'expectations.json';sealed=candidate_dir/'expectations-pre-controls.json'
 if sealed.exists():raise FileExistsError('Controls already sealed')
 shutil.copyfile(pending,sealed);e=json.loads(pending.read_text())
 e['reference_print']={'path':str(streams[0]),'size':streams[0].stat().st_size,'sha256':sha(streams[0])}
 e['qualified_original_controls']=[str((HERE/'runs'/f'wp25-control-two-pair-typeover-Q-r{i}'/'control-observation.json').relative_to(ROOT)) for i in (1,2)]
 write(pending,e)
 write(HERE/'two-pair-baseline-seal.json',{'status':'two fresh original controls qualified; Go changed candidate interoperability still unrun',
  'source_body':'41c30cc3c40cc4c30cc3584243c40cc444','control_final_body':observations[0]['final_body_hex'],
  'streams':[{'path':str(p.relative_to(ROOT)),'size':p.stat().st_size,'sha256':sha(p)} for p in streams],
  'exact_stream_equality':True,'before_gap':4,'after_gap':5})

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('kind',choices=['control','candidate','seal-controls']);parser.add_argument('name',nargs='?',default='two-pair-typeover-Q');parser.add_argument('--repeat',type=int,default=1)
 args=parser.parse_args()
 if args.kind=='seal-controls':seal_control()
 else:invoke(args.kind,args.name,args.repeat)
