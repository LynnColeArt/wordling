# Author and edit a two-page secondary

The reference is WordPerfect 5.1 US DOS dated March 9, 1992 with Standard Printer. Type A1 through A60 and press F9 after each value. At field 54 the native separator changes to D4 followed by `8C`, and the next field remains 55. Press Shift+F9 and 2 to close the record. Repeat for B1 through B60. The original [SECOND.WP5](SECOND.WP5) is 1896 bytes.

Retrieve the saved file and use Fast Save No. Insert `X` before A1. Find A55 with F2, type `Y` after it, and save as [EDITED.WP5](EDITED.WP5). The editing run retains both automatic page boundaries and both original record counts. The exact source and edited saves produced by Wordling match their DOS counterparts. Delete and Undelete of End Field before the page break are also covered by a document regression that checks the count on the next page and verifies the restored bytes.

In fresh DOS guests, retrieve Wordling's newly authored file and the edited file. For each, search through to page 2, close the document, and run Ctrl+F9 against the same file. The edited journey uses [EDITPRI.WP5](EDITPRI.WP5), which changes field 52 to 55 in the original test primary. The DOS results match [MERGED.WP5](MERGED.WP5) and [EDITMERG.WP5](EDITMERG.WP5) byte for byte. Wordling's terminal journey also merges its edited file against the exact DOS result.

```sh
run_dir=$(mktemp -d /tmp/wordling-secondary.XXXXXX)
evidence=docs/research/everyday-contract-2026-11-05/native-merge/wide/60
go build -o "$run_dir/wordling" ./cmd/wordling
python3 tests/everyday_qualification/merge_authoring.py "$PWD" "$run_dir/wordling" "$run_dir/product" --multipage
python3 "$evidence/reopen.py" "$PWD" "$run_dir/new-dos" "$run_dir/product/files/NEW.WP5" --untouched
cmp "$run_dir/new-dos/MERGED.WP5" "$evidence/MERGED.WP5"
python3 "$evidence/reopen.py" "$PWD" "$run_dir/edit-dos" "$run_dir/product/files/EDITED.WP5"
cmp "$run_dir/edit-dos/MERGED.WP5" "$evidence/EDITMERG.WP5"
```

This replay uses explicit one-line fields and one automatic break per record. The extended replays cover field wrapping and additional physical pages. [Extended round trips](../extended.md)
