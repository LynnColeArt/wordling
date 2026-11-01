#!/usr/bin/env python3
"""WP54 offline Retrieve field-history checker. No original-run implementation exists."""
from pathlib import Path
import argparse,json,sys,tempfile
sys.dont_write_bytecode=True
from bounded import Refusal,require,read_limited,atomic_report
import sources
from field_contract import classify,observations
HERE=Path(__file__).resolve().parent

def plan():
 return dict(schema='wordling.retrieve.plan/v1',prelaunch_ready=False,new_original_attempts=0,launch_selection=[],original_stage='BLOCKED; no run path implemented',missing=['second Retrieve empty/recall/prefill frame after successful Retrieve/Save/clear','whole-field typing replacement/cue/cursor in that history','state-specific next key/cancel/normal exit authority','mode after clear: Typeover-before-clear is NOT Typeover-after-clear'],prospective_only=dict(maximum_if_separate_review_and_grant=4,matrix='two fresh reps of each independently justified mode context; NOT launchable',input='existing original43 G43TEXT332B only; no H1/candidate',new_acquisition_requires='separate future task or explicit contract amendment, source/prelaunch review and root grant'),old51=dict(cap=8,spent=1,incomplete=1,qualified=0,H1_observations=0,native_exports=0,abandoned=7,permanent_whole_plan_halt=True),historical46_spent=13,B='BLOCKED; no fallback or native permission',native_permission=False,full_M1='38/91/36/nested/SC001–005 OPEN',M2_PDF='gated')

def context(full=False):
 idx,cache,audit=sources.load(full);decoder=sources.Decoder(idx,cache);records=observations(idx,cache);return records,decoder,audit

def read_packet(path):
 raw=read_limited(path,32*1024)
 try:
  def unique(pairs):
   d={}
   for k,v in pairs:
    require(k not in d,'PacketJSON','duplicate object key');d[k]=v
   return d
  packet=json.loads(raw,object_pairs_hook=unique)
 except (ValueError,UnicodeError,RecursionError)as e:raise Refusal('PacketJSON',str(e))from e
 require(type(packet)is dict,'PacketSchema','JSON object')
 pending=[(packet,0)];nodes=0
 while pending:
  v,depth=pending.pop();nodes+=1;require(depth<=32 and nodes<=4096,'PacketComplexity','finite depth<=32/nodes<=4096')
  if type(v)is dict:pending.extend((x,depth+1)for x in v.values())
  elif type(v)is list:pending.extend((x,depth+1)for x in v)
 return packet

def inspect(packet,records,decoder):
 ident=packet.get('id');require(type(ident)is str and ident in records,'ObservationID','explicit known source context ID, no path lookup');return classify(packet,records[ident],decoder)

def simulate(packet,records,decoder):
 """Public offline transport guard: replay only; no QMP object connects or sends keys."""
 require(type(packet)is dict and set(packet)=={'before','after'},'ReplaySchema','exact before/after packets')
 actions=[]
 try:
  first=inspect(packet['before'],records,decoder);require(first['kind']=='fresh-empty'and not first['diagnosis_only'],'ReplayPredecessor','only paired approved fresh-empty source context')
  after=packet['after'];require(type(after)is dict,'ReplaySchema','after packet object');ident=after.get('id');require(ident in records,'ObservationID','after ID');expected=records[ident]
  require(expected['kind']=='fresh-whole-field-typed'and not ident.startswith('diagnosis/'),'ReplaySuccessor','no diagnostic/error-return as fresh draft')
  require(expected['source_context']['run_id']==records[packet['before']['id']]['source_context']['run_id']and expected['source_context']['capture'].replace('-draft','-prompt')==records[packet['before']['id']]['source_context']['capture'],'ReplayWrapper','same fresh run and field transition')
  actions.append(dict(simulated_only='type-field',literal=expected['literal']))
  second=inspect(after,records,decoder)
  return dict(mode='OFFLINE replay only',actions=actions,matched_after=second,enter_or_next_key_authorized=False,prelaunch_ready=False,real_guest_keys=0)
 except Refusal as e:
  e.replay_actions=actions;raise

