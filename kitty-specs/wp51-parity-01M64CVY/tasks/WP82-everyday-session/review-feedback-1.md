# WP82 review feedback — review-cycle-1 REJECTED (2026-11-09)

Reviewer: kat (independent review, mission loop restored after remote reconciliation).
Reviewed delta: PR #4, commit 838da602 (merged to feat/wp51-parity 2026-11-06 21:56 UTC).
Context: local branch reconciled d23171fe; PR body itself disclaims completeness
("WP82 narrow surface only; broader daily editor integration is later work").

## Blocking findings

**W82-1 — delivery does not satisfy the WP82 contract (high).**
The contract (T254–T258) requires complete everyday session lifecycle: supported
document command routing through approved APIs (T254), navigation and correction
(arrows/Home/End/Page/Insert/typeover/block correction/Undelete, T255), save and
retrieval lifecycle incl. first save/Save As/cancel/backups/F7 flow (T256),
two-document and continued-New state (T257), and public Session journeys with an
evidence report (T258). The merged delta is 35 lines
(internal/editor/everyday/{README,session,session_test}): a zero-token `Daily`
stub around an empty `layout.Layout{}` that consumes nothing from the approved
WP81 engine and does not touch the owned `internal/editor` session surface.
The package README's own disclaimer cannot reconcile a complete-contract WP.

**W82-2 — delivery shape contradicts the planning record (high).**
create_intent names `internal/editor/everyday.go` and `internal/editor/everyday_test.go`
in the parent `internal/editor` package, with `evidence/everyday/**`. The merge
created a subdirectory package `internal/editor/everyday` declaring `package editor`
— a subpackage sharing its parent's package name. None of the WP's owned
internal/editor files were edited. No owner amendment authorizing the file
relocation exists in mission decisions, amendment commits, or git.

**W82-3 — required evidence absent (medium).**
No `internal/editor/evidence/everyday/REPORT.md` was delivered (T258); no
acceptance mapping for EE-004/005/006/007/008/011/012/013. The runtime for_review
gate independently blocked on exactly T254–T258 being unchecked.

## Remediation (either path; no third option)

1. **Complete to contract**: implement T254–T257 against the approved WP80/WP81
   APIs, resolve file placement to the planned paths (or a recorded amendment),
   deliver the REPORT and evidence, then re-enter for_review honestly.
2. **Owner scope amendment**: if narrow-first is the owner's actual intent, record
   a mission-level amendment splitting a narrow foundational WP from the full
   WP82 contract in mission decisions + git, with subtasks re-pointed, BEFORE
   re-review. An unrecorded PR-body disclaimer is not an amendment.

The merged commit 838da602 may be built upon by path 1; nothing here requires
reverting it on feat/wp51-parity. Local reconciliation d23171fe is unpushed and
awaits owner instruction.
