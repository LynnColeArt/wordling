#!/usr/bin/env python3
"""Exercise native merge source saves and Ctrl+F9 over a real Linux PTY."""
import argparse
from pathlib import Path

from physical_cases import RIGHT, close_doc2, press
from qualification import ENTER, F1, F5, F11, SWITCH, Run, sha

MERGE = b"\x1b[20;5~"
FIXTURES = "docs/research/reference-runs/2026-10-29-extended-04/CMD51-134"
ORIGINAL = {
    False: (
        "105ba3c4c4efdb1e13c61cdf17863aa47a43b74a8699af6f89adedf9bbb03dd0",
        "b2081ccccb76fc850a25bbe21462d06963de54237259b009247be4074a47c866",
        "aad07eca0a3309080a888eaba0a2515b5176252112c1b9a568e16c879ffcec42",
    ),
    True: (
        "59ec19c2cd098c7f003c202d897d1da54236d0131a46b9c45750652940af24e8",
        "31de89dfb1d5e9b14e611e3b18fba36903175fbdd2fa26c2d78edf70ceffcac1",
        "645a17f07e67eee94cbb90dc3cf948ca75af0467784face2841c603654a02406",
    ),
}


def select(run, name):
    run.step(F5, "F5 in merge role", "Dir C:\\*.*", 24)
    run.step(ENTER, "list the scoped files", "Directory C:\\*.*", 0)
    run.step("n", "name search", "Name Search", 24)
    run.step(name, "find the exact merge file")
    run.step(ENTER, "select the located row")
    run.step("1", "retrieve this file into the current merge role")


def enter_primary(run):
    run.step(MERGE, "Ctrl+F9 Merge", "1 Merge; 2 Sort; 3 Convert Old Merge Codes: 0", 24)
    run.step("1", "open primary prompt", "Primary file:", 24)


def exercise(run, fast):
    fixtures = run.repo / FIXTURES
    expected = ORIGINAL[fast]
    offset = 564 if fast else 324
    for name in ("PRIMARY", "SECOND"):
        run.seed(fixtures / (name + ".WP5"), name + ".WP5")
    run.launch()
    if not fast:
        run.set_fast_save(False)
    for original, edited, key, word, label, digest in (
        ("PRIMARY", "PRI", "X", "Hello", "{FIELD}", expected[0]),
        ("SECOND", "SEC", "Z", "Alice", "{END FIELD}", expected[1]),
    ):
        run.step(SWITCH, "open fresh Doc 2", "Doc 2 Pg")
        run.retrieve(original + ".WP5")
        run.wait(word)
        run.step(F11, "show original merge owner in Reveal Codes")
        run.wait(label)
        run.step(F11, "close Reveal Codes")
        run.step(key, "edit the admitted literal only", key + word)
        data = run.save(edited + ".WP5", expected_offset=offset)
        assert sha(data) == digest, (edited, sha(data), digest)
        assert (run.p.work / (original + ".WP5")).read_bytes() == (fixtures / (original + ".WP5")).read_bytes()
        close_doc2(run)

    if not fast:
        run.step("BEFOREAFTER", "type occupied receiver", "BEFOREAFTER")
        run.start_of_document()
        press(run, *([RIGHT] * 6))
        enter_primary(run)
        run.step("MISSING.WP5", "use a missing primary")
        run.step(ENTER, "settle missing primary", "Primary file: MISSING.WP5")
        run.wait("ReadFailed")
        run.step(F1, "cancel after missing primary")
        run.wait("BEFOREAFTER")
        enter_primary(run)
        run.step(F5, "open primary List Files", "Dir C:\\*.*", 24)
        run.step(ENTER, "view primary List Files", "Directory C:\\*.*", 0)
        run.step(F1, "cancel list back to primary", "Primary file:", 24)
        run.step("PRI.WP5", "type qualified primary")
        run.step(ENTER, "advance to secondary by filename", "Secondary file:", 24)
        run.step(F1, "cancel from secondary without edits")
        run.wait("BEFOREAFTER")
        enter_primary(run)
        select(run, "PRI.WP5")
        run.wait("Secondary file:", 24)
        select(run, "SEC.WP5")
    else:
        enter_primary(run)
        run.step("PRI.WP5", "type edited primary")
        run.step(ENTER, "advance to secondary", "Secondary file:", 24)
        run.step("SEC.WP5", "type edited secondary")
        run.step(ENTER, "merge by typed secondary")
    run.wait("XHello ZAlice")
    run.wait("XHello Bob")
    assert sum(row == "=" * 80 for row in run.rows()) == 3
    if not fast:
        run.wait("BEFOREXHello ZAlice")
        run.wait("AFTER")
    data = run.save("MERGED.WP5", expected_offset=offset)
    assert sha(data) == expected[2], (sha(data), expected[2])
    run.step(SWITCH, "open another screen for native result reopen", "Doc 2 Pg")
    run.retrieve("MERGED.WP5")
    run.wait("XHello ZAlice")
    run.wait("XHello Bob")
    assert run.save("COPY.WP5", expected_offset=offset) == data
    close_doc2(run)
    run.exit_application()


