# Overlapping attributes across a merge page break

The reference is WordPerfect 5.1 US DOS (March 9, 1992), using Standard Printer. The secondary starts with 53 empty fields. Field 54 contains:

| Text | Active attributes |
| --- | --- |
| `BoldStart ` | Bold |
| Four repetitions of `A alpha beta gamma delta ` | Bold and Underline |
| `UnderTail` | Underline |
| ` PlainEnd` | None |

The original keys are F6, type the Bold opening, F8, type the overlap, F6, type the underlined tail, F8, and type the plain ending. End the field with F9, type `ATail` as field 55, press F9, then press Shift+F9 and 2 to end the record. The automatic page break inside field 54 is a native D4 page record plus a space-consuming soft-page owner (`0B`). The four attribute owners stay in order, with no extra attribute owners at the page boundary. The edited reference inserts `XXXX` after the first `A alpha`, inside the overlap. Both secondary saves use Fast Save No.

[PRIMARY.WP5](PRIMARY.WP5) merges fields 54 and 55. [DESTPRI.WP5](DESTPRI.WP5) prepends 53 hard returns before the field 54 line and omits field 55, so the overlap also crosses a page break in the result. All result fixtures were saved in DOS with Fast Save Yes.

The Wordling terminal replays compare the complete authored and edited sources and merged results with DOS. They also check the color roles for Bold only, both attributes on both sides of the destination page divider, Underline only, and plain text. The corresponding DOS VGA attributes are `1F`, `7F`, `71`, and `17`; `7F` was observed on both sides of the page divider. The DOS replays Retrieve the actual Wordling files and compare complete merge outputs, including all formatting owners and page caches.

```sh
run_dir=$(mktemp -d /tmp/wordling-overlap-page.XXXXXX)
wide=docs/research/everyday-contract-2026-11-05/native-merge/wide
fixtures=$wide/overlap-page
go build -o "$run_dir/wordling" ./cmd/wordling
python3 tests/everyday_qualification/merge_authoring.py "$PWD" "$run_dir/wordling" "$run_dir/product" --extended overlap-page
python3 tests/everyday_qualification/merge_wide_cases.py "$PWD" "$run_dir/wordling" "$run_dir/destination" overlap-destination
for kind in NEW EDITED; do
  python3 "$wide/reopen_extended.py" "$PWD" "$run_dir/$kind-dos" \
    "$fixtures/PRIMARY.WP5" "$run_dir/product/files/$kind.WP5" --merge-cue '55=[ATail]'
done
python3 "$wide/reopen_extended.py" "$PWD" "$run_dir/dest-dos" \
  "$fixtures/DESTPRI.WP5" "$run_dir/product/files/NEW.WP5" --merge-cue 'PlainEnd]'
cmp "$run_dir/NEW-dos/MERGED.WP5" "$fixtures/MERGED.WP5"
cmp "$run_dir/EDITED-dos/MERGED.WP5" "$fixtures/EDITMERG.WP5"
cmp "$run_dir/dest-dos/MERGED.WP5" "$fixtures/DESTMERG.WP5"
```
