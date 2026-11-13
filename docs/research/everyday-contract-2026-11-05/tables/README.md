# Original 2 by 2 table

In WordPerfect 5.1 US DOS, press Alt+F7, 2 for Tables, and 1 for Create at the start of a blank document. Enter 2 columns and 2 rows. Press F7 to leave Table Edit, then type ALPHA, BETA, GAMMA, and DELTA in successive cells using Tab to advance. Save with F10. This is the source for CMD51-120.

The 577-byte file has a 324-byte prefix. Its table begins with a D2 subtype 0B owner, followed by DC subtype 01 row owners and DC subtype 00 cell owners. The final DC subtype 02 owner follows the last cell. The row and cell owners include layout values, so changing cell text requires an editing and layout contract beyond identifying the framing.

The Wordling terminal test retrieved the original file and reproduced all bytes on both an unchanged F10 save and Save As. This fixture establishes preservation. Table rendering, cell editing, and original reopen after a cell edit remain to be verified.
