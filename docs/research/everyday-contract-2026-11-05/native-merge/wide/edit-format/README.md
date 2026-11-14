# Editing attributes inside a saved secondary file

These fixtures came from WordPerfect 5.1 US DOS (March 9, 1992), using Standard Printer. All edits are inside field 54, whose text crosses an automatic page break. The edited secondary files were saved with Fast Save No. The corresponding merge outputs use Fast Save Yes.

| Fixture | Source | DOS editing keys |
| --- | --- | --- |
| BOLD | [Plain wrapped secondary](../55/SECOND.WP5) | Find `A alpha` with F2, press Alt+F4, move Right 72 times, and press F6. |
| UNDER | Same plain secondary | Repeat the selection and press F8. |
| NO-BOLD | BOLD.WP5 | Find `A alpha`, open Reveal Codes with Alt+F3, and press Delete at the Bold opening code. |
| NO-UND | [Secondary with overlapping Bold and Underline](../overlap-page/SECOND.WP5) | Find `BoldStart `, open Reveal Codes, and press Delete at the Underline opening code. Bold remains. |

Each edit changes the attribute owners and leaves the underlying text, page records, and field delimiters intact. Each `-M.WP5` file is the result of merging the edited secondary with [PRIMARY.WP5](../overlap-page/PRIMARY.WP5) in DOS.

Run the Wordling terminal replay and feed its actual edited output back to DOS for each case.

```sh
run_dir=$(mktemp -d /tmp/wordling-edit-format.XXXXXX)
wide=docs/research/everyday-contract-2026-11-05/native-merge/wide
go build -o "$run_dir/wordling" ./cmd/wordling
for case in BOLD UNDER NO-BOLD NO-UND; do
  python3 tests/everyday_qualification/merge_format_edit.py "$PWD" "$run_dir/wordling" "$run_dir/$case" "$case"
  python3 "$wide/reopen_extended.py" "$PWD" "$run_dir/$case-dos" \
    "$wide/overlap-page/PRIMARY.WP5" "$run_dir/$case/files/EDITED.WP5" --merge-cue '55='
  cmp "$run_dir/$case-dos/MERGED.WP5" "$wide/edit-format/$case-M.WP5"
done
```
