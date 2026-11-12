"""Queued finite normal code-question cancellation recipe, no history assumptions."""
import native_edits as n

def run(p):
 for gap,key in ((1,'delete'),(4,'delete'),(2,'backspace'),(5,'backspace')):
  for answer in ('n','f1','esc'):
   label=f'normal-question-{key}-g{gap}-{answer}'
   if p.cases:p.normal();p.clear()
   source=p.fixture();p.at(gap,False);p.capture(label+'-before');p.key(key);screen=p.capture(label+'-question')
   if not ('Delete [' in screen and '? No (Yes)' in screen):raise ValueError('Required original normal code question missing')
   p.key(answer);p.q.wait_absent('? No (Yes)');result=p.capture(label+'-result')
   if 'Undelete:' in result:raise ValueError('Question answer entered distinct history context; no guessed cleanup')
   block='Block on' in result or '[Block]' in result
   if block:raise ValueError('Unexpected persistent block context; no guessed cleanup')
   p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture(label+'-cursor')
   final=p.snapshot(label+'-final');p.normal()
   p.cases.append({'id':label,'case_id':'CMD51-200' if key=='delete' else 'CMD51-201','source':source,'final':final,'gap':gap,'key':key,'answer':answer,'view':'normal-then-reveal-no-navigation','question':screen.splitlines()[-1],'block_persisted':block,'interop_alias_required':True,'alias_rule':'must equal entire SHA/length/bytes of an actually interoperated native input; body equality alone is insufficient'})
