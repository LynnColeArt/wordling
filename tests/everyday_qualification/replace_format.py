"""Compare removal and substitution of formatting codes with DOS native saves."""
from pathlib import Path
import sys

from qualification import F2, F6, F8, REF, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
output.mkdir()


def replace(run, query, replacement):
    run.start_of_document()
    run.step(b"\x1b[1;3Q", "open Replace", "w/Confirm?")
    run.step("n", "replace without confirmation", "Srch:")
    for key in query:
        run.step(key, "enter search owner")
    run.step(F2, "enter replacement", "Replace with:")
    for key in replacement:
        run.step(key, "enter replacement owner")
    run.step(F2, "apply replacement")


for case in ("remove", "span", "adjacent"):
    run = Run(repo, binary, output / case, classic_canvas=True)
    try:
        run.launch()
        if case == "remove":
            for key in ("AB", F6, "C", F6, F8, "D", F8):
                run.step(key, "type separately formatted text")
            replace(run, (F6, F6), ())
            replace(run, (F8, F8), ())
            run.step(b"\x1b[1;3R", "verify nonadjacent pairs survived", "AB[BOLD]C[bold][UND]D[und]")
            replace(run, (F6,), ())
            run.wait("ABC[UND]D[und]")
            run.save("BOLD.WP")
            reference = repo / REF / "replace-format-dos/exports/SINGLE.WP"
            assert native(run.p.work / "BOLD.WP")[2] == native(reference)[2]
            replace(run, (F8,), ())
            run.wait("ABCD")
            run.save("PLAIN.WP")
            plain = repo / REF / "replace-format-underline-dos/exports/PLAIN.WP"
            assert native(run.p.work / "PLAIN.WP")[2] == native(plain)[2]
        elif case == "adjacent":
            fixtures = repo / REF / "replace-adjacent-pairs-dos/exports"
            run.set_fast_save(False)
            run.seed(fixtures / "PAIRS.WP", "PAIRS.WP")
            run.retrieve("PAIRS.WP")
            run.step(b"\x1b[1;3R", "show adjacent codes", "AB[BOLD][bold][UND][und]CD")
            replace(run, (F6, F6), ())
            run.wait("AB[UND][und]CD")
            replace(run, (F8, F8), ())
            run.save("CLEAN.WP")
            assert native(run.p.work / "CLEAN.WP")[2] == native(fixtures / "CLEAN.WP")[2]
        else:
            for key in ("A", F6, "B", F6, "C"):
                run.step(key, "type Bold span")
            replace(run, (F6, "b", F6), (F8, "b", F8))
            run.step(b"\x1b[1;3R", "verify converted span", "A[UND]b[und]C")
            run.save("SPAN.WP")
            reference = repo / REF / "replace-format-span-dos/exports/SPAN.WP"
            assert native(run.p.work / "SPAN.WP")[2] == native(reference)[2]
        run.exit_application()
    except Exception as exc:
        run.finish(repr(exc), "Replace formatting codes")
        raise
    else:
        run.finish(None, "Replace formatting codes")
