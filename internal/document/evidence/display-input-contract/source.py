"""Closed immutable authority, using Git and exact working bytes; no resource scans."""
from pathlib import Path
import importlib.util,json,sys
from boundaries import read,parse,sha,require,process
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Sources:
 def __init__(self):
  self.rows=parse(read(HERE/'authority.json',1<<20))['sources'];require(len(self.rows)<=600,'RosterLimit',len(self.rows));self.pins={}
  request=''.join(r['commit']+':'+r['path']+'\n'for r in self.rows).encode();raw,_=process(['git','cat-file','--batch'],ROOT,input_bytes=request);pos=0;total=0
  for r in self.rows:
   end=raw.find(b'\n',pos);require(end>=pos,'GitFrame',r['path']);head=raw[pos:end].split();require(len(head)==3 and head[1]==b'blob','GitFrame',r['path']);n=int(head[2]);pos=end+1;b=raw[pos:pos+n];pos+=n;require(raw[pos:pos+1]==b'\n','GitFrame',r['path']);pos+=1;total+=n
   require(n==r['bytes']and head[0].decode()==r['git_blob']and sha(b)==r['sha256'],'SourceGitMismatch',r['path']);require(read(ROOT/r['path'],16<<20)==b,'SourceWorkingMismatch',r['path']);self.pins[r['path']]=r
  require(pos==len(raw)and total<=64<<20,'RosterBytes',total);self.total=total
 def data(self,path):
  require(path in self.pins,'SourceNotOwned',path);r=self.pins[path];b=read(ROOT/path,16<<20);require(sha(b)==r['sha256'],'SourceChanged',path);return b
 def json(self,path):return parse(self.data(path))
 def load_extractors(self):
  # Bind every transitively imported project module BEFORE any import. No VM function called.
  helper_names=['text_layout','document','guest','qmp','smoke','extended','advanced','history_loops','iteration_nesting','value_secondary']
  for name in helper_names:self.data('scripts/reference/'+name+'.py')
  self.data('docs/research/continuation/text-layout/analyze.py');self.data('scripts/reference/text_flow_contract.py')
  sys.path.insert(0,str(ROOT/'scripts/reference'))
  import text_layout
  def module(name,path):
   spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
  return text_layout,module('wp56_approved14_analysis','docs/research/continuation/text-layout/analyze.py'),module('wp56_approved49_extraction','scripts/reference/text_flow_contract.py')
