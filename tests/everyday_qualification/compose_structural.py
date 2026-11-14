"""Compare composed table and merge source edits to WP 5.1 DOS saves."""
from pathlib import Path
import sys

from qualification import ENTER, F7, REF, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
output.mkdir()
for role in ("table", "merge", "primary", "table-wrap"):
    run = Run(repo, binary, output / role, classic_canvas=True)
    try:
        if role.startswith("table"):
            run.launch()
            for key, cue in ((b"\x1b[18;3~", "2 Tables"), ("2", "1 Create"), ("1", "Number of Columns"), ("2", None), (ENTER, "Number of Rows"), ("2", None), (ENTER, "1 Size"), (F7, "Cell A1")):
                run.step(key, "create default table", cue)
        elif role == "merge":
            run.launch()
            run.step("X", "first secondary field")
            run.step(b"\x1b[20~", "insert End Field")
            run.step("Y", "second secondary field")
        else:
            run.launch()
            run.step("P", "type primary literal")
            run.step(b"\x1b[20;2~", "open merge codes")
            run.step("1", "select Field")
            run.step("1", "enter field number")
            run.step(ENTER, "insert Field 1")
            run.start_of_document()
            run.step(b"\x1b[C", "move before the Field owner")
        if role == "table-wrap":
            run.step("A" * 29, "fill the line to its last text column")
        run.step(b"\x16", "start Compose", "Key =")
        run.step("1,36", "enter the native character identity")
        run.step(b"\r", "insert the glyph", "Æ")
        if role == "table-wrap":
            run.step("Z", "type through the cell boundary")
        else:
            run.step(b"\x1b[1;3R", "open Reveal Codes")
            run.step(b"\x1b[D", "select the extended owner", "[Æ:1,36]")
            prefix = {"table": "[Row][Cell]", "merge": "Y", "primary": "P"}[role]
            run.wait(prefix + "[Æ:1,36]")
        run.save("COMPOSE.WP")
        name = "WRAP.WP" if role == "table-wrap" else "COMPOSE.WP"
        reference = repo / REF / f"compose-{role}-reference/exports" / name
        assert native(run.p.work / "COMPOSE.WP")[2] == native(reference)[2]
        run.exit_application()
    except Exception as exc:
        run.finish(repr(exc), role + " Compose")
        raise
    else:
        run.finish(None, role + " Compose")
