# WP79 independent storage review

Verdict: **APPROVE** the bounded storage foundation. No blocking finding.

Reviewer: `/root/everyday_baseline_audit`, independent of the implementation author; runtime actor `codex`. Issued review invocation `8cc67a372dff4709871add3a9f77eaf5`. Frozen source `7e99079ddf0f75f43e8c7027f52378cbe746b63a`, base `cf9b2af5d0cdb4cb85a22c74c8e9ca9ef54bbb46`.

## Scope and source custody

Reviewed the complete nine-path delta: both new production files, the shared stageCandidate extraction/Close serialization, all new tests, authoritative README and focused evidence. No old tests, immutable reference artifacts, native parser/writer, editor or TUI source changed. All manifest source/reference sizes and SHA-256 values independently matched. WP77 d55067a6, WP78 d6b24d3f and WP90 78a05497 are actual ancestors, not an overlay; corresponding approval event IDs exist in the canonical event log. WP41 source and its unchanged publication contracts are inherited on the B lane. Primary shared planning/status remains separate from this frozen source review.

This is the explicitly scoped sequential B-lane continuation of WP03/WP24/WP34/WP41. It changes the owned shared storage implementation/README while preserving existing local-flat and macro callers and their assertions. New consumer routes remain WP82 lifecycle, WP84 browser and WP86 executable qualification. Their absence now is permitted by the package's explicit foundation contract, not a claim of already integrated end-user behavior.

## Findings and acceptance assessment

T239/T240 pass: pinned C-root/child capabilities, parent boundary, declared ASCII 8.3/case/wildcard/symlink/metadata mapping, bounded enumeration/acquisitions, detached display rows and private selected observations are present. Selection read verifies the selected stamp and later native snapshot; replaced selections and ambiguous aliases fail explicitly. Logical ancestry after a host rename is documented rather than falsely claiming a current path.

T241 passes: sourced versus never-sourced preparation remains explicit. Candidate bytes and source/destination wrappers are captured; IDs/receiver and single-use state are checked; wrong IDs do not consume an otherwise valid request. Existing destinations require explicit Yes. Full previous destination bytes become the shared basename.BK!, including Save As; repeated enabled rotation and disabled deletion agree with approved WP78 observations. New saves do not invent a prior backup. Refusal/cancel preserve both files. Unqualified backup-as-target collision and backup inode aliases are safely refused and identified as open full-M1 cases.

T242 passes within the documented trusted local-filesystem boundary: actual stage/file-sync/namespace/directory-sync/cleanup failures are tested; rollback preserves prior main/backup when entries still belong to the transaction. Observed external interference prevents destructive rollback and exposes uncertainty/recovery names. Post-commit failure never returns an admitted new source. Same-capability transactions and Close serialize; stale prepared requests and replays refuse. This is not an atomic multi-file transaction, malicious concurrent-writer defense or crash-recovery manager, and documentation does not claim otherwise.

T243 passes: API/evidence/acceptance mapping is concrete and original raw backup snapshots are compared as complete bytes. Storage preserves framing and unrelated bytes without granting semantic-edit permission. Original supplementary filenames and native bytes work through the same publication APIs; provider semantics remain WP87's responsibility.

## Independent execution

Executed from the fixed lane B checkout:

- `go build ./...` — PASS.
- `go test ./...` — PASS, including baseline, native/document/editor/TUI and macro suites.
- `go vet ./...` — PASS.
- `go test -race ./internal/storage` — PASS.
- `go test -count=1 -race ./internal/storage` — PASS, fresh execution of all storage tests and actual staged-failure hooks (4.624s).
- `gofmt -l` on all four changed Go files — no output; diff check — clean.

A separate temporary module imports only public storage APIs using the actual frozen checkout via a Go module replace, without source overlay or private hooks. `GOWORK=off go test -mod=mod -race -v ./...` passed. Its independent sequence performs 35 alternating A.WP/A.TXT cross-directory/repeated saves with enabled/disabled backups, checks complete destination/backup bytes, preserves the original source, rejects replay/default-No/cancel, induces real directory permission denial using chmod0500, rejects a replaced selected file, refuses an outside-directory symlink, and rejects a case alias appearing after preparation. Permission failure preserves both prior files. Exact probe source is retained below for reproducibility; the temporary module path is not a product dependency.

The full suite includes actual original STAGE1/2/3 and BACK2/3 byte comparisons, stale source/target/backup, short writes, file/dir sync and close failures, rollback interference, resource bounds and close concurrency. Independent review inspected hook reachability/assertions; it did not count synthetic result messages as real publication evidence.

## Required anti-pattern checklist

1. Dead code — **PASS under explicit foundation exception**: public API tests execute the real layer; production consumers are explicitly assigned82/84/86. Shared stageCandidate already has legacy and new callers. No UI completion claimed.
2. Synthetic fixtures — **PASS**: real filesystem/native APIs produce asserted state; independent arbitrary revision bytes extend original framing, and raw original backup snapshots supply separate expected bytes.
3. Silent empty returns — **PASS**: empty getters represent nil/absent observations; acquisition/publication failures carry errors. No failed save returns success or an admitted new source.
4. FR coverage — **PASS for assigned layer**: file lifecycle, browse/acquisition and backup preservation exercised; broader FR006/017 whole-product coverage is not inferred.
5. Frozen surface — **PASS**: nine scoped files only; old tests/reference artifacts unchanged.
6. Locked decisions — **PASS**: no native replacement format, unknown-byte rewriting, unreviewed resource substitution, full-M1 acceptance or M2 work.
7. Shared-file ownership — **PASS**: B-lane continuation and source coordination stated above; no unrelated component edits.
8. Production fragility — **PASS**: explicit ordinary errors/uncertainty, no transient-race panic path introduced.

