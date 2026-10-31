import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('measure',Path(__file__).with_name('measure.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class DistributionTests(unittest.TestCase):
 def test_nearest_rank_retains_outlier(self):
  q=m.quantiles([1]*99+[10000]);self.assertEqual(q['p99'],1);self.assertEqual(q['max'],10000);self.assertEqual(q['count'],100)
 def test_invalid_samples_refused(self):
  for x in [[],[-1],[float('nan')],[float('inf')]]:
   with self.assertRaises(ValueError):m.quantiles(x)
 def test_refusals_not_mixed_into_success(self):
  rows=m.summarize({'phases':[{'name':'parse','warmup':[{}],'samples':[{'ns':1,'alloc_bytes':0,'allocs':0},{'ns':100,'alloc_bytes':5,'allocs':1,'error':'limit'}]}]})
  self.assertEqual([(r['status'],r['ns']['count']) for r in rows],[('accepted',1),('refused',1)])
 def test_incomparable_boundaries_and_refusals_not_ratios(self):
  row={'name':'parse','unit':'ns','status':'accepted','boundary':'memory-parse','ns':{'p50':1}}
  self.assertEqual(m.ratio(row,dict(row,ns={'p50':2})),2)
  for field,value in [('name','view'),('unit','ms'),('status','refused'),('boundary','read-parse')]:
   with self.assertRaises(ValueError):m.ratio(row,dict(row,**{field:value}))
  with self.assertRaises(ValueError):m.ratio(dict(row,status='refused'),dict(row,status='refused'))

if __name__=='__main__':unittest.main(verbosity=2)
