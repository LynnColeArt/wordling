"""Run captured native macro programs through the Linux terminal and F10."""
import json
from pathlib import Path
import sys

from macro_recording import ALT_F10
from qualification import ENTER, Run, native, sha


CASES = {
    178, 205, 206, 210, 212, 213, 214, 215, 218, 219, 220, 221, 222,
    226, 227, 228, 229, 230,
}
LOADED_DOCUMENT_CASES = {210, 212, 213, 230}
EMPTY_NATIVE = "internal/document/evidence/wp46/candidates/empty.WP5"


def exercise(run, case, sources):
    directory = run.p.work / "OUT"
    directory.mkdir()
    staged = {}
    for source in sources:
        original = run.repo / source["path"]
        raw = original.read_bytes()
        assert sha(raw) == source["sha256"], original
        staged[directory / original.name] = raw
    for target, raw in staged.items():
        target.write_bytes(raw)
    assert directory / case["root_macro"] in staged

    result = case["native_results"][0]
    original_document = run.repo / result["path"]
    raw, _, expected = native(original_document)
    assert sha(raw) == result["sha256"], original_document
    assert expected == bytes.fromhex(case["expected"]["expected_hex"])

    needs_loaded = int(case["case_id"][-3:]) in LOADED_DOCUMENT_CASES
    if needs_loaded:
        template = run.repo / EMPTY_NATIVE
        assert native(template)[2] == b""
        run.seed(template, "EMPTY.WP")
    run.launch()
    if needs_loaded:
        run.set_fast_save(False)
        run.retrieve("EMPTY.WP")
        assert not any("Refused" in row for row in run.rows()), run.rows()
    if case.get("found"):
        run.step("ABSENT tail", "seed a real search match")
        run.start_of_document()
    run.step(ALT_F10, "open the native macro prompt", "Macro:")
    run.step("C:\\OUT\\" + Path(case["root_macro"]).stem, "select the original WPM")
    run.step(ENTER, "execute the original WPM")
    if case["case_id"] == "CMD51-178":
        run.wait("UnhandledCondition", timeout=10)
        assert any(row.strip() == "BEFORE" for row in run.rows())
        run.step("READY", "type after the failed search, as in the DOS capture")
    else:
        run.wait("Macro complete", timeout=10)
    if case.get("found"):
        run.step("X", "mark the macro's final cursor position")
    run.save("RESULT.WP", expected_offset=324)
    assert native(run.p.work / "RESULT.WP")[2] == expected
    assert {target: target.read_bytes() for target in staged} == staged
    run.exit_application()


def main(repo, binary, output):
    ledger = json.loads((repo / "internal/macro/runtime/testdata/original-cases.json").read_text())
    output.mkdir()
    selected = [case for case in ledger["macro_cases"] if int(case["case_id"][-3:]) in CASES]
    assert len(selected) == len(CASES)
    handler = next(case for case in selected if case["case_id"] == "CMD51-206")
    found_path = Path("docs/research/reference-runs/mission1-macro-search/FOUND.WP")
    found_sha = "7ad16a85bb81d5f6347e0121243dc17a5ba14ee871c04e7e59e063da0fd29c3e"
    selected.append({**handler, "found": True,
                     "native_results": [{"path": found_path, "sha256": found_sha}],
                     "expected": {"expected_hex": b"BEFOREABSENTSHOULDNOTX tail".hex()}})
    failures = []
    for case in selected:
        key = case["case_id"]
        sources = [source for source in ledger["wpm_exports"]
                   if source["case_id"] == key and source["run"] == case["run"]]
        label = key + "-found" if case.get("found") else key
        run = Run(repo, binary, output / label, classic_canvas=True)
        failure = None
        try:
            exercise(run, case, sources)
        except Exception as error:
            failure = repr(error)
        try:
            run.finish(failure, label)
        except Exception as error:
            failures.append(label)
            print(f"{label}: {error}", file=sys.stderr)
    print(f"Macro control: {len(selected) - len(failures)} of {len(selected)} passed", flush=True)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main(*(Path(arg).resolve() for arg in sys.argv[1:4])))
