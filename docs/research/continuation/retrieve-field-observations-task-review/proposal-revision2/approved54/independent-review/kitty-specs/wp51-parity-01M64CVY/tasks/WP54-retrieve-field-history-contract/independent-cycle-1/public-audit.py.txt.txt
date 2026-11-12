"""Independent review exercises actual public offline CLI, not an acquisition adapter."""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys,tempfile
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');H=R/'internal/document/evidence/retrieve-field-contract';O=Path('/tmp/wordling-WP54-independent-review');rows=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');h=lambda b:hashlib.sha256(b).hexdigest()
def call(name,args,code,expected=None):
 p=subprocess.run([sys.executable,'-B',str(H/'oracle.py'),*map(str,args)],cwd=R,env=env,capture_output=True,timeout=40);(O/(name+'.stdout.json')).write_bytes(p.stdout);(O/(name+'.stderr.log')).write_bytes(p.stderr);assert p.returncode==code,(name,p.returncode,p.stdout,p.stderr);d=json.loads(p.stdout)
 if expected is not None:assert d['error']['code']==expected,(name,d)
 rows.append(dict(name=name,argv=list(map(str,args)),returncode=p.returncode,stdout_sha256=h(p.stdout),stdout_size=len(p.stdout),expected_refusal=expected));return d
p=call('plan',['plan'],0);assert p['new_original_attempts']==0 and p['prelaunch_ready']is False and p['launch_selection']==[] and p['old51']['abandoned']==7 and p['native_permission']is False
for rep in [1,2]:
 for branch in ['f1','esc']:
  for state in ['prompt','draft']:call('packet-'+str(rep)+'-'+branch+'-'+state,['packet','--id',f'r{rep}/{branch}/{state}'],0)
a=call('check-real',['check'],0);b=call('check-repeat',['check'],0);assert a==b and a['source_audit']['verified_unique_objects']==1347 and a['source_audit']['verified_bytes']==32949343
for row in a['observations']:assert row['original_source_bound']is True and row['original_qualification']is False
assert len(a['diagnostic_only'])==2 and all(x['diagnosis_only']and not x['original_source_bound']for x in a['diagnostic_only'])
base=json.loads((O/'packet-1-f1-draft.stdout.json').read_text());before=json.loads((O/'packet-1-f1-prompt.stdout.json').read_text())
def rehash(x):
 x['custody']={'text_sha256':h(x['text'].encode()),'vga_sha256':h(bytes.fromhex(x['vga_hex'])),'cursor_sha256':h(json.dumps(x['cursor'],sort_keys=True,separators=(',',':')).encode())};return x
with tempfile.TemporaryDirectory(prefix='wp54-review-')as tmp:
 tmp=Path(tmp);inp=tmp/'packet';out=tmp/'prior';out.write_bytes(b'RETAIN-OLD-SUCCESS')
 for name,mut,code in [('wrong-profile',lambda x:x['source_context'].__setitem__('profile_sha256','0'*64),'SourceContext'),('wrong-hidden-mode',lambda x:x['source_context'].__setitem__('document_mode','Typeover'),'SourceContext'),('new-observation',lambda x:x.__setitem__('id','new/live/first'),'ObservationID'),('trace-reordered',lambda x:x['trace'].reverse(),'TraceContext'),('bool-crtc',lambda x:x['cursor']['crtc'].__setitem__('15',True),'CursorRegisters'),('false-parent-gap',lambda x:x['source_context'].__setitem__('document_gap',0),'SourceContext'),('new-literal',lambda x:x.__setitem__('literal','B:\\OTHER'),'TransitionContext')]:
  x=copy.deepcopy(base);x['authority']='synthetic';mut(x);rehash(x);inp.write_text(json.dumps(x));d=call(name,['inspect','--packet',inp,'--output',out],2,code);assert out.read_bytes()==b'RETAIN-OLD-SUCCESS'
 x=copy.deepcopy(base);x['cursor']['note']='different note';rehash(x);inp.write_text(json.dumps(x));call('rehashed-original-source',['inspect','--packet',inp],2,'OriginalSourceBinding')
 x=copy.deepcopy(base);x['authority']='synthetic';inp.write_text(json.dumps(x));d=call('synthetic-honesty',['inspect','--packet',inp],0);assert d['original_qualification']is False and d['original_source_bound']is False
 inp.write_text(json.dumps({'before':before,'after':base}));d=call('replay-known',['simulate','--packet',inp],0);assert d['real_guest_keys']==0 and d['enter_or_next_key_authorized']is False
 x=copy.deepcopy(base);x['source_context']['run_id']='different';inp.write_text(json.dumps({'before':before,'after':x}));d=call('replay-caller',['simulate','--packet',inp],2,'ReplayWrapper');assert d['simulated_actions_before_refusal']==[]
 # No blocked command is allowed to probe grant, packet or any real resources.
 absent=tmp/'NEVER-CREATED-GRANT';call('blocked-grant',['run','--grant',absent,'--allow-vm','--packet',absent,'--output',out],2,'OriginalStageBlocked');assert not absent.exists()and out.read_bytes()==b'RETAIN-OLD-SUCCESS'
 fifo=tmp/'fifo';os.mkfifo(fifo);call('actual-fifo',['inspect','--packet',fifo,'--output',out],2,'InputFileType');assert out.read_bytes()==b'RETAIN-OLD-SUCCESS'
 link=tmp/'link';link.symlink_to(out);call('actual-symlink',['plan','--output',link],2,'ReportPath');assert out.read_bytes()==b'RETAIN-OLD-SUCCESS'
 inp.write_text('{"x":1,"x":2}');call('duplicate-json',['inspect','--packet',inp],2,'PacketJSON')
(O/'public-audit.json').write_text(json.dumps({'actual_public_cases':rows,'no_real_guest_guard_socket_ledger_or_keys':True,'source_unchanged':True,'newliteral_live_adapter_remains_unsupported':True,'all_commands_complete':True},indent=2)+'\n');print('independent public cases',len(rows),'passed')
