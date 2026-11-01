#!/usr/bin/env python3
"""WP57 executable source-contract prerequisite and harmless safety proof.
Original acquisition is disabled by a demonstrated missing PUBLIC startup seam.
No request, review/grant JSON or flag can upgrade this implementation.
"""
from pathlib import Path
import argparse,copy,hashlib,inspect,json,os,re,sys
sys.dont_write_bytecode=True
from enter_sources import B,HERE,ROOT,verify,interfaces,contract,sha
import enter_safety
SCHEMA='wordling.wp57.source-contract-prerequisite/v1'
def plan():
 leaves=[]
 for mode,stem in [('Insert','EI1'),('Typeover','ET1')]:
  for rep in [1,2]:
   ident='wp57-enter-'+mode.lower()+'-r'+str(rep);private='/home/lynn/projects/wordling/research/cache/reference/runs/wp57-enter-v1/'+ident
   leaves.append(dict(id=ident,mode=mode,repetition=rep,initial_text='abc',PRE_literal='C:\\OUT\\'+stem+'PRE',POST_literal='C:\\OUT\\'+stem+'PST',PRE_bytes_hex=('C:\\OUT\\'+stem+'PRE').encode().hex(),POST_bytes_hex=('C:\\OUT\\'+stem+'PST').encode().hex(),private_work=private,public_output=str(HERE/'runs/wp57-enter-v1'/ident),history=['New Insert','abc','PRE Save Insert','source-known gap1','source-known mode '+mode,'ONE Enter','prospective finite split only','mode-aware named POST SaveAs','history-specific saved exit'],output_scope='PREPOST SaveAs-mediated; NOT pure Enter prefix delta',native_cap=65536))
 return dict(schema=SCHEMA+'/plan',leaves=leaves,ordered_failure_inclusive_cap=4,run_enabled=False,originals_attempted=0,old51=dict(incomplete=1,abandoned=7,qualified=0),historical46=13,old55=dict(incomplete=1,abandoned=3,qualified=0),old_grants='DEAD; never reusable',ROOT_logical_reservation=False,original_authority_IO=False)
def binding_report():
 mods=interfaces();rows={}
 for name,fn in [('peer.connect',mods['peer'].connect),('stopping.normal_quit',mods['stopping'].normal_quit),('stopping.validate',mods['stopping'].validate),('account.drive',mods['account'].drive),('OwnedFile.__init__',mods['OwnedFile'].__init__),('native.inspect',mods['native'].inspect),('native.fields72',mods['native'].fields72),('fresh_start',mods['session'].fresh_start)]:
  source_fn=inspect.unwrap(fn);path=Path(inspect.getsourcefile(source_fn)).resolve();rows[name]=dict(path=str(path.relative_to(ROOT)),name=fn.__qualname__,signature=str(inspect.signature(fn)),function_source_sha256=sha(inspect.getsource(source_fn).encode()))
 globals_used=inspect.getclosurevars(mods['stopping'].normal_quit).globals;B.require(globals_used['peer'].connect is mods['peer'].connect,'ImportBinding','actual stop uses actual approved peer.connect')
 return rows
def native_check():
 m=interfaces()['native'];paths=[ROOT/'docs/research/continuation/text-layout/runs/wp14-r01-L1-HR'/n for n in ['BASEB.WP5','BASEA.WP5']];rows=[]
 for p in paths:
  row=m.inspect(p);facts=m.fields72(row);B.require(len(facts['all72_fields'])==72,'Fields72','actual public51 projection');rows.append(facts)
 # Actual approved public outer tokenizer corroborates framing, not a new decoder.
 import text_layout
 report=[]
 for p,row in zip(paths,rows):
  a=text_layout.annotate(B.read(p,65536));report.append(dict(path=str(p.relative_to(ROOT)),raw_0A_count=B.read(p,65536).count(b'\x0a'),outer_HR_count=a['counts'].get('hard-return',0),body_hex=row['body_hex']))
 return dict(schema=SCHEMA+'/native',observations=rows,outer_token_corroboration=report,source_gate=65536,new_native_images=0,writer_or_Enter_permission=False)
