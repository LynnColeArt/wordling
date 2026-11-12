# WordPerfect 5.1 DOS edited merge result saves

Captured from the pinned US March 9, 1992 DOS release, using a private guest
with the Standard Printer. The source files are `PRIMARY.WP5` and `SECOND.WP5`
from `docs/research/reference-runs/2026-10-29-extended-04/CMD51-134`.

`Y` and `N` indicate Fast Save Yes and No. For each setting:

- `FIRST` starts a merge in an empty document, goes to document start with
  Home Home Up, inserts `EDIT `, and saves with F10.
- `AGAIN` adds `MORE ` after `EDIT ` in the same buffer and saves again.
- `OPEN` closes the buffer, retrieves `FIRST`, inserts `OPEN ` at the start,
  and saves under a fresh name.
- `NEXT` adds `NEXT ` after `OPEN ` in that retrieved buffer and saves again.

The Yes files use body offset 564. The middle index starts at byte 270 on
`FIRST` and `AGAIN`, and byte 272 on `OPEN` and `NEXT`. The active formatting
state is 8. The No files use body offset 324 and clear the formatting state.

These documents were extracted after the guest stopped. They contain
fixture content and native metadata only.

A second pinned replay captures Fast Save setting changes after `FIRST`.
`NOTHER` switches from No to Yes before inserting `OTHER ` after `EDIT `.
`YOTHER` switches from Yes to No for the same edit, and `YBACK` switches
back to Yes before inserting `BACK ` at the same location. All three files
retain the reordered offset-324 graph. The Yes saves set the active
formatting bit. The No save clears it.
