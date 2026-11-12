from pathlib import Path
import json,subprocess,sys,copy
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-u');sys.path.insert(0,str(R/'scripts/reference'));import text_flow_contract as t
O=Path('/tmp/wordling-wp49-independent');base=json.loads((O/'actual-report.json').read_text());rows=[]
def units(v):v['data']['runs'][0]['states'][0]['after']['selected_font_fields'][0]['units']='DPI'
def repeat(v):v['data']['runs'][0]['repetition']=2
def reader(v):v['data']['actual_reader']['binary_sha256']='0'*64
def stream(v):
 p=v['data']['runs'][0]['states'][0]['full_PRN'];p['full_hex']='41';p['bytes']=1;p['sha256']=t.sha(b'A')
for name,mutate in [('literal-units',units),('same-bytes-wrong-repetition',repeat),('reader-binary-forgery',reader),('whole-PRN-forgery',stream)]:
 v=copy.deepcopy(base);mutate(v);v['data_sha256']=t.sha(t.canonical(v['data']));path=O/(name+'.json');path.write_text(json.dumps(v));p=subprocess.run([sys.executable,str(R/'scripts/reference/text_flow_contract.py'),'result',str(path)],cwd=R,capture_output=True,text=True);(O/(name+'.stderr')).write_text(p.stderr);assert p.returncode==1 and 'SemanticMismatch'in p.stderr;rows.append({'mutation':name,'actual_CLI_exit':p.returncode,'all_data_hashes_recomputed':True,'reason':'SemanticMismatch after actual full sources/reader recomputation'});path.unlink()
(O/'cli-negatives.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS4 rehashed authentic public CLI negatives: unit/repetition/reader/fullPRN binding')
