# Saving edited merge results

The pinned US March 9, 1992 WordPerfect 5.1 DOS release ran on private copies
of the established reference disks with the Standard Printer. The merge uses
CMD51-134's original primary and explicit secondary fixtures. This replay
merges into a blank buffer and goes to document start before typing. The
output has ordinary text and native hard page breaks. The reopened document
contains no merge-source marker.

| Setting | First and repeated dirty saves | Retrieve first save, edit and save |
| --- | --- | --- |
| Yes | Body starts at 564. The middle index starts at 270, with active state 8 and retired state 0. | Body starts at 564. The middle index moves to 272, with active and retired states 8. A further save retains this index. |
| No | Body starts at 324. The formatting owner is first and its state is clear. | The same compact order and clear state recur on each save. |

When No is selected after a Yes save, the next dirty save compacts the graph.
When Yes is selected after a successful No save in the same buffer, the next
dirty save retains that compact order and sets the active formatting bit. This
happens whether the first save used No or the buffer switched from Yes to No.
A new buffer or actual Retrieve starts from that buffer's own provenance.
The product retains exact acquired or last-published bytes for unchanged saves.

The same No rewrite was observed after Retrieve on initially ordered
Standard Printer documents with plain text, with a Bold pair, and with
formatted proofreading text on two pages. In each case WordPerfect saved
the checked pre-print resources in reordered compact form and cleared the
active formatting bit. The [loaded No manifest](loaded-no/expected.json)
records the exact witnesses and source files. Each packet payload remains
identical except for the active formatting bit. The earlier same-buffer
proofreading witness uses a different acquisition sequence and retains the
initial graph. Other printer-resource generations keep their existing
publication path.

An independent DOS replay also switched the retrieved plain document back to
Yes after its first No save. The next dirty save kept the reordered graph and
restored the active formatting bit. The editor regression compares both full
files and verifies that the acquired source stays byte-identical.

The [expected file manifest](expected.json) is derived from the exact original
bytes in [the regression fixtures](../../../../internal/editor/testdata/merge_result_save).
The fixture directory documents the edits. `replay.py` drives physical DOS
key chords, keeps a copy of the command line and captures the observed screens.
It stops the guest before extracting files, then compares every complete
native file with its tracked original fixture. The private WordPerfect
installation and disk files stay outside this repository.

From the repository root, use an existing pinned private reference installation:

```sh
run_dir=$(mktemp -d /tmp/wp51-merge-result.XXXXXX)
reference=docs/research/continuation/edited-merge-result-save/replay.py
python3 "$reference" "$PWD" "$run_dir/fixed" fixed
python3 "$reference" "$PWD" "$run_dir/toggle" toggle
python3 "$reference" "$PWD" "$run_dir/loaded-no" loaded-no
```

Build Wordling and run its physical terminal journeys against the same bytes:

```sh
go build -o "$run_dir/wordling" ./cmd/wordling
for scenario in yes-result-edit no-result-edit yes-result-toggle no-result-toggle; do
    python3 tests/everyday_qualification/merge_cases.py \
        "$PWD" "$run_dir/wordling" "$run_dir/$scenario" "$scenario" || exit 1
done
python3 "$reference" "$PWD" "$run_dir/product" product \
    --yes-product "$run_dir/yes-result-edit/files/YFIRST.WP5" \
    --no-product "$run_dir/no-result-edit/files/NFIRST.WP5"
```

The four terminal journeys passed. A fresh original guest reopened both
actual Wordling FIRST outputs, accepted edits and resaved them to the exact
independent original OPEN bytes. The Go editor regression verifies the fixed
and switched settings through authenticated workspace saves and actual
Retrieve. These tests qualify the recorded graph, settings and edit sequences.
