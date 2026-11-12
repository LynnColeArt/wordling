# Original WordPerfect 5.1 DOS Fast Save Yes files

The user-authored text was saved in private copies of the pinned March 9,
1992 US reference with the Standard Printer and Fast Save Yes. The source
disks were stopped before extracting any files. No original program or
printer files are included.

- FIRST: New document typed `Alpha`, then saved.
- SECOND: same New document edited to `Alpha beta`, then saved under a
  different name. A separate same-name replace produced the same bytes.
- THIRD: retrieved SECOND into an empty Doc 2, appended ` gamma`, and saved.
- FOURTH: appended ` delta` in the same loaded Doc 2, then saved again.
- REOPEN: fresh original guest retrieved THIRD, appended ` ONEDIT`, and saved.
- REORDER: fresh original guest retrieved the existing original compact
  `internal/tui/evidence/everyday/FLOW.WP`, appended ` ONEDIT`, and saved.

FIRST and SECOND have body offset 324 with the original initial packet
order. THIRD and FOURTH have body offset 564 and a middle index at 270.
REOPEN and REORDER have body offset 564 and a middle index at 272.

SHA-256 (in order FIRST, SECOND, THIRD, FOURTH, REOPEN, REORDER):

```text
6df0eaf73a5934d77a615fb6d1df25f9c300f4e59db3576ba294abafcd67e717
dee441c26ae3c1ec6718b98ba8dc6b2af7bd0fb6725207f62b968730982fc969
54d433ba7faf8c01c95c0b6999036f506b781653fd57dc73f892d0274c6fc781
4748dd61ee27105ac51c4ad868423cba9d19db9a2bcca5cba3e1922e4b9f875f
5cf2b3876e6efbdd9b9d4fbdf12493c7b4acd2d4824ca8add0e3c637c5e0242a
46a925a0e3fe5ca14399cf0414f90fc44b4ffd7854db36722425ad21ac5830fc
```
