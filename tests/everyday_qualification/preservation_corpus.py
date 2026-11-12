#!/usr/bin/env python3
"""Probe actual native corpus admission and no-edit save through cmd/wordling."""
import argparse
import hashlib
import json
from pathlib import Path

from qualification import Run, RETRIEVE, F1, F10, ENTER, native_info


def exercise(repo, binary, output, fixture):
    source = repo / fixture["path"]
    raw = source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == fixture["sha256"], fixture["id"]
    run = Run(repo, binary, output)
    failure = None
    verdict = "unverified"
    try:
        run.seed(source, "SOURCE.WP")
        run.launch()
        run.step(RETRIEVE, "ordinary native document Retrieve", "Document to be retrieved:")
        run.step("SOURCE.WP", "enter recorded original fixture")
        run.step(ENTER, "settle original fixture acquisition")
        def settled():
            rows = run.rows()
            modal = "Document to be retrieved:" in rows[24]
            return not modal or bool(rows[23].strip())
        run.until(settled, "fixture acquisition applied or visibly refused")
        if "Document to be retrieved:" in run.rows()[24]:
            verdict = "explicit refusal"
            run.capture("original fixture refused by editor")
            assert "refus" in run.rows()[23].lower() or "unsupported" in run.rows()[23].lower(), run.rows()[23]
            run.step(F1, "cancel refused acquisition")
            run.step("CONTROL", "ordinary typing resumes", "CONTROL")
            run.save("CONTROL.WP", body_fragment=b"CONTROL")
        else:
            run.step(F10, "F10 on unmodified original source", "Document to be saved:")
            run.step(ENTER, "accept unchanged source name", "Replace SOURCE.WP? No (Yes)")
            run.step("y", "confirm same-source no-edit save", "Doc 1 Pg")
            assert (run.p.work / "SOURCE.WP").read_bytes() == raw, "same-source no-edit bytes changed"
            copied = run.save("COPY.WP", expected_offset=fixture["body_offset"])
            assert copied == raw, "no-edit native Save As bytes changed"
            verdict = "exact same-source and Save As"
            if fixture["id"] == "paired":
                run.step(b"\x1b[C", "place caret adjacent to original BoldOn")
                run.step("SAFE", "edit a supported span beside original pair")
                edited = run.save("EDITED.WP")
                offset = fixture["body_offset"]
                expected = bytearray(raw[:offset] + raw[offset:offset+1] + b"SAFE" + raw[offset+1:])
                expected[256] |= 0x08
                assert edited == expected, "adjacent edit changed unrelated native bytes"
                verdict += " plus exact adjacent native edit"
        assert (run.p.work / "SOURCE.WP").read_bytes() == raw
        run.exit_application()
    except Exception as err:
        failure = repr(err)
    finally:
        evidence = {"fixture": fixture["id"], "source": str(source), "original": native_info(source),
                    "editor_observation": verdict, "failure": failure}
        (output / "corpus-observation.json").write_text(json.dumps(evidence, indent=2) + "\n")
        run.finish(failure, "EE-A13 / " + fixture["id"])
    return evidence


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("binary", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    repo, binary, output = (x.resolve() for x in (a.repo, a.binary, a.output))
    output.mkdir()
    manifest = repo / "kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json"
    fixtures = json.loads(manifest.read_text())["fixtures"]
    results = []
    for fixture in fixtures:
        # The native macro binary is a separate resource type and is not a
        # document. Record that scope rather than calling it a passed save.
        if fixture["id"] == "macro":
            results.append({"fixture": fixture["id"], "editor_observation": "separate native macro resource"})
            continue
        try:
            results.append(exercise(repo, binary, output / fixture["id"], fixture))
        except AssertionError as err:
            results.append({"fixture": fixture["id"], "editor_observation": "failed", "failure": repr(err)})
    (output / "corpus.json").write_text(json.dumps(results, indent=2) + "\n")
    return 1 if any(row.get("failure") for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
