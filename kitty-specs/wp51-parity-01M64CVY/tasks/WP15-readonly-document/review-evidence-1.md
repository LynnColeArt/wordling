# WP15 independent review — 2026-10-30

Reviewed implementation: `44f1a6d`, scoped against approved dependency `e7de080`.
Reviewer: independent Codex agent with resolver-loaded reviewer-renata and review
charter context. The runtime prompt's displayed implementer profile is authored
WP metadata; this review uses the separately resolved reviewer role. Full runtime
prompt2906d25205b64b979fe001f5ed0c6d33, WP15 T043–T045, spec/plan/domain model,
compatibility/roadmap, WP02/WP04/WP10/WP12 outputs and relevant prior review
findings were considered. Code Review Checklist has no authored charter section.
Assessment: approve bounded read-only component; no blocking findings.
The canonical review_result event, not this prose, records the verdict.

## Contract assessment

T043: `document.Parse` calls actual approved `wp51.Parse`; its native failures
retain typed categories, and no private native validator or acceptance fallback
is introduced. After validation, a separate compact token-gap index uses the
published fixed widths and variable L+4 spans over the immutable image. This
post-validation indexing is not opaque-payload interpretation or another native
validity decision. Tests cover all16 fixed widths and maximum variable lengths;
future framing changes must keep this bounded consumer in sync. Only printable
ASCII20–7E and exact C3/0C/C3, C4/0C/C4 are interpreted. All other framed identities,
including C0 and arbitrary attributes, remain opaque with exact spans/raw bytes.
The constructor does not infer pair validity, edit safety, layout or character
conversion. No approved dependency file, module pin or original fixture changed.

T044: ORIGIN is independently pinned at334 bytes and SHA256
c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d.
Its six complete tokens yield exact absolute gaps324,325,328,329,330,333,334.
Both projections retain the same token/span/gap identity. Bold's normal text is
empty while its typed element remains; Reveal labels retain case. Cursor values
are copied and no operation can mutate its document. Adjacent movement across
opaque data refuses with token/span and unchanged cursor; Present refuses the
entire requested window, while independent supported windows still work. Explicit
CursorAt coordinates are not original Home/GoTo implementations. No code derives
semantic positions from terminal cells, inches or bytes inside a framed token.

T045: external-package tests execute production Parse/Export/Token/Cursor/Present.
Original corpus hashes, all truncations, malformed framing versus opaque valid
semantics, zero/nil handles, extreme integer arguments, exact/over token/window
ceilings, the exact16MiB native input, and copied buffers are covered. Policies
are explicit: WP02 input16MiB, token count1,048,576, index at most4,194,308 bytes,
presentation4096 tokens and bounded window/body copies. Recorded fuzz60s and120s
runs pass at6,185,417 and11,951,069 executions with two workers; their actual
source hash matches current production and host.json. Four selected recorded
compiling mutations were killed by assertions and source restored. This review
inspected those logs rather than claiming a repeated independent180s fuzz run.
Measured allocations/RSS/timing remain harness observations, not product budgets.

## Independently executed checks

- Runtime-directed git log/diff/stat inspected; scoped implementation changes
  only internal/document/. Earlier internal/wp51 additions in mission-base diff
  are the unchanged approved e7de080 dependency, not new WP15 edits.
- `python3 scripts/review_checks.py --junitxml /tmp/wp15-independent-review.xml`:
  seven real checks PASS, zero failures/skips, including Go build/test/vet.
- `git diff --check e7de080..44f1a6d` PASS; `gofmt -l internal/document` empty.
- Current document.go/module/sum SHA256 values equal recorded host.json fields.
  Both committed fuzz logs contain genuine PASS/exit0 and matching final counts.
- Supplemental virtual Go overlay below: `go test -overlay
  /tmp/wp15-independent-overlay.json -race ./internal/document -run
  '^TestIndependent' -count=1 -v` PASS. Exercises externally observable arbitrary
  opaque variable lengths/leading types, whole-span boundaries and exact refusal
  identities, empty native bodies and concurrent copy mutation/view access.
