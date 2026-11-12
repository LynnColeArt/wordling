# WP91 independent review

**Approve** the storage provenance seam at frozen commit
`5aa6905008c884a1d0228ec2cb4efbdc3d6da7be`. Its single parent is the issued
lane B source `d70690b43fe276287bdb20fb71443ff7cb013d84`. The approved WP79
source `7e99079ddf0f75f43e8c7027f52378cbe746b63a` is an ancestor. The diff
changes exactly the two owned storage paths. I did not implement WP91 or
modify its source during review.

Workspace provenance compares live private workspace and acquired directory
capabilities, including independent opens of the same filesystem path. Root,
Navigate, Enter and Selection.Directory return copied public wrappers. Listings
retain private nodes, so reassigning a public wrapper cannot change an earlier
selection. OwnsSelection deliberately checks authority separately from freshness.
Read rechecks observed spelling, DOS alias resolution and the complete file
stamp, then checks the returned Document's private acquisition, name and stamp.
A stale or ambiguous name cannot be treated as another selected file. Closing
a child revokes child authority while preserving the open root. Workspace
closure revokes copies. The workspace lock and atomic directory open state
protect lifetime checks, and operations revalidate after admission.

The WP78 EE-A10 captures show child and parent traversal (files frames 42–47),
Look preserving the buffer and list selection (27–30, 48), and blank and
occupied retrieval (61–66). WP91 supplies the pinned source observation for
those routes. WP94 owns adoption, and WP84 owns the actual F5 UI. This review
does not grant terminal behavior, formatting, pagination, or milestone
qualification for a standalone storage capability.

| Check | Result |
| --- | --- |
| Dead code | N/A for planned foundation consumers WP94 and WP84. MatchesDocument already runs on the selected Read production path. Full executable reachability remains a consumer gate. |
| Synthetic fixture | PASS. The new tests invoke production OpenWorkspace, Navigate, List, Select, Enter, Read, provenance and close on a real filesystem. |
| Silent empty return | PASS. Nil or invalid capability observations return false or empty read-only metadata by contract. Operations fail explicitly. |
| FR coverage | PASS within the WP scope. Real filesystem assertions cover the FR-006 storage behavior and provide the qualified acquisition needed by FR-004/005/008/009 consumers. Exact stored bytes and existing backup/publication tests remain intact. No additional parser behavior is claimed (NFR-003). The original capture and executable consumer references provide the NFR-004 evidence boundary. |
| Frozen surface | PASS. Only everyday_paths_linux.go and everyday_test.go changed. No original captures, backup code, parser, editor, or TUI source changed in this commit. |
| Locked decision | PASS. Actual pinned capabilities, no alias invention or foreign reacquisition, no native writer change. |
| Shared ownership | PASS. WP91 explicitly succeeds WP79 on its original lane and shares exactly the two documented paths. WP94/WP84 consume the public seam. |
| Production fragility | PASS. No panic, unbounded retry or transient error promoted to successful acquisition. |

Independently reran `go build ./...`, `go test ./...`, `go vet ./...`,
`go test -race ./internal/storage -run TestEveryday -count=3`, scoped gofmt
inspection and `git diff --check`. All passed. The frozen lane was clean before
and after verification.
