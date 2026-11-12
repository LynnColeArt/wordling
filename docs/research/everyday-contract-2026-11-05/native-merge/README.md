# Native merge and Save

The reference is WordPerfect 5.1 US DOS, 03/09/92, with Standard Printer. The input pair is the original [CMD51-134 capture](../../reference-runs/2026-10-29-extended-04/CMD51-134). The source-edit witness inserts `X` before the primary's `Hello` and `Z` before the secondary's first value, `Alice`. Reveal Codes and body comparisons preserve the original FIELD, END FIELD, END RECORD, return, and page owners.

Ctrl+F9 → 1 opens the Primary file prompt and then the Secondary file prompt. F1 cancels either prompt. F5 opens List Files in either prompt. Selecting a row with 1 advances from primary to secondary or runs the merge after secondary. In the original, merging at `BEFORE|AFTER` leaves `BEFORE` adjacent to the first substituted text and keeps `AFTER` after the last hard page, with the caret before `AFTER`. The primary's explicit hard page follows each record. Default PAGE ON supplies a separate hard page between records. The intervening blank page and three printed separators are visible in the original.

| Destination | Fast Save Yes | Fast Save No |
| --- | --- | --- |
| Blank, original compact primary | 564-byte prefix, middle index at 270, live format bit clear | 324-byte reordered prefix, format bit clear |
| Blank after editing both sources | 564-byte prefix, middle index at 272, live format bit clear | 324-byte reordered prefix, format bit clear |
| Occupied New | 324-byte receiver order, format bit set for mid-document insertion and clear at EOF | 324-byte receiver order, format bit clear |
| Occupied, loaded compact receiver | 564-byte receiver generation, live format bit set for mid-document insertion and clear at EOF | 324-byte reordered prefix, format bit clear |

The physical Linux terminal replay tests compare complete saved images to SHA-256 digests captured from the DOS exports. They exercise the two edited source files, type-in and F5 roles, missing primary and cancellation, blank and occupied destinations, and result reopening. The `yes` and `no` product sources and results were also retrieved in separate copies of the original DOS guest. Running the original Merge with the product sources reproduced each product result byte for byte.

```sh
go build -o /tmp/wordling-merge ./cmd/wordling
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-yes yes
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-no no
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-occupied yes-occupied
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-loaded-yes yes-loaded
python3 tests/everyday_qualification/merge_cases.py "$PWD" /tmp/wordling-merge /tmp/merge-loaded-no no-loaded
```

The editor compares complete outputs for the original CMD51-207 and CMD51-209 cases. Additional Ctrl+F9 terminal tests cover PAGE OFF and PAGE ON restoration in CMD51-208 and CMD51-216/217, nested primary return and page state in CMD51-223–225 and CMD51-236, and nested secondary replacement and page state in CMD51-233–235. The automatic separator takes the state left by the preceding copy. A nested file's PAGE setting persists after return.

Nested reads stay inside the configured workspace. A bare DOS name resolves relative to the workspace directory active when Merge starts, corresponding to the original working directory. A native DOS name without a suffix names that exact file. The research capture adds `.WP5` to export filenames, so the test copies the child back under its extensionless guest filename. An absent nested file stops the merge and retains the already emitted text. The original can leave the next primary's literal prefix before the failed FIELD read in a missing secondary. Wordling reports the missing filename while preserving the checked partial output. Malformed, stale, and recursive sources leave the receiving document unchanged.

```sh
for case in 208 216 217 223 224 225 233 234 235 236 missing-primary missing-secondary relative ordinals field3 literal-tilde loaded-eof; do
  python3 tests/everyday_qualification/merge_nested_cases.py "$PWD" /tmp/wordling-merge "/tmp/merge-case-$case" "$case"
done
```

The [fresh original replays](fresh/README.md) qualify relative and missing files, ordinal reads, literal tildes, and the initial occupied EOF save state. The [wider merge replays](wide/README.md) cover up to 53 explicit one-line fields, decimal operands, literal-only primaries, and wrapper-only primaries. The execution scope also includes ELSE/END IF, PAGE ON/OFF, nested primary and secondary, and file-level primary BREAK. Wordling bounds a source at 32 explicit secondary records, nesting at 16 levels per role, and a run at 64 nested references, with independent work and output limits. Other merge instructions, additional record layouts, Sort, and Convert Old Merge Codes remain open. [Authoring replay](authoring.md) and [earlier independent increment review](increment-review.md)
