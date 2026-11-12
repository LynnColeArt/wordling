"""Real owned-source mutants, run public CLI tests, restore exact source in finally.
No mutation to original captures/approved helper/core/Go or any guest operation.
"""
from pathlib import Path
import ast,hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent;SOURCE=HERE/'field_contract.py';CHECKS=HERE/'checks';CHECKS.mkdir(exist_ok=True)
def main():
 original=SOURCE.read_bytes();text=original.decode();cases=[
 ('nonempty-strip',[("return line.ljust(67)+CUE if kind!='fresh-whole-field-typed'else line","return line.ljust(67)+CUE if literal==''else line")],'test_cli.CLI.test_actual_paired_three_contexts'),
 ('accept-optional-cue',[("line=expected_line(expected['kind'],expected['literal']);","line=rows[24];")],'test_cli.PublicContract.test_rehashed_wrong_cue_framed_semantics'),
 ('ignore-state',[("packet['kind']==expected['kind']and packet['literal']==expected['literal']","True")],'test_cli.PublicContract.test_state_ignored_mutant_witness'),
 ('ignore-cursor',[("type(c.get(k))is int and c[k]==value","True"),("type(c.get('crtc'))is dict and set(c['crtc'])==set(want)and all(type(c['crtc'][k])is int and c['crtc'][k]==v for k,v in want.items())","True")],'test_cli.PublicContract.test_cursor_ignored_mutant_witness'),
 ('accept-rehashed-original-substitution',[("all(packet[k]==expected[k]for k in ['text','vga_hex','cursor'])","True")],'test_cli.PublicContract.test_source_rehashed_substitution_mutant_witness')]
 rows=[]
 try:
  for name,changes,test in cases:
   mutant=text
   for before,after in changes:
    if mutant.count(before)!=1:raise AssertionError('unique mutant seam '+name)
    mutant=mutant.replace(before,after)
   mutant+='\n# Deliberate controlled mutant: '+name+'\n';ast.parse(mutant);SOURCE.write_text(mutant)
   start=time.monotonic();p=subprocess.run([sys.executable,'-B','-m','unittest',test],cwd=HERE,capture_output=True,timeout=30);(CHECKS/(name+'.stdout.log')).write_bytes(p.stdout);(CHECKS/(name+'.stderr.log')).write_bytes(p.stderr)
   if p.returncode==0:raise AssertionError('SURVIVED '+name)
   if b'FAIL:'not in p.stderr or b'FAILED (failures='not in p.stderr:raise AssertionError('not semantic test failure: '+name)
   rows.append(dict(name=name,actual_source_sha256=hashlib.sha256(mutant.encode()).hexdigest(),test=test,returncode=p.returncode,compiled_ast=True,killed_by_public_CLI_assertion=True,seconds=time.monotonic()-start))
   SOURCE.write_bytes(original)
 finally:SOURCE.write_bytes(original)
 if SOURCE.read_bytes()!=original:raise AssertionError('source restore')
 (CHECKS/'mutants.json').write_text(json.dumps(dict(original_source_sha256=hashlib.sha256(original).hexdigest(),mutants=rows,source_restored_exact=True,original_guest_or_native_mutations=0),indent=2)+'\n');print('Killed',len(rows),'real executable mutants; exact source restored')
if __name__=='__main__':main()
