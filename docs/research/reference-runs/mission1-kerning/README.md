# Kerning control: DOS observations

Shift+F8, Other (4), Printer Functions (6), Kerning (1), Yes
inserts a native D9/03 record at the cursor. Reveal Codes
shows `AV [Kern:On]AV`; ordinary editing still shows `AV AV`.

Wordling matches the [native body](KERN.WP) and the
[Standard Printer output](KERN.PRN) for the pinned fixed-pitch
profile. Proportional font kerning and its printer resources
remain open. [Prompt](kerning.txt) · [Reveal Codes](reveal.txt)

Run the scripts with `PYTHONPATH=scripts/reference` from the
repository root.
