# Binding offset

Shift+F7, B sets binding offset in the document state packet. At 0.25
inches, WordPerfect stores 300 units. The native body is identical to the
zero-offset save. The Standard Printer shifts the odd page three cells
right and the even page two cells left. Linux matches the native field,
the reset to zero, and the printer bytes for the two-page fixture.
[Prompt](binding-set.txt) · [Native save](BIND.WP) · [Zero offset](ZERO.WP) ·
[Printer output](BIND.PRN)

Run the replays from the repository root with `PYTHONPATH=scripts/reference`.
