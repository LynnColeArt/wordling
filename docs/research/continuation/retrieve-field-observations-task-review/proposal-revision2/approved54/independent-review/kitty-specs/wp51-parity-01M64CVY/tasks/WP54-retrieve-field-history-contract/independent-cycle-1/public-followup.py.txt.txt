"""Follow-up only after reviewer corrected an expectation about the after-frame stage.
The prior changed after-run_id correctly refused SourceContext AFTER local type;
this is not a source failure or a real-key result. Preserve prior script/log/raw.
"""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys,tempfile
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');H=R/'internal/document/evidence/retrieve-field-contract';O=Path('/tmp/wordling-WP54-independent-review');rows=[]
def call(name,args,code,error=None):
 p=subprocess.run([sys.executable,'-B',str(H/'oracle.py'),*map(str,args)],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=40);(O/(name+'.stdout.json')).write_bytes(p.stdout);(O/(name+'.stderr.log')).write_bytes(p.stderr);d=json.loads(p.stdout);assert p.returncode==code
 if error:assert d['error']['code']==error,(name,d)
 rows.append(dict(name=name,argv=list(map(str,args)),returncode=p.returncode,error=error));return d
before=json.loads((O/'packet-1-f1-prompt.stdout.json').read_text());after=json.loads((O/'packet-1-f1-draft.stdout.json').read_text());r2=json.loads((O/'packet-2-f1-draft.stdout.json').read_text())
with tempfile.TemporaryDirectory(prefix='wp54-followup-')as tmp:
 tmp=Path(tmp);p=tmp/'packet';out=tmp/'prior';out.write_bytes(b'KEEP')
 p.write_text(json.dumps({'before':before,'after':r2}));d=call('cross-run-source-wrapper',['simulate','--packet',p],2,'ReplayWrapper');assert d['simulated_actions_before_refusal']==[]
 x=copy.deepcopy(before);x['source_context']['document_mode']='Typeover';p.write_text(json.dumps({'before':x,'after':after}));d=call('unknown-predecessor',['simulate','--packet',p],2,'SourceContext');assert d['simulated_actions_before_refusal']==[]
 absent=tmp/'NEVER-CREATED-GRANT';call('blocked-grant',['run','--grant',absent,'--allow-vm','--packet',absent,'--output',out],2,'OriginalStageBlocked');assert not absent.exists()and out.read_bytes()==b'KEEP'
 fifo=tmp/'fifo';os.mkfifo(fifo);call('actual-fifo',['inspect','--packet',fifo,'--output',out],2,'InputFileType');assert out.read_bytes()==b'KEEP'
 link=tmp/'link';link.symlink_to(out);call('actual-symlink',['plan','--output',link],2,'ReportPath');assert out.read_bytes()==b'KEEP'
 p.write_text('{"x":1,"x":2}');call('duplicate-json',['inspect','--packet',p],2,'PacketJSON')
prior=json.loads((O/'replay-caller.stdout.json').read_text());assert prior['error']['code']=='SourceContext'and len(prior['simulated_actions_before_refusal'])==1 and prior['real_guest_keys']==0
result=dict(followup_cases=rows,reviewer_initial_expectation_correction='After-frame wrong run_id correctly refuses SourceContext after ONE local simulated type; no Enter/real keys. Separate cross-run expected wrapper now proves zero local actions.',source_failures=0,no_guest_guard_or_ledger=True,all_followup_commands_complete=True)
(O/'public-followup.json').write_text(json.dumps(result,indent=2)+'\n');print('six focused followups passed; prior reviewer expectation failure retained')
