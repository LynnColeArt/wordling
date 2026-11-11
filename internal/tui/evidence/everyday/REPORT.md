# WP84 original editing viewport and file browser

This package uses the standard US WordPerfect 5.1 DOS release dated 03/09/92 and the Standard Printer profile. The original [everyday reference](../../../../docs/research/everyday-contract-2026-11-05/) supplies native documents, exact VGA cells and observed command sequences. The ordinary `cmd/wordling` program sets the existing historic-editor configuration. Its normal keys go through Bubble Tea and the editor reducer. The older bounded runtime configuration retains its existing API behavior.

## Approved source and file custody

Lane H consumes the independently approved session and native/layout/storage ancestry through merge `988addf36bc9591621e91e0692abfd29240064e2`. WP94 source `3ef16980`, WP99 `1885c068`, WP93 and WP91 are actual ancestors. The shared baseline test intake and final owned source are recorded with the release handoff. No native prefix admission changes are part of WP84.

The committed `FLOW.WP` is an actual 03/09/92 original output. The original WP78 FLOW (SHA-256 `757d4466fb78e843ee6bb6355c3e0d6353766c626a47e8ba1875e395ea8dd003`) used a 564-byte Fast Save prefix. In a private verified copy of the reference disk, Setup switched Fast Save to No, the same file was retrieved, and F10 saved under a fresh name before the guest was stopped. The new file is 773 bytes with a 324-byte admitted prefix and SHA-256 `549b55dea301b159bc00ea7910de3695f6169630cfa72f1a2136f74ba39ed7f5`. Its entire 449-byte native body matches the source. The private acquisition captures and replay are at the path recorded in the verification section. The unsupported 564-byte receiver still reports its existing refusal.

## Journeys

| Contract | Verified behavior |
| --- | --- |
| T264 and EE-004/006/008 | Physical F2 search, F11 and Alt+F3 Reveal, F5 List Files, End, Home Home Left, Page Up/Down, menu keystrokes, SGR click and F10/F7 through the ordinary binary. Model cases include native search cancel, search repeat notice, previous/next page and loaded native conservation. |
| T265 and EE-005/010 | Shared physical layout drives the editor and multiline Reveal. The ANSI PTY 80×25 cells match the selected original upper text, foreground/background roles, ruler, lower pane, bottom-right status and restore prompt. The original reference had the menu hidden. The Linux menu row shifts upper text down one row, while status and Reveal rows keep their original positions. |
| T265 and EE-006 | Undelete projects the read-only overlay through the same physical layout. A terminal-side wrap label is view-only, and the restored text and caret never use a display string as native input. The model test reproduces the original trailing DSRt/YZ preview, including the red upper-pane selection. F1 cancels without modifying native bytes. |
| T266 and EE-009/011 | Original F5 directory prompt, actual pinned listing, current/parent/child and name selection, short/long choice, paging, Look Next/Previous/return, and selected native Retrieve. A declined occupied Retrieve keeps the selected entry and untouched editor document. Confirmed retrieval uses the editor's actual authenticated operation. |
| T267 and EE-014 | WP90/R77-001 modal safety survives 12→11→25 rows for menu, directory prompt and entered list. Browser model and Linux PTY tests preserve bytes and history and verify ordinary editing focus after cancel. Layout and terminal clipping remain separate. |
| T268 | The normally built executable opened and copied the reference native file byte for byte. Physical terminal restoration and normal F7 exit are checked by the PTY driver. |

The original file list Red header, 80-column divider, current/parent rows, long-list headings, command accelerators and Look banner come from WP78 files captures 20, 26, 27 and 50. The Linux clock, available space, file count and timestamps describe the actual local workspace. Original 03/09/92 probe captures recorded resident document sizes of 0 for a new blank buffer, 262 for four typed bytes, and 963 for the retrieved 449-byte FLOW body. The ordinary draft and loaded cases use those observed default-profile rules. Unimplemented List Files actions retain their original labels and give an explicit unsupported command response. WP85 owns the full menu geometry and focus profile, and later packages own proofreading and final release delivery.

