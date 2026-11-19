import json, sys, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0,'scripts/reference/everyday')
from run import perform, qmp
evidence = Path(__file__).resolve().parent.parent
pairs = [pair for i in range(6) for pair in json.loads((evidence / f'compose-final-{i}' / 'input-pairs.json').read_text())]
punct=dict(zip("!*?':\\^@`\"~,-=_/.;<>+",'shift-1 shift-8 shift-slash apostrophe shift-semicolon backslash shift-6 shift-2 grave_accent shift-apostrophe shift-grave_accent comma minus equal shift-minus slash dot semicolon shift-comma shift-dot shift-equal'.split()))
def key(c): return punct.get(c,'shift-'+c.lower() if c.isupper() else c)
chunks=[pairs[i:i+140] for i in range(0,len(pairs),140)]
def batch(args):
 i,items=args
 slug='compose-matrix-replay-'+str(i)
 perform(slug,[['start'],['wait','Doc 1 Pg 1'],['key','f3'],['wait','03/09/92'],['key','ret']])
 def tap(q,chord):
  keys=chord.split('-')
  for down,seq in [(True,keys),(False,keys[::-1])]:
   q.execute('input-send-event',{'events':[{'type':'key','data':{'down':down,'key':{'type':'qcode','data':k}}} for k in seq]})
 try:
  with qmp.QMP() as q:
   for pair in items:
    for k in ['ctrl-v',*map(key,pair),'shift-backslash','shift-backslash','shift-backslash']: tap(q,k); time.sleep(.004)
   q.wait_until(lambda t:'Key =' not in t,'compose completed')
  perform(slug,[['save',r'C:\OUT\PAIRS.WP'],['stop'],['export']])
 finally:
  perform(slug,[['stop']])
if __name__=='__main__':
 with ProcessPoolExecutor(3) as pool: list(pool.map(batch,enumerate(chunks)))