def occupied_yes(run):
    fixtures = run.repo / FIXTURES
    for name in ("PRIMARY.WP5", "SECOND.WP5"):
        run.seed(fixtures / name, name)
    run.launch()
    run.step("BEFOREAFTER", "type occupied receiver", "BEFOREAFTER")
    run.start_of_document()
    press(run, *([RIGHT] * 6))
    enter_primary(run)
    run.step("PRIMARY.WP5", "type compact original primary")
    run.step(ENTER, "advance to secondary", "Secondary file:", 24)
    run.step("SECOND.WP5", "type original secondary")
    run.step(ENTER, "merge in occupied New")
    run.wait("BEFOREHello Alice")
    run.wait("AFTER")
    data = run.save("MERGED.WP5")
    assert sha(data) == "2f82538e41e144e7e752d7b95c2a816180c8667f7623c572ee93821a45fb5953"
    run.exit_application()


def occupied_loaded(run, fast):
    fixtures = run.repo / FIXTURES
    for name in ("PRIMARY.WP5", "SECOND.WP5"):
        run.seed(fixtures / name, name)
    run.seed(run.repo / "internal/document/testdata/fast_save_yes/SECOND.WP", "RECEIVER.WP5")
    run.launch()
    if not fast:
        run.set_fast_save(False)
    run.retrieve("RECEIVER.WP5")
    run.wait("Alpha beta")
    press(run, *([RIGHT] * 6))
    enter_primary(run)
    run.step("PRIMARY.WP5", "type compact original primary")
    run.step(ENTER, "advance to secondary", "Secondary file:", 24)
    run.step("SECOND.WP5", "type original secondary")
    run.step(ENTER, "merge in acquired receiver")
    run.wait("Alpha Hello Alice")
    run.wait("beta")
    data = run.save("MERGED.WP5", expected_offset=564 if fast else 324)
    want = ("4a90d3781f5f34df7a10887c43fb1417b0537c0f15a4eb2087353ed7aab95065"
            if fast else "7ea4a607f18c599d59cdf8deb31e3c47882e5664dc890d550997f8da7ef9236d")
    assert sha(data) == want, (sha(data), want)
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("setting", choices=("yes", "no", "yes-occupied", "yes-loaded", "no-loaded"))
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be fresh")
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        if args.setting == "yes-occupied":
            occupied_yes(run)
        elif args.setting.endswith("-loaded"):
            occupied_loaded(run, args.setting == "yes-loaded")
        else:
            exercise(run, args.setting == "yes")
    except Exception as error:
        failure = repr(error)
    finally:
        run.finish(failure, "native merge with Fast Save " + args.setting)


if __name__ == "__main__":
    main()
