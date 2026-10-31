"""Explicit fresh-copy followups; no reset-history assumption or product writer."""
import native_edits as n

def finish(p,label,cid,source,extra=None):
 final=p.snapshot(label+'-final');p.normal()
 c={'id':label,'case_id':cid,'source':source,'final':final,'interop':p.interop(final,label)}
 c.update(extra or {});p.cases.append(c)

def normal_cursor(p):
 for mode in ('insert','typeover'):
  for gap in (1,2,4,5):
   label=f'cursor-normal-{mode}-g{gap}'
   if p.cases:p.normal();p.clear()
   source=p.fixture();p.at(gap,False);p.capture(label+'-before')
   if mode=='typeover':p.key('insert');p.q.wait_for('Typeover')
   p.type('X');p.capture(label+'-after-X')
   # No pane switch or cursor movement between X and Y. Y witnesses actual gap;
   # typeover remains on until after Y, so native records its replacement/insert.
   p.type('Y');p.capture(label+'-after-Y');p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture(label+'-reveal-after-Y')
   if mode=='typeover':p.key('insert');p.q.wait_absent('Typeover')
   finish(p,label,'CMD51-047',source,{'mode':mode,'gap':gap,'view':'normal-XY-then-reveal-no-navigation','marker':'Y'})

def ascii_middle(p):
 source=p.fixture(False);p.at(1,False);p.key('insert');p.q.wait_for('Typeover');p.type('X');p.capture('ascii-intermediate-after-X');p.key('insert');p.q.wait_absent('Typeover')
 finish(p,'ascii-intermediate','CMD51-046',source)

def code_questions(p):
 for gap,key in ((1,'delete'),(5,'backspace')):
  for answer in ('n','f1','esc'):
   label=f'code-question-{key}-g{gap}-{answer}'
   if p.cases:p.normal();p.clear()
   source=p.fixture();p.at(gap,False);p.capture(label+'-before');p.key(key);screen=p.capture(label+'-question')
   if not ('Delete [' in screen and '? No (Yes)' in screen):raise ValueError('Expected exact original code question not observed')
   p.key(answer);p.q.wait_absent('? No (Yes)');p.capture(label+'-answer')
   p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture(label+'-cursor')
   finish(p,label,'CMD51-200' if key=='delete' else 'CMD51-201',source,{'gap':gap,'key':key,'answer':answer})

def history(p,variant):
 source=p.fixture(variant=='repair-restore');records=[];stages=[]
 if variant=='repair-restore':
  p.at(1,True);p.key('alt-f4,right,backspace');p.q.wait_for('Delete Block?');p.capture('repair-question');p.key('y');p.q.wait_absent('Delete Block?');p.capture('repair-result')
  records.append(n.browse(p,'repair-history',previous=1));records.append(n.browse(p,'repair-restore',restore=True));p.capture('repair-after-restore')
  records.append(n.browse(p,'repair-reopen',previous=1));p.capture('repair-after-history')
  # marker without moving cursor; saved native and raw pane resolve actual gap.
  p.type('X');p.capture('repair-restored-marker')
 elif variant in ('consecutive','save-only'):
  p.at(0,False);p.key('delete');p.capture('delete-a')
  if variant=='save-only':stages.append(p.snapshot('saved-between-consecutive-deletes'))
  p.key('delete');p.capture('delete-b')
  records.append(n.browse(p,'grouping',previous=3));records.append(n.browse(p,'grouping-restore',restore=True));p.capture('grouping-restored')
  records.append(n.browse(p,'grouping-reopen',previous=2));p.capture('grouping-after-history')
  p.type('X');p.capture('grouping-restored-marker')
 elif variant=='consume-direct':
  p.at(0,False);p.key('delete,right,delete');p.capture('direct-deletions')
  records.append(n.browse(p,'direct-first',restore=True));p.capture('direct-first-restored')
  records.append(n.browse(p,'direct-second',restore=True));p.capture('direct-second-restored')
  records.append(n.browse(p,'direct-reopen',previous=2));p.capture('direct-after-history')
  p.type('X');p.capture('direct-restored-marker')
 else:raise ValueError('Unknown isolated history recipe')
 finish(p,'follow-history-'+variant,'CMD51-202' if variant=='repair-restore' else 'CMD51-043',source,{'history':records,'intermediates':stages,'marker':'X'})

RECIPES={'normal-cursor':normal_cursor,'ascii-middle':ascii_middle,'code-questions':code_questions,**{'history-follow-'+v:(lambda p,v=v:history(p,v)) for v in ('consecutive','save-only','consume-direct','repair-restore')}}