- `GOARCH=386 go test ./internal/document -count=1` PASS; this is checked integer
  handling, not an expanded platform support claim.
- Checked source before/after: a9b13f4ff5d759059ccebd6b8a5d6066c723ea17136c0d1261dc3290dd7d3aff.
  No implementation or fixture edits were made; generated untracked .spec-kitty
  state was not staged or altered.

## Required anti-pattern checklist

1. Dead code: N/A for user-facing reachability in this explicitly bounded library
   package, following approved WP02's same scope disposition. The actual native
   reader is called from production; WP17/WP18 are authorized future consumers
   of this component. No fabricated CLI/caller outside WP15 ownership, or claim
   of an existing end-user editor, is appropriate. Those integration WPs must
   demonstrate live use of these APIs before their own approval.
2. Synthetic-fixture assertions: PASS. External tests invoke actual production
   behavior; original bytes/hashes are pinned, synthetic malformed/opaque cases
   explicitly supplement rather than replace original observations.
3. Silent empty return: PASS. Invalid or unsupported behavior returns typed
   refusal. TokenCount zero for an unconstructed handle is inspection only;
   actual export/token/cursor operations refuse. Empty normal Bold display
   preserves its typed element/span; empty valid body/window is explicit.
4. FR coverage: PASS for scoped FR-002/004/005, NFR-001/003 and C-001 obligations:
   exact native preservation, shared read-only view/cursor behavior, typed
   unsupported handling and measured bounds are real assertions. Full original
   command/editing and all parent FR/FC obligations remain open.
5. Frozen surface: PASS. Original fixtures, native reader, go.mod/go.sum and
   dependency planning artifacts unchanged in the scoped WP15 diff.
6. Locked decisions: PASS. Original format and bytes retained; no writer,
   deletion/Undelete/typeover/selection, C0 mapping, layout, Bubble Tea or PDF work.
7. Shared-file ownership: PASS. Only internal/document/ production/evidence
   surfaces are owned/modified by WP15 in its independent code lane. Root owns
   shared mission bookkeeping; this reviewer only adds this authorized record.
8. Production fragility: PASS. Internal private indexes come only from checked
   immutable framing; bounded arithmetic and typed refusal paths, no transient
   IO race or uncontrolled user-input panic identified.

Approval establishes a reusable read-only component, not original-session
movement equivalence, native editing/writing, terminal qualification, complete
Reveal Codes functionality or M1 acceptance.

## Reproduce independent external-API overlay

Extract the following Go block to /tmp/wp15-independent-adversarial_test.go.
Map the virtual absolute lane path internal/document/independent_review_test.go
into that file with Go's -overlay JSON Replace object. This adds review tests
without touching tracked implementation files.

