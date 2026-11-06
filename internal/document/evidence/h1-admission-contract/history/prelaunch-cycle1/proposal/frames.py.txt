"""Closed source-bound text frames. Real helper agreement is necessary, not enough."""
from pathlib import Path
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts/reference'))
import macro_session,macro_quit
class Refusal(ValueError):
 def __init__(self,code,detail):self.code=code;super().__init__(detail)
def require(ok,code,detail):
 if not ok:raise Refusal(code,detail)
def rows(text):
 result=text.split('\n');return result[:-1]if result and result[-1]==''else result
def atlas():
 a=json.loads((HERE/'frame-atlas.json').read_text())
 for pin in a['templates'].values():
  path=ROOT/pin['path'];require(path.stat().st_size==pin['size']and hashlib.sha256(path.read_bytes()).hexdigest()==pin['sha256'],'FrameSourceDrift',pin['path'])
 return a
def template(label):return rows(atlas()['templates'][label]['text'])
def status(name,gap,over=False):
 a=atlas();require(str(gap)in a['position_witnesses'],'GapUnqualified','no source-qualified position witness');prefix='Typeover'if over else('C:\\OUT\\'+name if name else'')
 return prefix.ljust(a['normal_Doc_column'])+a['position_witnesses'][str(gap)]['status_suffix']
def expected(spec):
 kind=spec['kind'];body=spec.get('body','');require(len(body)<=9 and all(' '<=x<='~'for x in body),'BodyBudget','closed short single-line ASCII frames only')
 if kind in ['normal','reveal']:
  result=template(kind);result[0]=body;result[11 if kind=='reveal'else 24]=status(spec.get('name'),spec['gap'],spec.get('over',False))
  if kind=='reveal':result[13]=body
  return '\n'.join(result)+'\n'
 if kind in ['save','clear-save','exit-wp']:
  result=template(kind);result[0]=body
  if kind=='save':result[24]='Document to be saved:'+(' C:\\OUT\\'+spec['name']if spec.get('name')else'')
  return '\n'.join(result)+'\n'
 if kind=='retrieve':
  result=template(kind);text=spec.get('text','');line=result[24];column=line.index('(List Files)');prefix='Document to be retrieved: ';require(len(prefix+text)<column,'PromptBudget','literal name must fit original field');result[24]=(prefix+text).ljust(column)+'(List Files)';return '\n'.join(result)+'\n'
 if kind=='other-path':
  result=template('print-C46PRN-other-path');result[-1]='Device or Filename:'+(' '+spec['text']if spec.get('text')else'');return '\n'.join(result)+'\n'
 result=template(kind)
 return '\n'.join(result).replace('C46PRN','H51PRN')+'\n'
def check(text,spec,cursor=None):
 require(len(rows(text))==25,'FrameShape','exact25 text rows, literal rulerRS is not a new row')
 want=expected(spec);require(text==want,'UnknownFrame','full body/status/ruler/prompt shape differs; no next key')
 kind=spec['kind'];state=macro_quit.exit_state(text);main=macro_session.main_document(text)
 if kind=='normal':require(state=='main'and main,'HelperStateMismatch','actual approved helpers must agree with exact normal frame')
 elif kind=='reveal':require(state=='unknown'and not main,'HelperStateMismatch','actual helper does not classify Reveal; exact independently sourced Reveal frame is required, never relabel unknown generic main')
 elif kind in ['clear-save','exit-wp','dos']:require(state=={'clear-save':'save','exit-wp':'exit-wp','dos':'dos'}[kind],'HelperStateMismatch','actual captured state differs')
 if kind in ['normal','reveal']:
  require(cursor is not None and type(cursor.get('row'))is int and type(cursor.get('column'))is int and cursor['row']==0 and cursor['column']==spec['gap'],'CursorFrameMismatch','actual hardware witness must agree with source-bound logical trace/body/status; no semantic gap inferred from hardware alone')
 return {'kind':kind,'actual_helper':state,'full25row_match':True,'cursor_checked':kind in ['normal','reveal']}
def normal(body,name,gap,over=False,reveal=False):return {'kind':'reveal'if reveal else'normal','body':body,'name':name,'gap':gap,'over':over}
