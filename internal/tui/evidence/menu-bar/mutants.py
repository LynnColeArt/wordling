"""Finite semantic faults in ACTUAL owned source, restored in finally. No overlays."""
from pathlib import Path
import subprocess,json,time
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
cases=[
 ('wrong-cell','menu_bar.go','File Edit Search','Xile Edit Search'),
 ('wrong-role','menu_bar.go','[22;34;47m','[22;32;47m'),
 ('wrong-mnemonic','menu_bar.go','case 5, 10, 17, 24, 29, 36, 40, 49:','case 5, 10, 17, 24, 29, 35, 40, 49:'),
 ('no-reset','menu_bar.go','out.WriteString("\\x1b[0m")','out.WriteString("")'),
 ('wrong-row','model.go','lines[0] = renderMenuBar()','lines[1] = renderMenuBar()'),
 ('insert-row','model.go','lines[0] = renderMenuBar()','lines = append([]string{renderMenuBar()}, lines...)'),
 ('delete-integration','model.go','if m.menuState().Visible {','if false {'),
 ('alias-primary','menu_bar.go',"k.Code == '='", "(k.Code == '=' || k.BaseCode == '=')"),
 ('altstrip','menu_bar.go','k.Mod == tea.ModAlt','(k.Mod == tea.ModAlt || k.Mod == 0)'),
 ('capslock','menu_bar.go','k.Mod == tea.ModAlt','k.Mod & ^tea.ModCapsLock == tea.ModAlt'),
 ('repeat','menu_bar.go','!k.IsRepeat','true'),
 ('associated-text','menu_bar.go','(k.Text == "" || k.Text == "=")','true'),
 ('release','model.go','if event.Kind != input.Press {','if event.Kind != input.Press && event.Kind != input.Release {'),
 ('fallthrough','menu_bar.go','if state.Visible {','if state.Visible && false {'),
 ('pristine','menu_bar.go','d == nil || m.session.Source() != nil || d.TokenCount() != 0 || s.GenesisRevision == (document.Revision{}) || s.GenesisRevision != s.NativeRevision || s.Revision != 1 || s.Gap != 0 || s.Provenance != 0','d == nil'),
 ('current-token','menu_bar.go','m.runtime.uiAuthority == m.uiAuthority','true'),
 ('lifetime','menu_bar.go','!m.runtime.stopping','true'),
 ('pending','menu_bar.go','if len(m.unsettled) != 0 || m.firstPending != nil {','if false {'),
 ('macro-worker','menu_bar.go','|| m.macroStatus.WorkerPending',''),
 ('frozen','menu_bar.go','|| m.macroFrozen != nil',''),
 ('hide-restore','menu_bar.go','if menuKey(k) {\n\t\t\tm.menu = menuDisplay{}','if menuKey(k) {\n\t\t\tm.menu = menuDisplay{shown: true}'),
 ('resize','model.go','m.menu = menuDisplay{}\n\t\tm.width','m.width'),
 ('dimension','menu_bar.go','m.width != 80 || m.height != 25','false'),
 ('notice-hide','menu_bar.go','|| m.notice != "" || m.reconcile != ""',''),
 ('admin-env','model.go','case tea.EnvMsg, tea.ColorProfileMsg:','case tea.ColorProfileMsg:'),
 ('admin-color','model.go','case tea.EnvMsg, tea.ColorProfileMsg:','case tea.EnvMsg:'),
]
results=[]
for name,file,old,new in cases:
 path=ROOT/'internal/tui'/file;original=path.read_text();assert old in original,(name,old)
 started=time.monotonic()
 try:
  path.write_text(original.replace(old,new,1))
  companion=ROOT/'internal/tui/model.go';saved=None
  if name=='no-reset':
   saved=companion.read_text();companion.write_text(saved.replace('if strings.Contains(s, \"\\x1b[\") {','if false {',1))
  r=subprocess.run(['go','test','-count=1','-run','^TestMenu','./internal/tui'],cwd=ROOT,capture_output=True,timeout=300)
  (HERE/(name+'.mutant.stdout')).write_bytes(r.stdout);(HERE/(name+'.mutant.stderr')).write_bytes(r.stderr)
  semantic=r.returncode!=0 and b'build failed' not in r.stdout and b'build failed' not in r.stderr
  results.append(dict(name=name,file=file,old=old,new=new,exit=r.returncode,semantic_kill=semantic,elapsed=time.monotonic()-started))
 finally:
  path.write_text(original)
  if saved is not None:companion.write_text(saved)
 (HERE/'mutants.json').write_text(json.dumps(results,indent=2)+'\n');print(name,results[-1]['semantic_kill'],flush=True)