def check():
 records,decoder,audit=context(True);positives=[];diagnoses=[]
 for packet in records.values():
  result=inspect(packet,records,decoder)
  (diagnoses if result['diagnosis_only']else positives).append(result)
 require(len(positives)==10 and len(diagnoses)==2,'ObservationRoster','two fresh original iteration sets plus permanently incomplete diagnostics')
 return dict(schema='wordling.retrieve.check/v1',observations=positives,diagnostic_only=diagnoses,source_audit=audit,actual_helper=decoder.provenance(),prelaunch_ready=False,new_original_attempts=0,remaining=plan(),native_read_only_probe='not executed; no fresh native/all72/read/write/admission claim',observation_not_general_prompt_or_H1_qualification=True)

def validate_output(output,packet_path):
 if output is None:return
 target=output.resolve();root=sources.ROOT.resolve()
 if root in target.parents:
  require(any(base.resolve()in target.parents for base in [HERE/'checks',HERE/'reports']),'ReportOwnership','repository reports only under owned checks/reports; no source/raw/historical writes')
 else:require(Path(tempfile.gettempdir()).resolve()in target.parents,'ReportOwnership','external reports only in temporary output directories')
 require(packet_path is None or target!=packet_path.resolve(),'ReportInputCollision','report must not replace its packet input')
 require(not output.exists()or output.is_file(),'ReportPath','only regular report files')

class Parser(argparse.ArgumentParser):
 def error(self,message):raise Refusal('CLIArguments',message)
def main(argv=None):
 output=None
 try:
  parser=Parser(description=__doc__);parser.add_argument('command',choices=['plan','check','packet','inspect','simulate','run']);parser.add_argument('--id');parser.add_argument('--packet',type=Path);parser.add_argument('--output',type=Path);parser.add_argument('--grant');parser.add_argument('--allow-vm',action='store_true');a=parser.parse_args(argv);output=a.output;validate_output(output,a.packet)
  if a.command=='run':raise Refusal('OriginalStageBlocked','no original-run path; any grant or allow-vm flag cannot override missing contract or revive old51')
  require(not a.grant and not a.allow_vm,'CLIArguments','grant/allow-vm cannot enable offline operations')
  if a.command=='plan':require(a.packet is None and a.id is None,'CLIArguments','plan takes no packet/id');result=plan()
  elif a.command=='check':require(a.packet is None and a.id is None,'CLIArguments','check uses finite immutable roster');result=check()
  else:
   records,decoder,_=context()
   if a.command=='packet':require(a.id in records and a.packet is None,'CLIArguments','packet needs known --id only');result=records[a.id]
   else:
    require(a.packet is not None and a.id is None,'CLIArguments','inspect/simulate needs --packet only');p=read_packet(a.packet);result=simulate(p,records,decoder)if a.command=='simulate'else inspect(p,records,decoder)
  raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode();require(len(raw)<=2*1024*1024,'ReportBudget','bounded JSON <=2MiB')
  if output is not None:atomic_report(output,raw)
  sys.stdout.buffer.write(raw);return 0
 except (Refusal,OSError,ValueError,KeyError,TypeError,StopIteration)as e:
  code=e.code if isinstance(e,Refusal)else'InvalidSourceOrInput';result=dict(error=dict(code=code,detail=str(e)),prelaunch_ready=False,new_original_attempts=0,real_guest_keys=0)
  if hasattr(e,'replay_actions'):result['simulated_actions_before_refusal']=e.replay_actions
  # Never replace a success report on validation/IO failure; errors go only to bounded stdout.
  sys.stdout.write(json.dumps(result,sort_keys=True)+'\n');return 2
if __name__=='__main__':raise SystemExit(main())
