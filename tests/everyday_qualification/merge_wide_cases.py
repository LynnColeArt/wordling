#!/usr/bin/env python3
"""Qualify wide data, wrapper programs, and archived F10 results over a Linux PTY."""
import argparse
from pathlib import Path

from merge_cases import enter_primary
from physical_cases import RIGHT, close_doc2, press
from qualification import ENTER, SWITCH, Run, sha

EVIDENCE = "docs/research/everyday-contract-2026-11-05/native-merge/wide"
BASELINE = "docs/research/reference-runs/2026-10-29-iteration-01/CMD51-223"
CUES = {
    "3": "3=[B3]", "12": "12=[B12]", "32": "32=[B32]", "53": "53=[B53]",
    "54": "54=[B54]", "60": "60=[B60]",
    "bounds": "65536=[Bob]", "bounds2": "MISSING",
    "nestedmissing": "HEAD=B1",
    "ifmissingone": "TAIL=Bob", "ifmissingwide": "TAIL=B1", "ifzero": "TAIL=Bob",
    "ifpresent": "TAIL=B1", "direct2": "WRAP=B2",
    "missingend": "MISSING", "missingliteral": "TAIL", "presentend": "HEAD=B1", "field2tail": "TAIL=B1", "literal": "LITERAL ONLY",
    "literal-page": "LITERAL ONLY", "wrapper": "CBob", "wrapper1": "CBob",
    "wrapper3": "CBob", "wrapperlead": "CBob", "wrapperno": "CBob",
    "wrapperocc": "CBob", "wrapper-literal": "LITERAL ONLY",
    "reorderedno": "CBob", "reorderedocc": "CBob", "wrapperflags": "CBob",
}


def verify(run, path, name):
    expected = path.read_bytes()
    offset = int.from_bytes(expected[4:8], "little")
    actual = run.save(name, expected_offset=offset)
    assert actual == expected, (sha(actual), sha(expected))


def exercise(run, case):
    fresh = run.repo / EVIDENCE
    baseline = run.repo / BASELINE
    fixture = fresh / case
    source = fresh / "wrapper" if case in ("wrapperno", "wrapperocc", "reorderedno", "reorderedocc", "reopen-yes", "reopen-no") else fixture
    secondary = source / "SECOND.WP5" if case.isdecimal() or case == "nestedmissing" else baseline / "SECOND.WP5"
    if case in ("bounds2", "ifmissingwide", "ifpresent", "direct2", "missingend", "missingliteral", "presentend", "field2tail"):
        secondary = fresh / "3" / "SECOND.WP5"
    seeds = {
        "OUT/PRIMARY.WP5": source / "PRIMARY.WP5",
        "OUT/SECOND.WP5": secondary,
    }
    if case == "nestedmissing":
        seeds["OUT/CHILD"] = run.repo / "docs/research/reference-runs/2026-10-30-values-01/CMD51-234/CHILD.WP5"
    if case.startswith(("wrapper", "reopen", "reordered")):
        leaf = "OUT/SUB/CHILD" if case == "wrapper-literal" else "OUT/CHILD"
        seeds[leaf] = baseline / "CHILD.WP5"
        if case.startswith("reordered"):
            seeds[leaf] = fresh / "reorderedno" / "CHILD.WP5"
        elif case in ("wrapper-literal", "wrapperflags"):
            seeds[leaf] = source / "CHILD.WP5"
        if case != "wrapper1":
            seeds["OUT/WRAP"] = source / "WRAP.WP5" if (source / "WRAP.WP5").exists() else fresh / "wrapper" / "WRAP.WP5"
        if case == "wrapper3":
            seeds["OUT/MID"] = source / "MID.WP5"
    (run.p.work / "OUT" / "SUB").mkdir(parents=True)
    for destination, original in seeds.items():
        run.seed(original, destination)
    run.launch()
    if case in ("wrapperno", "reorderedno"):
        run.set_fast_save(False)
    if case in ("wrapperocc", "reorderedocc"):
        run.step("BEFOREAFTER", "type occupied receiver", "BEFOREAFTER")
        run.start_of_document()
        press(run, *([RIGHT] * 6))
    enter_primary(run)
    run.step(r"C:\OUT\PRIMARY.WP5", "type the exact original primary")
    run.step(ENTER, "accept the primary", "Secondary file:", 24)
    run.step(r"C:\OUT\SECOND.WP5", "type the exact original secondary")
    run.step(ENTER, "run the merge", CUES.get(case, "CBob"))
    if case == "nestedmissing":
        run.wait("HEAD=Carol")
        assert not any("HEAD=Dave" in row for row in run.rows())
    original_result = source / "MERGED.WP5" if case.startswith("reopen-") else fixture / "MERGED.WP5"
    verify(run, original_result, "MERGED.WP5")
    if case == "wrapper":
        run.start_of_document()
        run.step("X", "edit wrapper result in its original session", "XCAlice")
        verify(run, fixture / "EDITED.WP5", "SAME.WP5")
    if case.startswith("reopen-"):
        run.step(SWITCH, "switch to Doc 2", "Doc 2 Pg")
        run.retrieve("MERGED.WP5")
        run.wait("CAlice")
        verify(run, original_result, "COPY.WP5")
        if case == "reopen-no":
            run.set_fast_save(False)
        run.step("X", "edit the result after actual retrieval", "XCAlice")
        verify(run, fixture / "EDITED.WP5", "EDITED.WP5")
        close_doc2(run)
    for destination, original in seeds.items():
        assert (run.p.work / destination).read_bytes() == original.read_bytes(), destination
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("case", choices=(*CUES, "reopen-yes", "reopen-no"))
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        exercise(run, args.case)
    except Exception as error:
        failure = repr(error)
    finally:
        run.finish(failure, "native wide merge " + args.case)


if __name__ == "__main__":
    main()
