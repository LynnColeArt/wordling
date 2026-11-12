# WP02 independent code review — 2026-10-30

Assessment: approve bounded native reader commit `e7de080452c2906e99c8ace0048c415d842f2f89`. The authoritative verdict is the Spec Kitty review_result event, not this prose. Reviewer is separate from the implementer and loaded reviewer-renata and review action governance.

Code and commands were inspected/executed in `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-a`. Exact baseline is `9585c4d0279627b91ef6e266def92181f68fef3a` / `kitty/mission-wp51-parity-01M64CVY`; only the 13 `internal/wp51/` files differ. This review artifact is placed on the primary planning branch; no implementation edits made.

## Contract assessment

T004–T006 meet approved WP01's bounded library contract. The 16 MiB limit precedes owned copying. Header/prefix widths are checked before reads; u32 pointer/length comparisons use widened arithmetic, and conversion to int occurs only inside the bounded image. Index count/size and complete-block spans are checked, traversal counts and visited offsets bound cycles, and early type0 terminates before untrusted unused entries/next pointers are interpreted. Metadata retains native traversal order; only a temporary span view is sorted. Nonempty overlaps are explicitly refused while zero-length opaque spans remain permitted.

Fixed C0–CF widths and delimiter checks agree with SDK/WP01; D0–FF full spans use L+4, including the observed L=4 empty functions, and mirrored length/subfunction/function fields must match. Single-byte and reserved/unknown framed functions retain their bytes. All opaque packet/function payloads and nested text remain expressly unvalidated; parse success grants no semantic edit permission. Macro/file-version/encryption/graphics/unsupported overlaps are explicit typed refusals, not silent conversion.

Exact whole-image export, copied inspection slices and copied span bytes have no mutable alias back into the owned image. Source image copying occurs after successful validation, with the documented precondition that callers do not mutate their input during Parse. No filesystem replacement, terminal, semantic writer, extra dependency or CLI was introduced. WP03 remains the authorized real storage consumer.

## Independently executed verification

- `python3 scripts/review_checks.py --junitxml=/tmp/wordling-wp02-review-junit.xml`: seven real checks pass, **zero skips**, including actual Go build/test/vet and original fixture/run-provenance checks in Go tests.
- `gofmt -l internal/wp51/*.go`: empty; `git diff --check 9585c4d..e7de080`: pass.
- `go test -race ./internal/wp51 -count=1`: pass.
- `GOARCH=386 go test ./internal/wp51 -count=1`: pass, validating bounded integer handling on Linux 32-bit in addition to the declared amd64 evidence host. This is test evidence, not an added product-platform compatibility claim.
- Temporary overlay adversarial tests below pass both normally and under `-race`: nonmonotonic block traversal preserves native order, concurrent exported/inspected/span copies stay isolated, empty opaque ranges may lie within indexes, malicious ignored pointers/unused bytes remain preserved, and high-bit u32 pointers/lengths refuse without input mutation.
- Reviewed complete committed malformed/resource tests, original fixture provenance/identity assertions and fuzz target. Source SHA-256 `e13c93687e6119bff44f8405616455849cb728f3b4a1b3949d987dbe2c30b1d6` matches `host.json` and final mutation restoration. Recorded 60s/600s commands, two-worker configuration, PASS/exit-zero logs and final 7,000,569 / 57,160,290 counts agree with evidence README. The long fuzz run is recorded implementer evidence, not rerun or misrepresented as a new independent 600s execution. Actual parser resource measurements and their harness/RSS limitations are explicitly reported.

## Generated anti-pattern checklist disposition

1. Dead code: **N/A for user-facing reachability in this bounded foundation package.** WP02 explicitly delivers a library and excludes a CLI/semantic writer; WP03 is its planned production consumer. API behavior is directly exercised by external-package tests. Do not claim an end-user workflow exists or manufacture a caller outside authorized scope.
2. Synthetic-fixture assertion: **PASS**. Tests invoke actual Parse/Export/Inspect/Bytes; original corpus bytes and run evidence are independently pinned. Supplemental synthetic cases are labelled.
3. Silent empty return: **PASS**. Parse failures return typed reasons/no accepted image; invalid requested spans use explicit false; helper success returns have documented semantics.
4. Requirement coverage: **PASS for this package's scoped obligations**. FR-002/NFR-001/003/C-001/002 have real byte-preservation, unsupported/malformed, isolation and resource tests. Full FR-002 editing/new-document writing remains pending beyond this WP.
5. Frozen surface: **PASS**. No original fixtures, manual/source evidence or other frozen surfaces changed in the scoped diff.
6. Locked decisions: **PASS**. Native formats unchanged, exact no-edit export, opaque data retained, no semantic mutation or PDF scope added.
7. Shared ownership: **PASS**. Lane-a WP02 alone owns `internal/wp51/`; no shared production surface changed.
8. Production fragility: **PASS**. Checked bounded reads and explicit typed refusals; no uncontrolled panic, infrastructure race handler or silent failure path identified.

No blocking findings. This approval cannot establish semantic editing, general companion support, safe filesystem saves, original print/layout equivalence or full M1 parity. Future storage/API consumers must honor the constructor and unsupported-structure contracts.

