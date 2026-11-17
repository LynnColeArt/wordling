# Date Text and Date Code

The pinned March 9, 1992 DOS guest inserts `March 9, 1992` as ordinary
text from Shift+F5, Date Text (1). Wordling uses the corresponding
default US format and saves those same literal text owners. The Linux
test controls the clock when typing the date and verifies the saved
document on retrieval under a different date.

The same DOS guest saves Date Code (2) as a D8 owner carrying the format
`3 1, 4`. Wordling writes the same owner and renders it using the
current date. On March 10, both DOS and Wordling reopen the same file
with its literal date unchanged and the Date Code updated. Custom
formats remain open.
[Reopened one day later](reopened-next-day.txt)

[Menu](menu.txt) · [Reveal Codes](reveal.txt) · [Literal save](LITERAL.WP) ·
[Literal and dynamic save](DATES.WP) · [Printer capture](DATES.PRN) ·
[DOS text export](DATES.TXT)

Run `replay.py` from the repository root with `PYTHONPATH=scripts/reference`.
Pass `literal` for the literal-only capture.