def semantic(request):
 B.require(type(request)is dict and set(request)in [{'mode','lines','caret','phase','provenance'},{'mode','lines','caret','phase','provenance','literal'}],'RuleShape','exact pure semantic counterexample envelope; no live capture/authority flags')
 B.require(request['provenance']=='prospective-manual-and-qualified-components-only','ProvenanceForgery','novel rule match is never historical observed qualification');B.require(request['mode']in ['Insert','Typeover'],'Mode','closed planned modes');B.require(request['phase']in ['before','split'],'Phase','closed semantic component only')
 if 'literal'in request:B.require(type(request['literal'])is str and re.fullmatch(r'C:\\OUT\\[A-Z0-9]{1,8}',request['literal'])is not None,'LiteralBoundary','exact DOS ASCII basename; no normalization/path traversal or implicit drive aliases')
 expected=['abc']if request['phase']=='before'else['a','bc'];caret=[0,1]if request['phase']=='before'else[1,0];B.require(request['lines']==expected and request['caret']==caret and all(type(v)is int for v in request['caret']),'UnexpectedEnterShape','lost/replaced b, advance-only, extra body or wrong caret refuse')
 return dict(semantic_prospective_match=True,phase=request['phase'],mode=request['mode'],lines=copy.deepcopy(expected),caret=caret,original_qualification=False,key_permission=False,live_full_frame_match=False,literal_ASCII_hex=request.get('literal','').encode().hex(),missing='full source/grant/owned startup and exact VGA/CRTC/history-aware SaveAs/exit remain unqualified; no transport attached')
def preflight():
 pins=verify();own={p.name:dict(size=p.stat().st_size,sha256=sha(B.read(p,2<<20)))for p in sorted(HERE.glob('*.py'))};c=contract();profile=B.parse(B.read(ROOT/'docs/research/reference-environment/environment.json',65536));p=plan();return dict(schema=SCHEMA+'/preflight',status='BLOCKED0',blocker='SourceContractPrereq',plan=p,source_binding=binding_report(),startup_contract=c,own_source=own,source_count=len(pins['files']),source_bytes=sum(x['size']for x in pins['files'].values()),public_profile_sha256=sha(B.read(ROOT/'docs/research/reference-environment/environment.json',65536)),master_identities_METADATA_ONLY=dict(boot=profile['master_boot_sha256'],harddisk=profile['master_disk_sha256']),private_master_bytes_read=False,originals_attempted=0,original_tickets_spent=0,original_authority_IO=False,independent_prelaunch_READY=False,ROOT_grant=False,run_enabled=False,full_live_frame_protocol_implemented=False,components='public source/ABI audits, native72 facts, pure semantic falsifiers, NEW launch telemetry + actual generic coordinator harmless OS backend',future='separately reviewed public startup prerequisite API; then source protocol/prelaunch review + fresh ROOT grant required; this code cannot run originals')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['plan','source-check','native-check','preflight','inspect-rule','simulate','peer-check','run']);p.add_argument('--input',type=Path);p.add_argument('--output',type=Path);p.add_argument('--fault',default='unknown');p.add_argument('--allow-vm',action='store_true');p.add_argument('--grant');p.add_argument('--source-review');a=p.parse_args()
 try:
  # No grant/review/private path is read, even when caller supplies fake authority.
  if a.command=='run':
   c=contract();raise B.Refusal('SourceContractPrereq','actual fresh_start has no bounded inner runner/launch observer/prepared-resource seam; original acquisition DISABLED')
  B.require(not a.allow_vm and a.grant is None and a.source_review is None,'AuthorityRefusal','offline commands never consume original authority')
  if a.command=='inspect-rule':
   B.require(a.input is not None,'RequestRequired','bounded pure semantic request');B.require(not Path(os.path.abspath(a.input)).is_relative_to(Path('/home/lynn/projects/wordling/research/cache')),'PrivateInputForbidden','no reference private resource/failed-HD input')
   result=semantic(B.parse(B.read(a.input,65536)))
  else:
   B.require(a.input is None,'RequestShape','input only for pure inspect-rule');result=plan()if a.command=='plan'else dict(startup_contract=contract(),bindings=binding_report())if a.command=='source-check'else native_check()if a.command=='native-check'else preflight()if a.command=='preflight'else __import__('enter_peer').challenge(a.fault=='foreign')if a.command=='peer-check'else enter_safety.simulate(plan(),a.fault)
  raw=json.dumps(result,sort_keys=True,indent=2).encode()+b'\n';B.require(len(raw)<=2<<20,'ReportBudget','bounded public report')
  if a.output:
   target=a.output.absolute();B.require(target.parent==HERE and target.name.endswith('.result.json'),'OutputScope','only owned immediate *.result.json reports');B.atomic_report(target,raw)
  else:sys.stdout.buffer.write(raw)
  return 0
 except (ValueError,OSError,KeyError,TypeError)as e:
  print(json.dumps(dict(error=getattr(e,'code',type(e).__name__),detail=str(e),original_tickets_spent=0,actual_original_launched=0,original_authority_IO=False,original_qualification=False,note='57 original path is structurally disabled; harmless OS counts, if requested, are separately derived inside simulate')),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
