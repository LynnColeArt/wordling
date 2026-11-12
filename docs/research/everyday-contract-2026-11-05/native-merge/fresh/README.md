# Fresh March 1992 DOS merge replays

These files are native inputs and saves from the offline Standard Printer reference guest. Start a fresh copy of the reference environment for each row. F3 identifies the US DOS release as 03/09/92. In Shift+F1 Setup, choose Environment (3) and leave Fast Save (5) at Yes. The missing-primary, missing-secondary, and relative cases also produce the same bytes with Fast Save No.

Copy the inputs into the guest under the names specified below. In the editor press Ctrl+F9, choose 1 Merge, and enter `C:\OUT\PRIMARY.WP5` and `C:\OUT\SECOND.WP5`. Save the result with F10 as `C:\OUT\MERGED.WP5`, exit, and compare the exported file with the tracked result for the case.

| Case | Guest inputs and preparation | Result |
| --- | --- | --- |
| missing-primary | Copy PRIMARY.WP5 and SECOND.WP5 from [CMD51-223](../../../reference-runs/2026-10-29-iteration-01/CMD51-223) into OUT. Leave OUT without a file named CHILD. Type `KEPT` in the new receiver and merge at EOF. | The checked output is `KEPTPAlice` and a hard return. |
| missing-secondary | Copy PRIMARY.WP5 and SECOND.WP5 from [CMD51-234](../../../reference-runs/2026-10-30-values-01/CMD51-234) into OUT. Leave OUT without a file named CHILD. Type `KEPT` and merge at EOF. | `KEPTHello Alice`, a hard return and hard page, then `Hello ` with no final hard return. |
| relative | Copy this directory's PRIMARY.WP5 and CMD51-223's SECOND.WP5 into OUT. Copy CMD51-223's CHILD.WP5 as `C:\WP51\CHILD`. F5 confirms the initial document directory is C:\WP51. Type `KEPT` and merge at EOF. | Both child calls succeed. Placing CHILD only in C:\ or C:\OUT leaves the same partial output as missing-primary. Placing only CHILD.WP5 in C:\WP51 also leaves that partial output. |
| ordinals | Copy this directory's PRIMARY.WP5 and SECOND.WP5 into OUT. Merge into an empty receiver. | IF BLANK 1 chooses the correct branch for each record and FIELD 2 produces Alice and Bob. |
| field3 | Copy this directory's PRIMARY.WP5 and the ordinals SECOND.WP5 into OUT. Merge into an empty receiver. | The missing FIELD 3 produces empty text in both copies. |
| literal-tilde | Copy this directory's PRIMARY.WP5 and the ordinals SECOND.WP5 into OUT. Merge into an empty receiver. | The literal suffix `1~` survives each copy. |
| loaded-eof | Copy PRIMARY.WP5 and SECOND.WP5 from [CMD51-134](../../../reference-runs/2026-10-29-extended-04/CMD51-134) into OUT. Copy [the original Alpha beta receiver](../../../../../internal/document/testdata/fast_save_yes/SECOND.WP) as `C:\OUT\RECEIVER.WP5`. Retrieve it with Shift+F10 and go to EOF with Home, Home, Down before merging. | The 564-byte prefix retains the loaded receiver generation and clears its live unformatted bit. |

The ordinal primary and secondary use the same native owners as CMD51-209, with the explicit field values exchanged and operand digits adjusted. The literal-tilde variant adds the ASCII text left by deleting a FIELD owner. The relative primary uses the native CMD51-223 command owner with a bare DOS filename operand. In each case WordPerfect itself read the inputs, performed the merge, and wrote the tracked result.
