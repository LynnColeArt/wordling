# Inserting a language code: DOS observations

In an ordinary US document, Shift+F8, Other (4), Language (4)
opens the current language entry. Typing UK and pressing Enter
inserts D3/11 at the cursor with old code US and new code UK.
F7 returns to editing. The code is invisible in the ordinary
pane and appears as `[Lang:UK]` in Reveal Codes.

Wordling matches the native [LANGUAGE.WP](LANGUAGE.WP) body and
[Reveal Codes](reveal.txt). Language-specific dictionaries, formatting
resources, and global Initial Codes remain open. This profile's
proofreader uses the US resource and refuses to check documents
that request another dictionary.

Run `replay.py` from the repository root with `PYTHONPATH=scripts/reference`.
