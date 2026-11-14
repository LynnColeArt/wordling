# Bold and Underline in secondary merge fields

WordPerfect 5.1 US DOS (March 9, 1992, Standard Printer) was the reference. For each prefix A and B, the secondary has three fields: a Bold value of the prefix, a space, four repetitions of `alpha beta gamma delta `, and `end`; the underlined value `Aunderlined` or `Bunderlined`; and the plain value `Atail` or `Btail`. In DOS, F6 toggles Bold, F8 toggles Underline, F9 ends the field, and Shift+F9 then 2 ends the record. The primary puts each field on its own line between brackets, labeled `1=`, `2=`, and `3=`.

The secondary stores native three-byte Bold and Underline owners. They occupy no columns. A soft return can appear between the on and off owners of a field. The merge carries those owners into the result, discards the source wrap, and wraps again in the primary. In the edited witness, F2 searches for `A alpha` and four characters are inserted at the end of the match, inside the Bold span. Fast Save No is used for the secondary, and Fast Save Yes for the result.

The fixture files are DOS outputs: [original secondary](SECOND.WP5), [edited secondary](EDITED.WP5), [primary](PRIMARY.WP5), [original merge result](MERGED.WP5), and [edited merge result](EDITMERG.WP5). The Linux terminal replay compares both Wordling secondary saves and its edited merge result with the corresponding complete DOS files. The two DOS replays then use Retrieve and Ctrl+F9 on the actual Wordling saves and compare their outputs with the original baselines.

```sh
run_dir=$(mktemp -d /tmp/wordling-formatted-fields.XXXXXX)
wide=docs/research/everyday-contract-2026-11-05/native-merge/wide
go build -o "$run_dir/wordling" ./cmd/wordling
python3 tests/everyday_qualification/merge_authoring.py "$PWD" "$run_dir/wordling" "$run_dir/product" --extended formatted
for kind in NEW EDITED; do
  python3 "$wide/reopen_extended.py" "$PWD" "$run_dir/$kind-dos" \
    "$wide/formatted/PRIMARY.WP5" "$run_dir/product/files/$kind.WP5"
done
cmp "$run_dir/NEW-dos/MERGED.WP5" "$wide/formatted/MERGED.WP5"
cmp "$run_dir/EDITED-dos/MERGED.WP5" "$wide/formatted/EDITMERG.WP5"
```

This covers balanced Bold and Underline within explicit fields, including normal word wrap and text edits inside a formatted value.
