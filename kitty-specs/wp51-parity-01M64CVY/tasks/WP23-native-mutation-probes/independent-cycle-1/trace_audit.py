import hashlib,json
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-k');here=root/'docs/research/continuation/native-edits'
plan=json.loads((here/'selection-plan.json').read_text());checks=[]
for recipe,prefix in plan['required_pairs'].items():
 for rep in (1,2):
  path=here/'runs'/f'{prefix}-r{rep}';r=json.loads((path/'run.json').read_text());trace=r['trace'];captures={x['capture']:i for i,x in enumerate(trace) if 'capture' in x}
  for c in r['cases']:
   label=c['id']
   if label.startswith('boundary-') or label.startswith('delete-') or recipe=='normal-questions':
    i=captures[label+'-before'];before=[x['key'] for x in trace[max(0,i-4):i] if 'key' in x];expected=['home,home,home,up']
    if c['gap']:expected.append(','.join(['right']*c['gap']))
    if c.get('view')=='reveal':expected.append('alt-f3')
    assert before[-len(expected):]==expected,(r['run_id'],label,before,expected)
    after=trace[i+1:]
    if label.startswith('boundary-'):
     if c['mode']=='typeover':assert after[0]=={'key':'insert'};after=after[1:]
     assert after[0]=={'type':'X'},(label,after[:3])
    else:
     assert after[0]=={'key':c['key']},(label,after[0])
     if recipe=='normal-questions':
      j=captures[label+'-question'];assert trace[j+1]=={'key':c['answer']}
    checks.append({'run':r['run_id'],'case':label,'incoming_gap_view_command_trace_bound':True})
assert len(checks)==72,len(checks)
print(json.dumps({'checked_case_instances':len(checks),'checks':checks},indent=2))
