# Structural merge Undelete

Reference US WordPerfect 5.1 DOS 03/09/92, Standard Printer. Each primary or secondary probe booted a private copy of the pinned guest, verified the release in Help, retrieved the original CMD51-134 fixture and captured the original 80×25 cells and VGA roles. The evidence directory for these runs is `/tmp/wordling-merge-undelete.bUkj4T`. The additional cross-screen original captures are in `/tmp/wordling-review-cross-history.gaqMKv`.

## Original behavior and physical checks

| Journey | Original steps and observation | Capture |
| --- | --- | --- |
| FIELD owner only | Retrieve PRIMARY.WP5, open Reveal, Right six times, Delete and press F1. The body still has `1~`; the overlay shows `Hello [Block][Mrg:FIELD]1~[HPg]`. The upper FIELD label is red, while lower pane emphasis is on the following `1`. Restore inserts only the FIELD owner at the active caret. | `field/{deleted,preview,restore}` |
| Original three entries | Delete H, Right/Delete l, Right/Delete o, Right/Delete FIELD. F1 previews FIELD, then Previous shows o, then l, then wraps to FIELD. H has fallen out. | `ring-repeat/{preview,previous,previous-again,restore}` |
| Consecutive owners | Delete FIELD and its now-literal digit at the same gap. One preview shows both before `~`, with the lower caret on the tilde, and one Restore restores both. | `adjacent-repeat/{deleted,preview,restore}` |
| Operand | At the numeric operand, insert `2` before `1`, then Delete `1`. F1 shows `[Mrg:FIELD]2[Block]1~`; Restore returns `21~` at that gap and preserves the rest of the source. | `operand/{at-operand,insert,deleted,preview,restore}` |
| Record structure | On SECOND.WP5, delete End Field or End Record in Reveal. F1 previews the actual owner, with the retained HRt or HPg at the lower caret. Restore reproduces the native record body. Deleting End Field, its exposed HRt and End Record consecutively forms one group. Restore returns both the original End Record field count and generated D4/HPg row. | `endfield`, `endrecord`, `cache`, `cache-triple` |
| Cancel | At the F1 prompt, Enter (default zero), literal 0 and Escape cancel without restoring or losing the group. F1 also cancels. In Reveal the prompt occupies row 11 and the ordinary Reveal footer stays on row 24. | `cancel/{preview,cancel-default,reopen-default,cancel-zero,reopen-zero,cancel-escape}` |
| Two screens | Delete FIELD in Doc 1, Shift+F3 to blank Doc 2, then F1. It previews the FIELD fragment. Restore into blank Doc 2 produces exactly one native FIELD owner without an operand. Retrieve on the blank screen retains the ring. Delete ordinary q in Doc 2 and switch to Doc 1. F1 shows q first and FIELD under Previous. Closing Doc 2, acquiring a fresh Doc 2, and clearing Doc 1 while staying in WP retain the newest group. | `dos`, `restore-settled`, `lifecycle`, `lifecycle-settled` in the cross-screen original root |

The parked-ring test is a Wordling safety check for the Linux/native admission boundary. An authenticated ring remains available after leaving a read-only native screen, while the read-only screen cannot consume a mutation receipt.

## Reproduce

```sh
go build -o /tmp/wordling-merge-undelete ./cmd/wordling
for case in structural cross-restore cross-lifecycle triple-original; do
    python3 tests/everyday_qualification/merge_undelete.py "$PWD" \
        /tmp/wordling-merge-undelete "/tmp/wordling-merge-undelete-$case" --case "$case"
done
go test -count=1 ./internal/document ./internal/editor \
    -run 'TestMergeHistory|TestWorkspaceReadOnlyScreenParks'
```

The driver launches the normal Linux CLI and delivers actual terminal input. The fresh four-case output is in `/tmp/wordling-merge-undelete.bUkj4T/screen-*`. It checks the original prompt rows and roles, the restored native bodies, selection cycling, canceled previews, and authenticated transfer across the observed screen lifecycle.

| Exact product and original output | Bytes | Body offset | SHA-256 |
| --- | ---: | ---: | --- |
| `CROSS.WP`, restore lone FIELD on the blank second screen | 332 | 324 | `976f6e23b93a8fbecd9e39848a611980d54015462a5cec9dd0f55556d6a94c8f` |
| Wordling `TRIPLE.WP` and original `REST.WP`, same-gap three-owner restoration with Fast Save Yes | 676 | 564 | `3130c4eb60a245fff778dbe6605be0dbd658480c4b2930919edbd676e5c66ad2` |

The shared ring uses the existing bounded immutable fragment history. Structural receipts hold the deleted owner separately from derived changes, and the current cursor and document own every restoration. The receiver still undergoes typed native validation. The accepted standalone FIELD can be saved faithfully and remains nonexecutable without a valid operand. Ordinary-only legacy history behavior retains its existing qualification.
