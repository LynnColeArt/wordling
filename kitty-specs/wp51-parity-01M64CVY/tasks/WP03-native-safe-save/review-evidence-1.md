# WP03 independent storage review — 2026-10-30

Assessment: approve bounded storage commit `7deeaf6d7b62ce291358eceb81cb08c6f82ce512` on top of approved native reader `e7de080452c2906e99c8ace0048c415d842f2f89`. The authoritative lifecycle verdict is the CLI review_result event; this prose supplies evidence. Reviewer-renata and review action governance were resolved; this reviewer is separate from the implementer.

Source/tests were reviewed and run exclusively in `/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-b`. `git diff e7de080..7deeaf6` is confined to eleven `internal/storage/` files. `git diff --exit-code e7de080..7deeaf6 -- internal/wp51` passes: approved reader source/tests/evidence are unchanged. This review artifact belongs to primary planning placement, not the code lane. No implementation edits made.

## Bounded acceptance and race assessment

- T007 establishes actual API/observation semantics before the code: flat bounded names, pinned directory authority, regular non-symlink leaves, explicit existing/absent destination observations and source metadata/hash snapshots. Source freshness, atomic new-name publication and final successful verification are distinct observation points, not a cross-file atomic transaction or a future-freshness promise.
- T008 is implemented safely for the declared subset. `Directory.Read` limits acquisition to reader limit+1 and actually calls `wp51.Parse`; exported native bytes remain exact. `Save` verifies loaded source freshness and destination observation, requires explicit permission for an existing destination, performs a verified same-inode no-op only, and refuses every actual existing-file replacement. Identical bytes in a different inode do not authorize replacement.
- New destinations use exclusive random candidates and atomic **no-replace `Root.Link`**, with no overwrite-capable rename or destination unlink. Candidate writes/short writes/close results and candidate inode/bytes are checked before publication. Read-only inode pinning prevents closed-writer inode reuse. Directory leaf opens use `openat` on a RawConn-pinned descriptor, with no-follow/nonblocking flags; candidate/source leaf substitution and concurrent directory Close are not treated as valid unchecked path opens.
- Link or later failure never produces successful outcome. Ambiguous publication and cleanup report destination/residue information. Post-link verification never rolls a destination back by unlinking a name that could now belong to a different writer. Final verification follows candidate unlink so its ctime change is accounted for. The documented same-user candidate check/unlink race limitation is retained; this is not a hostile-directory conditional-delete primitive.
- T009 covers real candidate-create/short/full/partial-write/write-close/read-close/pin faults, stale source and destination changes, source symlink/FIFO/open races, publication failure before/after actual side effects, candidate substitution before/between check/link, and foreign destination replacement after link/during cleanup. Source/foreign files stay intact and failures have typed causes with empty successful outcomes.
- Ordinary rename failure is **N/A**: production publishes with Link, and its real failure boundary is tested. Full existing replacement, original F10/backup/Fast Save/locking/recovery, nested path mappings, network filesystems, mount/hostile-filesystem races and fsync/power-loss durability remain explicitly unsupported M1 follow-up. This is a bounded no-edit filesystem foundation, not acceptance of those original behaviors or a semantic writer.

## Independently executed checks

- `python3 scripts/review_checks.py --junitxml=/tmp/wordling-wp03-review-junit.xml`: all seven genuine checks pass with no skips, including Go build/all tests/vet and both catalogue validators. Tests include unchanged WP02 original-run provenance/hash checks plus storage reads/new publications of all five accepted originals; macro retains typed native refusal.
- `go test -race ./internal/storage -count=1 -timeout=60s`: pass (2.569s package result).
- `gofmt -l internal/storage/*.go`: no output. `git diff --check e7de080..7deeaf6`: pass.
- Production SHA-256 `75e773e7ec01faa3943c76c874dd0bb4e99937113965139e9239e5ce498beb56` matches host/mutation restoration evidence. Resource/race RSS evidence is qualified as harness-wide, not isolated storage memory or product performance. No unexecuted storage/native fuzz result is claimed.
- Independent overlay probes below pass **five repetitions under race**. Sixteen concurrent saves of the same absent observation yield exactly one publisher, exact original bytes and no temporary residue. Cross-directory hardlink aliases require explicit permission and then return a verified same-inode no-op; a newly published copy has exact bytes and an independent inode. No caller exclusivity flag supplies a missing replacement guarantee.

## Anti-pattern checklist disposition

