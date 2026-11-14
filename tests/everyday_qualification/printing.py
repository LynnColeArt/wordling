import sys
from pathlib import Path
from qualification import Run, ENTER, F2, F6, F7, F8, REF
repo, binary, root = map(Path, sys.argv[1:4])
case = sys.argv[4]
run = Run(repo.resolve(), binary.resolve(), root.resolve())
failure = None
try:
    run.launch()
    if case in ("compose", "compose-trailing"):
        def compose(identity):
            run.step(b"\x16", "start Compose")
            run.step(identity, "enter character identity")
            run.step(ENTER, "insert character")

        run.step("X", "type leading ASCII")
        if case == "compose":
            run.step(F6, "start Bold")
            run.step(F8, "start Underline")
            for identity in ("1,36", "1,41", "4,23", "6,1"):
                compose(identity)
            run.step(F6, "end Bold")
            run.step(F8, "end Underline")
            run.step("Z", "type following ASCII")
        else:
            compose("1,36")
            run.step(ENTER, "end first line")
            run.step(F6, "start Bold")
            compose("1,41")
            run.step(F6, "end Bold")
            run.step(ENTER, "end second line")
            compose("4,23")
        run.start_of_document()
        run.step(F2, "open Search")
        compose("1,36")
        run.wait("Srch: Æ")
        run.step(b"\x7f", "delete one complete query character")
        assert "Srch: Æ" not in "\n".join(run.rows())
        compose("1,36")
        run.step(F2, "find the native character", 'Pos 1.2"')
    elif case == "literal":
        for key in ("Before", b"\x1b[19;2~", "4", "6", "2", "1", "<36>TEST", ENTER, F7, "After"):
            run.step(key, "insert a literal printer command between two words")
        run.wait("BeforeAfter")
        reference_native = repo / "docs/research/reference-runs/mission1-printer-command/PRTCMD.WP"
        saved = run.save("PRTCMD.WP")
        want = reference_native.read_bytes()
        assert saved[int.from_bytes(saved[4:8], "little"):] == want[int.from_bytes(want[4:8], "little"):]
    elif case == "attrs":
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
    if case == "compose":
        reference = repo / REF / "compose-standard-print/exports/COMPOSE.PRN"
    elif case == "compose-trailing":
        reference = repo / REF / "compose-standard-trailing/exports/TRAIL.PRN"
    elif case == "literal":
        reference = repo / "docs/research/reference-runs/mission1-printer-command/PRTCMD.PRN"
    assert outfile.read_bytes() == reference.read_bytes(), f"{case} printer bytes differ"
    run.exit_application()
except Exception as e:
    failure=repr(e)
    raise
finally:
    run.finish(failure,"Standard Printer "+case)
