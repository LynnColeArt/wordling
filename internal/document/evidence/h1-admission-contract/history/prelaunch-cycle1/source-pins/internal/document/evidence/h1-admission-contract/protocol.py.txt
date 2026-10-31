"""Original-only counted UI protocol, guarded before and after each primitive."""
from pathlib import Path
import json
import frames,recipes
class Protocol:
 def __init__(self,probe):self.p=probe;self.body='';self.gap=0;self.name=None;self.over=False;self.receipts=[];self.count=0
 def label(self,text):self.count+=1;frames.require(self.count<=240,'CaptureBudget','bounded source-state protocol');return f'{self.count:03d}-{text}'
 def capture(self,spec,label):
  label=self.label(label);text=self.p.capture(label);cursor_path=self.p.out/label/'cursor.json';cursor=json.loads(cursor_path.read_text())if cursor_path.exists()else None;proof=frames.check(text,spec,cursor);self.receipts.append({'capture':label,'expected':spec,'proof':proof});return text
 def current(self,reveal=False):return frames.normal(self.body,self.name,self.gap,self.over,reveal)
 def step(self,key,before,after,label,typed=False):
  self.capture(before,label+'-before')
  if typed:self.p.type(key)
  else:
   frames.require(','not in key or key=='home,home,home,up','UnqualifiedKeyGroup','only approved atomic Home3Up movement gesture may contain prefixes');self.p.key(key)
  return self.capture(after,label+'-after')
 def mode_capture(self,body,name,gap,allow_typeover,label):
  label=self.label(label);text=self.p.capture(label);path=self.p.out/label/'cursor.json';cursor=json.loads(path.read_text())if path.exists()else None;accepted=[]
  for mode in ([False,True]if allow_typeover else[False]):
   try:proof=frames.check(text,frames.normal(body,name,gap,mode),cursor);accepted.append((mode,proof))
   except frames.Refusal:pass
  frames.require(len(accepted)==1,'UnknownModeFrame','only explicitly allowed full normal state variants; no guessed mode');self.over=accepted[0][0];self.body=body;self.name=name;self.gap=gap;self.receipts.append({'capture':label,'mode_observed':self.over,'expected':frames.normal(body,name,gap,self.over),'proof':accepted[0][1]})
 def setup(self):
  self.step('shift-f1',self.current(),{'kind':'fast-save-setup'},'setup')
  self.step('3',{'kind':'fast-save-setup'},{'kind':'fast-save-environment-before'},'environment')
  self.step('5',{'kind':'fast-save-environment-before'},{'kind':'fast-save-answer-question'},'fastsave-choice')
  self.step('n',{'kind':'fast-save-answer-question'},{'kind':'fast-save-environment-after'},'fastsave-no')
  self.step('f7',{'kind':'fast-save-environment-after'},self.current(),'settings-return')
 def retrieve(self,name,body,allow_typeover=False):
  blank=self.current();self.step('shift-f10',blank,{'kind':'retrieve'},'retrieve-prompt')
  self.step('C:\\OUT\\'+name,{'kind':'retrieve'},{'kind':'retrieve','text':'C:\\OUT\\'+name},'retrieve-name',True)
  self.capture({'kind':'retrieve','text':'C:\\OUT\\'+name},'retrieve-enter-before');self.p.key('ret');self.mode_capture(body,name,0,allow_typeover,'retrieved-full-main')
 def reveal_roundtrip(self):
  self.step('alt-f3',self.current(),self.current(True),'known-Reveal')
  self.step('alt-f3',self.current(True),self.current(),'restore-normal')
 def move(self,key):
  before=self.current();gap=0 if key=='home,home,home,up'else len(self.body)if key=='end'else self.gap+1
  frames.require(0<=gap<=len(self.body),'OperationGap','frozen exact ASCII trace');self.gap=gap;self.step(key,before,self.current(),'move')
 def mode(self,want):
  if self.over!=want:
   before=self.current();self.over=want;self.step('insert',before,self.current(),'mode-toggle')
  else:self.capture(self.current(),'mode-already-qualified')
 def text(self,text):
  for char in text:
   before=self.current();self.body=self.body[:self.gap]+char+(self.body[self.gap+1:]if self.over and self.gap<len(self.body)else self.body[self.gap:]);self.gap+=1;self.step(char,before,self.current(),'ASCII',True)
 def operations(self,ops):
  for kind,arg in ops:
   if kind=='text':self.text(arg)
   elif kind=='home':self.move('home,home,home,up')
   elif kind=='end':self.move('end')
   elif kind=='right':
    for _ in range(arg):self.move('right')
   elif kind=='mode':self.mode(arg)
   else:raise frames.Refusal('UnknownOperation',kind)
 def save(self,name):
  self.step('f10',self.current(),{'kind':'save','body':self.body,'name':self.name},'save-prompt')
  self.step('C:\\OUT\\'+name,{'kind':'save','body':self.body,'name':self.name},{'kind':'save','body':self.body,'name':name},'save-name',True)
  before={'kind':'save','body':self.body,'name':name};self.name=name;self.step('ret',before,self.current(),'save-complete');self.p.exports.append((name,name+'.WP5'))
 def clear_retrieve(self):
  body,name,mode=self.body,self.name,self.over
  self.step('f7',self.current(),{'kind':'clear-save','body':body},'clear-Save-question')
  self.step('n',{'kind':'clear-save','body':body},{'kind':'exit-wp','body':body},'clear-exit-question')
  self.capture({'kind':'exit-wp','body':body},'clear-No-before');self.p.key('n');self.mode_capture('',None,0,mode,'clear-blank-known-mode')
  self.retrieve(name,body,mode);self.reveal_roundtrip()
 def print_disk(self):
  menu={'kind':'print-C46PRN-menu'};select={'kind':'print-C46PRN-printer-list'};edit={'kind':'print-C46PRN-printer-edit'};ports={'kind':'print-C46PRN-ports'};other={'kind':'other-path'};entered={'kind':'other-path','text':'C:\\OUT\\H51PRN.PRN'};accepted={'kind':'print-C46PRN-other-accepted'};jobs={'kind':'print-C46PRN-job-status'}
  self.step('shift-f7',self.current(),menu,'print-menu');self.step('s',menu,select,'select-printer');self.step('3',select,edit,'printer-edit');self.step('2',edit,ports,'port-list');self.step('8',ports,other,'other-port');self.step('C:\\OUT\\H51PRN.PRN',other,entered,'print-name',True);self.step('ret',entered,accepted,'print-accepted');self.step('f7',accepted,select,'print-list-return');self.step('f7',select,menu,'print-main-menu');self.step('1',menu,self.current(),'print-submitted');self.step('shift-f7',self.current(),menu,'print-status-menu');self.step('4',menu,jobs,'completed-print-queue');self.step('f7',jobs,self.current(),'print-return');self.p.exports.append(('H51PRN.PRN','H51PRN.PRN'))
 def finish(self):
  self.step('f7',self.current(),{'kind':'clear-save','body':self.body},'final-save-question');self.step('n',{'kind':'clear-save','body':self.body},{'kind':'exit-wp','body':self.body},'final-exit-question');self.step('y',{'kind':'exit-wp','body':self.body},{'kind':'dos'},'normal-DOS');self.capture({'kind':'dos'},'clean-exit')
 def perform(self,index):
  recipe=recipes.operation_plan(index);self.setup();self.retrieve('H1INPUT','');self.reveal_roundtrip();self.operations(recipe['before_Save_S0']);frames.require(self.body==recipe['S0_body'],'InternalRecipe','declared S0 body');self.save('H51S0');initial_mode=self.over;self.clear_retrieve();self.operations(recipe['after_clear_Retrieve_S0']);frames.require(self.body==recipe['S1_FIN_body'],'InternalRecipe','declared S1 body');self.save('H51S1');self.print_disk();self.save('H51FIN');self.finish();return {'recipe':recipe,'initial_and_reload_source_contexts':['exact-supplied-H1-native','original-S0-Save-clear-Retrieve-before-next-ASCII'],'initial_source_sha256':'d490c635fa653ec9a9817e291220285e0794aec0f6a29f18e447d70ee23e5629','receipts':self.receipts,'initial_mode_after_sequence':initial_mode,'body':self.body,'native_API_mutations':0,'H1_permission':False}


def preview(index,clear_mode=False,reload_mode=False):
 """Pure planned UI trace; produces no native bytes, guest or filesystem output."""
 class Planned(Protocol):
  def capture(self,spec,label):
   label=self.label(label);self.receipts.append({'capture':label,'expected':spec});return ''
  def mode_capture(self,body,name,gap,allow_typeover,label):
   selected=clear_mode if label=='clear-blank-known-mode'else reload_mode if name=='H51S0'else False
   frames.require(type(selected)is bool and (not selected or allow_typeover),'UnplannedMode','only predeclared actual known variants')
   self.over=selected;self.body=body;self.name=name;self.gap=gap;self.capture(self.current(),label);self.receipts[-1]['mode_observed']=selected
 class Core:
  def __init__(self):self.exports=[]
  def key(self,key):pass
  def type(self,text):pass
 return Planned(Core()).perform(index)