```go
package document_test

import (
 "bytes"
 "encoding/binary"
 "errors"
 "os"
 "sync"
 "testing"

 "github.com/lynncoleart/wordling/internal/document"
 "github.com/lynncoleart/wordling/internal/wp51"
)

func TestIndependentOpaqueVariableGapBoundaries(t *testing.T) {
 original,err:=os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5");if err!=nil {t.Fatal(err)}
 base:=int(binary.LittleEndian.Uint32(original[4:8]))
 for _,lead:=range []byte{0xd0,0xde,0xff} {
  for _,length:=range []int{4,5,31,65535} {
   raw:=make([]byte,length+4);raw[0]=lead;raw[1]=0xff;binary.LittleEndian.PutUint16(raw[2:4],uint16(length));binary.LittleEndian.PutUint16(raw[length:length+2],uint16(length));raw[length+2]=0xff;raw[length+3]=lead
   if length>=8 {copy(raw[4:],[]byte{0xc3,12,0xc3,0})}
   input:=append(bytes.Clone(original[:base]),'A');input=append(input,raw...);input=append(input,'B')
   d,e:=document.Parse(input);if e!=nil||d.TokenCount()!=3 {t.Fatalf("%x/%d: %v",lead,length,e)}
   tok,e:=d.Token(1);if e!=nil||tok.Kind!=document.Opaque||tok.Span.Offset!=base+1||tok.Span.Length!=len(raw)||!bytes.Equal(tok.Raw,raw) {t.Fatal("opaque payload was split/interpreted",e)}
   before,_:=d.CursorAt(1);after,_:=d.CursorAt(2)
   for _,pair:=range []struct{c document.Cursor;dir int}{{before,1},{after,-1}} {
    next,e:=pair.c.Move(pair.dir);var f *document.Failure
    if !errors.As(e,&f)||f.Category!=document.UnsupportedToken||f.TokenIndex!=1||f.Span!=tok.Span||next!=pair.c {t.Fatal("opaque crossing/refusal identity",e)}
   }
   for _,reveal:=range []bool{false,true} {
    p,e:=before.WithReveal(reveal).Present(0,3);var f *document.Failure
    if !errors.As(e,&f)||f.Category!=document.UnsupportedToken||len(p.Elements)!=0 {t.Fatal("partial unsupported presentation",e)}
    p,e=after.WithReveal(reveal).Present(2,1);if e!=nil||len(p.Elements)!=1||p.Elements[0].Text!="B"||p.CursorGap!=2 {t.Fatal("opaque refusal contaminated later supported window",e)}
   }
   for gap,want:=range []int{base,base+1,base+1+len(raw),len(input)} {c,e:=d.CursorAt(gap);off,oe:=c.Offset();if e!=nil||oe!=nil||off!=want {t.Fatal("gap inside opaque token")}}
   got,e:=d.Export();if e!=nil||!bytes.Equal(got,input) {t.Fatal("native bytes changed")}
  }
 }
}

func TestIndependentEmptyAndConcurrentViews(t *testing.T) {
 input,err:=os.ReadFile("../../docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5");if err!=nil {t.Fatal(err)}
 base:=int(binary.LittleEndian.Uint32(input[4:8]))
 empty:=bytes.Clone(input[:base]);d,e:=document.Parse(empty);if e!=nil||d.TokenCount()!=0 {t.Fatal("empty native body",e)}
 c,e:=d.CursorAt(0);p,pe:=c.Present(0,0);off,oe:=c.Offset();if e!=nil||pe!=nil||oe!=nil||off!=base||len(p.Elements)!=0 {t.Fatal("empty boundary")}
 for _,dir:=range []int{-1,1} {next,e:=c.Move(dir);if e==nil||next!=c {t.Fatal("empty movement accepted")}}
 var nilDoc *document.Document
 if nilDoc.TokenCount()!=0 {t.Fatal("nil token count")};if _,e=nilDoc.Token(0);e==nil {t.Fatal("nil inspection accepted")}
 d,e=document.Parse(input);if e!=nil {t.Fatal(e)}
 var wg sync.WaitGroup
 for n:=0;n<8;n++ {wg.Add(1);go func(){defer wg.Done();for i:=0;i<32;i++ {
  c,e:=d.CursorAt(i%7);if e!=nil {t.Error(e);return}
  for _,r:=range []bool{false,true} {p,e:=c.WithReveal(r).Present(0,6);if e!=nil||p.CursorGap!=i%7||len(p.Elements)!=6 {t.Error("concurrent view drift");return};p.Elements[0].Text="mutated";p.Elements[0].Span=wp51.Span{}}
  tok,e:=d.Token(1);if e!=nil||!bytes.Equal(tok.Raw,[]byte{0xc3,12,0xc3}) {t.Error("token isolation");return};tok.Raw[0]=0
  output,e:=d.Export();if e!=nil||!bytes.Equal(output,input) {t.Error("concurrent source drift");return};output[0]=0
 }}()}
 wg.Wait()
 got,e:=d.Export();if e!=nil||!bytes.Equal(got,input) {t.Fatal("shared document changed")}
}

```