## Verification

Build and run from the repository root.

```sh
go build ./...
go test ./...
go vet ./...
go test -race ./internal/tui
go build -o /tmp/wordling-wp84 ./cmd/wordling
python3 internal/tui/evidence/everyday/pty-everyday.py "$PWD" /tmp/wordling-wp84 /tmp/wordling-wp84-pty-fresh
```

The runner uses a synthetic Linux PTY with actual encoded terminal keys and SGR mouse events, checks terminal restoration, and keeps all workspace writes in its disposable directory. It compares exact VGA glyphs and logical attributes, with the original ruler and divider glyphs translated to their single-cell Linux equivalents. A physical terminal emulator's raster and theme palette can differ. Original source captures and exact PTY result paths appear in the final verification record.

- Shared invariant baseline source is `ca9a5039`, integrated through `710809cdf8f815c6c44c6d861106eafc87d86659`.
- Actual DOS fixture resave, release and Setup captures are at `/tmp/wordling-WP84-flow-native.Sp7h04`. Resident-size probe folders are listed in the terminal verification record.

- Approved source identities: WP91 `5aa69050`, WP93 `2df0dd6d`, WP99 `1885c068`, WP94 `3ef16980`. All are ancestors of this implementation.
- Full Go build, test and vet passed. Focused TUI race, Go formatting, Python syntax and Git diff checks passed.
- Two physical-key PTY captures: `/tmp/wordling-WP84-accept.7w3elM/first` and `/tmp/wordling-WP84-accept.7w3elM/repeat`. Both recorded 38 steps and restored terminal attributes after normal F7 exit.
- Executable SHA-256 `460cbe630586cae3451aee78db5e52905410e205246640654738e8fa8ce9a581`. The F10 native copy in both runs matched original fixture SHA-256 `549b55dea301b159bc00ea7910de3695f6169630cfa72f1a2136f74ba39ed7f5`.
- Original resident-size probe folders: `/tmp/wordling-WP84-files-metrics.QydriP`, `/tmp/wordling-WP84-metrics-flow.fs9kh6` and `/tmp/wordling-WP84-metrics-before.UvUgCb`.

Changed source and fixture SHA-256 at verification:

```text
0c9b38554e817170928e7fce14f43c733168872159dd7b34d0c0ad8cdb6148fc  internal/tui/bold_authoring.go
b505a0a12608dcc6960f0f73b1297aa040b4ec14a96655ebaed5273529302984  internal/tui/chrome.go
e4bfe40030dff3f9f81eef2b4d749241ff9c28353e5d144e6c4b20f3dc1db9b0  internal/tui/chrome_test.go
3e5c63d6f989a785f74f4bb1d88651d7e0439dde9226da2dad41b7803e1d4acf  internal/tui/everyday_files.go
50dc9e2dcb44d60f2b386bd2558bdeeb1a225d19ae18238eb7805bfcac2f3b73  internal/tui/everyday_ui_test.go
0daea2df46345f0a01c5d0d8906c560b7ab260a7eee0d2f7d35d052bcf54002b  internal/tui/everyday_view.go
41d3fc54791eff90dd81326cd0f01e4bcff9b20ec21d8a2e118bdc5430ffdf9b  internal/tui/historic.go
e7bb0da5a2dbd1724166e873026a7d8f281eebb62083e699ee586d1f964384e2  internal/tui/model.go
328d60efc9dca126d3cfb23a93e3fd6c38b88ff804cc7526901c97764980c411  internal/tui/runtime.go
549b55dea301b159bc00ea7910de3695f6169630cfa72f1a2136f74ba39ed7f5  internal/tui/evidence/everyday/FLOW.WP
1eae5440940035241776e2ab2d339964a7d591fc265c96ace1eb018f593b0556  internal/tui/evidence/everyday/pty-everyday.py
```