1. Live integration: **PASS** for the new reader consumption (`Directory.Read` calls `wp51.Parse`); **N/A** for user-facing storage entry points in this explicit API foundation. No CLI/F10 workflow is claimed or manufactured outside this WP.
2. Synthetic-fixture assertion: **PASS**. Public APIs and actual OS files exercise production behavior; injected failures occur at filesystem responsibility boundaries, rather than constructed passing outcomes.
3. Silent empty return: **PASS**. Invalid spans/requests and IO failures carry explicit refusal/causes; cleanup no-ops are explicitly for an absent/uncreated owned candidate.
4. Scoped requirement coverage: **PASS** for FR-006/NFR-001/002/C-002's declared slice; full file operations remain M1 follow-up.
5. Frozen surface: **PASS**; reader dependency and all original evidence unchanged.
6. Locked decisions: **PASS**; native formats unchanged, no hidden normalization, no semantic writer or modern feature added.
7. Shared ownership: **PASS**; new production surface stays inside storage, dependency reader is consumed without changes.
8. Production fragility: **PASS**; typed refusal and conservative uncertain/residue outcomes replace silent success; no unsafe destination rollback or unbounded leaf acquisition identified.

No blocking findings. Approval does not establish general overwrite, durability, original-app semantic edit/print interoperability or full M1 acceptance.

## Reproducible independent race probes

The following is temporary Go-overlay review code only; it uses existing test helpers and real temporary files. It does not change production or checked-in tests.

<!-- WP03_REVIEW_GO_BEGIN -->
```go
package storage

import (
 "bytes"
 "errors"
 "os"
 "path/filepath"
 "sync"
 "testing"
)

func TestReviewerOneWinnerForConcurrentAbsentObservation(t *testing.T) {
 d,doc,target,path,input:=storageCase(t)
 type answer struct {out Outcome; err error};results:=make(chan answer,16)
 var wg sync.WaitGroup;start:=make(chan struct{})
 for i:=0;i<16;i++ {wg.Add(1);go func(){defer wg.Done();<-start;o,e:=d.Save(doc,target,NoOverwrite);results<-answer{o,e}}()}
 close(start);wg.Wait();close(results);winners:=0
 for r:=range results {
  if r.err==nil {if r.out.State!=Published {t.Fatal("false success outcome")};winners++;continue}
  var f *Failure
  if r.out.State!=""||!errors.As(r.err,&f)||(f.Kind!=DestinationChanged&&f.Kind!=PublicationFailed){t.Fatalf("bad racing refusal: %+v %v",r.out,r.err)}
 }
 if winners!=1 {t.Fatalf("want one atomic publication winner, got %d",winners)}
 content(t,filepath.Join(path,"source"),input);content(t,filepath.Join(path,"destination"),input)
 if len(candidateNames(t,path))!=0 {t.Fatal("racing operation leaked candidate")}
}

func TestReviewerSameInodeAcrossBoundDirectories(t *testing.T) {
 input,err:=os.ReadFile("../../docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5");must(t,err)
 parent:=t.TempDir();source:=filepath.Join(parent,"source-dir");dest:=filepath.Join(parent,"dest-dir")
 must(t,os.Mkdir(source,0700));must(t,os.Mkdir(dest,0700));must(t,os.WriteFile(filepath.Join(source,"source"),input,0600))
 must(t,os.Link(filepath.Join(source,"source"),filepath.Join(dest,"alias")))
 src,err:=OpenDirectory(source);must(t,err);defer src.Close();dst,err:=OpenDirectory(dest);must(t,err);defer dst.Close()
 doc,err:=src.Read("source");must(t,err);observation,err:=dst.Observe("alias");must(t,err)
 out,err:=dst.Save(doc,observation,NoOverwrite);refusal(t,out,err,OverwriteRequired)
 out,err=dst.Save(doc,observation,AllowOverwrite);must(t,err)
 if out.State!=Unchanged||out.DirectoryID!=dst.ID()||out.Identity.ID!=doc.identity.ID {t.Fatal("same inode no-op lost bound identity")}
 absentTarget,err:=dst.Observe("published");must(t,err);out,err=dst.Save(doc,absentTarget,NoOverwrite);must(t,err)
 if out.State!=Published {t.Fatal("cross-directory snapshot not published")}
 content(t,filepath.Join(source,"source"),input);content(t,filepath.Join(dest,"alias"),input);content(t,filepath.Join(dest,"published"),input)
 copied,err:=dst.Read("published");must(t,err)
 if !bytes.Equal(copied.Export(),doc.Export())||copied.identity.ID==doc.identity.ID {t.Fatal("publication should be exact independent new inode")}
}
```
<!-- WP03_REVIEW_GO_END -->

From lane-b:

```sh
python3 - <<'PYCODE'
from pathlib import Path
import json
artifact=Path('/home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/tasks/WP03-native-safe-save/review-evidence-1.md').read_text()
code=artifact.split('<!-- WP03_REVIEW_GO_BEGIN -->',1)[1].split('```go\n',1)[1].split('\n```',1)[0]
source=Path('/tmp/wordling-wp03-review-adversarial_test.go');source.write_text(code)
virtual=Path.cwd()/'internal/storage/reviewer_adversarial_test.go'
Path('/tmp/wordling-wp03-overlay.json').write_text(json.dumps({'Replace':{str(virtual):str(source)}}))
PYCODE
go test -race -overlay=/tmp/wordling-wp03-overlay.json ./internal/storage -run='^TestReviewer' -count=5 -timeout=60s -v
```