The charter Code Review Checklist query reports that section is unauthored; no charter mutation was made. Verdict qualifies WP79 only. No preview replacement or overall parity acceptance follows from it.

## Independent public probe

```go
package review79
import("bytes";"fmt";"os";"path/filepath";"testing";"github.com/lynncoleart/wordling/internal/storage")
const repo="/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-b"
func must(t *testing.T,e error){t.Helper();if e!=nil{t.Fatal(e)}}
func eq(t *testing.T,p string,b []byte){t.Helper();got,e:=os.ReadFile(p);must(t,e);if !bytes.Equal(got,b){t.Fatalf("byte difference %s",p)}}
func TestIndependentPublicFilesystem(t *testing.T){
 root:=t.TempDir();childPath:=filepath.Join(root,"DOCS");must(t,os.Mkdir(childPath,0700));b,e:=os.ReadFile(repo+"/docs/research/everyday-contract-2026-11-05/r2/EVERY.WP");must(t,e);must(t,os.WriteFile(filepath.Join(root,"START.WP"),b,0600))
 w,e:=storage.OpenWorkspace(root);must(t,e);defer w.Close();r,e:=w.Root();must(t,e);child,e:=r.Navigate("DOCS");must(t,e);src,e:=r.Directory().Read("START.WP");must(t,e)
 for i:=1;i<=35;i++{name:="A.WP";if i%2==0{name="A.TXT"};path:=filepath.Join(childPath,name);old,readErr:=os.ReadFile(path);setting:=storage.OriginalBackupOn;if i%3==0{setting=storage.OriginalBackupOff};edited:=append(append([]byte{},b...),[]byte(fmt.Sprintf("independent revision %d",i))...);dst,e:=child.Observe(name);must(t,e);id:=storage.PublicationID{Operation:uint64(i),Revision:uint64(i)};req,e:=child.Directory().PrepareSave(src,dst,edited,storage.AllowOverwrite,setting,id);must(t,e);res,e:=child.Directory().PublishSave(req,id);must(t,e);eq(t,path,edited);if res.Document==nil{t.Fatal("missing source receipt")};src=res.Document
 if readErr==nil{if setting==storage.OriginalBackupOn{eq(t,filepath.Join(childPath,"A.BK!"),old)}else{if _,e=os.Stat(filepath.Join(childPath,"A.BK!"));!os.IsNotExist(e){t.Fatal("backup not removed",e)}}};if _,e=child.Directory().PublishSave(req,id);e==nil{t.Fatal("replay accepted")}}
 eq(t,filepath.Join(root,"START.WP"),b)
 dst,e:=child.Observe("A.WP");must(t,e);old,e:=os.ReadFile(filepath.Join(childPath,"A.WP"));must(t,e);backup,e:=os.ReadFile(filepath.Join(childPath,"A.BK!"));must(t,e);id:=storage.PublicationID{Operation:50,Revision:50}
 if _,e=child.Directory().PrepareSave(src,dst,b,storage.NoOverwrite,storage.OriginalBackupOn,id);e==nil{t.Fatal("No overwritten")};p,e:=child.Directory().PrepareSave(src,dst,b,storage.AllowOverwrite,storage.OriginalBackupOn,id);must(t,e);if !p.Cancel(){t.Fatal("cancel")};if _,e=child.Directory().PublishSave(p,id);e==nil{t.Fatal("canceled publish")};eq(t,filepath.Join(childPath,"A.WP"),old);eq(t,filepath.Join(childPath,"A.BK!"),backup)
 p,e=child.Directory().PrepareSave(src,dst,b,storage.AllowOverwrite,storage.OriginalBackupOn,id);must(t,e);must(t,os.Chmod(childPath,0500));_,e=child.Directory().PublishSave(p,id);must(t,os.Chmod(childPath,0700));if e==nil{t.Fatal("permission failure claimed success")};eq(t,filepath.Join(childPath,"A.WP"),old);eq(t,filepath.Join(childPath,"A.BK!"),backup)
 l,e:=child.List("");must(t,e);sel,e:=l.Select(l.Find("A.WP"));must(t,e);must(t,os.Rename(filepath.Join(childPath,"A.WP"),filepath.Join(childPath,"OLD.WP")));must(t,os.WriteFile(filepath.Join(childPath,"A.WP"),old,0600));if _,e=sel.Read();e==nil{t.Fatal("replacement selected")}
 must(t,os.Symlink(t.TempDir(),filepath.Join(root,"LINK")));if _,e=r.Navigate("LINK");e==nil{t.Fatal("outside symlink followed")}
 dst,e=r.Observe("NEW.WP");must(t,e);id=storage.PublicationID{Operation:51,Revision:51};np,e:=r.Directory().PrepareNewSave(dst,b,storage.NoOverwrite,storage.OriginalBackupOff,id);must(t,e);must(t,os.WriteFile(filepath.Join(root,"new.wp"),b,0600));if _,e=r.Directory().PublishNewSave(np,id);e==nil{t.Fatal("late alias accepted")};if _,e=os.Stat(filepath.Join(root,"NEW.WP"));!os.IsNotExist(e){t.Fatal("unexpected target",e)}
}

```
