# Wider data and nested wrapper replays

The original is WordPerfect 5.1 US DOS 03/09/92 in the Standard Printer reference guest. Start a fresh guest for each case and verify the date with F3. Put the supplied PRIMARY.WP5 and the secondary specified below in C:\OUT. In Ctrl+F9 choose 1 Merge, enter those two files by absolute name, and save the result as C:\OUT\MERGED.WP5 with F10. The tracked MERGED.WP5 files are exports from the guest.

| Cases | Secondary and preparation |
| --- | --- |
| 3, 12, 32, 53 | Use each directory's SECOND.WP5. The original authored two records. For the first, type A1 through An, pressing F9 after every value, then Shift+F9 → 2 End Record. Repeat with B1 through Bn. |
| bounds, ifmissingone, ifzero, literal, literal-page | Use [CMD51-223 SECOND.WP5](../../../reference-runs/2026-10-29-iteration-01/CMD51-223/SECOND.WP5). |
| bounds2, ifmissingwide, ifpresent, direct2, missingend, missingliteral, presentend, field2tail | Use the three-field SECOND.WP5 from this directory. |
| nestedmissing | Use the case's SECOND.WP5 and copy [CMD51-234 CHILD.WP5](../../../reference-runs/2026-10-30-values-01/CMD51-234/CHILD.WP5) as C:\OUT\CHILD. The root records contain three fields. The first child record lacks the tested second field. DOS emits Carol's missing branch, skips Dave, resumes the parent with B1 and retains the child's PAGE OFF. |
| wrapper1, wrapper, wrapper3, wrapperlead | Use CMD51-223 SECOND.WP5. Copy its CHILD.WP5 to C:\OUT\CHILD. Copy WRAP.WP5 under the name WRAP if the primary needs it, using wrapper's WRAP for wrapperlead. Copy MID.WP5 under the name MID for wrapper3. |
| wrapper-literal | Use CMD51-223 SECOND.WP5. Copy the provided WRAP.WP5 as C:\OUT\WRAP and CHILD.WP5 as C:\OUT\SUB\CHILD. |
| wrapperflags | Use the wrapper chain, taking PRIMARY.WP5 and CHILD.WP5 from wrapperflags. The primary and leaf have the source format bit set; the intermediate file has it clear. |
| wrapperno, wrapperocc, reorderedno, reorderedocc | Use the wrapper chain. The reordered cases use reorderedno's CHILD.WP5 under the name CHILD. For No choose Shift+F1 → 3 → 5 → No. For occupied, type BEFOREAFTER and move five characters left before merging. |
| reopen-yes, reopen-no | In a fresh guest use Shift+F10 to retrieve the wrapper case's MERGED.WP5. Type X before CAlice and use F10 to save EDITED.WP5 under the named setting. |
| wrapper/EDITED.WP5 | After the original wrapper merge and first F10, stay in the same session. Use Home, Home, Up, type X, and save with F10 under another name with Fast Save Yes. |

The wider data records have one hard return per explicit END FIELD, an END RECORD count one larger than the number of fields, and a Standard Printer page owner whose row matches the field count. The 53-field case reaches row 53 without an internal soft page. The 53-field ceiling is the scope of this checked single-page record form.

DOS accepts decimal field operands with leading zeros and wraps the accumulated value at 16 bits. Zero aliases field 1, including 65536 after wrapping. Out-of-record FIELD yields empty text and continues. A missing IF BLANK takes its true branch. If the copy finishes without another present field access, DOS ends iteration. The bounds cases capture wrapped FIELD 2, wrapped IF BLANK, missing conditions with and without a later FIELD, and ordinals outside the data record.

An ASCII primary repeats its literal text per record. A wrapper may contain only NEST PRIMARY and page commands. The first leading nested primary entered in a blank result adds a 256-byte retired resource generation with Fast Save Yes. The measured one-, two-, and three-link chains yield 820, 1076, and 1332-byte prefixes. Text emitted before nesting leaves the 564-byte graph. Fast Save No and occupied New retain the appropriate 324-byte graph. The archived packet state follows each source, including the mixed bits in wrapperflags. Reopening a checked archived result preserves an untouched image on Save As and saves subsequent edits in the original 564-byte Yes or 324-byte No graph. In the originating session, editing retains the archive and marks the live formatting bit.

The archive writer qualifies compact original-order Standard Printer sources with matching live resources. A reordered child still works when the result uses Fast Save No or an occupied receiver, where that archive is absent. A blank Yes result needing a different archive shape remains outside this qualification.

For the independent numeric authoring witness, start a New document in DOS. Press Shift+F9, 1, type the operand, and press Enter for each of `0`, `001`, `1000`, `32767`, `65535`, and `65536` consecutively. Save with F10 under the default Yes setting. The original [DIGITS.WP](DIGITS.WP) is 401 bytes, with SHA-256 `f0809fae0fc7b9c03b02740781ab87a6b0830ab649065c3210f02b56f764128a`.

The Wordling authoring replay uses a fresh 80×25 terminal and compares the entire 53-field data file, numeric authoring file, wrapper primary, and 820-byte-index wrapper output with the original exports.

```sh
python3 tests/everyday_qualification/merge_authoring.py "$PWD" "$binary" "$run_dir/authoring"
python3 tests/everyday_qualification/merge_wide_cases.py "$PWD" "$binary" "$run_dir/wrapper" wrapper
```
