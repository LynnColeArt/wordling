# Wrapped and longer secondary records

Reference files come from WordPerfect 5.1 US DOS dated March 9, 1992 with Standard Printer. The [wrapped record](wrapped/SECOND.WP5) uses a value that wraps at a space and a long unbroken value. DOS writes `0D` for the space and `90` for the break inside a word. The [55-field record](55/SECOND.WP5) wraps field 54 across a physical page. The soft page separator preserves the logical space. Ctrl+F9 reflows the substituted values in the primary document.

The [110-field record](110/SECOND.WP5) crosses two automatic page breaks. The values A1, A54, A55, A108, A109, and A110 identify the tested positions. The other fields are empty. The [164-field record](164/SECOND.WP5) crosses three automatic breaks, and its original merge checks values on the fourth page. The [101-field record](101/SECOND.WP5) supplies another original two-page control.

The terminal replay authors the wrapped and 110-field sources with F9 and Shift+F9, compares the complete saved files, then reopens each and inserts `XXXX` before the first value. Fast Save No uses the original compact save layout for the edited file. Both edited files match DOS saves, including the adjusted wrap in the first case. The replay then merges the edited file and compares the entire result. Separate DOS replays Retrieve the actual Wordling files and merge each using the same primary.

```sh
run_dir=$(mktemp -d /tmp/wordling-extended-secondary.XXXXXX)
evidence=docs/research/everyday-contract-2026-11-05/native-merge/wide
go build -o "$run_dir/wordling" ./cmd/wordling
for case in wrapped 110; do
  python3 tests/everyday_qualification/merge_authoring.py "$PWD" "$run_dir/wordling" "$run_dir/$case" --extended "$case"
  for kind in NEW EDITED; do
    python3 "$evidence/reopen_extended.py" "$PWD" "$run_dir/$case-$kind-dos" "$evidence/$case/PRIMARY.WP5" "$run_dir/$case/files/$kind.WP5"
  done
  cmp "$run_dir/$case-NEW-dos/MERGED.WP5" "$evidence/$case/MERGED.WP5"
  cmp "$run_dir/$case-EDITED-dos/MERGED.WP5" "$evidence/$case/EDITMERG.WP5"
done
```

Use `--find A110` on either DOS replay to navigate to the last value before closing the source. To reproduce an edited oracle inside DOS, point the replay at the original `SECOND.WP5` and use `--edit`. The checked scope is plain printable fields in the Standard Printer layout and existing document-size bounds.
