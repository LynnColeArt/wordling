package storage_test
import("bytes";"os";"path/filepath";"sync";"testing";"github.com/lynncoleart/wordling/internal/macro/wpm";"github.com/lynncoleart/wordling/internal/storage")
func TestReviewerConcurrentWrapperReplacementIsolation(t *testing.T){
 raw,e:=os.ReadFile("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM");if e!=nil{t.Fatal(e)};root:=t.TempDir();if e=os.WriteFile(filepath.Join(root,"macro"),raw,0600);e!=nil{t.Fatal(e)};d,e:=storage.OpenDirectory(root);if e!=nil{t.Fatal(e)};defer d.Close();m,e:=d.ReadMacro("macro");if e!=nil{t.Fatal(e)};id,name,dir:=m.Identity(),m.Name(),m.DirectoryID()
 var wg sync.WaitGroup;for n:=0;n<8;n++{wg.Add(1);go func(){defer wg.Done();for j:=0;j<100;j++{a,b:=m.Image(),m.Image();*a=wpm.Image{};out:=b.Export();out[0]=0;words:=b.BodyWords();words[0].Value=0;description:=b.Description();description[0]=0;if !bytes.Equal(m.Export(),raw)||!bytes.Equal(b.Export(),raw)||m.Image().SHA256()!=id.SHA256||m.Identity()!=id||m.Name()!=name||m.DirectoryID()!=dir{t.Error("owned snapshot/another wrapper changed")};*b=wpm.Image{}}}()};wg.Wait()
}
