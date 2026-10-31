"""Component traces, not original observations or actual mode qualification."""
import copy,unittest
import oracle,ui
from boundaries import Refusal
KINDS=['blank','first-empty','first-typed','loaded','save-before','save-typed','saved','clear-save','clear-exit','blank']
class Replay:
 def __init__(self,leaf,hypothesis='H-empty',bad=None):
  self.leaf=leaf;self.frames=KINDS+(['blank-typeover']if leaf['mode']=='Typeover'else[])+['blank-typeover'if leaf['mode']=='Typeover'else'blank','second-entry','after-F1','empty-save','empty-exit','dos'];self.h=hypothesis;self.events=[];self.bad=bad
 def capture(self,label):
  kind=self.frames.pop(0);f=oracle.example(kind,self.leaf['id'],self.h if kind=='second-entry'else'H-empty')['capture']if kind.startswith('first')or kind=='second-entry'else ui.expected(kind,self.leaf)
  if kind==self.bad:f['text']='UNKNOWN\n'*25
  self.events.append(('capture',kind));return f
 def key(self,key):self.events.append(('key',key))
 def type(self,value):self.events.append(('type',value))
class ProtocolContract(unittest.TestCase):
 def test_twelve_component_traces_firsthistory_insert_second_f1_only(self):
  for leaf in oracle.plan()['leaves']:
   for h in ['H-empty','H-priorRetrieve','H-priorSave']:
    with self.subTest(leaf=leaf['id'],hypothesis=h):
     r=Replay(leaf,h);out=ui.Protocol(r,leaf,lambda:None).perform();self.assertTrue(out['normal_DOS']);self.assertFalse(out['original_qualification']);self.assertEqual(out['hypothesis'],h);self.assertFalse(r.frames)
     pivot=r.events.index(('capture','second-entry'));end=r.events.index(('capture','after-F1'));self.assertEqual(r.events[pivot+1:end],[('key','f1')]);self.assertEqual([x for x in r.events if x[0]=='type'],[('type',leaf['input_literal']),('type',leaf['save_literal'])])
     if leaf['mode']=='Typeover':self.assertLess(r.events.index(('capture','blank'),9),r.events.index(('key','insert')))
 def test_unknown_and_authority_loss_before_effect(self):
  leaf=oracle.plan()['leaves'][0]
  for bad in ['blank','first-empty','first-typed','clear-exit','second-entry','after-F1']:
   with self.subTest(bad=bad):
    r=Replay(leaf,bad=bad)
    with self.assertRaises(Refusal):ui.Protocol(r,leaf,lambda:None).perform()
    self.assertEqual(r.events[-1][0],'capture')
  r=Replay(leaf)
  def deny():raise Refusal('StaleOwner','fork/closed/source changed before primitive')
  with self.assertRaises(Refusal):ui.Protocol(r,leaf,deny).perform()
  self.assertEqual(r.events,[])
 def test_authority_lost_between_capture_and_key(self):
  leaf=oracle.plan()['leaves'][0];r=Replay(leaf);calls=[0]
  def current():
   calls[0]+=1
   if calls[0]>=2:raise Refusal('StaleOwner','same-context changed after capture before effect')
  with self.assertRaises(Refusal):ui.Protocol(r,leaf,current).perform()
  self.assertEqual(r.events,[('capture','blank')])
 def test_public_normal_predictions_still_not_originals(self):
  for leaf in oracle.plan()['leaves']:
   for kind in ['blank','blank-typeover','after-F1','loaded','saved','save-before','save-typed','clear-save','clear-exit','empty-save','empty-exit','dos']:
    r=ui.match(ui.expected(kind,leaf),kind,leaf);self.assertFalse(r['key_permission']);self.assertFalse(r['original_qualification'])
if __name__=='__main__':unittest.main()
