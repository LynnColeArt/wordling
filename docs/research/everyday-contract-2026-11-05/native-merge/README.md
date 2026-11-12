# Native merge and Save

The reference is WordPerfect 5.1 US DOS, 03/09/92, with Standard Printer. The input pair is the original [CMD51-134 capture](../../reference-runs/2026-10-29-extended-04/CMD51-134). The source-edit witness inserts `X` before the primary's `Hello` and `Z` before the secondary's first value, `Alice`. Reveal Codes and body comparisons preserve the original FIELD, END FIELD, END RECORD, return, and page owners.

Ctrl+F9 → 1 opens the Primary file prompt and then the Secondary file prompt. F1 cancels either prompt. F5 opens List Files in either prompt. Selecting a row with 1 advances from primary to secondary or runs the merge after secondary. In the original, merging at `BEFORE|AFTER` leaves `BEFORE` adjacent to the first substituted text and keeps `AFTER` after the last hard page, with the caret before `AFTER`. The primary's explicit hard page follows each record. Default PAGE ON supplies a separate hard page between records. The intervening blank page and three printed separators are visible in the original.

| Destination | Fast Save Yes | Fast Save No |
| --- | --- | --- |
| Blank, original compact primary | 564-byte prefix, middle index at 270, live format bit clear | 324-byte reordered prefix, format bit clear |
| Blank after editing both sources | 564-byte prefix, middle index at 272, live format bit clear | 324-byte reordered prefix, format bit clear |
| Occupied New | 324-byte receiver order, format bit set | 324-byte receiver order, format bit clear |
| Occupied, loaded compact receiver | 564-byte receiver generation, live format bit set | 324-byte reordered prefix, format bit clear |

The physical Linux terminal replay tests compare complete saved images to SHA-256 digests captured from the DOS exports. They exercise the two edited source files, type-in and F5 roles, missing primary and cancellation, blank and occupied destinations, and result reopening. The `yes` and `no` product sources and results were also retrieved in separate copies of the original DOS guest. Running the original Merge with the product sources reproduced each product result byte for byte.

```sh
go build -o /tmp/wordling-merge ./cmd/wordling
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-yes yes
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-no no
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-occupied yes-occupied
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-loaded-yes yes-loaded
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-loaded-no no-loaded
```

The executable primary forms are FIELD 1 with a terminal hard return or qualified hard page, and the previously qualified IFBLANK 2 conditional. The editor tests compare complete outputs for the original CMD51-207 and CMD51-209 cases. Secondary acquisition admits the reviewed explicit DATA records. Editing is printable insertion inside a qualified source literal while preserving every nontext owner. Further native merge commands, structural source edits, Sort, Convert Old Merge Codes, and save behavior after subsequent changes to a merged result still require qualification.
