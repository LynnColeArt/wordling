# Inserting a subdocument link: DOS observations

Alt+F5, Subdoc (2), and Enter inserts a condensed link at the cursor.
DOS normalizes the filename to uppercase. It displays the name in a
comment box and as a `[Subdoc:NAME]` code in Reveal Codes. Inserting the
link adds no page break, and Standard Printer omits it entirely.

Wordling matches the native bodies for an inline link to a missing file
([MASTER.WP](MASTER.WP)) and a link at the start of a document
([BEGIN.WP](BEGIN.WP)). The inline [printer stream](MASTER.PRN) also
matches. Master document expansion and condensation remain open.

[Prompt](link-prompt.txt) · [Box](linked.txt) · [Reveal Codes](reveal.txt)

Run the replay scripts with `PYTHONPATH=scripts/reference` from the repository root.