## Reproducible reviewer overlay probes

These are supplemental review probes, not production edits. To rerun, extract the following Go block into `/tmp/wordling-wp02-review-adversarial_test.go`, map it as an added Go test with `-overlay`, and run the commands after it. The virtual target does not alter a checked-in file.

<!-- WP02_REVIEW_GO_BEGIN -->
```go
package wp51_test

import (
 "bytes"
 "encoding/binary"
 "errors"
 "sync"
 "testing"
 "github.com/lynncoleart/wordling/internal/wp51"
)

func reviewerDoc(prefix int, body []byte) []byte {
 b:=make([]byte,prefix+len(body));copy(b,[]byte{255,'W','P','C'});binary.LittleEndian.PutUint32(b[4:],uint32(prefix));copy(b[8:],[]byte{1,10,0,1});binary.LittleEndian.PutUint16(b[16:],0xfffb);binary.LittleEndian.PutUint16(b[18:],5);binary.LittleEndian.PutUint16(b[20:],50);copy(b[prefix:],body);return b
}
func reviewerPutBlock(b []byte, offset int, next uint32) {
 binary.LittleEndian.PutUint16(b[offset:],0xfffb);binary.LittleEndian.PutUint16(b[offset+2:],5);binary.LittleEndian.PutUint16(b[offset+4:],50);binary.LittleEndian.PutUint32(b[offset+6:],next)
 for j:=1;j<5;j++ { p:=offset+j*10;binary.LittleEndian.PutUint16(b[p:],9);binary.LittleEndian.PutUint32(b[p+6:],uint32(len(b))) }
}
func TestReviewerNonmonotoneChainAndOwnership(t *testing.T) {
 b:=reviewerDoc(166,nil);reviewerPutBlock(b,16,116);reviewerPutBlock(b,116,66);reviewerPutBlock(b,66,0)
 image,err:=wp51.Parse(b);if err!=nil {t.Fatal(err)}
 info:=image.Inspect();if len(info.Blocks)!=3||info.Blocks[1].Data.Offset!=116||info.Blocks[2].Data.Offset!=66 {t.Fatal("lost native traversal order")}
 if !bytes.Equal(image.Export(),b) {t.Fatal("nonmonotone chain changed")}
 want:=bytes.Clone(b);var wg sync.WaitGroup
 for j:=0;j<8;j++ {wg.Add(1);go func(){defer wg.Done();for i:=0;i<50;i++ {out:=image.Export();out[0]=0;meta:=image.Inspect();meta.Blocks[0].Data.Offset=0;span,_:=image.Bytes(wp51.Span{Offset:0,Length:16});span[0]=0}}()};wg.Wait()
 if !bytes.Equal(image.Export(),want) {t.Fatal("shared ownership escaped")}
}
func TestReviewerEmptyOpaqueSpansAndUnusedBytes(t *testing.T) {
 // A zero-length opaque span can point inside an index block: nonempty overlap alone is refused.
 b:=reviewerDoc(90,[]byte("EOF"));binary.LittleEndian.PutUint16(b[26:],0xffff);binary.LittleEndian.PutUint32(b[32:],30)
 binary.LittleEndian.PutUint32(b[22:],0xffffffff) // type0 at the next entry ends enumeration
 for i:=46;i<90;i++ {b[i]=0xff}
 image,err:=wp51.Parse(b);if err!=nil {t.Fatal(err)};if !bytes.Equal(image.Export(),b){t.Fatal("unused bytes dropped")}
 // Offset arithmetic must stay refusal-only for every high-bit pointer/length combination.
 for _,pos:=range []uint32{0x80000000,0xfffffffe,0xffffffff} {for _,n:=range []uint32{0,1,0x80000000,0xffffffff} {bad:=bytes.Clone(b);binary.LittleEndian.PutUint32(bad[28:],n);binary.LittleEndian.PutUint32(bad[32:],pos);before:=bytes.Clone(bad);im,e:=wp51.Parse(bad);var failure *wp51.Failure;if im!=nil||!errors.As(e,&failure)||failure.Category!=wp51.MalformedPrefix||!bytes.Equal(bad,before){t.Fatalf("bad pointer acceptance: %x/%x %v",pos,n,e)}}}
}
```
<!-- WP02_REVIEW_GO_END -->

From the lane checkout:

```sh
python3 - <<'PYCODE'
from pathlib import Path
import json
artifact = Path('/home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP02-native-reader/review-evidence-1.md').read_text()
code = artifact.split('<!-- WP02_REVIEW_GO_BEGIN -->', 1)[1].split('```go\n', 1)[1].split('\n```', 1)[0]
source = Path('/tmp/wordling-wp02-review-adversarial_test.go')
source.write_text(code)
virtual = Path.cwd() / 'internal/wp51/reviewer_adversarial_test.go'
Path('/tmp/wordling-wp02-overlay.json').write_text(json.dumps({'Replace': {str(virtual): str(source)}}))
PYCODE
go test -overlay=/tmp/wordling-wp02-overlay.json ./internal/wp51 -run='^TestReviewer' -count=1 -v
go test -race -overlay=/tmp/wordling-wp02-overlay.json ./internal/wp51 -run='^TestReviewer' -count=1 -v
```
