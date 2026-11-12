import json,subprocess
from pathlib import Path
r=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g');o=Path(__file__).resolve().parent
s=(r/'internal/editor/editing_test.go').read_text().replace('"bytes"','"bytes"\n"reflect"')
s+='''
func TestIndependentBlockQuestionForkAndRefusal(t *testing.T) {
 for _, span := range [][2]int{{1,2},{4,5},{1,5}} {
  f:=setup(t); s:=key(t,load(t,f),editor.Reveal)
  for j:=0;j<span[0];j++ {s=key(t,s,editor.Right)}
  s=key(t,s,editor.Block);for j:=span[0];j<span[1];j++ {s=key(t,s,editor.Right)}
  selected:=s.Snapshot(); rev:=s.Document().Revision(); hr:=s.History().Revision()
  q:=key(t,s,editor.Backspace)
  for _, cmd:=range []editor.Command{editor.Delete,editor.Backspace,editor.Text,editor.Save,editor.Restore} {
   got,intent,err:=q.Reduce(editor.Event{Command:cmd,Text:"Q"})
   if err==nil||intent!=nil||!reflect.DeepEqual(got.Snapshot(),q.Snapshot())||got.History().Revision()!=hr||got.Document().Revision()!=rev {t.Fatal("pending invalid command changed question")}
  }
  for _,cmd:=range []editor.Command{editor.No,editor.F1,editor.Escape} {
   d:=key(t,q,cmd);raw,_:=d.Document().Export()
   if !bytes.Equal(raw,f.raw)||d.Document().Revision()!=rev||d.Snapshot().HistoryCount!=selected.HistoryCount||d.Snapshot().HistoryCountKnown!=selected.HistoryCountKnown||d.Snapshot().HistoryQualified!=selected.HistoryQualified||d.Snapshot().Gap!=span[1]||!d.Snapshot().Selection||d.Snapshot().Dirty {t.Fatal("decline changed native/history/selected gap")}
   d=key(t,d,editor.F1);if d.Snapshot().Selection||d.Snapshot().Dirty||d.Document().Revision()!=rev||d.Snapshot().HistoryCount!=selected.HistoryCount||d.Snapshot().HistoryCountKnown!=selected.HistoryCountKnown||d.Snapshot().HistoryQualified!=selected.HistoryQualified {t.Fatal("cleanup changed native/history")}
  }
  // A whole getter-wrapper replacement cannot retarget the outstanding question.
  *q.Document()=document.Document{}
  if span[0]==4 {expectRefusal(t,q,editor.Event{Command:editor.Yes});continue}
  yes:=key(t,q,editor.Yes)
  if yes.Snapshot().Selection||!yes.Snapshot().Dirty||yes.Document().Revision()==rev||yes.Snapshot().Revision!=selected.Revision+1 {t.Fatal("Yes failed revision/dirty/block contract")}
  if s.Document().Revision()!=rev||!reflect.DeepEqual(s.Snapshot(),selected)||q.Snapshot().Mode!=editor.DeleteQuestion {t.Fatal("fork mutated earlier session")}
 }
}
'''
(o/'adversarial_test.go.txt').write_text(s);(o/'adversarial-overlay.json').write_text(json.dumps({'Replace':{str(r/'internal/editor/editing_test.go'):str(o/'adversarial_test.go.txt')}}))
p=subprocess.run(['go','test','-overlay',str(o/'adversarial-overlay.json'),'./internal/editor','-run','^TestIndependentBlockQuestionForkAndRefusal$','-count=1','-v'],cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'adversarial.txt').write_bytes(p.stdout);raise SystemExit(p.returncode)
