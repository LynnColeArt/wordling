# Paragraph justification

Format → Line → Justification changes the paragraph's justification.
The D0 subfunction 6 owner stores its prior and new mode. The Left and
Full paragraphs in the original wrap at the same place. The Standard
Printer only pads the Full paragraph's interword gap. Linux matches the
native body and print stream. [Native save](JUSTIFY.WP) · [Printer output](JUSTIFY.PRN)

Paragraph Center and Right also write a D4 subfunction 5 position record
for each affected line. Linux updates those records as text changes and
matches the native save with all four modes. [Native save](CENTER.WP)

Run the replay scripts from the repository root with `PYTHONPATH=scripts/reference`.
