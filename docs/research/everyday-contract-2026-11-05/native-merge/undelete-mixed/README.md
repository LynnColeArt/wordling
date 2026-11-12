# Undelete across an ordinary text edit

Use the pinned WordPerfect 5.1 US DOS 03/09/92 guest with Standard Printer and Fast Save Yes. With the guest stopped, copy the original CMD51-134 `PRIMARY.WP5` into `C:\OUT\PRIM.WP`. It has SHA-256 `635a545c0bd722194f5aa8fa300e384732428ee2c39c64fbeb99c6e32cc2ccb4`.

1. Retrieve the primary with Shift+F10 and open Reveal Codes with Alt+F3.
2. Starting at the beginning, move right six times and press Delete. The lower pane shows `Hello 1~[HPg]`.
3. Type `X`. The lower pane shows `Hello X1~[HPg]`.
4. Press F1. The lower pane previews `Hello X[Block][Mrg:FIELD]1~[HPg]` and the status offers Restore and Previous Deletion.
5. Press 1. The lower pane shows `Hello X[Mrg:FIELD]1~[HPg]` at the current gap after `X`.
6. Press F10 and save to `C:\OUT\REST.WP`. Stop the guest before extracting the file.

The original [REST.WP](REST.WP) is 614 bytes, with body offset 564 and SHA-256 `a0cba248fb8e49c1f3bd9a38dd4eacc55178c3d8440a855727b6d073f6b0efc9`.

For the alternate restore location, omit step 3 and press Home, Home, Up
after deleting the owner. Press F1 and 1. The original restores the
recognized FIELD frame at the start, giving `[Mrg:FIELD]Hello 1~[HPg]`
with the caret on the `H`. The original [RESTGAP.WP](RESTGAP.WP) is
613 bytes, with body offset 564 and SHA-256
`313f17007256059057f35801f8898a17f7a65aad5eea054e355a130a98083194`.
The nonnumeric operand is preserved as document bytes.

Run the Linux replay against a built Wordling executable, using a fresh
output directory for each invocation.

```sh
python3 tests/everyday_qualification/merge_undelete_interleaving.py "$PWD" "$binary" "$run_dir/type"
python3 tests/everyday_qualification/merge_undelete_interleaving.py "$PWD" "$binary" "$run_dir/move" --move
```

Each replay checks the active Reveal cell, compares the entire original save,
and verifies that the acquired primary stayed byte-identical.
