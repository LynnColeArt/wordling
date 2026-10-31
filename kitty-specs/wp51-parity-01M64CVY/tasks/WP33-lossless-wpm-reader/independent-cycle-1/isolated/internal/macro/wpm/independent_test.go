package wpm_test
import("bytes";"encoding/binary";"errors";"os";"testing";"github.com/lynncoleart/wordling/internal/macro/wpm")
func seed(t *testing.T) []byte {t.Helper();b,e:=os.ReadFile("/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-n/docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM");if e!=nil{t.Fatal(e)};return b}
func accepted(t *testing.T,b []byte)*wpm.Image {t.Helper();i,e:=wpm.Parse(b,wpm.DefaultLimits());if e!=nil{t.Fatal(e)};if !bytes.Equal(i.Export(),b){t.Fatal("changed")};return i}
func TestIndependentOpaqueIndexRelations(t *testing.T){
 b:=seed(t);b=append(append(append([]byte{},b[:70]...),0x91,0x92),b[70:]...);binary.LittleEndian.PutUint32(b[4:8],72)
 for n,at:=range []int{36,46}{binary.LittleEndian.PutUint16(b[at:at+2],uint16(n+2));binary.LittleEndian.PutUint32(b[at+2:at+6],1);binary.LittleEndian.PutUint32(b[at+6:at+10],uint32(70+n))}
 i:=accepted(t,b);if len(i.Inspect().Findings)!=2{t.Fatal(i.Inspect())};for _,f:=range i.Inspect().Findings{if !f.ExecutionBlocked{t.Fatal(f)}}
 binary.LittleEndian.PutUint32(b[52:56],70);i,e:=wpm.Parse(b,wpm.DefaultLimits());var f *wpm.Failure;if i!=nil||!errors.As(e,&f)||f.Code!="UnsupportedStructure"{t.Fatal(i,e)}
 b=seed(t);binary.LittleEndian.PutUint16(b[46:48],2);binary.LittleEndian.PutUint32(b[52:56],^uint32(0));i=accepted(t,b);if len(i.Inspect().Findings)!=1||i.Inspect().Findings[0].Code!="OpaquePrefixIndex"{t.Fatal(i.Inspect())}
}
func TestIndependentDescriptionAndTerminal(t *testing.T){
 b:=seed(t);binary.LittleEndian.PutUint32(b[32:36],57);binary.LittleEndian.PutUint32(b[28:32],13);i:=accepted(t,b);if i.Inspect().Description!=(wpm.Span{Offset:57,Length:13})||len(i.Inspect().Findings)!=1{t.Fatal(i.Inspect())}
 b=seed(t);b[58]=0;i=accepted(t,b);if len(i.Inspect().Findings)!=1{t.Fatal(i.Inspect())}
 b=seed(t);b[70]=0;b[71]=0;i=accepted(t,b);if len(i.BodyWords())!=1||i.Inspect().Body.Length!=2||i.Inspect().Suffix.Length!=8{t.Fatal(i.Inspect())}
 b=seed(t);i,e:=wpm.Parse(b,wpm.Limits{InputBytes:80,DescriptionBytes:14,Words:5});if e!=nil||i==nil{t.Fatal(e)}
}
func TestIndependentFindingBoundAndSourceCopies(t *testing.T){
 b:=seed(t);b=append(bytes.Clone(b[:70]),make([]byte,2*wpm.MaxWords)...);for n:=70;n<len(b)-2;n+=2{b[n]=0xfd;b[n+1]=0xfc};i:=accepted(t,b);f:=i.Inspect().Findings;if len(f)!=1||f[0].Code!="UnqualifiedMacro"{t.Fatal(f)};f[0].ExecutionBlocked=false;if !i.Inspect().Findings[0].ExecutionBlocked{t.Fatal("alias")};w:=i.BodyWords();if len(w)!=wpm.MaxWords||w[len(w)-1].Kind!=wpm.Terminal{t.Fatal("word bound")}
}
