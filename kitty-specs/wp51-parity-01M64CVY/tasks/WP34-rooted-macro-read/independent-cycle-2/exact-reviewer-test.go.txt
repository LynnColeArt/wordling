package storage_test

import (
 "bytes"
 "os"
 "path/filepath"
 "testing"
 "github.com/lynncoleart/wordling/internal/macro/wpm"
 "github.com/lynncoleart/wordling/internal/storage"
)

func TestReviewerMacroImagePointerMustNotChangeSnapshot(t *testing.T) {
 raw,err:=os.ReadFile("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM");if err!=nil{t.Fatal(err)}
 root:=t.TempDir();if err=os.WriteFile(filepath.Join(root,"macro"),raw,0600);err!=nil{t.Fatal(err)}
 d,err:=storage.OpenDirectory(root);if err!=nil{t.Fatal(err)};defer d.Close()
 m,err:=d.ReadMacro("macro");if err!=nil{t.Fatal(err)}
 id:=m.Identity()
 *m.Image()=wpm.Image{}
 if !bytes.Equal(m.Export(),raw)||m.Image().SHA256()!=id.SHA256 {t.Fatal("caller assignment through Image pointer changed acquired snapshot while stored Identity still describes original")}
}

func TestReviewerMacroImageReplacementMustNotRebindSnapshot(t *testing.T) {
 raw,err:=os.ReadFile("../../docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM");if err!=nil{t.Fatal(err)}
 root:=t.TempDir();if err=os.WriteFile(filepath.Join(root,"macro"),raw,0600);err!=nil{t.Fatal(err)}
 d,err:=storage.OpenDirectory(root);if err!=nil{t.Fatal(err)};defer d.Close()
 m,err:=d.ReadMacro("macro");if err!=nil{t.Fatal(err)}
 id:=m.Identity();other:=bytes.Clone(raw);other[72]='Z'
 changed,err:=wpm.Parse(other,wpm.DefaultLimits());if err!=nil{t.Fatal(err)}
 *m.Image()=*changed
 if !bytes.Equal(m.Export(),raw)||m.Image().SHA256()!=id.SHA256 {t.Fatal("caller replaced image through accessor; acquired source identity and native bytes diverged")}
}
