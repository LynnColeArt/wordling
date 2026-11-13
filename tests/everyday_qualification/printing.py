import sys
from pathlib import Path
from qualification import Run, ENTER, F6, F7, F8
repo, binary, root = map(Path, sys.argv[1:4])
case = sys.argv[4]
run = Run(repo.resolve(), binary.resolve(), root.resolve())
failure = None
try:
    run.launch()
    if case == "attrs":
        for k in ("A ", F6, "B", F8, "C", F6, "D", F8, " E  "):
            run.step(k, "type original styled input")
    elif case in ("pages","current"):
        run.step("One", "type first page")
        run.step(b"\x1b[13;5u", "hard page", "Pg 2")
        run.step("Two", "type second page")
    else:
        run.step("Hello print", "type first line")
        run.step(ENTER, "line break")
        run.step("Second line", "type second line")
    shift_f7=b"\x1b[18;2~"
    run.step(shift_f7, "open Print", "Full Document")
    if case == "pages":
        run.step("6", "view second page", "Page 2 of 2")
        run.wait("Two")
        run.step(b"\x1b[5~", "view first page", "Page 1 of 2")
        run.wait("One")
        run.step(F7, "exit view")
        run.step(shift_f7, "open Print again", "Full Document")
    for k, cue in [("s","Select Printer"),("3","STANPRIN.PRS"),("2","8 Other"),("8","Device or Filename"),("PRINT.PRN","PRINT.PRN"),(ENTER,"PRINT.PRN"),(F7,"Full Document")]:
        run.step(k,"configure disk port",cue)
    run.step("2" if case=="current" else "1", "print to disk")
    outfile=run.p.work/"PRINT.PRN"
    run.until(outfile.is_file, "print file exists")
    reference = repo / "docs/research/everyday-contract-2026-11-05/printing" / (case + ".PRN")
    assert outfile.read_bytes() == reference.read_bytes(), f"{case} printer bytes differ"
    run.exit_application()
except Exception as e:
    failure=repr(e)
    raise
finally:
    run.finish(failure,"Standard Printer "+case)
