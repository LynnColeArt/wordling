"""Compare Alt+F2 Compose replacement with the original DOS native result."""
from pathlib import Path
import sys

from qualification import F1, F2, F6, F8, REF, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
run = Run(repo, binary, output, classic_canvas=True)
reference = repo / REF / "replace-compose-dos/exports/REPLACE.WP"


def compose(pair, glyph):
    run.step(b"\x16", "start Compose", "Key =")
    run.step(pair, "compose character", glyph)


def replace(confirm):
    run.step(b"\x1b[1;3Q", "open Alt+F2 Replace", "w/Confirm?")
    run.step(confirm, "set confirmation", "Srch:")
    compose("AE", "Srch: Æ")
    run.step(F2, "continue to replacement", "Replace with:")
    compose("'e", "Replace with: é")
    run.step(F2, "execute replacement")


try:
    run.launch()
    run.step(F6, "start Bold")
    run.step(F8, "start Underline")
    compose("AE", "Æ")
    run.step(" A ", "type intervening text")
    compose("AE", "Æ A Æ")
    run.step(F8, "end Underline")
    run.step(F6, "end Bold")
    run.start_of_document()
    replace("y")
    run.step("n", "skip the first match", "Confirm?")
    run.step(F1, "cancel the rest", "Æ A Æ")
    run.start_of_document()
    replace("n")
    run.wait("é A é")
    run.step(b"\x1b[1;3R", "check Reveal Codes", "[BOLD][UND]é A é[und][bold]")
    run.save("REPLACE.WP")
    assert native(run.p.work / "REPLACE.WP")[2] == native(reference)[2]
    run.exit_application()
except Exception as exc:
    run.finish(repr(exc), "Compose Replace")
    raise
else:
    run.finish(None, "Compose Replace")
